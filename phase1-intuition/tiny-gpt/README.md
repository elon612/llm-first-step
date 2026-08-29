# tiny-gpt — 你自己手打的那一份

这个目录放你跟 [Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) 手写的代码。

“其余代码不在本仓库另开一套”指的是不 fork 别人的实现。
你自己一行行打出来的 tiny GPT 不是别人的代码——它是 Phase 1 的核心产出物，必须提交。
git 历史就是你真实进度的证据，比 PROGRESS.md 里的勾更诚实。

## 怎么用

- 按 [PROGRESS.md](../../PROGRESS.md) 的 02.1 ~ 02.6 推进，每完成一个小节提交一次。
- 文件组织随意（一个 `gpt.py` 也行，按小节拆也行），唯一要求：**当前提交能跑**。
- 训练语料用视频同款 tiny shakespeare 即可，约 1MB，CPU 就能训。

## 不要做的事

- 不要复制 nanoGPT 的代码进来。nanoGPT 留到 02.6 对照用。
- 不要在这里加 LoRA、RAG、聊天界面。这里只回答一件事：next-token 这条链你能不能亲手写通。
