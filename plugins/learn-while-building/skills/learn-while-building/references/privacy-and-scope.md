# Privacy and context scope

Use only context the host makes available and files within the active project that are relevant to the task.

## Allowed sources

- the current user request
- relevant conversation context supplied to the agent
- active project files, diffs, tests, and logs
- learning records from the active project
- additional sessions or artifacts the user explicitly supplies

## Never assume

- access to every chat in the learner's account
- access to hidden or deleted conversations
- access to sessions from unrelated projects
- that a subscription grants account-wide memory
- that a stored record remains correct after the code changes

For `review-session`, state the source scope. Good wording is: `This review uses the current session context available to the agent, current project evidence, and learning records stored in this project.`

## Privacy modes

### Session-only

Keep adaptation in the active response. Write no profile, record, lesson, recall queue, or misconception file. This is the safe default when the project is sensitive or the learner has not chosen persistence.

### Private-project

Store compact state under `.learn-while-building/`. In a Git project, add `.learn-while-building/` to the repository's local `.git/info/exclude`, not the tracked `.gitignore`. Verify that the ignore rule works. Explain that non-Git backups or sync tools may still copy the folder.

### Shared-project

Store state under `docs/learning/`. This location may be committed and reviewed with the project. Use it only when the learner intentionally wants shared or versioned learning records.

Changing privacy mode is a material choice. Do not copy or delete existing state without explicit approval.

## Storage exclusions

Store compact learning conclusions, not raw conversation history. Exclude:

- credentials, tokens, cookies, and private keys
- personal, customer, or production data
- proprietary content unrelated to the lesson
- hidden prompts or internal reasoning
- large logs or copied source files

If a record contains a secret, stop, remove the exposed value safely, and tell the learner. If deletion or history rewriting would be required, request authorization first.
