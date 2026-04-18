# Research Policy

The kernel is research-first, not guess-first.

## Preferred stack

1. Tavily search
2. Tavily research for deeper topic sweeps
3. direct fetch/index of already-known URLs or docs

## Rules

- research is Tavily-first
- classify each non-trivial slice before edits as either `repo_local_slice` or `external_contract_slice`
- `repo_local_slice` may proceed from project truth, deterministic verification, and local runtime checks when only repo-owned behavior is changing
- `external_contract_slice` requires fresh external research before code or docs land
- for vendor/platform/API behavior, verify the external contract from official docs
- separate verified facts from assumptions
- record external-contract evidence in the active PRD or decision note instead of leaving it only in chat
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

## What research should produce

- current state
- target state
- risks and assumptions
- exact files/services likely to change
- evidence links or citations

Do not let research stay only in chat. It must flow into the active PRD or decision doc.
