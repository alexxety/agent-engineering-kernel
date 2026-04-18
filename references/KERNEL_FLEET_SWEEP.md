# Kernel Fleet Sweep

Use this reference when one operator machine needs a single view across multiple consumer repositories of `agent-engineering-kernel`.

## Problem

`kernel_upstream_check` already works per consumer repository, but operators with several active repos still need a multi-repo control point. `kernel_fleet_sweep` is that optional operator-local layer.

## Canonical name

- protocol: `kernel_fleet_sweep`

This protocol does not replace `kernel_upstream_check`.

- `kernel_upstream_check` is the per-repo drift check
- `kernel_fleet_sweep` is the optional multi-repo wrapper around that same contract

## Scope

- operator-local only
- read-only
- optional
- not a bootstrap default

Do not turn this into blind auto-adoption.

## Default config path

- `~/.config/agent-engineering-kernel/fleet-repos.json`

Accepted file shapes:

1. JSON object:

```json
{
  "repos": [
    "/absolute/path/to/project-a",
    "/absolute/path/to/project-b"
  ]
}
```

2. JSON array:

```json
[
  "/absolute/path/to/project-a",
  "/absolute/path/to/project-b"
]
```

3. Plain text file:

```text
# one repo path per line
/absolute/path/to/project-a
/absolute/path/to/project-b
```

## Rules

- prefer each consumer repo's own `scripts/check_kernel_upstream.py` when present
- fall back to the kernel's `scripts/check_kernel_upstream.py` with the consumer repo's `.kernel/upstream.json` when the consumer checker is missing
- support both explicit repo paths and config-file-driven repo discovery
- never auto-apply kernel updates
- if a repo reports `update_available`, turn it into a normal project-local adoption slice or explicitly defer it

## Canonical statuses

Per-repo status remains the same as `kernel_upstream_check`:

- `current`
- `update_available`
- `not_configured`
- `unknown`

## Example

Scan the default local fleet config:

```bash
python3 scripts/kernel_fleet_sweep.py --json
```

Scan explicit repos:

```bash
python3 scripts/kernel_fleet_sweep.py /path/to/repo-a /path/to/repo-b
```

Fail non-zero if any repo needs attention:

```bash
python3 scripts/kernel_fleet_sweep.py --fail-if-attention-required
```
