# Contributing to Agent Engineering Kernel

This repository is itself governed by the engineering kernel it defines.

## Start with the correct issue

Use:

- `Epic` for a non-trivial parent change
- `Task` for one executable slice
- `Bug` for a confirmed regression or incident

If the work spans multiple slices, decompose it into GitHub sub-issues.

## Research policy

- Tavily first
- official docs for external contracts
- known URLs fetched directly when already available
- verified facts separated from assumptions

## PR rule

- one PR should normally close one leaf issue
- parent epic stays open until acceptance and required verification are complete
- use draft PR while scope or verification is still moving
- prefer squash merge

## Minimum PR contents

- linked leaf issue
- parent context
- scope
- verification
- rollback path

## Repo-managed metadata

- `.github/labels.yml` is source-of-truth
- `scripts/sync_github_labels.py` is the sync path
- `CODE_OF_CONDUCT.md` and `SECURITY.md` stay in the repo, not only in chat/process memory
