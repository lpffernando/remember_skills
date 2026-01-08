# Usage Examples

## Basic Operations

### Add Memory
```bash
# Add to specific layer
python memory.py --add "我偏好TDD开发方式" -l core --tags "开发 习惯 TDD"

# Add with auto-detection
python memory.py --add "城市更新的核心逻辑是..." -l cognitive
```

### Retrieve Memory
```bash
# Search memories
python memory.py --search "城市更新"

# List layer contents
python memory.py --list -l cognitive
```

### Manage Memory
```bash
# Delete specific memory
python memory.py --delete "memory_key" -l cognitive

# Delete all memories
python memory.py --delete-all
```

## Workflow Examples

### Storing Document Knowledge
1. LLM uses `pdf`/`docx`/`pptx` skill to read document
2. LLM summarizes key concepts
3. Add to appropriate layer with tags:
```bash
python memory.py --add "关键概念..." -l cognitive --tags "文档 主题"
```

### Building Long-term Memory
1. Identify core values/preferences → Core layer
2. Add technical knowledge → Cognitive layer
3. Record work patterns → Behavioral layer

### Managing Project Context
1. Add project docs → Contextual layer
2. Track progress → State layer
3. Cleanup on project end → Forget
