# 04. 验证与评估：怎么知道“变好了”

第二课讲的是**单次任务**的验证：让 agent 跑测试，别信它的自我感觉。

这一课讲的是**跨任务**的评估：你改了 `AGENTS.md`、换了模型、装了一个 MCP——整体是变好了还是变坏了？

没有评估，“这个模型更好用”“这条 rule 有用”都只是印象。LLM 输出有随机性，一两次的印象很容易骗人。

读 Hamel Husain — [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)。

## 验证信号从强到弱

| 信号 | 例子 | 可信度 |
| --- | --- | --- |
| 可执行检查 | `flutter test`、`flutter analyze`、编译通过 | 高，而且 agent 能自己跑 |
| 确定性规则 | 没改生成文件、没新增依赖、diff 只动了指定目录 | 高，写个脚本就能查 |
| 人工对照 | 截图和设计稿对比、你 review diff | 高，但贵 |
| LLM 评审 | 让另一个模型按标准打分 | 中，要先用人工结果校准 |
| 模型自述 | “我已经修好了” | 低 |

能往上挪一格就往上挪。给 agent 的任务尽量配上前两类信号。

## 看懂榜单

[SWE-bench](https://www.swebench.com/) 是 coding agent 最常被引用的榜单：真实 GitHub issue + 隐藏测试，测试通过才算解决。

它能说明模型的通用能力，但不能替你回答“在我们的 Flutter 项目里谁更好”，因为：

- 题目以 Python 仓库为主
- 没有 UI、没有多端、没有你们的约定
- 榜单成绩也可能来自训练数据污染

所以你需要自己的小评估集。

## 动手：你们项目的 10 个任务

用 [templates/eval-tasks.md](../templates/eval-tasks.md)：

1. 从最近的真实需求和 bug 里挑 10 个，大小适中（agent 一次对话能做完）
2. 每个写清：起始 commit、任务描述、通过标准（最好是一条测试命令）
3. 每次改 rules、换模型、换工具，都在同一批任务上跑一遍，记录通过数、轮数、花费

不需要自动化。表格加 git 分支就够用。重要的是**同一批任务、同一套标准**。

## 真实案例

[案例 01：测试全绿，Bug 还是很多](../case-studies/01-green-tests-many-bugs.md)：一个 Flutter monorepo 有 1,594 个测试文件，
一半以上的提交仍然在修 bug。原因是测试和实现出自同一个 agent 的上下文，而 bug 住在接缝里。
案例里的 [fail_first_check.sh](../templates/fail_first_check.sh) 把“测试必须先在旧代码上失败”变成了 CI 检查。

## 这一课结束的标准

- 能说出五种验证信号的强弱顺序，以及“模型自述”为什么最弱
- 有一份 10 个任务的评估集，至少跑过两种配置并有对比

## 下一步

[05-how-models-are-trained.md](05-how-models-are-trained.md)
