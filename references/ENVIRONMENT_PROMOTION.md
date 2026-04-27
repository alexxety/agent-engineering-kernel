# Environment Promotion

Use this when a project is moving from local development toward a real deployment.

## Canon

Production-bound projects should use one codebase with multiple deploy environments, not copied projects that drift.

Default environment classes:

- `local`: developer/operator machine for iteration. It may contain throwaway data and local-only secrets.
- `verify`: disposable automated verification environment. Mutating automated tests belong here or in another explicitly disposable test environment.
- `staging`: persistent production-like environment for acceptance, deploy rehearsal, and sandbox provider checks.
- `production`: real users, real customer data, and production provider identities.

## Rules

- Document environment boundaries before launch hardening or production deploy work.
- Do not put production secrets, production database URLs, or production provider credentials in local config.
- Do not run mutating automated tests against production.
- Staging and production must have separate secrets and backing resources.
- Schema and deploy changes must move through the repository's auditable delivery path.
- Each project must document the exact production-safe migration/deploy command before production use.
- Each project must document the backup or restore-point path before production migrations.
- Production smoke checks should be read-safe unless a PRD or decision note approves a specific production write and rollback path.
- Production data may move down to staging only through documented backup/restore and sanitization.
- Local or staging data must not move up to production.

## What To Encode In Project Canon

Project-local canon should state:

- exact environment names;
- local bootstrap and verification commands;
- disposable verification project/resource names;
- staging and production secret boundaries;
- provider sandbox versus production identities;
- production-safe migration/deploy command;
- pre-production backup or restore-point procedure;
- staging smoke checks;
- production smoke checks;
- rollback path for app and data changes;
- rules for production-data copies into staging, including sanitization.

## Relationship To Execution Surfaces

Execution surfaces answer where work runs. Environment promotion answers how code, config, secrets, schema, and data move toward production.

GitHub may coordinate deploy triggers and environment approvals, but owned compute or the selected hosting platform may execute the deploy. The project must record the concrete surface instead of assuming GitHub-hosted runners are the default.
