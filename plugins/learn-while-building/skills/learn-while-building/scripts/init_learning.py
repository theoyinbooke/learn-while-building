#!/usr/bin/env python3
"""Create a privacy-conscious project learning folder without overwriting user files."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize docs/learning for a project.")
    parser.add_argument("--root", default=".", help="Project root. Defaults to the current directory.")
    parser.add_argument("--objective", default="To be completed with the learner")
    parser.add_argument("--level", default="Not specified")
    parser.add_argument("--focus", default="Understanding the current project")
    parser.add_argument("--depth", choices=("concise", "balanced", "deep"), default="balanced")
    parser.add_argument("--practice", default="mixed")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    learning = root / "docs" / "learning"
    (learning / "records").mkdir(parents=True, exist_ok=True)
    (learning / "lessons").mkdir(parents=True, exist_ok=True)
    (learning / "data").mkdir(parents=True, exist_ok=True)

    profile = f"""# Learning profile

## Learning objective
{args.objective}

## Experience level
{args.level}

## Current focus
{args.focus}

## Explanation depth
{args.depth}

## Preferred practice
{args.practice}

## Last updated
{date.today().isoformat()}
"""

    index = """# Project learning

This folder keeps compact learning notes grounded in this project. It should not contain chat transcripts, secrets, or unrelated personal data.

## Profile

- [Learning profile](profile.md)

## Recent records

No records yet.

## Lessons

No lessons yet.

## Current concepts

Add concepts after meaningful project work.

## Next practice

Choose one nearby task that reuses a concept from the latest record.
"""

    created = []
    if write_if_missing(learning / "profile.md", profile):
        created.append("docs/learning/profile.md")
    if write_if_missing(learning / "index.md", index):
        created.append("docs/learning/index.md")

    if created:
        print("Created " + ", ".join(created))
    else:
        print("Learning folder already exists. Existing profile and index were preserved.")
    print(f"Learning directory: {learning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
