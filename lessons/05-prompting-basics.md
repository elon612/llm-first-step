# 05. Prompting basics (just enough for lesson 01)

A prompt is not a spell. It is the context the next-token machine conditions
on. Better context → better continuation.

## Five patterns that actually move the needle

1. **Task + constraints + output shape**
   > "List 3 risks of temperature &gt; 1. One sentence each. No intro."

2. **Show, don't lecture (few-shot)**
   Give one or two input/output pairs before the real item.

3. **Put the important instruction where it cannot be missed**
   Short system message + a crisp last user line beats a 2,000-word essay.

4. **Separate data from instructions**
   ```
   INSTRUCTIONS: ...
   DATA:
   """ ... """
   ```
   This reduces "the model followed a sentence inside the pasted email".

5. **Ask for a check when the cost of being wrong is high**
   > "If you are not sure, say you are not sure. Do not invent a number."

## Temperature, for writers

- `0.0–0.3`  extraction, classification, code, anything that should be stable
- `0.5–0.8`  explanations, tutoring, brainstorming
- `> 1.0`    only when you *want* drift; expect more nonsense

The toy model in `next_token_demo.py` is the right place to feel this before
you spend API tokens.

## What prompting cannot do

- It cannot add facts the weights never saw (without tools or retrieval).
- It cannot extend the context window.
- It cannot make a 7B model behave like a frontier model on hard reasoning.

When a prompt fails, decide which layer is wrong:

```
bad task spec  →  fix the prompt
missing facts  →  retrieve or tool-call
too hard       →  stronger model / decompose
wrong format   →  show a schema, or use structured output
```

## Mini drill

Rewrite this weak prompt three ways, then send each through `chat_hello.py`:

> "帮我写点关于大模型的。"

Target: one version for a 5-year-old, one for an engineer, one as a 6-row
markdown table. Notice that you changed the **context**, not the model.
