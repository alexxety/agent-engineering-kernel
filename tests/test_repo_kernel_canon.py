from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent


class RepoKernelCanonTests(unittest.TestCase):
    def test_repo_has_expected_top_level_health_files(self) -> None:
        for rel in (
            "README.md",
            "LICENSE",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "SKILL.md",
            "ENGINEERING_KERNEL.yaml",
            "references/BOOTSTRAP.md",
            "references/MODEL_ADAPTERS.md",
            "references/RESEARCH_POLICY.md",
            "references/GITHUB_DELIVERY.md",
        ):
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_machine_readable_kernel_parses(self) -> None:
        payload = yaml.safe_load((ROOT / "ENGINEERING_KERNEL.yaml").read_text(encoding="utf-8"))
        self.assertIn("layers", payload)
        self.assertIn("model_adapter_policy", payload)
        self.assertIn("research_policy", payload)
        self.assertIn("github_delivery_flow", payload)

    def test_project_templates_include_minimal_core(self) -> None:
        for rel in (
            "templates/project/AGENTS.md",
            "templates/project/README.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/.github/CODEOWNERS",
            "templates/project/.github/labels.yml",
            "templates/project/.github/pull_request_template.md",
            "templates/project/docs/PRD_TEMPLATE.md",
        ):
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_issue_and_label_templates_parse(self) -> None:
        for rel in (
            "templates/project/.github/labels.yml",
            "templates/project/.github/ISSUE_TEMPLATE/config.yml",
            "templates/project/.github/ISSUE_TEMPLATE/epic.yml",
            "templates/project/.github/ISSUE_TEMPLATE/task.yml",
            "templates/project/.github/ISSUE_TEMPLATE/bug.yml",
        ):
            payload = yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))
            self.assertIsNotNone(payload, rel)


if __name__ == "__main__":
    unittest.main()
