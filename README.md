# Learn While Building

Ship the code. Keep the understanding.

Learn While Building adds a calm learning layer to real work with coding agents. It does not replace the build with a course. It uses the active project, current evidence, and the learner's goal to explain the decisions that matter.

Every meaningful update starts with a maximum 30-second learning brief and ends that artifact with the same fixed marker:

```text
30-second learning brief
...
End of 30-second learning brief
```

The agent's normal detailed response begins only after that boundary.

## Why it is different

- **Learning Diff:** connects the software change to the mental model, project evidence, practice target, and verification limits.
- **Quiet, Coach, and Deep:** the learner controls how much teaching appears. Quiet is the default.
- **Gradual handback:** moves from agent demonstration to learner-owned nearby tasks as understanding is demonstrated.
- **Real practice:** prioritizes prediction, explanation, debugging, code reading, and modification over passive reading.
- **Delayed recall:** brings important concepts back in later sessions and retires them after repeated transfer.
- **Misconception tracking:** records only evidence-backed misunderstandings, never guesses about the learner.
- **Project privacy:** supports session-only, locally ignored private state, or intentionally shared project records.
- **Calm lessons:** generates self-contained HTML lessons with open response, accessible static visuals, and optional user-triggered Three.js views.

## Install in compatible coding agents

Use the portable skill installer:

```bash
npx skills add theoyinbooke/learn-while-building --skill learn-while-building --global
```

List what will be installed first:

```bash
npx skills add theoyinbooke/learn-while-building --list
```

## Install as a Codex plugin

```bash
codex plugin marketplace add theoyinbooke/learn-while-building
codex plugin add learn-while-building@learn-while-building
```

Restart Codex or begin a new thread after installation so the updated skill contract is loaded.

To update later:

```bash
codex plugin marketplace upgrade learn-while-building
codex plugin add learn-while-building@learn-while-building
```

## Use it

The skill can activate automatically for learning-oriented coding requests, or it can be invoked explicitly:

```text
$learn-while-building initialize
$learn-while-building review-session
$learn-while-building render-lesson
$learn-while-building recall
$learn-while-building progress
```

Choose a mode in natural language:

```text
Use Quiet mode while we build this feature.
Switch to Coach mode and ask me to predict important behavior.
Give me a Deep review of what changed today.
```

## Initialize learning state

Session-only writes nothing:

```bash
python3 plugins/learn-while-building/skills/learn-while-building/scripts/init_learning.py \
  --root . --privacy session-only --mode quiet
```

Private-project stores learning under `.learn-while-building/` and adds it to the local Git exclude file:

```bash
python3 plugins/learn-while-building/skills/learn-while-building/scripts/init_learning.py \
  --root . --privacy private-project --mode coach \
  --objective "Understand the architecture I am changing"
```

Shared-project stores reviewable records under `docs/learning/`:

```bash
python3 plugins/learn-while-building/skills/learn-while-building/scripts/init_learning.py \
  --root . --privacy shared-project --mode deep \
  --objective "Learn how this team validates API requests"
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

Behavioral scenarios live in `evals/scenarios.json`. They test decisions such as staying quiet during trivial work, respecting storage boundaries, refusing unsupported history access, and requiring an attempt before revealing guidance.

## Repository structure

This repository is both the source and a Codex plugin marketplace. The portable skill lives at:

`plugins/learn-while-building/skills/learn-while-building`

Tagged releases provide a stable update path for installed agents.

## Upgrade from 0.1.0

Existing 0.1.0 lesson JSON remains valid. New lessons should set `schemaVersion` to `0.1.1`, which requires a Learning Diff, project trace, and at least one open-response practice item.

Existing `docs/learning/` state is treated as shared-project state. The upgrade does not move or delete it. To use private-project storage, initialize the private mode separately and move records only after reviewing them and choosing to do so.

## License

MIT
