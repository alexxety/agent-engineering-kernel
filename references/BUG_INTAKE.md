# Automatic GitHub Bug Intake

Use this when the user wants runtime failures and engineering incidents to land
in GitHub as durable `Bug` work instead of dying inside logs or chat alerts.

## Canonical source-of-truth

Bug intake starts from normalized engineering surfaces, not from raw log text.

Allowed primary sources:

- verifier results
- watchdog verdicts
- readiness-gate failures
- other explicit runtime gates that already classify the incident

Do **not** create bug issues directly from:

- raw logs
- raw stderr/stdout fragments
- one-off retry noise
- Telegram alerts by themselves
- chat summaries without a stable fingerprint

## Required model

1. Normalize the incident.
2. Compute one stable fingerprint for the bug class.
3. Search for an existing open `Bug` issue with that fingerprint.
4. Update it if it exists.
5. Create it if it does not.

One bug class should map to one durable GitHub issue until the class is
verified as resolved.

## Fingerprint rules

Good fingerprints are stable and implementation-relevant.

Examples:

- `dudarik:manual_slug_collision:auto_generated`
- `yotubol:notebooklm_auth_expired`
- `pipeline:scheduled_publish:stale`

Bad fingerprints:

- full exception strings with timestamps
- raw HTTP bodies
- ad hoc human prose with no stable key

## Threshold policy

Do not open a bug issue for every transient failure.

Use one of these gates first:

- repeated occurrence threshold
- `broken` verifier status
- confirmed auth expiry/revocation
- queue stuck beyond canon threshold
- confirmed terminal runtime state

## Issue contents

Automatic or semi-automatic bug issues should include:

- stable fingerprint
- source surface
- observed behavior
- impact
- first seen
- last seen
- occurrence count
- current evidence
- containment / rollback status

## Target repository rule

Automatic bug intake belongs in the repository that owns the runtime or workflow
being observed.

That means:

- project/runtime incidents land in the target project repo
- the kernel repo stores the canon, not the target project's live bug backlog

## Fix flow

- create or update the `Bug` intake issue
- if the fix is multi-slice, use an `Epic` plus executable `Task`/`Bug`
  sub-issues
- PR closes the executable leaf only
- do not auto-close the intake issue until recovery is verified by the same
  canonical surface that opened it
