# PRD: Session Issue Sync Canon

Date: `2026-05-11`

Status: `active`

## Problem

The kernel already requires PRD-first work, GitHub `Epic / Task / Bug`
decomposition, sub-issues, PR delivery discipline, and `kernel_sync_review`.
It does not yet require agents to make an explicit end-of-slice decision about
whether the relevant GitHub issue state was updated.

That leaves a practical gap: code, docs, or verification may be complete while
the durable operational memory in GitHub Issues still has stale status, missing
next steps, or no explanation for why no issue update was needed.

## Current State

Verified facts:

- `ENGINEERING_KERNEL.yaml` defines `github_issue_tree`,
  `github_delivery_flow`, `automatic_bug_intake`, and `kernel_sync_policy`.
- `references/GITHUB_DELIVERY.md` defines the branch, PR, issue, and sub-issue
  delivery flow.
- `templates/project/docs/PRD_TEMPLATE.md` records verification and
  `kernel_impact`, but has no `Issue Sync` closeout field.
- GitHub Issues support task and bug tracking, sub-issues, filtering/searching,
  labels, issue types, and REST endpoints for issue and sub-issue operations.
- The external `ris-manager` skill demonstrates useful patterns for
  session-to-issue sync, track status reads, false-positive filtering, stale
  epic detection, and search-before-create.

## GitHub Issues

- Task: #62

## External Source-Of-Truth Matrix

Canonical field name: `external_source_of_truth_matrix`

- `surface_name`: GitHub Issues and sub-issues
- `project_local_source_of_truth`: `references/GITHUB_DELIVERY.md`,
  `ENGINEERING_KERNEL.yaml`, `scripts/link_github_sub_issue.py`
- `upstream_or_vendor_source`: GitHub Docs for Issues, issue filtering/search,
  and REST issue/sub-issue endpoints
- `exact_version_commit_build_url_or_identifier`: GitHub Docs checked on
  `2026-05-11`
- `local_verification_method`: repository tests plus text checks proving the
  new canon is present in references, templates, and machine-readable kernel
  state
- `divergence_notes`: kernel keeps Projects optional and does not require
  weekly labels or CRM-specific tracking

## Target State

Every serious engineering slice ends with an explicit `Issue Sync` decision:

- `updated`: the relevant GitHub issue body, labels, links, or status were
  updated to reflect the slice outcome.
- `skipped`: an issue update would normally apply, but was intentionally not
  performed; the closeout records the reason.
- `not_applicable`: the work has no durable GitHub issue state to update.

The rule is a closeout contract, not an automatic write permission. Agents must
still respect project-local authorization, public-repo privacy risks, connector
permissions, shell-safe `gh` usage, and existing issue-first delivery rules.

The canon also records these operational rules:

- search before creating a new issue;
- prefer updating the issue body for durable status and next steps;
- use comments only for short chronological notes or when explicitly requested;
- surface stale or unhealthy issue state instead of silently fixing it;
- keep weekly labels, CRM pointers, and business cadence policies optional and
  project-local.

## Write Scope

Expected repository changes:

- create `references/SESSION_ISSUE_SYNC.md`;
- update `ENGINEERING_KERNEL.yaml`;
- update `SKILL.md`;
- update `README.md`;
- update `CHANGELOG.md`;
- update `references/BOOTSTRAP.md`;
- update `templates/project/AGENTS.md`;
- update `templates/project/CONTRIBUTING.md`;
- update `templates/project/README.md`;
- update `templates/project/docs/PRD_TEMPLATE.md`;
- update `references/GITHUB_DELIVERY.md`;
- add or update tests that enforce the new canon text.

Out of scope:

- creating a new `ris-manager` clone;
- adding weekly planning or retro as a universal requirement;
- making `W-label` mandatory;
- adding CRM-specific issue fields;
- automatically writing to GitHub without project-local authorization.

## Process Skills

- available skill pack: `Superpowers`
- relevant skills:
  - `using-superpowers`
  - `brainstorming`
  - `writing-plans`
  - `test-driven-development`
  - `verification-before-completion`
- exceptions or conflicts with project canon: none

## MCP / App Connector Surface

- MCP or App connector in scope: GitHub for issue creation/update only
- GitHub App repository access checked: `n/a` for local doc changes; required
  before connector-backed issue writes
- required App connector permissions: `issues:write` only if using the GitHub
  connector to create or close issues
- local `gh` fallback required: yes, for GitHub issue creation/closure if the
  connector is unavailable
- identity note: `MCP/App connector and local gh are different identities`
- token handling: `no tokens recorded`

## Kernel Upstream Check

This repository is the upstream kernel.

- protocol: `kernel_upstream_check`
- status: `not_applicable`
- action: `none`
- `kernel_adoption_task`: `n/a`
- adoption decision when drift exists: `not_applicable`

## Rollout

1. Open a GitHub `Task` for this executable slice.
2. Create an implementation plan in `docs/superpowers/plans/`.
3. Add the reference document and machine-readable kernel policy.
4. Propagate the closeout field and policy into project templates.
5. Add tests that fail if the policy or template field disappears.
6. Run repository verification.
7. Commit and push the slice branch.
8. Close the leaf issue only after verification and closeout.

Rollback is documentation-only: revert the slice commit and remove the new
reference, template fields, and tests.

## Verification Matrix

- code-path tests: repository canon tests must pass
- build/runtime checks: not applicable
- source-of-truth / sync checks: `ENGINEERING_KERNEL.yaml`, references, and
  templates must agree on the same `Issue Sync` values
- live checks: GitHub issue closeout should reference verification evidence
- rollback validation: `git diff --check` must pass

## Verification Evidence

- `.venv/bin/python -m unittest tests.test_repo_kernel_canon tests.test_bootstrap_project_kernel`: 32 tests, OK
- `.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: 44 tests, OK
- `git diff --check`: exit 0
- `.venv/bin/python -m pytest ...`: not available in the repo virtualenv; `requirements-dev.txt` does not include `pytest`, so verification used the repository's `unittest` suite

## Issue Sync

Choose one:

- `updated`

Why:

This slice owns Task #62. The PRD now records the closeout state and verification evidence; the GitHub issue/PR state will be kept current through the branch and draft PR flow.

## Kernel Impact

Choose one:

- `promote_to_kernel`

Why:

This slice adds a reusable engineering workflow rule: serious agent-led work
must close the loop between implementation state and GitHub issue state. The
rule is process-level, model-agnostic, and likely to recur in every repository
that uses the kernel.
