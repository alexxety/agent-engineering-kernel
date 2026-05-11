# Kernel Update Publisher Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the local Codex skill that runs the `agent-engineering-kernel` article and Telegram update workflow through `dudarik.com` while blocking every media-pack path.

**Architecture:** This slice creates a local operator skill under `~/.codex/skills/publish-kernel-update/` plus a project plan record in this repository. The skill is documentation-first: it gives future agents exact paths, commands, frontmatter contracts, no-op rules, and verification gates, but this slice does not generate articles or post Telegram messages.

**Tech Stack:** Codex skill Markdown, OpenAI skill UI metadata YAML, shell validation commands, `skill-creator` validation scripts.

**Execution status:** Completed for the local skill slice. Publication, dudarik
content mutation, and production Telegram sends were intentionally not run.

---

### Task 1: Create Delivery Issue And Baseline

**Files:**
- Create GitHub issue: `Task: Create publish-kernel-update operator skill`
- Modify: `docs/kernel-update-publisher-skill-prd-2026-04-28.md`
- Create: `docs/superpowers/plans/2026-04-28-kernel-update-publisher-skill.md`

- [x] **Step 1: Open the executable Task issue**

Run:

```bash
tmp="$(mktemp)"
printf '%s\n' \
  'Implement the local Codex skill described in docs/kernel-update-publisher-skill-prd-2026-04-28.md.' \
  '' \
  'Scope for this slice:' \
  '- create ~/.codex/skills/publish-kernel-update/' \
  '- document the dudarik article and Telegram-only route' \
  '- encode skip_media_pack and GitHub OpenGraph guardrails' \
  '- do not generate articles, send Telegram, or touch yotubol/media pipelines' \
  > "$tmp"
gh issue create --title 'Task: Create publish-kernel-update operator skill' --label task --body-file "$tmp"
rm "$tmp"
```

Expected: GitHub prints the new issue URL.

- [x] **Step 2: Record the Task number in the PRD**

Recorded `Task: #46` in the PRD. Leave the Epic line unchanged because this is one executable slice.

- [x] **Step 3: Capture baseline validation**

Run:

```bash
python3 /Users/raketa23/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/raketa23/.codex/skills/publish-kernel-update
```

Actual follow-up status: the skill directory now exists and validates.

### Task 2: Initialize The Skill Shell

**Files:**
- Create: `/Users/raketa23/.codex/skills/publish-kernel-update/SKILL.md`
- Create: `/Users/raketa23/.codex/skills/publish-kernel-update/agents/openai.yaml`
- Create: `/Users/raketa23/.codex/skills/publish-kernel-update/references/`

- [x] **Step 1: Scaffold with the official initializer**

Run:

```bash
python3 /Users/raketa23/.codex/skills/.system/skill-creator/scripts/init_skill.py publish-kernel-update \
  --path /Users/raketa23/.codex/skills \
  --resources references \
  --interface display_name='Publish Kernel Update' \
  --interface short_description='Publish kernel article and Telegram updates' \
  --interface default_prompt='Use $publish-kernel-update to check agent-engineering-kernel updates and publish through dudarik Telegram without media.'
```

Expected: the skill folder, `SKILL.md`, `agents/openai.yaml`, and `references/` exist.

### Task 3: Write Skill Instructions

**Files:**
- Modify: `/Users/raketa23/.codex/skills/publish-kernel-update/SKILL.md`
- Create: `/Users/raketa23/.codex/skills/publish-kernel-update/references/dudarik-kernel-update-flow.md`

- [x] **Step 1: Replace scaffolded `SKILL.md`**

Use this frontmatter exactly:

```yaml
---
name: publish-kernel-update
description: Use when the operator wants to publish or update a dudarik.com article and Telegram post about alexxety/agent-engineering-kernel while excluding NotebookLM, yotubol, audio, infographic, video, and YouTube media automation.
---
```

The body must include:

- target repo `/Users/raketa23/Work/Vs/agent-engineering-kernel`;
- dudarik repo `/Users/raketa23/Work/Vs/g3/dudarik.com`;
- slug `agent-engineering-kernel`;
- mandatory `skip_media_pack: true`;
- mandatory GitHub OpenGraph image URL;
- first-run and update-run branches;
- no-op behavior when no meaningful updates exist;
- dry-run verification before production Telegram commands;
- a hard ban on NotebookLM, `yotubol`, audio, infographic, video, and YouTube commands.

- [x] **Step 2: Add the detailed flow reference**

Create `references/dudarik-kernel-update-flow.md` with the article frontmatter contract, command checklist, meaningful-update criteria, failure handling, and verification matrix from the PRD.

### Task 4: Validate The Skill

**Files:**
- Validate: `/Users/raketa23/.codex/skills/publish-kernel-update/SKILL.md`
- Validate: `/Users/raketa23/.codex/skills/publish-kernel-update/agents/openai.yaml`
- Validate: `/Users/raketa23/.codex/skills/publish-kernel-update/references/dudarik-kernel-update-flow.md`

- [x] **Step 1: Run official skill validation**

Run:

```bash
python3 /Users/raketa23/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/raketa23/.codex/skills/publish-kernel-update
```

Expected: PASS.

- [x] **Step 2: Run guardrail content checks**

Run:

```bash
rg -n 'skip_media_pack: true|opengraph.githubassets.com/dudarik/alexxety/agent-engineering-kernel|telegram-publish.py|queue-yotubol.py|NotebookLM|YouTube|audio|infographic|video' /Users/raketa23/.codex/skills/publish-kernel-update
rg -n 'TB''D|TO''DO|FIX''ME|\?\?\?|PLACE''HOLDER' /Users/raketa23/.codex/skills/publish-kernel-update
```

Expected: the first command finds the required guardrail terms; the second command exits with no matches.

- [x] **Step 3: Run whitespace checks**

Run:

```bash
git diff --check
git diff --no-index --check /dev/null /Users/raketa23/.codex/skills/publish-kernel-update/SKILL.md || test $? -eq 1
git diff --no-index --check /dev/null /Users/raketa23/.codex/skills/publish-kernel-update/references/dudarik-kernel-update-flow.md || test $? -eq 1
git diff --no-index --check /dev/null /Users/raketa23/.codex/skills/publish-kernel-update/agents/openai.yaml || test $? -eq 1
```

Expected: no whitespace errors.
