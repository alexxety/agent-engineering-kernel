# PRD: Claude Code Subagent Adapter Canon

Date: 2026-05-02

Status: accepted

Last updated: 2026-05-02

## Purpose

Define how projects that use this kernel may run Claude Code as a bounded
subagent without forking the engineering process or inheriting the
orchestrator's MCP/App connector surface.

The kernel already defines orchestrator, worker, reviewer, no-MCP worker, and
thread-lifecycle rules. This slice adds the Claude Code adapter details:
startup, auth checks, MCP isolation, allowed tools, one-shot lifecycle,
failure handling, and the no-silent-fallback rule.

## Classification

This is an `external_contract_slice` because it documents Claude Code CLI,
settings, MCP, SDK, and subagent behavior.

## Problem

Projects can run a rich orchestrator with many MCP/App connector tools, then
ask for "Claude Code as a subagent." Without a durable adapter rule, agents can
make two unsafe mistakes:

- launch Claude Code with inherited MCP or broad tools, multiplying processes
  and external surfaces;
- if Claude Code fails, silently switch to a GPT/Codex worker instead of
  diagnosing the Claude Code setup the operator explicitly requested.

One real failure mode observed on 2026-05-02: `claude -p --bare ...` failed
with `Not logged in` on an OAuth-backed local installation. The same local
Claude Code installation worked when run without `--bare` and with explicit
empty MCP config plus strict MCP enforcement.

## Goals

- Keep one model-agnostic engineering workflow.
- Treat Claude Code as an adapter under the same orchestrator/worker/reviewer
  canon.
- Make the default Claude Code worker one-shot and read-only.
- Disable MCP by configuration/CLI flags, not only by prompt text.
- Preserve OAuth-backed local Claude Code sessions by avoiding `--bare` unless
  API-key or `apiKeyHelper` mode is explicitly configured.
- Require root-cause diagnosis when the user explicitly requests Claude Code
  and Claude Code fails.

## Non-Goals

- Do not make Claude Code the default implementation worker for every project.
- Do not require every bootstrapped project to install or authenticate Claude
  Code.
- Do not grant Claude Code live services, production, GitHub writes, database
  writes, or messaging access by default.
- Do not store Anthropic API keys, Claude account state, or operator identity
  in repository files.

## External Source Of Truth Matrix

| Contract | Source | Verified fact | Kernel decision |
| --- | --- | --- | --- |
| Non-interactive CLI | Anthropic Claude Code CLI reference | `claude -p` / `--print` runs non-interactively; CLI supports `--mcp-config`, `--strict-mcp-config`, `--permission-mode`, `--settings`, and prompt input | Use CLI one-shot mode for worker/reviewer adapter runs |
| MCP isolation | Anthropic Claude Code CLI and MCP docs | Claude Code accepts MCP config and strict MCP config controls | Pass an explicit empty MCP config and strict MCP flag for no-MCP worker runs |
| Tool allowlist | Anthropic Claude Code SDK docs | SDK examples constrain agents with `allowed_tools`, including `Read`, `Glob`, and `Grep` | Default read-only Claude worker uses only `Read`, `Grep`, and `Glob` |
| Project subagents | Anthropic Claude Code subagents docs | Project agents can live under `.claude/agents/` and define tools/model/limits in frontmatter | Projects may add `.claude/agents/<project_slug>_readonly_reviewer.md` as an optional project-local Claude role |
| Settings and auth surfaces | Anthropic Claude Code settings docs | User/local/project settings and MCP configuration are separate surfaces | Do not store Claude auth secrets in project docs; run an auth health check before relying on Claude Code |

Sources checked with Tavily Search and Extract on 2026-05-02:

- https://docs.anthropic.com/en/docs/claude-code/cli-reference
- https://docs.anthropic.com/en/docs/claude-code/settings
- https://docs.anthropic.com/en/docs/claude-code/mcp
- https://docs.anthropic.com/en/docs/claude-code/sdk
- https://docs.anthropic.com/en/docs/claude-code/sub-agents

## Decision

Claude Code is a model adapter, not a second engineering process.

Default approved use:

- one-shot read-only reviewer or design-review worker;
- local repository context only;
- no MCP;
- no Bash/Edit/Write/MultiEdit by default;
- orchestrator performs external research and live-service operations, then
  passes evidence into the Claude Code prompt.

The canonical OAuth-backed local invocation shape is:

```bash
claude -p \
  --no-session-persistence \
  --mcp-config '{"mcpServers":{}}' \
  --strict-mcp-config \
  --tools 'Read,Grep,Glob' \
  --permission-mode dontAsk \
  --max-budget-usd "${CLAUDE_WORKER_MAX_BUDGET_USD:-2}" \
  "$prompt"
```

Rules:

- Do not add `--bare` to the default command. Use `--bare` only when the
  project/operator explicitly configured API-key or `apiKeyHelper` mode and
  verified it with a smoke test.
- The empty MCP config is `{"mcpServers":{}}`, not `{}`.
- If Claude Code fails auth, tool, MCP, permission, or process startup checks,
  stop and diagnose. Do not silently substitute a GPT/Codex worker when the
  operator explicitly asked for Claude Code.
- If fallback is needed, ask for explicit operator approval and record the
  adapter gap.
- Claude Code process exit ends the one-shot worker. There is no persistent
  thread to keep open.
- If Claude Code hangs, terminate that process, record partial evidence, and
  recover sequentially before retrying.

The default local worker budget guardrail is USD 2 per run:

```text
CLAUDE_WORKER_MAX_BUDGET_USD:-2
```

Projects may lower or raise that environment variable in local/operator
configuration, but should not hard-code billing credentials or account details
in the repository.

## Project Template Decision

Bootstrapped projects receive an optional helper:

```text
scripts/claude-code-readonly-subagent.sh
```

The helper:

- checks that `claude` exists;
- runs `claude auth status` as a health check;
- uses non-interactive `-p`;
- passes an explicit empty MCP config;
- enforces strict MCP config;
- allows only `Read,Grep,Glob`;
- requires a prompt argument;
- does not store or print secrets.

Projects can later add an optional Claude project subagent definition:

```text
.claude/agents/<project_slug>_readonly_reviewer.md
```

That file is project-specific and should not be generated blindly by the
universal bootstrap unless the project has decided to support Claude Code.

## Verification Plan

- Update machine-readable kernel policy.
- Update long-form references.
- Update project bootstrap templates.
- Add the helper script to the bootstrap file set.
- Add tests proving the bootstrap includes the helper and canon text.
- Run unit tests and diff whitespace checks.

## Rollback

- Remove the Claude Code adapter sections from kernel references and templates.
- Remove `scripts/claude-code-readonly-subagent.sh` from project templates.
- Leave the generic no-MCP worker canon unchanged.

## Kernel Impact

`promote_to_kernel`

This rule is reusable across repositories and prevents a repeated operator
failure mode: treating "Claude Code as subagent" as either an unconstrained
external process or a request that can be silently replaced by a different
agent family.
