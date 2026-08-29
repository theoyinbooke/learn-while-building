# Response format

Use two clearly separated layers for meaningful updates and final handoffs.

## Required boundary

Use this exact structure:

```markdown
### 30-second learning brief

The brief goes here.

**End of 30-second learning brief**

The agent's normal detailed response begins here when detail is needed.
```

The heading identifies where the learning artifact starts. The fixed end marker identifies exactly where it stops. Do not change the marker wording, place detail inside the marker, or put any preamble above the heading.

## The brief

The brief must stand on its own and take no more than about 30 seconds to read. Hard limit: 130 words. Aim for 55 to 100 words.

Cover these points in compact prose or a short list:

1. What happened?
2. Why does it matter?
3. What reusable idea should the learner keep?
4. What was verified, and what remains uncertain?

The brief may mention what changed separately when that is not already clear. Never hide a failure, risk, security issue, or missing verification to stay short.

## The normal response

After the end marker, continue with the normal task response only when detail is useful. Prefer this order:

1. Outcome and material changes
2. Evidence or verification
3. Technical detail needed to understand or continue
4. One learning check in Coach or Deep mode
5. Remaining next step or limitation

Do not restate the brief sentence by sentence. Quiet mode can stop immediately after the marker when the brief fully answers the update.

## Mode examples

Quiet:

```markdown
### 30-second learning brief

The validation bug came from checking the display value instead of the saved value. The fix moves validation to the data boundary and adds a regression test. The reusable idea is that validation is most reliable where data enters the system. The focused test passes. The full suite has not run yet.

**End of 30-second learning brief**
```

Coach adds normal details and one useful check after the marker. Deep adds a Learning Diff and project-grounded practice after the marker.

## Trivial messages

Do not force the full format onto greetings, tiny clarifications, requests to repeat something, or one-line factual answers. Keep those natural.

## Language rules

- Use plain language and short paragraphs.
- Define unfamiliar terms in place.
- Use no emojis.
- Use no em dashes.
- Avoid hype and generic praise.
- Avoid phrases such as `unlock`, `delve`, `game-changing`, `seamlessly`, and `revolutionary`.
- Do not claim mastery, professional status, or verified understanding without evidence.
