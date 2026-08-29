# Phase 2 chapter checks

每学完 rasbt 的一章，合上书回答。写不出就回去重写那一章的代码，不要往下翻。

把答案写在你自己的笔记里，不必提交到本仓库。

## Ch 2 — Tokenizer

- 为什么 LLM 不用空格分词？
- BPE merge 一次，序列长度和词表发生了什么？
- token id 进模型之前，为什么还要 embedding？那一层的输入/输出形状是什么？

## Ch 3 — Attention

不要停在 `Q × K → softmax → V`。必须能讲：

- 当前 token 的 **Q** 在表达什么？
- 其它 token 的 **K** 在表达什么？
- `Q·K`（或 scaled dot-product）决定了什么？
- **V** 被加权之后，当前位置得到的是什么？
- causal mask 删掉了什么？若删掉，训练时会发生什么泄漏？
- 多头相对单头，到底多了什么，而不是“多算几次”这种空话？

## Ch 4 — GPT

- 一个 Transformer Block 里，attention 之后为什么还要 FFN？
- residual + LayerNorm 解决的是训练问题还是表达问题？你倾向哪种解释？
- 最终线性层为什么映射回词表大小？logits 和 next-token 概率差在哪？
- 参数量大致由哪些矩阵贡献？（embedding、QKV、FFN、输出头）

## Ch 5 — Pretraining

- 预训练的标签从哪来？为什么说它是自监督？
- teacher forcing 时，模型一次看见整段，但仍用 causal mask，这是怎么同时成立的？
- loss 下降意味着“更懂世界”，还是“更会续写这篇语料的统计”？两者边界在哪？

## Ch 7 — Instruction fine-tuning

- 指令微调改的是架构，还是数据格式 + 权重？
- 为什么要把样本排成 `User: ... Assistant: ...` 这种模板？（回到第一课）
- 只训 assistant token 的 loss、不训 user token 的 loss，原因是什么？
- 到这里，你能不能用一段话连接：next-token → 预训练续写 → 指令微调后会聊天？

写完 Ch 7 的答案，再打开 [`../phase3-engineering/`](../phase3-engineering/README.md)。
