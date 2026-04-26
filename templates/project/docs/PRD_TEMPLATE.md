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

## Verification Matrix

- code-path tests
- build/runtime checks
- source-of-truth / sync checks
- live checks
- rollback validation

## Kernel Impact

Record this during `kernel_sync_review`.

Choose one:

- `none`
- `project_local_only`
- `promote_to_kernel`

Why:

Explain whether this slice produced a reusable engineering rule or only a project-local decision.
