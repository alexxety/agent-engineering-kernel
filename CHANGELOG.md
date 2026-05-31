# Changelog

All notable changes to `agent-engineering-kernel` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Updated the canonical Claude Code read-only worker default model from `claude-opus-4-7` to `claude-opus-4-8` across kernel policy, docs, project templates, wrapper script, and tests.
- Added operational canon layers for work item routing, project health audit, and optional weekly operating loops.
- Added session issue sync canon so serious slices record whether GitHub issue state was updated, intentionally skipped, or not applicable.
- Added agentic coding orchestration canon: orchestrator/worker/reviewer roles, subagent concurrency limits, prompt write-set contract, review boundaries, and recovery protocol for executor resource failures.
- Added project-local no-MCP worker canon and templates so rich-MCP orchestrators can dispatch lightweight implementation workers with global fallback behavior.
- Added Claude Code subagent adapter canon for one-shot read-only review, strict empty MCP startup, OAuth-safe CLI defaults, and no silent fallback to another agent family when Claude Code was explicitly requested.
- Tightened Claude Code subagent runtime defaults with direct-binary preference, stream-json visibility, explicit non-plan permission mode, mode-specific tool allowlists, and larger review budget guardrails.
- Clarified Claude Code operating modes: `design_readonly` and `review_readonly` are enabled by the default wrapper, while `implementation_no_mcp` and `research_mcp_readonly` require separate active PRDs with explicit surfaces and verification.
- Added Claude Code context-packet guardrail: prefer focused snippets, symbol/interface excerpts, and selected diff context before sending huge or whole files to external workers.
- Added explicit subagent thread lifecycle rules: same-patch worker fix loops, one-shot reviewers, fresh re-reviewers, and required `thread_disposition` in final responses.
- Added Superpowers-compatible process-skill orchestration to the kernel canon and project templates.
- Added MCP/App connector tooling policy, including GitHub App permission checks, different identities for connector versus local `gh`, and shell-safe fallback behavior.
- Research policy is now explicitly Tavily Search-first, not Tavily Research-first. Tavily Research is reserved for explicitly justified expensive broad deep-sweeps after search, known official docs, and manual synthesis are insufficient.

## [0.1.0] - 2026-04-20

First public release. Kernel is functional and self-consuming (dog-fooded on its own development), but API surface (policy names, YAML keys, script flags) is not frozen — expect breaking changes on minor bumps until `1.0.0`.

### Added

- `ENGINEERING_KERNEL.yaml` — machine-readable kernel canon with 12 policies: research, execution, kernel_sync, model_adapter, behavioral_overlay, research_policy, bug_intake, kernel_upstream_awareness, kernel_adoption_task, and others.
- `SKILL.md` + `agents/openai.yaml` — Codex skill entrypoint.
- `references/` — 11 long-form policy references (BOOTSTRAP, BEHAVIORAL_OVERLAY, BUG_INTAKE, RESEARCH_POLICY, KERNEL_SYNC_POLICY, KERNEL_UPSTREAM_AWARENESS, KERNEL_ADOPTION_TASK, KERNEL_FLEET_SWEEP, GITHUB_DELIVERY, MODEL_ADAPTERS, EXECUTION_SURFACES).
- `docs/` — PRD decision records per policy.
- `templates/project/` — bootstrap template: AGENTS.md, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, `.github/` (ISSUE_TEMPLATE, labels.yml, CODEOWNERS, pull_request_template), `.kernel/upstream.json`, PRD template, `scripts/check_kernel_upstream.py`.
- `scripts/` — `bootstrap_project_kernel.py`, `check_kernel_upstream.py`, `kernel_fleet_sweep.py`, `link_github_sub_issue.py`, `sync_github_labels.py`.
- `tests/` — unittest suite: 6 test modules covering scripts and YAML canon invariants.
- Community health files: LICENSE (MIT), CODE_OF_CONDUCT, CONTRIBUTING, SECURITY.
- `.github/` baseline: CODEOWNERS, ISSUE_TEMPLATE (bug, feature, kernel-adoption, sync-review), pull_request_template, labels.yml.

### Changed

- Pre-publish cleanup: all absolute `/Users/<username>/Work/Vs/agent-engineering-kernel/...` references in markdown converted to relative paths, shell examples use `~/...` ([#32](https://github.com/alexxety/agent-engineering-kernel/pull/32)).

### Security

- No secrets, credentials or tokens in tracked files or git history (audited before going public).

[Unreleased]: https://github.com/alexxety/agent-engineering-kernel/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/alexxety/agent-engineering-kernel/releases/tag/v0.1.0
