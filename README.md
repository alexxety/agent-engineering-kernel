# Agent Engineering Kernel

Universal engineering kernel for agent-led software work.

This repository is the standalone source-of-truth for:

- PRD-first execution
- GitHub issue decomposition
- PR verification discipline
- project bootstrap templates
- a reusable Codex skill

The goal is simple: a new agent in a new repository should not need the workflow re-explained in chat.

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
- PR closes leaf issue only

Research canon:

- Tavily first
- official docs for external contracts
- known URLs fetched directly when already available

Model-specific behavior is a thin adapter only:

- tool selection
- shell/editor constraints
- verbosity
- planning mechanics

Do not fork the engineering process by model unless a tool constraint truly forces it.

## Repository contents

- [SKILL.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/SKILL.md)
  - reusable skill entrypoint for agents
- [ENGINEERING_KERNEL.yaml](/Users/raketa23/Work/Vs/agent-engineering-kernel/ENGINEERING_KERNEL.yaml)
  - machine-readable kernel
- [references/BOOTSTRAP.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/BOOTSTRAP.md)
  - how to materialize the kernel into a project
- [references/MODEL_ADAPTERS.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/references/MODEL_ADAPTERS.md)
  - model adapter policy
- [templates/project](/Users/raketa23/Work/Vs/agent-engineering-kernel/templates/project)
  - reusable project-local files
- [scripts/bootstrap_project_kernel.py](/Users/raketa23/Work/Vs/agent-engineering-kernel/scripts/bootstrap_project_kernel.py)
  - deterministic template copier
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
