<div align="center">

# Spec Dev Arcega

**A kit of skills and agents for working on your project.**

From planning through delivery, following your team's context and rules.

`Codex` · `Cursor` · `Claude Code` · `other compatible tools`

Current kit version: **0.5.0**

</div>

---

## Install with one message

Open the project that will receive the kit in your agent and send:

```text
Read https://github.com/LucasArcega/spec-dev-arcega/blob/main/INSTALL.md and install the kit in this project.
Then start the guided setup.
```

The agent will locate the kit, inspect the project, simulate the installation,
and apply the changes. It will then ask questions to learn about your project
and help you fill in its configuration.

> **Access to the kit:** the agent needs access to this repository or a complete
> local copy. If it cannot find the source, it will ask for the path or address.

The installer requires **Python 3.11+** on the machine performing the
installation. Guided setup uses the agent's capabilities and is not tied to a
specific client.

## What happens next?

| Step | Your agent will |
| --- | --- |
| **Install** | Check the source and destination, simulate and install the kit. |
| **Explore** | Read the project's documentation and conventions. |
| **Ask** | Collect the decisions, one at a time, using your client's selector when available. |
| **Configure** | Apply the answers after the interview and record any pending decisions. |
| **Check** | Verify the installation and report anything still pending. |

The `generic` profile starts without validation commands. During setup, the agent
helps register the actual commands and prerequisites for your project. The
installer does not run those commands automatically.

## How to use the skills

After installation, you can request tasks in natural language or name the skill
when you want to be specific. Send the examples below **in the agent chat**.
Replace ticket numbers and paths with those of your project; these are not
terminal commands.

| Skill | When to use it | Example request |
| --- | --- | --- |
| [`setup-project`](.agents/skills/setup-project/SKILL.md) | Configure the project or continue setup. | `Use setup-project to configure this project.` |
| [`write-ticket`](.agents/skills/write-ticket/SKILL.md) | Draft or review a ticket. | `Use write-ticket to draft a ticket about report exports.` |
| [`enrich-plan`](.agents/skills/enrich-plan/SKILL.md) | Investigate and complete a ticket's plan. | `Use enrich-plan to prepare the plan for ticket 12.` |
| [`implement-ticket`](.agents/skills/implement-ticket/SKILL.md) | Implement, review and validate the plan. | `Use implement-ticket to implement the plan for ticket 12.` |
| [`implement-in-worktree`](.agents/skills/implement-in-worktree/SKILL.md) | Implement the task in an isolated worktree. | `Use implement-in-worktree to implement ticket 12.` |
| [`review-changes`](.agents/skills/review-changes/SKILL.md) | Review changes and identify problems. | `Use review-changes to review the changes on this branch.` |
| [`create-pr`](.agents/skills/create-pr/SKILL.md) | Create or reuse a PR and link the ticket when requested. | `Use create-pr to open a PR for this branch and link ticket 12.` |
| [`merge-and-close`](.agents/skills/merge-and-close/SKILL.md) | Merge a validated PR and close the ticket. | `Use merge-and-close to merge PR 34 and close ticket 12.` |
| [`fast-merge`](.agents/skills/fast-merge/SKILL.md) | Perform a direct merge without PR or CI when explicitly requested. | `Use fast-merge to merge the current branch directly into develop.` |
| [`record-test`](.agents/skills/record-test/SKILL.md) | Record a specific UI test. | `Use record-test to record the test at path/to/spec.` |

To resume an interrupted setup, ask:

```text
Use setup-project to continue setup from where we left off.
```

A typical workflow is to prepare a plan with `enrich-plan`, implement it with
`implement-ticket`, then request `create-pr` or `merge-and-close` when you are
ready to deliver. Use `fast-merge` when you explicitly want a **direct merge**
without PR or CI.

`enrich-plan` prepares a plan without implementing code. `implement-ticket`
goes through review, validation and handoff; commit, push and PR depend on the
request. PR and merge skills currently use GitHub. Linking or closing a ticket
depends on the configured tracker and the requested action.

