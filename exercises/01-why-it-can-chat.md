# Exercise 01 — 为什么它能聊天

先读 [lessons/01-why-next-token-can-chat.md](../lessons/01-why-next-token-can-chat.md)。

1. 跑 `python3 src/chat_as_completion.py`
2. 再跑 `python3 src/chat_as_completion.py --question "什么是 token？"`
3. 用笔抄下脚本打印的 prompt。最后一行必须是 `Assistant:`
4. 回答：如果把最后一行改成 `Database:`，模型在机制上会做什么？它会不会“切换到数据库模式”？
5. 玩具模型只看前一个词，回复为什么会跑题？GPT 改的是循环，还是上下文？

6. 联系你每天用的 agent：它在一次长对话里“忘了”你开头交代的约定。用上下文解释，而不是用“它变笨了”解释。

不看笔记说出下面这段，再去 [第二课](../lessons/02-agent-is-a-loop.md)：

> 聊天是一种 prompt 格式。模型在 Assistant: 后面反复采样下一个 token。
> 没有单独的聊天大脑。Transformer 只是让每一次预测能看见整段上下文。
