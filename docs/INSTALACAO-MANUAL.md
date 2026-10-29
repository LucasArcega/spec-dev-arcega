<div align="center">

# Spec Dev Arcega

**Skills, agents and workflows for developing with context.**

A specification-driven kit that adapts to your project and team.

`Python 3.11+` · `Standard library` · `Codex` · `Cursor` · `Claude Code`

[Installation](#installation) · [Guided setup](#5-configure-your-project) · [Skills](#explore-the-skills) · [Updates](#update-the-kit) · [Help](#troubleshooting)

</div>

---

Spec Dev Arcega collects reusable instructions to help agents understand a
project, prepare plans, implement, review and deliver changes. The kit grew out
of JourneyCore practices and keeps their specific conventions in a
[separate example](../examples/journey-core/project.json).

Use it with projects in different languages and architectures. Project-specific
information stays in the consumer's configuration and documents.

## Before you start

You need:

1. **A copy of this repository** containing `scripts/specdev.py` and `.agents/`.
2. **Python 3.11 or later** on the machine running the installer. There are no external Python dependencies.
3. **A destination project**: the directory that will receive the skills and agents.
4. **A compatible agent**, such as Codex, Cursor or Claude Code. Other clients can read the shared instructions through the catalog.

Check your Python version:

```bash
python --version
```

On macOS or Linux, use `python3 --version` if `python` is unavailable. Python is
needed to install and update the kit; the guided setup conversation uses the
agent's capabilities.

## Installation

### 1. Open a terminal in the kit directory

Run all commands below **from this repository's root**, where
`scripts/specdev.py` lives. The destination is the project receiving the kit.
Replace example paths with real ones. Keep quotes around paths containing spaces.

### 2. Simulate the installation

`--dry-run` shows files that would be created or updated and detects conflicts.
It does not write files to the destination.

**Windows — PowerShell**

```powershell
python scripts/specdev.py install --target "C:/Projects/my-project" --profile generic --tools codex cursor claude --dry-run
```

**macOS / Linux**

```bash
python3 scripts/specdev.py install --target "/path/to/my-project" --profile generic --tools codex cursor claude --dry-run
```

The examples select all three clients. Select only those you use, for example
`--tools codex` or `--tools cursor claude`. If `--tools` is omitted on first
installation, all three are selected.

### 3. Install the kit

If the simulation looks right, run the same command without `--dry-run`:

**Windows — PowerShell**

```powershell
python scripts/specdev.py install --target "C:/Projects/my-project" --profile generic --tools codex cursor claude
```

**macOS / Linux**

```bash
python3 scripts/specdev.py install --target "/path/to/my-project" --profile generic --tools codex cursor claude
```

The installer preserves existing configuration and instructions. If a managed
file has local changes that cannot be updated safely, it reports a conflict
before writing the planned files.

### 4. Open the project in your agent

Open the **destination project** in Codex, Cursor or Claude Code and start a new
session. Check that the client recognizes the installed skills and agents.

| Client | How the kit is provided |
| --- | --- |
| **Codex** | `AGENTS.md`, skills in `.agents/skills/` and agents in `.codex/agents/`. |
| **Cursor** | `AGENTS.md`, rule in `.cursor/rules/`, shared skills and agents in `.cursor/agents/`. |
| **Claude Code** | `CLAUDE.md`, skill copies in `.claude/skills/` and agents in `.claude/agents/`. |
| **Other agent** | Read `AGENTS.md` and `.agents/CATALOG.md`; automatic discovery depends on client support. |

See [Compatibility](COMPATIBILITY.md) for client details and limitations.

### 5. Configure your project

Ask the agent:

> Use setup-project to learn about and configure this project.

The skill inspects available files, distinguishes facts from hypotheses and
asks about missing decisions. Answers are recorded progressively; you can
interrupt and resume the conversation later.

The **generic profile starts without validation commands**. Configure the actual
commands, directories and prerequisites before implementing tickets. The agent
can help; commands are declarative and the installer does not execute them.
See [Guided setup](SETUP.md) and [Configuration](CONFIGURATION.md).

## Choose a profile

The profile supplies a starting point for `.specdev/project.json`. If `--profile`
is omitted on first installation, `generic` is used.

| Profile | When to choose it | Starting point |
| --- | --- | --- |
| `generic` | Any stack or architecture | No validation commands; configure them for the project. |
| `python` | Python project | Python context and an example `unittest` validation. |
| `dotnet-angular` | Project with .NET and Angular | Stack context and example build and test commands. |
| `node` | Node.js project | Node context; configure project-specific validations. |
| `react` | React project | React context; configure project-specific validations. |
| `node-react` | Project using both Node.js and React | Both contexts; configure project-specific validations. |

Review the commands and paths in each profile: they are adjustable examples,
not automatic architecture detection. Use `--profile` only for the first
installation; later, edit `.specdev/project.json` in the consumer project. New
profiles default to English; existing consumers retain their language. Set
`project.language` to `pt-BR` or another appropriate language when needed.

## Explore the skills

Ask for a skill by name or describe the task. Shared instructions and resources
for each workflow are in `.agents/skills/`.

| Skill | Purpose |
| --- | --- |
| [`setup-project`](../.agents/skills/setup-project/SKILL.md) | Learn about and configure a project with guided questions. |
| [`write-ticket`](../.agents/skills/write-ticket/SKILL.md) | Write or review tickets with verifiable criteria. |
| [`enrich-plan`](../.agents/skills/enrich-plan/SKILL.md) | Investigate and complete a ticket plan. |
| [`implement-ticket`](../.agents/skills/implement-ticket/SKILL.md) | Implement, review and validate a ticket through handoff. |
| [`review-changes`](../.agents/skills/review-changes/SKILL.md) | Review changes with structured findings and evidence. |
| [`create-pr`](../.agents/skills/create-pr/SKILL.md) | Create or reuse a PR and link it to the ticket when authorized. |
| [`merge-and-close`](../.agents/skills/merge-and-close/SKILL.md) | Merge a validated PR and close the ticket when requested. |
| [`fast-merge`](../.agents/skills/fast-merge/SKILL.md) | Perform a direct merge when explicitly requested. |
| [`implement-in-worktree`](../.agents/skills/implement-in-worktree/SKILL.md) | Implement a task in an isolated worktree. |
| [`record-test`](../.agents/skills/record-test/SKILL.md) | Record a requested UI test. |

Example requests:

> Use enrich-plan to prepare the plan for ticket 12.

> Use implement-ticket to implement plan 12-export-report.

> Use review-changes to review the changes on this branch.

Creating a PR, publishing, merging or updating a tracker depends on task
authorization. A skill or configured preference does not trigger those actions.

## What goes into the project

| Path | Purpose |
| --- | --- |
| `.agents/` | Shared source of skills, roles, rules, templates, contexts and integrations. |
| `.specdev/project.json` | Consumer project configuration. |
| `.specdev/manifest.json` | Version, selected clients and generated-file hashes. |
| `AGENTS.md` | Shared entry point, preserving local content. |
| `.codex/`, `.cursor/` and `.claude/` | Selected client adapters; Claude also receives skill copies. |
| `CLAUDE.md` | Claude Code entry point, created or updated when that client is selected. |

During guided setup, the agent may create `.specdev/setup-state.json` to resume
the interview and a local context document such as `docs/PROJECT_CONTEXT.md`.
These files belong to the consumer project. The installer does not create or
manage them.

The installer does not alter Git. For team conventions, consider versioning the
entry points, skills, profile and manifest. Add `.specdev/backups/` and
`.specdev/install.lock` to the consumer project's `.gitignore`.

## Update the kit

After updating your copy of this repository, run these from the kit root. Use
your project path and the same Python command as for installation.

```powershell
python scripts/specdev.py install --target "C:/Projects/my-project" --dry-run
python scripts/specdev.py install --target "C:/Projects/my-project"
python scripts/specdev.py check --target "C:/Projects/my-project"
```

On macOS/Linux, switch `python` to `python3` when needed and use a local project
path. Omitting options preserves the profile and selected clients. To add a client
with `--tools`, provide the complete set including installed clients. Adapter
removal is manual; the installer does not delete files.

Updates create backups of replaced files in `.specdev/backups/`. Planning finds
conflicts before writing, but a disk failure during writing can leave a partial
installation. Use the backups and `check` to identify what needs restoration.
Avoid concurrent installations to the same destination.

## Troubleshooting

| Situation | What to do |
| --- | --- |
| **Python missing or outdated** | Install or select Python 3.11+ and check `python --version` or `python3 --version`. |
| **The agent cannot find a skill** | Start a new session at the destination project root, check the selected client and consult `.agents/CATALOG.md`. |
| **The destination has existing instructions or generated files** | Run `install --dry-run`, read conflicts and preserve customizations when resolving them. |
| **check reports missing or changed files** | Inspect the result, simulate installation and resolve conflicts before updating. |
| **doctor reports missing validation** | Configure real commands and prerequisites in `.specdev/project.json`; the generic profile starts empty. |
| **I edited a copy in `.claude/`** | The kit source is `.agents/`. Changes to the generated copy may need manual resolution on update. |

To check integrity and local readiness, run from the kit root:

```powershell
python scripts/specdev.py check --target "C:/Projects/my-project"
python scripts/specdev.py doctor --target "C:/Projects/my-project"
```

`check` verifies integrity and version. `doctor` also reports incomplete
configuration and local directory/executable availability; it does not run
tests, contact services or prove that validation passed.

## Further documentation

- [Guided setup and resuming](SETUP.md)
- [Project configuration](CONFIGURATION.md)
- [Client compatibility](COMPATIBILITY.md)
- [Evidence-based review](REVIEW.md)
- [Criteria, evidence and resuming delivery](WORKFLOWS.md)
- [JourneyCore origins and extraction](EXTRACTION.md)
- [Shared skill and role catalog](../.agents/CATALOG.md)

To validate changes to the kit itself:

```bash
python -m unittest discover -s tests -v
python scripts/specdev.py validate
python scripts/specdev.py check --target .
```

Tests check formats and on-disk behavior. Actual discovery and use of skills must
be checked in each client's session.
