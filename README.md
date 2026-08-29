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

本仓库自带的脚本只有 `src/chat_as_completion.py`。但你自己的产出要提交进来：

- 跟视频手写的 tiny GPT 放 [phase1-intuition/tiny-gpt/](phase1-intuition/tiny-gpt/)
- Phase 2 每章的检查题答案放 [phase2-from-scratch/my-answers/](phase2-from-scratch/my-answers/)

不 fork 别人的实现，但你亲手写的代码和答案是进度的证据，git 历史比勾选框诚实。

硬件预期：Phase 1 的 tiny GPT 和 Phase 2 的小语料预训练，CPU 或免费 Colab 就够；
真正需要 GPU 的只有 Phase 3 的 LoRA 实操。“没有显卡”不是不开始的理由。

## 只留 3 个外部资源

1. Karpathy — Let's build GPT
2. [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)
3. Hugging Face / LLaMA-Factory（第三阶段）

## License

MIT. See [LICENSE](LICENSE).
