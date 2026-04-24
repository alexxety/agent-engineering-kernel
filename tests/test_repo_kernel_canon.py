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
            "scripts/link_github_sub_issue.py",
            "references/BOOTSTRAP.md",
            "references/BEHAVIORAL_OVERLAY.md",
            "references/BUG_INTAKE.md",
            "references/EXECUTION_SURFACES.md",
            "references/KERNEL_FLEET_SWEEP.md",
            "references/KERNEL_SYNC_POLICY.md",
            "references/KERNEL_UPSTREAM_AWARENESS.md",
            "references/KERNEL_ADOPTION_TASK.md",
            "references/MODEL_ADAPTERS.md",
            "references/RESEARCH_POLICY.md",
            "references/GITHUB_DELIVERY.md",
            "scripts/check_kernel_upstream.py",
            "scripts/kernel_fleet_sweep.py",
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
        self.assertIn("optional_operator_layers", payload)
        self.assertIn("behavioral_overlay_policy", payload)
        self.assertIn("kernel_upstream_awareness_policy", payload)
        self.assertIn("kernel_adoption_task_policy", payload)
        self.assertIn("kernel_fleet_sweep_policy", payload)
        self.assertIn("kernel_sync_policy", payload)
        prd_first = payload["prd_first_execution"]
        self.assertIn("baseline_verification", prd_first["order"])
        self.assertIn("post_change_verification", prd_first["order"])
        self.assertIn(
            "capture_smallest_relevant_baseline_verification_before_edits_when_existing_contract_exists",
            prd_first["rules"],
        )
        research_policy = payload["research_policy"]
        self.assertIn("slice_classification", research_policy)
        self.assertEqual(
            research_policy["slice_classification"]["allowed_values"],
            ["repo_local_slice", "external_contract_slice"],
        )
        self.assertIn("external_source_of_truth_matrix", research_policy)
        self.assertEqual(
            research_policy["external_source_of_truth_matrix"]["required_for"],
            ["external_contract_slice"],
        )
        self.assertIn(
            "external_contract_slice_requires_fresh_external_research_before_code_or_docs_land",
            research_policy["rules"],
        )
        self.assertIn(
            "research_is_tavily_search_first_not_tavily_research_first",
            research_policy["rules"],
        )
        self.assertIn(
            "use_tavily_research_only_when_tavily_search_known_docs_and_manual_synthesis_are_insufficient",
            research_policy["rules"],
        )
        self.assertIn(
            "every_external_contract_slice_must_record_an_external_source_of_truth_matrix_before_implementation_lands",
            research_policy["rules"],
        )

    def test_kernel_readme_and_templates_document_pre_change_baseline_rule(self) -> None:
        readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("baseline verification when an existing contract already exists", readme_text)
        self.assertIn("post-change verification", readme_text)

        agents_text = (ROOT / "templates" / "project" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("capture baseline verification when an existing deterministic contract already exists", agents_text)
        self.assertIn("## Minimum verification contract", agents_text)
        self.assertIn("bugfixes should prefer a reproducer before the fix", agents_text)

        contributing_text = (ROOT / "templates" / "project" / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("baseline verification", contributing_text)
        self.assertIn("Verification timing", contributing_text)
        self.assertIn("refactors should prefer before/after equivalence checks", contributing_text)

        delivery_text = (ROOT / "references" / "GITHUB_DELIVERY.md").read_text(encoding="utf-8")
        self.assertIn("Capture baseline verification when an existing deterministic contract already exists", delivery_text)
        self.assertIn("baseline-before-edits and post-change verification are different moments", delivery_text)

    def test_project_templates_include_minimal_core(self) -> None:
        for rel in (
            "templates/project/AGENTS.md",
            "templates/project/README.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/CODE_OF_CONDUCT.md",
            "templates/project/SECURITY.md",
            "templates/project/.kernel/upstream.json",
            "templates/project/.github/CODEOWNERS",
            "templates/project/.github/labels.yml",
            "templates/project/.github/pull_request_template.md",
            "templates/project/scripts/check_kernel_upstream.py",
            "templates/project/scripts/link_github_sub_issue.py",
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

    def test_kernel_docs_and_templates_treat_github_as_coordinator_not_default_compute(self) -> None:
        for rel in (
            "README.md",
            "references/EXECUTION_SURFACES.md",
            "references/BOOTSTRAP.md",
            "references/GITHUB_DELIVERY.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("GitHub coordinates", content, rel)
            self.assertIn("owned compute", content, rel)
            self.assertIn("paid GitHub-hosted", content, rel)
            self.assertIn("dependency cache", content, rel)

    def test_kernel_workflow_uses_owned_compute_runner(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "tests.yml").read_text(encoding="utf-8")
        self.assertIn("runs-on: [self-hosted, agent-kernel-ci]", workflow)
        self.assertIn('python: ["python3.11", "python3.12"]', workflow)
        self.assertNotIn("ubuntu-latest", workflow)
        self.assertNotIn("actions/setup-python", workflow)
        self.assertNotIn("cache: pip", workflow)

    def test_kernel_docs_and_templates_mention_research_boundary(self) -> None:
        for rel in (
            "README.md",
            "references/RESEARCH_POLICY.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("repo_local_slice", content, rel)
            self.assertIn("external_contract_slice", content, rel)
            self.assertIn("fresh external research", content, rel)
            self.assertIn("Tavily Search", content, rel)
            self.assertIn("Tavily Research", content, rel)
            self.assertIn("external_source_of_truth_matrix", content, rel)

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
            self.assertIn("sub_issue_id", content, rel)
            self.assertIn("database id", content, rel)

    def test_kernel_docs_and_templates_mention_optional_github_projects(self) -> None:
        for rel in (
            "README.md",
            "references/GITHUB_DELIVERY.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("GitHub Projects", content, rel)
            self.assertIn("optional", content.lower(), rel)

    def test_kernel_docs_and_templates_mention_kernel_sync_review(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/KERNEL_SYNC_POLICY.md",
            "references/KERNEL_UPSTREAM_AWARENESS.md",
            "references/BOOTSTRAP.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/README.md",
            "templates/project/docs/PRD_TEMPLATE.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("kernel", content.lower(), rel)
            self.assertIn("kernel_upstream_check", content, rel)
            if rel != "references/KERNEL_UPSTREAM_AWARENESS.md":
                self.assertIn("kernel_sync_review", content, rel)
                self.assertIn("Kernel Impact", content, rel)

    def test_kernel_docs_and_templates_mention_external_source_of_truth_matrix(self) -> None:
        for rel in (
            "README.md",
            "references/RESEARCH_POLICY.md",
            "references/BOOTSTRAP.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/docs/PRD_TEMPLATE.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("external_source_of_truth_matrix", content, rel)

    def test_kernel_docs_mention_kernel_fleet_sweep(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/KERNEL_UPSTREAM_AWARENESS.md",
            "references/KERNEL_FLEET_SWEEP.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("kernel_fleet_sweep", content, rel)

    def test_kernel_docs_and_templates_mention_behavioral_overlay_policy(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/BEHAVIORAL_OVERLAY.md",
            "references/MODEL_ADAPTERS.md",
            "references/BOOTSTRAP.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("thin", content.lower(), rel)
            self.assertIn("Cursor", content, rel)
            self.assertIn("CLAUDE.md", content, rel)

    def test_kernel_docs_and_templates_mention_kernel_adoption_task(self) -> None:
        for rel in (
            "README.md",
            "references/KERNEL_UPSTREAM_AWARENESS.md",
            "references/KERNEL_ADOPTION_TASK.md",
            "references/GITHUB_DELIVERY.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/docs/PRD_TEMPLATE.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("kernel_adoption_task", content, rel)
            self.assertIn("adopt_now", content, rel)
            self.assertIn("defer", content, rel)


if __name__ == "__main__":
    unittest.main()
