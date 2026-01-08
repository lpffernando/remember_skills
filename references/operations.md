# 6 Memory Operations

## 1. Consolidation (固化)

Store content in memory with automatic routing and indexing.

**Command:**
```bash
python memory.py --add "content" -l cognitive --tags "tag1 tag2"
```

**LLM Processing:**
- Extract key concepts and keywords
- Generate summary
- Identify document type
- Route to appropriate layer

## 2. Indexing (索引)

Add tags and build associations for existing memories.

**Command:**
```bash
python memory.py --index "memory_key" --tags "tag1 tag2 tag3"
```

**LLM Processing:**
- Suggest related tags
- Build semantic associations
- Update search index

## 3. Updating (更新)

Update existing memory content while preserving metadata.

**Command:**
```bash
python memory.py --update "memory_key" -v "new content"
```

**LLM Processing:**
- Merge changes intelligently
- Preserve important metadata
- Reset activity score

## 4. Forgetting (遗忘)

Remove or compress low-activity memories.

**Command:**
```bash
python memory.py --forget --layer cognitive
python memory.py --forget --compress-low
```

**Strategies:**
- **Compress**: Keep summary, discard full content
- **Evict**: Remove entirely when layer is full
- **Preserve**: High-activity memories stay

## 5. Retrieval (检索)

Search and retrieve memories with relevance ranking.

**Command:**
```bash
python memory.py --search "query"
```

**LLM Processing:**
- Semantic matching across layers
- Relevance scoring
- Activity-weighted ranking

## 6. Compression (压缩)

Generate concise summaries of long memories.

**Command:**
```bash
python memory.py --compress "memory_key"
```

**LLM Processing:**
- Extract key points
- Generate summary
- Preserve original (reversible)
