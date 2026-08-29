#!/usr/bin/env python3
"""Phase 1, lesson 01: chatting is next-token prediction on a formatted prompt.

A hosted chat API looks like a new product. Underneath, the server turns the
message list into a token string that ends with the assistant role, then runs
the ordinary generation loop.

This script makes that visible with a toy word-bigram. The replies will be
clumsy. That is the point: the *interface* is already chat. Quality is just
better next-token prediction.

Run:
    python3 src/chat_as_completion.py
    python3 src/chat_as_completion.py --question "What is a token?"
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bigram import WordBigramLM, load_text  # noqa: E402

DEFAULT_DIALOGUES = ROOT / "data" / "tiny_dialogues.txt"


def format_chat(question: str, history: list[tuple[str, str]] | None = None) -> str:
    """Turn a conversation into the raw string a completer would see."""
    lines: list[str] = []
    for role, text in history or []:
        lines.append(f"{role}: {text}")
    lines.append(f"User: {question}")
    lines.append("Assistant:")
    return "\n".join(lines) + " "


def messages_payload(question: str) -> list[dict[str, str]]:
    """The JSON a Chat Completions API actually receives."""
    return [
        {
            "role": "system",
            "content": "You are a concise tutor. Chat is next-token prediction.",
        },
        {"role": "user", "content": question},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Show that chat is completion")
    parser.add_argument("--question", default="Why can it chat?")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_DIALOGUES)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--greedy", action="store_true")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    prompt = format_chat(args.question)
    model = WordBigramLM.train(load_text(args.corpus))
    reply_full = model.generate(
        prompt,
        steps=24,
        temperature=args.temperature,
        greedy=args.greedy,
        rng=random.Random(args.seed),
    )
    continuation = reply_full[len(prompt) :].strip()
    payload = messages_payload(args.question)

    if args.json:
        print(
            json.dumps(
                {
                    "question": args.question,
                    "prompt": prompt,
                    "continuation": continuation,
                    "chat_api_messages": payload,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    print("=" * 64)
    print("1. A chat API looks like this JSON")
    print("-" * 64)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print()
    print("2. The server turns it into a string that ends with the assistant role")
    print("-" * 64)
    print(prompt.rstrip() + " █")
    print()
    print("3. Then it only predicts the next token, again and again")
    print("-" * 64)
    print(continuation or "(empty continuation)")
    print()
    print("This toy model looks at one previous word, so the reply is clumsy.")
    print("GPT does the same loop with the whole prompt in context.")
    print("There is no extra 'chat brain'. Chat is a prompt format.")
    print("=" * 64)


if __name__ == "__main__":
    main()
