#!/usr/bin/env python3
"""
Multi-Layer Memory System - Minimal Wrapper

This is a thin wrapper that delegates to skills and LLM.
Core processing done by:
  - markitdown (for file reading: pptx, pdf, docx, etc.)
  - LLM (for summarization, routing, indexing)
  - JSON storage (for persistence)

Full capabilities: See SKILL.md
"""

import argparse
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
import shutil
import sys
import numpy as np

try:
    from sentence_transformers import SentenceTransformer, util
    # Using Qwen2.5/Qwen3 series for better multilingual performance
    # Note: Qwen/Qwen3-Embedding-0.6B is a great balance of size and performance
    print("[Init] Loading Qwen3 embedding model... (This may take a while first time)")
    model = SentenceTransformer('Qwen/Qwen3-Embedding-0.6B', trust_remote_code=True)
    HAS_SEMANTIC = True
except ImportError:
    HAS_SEMANTIC = False
    model = None
    print("[Warning] sentence-transformers not found or model failed. Semantic search disabled.")
except Exception as e:
    HAS_SEMANTIC = False
    model = None
    print(f"[Warning] Failed to load embedding model: {e}")


# Config
MEMORY_DIR = Path(os.environ.get("CLAUDE_MEMORY_DIR",
    os.path.expanduser("~/.claude/memory")))
MEMORY_FILE = MEMORY_DIR / "memories.json"
INDEX_FILE = MEMORY_DIR / "index.json"


# ==================== LIGHTWEIGHT STORAGE ====================
def ensure_dir():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def load_memories() -> dict:
    ensure_dir()
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"[Error] Corrupted memory file: {MEMORY_FILE}")
            # Backup corrupted file
            backup_path = str(MEMORY_FILE) + ".bak"
            try:
                shutil.copy(MEMORY_FILE, backup_path)
                print(f"[Error] Backed up to {backup_path}")
            except Exception as e:
                print(f"[Error] Could not backup: {e}")
            
            print("[Error] Exiting to prevent data loss. Please fix the file manually.")
            sys.exit(1)
        except Exception as e:
            print(f"[Error] Failed to load memory file: {e}")
            return {}
    return {}


def save_memories(memories: dict):
    ensure_dir()
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memories, f, ensure_ascii=False, indent=2)


# ==================== SIMPLE OPERATIONS ====================
def add_memory(content: str, layer: str, key: str = None, tags: list = None, source: str = None):
    """Add memory to layer (delegates to LLM for processing)."""
    memories = load_memories()
    if layer not in memories:
        memories[layer] = {}

    # 生成唯一 key，避免同一分钟内多次调用覆盖
    base_key = f"mem_{datetime.now().strftime('%m%d_%H%M')}"
    if key is None:
        # 加纳秒后缀确保唯一性
        key = f"{base_key}_{datetime.now().strftime('%S%f')}"
    # 如果 key 已存在，自动加后缀
    while key in memories[layer]:
        key = f"{key}_1"
    now = datetime.now().isoformat()

    memories[layer][key] = {
        "content": content,
        "layer": layer,
        "tags": tags or [],
        "source": source or "",
        "created": now,
        "updated": now,
        "accessed": 0,
    }

    if HAS_SEMANTIC:
        try:
            embedding = model.encode(content).tolist()
            memories[layer][key]["embedding"] = embedding
        except Exception as e:
            print(f"[Warning] Failed to generate embedding: {e}")


    save_memories(memories)
    print(f"[{layer[:3].upper()}] {key}")


def get_memory(key: str = None, layer: str = None) -> dict:
    """Get memory."""
    memories = load_memories()
    
    if not layer and key:
        # Search all layers for key
        for l, items in memories.items():
            if key in items:
                layer = l
                break
    
    if layer and key and layer in memories and key in memories[layer]:
        memories[layer][key]["accessed"] += 1
        save_memories(memories)
        return memories[layer][key]
    return {}


def list_memories(layer: str = None):
    """List memories."""
    memories = load_memories()
    if layer:
        items = memories.get(layer, {})
        print(f"\n[{layer.upper()}] {len(items)} items")
        for k, v in items.items():
            print(f"  - {k}: {v.get('content','')[:50]}...")
    else:
        print("\n" + "=" * 50)
        print("    MEMORY SYSTEM")
        print("=" * 50)
        for layer, items in memories.items():
            print(f"  {layer:12} | {len(items):3} items")
        print("=" * 50)


