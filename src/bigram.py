"""Tiny language models for phase 1 labs.

Character bigram: feel next-token sampling and temperature.
Word bigram: feel that a chat reply is just a continuation of a formatted prompt.
Neither is a Transformer. Both run the same loop a GPT runs.
"""

from __future__ import annotations

import collections
import math
import random
import re
from pathlib import Path


class CharBigramLM:
    """P(next_char | current_char) estimated by counting."""

    def __init__(self, counts: dict[str, collections.Counter[str]]) -> None:
        self.counts = counts
        self.vocab = sorted({ch for row in counts.values() for ch in row} | set(counts))

    @classmethod
    def train(cls, text: str) -> "CharBigramLM":
        counts: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
        for a, b in zip(text, text[1:]):
            counts[a][b] += 1
        return cls(counts)

    def probs(self, context: str, temperature: float = 1.0) -> dict[str, float]:
        last = context[-1] if context else " "
        return _softmax_counts(self.counts.get(last), self.vocab, temperature)

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
        stop: str | None = None,
    ) -> str:
        rng = rng or random.Random()
        text = prompt
        for _ in range(steps):
            dist = self.probs(text, temperature=0.01 if greedy else temperature)
            text += _pick(dist, greedy=greedy, rng=rng)
            if stop and text.endswith(stop):
                break
        return text


WORD_RE = re.compile(r"User:|Assistant:|\n|[^\s]+", re.MULTILINE)


def tokenize_words(text: str) -> list[str]:
    """Keep role markers as whole tokens so 'Assistant:' is a real context."""
    return WORD_RE.findall(text)


class WordBigramLM:
    """P(next_word | current_word). Enough to continue a chat template badly."""

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

    def probs(self, last_token: str, temperature: float = 1.0) -> dict[str, float]:
        return _softmax_counts(self.counts.get(last_token), self.vocab, temperature)

    def generate(
        self,
        prompt: str,
        steps: int = 40,
        temperature: float = 0.8,
        greedy: bool = False,
        rng: random.Random | None = None,
        stop_roles: tuple[str, ...] = ("User:", "Assistant:"),
    ) -> str:
        rng = rng or random.Random()
        tokens = tokenize_words(prompt)
        if not tokens:
            tokens = ["Assistant:"]
        generated: list[str] = []
        last = tokens[-1]
        for _ in range(steps):
            dist = self.probs(last, temperature=0.01 if greedy else temperature)
            nxt = _pick(dist, greedy=greedy, rng=rng)
            if generated and nxt in stop_roles:
                break
            generated.append(nxt)
            last = nxt
        return prompt + _detokenize(generated)


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


def _softmax_counts(
    row: collections.Counter[str] | None,
    vocab: list[str],
    temperature: float,
) -> dict[str, float]:
    if not row:
        if not vocab:
            return {}
        uniform = 1.0 / len(vocab)
        return {item: uniform for item in vocab}
    temperature = max(temperature, 1e-6)
    logits = {item: math.log(count) / temperature for item, count in row.items()}
    max_logit = max(logits.values())
    exps = {item: math.exp(logit - max_logit) for item, logit in logits.items()}
    total = sum(exps.values())
    return {item: value / total for item, value in exps.items()}


def _pick(dist: dict[str, float], greedy: bool, rng: random.Random) -> str:
    if not dist:
        return ""
    if greedy:
        return max(dist.items(), key=lambda item: item[1])[0]
    items, weights = zip(*dist.items())
    return rng.choices(items, weights=weights, k=1)[0]


def load_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Corpus not found: {path}")
    return path.read_text(encoding="utf-8")


# Back-compat alias used by the original demo/tests.
BigramLM = CharBigramLM
