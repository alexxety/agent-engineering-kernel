# PRD: Superpowers Skill Orchestration

Date: `2026-04-26`

Status: `active`

## GitHub Issues

- Epic: #38
- Task: #39

## Problem

The kernel already defines PRD-first, issue-first, verification-first engineering workflow, but it does not explicitly tell agents how to use Superpowers skills when they are available. That leaves a gap: a consumer project can have both the engineering kernel and Superpowers installed, yet the agent may treat them as unrelated systems.

## Current State

Verified facts:

- `ENGINEERING_KERNEL.yaml` has policies for PRD-first execution, research, execution surfaces, GitHub delivery, kernel sync, and model adapters.
- Project templates materialize `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, PRD templates, GitHub metadata, and sync scripts.
- Superpowers skills installed locally include `using-superpowers`, `brainstorming`, `writing-plans`, `test-driven-development`, `systematic-debugging`, `verification-before-completion`, `requesting-code-review`, `receiving-code-review`, `using-git-worktrees`, `dispatching-parallel-agents`, `subagent-driven-development`, `executing-plans`, `finishing-a-development-branch`, and `writing-skills`.
- No current kernel reference maps those skills into kernel priority, PRD-first execution, or project bootstrap.

## Target State

The kernel treats Superpowers as a tactical process-skill layer:

- agents must read or invoke relevant skills before acting when they are available;
- project-local canon, active PRD, tests, and explicit user instructions remain higher priority;
- core Superpowers triggers are mapped to kernel phases;
- subagent and parallel workflows require platform support and user or project permission;
- consumer project templates inherit the rule without copying full vendor skill text.

## Write Scope

- `ENGINEERING_KERNEL.yaml`
- `README.md`
- `SKILL.md`
- `CHANGELOG.md`
- `references/SUPERPOWERS_SKILL_ORCHESTRATION.md`
- `references/BOOTSTRAP.md`
- `references/MODEL_ADAPTERS.md`
- `references/BEHAVIORAL_OVERLAY.md`
- `templates/project/AGENTS.md`
- `templates/project/README.md`
- `templates/project/CONTRIBUTING.md`
- `templates/project/docs/PRD_TEMPLATE.md`
- `tests/test_repo_kernel_canon.py`

## Process Skills

- available skill pack: `Superpowers`
- relevant skills:
  - `using-superpowers`
  - `brainstorming`
  - `writing-plans`
  - `test-driven-development`
  - `systematic-debugging`
  - `verification-before-completion`
- exceptions or conflicts with project canon: `none`

## Kernel Upstream Check

This change updates the kernel itself, not a downstream consumer repository.

- protocol: `kernel_upstream_check`
- status: `not_applicable`
- action: `none`
- `kernel_adoption_task`: `n/a`
- adoption decision when drift exists: `not_applicable`

## Rollout

1. Add machine-readable `agent_skill_orchestration_policy`.
2. Add a durable reference document.
3. Update README, skill entrypoint, model adapter, bootstrap, behavioral overlay, and project templates.
4. Add tests that pin the new canon across YAML, docs, and templates.
5. Run the local unittest suite.

## Verification Matrix

- code-path tests: `.venv/bin/python -m unittest discover -s tests`
- build/runtime checks: YAML parsing through existing tests
- source-of-truth / sync checks: tests assert new reference and template coverage
- live checks: not required; docs and tests only
- rollback validation: revert the docs/templates/YAML/test changes as one slice if needed

## Kernel Impact

Record this during `kernel_sync_review`.

Choose one:

- `promote_to_kernel`

Why:

This slice adds a reusable process rule for every consumer project that combines the engineering kernel with Superpowers or another process-skill pack.
