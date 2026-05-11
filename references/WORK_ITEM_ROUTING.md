# Work Item Routing

Use this before creating, moving, or updating durable work items such as GitHub
Issues, project tasks, backlog rows, or cross-repo follow-up tasks.

The rule is simple: the work item lives where the work happens, not where the
agent happens to be running.

## Canonical Decision

Record routing in the active PRD, issue body, or closeout when the target is not
obvious:

```text
Work Item Routing: <target repo or project-local surface> | ambiguous | not_applicable
```

Use:

- a concrete target when the project-local routing rules identify one;
- `ambiguous` when no routing rule matches and the user or maintainer must pick;
- `not_applicable` when no durable work item is being created or moved.

## Rules

- identify the target repository or project-local surface before creating the
  issue;
- never default to the current checkout, current worktree, or current terminal
  directory as the target repository;
- match by task domain, affected system, owner, and source-of-truth path;
- search duplicates in the target surface before create;
- if multiple targets match, choose the most specific target or ask;
- if no routing rule exists, ask or record `ambiguous` instead of guessing;
- keep routing maps project-local, usually in `AGENTS.md`, repo canon, or a
  small project-local routing table;
- do not make GitHub Projects or weekly labels mandatory just to route work.

## Minimum Routing Table

Project-local canon may define:

```markdown
## Work Item Routing

| Pattern / surface | Target repo or tracker | Owner | Notes |
|---|---|---|---|
| backend API, migrations | owner/api-repo | platform | Runtime code lives here |
| docs, runbooks | owner/docs-repo | docs | Durable docs live here |
| strategy, cross-cutting | owner/planning-repo | operator | No runtime code |
```

This table is optional, but when it exists the agent must use it before issue
creation.

## Duplicate Search

Search the target surface first. If a possible match exists, update or link the
existing work item instead of creating another one.

Good outcome:

- one task in the correct repo;
- links to related issues when the work spans surfaces;
- ambiguity recorded when routing cannot be resolved safely.

Bad outcome:

- an issue created in the current checkout because it was convenient;
- duplicate tasks across repositories;
- a weekly label or Project field used as a substitute for routing.

## Related Operating Canon

Work Item Routing is paired with Project Health Audit and Optional Weekly
Operating Loop:

- routing prevents the current checkout from becoming an accidental source of
  truth;
- Project Health Audit checks whether the project has a decision log, owners,
  escalation rules, and source-of-truth files;
- Optional Weekly Operating Loop uses outcomes and evidence when a project
  chooses a weekly cadence.
