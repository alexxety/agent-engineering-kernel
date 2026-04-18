# PRD: <title>

Date: `<YYYY-MM-DD>`

Status: `active`

## Problem

Describe the current gap.

## Current State

Verified facts only.

## Target State

What should be true after the change.

## Write Scope

Files, workflows, services, or systems expected to change.

## Kernel Upstream Check

Record near slice start.

- protocol: `kernel_upstream_check`
- status: `current | update_available | not_configured | unknown`
- action: `none | task_opened_or_updated | explicitly_deferred`
- `kernel_adoption_task`: `<issue id or n/a>`
- adoption decision when drift exists: `adopt_now | defer | not_applicable`

## Rollout

Phased plan with validation and rollback.

## Verification Matrix

- code-path tests
- build/runtime checks
- source-of-truth / sync checks
- live checks
- rollback validation

## Kernel Impact

Record this during `kernel_sync_review`.

Choose one:

- `none`
- `project_local_only`
- `promote_to_kernel`

Why:

Explain whether this slice produced a reusable engineering rule or only a project-local decision.