def search_memories(query: str, top_k: int = 5):
    """Search memories (Hybrid: Semantic + Keyword)."""
    memories = load_memories()
    results = []
    
    # 1. Semantic Search
    # 1. Semantic Search
    if HAS_SEMANTIC:
        # Encode query to tensor directly
        query_embedding = model.encode(query, convert_to_tensor=True)
        candidates = []
        
        for layer, items in memories.items():
            for key, data in items.items():
                if "embedding" in data:
                    try:
                        # Convert stored list to tensor, ensuring float32 to match query
                        stored_emb = model.tokenizer.backend_tokenizer.normalizer = None # Hack for some models, but safe here
                        # Actually just util.cos_sim handles tensors well
                        emb_tensor = util.cos_sim(query_embedding, data["embedding"])
                        score = emb_tensor.item()
                        candidates.append((score, layer, key, data))
                    except Exception as e:
                         # Fallback if dimension mismatch
                        pass
                elif query.lower() in data.get("content", "").lower():
                    # Fallback for old memories without embeddings
                    candidates.append((0.5, layer, key, data))
        
        # Sort by score descending
        candidates.sort(key=lambda x: x[0], reverse=True)
        results = [(c[1], c[2], c[3]) for c in candidates]
        
        print(f"\n[Search] '{query}' (Semantic): {len(results)} results")
        for i, (score, layer, key, data) in enumerate(candidates[:top_k], 1):
            print(f"  {i}. [{layer}] {key} (Score: {score:.2f})")
            print(f"     {data.get('content','')[:80]}...")
            
    # 2. Keyword Fallback
    else:
        query_lower = query.lower()
        for layer, items in memories.items():
            for key, data in items.items():
                content = data.get("content", "").lower()
                if query_lower in content or query_lower in key.lower():
                    results.append((layer, key, data))

        print(f"\n[Search] '{query}' (Keyword): {len(results)} results")
        for i, (layer, key, data) in enumerate(results[:top_k], 1):
            print(f"  {i}. [{layer}] {key}")
            print(f"     {data.get('content','')[:80]}...")


def delete_memory(key: str = None, layer: str = None, remove_all: bool = False):
    """Delete memories."""
    memories = load_memories()

    if remove_all:
        confirm = input("DELETE ALL? Type 'yes': ")
        if confirm != "yes":
            print("Cancelled")
            return
        save_memories({})
        print("[Delete] All memories deleted")
        return

    if not layer:
        # Try to find key in any layer
        found_layers = []
        for l, items in memories.items():
            if key in items:
                found_layers.append(l)
        
        if not found_layers:
            print(f"[Delete] Memory '{key}' not found in any layer")
            return
            
        if len(found_layers) > 1:
            print(f"[Delete] Ambiguous key '{key}' found in layers: {found_layers}. Please specify -l layer.")
            return
            
        layer = found_layers[0]

    if layer in memories and key in memories[layer]:
        del memories[layer][key]
        save_memories(memories)
        print(f"[Delete] {key} (from {layer})")
    else:
        print(f"[Delete] Memory '{key}' not found in layer '{layer}'")


# ==================== INDEXING & UPDATING ====================
def index_memory(key: str, layer: str, tags: list):
    """Add tags to existing memory."""
    memories = load_memories()

    if layer not in memories:
        print(f"[Error] Layer '{layer}' not found")
        return

    if key not in memories[layer]:
        print(f"[Error] Memory '{key}' not found")
        return

    memory = memories[layer][key]
    existing = set(memory.get("tags", []))
    new_tags = set(tags)
    memory["tags"] = list(existing | new_tags)
    memory["updated"] = datetime.now().isoformat()
    memory["accessed"] = memory.get("accessed", 0) + 1

    save_memories(memories)
    print(f"[Index] {key}: added {len(new_tags)} tags")


def update_memory(key: str, layer: str, new_content: str):
    """Update memory content."""
    memories = load_memories()

    if layer not in memories:
        print(f"[Error] Layer '{layer}' not found")
        return

    if key not in memories[layer]:
        print(f"[Error] Memory '{key}' not found")
        return

    if len(new_content.strip()) < 20:
        print("[Error] Content too short (<20 chars)")
        return

    memory = memories[layer][key]
    memory["content"] = new_content
    memory["updated"] = datetime.now().isoformat()
    memory["accessed"] = 0

    save_memories(memories)
    print(f"[Update] {key}: content updated")


    save_memories(memories)
    print(f"[Update] {key}: content updated")


def reindex_memories():
    """Backfill embeddings for all memories."""
    if not HAS_SEMANTIC:
        print("[Error] sentence-transformers not installed. Cannot reindex.")
        return

    memories = load_memories()
    count = 0
    total = 0
    
    print("[Reindex] Generating embeddings for existing memories...")
    for layer, items in memories.items():
        for key, data in items.items():
            total += 1
            if "content" in data and data["content"].strip():
                try:
                    # Always regenerate to ensure latest model compatibility
                    embedding = model.encode(data["content"]).tolist()
                    data["embedding"] = embedding
                    count += 1
                    if count % 10 == 0:
                        print(f"  Processed {count} items...", end='\r')
                except Exception as e:
                    print(f"  [Error] Failed to encode {key}: {e}")
                    
    save_memories(memories)
    print(f"\n[Reindex] Complete. Updated {count}/{total} memories.")
