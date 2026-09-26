# Progress

只勾自己真正做过、能讲出来的项。能提交的产出要提交，git 历史比勾选框诚实。

## 主线

- [ ] 00 遇到一个新名词，能用三个问题判断它属于哪一层
- [ ] 01 能解释：聊天是 `Assistant:` 之后的 next-token，没有单独的聊天大脑
- [ ] 01 跑过 `python3 src/chat_as_completion.py`，做过 [练习 01](exercises/01-why-it-can-chat.md)
- [ ] 02 跑过 `python3 src/agent_loop.py` 和 `--no-verify`，能解释为什么后者失败
- [ ] 02 [练习 02](exercises/02-build-a-mini-agent.md)：真模型接进 `run_agent`，修好了 `cart.py`
- [ ] 03 项目里有一份提交了的 `AGENTS.md`
- [ ] 03 有一次“不换模型、只改上下文就变好了”的前后记录
- [ ] 04 有 10 个任务的评估集，至少对比过两种配置
- [ ] 05 能讲清预训练 / SFT / RLHF / RL 各自改变了什么行为
- [ ] 06 能估算一次 agent 任务的 token 花费，说出缓存为什么命中或没命中

## 分支：App 加 AI 功能

- [ ] 07 为一个具体功能选定云端或端侧，并写下理由
- [ ] 07 做过最小 RAG，定位过一次失败在切块 / 召回 / 使用的哪一步
- [ ] 07 LLM 调用有流式输出、结构化输出和失败兜底

## Deep dive（可选）

D1 跟 Karpathy *Let's build GPT*。几十小时的投入，按视频进度拆开勾，
每一小节都要求“代码在 [deep-dive/1-karpathy/tiny-gpt/](deep-dive/1-karpathy/tiny-gpt/) 里能跑”，不是“看完了”：

- [ ] D1.1 读数据、字符级 tokenizer、train/val 切分
- [ ] D1.2 bigram 语言模型能训练、能采样（视频前 1/3）
- [ ] D1.3 单头 self-attention：手写 `Q·K → mask → softmax → V`
- [ ] D1.4 multi-head + FFN + residual + LayerNorm，拼成一个 Block
- [ ] D1.5 叠 Block 成 GPT，训练 loss 明显下降，能生成整段文本
- [ ] D1.6 对照 nanoGPT，能说出每个文件在链上的位置

D2 LLMs-from-scratch（答案写进 [my-answers/](deep-dive/2-from-scratch/my-answers/)）：

- [ ] Ch 2 Tokenizer + embedding 形状
- [ ] Ch 3 用自己的话讲完 Q/K/V
- [ ] Ch 4 画出 GPT 前向
- [ ] Ch 5 预训练 loss 来自哪里
- [ ] Ch 7 指令微调如何把续写变成聊天
- [ ] 跳过或后置：Ch 6 分类微调

D3 推理与微调工程：

- [ ] Prefill vs decode
- [ ] KV Cache 的维度：layer × head × sequence × K/V
- [ ] 量化在省哪一块内存
- [ ] LoRA 改的是哪些矩阵
- [ ] 用 Transformers 或 LLaMA-Factory 跑通过一次加载 / 微调 / 推理
