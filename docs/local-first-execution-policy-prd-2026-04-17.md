# PRD: Local-First Execution Surface Policy

Date: `2026-04-17`

Status: `active`

## 1. Problem

The kernel currently defines workflow, GitHub decomposition, verification, and
bug-intake canon, but it does not explicitly define the preferred execution
surface for ordinary engineering work.

That leaves a gap:

- agents may default to GitHub-hosted Actions even when the same work can be
  executed locally
- teams may spend paid hosted-runner minutes for development, research, and
  verification that belong on an operator machine or self-hosted runner
- new repositories do not inherit a clear rule for prerequisite detection and
  local bootstrap before work begins

## 2. Reconciled Current State

### 2.1 Kernel today

Current kernel already covers:

- PRD-first execution
- GitHub `Epic / Task / Bug`
- automatic bug-intake canon
- bootstrap templates
- labels and GitHub delivery flow

It does **not** yet say explicitly:

- local machine is the default execution surface for ordinary development
- self-hosted/local execution should be preferred before paid hosted Actions
- agents must check/bootstrap prerequisites locally before assuming CI is the
  place to run work

### 2.2 Official platform contract

Official GitHub docs confirm:

- GitHub-hosted runners in private repositories consume included/billed Actions
  minutes
- self-hosted runners are free from GitHub Actions minute billing
- self-hosted runners are intended for custom environments and repo-controlled
  execution

Sources:

- `docs.github.com/.../managing-billing-for-github-actions`
- `docs.github.com/.../about-self-hosted-runners`

### 2.3 Policy implication

The kernel should not teach agents to default to GitHub-hosted Actions for
ordinary engineering work when:

- the same work can be done locally
- the operator machine can install prerequisites deterministically
- a self-hosted runner or local machine is the canonical dev/test surface

At the same time, the kernel should not ban GitHub Actions.

GitHub Actions remain the right surface for:

- repository-native automation
- scheduled workflows
- deploy pipelines
- hosted verification that must execute inside the repository platform
- event-driven automation that should run without an operator terminal

## 3. Target State

Add a kernel-wide `local-first execution surface` policy.

### 3.1 Default rule

For ordinary development, debugging, research, and verification:

- prefer the local operator machine first
- if the repository has self-hosted runners, prefer them over paid hosted
  runners for recurring execution

### 3.2 Required bootstrap rule

Before serious work starts, the agent should:

1. detect the local execution prerequisites
2. install/bootstrap missing prerequisites deterministically if the repository
   already defines that path
3. only escalate to GitHub Actions when local execution is not the right
   surface

### 3.3 Actions rule

GitHub Actions should be treated as:

- repository automation
- schedule/event runtime
- deployment or hosted verification surface

Not as the default place to run ordinary engineering work that could be executed
locally.

## 4. Write Scope

- `ENGINEERING_KERNEL.yaml`
- `SKILL.md`
- `README.md`
- `references/BOOTSTRAP.md`
- `references/GITHUB_DELIVERY.md`
- `templates/project/README.md`
- `templates/project/AGENTS.md`
- `templates/project/CONTRIBUTING.md`
- `tests/test_repo_kernel_canon.py`
- `tests/test_bootstrap_project_kernel.py`

## 5. Rollout

### Phase 1: Add the policy to the kernel core

Entry condition:

- PRD is active

Changes:

- add machine-readable execution-surface policy
- add human-readable explanation in kernel docs

Validation:

- kernel docs/tests remain coherent

Success:

- the kernel expresses local-first execution clearly and durably

Rollback trigger:

- policy text becomes contradictory with the existing GitHub delivery layer

### Phase 2: Materialize the policy in project bootstrap

Entry condition:

- core policy exists in kernel docs

Changes:

- update project templates so newly bootstrapped repos inherit local-first
  execution canon

Validation:

- bootstrap output contains local-first execution guidance

Success:

- a new repo no longer depends on chat memory to inherit the policy

Rollback trigger:

- bootstrap output omits or weakens the rule

## 6. Verification Matrix

Code-path tests:

- `tests/test_repo_kernel_canon.py`
- `tests/test_bootstrap_project_kernel.py`

Build/runtime checks:

- `.venv/bin/python -m unittest discover -s tests`

Sync checks:

- bootstrap apply on a clean target includes local-first execution text in
  generated canon files

Live acceptance:

- kernel repo pushed to GitHub
- skill consumers can read the updated kernel and bootstrap a repo without chat
  re-explanation

## 7. Acceptance

This slice is closed only when:

- kernel machine-readable core contains explicit local-first execution policy
- human-readable docs align with that policy
- project templates inherit the policy
- tests and bootstrap verification are green
