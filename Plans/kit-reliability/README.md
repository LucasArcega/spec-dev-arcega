# Kit reliability and contract evolution

**Local identifier:** kit-reliability
**Status:** Completed locally
**Branch:** existing main, with no commits at that time; publication was not authorized.
**Dependencies:** no new external dependencies.

## Accepted scope

Fix audit findings P2/P3 and evolve items 4 through 8 of the response: traceable
review, agents, delivery resumption, configuration diagnostics, and links between
criteria and evidence. Preserve existing consumers, canonical source, Python 3.11+
and the standard library.

## Criteria and evidence

| ID | Required behavior | Implementation/test | Evidence and review |
| --- | --- | --- | --- |
| AC1 | Equivalent EOL does not block installation; real edits remain protected | scripts/specdev.py; CRLF, legacy and binary tests | Passed; full suite and review with no open findings |
| AC2 | Review schema and validator agree, preserving legacy | schema/validator; tests/test_review_contract.py | Passed; valid/invalid cases and schema-interpreted rules |
| AC3 | New reviews record scope, checks and blockers | Review v2 and --require-evidence flag | Passed; CLI, evidence, blocker and compatibility tests |
| AC4 | Agents have defined return/interruption behavior and supported native options | DELEGATION, roles, generator and option tests | Passed; reviewed contracts, TOML/frontmatter and client isolation tested |
| AC5 | Delivery resumes a completed merge and links evidence to validated content | implementation, merge and fast-merge skills | Passed contract review; no external mutations executed |
| AC6 | Diagnostics separate integrity, configuration and availability without executing commands | doctor and snapshot/marker tests | Passed; cwd-relative PATH, marker not executed, files preserved |
| AC7 | Plans link criteria to implementation/tests and evidence | PLAN template, enrich-plan and WORKFLOW | Passed contract review and this plan's record |

## Validation

- `python -m unittest discover -s tests -v`
- `python scripts/specdev.py validate`
- `python scripts/specdev.py check --target .`
- `python scripts/specdev.py doctor --target .`
- Structured v2 review against an earlier snapshot, because Git had no commits.

On 27 October 2026, 49 tests passed on Python 3.14.0 (44.999 s). `validate`
returned nine skills; `check` returned no issues/warnings; `doctor` reported all
three groups ready and `executed=false`; `install --dry-run` returned `changed=[]`.
Adapters were regenerated with backups by the installer. Consolidated review in
[review.json](review.json), validated with `--require-evidence`.

The sandbox's default TEMP/TMP denied access during the audit; a writable
folder was used when necessary. This does not change the expected suite result.
Client discovery does not prove all external workflows.

## Checkpoint

- Last confirmed step: implementation, adaptation, review and validation completed.
- Validated content: SHA-256 snapshot in review.json; Git had no commits at that time.
  Both independent review hashes were rechecked after the full suite.
- Blockers: none known.
- Next action at that time: local handoff; publication, commit and merge required a separate request.

## Validation limits

Python 3.11 and the Cursor/Claude clients were not exercised for this change.
Actual models and allowlists were checked as configuration/generated formats,
without checking account availability. Merge/closure were reviewed as contracts;
no real GitHub or tracker operations were performed as part of that work.

## Out of scope

Behavioral evaluation corpus for item 3, new providers, new roles, publication,
commit, merge and changes to JourneyCore.

The accompanying review JSON is a translation of the historical record; its
original recorded snapshot hashes and scope identifiers are unchanged.
