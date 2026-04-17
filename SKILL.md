---
name: engineering-kernel
description: Bootstrap or audit a serious agent-led engineering workflow in any repository. Use when Codex must establish or update project canon, PRD-first execution, GitHub Epic/Task/Bug decomposition, PR verification discipline, reusable bootstrap files, or a model-agnostic workflow that future GPT/Codex and Claude-style agents can reuse without re-explaining the process in chat.
---

# Engineering Kernel

Use this skill when the task is to establish or upgrade a repository's engineering operating system, not when the task is simply to ship a normal feature.

Read [ENGINEERING_KERNEL.yaml](ENGINEERING_KERNEL.yaml) for the machine-readable core.
Read [references/BOOTSTRAP.md](references/BOOTSTRAP.md) when you need to materialize the kernel into a project.
Read [references/MODEL_ADAPTERS.md](references/MODEL_ADAPTERS.md) when the user asks how the kernel should map across GPT/Codex and Claude-style agents.
Read [references/RESEARCH_POLICY.md](references/RESEARCH_POLICY.md) when the user asks how research and evidence collection should work.
Read [references/GITHUB_DELIVERY.md](references/GITHUB_DELIVERY.md) when the user asks how branch/PR/merge flow should work end-to-end.

## Use this skill for

- creating a reusable engineering kernel for future projects
- bootstrapping a new repository so agents stop depending on chat memory
- establishing PRD-first execution
- establishing GitHub `Epic / Task / Bug` workflow
- establishing Tavily-first research behavior
- establishing branch / draft PR / merge discipline
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

Use the templates in [templates/project](/Users/raketa23/Work/Vs/agent-engineering-kernel/templates/project) when bootstrapping a repo.
