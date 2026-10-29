# Guided project setup

After installing the kit, open the consumer project in an agent and ask, for
example:

> Use setup-project to learn about and configure this project.

The canonical skill is [setup-project](../.agents/skills/setup-project/SKILL.md).
The agent investigates documentation and relevant files, distinguishes verified
facts from hypotheses, and asks one relevant decision at a time using the
client's question selector when available. It collects all answers first, then
applies the configuration and records any pending decisions. The
[questions.md](../.agents/skills/setup-project/references/questions.md) guide
organizes decisions by topic without imposing a fixed questionnaire.

The workflow depends on reading, editing and conversation capabilities, not a
specific client, terminal, Python or command. It may consult available local
tools, including doctor, when helpful. It does not run validation just because
it appears in the profile; availability and execution are recorded separately.
If the kit or profile is not installed, report the installation step. The kit
installer still requires Python 3.11+.

The interview uses the native question tool available in the current session:
Cursor's question tool, Claude Code's `AskUserQuestion`, or Codex's available
user-input tool. Availability depends on the client and mode. When a selector
is unavailable, the agent explains this and asks in chat; custom answers remain
possible. The agent waits for each response and does no project work between
questions. It applies changes only after the interview ends.

## Consumer-owned files

| File | Purpose |
| --- | --- |
| `.specdev/project.json` | Confirmed operational configuration: paths, validations, Git and applicable integrations. |
| `docs/PROJECT_CONTEXT.md` | Suggested path for project-specific information; another local path may be used. |
| `.specdev/setup-state.json` | Consumer-owned checkpoint written after the interview. |

The installer distributes the skill, reference and template, but does not create
the project's context or checkpoint. The skill creates or updates them during
requested setup. It preserves local configuration and existing documents. When
using a local context document, it adds the path to `context` after the file
exists, without duplicating entries. If the suggested document already exists,
the agent reads and preserves its content and agrees on another path if needed.

The [context template](../.agents/skills/setup-project/assets/project-context.md)
is adapted only to useful sections. Do not store credentials or secret values in
the profile, context or checkpoint. Client connections and permissions remain
the session's responsibility.

## Resuming and states

Answers collected during an interrupted interview remain only in the
conversation until the interview finishes. Resume from that history when it is
available; if it is lost, the unsaved answers need to be provided again. The
checkpoint is created or updated after the interview, including when the user
explicitly skips a decision, so later setup can resume pending work.

Checkpoint v1 stores `schema_version`, `status`, `context_path`, `scope`,
`decisions`, `pending`, `next_question` and `verification`. `scope` identifies
the decisions in the request; other decisions are not considered assessed in a
partial setup. Decisions have a stable ID, state and summarized source. Confirmed
values remain in the profile or context instead of being duplicated in state.

- `confirmed`: user answer or directly verified fact, with source.
- `inferred`: hypothesis still awaiting confirmation.
- `pending`: unresolved decision.
- `not_applicable`: explicitly inapplicable or proven inapplicable.

`pending` lists applicable IDs still pending or inferred; `next_question` stores
the next question or `null`. `verification` records configuration status,
observed availability and what was executed as text. This does not turn a
hypothesis into fact or a configured command into an executed test.

When an ID groups multiple fields, all applicable fields must be confirmed,
verified or explicitly found inapplicable before the group is resolved. The agent
preserves known fields and keeps the rest pending; partial confirmations do not
complete the whole ID.

On resumption, the agent rereads state and files, reconciling differences without
deleting local changes. Unknown versions, invalid state or unsafe paths stop the
affected edit and preserve data for resolution. Completion requires resolved
in-scope decisions, no pending IDs and a structurally checked configuration.
Service availability and test execution are reported as observed; they are not
automatic prerequisites for completing configuration.

## Compatibility

The installer provides the shared source for Codex and Cursor and generates the
Claude Code copy with the same resources. Another client can read the skill via
the catalog and follow its contract using available capabilities. Automatic
recognition and actual execution depend on each client's version and session;
check them in the environment where the kit will be used.
