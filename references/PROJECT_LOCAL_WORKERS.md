# Project-Local Workers

Project-local workers are custom agents that live inside a repository and carry
that repository's operating rules. They are the preferred way to let a rich
orchestrator use MCP while keeping implementation, review, and documentation
workers lightweight and free of inherited external tools.

## Upstream Research Notes

Checked on 2026-04-27:

- Codex subagents can be defined as custom agents in `.codex/agents/*.toml`,
  and a project-level `.codex/config.toml` can register project agents:
  https://developers.openai.com/codex/subagents
- Codex MCP config supports `enabled = false` to disable a server without
  deleting the server definition:
  https://developers.openai.com/codex/mcp
- Codex config reference documents app/MCP enablement controls and managed MCP
  allowlist behavior:
  https://developers.openai.com/codex/config-reference

Checked on 2026-05-02:

- Claude Code CLI supports non-interactive print mode, `--mcp-config`, and
  `--strict-mcp-config`:
  https://docs.anthropic.com/en/docs/claude-code/cli-reference
- Claude Code CLI supports `--output-format stream-json`, `--verbose`,
  `--permission-mode`, `--max-budget-usd`, `--tools`,
  `--disable-slash-commands`, and `--no-chrome`:
  https://docs.anthropic.com/en/docs/claude-code/cli-reference
- Claude Code settings and MCP configuration are separate local/project
  surfaces and must not be treated as repository secrets:
  https://docs.anthropic.com/en/docs/claude-code/settings
  https://docs.anthropic.com/en/docs/claude-code/mcp
- Claude Code SDK examples support constrained read-only tool allowlists:
  https://docs.anthropic.com/en/docs/claude-code/sdk
- Claude Code project subagents can be described under `.claude/agents/` with
  frontmatter-defined tools and limits:
  https://docs.anthropic.com/en/docs/claude-code/sub-agents

## Pattern

Use four role layers:

1. Rich orchestrator.
   - May use MCP/App connectors for research, GitHub, browser, analytics,
     messaging, or other external operations.
   - Owns scope, research, worker selection, integration, verification, docs,
     commits, live checks, and rollback notes.
2. Project-local code worker.
   - Lives in the repository.
   - Knows the project canon, forbidden live actions, privacy rules, and local
     verification commands.
   - Explicitly disables the MCP server ids that exist in the current project
     or operator environment.
3. Optional project-local specialist workers.
   - Added only when the project repeatedly needs that role.
   - Common useful roles are read-only reviewer and documentation worker.
   - They follow the same no-MCP and project-canon rules as the code worker.
4. Global fallback code worker.
   - Lives in the operator's Codex home.
   - Contains universal no-MCP coding rules.
   - Used only when a project-local worker does not exist or the task is truly
     project-agnostic.

Reviewer and docs agents follow the same principle: use no-MCP project-local
roles for normal review and closeout writing, and reserve rich MCP or
live-service tooling for the orchestrator or a separate explicitly scoped
read-only research/review role.

Do not rely on prompt text alone to keep workers away from MCP. Worker prompts
are seen after the worker starts; MCP startup decisions happen before task
instructions matter. Disable MCP at the worker config layer.

The universal kernel does not prescribe a fixed MCP server list. Do not copy
another project's MCP ids or local command paths into a new project. Each
project should inspect its own configured MCP/App connector surface, decide
which ids must be unavailable to workers, and put those ids in the project or
global worker config with valid transport fields and `enabled = false`.

## Role Lifecycle

Do not start a new project with a zoo of agents. Start with one project-local
code worker:

```text
<project_slug>_code_worker
```

Add more project-local roles only when the work pattern is repeated and the
boundary is clear:

- add `<project_slug>_reviewer` when independent read-only reviews regularly
  catch meaningful spec, safety, privacy, runtime, or test gaps;
- add `<project_slug>_docs_worker` when handoff, runbook, README, or closeout
  writing is frequent enough to justify a separate docs-only role;
- add narrowly scoped roles such as `<project_slug>_frontend_worker` only when
  the project has a sustained specialty surface and a distinct rule set;
