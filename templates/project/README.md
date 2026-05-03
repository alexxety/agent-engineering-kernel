# Project Name

This repository follows the agent engineering kernel.

## Engineering canon

- non-trivial work is PRD-first
- Superpowers or equivalent process skills are used as tactical workflow aids when available, without replacing project canon
- non-trivial work starts from a parent GitHub issue
- MCP or App connector tooling is preferred for supported structured external-service operations when available and authorized
- local `gh` auth and GitHub App connector auth are different identities with separate permissions
- GitHub App repository access and permissions are configured in GitHub Installed Apps, not in repo files or local `gh` token settings
- each non-trivial slice is classified before edits as `repo_local_slice` or `external_contract_slice`
- repo-owned slices may proceed from project truth, deterministic verification, and local runtime checks
- slices that change or claim current external-system behavior require fresh external research before code or docs land
- external research is Tavily Search-first; Tavily Research is only an explicitly justified expensive fallback for broad deep-sweeps
- every `external_contract_slice` records an `external_source_of_truth_matrix` so project pins, vendor docs, exact versions, and live verification are reconciled explicitly
- GitHub hierarchy:
  - `Epic`
  - `Task`
  - `Bug`
- runtime bugs come from verifier/watchdog/runtime-gate fingerprints, not raw logs or chat alerts
- ordinary development, debugging, and verification should run locally first
- GitHub coordinates issues, PRs, check status, schedules, and deploy triggers; owned compute should execute routine work by default
- if the project has self-hosted runners or can reasonably provide them, prefer them over paid GitHub-hosted Actions for recurring work
- document self-hosted runner labels before enabling recurring GitHub checks
- required workflows should stay triggered; use risk-based classifier jobs and job-level `if` gates for expensive jobs instead of workflow-level skips that can leave required checks `Pending`
- `full-ci` or an equivalent explicit override forces the full matrix, as do main, release, scheduled, manual, dependency, and workflow changes
- GitHub Actions are for repository-native automation, schedules, deploys, and hosted checks that genuinely belong there
- paid GitHub-hosted runners, dependency cache uploads, and long-lived artifact storage require an explicit PRD/decision note
- production-bound work documents `local`, disposable `verify`, `staging`, and `production` boundaries before launch hardening
- production secrets and production database URLs must not be used in local verification
- mutating automated tests must not run against production
- production-safe migration/deploy command, backup or restore-point path, smoke checks, and rollback must be project-local canon
- serious slices begin with `kernel_upstream_check`
- the project pins its upstream kernel commit in `.kernel/upstream.json`
- if drift exists, open or update a `kernel_adoption_task`
- `kernel_adoption_task` records one decision:
  - `adopt_now`
  - `defer`
  - `not_applicable`
- `.kernel/upstream.json` only advances after adoption is implemented and verified
- kernel updates are adopted explicitly through normal project issues/PRDs, not auto-applied blindly
- every serious slice ends with `kernel_sync_review`
- serious closeouts record `Kernel Impact`
- PR closes the leaf issue only
- agents should read or invoke relevant Superpowers skills before acting: `using-superpowers` / `brainstorming` for new behavior, `writing-plans` for multi-step work, `test-driven-development` for implementation, `systematic-debugging` for bugs, and `verification-before-completion` before success claims
- orchestrated agentic coding keeps one accountable orchestrator, defaults to one worker agent, permits at most two parallel workers only with disjoint write sets, uses targeted one-shot reviewer agents, keeps implementation workers open only for the same-patch review/fix loop, requires `thread_disposition`, and stops spawning agents after executor/resource failures such as `Too many open files`
- rich-MCP orchestrators use project-local no-MCP coding workers from `.codex/agents/` so implementation workers do not inherit external MCP servers
- Claude Code, when used as a subagent, defaults to `design_readonly` or `review_readonly` through `scripts/claude-code-readonly-subagent.sh` with direct-binary preference, `claude-opus-4-7` model pin, `stream-json --verbose`, strict empty MCP config, `dontAsk` permission mode, mode-specific tools such as `Read` or `Read,Grep,Glob`, and budget caps; use it for UX/workflow, PRD/spec, independent review, test planning, and refactor-boundary questions with a context packet, focused snippets, or selected diff context first, not whole-repo or huge-file context by habit; if explicitly requested and it fails, diagnose Claude Code instead of silently switching agent families
- `gh issue create` and `gh pr create` should use `--body-file` or a single-quoted heredoc-generated file, not inline markdown bodies
- shell-safe `gh` is the fallback when MCP/App connector tooling is missing, stale, or blocked
- for GitHub sub-issues, prefer `scripts/link_github_sub_issue.py`; if you call REST directly, `sub_issue_id` means child issue database id, not `#issue_number`
- GitHub Projects are optional and should be adopted only when issue-first execution needs shared fields/views or cross-repo planning
- any optional `CLAUDE.md` / Cursor / skill-style behavior overlay must stay thin and subordinate to the repo-local canon

## Canon files

- `README.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `.kernel/upstream.json`
- `.github/ISSUE_TEMPLATE/*`
- `.github/pull_request_template.md`
- `.github/CODEOWNERS`
- `.github/labels.yml`
- `scripts/sync_github_labels.py`
- `scripts/check_kernel_upstream.py`
- `scripts/claude-code-readonly-subagent.sh`
- active PRD in `docs/`
