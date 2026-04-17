#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_ROOT = ROOT / "templates" / "project"


def iter_template_files(root: Path = TEMPLATES_ROOT) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def copy_templates(target: Path, *, apply: bool, force: bool) -> tuple[list[str], list[str]]:
    created: list[str] = []
    skipped: list[str] = []
    for source in iter_template_files():
        rel = source.relative_to(TEMPLATES_ROOT)
        destination = target / rel
        if destination.exists() and not force:
            skipped.append(str(rel))
            continue
        created.append(str(rel))
        if apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
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
