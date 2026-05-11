from __future__ import annotations

import tomllib
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
            "references/AGENTIC_CODING_ORCHESTRATION.md",
            "references/PROJECT_LOCAL_WORKERS.md",
            "references/SUPERPOWERS_SKILL_ORCHESTRATION.md",
            "references/MCP_TOOLING.md",
            "references/BUG_INTAKE.md",
            "references/ENVIRONMENT_PROMOTION.md",
            "references/EXECUTION_SURFACES.md",
            "references/KERNEL_FLEET_SWEEP.md",
            "references/KERNEL_SYNC_POLICY.md",
            "references/KERNEL_UPSTREAM_AWARENESS.md",
            "references/KERNEL_ADOPTION_TASK.md",
            "references/MODEL_ADAPTERS.md",
            "references/RESEARCH_POLICY.md",
            "references/SESSION_ISSUE_SYNC.md",
            "references/GITHUB_DELIVERY.md",
            "scripts/check_kernel_upstream.py",
            "scripts/kernel_fleet_sweep.py",
        ):
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_machine_readable_kernel_parses(self) -> None:
        payload = yaml.safe_load((ROOT / "ENGINEERING_KERNEL.yaml").read_text(encoding="utf-8"))
        self.assertIn("layers", payload)
        self.assertIn("model_adapter_policy", payload)
        self.assertIn("agent_skill_orchestration_policy", payload)
        self.assertIn("agentic_coding_orchestration_policy", payload)
        self.assertIn("project_local_worker_policy", payload)
        self.assertIn("mcp_tooling_policy", payload)
        self.assertIn("research_policy", payload)
        self.assertIn("github_delivery_flow", payload)
        self.assertIn("automatic_bug_intake", payload)
        self.assertIn("execution_surface_policy", payload)
        self.assertIn("environment_promotion_policy", payload)
        self.assertIn("optional_operator_layers", payload)
        self.assertIn("behavioral_overlay_policy", payload)
        self.assertIn("kernel_upstream_awareness_policy", payload)
        self.assertIn("kernel_adoption_task_policy", payload)
        self.assertIn("kernel_fleet_sweep_policy", payload)
        self.assertIn("kernel_sync_policy", payload)
        self.assertIn("session_issue_sync_policy", payload)
        self.assertIn("cutover_entitlement_parity_policy", payload)
        prd_first = payload["prd_first_execution"]
        self.assertIn("baseline_verification", prd_first["order"])
        self.assertIn("post_change_verification", prd_first["order"])
        self.assertIn(
            "capture_smallest_relevant_baseline_verification_before_edits_when_existing_contract_exists",
            prd_first["rules"],
        )
        cutover_policy = payload["cutover_entitlement_parity_policy"]
        self.assertIn("workspace_member", cutover_policy["required_role_matrix"])
        self.assertIn("platform_admin", cutover_policy["required_role_matrix"])
        self.assertIn("command_or_search_palette", cutover_policy["required_surfaces"])
        self.assertIn(
            "do_not_make_new_shell_navigation_admin_ia_or_major_ui_default_until_role_matrix_parity_is_green",
            cutover_policy["default_cutover_rules"],
        )
        skill_policy = payload["agent_skill_orchestration_policy"]
        self.assertEqual(skill_policy["preferred_skill_pack"], "Superpowers")
        self.assertIn("using-superpowers", skill_policy["canonical_skill_triggers"]["project_or_feature_design"])
        self.assertIn(
            "verification-before-completion",
            skill_policy["canonical_skill_triggers"]["completion_claim_or_pr_ready"],
        )
        self.assertIn(
            "project_local_canon_active_prd_and_explicit_user_instructions_override_skill_defaults",
            skill_policy["rules"],
        )
        agentic_policy = payload["agentic_coding_orchestration_policy"]
        self.assertEqual(agentic_policy["concurrency_defaults"]["max_worker_agents_default"], 1)
        self.assertEqual(agentic_policy["concurrency_defaults"]["max_worker_agents_parallel"], 2)
        self.assertEqual(agentic_policy["concurrency_defaults"]["max_open_subagent_threads"], 3)
        self.assertIn(
            "project_local_code_worker_for_project_implementation_and_docs_changes",
            agentic_policy["worker_selection_order"],
        )
        self.assertIn(
            "claude_code_readonly_adapter_only_when_explicitly_requested_or_project_authorized",
            agentic_policy["worker_selection_order"],
        )
        self.assertIn(
            "do_not_rely_on_task_prompt_to_disable_mcp_startup",
            agentic_policy["worker_mcp_rules"],
        )
        self.assertIn(
            "claude_code_one_shot_workers_pass_explicit_empty_mcp_config_and_strict_mcp_config",
            agentic_policy["worker_mcp_rules"],
        )
        self.assertIn(
            "kernel_does_not_prescribe_a_fixed_mcp_server_id_list",
            agentic_policy["worker_mcp_rules"],
        )
        self.assertIn(
            "avoid_parallel_shell_or_tool_wrappers_while_worker_agents_are_active",
            agentic_policy["tool_load_rules"],
        )
        self.assertIn(
            "serialize_git_ref_index_and_worktree_mutating_commands_per_repository",
            agentic_policy["tool_load_rules"],
        )
        self.assertIn(
            "do_not_run_git_fetch_pull_switch_checkout_merge_rebase_branch_delete_or_push_in_parallel_for_the_same_repository",
            agentic_policy["tool_load_rules"],
        )
        self.assertIn(
            "implementation_worker_thread_is_kept_open_only_for_same_patch_review_fix_loop",
            agentic_policy["thread_lifecycle_rules"],
        )
        self.assertIn(
            "reviewer_explorer_and_docs_specialist_threads_are_single_use_by_default",
            agentic_policy["thread_lifecycle_rules"],
        )
        self.assertIn("parent_may_close_thread", agentic_policy["thread_disposition_values"])
        self.assertIn("too_many_open_files", agentic_policy["recovery_triggers"])
        self.assertIn(
            "do_not_edit_runtime_code_or_claim_verification_until_git_status_and_git_diff_check_can_run",
            agentic_policy["recovery_rules"],
        )
        self.assertIn(
            "after_git_ref_lock_race_recover_with_sequential_git_status_fetch_pull_ff_only_and_diff_check",
            agentic_policy["recovery_rules"],
        )
        worker_policy = payload["project_local_worker_policy"]
        self.assertEqual(
            worker_policy["preferred_files"]["project_worker"],
            ".codex/agents/<project_slug>_code_worker.toml",
        )
        self.assertEqual(
            worker_policy["preferred_files"]["optional_project_reviewer"],
            ".codex/agents/<project_slug>_reviewer.toml",
        )
        self.assertEqual(
            worker_policy["preferred_files"]["optional_project_docs_worker"],
            ".codex/agents/<project_slug>_docs_worker.toml",
        )
        self.assertEqual(
            worker_policy["preferred_files"]["optional_claude_code_readonly_wrapper"],
            "scripts/claude-code-readonly-subagent.sh",
        )
        self.assertIn(
            "claude_code_adapter_default_role_is_one_shot_readonly_review_or_design_review",
            worker_policy["selection_rules"],
        )
        self.assertIn(
            "each_project_owns_its_mcp_disable_list",
            worker_policy["worker_mcp_inventory_rules"],
        )
        self.assertIn(
            "start_a_fresh_session_after_agent_config_changes",
            worker_policy["verification_rules"],
        )
        self.assertIn(
            "keep_worker_config_small_and_use_project_docs_skills_runbooks_handoffs_for_domain_knowledge",
            worker_policy["worker_content_rules"],
        )
        self.assertIn(
            "require_thread_disposition_in_worker_final_response",
            worker_policy["worker_content_rules"],
        )
        self.assertIn(
            "disabled_mcp_entries_still_include_command_or_url_transport_to_avoid_invalid_transport_loader_errors",
            worker_policy["worker_content_rules"],
        )
        self.assertIn(
            "claude_code_oauth_backed_local_runs_do_not_use_bare_by_default",
            worker_policy["worker_content_rules"],
        )
        self.assertIn(
            "do_not_copy_project_specific_mcp_ids_or_local_paths_from_another_project",
            worker_policy["worker_content_rules"],
        )
        model_policy = payload["model_adapter_policy"]
        claude_adapter = model_policy["claude_code_subagent_adapter"]
        self.assertEqual(claude_adapter["default_role"], "readonly_one_shot_reviewer_or_design_reviewer")
        self.assertIn("test_planning_before_implementation", claude_adapter["high_leverage_uses"])
        self.assertEqual(claude_adapter["operating_modes"]["design_readonly"]["status"], "enabled_by_default_wrapper")
        self.assertEqual(claude_adapter["operating_modes"]["review_readonly"]["status"], "enabled_by_default_wrapper")
        self.assertEqual(claude_adapter["operating_modes"]["implementation_no_mcp"]["status"], "separate_active_prd_required")
        self.assertEqual(claude_adapter["operating_modes"]["research_mcp_readonly"]["status"], "separate_active_prd_required")
        self.assertEqual(
            claude_adapter["context_policy"],
            "prefer_context_packet_focused_snippets_and_selected_diff_context_before_large_or_whole_files",
        )
        self.assertIn("focused_snippets_or_excerpted_sections", claude_adapter["context_packet_requirements"])
        self.assertIn("explicit_reason_when_whole_large_file_is_needed", claude_adapter["context_packet_requirements"])
        self.assertEqual(claude_adapter["preferred_binary"], "$HOME/.local/bin/claude")
        self.assertEqual(claude_adapter["default_model"], "claude-opus-4-7")
        self.assertEqual(claude_adapter["output_format"], "stream-json")
        self.assertTrue(claude_adapter["verbose_required_for_stream_json"])
        self.assertEqual(claude_adapter["permission_mode"], "dontAsk")
        self.assertIn("plan", claude_adapter["forbidden_permission_modes"])
        self.assertEqual(claude_adapter["mode_tool_allowlists"]["smoke"], [])
        self.assertEqual(claude_adapter["mode_tool_allowlists"]["review-files"], ["Read"])
        self.assertEqual(claude_adapter["mode_tool_allowlists"]["review-repo"], ["Read", "Grep", "Glob"])
        self.assertEqual(claude_adapter["default_mcp_config"], '{"mcpServers":{}}')
        self.assertTrue(claude_adapter["strict_mcp_config_required"])
        self.assertFalse(claude_adapter["bare_mode_default"])
        self.assertEqual(claude_adapter["default_max_budget_usd_by_mode"]["smoke"], 1)
        self.assertEqual(claude_adapter["default_max_budget_usd_by_mode"]["review-files"], 5)
        self.assertEqual(claude_adapter["default_max_budget_usd_by_mode"]["review-repo"], 10)
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
        mcp_policy = payload["mcp_tooling_policy"]
        self.assertIn("structured_external_service_interface", mcp_policy["role"])
        self.assertIn("github_app_installation_token", mcp_policy["identity_boundaries"])
        self.assertIn(
            "prefer_mcp_or_app_connector_for_supported_structured_external_service_operations",
            mcp_policy["rules"],
        )
        self.assertIn(
            "local_cli_tokens_and_mcp_connector_tokens_are_different_identities",
            mcp_policy["rules"],
        )
        environment_promotion_policy = payload["environment_promotion_policy"]
        self.assertEqual(
            environment_promotion_policy["default_environment_classes"],
            ["local", "verify", "staging", "production"],
        )
        self.assertIn(
            "mutating_automated_tests_must_not_run_against_production",
            environment_promotion_policy["rules"],
        )
        self.assertIn(
            "project_canon_must_document_the_production_safe_migration_or_deploy_command_before_production_use",
            environment_promotion_policy["rules"],
        )
        session_issue_sync_policy = payload["session_issue_sync_policy"]
        self.assertEqual(session_issue_sync_policy["closeout_field"], "Issue Sync")
        self.assertEqual(
            session_issue_sync_policy["allowed_values"],
            ["updated", "skipped", "not_applicable"],
        )
        self.assertIn(
            "every_serious_slice_records_issue_sync_closeout_decision",
            session_issue_sync_policy["rules"],
        )
        self.assertIn(
            "prefer_issue_body_updates_for_durable_status_next_steps_verification_and_links",
            session_issue_sync_policy["rules"],
        )
        self.assertIn(
            "weekly_labels_crm_pointers_projects_and_weekly_cadence_are_optional_project_local_policies",
            session_issue_sync_policy["rules"],
        )

    def test_machine_readable_kernel_includes_risk_based_required_ci(self) -> None:
        payload = yaml.safe_load((ROOT / "ENGINEERING_KERNEL.yaml").read_text(encoding="utf-8"))
        execution_policy = payload["execution_surface_policy"]
        rules = execution_policy["rules"]
        self.assertIn(
            "do_not_use_workflow_level_path_filters_or_commit_message_skips_for_required_workflows",
            rules,
        )
        self.assertIn("use_lightweight_classifier_jobs_before_expensive_required_jobs", rules)
        self.assertIn("risk_gate_expensive_required_jobs_with_job_level_if_conditions", rules)
        self.assertIn(
            "force_full_required_ci_for_main_release_manual_scheduled_dependency_workflow_and_explicit_full_ci_override",
            rules,
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
            "templates/project/scripts/claude-code-readonly-subagent.sh",
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

    def test_kernel_docs_and_templates_explain_risk_based_required_ci(self) -> None:
        for rel in (
            "README.md",
            "references/EXECUTION_SURFACES.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            normalized = content.lower()
            self.assertIn("risk-based", normalized, rel)
            self.assertIn("job-level", normalized, rel)
            self.assertIn("required check", normalized, rel)
            self.assertIn("pending", normalized, rel)
            self.assertIn("full-ci", normalized, rel)

    def test_kernel_docs_and_templates_mention_environment_promotion(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/ENVIRONMENT_PROMOTION.md",
            "references/EXECUTION_SURFACES.md",
            "references/BOOTSTRAP.md",
            "references/GITHUB_DELIVERY.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/docs/PRD_TEMPLATE.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("local", content.lower(), rel)
            self.assertIn("verify", content.lower(), rel)
            self.assertIn("staging", content.lower(), rel)
            self.assertIn("production", content.lower(), rel)
            if rel != "references/GITHUB_DELIVERY.md":
                self.assertIn("production secrets", content.lower(), rel)
                self.assertIn("mutating", content.lower(), rel)

    def test_kernel_docs_and_templates_mention_cutover_entitlement_parity(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/BOOTSTRAP.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/docs/PRD_TEMPLATE.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            normalized = content.lower()
            self.assertIn("cutover", normalized, rel)
            self.assertIn("entitlement", normalized, rel)
            self.assertIn("role-matrix", normalized, rel)
            self.assertIn("default", normalized, rel)

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

    def test_kernel_docs_and_templates_mention_mcp_tooling_policy(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/MCP_TOOLING.md",
            "references/GITHUB_DELIVERY.md",
            "references/BOOTSTRAP.md",
            "references/MODEL_ADAPTERS.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/docs/PRD_TEMPLATE.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("MCP", content, rel)
            self.assertIn("App connector", content, rel)
            self.assertIn("GitHub App", content, rel)
            self.assertIn("gh", content, rel)
            self.assertIn("different identities", content, rel)

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

    def test_kernel_docs_and_templates_mention_session_issue_sync(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/SESSION_ISSUE_SYNC.md",
            "references/BOOTSTRAP.md",
            "references/GITHUB_DELIVERY.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/docs/PRD_TEMPLATE.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("Issue Sync", content, rel)
            self.assertIn("updated", content, rel)
            self.assertIn("skipped", content, rel)
            self.assertIn("not_applicable", content, rel)
            self.assertIn("issue body", content.lower(), rel)

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

    def test_kernel_docs_and_templates_mention_superpowers_skill_orchestration(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/SUPERPOWERS_SKILL_ORCHESTRATION.md",
            "references/BOOTSTRAP.md",
            "references/MODEL_ADAPTERS.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
            "templates/project/docs/PRD_TEMPLATE.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("Superpowers", content, rel)
            self.assertIn("using-superpowers", content, rel)
            self.assertIn("verification-before-completion", content, rel)
            self.assertIn("project canon", content, rel)

    def test_kernel_docs_and_templates_mention_agentic_coding_orchestration(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/AGENTIC_CODING_ORCHESTRATION.md",
            "references/PROJECT_LOCAL_WORKERS.md",
            "templates/project/AGENTS.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("orchestrator", content.lower(), rel)
            self.assertIn("worker", content.lower(), rel)
            self.assertIn("reviewer", content.lower(), rel)
            self.assertIn("Too many open files", content, rel)
            self.assertIn("git status --short --branch", content, rel)
            self.assertIn("parallel", content.lower(), rel)

    def test_kernel_docs_and_templates_serialize_git_ref_operations(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/GITHUB_DELIVERY.md",
            "references/AGENTIC_CODING_ORCHESTRATION.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("git fetch", content, rel)
            self.assertIn("git pull", content, rel)
            self.assertIn("git diff --check", content, rel)
            self.assertIn("parallel", content.lower(), rel)
            self.assertIn("same repo", content.lower(), rel)

    def test_kernel_docs_and_templates_mention_claude_code_adapter(self) -> None:
        for rel in (
            "README.md",
            "SKILL.md",
            "references/MODEL_ADAPTERS.md",
            "references/AGENTIC_CODING_ORCHESTRATION.md",
            "references/PROJECT_LOCAL_WORKERS.md",
            "templates/project/README.md",
            "templates/project/AGENTS.md",
            "templates/project/CONTRIBUTING.md",
            "docs/claude-code-subagent-canon-prd-2026-05-02.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("Claude Code", content, rel)
            self.assertIn("MCP", content, rel)
            self.assertIn("Read", content, rel)
            self.assertIn("design_readonly", content, rel)
            self.assertIn("review_readonly", content, rel)
            self.assertIn("context packet", content.lower(), rel)
            if rel != "templates/project/README.md":
                self.assertIn("Grep", content, rel)
                self.assertIn("Glob", content, rel)
            self.assertIn("fallback", content.lower(), rel)

    def test_project_local_worker_templates_parse_and_use_project_mcp_inventory(self) -> None:
        config = tomllib.loads((ROOT / "templates/project/.codex/config.toml").read_text(encoding="utf-8"))
        self.assertIn("project_code_worker", config["agents"])

        worker_path = ROOT / "templates/project/.codex/agents/project_code_worker.toml"
        worker_content = worker_path.read_text(encoding="utf-8")
        worker = tomllib.loads(worker_content)
        self.assertEqual(worker["name"], "project_code_worker")
        self.assertNotIn("mcp_servers", worker)
        self.assertIn("<server_id_from_your_config>", worker_content)
        self.assertIn("Copy real transport fields from the MCP config", worker_content)
        self.assertNotIn("telegram-mcp", worker_content)
        self.assertNotIn("/Users/", worker_content)
        self.assertIn("NEEDS_CONTEXT", worker["developer_instructions"])
        self.assertIn("repo-local skills, runbooks, README files, and handoffs", worker["developer_instructions"])
        self.assertIn("thread_disposition", worker["developer_instructions"])

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
