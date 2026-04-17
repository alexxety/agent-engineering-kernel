from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "scripts" / "sync_github_labels.py"


def load_module():
    spec = importlib.util.spec_from_file_location("sync_github_labels_module", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SyncGitHubLabelsTests(unittest.TestCase):
    def test_load_desired_labels_rejects_duplicates(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "labels.yml"
            path.write_text(
                """
labels:
  - name: epic
    color: "5319e7"
    description: first
  - name: epic
    color: "0e8a16"
    description: second
""".strip(),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Duplicate label name: epic"):
                module.load_desired_labels(path)

    def test_plan_label_sync_reports_create_update_delete(self) -> None:
        module = load_module()
        desired = {
            "epic": {"color": "5319e7", "description": "Parent issue"},
            "task": {"color": "0e8a16", "description": "Leaf issue"},
        }
        current = {
            "epic": {"color": "000000", "description": "stale"},
            "legacy": {"color": "ffffff", "description": "remove me"},
        }
        plan = module.plan_label_sync(desired, current, prune=True)
        self.assertEqual(
            [{"name": "task", "color": "0e8a16", "description": "Leaf issue"}],
            plan["create"],
        )
        self.assertEqual("epic", plan["update"][0]["name"])
        self.assertEqual("legacy", plan["delete"][0]["name"])


if __name__ == "__main__":
    unittest.main()
