# Agentic Coding Orchestration

This reference defines the default kernel rules for orchestrated agentic coding:
one primary orchestrator coordinates focused coding workers, review agents,
tests, docs, commits, and deployment checks.

The goal is not to maximize the number of agents. The goal is to preserve
correctness, reviewability, low resource pressure, and clean integration while
using extra coding agents only where they materially help.

## Upstream Research Notes

Checked on 2026-04-27:

- Codex delegated tasks run in isolated sandboxes/worktrees and produce code for
  review, merge, or pull-down:
  https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- Multi-agent architectures add nondeterminism and should be driven by observed
  need and evaluations:
  https://platform.openai.com/docs/guides/evaluation-best-practices
- Tool/function calling guidance recommends keeping the active tool surface
  small and disabling parallel calls when deterministic behavior matters:
  https://platform.openai.com/docs/guides/function-calling
- Codex custom subagents can be defined in `.codex/agents/*.toml`, and MCP
  servers can be disabled per config with `enabled = false`:
  https://developers.openai.com/codex/subagents
  https://developers.openai.com/codex/mcp

Checked on 2026-05-02:

- Claude Code CLI supports non-interactive print mode, MCP config, and strict
  MCP config:
  https://docs.anthropic.com/en/docs/claude-code/cli-reference
- Claude Code CLI supports stream JSON output, verbose output, explicit
  permission mode, tool allowlists, and max budget controls:
  https://docs.anthropic.com/en/docs/claude-code/cli-reference
- Claude Code SDK examples support constrained `allowed_tools`, including
  read-only `Read`, `Glob`, and `Grep`:
  https://docs.anthropic.com/en/docs/claude-code/sdk
- Claude Code project subagents can live in `.claude/agents/` and define tool
  and runtime limits in frontmatter:
  https://docs.anthropic.com/en/docs/claude-code/sub-agents

## Roles

The orchestrator is the single accountable engineering owner for the slice.

The orchestrator owns:

- problem framing and slice classification;
- research and source-of-truth matrix;
- implementation plan;
- subagent task boundaries;
- write-set isolation;
- review decisions;
- test selection and verification;
- runtime, staging, and production checks;
- docs, handoff, commits, PRs, merges, and rollback notes.

Worker agents are coding hands. They receive a narrow task and an explicit
write set. They must not deploy, run production sends, print secrets or PII,
edit outside scope, revert others' changes, or silently expand scope.

Coding workers should be project-local no-MCP workers whenever the platform
supports custom agents. A rich orchestrator may use MCP/App connectors for
research, GitHub, browser, analytics, messaging, or other external operations,
but implementation workers should not inherit that tool surface by default.

Use this role order:

1. Project-local worker, such as `<project_slug>_code_worker`, for project
   implementation and documentation changes.
2. Global fallback worker, such as `code_worker_no_mcp`, only when the
   project-local worker is unavailable or the task is truly project-agnostic.
3. Built-in generic workers only when no no-MCP worker exists or when the
   orchestrator is already running in a deliberately lightweight session.

Project-local workers live in `.codex/agents/*.toml` and should explicitly set
the project's or operator's MCP server ids to `enabled = false`. The universal
kernel does not prescribe a fixed MCP list; each project copies its own server
ids and valid transport fields from the local MCP configuration. See
`references/PROJECT_LOCAL_WORKERS.md` for the full setup pattern.

Claude Code may be used as an external subagent adapter under the same role
model. The default Claude Code adapter role is one-shot, read-only review or
design review, not implementation. It should be launched with explicit empty
MCP config, strict MCP enforcement, a small read-only tool allowlist,
observable stream output, explicit non-plan permission mode, and a budget cap.
If the operator explicitly requested Claude Code and the launch fails,
diagnose the Claude Code CLI/auth/MCP/tool/output/binary configuration before
using another agent family.

Use Claude Code where second-model perspective has high leverage: UI/UX
architecture, operator workflows, PRD/spec/runbook cleanup, independent
plan/diff review, test planning, and refactor-boundary advice. The default
enabled modes are `design_readonly` and `review_readonly`. Treat
`implementation_no_mcp` and `research_mcp_readonly` as separate PRD-gated
adapter slices. Do not pass the whole repository or huge files by habit. Build
a context packet first: goal, exact question, relevant symbols or interfaces,
error evidence, focused snippets or excerpted sections, and selected diff
context when reviewing changes.

