# Behavioral Overlay Policy

Use this reference when a project wants a thin behavior-only layer for agents in addition to the engineering kernel.

## Purpose

The engineering kernel is the operating system.

A behavioral overlay is only a small reinforcement layer for model behavior. It can help with:

- explicit assumptions instead of silent guessing
- simplicity over overengineering
- surgical edits instead of drive-by rewrites
- goal-driven verification instead of vague "make it work"

This is useful, but it must not replace the kernel.

## Hard boundary

Behavioral overlays are:

- optional
- thin
- subordinate to project canon

They must not replace:

- PRD-first execution
- GitHub `Epic / Task / Bug`
- verification discipline
- `kernel_upstream_check`
- `kernel_sync_review`
- research classification

Process-skill packs such as Superpowers are not merely behavioral overlays. They can provide task-specific workflows for brainstorming, planning, TDD, debugging, review, and verification. They still remain subordinate to project canon and must not replace the engineering kernel.

## Multi-surface sync rule

If a project uses several agent surfaces, keep one canonical behavioral-overlay source and derive the rest from it.

Typical derived surfaces:

- `CLAUDE.md`-style root instructions
- Cursor project rules
- skill/plugin variants

Do not let these drift semantically. Different syntax is acceptable; different meaning is not.

## What to borrow from compact guideline repos

The reusable pattern is structural, not textual:

- one compact behavioral layer
- repeated consistently across several agent surfaces
- intentionally merged with stronger project-local rules

What not to borrow blindly:

- replacing the repo canon with a single-file guideline
- enabling `alwaysApply` / implicit auto-apply as a universal default
- copying another repo's exact phrasing without reconciling it with the local kernel and project canon

## Recommended universal candidate principles

These principles are reasonable overlay candidates across many projects:

1. State assumptions explicitly. If confused, name it.
2. Prefer the simplest code that solves the asked problem.
3. Touch only what is necessary; clean up only what your slice made obsolete.
4. Define success through verification, not only through intent.

## Project adoption rule

If a consumer repository adopts a behavioral overlay:

- document that it is optional and thin;
- document that `AGENTS.md`, PRD, tests, and repo-local canon outrank it;
- if several tool-specific variants exist, record which file is canonical and which files are derived.
