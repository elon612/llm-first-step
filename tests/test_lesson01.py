#!/usr/bin/env python3
"""Offline checks for phase 1. No API key required."""

from __future__ import annotations

import math
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bigram import CharBigramLM, WordBigramLM, load_text, tokenize_words  # noqa: E402
from chat_as_completion import format_chat, messages_payload  # noqa: E402
from next_token_demo import BigramLM, load_corpus  # noqa: E402
from tokenize_demo import TinyBPE, compare  # noqa: E402


class ChatFormatTests(unittest.TestCase):
    def test_prompt_ends_with_assistant_role(self) -> None:
        prompt = format_chat("What is a token?")
        self.assertTrue(prompt.rstrip().endswith("Assistant:"))
        self.assertIn("User: What is a token?", prompt)

    def test_history_is_inlined(self) -> None:
        prompt = format_chat("Follow up", history=[("User", "Hi"), ("Assistant", "Hello")])
        self.assertIn("User: Hi", prompt)
        self.assertIn("Assistant: Hello", prompt)
        self.assertTrue(prompt.rstrip().endswith("Assistant:"))

    def test_api_payload_is_messages(self) -> None:
        payload = messages_payload("Why can it chat?")
        self.assertEqual(payload[-1]["role"], "user")
        self.assertEqual(payload[-1]["content"], "Why can it chat?")


class WordBigramTests(unittest.TestCase):
    def test_keeps_role_markers(self) -> None:
        tokens = tokenize_words("User: Hello\nAssistant: Hi")
        self.assertIn("User:", tokens)
        self.assertIn("Assistant:", tokens)

    def test_continues_after_assistant(self) -> None:
        corpus = load_text(ROOT / "data" / "tiny_dialogues.txt")
        model = WordBigramLM.train(corpus)
        prompt = format_chat("What is a token?")
        out = model.generate(prompt, steps=12, greedy=True)
        self.assertTrue(out.startswith(prompt))
        self.assertGreater(len(out), len(prompt))


class TokenizeTests(unittest.TestCase):
    def test_bpe_shortens_repeated_text(self) -> None:
        text = "abababababab"
        bpe = TinyBPE.train(text, num_merges=4)
        encoded = bpe.encode(text)
        self.assertLess(len(encoded), len(text))
        self.assertEqual("".join(encoded), text)

    def test_compare_counts(self) -> None:
        report = compare("Hello world")
        self.assertEqual(report["char_count"], len("Hello world"))
        self.assertEqual(report["naive_word_count"], 2)
        self.assertGreaterEqual(report["tiny_bpe_count"], 1)


class NextTokenTests(unittest.TestCase):
    def test_probs_sum_to_one(self) -> None:
        model = BigramLM.train("the cat sat on the mat")
        probs = model.probs("the")
        self.assertAlmostEqual(sum(probs.values()), 1.0, places=6)

    def test_char_alias_matches_export(self) -> None:
        self.assertIs(BigramLM, CharBigramLM)

    def test_deterministic_greedy(self) -> None:
        corpus = load_corpus(ROOT / "data" / "tiny_corpus.txt")
        model = BigramLM.train(corpus)
        a = model.generate("The little cat", steps=20, greedy=True)
        b = model.generate("The little cat", steps=20, greedy=True)
        self.assertEqual(a, b)
        self.assertTrue(a.startswith("The little cat"))

    def test_sampling_is_seeded(self) -> None:
        model = BigramLM.train("aaaaabbbbbccccc")
        one = model.generate("a", steps=10, temperature=1.0, rng=random.Random(0))
        two = model.generate("a", steps=10, temperature=1.0, rng=random.Random(0))
        self.assertEqual(one, two)

    def test_low_temperature_is_peakier(self) -> None:
        model = BigramLM.train("ab" * 40 + "ac" * 5)
        cold = model.probs("a", temperature=0.2)
        hot = model.probs("a", temperature=2.0)
        self.assertGreater(max(cold.values()), max(hot.values()))
        self.assertTrue(all(math.isfinite(p) for p in cold.values()))


if __name__ == "__main__":
    unittest.main()
