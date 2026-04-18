#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_METADATA = ROOT / ".kernel" / "upstream.json"


def load_metadata(path: Path) -> dict:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping in {path}")
    return payload


def resolve_remote_head(repo_url: str, branch: str) -> str:
    completed = subprocess.run(
        ["git", "ls-remote", repo_url, f"refs/heads/{branch}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "git ls-remote failed")
    line = completed.stdout.strip()
    if not line:
        raise RuntimeError("remote branch not found")
    return line.split()[0]


def build_result(metadata_path: Path) -> dict:
    payload = load_metadata(metadata_path)
    if not payload:
        return {
            "status": "not_configured",
            "metadata_path": str(metadata_path),
        }

    repo = str(payload.get("kernel_repo") or "").strip()
    branch = str(payload.get("kernel_default_branch") or "").strip()
    pinned_commit = str(payload.get("pinned_commit") or "").strip()
    if not repo or not branch or not pinned_commit:
        return {
            "status": "unknown",
            "metadata_path": str(metadata_path),
            "error": "missing required metadata fields",
            "kernel_repo": repo,
            "kernel_default_branch": branch,
            "pinned_commit": pinned_commit,
        }

    try:
        remote_commit = resolve_remote_head(repo, branch)
    except Exception as exc:  # pragma: no cover - exercised in tests with patching
        return {
            "status": "unknown",
            "metadata_path": str(metadata_path),
            "kernel_repo": repo,
            "kernel_default_branch": branch,
            "pinned_commit": pinned_commit,
            "error": str(exc),
        }

    status = "current" if remote_commit == pinned_commit else "update_available"
    return {
        "status": status,
        "metadata_path": str(metadata_path),
        "kernel_repo": repo,
        "kernel_default_branch": branch,
        "pinned_commit": pinned_commit,
        "remote_commit": remote_commit,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check whether a consumer repository is behind the upstream engineering kernel.")
    parser.add_argument("--metadata", default=str(DEFAULT_METADATA), help="Path to .kernel/upstream.json")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--fail-if-update-available",
        action="store_true",
        help="Exit non-zero when upstream differs from the pinned kernel commit.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = build_result(Path(args.metadata).expanduser().resolve())
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for key in (
            "status",
            "metadata_path",
            "kernel_repo",
            "kernel_default_branch",
            "pinned_commit",
            "remote_commit",
            "error",
        ):
            if key in result:
                print(f"{key}: {result[key]}")
    if args.fail_if_update_available and result.get("status") == "update_available":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
