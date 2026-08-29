# llm-first-step

一条主线，一个仓库：

```text
Karpathy 建立直觉
        ↓
rasbt/LLMs-from-scratch 系统补全
        ↓
再进入 RAG / 微调 / 部署
```

第一课不是 Transformer 是什么，而是：

> **为什么 LLM 只做 next-token prediction，却能聊天？**

[ROADMAP.md](ROADMAP.md) · [PROGRESS.md](PROGRESS.md)

## 今天

```bash
git clone https://github.com/elon612/llm-first-step.git
cd llm-first-step
python3 src/chat_as_completion.py
```

读 [phase1-intuition/01-why-next-token-can-chat.md](phase1-intuition/01-why-next-token-can-chat.md)，做 [exercises/01-why-it-can-chat.md](exercises/01-why-it-can-chat.md)。

不要碰 RAG / Agent / LoRA，也不要先啃 nanoGPT。

## 三阶段

| 阶段 | 目录 | 做什么 |
| --- | --- | --- |
| 1 | [phase1-intuition/](phase1-intuition/) | 第一课搞懂聊天 = next-token；再跟 [Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) 手写 tiny GPT |
| 2 | [phase2-from-scratch/](phase2-from-scratch/) | 只跟 [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) |
| 3 | [phase3-engineering/](phase3-engineering/) | KV Cache、量化、LoRA、RAG、vLLM。入口：Transformers / LLaMA-Factory |

本仓库只有一个脚本：`src/chat_as_completion.py`。其余代码跟着 Karpathy 和 rasbt 写，不在这里另开一套。

## 只留 3 个外部资源

1. Karpathy — Let's build GPT
2. [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)
3. Hugging Face / LLaMA-Factory（第三阶段）

## License

MIT. See [LICENSE](LICENSE).
