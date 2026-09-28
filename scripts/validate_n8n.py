"""Validate n8n workflow exports before they reach GitHub.

Checks every workflows/**/workflow.json:
  • valid JSON with a non-empty "nodes" list and a "connections" object
  • no hard-coded secrets (OpenAI/Anthropic keys, Slack/Telegram/Google tokens, bearer headers)
  • no pinned execution data ("pinData"), which often contains real messages or emails

Usage:  python scripts/validate_n8n.py            (exit code 1 on any problem)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SECRET_PATTERNS = {
    "OpenAI/Anthropic key": re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_\-]{20,}"),
    "Slack token": re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    "Telegram bot token": re.compile(r"\b\d{8,10}:[A-Za-z0-9_\-]{35}\b"),
    "SerpApi key": re.compile(r"\b[a-f0-9]{64}\b"),
    "Bearer header": re.compile(r"Bearer\s+[A-Za-z0-9._\-]{20,}"),
}


def check(path: Path) -> list[str]:
    problems: list[str] = []
    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    if not isinstance(data.get("nodes"), list) or not data["nodes"]:
        problems.append('missing or empty "nodes" list')
    if not isinstance(data.get("connections"), dict):
        problems.append('missing "connections" object')
    if data.get("pinData"):
        problems.append('contains "pinData" (pinned execution data) — unpin before exporting')

    # n8n's own instance/webhook IDs are random hex, not secrets — don't flag them.
    scannable = re.sub(r'"(instanceId|webhookId|id)"\s*:\s*"[^"]*"', "", raw)
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(scannable):
            problems.append(f"possible {label} found — move it into an n8n credential")
    return problems


def main() -> int:
    files = sorted(Path("workflows").glob("**/*.json"))
    files = [f for f in files if "sample-data" not in f.parts and "data" not in f.parts]
    if not files:
        print("No workflow exports found under workflows/")
        return 1

    failed = False
    for f in files:
        problems = check(f)
        status = "✗" if problems else "✓"
        print(f"{status} {f}")
        for p in problems:
            print(f"    - {p}")
        failed |= bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
