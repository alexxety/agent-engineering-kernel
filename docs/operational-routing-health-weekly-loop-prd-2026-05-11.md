# PRD: Operational Routing, Health Audit, And Weekly Loop Canon

Date: `2026-05-11`

Status: `active`

## Problem

The kernel already covers PRD-first execution, GitHub issue delivery, session
issue sync, kernel sync, MCP boundaries, environment promotion, and multi-agent
release coordination.

It still has three operating gaps:

- agents can create a correct issue in the wrong repository or surface;
- bootstrapped projects have no compact health-audit checklist for missing
  operating artifacts;
- projects that use a weekly cadence have no optional plan-vs-actual loop that
  prevents stale work from rolling forward forever.

## Current State

Verified facts:

- `SESSION_ISSUE_SYNC.md` says weekly labels, CRM pointers, Projects, and weekly
  cadence remain optional project-local policies.
- `GITHUB_DELIVERY.md` covers branch, PR, merge, and shell-safe GitHub writes.
- Project templates mention GitHub Projects as optional.
- `BOOTSTRAP.md` lists minimal bootstrap outputs but does not ask for task
  routing, health audit, or weekly loop decisions.
- The scanned RIS skills contain useful source patterns:
  - `task-routing`: explicit routing before issue creation;
  - `product-data-audit`: missing artifact checklist;
  - `weekly-planning` and `weekly-retro`: outcomes, scorecards, and terminal
    carryover decisions.

## GitHub Issues

- Task: #65

## External Source-Of-Truth Matrix

Canonical field name: `external_source_of_truth_matrix`

- `surface_name`: RIS skills scan
- `project_local_source_of_truth`: this PRD, `ENGINEERING_KERNEL.yaml`,
  `references/GITHUB_DELIVERY.md`, `references/SESSION_ISSUE_SYNC.md`
- `upstream_or_vendor_source`: `https://github.com/serejaris/ris-claude-code/tree/main/skills`
- `exact_version_commit_build_url_or_identifier`: public GitHub repository
  scanned on `2026-05-11`
- `local_verification_method`: repository canon tests and bootstrap template
  tests prove the new policies are present and inherited
- `divergence_notes`: kernel extracts universal invariants only; it does not
  copy RIS skill text, Paperclip workflows, CRM fields, W-label enforcement,
  or mandatory GitHub Projects.

## Target State

Add three universal-but-small canon surfaces:

1. `work_item_routing_policy`
   - before creating or moving durable work, identify the correct repo or
     project-local surface;
   - never default to the current checkout;
   - search duplicates in the target surface before creating;
   - ask or record ambiguity when no routing rule matches.

2. `project_health_audit_policy`
   - bootstrap and audits can flag missing operating artifacts;
   - default checklist: SSOT, metric definitions, freshness policy, decision
     log, escalation rules, incident log, prohibited actions, eval/golden
     cases, runbooks for critical pipelines;
   - findings classify as control, visibility, or consistency gaps.

3. `optional_weekly_operating_loop_policy`
   - weekly cadence is optional, not bootstrap mandatory;
   - when enabled, planning records outcomes with measurable checks;
   - retro compares planned outcomes against evidence;
   - stale carryover gets a terminal decision: close, drop, promote, or
     spillover with explicit reason;
   - weekly labels and GitHub Projects remain project-local choices.

## Write Scope

Expected changes:

- create `references/WORK_ITEM_ROUTING.md`;
- create `references/PROJECT_HEALTH_AUDIT.md`;
- create `references/OPTIONAL_WEEKLY_OPERATING_LOOP.md`;
- update `ENGINEERING_KERNEL.yaml`;
- update `README.md`;
- update `SKILL.md`;
- update `CHANGELOG.md`;
- update `references/BOOTSTRAP.md`;
- update `references/GITHUB_DELIVERY.md`;
- update project templates;
- add or update tests that enforce the new canon text.

Out of scope:

- no direct copy of RIS skill bodies;
- no mandatory weekly labels, GitHub Projects, CRM fields, or weekly cadence;
- no Paperclip, Claude analytics, ris-draft, README generator, or CEO council
  workflow in universal core;
- no runtime code or external service automation.

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

- MCP or App connector in scope: GitHub for issue/PR operations only
- GitHub App repository access checked: `n/a`; using local `gh` fallback
- required App connector permissions: `n/a`
- local `gh` fallback required: yes, for issue and PR delivery
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

1. Add failing tests that pin the three new policies and template inheritance.
2. Add focused reference docs and YAML policy entries.
3. Propagate concise rules into root docs, bootstrap, delivery, and templates.
4. Run focused and full repository verification.
5. Commit, push, open PR, and update Task #65 issue body.
6. Merge only after local and GitHub checks pass.

Rollback is documentation-only: revert the slice commit and remove the three
new policies, references, template text, and tests.

## Verification Matrix

- code-path tests: `tests.test_repo_kernel_canon` and
  `tests.test_bootstrap_project_kernel`
- build/runtime checks: not applicable
- source-of-truth / sync checks: YAML, references, README/SKILL, bootstrap,
  delivery docs, and templates agree on the same optional boundaries
- live checks: GitHub issue and PR state updated through shell-safe `gh`
- rollback validation: `git diff --check`

## Verification Evidence

- `.venv/bin/python -m unittest tests.test_repo_kernel_canon tests.test_bootstrap_project_kernel`: 33 tests, OK
- `.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: 45 tests, OK
- `git diff --check`: exit 0

## Issue Sync

Record this during closeout.

Choose one:

- `updated`

Why:

Task #65 will be updated with branch, commit, PR, verification, and next step
after commit/PR publication.

## Kernel Impact

Record this during `kernel_sync_review`.

Choose one:

- `promote_to_kernel`

Why:

The extracted rules are reusable across serious agent-led projects: route work
to the right surface, audit missing operational artifacts, and optionally close
weekly planning loops without forcing one business cadence on every repo.