- do not add live-service, deployment, production database, messaging broadcast,
  or generic research workers by default.

Each role differs in its own TOML file: role identity, allowed work type,
forbidden actions, privacy rules, MCP policy, and response format. The
orchestrator still supplies the current task: exact write set, forbidden paths,
evidence to use, checks to run, and return format. The TOML is the durable
guardrail; the dispatch prompt is the per-task contract.

## Files

Global fallback:

```text
~/.codex/agents/code_worker_no_mcp.toml
```

Project-local registration:

```text
<repo>/.codex/config.toml
```

Project-local worker:

```text
<repo>/.codex/agents/<project_slug>_code_worker.toml
```

Optional project-local specialist workers:

```text
<repo>/.codex/agents/<project_slug>_reviewer.toml
<repo>/.codex/agents/<project_slug>_docs_worker.toml
```

Optional Claude Code project subagent:

```text
<repo>/.claude/agents/<project_slug>_readonly_reviewer.md
```

Optional Claude Code one-shot wrapper:

```text
<repo>/scripts/claude-code-readonly-subagent.sh
```

Project canon:

```text
<repo>/AGENTS.md
```

## Global Fallback Worker

Create this once per operator machine:

```toml
name = "code_worker_no_mcp"
description = "Universal implementation worker for scoped coding tasks that do not need external MCP services."
model = "gpt-5.5"
model_reasoning_effort = "medium"

developer_instructions = """
You are a coding worker, not an orchestrator.

Work only inside the repository and exact file scope assigned by the parent
agent. Do not deploy, contact live production services, run mass sends, print
secrets, or change files outside the assigned write set.

Do not use MCP servers. If a task needs external research, live service access,
messaging, browser automation, analytics, GitHub connector writes, or another
external tool, return NEEDS_CONTEXT.

In the final response, include `thread_disposition`. Use
`parent_may_close_thread` unless the parent explicitly needs this same thread
for the same-patch fix loop.
"""

# Add one [mcp_servers."<server_id_from_your_config>"] block for each MCP
# server id that exists in this operator/project environment and must be
# unavailable to this worker. Use the real transport fields from that MCP
# server's config, then set enabled = false.
```

Replace the example MCP block with the MCP server ids that are actually
configured on the operator machine. Unknown MCP servers cannot be disabled by a
worker config until their ids are known, so keep the list current when new MCP
servers are installed.

Each disabled MCP entry still needs a valid transport definition (`command` for
stdio or `url` for HTTP). Do not write only `enabled = false`; Codex may reject
the custom agent file as `invalid transport`.

Generic stdio pattern:

```toml
[mcp_servers."<server_id_from_your_config>"]
command = "<same command used by that MCP server>"
args = ["<same args, if any>"]
enabled = false
```

Generic HTTP pattern:

```toml
[mcp_servers."<http_server_id_from_your_config>"]
url = "https://example.invalid/mcp"
enabled = false
```

## Project-Local Code Worker

Each serious project should define its own code worker first. Use the project's
slug in the name:

```text
<project_slug>_code_worker
```

Example:

```toml
name = "project_code_worker"
description = "Project-local implementation worker without MCP."
model = "gpt-5.5"
model_reasoning_effort = "medium"

developer_instructions = """
You are a project-local coding worker, not the orchestrator.

Follow AGENTS.md and the active plan/PRD supplied by the parent agent. Work
only inside the exact allowed write paths. Do not deploy, mutate live systems,
print secrets, print customer PII, or edit outside scope.

Do not use MCP servers. If the task needs external research, messaging, browser
automation, analytics, GitHub connector writes, or live runtime access, return
NEEDS_CONTEXT and let the orchestrator handle it.

You are not alone in the codebase. Do not revert edits made by others. Adapt to
current files, run only assigned local checks, and return changed files,
commands run, concerns, and `thread_disposition`.

Set `thread_disposition` to:
- `parent_may_close_thread` when the assigned task is done, blocked, or handed
  back to the parent;
- `keep_open_for_same_patch_fix_loop` only when you expect the parent to send a
  follow-up fix request for this same patch and write set;
- `blocked_needs_context` when external context or live access is required.
"""

# Add one [mcp_servers."<server_id_from_your_config>"] block for each MCP
# server id that exists in this operator/project environment and must be
# unavailable to this worker. Use the real transport fields from that MCP
# server's config, then set enabled = false.
```

