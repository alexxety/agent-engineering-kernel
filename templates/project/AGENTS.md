# Project workflow canon

This repository follows the agent engineering kernel.

## Required order for non-trivial work

1. Research
2. Code audit
3. Reconciliation
4. Documentation first
5. Baseline verification when an existing deterministic contract already exists
6. Implementation
7. Post-change verification

## Skill-assisted execution canon

If Superpowers or an equivalent process-skill pack is available, agents must read or invoke the relevant skill before acting.

Priority order:

1. Direct user instruction
2. This project-local canon and the active PRD
3. The engineering kernel
4. Applicable Superpowers or equivalent process skill
5. Model default behavior

Canonical mapping:

- new behavior, feature design, UI, workflow, or architecture: `using-superpowers`, then `brainstorming`
- approved spec or multi-step requirements: `writing-plans`
- implementation or bugfix: `test-driven-development`
- bug, failed test, build failure, regression, or unexpected behavior: `systematic-debugging`
- isolated branch or plan execution workspace: `using-git-worktrees`
- independent parallel problem domains: `dispatching-parallel-agents`
- implementation plan with permitted subagents: `subagent-driven-development`
- implementation plan without subagents: `executing-plans`
- code review request or review response: `requesting-code-review`, `receiving-code-review`
- success, fixed, passing, done, commit-ready, or PR-ready claim: `verification-before-completion`
- verified branch completion: `finishing-a-development-branch`

Rules:

- Superpowers skills are tactical workflow aids, not a replacement for PRD-first, issue-first, verification, or kernel-sync discipline.
- The project canon remains the source of truth for requirements, scope, and verification.
- If a skill default conflicts with this canon, the active PRD, tests, or an explicit user instruction, follow the higher-priority source and record the exception when it affects the slice.
- If skill tooling is unavailable, apply the same principles manually and record the gap only when it changes the work or verification.
- Do not run subagent or parallel workflows unless the platform supports them and user or project policy permits them.

## Agentic coding orchestration canon

When this repository uses orchestrated agentic coding, one primary orchestrator remains accountable for:

- scope and task boundaries;
- research and source-of-truth reconciliation;
- worker write-set isolation;
- review decisions;
- tests and verification;
- documentation and handoff;
- git commits, PRs, merges, deploy checks, and rollback notes.

Worker agents are coding hands. They must receive a narrow task, explicit allowed write paths, forbidden paths/actions, verification commands, and a required return format.

When custom agents are available, implementation workers should be project-local
no-MCP workers. A rich orchestrator may use MCP/App connectors for research,
GitHub, browser, analytics, messaging, or other external operations, but coding
workers must not inherit that external tool surface.

Project-local worker files:

```text
.codex/config.toml
.codex/agents/project_code_worker.toml
scripts/claude-code-readonly-subagent.sh
```

Selection rules:

- use `project_code_worker` for scoped implementation changes and small docs updates in this repository
- use Claude Code only as an explicitly requested or project-authorized one-shot read-only reviewer/design reviewer unless an active PRD defines a stronger role
- add project-local specialist roles only after repeated need proves a clear boundary, for example `project_reviewer` for read-only diff/spec review or `project_docs_worker` for docs-only closeout writing
- use the global `code_worker_no_mcp` only as a fallback when the project-local worker is unavailable or the task is truly project-agnostic
- do not use built-in generic workers from a rich-MCP orchestrator session when a project-local no-MCP worker exists
- do not silently substitute GPT/Codex or another worker family when the operator explicitly asks for Claude Code and Claude Code fails; diagnose Claude Code CLI/auth/MCP/tool/process setup first
- if a worker needs external research or live service access, it returns `NEEDS_CONTEXT` and the orchestrator performs that step
- keep research, live runtime, deployment, provider consoles, customer data cleanup, and production operations with the orchestrator unless this project explicitly designs a narrow audited role for one of those surfaces

Default concurrency:

- one worker agent at a time;
- at most two worker agents in parallel, only when write sets and runtime resources are disjoint;
- at most one reviewer agent at a time unless review questions are independent;
- at most three open subagent threads total;
- close completed or errored agents immediately after recording their result.

Thread lifecycle:

