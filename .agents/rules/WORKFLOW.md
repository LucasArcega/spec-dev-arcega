# Shared agreements

Read the profile in .specdev/project.json and the project's specific instructions.
The profile is a contract of this kit, not a native editor configuration.
Profile fields describe options; they neither authorize nor execute actions.

## Scope and context

- Use the relevant skill in .agents/skills/. Do not load every skill, stack rule,
  and document at once. Consult .agents/CATALOG.md.
- Work only on the request and accepted criteria. Suggestions stay outside the
  plan until accepted. Do not include optional tasks in acceptance criteria.
- Resolve paths from the project root. Read only the documents selected in
  context; additional project conventions remain valid.
- Before changing contracts, read actual code and tests. Do not invent paths,
  priority, dependencies, endpoints, tool capabilities, or results.
- Consult applicable architectural responsibilities, dependency boundaries,
  exceptions and checks in the selected project context. Use verified rules and
  their sources; do not infer a mandatory architecture from folder names or
  assume an undocumented boundary is absent. Surface uncertainty when material.
- When a missing decision changes scope, clarify one question at a time with a
  suggestion. Continue independent work; do not repeat resolved questions.
  For the setup-project interview, follow its question-first workflow instead:
  wait for all applicable answers before doing further work or editing files.

## Asking for decisions

- When user input is needed, use the session's native question tool whenever it
  is available and permitted: Cursor's question tool, Claude Code's
  AskUserQuestion, or Codex's available user-input tool. Follow the actual tool
  schema and mode; do not assume a tool or popup exists. If unavailable, explain
  the limitation and ask in chat.
- For choices, provide meaningful options grounded in the task, a recommendation
  when supported by evidence, and a way to supply a custom answer. Respect the
  client's built-in custom option; if none exists, offer a custom-value option
  and collect its value in chat. Use free text for questions without sensible
  choices. Never treat a preselected option, skipped question, cancellation or
  missing response as an answer.
- Ask only when the answer matters and cannot be inferred from the request or
  available context; do not ask for permission already granted. Where practical,
  collect related open decisions together while keeping each question clear.
  With asynchronous tools, wait for required answers before dependent work;
  continue independent work unless a skill, such as setup-project, says otherwise.

## Planning and implementation

- Use paths.plans and paths.status to locate plans and dependencies. The branch
  pattern comes from git.branch_pattern, with ticket and slug resolved.
- Separate BACKEND.md and FRONTEND.md when both surfaces exist. For UI, record
  flows, transient states, errors, loading, responsiveness, and product-supported
  themes in PLAYWRIGHT.md (or TESTS.md for another runner).
- Dark mode is required only when the product offers it. JourneyCore technology
  and architecture do not become requirements for other projects.
- Each criterion needs a stable ID, observable behavior, and validation evidence.
  Connect criteria, implementation or tests, and results in the plan. Use
  .agents/templates/ as models, filling only applicable sections.
- Before implementing, confirm dependencies and Git state. Preserve existing
  changes. Do not stash, reset, clean, force checkout, or refactor incidentally.

## Validation and completion

- Select validation entries by changed surfaces. Run applicable commands in the
  specified cwd, passing argv as arguments with the appropriate shell. Do not
  execute configuration strings with eval.
- Check environment dependencies in requires. Integration, running services, and
  UI validation depend on scope. Do not run broad suites on every iteration.
- Commands are declarative: the installer never executes them. The agent checks
  whether they fit the task and records command, result, and limitation.
- For changed executable code, review with evidence before delivery. Use
  review-changes with the current evidence contract and --require-evidence.
  Record base/head and the identity of local changes reviewed; the HEAD SHA alone
  does not identify the working tree. If content or revision changes, reassess
  coverage and invalidate or rerun affected evidence before completion.
  Simple documentation does not require a heavy process or tests that only
  check words in text.
- Completion requires mandatory criteria and applicable validations to be green.
  A failed or unavailable required environment remains a documented blocker;
  do not claim tests passed without execution.
- Updating an image requires a rebuild and exercising the changed route or flow;
  a healthy process does not prove the current code is present.
- Handoff includes files, behavior, validations, and actual outstanding work.
  Use project.language for tickets and plans.
- For long or interrupted work, record the last completed step, revision and
  evidence, blocker, and next action in the plan; include actual PR/ticket
  states where applicable. On resume, reread the record and current state. Do not
  repeat completed mutations or reuse evidence for changed content. For a small
  task, keep this record in the handoff without creating extra artifacts.

## Integrations and authority

- Read .agents/integrations/github.md or clickup.md only when using the service.
  tracking.provider = none allows work with local plans.
- Creating PRs, commenting, updating status, or publishing depends on authorized
  scope; enabling a provider in the profile does not trigger these operations.
- delivery.create_pr expresses a preference. Respect the task's authorization.
  Merge and closure require an explicit request; fast-merge only serves that mode.
- Do not copy tokens, passwords, credential files, personal MCPs, or permission
  configuration between projects. Use the available authentication mechanisms.
