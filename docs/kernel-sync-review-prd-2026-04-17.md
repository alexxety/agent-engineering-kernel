# PRD: Kernel Sync Review Canon

Date: `2026-04-17`

Status: `active`

## Problem

The kernel does not yet formalize how live project learnings should be reviewed and promoted back into the universal kernel. Without that rule, agents either forget reusable lessons or pollute the kernel with project-local specifics.

## Current State

The kernel already defines PRD-first execution, issue hierarchy, local-first execution, and automatic bug intake. It does not yet define a required closure step for deciding whether a finished slice has reusable kernel impact.

## Target State

The kernel defines one formal sub-protocol:

- `kernel_sync_review`

And one required decision field:

- `kernel_impact = none | project_local_only | promote_to_kernel`

Templates, docs, and machine-readable kernel state all carry this canon so new projects inherit it automatically.

## Write Scope

- `ENGINEERING_KERNEL.yaml`
- `SKILL.md`
- `README.md`
- `references/BOOTSTRAP.md`
- `references/KERNEL_SYNC_POLICY.md`
- `templates/project/AGENTS.md`
- `templates/project/CONTRIBUTING.md`
- `templates/project/docs/PRD_TEMPLATE.md`
- kernel tests

## Rollout

1. Add machine-readable kernel sync policy.
2. Add reference documentation and skill wiring.
3. Add template-level `Kernel Impact`.
4. Update tests and bootstrap verification.

## Verification Matrix

- code-path tests: kernel unit tests
- build/runtime checks: bootstrap apply into temp target
- source-of-truth / sync checks: generated files contain new canon
- live checks: GitHub issue/PR flow in kernel repo
- rollback validation: revert kernel sync policy files and rerun tests
