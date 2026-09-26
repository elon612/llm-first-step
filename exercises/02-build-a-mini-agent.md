# Exercise 02 — 把 ScriptedModel 换成真模型

先读 [lessons/02-agent-is-a-loop.md](../lessons/02-agent-is-a-loop.md)，跑过 `python3 src/agent_loop.py`。

这个练习需要一个模型 API key（任意一家支持 tool calling 的都行）。key 放环境变量，不要提交。

## 做什么

1. 新建 `my-agent/real_model.py`（你自己的代码，要提交）。
2. 写一个类，实现和 `ScriptedModel` 一样的接口：

   ```python
   def next_message(self, messages, tools) -> dict
   ```

   里面做三件事：
   - 把 `messages` 和 `TOOLS` 转成你用的 API 的格式
   - 调用 API
   - 把返回转回 `{"role": "assistant", "tool_call": {...}}` 或 `{"role": "assistant", "content": ...}`
3. 复用 `src/agent_loop.py` 里的 `make_sandbox`、`run_agent`、`run_tests`，让真模型修 `cart.py`。

`run_agent` 一行都不要改。如果你发现必须改它，说明格式转换没写对。

## 做完回答（写进 `my-agent/NOTES.md`）

1. 真模型第一步做了什么？和 ScriptedModel 一样吗？
2. 打印每次 API 返回的 usage。输入 token 是怎么随步数增长的？为什么增长得比 `~tokens` 快？
   （提示：工具列表每次都要发）
3. 把 system prompt 改成“不要运行测试”，它还能修好两个 bug 吗？
4. 删掉 `grep` 工具，只留 `read_file`，它怎么找到 `cart.py` 的？
5. 把 `edit_file` 换成“整文件覆盖写入”，输出 token 变多了多少？

## 加分：换成 Dart

把 sandbox 换成一个最小 Dart 包（`lib/cart.dart` + `test/cart_test.dart`），
`run_tests` 改成调用 `dart test`。你会看到：**换语言只改工具，不改循环。**

## 过关标准

不看笔记说出：

> agent 是一个循环。模型每轮只输出一条消息：调用工具，或者回答。
> 工具由外面的程序执行，结果追加进 messages。模型知道的一切都在 messages 里。
