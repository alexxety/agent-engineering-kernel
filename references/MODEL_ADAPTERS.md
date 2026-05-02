# Model Adapter Policy

The engineering kernel is shared. The model adapter is thin.

## Shared across GPT/Codex and Claude-style agents

- PRD-first workflow
- research -> code audit -> reconciliation -> documentation first -> implementation -> verification
- GitHub `Epic / Task / Bug`
- PR closes leaf issue only
- docs updated in the same slice
- verification matrix and rollback discipline
- MCP or App connector use for structured external-service operations, with local `gh` fallback treated as a different identity

## Allowed to differ by model

- which tools are available
- how planning is surfaced
- shell/editor constraints
- verbosity and final report style
- local skills/plugins/integrations
- how Superpowers or equivalent process skills are invoked or surfaced
- which MCP server or App connector surfaces are available
- whether a thin behavior-only overlay is materialized in a tool-specific surface

## Claude Code as a subagent adapter

Claude Code can be used as an external subagent, but it remains an adapter
under the shared orchestrator/worker/reviewer workflow. It is not a separate
engineering process and not a reason to bypass PRD, write-set, review,
verification, or rollback rules.

Default approved shape:

- one-shot read-only reviewer or design-review worker;
- local repository context only;
- no inherited MCP/App connector surface;
- direct Claude Code binary preferred over wrapper binaries;
- controlled review model pinned by default, currently `claude-opus-4-7`;
- observable stream output for long runs;
- explicit `dontAsk` permission mode, never `plan`;
- smallest possible tool set: no tools for smoke, `Read` for exact-file
  review, and `Read,Grep,Glob` only when repo search is required;
- mode-specific budget cap as a runaway guardrail;
- orchestrator supplies external research evidence, live-system facts, and the
  exact question to review.

When the operator explicitly asks for Claude Code, do not silently substitute a
GPT/Codex worker if Claude Code fails. Diagnose Claude Code first:

- is the CLI installed;
- is auth healthy for the intended auth mode;
- is MCP disabled with strict config;
- are tool permissions scoped correctly;
- is `stream-json` paired with `--verbose`;
- is `plan` mode avoided;
- is the command using a direct binary rather than an unexpected wrapper;
- did the process exit, hang, or fail before starting.

Fallback to another agent family only after explicit operator approval and a
recorded adapter gap.

For OAuth-backed local Claude Code installs, do not add `--bare` to the default
worker command. `--bare` is reserved for explicitly verified API-key or
`apiKeyHelper` configurations.

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

## MCP/App connector adapter rule

MCP servers and App connector integrations are tool surfaces, not separate engineering processes. Use them for supported structured operations when available and authorized.

Local `gh` auth and GitHub App connector auth are different identities with separate permissions. A platform may expose GitHub through an MCP-backed App connector, while another agent only has `gh`; both must preserve the same issue-first, PRD-first, verification-first workflow.

If a GitHub App connector is missing or blocked, use the canonical shell-safe `gh` fallback and record the gap when it affects the slice. Do not copy tokens between adapters or store them in repo files.

## Hard rule

Do not create one process for GPT and another for Claude unless the platform genuinely prevents a shared workflow.
