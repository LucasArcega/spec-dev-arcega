# Guided, client-independent setup

**Local identifier:** setup-project

**Status:** Completed locally

**Dependencies:** kit installed in the consumer project; agent reading, editing
and conversation capabilities. Terminal and external tools are optional.

## Why and scope

Let an agent investigate a project, ask about missing relevant decisions and
progressively record consumer-specific details. The same canonical definition
must work in supported clients and be readable by other agents; the installer
preserves existing formats and data.

| Criterion | Implementation and validation | Evidence and state |
| --- | --- | --- |
| AC-01 — Setup discovers context and asks one decision at a time, distinguishing facts, hypotheses and answers | Skill and questions guide | Passed: isolated interview and review, including IDs with multiple fields |
| AC-02 — Configuration, context and checkpoint belong to the consumer, preserve data and allow resumption | Skill, template and isolated scenario | Passed: resumptions preserved answers and context; partial confirmation reopened |
| AC-03 — Workflow is independent of editor, CLI and doctor; declarative commands do not run automatically | Skill and isolated scenario | Passed: scenario did not require doctor, Python or project commands; contract reviewed |
| AC-04 — Installer distributes skill and resources without creating consumer state/context | Tests in temporary directories | Passed: distribution for all three adapters and absence of local files tested |
| AC-05 — Updates preserve checkpoint, local context and existing profile | Tests in temporary directories | Passed: skill and Claude-copy update preserved local data |
| AC-06 — Catalog, documentation and adapters indicate the new capability | Generation, validate and check | Passed: 10 skills, integrity check and dry-run with no changes |

## Validation

- Independent usage test in a temporary consumer, without external services.
- `python -m unittest discover -s tests -v`.
- `python scripts/specdev.py validate` and `python scripts/specdev.py check --target .`.
- Review of the actual set of files and generated state.

On 27 October 2026, 51 tests passed on Python 3.14.0 (38.148 s). `validate`
returned ten skills; `check` reported no issues/warnings; `install --dry-run`
reported no changes; the skill validator passed. Independent evaluation included
two resumptions in a temporary project and verified data preservation. Review
identified and followed a fix for a P2 in composite decisions; the new review and
resumption test found no open findings.

## Checkpoint

**Last step:** implementation, distribution, review and validation completed.

**Review/evidence:** [review.json](review.json); snapshot identified by hash,
because the repository had no commits at that time.

**Blocker:** none known.

**Next action at that time:** local handoff; publishing or committing required a separate request.

## Limitations

The interview test used agents in a Codex session, a fictional project and
simulated answers; it does not replace a Cursor or Claude smoke test. Automated
tests ran on Python 3.14; Python 3.11 was not exercised.

## Out of scope

Automatically executing setup in the kit's own repository, new external
integrations, publication, commit, merge or credential changes.

The accompanying review JSON is a translation of the historical record; its
original recorded snapshot hashes and scope identifiers are unchanged.
