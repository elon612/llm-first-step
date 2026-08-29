# Progress

只勾自己真正写过、能讲出来的项。

## Phase 1 — intuition

- [ ] 01 能解释：聊天是 `Assistant:` 之后的 next-token，没有单独的聊天大脑
- [ ] 跑过 `python3 src/chat_as_completion.py`，做过练习

02 跟 Karpathy *Let's build GPT*。这一步是几十小时的投入，按视频进度拆开勾，
每一小节都要求“代码在 [phase1-intuition/tiny-gpt/](phase1-intuition/tiny-gpt/) 里能跑”，不是“看完了”：

- [ ] 02.1 读数据、字符级 tokenizer、train/val 切分
- [ ] 02.2 bigram 语言模型能训练、能采样（视频前 1/3）
- [ ] 02.3 单头 self-attention：手写 `Q·K → mask → softmax → V`
- [ ] 02.4 multi-head + FFN + residual + LayerNorm，拼成一个 Block
- [ ] 02.5 叠 Block 成 GPT，训练 loss 明显下降，能生成整段文本
- [ ] 02.6 对照 nanoGPT，能说出每个文件在链上的位置（在 tiny GPT 之后）

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
