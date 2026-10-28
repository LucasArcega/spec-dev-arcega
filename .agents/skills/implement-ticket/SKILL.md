---
name: implement-ticket
description: "Implementa um ticket ou plano até revisão, validação e handoff, com entrega externa somente quando autorizada."
---

# Implementar ticket

Leia .specdev/project.json e .agents/rules/WORKFLOW.md.
O principal mantém escopo, contratos, integração e conclusão.

1. Resolva ticket/plano, dependências e estado Git. Leia código e testes reais.
   Identifique backend, frontend, UI, infra e documentação afetados.
   tracking.provider = none permite execução integral com plano local.
   Ao retomar, confira o último passo registrado e o estado atual antes de agir;
   preserve operações concluídas e reavalie evidências cujo conteúdo mudou.
2. Se o plano precisar ser enriquecido, siga enrich-plan antes de implementar.
   Esclareça somente decisões que mudem o escopo. Não invente dependências.
3. Se a tarefa exigir branch, use git.branch_pattern e git.base_branch.
   Preserve alterações existentes; reutilize a branch correta quando já ativa.
4. Defina contratos antes de delegar partes com arquivos exclusivos.
   Consulte .agents/rules/DELEGATION.md. Execute sequencialmente se não houver
   trabalho independente ou runtime de subagents.
5. Implemente os critérios aceitos, usando testes focados durante a mudança.
   Confira plano versus código e complete lacunas obrigatórias sem expandir escopo.
   Relacione cada ID de critério aos arquivos/testes e à evidência obtida no plano.
6. Faça review-changes no diff pertinente; corrija bugs e regressões relevantes.
   Use review v2 e valide com --require-evidence. Registre base/head e a identidade
   do diff local ou snapshot dos arquivos; HEAD sozinho não cobre mudanças locais.
   Revalide o comportamento afetado pelas correções e atualize a evidência.
7. Execute a matriz de validation aplicável aos surfaces alterados, com cwd,
   argumentos e pré-requisitos reais. UI exige a cobertura acordada no plano;
   persistência e contratos compartilhados exigem integração pertinente.
   Nenhum comando configurado significa validação ainda não definida,
   e não aprovação automática.
8. Só marque o plano concluído e atualize paths.status quando critérios e
   verificações obrigatórias tiverem evidência verde. Preserve o histórico.
   Confirme que review e testes cobrem a revisão e o conteúdo atuais; mudança de
   head ou de arquivos exige avaliar e repetir a cobertura afetada.
9. Prepare commit/push/PR somente quando essa entrega estiver no pedido.
   Se delivery.create_pr estiver habilitado e houver autorização, siga create-pr.
   Merge e fechamento não são parte deste fluxo.

O handoff apresenta comportamento, arquivos, branch, testes executados e seus
resultados, bloqueios, URLs/artifacts produzidos e exclusões. Ambiente indisponível
não é aprovação. Não afirme que publicou, revisou ou testou sem evidência.

Em trabalho longo, atualize um checkpoint no plano após cada fase concluída ou
interrupção: último passo, revisão/evidências, bloqueio e próxima ação. Registre
também PR/ticket e seus estados reais quando existirem. Retomada não concede
autorização adicional para commit, publicação, merge ou fechamento.
