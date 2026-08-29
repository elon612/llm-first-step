# Progress

只勾自己真正写过、能讲出来的项。

## Phase 1 — intuition

- [ ] 01 能解释：聊天是 `Assistant:` 之后的 next-token，没有单独的聊天大脑
- [ ] 跑过 `python3 src/chat_as_completion.py`
- [ ] 02 能解释 token ≠ 字 ≠ 词，并跑过 `tokenize_demo.py`
- [ ] 03 能画出 score → pick → append 循环，并跑过 greedy / temperature
- [ ] 04 跟完 Karpathy *Let's build GPT*，自己写出 tiny GPT
- [ ] 对照过 nanoGPT，能指认 tokenizer / attn / block / generate（在 tiny GPT 之后）

## Phase 2 — LLMs-from-scratch

- [ ] Ch 2 Tokenizer + embedding 形状
- [ ] Ch 3 用自己的话讲完 Q/K/V（见 chapter-checks）
- [ ] Ch 4 画出 GPT 前向
- [ ] Ch 5 预训练 loss 来自哪里
- [ ] Ch 7 指令微调如何把续写变成聊天
- [ ] 跳过或后置：Ch 6 分类微调

## Phase 3 — engineering（Phase 2 完成前不要勾）

- [ ] Prefill vs decode
- [ ] KV Cache 的维度：layer × head × sequence × K/V
- [ ] 量化在省哪一块内存
- [ ] LoRA 改的是哪些矩阵
- [ ] RAG 只是在改 prompt
- [ ] 用 Transformers 或 LLaMA-Factory 跑通过一次加载 / 微调 / 推理
