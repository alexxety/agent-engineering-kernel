#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
Usage:
  scripts/claude-code-readonly-subagent.sh [--mode smoke|review-files|review-repo] "review prompt"

Runs Claude Code as a one-shot read-only subagent:
  - no session persistence
  - empty MCP config with strict MCP enforcement
  - stream-json output with --verbose for observable long runs
  - explicit permission mode: dontAsk, never plan
  - default direct binary preference: $HOME/.local/bin/claude

Modes:
  smoke        no tools, default max budget 1 USD
  review-files Read only, default max budget 5 USD
  review-repo  Read,Grep,Glob, default max budget 10 USD

Environment:
  CLAUDE_CODE_BIN                 override the claude binary path
  CLAUDE_CODE_MODEL               override the model, defaults to claude-opus-4-8
  CLAUDE_WORKER_MAX_BUDGET_USD    override the mode default budget
  CLAUDE_CODE_ALLOW_WRAPPER=1     allow known wrapper binaries such as cmux

Do not use this wrapper for implementation edits, live systems, production
operations, secrets, customer data export, messaging sends, or GitHub writes.

Exit codes:
  64  invalid usage
  78  Claude Code auth/config is unhealthy
  127 claude command not found
EOF
}

mode="review-files"

if [[ $# -ge 2 && "$1" == "--mode" ]]; then
  mode=$2
  shift 2
fi

if [[ $# -ne 1 ]]; then
  usage
  exit 64
fi

case "$mode" in
  smoke)
    tools=""
    default_budget="1"
    ;;
  review-files)
    tools="Read"
    default_budget="5"
    ;;
  review-repo)
    tools="Read,Grep,Glob"
    default_budget="10"
    ;;
  *)
    echo "invalid_mode: expected smoke, review-files, or review-repo" >&2
    usage
    exit 64
    ;;
esac

if [[ -n "${CLAUDE_CODE_BIN:-}" ]]; then
  claude_bin=$CLAUDE_CODE_BIN
elif [[ -x "$HOME/.local/bin/claude" ]]; then
  claude_bin="$HOME/.local/bin/claude"
else
  claude_bin=$(command -v claude || true)
fi

if [[ -z "$claude_bin" || ! -x "$claude_bin" ]]; then
  echo "claude_not_found: install and authenticate Claude Code before using this adapter" >&2
  exit 127
fi

if [[ "$claude_bin" == *"/cmux.app/"* && "${CLAUDE_CODE_ALLOW_WRAPPER:-}" != "1" ]]; then
  echo "claude_wrapper_detected: set CLAUDE_CODE_BIN to a direct Claude Code binary or CLAUDE_CODE_ALLOW_WRAPPER=1 to proceed" >&2
  exit 78
fi

if ! "$claude_bin" auth status >/dev/null 2>&1; then
  echo "claude_auth_unhealthy: run 'claude auth login' or configure the approved API-key helper path" >&2
  exit 78
fi

prompt=$1
budget=${CLAUDE_WORKER_MAX_BUDGET_USD:-$default_budget}
model=${CLAUDE_CODE_MODEL:-claude-opus-4-8}

exec "$claude_bin" -p \
  --model "$model" \
  --no-session-persistence \
  --output-format stream-json \
  --verbose \
  --mcp-config '{"mcpServers":{}}' \
  --strict-mcp-config \
  --tools "$tools" \
  --permission-mode dontAsk \
  --disable-slash-commands \
  --no-chrome \
  --max-budget-usd "$budget" \
  "$prompt"
