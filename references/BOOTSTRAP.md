# Bootstrap Workflow

Use this file when applying the kernel to a new repository.

## Order

1. Inspect the repository before writing canon.
2. Decide whether the project already has stronger local rules.
3. Install the minimal core first.
4. Document the maximum GitHub layer separately if settings or plan limits block enforcement.
5. Record the canonical execution surface and local bootstrap path before normal work begins.

## Minimal bootstrap outputs

Write or update:

- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/ISSUE_TEMPLATE/epic.yml`
- `.github/ISSUE_TEMPLATE/task.yml`
- `.github/ISSUE_TEMPLATE/bug.yml`
- `.github/pull_request_template.md`
- `.github/CODEOWNERS`
- `.github/labels.yml`
- `scripts/sync_github_labels.py`
- `scripts/check_kernel_upstream.py`
- `.kernel/upstream.json`
- one active PRD / decision doc

The bootstrapped canon should also make explicit:

- canonical local bootstrap command
- canonical local verifier/test commands
- whether the repo uses self-hosted runners
- the self-hosted runner label(s) if recurring GitHub checks are required
- which workflows must stay in GitHub Actions
- that GitHub coordinates repository workflow but owned compute executes routine development and verification by default
- that routine development and verification should not default to paid GitHub-hosted Actions, dependency cache uploads, or long-lived artifact storage
- that each serious slice begins with `kernel_upstream_check`
- that each serious slice ends with `kernel_sync_review`
- that active PRDs and closeouts carry a `Kernel Impact` decision
- that Superpowers or equivalent process skills are tactical workflow aids, subordinate to repo canon, and should be read or invoked before acting when relevant and available
- that the minimum Superpowers mapping includes `using-superpowers` for skill selection and `verification-before-completion` before success claims
- that MCP or App connector tooling is preferred for supported structured external-service operations when available and authorized
- that local `gh` auth and GitHub App connector auth are different identities with separate permissions
- that GitHub App repository access and permissions are configured in GitHub Installed Apps, not by storing or editing tokens in project files
- that shell-safe `gh` fallback remains canonical when an App connector is missing, stale, or blocked
- that the consumer project pins the exact kernel commit it bootstrapped from
- that every `external_contract_slice` records an explicit `external_source_of_truth_matrix` in the active PRD or decision note
- that any optional `CLAUDE.md` / Cursor rule / skill-style behavior overlay is thin, subordinate to repo canon, and synced from one canonical overlay source if the project chooses to use it

## How to use the templates

Use the bootstrap script for deterministic materialization:

```bash
python3 scripts/bootstrap_project_kernel.py --target /absolute/path/to/repo --apply
```

After bootstrap, sync labels from file instead of hand-editing them in the GitHub UI:

```bash
python3 scripts/sync_github_labels.py --dry-run
python3 scripts/sync_github_labels.py --apply
```

Do not blindly overwrite stronger project-local canon unless the task is an intentional migration.

Do not treat a compact behavior guideline file as a replacement for the bootstrapped canon. If a project wants that extra layer, add it separately and keep it thin.

Do not treat Superpowers or another process-skill pack as a replacement for the bootstrapped canon. Skills help the agent choose the right workflow; the project canon remains the source of truth.

Do not treat MCP or App connector access as the same thing as local `gh` access. They are different identities. If a GitHub App connector fails with a permissions error, fix the installed GitHub App repository access and permissions before refreshing local CLI auth.

Bootstrap should pin the current kernel commit into `.kernel/upstream.json` instead of leaving placeholder or branch-only metadata.

If the target repository needs a license, choose it intentionally for that project instead of copying a random default.

## What to tell the user

Summaries should separate:

- current repo reality
- kernel artifacts created or updated
- enforcement that is live now
- enforcement that is still blocked by GitHub settings or plan limits
