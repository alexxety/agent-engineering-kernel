# PRD: External Source-Of-Truth Matrix For External-Contract Slices

Date: `2026-04-18`

Status: `active`

## Problem

The kernel already distinguishes `repo_local_slice` from `external_contract_slice` and already requires fresh research for external-contract work.

That is necessary but not sufficient.

An agent can still do all of the following and ship the wrong thing:

- classify the slice correctly;
- read fresh vendor docs;
- forget the repo's current pinned version or local source-of-truth file;
- revive a stale helper or old project note that no longer matches the active external contract.

This is the exact failure class behind stale dependency/version/login assumptions. The missing layer is a small explicit matrix that reconciles project truth, upstream truth, exact active version or identifier, and live verification before implementation lands.

## Current State

Verified facts only:

- kernel canon already requires `external_contract_slice` classification and fresh external research;
- kernel canon already requires evidence to be recorded in the active PRD or decision note;
- kernel canon does not yet require one canonical structure that records the exact external surfaces in scope with their source-of-truth fields and pinned identifiers.

## Target State

For every `external_contract_slice`, the active PRD or decision note must record an `external_source_of_truth_matrix`.

The matrix must explicitly capture, per external surface in scope:

- the surface name;
- the project-local source-of-truth file, pin, or config;
- the current upstream/vendor source;
- the exact active version, commit, build, URL, identifier, or contract revision;
- the local verification method used to confirm current reality;
- any known divergence between project-local truth, vendor docs, and live behavior.

## Write Scope

- `ENGINEERING_KERNEL.yaml`
- `README.md`
- `references/RESEARCH_POLICY.md`
- `references/BOOTSTRAP.md`
- `templates/project/README.md`
- `templates/project/AGENTS.md`
- `templates/project/CONTRIBUTING.md`
- `templates/project/docs/PRD_TEMPLATE.md`
- `tests/test_repo_kernel_canon.py`

## Rollout

1. Add `external_source_of_truth_matrix` to the machine-readable kernel under research policy.
2. Update narrative kernel docs to explain when the matrix is mandatory and what it must contain.
3. Update project templates so bootstrapped repos inherit the rule.
4. Update the PRD template so the matrix has an explicit home instead of staying only in prose.
5. Add regression coverage for the new canon.

## Verification Matrix

- code-path tests:
  - `.venv/bin/python -m unittest tests.test_repo_kernel_canon`
- build/runtime checks:
  - `python3 -m py_compile scripts/*.py`
- source-of-truth / sync checks:
  - `git diff --check`
  - docs/templates mention `external_source_of_truth_matrix`
- live checks:
  - none; this is a kernel-process slice
- rollback validation:
  - removing the new matrix requirement would leave the existing research-boundary rule intact but would re-open stale-version/source-of-truth drift

## Kernel Impact

- `none`

Why:

This slice updates the universal kernel itself rather than promoting a project-local learning to another higher layer.
