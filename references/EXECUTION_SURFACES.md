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
- that agents should not route routine dev/test work to paid hosted Actions by
  default
- that dependency cache uploads and artifact retention are disabled or bounded
  unless the project explicitly accepts GitHub storage usage
