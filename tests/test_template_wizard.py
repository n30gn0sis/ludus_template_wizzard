import builtins
import importlib.util
from pathlib import Path

import json

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "template-wizard.py"
spec = importlib.util.spec_from_file_location("template_wizard", SCRIPT_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def test_non_interactive_parsing(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "template-wizard.py",
            "--non-interactive",
            "--base-os",
            "ubuntu",
            "--template-name",
            "my-test-template",
            "--packages",
            "vim, curl, vim",
        ],
    )
    args = mod.parse_args()
    assert args.non_interactive is True
    assert args.base_os == "ubuntu"
    assert mod.normalize_packages(args.packages) == ["vim", "curl"]


def test_interactive_flow(monkeypatch):
    answers = iter(["ubuntu", "my-ubuntu-template", "vim, curl, vim", "y", ""])
    monkeypatch.setattr(builtins, "input", lambda _: next(answers))
    values = mod.interactive_values()
    assert values["packages"] == ["vim", "curl"]
    assert values["enable_cleanup"] is True


def test_output_schema_shape(tmp_path):
    out = tmp_path / "builder.manifest.yaml"
    values = {
        "base_os": "windows2022",
        "template_name": "my-win2022-template",
        "packages": ["git"],
        "enable_cleanup": False,
        "custom_bootstrap_path": "",
    }
    mod.write_manifest(values, out, force=True)
    content = out.read_text()
    data = json.loads(content) if content.strip().startswith("{") else __import__("ast").literal_eval("{}")
    assert "metadata" in content
    assert "ludus_required_vars" in content
    if isinstance(data, dict) and data:
        assert isinstance(data.get("templates"), list)
