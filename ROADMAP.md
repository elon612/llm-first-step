# Roadmap

一条主线，一个仓库。不要同时铺开十几个教程仓库。

```text
Karpathy 建立直觉
        ↓
LLMs-from-scratch 系统补全
        ↓
再进入 RAG / 微调 / 部署
```

参考资料（llm-course、Datawhale、Awesome-LLM）只当索引，不当主线。
风险不是学不会，是每天换一个教程，Attention 却从没认真写过一次。

## 现在的状态

按 [PROGRESS.md](PROGRESS.md) 勾。默认从第一课开始：

**[phase1-intuition/01-why-next-token-can-chat.md](phase1-intuition/01-why-next-token-can-chat.md)**

第一课不是 “Transformer 是什么”，而是：

> LLM 为什么只做 next-token prediction，却能聊天？

## 三阶段

### 1. 直觉 — Karpathy

目录：[phase1-intuition/](phase1-intuition/)

- 01 聊天 = 对话格式上的 next-token
- 02 token
- 03 生成循环
- 04 跟 [Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) 手写 tiny GPT

这一阶段禁止：RAG、Agent、LoRA、以及直接啃 [nanoGPT](https://github.com/karpathy/nanoGPT) 源码。
nanoGPT 约 6.2 万 Star，极简、适合**写过 tiny GPT 之后**对照。

### 2. 系统 — rasbt/LLMs-from-scratch

目录：[phase2-from-scratch/](phase2-from-scratch/)

主教材：[rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)
（约 10.2 万 Star，2026-08 仍活跃：Tokenizer → Attention → GPT → Pretrain → Instruction FT）

### 3. 工程 — 推理与微调

目录：[phase3-engineering/](phase3-engineering/)

KV Cache、量化、LoRA / QLoRA、RAG、vLLM / llama.cpp。
入口：Hugging Face Transformers + LLaMA-Factory。

## 外部资源只保留这 3 个

1. Karpathy — Let's build GPT
2. `rasbt/LLMs-from-scratch`
3. Hugging Face / LLaMA-Factory（第三阶段才打开）
