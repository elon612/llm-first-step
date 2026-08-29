#!/usr/bin/env python3
"""Phase 1 demo: what a token actually is.

Run:
    python3 src/tokenize_demo.py
    python3 src/tokenize_demo.py --text "Hello, 大模型"
"""

from __future__ import annotations

import argparse
import collections
import json


def naive_word_tokens(text: str) -> list[str]:
    """Split on whitespace. Looks simple. Breaks on punctuation and CJK."""
    return text.split()


def char_tokens(text: str) -> list[str]:
    return list(text)


class TinyBPE:
    """A tiny byte-pair encoder so you can watch merges happen.

    Real models use a much larger vocabulary (50k–200k tokens) trained on
    terabytes of text. The algorithm is the same idea: start from characters
    (or bytes), repeatedly merge the most common adjacent pair.
    """

    def __init__(self, merges: list[tuple[str, str]]) -> None:
        self.merges = merges
        self.merge_ranks = {pair: i for i, pair in enumerate(merges)}

    @classmethod
    def train(cls, text: str, num_merges: int = 40) -> "TinyBPE":
        tokens = list(text)
        merges: list[tuple[str, str]] = []
        for _ in range(num_merges):
            if len(tokens) < 2:
                break
            counts = collections.Counter(zip(tokens, tokens[1:]))
            pair, freq = counts.most_common(1)[0]
            if freq < 2:
                break
            merges.append(pair)
            tokens = _apply_merge(tokens, pair)
        return cls(merges)

    def encode(self, text: str) -> list[str]:
        tokens = list(text)
        for pair in self.merges:
            tokens = _apply_merge(tokens, pair)
        return tokens


def _apply_merge(tokens: list[str], pair: tuple[str, str]) -> list[str]:
    a, b = pair
    merged: list[str] = []
    i = 0
    while i < len(tokens):
        if i + 1 < len(tokens) and tokens[i] == a and tokens[i + 1] == b:
            merged.append(a + b)
            i += 2
        else:
            merged.append(tokens[i])
            i += 1
    return merged


def try_tiktoken(text: str) -> dict | None:
    try:
        import tiktoken
    except ImportError:
        return None
    encoding = tiktoken.get_encoding("cl100k_base")
    ids = encoding.encode(text)
    pieces = [encoding.decode([i]) for i in ids]
    return {
        "encoding": "cl100k_base (GPT-4 / many OpenAI-compatible models)",
        "token_count": len(ids),
        "ids": ids,
        "pieces": pieces,
    }


def compare(text: str) -> dict:
    words = naive_word_tokens(text)
    chars = char_tokens(text)
    bpe = TinyBPE.train(text, num_merges=40)
    bpe_tokens = bpe.encode(text)
    report = {
        "text": text,
        "char_count": len(chars),
        "naive_word_count": len(words),
        "tiny_bpe_count": len(bpe_tokens),
        "naive_words": words,
        "tiny_bpe_tokens": bpe_tokens,
        "tiny_bpe_merges": ["+".join(pair) for pair in bpe.merges[:12]],
        "tiktoken": try_tiktoken(text),
    }
    return report


def print_report(report: dict) -> None:
    print("=" * 64)
    print("INPUT")
    print(report["text"])
    print("-" * 64)
    print(f"characters        : {report['char_count']}")
    print(f"naive words       : {report['naive_word_count']}")
    print(f"tiny BPE tokens   : {report['tiny_bpe_count']}")
    if report["tiktoken"]:
        print(f"tiktoken tokens   : {report['tiktoken']['token_count']}")
    else:
        print("tiktoken tokens   : (install tiktoken to compare with a real vocab)")
    print("-" * 64)
    print("naive words :", report["naive_words"])
    print("tiny BPE    :", report["tiny_bpe_tokens"])
    print("first merges:", report["tiny_bpe_merges"])
    if report["tiktoken"]:
        print("tiktoken    :", report["tiktoken"]["pieces"])
        print("token ids   :", report["tiktoken"]["ids"])
    print()
    print("Takeaway: models do not read words. They read tokens.")
    print("Chinese, code, and punctuation usually cost more tokens than English.")
    print("=" * 64)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tokenization demo for LLM lesson 01")
    parser.add_argument(
        "--text",
        default="Hello, large language models! 你好，大语言模型！",
        help="Text to tokenize",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    args = parser.parse_args()
    report = compare(args.text)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
