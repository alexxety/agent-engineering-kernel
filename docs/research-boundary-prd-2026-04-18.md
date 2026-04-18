# PRD: Research Boundary Classification

Date: `2026-04-18`

Status: `active`

Primary Task: `#12`

## Problem

The universal kernel already says research matters and official docs should verify external contracts.

That is not yet specific enough.

Without an explicit boundary, agents make two opposite mistakes:

- they over-research repo-local UI or documentation slices that only need project truth and deterministic verification;
- they under-research dependency, vendor-platform, auth-contract, or compatibility slices and ship them from stale memory.

## Canonical distinction

Every non-trivial slice must be classified before edits as exactly one of:

- `repo_local_slice`
- `external_contract_slice`

### `repo_local_slice`

Use this only when the work changes repository-owned behavior such as:

- local UI copy, layout, navigation, or progressive disclosure
- local state and deterministic tests
- internal docs that describe already verified project behavior

Execution rule:

- project truth, deterministic verification, and local runtime checks are sufficient;
- fresh external research is optional.

### `external_contract_slice`

Use this whenever the work changes or claims current behavior for any changing outside system such as:

- dependency source, version, install flow, or packaging
- vendor/platform/API behavior
- external authentication/runtime assumptions
- interpreter or dependency compatibility

Execution rule:

- fresh external research is mandatory before code or docs land;
- prefer official docs and primary upstream/vendor sources;
- record evidence in the active PRD or decision note instead of leaving it only in chat.

## Files To Change

- `ENGINEERING_KERNEL.yaml`
- `references/RESEARCH_POLICY.md`
- `README.md`
- `templates/project/README.md`
- `templates/project/AGENTS.md`
- `templates/project/CONTRIBUTING.md`
- `tests/test_repo_kernel_canon.py`

## Verification

- `.venv/bin/python -m unittest discover -s tests`
- `git diff --check`

## Success Condition

The kernel is complete for this slice when future projects bootstrap a non-ambiguous research rule:

- repo-local slices can move from local truth without fake upstream discovery;
- external-contract slices cannot land without fresh external research and recorded evidence.
