# PRD: Agent Engineering Kernel

Date: `2026-04-17`

Status: `implemented`

## Problem

Future agent sessions should not need the engineering process re-explained from chat history.

## Decision

Create one standalone repository that is both:

- the durable source-of-truth for the engineering kernel
- the installable skill root for future Codex sessions

## Core

Minimal core:

- project canon
- PRD-first execution
- GitHub `Epic / Task / Bug`
- PR verification contract
- ownership and labels

Maximum practical layer:

- GitHub settings enforcement
- branch protection / rulesets
- required approvals
- stale review dismissal
- code-owner review
- status checks
- Projects / issue types

## Implementation

This repository now contains:

- root `SKILL.md`
- machine-readable `ENGINEERING_KERNEL.yaml`
- references for bootstrap and model adapters
- reusable project templates
- deterministic bootstrap script

## Acceptance

- future agents can read one standalone source
- the same kernel can be reused across repositories
- the same kernel can be consumed by GPT/Codex and Claude-style agents
