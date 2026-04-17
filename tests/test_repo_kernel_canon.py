from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent


class RepoKernelCanonTests(unittest.TestCase):
    def test_repo_has_expected_top_level_health_files(self) -> None:
        for rel in (
            "README.md",
            "CONTRIBUTING.md",
            "LICENSE",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "SKILL.md",
            "ENGINEERING_KERNEL.yaml",
            "agents/openai.yaml",
            "scripts/sync_github_labels.py",
            "references/BOOTSTRAP.md",
            "references/BUG_INTAKE.md",
            "references/EXECUTION_SURFACES.md",
            "references/KERNEL_SYNC_POLICY.md",
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
        self.assertIn("automatic_bug_intake", payload)
        self.assertIn("execution_surface_policy", payload)
        self.assertIn("kernel_sync_policy", payload)

    def test_project_templates_include_minimal_core(self) -> None:
        for rel in (
            "templates/project/AGENTS.md",
            "templates/project/README.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/CODE_OF_CONDUCT.md",
            "templates/project/SECURITY.md",
            "templates/project/.github/CODEOWNERS",
            "templates/project/.github/labels.yml",
            "templates/project/.github/pull_request_template.md",
            "templates/project/scripts/sync_github_labels.py",
            "templates/project/docs/PRD_TEMPLATE.md",
        ):
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_root_repo_github_health_files_exist(self) -> None:
        for rel in (
            ".github/CODEOWNERS",
            ".github/labels.yml",
            ".github/ISSUE_TEMPLATE/config.yml",
            ".github/ISSUE_TEMPLATE/epic.yml",
            ".github/ISSUE_TEMPLATE/task.yml",
            ".github/ISSUE_TEMPLATE/bug.yml",
            ".github/pull_request_template.md",
        ):
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_issue_and_label_templates_parse(self) -> None:
        for rel in (
            "agents/openai.yaml",
            ".github/labels.yml",
            ".github/ISSUE_TEMPLATE/config.yml",
            ".github/ISSUE_TEMPLATE/epic.yml",
            ".github/ISSUE_TEMPLATE/task.yml",
            ".github/ISSUE_TEMPLATE/bug.yml",
            "templates/project/.github/labels.yml",
            "templates/project/.github/ISSUE_TEMPLATE/config.yml",
            "templates/project/.github/ISSUE_TEMPLATE/epic.yml",
            "templates/project/.github/ISSUE_TEMPLATE/task.yml",
            "templates/project/.github/ISSUE_TEMPLATE/bug.yml",
        ):
            payload = yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))
            self.assertIsNotNone(payload, rel)

    def test_kernel_docs_and_templates_mention_bug_intake_canon(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/BUG_INTAKE.md",
            "references/EXECUTION_SURFACES.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            if "EXECUTION_SURFACES" in rel:
                self.assertIn("local", content.lower(), rel)
                self.assertIn("GitHub Actions", content, rel)
                continue
            self.assertIn("fingerprint", content, rel)
            self.assertIn("raw logs", content, rel)

    def test_kernel_docs_and_templates_mention_local_first_execution(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/EXECUTION_SURFACES.md",
            "references/BOOTSTRAP.md",
            "references/GITHUB_DELIVERY.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("local", content.lower(), rel)
            self.assertIn("GitHub Actions", content, rel)

    def test_kernel_docs_and_templates_mention_shell_safe_gh_delivery(self) -> None:
        for rel in (
            "README.md",
            "references/GITHUB_DELIVERY.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("--body-file", content, rel)
            self.assertIn("heredoc", content, rel)

    def test_kernel_docs_and_templates_mention_kernel_sync_review(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/KERNEL_SYNC_POLICY.md",
            "references/BOOTSTRAP.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/docs/PRD_TEMPLATE.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("kernel", content.lower(), rel)
            self.assertIn("kernel_sync_review", content, rel)
            self.assertIn("Kernel Impact", content, rel)


if __name__ == "__main__":
    unittest.main()
