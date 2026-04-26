# Model Adapter Policy

The engineering kernel is shared. The model adapter is thin.

## Shared across GPT/Codex and Claude-style agents

- PRD-first workflow
- research -> code audit -> reconciliation -> documentation first -> implementation -> verification
- GitHub `Epic / Task / Bug`
- PR closes leaf issue only
- docs updated in the same slice
- verification matrix and rollback discipline

## Allowed to differ by model

- which tools are available
- how planning is surfaced
- shell/editor constraints
- verbosity and final report style
- local skills/plugins/integrations
- how Superpowers or equivalent process skills are invoked or surfaced
- whether a thin behavior-only overlay is materialized in a tool-specific surface

## Behavioral overlay rule

An optional behavior-only layer may exist across tool-specific surfaces such as:

- `CLAUDE.md`
- Cursor project rules
- skill/plugin wrappers

But it must stay:

- thin
- synced from one canonical source
- lower priority than the repo-local canon and the shared engineering kernel

Do not confuse a behavior overlay with the engineering workflow itself.

## Process-skill adapter rule

Superpowers or another process-skill pack may provide model-specific invocation mechanics, but the workflow intent stays shared:

- design before implementation
- explicit plan before multi-step edits
- TDD for implementation and bugfixes
- systematic debugging before fixes
- fresh verification before completion claims
- review before merge or handoff

If one platform has a skill tool and another only has markdown instructions, keep the same meaning and adapt only the invocation surface.

Process skills remain lower priority than project canon, the active PRD, tests, and explicit user instructions.

The shared meaning includes `using-superpowers` for skill selection and `verification-before-completion` before success claims when Superpowers is available.

## Hard rule

Do not create one process for GPT and another for Claude unless the platform genuinely prevents a shared workflow.
