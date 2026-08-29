#!/usr/bin/env python3
"""Phase 1 demo: a language model is a next-token machine.

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
import random
from pathlib import Path

from bigram import CharBigramLM as BigramLM, load_text as load_corpus


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "data" / "tiny_corpus.txt"


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
