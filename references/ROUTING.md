# Memory Routing & Batch Processing

Detailed rules for routing document content to appropriate memory layers.

## Routing Rules

| Content Pattern | Target Layer | Priority |
|-----------------|--------------|----------|
| Core principle/breakthrough/fundamental | core | 1 |
| Contact info/deadline/specification/data | cognitive | 1 |
| Process/steps/workflow/procedure | behavioral | 1 |
| Document structure/section hierarchy | contextual | 1 |
| Cross-document concept | contextual (with link) | 2 |
| Ambiguous content | LLM decides | - |

## Batch Processing Workflow

```
INPUT: One or multiple documents (PDF, DOCX, PPTX, MD)
OUTPUT: Multiple memories across layers

Steps:
1. Read all documents using pdf/docx/pptx skills
2. Extract document structure (sections, subsections, key points)
3. Apply routing rules to each content chunk
4. LLM reviews unclear items for intelligent routing
5. Create memories with layer, tags, source, section_path
6. Store to memories.json with full metadata
```

## Memory Structure

```json
{
  "memories": {
    "core": {
      "key": {
        "content": "Detailed content...",
        "layer": "core",
        "tags": ["tag1", "tag2"],
        "source": "document.pdf",
        "section_path": "1.2.3 Section Title",
        "created": "2026-01-08T10:00:00",
        "updated": "2026-01-08T10:00:00",
        "accessed": 0
      }
    },
    "cognitive": {...},
    "behavioral": {...},
    "contextual": {...},
    "state": {...}
  }
}
```

## Commands Reference

| Command | Purpose |
|---------|---------|
| `--add "content"` | Store new memory |
| `--batch "file1 file2..."` | Process multiple files |
| `--search "query"` | Find memories |
| `--list` | List all layers |
| `--get "key"` | Retrieve memory |
| `--delete "key"` | Remove memory |

## Document Consolidation Example

**Input**: 申报通知.pdf + 初步思路.docx

**Output Memories**:

| Layer | Key | Content Summary |
|-------|-----|-----------------|
| core | tech_breakthrough | 奖申报核心要素：技术突破→先进性论证→行业应用成效 |
| cognitive | deadline_0108 | 截止时间2026年1月8日，联系人韩老师，电话010111111 |
| cognitive | key_tech_areas | 关键技术领域：产业创新垂类大模型、信息感知与交互、复杂网络分析 |
| cognitive | contact_info | 邮箱111111@163.com，地址北京市海淀区 |
| behavioral | material_list | 申报材料清单：登记表、推荐表、工作总结、证明材料 |
| contextual | doc_structure_1 | 申报通知.pdf: 时间线 |
| contextual | doc_structure_2 | 初步思路.docx: 技术框架 |
