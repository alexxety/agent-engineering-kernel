# GitHub Delivery Flow

Use this when the user wants the full branch / PR / merge discipline, not just issue templates.

Execution-surface rule:

- GitHub delivery flow does not mean GitHub-hosted Actions are the default place to do ordinary engineering work
- GitHub coordinates issues, PRs, check status, schedules, and deploy triggers; owned compute executes routine work by default
- local operator execution or self-hosted runners stay primary for normal dev/test/bootstrap work
- GitHub Actions are for repository-native automation, scheduled/event jobs, deploys, and hosted verification that must live in the platform
- paid GitHub-hosted runners, dependency caches, and long-lived artifacts in private repositories require an explicit PRD/decision note that accepts the paid surface

Tooling rule:

- use MCP or App connector tooling for supported structured GitHub issue, pull request, review, and metadata operations when available and authorized
- local `gh` auth and GitHub App connector auth are different identities with separate permissions
- if the App connector returns `Resource not accessible by integration`, check the installed GitHub App repository access and permissions before refreshing the local `gh` token
- when the connector is unavailable, stale, or missing a needed operation, use the shell-safe `gh` fallback below

Git state serialization rule:

- serialize git commands that touch refs, the index, or the working tree within
  one repository
- do not run `git fetch`, `git pull`, `git switch`, `git checkout`, `git
  merge`, `git rebase`, `git branch -d/-D`, or `git push` through parallel
  tool wrappers for the same repo
- read-only commands such as `git diff`, `git status`, `git log`, and `git
  show` may be parallelized only when they do not depend on a fresh ref update
  and no ref-mutating git command is running for that repo
- if a ref lock race occurs, recover sequentially: `git status --short
  --branch`, then the needed `git fetch`, then `git pull --ff-only` when
  appropriate, then `git diff --check`

## Canonical sequence

1. Create or update the PRD
2. Open the parent `Epic` if the work is non-trivial
3. Create the executable leaf issue (`Task` or `Bug`)
4. Create the branch from the leaf issue
5. Capture baseline verification when an existing deterministic contract already exists
6. Implement in a small slice
7. Open or update a draft PR
8. Run post-change verification
9. Mark the PR ready
10. Merge
11. Delete the head branch

For production-bound work, the project-specific rollout should continue after
merge from local verification through disposable verify, staging deploy, staging
smoke checks, manual production approval, production backup or restore point,
production deploy, read-safe production smoke checks, and monitoring.

## Rules

- PR closes the leaf issue only
- parent epic stays open until all required leaf issues and acceptance checks are complete
- baseline-before-edits and post-change verification are different moments; keep both explicit when an existing contract already exists
- keep the PR description aligned with the real scope and verification
- production-bound PRs should name the staging and production promotion gates or link the decision note that owns them
- use draft PR while the scope or verification is still moving
- prefer squash merge unless the project canon explicitly chooses another method
- automatic bug intake opens or updates the `Bug` issue before the fix slice starts
- repeated incidents should update the existing bug issue for the same fingerprint instead of spawning duplicates
- if `kernel_upstream_check` reports `update_available`, open or update a `kernel_adoption_task` unless the active slice explicitly documents a deferral
- `kernel_adoption_task` should record one decision:
  - `adopt_now`
  - `defer`
  - `not_applicable`
- when using `gh issue create`, `gh issue edit`, or `gh pr create` from shell, prefer `--body-file` over inline `--body`
- when MCP or an App connector can do the structured write, prefer it over shelling out, then verify the connector path itself
- do not treat a working local `gh` token as proof that the GitHub App connector has repository access or write permissions
- serialize git ref/index/worktree-mutating commands per repository; never run
  fetch/pull/merge/switch/branch-delete/push in parallel for the same repo
- never embed markdown with backticks or fenced code blocks in inline double-quoted `gh --body` arguments
- acceptable fallback is a single-quoted heredoc such as `<<'EOF'` that writes the body file first
- when linking GitHub sub-issues from the CLI, prefer `scripts/link_github_sub_issue.py` or GraphQL `addSubIssue` after resolving issue node ids
- if you must call REST `POST /repos/{owner}/{repo}/issues/{issue_number}/sub_issues`, remember that `sub_issue_id` is the child issue database id, not `#issue_number`
- GitHub Projects are an optional planning layer, not a bootstrap default
- adopt a Project when multiple simultaneous engineering epics need shared custom fields, iteration views, roadmap views, or cross-repo planning
- do not require Projects when issue-first execution already covers the repo and the non-engineering lanes are data-driven outside GitHub Issues

## Why this matters

The branch/PR layer is part of the engineering kernel, not a separate afterthought. It prevents code from landing without an issue tree, verification, and an auditable review surface.

It also has to survive the shell. Inline markdown bodies are fragile in `zsh` because backticks trigger command substitution. `--body-file` keeps GitHub delivery deterministic and prevents the shell from executing or corrupting issue/PR body content.

It also has to survive multiple identities. MCP-backed App connector tokens, GitHub App installation tokens, and local `gh` tokens are different identities; diagnose permission failures on the identity that actually made the failed request.
