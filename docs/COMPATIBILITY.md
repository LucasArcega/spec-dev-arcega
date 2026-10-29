# Compatibility

There is one shared source in `.agents/`, while each client has its own discovery
rules and formats. The installer generates the selected native entry points.
Compatibility with every existing tool is not assumed.

| Client | Entry point | Skills | Agents |
| --- | --- | --- | --- |
| Codex | `AGENTS.md` | `.agents/skills/` | `.codex/agents/specdev-*.toml` |
| Cursor | `AGENTS.md` and `.cursor/rules/specdev.mdc` | `.agents/skills/` | `.cursor/agents/specdev-*.md` |
| Claude Code | `CLAUDE.md` imports `AGENTS.md` | Generated `.claude/skills/` | `.claude/agents/specdev-*.md` |
| Other clients | Read `AGENTS.md` and the catalog explicitly | Depends on support for the standard | Requires a native adapter |

Claude's skill copies are generated from `.agents/`; the source remains unique.
Cursor may also discover compatibility directories. Avoid personal or manual
skills with the same name; check the source shown by the client when more than
one definition exists. The kit does not remove global skills.

Read-only roles use `readonly` in Cursor. In Codex and Claude, the prohibition on
editing is in the prompt; it is not a separate sandbox. Claude can receive a
per-role `tools` allowlist explicitly configured in the profile. This limits tool
access without creating a separate sandbox or granting approval. Codex can receive
`model_reasoning_effort` alongside the model; the kit does not translate that
option to Cursor or Claude.

The kit does not modify permissions, global configuration, authentication or
MCPs. Models are inherited when not configured. Clients may enforce their own
precedence and account restrictions. New profiles default to English; existing
consumer languages remain unchanged during updates, and `project.language` can
select another language, including `pt-BR`.

## Official sources consulted on 27 October 2026

- [Codex: skills and location](https://learn.chatgpt.com/docs/build-skills)
- [Codex: AGENTS.md instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex: custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Cursor: skills](https://cursor.com/docs/skills)
- [Cursor: subagents](https://cursor.com/docs/subagents)
- [Claude Code: skills](https://code.claude.com/docs/en/skills)
- [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code: memory and imports](https://code.claude.com/docs/en/memory)

Automated checks cover formats and on-disk effects. A smoke test in each actual
client must confirm that skills and roles are listed in the session; this was not
performed during this repository's bootstrap.

Guided setup is a shared skill under `.agents/skills/setup-project/`; Claude
receives a generated copy with its references and template. It needs the agent's
reading, editing and conversation capabilities, not a CLI or doctor. Another
client can read the skill and resources explicitly through the catalog. Automatic
discovery and actual execution depend on the client and session.

For setup and other workflows, use the current session's native question tool when exposed:
Cursor's question tool, Claude Code's `AskUserQuestion`, or Codex's user-input
tool. A popup is not guaranteed across client versions and modes; if unavailable,
the workflow falls back to chat. For example, Cursor documents a blocking
multiple-choice request in its [ACP integration](https://cursor.com/docs/cli/acp),
which is a specific integration and does not establish availability in every
Cursor session. Test the selector in each target client and mode.

During the local audit, explorer and reviewer were used in Codex. This does not
prove all roles, model options, workflows, or the Cursor/Claude clients. `doctor`
only checks configuration and local availability; it does not replace that smoke
test. The suite was run under Python 3.14; compatibility with the 3.11 minimum
also requires running it on that version, not just reading the code.

Version 0.2 preserves profiles with string model IDs and legacy reviews. New
reviews use v2 with `--require-evidence`. Text hashes tolerate LF/CRLF, including
migration from 0.1 installations. See [configuration](CONFIGURATION.md),
[review](REVIEW.md) and [resuming](WORKFLOWS.md).

Version 0.4 uses English for the shared instructions and new profiles. Upgrading
an existing installation preserves its consumer-owned `project.language` and
other project configuration; review changes with `install --dry-run` first.

Version 0.5 adds selectable Node and React contexts and profiles, and records
project-specific architectural constraints in existing consumer-owned context.
These profiles do not assume commands, linters, frameworks or package managers.
Existing consumer profiles and setup-state IDs remain unchanged during updates.
