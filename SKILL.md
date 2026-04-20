---
name: engineering-kernel
description: Bootstrap or audit a serious agent-led engineering workflow in any repository. Use when Codex must establish or update project canon, PRD-first execution, GitHub Epic/Task/Bug decomposition, PR verification discipline, reusable bootstrap files, or a model-agnostic workflow that future GPT/Codex and Claude-style agents can reuse without re-explaining the process in chat.
---

# Engineering Kernel

Use this skill when the task is to establish or upgrade a repository's engineering operating system, not when the task is simply to ship a normal feature.

Read [ENGINEERING_KERNEL.yaml](ENGINEERING_KERNEL.yaml) for the machine-readable core.
Read [references/BOOTSTRAP.md](references/BOOTSTRAP.md) when you need to materialize the kernel into a project.
Read [references/MODEL_ADAPTERS.md](references/MODEL_ADAPTERS.md) when the user asks how the kernel should map across GPT/Codex and Claude-style agents.
Read [references/BEHAVIORAL_OVERLAY.md](references/BEHAVIORAL_OVERLAY.md) when the user asks whether a thin behavior-only guideline layer should exist across `CLAUDE.md`, Cursor rules, or skill/plugin surfaces.
Read [references/RESEARCH_POLICY.md](references/RESEARCH_POLICY.md) when the user asks how research and evidence collection should work.
Read [references/EXECUTION_SURFACES.md](references/EXECUTION_SURFACES.md) when the user asks where work should run locally versus in GitHub Actions or CI.
Read [references/KERNEL_SYNC_POLICY.md](references/KERNEL_SYNC_POLICY.md) when the user asks how live project learnings should be reviewed and promoted back into the universal kernel.
Read [references/KERNEL_UPSTREAM_AWARENESS.md](references/KERNEL_UPSTREAM_AWARENESS.md) when the user asks how consumer projects should notice upstream kernel changes and decide whether to adopt them.
Read [references/KERNEL_ADOPTION_TASK.md](references/KERNEL_ADOPTION_TASK.md) when the user asks what exact downstream `Task` should be opened or updated after `kernel_upstream_check` reports drift.
Read [references/KERNEL_FLEET_SWEEP.md](references/KERNEL_FLEET_SWEEP.md) when the user asks how one operator machine should check kernel drift across many consumer repositories at once.
Read [references/GITHUB_DELIVERY.md](references/GITHUB_DELIVERY.md) when the user asks how branch/PR/merge flow should work end-to-end.
Read [references/BUG_INTAKE.md](references/BUG_INTAKE.md) when the user asks how runtime failures should become GitHub `Bug` issues without noisy duplication.

The bug-intake rule is explicit:

- do not create bug issues from raw logs or chat alerts
- use one stable fingerprint per bug class
- update the existing open bug issue when the fingerprint matches

## Use this skill for

- creating a reusable engineering kernel for future projects
- bootstrapping a new repository so agents stop depending on chat memory
- establishing PRD-first execution
- establishing GitHub `Epic / Task / Bug` workflow
- establishing automatic deduplicated GitHub bug intake
- establishing Tavily-first research behavior
- establishing local-first execution and prerequisite bootstrap
- establishing kernel sync review and kernel impact discipline
- establishing kernel upstream awareness and downstream adoption checks
- establishing the canonical `kernel_adoption_task` work item for downstream kernel updates
- establishing optional multi-repo kernel fleet sweep on the operator machine
- running the `kernel_upstream_check` protocol in consumer repositories
- running the `kernel_fleet_sweep` protocol for multiple consumer repositories
- running the `kernel_sync_review` closure protocol
- establishing branch / draft PR / merge discipline
- establishing safe GitHub sub-issue linkage from normal issue numbers
- creating project-local canon files and templates
- creating repo-managed GitHub metadata and community-health files
- auditing an existing repo against the kernel and closing the gaps

## Do not use this skill for

- ordinary feature implementation
- routine debugging
- generic documentation edits
- code review that does not change the workflow canon

## Workflow

1. Inspect project reality first.
- source-of-truth docs
- runtime and CI entrypoints
- current GitHub workflow state
- current validation layers

2. Apply the minimal core before discussing maximum enforcement.
- project canon
- PRD-first execution
- issue tree
- local-first execution surface
- kernel upstream awareness
- kernel sync review
- PR verification contract
- ownership and labels
- research policy
- GitHub delivery flow

3. Keep the core model-agnostic.
One engineering process, thin adapters only.

4. Prefer deterministic bootstrap.
Use the provided templates and bootstrap script instead of recreating the same files from scratch.

5. Record plan-gated enforcement honestly.
If GitHub settings or plan limits block a stronger layer, document the gap. Do not pretend enforcement exists when the platform is not enforcing it.

## Output standard

Prefer a small durable set of outputs:

- project-local canon docs
- `AGENTS.md`
- `CONTRIBUTING.md`
- issue templates
- PR template
- labels source-of-truth
- `scripts/sync_github_labels.py`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `CODEOWNERS`
- active PRD / decision record
- explicit bug-intake policy for verifier/watchdog/runtime incidents
- explicit `kernel_impact` field in PRD/closeout flow
- explicit `Kernel Impact` closeout decision after serious slices

Use the templates in [templates/project](templates/project) when bootstrapping a repo.