- implementation workers may stay open only through the same-patch review/fix loop;
- close an implementation worker after its patch is accepted, rejected, blocked, taken over locally, or moved to a different write set;
- reviewer, explorer, and docs-specialist threads are one-shot by default; close them after recording the result;
- use a fresh reviewer for re-review after fixes;
- every subagent final response should include `thread_disposition`: `parent_may_close_thread`, `keep_open_for_same_patch_fix_loop`, or `blocked_needs_context`.

While worker agents are active:

- avoid parallel shell/tool calls;
- avoid broad repeated file scans unless needed;
- do not busy-poll agents;
- do not launch background services unless the task requires them.

Claude Code adapter rules:

- default Claude Code role is one-shot read-only review/design review;
- use Claude Code where second-model perspective has high leverage: UI/UX architecture, operator workflows, PRD/spec/runbook cleanup, independent plan/diff review, test planning, and refactor-boundary advice;
- enabled default modes are `design_readonly` and `review_readonly`;
- `implementation_no_mcp` and `research_mcp_readonly` require a separate active PRD with exact surface, identity, verification, and rollback;
- do not feed Claude Code the whole repository or a huge file by habit; prefer a context packet with the goal, exact question, relevant symbols/interfaces, focused snippets, and selected diff context; whole large files require an explicit reason;
- launch through `scripts/claude-code-readonly-subagent.sh` when available;
- prefer a direct Claude Code binary over wrapper binaries such as cmux;
- pin the controlled review model, defaulting to `claude-opus-4-7` unless the operator overrides it;
- use non-interactive `claude -p`, `--no-session-persistence`, `--output-format stream-json`, `--verbose`, `--mcp-config '{"mcpServers":{}}'`, and `--strict-mcp-config`;
- use explicit `--permission-mode dontAsk`; do not use `plan` mode for read-only workers;
- use the smallest tool set: no tools for smoke, `Read` for exact-file review, and `Read,Grep,Glob` only when repo search is required;
- use mode budget caps as runaway guardrails: USD 1 smoke, USD 5 exact-file review, USD 10 repo-search review unless the operator overrides them;
- do not use `--bare` for OAuth-backed local Claude Code sessions unless API-key or `apiKeyHelper` mode was explicitly configured and smoke-tested;
- recognize that OAuth non-`--bare` runs can still load user hooks/settings; fully hook-free `--bare` requires API-key or helper auth;
- do not grant Claude Code implementation, live systems, GitHub writes, database writes, messaging, secrets, or customer data access without an active PRD;
- process exit closes the Claude Code worker; if it hangs, terminate it, record partial evidence, and recover sequentially.

If the executor reports resource failures such as `Too many open files`, stream disconnects, or failed process creation:

1. stop spawning agents;
2. stop parallel shell/tool calls;
3. close completed or errored agent threads;
4. recover with sequential `true`, `git status --short --branch`, and `git diff --check`;
5. do not edit runtime code or claim verification until shell health is restored.

Project-local rules may make these limits stricter, especially for live production surfaces.

Git ref/index/worktree operations must be serialized per repository. Do not run
`git fetch`, `git pull`, `git switch`, `git checkout`, `git merge`, `git
rebase`, `git branch -d/-D`, or `git push` in parallel for the same repo. If a
ref lock race occurs, recover with sequential `git status --short --branch`,
the needed `git fetch`, `git pull --ff-only` when appropriate, and `git diff
--check`.

## Multi-agent release coordination canon

When several agents, branches, or worktrees touch the same production-bound
project, one orchestrator owns the release candidate.

Rules:

- `main` is source of truth only after the verified PR or integration PR is
  merged.
- Before merge, the source of truth is the active release candidate: branch,
  exact commit SHA, PR, deploy command, runtime state, and verification
  evidence.
- Do not recover production by deploying from a stale `main`, dirty checkout,
  detached runtime directory, or "closest" local folder.
- Multiple agent branches that must ship together go through an integration
  branch and draft PR before staging or production.
- Deploy only from a clean release-candidate worktree and the documented
  project deploy command.
- Runtime recovery starts by identifying live health, current deployed state,
  active PR/branch/SHA, deploy overlays/env, schema state, and logs.
- Workers do not deploy, mutate live databases, send live messages, or change
  provider consoles unless an active PRD creates a narrow audited role for that
  surface.
