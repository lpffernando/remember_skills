# remember - AI 持久记忆系统

**AI as Me** —— 让 AI 成为你的记忆延伸。

一个 Claude Code Skill，解决 AI 无记忆的先天缺陷。通过建立持久记忆系统，把零散信息沉淀为可检索的知识资产，让 AI 在每次对话中都能"想起"你是谁、你关心什么、你在做什么。

**核心价值**：
- 跨会话保持身份连贯
- 零散信息沉淀为结构化知识
- AI 成为真正理解你的智能伙伴

---

## 特色概览

### 6 种记忆操作

| 操作 | 功能 |
|------|------|
| **固化 (Consolidation)** | 存储新记忆，自动路由到合适层级 |
| **索引 (Indexing)** | 打标签、建关联，方便检索 |
| **更新 (Updating)** | 修改内容，保留元数据 |
| **遗忘 (Forgetting)** | 删除或压缩低活跃度记忆 |
| **检索 (Retrieval)** | 语义搜索，相关性排序 |
| **压缩 (Compression)** | 长记忆生成摘要，节省空间 |

### 5 层记忆分类

| 层级 | 容量 | 存放内容 |
|------|------|----------|
| **core** | 20 | 身份、价值观、长期目标 |
| **cognitive** | 100 | 知识、概念、专业技能 |
| **behavioral** | 100 | 习惯、偏好、工作模式 |
| **contextual** | 200 | 项目背景、任务上下文 |
| **state** | 500 | 临时待办、进度追踪 |

---

## 核心功能

### 1. 记忆存储
随时记录重要信息：
```
/remeber --add "用户偏好TDD开发方式"
```

### 2. 智能文档转换
把 PPT/PDF/DOCX 转成结构化记忆：
```
/remeber --process "项目报告.pptx"
/remeber --batch "文件1.pptx 文件2.pdf 文件3.docx"
```

### 3. 跨会话检索
随时找回之前的信息：
```
/remeber --search "之前的项目背景"
/remeber --list
```

---

## 使用场景

### 场景1：整理项目资料
把散落在各处的 PPT、PDF 整理成可搜索的知识库，自动分拆成多条记忆。

### 场景2：记录用户偏好
让 AI 记住你的工作风格、文档格式偏好，跨会话保持一致。

### 场景3：跨项目延续
新会话开始时，快速加载之前项目的上下文和背景信息。

### 场景4：团队知识共享
统一的知识库，不同成员可共同维护，沉淀组织知识资产。

---

## 快速开始

**1. 安装依赖**
```bash
pip install markitdown
```

**2. 放入 Skills 目录**
```bash
# Linux/Mac
cp -r remeber ~/.claude/skills/

# Windows - 手动复制 remeber 文件夹到 C:\Users\你的用户名\.claude\skills\
```

**3. 重启 Claude Code，直接使用**
```
/remeber --add "重要信息"
/remeber --process "报告.pptx"
/remeber --search "关键词"
```

---

## 存储位置

默认存储在 `~/.claude/memory/memories.json`，标准 JSON 格式，可被任何程序读取。

---

## 全局配置使用 (推荐)

将记忆库路径配置到 `~/.claude/CLAUDE.md`，让所有项目共享同一个记忆库：

**1. 编辑全局配置文件**

在 `~/.claude/CLAUDE.md` 中添加：

```markdown
# Active Memory System & Retrieval Protocol

## 一、 核心调用协议

> **记忆库物理路径**: `~/.claude/memory/memories.json`
```

**2. 在项目级 CLAUDE.md 中引用**

在项目根目录的 `CLAUDE.md` 中添加：

```markdown
# Active Memory System & Retrieval Protocol

> **重要**: 请优先读取全局记忆库 `~/.claude/memory/memories.json`
> 并在响应中体现对记忆的引用和更新
```

这样配置后：
- 所有项目的 AI 都会读取同一个记忆库
- 保持身份、偏好、上下文在全局范围内一致
- 跨项目无缝切换，知识不丢失

---

## 设计理念

**用进废退**：不用时间过期机制，基于活跃度管理记忆。
- 经常搜索 → 保留
- 长期不用 → 压缩或淘汰

让记忆系统像大脑一样工作。
