# PRD: Agentic Coding Orchestration Canon

Date: 2026-04-27

Status: accepted

Last updated: 2026-04-27

## Purpose

This document defines the default engineering-kernel rules for orchestrated
agentic coding: one primary orchestrator coordinates focused coding workers,
reviewers, tests, docs, commits, and deployment checks.

The goal is not to maximize the number of agents. The goal is to preserve
correctness, reviewability, low resource pressure, and clean integration while
using extra coding agents only where they materially help.

## Source Notes

This canon is based on project experience plus upstream OpenAI guidance checked
on 2026-04-27:

- Codex delegated tasks run in isolated sandboxes/worktrees and produce code for
  human review, merge, or pull-down.
  Source: https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- Multi-agent architectures add nondeterminism and should be driven by observed
  need and evaluations, not by default fan-out.
  Source: https://platform.openai.com/docs/guides/evaluation-best-practices
- Tool/function calling accuracy improves when available tools are limited, and
  parallel calls can be disabled where deterministic behavior is more important.
  Source: https://platform.openai.com/docs/guides/function-calling

## Roles

### Orchestrator

The orchestrator is the single accountable engineering owner for the slice.

The orchestrator owns:

- problem framing and classification;
- research and source-of-truth matrix;
- implementation plan;
- subagent task boundaries;
- write-set isolation;
- review decisions;
- test selection and verification;
- runtime/staging/prod checks;
- docs and handoff;
- git commits, PRs, merges, and rollback notes.

The orchestrator must not delegate the immediate blocker on the critical path
when the next local decision depends on it. In that case the orchestrator does
the work locally.

### Worker Agents

Worker agents are coding hands. They receive a narrow task and an explicit
write set.

A worker must not:

- edit outside its allowed files;
- deploy;
- run production sends or destructive commands;
- print secrets, customer identifiers, chat IDs, tokens, credentials, or raw PII;
- revert changes made by others;
- silently expand scope.

A worker returns:

- status: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`;
- changed files;
- commands run;
- tests passed/failed;
- concerns and assumptions.

### Reviewer Agents

Reviewer agents are optional and targeted. They are not a replacement for the
orchestrator.

Use a reviewer agent for:

- security-sensitive code;
- database migrations;
- runtime/deploy scripts;
- privacy/logging changes;
- production integrations;
- broad multi-file changes.

Do not use reviewer agents by reflex for every small docs/test edit.

## Concurrency Rules

### Default

Default concurrency is one worker agent at a time.

The orchestrator may run two worker agents in parallel only when all of the
following are true:

- their write sets are disjoint;
- their test/runtime resources are disjoint;
- neither worker touches shared deployment scripts, shared fixtures, shared
  generated files, live state, or the same plan/doc section;
- the orchestrator can review and integrate both outputs without guessing;
- local executor health is normal.

Never run more than two implementation workers concurrently from one local
orchestrator session unless a project-specific canon explicitly raises the
limit and the environment has proven it can handle the load.

### Reviewer Limit

Run at most one reviewer agent at a time per slice unless the review questions
are demonstrably independent and no local shell/resource issue is present.

### Open Thread Limit

Keep at most three subagent threads open:

- one active worker;
- one optional active reviewer;
- one spare or recently completed thread.

Close completed or abandoned agents immediately after recording their result.
Do not accumulate completed threads during a long session.

## Tool And Shell Load Rules

Subagents consume resources. Shell tools consume resources. Parallel shell calls
consume resources faster.

While any worker agent is active:

- avoid `multi_tool_use.parallel`;
- prefer sequential `exec_command` calls;
- avoid broad `find`, large `rg`, or repeated file reads unless needed;
- do not launch background dev servers unless the task requires them;
- do not busy-poll agents.

Before spawning a worker:

```bash
git status --short --branch
```

After a worker returns:

```bash
git status --short --branch
git diff --check
```

If the local executor reports resource failures such as:

```text
Too many open files
stream disconnected before completion
failed to create process
```

then stop spawning agents, stop parallel shell calls, close completed agents,
and recover sequentially.

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

## Kernel Impact Guidance

Promote a local orchestration rule into this kernel only when it is:

- project-independent;
- repeated across at least one real workflow or incident;
- phrased as an actionable rule, not a chat anecdote;
- safe for future agents to follow without knowing the original conversation.
