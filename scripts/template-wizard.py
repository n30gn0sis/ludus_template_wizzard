#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import yaml  # type: ignore
except ModuleNotFoundError:
    yaml = None

import json

from template_wizard_common import OS_CHOICES, REQUIRED_VARS, normalize_packages


MANIFEST_PATH = Path("builder.manifest.yaml")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Ludus template manifest entries")
    parser.add_argument("--non-interactive", action="store_true", help="Use CLI flags instead of prompts")
    parser.add_argument("--base-os", choices=sorted(OS_CHOICES.keys()))
    parser.add_argument("--template-name")
    parser.add_argument("--packages", default="", help="Comma-separated packages/software")
    parser.add_argument("--enable-cleanup", action="store_true")
    parser.add_argument("--custom-bootstrap-path", default="")
    parser.add_argument("--output", default=str(MANIFEST_PATH))
    parser.add_argument("--force", action="store_true", help="Overwrite output without confirmation")
    return parser.parse_args()


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def interactive_values() -> dict:
    base_os = ask(f"Base OS ({', '.join(OS_CHOICES.keys())})", "ubuntu")
    template_name = ask("Template name", f"my-{base_os}-template")
    packages = normalize_packages(ask("Packages/software (comma-separated)", ""))
    enable_cleanup = ask("Enable cleanup script? (y/n)", "y").lower() in {"y", "yes"}
    custom_bootstrap_path = ask("Custom bootstrap path (optional)", "")
    return {
        "base_os": base_os,
        "template_name": template_name,
        "packages": packages,
        "enable_cleanup": enable_cleanup,
        "custom_bootstrap_path": custom_bootstrap_path,
    }


def validate_values(values: dict) -> None:
    if values["base_os"] not in OS_CHOICES:
        raise ValueError(f"Unknown OS choice: {values['base_os']}")
    if not values["template_name"]:
        raise ValueError("Template name is required")


def update_bootstrap(values: dict) -> None:
    packages = values["packages"]
    if not packages:
        return

    if values["base_os"] == "ubuntu":
        path = Path("scripts/linux-bootstrap.sh")
        marker = "# TEMPLATE_WIZARD_PACKAGES"
        text = path.read_text()
        if marker not in text:
            text += f"\n{marker}\n"
        install_line = "sudo apt-get install -y " + " ".join(packages)
        text = text.split(marker)[0] + marker + "\n" + install_line + "\n"
        path.write_text(text)
    elif values["base_os"] == "windows2022":
        path = Path("scripts/windows-bootstrap.ps1")
        marker = "# TEMPLATE_WIZARD_PACKAGES"
        text = path.read_text()
        if marker not in text:
            text += f"\n{marker}\n"
        install_lines = [f"Write-Host 'Install {p}'" for p in packages]
        text = text.split(marker)[0] + marker + "\n" + "\n".join(install_lines) + "\n"
        path.write_text(text)


def write_manifest(values: dict, output: Path, force: bool = False) -> None:
    if output.exists() and not force:
        should = ask(f"{output} exists. Overwrite? (y/n)", "n").lower() in {"y", "yes"}
        if not should:
            raise SystemExit("Aborted by user")

    if output.exists():
        raw = output.read_text()
        if yaml:
            data = yaml.safe_load(raw) or {}
        else:
            data = json.loads(raw) if raw.strip() else {}
    else:
        data = {}

    data.setdefault("metadata", {"name": "ludus-template-builder", "version": "0.1.0"})
    data.setdefault("ludus_required_vars", REQUIRED_VARS)
    data.setdefault("templates", [])

    cfg = OS_CHOICES[values["base_os"]]
    new_entry = {
        "name": values["template_name"],
        "file": cfg["template_file"],
        "os_family": cfg["os_family"],
        "automated": True,
    }
    data["templates"] = [t for t in data["templates"] if t.get("name") != values["template_name"]]
    data["templates"].append(new_entry)

    extras = {
        "packages": values["packages"],
        "enable_cleanup": values["enable_cleanup"],
        "custom_bootstrap_path": values["custom_bootstrap_path"],
    }
    data.setdefault("wizard", {})[values["template_name"]] = extras

    if yaml:
        output.write_text(yaml.safe_dump(data, sort_keys=False))
    else:
        output.write_text(json.dumps(data, indent=2))


def main() -> None:
    args = parse_args()
    if args.non_interactive:
        values = {
            "base_os": args.base_os,
            "template_name": args.template_name,
            "packages": normalize_packages(args.packages),
            "enable_cleanup": args.enable_cleanup,
            "custom_bootstrap_path": args.custom_bootstrap_path,
        }
    else:
        values = interactive_values()

    validate_values(values)
    update_bootstrap(values)
    write_manifest(values, Path(args.output), force=args.force)
    print(f"Wrote manifest to {args.output}")


if __name__ == "__main__":
    main()
