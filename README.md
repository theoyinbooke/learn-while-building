# Learn While Building

Learn While Building turns real work with a coding agent into practical, project-grounded learning. It keeps the software outcome first, then adds a short explanation layer that helps the user understand important decisions, evidence, and reusable concepts.

Every meaningful update begins with a standalone 30-second summary. Deeper explanations, project examples, checks for understanding, and optional HTML lessons follow only when useful.

## What it adds

- a project learning objective and learner profile
- adaptive explanations based on the active request, project evidence, and project learning records
- compact cross-session learning records stored in the project, without full chat transcripts
- explicit session review and progress modes
- validated offline HTML lessons with quizzes and accessible visual fallbacks
- optional Three.js views that load only when the learner asks for them
- a calm editorial design with no purple or blue gradients, emojis, hype, or em dashes

## Install in Codex

Add the public marketplace, then install the plugin:

```bash
codex plugin marketplace add theoyinbooke/learn-while-building
codex plugin add learn-while-building@learn-while-building
```

Restart Codex after installation so newly installed skills are discovered.

To update later:

```bash
codex plugin marketplace upgrade learn-while-building
codex plugin add learn-while-building@learn-while-building
```

## Use it

Select **Learn While Building** from the skill menu or write:

```text
$learn-while-building initialize
$learn-while-building review-session
$learn-while-building render-lesson
$learn-while-building progress
```

The skill uses only conversation context supplied by the host and relevant evidence from the active project. It does not assume access to account-wide chat history.

## Generate the sample lesson

```bash
SKILL=plugins/learn-while-building/skills/learn-while-building
python3 "$SKILL/scripts/validate_lesson.py" "$SKILL/assets/sample-lesson.json"
python3 "$SKILL/scripts/render_lesson.py" "$SKILL/assets/sample-lesson.json" --output outputs/sample-lesson.html
```

## Validate the package

```bash
python3 -m unittest discover -s tests -v
python3 /path/to/quick_validate.py plugins/learn-while-building/skills/learn-while-building
python3 /path/to/validate_plugin.py plugins/learn-while-building
```

## Distribution

This repository is both the source repository and a Codex plugin marketplace. The portable skill lives at:

`plugins/learn-while-building/skills/learn-while-building`

The repository can be updated through normal tagged releases. Users refresh the marketplace to receive the latest version.

## License

MIT
