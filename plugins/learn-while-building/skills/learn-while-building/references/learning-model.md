# Project learning model

Durable learning state is optional and belongs only to the active project.

## Storage locations

- `session-only`: no learning files
- `private-project`: `.learn-while-building/`
- `shared-project`: `docs/learning/`

Both stored modes use the same internal shape so the learner can migrate deliberately.

## Profile

`profile.md` contains:

- Learning objective
- Experience level
- Current focus
- Learning mode: quiet, coach, or deep
- Explanation depth: concise, balanced, or deep
- Preferred practice: prediction, debugging, code reading, explain-back, or mixed
- Privacy mode
- Current handback stage from 1 to 6
- Last updated date

Treat the profile as user-editable. Do not overwrite the learner's wording. Ask before materially changing the objective, privacy mode, or handback stage.

## Records

Create a compact Markdown record after meaningful work. Use an ISO date plus a short slug, such as `records/2026-08-29-request-validation.md`.

```markdown
# Request validation

## Software change
One short factual description.

## Why it works
The causal explanation.

## Mental model
The reusable concept in plain language.

## Project trace
- Relevant file, component, test, or observed behavior.

## Understanding evidence
- A prediction, explanation, modification, transfer, or `Not checked yet`.

## Misconception
- A supported misconception and correction, or `None observed`.

## Recall
- One prompt and due date, or `Not scheduled`.

## Next practice
One nearby task that transfers the concept.
```

Do not copy chat transcripts into records. Do not record secrets, personal data, hidden prompts, unrelated project history, or unsupported assumptions.

## State files

- `recall.json`: delayed-recall queue
- `misconceptions.json`: compact evidence-backed misconception records
- `index.md`: links to the profile, recent records, lessons, current concepts, and next practice

Use `scripts/manage_learning.py` to add, list, or review recall items. Do not hand-edit state during routine updates when the helper can preserve its shape.

## Adaptation order

1. Explicit objective, mode, privacy, and preferences
2. Demonstrated understanding in this project
3. Current request and active project evidence
4. Prior records from this project
5. A cautious inference from host-provided conversation, clearly labeled

Increase difficulty through better prediction and transfer, not denser jargon.
