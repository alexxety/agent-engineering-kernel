# Project Name

This repository follows the agent engineering kernel.

## Engineering canon

- non-trivial work is PRD-first
- non-trivial work starts from a parent GitHub issue
- GitHub hierarchy:
  - `Epic`
  - `Task`
  - `Bug`
- runtime bugs come from verifier/watchdog/runtime-gate fingerprints, not raw logs or chat alerts
- ordinary development, debugging, and verification should run locally first
- if the project has self-hosted runners, prefer them over paid GitHub-hosted Actions for recurring work
- GitHub Actions are for repository-native automation, schedules, deploys, and hosted checks that genuinely belong there
- PR closes the leaf issue only
- `gh issue create` and `gh pr create` should use `--body-file` or a single-quoted heredoc-generated file, not inline markdown bodies

## Canon files

- `README.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `.github/ISSUE_TEMPLATE/*`
- `.github/pull_request_template.md`
- `.github/CODEOWNERS`
- `.github/labels.yml`
- `scripts/sync_github_labels.py`
- active PRD in `docs/`
