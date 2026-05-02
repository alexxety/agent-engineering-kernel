#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/claude-code-readonly-subagent.sh "review prompt"

Runs Claude Code as a one-shot read-only subagent:
  - no session persistence
  - empty MCP config with strict MCP enforcement
  - read-only tools only: Read,Grep,Glob
  - default max budget: ${CLAUDE_WORKER_MAX_BUDGET_USD:-2} USD

Do not use this wrapper for implementation edits, live systems, production
operations, secrets, customer data export, messaging sends, or GitHub writes.

Exit codes:
  64  invalid usage
  78  Claude Code auth/config is unhealthy
  127 claude command not found
EOF
}

if [[ $# -ne 1 ]]; then
  usage
  exit 64
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "claude_not_found: install and authenticate Claude Code before using this adapter" >&2
  exit 127
fi

if ! claude auth status >/dev/null 2>&1; then
  echo "claude_auth_unhealthy: run 'claude auth login' or configure the approved API-key helper path" >&2
  exit 78
fi

prompt=$1

exec claude -p \
  --no-session-persistence \
  --mcp-config '{"mcpServers":{}}' \
  --strict-mcp-config \
  --tools 'Read,Grep,Glob' \
  --permission-mode dontAsk \
  --max-budget-usd "${CLAUDE_WORKER_MAX_BUDGET_USD:-2}" \
  "$prompt"
