# Exercise 01 — 为什么它能聊天

先做完 [phase1-intuition/01-why-next-token-can-chat.md](../phase1-intuition/01-why-next-token-can-chat.md)。不要打开 RAG 教程。

## A. 把聊天看成字符串

1. 跑 `python3 src/chat_as_completion.py`
2. 再跑 `python3 src/chat_as_completion.py --question "什么是 token？"`
3. 用笔抄下脚本打印的 prompt。最后一行必须是 `Assistant:`
4. 回答：如果你把最后一行改成 `Database:`，模型在机制上会做什么？它会不会“切换到数据库模式”？

## B. 生成循环

1. `python3 src/next_token_demo.py --prompt "The little cat" --greedy`
2. 同样 prompt，去掉 `--greedy`，加上 `--temperature 1.2`
3. 回答：玩具模型为什么几步之后就忘了主题？GPT 改的是循环，还是上下文？

## C. Token

1. `python3 src/tokenize_demo.py --text "User: Why can it chat?"`
2. 对 `"你好世界"` 再跑一次
3. 一句话：Chat API 的 `messages` 和中文句子，对模型分别是什么？

## D. 合格线

不看笔记说出：

> 聊天是一种 prompt 格式。模型在 Assistant: 后面反复采样下一个 token。
> 没有单独的聊天大脑。Transformer 只是让每一次预测能看见整段上下文。

说得出来，再去 [04-watch-karpathy.md](../phase1-intuition/04-watch-karpathy.md)。
