#!/usr/bin/env python3
"""Checks templates/fail_first_check.sh against throwaway git repos."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "templates" / "fail_first_check.sh"

BUGGY = "def total(items):\n    return sum(p for p, q in items)\n"
FIXED = "def total(items):\n    return sum(p * q for p, q in items)\n"

TEST_HEADER = (
    "import sys, pathlib\n"
    "sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))\n"
    "from cart import total\n"
)
BEHAVIOUR_TEST = TEST_HEADER + "assert total([(2, 3)]) == 6\n"
TAUTOLOGY_TEST = TEST_HEADER + "assert callable(total)\n"

ENV = {
    "TEST_PATH_RE": r"(^|/)tests/test_.*\.py$",
    "TEST_SUPPORT_RE": r"(^|/)tests/",
    "SRC_PATH_RE": r"(^|/)src/.*\.py$",
    "RUN_TESTS": "python3",
}


@unittest.skipUnless(shutil.which("git") and shutil.which("bash"), "needs git and bash")
class FailFirstCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")
        self.write("src/cart.py", BUGGY)
        self.commit("buggy cart")
        self.git("checkout", "-q", "-b", "fix")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def git(self, *args: str) -> None:
        subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True)

    def write(self, rel: str, text: str) -> None:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit(self, message: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def check(self, **extra: str) -> subprocess.CompletedProcess[str]:
        env = {**os.environ, **ENV, **extra}
        return subprocess.run(
            ["bash", str(SCRIPT), "main"], cwd=self.repo, env=env, capture_output=True, text=True
        )

    def test_behaviour_test_that_fails_before_fix_passes_gate(self) -> None:
        self.write("src/cart.py", FIXED)
        self.write("tests/test_cart.py", BEHAVIOUR_TEST)
        self.commit("fix quantity")
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("在改动前失败", result.stdout)

    def test_tautology_that_passes_before_fix_is_rejected(self) -> None:
        self.write("src/cart.py", FIXED)
        self.write("tests/test_cart.py", TAUTOLOGY_TEST)
        self.commit("fix quantity")
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("tests/test_cart.py", result.stdout)

    def test_tests_only_change_is_skipped(self) -> None:
        self.write("tests/test_cart.py", TAUTOLOGY_TEST)
        self.commit("characterise cart")
        result = self.check()
        self.assertEqual(result.returncode, 0)
        self.assertIn("没有实现改动", result.stdout)

    def test_skip_trailer_is_honoured(self) -> None:
        self.write("src/cart.py", FIXED)
        self.write("tests/test_cart.py", TAUTOLOGY_TEST)
        self.commit("refactor cart\n\nFail-First: skip pure rename")
        result = self.check()
        self.assertEqual(result.returncode, 0)
        self.assertIn("pure rename", result.stdout)

    def test_missing_test_warns_or_fails(self) -> None:
        self.write("src/cart.py", FIXED)
        self.commit("fix without test")
        self.assertEqual(self.check().returncode, 0)
        self.assertEqual(self.check(REQUIRE_TEST="1").returncode, 1)

    def test_worktree_is_cleaned_up(self) -> None:
        self.write("src/cart.py", FIXED)
        self.write("tests/test_cart.py", BEHAVIOUR_TEST)
        self.commit("fix quantity")
        self.check()
        listing = subprocess.run(
            ["git", "worktree", "list"], cwd=self.repo, capture_output=True, text=True
        ).stdout
        self.assertEqual(len(listing.strip().splitlines()), 1, listing)


if __name__ == "__main__":
    unittest.main()