Then register it in project `.codex/config.toml`:

```toml
[agents]
max_threads = 3
max_depth = 1

[agents.project_code_worker]
config_file = "agents/project_code_worker.toml"
description = "Project-local implementation worker without MCP."
```

## Optional Project-Local Specialist Roles

Add specialist roles only after the project proves the need. Keep them
no-MCP, small, and scoped.

Recommended starter extensions:

```text
<project_slug>_reviewer
```

Use for read-only review of assigned diffs, specs, security/privacy risks,
runtime blast radius, and test gaps. The reviewer should not edit files or run
live checks. It returns findings, open questions, verification gaps, and a
blocking/approved summary.

```text
<project_slug>_docs_worker
```

Use for assigned documentation paths only: handoff, runbook, README, PRD
closeout, canon updates, and rollback notes. The docs worker writes from
evidence supplied by the orchestrator and project docs. It must not invent live
verification, deployment status, customer counts, or production state.

Avoid these default roles:

- deployment worker;
- production database worker;
- messaging or mass-broadcast worker;
- cleanup worker for customer or subscriber data;
- broad research worker with inherited external tools.

Those surfaces stay with the orchestrator unless a project explicitly designs a
separate audited, read-only, sandboxed role for one narrow operation.

## Claude Code Read-Only Subagent Adapter

Claude Code is an external model adapter under this same worker canon. It does
not create a second engineering workflow.

Use Claude Code by default only for:

- read-only review of an existing diff;
- UI/UX architecture, operator workflows, mobile/desktop layout, and
  design-system decisions from repository files and evidence supplied by the
  orchestrator;
- PRD, spec, runbook, closeout, and handoff drafting or cleanup;
- independent review of an orchestrator plan or diff for missed UX, tests,
  privacy issues, and edge cases;
- test planning before implementation;
- refactor-boundary advice before splitting large files or workflows;
- small, bounded comparison of project docs, plans, or code paths.

Do not use the default Claude Code adapter for:

- implementation edits;
- live service access;
- production/staging operations;
- database writes or migrations;
- GitHub issue/PR writes;
- messaging sends;
- customer data export;
- external research unless a separate research role is explicitly designed.

Canonical Claude Code operating modes:

| Mode | Default status | Surface | Output |
| --- | --- | --- | --- |
| `design_readonly` | enabled by the read-only wrapper | `Read`, empty strict MCP, no edits | plan, spec, architecture, UX/workflow notes |
| `review_readonly` | enabled by the read-only wrapper | selected files or diff context, optionally `Read,Grep,Glob`, empty strict MCP, no edits | findings: risks, missing tests, UX/privacy issues, edge cases |
| `implementation_no_mcp` | separate active PRD required | exact allowed write paths, no MCP, no live systems, no secrets, no deploys, explicit verification | patch plus verification evidence |
| `research_mcp_readonly` | separate active PRD required | explicit read-only identity and allowed external sources/tools | cited evidence and assumptions, no mutating provider actions |

Do not feed Claude Code the whole repository by habit. Prefer a brief,
selected files, and selected diff context. Large generated/type files are
allowed only when directly relevant to the question.

The canonical observable one-shot command for an OAuth-backed local Claude
Code install is:

```bash
"${CLAUDE_CODE_BIN:-$HOME/.local/bin/claude}" -p \
  --model "${CLAUDE_CODE_MODEL:-claude-opus-4-7}" \
  --no-session-persistence \
  --output-format stream-json \
  --verbose \
  --mcp-config '{"mcpServers":{}}' \
  --strict-mcp-config \
  --tools 'Read' \
  --permission-mode dontAsk \
  --disable-slash-commands \
  --no-chrome \
  --max-budget-usd "${CLAUDE_WORKER_MAX_BUDGET_USD:-5}" \
  "$prompt"
```

Use the project helper when available:

```bash
scripts/claude-code-readonly-subagent.sh "$prompt"
```

