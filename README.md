# llm-first-step

**Large language models, first lesson.**
大模型学习第一课：token、下一个 token 预测、以及你的第一次 API 调用。

This repository is a single sitting. After it, "the model answered me" should
feel like: *the model sampled tokens until it decided to stop*.

## What you will learn

1. An LLM is a **next-token machine**, not a database.
2. Models read **tokens**, not words. Chinese, code, and punctuation have their own costs.
3. **Temperature** reshapes the next-token distribution.
4. A chat API is that same loop behind HTTP.

## Layout

```
llm-first-step/
├── lessons/                 # read in order, 01 → 05
│   ├── 01-what-is-an-llm.md
│   ├── 02-tokens.md
│   ├── 03-next-token-prediction.md
│   ├── 04-first-api-call.md
│   └── 05-prompting-basics.md
├── src/
│   ├── tokenize_demo.py     # characters vs words vs tiny BPE vs tiktoken
│   ├── next_token_demo.py   # train a bigram LM, print top-k, generate
│   └── chat_hello.py        # live call to xAI Grok / OpenAI-compatible APIs
├── exercises/01-warmup.md
├── data/tiny_corpus.txt
└── tests/test_lesson01.py
```

## Setup

Python 3.10+ is enough for the offline demos. They use the standard library.

```bash
git clone https://github.com/elon612/llm-first-step.git
cd llm-first-step
```

Optional extras (real tokenizer + live API):

```bash
python3 -m pip install -r requirements.txt
cp .env.example .env
# put XAI_API_KEY=... into .env
```

## Run the lesson

```bash
# 1. Read lessons/01-what-is-an-llm.md

# 2. See tokens
python3 src/tokenize_demo.py
python3 src/tokenize_demo.py --text "大语言模型第一课"

# 3. Feel next-token prediction
python3 src/next_token_demo.py
python3 src/next_token_demo.py --prompt "The little cat" --greedy

# 4. Optional live call
python3 src/chat_hello.py

# 5. Do exercises/01-warmup.md
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

No API key is required. The tests cover BPE merges, probability normalization,
greedy determinism, and temperature.

## Mental model

```
prompt  →  score every token  →  pick one  →  append  →  repeat
```

The toy model looks at **one previous character**. A Transformer looks at
**the whole prompt**. Same loop, better context. That is the jump from
`next_token_demo.py` to Grok.

## 中文速览

- 大模型不是在查表，是在续写。
- 计费和截断的单位是 token，不是字，也不是词。
- temperature 低 → 更稳、更重复；高 → 更散、更容易胡说。
- Chat API 的 `messages` 只是把对话格式化成提示词。
- 先跑通离线两个 demo，再花 API 额度。

## License

MIT. See [LICENSE](LICENSE).
