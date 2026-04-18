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
- classify each non-trivial slice before edits as `repo_local_slice` or `external_contract_slice`
- `repo_local_slice` may proceed from project truth, deterministic verification, and local runtime checks when only repo-owned behavior is changing
- `external_contract_slice` requires fresh external research before code or docs land
- use official vendor docs to verify external contracts
- if a known URL already exists, fetch/index it directly instead of re-running broad search
- distinguish verified facts from assumptions

## Execution surface canon

- prefer the local operator machine first for ordinary development, debugging, research, and verification
- if the project already has self-hosted runners, prefer them over paid GitHub-hosted Actions for recurring work
- check local prerequisites before work starts
- if the repo defines a local bootstrap path, use or repair it before escalating elsewhere
- use GitHub Actions for repository-native automation, schedules, deploys, and hosted verification that genuinely belongs there

## Kernel sync canon

- every serious slice ends with `kernel_sync_review`
- record `Kernel Impact` as one of:
  - `none`
  - `project_local_only`
  - `promote_to_kernel`
- only promote reusable process patterns into the universal kernel
- keep project-specific operational rules in this repository, not in the universal kernel

## GitHub workflow canon

- non-trivial work starts from a parent GitHub issue
- canonical hierarchy:
  - `Epic`
  - `Task`
  - `Bug`
- use sub-issues for multi-slice work
- PR closes the leaf issue only, not the parent epic
- when invoking `gh issue create`, `gh issue edit`, or `gh pr create` from shell, use `--body-file` instead of inline double-quoted `--body`
- if a file is inconvenient, write it first with a single-quoted heredoc such as `<<'EOF'`
- GitHub Projects are optional and threshold-based, not bootstrap default; adopt them only when engineering planning needs shared custom fields/views or cross-repo coordination

## Automatic bug intake canon

- canonical bug intake comes from verifier, watchdog, or other normalized runtime gates
- do not create GitHub bug issues directly from raw logs or Telegram alerts
- use one stable fingerprint per bug class
- update the existing open bug issue when the fingerprint matches
- only create a new bug issue when there is no open match for that fingerprint

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