- A second agent touching live runtime must receive or reconstruct a handoff
  packet before acting.

Minimum handoff packet:

```text
repo path
source-of-truth branch
active worktree
current release candidate branch and SHA
issue or PR
staging and production URLs
documented deploy command
backup requirement
allowed actions
forbidden actions
verification commands
open questions
```

Production-bound closeout records:

- staging deploy and smoke evidence;
- production backup or restore point when schema/data can change;
- production deploy command and commit SHA;
- read-safe production smoke checks;
- log scan result;
- PR comment or closeout evidence;
- merge to `main` and release branch cleanup decision.

## Research canon

- use Tavily Search first, not Tavily Research first
- fetch/index known official URLs directly when already available
- do manual source reading, comparison, and synthesis before escalation
- use Tavily Research only as an explicitly justified expensive fallback for broad deep-sweeps
- classify each non-trivial slice before edits as `repo_local_slice` or `external_contract_slice`
- `repo_local_slice` may proceed from project truth, deterministic verification, and local runtime checks when only repo-owned behavior is changing
- `external_contract_slice` requires fresh external research before code or docs land
- every `external_contract_slice` must record an `external_source_of_truth_matrix` in the active PRD or decision note before implementation lands
- use official vendor docs to verify external contracts
- if a known URL already exists, fetch/index it directly instead of re-running broad search
- distinguish verified facts from assumptions

## MCP/App connector canon

- use MCP or App connector tooling for supported structured external-service operations when available and authorized
- local `gh` auth and GitHub App connector auth are different identities with separate permissions
- configure GitHub App repository access and permissions in GitHub Installed Apps, not by storing or editing tokens in repo files
- if an App connector returns a permission error, check its repository access and permissions before refreshing local `gh` auth
- use shell-safe `gh` fallback when connector tooling is unavailable, stale, or missing the needed operation
- do not paste or record tokens in PRDs, issues, PR bodies, or project docs

## Execution surface canon

- prefer the local operator machine first for ordinary development, debugging, research, and verification
- GitHub coordinates issues, PRs, check status, schedules, and deploy triggers; owned compute should execute routine work by default
- if the project already has self-hosted runners or can reasonably provide them, prefer them over paid GitHub-hosted Actions for recurring work
- document the project self-hosted runner label(s) before enabling recurring GitHub checks
- check local prerequisites before work starts
- if the repo defines a local bootstrap path, use or repair it before escalating elsewhere
- keep required workflows triggered and use risk-based classifier jobs plus job-level `if` gates for expensive jobs instead of workflow-level skips that can leave required checks `Pending`
- use `full-ci` or an equivalent explicit override for the full matrix; main, release, scheduled, manual, dependency, and workflow changes also run full CI
- use GitHub Actions for repository-native automation, schedules, deploys, and hosted verification that genuinely belongs there
- do not enable paid GitHub-hosted runners, dependency cache uploads, or long-lived artifact storage without an explicit PRD/decision note

## Environment promotion canon

- production-bound projects should use one codebase with separate `local`, disposable `verify`, `staging`, and `production` environments
- `local` is for developer/operator iteration and must not be treated as production data
- disposable `verify` owns mutating automated tests
- `staging` is production-like and uses sandbox or non-production provider identities
- `production` contains real users, real customer data, and production provider identities
- production secrets and production database URLs must not be copied into local config or local tests
- mutating automated tests must not run against production
- schema and deploy changes move through the repository's auditable delivery path
- project canon must document the production-safe migration/deploy command before production use
- project canon must document backup or restore-point path, staging smoke checks, production smoke checks, and rollback
- production data may move down to staging only through documented backup/restore and sanitization; local or staging data must not move up to production

## Cutover entitlement parity canon

- a new shell, navigation model, admin information architecture, or major UI cannot become default until it proves entitlement parity with the existing source of truth
- record cutover role-matrix evidence in the active PRD or closeout before default rollout
- the default role-matrix covers unauthenticated, personal user, workspace owner/admin, workspace member, enterprise/admin, and platform admin
- the default surface matrix covers desktop navigation, mobile navigation, command/search palette, topbar/page chrome, and direct restricted routes
- server authorization remains the security boundary, but UI surfaces that expose the wrong role experience are regressions

