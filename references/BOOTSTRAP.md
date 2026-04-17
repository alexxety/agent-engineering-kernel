# Bootstrap Workflow

Use this file when applying the kernel to a new repository.

## Order

1. Inspect the repository before writing canon.
2. Decide whether the project already has stronger local rules.
3. Install the minimal core first.
4. Document the maximum GitHub layer separately if settings or plan limits block enforcement.

## Minimal bootstrap outputs

Write or update:

- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/ISSUE_TEMPLATE/epic.yml`
- `.github/ISSUE_TEMPLATE/task.yml`
- `.github/ISSUE_TEMPLATE/bug.yml`
- `.github/pull_request_template.md`
- `.github/CODEOWNERS`
- `.github/labels.yml`
- one active PRD / decision doc

## How to use the templates

Use the bootstrap script for deterministic materialization:

```bash
python3 scripts/bootstrap_project_kernel.py --target /absolute/path/to/repo --apply
```

Do not blindly overwrite stronger project-local canon unless the task is an intentional migration.

## What to tell the user

Summaries should separate:

- current repo reality
- kernel artifacts created or updated
- enforcement that is live now
- enforcement that is still blocked by GitHub settings or plan limits
