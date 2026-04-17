# Kernel Sync Policy

Use this reference when deciding whether a live project learning belongs in the universal kernel.

## Canonical names

- protocol: `kernel_sync_review`
- decision field: `kernel_impact`

Do not split this into a separate skill name when `engineering-kernel` already applies. The safe pattern is one kernel skill with a formal sub-protocol.

## Allowed `kernel_impact` values

- `none`
  - the slice changed product/runtime behavior only
  - no reusable engineering-process learning was added
- `project_local_only`
  - the slice produced a durable rule, but it is specific to this repository, runtime, vendor, or topology
- `promote_to_kernel`
  - the slice produced a reusable engineering rule, workflow, template, or verification pattern that future projects should inherit

## Promotion test

Promote only when all are true:

- the learning was validated on a real project, not guessed in chat
- the learning is process-level or pattern-level, not path/host/service specific
- the learning reduces future agent dependence on chat memory
- the learning is likely to recur in another serious repository

## Required timing

Run `kernel_sync_review` only after:

- implementation is complete
- verification is green
- live/runtime acceptance is complete when relevant

Do not promote half-proven ideas into the kernel.

## Required output

Every serious slice should end with:

- `Kernel Impact: none | project_local_only | promote_to_kernel`
- short justification
- exact reusable artifact to update when promoting

If `kernel_impact = promote_to_kernel`:

- open or update the linked work in the kernel repository
- update machine-readable kernel state, references, templates, and tests
- keep project-specific residue in the project repo, not in the kernel
