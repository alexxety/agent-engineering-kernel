# PRD: Git Ref Operation Serialization Canon

Date: `2026-05-09`

Status: `implemented`

## Problem

Agent orchestrators may parallelize shell commands for speed. That is fine for
read-only file inspection, but it is unsafe for git commands that mutate or
refresh repository state. A real downstream slice launched `git fetch` and
`git pull` concurrently in one repository and hit a lock race on
`refs/remotes/origin/main`.

## Decision

The kernel now treats git commands that touch refs, the index, or the working
tree as serialized per repository.

These commands must not be run in parallel for the same repo:

- `git fetch`
- `git pull`
- `git switch`
- `git checkout`
- `git merge`
- `git rebase`
- `git branch -d/-D`
- `git push`

Read-only commands such as `git status`, `git diff`, `git log`, and `git show`
may be parallelized only when no ref-mutating git command is running for that
repo and the answer does not depend on a fresh ref update.

## Recovery

After a ref-lock race:

1. stop parallel git calls for that repository;
2. run `git status --short --branch`;
3. run the needed `git fetch`;
4. run `git pull --ff-only` when the goal is to update the current branch;
5. run `git diff --check` before claiming the repo is healthy.

## Kernel Impact

`promote_to_kernel`

This is a reusable orchestration rule across all repositories, not a
project-local Plaud rule.
