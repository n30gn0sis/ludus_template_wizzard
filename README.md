# Ludus Template Builder Scaffold

This repository now includes:
- Linux and Windows `.pkr.hcl` template scaffolds with required Ludus variables.
- A manifest and JSON Schema for builder metadata.
- A validator script to enforce Ludus template conventions.
- A template wizard to generate/update manifest template entries.

## Commands

```bash
python3 validate_templates.py
python3 scripts/template-wizard.py
python3 scripts/template-wizard.py --non-interactive --base-os ubuntu --template-name my-ubuntu-template --packages "qemu-guest-agent,curl" --enable-cleanup --force
ludus templates add -d .
ludus templates build -n my-ubuntu-template
ludus templates logs -f
```

## Wizard

The wizard supports interactive prompts by default and writes a `builder.manifest.yaml`-compatible structure.

Interactive prompts include:
- Base OS (`ubuntu`, `windows2022`)
- Template name
- Packages/software list (comma-separated)
- Optional bootstrap extras (`enable cleanup`, `custom bootstrap path`)

Output behavior:
- Adds or updates a template entry under `templates`.
- Stores wizard-specific selections under `wizard.<template_name>`.
- Appends selected package install commands to OS-specific bootstrap scripts.
- Asks for confirmation before overwriting existing output files unless `--force` is used.

### Non-interactive mode

For CI/scripted generation:

```bash
python3 scripts/template-wizard.py \
  --non-interactive \
  --base-os windows2022 \
  --template-name my-win2022-template \
  --packages "git,7zip" \
  --enable-cleanup \
  --custom-bootstrap-path scripts/windows-bootstrap.ps1 \
  --output builder.manifest.yaml \
  --force
```

## Notes

- macOS automated templating is intentionally not included; use non-automated/manual build workflow.
- Default credentials follow Ludus convention: `localuser:password`.
