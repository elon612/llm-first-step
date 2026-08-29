# llm-first-step

一条主线，一个仓库。大模型学习从这一课开始：

> **为什么 LLM 只做 next-token prediction，却能聊天？**

不要同时铺开十几个教程仓库。路径是：

```text
Karpathy 建立直觉
        ↓
rasbt/LLMs-from-scratch 系统补全
        ↓
再进入 RAG / 微调 / 部署
```

细节在 [ROADMAP.md](ROADMAP.md)。勾选在 [PROGRESS.md](PROGRESS.md)。

## 今天做什么

读第一课，跑一个脚本：

```bash
git clone https://github.com/elon612/llm-first-step.git
cd llm-first-step

# 第一课
# phase1-intuition/01-why-next-token-can-chat.md
python3 src/chat_as_completion.py
```

离线、标准库即可。不要在这一步碰 RAG、Agent、LoRA。也不要一上来啃 nanoGPT 源码。

## 三阶段

| 阶段 | 目录 | 你要得到的东西 |
| --- | --- | --- |
| 1 直觉 | [phase1-intuition/](phase1-intuition/) | 聊天 = 对话格式上的 next-token；再跟 [Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) 手写 tiny GPT |
| 2 系统 | [phase2-from-scratch/](phase2-from-scratch/) | 把 [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)（约 10.2 万 Star，2026-08 仍活跃）当主教材写完 |
| 3 工程 | [phase3-engineering/](phase3-engineering/) | KV Cache、量化、LoRA、RAG、vLLM。入口：Transformers / LLaMA-Factory |

第一阶段的链，先建立画面，再去视频里写代码：

```text
一句话 → Tokenizer → token id → Embedding → Attention → Block × N → logits → next token
```

## 本仓库的代码（只服务第一阶段）

```text
src/chat_as_completion.py   # 聊天 JSON → 以 Assistant: 结尾的字符串 → 续写
src/tokenize_demo.py        # 字 / 词 / tiny BPE / tiktoken
src/next_token_demo.py      # 字符 bigram：score → pick → append
src/chat_hello.py           # 可选，真 API。不是主线
```

```bash
python3 src/tokenize_demo.py
python3 src/next_token_demo.py --greedy
python3 -m unittest discover -s tests -v
```

## 只保留 3 个外部资源

1. **Karpathy — Let's build GPT** — 让你突然理解 Transformer
2. **[rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)** — 真正的主教材
3. **Hugging Face / LLaMA-Factory** — 懂底层之后再学加载、微调、部署

[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)（约 6.2 万 Star）放在 tiny GPT **写完之后**对照。它是精简实现，不是入门教材。

## License

MIT. See [LICENSE](LICENSE).
