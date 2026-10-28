# Extração do JourneyCore

Origem: LucasArcega/journey-core, branch develop,
commit 8084d288b0432dff01747a5832c71c20cd07cddd.
A extração usa a versão centralizada em .agents/skills/ após o pull.
As cópias pessoais em .codex/skills não são a fonte deste kit.

## Skills

| Origem | Destino compartilhado |
| --- | --- |
| write-kanban-tickets | write-ticket |
| enrich-plans | enrich-plan |
| implement-feature-ticket | implement-ticket |
| codex-review-json | review-changes |
| pr-to-clickup | create-pr + integrações |
| merge-and-close-ticket | merge-and-close |
| fast-merge | fast-merge |
| implement-feature-ticket-worktree | implement-in-worktree |
| test-record | record-test |

Preservados: critérios verificáveis, esclarecimento de escopo antes de escrever
critérios dependentes, separação de planos, auditoria plano/código, revisão
estruturada, validação por superfície, confirmação de resultados e handoff.
Removedores de portabilidade: caminhos pessoais, perfis fixos de modelo, nomes
de MCP, versões fixas de runtime, ports e dados de uma aplicação específica.

## Regras e AGENTS.md

| Material de origem | Tratamento |
| --- | --- |
| AGENTS.md: produto, entidades e pipeline | Contexto do consumidor; não integra o núcleo |
| scope-guardian.mdc e plans-no-optional.mdc | .agents/rules/WORKFLOW.md |
| codex-subagent-delegation.mdc | .agents/rules/DELEGATION.md + papéis |
| tickets-plans-branches.mdc | Perfil, templates e integrações |
| issues-tickets-ptbr.mdc | project.language, com pt-BR como padrão |
| clean-architecture-dependencies.mdc | Contexto dotnet-angular |
| controllers-services-patterns.mdc | Contexto dotnet-angular |
| domain-entities-organization.mdc e domain-validation.mdc | Contexto dotnet-angular, respeitando a arquitetura existente |
| repository-bulk-operations.mdc | Contexto dotnet-angular; dono do commit definido pelo projeto |
| angular-frontend-patterns.mdc e i18n-angular.mdc | Contexto dotnet-angular, incluindo overlays abertos e idiomas oferecidos |
| naming-conventions.mdc e clean-code.mdc | Padrões existentes; sem limites universais de linhas e refatorações automáticas |
| codex-cli-path.mdc | Resolução por capacidade do ambiente; sem caminho pessoal obrigatório |

As regras de origem divergiam sobre persistência em repositórios e perfis de
delegação. O kit preserva o dono explícito da unidade de trabalho e um único
contrato de delegação; cada projeto mantém sua arquitetura concreta.

## Scripts, configuração e worktrees

Foram considerados os fluxos de create-worktree, setup-worktree, worktree-run,
worktrees.json, templates locais e launchers de trilhas.
A skill genérica usa capacidades nativas/Git e exige definição explícita de
isolamento de serviços quando necessário. Não copiamos pools, portas, nomes de
banco, infraestrutura Azure ou automação de ondas do JourneyCore.

CLICKUP_USAGE_RULE e MCP_SETUP viraram contratos de integração por capacidades.
MCPs pessoais, credenciais, arquivos de ambiente e configurações de permissões
não são redistribuídos. Arquivos ADO legados não viram dependências do kit.

O exemplo em examples/journey-core/project.json guarda remote, base, comandos
e IDs de lista/workspace específicos. É um exemplo para revisar, não uma operação
de migração no JourneyCore. A adoção no projeto de origem é uma etapa separada.
