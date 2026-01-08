---
name: remember
description: Multi-layer global memory system for AI agents. Store/retrieve knowledge across sessions. Use when user wants to remember info, process documents into memories, or search past conversations.
---

# Multi-Layer Memory System

## Quick Start

```bash
# Add memory
/remember --add "重要信息"

# Search
/remember --search "关键词"

# Process file → 1-10 memories
/remember --process "文件.pptx"

# List all
/remember --list
```

## Core Layers

| Layer | Use For | Stability |
|-------|---------|-----------|
| core | Identity, values, long-term goals | Stable |
| cognitive | Knowledge, concepts, expertise | Stable |
| behavioral | Habits, preferences, workflows | Evolving |
| contextual | Project context, tasks | Dynamic |
| state | Temporary notes, progress | Volatile |

## Commands

| Command | Description |
|---------|-------------|
| `--add "content"` | Store memory |
| `--search "query"` | Search memories |
| `--process "file"` | Convert file to memories |
| `--list` | List all layers |
| `--get "key"` | Get single memory |
| `--delete "key"` | Delete memory |
| `--delete-all` | Clear all |

## Detailed References

### Memory Layers
- Capacity, selection guide, use cases
- See [layers.md](references/layers.md)

### 6 Memory Operations
- Consolidation, Indexing, Updating, Forgetting, Retrieval, Compression
- See [operations.md](references/operations.md)

### Routing & Batch Processing
- Content routing rules, batch workflow, cross-links
- See [ROUTING.md](references/ROUTING.md)

### Usage Examples
- Workflow patterns, document storage, long-term memory building
- See [examples.md](references/examples.md)

## Storage

Default: `~/.claude/memory/memories.json`
Override: `export CLAUDE_MEMORY_DIR="/path"`

## Trigger Keywords

memory, remember, recall, store, forget, core, cognitive, behavioral, contextual, state, layer, consolidate, compress, 记住, 记忆, 遗忘, 文档, process, 文件
