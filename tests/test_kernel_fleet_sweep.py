from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "scripts" / "kernel_fleet_sweep.py"


def load_module():
    spec = importlib.util.spec_from_file_location("kernel_fleet_sweep_module", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class KernelFleetSweepTests(unittest.TestCase):
    def test_load_repo_paths_from_json_mapping(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "fleet-repos.json"
            config.write_text(json.dumps({"repos": ["/tmp/a", "/tmp/b"]}), encoding="utf-8")
            repos = module.load_repo_paths_from_config(config)
        self.assertEqual(repos, ["/tmp/a", "/tmp/b"])

    def test_load_repo_paths_from_plain_text_ignores_comments(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "fleet-repos.txt"
            config.write_text("# comment\n\n/tmp/a\n/tmp/b\n", encoding="utf-8")
            repos = module.load_repo_paths_from_config(config)
        self.assertEqual(repos, ["/tmp/a", "/tmp/b"])

    def test_select_checker_prefers_consumer_repo_script(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            scripts_dir = repo / "scripts"
            scripts_dir.mkdir()
            checker = scripts_dir / "check_kernel_upstream.py"
            checker.write_text("print('ok')\n", encoding="utf-8")
            selected, source = module.select_checker(repo)
        self.assertEqual(selected, checker)
        self.assertEqual(source, "consumer_repo")

    def test_build_fleet_result_aggregates_status_counts(self) -> None:
        module = load_module()
        repos = [Path("/tmp/a"), Path("/tmp/b"), Path("/tmp/c")]
        with mock.patch.object(
            module,
            "inspect_repo",
            side_effect=[
                {"repo_path": "/tmp/a", "status": "current", "checker_source": "consumer_repo"},
                {"repo_path": "/tmp/b", "status": "update_available", "checker_source": "consumer_repo"},
                {"repo_path": "/tmp/c", "status": "unknown", "checker_source": "kernel_fallback", "error": "boom"},
            ],
        ):
            result = module.build_fleet_result(repos, None)
        self.assertEqual(result["repo_count"], 3)
        self.assertEqual(result["needs_attention_count"], 2)
        self.assertEqual(result["status_counts"]["current"], 1)
        self.assertEqual(result["status_counts"]["update_available"], 1)
        self.assertEqual(result["status_counts"]["unknown"], 1)

    def test_main_returns_nonzero_when_attention_required(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            with mock.patch.object(
                module,
                "build_fleet_result",
                return_value={
                    "repo_count": 1,
                    "needs_attention_count": 1,
                    "status_counts": {
                        "current": 0,
                        "update_available": 1,
                        "not_configured": 0,
                        "unknown": 0,
                    },
                    "config_path": None,
                    "repos": [
                        {
                            "repo_path": str(repo),
                            "status": "update_available",
                            "checker_source": "consumer_repo",
                            "pinned_commit": "abc",
                            "remote_commit": "def",
                        }
                    ],
                },
            ):
                with mock.patch.object(module, "collect_repo_paths", return_value=[repo]):
                    with mock.patch("sys.argv", ["kernel_fleet_sweep.py", str(repo), "--fail-if-attention-required"]):
                        with mock.patch("builtins.print"):
                            exit_code = module.main()
        self.assertEqual(exit_code, 2)
