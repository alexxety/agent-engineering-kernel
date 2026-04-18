#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_ROOT = ROOT / "templates" / "project"


def iter_template_files(root: Path = TEMPLATES_ROOT) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        files.append(path)
    return sorted(files)


def build_replacements() -> dict[str, str]:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return {
        "__KERNEL_REPO_URL__": "https://github.com/alexxety/agent-engineering-kernel.git",
        "__KERNEL_PINNED_COMMIT__": completed.stdout.strip(),
    }


def render_content(source: Path, replacements: dict[str, str]) -> str:
    content = source.read_text(encoding="utf-8")
    for needle, value in replacements.items():
        content = content.replace(needle, value)
    return content


def copy_templates(target: Path, *, apply: bool, force: bool) -> tuple[list[str], list[str]]:
    created: list[str] = []
    skipped: list[str] = []
    replacements = build_replacements()
    for source in iter_template_files():
        rel = source.relative_to(TEMPLATES_ROOT)
        destination = target / rel
        if destination.exists() and not force:
            skipped.append(str(rel))
            continue
        created.append(str(rel))
        if apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.suffix in {".json", ".md", ".yml", ".yaml", ".py"}:
                destination.write_text(render_content(source, replacements), encoding="utf-8")
            else:
                shutil.copy2(source, destination)
    return created, skipped


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bootstrap the minimal engineering kernel into a target repository.")
    parser.add_argument("--target", required=True, help="Absolute or relative path to the target repository.")
    parser.add_argument("--apply", action="store_true", help="Write files. Default is dry-run.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    target = Path(args.target).expanduser().resolve()
    created, skipped = copy_templates(target, apply=args.apply, force=args.force)
    print(f"target: {target}")
    print(f"mode: {'apply' if args.apply else 'dry-run'}")
    print(f"force: {'yes' if args.force else 'no'}")
    if created:
        print("planned:")
        for item in created:
            print(f"  - {item}")
    else:
        print("planned: none")
    if skipped:
        print("skipped:")
        for item in skipped:
            print(f"  - {item}")
    else:
        print("skipped: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
