# Agent Engineering Kernel

Universal engineering kernel for agent-led software work.

This repository is the standalone source-of-truth for:

- PRD-first execution
- GitHub issue decomposition
- PR verification discipline
- project bootstrap templates
- a reusable Codex skill
- repo-managed GitHub metadata and community-health baseline
- kernel sync review for promoting proven project learnings back into the universal kernel
- optional GitHub Projects layer only when the repository actually needs shared planning views beyond issue-first execution
- kernel upstream awareness so consumer repositories can detect kernel drift explicitly
- a canonical `kernel_adoption_task` so downstream repos handle kernel drift deterministically
- optional kernel fleet sweep so one operator machine can review many consumer repos at once

The goal is simple: a new agent in a new repository should not need the workflow re-explained in chat.

Execution-surface canon:

- ordinary engineering work should default to the local operator machine first
- self-hosted runners are preferred over paid GitHub-hosted Actions when the repository already has them
- GitHub Actions remain for repo-native automation, schedules, deploys, and hosted checks that actually belong there

## Core idea

Use one shared engineering process across agent families.

Shared core:

- research
- code audit
- reconciliation
- documentation first
- baseline verification when an existing contract already exists
- implementation
- post-change verification
- GitHub `Epic / Task / Bug` hierarchy
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

- Tavily first
- classify each non-trivial slice before edits as `repo_local_slice` or `external_contract_slice`
- `repo_local_slice` may proceed from project truth, deterministic verification, and local runtime checks when only repo-owned behavior is changing
- `external_contract_slice` requires fresh external research before code or docs land
- every `external_contract_slice` records an `external_source_of_truth_matrix` in the active PRD or decision note
- official docs for external contracts
- known URLs fetched directly when already available

Verification canon:

- define verification before edits
- when a deterministic contract already exists, capture the smallest relevant baseline before editing
- for bugfixes, prefer a reproducer first
- for refactors, prefer before/after equivalence checks
- for docs-only, canon-only, or greenfield slices without an existing contract, do not invent a fake pre-change baseline
- post-change verification before publish remains mandatory

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

- [SKILL.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/SKILL.md)
  - reusable skill entrypoint for agents
- [agents/openai.yaml](/Users/raketa23/Work/Vs/agent-engineering-kernel/agents/openai.yaml)
  - skill metadata for Codex UI surfaces
- [ENGINEERING_KERNEL.yaml](/Users/raketa23/Work/Vs/agent-engineering-kernel/ENGINEERING_KERNEL.yaml)
  - machine-readable kernel
- [references/BOOTSTRAP.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/BOOTSTRAP.md)
  - how to materialize the kernel into a project
- [references/MODEL_ADAPTERS.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/MODEL_ADAPTERS.md)
  - model adapter policy
- [references/BEHAVIORAL_OVERLAY.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/BEHAVIORAL_OVERLAY.md)
  - thin behavior-layer policy for `CLAUDE.md` / Cursor / skill/plugin surfaces
- [references/EXECUTION_SURFACES.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/EXECUTION_SURFACES.md)
  - local-first versus GitHub Actions execution policy
- [references/KERNEL_SYNC_POLICY.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/KERNEL_SYNC_POLICY.md)
  - how kernel learnings are promoted without polluting the universal core
- [references/KERNEL_UPSTREAM_AWARENESS.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/KERNEL_UPSTREAM_AWARENESS.md)
  - how consumer repositories notice upstream kernel changes and decide whether to adopt them
- [references/KERNEL_ADOPTION_TASK.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/KERNEL_ADOPTION_TASK.md)
  - exact downstream `Task` shape for adopting, deferring, or rejecting a kernel update
- [references/KERNEL_FLEET_SWEEP.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/KERNEL_FLEET_SWEEP.md)
  - how one operator machine can scan several consumer repos for kernel drift
- [references/RESEARCH_POLICY.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/RESEARCH_POLICY.md)
  - how research works, including the repo-local versus external-contract boundary
- [docs/external-source-of-truth-matrix-prd-2026-04-18.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/docs/external-source-of-truth-matrix-prd-2026-04-18.md)
  - decision record for explicit version/source-of-truth reconciliation inside external-contract slices
- [references/GITHUB_DELIVERY.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/GITHUB_DELIVERY.md)
  - how branch/PR/merge flow should work end-to-end
- [references/BUG_INTAKE.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/BUG_INTAKE.md)
  - how runtime incidents become deduplicated GitHub `Bug` issues
- [templates/project](/Users/raketa23/Work/Vs/agent-engineering-kernel/templates/project)
  - reusable project-local files
- [scripts/bootstrap_project_kernel.py](/Users/raketa23/Work/Vs/agent-engineering-kernel/scripts/bootstrap_project_kernel.py)
  - deterministic template copier
- [scripts/sync_github_labels.py](/Users/raketa23/Work/Vs/agent-engineering-kernel/scripts/sync_github_labels.py)
  - repo-managed label sync for the kernel repo itself
- [scripts/check_kernel_upstream.py](/Users/raketa23/Work/Vs/agent-engineering-kernel/scripts/check_kernel_upstream.py)
  - local-first kernel drift check for consumer repositories
- [scripts/kernel_fleet_sweep.py](/Users/raketa23/Work/Vs/agent-engineering-kernel/scripts/kernel_fleet_sweep.py)
  - optional local multi-repo wrapper around `kernel_upstream_check`
- [docs/agent-engineering-kernel-prd-2026-04-17.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/docs/agent-engineering-kernel-prd-2026-04-17.md)
  - decision record for this repository
- [docs/research-boundary-prd-2026-04-18.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/docs/research-boundary-prd-2026-04-18.md)
  - decision record for the research-boundary classification rule
- [docs/behavioral-overlay-policy-prd-2026-04-20.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/docs/behavioral-overlay-policy-prd-2026-04-20.md)
  - decision record for optional thin behavior-only overlays across `CLAUDE.md` / Cursor / skill-plugin surfaces
- [docs/kernel-adoption-task-prd-2026-04-18.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/docs/kernel-adoption-task-prd-2026-04-18.md)
  - decision record for the canonical downstream kernel adoption task

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
ln -s /Users/raketa23/Work/Vs/agent-engineering-kernel /Users/raketa23/.codex/skills/engineering-kernel
```

After that, agents can use the `engineering-kernel` skill as the reusable source for project bootstrap and workflow canon.

## Repository hygiene

This repository also carries the minimum GitHub community-health layer for the kernel itself:

- [LICENSE](/Users/raketa23/Work/Vs/agent-engineering-kernel/LICENSE)
- [CODE_OF_CONDUCT.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/CODE_OF_CONDUCT.md)
- [SECURITY.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/SECURITY.md)
- [.github/labels.yml](/Users/raketa23/Work/Vs/agent-engineering-kernel/.github/labels.yml)
- [.github/CODEOWNERS](/Users/raketa23/Work/Vs/agent-engineering-kernel/.github/CODEOWNERS)
- [.github/ISSUE_TEMPLATE](/Users/raketa23/Work/Vs/agent-engineering-kernel/.github/ISSUE_TEMPLATE)
- [.github/pull_request_template.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/.github/pull_request_template.md)
