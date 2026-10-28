# {{ticket}} - {{title}}

**Branch:** {{branch}}
**Status:** {{current_state}}
**Prioridade:** {{priority_or_not_defined}}
**Dependências:** {{verified_dependencies}}
**Ticket:** {{ticket_url_or_local_id}}

## Por quê

{{problem_and_expected_value}}

## Escopo

{{accepted_scope}}

## Critérios de aceite

- [ ] AC-01 — {{observable_required_behavior}}

Mantenha os IDs ao revisar o plano; acrescente apenas critérios aceitos.

## Plano técnico

{{links_to_existing_backend_frontend_and_test_plans}}

## Validação

{{commands_working_directories_prerequisites_and_expected_evidence}}

| Critério | Implementação/teste | Evidência e revisão | Estado |
| --- | --- | --- | --- |
| AC-01 | {{real_file_or_test_or_planned_location}} | {{expected_evidence_until_executed_then_result_artifact_and_revision}} | {{pending_passed_failed_or_blocked}} |

Antes da execução, descreva evidência esperada e mantenha estado pendente.
Depois, registre resultado observado, artefato/comando e base/head mais identidade
do diff local ou snapshot. Uma mudança de conteúdo exige reavaliar essa cobertura.

## Retomada — quando o trabalho for longo ou interrompido

**Último passo concluído:** {{last_completed_step}}
**Revisão e evidências:** {{base_head_local_change_identity_and_evidence}}
**Bloqueio:** {{actual_blocker_or_none}}
**Próxima ação:** {{next_action}}
**Entrega externa:** {{pr_ticket_identifiers_states_and_merge_commit_when_applicable}}

Remova esta seção quando não se aplicar; não crie outro artefato só para checkpoint.

## Fora do escopo

{{excluded_work_and_known_followups}}
