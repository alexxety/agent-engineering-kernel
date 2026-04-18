# Canonical Kernel Adoption Task

Use this reference when a consumer repository reports `update_available` from `kernel_upstream_check`.

## Problem

Knowing that the kernel changed is not enough. Downstream repositories need one deterministic work-item shape for deciding whether and how to adopt that update.

## Canonical names

- work item: `kernel_adoption_task`
- issue type: `Task`

This is not a new top-level protocol. It is the canonical downstream work item triggered by `kernel_upstream_check` when adoption work is needed.

## Canonical decisions

- `adopt_now`
- `defer`
- `not_applicable`

## Required fields

Every `kernel_adoption_task` should capture:

- the target upstream kernel commit
- the current pinned downstream commit
- the kernel delta summary or reference link
- the chosen decision
- the exact local write scope if adoption happens now
- the verification plan

## Required rules

- if `kernel_upstream_check` reports `update_available`, open or update one `kernel_adoption_task` in the consumer repo unless the active slice explicitly defers adoption
- the task should remain one durable downstream tracker for that kernel delta, not a stream of duplicates
- `.kernel/upstream.json` advances only after the adoption slice is implemented and verified
- if the decision is `defer`, record:
  - why the update is deferred
  - what future trigger should cause re-review
- if the decision is `not_applicable`, record why the kernel delta does not apply to this repository

## Minimum checklist

- compare the consumer's pinned commit with the target upstream commit
- identify which kernel files/rules changed
- decide `adopt_now | defer | not_applicable`
- if adopting now:
  - update local docs/scripts/templates as needed
  - update `.kernel/upstream.json`
  - verify locally
- if deferring or marking not applicable:
  - leave `.kernel/upstream.json` unchanged
  - document the reason in the task or active PRD/closeout

## Relationship to other kernel flows

- `kernel_upstream_check`
  - detects drift at slice start
- `kernel_adoption_task`
  - tracks the downstream decision and implementation work when drift matters
- `kernel_sync_review`
  - decides whether a finished project slice should promote new learning back into the kernel