def analyze_content_richness(content: str) -> int:
    """
    Analyze content richness and return a score from 1-10.
    Factors considered:
    - Character count
    - Number of paragraphs
    - Number of bullet points/lists
    - Number of distinct topics (headers)
    """
    if not content or not content.strip():
        return 1

    # Count paragraphs (non-empty lines)
    paragraphs = [p for p in content.split('\n') if p.strip()]
    para_count = len(paragraphs)

    # Count bullet points (lines starting with -, *, •, or numbered lists)
    bullet_pattern = r'^[\s]*[-*•\d]+\.?\s'
    bullet_count = len(re.findall(bullet_pattern, content, re.MULTILINE))

    # Count headers (lines that look like titles/headers)
    header_pattern = r'^#{1,6}\s|^[A-Z][^.!?\n]{5,60}$'
    header_count = len(re.findall(header_pattern, content, re.MULTILINE))

    # Count distinct concepts (look for key terms - nouns/capitalized words)
    concept_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
    concept_count = len(set(re.findall(concept_pattern, content)))

    # Character count (logarithmic scale contribution)
    char_count = len(content)
    char_score = min(10, char_count // 500)

    # Weighted scoring
    richness = (
        min(3, char_score) +
        min(2, para_count // 5) +
        min(2, bullet_count // 5) +
        min(2, header_count // 3) +
        min(1, concept_count // 20)
    )

    return max(1, min(10, richness))


def split_into_memories(content: str, min_memories: int = 1, max_memories: int = 10) -> list:
    """
    Split content into multiple independent memories based on structure.
    Returns a list of memory contents.
    """
    if not content or not content.strip():
        return []

    # Estimate number of memories based on richness
    richness = analyze_content_richness(content)
    estimated_count = max(min_memories, min(max_memories, richness))

    # Strategy 1: Split by headers (most common structure)
    header_pattern = r'(?=^#{1,6}\s|^[A-Z][^.!?\n]{5,60}$)'

    # Split by major sections (double newline + header or numbered sections)
    section_pattern = r'(?=\n\s*\n#{1,6}\s|\n\s*\d+\.\s|\n\s*[-•]\s*[-•\s])'

    # Alternative: split by numbered sections
    numbered_pattern = r'(?=\n\s*\d+\.\s|\n#{1,6}\s)'

    # Extract potential memory sections
    sections = []
    current_section = ""

    lines = content.split('\n')
    in_code_block = False

    for line in lines:
        # Handle code blocks
        if '```' in line:
            in_code_block = not in_code_block

        if not in_code_block:
            # Check for new section start
            is_new_section = (
                line.startswith('# ') or
                line.startswith('## ') or
                line.startswith('### ') or
                re.match(r'^\d+\.\s', line) or
                (line.strip() and not line.startswith(' ') and not line.startswith('\t'))
            )
            if is_new_section and current_section.strip():
                sections.append(current_section.strip())
                current_section = line
            else:
                current_section += '\n' + line
        else:
            current_section += '\n' + line

    if current_section.strip():
        sections.append(current_section.strip())

    # If we have good sections, use them
    if len(sections) >= 2:
        # Filter out very short sections
        meaningful_sections = [s for s in sections if len(s) > 50]
        if len(meaningful_sections) >= min_memories:
            return meaningful_sections[:max_memories]

    # Strategy 2: Split by paragraphs if content is long
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 30]

    if len(paragraphs) >= min_memories:
        # Group paragraphs into memories
        target_count = estimated_count
        paragraph_per_memory = max(1, len(paragraphs) // target_count)

        memories = []
        current_memory = ""

        for i, para in enumerate(paragraphs):
            current_memory += para + "\n\n"
            if (i + 1) % paragraph_per_memory == 0 or i == len(paragraphs) - 1:
                if current_memory.strip():
                    memories.append(current_memory.strip())
                current_memory = ""

        return memories[:max_memories]

    # Strategy 3: If content is short, return as single memory
    return [content.strip()] if len(content.strip()) > 20 else []


def extract_file_content(file_path: str) -> str:
    """
    Extract text content from file using markitdown.
    Supports: pptx, pdf, docx, xlsx, html, markdown, etc.
    """
    path = Path(file_path)
    if not path.exists():
        print(f"[Error] File not found: {file_path}")
        return None

    try:
        # Use markitdown for extraction
        result = subprocess.run(
            [sys.executable, "-m", "markitdown", str(path)],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            return result.stdout
        else:
            print(f"[Error] markitdown failed: {result.stderr}")
            return None

    except FileNotFoundError:
        print("[Error] markitdown not found. Install: pip install markitdown")
        return None
    except subprocess.TimeoutExpired:
        print(f"[Error] Timeout extracting: {file_path}")
        return None
    except Exception as e:
        print(f"[Error] Extraction failed: {e}")
        return None


def process_file(file_path: str, layer: str = "cognitive", min_memories: int = None, max_memories: int = 10):
    """
    Process a file and create multiple memories based on content richness.
    Automatically determines memory count (1-10) based on content analysis.
    """
    print(f"[Process] Reading: {file_path}")

    # Extract content
    content = extract_file_content(file_path)
    if not content:
        return 0

    # Analyze richness to determine memory count
    richness = analyze_content_richness(content)
    auto_min = max(1, richness - 2)
    auto_max = min(10, richness + 2)
    effective_min = min_memories if min_memories is not None else auto_min

    print(f"[Process] Content richness: {richness}/10, creating {effective_min}-{auto_max} memories")

    # Split into memories
    memories = split_into_memories(content, min_memories=effective_min, max_memories=max(10, auto_max))

    if not memories:
        print("[Process] No meaningful content extracted")
        return 0

    # Create memories
    file_stem = Path(file_path).stem
    created = 0

    for i, mem_content in enumerate(memories):
        # Store full content
        display_content = mem_content

        key = f"{file_stem}_{i+1:02d}"
        add_memory(display_content, layer, key=key, tags=[file_stem], source=file_path)
        created += 1

    print(f"[Process] Created {created} memories from {file_path}")
    return created


# ==================== MAIN ====================
def main():
    parser = argparse.ArgumentParser(
        description="Multi-Layer Memory System - Minimal Wrapper",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
OPERATIONS:
  --add "content" -l layer    Add memory
  --get "key" -l layer        Get memory
  --list                      List memories
  --search "query"            Search memories
  --delete "key" -l layer     Delete memory
  --delete-all                Delete all
  --process "file"            Process file → 1-10 memories

LAYERS:
  core, cognitive, behavioral, contextual, state

Full docs: See SKILL.md
        """
    )

    parser.add_argument("--add", nargs=argparse.REMAINDER, help="Add memory")
    parser.add_argument("--get", metavar="KEY", help="Get memory")
    parser.add_argument("--list", action="store_true", help="List memories")
    parser.add_argument("--search", "-s", metavar="QUERY", help="Search memories")
    parser.add_argument("--delete", metavar="KEY", help="Delete memory")
    parser.add_argument("--delete-all", action="store_true", help="Delete all")
    parser.add_argument("--process", metavar="FILE", help="Process file and create 1-10 memories")
    parser.add_argument("-l", "--layer", choices=["core", "cognitive", "behavioral", "contextual", "state"])
    parser.add_argument("--tags", nargs="+", help="Tags for memory")
    parser.add_argument("--source", help="Source file/path")
    parser.add_argument("--min", type=int, help="Minimum memories to create (default: auto)")
    parser.add_argument("--max", type=int, default=10, help="Maximum memories to create (default: 10)")
    parser.add_argument("--batch", metavar="FILES", help="Process multiple files (space-separated)")
    parser.add_argument("--index", metavar="KEY", help="Index memory with tags")
    parser.add_argument("--update", metavar="KEY", help="Update memory content")
    parser.add_argument("--content", help="New content for update")
    parser.add_argument("--reindex", action="store_true", help="Regenerate embeddings for all memories")

    args = parser.parse_args()

    if args.add:
        add_memory(" ".join(args.add), args.layer or "cognitive", key=None, tags=args.tags, source=args.source)
    elif args.get:
        result = get_memory(args.get, args.layer)
        if result:
            print(result.get("content", ""))
        else:
            print("Not found")
    elif args.list:
        list_memories(args.layer)
    elif args.search:
        search_memories(args.search)
    elif args.delete:
        delete_memory(args.delete, args.layer)
    elif args.delete_all:
        delete_memory(remove_all=True)
    elif args.process:
        process_file(args.process, args.layer or "cognitive", args.min, args.max)
    elif args.batch:
        files = args.batch.split()
        total = 0
        for f in files:
            count = process_file(f, args.layer or "cognitive", args.min, args.max)
            total += count
        print(f"[Batch] Total: {total} memories from {len(files)} files")
    elif args.index:
        if not args.tags:
            print("[Error] --tags required for --index")
        else:
            index_memory(args.index, args.layer or "cognitive", args.tags)
    elif args.update:
        if not args.content:
            print("[Error] --content required for --update")
        else:
            update_memory(args.update, args.layer or "cognitive", args.content)
    elif args.reindex:
        reindex_memories()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
