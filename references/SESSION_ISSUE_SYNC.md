# Session Issue Sync

Use this when closing a serious engineering slice, PRD slice, bugfix, or
agent-led work session that has durable GitHub issue state.

This policy closes the loop between implementation state and operational memory.
GitHub Issues remain the durable task surface; chat summaries and local memory
are not enough for serious work.

## Closeout Field

Every serious slice records:

```text
Issue Sync: updated | skipped | not_applicable
```

Use exactly one value:

- `updated`: the relevant GitHub issue body, labels, links, status, or next
  step was updated to reflect the slice outcome.
- `skipped`: an issue update would normally apply, but was intentionally not
  performed; record the reason.
- `not_applicable`: the work has no durable GitHub issue state to update.

## Rules

- Search before creating a new issue. Prefer updating the existing matching
  issue when scope overlaps.
- Durable status belongs in the issue body: current state, next step,
  verification, links, and closeout decisions.
- Comments are for short chronological notes, explicit user-requested comments,
  or external blockers that would clutter the body.
- Surface stale issue state instead of silently fixing it: missing parent epic,
  stale-open epic, missing next step, false-positive search match, or issue
  state that conflicts with the active PRD.
- Do not close issues without verified completion and project-local authority.
- Do not write to public issues with private, personal, customer, credential, or
  production-sensitive details.
- Use MCP/App connector GitHub writes when available and authorized; otherwise
  use shell-safe `gh` with `--body-file` or a single-quoted heredoc-generated
  body file.

## Optional Project Policies

The universal kernel does not require weekly labels, CRM pointers, GitHub
Projects, or a weekly planning cadence.

Project-local canon may add those policies when they fit the repository. If a
project adds them, the `Issue Sync` closeout should respect them without
promoting project-specific details into the universal kernel.

## Read Mode

When asked "what is the status of X?", agents should answer from durable issue
state where possible:

- matching issue references and titles;
- parent epic or missing-parent warning;
- open/closed state;
- labels or fields that matter to the project;
- last meaningful activity;
- known gaps or stale state;
- false positives that were ignored.

If the answer depends on an external service, current GitHub state, or a live
project board, verify through the appropriate connector or shell-safe `gh`
fallback before claiming current status.
