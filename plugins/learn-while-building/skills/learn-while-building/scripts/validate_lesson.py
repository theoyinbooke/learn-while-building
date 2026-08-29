#!/usr/bin/env python3
"""Validate structured lesson data and enforce the writing contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQUIRED_SUMMARY = ("whatHappened", "whyItMatters", "whatChanged", "whatToLearn", "verification")
OPEN_RESPONSE_TYPES = ("prediction", "short-answer", "code-reading")
QUIZ_TYPES = ("multiple-choice", *OPEN_RESPONSE_TYPES)
HYPE_PHRASES = ("unlock", "delve", "game-changing", "seamlessly", "revolutionary", "ai-powered magic")
EMOJI_RE = re.compile(
    "["
    "\U0001F1E6-\U0001F1FF"
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U00002600-\U000026FF"
    "]"
)


class LessonError(ValueError):
    pass


def walk_strings(value: Any, path: str = "root"):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_strings(item, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk_strings(item, f"{path}.{key}")


def require_text(mapping: dict[str, Any], key: str, path: str) -> None:
    if not isinstance(mapping.get(key), str) or not mapping[key].strip():
        raise LessonError(f"{path}.{key} must be non-empty text")


def word_count(values: list[str]) -> int:
    return sum(len(re.findall(r"\b[\w'-]+\b", value)) for value in values)


def validate_data(data: Any) -> None:
    if not isinstance(data, dict):
        raise LessonError("root must be an object")

    meta = data.get("meta")
    if not isinstance(meta, dict):
        raise LessonError("root.meta must be an object")
    for key in ("title", "project", "generatedAt"):
        require_text(meta, key, "root.meta")
    scope = meta.get("sourceScope")
    if not isinstance(scope, list) or not scope or not all(isinstance(item, str) and item.strip() for item in scope):
        raise LessonError("root.meta.sourceScope must be a non-empty list of text values")

    require_text(data, "learningObjective", "root")
    require_text(data, "transferQuestion", "root")

    summary = data.get("summary")
    if not isinstance(summary, dict):
        raise LessonError("root.summary must be an object")
    for key in REQUIRED_SUMMARY:
        require_text(summary, key, "root.summary")
    summary_words = word_count([summary[key] for key in REQUIRED_SUMMARY])
    if summary_words > 130:
        raise LessonError(f"root.summary contains {summary_words} words; the 30-second learning brief limit is 130")

    learning_diff = data.get("learningDiff")
    if learning_diff is not None:
        if not isinstance(learning_diff, dict):
            raise LessonError("root.learningDiff must be an object")
        for key in ("softwareChange", "whyItWorks", "mentalModel", "verificationLimits"):
            require_text(learning_diff, key, "root.learningDiff")
        can_now = learning_diff.get("canNow")
        if not isinstance(can_now, list) or not can_now or not all(isinstance(item, str) and item.strip() for item in can_now):
            raise LessonError("root.learningDiff.canNow must be a non-empty list of text values")

    concepts = data.get("concepts")
    if not isinstance(concepts, list) or not concepts:
        raise LessonError("root.concepts must contain at least one concept")
    for index, concept in enumerate(concepts):
        if not isinstance(concept, dict):
            raise LessonError(f"root.concepts[{index}] must be an object")
        for key in ("name", "plainExplanation", "projectExample"):
            require_text(concept, key, f"root.concepts[{index}]")

    project_trace = data.get("projectTrace")
    if project_trace is not None:
        if not isinstance(project_trace, list) or not project_trace:
            raise LessonError("root.projectTrace must contain at least one item")
        for index, item in enumerate(project_trace):
            if not isinstance(item, dict):
                raise LessonError(f"root.projectTrace[{index}] must be an object")
            for key in ("label", "path", "reason"):
                require_text(item, key, f"root.projectTrace[{index}]")

    quiz = data.get("quiz")
    if not isinstance(quiz, list) or not quiz:
        raise LessonError("root.quiz must contain at least one question")
    open_response_count = 0
    for index, item in enumerate(quiz):
        if not isinstance(item, dict):
            raise LessonError(f"root.quiz[{index}] must be an object")
        require_text(item, "question", f"root.quiz[{index}]")
        require_text(item, "explanation", f"root.quiz[{index}]")
        quiz_type = item.get("type", "multiple-choice")
        if quiz_type not in QUIZ_TYPES:
            raise LessonError(f"root.quiz[{index}].type must be one of: {', '.join(QUIZ_TYPES)}")
        if quiz_type == "multiple-choice":
            choices = item.get("choices")
            if not isinstance(choices, list) or len(choices) < 2 or not all(isinstance(choice, str) and choice.strip() for choice in choices):
                raise LessonError(f"root.quiz[{index}].choices must contain at least two text choices")
            answer = item.get("answer")
            if not isinstance(answer, int) or isinstance(answer, bool) or answer < 0 or answer >= len(choices):
                raise LessonError(f"root.quiz[{index}].answer must be a valid zero-based choice index")
        else:
            open_response_count += 1
            require_text(item, "guidance", f"root.quiz[{index}]")
            require_text(item, "modelAnswer", f"root.quiz[{index}]")

    if data.get("schemaVersion") == "0.1.1":
        if learning_diff is None:
            raise LessonError("root.learningDiff is required for schemaVersion 0.1.1")
        if project_trace is None:
            raise LessonError("root.projectTrace is required for schemaVersion 0.1.1")
        if open_response_count == 0:
            raise LessonError("schemaVersion 0.1.1 requires at least one open-response practice item")

    stage = data.get("scaffoldingStage")
    if stage is not None and (not isinstance(stage, int) or isinstance(stage, bool) or stage < 1 or stage > 6):
        raise LessonError("root.scaffoldingStage must be an integer from 1 to 6")

    for path, text in walk_strings(data):
        if "\u2014" in text:
            raise LessonError(f"{path} contains an em dash")
        if EMOJI_RE.search(text):
            raise LessonError(f"{path} contains an emoji")
        lowered = text.casefold()
        for phrase in HYPE_PHRASES:
            if phrase in lowered:
                raise LessonError(f"{path} contains the discouraged phrase: {phrase}")


def load_and_validate(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise LessonError(f"invalid JSON: {exc}") from exc
    validate_data(data)
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Learn While Building lesson JSON.")
    parser.add_argument("lesson", type=Path)
    args = parser.parse_args()
    try:
        load_and_validate(args.lesson)
    except (OSError, LessonError) as exc:
        print(f"Invalid lesson data: {exc}")
        return 1
    print(f"Valid lesson data: {args.lesson}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
