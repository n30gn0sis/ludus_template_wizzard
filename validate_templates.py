#!/usr/bin/env python3
import re
from pathlib import Path

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

for file in Path('.').glob('*.pkr.hcl'):
    text = file.read_text()
    assert ".pkr." in file.name, f"{file}: missing .pkr. in filename"
    for var in REQUIRED_VARS:
        assert f'variable "{var}"' in text, f"{file}: missing required var {var}"
    assert re.search(r'-template', text), f"{file}: missing -template string"

print("All template checks passed")
