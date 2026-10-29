---
name: fast-merge
description: "Performs a direct Git merge when the user requests fast-merge or a merge without PR and CI."
---

# Direct merge

Activate only on an explicit request for direct merge/fast-merge.
Read git.remote and git.base_branch from the profile; an explicit target in the
request takes precedence. The current branch is the source. This workflow
dispenses with PR, CI and tracker gates; do not publish to another target or force.

Before mutation, check cwd/repository, source branch and HEAD SHA. Require HEAD
on a branch and a clean tree, including untracked files and no merge/rebase in
progress. If not clean, record the blocker; do not stash, auto-commit, reset or
clean. Validate remote identity and target branch name without changing the
remote or deducing another destination.

With remote and target resolved, execute sequentially, passing values as
arguments without building shell commands from interpolated text:
1. git fetch REMOTE
2. Resolve and record the SHA of refs/remotes/REMOTE/TARGET. If the ref does not
   exist, stop. Recheck source/HEAD/state for changes.
3. git merge --no-edit TARGET_SHA
4. Record RESULT_SHA and confirm the source branch is still active and the
   tree is clean. git push REMOTE RESULT_SHA:refs/heads/TARGET

Do not check out the base, create a PR or close a ticket.
If there is a conflict, do not resolve or abort automatically. Show git status
and git diff --name-only --diff-filter=U; wait for a decision.
If push or another command fails, present the error and stop; do not retry in a
loop or use --force. Confirm the remote ref after pushing and report source,
target and published SHA. After interruption, reread local and remote Git state
before resuming; do not repeat a confirmed push or assume success from a missing
response. Session authentication and permissions still apply.
