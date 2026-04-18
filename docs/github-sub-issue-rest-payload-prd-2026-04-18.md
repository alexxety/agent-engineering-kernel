# GitHub Sub-Issue Payload Canon PRD

## Current state

- The kernel canon already requires `Epic / Task / Bug` issue trees and GitHub sub-issues for multi-slice work.
- A live audit against `alexxety/dudarik.com` showed that `POST /repos/{owner}/{repo}/issues/{issue_number}/sub_issues` returned `404` when called with:
  - parent issue number in the path
  - child issue **number** in `sub_issue_id`
- The same account, repository, and feature worked through GraphQL `addSubIssue`.
- A follow-up REST call succeeded once `sub_issue_id` used the child issue **database id** instead of the child issue number.

## Root cause

- The failure was not:
  - missing repo scope
  - missing API version header
  - sub-issues feature gate
- The failure was payload misuse:
  - REST `sub_issue_id` expects the child issue database id
  - we provided the child issue number
- On a private repository, GitHub returned `404 Not Found`, which masked the mistake and looked like an auth or feature problem.

## Target state

- Kernel docs must explicitly record the payload semantics.
- Kernel delivery canon must steer agents away from raw REST add-sub-issue calls with issue numbers.
- Kernel must provide a safe helper that starts from normal issue numbers and resolves the correct node identifiers before linking.
- Downstream project canon must inherit the same rule.

## Write scope

- `README.md`
- `SKILL.md`
- `ENGINEERING_KERNEL.yaml`
- `references/GITHUB_DELIVERY.md`
- `templates/project/README.md`
- `templates/project/AGENTS.md`
- `templates/project/CONTRIBUTING.md`
- `scripts/link_github_sub_issue.py`
- `templates/project/scripts/link_github_sub_issue.py`
- `tests/test_repo_kernel_canon.py`
- `tests/test_link_github_sub_issue.py`

## Chosen path

- Prefer a kernel helper backed by GraphQL `addSubIssue`, because agents naturally start from issue numbers and `gh issue view --json id` already exposes GraphQL node ids.
- Keep the REST payload rule in docs because the semantics still matter for audits and any direct REST usage.

## Verification matrix

- Unit tests:
  - helper resolves parent and child node ids before linking
  - helper calls GraphQL with node ids, not issue numbers
- Syntax checks:
  - `python3 -m py_compile scripts/link_github_sub_issue.py`
- Canon tests:
  - docs and templates mention `database id` semantics or the helper path
- Live checks:
  - reproduce failing REST call with child issue number -> `404`
  - confirm GraphQL link works
  - confirm REST succeeds with child database id

## Rollback

- Remove the helper and revert the canon text.
- Fallback remains manual issue body linkage plus UI or GraphQL linking.

## Acceptance criteria

- Kernel canon explicitly explains the REST payload trap.
- A reusable helper exists in root and templates.
- Tests cover the helper and the documentation rule.

## Kernel Impact

- `promote_to_kernel`

Why:

This is a reusable GitHub delivery rule, not a project-local operational detail.
