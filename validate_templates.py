#!/usr/bin/env python3
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "scripts"))
from template_wizard_common import REQUIRED_VARS  # noqa: E402

for file in Path('.').glob('*.pkr.hcl'):
    text = file.read_text()
    assert ".pkr." in file.name, f"{file}: missing .pkr. in filename"
    for var in REQUIRED_VARS:
        assert f'variable "{var}"' in text, f"{file}: missing required var {var}"
    assert re.search(r'-template', text), f"{file}: missing -template string"

print("All template checks passed")
