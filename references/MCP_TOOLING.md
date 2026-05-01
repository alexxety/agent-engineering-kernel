# MCP Tooling Policy

Use this when a project has MCP servers, app integrations, or an App connector for an external service.

## Purpose

MCP and App connector tooling is the preferred structured interface for supported external-service operations. It should be used for repository, issue, pull request, review, CI, search, or vendor-data operations when the connector has the needed capability and permissions.

The connector is not the project canon, not a secret store, and not a reason to skip PRD-first or verification-first work.

For orchestrated coding, keep MCP on the orchestrator or a dedicated read-only
research agent. Do not pass rich MCP tool surfaces to implementation workers by
default. Use project-local no-MCP workers as described in
`references/PROJECT_LOCAL_WORKERS.md`.

## Identity Boundaries

Treat these as different identities:

- MCP server or App connector token
- GitHub App installation token
- local `gh` CLI token
- personal access token
- service account or sandbox identity
- external account, workspace, organization, tenant, or profile selected inside one MCP server

Local `gh` auth and GitHub App connector auth are different identities with separate permissions. A working `gh auth status` does not prove that the App connector can create issues or pull requests. A connector `403 Resource not accessible by integration` usually points at the installed GitHub App repository access or App permissions, not the local `gh` token.

Do not paste or record tokens in repo docs, PRDs, issue bodies, or chat transcripts. Record the identity class and permission surface, not the secret.

## Multi-Identity MCP Tools

Some MCP servers expose multiple external identities through one backend, for
example several accounts, workspaces, organizations, tenants, or profiles.
Identity selection is part of the operation contract, not something the model
should guess from a default.

When a discovery tool exists, such as `list_accounts`, `list_workspaces`,
`list_organizations`, or an equivalent provider-specific tool, use it before a
mutating operation unless the target identity is already explicit in the user
request, PRD, runbook, or project canon.

Read-only fan-out across identities is allowed only when the tool documents that
behavior and labels results by identity.

Mutating operations must pass an explicit identity selector such as `account`,
`workspace`, `organization`, `tenant`, or the provider's equivalent. If the
target identity is ambiguous, ask or use project canon; do not silently choose a
default account, workspace, organization, tenant, or profile.

Do not paste or record secrets, session strings, tokens, or private account
content in repo docs, PRDs, issue bodies, pull requests, or chat transcripts.

## GitHub App Connector Minimums

For GitHub delivery through an MCP-backed App connector, the installed GitHub App should have access to the target repository and the minimum permissions for the operation:

- repository access to the target repo, or all repositories when the operator intentionally chooses that broader scope
- `Contents: Read and write` when the connector changes code, branches, files, or workflow files
- `Issues: Read and write` when it creates or updates issues
- `Pull requests: Read and write` when it creates or updates pull requests
- `Actions` or `Workflows: Read and write` only when action state or workflow files are in scope

If the connector fails with a permission error, check the installed GitHub App first: `GitHub Settings -> Applications -> Installed GitHub Apps -> Configure`. Confirm repository access and the requested permissions there before refreshing the local `gh` token.

## Preferred Flow

1. Use the MCP server or App connector for structured operations it supports.
2. For multi-identity MCP tools, discover or confirm the target identity before mutating operations.
3. Check that the connector identity has repository access and write permissions before assuming a token problem.
4. If the connector is unavailable, incomplete, stale, or blocked, use the canonical CLI fallback.
5. Keep the fallback shell-safe: use `gh --body-file`, single-quoted heredoc-generated body files, and the kernel sub-issue helper when normal issue numbers must be linked.
6. Record the capability gap in the active PRD, issue, or closeout when it changes execution, verification, or operator setup.

## Verification

Live external writes require evidence. Prefer low-impact checks:

- list or read through the connector when a read permission is enough
- create a temporary sandbox issue or branch only when write permission must be proven
- close or clean up temporary verification artifacts immediately
- never use production identities as test identities when sandbox identities are required

Do not claim MCP or App connector access works only because local CLI access works. Verify the connector path itself.

## Non-goals

- Do not store tokens in the repository.
- Do not replace project-local canon, active PRDs, or verification contracts with connector defaults.
- Do not require MCP for every project; use it when available and useful.
- Do not create a separate engineering workflow for each connector. Adapt only the tool surface.
