# 01. 为什么只会预测下一个 token，却能聊天？

今天不讲 Transformer 是什么。

先把这个悖论钉死：

> 大语言模型在训练和推理时，做的都是同一件事——给定已经出现的 token，预测下一个 token。
> 但它看起来会聊天、会写代码、会拒绝、会“思考”。

如果你把这句话当成口号，后面 Attention、KV Cache、LoRA 都会变成零散知识点。
如果你把它当成**机制**，后面整条链都会顺。

## 聊天不是另一种能力

把一次对话写成纯文本，它只是字符串：

```text
User: Why can it chat?
Assistant:
```

光标停在 `Assistant:` 后面。模型要做的，不是“进入聊天模式”，而是：

```text
prompt  →  给词表里每个 token 打分
        →  选出一个
        →  接到 prompt 后面
        →  重复，直到停止
```

停止条件也很普通：结束符、长度上限、或者碰到你设的 stop string。

托管 Chat API 看起来像新产品，服务器端只是把 JSON 消息列表拼成上面这种字符串，然后跑同一个循环。

自己看一遍：

```bash
python3 src/chat_as_completion.py
python3 src/chat_as_completion.py --question "What is a token?"
```

脚本会打印三样东西：

1. API 那种 `messages` JSON
2. 拼出来的、以 `Assistant:` 结尾的 prompt
3. 玩具模型在后面续写的内容

玩具模型的回复会很笨。这正是重点：**接口已经是聊天，质量只是更好的 next-token。**

## 那“智能”从哪来？

同一个循环，三种不同的东西叠在上面，看起来就像智能：

| 看起来像 | 实际发生的事 |
| --- | --- |
| 在跟你对话 | 训练数据里有大量对话；推理时 prompt 被排成对话格式 |
| 听得懂指令 | Instruction fine-tuning 让 `Assistant:` 后面更像“有用的回答” |
| 在思考 | 先采样出隐藏的推理 token，再采样可见答案。仍然是 next-token |
| 在查知识 | 在补全“这种问题后面通常接什么”。不是查表 |

所以：

- 流利 ≠ 真
- 会聊天 ≠ 另有一个对话引擎
- RAG / Tool / Agent 以后会加进来，但它们都是给这个循环**换上下文**，不是换目标函数

幻觉也是同一套机制：如果某种问题在训练里常常跟着一段流畅的解释，模型就会续上一段流畅的解释，哪怕事实不存在。

## 玩具模型和 GPT 差在哪？

本仓库的词级 bigram **只看前一个词**。所以它很快跑题。

GPT 做的是同一件事，只是每次预测时能看见**整段 prompt**：

```text
一句话
  → Tokenizer
  → token id
  → Embedding
  → Attention
  → Transformer Block × N
  → logits
  → 预测下一个 token
```

这一条链不是另一门课。它是在回答：

> 怎样才能把 next-token 这件事做好？

- Tokenizer：模型读的单位
- Embedding：token 如何变成可计算的向量
- Attention：当前 token 如何从上下文里把有用信息取回来
- Block × N：把“看上下文 + 变换”重复到足够深
- logits：词表上的分数，采样出下一个 token

**现在不要把这条链背下来。** 只要知道：它们全是为 next-token 服务的。Karpathy 视频会把这条链写出来；`LLMs-from-scratch` 会把每一层讲透。

## 这一课结束的标准

能不看笔记说出下面这段，再进入 02：

> 聊天是一种 prompt 格式。模型在 `Assistant:` 后面反复采样下一个 token。
> 没有单独的聊天大脑。更好的模型只是在同一种循环里，看见了更长的上下文、学到了更好的统计。

## 下一步

1. [02-tokens.md](02-tokens.md) — 模型读的不是字，也不是词
2. [03-generation-loop.md](03-generation-loop.md) — 采样、temperature、上下文窗口
3. [04-watch-karpathy.md](04-watch-karpathy.md) — 跟视频手写 tiny GPT，先不要啃 nanoGPT 源码

这一阶段不要碰 RAG、Agent、LoRA。它们会在第三阶段、等你写过 Attention 之后再出现。
