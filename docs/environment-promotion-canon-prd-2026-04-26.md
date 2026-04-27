# Environment Promotion Canon PRD

Date: `2026-04-26`

Status: `active`

Issue: `#42`

## Problem

The kernel already distinguishes local execution, self-hosted runners, GitHub Actions, and sandbox identities, but it does not yet name the full environment promotion path that production-bound applications need.

Without that rule, downstream repos can drift into copied dev/prod projects, production secrets in local `.env` files, mutating tests against production, or schema changes that are not promoted through an auditable deploy path.

## Current State

Verified facts:

- `references/EXECUTION_SURFACES.md` defines local/self-hosted first execution and GitHub as coordinator.
- `ENGINEERING_KERNEL.yaml` defines execution surface rules and sandbox identity rules for live external writes.
- Consumer project Breez promoted a reusable `local -> verify -> staging -> production` model in Breez issue `#115` and PR `#116`.

## Target State

The universal kernel should require projects to document environment boundaries before production-bound work:

- one codebase can deploy to multiple environments;
- `local` is for development;
- disposable `verify` is for automated mutating tests;
- `staging` is for production-like acceptance with sandbox identities;
- `production` is for real customer data and real provider identities;
- production secrets must not be used locally;
- mutating automated tests must not run against production;
- production schema/data/deploy commands, backup, smoke checks, and rollback must be explicit project-local canon.

## Write Scope

- `ENGINEERING_KERNEL.yaml`
- `README.md`
- `SKILL.md`
- `references/ENVIRONMENT_PROMOTION.md`
- `references/BOOTSTRAP.md`
- `references/EXECUTION_SURFACES.md`
- `references/GITHUB_DELIVERY.md`
- `templates/project/README.md`
- `templates/project/AGENTS.md`
- `templates/project/CONTRIBUTING.md`
- `templates/project/docs/PRD_TEMPLATE.md`
- `tests/test_repo_kernel_canon.py`
- `tests/test_bootstrap_project_kernel.py`

## Rollout

1. Add a new reference document.
2. Add machine-readable kernel rules.
3. Add the rule to bootstrap templates.
4. Add tests so the rule cannot disappear from docs or generated projects.

## Verification Matrix

- code-path tests: `python3 -m pytest`
- build/runtime checks: n/a for docs/canon slice
- source-of-truth checks: machine-readable kernel parses and template tests pass
- live checks: n/a, no external writes
- rollback validation: revert this PR and remove the environment promotion reference from templates

## Kernel Impact

`promote_to_kernel`

Why:

This slice promotes a reusable production-safety workflow from a consumer repository into the universal kernel without adding Breez-specific provider choices.
