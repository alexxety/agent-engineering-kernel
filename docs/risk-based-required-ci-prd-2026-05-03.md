# Risk-Based Required CI PRD

Date: 2026-05-03
Issue: #55

## Source Learning

This kernel update promotes a verified downstream learning from `telethone` #350 / PR #351.

The downstream problem was practical: a single self-hosted runner kept small PRs waiting for the full backend, frontend, and supply-chain matrix. The unsafe shortcut would be workflow-level path filters or commit-message skips on required workflows.

## External Contract

Fresh GitHub documentation checked on 2026-05-03:

- GitHub documents that workflow-level path filtering, branch filtering, or skip commit messages can leave required checks in `Pending` when the workflow is skipped before jobs are created.
- GitHub documents that skipped jobs report `Success` and do not block required checks.
- GitHub workflow syntax supports job-level `jobs.<job_id>.if` conditions.

## Decision

For required CI workflows:

- keep required workflows triggered;
- add a lightweight classifier job;
- use job-level `if` conditions to skip expensive irrelevant jobs;
- treat skipped jobs as acceptable only when the job was created and skipped by the documented classifier;
- force full required CI for main, release/deploy, scheduled, manual, dependency, workflow, and explicit `full-ci` override changes.

## Acceptance

- `ENGINEERING_KERNEL.yaml` records the rule.
- `references/EXECUTION_SURFACES.md` explains the pattern and why workflow-level skips are not the default optimization path.
- Project templates carry the rule into downstream `README.md`, `AGENTS.md`, and `CONTRIBUTING.md`.
- Deterministic tests prevent regression.

## Kernel Impact

This is the universal kernel change. Consumer repositories may adopt it through their normal `kernel_upstream_check` / `kernel_adoption_task` flow.
