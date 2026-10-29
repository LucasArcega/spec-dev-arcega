# English language migration

**Status:** Completed locally

## Scope

Translate the kit's canonical instructions, agents, skills, templates,
documentation and installer messages into English. Set new profiles and this
project to English while preserving existing consumer configurations. Keep
identifiers, commands, paths and project-specific integration values unchanged.
Regenerate client adapters and verify upgrades from the existing version.

## Acceptance criteria

| ID | Required behavior | Evidence |
| --- | --- | --- |
| AC-01 | Canonical guidance, skills and templates are in English with behavior preserved | Translation review approved; validate recognized all 10 skills |
| AC-02 | Installer and generated client instructions are in English | 53 tests passed; validate/check passed; installer dry-run reported no changes |
| AC-03 | New profiles default to English; upgrades preserve consumer language and instructions | Automated regression tests and an actual 0.3-to-0.4 temporary upgrade passed |
| AC-04 | README, installation guide and documentation are in English and links work | Documentation review and local link checks passed; README command examples exercised |
| AC-05 | Existing project-specific values and historical evidence remain accurate | Review confirmed preserved IDs, statuses, hashes and recorded facts; historical reviews validate |

## Validation

- `python -m unittest discover -s tests -v`
- `python scripts/specdev.py validate`
- `python scripts/specdev.py check --target .`
- Review of the actual changes and generated artifacts.

Results: 53 tests passed in Python 3.14.0; `validate` recognized all 10 skills;
`check` passed without issues or warnings; installation dry-run reported no
changes. An isolated upgrade from committed version 0.3.0 preserved a `pt-BR`
consumer profile, local instructions, context and setup checkpoint. Reviews
of the migration, canonical guidance and documentation found no actionable
issues. The consolidated [review](review.json) identifies the reviewed snapshot.

## Checkpoint

Translation, adapter regeneration, review and validation are complete locally.
The previous state is the repository HEAD. No commit, push, merge or publication
was requested for this task.

## Validation limits

Python 3.11 and real Cursor and Claude sessions were not exercised. An additional
interactive English setup smoke test could not run because its subagent hit a
usage limit. The existing JourneyCore example deliberately retains its actual
`pt-BR` locale and tracker status names as project-specific data.
