---
name: review-changes
description: "Revisa um diff ou conjunto de arquivos e devolve achados estruturados para um ciclo de correção."
---

# Revisar mudanças

Leia o perfil, os critérios do plano e o diff solicitado. A base vem do pedido
ou de git.base_branch. Distinga mudanças commitadas e locais: um diff de branches
não contém automaticamente o working tree. Registre o conjunto efetivamente revisado.

Revise bugs, regressões, segurança, contratos, concorrência e lacunas de testes
relacionadas ao comportamento. Inspecione contexto e linhas reais.
Para código amplo, use specdev-reviewer em partes independentes, se disponível;
mantenha o resultado consolidado sob responsabilidade do principal.
Não exija um executável específico nem troque o modelo da sessão.
Se usar CLI, inspecione as capacidades da versão e o caminho disponível;
não force binários bloqueados nem relaxe permissões como pré-requisito.

Produza JSON v2 conforme references/review.schema.json, com schema_version = 2:
- summary e verdict (approve, request_changes ou blocked).
- scope com base, head e files não vazio. Resolva revisões exatas; para arquivos
  locais use identidade explícita de working tree/snapshot e registre os arquivos.
- checks com cwd, argv, status (passed, failed ou not_run) e evidence.
  Registre apenas comandos realmente executados como passed/failed; leitura de
  testes ou ambiente indisponível não é execução. Não invente checks para preencher.
- limitations e blockers como listas de textos; use listas vazias quando ausentes.
- findings contendo severity (P1/P2/P3), file, line, title e body.

P1 bloqueia por falha grave; P2 é bug ou regressão relevante; P3 é observação de
baixo impacto. Cada finding explica condição e consequência verificáveis.
approve exige ausência de P1/P2, de blockers e de checks failed/not_run.
request_changes exige ao menos um P1/P2; blocked exige um blocker explícito.
Checks podem ficar vazios quando não houver comandos aplicáveis; explique a
limitação pertinente sem inventar execução. JSON inválido não conclui o review.
O formato legado continua aceito pelo validador sem a flag abaixo apenas para
histórico/compatibilidade; não substitui evidência v2 em novas revisões.

Use o validador local:
python .agents/skills/review-changes/scripts/validate_review.py CAMINHO_DO_JSON --require-evidence

Ao receber autorização para corrigir, implemente os achados pertinentes e rode
testes afetados. Para correção ampla, faça uma nova revisão delimitada.
Se o reviewer/parse falhar, tente uma vez com conjunto menor; persistindo,
registre o bloqueio. Não descarte achados apenas porque o limite foi atingido.
Informe conjunto revisado, limitações, achados abertos e evidência de validação.
Se base, head ou arquivos locais mudarem, reavalie o trecho afetado e atualize a
identidade da revisão antes de reutilizar evidência. O validador confere contrato,
não comprova a existência dos caminhos, a execução dos comandos ou sua cobertura.
