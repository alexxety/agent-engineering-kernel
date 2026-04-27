# Environment Promotion Canon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the reusable local/verify/staging/production promotion model to the universal engineering kernel.

**Architecture:** The rule lives in one reference document, one machine-readable kernel section, and the bootstrap templates that downstream projects inherit. Tests assert that the kernel docs and generated templates keep the rule.

**Tech Stack:** Markdown, YAML, Python unittest/pytest.

---

### Task 1: Add Canon And Templates

**Files:**
- Create: `references/ENVIRONMENT_PROMOTION.md`
- Modify: `ENGINEERING_KERNEL.yaml`
- Modify: `README.md`
- Modify: `SKILL.md`
- Modify: `references/BOOTSTRAP.md`
- Modify: `references/EXECUTION_SURFACES.md`
- Modify: `references/GITHUB_DELIVERY.md`
- Modify: `templates/project/README.md`
- Modify: `templates/project/AGENTS.md`
- Modify: `templates/project/CONTRIBUTING.md`
- Modify: `templates/project/docs/PRD_TEMPLATE.md`

- [ ] Add environment promotion rules without project-specific provider choices.
- [ ] Ensure project templates require local, disposable verify, staging, and production boundaries.
- [ ] Ensure production secrets and mutating production tests are forbidden.

### Task 2: Add Verification

**Files:**
- Modify: `tests/test_repo_kernel_canon.py`
- Modify: `tests/test_bootstrap_project_kernel.py`

- [ ] Assert the machine-readable kernel has `environment_promotion_policy`.
- [ ] Assert README/reference/templates mention local, verify, staging, production, production secrets, and mutating tests.
- [ ] Assert bootstrapped projects inherit the rule.
- [ ] Run `python3 -m pytest`.
