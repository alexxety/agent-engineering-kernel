# Execution Surfaces

Use this when the question is not only *what* the workflow is, but *where* it
should run.

## Canon

Default to the cheapest correct execution surface.

For ordinary engineering work, that usually means:

- the local operator machine first
- a self-hosted runner next, if the repository already has one

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

So the kernel rule is:

- local/self-hosted first for ordinary work
- GitHub Actions for automation that genuinely belongs there

## What to encode in project canon

Project-local canon should state:

- the canonical local bootstrap command
- the canonical local test/verifier commands
- whether the project has self-hosted runners
- which workflows must remain in GitHub Actions
- that agents should not route routine dev/test work to paid hosted Actions by
  default
