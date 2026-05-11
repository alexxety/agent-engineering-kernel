# Project Health Audit

Use this when bootstrapping or auditing a project for agent-led engineering
readiness.

The audit does not ask whether the project is "organized." It asks whether an
agent can make safe, repeatable decisions without relying on chat memory.

## Default Artifact Checklist

Check for:

- `ssot_per_domain`: one source of truth per domain or metric family;
- `metric_definitions`: formulas, inclusions, exclusions, and units;
- `data_freshness_policy`: when a snapshot becomes stale and how to label it;
- `decision_log`: date, decision, reason, rejected alternatives, owner;
- `escalation_rules`: when an agent must stop and ask;
- `incident_log`: what broke, root cause, fix, and rule added;
- `prohibited_actions`: actions agents must not take without confirmation;
- `eval_or_golden_cases`: known inputs and expected outputs for critical agent
  workflows;
- `critical_pipeline_runbooks`: trigger, steps, failure modes, rollback, and
  escalation path.

## Finding Classes

Classify each gap as one of:

- `control_gap`: no mechanism prevents a serious mistake;
- `visibility_gap`: no reliable way to see state, freshness, or ownership;
- `consistency_gap`: several sources can disagree without a resolution rule.

## Minimum Finding Format

```markdown
### <artifact> - missing

- Class: control_gap | visibility_gap | consistency_gap
- Symptom:
- Risk:
- Minimum fix:
- Owner:
```

## Rules

- do not invent fake metrics, owners, or decision history;
- mark missing data as missing instead of filling from memory;
- treat stale snapshots as stale when no freshness policy proves otherwise;
- prefer a small durable file over a large undocumented process;
- keep business-specific metrics project-local;
- use the audit to create project-local tasks only after Work Item Routing
  identifies the correct target surface.

## Bootstrap Guidance

A healthy project does not need every artifact on day one. It does need clear
answers for high-risk areas:

- where the canonical numbers live;
- who owns decisions;
- when agents must escalate;
- what agents must never do without confirmation;
- how incidents change the canon;
- which critical workflows have eval or golden cases.

## Related Operating Canon

Project Health Audit is paired with Work Item Routing and Optional Weekly
Operating Loop:

- Work Item Routing prevents the current checkout from receiving unrelated
  issues;
- the audit checks for a decision log, SSOT, escalation rules, incident log,
  freshness policy, and eval cases;
- Optional Weekly Operating Loop turns planned outcomes into evidence-based
  retro decisions when a project chooses that cadence.
