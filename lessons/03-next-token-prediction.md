# 03. Next-token prediction

Training an LLM is supervised learning with a boring label: **the next token**.

```
Input :  The cat sat on the
Target:  mat
```

Slide the window one token and repeat over the entire internet. The loss is
cross-entropy: how surprised was the model by the true next token?

## Inference is the same objective

At inference time nobody gives the target. The model outputs a probability
distribution over the whole vocabulary, then someone picks a token.

Common picking rules:

| Strategy | Behavior |
| --- | --- |
| greedy (`argmax`) | Always take the top token. Repetitive, stable |
| temperature &lt; 1 | Peakier distribution. More conservative |
| temperature = 1 | Raw model distribution |
| temperature &gt; 1 | Flatter. More surprising, more nonsense |
| top-k / top-p | Ignore the long tail, then sample |

`chat_hello.py` exposes `temperature`. `next_token_demo.py` lets you feel it
on a model small enough to print the full distribution.

## Context is the only memory in the loop

The toy model in this repo is a **bigram**: it only looks at the previous
character. That is why the story collapses after a few words.

A Transformer replaces "previous character" with "the entire prompt":

- every token can attend to every earlier token
- that is why a system message at the top still affects the last answer
- that is also why the context window is a hard wall

Same loop. Better context.

## Hallucination, in this picture

The model is not retrieving a row from a table. It is completing a pattern.
If the prompt *looks like* a question that had a fluent answer in training,
the model will produce a fluent continuation — even when no such fact exists.

So:

- fluency is not evidence
- citations must be checked
- tools and retrieval exist to ground the continuation

## Try it

```bash
python3 src/next_token_demo.py
python3 src/next_token_demo.py --prompt "小猫" --temperature 0.2
python3 src/next_token_demo.py --prompt "The little cat" --greedy
```

Watch the top-8 next characters. Then read the generated text. The gap
between "local statistics" and "a real LLM" is exactly: **how much context
the model can see, and how well those weights were trained**.
