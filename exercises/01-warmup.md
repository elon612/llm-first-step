# Exercise 01 — Warmup

Do the offline work first. The API call is optional.

## A. Tokens

1. Run `python3 src/tokenize_demo.py --text "Hello world"`.
2. Run it again on `"你好世界"` and `"hello_world()"`.
3. Write down, in one line each:
   - which string used the most characters
   - which string would likely cost the most tokens on a real model
4. Extra: install `tiktoken` and compare the tiny BPE with `cl100k_base`.

## B. Next token

1. Run `python3 src/next_token_demo.py --prompt "The little cat" --greedy`.
2. Run the same prompt with `--temperature 1.2` (not greedy).
3. Answer:
   - Why does greedy text loop or collapse?
   - Why does the toy model forget the topic after a few words?
   - What would a Transformer change about that?

## C. Prompt as context

Rewrite the prompt `"介绍一下大模型"` into **three** prompts:

1. 80 words, for a product manager, no jargon.
2. 5 bullets, for a backend engineer, mention tokens and temperature.
3. A JSON object with keys `definition`, `loop`, `limitation`.

If you have an API key, send all three through `src/chat_hello.py`.

## D. Self-check

You are done with lesson 01 when you can say this out loud without notes:

> An LLM does not look up answers. It repeatedly samples the next token
> from a distribution conditioned on the prompt. Tokens are subword pieces.
> Temperature reshapes that distribution. The context window is a hard cap.
