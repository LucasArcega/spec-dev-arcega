---
name: implement-ticket
description: "Implements a ticket or plan through review, validation and handoff, with external delivery only when authorized."
---

# Implement a ticket

Read .specdev/project.json and .agents/rules/WORKFLOW.md. The lead owns scope,
contracts, integration and completion.

1. Resolve the ticket/plan, dependencies and Git state. Read actual code and
   tests. Identify affected backend, frontend, UI, infrastructure and docs.
   tracking.provider = none allows the full workflow with a local plan.
   When resuming, check the last recorded step and current state before acting;
   preserve completed operations and reassess evidence whose content changed.
2. If the plan needs enrichment, follow enrich-plan before implementation.
   Clarify only decisions that change scope, using the shared native-question
   guidance in WORKFLOW.md. Apply the same rule to scope decisions discovered
   during implementation; continue independent work while waiting where possible.
   Do not invent dependencies.
3. If the task requires a branch, use git.branch_pattern and git.base_branch.
   Preserve existing changes; reuse the correct branch if already active.
4. Define contracts before delegating parts with exclusive files. Consult
   .agents/rules/DELEGATION.md. Work sequentially when there is no independent
   work or subagent runtime.
5. Implement accepted criteria, using focused tests during changes. Check plan
   against code and complete required gaps without expanding scope. Link each
   criterion ID to its files/tests and evidence in the plan. Respect applicable
   documented architectural boundaries and exceptions in selected context; do
   not silently introduce a new dependency or ignore a relevant unknown boundary.
6. Run review-changes on the relevant diff; fix meaningful bugs and regressions.
   Use review v2 and validate with --require-evidence. Record base/head and the
   identity of the local diff or file snapshot; HEAD alone does not cover local
   changes. Revalidate behavior affected by fixes and update the evidence.
7. Run the validation matrix applicable to changed surfaces with real cwd,
   arguments and prerequisites. UI requires the coverage agreed in the plan;
   persistence and shared contracts require relevant integration coverage.
   No configured commands means validation is not yet defined, not automatic approval.
8. Mark the plan complete and update paths.status only when required criteria
   and checks have green evidence. Preserve history. Confirm review and tests
   cover the current revision and content; a change in head or files requires
   reassessing and repeating affected coverage.
9. Prepare commit/push/PR only when requested. If delivery.create_pr is enabled
   and there is authorization, follow create-pr. Merge and closure are not part
   of this workflow.

The handoff includes behavior, files, branch, tests and results, blockers, produced
URLs/artifacts and exclusions. An unavailable environment is not approval. Do
not claim publication, review or testing without evidence.

For long work, update a checkpoint in the plan after each completed phase or
interruption: last step, revision/evidence, blocker and next action. Include
actual PR/ticket states when applicable. Resuming does not grant additional
authorization to commit, publish, merge or close.
