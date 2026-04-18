# PRD: Canonical Kernel Adoption Task

Date: `2026-04-18`

Status: `completed`

## Problem

The kernel already defines `kernel_upstream_check`, but downstream repos only know that they should open or update a project-local `Task` when the checker reports `update_available`. The kernel does not yet define the exact canonical shape of that work item. Without a stable name, decision model, and checklist, downstream adoption drifts into free-form prose and inconsistent verification.

## Research Basis

- slice classification: `repo_local_slice`
- external Tavily research used: `no`
- official docs used: `no`
- live runtime evidence used: `yes`

Why:

This slice changes the internal engineering kernel only. The source of truth is the existing kernel canon, current consumer-repo behavior, and current fleet-sweep output. No vendor or external API contract is changing.

## Current State

Verified facts only:

- The kernel already defines `kernel_upstream_check`, `.kernel/upstream.json`, and the statuses `current | update_available | not_configured | unknown`.
- The kernel already states that downstream repos must open or update a project-local `Task` or explicitly defer adoption when `update_available` is reported.
- The kernel does not yet define a canonical task name, canonical decision values, or a required checklist for that adoption task.
- Current consumer repos (`dudarik.com`, `yotubol`) therefore only carry the generic wording about “open or update a Task”.

## Target State

- The kernel defines a canonical downstream work item name: `kernel_adoption_task`.
- The kernel defines canonical decisions for that task:
  - `adopt_now`
  - `defer`
  - `not_applicable`
- The kernel defines the minimum required fields/checklist for the task:
  - target upstream commit
  - linked kernel delta summary/reference
  - decision
  - exact local write scope
  - verification plan
  - `.kernel/upstream.json` update rule
  - defer reason and review trigger when deferred
- Kernel references, templates, and tests encode this canon.
- Active consumer repos inherit the same canon in their local docs.

## Write Scope

- `ENGINEERING_KERNEL.yaml`
- `SKILL.md`
- `README.md`
- `references/KERNEL_UPSTREAM_AWARENESS.md`
- `references/GITHUB_DELIVERY.md`
- new reference for the adoption task canon
- `templates/project/README.md`
- `templates/project/AGENTS.md`
- `templates/project/CONTRIBUTING.md`
- `templates/project/docs/PRD_TEMPLATE.md`
- kernel tests
- consumer repo docs/tests needed to keep active repos aligned

## Rollout

### Phase 1: Kernel canon

Entry condition:
- active PRD exists

Actions:
- add the canonical `kernel_adoption_task` rules to the kernel
- add a dedicated reference doc
- update templates and machine-readable kernel state
- add regressions

Validation:
- kernel unit tests
- template/bootstrap related tests

Success condition:
- kernel repo contains a stable canon for downstream adoption tasks

Rollback trigger:
- tests fail or the canon conflicts with the existing upstream-awareness protocol

### Phase 2: Consumer sync

Entry condition:
- kernel Phase 1 merged locally and green

Actions:
- sync the new adoption-task canon into active consumer repos
- add project-local regressions where needed

Validation:
- project-local canon tests
- local `check_kernel_upstream.py --json`
- local fleet sweep

Success condition:
- active consumers mention the canonical adoption-task contract and still report `current`

Rollback trigger:
- consumer docs/tests drift or fleet sweep regresses from `current`

## Verification Matrix

- code-path tests:
  - kernel canon tests
  - consumer canon tests
- build/runtime checks:
  - `python3 -m py_compile` for touched scripts if any
- source-of-truth / sync checks:
  - consumer `.kernel/upstream.json` still parses
  - fleet sweep still reports expected statuses
- live checks:
  - per-consumer `scripts/check_kernel_upstream.py --json`
  - operator `kernel_fleet_sweep.py --json`
- rollback validation:
  - remove the new canon and verify existing upstream-awareness behavior still stands if rollback is required

## Kernel Impact

- `promote_to_kernel`

Why:

This slice defines a reusable downstream-adoption workflow that every kernel consumer can share.

## Closure

- kernel now defines the canonical downstream work item `kernel_adoption_task`
- canonical decisions are fixed as `adopt_now | defer | not_applicable`
- kernel references, templates, and tests were updated accordingly
- verification passed:
  - `.venv/bin/python -m unittest discover -s tests`
  - `python3 -m py_compile scripts/check_kernel_upstream.py scripts/kernel_fleet_sweep.py scripts/bootstrap_project_kernel.py`
