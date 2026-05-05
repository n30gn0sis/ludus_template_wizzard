"""Shared constants/helpers for template validation and generation."""
from __future__ import annotations

from typing import Iterable

REQUIRED_VARS = [
    "proxmox_url",
    "proxmox_host",
    "proxmox_username",
    "proxmox_password",
    "proxmox_storage_pool",
    "proxmox_storage_format",
    "proxmox_skip_tls_verify",
    "proxmox_pool",
    "iso_storage_pool",
    "ansible_home",
    "ludus_nat_interface",
]

OS_CHOICES = {
    "ubuntu": {
        "os_family": "linux",
        "template_file": "my-ubuntu-template.pkr.hcl",
    },
    "windows2022": {
        "os_family": "windows",
        "template_file": "my-win2022-template.pkr.hcl",
    },
}


def normalize_packages(raw_values: Iterable[str] | str | None) -> list[str]:
    """Trim/dedupe package names while preserving input order."""
    if raw_values is None:
        return []

    if isinstance(raw_values, str):
        candidates = raw_values.split(",")
    else:
        candidates = []
        for value in raw_values:
            candidates.extend(str(value).split(","))

    normalized: list[str] = []
    seen = set()
    for item in candidates:
        package = item.strip()
        if not package:
            continue
        key = package.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(package)
    return normalized
