---
name: merge-and-close
description: "Merges a validated PR and closes its ticket when the user requests that delivery."
---

# Merge and close

Use when the user requests merge and closure. Read the profile and integrations.
The initial version uses GitHub for PRs and GitHub/ClickUp/none for tracking.

Confirm Git state and the exact repository, PR number, head and base.
Do not pick commits or modify pending files as part of this workflow.
Resolve a single PR; if one does not yet exist and creation is authorized,
follow create-pr and query again.

Read the PR state again before choosing the next step:
- Open: record the reviewed head SHA, validate mergeability and required
  checks/reviews for that revision. If draft, mark ready only within the
  authorized delivery after checking the conditions.
- Already merged: confirm repository/head/base, merge date and commit, and the
  association with the ticket. Skip merge and proceed only with authorized pending steps.
- Closed without merge: record the blocker; do not reopen or choose another PR
  on your own.

Do not use --admin, --force or bypass protections.

Before merging, resolve and read a single ticket when a tracker is in use.
Avoid a merge that cannot afterward be associated with the correct ticket.
Only for an open PR, use the project's merge method or the user's specified one.
Use an expected-SHA condition when the available API/CLI supports it. If head
changes, invalidate the previous approval and revalidate the new revision.
Without a conditional operation, reread head and checks immediately before
merging and record that the check is not atomic; do not promise race protection.
If the project requires that guarantee and the tool cannot provide it, record
the blocker. Do not repeat the merge for an already merged PR.
Read the PR back and confirm merged state, date and commit.

Update the local base only if its checkout is clean and the branch is not in
use in another worktree. Use fast-forward; report a pending action otherwise.
Read the ticket again and close it in the configured valid status only if still
pending. If already complete, confirm the state without repeating the update.
If merge succeeded and closing failed, report both actual states; do not repeat
the merge or declare delivery complete.

Record in the plan or handoff the PR/ticket, validated SHA and merge commit,
last completed step, evidence, blocker and next action. Resuming starts by
reading these states again; updating the local base can remain independently pending.
