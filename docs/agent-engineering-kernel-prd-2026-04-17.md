# PRD: Agent Engineering Kernel

Date: `2026-04-17`

Status: `active`

## Problem

Future agent sessions should not need the engineering process re-explained from chat history.

The reusable kernel must be strong enough that a new agent can enter a fresh repository and immediately know:

- research is Tavily-first
- non-trivial work is PRD-first
- GitHub work is issue-first with `Epic / Task / Bug`
- PRs are leaf-issue scoped
- verification and rollback are required before merge
- repo-managed GitHub metadata lives in files, not only in UI memory

## Current State

The standalone repository already exists and is live on GitHub. It already contains:

- root `SKILL.md`
- machine-readable `ENGINEERING_KERNEL.yaml`
- reusable references
- reusable project bootstrap templates
- deterministic bootstrap copier
- root community-health files for the kernel repo itself

Gaps before closure:

- the kernel repo itself still needs complete repo-managed GitHub canon files committed and pushed
- label source-of-truth needs a durable sync script and regression coverage
- bootstrap acceptance should prove that target repos receive the full kernel surface, not a partial subset
- the skill should expose explicit UI metadata so it is consumable as a first-class reusable skill, not only as a raw directory
- template outputs should include the minimum community-health layer expected for serious repositories, not just issue/PR plumbing

## Target State

One standalone repository acts as both:

- the durable source-of-truth for the engineering kernel
- the installable skill root for future agent sessions

The minimal universal core must include:

- project canon
- PRD-first execution
- Tavily-first research policy
- GitHub `Epic / Task / Bug`
- PR verification contract
- repo-managed labels
- issue forms
- PR template
- `CODEOWNERS`
- contributor guidance
- community-health starter files
- deterministic bootstrap and validation path

The maximum practical layer remains separate and may be plan-gated:

- protected branches / rulesets
- required approvals
- stale review dismissal
- required code-owner review
- required status checks
- merge queue / auto-merge
- GitHub Projects / issue types

## Files To Change

Kernel repo:

- `README.md`
- `SKILL.md`
- `ENGINEERING_KERNEL.yaml`
- `CONTRIBUTING.md`
- `.github/CODEOWNERS`
- `.github/labels.yml`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/ISSUE_TEMPLATE/epic.yml`
- `.github/ISSUE_TEMPLATE/task.yml`
- `.github/ISSUE_TEMPLATE/bug.yml`
- `.github/pull_request_template.md`
- `agents/openai.yaml`
- `references/BOOTSTRAP.md`
- `scripts/sync_github_labels.py`
- `tests/test_repo_kernel_canon.py`
- `tests/test_bootstrap_project_kernel.py`
- `tests/test_sync_github_labels.py`

Project templates:

- `templates/project/README.md`
- `templates/project/AGENTS.md`
- `templates/project/CONTRIBUTING.md`
- `templates/project/.github/CODEOWNERS`
- `templates/project/.github/labels.yml`
- `templates/project/.github/ISSUE_TEMPLATE/config.yml`
- `templates/project/.github/ISSUE_TEMPLATE/epic.yml`
- `templates/project/.github/ISSUE_TEMPLATE/task.yml`
- `templates/project/.github/ISSUE_TEMPLATE/bug.yml`
- `templates/project/.github/pull_request_template.md`
- `templates/project/scripts/sync_github_labels.py`
- `templates/project/docs/PRD_TEMPLATE.md`
- `templates/project/CODE_OF_CONDUCT.md`
- `templates/project/SECURITY.md`

## Rollout

### Phase 1: Document the full kernel target

Entry condition:

- standalone kernel repo exists

Validation:

- PRD reflects current state, target state, files, verification, and rollback

Success:

- repo has one active execution source-of-truth

Rollback trigger:

- if target state is still ambiguous, stop before further edits

### Phase 2: Close kernel repo gaps

Entry condition:

- PRD updated

Validation:

- repo-managed GitHub files exist at root
- `agents/openai.yaml` exists
- label sync script exists and is tested

Success:

- kernel repo is internally self-consistent

Rollback trigger:

- if root repo files and tests disagree, stop before push

### Phase 3: Close bootstrap gaps

Entry condition:

- kernel repo surface is complete

Validation:

- bootstrap dry-run lists the expected files
- bootstrap apply writes the expected files into a clean target

Success:

- a fresh target repo receives the same canon consistently

Rollback trigger:

- if template outputs drift from kernel intent, do not close

### Phase 4: Live repository application

Entry condition:

- local tests pass

Validation:

- `git diff --check`
- root label sync dry-run / apply against the live kernel repo
- live repo settings verified where supported

Success:

- GitHub repo reflects the file-managed canon

Rollback trigger:

- any live GitHub mutation fails or produces unexpected drift

## Verification Matrix

Code-path tests:

- `tests/test_bootstrap_project_kernel.py`
- `tests/test_repo_kernel_canon.py`
- `tests/test_sync_github_labels.py`

Build/runtime checks:

- `.venv/bin/python -m unittest discover -s tests`

Config drift checks:

- `git diff --check`

Sync checks:

- `.venv/bin/python scripts/sync_github_labels.py --dry-run`

Live runtime checks:

- live GitHub label sync against `alexxety/agent-engineering-kernel`
- live repo merge/delete settings verification when supported

Rollback:

- revert the kernel repo commit
- restore previous root/template files
- if GitHub labels were mutated incorrectly, rerun label sync from the corrected `.github/labels.yml`

## Acceptance

- future agents can read one standalone source instead of chat memory
- the same kernel can be reused across repositories
- the same kernel can be consumed by GPT/Codex and Claude-style agents
- bootstrap produces PRD/issue/label/community-health canon deterministically
- the kernel repo itself follows the same GitHub canon it prescribes
