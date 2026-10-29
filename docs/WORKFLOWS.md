# Evidence, completion and resumption

Canonical workflows link criteria, review and results to the content actually
examined. The amount of recorded information should match the size of the task.

## Questions and decisions

When a decision needs user input, the agent uses the session's native question
tool when available, with grounded choices and a way to give a custom answer.
If it is unavailable, the agent asks in chat. Decisions already resolved by the
request or project context are not asked again. Enrichment, implementation and
ticket writing can group related questions and continue independent work while
waiting. Guided setup instead collects its answers before making changes, as
described in [guided setup](SETUP.md).

## Criteria and validation

The [plan template](../.agents/templates/PLAN.md) assigns stable IDs to criteria.
The validation matrix links each ID to implementation/tests and evidence. Until a
test runs, record the expected result and pending state. Afterwards, replace the
expectation with the command/artifact, observed result and covered revision. A
green test that does not cover a criterion does not complete it.

Use [enrich-plan](../.agents/skills/enrich-plan/SKILL.md) to prepare the links and
[implement-ticket](../.agents/skills/implement-ticket/SKILL.md) to maintain them
during implementation. Do not create tests that merely search documentation for
words.

## Evidence identity

Record base and head when available, plus the identity of the local diff or a
snapshot of the files examined. HEAD SHA alone does not identify uncommitted
changes. If there are no commits, use a verifiable snapshot and declare that
condition without inventing a SHA.

Changes to head or local content require assessing their impact on evidence.
Invalidate and repeat affected reviews/tests; do not claim a new revision is
covered by an old result. New [reviews](../.agents/skills/review-changes/SKILL.md)
use the v2 contract and validator option `--require-evidence`.

## Proportionate checkpoint

For long or interrupted work, record in the plan itself:

- The last step actually completed.
- The corresponding revision and evidence.
- The actual blocker, or absence of one.
- The next concrete action.
- PR/ticket identifiers and states and merge commit, when available.

When resuming, reread the records and inspect current state before acting. Do not
repeat completed mutations or treat recorded intent as proof of success. For a
small task, this information can be in the handoff; there is no need to create
an additional plan or artifact solely for a checkpoint.

## Merge and partial closure

[merge-and-close](../.agents/skills/merge-and-close/SKILL.md) distinguishes open,
merged and closed-without-merge PRs. A merged PR may have only ticket closure
pending: verify its identity and commit and proceed only with that authorized
step. An already completed ticket needs no repeated update. A PR closed without
merge is a blocker, not authorization to reopen it or create another PR.

For an open PR, bind checks/reviews to head SHA and use a merge conditional on the
expected SHA when supported by the tool. Revalidate if head changed. Without this
capability, reread immediately before the operation and report the atomicity
limit. If the project requires an atomic guarantee, its absence is a blocker.

Updating the local base may remain pending if the checkout does not allow a safe
fast-forward. Report that state separately from the merge and ticket.

## Direct merge

[fast-merge](../.agents/skills/fast-merge/SKILL.md) continues to bypass PR, CI and
tracker when explicitly requested. Preparation checks the source branch, HEAD,
clean working tree, remote and target. The workflow records the remote SHA used
for the merge and pushes the resulting SHA explicitly, without force.

Conflicts or unexpected state stop the sequence. Preserve changes and wait for a
decision on resolution; do not stash, reset, clean or abort as a side effect.
After interruption, confirm local and remote state before resuming, including
when the push response was not received.
