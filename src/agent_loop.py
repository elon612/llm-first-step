#!/usr/bin/env python3
"""Lesson 02: a coding agent is a loop around next-token prediction.

The model only ever returns one message: either a tool call or a final answer.
The harness runs the tool, appends the result to `messages`, and asks again.
Everything the agent "knows" about your repo is whatever landed in `messages`.

ScriptedModel stands in for a real LLM so this runs offline with no API key.
Swap it for an API call (exercise 02) and the loop does not change.

    python3 src/agent_loop.py
    python3 src/agent_loop.py --no-verify
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

TASK = "test_cart.py is failing. Fix cart.py."

SYSTEM = (
    "You are a coding agent. Reply with exactly one tool call as JSON, "
    "or with a final answer when the task is done."
)

SANDBOX_FILES = {
    "cart.py": (
        "def total_price(items, discount=0.0):\n"
        '    """items: [(unit_price, qty)]; discount=0.1 means 10% off."""\n'
        "    subtotal = sum(price for price, qty in items)\n"
        "    return round(subtotal - discount, 2)\n"
    ),
    "test_cart.py": (
        "import unittest\n"
        "\n"
        "from cart import total_price\n"
        "\n"
        "\n"
        "class CartTests(unittest.TestCase):\n"
        "    def test_quantity_counts(self):\n"
        "        self.assertEqual(total_price([(2.5, 4)]), 10.0)\n"
        "\n"
        "    def test_discount_is_a_percentage(self):\n"
        "        self.assertEqual(total_price([(10.0, 2)], discount=0.1), 18.0)\n"
        "\n"
        "    def test_empty_cart(self):\n"
        "        self.assertEqual(total_price([]), 0)\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    unittest.main()\n"
    ),
}

TOOLS = [
    {"name": "run_tests", "description": "Run the unit tests", "parameters": {}},
    {"name": "grep", "description": "Search files for a string", "parameters": {"pattern": "str"}},
    {"name": "read_file", "description": "Read one file", "parameters": {"path": "str"}},
    {
        "name": "edit_file",
        "description": "Replace an exact string in a file",
        "parameters": {"path": "str", "old": "str", "new": "str"},
    },
]

Message = dict[str, object]


def make_sandbox(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    for name, text in SANDBOX_FILES.items():
        (root / name).write_text(text, encoding="utf-8")
    return root


def run_tests(sandbox: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "test_cart"],
        cwd=sandbox,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


def _inside(sandbox: Path, rel: str) -> Path:
    path = (sandbox / rel).resolve()
    if sandbox.resolve() not in path.parents:
        raise ValueError(f"path escapes sandbox: {rel}")
    return path


def execute_tool(sandbox: Path, name: str, args: dict[str, str]) -> str:
    if name == "run_tests":
        ok, output = run_tests(sandbox)
        return ("PASSED\n" if ok else "FAILED\n") + output
    if name == "grep":
        hits = []
        for file in sorted(sandbox.glob("*.py")):
            for i, line in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
                if args["pattern"] in line:
                    hits.append(f"{file.name}:{i}:{line}")
        return "\n".join(hits) or "(no matches)"
    if name == "read_file":
        return _inside(sandbox, args["path"]).read_text(encoding="utf-8")
    if name == "edit_file":
        path = _inside(sandbox, args["path"])
        text = path.read_text(encoding="utf-8")
        if args["old"] not in text:
            return "ERROR: old string not found"
        path.write_text(text.replace(args["old"], args["new"], 1), encoding="utf-8")
        return f"edited {args['path']}"
    return f"ERROR: unknown tool {name}"


class Model(Protocol):
    def next_message(self, messages: list[Message], tools: list[dict]) -> Message: ...


class ScriptedModel:
    """Reacts to what is in `messages`, like an LLM would, but with fixed rules.

    It fixes only the failure it can see in the latest test output, which is
    what real agents tend to do too. With verify=False it never re-runs tests
    after editing, so it declares success on a half-fixed file.
    """

    def __init__(self, verify: bool = True) -> None:
        self.verify = verify

    def next_message(self, messages: list[Message], tools: list[dict]) -> Message:
        results = [m for m in messages if m["role"] == "tool"]
        last = results[-1] if results else None
        seen = {m["name"] for m in results}

        if last is None:
            return _call("run_tests")
        if last["name"] == "run_tests" and str(last["content"]).startswith("PASSED"):
            return {"role": "assistant", "content": "All tests pass. Fixed cart.py."}
        if "grep" not in seen:
            return _call("grep", pattern="def total_price")
        if "read_file" not in seen:
            return _call("read_file", path="cart.py")
        if last["name"] == "edit_file":
            if self.verify:
                return _call("run_tests")
            return {"role": "assistant", "content": "Fixed cart.py: quantity is now counted."}

        failing = _latest_test_output(results)
        if "test_quantity_counts" in failing:
            return _call(
                "edit_file",
                path="cart.py",
                old="sum(price for price, qty in items)",
                new="sum(price * qty for price, qty in items)",
            )
        if "test_discount_is_a_percentage" in failing:
            return _call(
                "edit_file",
                path="cart.py",
                old="round(subtotal - discount, 2)",
                new="round(subtotal * (1 - discount), 2)",
            )
        return {"role": "assistant", "content": "I could not work out the failure."}


def _call(name: str, **arguments: str) -> Message:
    return {"role": "assistant", "tool_call": {"name": name, "arguments": arguments}}


def _latest_test_output(results: list[Message]) -> str:
    for message in reversed(results):
        if message["name"] == "run_tests":
            return str(message["content"])
    return ""


def approx_tokens(messages: list[Message]) -> int:
    """Rough rule of thumb: ~4 characters per token for English and code."""
    return len(json.dumps(messages, ensure_ascii=False)) // 4


@dataclass
class Step:
    call: dict | None
    result: str
    message_count: int
    tokens: int


@dataclass
class AgentRun:
    messages: list[Message]
    steps: list[Step] = field(default_factory=list)
    final: str = ""


def run_agent(model: Model, sandbox: Path, task: str = TASK, max_steps: int = 12) -> AgentRun:
    run = AgentRun(messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": task}])
    for _ in range(max_steps):
        reply = model.next_message(run.messages, TOOLS)
        run.messages.append(reply)
        call = reply.get("tool_call")
        if not call:
            run.final = str(reply.get("content", ""))
            break
        result = execute_tool(sandbox, call["name"], call["arguments"])
        run.messages.append({"role": "tool", "name": call["name"], "content": result})
        run.steps.append(Step(call, result, len(run.messages), approx_tokens(run.messages)))
    return run


def _preview(text: str, lines: int = 3) -> str:
    rows = text.splitlines()
    head = "\n".join("    " + row for row in rows[:lines])
    return head + (f"\n    ... ({len(rows) - lines} more lines)" if len(rows) > lines else "")


def main() -> None:
    parser = argparse.ArgumentParser(description="Show that a coding agent is a loop")
    parser.add_argument("--no-verify", action="store_true", help="agent skips re-running tests")
    parser.add_argument("--json", action="store_true", help="dump the final messages list")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        sandbox = make_sandbox(Path(tmp) / "repo")
        run = run_agent(ScriptedModel(verify=not args.no_verify), sandbox)
        ok, _ = run_tests(sandbox)

    if args.json:
        print(json.dumps(run.messages, ensure_ascii=False, indent=2))
        return

    print("=" * 64)
    print(f"Task: {TASK}")
    print("=" * 64)
    for i, step in enumerate(run.steps, 1):
        call = step.call or {}
        print(f"step {i}  messages={step.message_count}  ~tokens={step.tokens}")
        print(f"  model -> {call.get('name')} {json.dumps(call.get('arguments', {}))}")
        print("  tool  <-")
        print(_preview(step.result))
        print()
    print(f"model final answer: {run.final}")
    print(f"independent test run after the agent stopped: {'PASS' if ok else 'FAIL'}")
    print("-" * 64)
    print("Every tool result was appended to messages. That list is all the model saw.")
    if args.no_verify:
        print("Without re-running tests, the agent trusted its own edit and stopped early.")
    print("=" * 64)


if __name__ == "__main__":
    main()
