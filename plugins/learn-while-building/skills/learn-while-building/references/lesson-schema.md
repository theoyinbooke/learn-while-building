# Lesson data schema

The renderer accepts one UTF-8 JSON object. The complete example lives in `assets/sample-lesson.json`.

## Required fields

```json
{
  "meta": {
    "title": "A factual lesson title",
    "project": "Project name",
    "generatedAt": "2026-08-29",
    "sourceScope": ["current session", "project evidence"]
  },
  "learningObjective": "One observable objective",
  "summary": {
    "whatHappened": "What happened",
    "whyItMatters": "Why it matters",
    "whatChanged": "What changed",
    "whatToLearn": "The reusable idea",
    "verification": "Evidence and limits"
  },
  "learningDiff": {
    "softwareChange": "The actual project change",
    "whyItWorks": "The causal explanation",
    "mentalModel": "The reusable model",
    "canNow": ["Predict one outcome", "Modify one nearby case"],
    "verificationLimits": "What the evidence proves and does not prove"
  },
  "concepts": [
    {
      "name": "Concept name",
      "plainExplanation": "A plain explanation",
      "projectExample": "A concrete example from this project"
    }
  ],
  "projectTrace": [
    {
      "label": "Validator",
      "path": "scripts/validate_lesson.py",
      "reason": "Enforces the content contract"
    }
  ],
  "quiz": [
    {
      "type": "prediction",
      "question": "What do you expect to happen, and why?",
      "guidance": "What a strong answer should consider",
      "modelAnswer": "A concise model answer",
      "explanation": "How it connects to project evidence"
    }
  ],
  "transferQuestion": "A nearby situation where the learner can reuse the idea"
}
```

The summary is rendered as the maximum 30-second learning brief. The renderer always places `End of 30-second learning brief` immediately after it.

## Practice types

Supported `type` values:

- `multiple-choice`: requires `choices` with at least two items and an integer `answer`
- `prediction`
- `short-answer`
- `code-reading`

Open-response types require `guidance` and `modelAnswer`. The renderer requires an attempt before revealing either. Every practice item requires `question` and `explanation`.

At least one practice item must be open response. Multiple choice may supplement it but cannot be the only evidence path.

## Optional fields

- `scaffoldingStage`: integer from 1 to 6
- `evidence`: short project evidence strings
- `beforeAfter`: `before`, `after`, and `reason`
- `misconceptions`: evidence-backed corrections relevant to this lesson
- `recallPrompt`: a prompt for a later session
- `visualizations`: `flow` or optional `three-scene`

Use `flow` for sequences. Use `three-scene` only when spatial separation adds explanatory value. The 3D view is optional and network-triggered. Its static text fallback is always rendered.

The validator rejects incomplete fields, unsupported practice types, a lesson with only multiple choice, invalid answer indexes, em dashes, emojis, common hype phrases, and a learning brief over 130 words.
