#!/usr/bin/env python3
"""Optional live call. Not the phase 1 mainline — chat_as_completion.py is.

Talks to any OpenAI-compatible Chat Completions endpoint. Prefers xAI Grok
when XAI_API_KEY is set.

    cp .env.example .env   # then put your key in .env
    python3 src/chat_hello.py
    python3 src/chat_hello.py --prompt "Explain tokens in one sentence."
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)


def resolve_client() -> tuple[str, str, str]:
    load_dotenv(ROOT / ".env")
    if os.getenv("XAI_API_KEY"):
        return (
            os.environ["XAI_API_KEY"],
            os.getenv("XAI_BASE_URL", "https://api.x.ai/v1"),
            os.getenv("XAI_MODEL", "grok-4"),
        )
    if os.getenv("OPENAI_API_KEY"):
        return (
            os.environ["OPENAI_API_KEY"],
            os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        )
    sys.exit(
        "No API key found.\n"
        "Offline path:  python3 src/tokenize_demo.py && python3 src/next_token_demo.py\n"
        "Live path:     copy .env.example to .env and set XAI_API_KEY or OPENAI_API_KEY."
    )


def chat(prompt: str, temperature: float) -> dict:
    try:
        import httpx
    except ImportError:
        sys.exit("Install extras first:  pip install -r requirements.txt")

    api_key, base_url, model = resolve_client()
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a precise teaching assistant for LLM Lesson 01. "
                    "Prefer short, concrete answers. Mention tokens when relevant."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=60.0) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    choice = data["choices"][0]
    return {
        "model": data.get("model", model),
        "base_url": base_url,
        "text": choice["message"]["content"],
        "finish_reason": choice.get("finish_reason"),
        "usage": data.get("usage", {}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="First live LLM API call")
    parser.add_argument(
        "--prompt",
        default="What is a large language model, in 4 short bullet points?",
    )
    parser.add_argument("--temperature", type=float, default=0.3)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = chat(args.prompt, args.temperature)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("=" * 64)
    print(f"model    : {result['model']}")
    print(f"endpoint : {result['base_url']}")
    usage = result["usage"]
    if usage:
        print(
            "usage    : "
            f"prompt={usage.get('prompt_tokens')} "
            f"completion={usage.get('completion_tokens')} "
            f"total={usage.get('total_tokens')}"
        )
    print("-" * 64)
    print(result["text"])
    print("=" * 64)
    print("Those usage numbers are tokens, not words. Compare them with tokenize_demo.py.")


if __name__ == "__main__":
    main()
