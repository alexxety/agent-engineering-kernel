from __future__ import annotations

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "scripts" / "link_github_sub_issue.py"


def load_module():
    spec = importlib.util.spec_from_file_location("link_github_sub_issue", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class LinkGitHubSubIssueTests(unittest.TestCase):
    def test_link_sub_issue_resolves_node_ids_before_graphql_mutation(self) -> None:
        module = load_module()
        responses = [
            subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout=json.dumps({"id": "PARENT_NODE", "number": 101, "title": "Parent"}),
                stderr="",
            ),
            subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout=json.dumps({"id": "CHILD_NODE", "number": 202, "title": "Child"}),
                stderr="",
            ),
            subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout=json.dumps(
                    {
                        "data": {
                            "addSubIssue": {
                                "issue": {"number": 101},
                                "subIssue": {"number": 202},
                            }
                        }
                    }
                ),
                stderr="",
            ),
        ]

        with patch.object(module.subprocess, "run", side_effect=responses) as run_mock:
            result = module.link_sub_issue("owner/repo", 101, 202)

        self.assertEqual(result["parent_issue_node_id"], "PARENT_NODE")
        self.assertEqual(result["child_issue_node_id"], "CHILD_NODE")
        graphql_call = run_mock.call_args_list[-1].args[0]
        self.assertIn("graphql", graphql_call)
        self.assertIn("issueId=PARENT_NODE", graphql_call)
        self.assertIn("subIssueId=CHILD_NODE", graphql_call)
        self.assertNotIn("subIssueId=202", graphql_call)


if __name__ == "__main__":
    unittest.main()
