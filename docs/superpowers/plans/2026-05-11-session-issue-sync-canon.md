# Session Issue Sync Canon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable kernel rule requiring every serious engineering slice to record an explicit `Issue Sync` closeout decision.

**Architecture:** Add one focused reference document, expose the policy in `ENGINEERING_KERNEL.yaml`, and propagate the closeout field into project templates. Tests pin the reference file, machine-readable policy, and bootstrap template text so downstream repos inherit the rule.

**Tech Stack:** Markdown canon files, YAML kernel state, Python `unittest` repository canon tests.

---

### Task 1: Add Reference And Machine-Readable Policy

**Files:**
- Create: `references/SESSION_ISSUE_SYNC.md`
- Modify: `ENGINEERING_KERNEL.yaml`
- Modify: `SKILL.md`
- Modify: `README.md`

- [x] **Step 1: Create the reference document**

Add `references/SESSION_ISSUE_SYNC.md` with the canonical values:

```markdown
# Session Issue Sync

Use this when closing a serious engineering slice, PRD slice, bugfix, or agent-led work session that has durable GitHub issue state.

Every serious slice ends with:

- `Issue Sync: updated`
- `Issue Sync: skipped`
- `Issue Sync: not_applicable`
```

- [x] **Step 2: Add `session_issue_sync_policy` to `ENGINEERING_KERNEL.yaml`**

Add it to `layers.minimal_core` and create a top-level policy with:

```yaml
session_issue_sync_policy:
  closeout_field: Issue Sync
  allowed_values:
    - updated
    - skipped
    - not_applicable
```

- [x] **Step 3: Surface the reference in root docs**

Add `references/SESSION_ISSUE_SYNC.md` to `SKILL.md` and `README.md`, keeping it subordinate to PRD-first, issue-first, and verification discipline.

### Task 2: Propagate Project Template Canon

**Files:**
- Modify: `templates/project/AGENTS.md`
- Modify: `templates/project/CONTRIBUTING.md`
- Modify: `templates/project/README.md`
- Modify: `templates/project/docs/PRD_TEMPLATE.md`
- Modify: `references/GITHUB_DELIVERY.md`

- [x] **Step 1: Add template instructions**

Project templates must say that serious slices close with `Issue Sync: updated | skipped | not_applicable`.

- [x] **Step 2: Add PRD template field**

Add this section before `Kernel Impact`:

```markdown
## Issue Sync

Record this during closeout.

Choose one:

- `updated`
- `skipped`
- `not_applicable`

Why:

Explain whether the relevant GitHub issue state was updated, intentionally skipped, or not applicable.
```

- [x] **Step 3: Link it from GitHub delivery**

Add a rule that PR/closeout updates the leaf issue or records why no update happened, without allowing unapproved GitHub writes.

### Task 3: Add Tests

**Files:**
- Modify: `tests/test_repo_kernel_canon.py`
- Modify: `tests/test_bootstrap_project_kernel.py`

- [x] **Step 1: Pin top-level reference and YAML policy**

Extend `test_repo_has_expected_top_level_health_files` and `test_machine_readable_kernel_parses` to require `references/SESSION_ISSUE_SYNC.md` and `session_issue_sync_policy`.

- [x] **Step 2: Pin bootstrap inheritance**

Extend `test_copy_templates_apply_writes_files` to require `Issue Sync` in generated `AGENTS.md`, `CONTRIBUTING.md`, and `docs/PRD_TEMPLATE.md`.

### Task 4: Verify And Commit

**Files:**
- All files above

- [x] **Step 1: Run focused tests**

Run:

```bash
.venv/bin/python -m unittest tests.test_repo_kernel_canon tests.test_bootstrap_project_kernel
```

Expected: 32 selected tests pass.

- [x] **Step 2: Run full tests**

Run:

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

Expected: 44 tests pass.

- [x] **Step 3: Run whitespace check**

Run:

```bash
git diff --check
```

Expected: no output.

- [ ] **Step 4: Commit**

Run:

```bash
git add ENGINEERING_KERNEL.yaml README.md SKILL.md references/SESSION_ISSUE_SYNC.md references/GITHUB_DELIVERY.md templates/project/AGENTS.md templates/project/CONTRIBUTING.md templates/project/README.md templates/project/docs/PRD_TEMPLATE.md tests/test_repo_kernel_canon.py tests/test_bootstrap_project_kernel.py docs/session-issue-sync-canon-prd-2026-05-11.md docs/superpowers/plans/2026-05-11-session-issue-sync-canon.md
git commit -m "docs: add session issue sync canon"
```
