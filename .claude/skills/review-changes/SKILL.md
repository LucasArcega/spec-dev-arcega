---
name: review-changes
description: "Reviews a diff or set of files and returns structured findings for a correction cycle."
---

# Review changes

Read the profile, plan criteria and requested diff. The base comes from the
request or git.base_branch. Distinguish committed and local changes: a branch
diff does not automatically include the working tree. Record the actual set reviewed.

Review bugs, regressions, security, contracts, concurrency and test gaps related
to behavior. Inspect real context and lines. For broad code, use
specdev-reviewer on independent portions when available; keep the consolidated
result under the lead's responsibility. Do not require a specific executable or
change the session model. If using a CLI, inspect the version's capabilities and
available path; do not force blocked binaries or relax permissions as a prerequisite.

Inspect the selected project context for architectural boundaries and applicable
exceptions. For affected components, check dependency direction, responsibilities
and existing enforcement tests or static checks against the actual diff. Report
a concrete introduced violation with its project rule, source, code location,
condition and consequence; distinguish pre-existing violations and allowed
exceptions. Record missing or unverified rules and checks as limitations when
relevant; do not invent an architecture or claim an unrun check passed.

Produce v2 JSON according to references/review.schema.json, with schema_version = 2:
- summary and verdict (approve, request_changes or blocked).
- scope with non-empty base, head and files. Resolve exact revisions; for local
  files use an explicit working tree/snapshot identity and record reviewed files.
- checks with cwd, argv, status (passed, failed or not_run) and evidence.
  Record only actually executed commands as passed/failed; reading tests or an
  unavailable environment is not execution. Do not invent checks to fill the document.
- limitations and blockers as lists of text; use empty lists when absent.
- findings containing severity (P1/P2/P3), file, line, title and body.

P1 blocks for a severe failure; P2 is a meaningful bug or regression; P3 is a
low-impact observation. Each finding explains verifiable conditions and effects.
approve requires no P1/P2, blockers or failed/not_run checks. request_changes
requires at least one P1/P2; blocked requires an explicit blocker.
Checks may be empty when no commands apply; explain a relevant limitation without
inventing execution. Invalid JSON does not complete the review.
The validator still accepts the legacy format without the flag below for
history/compatibility only; it does not replace v2 evidence for new reviews.

Use the local validator:
python .agents/skills/review-changes/scripts/validate_review.py PATH_TO_JSON --require-evidence

When authorized to fix, implement relevant findings and run affected tests.
For broad fixes, perform another focused review. If reviewer/parsing fails, try
once with a smaller set; if it still fails, record the blocker. Do not discard
findings merely because the limit was reached. Report the reviewed set,
limitations, open findings and validation evidence.
If base, head or local files change, reassess the affected portion and update the
review identity before reusing evidence. The validator checks the contract; it
does not prove that paths exist, commands ran or coverage is sufficient.
