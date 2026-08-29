# Lesson data schema

The renderer accepts one UTF-8 JSON object.

## Required fields

```json
{
  "meta": {
    "title": "A factual lesson title",
    "project": "Project name",
    "generatedAt": "2026-08-29",
    "sourceScope": ["current session", "project learning records"]
  },
  "learningObjective": "One observable objective",
  "summary": {
    "whatHappened": "What happened",
    "whyItMatters": "Why it matters",
    "whatChanged": "What changed",
    "whatToLearn": "The reusable idea",
    "verification": "Evidence and limits"
  },
  "concepts": [
    {
      "name": "Concept name",
      "plainExplanation": "A plain explanation",
      "projectExample": "A concrete example from this project"
    }
  ],
  "quiz": [
    {
      "question": "A prediction, debugging, or transfer question",
      "choices": ["Choice one", "Choice two"],
      "answer": 0,
      "explanation": "Why the answer fits the project evidence"
    }
  ],
  "transferQuestion": "A nearby situation where the learner can reuse the idea"
}
```

## Optional fields

```json
{
  "evidence": ["File, test, log, or observed behavior"],
  "beforeAfter": {
    "before": "Prior behavior or model",
    "after": "New behavior or model",
    "reason": "Why the change works"
  },
  "visualizations": [
    {
      "type": "flow",
      "title": "Request path",
      "description": "Why this view helps",
      "nodes": ["User request", "Validation", "Saved result"]
    },
    {
      "type": "three-scene",
      "title": "System relationship",
      "description": "A spatial view of three connected parts",
      "objects": [
        {"label": "Conversation", "color": "olive"},
        {"label": "Project evidence", "color": "terracotta"},
        {"label": "Lesson", "color": "warm-gray"}
      ]
    }
  ]
}
```

Use `flow` for sequences. Use `three-scene` only when spatial separation or relationships add real explanatory value. The 3D view is optional and network-triggered. Its static text fallback is always rendered.

The validator rejects missing required fields, invalid quiz answers, em dashes, emojis, and common hype phrases.
