# Roadmap

一条主线，一个仓库。不要同时铺开十几个教程仓库。

```text
Karpathy 建立直觉
        ↓
LLMs-from-scratch 系统补全
        ↓
再进入 RAG / 微调 / 部署
```

llm-course、Datawhale、Awesome-LLM 只当索引。风险不是学不会，是每天换教程，Attention 却从没写过一次。

## 现在

[phase1-intuition/01-why-next-token-can-chat.md](phase1-intuition/01-why-next-token-can-chat.md)

勾选：[PROGRESS.md](PROGRESS.md)

## Phase 1 — Karpathy

[phase1-intuition/](phase1-intuition/)

1. 为什么只会预测下一个 token，却能聊天
2. 跟 [Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) 手写 tiny GPT

禁止：RAG、Agent、LoRA、直接啃 [nanoGPT](https://github.com/karpathy/nanoGPT)。
nanoGPT 留给 tiny GPT 写完之后对照。

## Phase 2 — rasbt/LLMs-from-scratch

[phase2-from-scratch/](phase2-from-scratch/)

主教材：[rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)

Tokenizer → Embedding → Self Attention → Multi-head → GPT → Pretraining → Instruction Fine-tuning

## Phase 3 — 工程

[phase3-engineering/](phase3-engineering/)

KV Cache、量化、LoRA / QLoRA、RAG、vLLM / llama.cpp。
入口：Hugging Face Transformers + LLaMA-Factory。Phase 2 写完再打开。

## 外部资源只留 3 个

1. Karpathy — Let's build GPT
2. `rasbt/LLMs-from-scratch`
3. Hugging Face / LLaMA-Factory（第三阶段）
