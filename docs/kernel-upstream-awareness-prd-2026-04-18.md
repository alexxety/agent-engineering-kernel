# PRD: Kernel upstream awareness for multi-project consumers

Date: `2026-04-18`

Status: `completed`

## Problem

`agent-engineering-kernel` is now shared by multiple repositories. One project can promote a learning into the kernel, while another consumer project remains pinned to an older kernel state without any explicit awareness check. Template/bootstrap repos do not auto-sync after generation, so downstream drift is currently silent unless an operator notices it manually.

## Research Basis

- Slice classification: `external_contract_slice`
- Tavily-first research used: `yes`
- Official docs used: `yes`

Confirmed external facts:

- GitHub template repositories are one-time generation, not built-in sync channels.
- GitHub documents releases/tags as the canonical way to view version history.
- Community tooling such as `cruft` uses explicit pinned upstream commit metadata plus `check/update` commands instead of silent propagation.

## Current State

Verified facts only.

- Kernel already has `kernel_sync_review` / `Kernel Impact` for promoting learnings back into the upstream kernel.
- Kernel does not yet define the inverse check for consumer repos.
- Bootstrapped projects do not yet record which exact kernel commit they came from.
- Bootstrapped projects do not yet ship a canonical upstream-check script.

## Target State

- Kernel defines a formal `kernel_upstream_check` protocol for consumer projects.
- Every bootstrapped consumer repo carries `.kernel/upstream.json` with:
  - upstream repo URL
  - upstream default branch
  - exact pinned kernel commit
- Every bootstrapped consumer repo ships `scripts/check_kernel_upstream.py`.
- Consumer repos can detect `current | update_available | not_configured | unknown`.
- If drift exists, the project opens/updates a local `Task` or explicitly documents deferral.
- Kernel changes are never auto-applied blindly.

## Write Scope

- `SKILL.md`
- `ENGINEERING_KERNEL.yaml`
- `README.md`
- `references/BOOTSTRAP.md`
- `references/GITHUB_DELIVERY.md`
- `references/KERNEL_SYNC_POLICY.md`
- new `references/KERNEL_UPSTREAM_AWARENESS.md`
- `scripts/bootstrap_project_kernel.py`
- new `scripts/check_kernel_upstream.py`
- `templates/project/AGENTS.md`
- `templates/project/README.md`
- `templates/project/CONTRIBUTING.md`
- `templates/project/docs/PRD_TEMPLATE.md`
- new `templates/project/.kernel/upstream.json`
- new `templates/project/scripts/check_kernel_upstream.py`
- tests

## Rollout

### Phase 1
- Add the new upstream-awareness canon and reference docs.
- Validation:
  - machine-readable kernel parses
  - docs mention `kernel_upstream_check`

### Phase 2
- Materialize consumer metadata and check script in templates/bootstrap.
- Validation:
  - bootstrap dry-run/apply includes the new files
  - `.kernel/upstream.json` is pinned to the current kernel commit, not placeholder junk

### Phase 3
- Add regression tests for current/update/not-configured states.
- Validation:
  - targeted tests pass
  - end-to-end bootstrap + local checker output is stable

## Verification Matrix

- code-path tests
  - parser/checker tests for `current`, `update_available`, `not_configured`
- build/runtime checks
  - `py_compile` for added scripts
- source-of-truth / sync checks
  - bootstrapped `.kernel/upstream.json` contains current kernel commit
- live checks
  - run the checker against the local kernel repo and a bootstrapped temp consumer repo
- rollback validation
  - reverting the new canon removes the metadata/check protocol cleanly

## Kernel Impact

- `promote_to_kernel`

Why:

This is universal process canon for any project consuming a shared upstream engineering kernel.

## Final State

- `kernel_upstream_check` is now a formal kernel protocol.
- consumer bootstrap now materializes `.kernel/upstream.json` with the exact pinned kernel commit
- consumer bootstrap now materializes `scripts/check_kernel_upstream.py`
- downstream status values are canonicalized as `current | update_available | not_configured | unknown`
- local-first verification proved that a freshly bootstrapped consumer project reports `current` against the live kernel repo
