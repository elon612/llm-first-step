#!/usr/bin/env python3
"""Offline checks for lesson 01. No API key required."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chat_as_completion import (  # noqa: E402
    WordBigramLM,
    format_chat,
    messages_payload,
    tokenize_words,
)


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
        corpus = (ROOT / "data" / "tiny_dialogues.txt").read_text(encoding="utf-8")
        model = WordBigramLM.train(corpus)
        prompt = format_chat("What is a token?")
        out = model.generate(prompt, steps=12, greedy=True)
        self.assertTrue(out.startswith(prompt))
        self.assertGreater(len(out), len(prompt))


if __name__ == "__main__":
    unittest.main()
