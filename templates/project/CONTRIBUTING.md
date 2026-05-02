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

## Agentic coding orchestration

When using orchestrated agentic coding, keep one accountable orchestrator. The orchestrator owns scope, worker write-set boundaries, review decisions, verification, docs, commits, runtime checks, and rollback notes.

Default to one worker agent at a time. Run at most two worker agents in parallel, and only when write sets and runtime resources are disjoint. Run reviewer agents selectively for security, database, deploy/runtime, privacy/logging, production integration, or broad multi-file changes.

When custom agents are available, use the project-local no-MCP worker from `.codex/agents/` for implementation work. Rich-MCP orchestrator sessions may use external tools, but coding workers should not inherit MCP servers; use the global `code_worker_no_mcp` only as fallback.

Claude Code may be used as a one-shot read-only reviewer/design reviewer through `scripts/claude-code-readonly-subagent.sh`. The default Claude Code adapter prefers a direct binary over wrapper binaries, pins `claude-opus-4-7` unless the operator overrides it, uses `claude -p`, no session persistence, `stream-json --verbose`, explicit empty MCP config, strict MCP enforcement, `dontAsk` permission mode, and the smallest read-only tool set for the task: no tools for smoke, `Read` for exact-file review, and `Read,Grep,Glob` only when repo search is required. Do not use `plan` mode for read-only workers. Do not use `--bare` for OAuth-backed local Claude Code sessions unless API-key or `apiKeyHelper` mode has been explicitly configured and smoke-tested. If the operator explicitly asks for Claude Code and it fails, diagnose Claude Code CLI/binary/auth/MCP/tool/output/permission/process setup before requesting approval to use any fallback agent family.

Keep at most three subagent threads open, close completed threads promptly, and avoid parallel shell/tool calls while workers are active. Implementation workers may remain open only for the same-patch review/fix loop; reviewers are one-shot and should be replaced by a fresh reviewer for re-review after fixes. Every subagent final response should include `thread_disposition` so the orchestrator can close threads deliberately. If the executor reports `Too many open files`, stream disconnects, or failed process creation, stop spawning agents and recover sequentially with `git status --short --branch` and `git diff --check` before continuing.

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

## Environment promotion policy

- Production-bound projects should use one codebase with separate `local`, disposable `verify`, `staging`, and `production` environments.
- Local development can use local throwaway data and local-only secrets.
- Disposable verification owns mutating automated tests.
- Staging should be production-like and use sandbox or non-production provider identities.
- Production contains real users, real customer data, and production provider identities.
- Do not place production secrets or production database URLs in local config.
- Do not run mutating automated tests against production.
- Document the production-safe migration/deploy command, backup or restore-point path, smoke checks, and rollback before production use.

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
