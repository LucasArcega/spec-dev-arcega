# Kit next improvements

**Status:** Proposed
**Priority:** Not defined
**Dependencies:** Access to representative client sessions for interactive validation.

## Why

The installer and review contract have automated coverage, but that does not
prove how agents use the skills in real client sessions. Improve confidence in
client behavior, compatibility, upgrades, and guided setup without imposing a
stack or changing consumer-owned configuration.

## Scope and sequence

1. Exercise setup-project, enrich-plan, and implement-ticket in Codex, Cursor,
   and Claude Code. Record client version/mode, scenarios, observed outcomes,
   native selector availability, and untested combinations.
2. Create repeatable agent evaluation scenarios using isolated consumer projects:
   preservation of existing configuration, setup interview ordering, ambiguous
   plan decisions, and implementation scope. Compare actual artifacts and actions
   with expected behavior; do not replace client smoke tests with text assertions.
3. Add GitHub CI for the existing unit suite, skill validation, and integrity
   check, including Python 3.11 and a newer supported version. Validate platform
   coverage according to available runners and report limitations.
4. Improve upgrade guidance: find the installed version, preview changes, handle
   conflicts while preserving local customizations, and maintain a changelog.
5. After the client evaluations, simplify duplicated or rigid skill instructions
   where evidence supports it, preserving data and compatibility guarantees.
6. Explore an optional way to export interview answers on explicit interruption,
   without writing files between questions. Select a solution only after assessing
   client capabilities, privacy, and the existing question-first requirement.

## Acceptance criteria

- [ ] AC-01 — Record reproducible client smoke-test outcomes and limitations for
  each skill and client; identify where selectors are exposed and observed.
- [ ] AC-02 — Provide isolated, repeatable scenarios with observable checks for
  preservation, interview sequencing, plan decisions, and implementation scope.
- [ ] AC-03 — CI runs applicable project validations on Python 3.11 and a newer
  version, with actionable failures and any platform limitations documented.
- [ ] AC-04 — Upgrade instructions and changelog let consumers identify versions,
  preview updates, and handle conflicts without losing their configuration.
- [ ] AC-05 — Any instruction simplification is justified by observed behavior,
  retains the existing contracts, and is validated against affected scenarios.
- [ ] AC-06 — Document the interruption-resume options and their tradeoffs; any
  selected implementation requires a separate decision and must not write between
  interview questions.

## Validation

Before implementation, expected evidence is pending. Record client versions,
scenarios, outcomes, artifacts, commands, results, and the revision actually
validated. Run the repository's configured unit, skill, and integrity checks for
changes where applicable. Interactive client results must not be inferred from
automated installer tests.

## Additional observations for discussion

The architectural-contract and Node/React implementation is tracked separately
in [architecture-node-react](../architecture-node-react/README.md); its client
behavior still needs validation. The notes below capture the earlier baseline.

The current review contract covers bugs, regressions, security, contracts,
concurrency and test gaps with structured evidence, but does not require an
explicit review of project-specific architectural boundaries. The generic profile
has no validation commands, and the Python profile does not configure a linter.
Possible follow-up work: identify and document the consumer's architectural
constraints, include applicable constraints in review, and discover existing
lint/static-analysis commands during setup. Decide scope and tooling with the
user before adding these items to acceptance criteria; do not impose a universal
architecture or linter on consumer projects.

## Out of scope

Publishing, changing consumer projects or global client configuration, and
installing a particular language, architecture or lint tool by default.
