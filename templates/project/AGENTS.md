# Project workflow canon

This repository follows the agent engineering kernel.

## Required order for non-trivial work

1. Research
2. Code audit
3. Reconciliation
4. Documentation first
5. Implementation
6. Verification

## Research canon

- use Tavily first for research
- use official vendor docs to verify external contracts
- if a known URL already exists, fetch/index it directly instead of re-running broad search
- distinguish verified facts from assumptions

## GitHub workflow canon

- non-trivial work starts from a parent GitHub issue
- canonical hierarchy:
  - `Epic`
  - `Task`
  - `Bug`
- use sub-issues for multi-slice work
- PR closes the leaf issue only, not the parent epic

## GitHub delivery flow

1. create or update PRD
2. open parent issue if needed
3. create executable leaf issue
4. create branch from the leaf issue
5. implement in a small slice
6. open or update draft PR
7. run verification
8. mark PR ready
9. merge
10. delete head branch

## Minimum verification contract

- code-path tests
- build/runtime checks
- source-of-truth / sync checks
- live checks when runtime or state changes
- rollback path

## Canon files

- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `.github/ISSUE_TEMPLATE/*`
- `.github/pull_request_template.md`
- `.github/CODEOWNERS`
- `.github/labels.yml`
- `scripts/sync_github_labels.py`
- active PRD / decision doc in `docs/`
