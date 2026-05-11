# Multi-Agent Release Coordination

Use this reference when several agents, branches, or worktrees touch one
production-bound project at the same time.

The goal is to prevent a new agent from "fixing" production by deploying a
stale checkout, dirty runtime directory, or incomplete branch while another
agent's already-verified work is still in flight.

## Core Rule

`main` is the source of truth only after the verified integration PR is merged.
Before that, the source of truth for a live recovery or feature cutover is the
active release candidate: exact branch, commit SHA, PR, deploy command, runtime
state, and verification evidence.

Do not deploy from memory, from a detached/dirty directory, or from "whatever is
currently on main" without checking whether a newer release candidate has
already been staged or deployed.

## Roles

The orchestrator owns release coordination:

- branch topology and active PRs;
- which worktree is allowed to deploy;
- which commit is deployed to staging and production;
- runtime/schema/env verification;
- PR comments or closeout evidence;
- merge and branch cleanup.

Worker agents own only their assigned patch. They do not deploy, mutate live
databases, send live messages, or make provider-console changes unless an
active PRD creates a narrow audited role for that exact surface.

If a worker or second agent is asked to recover a live failure, it must first
return a state report when it does not know the release candidate:

```text
NEEDS_RELEASE_CONTEXT:
- repo path / worktree path
- current branch and commit
- open PRs or integration branch
- deployed commit if known
- runtime health/log symptom
- deploy script expected by project canon
```

## Branch Topology

Use one of these shapes.

### Single Slice

```text
main
  -> feature-or-fix-branch
    -> draft PR
    -> staging
    -> production when approved
    -> merge to main
```

### Multiple Agent Slices

```text
main
  -> agent-a-branch
  -> agent-b-branch
  -> integration/<release-name>
    -> draft PR
    -> staging
    -> production when approved
    -> merge to main
```

The integration branch is a release candidate, not another scratch branch. It
must be clean, reviewable, and deployed only by the orchestrator or by a
project-authorized release agent following the documented command.

## Worktree Rules

- Create implementation branches in isolated worktrees.
- Never switch a dirty shared checkout to "just deploy quickly".
- Never deploy from a detached checkout unless the project canon explicitly
  marks that checkout as the release candidate and records its SHA.
- If a branch is already checked out in another worktree, do not force switch
  it locally; use that worktree or create a new branch/worktree.
- Before accepting a worker result or deploying:

```bash
git status --short --branch
git diff --check
git log --oneline --decorate --max-count=5
```

Git ref/index/worktree-mutating commands remain serialized per repository. Do
not parallelize fetch, pull, switch, checkout, merge, rebase, branch deletion,
or push for the same repo.

## Runtime Recovery Protocol

When production is broken, do not start by rebuilding the app from the closest
directory.

Use this order:

1. Identify the live symptom and current health.
2. Identify the expected release candidate branch/PR/SHA.
3. Inspect the runtime deploy directory for dirty or detached state, but do not
   mutate it.
4. Check the project deploy/runbook command, including compose overlays,
   migration mode, env forwarding, and secret boundaries.
5. Package any recovery change into a branch or integration branch.
6. Verify locally or in CI as appropriate.
7. Deploy staging from the exact release candidate SHA.
8. Run staging smoke checks.
9. Take a production backup or restore point before schema/data changes.
10. Deploy production from the same release candidate SHA with the documented
    production-safe command.
11. Run read-safe production smoke checks and log scans.
12. Record evidence in the PR or closeout.
13. Merge the verified PR to `main`.

If production was hot-fixed from a runtime directory under emergency pressure,
the next action is to package that exact runtime delta into a normal branch/PR
and reconcile `main`. Do not leave production ahead of GitHub.

## Deploy Command Contract

Production-bound projects must document the exact deploy command. Agents must
use the project command instead of inventing a raw shell sequence.

The command contract should name:

- working directory;
- branch or SHA;
- build flags;
- migration mode;
- compose or service overlays;
- env file ownership;
- backup path;
- health endpoints;
- rollback path.

For database drift, prefer the narrowest safe schema path. If a broad migration
or `db push` preview includes destructive or unrelated changes, create a
focused additive patch and record why the broad path is blocked.

## Handoff Packet Between Agents

When opening or handing off to another agent, include:

```text
repo:
  path:
  source_of_truth_branch:
  active_worktree:
  current_release_candidate:
  exact_commit_sha:
github:
  issue_or_pr:
  draft_or_ready:
runtime:
  staging_url:
  production_url:
  deploy_command:
  backup_required:
allowed_actions:
  - ...
forbidden_actions:
  - no deploy from dirty/detached checkout
  - no raw compose/service restart unless runbook says so
  - no broad schema push without preview
  - no live sends/customer cleanup/provider writes
verification:
  local:
  staging:
  production_read_safe:
open_questions:
  - ...
```

If this packet is missing and the task touches live runtime, the second agent
should ask for or reconstruct it before acting.

## Merge And Closeout

A release candidate can be merged only after:

- CI or local verification required by the project is green;
- staging was verified for production-bound changes;
- production was verified when the PR was already rolled out before merge;
- schema/data backup evidence exists when applicable;
- runtime smoke checks and log scans were recorded;
- the PR body/comment or closeout says what commit was deployed;
- the head branch can be deleted or explicitly kept with a reason.

After merge:

- fetch `origin/main`;
- confirm `origin/main` contains the merge commit;
- delete the remote release branch when appropriate;
- keep or remove local worktrees intentionally;
- treat `main` as source of truth again.

## Red Flags

Stop and recover before changing runtime when any of these are true:

- the checkout is dirty and the dirty files are not fully understood;
- the checkout is detached and no release candidate SHA was recorded;
- another agent has an open branch/PR that was already staged or deployed;
- the deploy command differs from the project runbook;
- compose/service overlays are ambiguous;
- schema preview includes destructive or unrelated changes;
- provider/webhook/runtime env is inferred instead of inspected;
- a worker wants to deploy or touch live data without explicit authority.
