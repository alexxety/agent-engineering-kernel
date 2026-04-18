#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHECKER = ROOT / "scripts" / "check_kernel_upstream.py"
DEFAULT_CONFIG = Path.home() / ".config" / "agent-engineering-kernel" / "fleet-repos.json"
CANONICAL_STATUSES = ("current", "update_available", "not_configured", "unknown")


def load_repo_paths_from_config(path: Path) -> list[str]:
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8")
    stripped = raw.strip()
    if not stripped:
        return []

    if path.suffix.lower() == ".json" or stripped[0] in "[{":
        payload = json.loads(raw)
        if isinstance(payload, dict):
            repos = payload.get("repos", [])
        elif isinstance(payload, list):
            repos = payload
        else:
            raise ValueError(f"Unsupported config payload in {path}")
        if not isinstance(repos, list):
            raise ValueError(f"Expected 'repos' list in {path}")
        return [str(item).strip() for item in repos if str(item).strip()]

    paths: list[str] = []
    for line in raw.splitlines():
        candidate = line.strip()
        if not candidate or candidate.startswith("#"):
            continue
        paths.append(candidate)
    return paths


def collect_repo_paths(cli_repos: list[str], config_path: Path | None) -> list[Path]:
    ordered: list[Path] = []
    seen: set[Path] = set()

    candidates: list[str] = []
    if config_path is not None and config_path.exists():
        candidates.extend(load_repo_paths_from_config(config_path))
    candidates.extend(cli_repos)

    for repo in candidates:
        resolved = Path(repo).expanduser().resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        ordered.append(resolved)
    return ordered


def select_checker(repo_path: Path) -> tuple[Path, str]:
    consumer_checker = repo_path / "scripts" / "check_kernel_upstream.py"
    if consumer_checker.exists():
        return consumer_checker, "consumer_repo"
    return DEFAULT_CHECKER, "kernel_fallback"


def run_checker(checker_path: Path, repo_path: Path, metadata_path: Path) -> dict:
    completed = subprocess.run(
        [sys.executable, str(checker_path), "--metadata", str(metadata_path), "--json"],
        check=False,
        capture_output=True,
        text=True,
        cwd=str(repo_path if repo_path.exists() else ROOT),
    )
    if completed.returncode != 0:
        return {
            "status": "unknown",
            "error": completed.stderr.strip() or completed.stdout.strip() or "checker failed",
        }
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return {
            "status": "unknown",
            "error": f"invalid checker JSON: {exc}",
        }
    if not isinstance(payload, dict):
        return {
            "status": "unknown",
            "error": "checker did not return a JSON object",
        }
    return payload


def inspect_repo(repo_path: Path) -> dict:
    if not repo_path.exists():
        return {
            "repo_path": str(repo_path),
            "status": "unknown",
            "error": "repo path does not exist",
        }

    metadata_path = repo_path / ".kernel" / "upstream.json"
    checker_path, checker_source = select_checker(repo_path)
    payload = run_checker(checker_path, repo_path, metadata_path)
    result = dict(payload)
    result["repo_path"] = str(repo_path)
    result["metadata_path"] = str(metadata_path)
    result["checker_path"] = str(checker_path)
    result["checker_source"] = checker_source
    if result.get("status") not in CANONICAL_STATUSES:
        result["status"] = "unknown"
        result.setdefault("error", "checker returned non-canonical status")
    return result


def summarize(results: list[dict]) -> dict[str, int]:
    counts = {status: 0 for status in CANONICAL_STATUSES}
    for result in results:
        status = str(result.get("status") or "unknown")
        if status not in counts:
            status = "unknown"
        counts[status] += 1
    return counts


def build_fleet_result(repo_paths: list[Path], config_path: Path | None) -> dict:
    results = [inspect_repo(path) for path in repo_paths]
    counts = summarize(results)
    return {
        "repo_count": len(results),
        "needs_attention_count": sum(count for status, count in counts.items() if status != "current"),
        "status_counts": counts,
        "config_path": str(config_path) if config_path is not None and config_path.exists() else None,
        "repos": results,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run kernel_upstream_check across multiple consumer repositories.")
    parser.add_argument("repos", nargs="*", help="Explicit repository paths to scan.")
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG),
        help="Optional config file listing repository paths. Defaults to ~/.config/agent-engineering-kernel/fleet-repos.json",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    parser.add_argument(
        "--fail-if-attention-required",
        action="store_true",
        help="Exit non-zero when any repository is not current.",
    )
    return parser


def render_text(result: dict) -> str:
    lines = [
        f"repo_count: {result['repo_count']}",
        f"needs_attention_count: {result['needs_attention_count']}",
    ]
    for status in CANONICAL_STATUSES:
        lines.append(f"{status}: {result['status_counts'][status]}")
    if result.get("config_path"):
        lines.append(f"config_path: {result['config_path']}")
    for repo in result["repos"]:
        lines.append(f"- [{repo['status']}] {repo['repo_path']}")
        lines.append(f"  checker_source: {repo['checker_source']}")
        if "pinned_commit" in repo:
            lines.append(f"  pinned_commit: {repo['pinned_commit']}")
        if "remote_commit" in repo:
            lines.append(f"  remote_commit: {repo['remote_commit']}")
        if repo.get("error"):
            lines.append(f"  error: {repo['error']}")
    return "\n".join(lines)


def main() -> int:
    args = build_parser().parse_args()
    config_path = Path(args.config).expanduser().resolve() if args.config else None
    repo_paths = collect_repo_paths(args.repos, config_path)
    if not repo_paths:
        raise SystemExit("No repositories configured. Pass repo paths or provide a config file.")

    result = build_fleet_result(repo_paths, config_path)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render_text(result))

    if args.fail_if_attention_required and result["needs_attention_count"] > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
