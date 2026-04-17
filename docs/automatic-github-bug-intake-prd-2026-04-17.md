# PRD: Automatic GitHub Bug Intake Canon

Date: `2026-04-17`

Status: `active`

## 1. Problem

The kernel already defines PRD-first execution, GitHub `Epic / Task / Bug`,
repo-managed labels, and draft-PR discipline.

What it does not yet define explicitly is how serious runtime and pipeline
failures should become GitHub `Bug` issues automatically without flooding the
repository with noise.

Without a canon here, future agents will choose inconsistent patterns:

- one issue per raw log line
- one issue per Telegram alert
- no deduplication
- no stable fingerprinting
- no reopen/update/resolve policy

That is not a serious engineering workflow.

## 2. External Contract

Verified against official GitHub docs:

- issues are the canonical unit for tracked work
- issue forms structure consistent bug intake
- sub-issues allow a parent issue to own smaller executable slices
- labels are first-class tracking metadata
- automatic closure from PR keywords should target the executable leaf, not the
  parent work envelope

Sources:

- `https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues`
- `https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues`
- `https://docs.github.com/en/rest/issues/sub-issues`
- `https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository`
- `https://docs.github.com/articles/closing-issues-using-keywords`

## 3. Reconciled Current State

The kernel already encodes:

- `Epic / Task / Bug`
- issue-first delivery
- PR closes leaf issue only
- repo-managed labels and issue forms

Missing:

- bug-intake source-of-truth
- deduplication/fingerprint rules
- threshold policy
- update vs create policy
- resolution/reopen policy
- explicit statement that raw logs and chat alerts are not canonical bug intake

## 4. Target State

The kernel must define one universal automatic bug-intake model.

Canonical intake path:

1. a verifier, watchdog, or readiness gate normalizes an incident
2. the incident is converted into a stable fingerprint
3. the system looks for an existing open `Bug` issue with that fingerprint
4. if found, it updates the existing issue instead of creating a duplicate
5. if not found, it creates one `Bug` issue
6. the issue remains the durable tracking surface for future fix work

Hard rules:

- do not open issues directly from raw logs
- do not open issues directly from Telegram alerts
- one bug class = one stable fingerprint
- transient failures must cross a threshold before becoming a bug issue
- create/update evidence must include symptom, impact, fingerprint, and last
  known evidence
- PRs close the executable fix issue, not the intake epic unless the slice is
  truly single-issue

## 5. Write Scope

- `README.md`
- `SKILL.md`
- `ENGINEERING_KERNEL.yaml`
- `references/GITHUB_DELIVERY.md`
- `templates/project/README.md`
- `templates/project/AGENTS.md`
- `templates/project/CONTRIBUTING.md`
- `tests/test_repo_kernel_canon.py`
- `tests/test_bootstrap_project_kernel.py`
- active PRD index in `docs/`

## 6. Rollout

### Phase 1: Document the canonical bug-intake model

Entry condition:

- kernel repo already defines issue hierarchy and delivery flow

Validation:

- this PRD records current state, target state, write scope, verification, and
  rollback

Success:

- bug-intake policy is explicit before file changes start

Rollback trigger:

- if fingerprint/update policy is still ambiguous, stop before editing templates

### Phase 2: Materialize the canon in the kernel

Entry condition:

- PRD is active

Changes:

- add bug-intake rules to machine-readable kernel
- add bug-intake guidance to README, skill, and delivery reference
- add the same rules to project bootstrap templates
- extend regression tests to require the new canon

Validation:

- unit tests for kernel and bootstrap pass
- bootstrap output contains the bug-intake rules

Success:

- future agents can inherit the automatic bug-intake canon without it being
  re-explained in chat

Rollback trigger:

- if template outputs drift from the machine-readable kernel, stop and reconcile

## 7. Verification Matrix

Code-path tests:

- `tests/test_repo_kernel_canon.py`
- `tests/test_bootstrap_project_kernel.py`

Build/runtime checks:

- `.venv/bin/python -m unittest discover -s tests`

Drift checks:

- `git diff --check`

Sync checks:

- bootstrap a clean target and verify the bug-intake canon appears there too

Live acceptance checks:

- kernel repo on GitHub contains the updated canon and bootstrap files

Rollback:

- revert kernel docs/templates/tests together as one slice

## 8. Acceptance

This slice is closed only when:

- the kernel clearly states bug intake comes from canonical verifier/watchdog
  surfaces, not raw logs
- fingerprinted dedupe/update policy is explicit
- project bootstrap output inherits the same rules
- kernel tests remain green
