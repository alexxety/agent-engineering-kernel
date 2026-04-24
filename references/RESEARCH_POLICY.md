# Research Policy

The kernel is research-first, not guess-first.

## Preferred stack

1. Tavily search
2. direct fetch/index of already-known official URLs or docs
3. manual source reading, comparison, and synthesis by the agent
4. Tavily research only as an explicitly justified expensive fallback for broad deep-sweeps

## Rules

- research is Tavily Search-first, not Tavily Research-first
- classify each non-trivial slice before edits as either `repo_local_slice` or `external_contract_slice`
- `repo_local_slice` may proceed from project truth, deterministic verification, and local runtime checks when only repo-owned behavior is changing
- `external_contract_slice` requires fresh external research before code or docs land
- for vendor/platform/API behavior, verify the external contract from official docs
- use Tavily Research only when Tavily Search, known official docs, and manual synthesis are insufficient
- if Tavily Research is used, record why lower-cost search/direct docs/manual synthesis were insufficient
- separate verified facts from assumptions
- record external-contract evidence in the active PRD or decision note instead of leaving it only in chat
- every `external_contract_slice` must record an `external_source_of_truth_matrix` before implementation lands
- if a known URL already exists, fetch or index it directly instead of re-running broad search
- if Tavily or the preferred stack is unavailable, record the capability gap and use the best documented fallback

## Research boundary

Use `repo_local_slice` only when the work is limited to repository-owned behavior such as:

- local UI copy, layout, navigation, or progressive disclosure
- local component state or deterministic tests
- internal docs that describe already verified project behavior

Use `external_contract_slice` whenever the work changes or asserts current behavior for any changing outside system such as:

- dependency source, version, install flow, or packaging claims
- vendor/platform/API behavior
- external authentication/runtime assumptions
- interpreter or dependency compatibility claims

The boundary exists to prevent two opposite mistakes:

- over-researching a pure repo-local slice as if it were an upstream-contract change
- shipping an external-contract slice from stale memory or old assumptions

## External source-of-truth matrix

For every `external_contract_slice`, the active PRD or decision note must record an `external_source_of_truth_matrix`.

Required fields per external surface in scope:

- `surface_name`
- `project_local_source_of_truth`
- `upstream_or_vendor_source`
- `exact_version_commit_build_url_or_identifier`
- `local_verification_method`
- `divergence_notes`

The point is simple:

- do not rely only on a fresh vendor doc if the project has a pinned local version or config
- do not rely only on a local helper or old note if the current vendor contract has changed
- do not let the exact active version/commit/build/URL stay implicit

The matrix is where those facts are reconciled before implementation lands.

## What research should produce

- current state
- target state
- risks and assumptions
- exact files/services likely to change
- evidence links or citations

Do not let research stay only in chat. It must flow into the active PRD or decision doc.
