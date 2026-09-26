# 02. Agent 只是一个循环

第一课：聊天 = 在 `Assistant:` 后面反复做 next-token。

这一课：**coding agent = 同一个模型 + 工具 + 一个 while 循环**。
Cursor、Claude Code、Copilot agent 模式，核心都是它。

## 循环长什么样

```text
messages = [system, 你的任务]
loop:
    reply = LLM(messages, 工具列表)
    if reply 不是工具调用: 结束，reply 就是最终回答
    result = 真正执行这个工具（读文件 / grep / 改文件 / 跑测试）
    messages += [reply, result]
```

跑一遍：

```bash
python3 src/agent_loop.py
python3 src/agent_loop.py --no-verify
```

脚本里有一个带两个 bug 的 `cart.py`。每一步会打印：

1. 模型要调用哪个工具、参数是什么
2. 工具返回了什么
3. `messages` 有多少条、大约多少 token

`ScriptedModel` 是固定规则，不是真模型，这样才能离线跑。**循环、工具、messages 都是真的。**
换成真模型 API，循环一行都不用改——这是 [练习 02](../exercises/02-build-a-mini-agent.md)。

## 从输出里看出来的四件事

### 1. 工具调用仍然是 next-token

模型没有“执行”任何东西。它只是生成一段符合格式的文本：

```json
{"name": "read_file", "arguments": {"path": "cart.py"}}
```

真正读文件的是外面的程序（harness）。模型会按格式输出工具调用，是后训练教出来的（见第五课）。

### 2. agent 知道的一切，都在 messages 里

模型没有“看过你的仓库”。它只看到被 `read_file`、`grep` 放进 messages 的那些内容。

所以：

- 它说“项目里没有这个类”，可能只是没搜到，不是真没有
- 你知道但没告诉它、它也没读到的约定，对它来说不存在
- 每读一个文件、每跑一次测试，上下文都在变长（看 `~tokens` 那一列）

### 3. 没有验证，就会“修了看得见的那个”

对比两次运行的最后两行：

```text
python3 src/agent_loop.py              → independent test run: PASS
python3 src/agent_loop.py --no-verify  → independent test run: FAIL
```

`--no-verify` 时，agent 修掉第一个报错就宣布完成。它不是在撒谎——它的上下文里没有任何信号说还有第二个 bug。
**“对不对”必须来自外部信号**（测试、编译器、analyzer），不能来自模型的自我感觉。

### 4. 工具设计决定 agent 能力上限

`edit_file` 用“精确替换一段字符串”，而不是“重写整个文件”：省 token，也不容易误删别处。
真实 agent 的工具设计都在做这种取舍。

## 自主 agent 还是固定流程？

读 Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents)。

核心区分：

| | 固定流程（workflow） | 自主 agent |
| --- | --- | --- |
| 谁决定下一步 | 你写死的代码 | 模型 |
| 适合 | 步骤已知：生成 → lint → 修复 | 步骤未知：排查一个奇怪的 bug |
| 风险 | 不灵活 | 跑偏、绕圈、成本不可控 |

日常的“先出计划、我确认、再执行”，就是在自主 agent 里人为插入一个固定检查点。

## MCP 是什么

MCP（Model Context Protocol）把“工具”做成可插拔的服务：文档查询、Figma、Jira、数据库……
对模型来说，MCP 工具和 `read_file` 没有区别，都是工具列表里的一项。**它不是新能力，是工具的接入标准。**

## 这一课结束的标准

- 能画出上面的循环，并指出模型在哪一步、harness 在哪一步
- 能解释 `--no-verify` 为什么会失败
- 能说出：agent 说“找不到某个文件”时，至少两种可能的原因

## 下一步

[练习 02](../exercises/02-build-a-mini-agent.md)（换真模型），然后 [03-context-engineering.md](03-context-engineering.md)。

想看一个真实但仍然很小的 coding agent：[mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent)。
