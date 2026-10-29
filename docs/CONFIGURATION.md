# Configuration

`.specdev/project.json` is read by the installer and skills. It is not a native
extension of Codex, Cursor or Claude. Editing the profile does not execute
commands. Do not store tokens or passwords in it.

## Fields

| Field | Contract |
| --- | --- |
| `schema_version` | 1 |
| `project.name` / `language` | Project name and language for tickets and plans |
| `git.remote` / `repository` | Existing remote and GitHub owner/repo, if known |
| `git.base_branch` | Work and PR base unless explicitly requested otherwise |
| `git.branch_pattern` | Pattern with ticket and slug, resolved by the agent |
| `paths.plans` / `status` | Paths relative to the root, using `/` |
| `context` | Documents the agent should read for the stack/project |
| `validation` | Declarative commands selected by surfaces |
| `tracking.provider` | `none`, `github` or `clickup` |
| `tracking.list_id` / `workspace_id` | ClickUp identifiers, when applicable |
| `tracking.statuses` | Map from pending, in_progress and done to actual statuses |
| `delivery.create_pr` | Preference; does not authorize publication |
| `models` | ID or native options by tool and role |

New profiles default to English (`project.language: "en"`). Existing consumer
configurations are preserved on update. Set the language to `pt-BR` or another
appropriate value for the project; agents use it for tickets and plans.

Each `validation` command has a unique `id`, relative `cwd`, argument-list `argv`,
nonempty `surfaces`, descriptive prerequisite list `requires`, and boolean
`required`. Applicable `required=true` commands block completion without passing
evidence. `required=false` describes extra checks; it does not make a requested
criterion optional. Surfaces are project conventions, such as backend, frontend,
ui, infra, tooling and skills. The agent chooses coverage based on the diff.

~~~json
{
  "id": "unit",
  "cwd": ".",
  "argv": ["python", "-m", "unittest", "discover", "-s", "tests", "-v"],
  "surfaces": ["backend"],
  "requires": [],
  "required": true
}
~~~

The installer does not check executables, start Docker, alter Git or call
trackers. Actual prerequisites are checked during the task. Configure UI tests
explicitly when applicable; the generic profile does not invent suites or paths.
For guided setup, use [setup-project](../.agents/skills/setup-project/SKILL.md).
Its state contract and completion conditions are in [Guided setup](SETUP.md).

Branch placeholders are `{ticket}` and `{slug}`, without attribute access,
conversions or formatters. Tracker IDs are nonempty strings or null; `statuses`
maps pending, in_progress and done to nonempty names. Additional consumer fields
are preserved; `doctor` flags unknown fields in the main contracts to help find
misspellings.

## Models

Roles are explorer, worker, reviewer and investigator. With no setting, or with
`inherit`, the client's inheritance applies. Replace the example ID with one
available to your account:

~~~json
{
  "models": {
    "codex": {
      "reviewer": {"model": "AVAILABLE_CODEX_MODEL_ID", "reasoning_effort": "high"}
    },
    "cursor": {},
    "claude": {"explorer": {"model": "inherit", "tools": ["Read", "Grep", "Glob"]}}
  }
}
~~~

Run `install` again after editing models to regenerate the roles. Availability
is not checked online. The legacy string ID remains valid. Objects accept
`model` for all clients, `reasoning_effort` only for Codex, and `tools` only for
Claude. Effort must be supported by the chosen model; known names do not prove
compatibility or account availability. Without explicit effort, client inheritance
applies. Do not use `sandbox_mode` or permissions in this object.

`tools` is a nonempty allowlist of tool names, not commands or approval rules.
The example limits the explorer to reading and searching, so it cannot execute
tests; the primary agent runs required validation. Include tools only when the
role's task requires them. The list cannot grant permissions absent from the
session. Without a configured list, the client inherits its tools.

## Update and customize

`install` is idempotent and updates files matching the version recorded in the
manifest. A user-modified file causes a conflict. There is no `--force` option
that discards customizations.

Since version 0.2, managed UTF-8 text files (.md, .mdc, .py, .json, .toml, .txt,
.yaml, .yml) use `hash_mode: text-lf`: LF and CRLF are equivalent. Checkout EOL
conversion does not cause conflicts or rewrites; updates preserve the consumer's
EOL. Binary content remains byte-exact. The new installer migrates version 0.1
receipts without discarding real customizations. Consumer Git policy remains
unchanged; the updated manifest receives hash metadata.

`AGENTS.md` and `CLAUDE.md` receive blocks delimited by specdev comments. Text
outside the block is preserved. Changes within the block require manual resolution;
replaced files are copied to `.specdev/backups/`.

Use `install --dry-run` to plan without creating or changing files; `check` exits
with code 1 for drift, missing files or an outdated version. Configuration errors
and installation conflicts exit with code 2.

## Read-only diagnostics

~~~powershell
python scripts/specdev.py doctor --target "C:/Projects/my-project"
python scripts/specdev.py doctor --target "C:/Projects/my-project" --surfaces backend ui
~~~

`doctor` returns three groups in JSON:

- `integrity`: files, version and configuration are consistent with the kit.
- `configuration`: selected validations and required identities are configured.
- `environment`: local cwd and executable availability, without executing argv.

Exit 0 indicates local readiness to start validation; it does not mean tests
passed. Exit 1 indicates pending integrity, configuration or a required prerequisite.
Nonempty `requires` remains `requires_verification` because Docker, databases,
authentication and services are not consulted. Unavailable optional commands are
shown without blocking; a requested surface without configured validation blocks.

`doctor` changes no files, executes no profile commands or tests, calls no Git
and makes no external requests. `check` retains its integrity contract: a generic
profile can pass `check` while `doctor` remains pending due to missing validation.
Test results belong in the task/review, not the diagnostic. Models and actual
client discovery require separate verification.

Keep project-specific context in local documentation and select its path in
`context`. Install the kit before adding references to local files. Editing
generated files in the consumer does not update the kit repository: updates flow
from kit to consumer.

The manifest provides traceability, not cryptographic trust against someone who
can already edit the files. Multi-version updates preserve files removed from the
kit; removals are reviewed manually.
