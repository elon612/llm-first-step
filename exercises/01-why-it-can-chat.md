# Exercise 01 — 为什么它能聊天

先读 [phase1-intuition/01-why-next-token-can-chat.md](../phase1-intuition/01-why-next-token-can-chat.md)。不要打开 RAG 教程。

1. 跑 `python3 src/chat_as_completion.py`
2. 再跑 `python3 src/chat_as_completion.py --question "什么是 token？"`
3. 用笔抄下脚本打印的 prompt。最后一行必须是 `Assistant:`
4. 回答：如果把最后一行改成 `Database:`，模型在机制上会做什么？它会不会“切换到数据库模式”？
5. 玩具模型只看前一个词，回复为什么会跑题？GPT 改的是循环，还是上下文？

不看笔记说出下面这段，再去 [02-watch-karpathy.md](../phase1-intuition/02-watch-karpathy.md)：

> 聊天是一种 prompt 格式。模型在 Assistant: 后面反复采样下一个 token。
> 没有单独的聊天大脑。Transformer 只是让每一次预测能看见整段上下文。
