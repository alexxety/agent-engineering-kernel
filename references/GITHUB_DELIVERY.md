# GitHub Delivery Flow

Use this when the user wants the full branch / PR / merge discipline, not just issue templates.

## Canonical sequence

1. Create or update the PRD
2. Open the parent `Epic` if the work is non-trivial
3. Create the executable leaf issue (`Task` or `Bug`)
4. Create the branch from the leaf issue
5. Implement in a small slice
6. Open or update a draft PR
7. Run verification
8. Mark the PR ready
9. Merge
10. Delete the head branch

## Rules

- PR closes the leaf issue only
- parent epic stays open until all required leaf issues and acceptance checks are complete
- keep the PR description aligned with the real scope and verification
- use draft PR while the scope or verification is still moving
- prefer squash merge unless the project canon explicitly chooses another method

## Why this matters

The branch/PR layer is part of the engineering kernel, not a separate afterthought. It prevents code from landing without an issue tree, verification, and an auditable review surface.
