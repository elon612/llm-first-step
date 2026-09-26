# 03. 上下文工程：控制模型看到什么

第二课的结论：agent 知道的一切都在 messages 里。

所以“怎么用 agent 更好”几乎全部可以归结为一个问题：

> **每一步，messages 里有没有正确的信息，有没有多余的噪声？**

这就是上下文工程。“提示词技巧”只是它的一小部分。

读 Anthropic — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)。

## 上下文里有什么

```text
system prompt           ← 工具厂商写的
rules / AGENTS.md       ← 你写的，每次都注入
工具列表                ← 工具厂商 + 你装的 MCP
你的消息                ← 任务描述、@ 的文件、截图
工具结果                ← agent 自己读的文件、grep 结果、测试输出
历史对话                ← 越来越长
```

你能直接控制的是第 2、3、4 行。

## 常见做法，和它们为什么有效

| 做法 | 为什么有效 |
| --- | --- |
| 先让 agent 出计划，确认后再执行 | 计划变成上下文里的 token，后续生成以它为条件；错误在便宜的时候暴露 |
| 任务拆小、做完一件开新对话 | 长上下文里注意力被稀释（context rot），失败的尝试会持续干扰后面 |
| 写 `AGENTS.md` / rules | 稳定的前缀，代替每次口头交代；还能命中 prompt cache（第六课） |
| 给测试、让它跑测试 | 第二课 `--no-verify` 的反面：外部信号代替自我感觉 |
| 直接指明文件路径 | 省掉一轮检索，也避免它读到同名的错误文件 |
| 让子 agent 去搜索 | 搜索的大量中间结果留在子 agent 里，主上下文只收结论 |
| 给截图 | 模型读不到渲染结果，文字描述 UI 丢失的信息太多 |
| 给错误日志全文，而不是“报错了” | 日志里的文件名、行号是最准的检索线索 |

## 移动端特有的坑

agent 在移动端通常不如 Web / 后端稳定。原因都能用“上下文里缺了什么”解释：

| 现象 | 原因 | 对策 |
| --- | --- | --- |
| 写出已废弃的 API | 训练数据里旧版本多，且有知识截止 | rules 写明 SDK 版本；用 MCP 或直接贴官方文档 |
| 编造 pub 包 / 方法名 | 幻觉：补全“看起来合理的”名字 | 要求先读 `pubspec.yaml`、查文档，再写代码 |
| UI 改完不对 | 看不到屏幕 | 给截图；让它跑 widget test / golden test |
| 改了 Dart 忘了原生侧 | platform channel 横跨 Dart / Kotlin / Swift，另两端不在上下文里 | 明确列出三端要改的文件 |
| 乱改生成代码 | 分不清 `*.g.dart`、`*.freezed.dart` 是生成的 | rules 写明“不改生成文件，改完跑 build_runner” |
| 构建报错来回修 | 没有可验证反馈，靠猜 | 每次改完跑 `flutter analyze` 和对应测试 |
| iOS 签名 / Gradle 配置乱改 | 这类配置高度依赖本机环境，模型看不到 | rules 里列为“不要改，改前先问” |

## 动手

1. 复制 [templates/AGENTS.flutter.md](../templates/AGENTS.flutter.md) 到你的项目根目录，改成 `AGENTS.md`，填完。
2. 挑一个 agent 在你们项目里常做砸的任务。**不换模型，只改上下文**（rules、给的文件、给的测试、截图），
   前后各跑一次，记录差异。

## 这一课结束的标准

- 能列出上下文的六个来源，指出哪些是你能控制的
- 你的项目里有一份提交了的 `AGENTS.md`
- 有一次“只改上下文就变好了”的前后对比记录

## 下一步

[04-verify-and-eval.md](04-verify-and-eval.md)
