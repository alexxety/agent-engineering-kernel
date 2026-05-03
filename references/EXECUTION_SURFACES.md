# Execution Surfaces

Use this when the question is not only *what* the workflow is, but *where* it
should run.

## Canon

Default to the cheapest correct execution surface.

For ordinary engineering work, that usually means:

- the local operator machine first
- a self-hosted runner next, if the repository already has one or can
  reasonably provide one

GitHub coordinates repository workflow: issues, pull requests, check status,
scheduled triggers, and deployment triggers. It is not the default compute
surface for routine development, verification, research, bootstrap, or audit
work. Owned compute executes routine work by default.

Do **not** default to paid GitHub-hosted Actions for work that can be executed
locally.

## Local-first rule

For normal development, debugging, research, verification, and bootstrap:

1. inspect the local prerequisites
2. use the repository's local bootstrap path if it already exists
3. install or repair missing local prerequisites deterministically
4. only escalate to GitHub Actions when local execution is not the right surface

Examples of good local-first work:

- running unit tests
- running project verification scripts
- local bootstrap / dependency install
- documentation generation
- research and code audit
- dry-run sync scripts

## When GitHub Actions are the right surface

Use GitHub Actions when the value is specifically repository-native automation:

- scheduled workflows
- event-driven automation
- deployment pipelines
- hosted verification that must execute inside GitHub
- branch/merge policy checks that belong to the repository platform

## Risk-Based Required CI

For required checks, do not use workflow-level `paths`, `paths-ignore`, or
commit-message skip instructions as the normal optimization path. If the whole
workflow is skipped before jobs are created, GitHub can leave required checks in
`Pending`.

Keep required workflows triggered, then reduce runner load inside the workflow:

- run a lightweight classifier job first
- gate expensive jobs with job-level `if` conditions
- let irrelevant jobs become `skipped` required checks instead of missing checks
- run the full required CI matrix for `main`, release/deploy, scheduled,
  manual, dependency, workflow, and explicit `full-ci` override changes

This is risk-based CI: the repository still gets required check visibility, but
small frontend-only, backend-only, docs-only, or canon-only PRs do not consume
unrelated self-hosted runner time.

## Environment Promotion

Execution surfaces answer where work runs. Environment promotion answers how code,
config, secrets, schema, and data move toward production.

Production-bound projects should document:

- `local` for development and operator iteration
- disposable `verify` for mutating automated tests
- `staging` for production-like acceptance with sandbox identities
- `production` for real users, customer data, and provider identities

Production secrets and production database URLs must not be used in local config
or local tests. Mutating automated tests must not run against production.

Projects should document the production-safe migration/deploy command, backup or
restore-point path, staging smoke checks, production smoke checks, and rollback
before production use.

## Why this matters

For private repositories, GitHub-hosted Actions consume billed/included runner
minutes. Self-hosted runners do not consume those GitHub-hosted minutes.
Actions artifacts and dependency caches can also consume billed/included
storage. Large dependency cache uploads are paid-surface work too, not a
harmless default.

So the kernel rule is:

- local/self-hosted first for ordinary work
- GitHub as the delivery/check coordinator
- owned compute as the default executor
- GitHub-hosted runners or cache/artifact storage only when a PRD/decision note
  explicitly accepts that paid surface

## What to encode in project canon

Project-local canon should state:

- the canonical local bootstrap command
- the canonical local test/verifier commands
- whether the project has self-hosted runners
- the self-hosted runner label(s) for recurring repository checks
- which workflows must remain in GitHub Actions
- which required workflows use risk-based classifier jobs and job-level gates
- the explicit `full-ci` override label or equivalent manual full-check path
- the environment promotion path from local to verify to staging to production
- the production-safe migration/deploy command and backup or restore-point path
- that agents should not route routine dev/test work to paid hosted Actions by
  default
- that dependency cache uploads and artifact retention are disabled or bounded
  unless the project explicitly accepts GitHub storage usage
