# Project learning model

Keep durable learning state inside the active project under `docs/learning/`.

## Profile

`docs/learning/profile.md` should contain:

- Learning objective
- Experience level
- Current focus
- Explanation depth: concise, balanced, or deep
- Preferred practice: prediction, debugging, code reading, explain-back, or mixed
- Last updated date

Treat the profile as user-editable. Do not overwrite a user's wording. Ask before making a material change to the objective.

## Records

Create a compact Markdown record after meaningful work. Use an ISO date plus a short slug, for example:

`docs/learning/records/2026-08-29-request-validation.md`

Use this structure:

```markdown
# Request validation

## What changed
One short, factual description.

## Why it matters
The user-facing or system consequence.

## Mental model
The reusable concept in plain language.

## Project evidence
- Relevant file, component, test, or observed behavior.

## Understanding evidence
- A question answered, prediction made, bug explained, or `Not checked yet`.

## Next practice
One nearby task that transfers the concept.
```

Do not copy chat transcripts into records. Do not record secrets, personal data, hidden prompts, unrelated project history, or unsupported assumptions.

## Index

`docs/learning/index.md` is the map, not a second copy of every lesson. Keep links to:

- the profile
- recent records
- rendered lessons
- current concepts
- next practice

Update it when adding a meaningful record or lesson.

## Adaptation

Adapt in this order:

1. Explicit user objective and preferences
2. Demonstrated understanding in this project
3. Current request and active code evidence
4. Prior project learning records
5. A cautious inference from conversation, clearly labeled

Increase difficulty through better questions and transfer tasks, not through denser jargon.
