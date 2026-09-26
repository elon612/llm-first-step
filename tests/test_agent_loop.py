#!/usr/bin/env python3
"""Offline checks for lesson 02. No API key required."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent_loop import (  # noqa: E402
    ScriptedModel,
    execute_tool,
    make_sandbox,
    run_agent,
    run_tests,
)


class AgentLoopTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.sandbox = make_sandbox(Path(self._tmp.name) / "repo")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_sandbox_starts_broken(self) -> None:
        ok, _ = run_tests(self.sandbox)
        self.assertFalse(ok)

    def test_verifying_agent_fixes_everything(self) -> None:
        run = run_agent(ScriptedModel(verify=True), self.sandbox)
        ok, _ = run_tests(self.sandbox)
        self.assertTrue(ok)
        self.assertIn("pass", run.final.lower())

    def test_non_verifying_agent_stops_half_fixed(self) -> None:
        run = run_agent(ScriptedModel(verify=False), self.sandbox)
        ok, output = run_tests(self.sandbox)
        self.assertFalse(ok)
        self.assertIn("test_discount_is_a_percentage", output)
        self.assertTrue(run.final)

    def test_every_tool_result_lands_in_messages(self) -> None:
        run = run_agent(ScriptedModel(), self.sandbox)
        tool_messages = [m for m in run.messages if m["role"] == "tool"]
        self.assertEqual(len(tool_messages), len(run.steps))
        tokens = [step.tokens for step in run.steps]
        self.assertEqual(tokens, sorted(tokens))

    def test_tools_cannot_leave_sandbox(self) -> None:
        with self.assertRaises(ValueError):
            execute_tool(self.sandbox, "read_file", {"path": "../../etc/passwd"})


if __name__ == "__main__":
    unittest.main()
