---
name: setup-project
description: "Investigates and configures the kit for a project through guided questions and resumable setup."
---

# Configure the project

Use this to start, continue or review setup of the kit in a consumer project.
The agent conducts the conversation and uses available read and edit capabilities;
a terminal, Python, doctor or specific clients are not prerequisites.
Use project.language for setup questions and project artifacts, respecting any explicit language choice in the user's request.

## Investigate and interview

1. Read local instructions, .specdev/project.json, the documents already selected
   in context and, if present, .specdev/setup-state.json. If the kit or profile is
   missing, report the installation step or blocker; do not fabricate a partial
   configuration. Identify relevant project docs and files without reading
   credentials or running commands.
2. Separate verified facts with sources, user-confirmed decisions and hypotheses.
   Profile defaults and examples are hypotheses, not confirmations. Compare
   state, files and current request; resume without repeating answers still valid.
   For full setup, evaluate each ID in [references/questions.md](references/questions.md);
   for a limited request, evaluate relevant IDs and report those not evaluated.
   Record gaps and applicable fields without imposing a fixed interview.
3. Prepare the applicable questions and their dependencies from this initial
   investigation. Present discoveries briefly, then collect all applicable
   answers before making any changes. Ask one material decision at a time, with
   a suggestion when there is evidence. Use the session's native question and
   selection tool whenever available: Cursor's question tool, Claude Code's
   AskUserQuestion, or Codex's available user-input tool. Follow its actual
   schema and availability, not an assumed client version or mode. Provide
   meaningful options and a way to supply a custom answer. If the selector has
   no custom input, offer a custom-value option and collect its value in chat.
   Use free text when choices are inappropriate. If the selection tool is unavailable, explain
   that limitation and ask in chat. Never claim a popup was displayed when it
   was not. Do not treat a preselected option as an answer until submitted.
4. During the interview, keep answers, pending items and the next question in
   conversation context only. Between questions and while waiting, do not read
   more files, run commands, delegate, validate, write the checkpoint or make
   any other project changes. Wait for each response, including for asynchronous
   question tools, before asking the next question. Adapt conditional questions
   from the answers already collected. Incorporate information already given;
   never invent confirmation, repository, IDs, commands, capabilities,
   environment or results. A skipped, cancelled, unknown or missing answer is
   unresolved, not confirmation. Continue the remaining applicable questions
   when the user explicitly skips or says they do not know; if the interview is interrupted, stop without
   applying changes. Resume from available conversation history without asking
   again for valid answers. If that history is unavailable, explain that
   unpersisted answers were lost and ask again as needed.
5. Once every applicable question has been answered or explicitly left unresolved and
   the interview is finished, apply the confirmed decisions together, then
   validate and report pending items. Do not wait for a second approval solely
   to apply the setup the user requested. An explicitly unresolved decision remains
   pending and does not prevent applying independent confirmed decisions.

## Apply and resume

After the interview, record confirmed facts and decisions in .specdev/project.json
and local context. The suggested path is docs/PROJECT_CONTEXT.md; use another
project-relative path when adopted or agreed. For a new document, adapt
[assets/project-context.md](assets/project-context.md) only to applicable
sections. If it already exists, read and preserve its contents: integrate only
relevant passages or agree on another path, without assuming ownership.
Append the selected document to context once, after it exists. Preserve other
fields, contexts, comments and local instructions; do not edit generated files or
replace the entire profile. Do not record tokens, passwords, credential contents
or sensitive data in the context, profile or state.
Record confirmed architectural boundaries and their evidence in the selected
consumer-owned context as described in references/questions.md. Capture existing
project-specific lint and architecture checks as validation only when confirmed;
do not create a universal architecture or install a lint tool.

Maintain .specdev/setup-state.json as a consumer-owned file, never managed by
the manifest. Create it only when absent; update known fields while preserving
extensions. The v1 contract is:

~~~json
{
  "schema_version": 1,
  "status": "in_progress",
  "context_path": "docs/PROJECT_CONTEXT.md",
  "scope": ["product.purpose"],
  "decisions": {
    "product.purpose": {"status": "pending", "source": "to clarify"}
  },
  "pending": ["product.purpose"],
  "next_question": "What problem does the project solve?",
  "verification": {
    "configuration": "pending",
    "availability": "not verified",
    "execution": "no commands run"
  }
}
~~~

General status is in_progress, blocked or complete. Each decision uses a stable
ID from the reference and status confirmed, inferred, pending or not_applicable,
with a short source without secrets. confirmed requires user confirmation or a
directly verified fact; record its origin in source.

scope is the list of stable IDs covered by the request. For full setup, record
all IDs in the map; for partial setup, only those selected. IDs not yet assessed
remain pending rather than disappearing. On resumption, use the persisted scope;
expand it only when the current request includes new decisions.

When an ID groups multiple fields, confirm each applicable field by user answer
or verified fact, or record evidence that it does not apply. A single source for
one field does not confirm the others. Mark the ID confirmed only when every
field is resolved this way; use not_applicable for the ID only when the entire
group does not apply. While a field remains pending or hypothetical, keep the ID
pending or inferred and in pending; ask one decision at a time. Apply confirmed
fields to their proper destinations and record each field's sources and pending
items in source without sensitive values; see the examples in
references/questions.md.

inferred does not authorize recording a hypothesis as fact. Record confirmed
values in their proper files, and do not duplicate sensitive answers in state.
pending contains applicable IDs still pending or inferred; next_question is the
next question as text or null when none exists. Create or update the checkpoint
only after the interview ends, together with the other setup changes. In
verification, record result or limitation of
structure, availability and execution without sensitive data. All three fields
are free text, not an enumeration. If unable to write, report the limitation and
continue only within the possible scope.

Before each change, reread the target; if it changed since reading, reconcile
without deleting others' work. If state is invalid, uses an unknown version,
points to an unsafe path or diverges from the files, preserve it, report the
problem and resolve the divergence before the affected edit. Do not reset.
On resumption, revalidate recorded sources and fields; a checkpoint does not
prove the files remain unchanged.

For every composite ID in scope, including those already marked confirmed or
not_applicable, check each applicable field in actual sources and destinations
before retaining its status and before concluding. A generic source citing only
documents does not prove every field was resolved: record each field's origin
or pending state there without sensitive data. If a field is not proven or
explicitly not applicable, reclassify the ID as pending or inferred, include it
in pending and adjust next_question and overall status to in_progress or blocked.
Preserve existing data and do not repeat questions for fields with valid evidence.
The context path must remain relative to the authorized root, without .., and
must not cross a link/junction that redirects reading or editing outside it.

## Check and hand off

Check the profile against the contract summarized in
[references/questions.md](references/questions.md), the existence of selected
contexts, unique IDs, paths and arguments for each validation. Consult local
configuration documentation if present. Record in the checkpoint what is
configured, what had availability actually checked and what was executed, with
result or limitation. Choose checks suited to available capabilities. Doctor
can help when available; its absence does not block setup. Do not run declared
commands merely because they are in the profile or assume services are active.

Mark complete only when all scoped IDs have been evaluated, applicable decisions
are confirmed or explicitly not_applicable, no IDs are pending, and the structure
is coherent and has been checked. Record a result or limitation for each type of
verification. An unconfirmed hypothesis, conflict or missing essential decision
keeps setup pending/blocked. If unable to check profile structure and paths,
record the limitation and keep in_progress or blocked. Service availability and
test execution are not prerequisites for setup completion.

Completion of configuration does not claim tests passed or services are
available. Deliver changed files, decisions, checks performed, limitations and
next action. External operations depend on the corresponding request.
