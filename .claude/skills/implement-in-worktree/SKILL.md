---
name: implement-in-worktree
description: "Prepares an isolated worktree and follows the ticket implementation workflow."
---

# Implement in a worktree

Read the profile, plan and dependencies. If already in the correct worktree,
follow implement-ticket. Do not recreate or reset an existing worktree.

Resolve the branch using git.branch_pattern and the base using git.base_branch.
Check git worktree list to find existing checkouts and avoid a branch already
active elsewhere. Preserve the main checkout. Prefer the native worktree feature
when available; otherwise use Git with an explicit agreed or task-derived
directory outside product files.

Fetch the remote/base when needed. Create the worktree from the resolved base
or reuse the existing branch without resetting. Do not change the branch of the
main checkout as a preparation step.

Confirm cwd, git branch --show-current and git worktree list before editing.
Use explicit paths if the runtime cannot change the session's working directory.
Check that .specdev and the skills exist in the new checkout; if configuration
was only in uncommitted changes, prepare the kit there without copying product
files or credentials from the main checkout.

Follow implement-ticket, skipping the branch creation already completed.
Define ports, database, queues and data per worktree before starting UI or
integration services. Do not assume shared infrastructure is safe.
The kit does not provision database slots or copy secrets automatically.
Deliver the path, branch, validations and URLs produced. Remove/archive the
worktree only when it is no longer needed and the action is authorized.
