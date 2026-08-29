# Phase 3 — 现代 LLM 工程（先锁住）

这一阶段在 Attention 和 GPT 写过之前开始，会学成工具清单。
第二阶段 Ch 7 的检查题写完再来。

## 顺序

```text
Transformer
     ↓
LLM inference
     ↓
KV Cache
     ↓
Quantization
     ↓
LoRA / QLoRA
     ↓
RAG
     ↓
vLLM / llama.cpp
```

实践入口（仍然只要两条，不要同时开十个仓库）：

1. [Hugging Face Transformers](https://github.com/huggingface/transformers) — 加载、推理、训练接口
2. [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) — 微调与部署的工程封装

`llm-course`、Datawhale、Awesome-LLM 只当索引。

## 用底层把工程问题串起来

这些不是新学科。它们是同一张图上的节点。

```text
为什么上下文越长越慢？
        ↓
Attention complexity  ~  sequence²

为什么首 token 慢？
        ↓
Prefill：第一次要对整段 prompt 做 attention

为什么后续 token 快？
        ↓
KV Cache：过去的 K/V 不必重算

为什么 KV Cache 很占内存？
        ↓
layer × head × sequence × K/V

为什么 3B 模型还能占很多 RAM？
        ↓
weights + KV cache + runtime buffer

为什么量化能省内存？
        ↓
FP16 → INT8 / INT4
```

LoRA / QLoRA 要等你能指出：预训练权重里哪些矩阵最大、微调时为什么只训低秩增量。
RAG 要等你能指出：检索进来的文档，不过是被拼进 prompt 的额外 token；模型仍然在预测下一个 token。

到那时再看这些工具，会比现在直接学容易很多。
