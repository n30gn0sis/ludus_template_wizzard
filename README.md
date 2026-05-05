# Ludus Template Builder Scaffold

This repository now includes:
- Linux and Windows `.pkr.hcl` template scaffolds with required Ludus variables.
- A manifest and JSON Schema for builder metadata.
- A validator script to enforce Ludus template conventions.

## Commands

```bash
python3 validate_templates.py
ludus templates add -d .
ludus templates build -n my-ubuntu-template
ludus templates logs -f
```

## Notes

- macOS automated templating is intentionally not included; use non-automated/manual build workflow.
- Default credentials follow Ludus convention: `localuser:password`.
