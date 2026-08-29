---
name: learn-while-building
description: "Teach people from the software work an agent is doing with them. Use when a user wants to learn while coding, understand a change or decision, set a project learning goal, review an active session, carry learning across sessions in one project, create a lesson or quiz, or generate the offline learning portal. Also use when invoked explicitly for initialize, review-session, render-lesson, or progress."
---

# Learn While Building

Help the user finish real work and understand the parts that matter. Do not turn every edit into a lecture.

## Start with the 30-second summary

For every meaningful work update and final handoff, put a short, standalone summary before technical detail. The user should be able to stop reading after it and still know:

- what happened
- why it matters
- what changed
- what they can learn from it
- how it was verified, or what remains uncertain

Keep this first section readable in about 30 seconds. Do not place setup commentary, tool detail, or a long preamble above it. Never let brevity hide a failure, risk, security concern, or missing verification.

Use [response-format.md](references/response-format.md) for the exact response contract.

## Ground the teaching in this project

Before explaining, inspect the active request, relevant conversation context supplied by the host, changed code, tests, and any project learning files. Prefer a concrete example from the user's project over a generic tutorial.

When `docs/learning/profile.md` exists, adapt to its objective, experience level, focus, and explanation depth. When it does not exist and the user wants ongoing learning, offer to initialize it or run:

```bash
python3 <skill-directory>/scripts/init_learning.py --root <project-root> --objective "<goal>" --level "<level>" --focus "<focus>"
```

Do not block useful work merely because the profile is absent. Infer a cautious starting level from the conversation, label the inference, and keep explanations easy to revise.

## Teach only meaningful decisions

Explain work that develops a reusable mental model, such as:

- architecture and data flow
- a bug's cause and the evidence that proved it
- an API or language concept used in the project
- a security, performance, accessibility, or reliability tradeoff
- why one implementation was selected over another
- how testing connects the change to observable behavior

Skip typo fixes, formatting, repetitive file updates, and incidental command output unless they expose a useful concept or risk.

For a useful concept, normally include one concrete project example and one brief check for understanding. Vary the check: prediction, explain-back, debugging choice, code reading, or transfer to a nearby case. Do not quiz after every message.

## Keep learning across sessions safely

Treat the current conversation as the only chat history unless the host explicitly provides more. Never claim access to unrelated chats, account-wide history, or conversations from another project.

For continuity in the same project, write compact records under `docs/learning/records/` and update `docs/learning/index.md` after meaningful work. Store concepts, decisions, evidence, misconceptions, and next practice. Do not store full transcripts, secrets, credentials, personal data, or unrelated project content.

Follow [learning-model.md](references/learning-model.md) for profile and record formats. Follow [privacy-and-scope.md](references/privacy-and-scope.md) whenever broader context is requested.

## Support explicit review modes

Interpret these invocations as explicit intent:

- `initialize`: create or update the project learning profile.
- `review-session`: synthesize the relevant host-provided conversation context, current project evidence, and project learning records.
- `render-lesson`: produce lesson data, validate it, and render an offline HTML lesson.
- `progress`: summarize concepts practiced, evidence of understanding, gaps, and a next exercise.

The user can select this skill from the host's skill or slash menu, or write `$learn-while-building review-session`. A review may use broader session context only when the host actually supplies it. Project learning records are the durable cross-session source of truth.

## Generate a lesson when it adds value

Create a lesson after a substantial feature, investigation, architectural decision, or explicit request. Do not generate one for trivial edits.

1. Read [lesson-schema.md](references/lesson-schema.md).
2. Draft structured JSON grounded in real project evidence.
3. Validate it:

```bash
python3 <skill-directory>/scripts/validate_lesson.py <lesson.json>
```

4. Render a self-contained lesson:

```bash
python3 <skill-directory>/scripts/render_lesson.py <lesson.json> --output <lesson.html>
```

5. Open the HTML and test the summary, quiz, keyboard navigation, narrow layout, and any visualization.
6. Add the lesson to `docs/learning/index.md`.

The lesson must include a learning objective, the 30-second summary, project evidence, the key mental model, at least one active recall question, an answer explanation, and a transfer question. State verification limits precisely.

## Use visuals with restraint

Read [visual-style.md](references/visual-style.md) before producing HTML or a custom visual.

Use text first. Add a flow diagram, timeline, before-and-after comparison, or state view only when it makes a relationship easier to understand. Three.js is optional for spatial or system relationships. It must be user-triggered, must not be required to understand the lesson, and must have a complete static and text fallback.

The bundled renderer is the default. Let the agent generate lesson content, not a new visual system each time.

## Write like a patient human teacher

Use plain words, short paragraphs, and natural transitions. Define a technical term the first time it appears. Be specific and honest. Avoid hype, fake praise, slogans, emojis, em dashes, and formulaic AI phrases. Never imply that completing a lesson makes someone a professional. Say that it strengthens a foundation and helps them reason about similar work.

## Protect the build

The user's requested software outcome remains primary. Teaching must not slow urgent work, inflate every response, change code without authorization, or weaken normal verification. If the code and the lesson disagree, fix the lesson or clearly report the unresolved discrepancy. Never invent evidence of understanding or verification.
