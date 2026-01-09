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
| `--add "content"` | Store new memory |
| `--index "key"` | Add tags to memory |
| `--update "key"` | Update memory content |
| `--search "query"` | Search memories |
| `--process "file"` | Convert file to memories |
| `--list` | List all layers |
| `--get "key"` | Get single memory |
| `--delete "key"` | Delete memory |
| `--delete-all` | Clear all |

## Detailed References

See [references/api.md](references/api.md) for complete API documentation, advanced usage, and examples.

## Storage

Default: `~/.claude/memory/memories.json`
Override: `export CLAUDE_MEMORY_DIR="/path"`

## Trigger Keywords

memory, remember, recall, store, forget, core, cognitive, behavioral, contextual, state, layer, consolidate, compress, 记住, 记忆, 遗忘, 文档, process, 文件
