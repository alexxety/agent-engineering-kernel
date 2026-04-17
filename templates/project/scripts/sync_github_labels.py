#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote

import yaml


ROOT = Path(__file__).resolve().parent.parent
LABELS_FILE = ROOT / ".github" / "labels.yml"


def load_desired_labels(path: Path = LABELS_FILE) -> dict[str, dict[str, str]]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    items = payload.get("labels")
    if not isinstance(items, list) or not items:
        raise ValueError(f"{path} must define a non-empty 'labels' list")
    labels: dict[str, dict[str, str]] = {}
    for item in items:
        name = str(item.get("name", "")).strip()
        color = str(item.get("color", "")).strip().lower()
        description = "" if item.get("description") is None else str(item.get("description")).strip()
        if not name:
            raise ValueError("Each label entry must have a non-empty name")
        if len(color) != 6 or any(ch not in "0123456789abcdef" for ch in color):
            raise ValueError(f"Label '{name}' must use a 6-character hex color without '#'")
        if name in labels:
            raise ValueError(f"Duplicate label name: {name}")
        labels[name] = {"color": color, "description": description}
    return labels


def infer_repo_slug() -> str:
    result = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    remote = result.stdout.strip()
    if remote.startswith("git@github.com:"):
        slug = remote.removeprefix("git@github.com:")
    elif remote.startswith("https://github.com/"):
        slug = remote.removeprefix("https://github.com/")
    else:
        raise ValueError(f"Unsupported GitHub remote format: {remote}")
    if slug.endswith(".git"):
        slug = slug[:-4]
    return slug


def gh_json(*args: str) -> Any:
    result = subprocess.run(["gh", *args], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def fetch_current_labels(repo: str) -> dict[str, dict[str, str]]:
    payload = gh_json("api", f"repos/{repo}/labels?per_page=100")
    return {
        item["name"]: {
            "color": item["color"].lower(),
            "description": item.get("description") or "",
        }
        for item in payload
    }


def plan_label_sync(
    desired: dict[str, dict[str, str]],
    current: dict[str, dict[str, str]],
    *,
    prune: bool = False,
) -> dict[str, list[dict[str, Any]]]:
    plan = {"create": [], "update": [], "delete": []}
    for name, target in desired.items():
        live = current.get(name)
        if live is None:
            plan["create"].append({"name": name, **target})
        elif live["color"] != target["color"] or live["description"] != target["description"]:
            plan["update"].append({"name": name, "from": live, "to": target})
    if prune:
        for name, live in current.items():
            if name not in desired:
                plan["delete"].append({"name": name, **live})
    return plan


def apply_plan(repo: str, plan: dict[str, list[dict[str, Any]]]) -> None:
    for item in plan["create"]:
        subprocess.run(
            ["gh", "api", "-X", "POST", f"repos/{repo}/labels", "-f", f"name={item['name']}", "-f", f"color={item['color']}", "-f", f"description={item['description']}"],
            check=True,
            capture_output=True,
            text=True,
        )
    for item in plan["update"]:
        subprocess.run(
            ["gh", "api", "-X", "PATCH", f"repos/{repo}/labels/{quote(item['name'], safe='')}", "-f", f"new_name={item['name']}", "-f", f"color={item['to']['color']}", "-f", f"description={item['to']['description']}"],
            check=True,
            capture_output=True,
            text=True,
        )
    for item in plan["delete"]:
        subprocess.run(
            ["gh", "api", "-X", "DELETE", f"repos/{repo}/labels/{quote(item['name'], safe='')}"],
            check=True,
            capture_output=True,
            text=True,
        )


def render_plan(repo: str, plan: dict[str, list[dict[str, Any]]], *, apply: bool, prune: bool) -> None:
    print(f"repo: {repo}")
    print(f"mode: {'apply' if apply else 'dry-run'}")
    print(f"prune: {'yes' if prune else 'no'}")
    if not any(plan.values()):
        print("No label changes required.")
        return
    for kind in ("create", "update", "delete"):
        if not plan[kind]:
            continue
        print(f"{kind.capitalize()}:")
        for item in plan[kind]:
            if kind == "update":
                print(
                    "  - "
                    f"{item['name']} color {item['from']['color']} -> {item['to']['color']}; "
                    f"description {item['from']['description']!r} -> {item['to']['description']!r}"
                )
            else:
                print(f"  - {item['name']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sync GitHub labels from .github/labels.yml")
    parser.add_argument("--repo", help="GitHub repository in owner/name form. Defaults to origin remote.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Apply changes.")
    mode.add_argument("--dry-run", action="store_true", help="Print the sync plan without changing GitHub.")
    parser.add_argument("--prune", action="store_true", help="Delete live labels missing from labels.yml.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo = args.repo or infer_repo_slug()
    desired = load_desired_labels()
    current = fetch_current_labels(repo)
    plan = plan_label_sync(desired, current, prune=args.prune)
    render_plan(repo, plan, apply=args.apply, prune=args.prune)
    if args.apply and any(plan.values()):
        apply_plan(repo, plan)
        print("Label sync applied.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        if exc.stderr:
            sys.stderr.write(exc.stderr)
        raise