The kit also includes agent roles, rules and templates. The shared source lives
in `.agents/`; each client receives its supported formats. See the full
[catalog](.agents/CATALOG.md).

## Installer commands

The easiest way is to ask your agent to follow [INSTALL.md](INSTALL.md). To run
the commands yourself, open a terminal **in the Spec Dev directory** containing
`scripts/specdev.py` and replace the destination with your project path.

The examples use `python`. On macOS/Linux, use `python3` if that is the available
command. The installer requires Python 3.11 or later.

### First installation

First, simulate the installation to inspect the files and potential conflicts:

```powershell
python scripts/specdev.py install --target "C:/Projects/my-project" --profile generic --tools codex cursor claude --dry-run
```

If everything looks right, run the same command without `--dry-run`:

```powershell
python scripts/specdev.py install --target "C:/Projects/my-project" --profile generic --tools codex cursor claude
```

On macOS/Linux, replace the destination with a local path such as
`/path/to/my-project`. The options work as follows:

| Option | Purpose |
| --- | --- |
| `--target` | Path of the project receiving the kit. Quote paths containing spaces. |
| `--profile` | Initial profile: `generic`, `python`, `dotnet-angular`, `node`, `react` or `node-react`. Use only for the first installation. |
| `--tools` | Clients to install: `codex`, `cursor` and/or `claude`. If omitted on first installation, all three are selected. |
| `--dry-run` | Show planned changes and conflicts without writing to the destination. |

Profiles are starting points. `generic`, `node`, `react` and `node-react` have
no validation commands; `python` and `dotnet-angular` provide examples that
must be adapted to the project. New
profiles use English by default. Existing consumer configurations are preserved;
set `project.language` to `pt-BR` or another language if the project requires it.

### Check an installation

```powershell
python scripts/specdev.py check --target "C:/Projects/my-project"
python scripts/specdev.py doctor --target "C:/Projects/my-project"
```

`check` checks generated files, configuration and version. `doctor` also reports
incomplete configuration, missing directories or executables, and prerequisites
that still need verification. It does not run the project's tests.

To check only selected configured surfaces, for example:

```powershell
python scripts/specdev.py doctor --target "C:/Projects/my-project" --surfaces backend frontend
```

### Update or add clients

After updating your copy of Spec Dev, simulate and apply the update:

```powershell
python scripts/specdev.py install --target "C:/Projects/my-project" --dry-run
python scripts/specdev.py install --target "C:/Projects/my-project"
```

Without `--profile` and `--tools`, the installer preserves the profile and
previously selected clients. To add a client with `--tools`, include the clients
already installed as well. For example, if the project already uses Codex and
Cursor and you want to add Claude:

```powershell
python scripts/specdev.py install --target "C:/Projects/my-project" --tools codex cursor claude --dry-run
python scripts/specdev.py install --target "C:/Projects/my-project" --tools codex cursor claude
```

If a conflict appears, inspect the indicated file and preserve local changes.
Updates create backups in `.specdev/backups/`; removing adapters is manual. See
[the installation guide](docs/INSTALACAO-MANUAL.md) for details and troubleshooting.

### Validate the kit itself

To check the skills and profiles of the Spec Dev copy you are using:

```powershell
python scripts/specdev.py validate
```

This checks the kit in the current directory. To inspect an installation in
another project, use `check --target` as shown above. The command and option list
is also available through `python scripts/specdev.py --help`.

## More information

- [Manual installation, profiles and troubleshooting](docs/INSTALACAO-MANUAL.md)
- [Guided setup and resuming](docs/SETUP.md)
- [Project configuration](docs/CONFIGURATION.md)
- [Client compatibility](docs/COMPATIBILITY.md)
- [Evidence-based review](docs/REVIEW.md)
- [Criteria, evidence and resuming delivery](docs/WORKFLOWS.md)
- [JourneyCore origins and extraction](docs/EXTRACTION.md)

Spec Dev Arcega grew out of JourneyCore practices. Its shared workflows can be
adapted to projects with other stacks and architectures.