## Kernel sync canon

- every serious slice begins with `kernel_upstream_check`
- consumer metadata lives in `.kernel/upstream.json`
- if `kernel_upstream_check` reports `update_available`, open or update a `kernel_adoption_task` or explicitly defer adoption in the active PRD/closeout
- `kernel_adoption_task` records one decision:
  - `adopt_now`
  - `defer`
  - `not_applicable`
- `.kernel/upstream.json` advances only after the adoption slice is implemented and verified
- downstream repos do not auto-apply kernel changes blindly
- every serious slice ends with `kernel_sync_review`
- record `Kernel Impact` as one of:
  - `none`
  - `project_local_only`
  - `promote_to_kernel`
- only promote reusable process patterns into the universal kernel
- keep project-specific operational rules in this repository, not in the universal kernel

## Session issue sync canon

Every serious slice records `Issue Sync: updated | skipped | not_applicable`
at closeout.

Use:

- `updated` when the relevant GitHub issue body, status, next step,
  verification, labels, or links were brought current
- `skipped` when issue sync normally applies but was intentionally skipped
  with a recorded reason
- `not_applicable` when the slice has no durable issue state to update

Rules:

- search existing issues before creating a new issue
- put durable state in the issue body instead of burying it in comments
- use comments only for short chronological notes, explicit user-requested
  notes, or external blockers
- surface stale, orphaned, or contradictory issue state instead of silently
  hiding it
- do not close issues without verified completion and project-local authority
- do not write private customer, credential, secret, or production-sensitive
  details to public issues
- weekly labels, CRM pointers, GitHub Projects fields, and weekly planning
  cadence are optional project-local policies, not universal invariants
- Issue Sync records the decision; it does not grant automatic GitHub write
  authority

## GitHub workflow canon

- non-trivial work starts from a parent GitHub issue
- canonical hierarchy:
  - `Epic`
  - `Task`
  - `Bug`
- use sub-issues for multi-slice work
- PR closes the leaf issue only, not the parent epic
- when invoking `gh issue create`, `gh issue edit`, or `gh pr create` from shell, use `--body-file` instead of inline double-quoted `--body`
- prefer MCP or App connector writes for GitHub issue/PR operations when the connector has the needed GitHub App permissions
- if a file is inconvenient, write it first with a single-quoted heredoc such as `<<'EOF'`
- when linking sub-issues from CLI, prefer `scripts/link_github_sub_issue.py` or GraphQL `addSubIssue` after resolving issue node ids
- if REST is used directly, `sub_issue_id` means child issue database id, not `#issue_number`
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
5. capture baseline verification when an existing deterministic contract already exists
6. implement in a small slice
7. open or update draft PR
8. run post-change verification
9. mark PR ready
10. merge
11. delete head branch

## Minimum verification contract

- pre-change baseline when an existing deterministic contract already exists
- code-path tests
- build/runtime checks
- source-of-truth / sync checks
- live checks when runtime or state changes
- sandbox identity guardrails for live external writes
- rollback path

Rules:

- bugfixes should prefer a reproducer before the fix;
- refactors should prefer before/after equivalence checks;
- docs-only, canon-only, or greenfield slices may skip pre-change baseline only when no existing deterministic contract exists.
- live verification that can write to an external service must use explicitly designated sandbox identities, never operator or production identities.

## Optional behavioral overlays

If this repository also uses a thin behavior-only layer such as `CLAUDE.md`, a Cursor project rule, or a skill/plugin wrapper:

- keep it optional and thin;
- keep one canonical overlay source if several derived variants exist;
- treat this `AGENTS.md`, the PRD, tests, and repo-local canon as higher priority than that overlay.
- treat process-skill packs such as Superpowers as workflow aids, not as replacements for this canon.

## Canon files

- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `.kernel/upstream.json`
- `.github/ISSUE_TEMPLATE/*`
- `.github/pull_request_template.md`
- `.github/CODEOWNERS`
- `.github/labels.yml`
- `scripts/sync_github_labels.py`
- `scripts/check_kernel_upstream.py`
- `scripts/claude-code-readonly-subagent.sh`
- active PRD / decision doc in `docs/`
