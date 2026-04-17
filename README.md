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
- implementation
- verification
- GitHub `Epic / Task / Bug` hierarchy
- automatic deduplicated `Bug` intake from verifier/watchdog/runtime gates
- PR closes leaf issue only

Bug-intake canon:

- runtime bugs come from canonical surfaces, not raw logs or Telegram alerts
- one stable fingerprint maps to one durable GitHub `Bug` issue
- repeated incidents update the open bug issue for that fingerprint instead of
  creating duplicates

Research canon:

- Tavily first
- official docs for external contracts
- known URLs fetched directly when already available

Kernel sync canon:

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
- [references/EXECUTION_SURFACES.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/EXECUTION_SURFACES.md)
  - local-first versus GitHub Actions execution policy
- [references/KERNEL_SYNC_POLICY.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/KERNEL_SYNC_POLICY.md)
  - how kernel learnings are promoted without polluting the universal core
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
- [docs/agent-engineering-kernel-prd-2026-04-17.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/docs/agent-engineering-kernel-prd-2026-04-17.md)
  - decision record for this repository

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
