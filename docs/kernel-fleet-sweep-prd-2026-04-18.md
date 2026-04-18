# PRD: Optional kernel fleet sweep for multi-repo operators

Date: `2026-04-18`

Status: `completed`

Source evidence:

- [kernel-upstream-awareness-prd-2026-04-18.md](/Users/raketa23/Work/Vs/agent-engineering-kernel/docs/kernel-upstream-awareness-prd-2026-04-18.md)

## Problem

`kernel_upstream_check` now gives deterministic drift awareness inside one consumer repository, but an operator working across several repositories still needs to enter each repo separately to run it. That is unnecessary operator friction and makes cross-project kernel drift easy to miss.

## Research Basis

- Slice classification: `repo_local_slice`
- Tavily-first research used: `no`
- Official docs used: `no`

Why:

- this slice extends already-verified kernel-owned local tooling
- no new vendor or platform behavior is being asserted beyond the existing kernel upstream-awareness contract

## Current State

Verified facts only.

- Kernel defines `kernel_upstream_check` and ships `scripts/check_kernel_upstream.py`.
- Consumer repos can pin `.kernel/upstream.json` and detect `current | update_available | not_configured | unknown`.
- Kernel docs already mention that an optional operator fleet sweep may exist.
- Kernel does not yet ship a canonical fleet-level script, config format, or operator reference.

## Target State

- Kernel defines a formal optional `kernel_fleet_sweep` operator protocol.
- Kernel ships a local-first script that scans multiple consumer repos in one pass.
- The script reuses each consumer repo's own `scripts/check_kernel_upstream.py` when present.
- The script supports both:
  - explicit repo paths passed on the CLI
  - a simple config file listing repo paths
- Output is deterministic and machine-readable through `--json`.
- The sweep remains read-only and non-destructive.

## Write Scope

- `SKILL.md`
- `ENGINEERING_KERNEL.yaml`
- `README.md`
- `references/KERNEL_UPSTREAM_AWARENESS.md`
- new `references/KERNEL_FLEET_SWEEP.md`
- new `scripts/kernel_fleet_sweep.py`
- `tests/test_check_kernel_upstream.py`
- new `tests/test_kernel_fleet_sweep.py`
- `tests/test_repo_kernel_canon.py`

## Rollout

### Phase 1
- define the new protocol in kernel canon and docs
- add a dedicated operator reference

Validation:
- docs mention `kernel_fleet_sweep`
- machine-readable kernel parses

### Phase 2
- implement the local-first fleet sweep script
- support CLI repo paths and config-file repo paths

Validation:
- script prints stable per-repo statuses
- JSON output is deterministic

### Phase 3
- add regression coverage for config parsing and aggregation

Validation:
- targeted tests pass
- script can scan a temp fleet with mixed statuses

## Verification Matrix

- code-path tests
  - config parsing
  - per-repo aggregation
  - current / update_available / not_configured / unknown reporting
- build/runtime checks
  - `py_compile` on added scripts
- sync checks
  - sweep uses project-local `scripts/check_kernel_upstream.py` when available
- live checks
  - run sweep against at least the local kernel consumer repos on this Mac
- rollback validation
  - removing the sweep leaves `kernel_upstream_check` unchanged for single-repo use

## Kernel Impact

- `promote_to_kernel`

Why:

This is universal operator workflow canon for multi-project users of the shared engineering kernel.

## Verification Snapshot

- code-path tests
  - `.venv/bin/python -m unittest tests.test_check_kernel_upstream tests.test_kernel_fleet_sweep tests.test_repo_kernel_canon` -> `OK`
- build/runtime checks
  - `python3 -m py_compile scripts/check_kernel_upstream.py scripts/kernel_fleet_sweep.py` -> `OK`
- live/operator check
  - `python3 scripts/kernel_fleet_sweep.py --json` -> `repo_count = 2`, `needs_attention_count = 2`
  - both current local consumer repos are honestly `not_configured` today, which is valid fleet-sweep evidence rather than a hidden failure

## Final State

- kernel now defines the optional `kernel_fleet_sweep` protocol
- kernel ships `scripts/kernel_fleet_sweep.py`
- kernel ships `references/KERNEL_FLEET_SWEEP.md`
- operator-local default config path is documented as `~/.config/agent-engineering-kernel/fleet-repos.json`
- fleet sweep reuses consumer checkers when available and falls back to the kernel checker otherwise
