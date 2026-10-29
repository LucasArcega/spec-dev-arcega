# Architectural contracts and Node/React context

**Status:** Implemented; interactive client validation pending
**Priority:** Not defined
**Dependencies:** None identified.

## Scope and acceptance criteria

- [ ] AC-01 — Guided setup captures confirmed project-specific architectural
  boundaries, allowed and forbidden dependencies, exceptions, sources and checks
  in consumer-owned context, without inventing constraints or writing during the
  interview. Existing setup state and consumer documents remain compatible.
- [ ] AC-02 — Planning, implementation and review consult applicable recorded
  boundaries; review reports a concrete violation and relevant coverage limits.
- [ ] AC-03 — Selectable Node and React contexts and initial profiles support
  either stack independently or together without assuming commands or tools.
- [ ] AC-04 — Setup identifies existing lint, static analysis and architectural
  checks as project-specific validation, without installing or executing them.
- [x] AC-05 — Temporary consumer tests cover profile installation, update and
  preservation. Documentation, generated adapters and version are synchronized.

## Validation

Expected: the unit suite, kit validation, integrity check and an idempotent
installation dry-run pass. Interactive agent behavior remains a separate client
smoke test; do not equate installer tests with proof of review quality.

Observed locally: 54 unit tests passed under Python 3.14, including installation
and preservation in temporary Node and React consumers. Kit validation and
integrity checks passed, and the installation dry-run was empty. Interactive
setup, planning, implementation and review have not been exercised across actual
client sessions; AC-01 through AC-04 remain pending that behavioral check.
