# Agent 编程路线（应用优先）

给每天用 coding agent 写代码、但想知道“为什么这么用更好”的人。

和 [ROADMAP.md](ROADMAP.md) 的区别：那条是“先手写 GPT，再学工程”；这条是“先把每天在用的东西拆开，原理按需往下挖”。
两条共用第一课，手写 GPT 在这里变成可选的加深。

## 先回答：RAG、后训练，哪个更好？

对“用 agent 做软件开发”的人，优先级是：

```text
上下文工程（prompt / rules / 给什么文件、什么测试）   ← 天天用，收益最大
        ↓
工具与检索（agent 自己 grep / 读文件，或者 RAG）       ← 解决“模型不知道你的代码/文档”
        ↓
评估（怎么知道改了 prompt 之后变好还是变坏）           ← 应用层最容易被跳过的一环
        ↓
后训练（SFT / RLHF / RL）                              ← 要懂原理，几乎不需要自己做
```

- **RAG 和后训练不是二选一**。RAG 改的是“这次输入里有什么”（知识），后训练改的是“模型权重倾向怎么回答”（行为/格式）。知识缺失用检索，行为不对先改 prompt，改不动、且有大量样本时才考虑微调。
- **后训练值得懂，不值得先做**。模型为什么会调用工具、为什么写代码比写散文稳、为什么会“讨好”你——答案都在后训练里。但你手上的前沿模型已经被厂商后训练过，自己微调很难超过它们。
- **coding agent 里经典向量 RAG 的地位在下降**。代码是结构化、可精确搜索的，主流 agent 更多靠 `grep` / 读文件 / 代码索引做“agentic search”。向量 RAG 更适合大量非结构化文档（产品文档、工单、知识库）。

## 阶段 0：最小原理（够用就停）

目标：能用“next-token + 上下文窗口”解释 agent 的大部分怪行为。

1. 本仓库 [第一课](phase1-intuition/01-why-next-token-can-chat.md)：聊天 = `Assistant:` 之后的 next-token
2. Karpathy — [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)（给使用者看的全景：预训练 → SFT → RL → 幻觉 → 工具）

学完能回答：

- token 是什么，为什么模型数不清 `strawberry` 里有几个 `r`
- 上下文窗口是什么，为什么对话越长 agent 越“健忘”、越容易跑偏
- temperature / 采样为什么让同一个 prompt 每次结果不一样
- 幻觉从哪来：模型在补全“看起来合理的下一段”，不是查表

## 阶段 1：拆开 agent（最重要的一步）

目标：知道 Cursor / Claude Code 这类工具在循环里到底做了什么。

核心只有一个循环：

```text
messages = [system, user_task]
loop:
    reply = LLM(messages, tools)
    if reply 没有 tool_call: 结束
    result = 执行 tool_call（读文件 / grep / 改文件 / 跑测试）
    messages += [reply, result]
```

- 读 Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
- 读 [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent)（约百行的真实 coding agent）
- **自己写一个**：`read_file`、`grep`、`write_file`、`run_tests` 四个工具，用任意模型 API，让它修一个故意写错的函数

学完能回答：

- tool calling 本质上仍是 next-token：模型输出一段符合 schema 的 JSON，是后训练教会的
- 为什么 agent 读的每个文件、每次测试输出都在吃上下文
- 什么时候用固定 workflow（可预测）比用自主 agent（灵活）更好
- MCP 是什么：把“工具”标准化成可插拔的服务，不是新能力

## 阶段 2：上下文工程（天天用得上）

目标：把“玄学提示词”换成“我在控制模型看到什么”。

- 读 Anthropic — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

把日常经验和原理对上：