Reviewer and specialist agents are optional and targeted. Start a project with
one project-local code worker, then add roles only when repeated work creates a
clear boundary. Common useful additions are a read-only reviewer and a
docs-only worker. Use reviewers for security-sensitive code, database
migrations, runtime/deploy scripts, privacy/logging changes, production
integrations, and broad multi-file changes. Use docs workers for handoff,
runbook, README, PRD closeout, and rollback-note writing from evidence the
orchestrator already collected. Do not add specialist agents by reflex for
every small docs/test edit.

## Concurrency Rules

Default concurrency is one worker agent at a time.

Two worker agents may run in parallel only when all of these are true:

- their write sets are disjoint;
- their tests and runtime resources are disjoint;
- neither worker touches shared deploy scripts, shared fixtures, generated
  files, live state, or the same plan/doc section;
- the orchestrator can review and integrate both outputs without guessing;
- local executor health is normal.

Never run more than two implementation workers concurrently from one local
orchestrator session unless a project-local canon explicitly raises the limit
and the environment has already proven it can handle the load.

Run at most one reviewer agent at a time per slice unless the review questions
are demonstrably independent and no local shell/resource issue is present.

Keep at most three subagent threads open:

- one active worker;
- one optional active reviewer;
- one spare or recently completed thread.

Close completed or abandoned agents immediately after recording their result.

## Thread Lifecycle Rules

Do not keep subagent threads open for memory. Keep them open only while the
same bounded task still needs the same thread.

Implementation workers may stay open through their own review/fix loop:

- worker returns a patch or red-state report;
- orchestrator inspects the diff and runs the required post-worker checks;
- optional reviewer finds a concrete issue in that same patch;
- orchestrator asks the same worker to fix the issue only if the write set,
  task boundary, and file state are still the same.

Close an implementation worker immediately after any of these happen:

- the patch is accepted or rejected;
- the orchestrator takes over the fix locally;
- the next task has a different write set or different PRD slice;
- the worker returns `NEEDS_CONTEXT` or `BLOCKED` and the answer was recorded;
- executor health degrades and recovery mode begins.

Reviewer, explorer, and docs-specialist threads are single-use by default.
Record their result, then close the thread. After a fix, spawn a fresh reviewer
with the current diff and context instead of preserving the old reviewer
thread.

Every subagent final response should include thread disposition:

```text
thread_disposition:
- parent_may_close_thread
- keep_open_for_same_patch_fix_loop
- blocked_needs_context
```

If the disposition is not explicitly `keep_open_for_same_patch_fix_loop`, the
orchestrator should close the thread after recording the result.

## Tool And Shell Load Rules

While any worker agent is active:

- avoid parallel shell/tool wrappers;
- prefer sequential shell commands;
- avoid broad repeated file scans unless needed;
- do not launch background services unless required;
- do not busy-poll agents.

Regardless of whether worker agents are active, git commands that touch refs,
the index, or the working tree are serialized per repository. Do not run `git
fetch`, `git pull`, `git switch`, `git checkout`, `git merge`, `git rebase`,
`git branch -d/-D`, or `git push` through parallel shell/tool wrappers for the
same repo. They can race on `.git/refs` lock files or leave the operator with a
misleading local view. If this happens, stop parallel git calls and recover with
sequential `git status --short --branch`, the needed `git fetch`, `git pull
--ff-only` when appropriate, and `git diff --check`.

Worker MCP policy:

- do not rely on the task prompt to disable MCP; MCP startup happens before the
  worker can follow prompt instructions;
- disable the current project/operator MCP server ids at the worker config
  layer for coding workers;
- for Claude Code one-shot workers, pass an explicit empty MCP config and
  strict MCP flag at launch time;
- if a coding worker needs external research or a live service, it returns
  `NEEDS_CONTEXT` and the orchestrator performs that step;
- keep rich-MCP sessions for orchestrators and read-only research agents, not
  implementation workers.

Claude Code one-shot lifecycle:

- choose `design_readonly` for plan/spec/architecture/UX output, or
  `review_readonly` for findings against a brief, selected files, or a diff;
- before handing Claude Code a huge file, prepare a context packet with focused
  snippets or exact symbol/interface excerpts; whole large files are opt-in
  only when full-file context is truly required;
