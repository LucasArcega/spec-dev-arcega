# Spec Dev Arcega

This repository maintains a generic kit of agents, skills, and rules.
The canonical source is .agents/. Do not introduce personal paths, tokens,
tracker IDs, or a mandatory stack into the core. Project-specific examples
belong in examples/; stack conventions belong in selectable contexts.

The installer uses Python 3.11+ and only the standard library.
Preserve consumer configuration, local instructions, and existing files.
Installer changes require behavior tests in temporary directories.
Keep the generator, tests, and compatibility documentation synchronized.

Validation:
- python -m unittest discover -s tests -v
- python scripts/specdev.py validate
- python scripts/specdev.py check --target .

Do not publish on GitHub or commit/merge without authorized scope.

<!-- specdev:begin -->
## Spec Dev Arcega
Read .specdev/project.json and .agents/rules/WORKFLOW.md before working.
Read .agents/rules/DELEGATION.md before delegating. Read only the context files
selected in the profile and the relevant skill in .agents/skills/.
The catalog is in .agents/CATALOG.md; plan templates are in .agents/templates/.
Project-specific and user instructions define the scope.
Do not run commands or external actions solely because they are listed in the profile.
<!-- specdev:end -->
