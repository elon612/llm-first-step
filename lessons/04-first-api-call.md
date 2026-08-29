# 04. Your first API call

A hosted LLM is the generation loop behind an HTTP endpoint.

Most vendors speak the OpenAI **Chat Completions** shape:

```json
{
  "model": "grok-4",
  "temperature": 0.3,
  "messages": [
    {"role": "system", "content": "You are a precise teaching assistant."},
    {"role": "user",   "content": "What is a token?"}
  ]
}
```

The response contains:

- `choices[0].message.content` — the sampled text
- `usage.prompt_tokens` / `completion_tokens` — the bill
- `finish_reason` — `stop`, `length`, or a safety/filter reason

## Roles

| Role | Job |
| --- | --- |
| `system` | Standing instructions. Applied for the whole call |
| `user` | This turn's request |
| `assistant` | Previous model replies, if you are keeping a thread |

A "chat" is not a special brain. It is the prompt formatted as a message
list, then fed into the same next-token loop.

## Run it

```bash
cp .env.example .env
# put XAI_API_KEY=... into .env

pip install -r requirements.txt
python3 src/chat_hello.py
python3 src/chat_hello.py --prompt "Explain temperature like I am 15."
```

The script prefers **xAI Grok** when `XAI_API_KEY` is set, and falls back to
any OpenAI-compatible base URL. Offline lessons do not need a key.

## What to look at besides the text

1. `usage` — compare it with `tokenize_demo.py` on the same sentence.
2. `temperature` — rerun the same prompt at `0.0` and `1.2`.
3. The system message — delete it and see the style change.
4. Failures — wrong key, wrong model name, and context overflow all show up
   as ordinary HTTP errors. Read the body. Do not retry blindly.

## Safety note

This repository never commits `.env`. Treat keys like passwords. If a key
leaks into git history, rotate it on the vendor dashboard immediately.
