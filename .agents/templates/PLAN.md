# {{ticket}} - {{title}}

**Branch:** {{branch}}
**Status:** {{current_state}}
**Priority:** {{priority_or_not_defined}}
**Dependencies:** {{verified_dependencies}}
**Ticket:** {{ticket_url_or_local_id}}

## Why

{{problem_and_expected_value}}

## Scope

{{accepted_scope}}

## Acceptance criteria

- [ ] AC-01 — {{observable_required_behavior}}

Keep IDs stable when revising the plan; add only accepted criteria.

## Technical plan

{{links_to_existing_backend_frontend_and_test_plans}}

## Validation

{{commands_working_directories_prerequisites_and_expected_evidence}}

| Criterion | Implementation/test | Evidence and revision | State |
| --- | --- | --- | --- |
| AC-01 | {{real_file_or_test_or_planned_location}} | {{expected_evidence_until_executed_then_result_artifact_and_revision}} | {{pending_passed_failed_or_blocked}} |

Before execution, describe the expected evidence and keep the state pending.
Afterward, record the observed result, artifact/command, base/head, and local
change or snapshot identity. A content change requires reassessing this coverage.

## Resumption — for long or interrupted work

**Last completed step:** {{last_completed_step}}
**Revision and evidence:** {{base_head_local_change_identity_and_evidence}}
**Blocker:** {{actual_blocker_or_none}}
**Next action:** {{next_action}}
**External delivery:** {{pr_ticket_identifiers_states_and_merge_commit_when_applicable}}

Remove this section when inapplicable; do not create another artifact just for a checkpoint.

## Out of scope

{{excluded_work_and_known_followups}}
