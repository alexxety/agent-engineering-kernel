# Contributing

This repository uses a PRD-first and issue-first engineering workflow.

## Process skill policy

If Superpowers or an equivalent process-skill pack is available, agents should read or invoke the relevant skill before acting:

- `using-superpowers` and `brainstorming` for new behavior or design work
- `writing-plans` for approved multi-step work
- `test-driven-development` for implementation and bugfixes
- `systematic-debugging` for bugs, failed tests, build failures, regressions, or unexpected behavior
- `verification-before-completion` before any success, fixed, passing, done, commit-ready, or PR-ready claim
- `requesting-code-review` and `receiving-code-review` around review
- `using-git-worktrees`, `dispatching-parallel-agents`, `subagent-driven-development`, or `executing-plans` only when the project, platform, and work shape allow them

Skills are tactical workflow aids. This project canon, the active PRD, tests, and explicit user instructions stay higher priority.

## MCP/App connector policy

- use MCP or App connector tooling for supported structured external-service operations when available and authorized
- local `gh` auth and GitHub App connector auth are different identities with separate permissions
- configure GitHub App repository access and permissions in GitHub Installed Apps, not by storing tokens in repo files
- if an App connector fails with a permission error, check repository access and App permissions before refreshing local `gh` auth
- use the canonical shell-safe `gh` fallback when connector tooling is missing, stale, or blocked

## Research policy

- Tavily Search first, not Tavily Research first
- known official URLs should be fetched/indexed directly when available
- agents should do manual source reading, comparison, and synthesis before escalation
- Tavily Research is only an explicitly justified expensive fallback for broad deep-sweeps
- classify each non-trivial slice before edits as `repo_local_slice` or `external_contract_slice`
- `repo_local_slice` may proceed from project truth, deterministic verification, and local runtime checks when only repo-owned behavior is changing
- `external_contract_slice` requires fresh external research before code or docs land
- every `external_contract_slice` must record an `external_source_of_truth_matrix` in the active PRD or decision note before implementation lands
- official docs for external contracts
- verified facts must be separated from assumptions

## Execution surface policy

- use the local machine first for ordinary development, debugging, research, and verification
- GitHub coordinates issues, PRs, check status, schedules, and deploy triggers; owned compute should execute routine work by default
- if the repository already has self-hosted runners or can reasonably provide them, prefer them over paid GitHub-hosted Actions for recurring work
- document the self-hosted runner label(s) before enabling recurring GitHub checks
- check or bootstrap local prerequisites before assuming CI is the right place to run the work
- keep GitHub Actions for repository-native automation, schedules, deploys, and hosted checks that genuinely need the platform
- do not enable paid GitHub-hosted runners, dependency cache uploads, or long-lived artifact storage without an explicit PRD/decision note

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

- every serious slice should begin with `kernel_upstream_check`
- consumer kernel metadata lives in `.kernel/upstream.json`
- if upstream kernel drift exists, open or update a `kernel_adoption_task` or explicitly defer it in the active PRD/closeout
- the canonical downstream task is `kernel_adoption_task`
- `kernel_adoption_task` records `adopt_now | defer | not_applicable`
- `.kernel/upstream.json` advances only after adoption is implemented and verified
- do not auto-apply kernel changes blindly into the project
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
- use `scripts/link_github_sub_issue.py` for CLI sub-issue linkage when starting from normal issue numbers
- raw REST add-sub-issue calls require the child issue database id in `sub_issue_id`; `#issue_number` is the wrong value

## GitHub Projects

- GitHub Projects are optional, not a default requirement
- add them only when issue-first execution no longer gives enough shared planning surface
- typical thresholds are shared custom fields, iteration/roadmap views, or cross-repo engineering planning

## Minimum PR contents

- linked leaf issue
- parent context
- write scope
- baseline verification
- verification
- sandbox identity confirmation for live external writes
- rollback path

## Verification timing

- define verification before edits
- when an existing deterministic contract already exists, capture the smallest relevant baseline before implementation begins
- bugfixes should prefer a reproducer before the fix
- refactors should prefer before/after equivalence checks
- docs-only, canon-only, or greenfield slices may skip pre-change baseline only when no existing deterministic contract exists
- post-change verification before merge remains mandatory
- live verification that can write to an external service must use explicitly designated sandbox identities, never operator or production identities

## Repo-managed metadata

- `CODEOWNERS`
- issue templates
- PR template
- labels source-of-truth
- `scripts/sync_github_labels.py`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
