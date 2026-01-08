# remember - AI Persistent Memory System

**AI as Me** — Let AI become an extension of your memory.

A Claude Code Skill that solves AI's inherent lack of memory. By building a persistent memory system, scattered information is transformed into retrievable knowledge assets, enabling AI to "remember" who you are, what you care about, and what you're working on in every conversation.

**Core Value**:
- Maintain identity consistency across sessions
- Transform scattered information into structured knowledge
- AI becomes a truly understanding intelligent partner

---

## Feature Overview

### 6 Memory Operations

| Operation | Function |
|-----------|----------|
| **Consolidation** | Store new memories, automatically route to appropriate layer |
| **Indexing** | Add tags, build associations for easy retrieval |
| **Updating** | Modify content while preserving metadata |
| **Forgetting** | Delete or compress low-activity memories |
| **Retrieval** | Semantic search with relevance ranking |
| **Compression** | Generate summaries for long memories to save space |

### 5 Memory Layers

| Layer | Capacity | Content |
|-------|----------|---------|
| **core** | 20 | Identity, values, long-term goals |
| **cognitive** | 100 | Knowledge, concepts, professional skills |
| **behavioral** | 100 | Habits, preferences, work patterns |
| **contextual** | 200 | Project background, task context |
| **state** | 500 | Temporary todos, progress tracking |

---

## Core Features

### 1. Memory Storage
Record important information anytime:
```
/remember --add "User prefers TDD development approach"
```

### 2. Intelligent Document Conversion
Convert PPT/PDF/DOCX into structured memories:
```
/remember --process "ProjectReport.pptx"
/remember --batch "File1.pptx File2.pdf File3.docx"
```

### 3. Cross-Session Retrieval
Retrieve information anytime:
```
/remember --search "Previous project background"
/remember --list
```

---

## Use Cases

### Scenario 1: Organize Project Materials
Convert scattered PPTs and PDFs into a searchable knowledge base, automatically split into multiple memories.

### Scenario 2: Record User Preferences
Let AI remember your work style and document format preferences, maintaining consistency across sessions.

### Scenario 3: Cross-Project Continuity
Quickly load previous project context and background information when starting a new session.

### Scenario 4: Team Knowledge Sharing
Unified knowledge base that team members can maintain together, building organizational knowledge assets.

---

## Quick Start

**1. Place in Skills Directory**
```bash
# Linux/Mac
cp -r remember ~/.claude/skills/

# Windows - Manually copy remember folder to C:\Users\YourUsername\.claude\skills\
```

**2. Restart Claude Code and Use**
```
/remember --add "Important information"
/remember --process "Report.pptx"
/remember --search "keyword"
```

---

## Storage Location

Default storage: `~/.claude/memory/memories.json` in standard JSON format, readable by any program.

---

## Global Configuration Usage (Recommended)

Configure the memory path in `~/.claude/CLAUDE.md` to share the same memory bank across all projects:

**1. Edit Global Configuration File**

Add to `~/.claude/CLAUDE.md`:

```markdown
# Active Memory System & Retrieval Protocol

## 一、 Core Protocol

> **Memory Bank Path**: `~/.claude/memory/memories.json`
```

**2. Reference in Project-level CLAUDE.md**

Add to your project's `CLAUDE.md`:

```markdown
# Active Memory System & Retrieval Protocol

> **Important**: Please read the global memory bank `~/.claude/memory/memories.json` first
> Reflect memory references and updates in your responses
```

After this configuration:
- All project AIs will read from the same memory bank
- Maintain consistent identity, preferences, and context globally
- Seamless cross-project switching without losing knowledge

---

## Design Philosophy

**Use It or Lose It**: No expiration mechanism, based on activity management:
- Frequently searched → Keep
- Long unused → Compress or discard

Let the memory system work like a brain.
