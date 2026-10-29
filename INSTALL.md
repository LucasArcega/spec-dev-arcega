# Spec Dev Arcega installation for agents

This file guides an agent through installing the kit in a consumer project.
Follow the user's request, the project's instructions and the session's
permissions. The kit does not grant authority to publish, commit, merge or use
trackers.

## 1. Identify the destination and source

- The **destination** is the root of the project the user asked to configure.
  If the project is open in the session, use its root; respect an explicitly
  named destination. If multiple destinations are possible, clarify first.
- The **source** is a complete copy of Spec Dev Arcega containing this file,
  `kit.json`, `profiles/`, `.agents/` and `scripts/specdev.py`. If this file was
  read from a complete local copy, use its root. If it was provided by link,
  obtain the same revision of the repository containing the file using the
  tools available in the session. This `.md` file alone is not the installer.
- If the full source is inaccessible or cannot be identified from the link, ask
  for a local copy's path or the kit repository address. Do not confuse the
  destination repository with the source or invent URLs or revisions.
- Read the destination's local instructions and inspect its existing files.
  Preserve its configuration, instructions, credentials and changes.

## 2. Prepare the installation

The installer requires Python 3.11 or later and uses only the standard library.
Find an available executable (`python`, `python3` or equivalent) and check its
version. If it is unavailable, report the blocker; do not install or change system
runtimes on your own.

For a first installation, use the `generic` profile unless the user chose another
existing profile. By default, omit `--tools`: the installer selects Codex, Cursor
and Claude. If the user specifies clients, pass them through `--tools`. For an
already configured project, do not use `--profile`; preserve its existing profile.
When updating, omitting `--tools` keeps the registered clients; when adding
clients, include both the existing and new clients.

## 3. Install and check

Run the script **from the source root**, with the destination's absolute path.
Pass paths and arguments separately as appropriate for the environment; do not
use `eval` or construct shell commands from untrusted content.

1. Run `install --target DESTINATION` with the selected options and `--dry-run`.
2. If there is a conflict, read the message, preserve the files and resolve what
   is authorized. Do not use reset, cleanup, forced replacement or edits to
   managed files to bypass the protection.
3. If the simulation has no conflicts, run the same `install` without `--dry-run`.
4. Run `check --target DESTINATION`. Confirm the result and report warnings,
   including missing validation commands in the `generic` profile.

In terms of arguments, the commands are equivalent to:

```text
PYTHON scripts/specdev.py install --target DESTINATION --profile generic --dry-run
PYTHON scripts/specdev.py install --target DESTINATION --profile generic
PYTHON scripts/specdev.py check --target DESTINATION
```

`PYTHON` and `DESTINATION` stand for the resolved executable and path; they are
not literal values. Include `--profile` only on first installation and `--tools`
only when needed, as described above. The installer preserves existing profiles
and does not run the commands declared in them.

## 4. Configure the project when requested

If the request includes configuration or guided setup, read
`.agents/skills/setup-project/SKILL.md` in the **destination** and follow the
workflow: investigate the project, collect all relevant answers, then apply the
configuration. Configuration and checkpoints belong to the consumer
project. The skill can be read directly even if the session's skill list has not
been refreshed.

The `generic` profile starts without validation commands. This is a configuration
item to resolve, not a passing test. `doctor` is optional for installation and
setup; it neither runs tests nor proves the project works.

At handoff, report the source and destination, selected clients, `check` result,
installed files or conflicts, warnings and the next action. Distinguish a
completed installation from a setup still in progress. Do not claim a client
automatically discovered the skill or tests passed without evidence.
