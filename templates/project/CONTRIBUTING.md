# Contributing

This repository uses a PRD-first and issue-first engineering workflow.

## Research policy

- Tavily first
- official docs for external contracts
- known URLs should be fetched/indexed directly when available
- verified facts must be separated from assumptions

## Execution surface policy

- use the local machine first for ordinary development, debugging, research, and verification
- if the repository already has self-hosted runners, prefer them over paid GitHub-hosted Actions for recurring work
- check or bootstrap local prerequisites before assuming CI is the right place to run the work
- keep GitHub Actions for repository-native automation, schedules, deploys, and hosted checks that genuinely need the platform

## Start from the correct issue

Use:

- `Epic` for the parent work envelope
- `Task` for one executable leaf slice
- `Bug` for a confirmed regression or incident

If the work spans multiple slices, decompose it into GitHub sub-issues.

## Automatic bug intake

- runtime and pipeline bugs should come from verifier/watchdog/readiness-gate evidence
- do not create bug issues directly from raw logs or chat alerts
- use one stable fingerprint per bug class
- reopen or update the existing bug issue when the fingerprint matches
- create a new bug issue only when no open issue already tracks that fingerprint

## Kernel sync review

- every serious slice must end with `kernel_sync_review`
- record `Kernel Impact` as:
  - `none`
  - `project_local_only`
  - `promote_to_kernel`
- use `promote_to_kernel` only for reusable engineering workflow or verification patterns
- keep repository-specific ops canon in the project repo instead of polluting the universal kernel

## PR rule

- one PR should normally close one leaf issue
- parent epic stays open until acceptance and required live verification are complete
- use draft PR while scope or verification is still moving
- prefer squash merge unless project canon says otherwise

## GitHub CLI shell-safety

- do not pass markdown through inline double-quoted `gh ... --body`
- use `--body-file` for issue and PR bodies
- if needed, create the body file with a single-quoted heredoc such as `<<'EOF'`

## Minimum PR contents

- linked leaf issue
- parent context
- write scope
- verification
- rollback path

## Repo-managed metadata

- `CODEOWNERS`
- issue templates
- PR template
- labels source-of-truth
- `scripts/sync_github_labels.py`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
