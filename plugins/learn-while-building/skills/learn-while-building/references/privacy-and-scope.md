# Privacy and context scope

Use only context the host makes available and files within the active project that are relevant to the task.

## Allowed sources

- the current user request
- relevant conversation context supplied to the agent
- active project files, diffs, tests, and logs
- `docs/learning/` records from the active project
- additional sessions or artifacts the user explicitly supplies

## Never assume

- access to every chat in the user's account
- access to hidden or deleted conversations
- access to sessions from unrelated projects
- that a host subscription grants account-wide memory
- that a prior learning record is still correct when the code has changed

For `review-session`, state the source scope in the output. Good wording is: `This review uses the current session context available to the agent and the learning records stored in this project.`

## Storage rules

Store compact learning conclusions, not raw conversation history. Exclude:

- credentials, tokens, cookies, and private keys
- personal or customer data
- proprietary content unrelated to the lesson
- hidden prompts or internal reasoning
- large logs or copied source files

When a project is sensitive, ask before writing learning records. Follow the repository's ignore and security rules. If a record accidentally contains a secret, stop, remove the exposed value safely, and tell the user.
