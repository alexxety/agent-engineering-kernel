#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess


GRAPHQL_MUTATION = """
mutation($issueId:ID!,$subIssueId:ID!){
  addSubIssue(input:{issueId:$issueId,subIssueId:$subIssueId}) {
    issue { number }
    subIssue { number }
  }
}
""".strip()


def run_json(command: list[str]) -> dict:
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "command failed")
    payload = json.loads(completed.stdout)
    if not isinstance(payload, dict):
        raise ValueError("expected JSON object")
    return payload


def resolve_issue_node_id(repo: str, number: int) -> str:
    payload = run_json(
        [
            "gh",
            "issue",
            "view",
            str(number),
            "--repo",
            repo,
            "--json",
            "id,number,title",
        ]
    )
    node_id = str(payload.get("id") or "").strip()
    if not node_id:
        raise ValueError(f"missing issue node id for {repo}#{number}")
    return node_id


def link_sub_issue(repo: str, parent_number: int, child_number: int) -> dict:
    parent_node_id = resolve_issue_node_id(repo, parent_number)
    child_node_id = resolve_issue_node_id(repo, child_number)
    payload = run_json(
        [
            "gh",
            "api",
            "graphql",
            "-f",
            f"query={GRAPHQL_MUTATION}",
            "-F",
            f"issueId={parent_node_id}",
            "-F",
            f"subIssueId={child_node_id}",
        ]
    )
    return {
        "repo": repo,
        "parent_issue_number": parent_number,
        "child_issue_number": child_number,
        "parent_issue_node_id": parent_node_id,
        "child_issue_node_id": child_node_id,
        "result": payload,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Link a GitHub sub-issue safely from normal issue numbers. "
            "This avoids the REST sub_issue_id trap, where the endpoint expects the child database id, not #issue_number."
        )
    )
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--parent", required=True, type=int, help="Parent issue number")
    parser.add_argument("--child", required=True, type=int, help="Child issue number")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = link_sub_issue(args.repo, args.parent, args.child)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            f"linked {result['repo']}#{result['child_issue_number']} "
            f"as sub-issue of #{result['parent_issue_number']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