| 你可能已经在做的事 | 为什么有效 |
| --- | --- |
| 先让 agent 出计划，再执行 | 计划变成上下文里的 token，后续生成以它为条件；错误在便宜的时候暴露 |
| 任务拆小、开新对话 | 长上下文里注意力被稀释（context rot），旧的错误尝试会持续干扰 |
| 写 `AGENTS.md` / rules | 每次都注入的稳定前缀，代替每次口头交代 |
| 给出测试、让它跑测试 | 把“对不对”从模型的自我感觉变成可验证的外部信号 |
| 让子 agent 去搜索 | 搜索过程的大量噪声留在子 agent 里，主上下文只收结论 |
| 指明文件路径而不是描述 | 省掉一轮检索，也减少检索错位 |

练习：挑一个你们项目里 agent 常做砸的任务，只改上下文（rules、给的文件、给的测试），不换模型，记录前后差异。

## 阶段 3：检索与 RAG

目标：知道什么时候需要 RAG，什么时候 `grep` 就够。

- 概念：embedding、chunking、向量检索、BM25、混合检索、rerank
- 对照：agentic search（agent 多轮搜索、读文件）vs 一次性 RAG（检索一次拼进 prompt）
- 练习：对你们的一份内部文档做一个最小 RAG；再故意问 5 个检索会失败的问题，看失败在哪一步（切块？召回？模型没用上？）

记住一句话：**检索进来的文档，只是被拼进 prompt 的额外 token**。RAG 的质量上限由“拼进去的东西对不对”决定。

## 阶段 4：评估

目标：改 prompt / 换模型 / 加 RAG 之后，能用数据说“变好了”。

- 读 Hamel Husain — [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)
- 了解 [SWE-bench](https://www.swebench.com/) 怎么评 coding agent：真实 issue + 隐藏测试
- 练习：从你们项目里收集 10–20 个真实任务，写成“输入 + 通过标准（最好是测试）”，每次改动都跑一遍

## 阶段 5：后训练（懂原理，不急着做）

目标：理解模型行为从哪来，判断“该不该微调”。

```text
预训练        → 会续写互联网文本
SFT           → 会按指令回答、会按格式输出工具调用
RLHF / DPO    → 回答更符合人类偏好（副作用：讨好、啰嗦）
RL（可验证奖励）→ 代码能跑、数学答案对就给奖励 → reasoning 模型、强 coding 能力
```

- 回看阶段 0 的 Karpathy 视频后半段
- 本仓库 [Phase 2 Ch 7](phase2-from-scratch/README.md)（指令微调如何把续写变成聊天）

什么时候才值得微调：固定输出格式/风格、要用小模型压成本和延迟、有大量高质量标注样本、且 prompt + 检索已经试过不行。
真要动手，再去 [phase3-engineering/](phase3-engineering/) 的 LoRA / LLaMA-Factory。

## 阶段 6：成本与延迟

目标：看懂账单和速度。

- 输入 token vs 输出 token 的价格差；reasoning token 也计费
- prefill / decode、KV Cache（见 [phase3-engineering/](phase3-engineering/)）
- prompt caching：前缀不变才能命中缓存 → 这是 rules 和 system prompt 放在最前面、保持稳定的工程原因
- 模型选择：大模型规划 + 小模型执行，什么时候划算

## 可选加深

想真正“看见”Attention，再回到主线 [ROADMAP.md](ROADMAP.md)：Karpathy 手写 tiny GPT → LLMs-from-scratch。
对应用开发者不是前置条件，但做完之后阶段 2、6 里的很多“为什么”会变成显然。

## 书（只推荐一本）

Chip Huyen — *AI Engineering*（O'Reilly, 2025）：prompt、RAG、agent、微调、评估的取舍，正好覆盖本路线。

## 进度

- [ ] 0 能用 next-token + 上下文窗口解释 agent 的一次跑偏
- [ ] 1 自己写的最小 coding agent 修好过一个 bug
- [ ] 2 只改上下文让一个常做砸的任务变好，有前后记录
- [ ] 3 做过最小 RAG，并定位过一次检索失败
- [ ] 4 有一个 10+ 任务的评估集，能重复跑
- [ ] 5 能讲清 SFT / RLHF / RL 各自改变了模型的什么行为
- [ ] 6 能估算一次 agent 任务的 token 成本，并说出缓存为什么命中/没命中
