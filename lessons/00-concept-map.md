# 00. 概念这么多，先学哪个？

LLM 的名词每周都在增加。不要按“热度”学，按一个问题筛：

> **学完之后，我明天用 agent 的方式会不会变？**

会变 → 第一层，要学到能用。
只影响判断和交流 → 第二层，知道一句话。
只影响造模型、部署模型的人 → 第三层，先放着。

下面的分层针对：Android / iOS / Flutter 应用层开发，主要用 agent 写代码。

## 第一层：必须掌握

| 概念 | 为什么对你重要 | 在哪课 |
| --- | --- | --- |
| next-token、token | 所有行为的底层解释，包括幻觉 | 01 |
| 上下文窗口、context rot | agent 为什么“忘了”约定、长对话为什么越来越差 | 01、03 |
| agent 循环、tool calling | agent 每一步在干什么，卡住时能判断卡在哪 | 02 |
| 可验证反馈 | 为什么一定要让 agent 跑 `flutter analyze` / 测试 | 02、04 |
| 上下文工程（rules、`AGENTS.md`） | 把项目约定固定下来，不再每次口头交代 | 03 |
| 知识截止、MCP | Flutter / SwiftUI / Compose 变得快，模型常写旧 API；MCP 把新文档接进来 | 03 |
| 多模态输入 | agent 看不到屏幕，UI 问题要给截图 | 03 |
| 评估 | 改了 rules、换了模型，到底变好没有 | 04 |
| reasoning 模型 | 什么任务值得用慢而贵的推理模型 | 05、06 |
| 成本、prompt caching | 看懂用量，知道为什么 rules 要稳定 | 06 |

## 第二层：知道一句话

| 概念 | 一句话 | 在哪课 |
| --- | --- | --- |
| 预训练 / SFT / RLHF / RL | 能力和“性格”的来源；coding 强是因为代码能跑测试，奖励可验证 | 05 |
| 微调 / LoRA | 改权重。应用开发者几乎用不到 | 05 |
| RAG / embedding | 把检索到的内容拼进 prompt；coding agent 多用 grep 代替 | 07 |
| 量化 | 用更低精度存权重，换更小体积、更快速度 | 06、07 |
| KV Cache | 缓存已算过的中间结果，所以首 token 慢、后面快 | 06 |
| MoE | 总参数大、每次只激活一部分，所以大模型也能便宜 | 05 |
| 蒸馏 | 大模型教小模型；“mini / flash”大多这么来 | 05 |
| 结构化输出 | 强制按 JSON schema 输出；tool calling 就建立在它上面 | 02 |
| Benchmark（SWE-bench 等） | 知道榜单测的是什么，以及为什么不等于你的项目 | 04 |

## 第三层：暂时忽略

Attention 的数学推导、反向传播、位置编码（RoPE）、BPE 算法细节、分布式训练、
PPO / GRPO 等 RL 算法、vLLM 部署、FlashAttention、scaling law 推导。

它们都是真知识，但不改变你明天怎么用 agent。想看，走 [deep-dive/](../deep-dive/README.md)。

## 例外：App 本身要加 AI 功能

那你就从“用 agent 的人”变成“做 LLM 应用的人”。[第七课](07-ai-inside-your-app.md) 里这些会升到第一层：
端侧模型、量化、流式输出、结构化输出、RAG、评估。

## 遇到新名词怎么办

先问三个问题，再决定要不要学：

1. 它改的是**输入**（上下文、检索、工具）、**模型**（权重、训练），还是**运行方式**（推理、部署）？
2. 我能控制它吗？应用开发者能控制的几乎只有输入。
3. 它能不能用“next-token + 上下文”解释？能，就不是新学科，只是给循环换了上下文。

大部分新名词（新的 agent 框架、新的 prompt 技巧、新的 memory 方案）都落在“输入”这一格。

## 下一步

[01-why-next-token-can-chat.md](01-why-next-token-can-chat.md)
