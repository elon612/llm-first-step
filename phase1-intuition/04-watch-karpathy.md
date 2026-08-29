# 04. 跟 Karpathy 把手写出来（先别啃 nanoGPT）

第一阶段的目标不是记公式，是把这条链**写一遍**：

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

## 看什么

主视频：**Andrej Karpathy — Let's build GPT: from scratch, in code, spelled out**

- YouTube: https://www.youtube.com/watch?v=kCc8FmEb1nY
- 配套思路来自他的 [Zero to Hero](https://karpathy.ai/zero-to-hero.html)

这是建立直觉的课。暂停，自己打。不要只看。

## 明确不要做的事

- 不要一上来打开 [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) 从 `train.py` 读到尾。nanoGPT 是给已经懂的人看的极简实现（约 6 万 Star，代码很短），不是教材。
- 不要并行去看 Datawhale、Awesome-LLM、llm-course。它们以后当索引。
- 不要在这一步碰 LoRA、RAG、Agent、vLLM。

跟完视频之后，再打开 nanoGPT，它会突然变得好读：你认得出 tokenizer、embedding、causal attention、block、生成循环各自在哪。

## 看的时候只追这 6 个问题

1. token 到底是什么？（你已经在 02 做过）
2. embedding 为什么能表示语义？
3. Q / K / V 到底在干嘛？
4. attention 为什么能“找上下文”？
5. Transformer Block 在重复做什么？
6. 为什么最终只是预测 next token，却能产生智能？（你已经在 01 回答过机制，现在要看见代码位置）

其中第 3、4 题，请用自己的话回答到这种粒度，再继续：

> 当前 token 用 Q 表达“我想找什么”，
> 其它 token 的 K 表达“我是什么信息”，
> Q·K 决定我要关注谁，
> 最后把对应的 V 加权取回来。

停在 `Q × K → softmax → V` 这一行，不算懂。

## 这一阶段怎么算过

- 自己写出一个能采样下一个字符/token 的 tiny GPT（不必快，不必大）
- 能在纸上画出上面那条链，并指到自己的代码
- 再去浏览 nanoGPT，能说出每个文件在链上的位置

然后进入第二阶段：把 [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) 当主教材，系统补全。见 [`../phase2-from-scratch/`](../phase2-from-scratch/README.md)。
