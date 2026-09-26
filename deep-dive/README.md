# Deep dive — 可选的原理路线

主线（[lessons/](../lessons/)）只要求你懂到“能解释 agent 的行为”。这里是给想再往下挖一层的人：
亲手写出 Tokenizer → Attention → GPT，再从实现层面看推理和微调。

**不是主线的前置条件。** 什么时候来：

- 主线第一课读完，对“Transformer 怎么看见整段上下文”好奇得不行
- 主线第五、六课读完，想知道指令微调、KV Cache、量化在代码里长什么样
- 工作要转向做模型相关的事

## 三段，按顺序

| 段 | 目录 | 做什么 | 硬件 |
| --- | --- | --- | --- |
| D1 | [1-karpathy/](1-karpathy/watch-karpathy.md) | 跟 [Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) 手写 tiny GPT，代码提交到 `tiny-gpt/` | CPU / 免费 Colab |
| D2 | [2-from-scratch/](2-from-scratch/README.md) | 跟 [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)，每章答案提交到 `my-answers/` | CPU / 免费 Colab |
| D3 | [3-engineering/](3-engineering/README.md) | KV Cache、量化、LoRA 实操，入口 Transformers / LLaMA-Factory | LoRA 需要 GPU |

规则不变：一次只跟一个教程；自己写的代码和答案要提交，git 历史就是进度。

进度勾选在 [PROGRESS.md](../PROGRESS.md) 的 Deep dive 部分。