Important details:

- prefer a direct Claude Code binary such as `$HOME/.local/bin/claude`; wrapper
  binaries such as cmux are explicit opt-in because they may add hooks or
  workspace behavior;
- pin the intended model for controlled runs; default to `claude-opus-4-7`
  unless the operator sets `CLAUDE_CODE_MODEL`;
- the empty MCP config is `{"mcpServers":{}}`, not `{}`;
- do not use `--bare` by default for OAuth-backed local sessions;
- use `--bare` only when API-key or `apiKeyHelper` mode is explicitly
  configured and smoke-tested;
- non-`--bare` OAuth mode can still load user settings, hooks, agents, skills,
  and memory surfaces; for the read-only adapter this is acceptable only when
  MCP and tools are explicitly restricted;
- long runs use `--output-format stream-json --verbose` so the orchestrator
  can see progress and stop the process deliberately;
- do not use `--permission-mode plan` for read-only workers because it can
  invoke Claude Code plan-file workflow outside the repository;
- keep `--permission-mode dontAsk` explicit so local settings do not widen the
  runtime mode;
- keep `--tools` as narrow as possible:
  - `smoke`: no tools;
  - `review-files`: `Read`;
  - `review-repo`: `Read,Grep,Glob`;
- keep mode-specific budget caps unless the operator sets
  `CLAUDE_WORKER_MAX_BUDGET_USD` for that environment:
  - `smoke`: USD 1;
  - `review-files`: USD 5;
  - `review-repo`: USD 10;
- treat the budget as a runaway guardrail, not as a target spend; normal
  controlled Opus 4.7 reviews may cost less than the cap, but the cap should be
  high enough for useful work;
- do not put Anthropic API keys, auth state, or operator account details in the
  repository;
- run `claude auth status` or the project wrapper health check before relying
  on the worker.

If the user explicitly requests Claude Code and Claude Code fails, stop and
diagnose:

- CLI missing;
- auth unhealthy;
- wrong auth mode, such as `--bare` with an OAuth-only local install;
- wrapper binary behavior, such as cmux hooks;
- invalid MCP config;
- missing `--verbose` with `--output-format stream-json`;
- forbidden `plan` permission mode;
- tool permission mismatch;
- process hang or resource exhaustion.

Do not silently switch to GPT/Codex or another agent family. Fallback requires
explicit operator approval and a recorded adapter gap.

An optional project-local Claude subagent file can document the role for Claude
Code users:

```markdown
---
name: <project_slug>_readonly_reviewer
description: Read-only project reviewer. No MCP, no edits, no live systems.
tools: Read, Grep, Glob
---

You are a read-only reviewer for this repository.

Follow AGENTS.md and the active PRD supplied by the orchestrator. Do not edit
files, run live checks, deploy, print secrets, or access customer data. If the
task needs external research or live context, return NEEDS_CONTEXT.

Return findings, open questions, verification gaps, and:
thread_disposition: parent_may_close_thread
```

Project subagent files are optional because not every project uses Claude
Code. The universal bootstrap includes only the shell wrapper and canon text.

## Thread Lifecycle

Project-local worker threads are disposable execution contexts, not durable
memory stores. The durable memory is the repo: PRDs, plans, handoffs, commits,
tests, and review notes.

Keep an implementation worker open only while it is in the same-patch
review/fix loop. Close it after the patch is accepted, rejected, taken over by
the orchestrator, blocked, or moved to a new write set.

Reviewer and explorer threads are one-shot by default. Close them immediately
after recording their findings, and use a fresh reviewer for re-review after
fixes.

Claude Code `claude -p` adapter runs are process-based one-shot workers. When
the process exits, the worker is closed. If a Claude Code process hangs, kill
that process, record the partial result, and recover sequentially before
retrying.

Every project worker and specialist should end with a `thread_disposition`
field so the orchestrator does not have to remember whether the thread can be
closed.

## What To Put In The Project Worker

The project-local worker config should include only durable project rules:

- where the canonical project rules live, usually `AGENTS.md`;
- whether live systems may be touched;
- forbidden actions such as deploys, database writes, broadcasts, customer-data
  export, or production-provider operations;
