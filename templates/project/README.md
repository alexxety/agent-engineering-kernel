# Project Name

This repository follows the agent engineering kernel.

## Engineering canon

- non-trivial work is PRD-first
- non-trivial work starts from a parent GitHub issue
- each non-trivial slice is classified before edits as `repo_local_slice` or `external_contract_slice`
- repo-owned slices may proceed from project truth, deterministic verification, and local runtime checks
- slices that change or claim current external-system behavior require fresh external research before code or docs land
- every `external_contract_slice` records an `external_source_of_truth_matrix` so project pins, vendor docs, exact versions, and live verification are reconciled explicitly
- GitHub hierarchy:
  - `Epic`
  - `Task`
  - `Bug`
- runtime bugs come from verifier/watchdog/runtime-gate fingerprints, not raw logs or chat alerts
- ordinary development, debugging, and verification should run locally first
- if the project has self-hosted runners, prefer them over paid GitHub-hosted Actions for recurring work
- GitHub Actions are for repository-native automation, schedules, deploys, and hosted checks that genuinely belong there
- serious slices begin with `kernel_upstream_check`
- the project pins its upstream kernel commit in `.kernel/upstream.json`
- if drift exists, open or update a `kernel_adoption_task`
- `kernel_adoption_task` records one decision:
  - `adopt_now`
  - `defer`
  - `not_applicable`
- `.kernel/upstream.json` only advances after adoption is implemented and verified
- kernel updates are adopted explicitly through normal project issues/PRDs, not auto-applied blindly
- every serious slice ends with `kernel_sync_review`
- serious closeouts record `Kernel Impact`
- PR closes the leaf issue only
- `gh issue create` and `gh pr create` should use `--body-file` or a single-quoted heredoc-generated file, not inline markdown bodies
- for GitHub sub-issues, prefer `scripts/link_github_sub_issue.py`; if you call REST directly, `sub_issue_id` means child issue database id, not `#issue_number`
- GitHub Projects are optional and should be adopted only when issue-first execution needs shared fields/views or cross-repo planning
- any optional `CLAUDE.md` / Cursor / skill-style behavior overlay must stay thin and subordinate to the repo-local canon

## Canon files

- `README.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `.kernel/upstream.json`
- `.github/ISSUE_TEMPLATE/*`
- `.github/pull_request_template.md`
- `.github/CODEOWNERS`
- `.github/labels.yml`
- `scripts/sync_github_labels.py`
- `scripts/check_kernel_upstream.py`
- active PRD in `docs/`
