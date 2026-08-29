# 01. What is a large language model?

A **large language model** (LLM) is a neural network trained to do one job:

> Given some text, predict the next token.

That sentence is the whole course in miniature. Chatbots, coding agents, and
"reasoning" models are all the same loop with better data, more parameters,
and extra scaffolding around the loop.

## What it is not

| People often say | What is actually happening |
| --- | --- |
| "It understands me" | It assigns high probability to replies that looked like good continuations in training |
| "It looks up knowledge" | It reconstructs patterns that were common in the training text |
| "It thinks, then speaks" | Hidden tokens are generated first (a chain of thought), then the visible answer |
| "It is a database" | Databases retrieve. Models **complete** |

Keep the distinction. Retrieval can be added later (RAG, tools, search).
The model itself still only emits the next token.

## The generation loop

```
prompt  →  model scores every token in the vocab
        →  pick one token (greedy or sample)
        →  append it to the prompt
        →  repeat until a stop condition
```

Stop conditions are ordinary:

- an end-of-sequence token
- a max-token budget
- a stop string you configured

There is no separate "thinking engine" behind this loop. If a model writes
`Let's think step by step`, that text is also sampled tokens.

## Scale, briefly

Three knobs made today's models useful:

1. **Parameters** — billions of weights that store the patterns.
2. **Data** — web text, books, code, conversations.
3. **Compute** — the cost of one training run.

You do not need the architecture diagram on day one. You need the loop.
The architecture (a Transformer) is a very good way to look at the whole
prompt at once before scoring the next token. Lesson 01 stops there.

## What you will do in this lesson

1. See that models read **tokens**, not words. (`src/tokenize_demo.py`)
2. Train a toy next-token model and sample from it. (`src/next_token_demo.py`)
3. Optionally send one real prompt to Grok / any OpenAI-compatible API.

When those three feel obvious, you already have the right mental model.
Later lessons (prompting, tools, RAG, fine-tuning) are all variations on it.
