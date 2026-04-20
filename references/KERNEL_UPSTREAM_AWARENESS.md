# Kernel Upstream Awareness

Use this reference when a shared `agent-engineering-kernel` is consumed by multiple downstream repositories.

## Problem

Template/bootstrap repos do not self-sync after generation. If one project promotes a learning into the kernel, other consumer repos need a deterministic way to notice that upstream changed and decide whether to adopt it.

## Canonical names

- protocol: `kernel_upstream_check`
- consumer metadata file: `.kernel/upstream.json`

Do not confuse this with `kernel_sync_review`.

- `kernel_upstream_check` happens near slice start in the consumer project
- `kernel_sync_review` happens near slice end after verification

## Required consumer metadata

Every bootstrapped consumer repository should carry:

- upstream kernel repository URL
- upstream default branch
- exact pinned kernel commit used by the consumer project

The pin must be explicit and immutable.

Do not treat template generation time as implicit truth.

## Required rules

- every serious consumer-project slice should begin with `kernel_upstream_check`
- `kernel_upstream_check` compares the project's pinned kernel commit with the upstream kernel default-branch head
- if upstream differs, record `update_available`
- downstream projects must not auto-apply kernel changes blindly
- kernel adoption remains an explicit project-local slice with PRD, issue tree, verification, and merge
- urgent incident work is not blocked by an available kernel update, but the drift must be recorded or turned into a project-local task
- the canonical downstream task name is `kernel_adoption_task`

## Canonical statuses

- `current`
- `update_available`
- `not_configured`
- `unknown`

## When update is available

If `kernel_upstream_check` reports `update_available`:

- open or update a `kernel_adoption_task` issue in the consumer repo to review/adopt the kernel update
- or explicitly defer the adoption in the active PRD/closeout
- the downstream decision model is:
  - `adopt_now`
  - `defer`
  - `not_applicable`

Do not silently ignore the drift.

See [KERNEL_ADOPTION_TASK.md](references/KERNEL_ADOPTION_TASK.md) for the exact downstream task shape and decisions.

## Optional operator layer

An operator machine may run `kernel_fleet_sweep` locally across many repositories and call the same checker contract in each consumer repo.

That fleet sweep is optional.

It is not part of the bootstrap minimum because it depends on the operator's local topology.

See [KERNEL_FLEET_SWEEP.md](references/KERNEL_FLEET_SWEEP.md).
