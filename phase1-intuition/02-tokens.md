# 02. Token 到底是什么

模型不读字，也不读词。它读 **token**。

Token 是固定词表里的一块文本，例如：

- 常见整词：`the`
- 子词：`ing`、`language`
- 标点：`,`
- 一个汉字，或很短的中文词
- 代码碎片：`def`、`()`、`!=`

上一课的聊天 prompt，对模型来说也只是一串 token id。

## 为什么不用空格分词？

空格分词看起来友好，立刻就会坏：

- 英语：`don't` / `dont` / `do not`
- 代码：`userId` vs `user_id`
- 中文：没有空格
- 新词、人名、新 API：全是“未知词”

BPE / SentencePiece 从高频碎片组词表。任何字符串都能表示；常见片段便宜，罕见片段拆细。

## 自己看

```bash
python3 src/tokenize_demo.py
python3 src/tokenize_demo.py --text "User: Why can it chat?"
python3 src/tokenize_demo.py --text "大语言模型第一课"
```

本仓库的 tiny BPE 只是显微镜，用来看 merge 发生。装 `tiktoken` 才能对比生产词表（如 `cl100k_base`）。

## 和下一课的关系

计费、截断、上下文窗口，单位都是 token：

- prompt tokens：你送进去的
- completion tokens：模型写出来的
- context window：两者加起来的硬顶

经验数量级（英语，很粗）：1 token ≈ 4 个字符 ≈ 0.75 个词。中文、代码、JSON 通常更贵。

“模型忽略了 PDF 后半段”常常是 token 预算问题，不是它决定不看。

## 这一课结束的标准

能解释：聊天 JSON、中文句子、一段 Python，对模型都是 token 序列；后面的 Embedding 吃的是这些 id，不是“意思”。
