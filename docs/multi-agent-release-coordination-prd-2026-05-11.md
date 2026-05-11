# Multi-Agent Release Coordination PRD

Date: 2026-05-11

## Problem

When several agents work on one production-bound repository, a later agent can
recover or deploy from a stale checkout, dirty runtime directory, or plain
`main` while another release candidate is already staged or partially deployed.
That creates runtime regressions, schema drift, and confusion about which branch
is authoritative.

## Scope

Add a universal kernel rule for coordinating:

- multiple agent branches;
- integration release branches;
- clean worktrees;
- staging and production promotion;
- runtime recovery;
- handoff packets between agents;
- merge and branch cleanup.

## Non-Goals

- Define project-specific deploy commands.
- Grant workers live production authority.
- Replace project-local `AGENTS.md` or active PRDs.
- Force every project to use the same branch names.

## Decision

The kernel now treats `main` as source of truth only after the verified release
candidate is merged. Before merge, the active release candidate is the source
of truth: branch, exact SHA, PR, deploy command, runtime state, and verification
evidence.

Multi-agent production-bound work should use an integration branch when several
agent branches must ship together. The integration branch is a release
candidate, gets a draft PR, passes staging, and only then moves to production
with backup/restore-point evidence when schema or data can change.

Workers do not deploy or mutate live runtime by default. A second agent touching
live runtime must receive or reconstruct a handoff packet before acting.

## Artifacts

- `references/MULTI_AGENT_RELEASE_COORDINATION.md`
- `ENGINEERING_KERNEL.yaml`
- `SKILL.md`
- `README.md`
- `references/BOOTSTRAP.md`
- `templates/project/AGENTS.md`
- `tests/test_repo_kernel_canon.py`

## Verification Plan

- YAML parses and exposes `multi_agent_release_coordination_policy`.
- Repo canon test confirms the new reference exists and key policy values are
  machine-readable.
- Full pytest suite passes.

## Kernel Impact

promote_to_kernel
