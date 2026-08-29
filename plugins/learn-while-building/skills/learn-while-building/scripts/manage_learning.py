#!/usr/bin/env python3
"""Manage the compact delayed-recall queue for one project."""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any


INTERVALS = (1, 3, 7, 14, 30)


def learning_dir(root: Path, privacy: str) -> Path:
    return root / (".learn-while-building" if privacy == "private-project" else "docs/learning")


def load_items(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise ValueError(f"learning state is not initialized: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("recall.json must contain a list")
    return data


def save_items(path: Path, items: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_day(value: str) -> date:
    return date.fromisoformat(value)


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage Learn While Building delayed recall.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--privacy", choices=("private-project", "shared-project"), default="private-project")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add")
    add.add_argument("--concept-id", required=True)
    add.add_argument("--prompt", required=True)
    add.add_argument("--evidence", required=True)
    add.add_argument("--due", default=date.today().isoformat())

    due = sub.add_parser("due")
    due.add_argument("--on", default=date.today().isoformat())

    review = sub.add_parser("review")
    review.add_argument("--concept-id", required=True)
    review.add_argument("--result", choices=("success", "retry", "transfer"), required=True)
    review.add_argument("--on", default=date.today().isoformat())
    review.add_argument("--transfer-evidence")

    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    path = learning_dir(root, args.privacy) / "recall.json"
    try:
        items = load_items(path)
        if args.command == "add":
            if any(item.get("conceptId") == args.concept_id for item in items):
                raise ValueError(f"concept already exists: {args.concept_id}")
            parse_day(args.due)
            items.append(
                {
                    "conceptId": args.concept_id,
                    "prompt": args.prompt,
                    "evidence": args.evidence,
                    "due": args.due,
                    "intervalDays": 1,
                    "attempts": 0,
                    "successfulTransfers": 0,
                    "transferEvidence": [],
                    "status": "scheduled",
                }
            )
            save_items(path, items)
            print(f"Added recall item: {args.concept_id}")
        elif args.command == "due":
            on = parse_day(args.on)
            found = [item for item in items if item.get("status") != "retired" and parse_day(item["due"]) <= on]
            print(json.dumps(found, indent=2, ensure_ascii=False))
        else:
            on = parse_day(args.on)
            item = next((entry for entry in items if entry.get("conceptId") == args.concept_id), None)
            if item is None:
                raise ValueError(f"unknown concept: {args.concept_id}")
            item["attempts"] = int(item.get("attempts", 0)) + 1
            if args.result == "retry":
                item["intervalDays"] = 1
                item["status"] = "scheduled"
            else:
                current = int(item.get("intervalDays", 1))
                next_interval = next((value for value in INTERVALS if value > current), INTERVALS[-1])
                item["intervalDays"] = next_interval
                if args.result == "transfer":
                    if not args.transfer_evidence:
                        raise ValueError("--transfer-evidence is required for a transfer result")
                    evidence = item.setdefault("transferEvidence", [])
                    if args.transfer_evidence in evidence:
                        raise ValueError("transfer evidence must describe a different nearby situation")
                    evidence.append(args.transfer_evidence)
                    item["successfulTransfers"] = len(evidence)
                item["status"] = "retired" if int(item.get("successfulTransfers", 0)) >= 2 else "scheduled"
            item["due"] = (on + timedelta(days=int(item["intervalDays"]))).isoformat()
            save_items(path, items)
            print(f"Updated recall item: {args.concept_id} ({item['status']})")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Could not manage recall: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
