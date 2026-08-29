#!/usr/bin/env python3
"""Lesson 01 demo: a language model is a next-token machine.

This is a character-level bigram model. It is tiny on purpose.
After you run it, you will have felt the three operations every LLM does:

1. score the next piece given the context
2. pick one piece (greedy, or sample with temperature)
3. append it and repeat

Run:
    python3 src/next_token_demo.py
    python3 src/next_token_demo.py --prompt "The little cat" --temperature 0.8
"""

from __future__ import annotations

import argparse
import collections
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "data" / "tiny_corpus.txt"


class BigramLM:
    """P(next_char | current_char) estimated by counting."""

    def __init__(self, counts: dict[str, collections.Counter[str]]) -> None:
        self.counts = counts
        self.vocab = sorted({ch for row in counts.values() for ch in row} | set(counts))

    @classmethod
    def train(cls, text: str) -> "BigramLM":
        counts: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
        for a, b in zip(text, text[1:]):
            counts[a][b] += 1
        return cls(counts)

    def probs(self, context: str, temperature: float = 1.0) -> dict[str, float]:
        last = context[-1] if context else " "
        row = self.counts.get(last)
        if not row:
            uniform = 1.0 / len(self.vocab)
            return {ch: uniform for ch in self.vocab}

        # Convert counts to a temperature-scaled distribution.
        # temperature -> 0  = greedy (peaky)
        # temperature = 1   = the raw frequencies
        # temperature > 1   = flatter / more random
        temperature = max(temperature, 1e-6)
        logits = {ch: math.log(count) / temperature for ch, count in row.items()}
        max_logit = max(logits.values())
        exps = {ch: math.exp(logit - max_logit) for ch, logit in logits.items()}
        total = sum(exps.values())
        return {ch: value / total for ch, value in exps.items()}

    def top_k(self, context: str, k: int = 8, temperature: float = 1.0) -> list[tuple[str, float]]:
        ranked = sorted(self.probs(context, temperature).items(), key=lambda item: -item[1])
        return ranked[:k]

    def generate(
        self,
        prompt: str,
        steps: int = 80,
        temperature: float = 0.8,
        greedy: bool = False,
        rng: random.Random | None = None,
    ) -> str:
        rng = rng or random.Random()
        text = prompt
        for _ in range(steps):
            dist = self.probs(text, temperature=0.01 if greedy else temperature)
            if greedy:
                nxt = max(dist.items(), key=lambda item: item[1])[0]
            else:
                chars, weights = zip(*dist.items())
                nxt = rng.choices(chars, weights=weights, k=1)[0]
            text += nxt
        return text


def load_corpus(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Corpus not found: {path}")
    return path.read_text(encoding="utf-8")


def print_topk(model: BigramLM, prompt: str, temperature: float) -> None:
    print("=" * 64)
    print(f"PROMPT: {prompt!r}")
    print(f"temperature = {temperature}")
    print("-" * 64)
    print("Most likely next characters:")
    for ch, p in model.top_k(prompt, k=8, temperature=temperature):
        visible = ch.replace("\n", "\\n")
        bar = "#" * max(1, int(p * 40))
        print(f"  {visible!r:6}  {p:6.1%}  {bar}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tiny next-token language model")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--prompt", default="The little cat")
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--greedy", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    corpus = load_corpus(args.corpus)
    model = BigramLM.train(corpus)
    print_topk(model, args.prompt, args.temperature)

    rng = random.Random(args.seed)
    sample = model.generate(
        args.prompt,
        steps=args.steps,
        temperature=args.temperature,
        greedy=args.greedy,
        rng=rng,
    )
    print("-" * 64)
    print("GENERATED TEXT")
    print(sample)
    print("-" * 64)
    print("This model only looks at 1 previous character, so the story falls apart.")
    print("A Transformer looks at the whole prompt at once. Same loop, much better context.")
    print("=" * 64)


if __name__ == "__main__":
    main()
