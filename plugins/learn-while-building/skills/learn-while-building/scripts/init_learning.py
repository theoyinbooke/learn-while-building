#!/usr/bin/env python3
"""Initialize privacy-conscious learning state without overwriting learner files."""

from __future__ import annotations

import argparse
import subprocess
from datetime import date
from pathlib import Path


PRIVATE_FOLDER = ".learn-while-building"


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def local_git_exclude(root: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--git-path", "info/exclude"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0 or not result.stdout.strip():
        return None
    path = Path(result.stdout.strip())
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def ensure_private_ignore(root: Path) -> bool:
    exclude = local_git_exclude(root)
    if exclude is None:
        return False
    exclude.parent.mkdir(parents=True, exist_ok=True)
    existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    rule = f"{PRIVATE_FOLDER}/"
    if any(line.strip() == rule for line in existing.splitlines()):
        return True
    separator = "" if not existing or existing.endswith("\n") else "\n"
    exclude.write_text(f"{existing}{separator}{rule}\n", encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize Learn While Building state for a project.")
    parser.add_argument("--root", default=".", help="Project root. Defaults to the current directory.")
    parser.add_argument("--objective", default="To be completed with the learner")
    parser.add_argument("--level", default="Not specified")
    parser.add_argument("--focus", default="Understanding the current project")
    parser.add_argument("--mode", choices=("quiet", "coach", "deep"), default="quiet")
    parser.add_argument("--privacy", choices=("session-only", "private-project", "shared-project"), default="session-only")
    parser.add_argument("--depth", choices=("concise", "balanced", "deep"), default="balanced")
    parser.add_argument("--practice", default="mixed")
    parser.add_argument("--handback-stage", type=int, choices=range(1, 7), default=1)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if args.privacy == "session-only":
        print("Session-only mode selected. No learning files were created.")
        print(f"Learning mode: {args.mode}")
        return 0

    learning = root / (PRIVATE_FOLDER if args.privacy == "private-project" else "docs/learning")
    (learning / "records").mkdir(parents=True, exist_ok=True)
    (learning / "lessons").mkdir(parents=True, exist_ok=True)

    profile = f"""# Learning profile

## Learning objective
{args.objective}

## Experience level
{args.level}

## Current focus
{args.focus}

## Learning mode
{args.mode}

## Explanation depth
{args.depth}

## Preferred practice
{args.practice}

## Privacy mode
{args.privacy}

## Handback stage
{args.handback_stage}

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

    created: list[str] = []
    for name, content in (
        ("profile.md", profile),
        ("index.md", index),
        ("recall.json", "[]\n"),
        ("misconceptions.json", "[]\n"),
    ):
        if write_if_missing(learning / name, content):
            created.append(str((learning / name).relative_to(root)))

    if args.privacy == "private-project":
        if ensure_private_ignore(root):
            print(f"Verified local Git ignore rule: {PRIVATE_FOLDER}/")
        else:
            print("No Git repository was detected. The private folder exists, but another sync or backup tool may still copy it.")

    if created:
        print("Created " + ", ".join(created))
    else:
        print("Learning state already exists. Existing learner files were preserved.")
    print(f"Learning directory: {learning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