- privacy rules: no secrets, tokens, raw customer data, chat ids, phone
  numbers, or credentials in chat/docs/git;
- local verification commands the worker may run;
- how to respond when external context is needed.

Do not put secrets, host credentials, token values, customer identifiers, or
temporary chat-memory-only details in the worker config.

Keep the worker config small. It is the worker's durable role and guardrail, not
the whole project manual.

Use this knowledge ladder for every project-local role:

1. Worker TOML: role identity, allowed work type, MCP policy, hard
   prohibitions, privacy rules, and where to find project truth.
2. `AGENTS.md`: project canon, workflow order, live-system rules, verification
   expectations, and source-of-truth priority.
3. Repo-local skills, runbooks, handoffs, and README files: domain knowledge
   for a specific subsystem.
4. Active PRD/plan: current slice truth.
5. Orchestrator prompt: exact write set, forbidden paths/actions, checks, and
   return format.

The project worker may contain short domain pointers such as:

```text
Use repo-local skills/runbooks/README files when the task names that subsystem.
If the task references billing, read docs/billing/README.md.
If the task references deploy scripts, read docs/deploy/RUNBOOK.md.
```

Avoid copying long runbooks into the worker config. Put long-lived domain
knowledge in project docs or skills, then point the worker at those files.

## Selection Rules

The orchestrator chooses workers explicitly. It does not expect workers to
self-route after launch:

- Use `<project_slug>_code_worker` for scoped implementation changes and small
  docs updates that are part of the same code slice.
- Use `<project_slug>_reviewer` for read-only review of an existing diff,
  broad safety/privacy/runtime risk review, or a spec-compliance check.
- Use `<project_slug>_docs_worker` for documentation-only closeout work when
  the facts and evidence are already available.
- Use `code_worker_no_mcp` only as fallback when the project-local worker is
  unavailable or the task is project-agnostic.
- Keep research, live runtime, provider consoles, messaging sends, deployment,
  and production operations with the orchestrator unless a project-specific
  audited role has been explicitly designed.
- Use a separate research role only for read-only external-source work with a
  narrow scope and explicit tool policy.
- Do not use built-in generic workers from a rich-MCP session for project
  implementation when a project-local no-MCP worker exists.

Multiple instances of the same project-local worker are allowed, but only when
write sets and verification resources are disjoint. The kernel default remains
one worker at a time and at most two parallel implementation workers.

## Prompt Contract

Even with a project-local worker, every dispatch prompt still includes:

- repository/worktree path;
- branch name;
- active plan/PRD path;
- task-specific project docs, skills, runbooks, or handoff files to read;
- exact allowed write paths;
- exact forbidden paths/actions;
- live-system access rule;
- secret/privacy rule;
- verification commands;
- return format.

The worker config is not a replacement for a scoped task prompt. It is the
baseline guardrail that prevents accidental MCP inheritance and makes project
rules durable.

## Verification

Before relying on the setup:

```bash
python3 - <<'PY'
import pathlib, tomllib
for path in [
    pathlib.Path.home() / ".codex/agents/code_worker_no_mcp.toml",
    pathlib.Path(".codex/config.toml"),
    pathlib.Path(".codex/agents/project_code_worker.toml"),
]:
    if path.exists():
        tomllib.loads(path.read_text())
        print(f"toml_ok={path}")
PY
```

Then start a fresh Codex session and confirm only the intended MCP servers start
for the orchestrator. Spawn workers only after the project-local worker is
available in the agent list for the running surface.

If a worker launch causes `Too many open files`, stream disconnects, or failed
process creation, stop spawning workers and recover sequentially:

```bash
true
git status --short --branch
git diff --check
```

Resume workers only after shell health is restored and completed agent threads
are closed.

## Rollback

Rollback is configuration-only:

- remove or rename `.codex/agents/<project_slug>_code_worker.toml`;
- remove its registration from `.codex/config.toml`;
- fall back to inline execution or the global `code_worker_no_mcp`.

Do not delete global MCP server definitions to reduce worker load. Disable MCP
in the worker config instead.
