# Owned-Compute Execution Surface PRD

Date: 2026-04-24
Issue: `#36`
Slice classification: `external_contract_slice`

## Problem

The kernel already said local/self-hosted execution should come before paid
GitHub-hosted Actions. A downstream repository produced a stronger live lesson:
private-repo GitHub-hosted runners and Actions cache/storage are not just a
minor convenience; they can become a billing blocker and can consume money even
when the engineering work itself is routine.

The universal rule should be explicit enough that future project bootstraps do
not accidentally treat GitHub-hosted compute as the default executor.

## External Source Baseline

GitHub docs checked on 2026-04-24:

- GitHub Actions usage is free for self-hosted runners.
- Private repositories consume included/billed runner minutes and
  artifact/cache storage when using GitHub-hosted runners.
- `jobs.<job_id>.runs-on` selects runner labels for workflow jobs.

Sources:

- https://docs.github.com/en/billing/concepts/product-billing/github-actions
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job
- https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners

## Decision

Promote this wording into the universal kernel:

- GitHub coordinates repository workflow: issues, PRs, check status, schedules,
  and deploy triggers.
- Owned compute executes routine work by default: local operator machine first,
  then self-hosted runners for recurring repository checks.
- Paid GitHub-hosted runners are explicit exceptions, not defaults.
- GitHub dependency cache uploads and long-lived artifacts are also paid-surface
  decisions in private repositories, so they require explicit acceptance.
- Project canon must document self-hosted runner labels before enabling
  recurring GitHub checks.

## Acceptance

- References describe GitHub as coordinator/orchestrator and owned compute as
  default executor.
- Project templates carry the stronger rule.
- The machine-readable kernel carries the stronger rule.
- Kernel's own test workflow stops using `ubuntu-latest` and GitHub dependency
  cache by default.
- Tests guard the wording.

## Verification

Completed:

- `python3.11` venv: `python -m unittest discover -s tests -v` -> 33 passed.
- `python3.12` venv: `python -m unittest discover -s tests -v` -> 33 passed.
- `python3.12` venv: `python -m unittest tests.test_repo_kernel_canon -v`.
- `git diff --check`.

Note: do not use bare `python3` as the kernel verification contract on this
operator machine; it currently points at `Python 3.14`, while the kernel workflow
intentionally verifies with runner-owned `python3.11` and `python3.12`.

## Kernel Impact

`promote_to_kernel`
