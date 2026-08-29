# 02. 跟 Karpathy 把手写出来（先别啃 nanoGPT）

第一课已经回答机制：聊天是 `Assistant:` 后面的 next-token。

接下来不要再开平行教程。看 **Let's build GPT**，把这条链写一遍：

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

**Andrej Karpathy — Let's build GPT: from scratch, in code, spelled out**

- https://www.youtube.com/watch?v=kCc8FmEb1nY
- 系列入口：[Zero to Hero](https://karpathy.ai/zero-to-hero.html)

暂停，自己打。不要只看。代码写进 [tiny-gpt/](tiny-gpt/)，它是这一阶段的核心产出物，要提交进仓库。

这一步是几十小时的投入，和第一课不是一个量级。不要指望一口气跟完——
按 [PROGRESS.md](../PROGRESS.md) 里 02.1 ~ 02.6 的小节推进，每节结束时代码必须能跑，再看下一段视频。
硬件不构成借口：整个视频用 CPU 或免费 Colab 就够，语料只有 1MB 的莎士比亚。

## 不要做的事

- 不要一上来读 [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)。那是给写过 tiny GPT 的人对照的极简实现，不是教材。
- 不要并行打开 Datawhale、Awesome-LLM、llm-course。
- 不要碰 LoRA、RAG、Agent、vLLM。

跟完视频再看 nanoGPT，会认得出 tokenizer、embedding、causal attention、block、generate 各自在哪。

## 只追这 6 个问题

1. token 到底是什么
2. embedding 为什么能表示语义
3. Q / K / V 到底在干嘛
4. attention 为什么能“找上下文”
5. Transformer Block 在重复做什么
6. 为什么最终只是预测 next token，却能产生智能（对照第一课，指到自己的代码）

第 3、4 题要讲到这种粒度，再继续：

> 当前 token 用 Q 表达“我想找什么”，
> 其它 token 的 K 表达“我是什么信息”，
> Q·K 决定我要关注谁，
> 最后把对应的 V 加权取回来。

停在 `Q × K → softmax → V` 这一行，不算懂。

## 这一阶段怎么算过

- 自己写出一个能采样下一个 token 的 tiny GPT
- 能在纸上画出上面那条链，并指到自己的代码
- 再浏览 nanoGPT，能说出每个文件在链上的位置

然后进入第二阶段，只跟 [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)。见 [`../phase2-from-scratch/`](../phase2-from-scratch/README.md)。
