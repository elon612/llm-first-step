#!/usr/bin/env python3
"""Lesson 01: chatting is next-token prediction on a formatted prompt.

A chat API looks like a product. Underneath, the server turns the message
list into a string that ends with the assistant role, then predicts the
next token again and again.

This toy word-bigram makes the format visible. The reply will be clumsy.
That is the point: the interface is already chat. Quality is just better
next-token prediction.

    python3 src/chat_as_completion.py
    python3 src/chat_as_completion.py --question "What is a token?"
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIALOGUES = ROOT / "data" / "tiny_dialogues.txt"
WORD_RE = re.compile(r"User:|Assistant:|\n|[^\s]+", re.MULTILINE)


def format_chat(question: str, history: list[tuple[str, str]] | None = None) -> str:
    """Turn a conversation into the raw string a completer would see."""
    lines: list[str] = []
    for role, text in history or []:
        lines.append(f"{role}: {text}")
    lines.append(f"User: {question}")
    lines.append("Assistant:")
    return "\n".join(lines) + " "


def messages_payload(question: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "You are a concise tutor. Chat is next-token prediction.",
        },
        {"role": "user", "content": question},
    ]


def tokenize_words(text: str) -> list[str]:
    return WORD_RE.findall(text)


class WordBigramLM:
    """P(next_word | current_word). Same loop as GPT, almost no context."""

    def __init__(self, counts: dict[str, collections.Counter[str]]) -> None:
        self.counts = counts
        self.vocab = sorted({w for row in counts.values() for w in row} | set(counts))

    @classmethod
    def train(cls, text: str) -> "WordBigramLM":
        tokens = tokenize_words(text)
        counts: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
        for a, b in zip(tokens, tokens[1:]):
            counts[a][b] += 1
        return cls(counts)

    def generate(
        self,
        prompt: str,
        steps: int = 24,
        temperature: float = 0.7,
        greedy: bool = False,
        rng: random.Random | None = None,
    ) -> str:
        rng = rng or random.Random()
        tokens = tokenize_words(prompt) or ["Assistant:"]
        generated: list[str] = []
        last = tokens[-1]
        for _ in range(steps):
            dist = self._probs(last, 0.01 if greedy else temperature)
            nxt = _pick(dist, greedy, rng)
            if generated and nxt in {"User:", "Assistant:"}:
                break
            generated.append(nxt)
            last = nxt
        return prompt + _detokenize(generated)

    def _probs(self, last: str, temperature: float) -> dict[str, float]:
        row = self.counts.get(last)
        if not row:
            if not self.vocab:
                return {}
            uniform = 1.0 / len(self.vocab)
            return {item: uniform for item in self.vocab}
        temperature = max(temperature, 1e-6)
        logits = {item: math.log(count) / temperature for item, count in row.items()}
        peak = max(logits.values())
        exps = {item: math.exp(logit - peak) for item, logit in logits.items()}
        total = sum(exps.values())
        return {item: value / total for item, value in exps.items()}


def _detokenize(tokens: list[str]) -> str:
    parts: list[str] = []
    for tok in tokens:
        if tok == "\n":
            parts.append("\n")
        elif tok in {"User:", "Assistant:"}:
            if parts and not parts[-1].endswith("\n"):
                parts.append("\n")
            parts.append(tok + " ")
        else:
            if parts and not parts[-1].endswith((" ", "\n")):
                parts.append(" ")
            parts.append(tok)
    return "".join(parts)


def _pick(dist: dict[str, float], greedy: bool, rng: random.Random) -> str:
    if not dist:
        return ""
    if greedy:
        return max(dist.items(), key=lambda item: item[1])[0]
    items, weights = zip(*dist.items())
    return rng.choices(items, weights=weights, k=1)[0]


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
    model = WordBigramLM.train(args.corpus.read_text(encoding="utf-8"))
    reply_full = model.generate(
        prompt,
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
