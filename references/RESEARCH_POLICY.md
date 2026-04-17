# Research Policy

The kernel is research-first, not guess-first.

## Preferred stack

1. Tavily search
2. Tavily research for deeper topic sweeps
3. direct fetch/index of already-known URLs or docs

## Rules

- research is Tavily-first
- for vendor/platform/API behavior, verify the external contract from official docs
- separate verified facts from assumptions
- if a known URL already exists, fetch or index it directly instead of re-running broad search
- if Tavily or the preferred stack is unavailable, record the capability gap and use the best documented fallback

## What research should produce

- current state
- target state
- risks and assumptions
- exact files/services likely to change
- evidence links or citations

Do not let research stay only in chat. It must flow into the active PRD or decision doc.
