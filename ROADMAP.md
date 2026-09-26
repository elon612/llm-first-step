# Roadmap

应用优先：先把每天在用的东西拆开，原理只挖到能解释行为为止。

风险不是学不会，是每天追新名词、换教程，却从没拆开过一次自己手上的 agent。
遇到新名词，先用 [00 概念地图](lessons/00-concept-map.md) 的三个问题筛一遍。

## 主线

| 课 | 回答的问题 | 产出 |
| --- | --- | --- |
| [00](lessons/00-concept-map.md) | 这么多概念，先学哪个 | 知道什么可以先不学 |
| [01](lessons/01-why-next-token-can-chat.md) | 只会预测下一个 token，为什么能聊天 | 跑过 `chat_as_completion.py`，做完练习 01 |
| [02](lessons/02-agent-is-a-loop.md) | coding agent 在循环里到底做了什么 | 跑过 `agent_loop.py`；练习 02 换成真模型 |
| [03](lessons/03-context-engineering.md) | 为什么“先计划、拆小、给测试、写 rules”有效 | 你项目里的 `AGENTS.md`，一次前后对比 |
| [04](lessons/04-verify-and-eval.md) | 怎么知道改了之后变好了 | 10 个任务的评估集 |
| [05](lessons/05-how-models-are-trained.md) | 模型的行为从哪来；要不要微调 | 能把 agent 的行为对回训练阶段 |
| [06](lessons/06-cost-and-latency.md) | 钱花在哪，为什么慢 | 估算过一次真实任务的花费 |

01–04 是核心，建议按顺序、做完产出再往下。05、06 可以穿插。

## 案例

[01 — 测试全绿，Bug 还是很多](case-studies/01-green-tests-many-bugs.md)：04 的实战版。独立 Oracle、接缝测试、fail-first 门禁、度量与路线图。

## 分支

[07 — App 本身要加 AI 功能](lessons/07-ai-inside-your-app.md)：云端 vs 端侧、流式与结构化输出、RAG、评估。有需求时再学。

## 可选：原理路线

[deep-dive/](deep-dive/README.md)：Karpathy 手写 tiny GPT → rasbt/LLMs-from-scratch → KV Cache / 量化 / LoRA。
不是主线前置条件；做完之后，03、06 里的很多“为什么”会变得显然。
