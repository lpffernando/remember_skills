# Remember API Reference

## Core Operations

### Add Memory
```bash
python memory.py --add "content" [-l layer] [--tags tag1 tag2] [--source path]
```

### Index Memory (add tags)
```bash
python memory.py --index "key" --tags "tag1" "tag2" [-l layer]
```

### Update Memory
```bash
python memory.py --update "key" --content "new content" [-l layer]
```

### Retrieve Memories
```bash
# Get specific memory
python memory.py --get "key" [-l layer]

# Search memories
python memory.py --search "query"

# List all memories
python memory.py --list

# List by layer
python memory.py --list -l cognitive
```

### Delete Memories
```bash
# Delete specific memory
python memory.py --delete "key" [-l layer]

# Delete all memories
python memory.py --delete-all
```

### Process Files
```bash
# Process single file
python memory.py --process "file.pptx" [-l layer]

# Process multiple files
python memory.py --batch "file1.pptx file2.pdf"
```

## JSON Structure

```json
{
  "layer_name": {
    "memory_id": {
      "content": "memory content",
      "layer": "layer_name",
      "tags": ["tag1", "tag2"],
      "source": "file/path or description",
      "created": "2026-01-08T10:00:00.000000",
      "updated": "2026-01-08T10:00:00.000000",
      "accessed": 0
    }
  }
}
```

## Memory Layers

| Layer | Capacity | Use Case |
|-------|----------|----------|
| core | 20 | Identity, values, long-term goals |
| cognitive | 100 | Knowledge, concepts, professional skills |
| behavioral | 100 | Habits, preferences, work patterns |
| contextual | 200 | Project background, task context |
| state | 500 | Temporary todos, progress tracking |

## Usage Examples

### Example 1: Store project information
```bash
python memory.py --add "User prefers TDD development approach" -l behavioral
```

### Example 2: Add tags to existing memory
```bash
python memory.py --index "mem_20260108_001" --tags "important" "project-x" -l cognitive
```

### Example 3: Update memory content
```bash
python memory.py --update "mem_20260108_001" \
  --content "Updated: User now prefers BDD over TDD for integration tests" \
  -l behavioral
```

### Example 4: Process a presentation
```bash
python memory.py --process "ProjectReport.pptx" -l cognitive
```

### Example 5: Search memories
```bash
python memory.py --search "testing methodology"
```
