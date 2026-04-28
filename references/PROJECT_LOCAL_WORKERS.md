# Project-Local Workers

Project-local workers are custom coding agents that live inside a repository
and carry that repository's operating rules. They are the preferred way to let a
rich orchestrator use MCP while keeping implementation workers lightweight and
free of inherited external tools.

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

## Pattern

Use three role layers:

1. Rich orchestrator.
   - May use MCP/App connectors for research, GitHub, browser, analytics,
     Telegram, or other external operations.
   - Owns scope, research, worker selection, integration, verification, docs,
     commits, live checks, and rollback notes.
2. Project-local code worker.
   - Lives in the repository.
   - Knows the project canon, forbidden live actions, privacy rules, and local
     verification commands.
   - Explicitly disables all known external MCP servers.
3. Global fallback code worker.
   - Lives in the operator's Codex home.
   - Contains universal no-MCP coding rules.
   - Used only when a project-local worker does not exist or the task is truly
     project-agnostic.

Reviewer agents follow the same principle: use no-MCP reviewer roles for normal
code quality/spec review, and reserve rich MCP or live-service tooling for the
orchestrator or a separate read-only research/review role with explicit scope.

Do not rely on prompt text alone to keep workers away from MCP. Worker prompts
are seen after the worker starts; MCP startup decisions happen before task
instructions matter. Disable MCP at the worker config layer.

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
Telegram, browser automation, analytics, GitHub connector writes, or another
external tool, return NEEDS_CONTEXT.
"""

[mcp_servers.exa]
command = "npx"
args = ["-y", "exa-mcp-server"]
enabled = false

[mcp_servers.tavily]
command = "node"
args = ["/Users/raketa23/Work/Vs/reserch/tavily-rotator/dist/index.js"]
enabled = false

[mcp_servers.chrome-devtools]
command = "npx"
args = ["-y", "chrome-devtools-mcp@latest", "--browser-url=http://127.0.0.1:9222", "--no-usage-statistics"]
enabled = false

[mcp_servers.telegram-mcp]
command = "/Users/raketa23/.codex/bin/start-telegram-mcp.sh"
enabled = false

[mcp_servers."analytics-mcp"]
command = "/Users/raketa23/.local/bin/analytics-mcp"
enabled = false

[mcp_servers.codeberg]
command = "/Users/raketa23/.codex/bin/start-codeberg-mcp.sh"
enabled = false
```

Add additional known MCP server ids used on the operator machine. Unknown MCP
servers cannot be disabled by a worker config until their ids are known, so keep
the list current when new MCP servers are installed.

Each disabled MCP entry still needs a valid transport definition (`command` for
stdio or `url` for HTTP). Do not write only `enabled = false`; Codex may reject
the custom agent file as `invalid transport`.

## Project-Local Worker

Each serious project should define its own code worker. Use the project's slug
in the name:

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

Do not use MCP servers. If the task needs external research, Telegram, browser
automation, analytics, GitHub connector writes, or live runtime access, return
NEEDS_CONTEXT and let the orchestrator handle it.

You are not alone in the codebase. Do not revert edits made by others. Adapt to
current files, run only assigned local checks, and return changed files,
commands run, and concerns.
"""

[mcp_servers.exa]
command = "npx"
args = ["-y", "exa-mcp-server"]
enabled = false

[mcp_servers.tavily]
command = "node"
args = ["/Users/raketa23/Work/Vs/reserch/tavily-rotator/dist/index.js"]
enabled = false

[mcp_servers.chrome-devtools]
command = "npx"
args = ["-y", "chrome-devtools-mcp@latest", "--browser-url=http://127.0.0.1:9222", "--no-usage-statistics"]
enabled = false

[mcp_servers.telegram-mcp]
command = "/Users/raketa23/.codex/bin/start-telegram-mcp.sh"
enabled = false

[mcp_servers."analytics-mcp"]
command = "/Users/raketa23/.local/bin/analytics-mcp"
enabled = false

[mcp_servers.codeberg]
command = "/Users/raketa23/.codex/bin/start-codeberg-mcp.sh"
enabled = false
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

## What To Put In The Project Worker

The project-local worker should include only durable project rules:

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

Use this knowledge ladder:

1. Worker TOML: role, MCP policy, hard prohibitions, privacy rules, and where
   to find project truth.
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

The orchestrator chooses workers explicitly:

- Use `<project_slug>_code_worker` for project implementation/docs changes.
- Use `code_worker_no_mcp` only as fallback when the project-local worker is
  unavailable or the task is project-agnostic.
- Use a separate research role only for read-only external-source work.
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
