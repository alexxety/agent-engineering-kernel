from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "scripts" / "check_kernel_upstream.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_kernel_upstream_module", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class KernelUpstreamCheckTests(unittest.TestCase):
    def test_build_result_reports_not_configured_without_metadata(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            result = module.build_result(Path(tmp) / ".kernel" / "upstream.json")
        self.assertEqual(result["status"], "not_configured")

    def test_build_result_reports_current_when_commits_match(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            metadata = Path(tmp) / "upstream.json"
            metadata.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "protocol": "kernel_upstream_check",
                        "kernel_repo": "https://github.com/alexxety/agent-engineering-kernel.git",
                        "kernel_default_branch": "main",
                        "pinned_commit": "abc123",
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(module, "resolve_remote_head", return_value="abc123"):
                result = module.build_result(metadata)
        self.assertEqual(result["status"], "current")
        self.assertEqual(result["remote_commit"], "abc123")

    def test_build_result_reports_update_available_when_commits_differ(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            metadata = Path(tmp) / "upstream.json"
            metadata.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "protocol": "kernel_upstream_check",
                        "kernel_repo": "https://github.com/alexxety/agent-engineering-kernel.git",
                        "kernel_default_branch": "main",
                        "pinned_commit": "abc123",
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(module, "resolve_remote_head", return_value="def456"):
                result = module.build_result(metadata)
        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["remote_commit"], "def456")

    def test_main_emits_json(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            metadata = Path(tmp) / "upstream.json"
            metadata.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "protocol": "kernel_upstream_check",
                        "kernel_repo": "https://github.com/alexxety/agent-engineering-kernel.git",
                        "kernel_default_branch": "main",
                        "pinned_commit": "abc123",
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(module, "resolve_remote_head", return_value="abc123"):
                with mock.patch("sys.argv", ["check_kernel_upstream.py", "--metadata", str(metadata), "--json"]):
                    with mock.patch("builtins.print") as print_mock:
                        exit_code = module.main()
        self.assertEqual(exit_code, 0)
        printed = print_mock.call_args[0][0]
        self.assertEqual(json.loads(printed)["status"], "current")
