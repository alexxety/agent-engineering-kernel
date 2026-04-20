# PRD: Thin behavioral overlay and multi-surface sync policy

Date: `2026-04-20`

Status: `completed`

Primary Task: `#28`

## Problem

Some projects want a compact behavior-only layer for agent ergonomics across surfaces such as:

- `CLAUDE.md`
- Cursor rules
- skill/plugin wrappers

That pattern can be useful, but it creates two recurring failure modes when it is adopted without kernel discipline:

- one small behavior file starts pretending to be the whole engineering operating system;
- multiple tool-specific copies drift until each surface teaches a different workflow.

The shared kernel needs an explicit rule for when this pattern is acceptable and what boundary keeps it from replacing repo canon.

## Research Basis

- Slice classification: `repo_local_slice`
- Project-local source reviewed: `forrestchang/andrej-karpathy-skills`

Verified observations from the reviewed repository:

- the strongest reusable idea is structural, not textual;
- one compact behavior layer is materialized across several agent surfaces;
- the repository treats those surfaces as synchronized variants of the same small guidance set.

## Decision

The universal kernel now allows an optional behavioral overlay layer with these hard constraints:

- it is optional, not bootstrap default;
- it stays thin relative to the engineering kernel and the project-local canon;
- if several agent surfaces exist, there must be one canonical overlay source and the rest are derived variants;
- `AGENTS.md`, PRD-first execution, issue-first delivery, verification, `kernel_upstream_check`, and `kernel_sync_review` remain higher priority than the overlay;
- auto-apply or `alwaysApply` behavior is a project-level choice, not a universal kernel default.

## Files To Change

- `ENGINEERING_KERNEL.yaml`
- `README.md`
- `SKILL.md`
- `references/BEHAVIORAL_OVERLAY.md`
- `references/BOOTSTRAP.md`
- `references/MODEL_ADAPTERS.md`
- `templates/project/AGENTS.md`
- `templates/project/README.md`
- `tests/test_repo_kernel_canon.py`

## Success Condition

The kernel is correct for this slice when:

- future projects can adopt a thin behavior-only layer without confusing it for the full workflow canon;
- multi-surface overlays are treated as one synced concept rather than drifting independent files;
- the shared kernel remains model-agnostic and process-first.
