# Recall and misconceptions

Use this model only when the learner has enabled private-project or shared-project storage.

## Recall queue

Create a recall item after a meaningful concept, not every edit. Store:

- stable concept identifier
- prompt that can be answered without seeing the original explanation
- project evidence pointer
- due date
- interval in days
- attempt count
- successful transfer count
- status: `due`, `scheduled`, or `retired`

Suggested intervals are 1, 3, 7, 14, and 30 days. Adapt based on evidence. A correct answer with reasoning moves forward. A lucky choice or unsupported answer does not. Retire an item only after at least two successful transfers in different nearby situations.

## Misconceptions

Record a misconception only when the learner's response provides evidence. Store:

- the learner's current model, paraphrased respectfully
- the project evidence that conflicts with it
- the corrected model
- one diagnostic prompt
- status: `active`, `improving`, or `resolved`

Do not label uncertainty, a typo, or a question as a misconception. Do not preserve embarrassing wording or a full transcript.

## Recall interaction

Show the prompt before guidance. Ask for reasoning. After the attempt, reveal a concise rubric or model answer and connect it to current project evidence. Record the outcome only when the user has enabled storage.
