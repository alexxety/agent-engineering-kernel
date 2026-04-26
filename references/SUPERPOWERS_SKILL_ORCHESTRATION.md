# Superpowers Skill Orchestration

Use this reference when a project has Superpowers or an equivalent process-skill pack available.

## Purpose

The engineering kernel defines the operating system: PRD-first work, issue hierarchy, research policy, verification, delivery, and kernel sync.

Superpowers skills are the tactical agent workflow layer. They tell the agent how to execute a moment of work without replacing the repo-local canon.

## Priority

Follow this order:

1. Direct user instruction
2. Project-local canon and active PRD
3. Engineering kernel
4. Applicable Superpowers or equivalent process skill
5. Model default behavior

If a Superpowers skill conflicts with the active PRD, `AGENTS.md`, repository tests, or an explicit user instruction, follow the higher-priority source and record the exception when it affects the slice.

## Required Skill Check

When a relevant Superpowers skill is available, the agent must read or invoke it before acting.

If skill tooling is unavailable, the agent still applies the same principles manually:

- design before implementation for new behavior
- explicit plan before multi-step edits
- TDD for implementation and bugfixes
- systematic root-cause investigation before fixes
- fresh verification before completion claims
- review before merge or handoff

Record the tooling gap in the active PRD, plan, or closeout only when it changes the work or verification.

## Canonical Mapping

Use `using-superpowers` at conversation start when the platform exposes it.

Use `brainstorming` when the task creates or changes behavior, UI, architecture, workflows, or project structure. Its output should reconcile with the project PRD or decision-doc location; do not create a parallel spec system if the project already has one.

Use `writing-plans` after a spec or requirement set exists and the work has multiple steps. Plans must reference exact files, verification commands, and rollback expectations.

Use `test-driven-development` before implementation code for features and bugfixes, except for documented exceptions such as pure docs, generated code, or throwaway prototypes.

Use `systematic-debugging` for bugs, failed tests, build failures, regressions, and unexpected behavior before proposing fixes.

Use `using-git-worktrees` when the work needs branch isolation or when executing an implementation plan. Project branch/worktree policy remains higher priority.

Use `dispatching-parallel-agents` only for independent problem domains with no shared write scope.

Use `subagent-driven-development` for independent plan tasks only when the platform supports subagents and the user or project policy permits them. Otherwise use `executing-plans`.

Use `requesting-code-review` before merge or after major tasks, and `receiving-code-review` before implementing review feedback.

Use `verification-before-completion` before any success, fixed, passing, done, commit-ready, or PR-ready claim.

Use `finishing-a-development-branch` after implementation is complete and verification is fresh.

Use `writing-skills` when creating or modifying reusable skills.

## Non-Goals

Do not vendor-copy Superpowers skill text into project canon when a short mapping is enough.

Do not let a skill pack bypass:

- PRD-first execution
- GitHub `Epic / Task / Bug`
- `kernel_upstream_check`
- `kernel_sync_review`
- external-contract research requirements
- the project verification matrix

Do not run subagent or parallel workflows merely because a skill mentions them. They require platform support, clear independence, and user or project permission.
