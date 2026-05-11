# PRD: <title>

Date: `<YYYY-MM-DD>`

Status: `active`

## Problem

Describe the current gap.

## Current State

Verified facts only.

## External Source-Of-Truth Matrix

Required for `external_contract_slice`. One entry per external surface in scope.

Canonical field name: `external_source_of_truth_matrix`

- `surface_name`:
- `project_local_source_of_truth`:
- `upstream_or_vendor_source`:
- `exact_version_commit_build_url_or_identifier`:
- `local_verification_method`:
- `divergence_notes`:

## Target State

What should be true after the change.

## Write Scope

Files, workflows, services, or systems expected to change.

## Process Skills

Record relevant Superpowers or equivalent process skills for this slice.

- available skill pack: `Superpowers | other | unavailable`
- relevant skills:
  - `using-superpowers`
  - `brainstorming`
  - `writing-plans`
  - `test-driven-development`
  - `systematic-debugging`
  - `verification-before-completion`
- exceptions or conflicts with project canon: `none | describe`

## MCP / App Connector Surface

Record external-service tooling and identity boundaries when the slice uses GitHub, vendor APIs, or other live services.

- MCP or App connector in scope: `none | name`
- GitHub App repository access checked: `n/a | yes | no`
- required App connector permissions: `n/a | issues:write | pull_requests:write | contents:write | workflows:write | describe`
- local `gh` fallback required: `no | yes, reason`
- identity note: `MCP/App connector and local gh are different identities`
- token handling: `no tokens recorded`

## Kernel Upstream Check

Record near slice start.

- protocol: `kernel_upstream_check`
- status: `current | update_available | not_configured | unknown`
- action: `none | task_opened_or_updated | explicitly_deferred`
- `kernel_adoption_task`: `<issue id or n/a>`
- adoption decision when drift exists: `adopt_now | defer | not_applicable`

## Rollout

Phased plan with validation and rollback.

## Cutover Entitlement Role-Matrix

Required when the slice makes a new shell, navigation model, admin information architecture, or major UI the default.

- default cutover in scope: `yes | no`
- entitlement source of truth:
- replacement decision if not using the existing entitlement source: `n/a | describe`
- role-matrix evidence:
  - unauthenticated:
  - personal user:
  - workspace owner/admin:
  - workspace member:
  - enterprise/admin:
  - platform admin:
- surface evidence:
  - desktop navigation:
  - mobile navigation:
  - command/search palette:
  - topbar/page chrome:
  - direct restricted routes:

For production-bound work, record:

- local verification path;
- disposable verify environment;
- staging deploy and smoke checks;
- production approval gate;
- production backup or restore point;
- production deploy or migration command;
- read-safe production smoke checks;
- rollback path.

Production-bound work must also confirm that production secrets and production database URLs are not used in local config or local tests, and that mutating automated tests do not run against production.

## Verification Matrix

- code-path tests
- build/runtime checks
- source-of-truth / sync checks
- live checks
- rollback validation

## Work Item Routing

Record this before creating durable work when the target is not obvious.

- target repo or project-local surface:
- duplicate search in target surface:
- ambiguity: `none | ambiguous | not_applicable`

Never default to the current checkout as the target repo.

## Project Health Audit

Record applicable findings when this slice bootstraps or audits project operations.

- SSOT / metric definitions / freshness policy:
- decision log / escalation rules / incident log:
- prohibited actions / eval or golden cases / runbooks:
- follow-up routing:

## Optional Weekly Operating Loop

Record only if this project uses a weekly cadence.

- adopted: `yes | no | not_applicable`
- planned outcomes and evidence checks:
- retro / plan-vs-actual evidence:
- stale carryover decision: `close | drop | promote | spillover | not_applicable`

## Issue Sync

Record this during closeout.

Choose one:

- `updated`
- `skipped`
- `not_applicable`

Why:

Explain whether the relevant GitHub issue state was updated, intentionally skipped, or not applicable.
When issue sync applies, keep durable status, next steps, verification, and links in the issue body.

## Kernel Impact

Record this during `kernel_sync_review`.

Choose one:

- `none`
- `project_local_only`
- `promote_to_kernel`

Why:

Explain whether this slice produced a reusable engineering rule or only a project-local decision.
