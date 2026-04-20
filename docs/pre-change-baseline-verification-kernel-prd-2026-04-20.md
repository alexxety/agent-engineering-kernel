## Pre-Change Baseline Verification Kernel Rule

Date: 2026-04-20
Issue: #30
Status: `implemented`
Classification: `project_local_only`
Kernel Impact: `n/a`

## Problem

The kernel already required verification before merge, but it did not yet state one earlier reusable rule strongly enough: when a deterministic contract already exists, capture the smallest relevant baseline verification before edits begin.

Without that rule, agents can still:

- refactor against an unverified mental model;
- “fix” bugs without reproducing the real failure mode first;
- change existing behavior without proving what the old contract was.

## Decision

Add a universal verification rule to the kernel:

- if a deterministic contract already exists, capture the smallest relevant baseline verification before edits;
- for bugfixes, prefer a reproducer first;
- for refactors, prefer before/after equivalence checks;
- for features that change existing behavior, run the focused current-contract baseline before edits when practical, then rerun verification after the change;
- for docs-only, canon-only, or greenfield slices with no existing contract, define verification before edits but do not invent a fake baseline.

This is not universal “always TDD” dogma. It is a narrower goal-driven verification rule that fits serious engineering work across repositories.

## Scope

Update the reusable kernel only:

- [ENGINEERING_KERNEL.yaml](ENGINEERING_KERNEL.yaml)
- [README.md](README.md)
- [references/GITHUB_DELIVERY.md](references/GITHUB_DELIVERY.md)
- [templates/project/AGENTS.md](templates/project/AGENTS.md)
- [templates/project/CONTRIBUTING.md](templates/project/CONTRIBUTING.md)
- kernel tests

## Acceptance

- machine-readable kernel includes pre-change baseline verification when relevant;
- kernel README and delivery reference explain the difference between baseline-before-edits and post-change verification;
- project templates inherit the rule;
- kernel tests protect the new rule.

## Verification

- `.venv/bin/python -m unittest discover -s tests`
- `git diff --check`
