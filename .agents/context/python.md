# Python profile

Read only when selected in context. Use the manager, virtual environment, import
style, and runner already adopted by the project. Do not migrate to pytest, uv,
poetry, or another tool as a side effect.

New file-handling scripts must preserve existing data and restrict paths to the
authorized target. Use subprocess with an argument list and shell=False when
executing programs; do not use eval for profile commands.
Test observable invariants, failures, and relevant side effects.
For the kit itself, the runner is standard-library unittest.
