# Review contract

New reviews use `schema_version: 2` and the schema at
`.agents/skills/review-changes/references/review.schema.json`. The Python
validator interprets this contract directly using the standard library; it does
not maintain a second definition of content and verdict rules.

## Evidence v2

Structural example; replace identities, commands and evidence with real values:

~~~json
{
  "schema_version": 2,
  "summary": "Reviewed the listed files; no significant findings.",
  "verdict": "approve",
  "scope": {
    "base": "VERIFIED_BASE_SHA",
    "head": "VERIFIED_HEAD_SHA",
    "files": ["src/file.py"]
  },
  "checks": [
    {
      "cwd": ".",
      "argv": ["python", "-m", "unittest", "discover", "-s", "tests", "-v"],
      "status": "passed",
      "evidence": "Command executed; record the actual result and artifact when available."
    }
  ],
  "limitations": [],
  "blockers": [],
  "findings": []
}
~~~

`scope` requires base, head and a nonempty file list. For local changes, include
an explicit identity such as `working-tree:SNAPSHOT_ID`, recorded with
the inspected files. In a repository without commits, declare `unborn` as the
base and identify the local snapshot. Branch names alone may change and do not
prove what content was reviewed. If content changes, reassess the review and
affected checks before reusing evidence.

Each check records cwd, separate arguments, status and textual evidence. `passed`
and `failed` require observed execution; `not_run` explains why it was not run.
Reading test code is not execution. A review without applicable commands may
have `checks: []`, with the relevant limitation explained. Do not invent commands
to fill the document.

- `approve`: no P1/P2, blockers or failed/not_run checks; P3 is allowed.
- `request_changes`: at least one P1/P2 finding with condition and consequence.
- `blocked`: at least one blocker, such as an unavailable required environment.

`limitations` describes coverage limits; `blockers` describes impediments that
prevent completing the review. Both are arrays of nonempty strings or empty
arrays. Findings retain severity, file, line, title and body.

~~~powershell
python .agents/skills/review-changes/scripts/validate_review.py review.json --require-evidence
~~~

## Compatibility and limits

The exact legacy `summary/verdict/findings` format remains accepted without
`--require-evidence`, including an empty `request_changes` as before. The flag
requires v2; legacy does not provide the evidence required for new reviews.
Approval with P1/P2 is rejected in both formats and by the published schema.

Strings must contain something beyond the Unicode White_Space characters listed
explicitly in the schema. Lines follow JSON Schema integer semantics: `1.0`
represents integer 1 and is accepted; booleans, fractions and non-finite values
are rejected. Unknown fields are rejected.

The validator implements only the features used by the bundled schema, with local
references. It is not a general-purpose JSON Schema engine. Schema changes using
another feature require corresponding support and tests.

Document validity does not prove that paths or lines exist, that a review or
execution occurred, or that coverage is sufficient. The primary agent verifies
evidence before handoff. The validator does not run commands, access Git,
contact services or write to the project.
