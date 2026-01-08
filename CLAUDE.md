# Active Memory System & Retrieval Protocol

## 一、 核心调用协议 (Critical Retrieval Protocol)

> [!IMPORTANT]
> **记忆库物理路径**: `~/.claude/memory/memories.json`
> **最高指令**:
> 1. 该 JSON 文件是你的“长期记忆”。在执行任何任务前，你**必须**优先参考该文件。
> 2. 若记忆内容与你的预训练知识冲突，**必须以记忆库内容为准**。
> 3. 必须保持记忆库的结构完整性，严禁破坏 JSON 格式。
> 
> 

### 1. 强制读取触发点

在以下场景，你必须首先执行 `cat ~/.claude/memory/memories.json`：

* **初始化会话**: 每次新启动 `claude` 终端或切换项目时。
* **身份识别**: 涉及“我”是谁、我的专业背景或个人偏好时。
* **专业任务**: 开始处理城市规划、UE5 脚本开发、空间数据分析等复杂任务前。
* **进度恢复**: 当我提到“继续”、“接上次”或询问“还有什么没做”时。

---

## 二、 记忆库 5 层架构 (Memory Architecture)

你必须理解并按照以下层级对信息进行检索和逻辑分类：

| 层级 (Layer) | 定义与范围 | 稳定性 | 检索优先级 |
| --- | --- | --- | --- |
| **core** | 身份（城市规划设计师）、长期目标、价值观、不可动摇的准则 | 极高 | 第一优先级 |
| **cognitive** | 知识体系（规划政策）、技术概念（UE5 API）、专业技能工具 | 高 | 第二优先级 |
| **behavioral** | 个人编程习惯、交互偏好、审美倾向、代码规范、回复风格 | 中 | 第三优先级 |
| **contextual** | 特定项目背景（如：上海某区域更新）、历史决策、当前任务上下文 | 低 | 第四优先级 |
| **state** | 临时待办（To-do）、即时工作进度、当前 Session 的临时状态 | 极低 | 第五优先级 |

---

## 三、 存储规范 (JSON Schema)

所有的记忆写入和更新必须遵循以下标准的 JSON 结构：

```json
{
  "层级名": {
    "记忆ID": {
      "content": "记忆内容详细描述",
      "layer": "core | cognitive | behavioral | contextual | state",
      "tags": ["标签1", "标签2"],
      "source": "来源（如：用户口述/项目代码分析/技术文档）",
      "created": "YYYY-MM-DD",
      "updated": "YYYY-MM-DD",
      "accessed": 访问次数计数
    }
  }
}

```

---

## 四、 维护与自进化指令 (Self-Evolution)

1. **语义检索**: 检索时通过 `tags` 和 `content` 关键词进行匹配，并结合当前对话的意图。
2. **写回建议**:
* 当我们达成一个重要结论（如：确定了某种空间算法逻辑）时，主动询问：“是否需要将此存入 **cognitive** 或 **behavioral** 层级记忆？”
* 在记录时，务必确保 `updated` 时间戳为当前日期。


3. **引用计数**: 每次引用某条记忆，请在内部逻辑中对该条目的 `accessed` 加 1，并在回复中体现你参考了哪条记忆。
4. **断点保存**: 在长会话结束或我离开前，主动建议更新 `state` 层级，记录当前的“断点”和“下一步计划”。

---

## 五、 初始用户画像 (Persona - Core)

* **基本身份**: 城市规划设计师 / AI 赋能专家。
* **核心关注**: 数字孪生、城市更新政策研究、空间智能（Spatial Intelligence）。
* **常用技术栈**: Python (Geopandas, Pandas), Unreal Engine 5 (Python API), Large Language Models.
* **工作哲学**: 强调 AI 对传统设计流的重塑，追求数据驱动的规划决策。

