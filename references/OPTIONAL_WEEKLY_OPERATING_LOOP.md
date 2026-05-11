# Optional Weekly Operating Loop

Use this only when a project chooses a weekly operating cadence.

Weekly planning is not universal kernel minimum. The universal rule is that, if
a project uses a weekly loop, the loop must compare planned outcomes with
evidence and must not roll stale work forward forever.

## Bootstrap Default

`bootstrap_default: false`

Projects may adopt this loop when weekly planning, retros, GitHub Projects,
W-labels, or a similar cadence are useful. The kernel must not require them for
every repository.

## Planning Rules

- plan outcomes, not task lists;
- each outcome states what should be true by the end of the cycle;
- each outcome has a measurable check or evidence path;
- route issues through Work Item Routing before create;
- record capacity constraints instead of planning an impossible week.

Example:

```markdown
Outcome: Signup bugfix is live without critical regressions by Friday.
Check: production smoke passes, bug issue closed by PR, rollback path recorded.
```

## Retro Rules

- compare planned outcomes against evidence;
- classify each outcome as `done`, `partial`, `miss`, `dropped`, or
  `spillover`;
- ask for human context only after evidence is gathered;
- write decisions to the durable retro, issue body, or project-local status
  artifact.

## Terminal Carryover Decisions

Open weekly work cannot remain open indefinitely without a decision. Use one:

- `close`: completed or no longer needs tracking;
- `drop`: intentionally removed from scope;
- `promote`: becomes an Epic or larger initiative;
- `spillover`: moves forward with an explicit reason and next check.

If the same work spills over repeatedly, stop and reformulate it instead of
blindly relabeling it again.

## Optional Local Mechanisms

These are project-local choices, not universal invariants:

- W-labels;
- retro labels;
- GitHub Projects fields and views;
- CRM pointers;
- calendar integration;
- cross-repo planning boards.

## Related Operating Canon

Optional Weekly Operating Loop is paired with Work Item Routing and Project
Health Audit:

- Work Item Routing prevents the current checkout from receiving weekly tasks
  that belong elsewhere;
- Project Health Audit checks whether a decision log, escalation rules, SSOT,
  incident log, freshness policy, and eval cases exist;
- weekly outcomes create the plan-vs-actual evidence used by retro closeout.
