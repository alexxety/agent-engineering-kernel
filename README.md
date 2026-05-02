# Agent Engineering Kernel

[![License: MIT](https://img.shields.io/github/license/alexxety/agent-engineering-kernel)](LICENSE)
[![Release](https://img.shields.io/github/v/release/alexxety/agent-engineering-kernel?include_prereleases&sort=semver)](https://github.com/alexxety/agent-engineering-kernel/releases)
[![Tests](https://github.com/alexxety/agent-engineering-kernel/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/alexxety/agent-engineering-kernel/actions/workflows/tests.yml)
[![Stars](https://img.shields.io/github/stars/alexxety/agent-engineering-kernel?style=social)](https://github.com/alexxety/agent-engineering-kernel/stargazers)

Universal engineering kernel for agent-led software work.

**Homepage:** [hq.dudarik.com/projects/agent-engineering-kernel](https://hq.dudarik.com/projects/agent-engineering-kernel/)

This repository is the standalone source-of-truth for:

- PRD-first execution
- Superpowers-compatible process-skill orchestration
- MCP and App connector tooling policy
- GitHub issue decomposition
- PR verification discipline
- project bootstrap templates
- a reusable Codex skill
- agentic coding orchestration with explicit worker/reviewer limits and recovery rules
- project-local no-MCP coding workers with global fallback worker guidance
- Claude Code subagent adapter rules for one-shot read-only review with strict no-MCP startup
- repo-managed GitHub metadata and community-health baseline
- kernel sync review for promoting proven project learnings back into the universal kernel
- optional GitHub Projects layer only when the repository actually needs shared planning views beyond issue-first execution
- kernel upstream awareness so consumer repositories can detect kernel drift explicitly
- a canonical `kernel_adoption_task` so downstream repos handle kernel drift deterministically
- optional kernel fleet sweep so one operator machine can review many consumer repos at once
- environment promotion canon for local, disposable verify, staging, and production boundaries

The goal is simple: a new agent in a new repository should not need the workflow re-explained in chat.

Execution-surface canon:

- ordinary engineering work should default to the local operator machine first
- GitHub coordinates repository workflow: issues, PRs, check status, schedules, and deploy triggers
- owned compute executes routine work by default: local machine first, then self-hosted runners for recurring checks
- self-hosted runners are preferred over paid GitHub-hosted Actions when the repository already has them or can reasonably provide them
- paid GitHub-hosted runners, dependency cache uploads, and long-lived artifact storage are explicit exceptions for private repositories, not defaults
- GitHub Actions remain for repo-native automation, schedules, deploys, and hosted checks that actually belong there
- production-bound work should document local, disposable verify, staging, and production boundaries before launch hardening

## Core idea

Use one shared engineering process across agent families.

Shared core:

- research
- code audit
- reconciliation
- process-skill selection when Superpowers or an equivalent skill pack is available
- documentation first
- baseline verification when an existing contract already exists
- implementation
- post-change verification
- GitHub `Epic / Task / Bug` hierarchy
- MCP or App connector use for supported structured external-service operations, with local `gh` fallback treated as a different identity
- automatic deduplicated `Bug` intake from verifier/watchdog/runtime gates
- PR closes leaf issue only
- shell-safe GitHub CLI delivery through `--body-file` or a single-quoted heredoc-generated body file instead of inline markdown bodies
- shell-safe sub-issue linking through `scripts/link_github_sub_issue.py`; if REST is used directly, `sub_issue_id` means child issue database id, not `#issue_number`

Bug-intake canon:

- runtime bugs come from canonical surfaces, not raw logs or Telegram alerts
- one stable fingerprint maps to one durable GitHub `Bug` issue
- repeated incidents update the open bug issue for that fingerprint instead of
  creating duplicates

Research canon:

- Tavily Search first, not Tavily Research first
- known official URLs are fetched directly when already available
- agents do manual source reading, comparison, and synthesis before escalating
- Tavily Research is an explicitly justified expensive fallback for broad deep-sweeps, not the default
- classify each non-trivial slice before edits as `repo_local_slice` or `external_contract_slice`
- `repo_local_slice` may proceed from project truth, deterministic verification, and local runtime checks when only repo-owned behavior is changing
- `external_contract_slice` requires fresh external research before code or docs land
- every `external_contract_slice` records an `external_source_of_truth_matrix` in the active PRD or decision note
- official docs for external contracts

Verification canon:

- define verification before edits
- when a deterministic contract already exists, capture the smallest relevant baseline before editing
- for bugfixes, prefer a reproducer first
- for refactors, prefer before/after equivalence checks
- for docs-only, canon-only, or greenfield slices without an existing contract, do not invent a fake pre-change baseline
- live verification that can write to an external service must use explicitly designated sandbox identities, never operator or production identities
- production secrets and production database URLs must not be used in local verification
- mutating automated tests must not run against production data or production provider identities
- post-change verification before publish remains mandatory

Environment-promotion canon:

- use one codebase with multiple deploy environments, not copied projects that drift
- `local` is for iteration, `verify` is disposable for automated mutating tests, `staging` is production-like with sandbox identities, and `production` is real users/data
- each project must document production-safe deploy or migration commands, backup/restore-point path, staging smoke checks, production smoke checks, and rollback before production use
- production data may move down to staging only through documented backup/restore and sanitization; local or staging data must not move up to production

Skill-assisted execution canon:

- Superpowers skills are a tactical process layer, not a replacement for project canon
- project-local `AGENTS.md`, the active PRD, explicit user instructions, tests, and the engineering kernel outrank skill defaults
- when a relevant Superpowers skill is available, agents should read or invoke it before acting
- map new behavior to `using-superpowers` and `brainstorming`
- map approved multi-step work to `writing-plans`
- map implementation and bugfixes to `test-driven-development`
- map bugs, failed tests, and unexpected behavior to `systematic-debugging`
- map completion claims to `verification-before-completion`
- use `subagent-driven-development`, `dispatching-parallel-agents`, or `executing-plans` only when the platform, independence, and user or project policy allow it

Agentic coding orchestration canon:

- one orchestrator stays accountable for scope, research, write-set boundaries, verification, docs, commits, and runtime checks
- rich-MCP orchestrators dispatch project-local no-MCP coding workers when custom agents are available
- project-local workers are preferred over the global `code_worker_no_mcp` fallback for implementation inside a repo
- project-local no-MCP configs disable the MCP server ids that exist in that project/operator environment; the kernel does not prescribe a fixed MCP list
- Claude Code may be used as a one-shot `design_readonly` or `review_readonly` adapter with `claude -p`, direct-binary preference, `claude-opus-4-7` model pin, `stream-json --verbose`, explicit empty MCP config, strict MCP enforcement, `dontAsk` permission mode, mode-specific tools such as `Read` or `Read,Grep,Glob`, and budget caps; use it for UX/workflow, PRD/spec, independent review, test planning, and refactor-boundary questions; `implementation_no_mcp` and `research_mcp_readonly` require a separate active PRD; if the operator explicitly asks for Claude Code and it fails, diagnose Claude Code instead of silently switching to another agent family
- default to one worker agent at a time
- run at most two worker agents concurrently, and only when write sets and runtime resources are disjoint
- run reviewer agents selectively for security, DB, runtime/deploy, privacy/logging, production integration, or broad multi-file changes
- keep at most three subagent threads open and close completed threads immediately
- keep implementation workers open only for the same-patch review/fix loop; treat reviewers as one-shot and require `thread_disposition` in subagent final responses
- avoid parallel shell/tool calls while worker agents are active
- stop spawning agents and recover sequentially after executor/resource failures such as `Too many open files` or stream disconnects
- resume only after `git status --short --branch` and `git diff --check` can run
- project-local `AGENTS.md` may impose stricter lower limits

MCP tooling canon:

- use MCP or App connector tooling for supported structured external-service operations when available and authorized
- local `gh` auth and GitHub App connector auth are different identities with separate permissions
- configure GitHub App repository access and permissions in GitHub Installed Apps, not by changing the local `gh` token
- never record tokens in repo docs, PRDs, issues, or PR bodies
- if the App connector is blocked or missing, use the canonical shell-safe `gh` fallback and record the gap when it affects the slice

Kernel sync canon:

- every serious consumer-project slice begins with `kernel_upstream_check`
- consumer repositories carry `.kernel/upstream.json` with an exact pinned kernel commit
- if upstream differs from the pinned commit, the project records `update_available` and either opens/updates a `kernel_adoption_task` or explicitly defers adoption
- `kernel_adoption_task` records one decision:
  - `adopt_now`
  - `defer`
  - `not_applicable`
- `.kernel/upstream.json` only advances after adoption is implemented and verified
- downstream repositories never auto-apply kernel changes blindly
- operators may optionally run `kernel_fleet_sweep` locally to scan several consumer repos in one pass without changing bootstrap minimums
- every serious slice ends with `kernel_sync_review`
- `kernel_impact` must be classified as `none`, `project_local_only`, or `promote_to_kernel`
- active PRDs and serious closeouts carry an explicit `Kernel Impact` decision
- only reusable process patterns belong in the universal kernel
- project-specific ops details stay in the project-local canon

Model-specific behavior is a thin adapter only:

- tool selection
- shell/editor constraints
- verbosity
- planning mechanics

Optional behavioral overlays are also allowed, but they stay thin:

- one compact behavior layer may be reused across `CLAUDE.md`, Cursor rules, and skill/plugin surfaces;
- that layer must remain subordinate to the engineering kernel and the project-local canon;
- keep one canonical overlay source and sync the derived surfaces instead of letting them drift;
- `alwaysApply` or implicit auto-apply is a project-level choice, not a universal kernel default.

Do not fork the engineering process by model unless a tool constraint truly forces it.

## Repository contents

- [SKILL.md](SKILL.md)
  - reusable skill entrypoint for agents
- [agents/openai.yaml](agents/openai.yaml)
  - skill metadata for Codex UI surfaces
- [ENGINEERING_KERNEL.yaml](ENGINEERING_KERNEL.yaml)
  - machine-readable kernel
- [references/BOOTSTRAP.md](references/BOOTSTRAP.md)
  - how to materialize the kernel into a project
- [references/MODEL_ADAPTERS.md](references/MODEL_ADAPTERS.md)
  - model adapter policy
- [references/BEHAVIORAL_OVERLAY.md](references/BEHAVIORAL_OVERLAY.md)
  - thin behavior-layer policy for `CLAUDE.md` / Cursor / skill/plugin surfaces
- [references/SUPERPOWERS_SKILL_ORCHESTRATION.md](references/SUPERPOWERS_SKILL_ORCHESTRATION.md)
  - how Superpowers and equivalent process skills should be used without replacing the kernel
- [references/AGENTIC_CODING_ORCHESTRATION.md](references/AGENTIC_CODING_ORCHESTRATION.md)
  - how an orchestrator should dispatch, limit, review, and recover worker/reviewer agents
- [references/PROJECT_LOCAL_WORKERS.md](references/PROJECT_LOCAL_WORKERS.md)
  - how to create project-local no-MCP coding/review/docs workers, global fallback workers, and worker selection rules
- [references/MCP_TOOLING.md](references/MCP_TOOLING.md)
  - how MCP and App connector tooling should be used with GitHub App permissions and `gh` fallback boundaries
- [references/EXECUTION_SURFACES.md](references/EXECUTION_SURFACES.md)
  - local-first versus GitHub Actions execution policy
- [references/ENVIRONMENT_PROMOTION.md](references/ENVIRONMENT_PROMOTION.md)
  - local, verify, staging, and production promotion policy
- [references/KERNEL_SYNC_POLICY.md](references/KERNEL_SYNC_POLICY.md)
  - how kernel learnings are promoted without polluting the universal core
- [references/KERNEL_UPSTREAM_AWARENESS.md](references/KERNEL_UPSTREAM_AWARENESS.md)
  - how consumer repositories notice upstream kernel changes and decide whether to adopt them
- [references/KERNEL_ADOPTION_TASK.md](references/KERNEL_ADOPTION_TASK.md)
  - exact downstream `Task` shape for adopting, deferring, or rejecting a kernel update
- [references/KERNEL_FLEET_SWEEP.md](references/KERNEL_FLEET_SWEEP.md)
  - how one operator machine can scan several consumer repos for kernel drift
- [references/RESEARCH_POLICY.md](references/RESEARCH_POLICY.md)
  - how research works, including the repo-local versus external-contract boundary
- [docs/external-source-of-truth-matrix-prd-2026-04-18.md](docs/external-source-of-truth-matrix-prd-2026-04-18.md)
  - decision record for explicit version/source-of-truth reconciliation inside external-contract slices
- [references/GITHUB_DELIVERY.md](references/GITHUB_DELIVERY.md)
  - how branch/PR/merge flow should work end-to-end
- [references/BUG_INTAKE.md](references/BUG_INTAKE.md)
  - how runtime incidents become deduplicated GitHub `Bug` issues
- [templates/project](templates/project)
  - reusable project-local files
- [scripts/bootstrap_project_kernel.py](scripts/bootstrap_project_kernel.py)
  - deterministic template copier
- [scripts/sync_github_labels.py](scripts/sync_github_labels.py)
  - repo-managed label sync for the kernel repo itself
- [scripts/check_kernel_upstream.py](scripts/check_kernel_upstream.py)
  - local-first kernel drift check for consumer repositories
- [scripts/kernel_fleet_sweep.py](scripts/kernel_fleet_sweep.py)
  - optional local multi-repo wrapper around `kernel_upstream_check`
- [docs/agent-engineering-kernel-prd-2026-04-17.md](docs/agent-engineering-kernel-prd-2026-04-17.md)
  - decision record for this repository
- [docs/research-boundary-prd-2026-04-18.md](docs/research-boundary-prd-2026-04-18.md)
  - decision record for the research-boundary classification rule
- [docs/behavioral-overlay-policy-prd-2026-04-20.md](docs/behavioral-overlay-policy-prd-2026-04-20.md)
  - decision record for optional thin behavior-only overlays across `CLAUDE.md` / Cursor / skill-plugin surfaces
- [docs/kernel-adoption-task-prd-2026-04-18.md](docs/kernel-adoption-task-prd-2026-04-18.md)
  - decision record for the canonical downstream kernel adoption task
- [docs/environment-promotion-canon-prd-2026-04-26.md](docs/environment-promotion-canon-prd-2026-04-26.md)
  - decision record for environment promotion canon
- [docs/agentic-coding-orchestration-prd-2026-04-27.md](docs/agentic-coding-orchestration-prd-2026-04-27.md)
  - decision record for orchestrated agentic coding limits and recovery protocol
- [docs/claude-code-subagent-canon-prd-2026-05-02.md](docs/claude-code-subagent-canon-prd-2026-05-02.md)
  - decision record for using Claude Code as a bounded no-MCP subagent adapter

## Bootstrap a project

Dry-run:

```bash
python3 scripts/bootstrap_project_kernel.py --target /absolute/path/to/repo
```

Apply:

```bash
python3 scripts/bootstrap_project_kernel.py --target /absolute/path/to/repo --apply
```

Force overwrite existing files:

```bash
python3 scripts/bootstrap_project_kernel.py --target /absolute/path/to/repo --apply --force
```

Sync the kernel repo labels from file to GitHub:

```bash
python3 scripts/sync_github_labels.py --dry-run
python3 scripts/sync_github_labels.py --apply
```

Check whether a consumer project is behind the current kernel:

```bash
python3 scripts/check_kernel_upstream.py --json
```

Optionally scan several consumer repos from one operator machine:

```bash
python3 scripts/kernel_fleet_sweep.py --json
```

## Validate this repository

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests
```

## Skill usage

The repository root is also the skill root. A Codex installation can expose it globally via symlink:

```bash
ln -s ~/Work/Vs/agent-engineering-kernel ~/.codex/skills/engineering-kernel
```

After that, agents can use the `engineering-kernel` skill as the reusable source for project bootstrap and workflow canon.

## Repository hygiene

This repository also carries the minimum GitHub community-health layer for the kernel itself:

- [LICENSE](LICENSE)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)
- [CHANGELOG.md](CHANGELOG.md)
- [.github/labels.yml](.github/labels.yml)
- [.github/CODEOWNERS](.github/CODEOWNERS)
- [.github/ISSUE_TEMPLATE](.github/ISSUE_TEMPLATE)
- [.github/pull_request_template.md](.github/pull_request_template.md)
- [.github/workflows/tests.yml](.github/workflows/tests.yml)

## Contact and community

- **Issues:** [github.com/alexxety/agent-engineering-kernel/issues](https://github.com/alexxety/agent-engineering-kernel/issues) — bugs, feature requests, questions
- **Pull Requests:** see [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution flow
- **Direct message (Telegram):** [@Shiva_Mart](https://t.me/Shiva_Mart) — private conversation if you don't want to use public tracker
- **Telegram channel:** [@alexeydudarik](https://t.me/alexeydudarik) — updates and devlog
- **Blog:** [dudarik.com](https://dudarik.com)

## License

MIT — see [LICENSE](LICENSE).