- do not use `implementation_no_mcp` or `research_mcp_readonly` without a
  separate active PRD defining surface, identity, verification, and rollback;
- run non-interactively with `claude -p`;
- prefer the direct Claude Code binary over wrapper binaries; wrapper binaries
  such as cmux are explicit opt-in only;
- pin the controlled review model, defaulting to `claude-opus-4-7` unless the
  operator sets `CLAUDE_CODE_MODEL`;
- avoid `--bare` for OAuth-backed local Claude Code sessions unless API-key or
  `apiKeyHelper` mode was explicitly configured and smoke-tested;
- recognize that non-`--bare` OAuth mode can still load user hooks/settings;
  if hook-free execution is required, configure and smoke-test `--bare`;
- use `--mcp-config '{"mcpServers":{}}'` and `--strict-mcp-config`;
- use `--output-format stream-json --verbose` for observable review runs;
- use explicit `--permission-mode dontAsk`; do not use `plan` for read-only
  workers because plan mode can write plan files outside the repository;
- use no tools for smoke, `Read` for exact-file review, and
  `Read,Grep,Glob` only when repo search is required;
- default budget caps are USD 1 for smoke, USD 5 for exact-file review, and
  USD 10 for repo-search review unless the operator overrides them;
- treat process exit as the end of the subagent thread;
- if it hangs, terminate the process, record partial evidence, and recover
  sequentially before retrying;
- do not silently replace it with another worker family when the user asked
  for Claude Code.

Before spawning a worker:

```bash
git status --short --branch
```

After a worker returns:

```bash
git status --short --branch
git diff --check
```

If the local executor reports resource failures such as `Too many open files`,
`stream disconnected before completion`, or failed process creation, stop
spawning agents, stop parallel shell calls, close completed agents, and recover
sequentially.

## Agent Task Contract

Every worker prompt must include:

- repository/worktree path;
- branch name;
- task goal;
- exact allowed write paths;
- explicit forbidden paths/actions;
- whether live systems may be touched;
- secret/privacy rules;
- verification commands;
- expected return format.

Use this shape:

```text
You are Worker N for <project/slice>.

Worktree: <absolute path>
Branch: <branch>
Plan/PRD: <path>

You are not alone in the codebase. Do not revert edits made by others.
Do not deploy. Do not contact live services. Do not print secrets or PII.

Allowed write paths:
- <path>

Forbidden:
- <path/action>

Task:
1. <specific step>
2. <specific step>

Run:
- <command>

Return:
- DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED
- changed files
- commands run
- concerns
- thread_disposition: parent_may_close_thread / keep_open_for_same_patch_fix_loop / blocked_needs_context
```

## Integration Rules

The orchestrator integrates only after checking:

- changed files are within the allowed write set;
- no secrets or raw customer data were introduced;
- `git diff --check` passes;
- focused tests pass or expected red-state is documented;
- review findings are resolved or explicitly rejected with technical reasoning.

Commit after each accepted slice when feasible. Small, reviewed commits are
easier to revert than a large mixed agent patch.

## Review Rules

Use two review modes:

- spec compliance: did the implementation do exactly what the plan/PRD asked;
- code quality: is the implementation maintainable, safe, testable, and
  consistent with the project.

External reviewer feedback is evaluated, not blindly obeyed. If a reviewer
flags an expected TDD red-state as a bug, the orchestrator records that as
intentional and addresses only the technically valid part.

## Recovery Protocol

When executor/resource failure occurs:

1. Stop spawning agents.
2. Close completed or errored agent threads.
3. Stop parallel shell use.
4. Try a minimal sequential command:

   ```bash
   true
   git status --short --branch
   ```

5. If shell still cannot start, do not edit runtime code and do not claim
   verification.
6. If a docs-only patch is necessary, state that verification/commit is blocked
   by executor health and complete it later.
7. Resume only after `git status` and `git diff --check` can run.

## Project Override Rule

Project-local `AGENTS.md` may impose stricter limits. Project-local limits win
over this kernel document.

Projects with live production surfaces should default to stricter rules:

- one worker at a time;
- staging-first;
- no live deploys by workers;
- all runtime verification by the orchestrator.

## Promotion Rule

Promote a local orchestration rule into this kernel only when it is:

- project-independent;
- repeated across at least one real workflow or incident;
- phrased as an actionable rule, not a chat anecdote;
- safe for future agents to follow without knowing the original conversation.
