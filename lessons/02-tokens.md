# 02. Tokens are the model's alphabet

Humans read characters and words. Models read **tokens**.

A token is a chunk of text from a fixed vocabulary. It might be:

- a whole common word: `the`
- a subword: `ing`, `tion`, `language`
- punctuation: `,`
- a single CJK character, or a short Chinese word
- a piece of code: `def`, `()`, `!=`

## Why not words?

Word splitting looks friendly and fails immediately:

- English: `don't` / `dont` / `do not`
- Code: `userId` vs `user_id`
- Chinese: there are no spaces
- Rare names and new APIs would be "unknown words"

Subword tokenization (BPE, SentencePiece, Unigram) solves this by building
a vocabulary from frequent pieces. Anything can be expressed. Frequent
phrases become cheap. Rare strings become a sequence of smaller pieces.

## Cost is measured in tokens

APIs bill and truncate in tokens:

- **prompt tokens** — everything you sent, including the system message
- **completion tokens** — everything the model wrote
- **context window** — prompt + completion must fit in this budget

Rule of thumb (rough, English):

- 1 token ≈ 4 characters ≈ 0.75 words
- Chinese usually costs **more tokens per meaning** than English
- Code and JSON can be surprisingly expensive

That is why `usage.prompt_tokens` from `chat_hello.py` will not match your
word count.

## Try it

```bash
python3 src/tokenize_demo.py
python3 src/tokenize_demo.py --text "print(hello_world)"
python3 src/tokenize_demo.py --text "大语言模型第一课"
```

Install `tiktoken` if you want the same vocabulary many production models
use (`cl100k_base`). The tiny BPE in this repo is only a microscope: it
shows merges happening, it is not a production tokenizer.

## Practical consequences

- A long system prompt is not free. It eats the context window on every call.
- Repeating the same documents in the prompt wastes tokens and attention.
- Truncation is silent if you are not looking at `usage`.
- "The model ignored the last part of my PDF" is often a token-budget bug.
