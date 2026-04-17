from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = ROOT / "scripts" / "bootstrap_project_kernel.py"


def load_module():
    spec = importlib.util.spec_from_file_location("bootstrap_project_kernel_module", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BootstrapProjectKernelTests(unittest.TestCase):
    def test_iter_template_files_contains_expected_core_files(self) -> None:
        module = load_module()
        files = {str(path.relative_to(module.TEMPLATES_ROOT)) for path in module.iter_template_files()}
        self.assertIn("AGENTS.md", files)
        self.assertIn("CODE_OF_CONDUCT.md", files)
        self.assertIn("SECURITY.md", files)
        self.assertIn(".github/ISSUE_TEMPLATE/epic.yml", files)
        self.assertIn(".github/pull_request_template.md", files)
        self.assertIn("scripts/sync_github_labels.py", files)
        self.assertIn("docs/PRD_TEMPLATE.md", files)

    def test_copy_templates_dry_run_skips_existing_without_force(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            existing = target / "AGENTS.md"
            existing.parent.mkdir(parents=True, exist_ok=True)
            existing.write_text("existing", encoding="utf-8")
            created, skipped = module.copy_templates(target, apply=False, force=False)
            self.assertIn("AGENTS.md", skipped)
            self.assertIn("CONTRIBUTING.md", created)

    def test_copy_templates_apply_writes_files(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            created, skipped = module.copy_templates(target, apply=True, force=False)
            self.assertFalse(skipped)
            self.assertIn("README.md", created)
            self.assertTrue((target / "README.md").exists())
            self.assertTrue((target / "CODE_OF_CONDUCT.md").exists())
            self.assertTrue((target / "SECURITY.md").exists())
            self.assertTrue((target / ".github" / "labels.yml").exists())
            self.assertTrue((target / "scripts" / "sync_github_labels.py").exists())
            self.assertIn("fingerprint", (target / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertIn("raw logs", (target / "AGENTS.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
