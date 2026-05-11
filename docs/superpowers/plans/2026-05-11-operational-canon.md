# Operational Canon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add universal work item routing, project health audit, and optional weekly operating loop canon to the engineering kernel.

**Architecture:** Add three focused reference docs and three machine-readable YAML policies. Propagate only short operational rules into root docs, bootstrap/delivery references, and project templates; tests pin the policies and bootstrap inheritance.

**Tech Stack:** Markdown canon files, YAML kernel state, Python `unittest` repository canon tests.

---

### Task 1: Write Failing Canon Tests

**Files:**
- Modify: `tests/test_repo_kernel_canon.py`
- Modify: `tests/test_bootstrap_project_kernel.py`

- [x] **Step 1: Require top-level references and YAML policies**

Add assertions requiring:

```python
"references/WORK_ITEM_ROUTING.md"
"references/PROJECT_HEALTH_AUDIT.md"
"references/OPTIONAL_WEEKLY_OPERATING_LOOP.md"
```

and:

```python
self.assertIn("work_item_routing_policy", payload)
self.assertIn("project_health_audit_policy", payload)
self.assertIn("optional_weekly_operating_loop_policy", payload)
```

- [x] **Step 2: Require docs and templates to mention the new canon**

Add text tests for:

```python
"Work Item Routing"
"Project Health Audit"
"Optional Weekly Operating Loop"
```

in root docs, references, and project templates.

- [x] **Step 3: Run focused tests and confirm RED**

Run:

```bash
.venv/bin/python -m unittest tests.test_repo_kernel_canon tests.test_bootstrap_project_kernel
```

Expected: fails because references and YAML policies do not exist yet.

### Task 2: Add Reference Docs And YAML Policies

**Files:**
- Create: `references/WORK_ITEM_ROUTING.md`
- Create: `references/PROJECT_HEALTH_AUDIT.md`
- Create: `references/OPTIONAL_WEEKLY_OPERATING_LOOP.md`
- Modify: `ENGINEERING_KERNEL.yaml`
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `CHANGELOG.md`

- [x] **Step 1: Add `WORK_ITEM_ROUTING.md`**

Define routing rules: identify target repo/surface, never default to current checkout, search duplicates in target, ask or record ambiguity, keep routing config project-local.

- [x] **Step 2: Add `PROJECT_HEALTH_AUDIT.md`**

Define audit checklist: SSOT, metric definitions, freshness policy, decision log, escalation rules, incident log, prohibited actions, eval/golden cases, runbooks.

- [x] **Step 3: Add `OPTIONAL_WEEKLY_OPERATING_LOOP.md`**

Define optional cadence: outcomes with checks, plan-vs-actual scorecard, evidence-based retro, terminal carryover decisions, no mandatory W-labels or Projects.

- [x] **Step 4: Add YAML policies**

Add all three policies to `layers.minimal_core` or `optional_operator_layers` as appropriate:

```yaml
work_item_routing_policy:
project_health_audit_policy:
optional_weekly_operating_loop_policy:
  bootstrap_default: false
```

- [x] **Step 5: Surface references in root docs**

Update `SKILL.md`, `README.md`, and `CHANGELOG.md`.

### Task 3: Propagate Project Templates

**Files:**
- Modify: `references/BOOTSTRAP.md`
- Modify: `references/GITHUB_DELIVERY.md`
- Modify: `templates/project/AGENTS.md`
- Modify: `templates/project/CONTRIBUTING.md`
- Modify: `templates/project/README.md`
- Modify: `templates/project/docs/PRD_TEMPLATE.md`

- [x] **Step 1: Add bootstrap guidance**

Bootstrap should make explicit whether the project has routing rules, health audit checklist owners, and optional weekly loop adoption.

- [x] **Step 2: Add delivery guidance**

GitHub delivery should route work before issue creation and search duplicates in the target surface.

- [x] **Step 3: Add project template sections**

Add concise sections for routing, health audit, and optional weekly loop.

- [x] **Step 4: Add PRD template fields**

Add fields for work item routing, health audit, and optional weekly loop applicability.

### Task 4: Verify, Commit, And Publish

**Files:**
- All files above
- `docs/operational-routing-health-weekly-loop-prd-2026-05-11.md`
- `docs/superpowers/plans/2026-05-11-operational-canon.md`

- [x] **Step 1: Run focused tests**

Run:

```bash
.venv/bin/python -m unittest tests.test_repo_kernel_canon tests.test_bootstrap_project_kernel
```

Expected: selected tests pass.

- [x] **Step 2: Run full tests**

Run:

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

Expected: all tests pass.

- [x] **Step 3: Run whitespace check**

Run:

```bash
git diff --check
```

Expected: no output.

- [ ] **Step 4: Commit and push**

Commit message:

```bash
docs: add operational canon layers
```

- [ ] **Step 5: Open PR and update Task #65**

Use `--body-file` for PR/issue body updates. Record `Issue Sync: updated`.
