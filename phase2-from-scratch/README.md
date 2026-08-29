# Phase 2 — 主教材：LLMs-from-scratch

第一阶段建立直觉以后，**只跟一个仓库**学系统：

[rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)

定位：用 PyTorch 从零一步步实现类似 ChatGPT 的 LLM。到 2026-08 仍在更新，约 10.2 万 Star。

nanoGPT 是“给懂的人看的精简代码”。这本书/这个仓库是“教你为什么这么写”。所以它才是主线，不是旁路。

不要把 rasbt 的代码 fork 进本仓库。本目录放两样东西：

1. **学习协议**：[chapter-checks.md](chapter-checks.md)，每章必须能回答的问题
2. **你的答案**：[my-answers/](my-answers/)，每章一个文件，写完提交，再往下

答案要进 git，不要只写在自己的笔记里。两个原因：
提交历史是真实进度的证据，勾选框容易骗自己；
写成文字的答案可以整段丢给 LLM 让它挑毛病——“用自己的话讲 Q/K/V，让模型批改”是最高效的自测。

## 阅读顺序

按仓库章节走，对应关系如下。Appendix A（PyTorch）如果生疏，插在 Ch 2 之前。

```text
Ch 2 Tokenizer / 文本数据
   ↓
   Embedding（出现在 Ch 2 末与 Ch 4）
   ↓
Ch 3 Self Attention → Multi-head Attention
   ↓
Ch 4 Transformer Block → GPT
   ↓
Ch 5 Pretraining
   ↓
Ch 7 Instruction Fine-tuning
```

Ch 6（分类微调）可以后看。它有用，但不是“聊天从哪来”的主路径。聊天来自 **pretrain + instruction tuning**，也就是 Ch 5 和 Ch 7。

## 每章一个问题

打开 [chapter-checks.md](chapter-checks.md)。学完一章，用自己的话写答案，不要复制公式。

Attention 那一章的合格线仍然是：

> 当前这个 token，通过 Q 表达“我想找什么”，
> 其它 token 的 K 表达“我是什么信息”，
> Q·K 决定我要关注谁，
> 最后把对应的 V 加权取回来。

## 和本仓库的关系

- 本仓库第一课已经回答：聊天 = 在对话格式上做 next-token。
- Karpathy 视频已经让你写过一遍 tiny GPT。
- 现在用 rasbt 把每一层写扎实，并补上预训练和指令微调。

第二阶段结束的标志：你能从零画出 GPT 前向，并能解释指令微调如何把“续写网页”变成“像助手那样接 `Assistant:`”。

在那之前，不要开始第三阶段的 RAG / LoRA / vLLM。
