# Compatibilidade

Há uma fonte compartilhada em .agents/, mas cada cliente possui descoberta e
formatos próprios. O instalador gera as entradas nativas selecionadas.
Compatibilidade com todas as ferramentas existentes não é presumida.

| Cliente | Entrada | Skills | Agentes |
| --- | --- | --- | --- |
| Codex | AGENTS.md | .agents/skills/ | .codex/agents/specdev-*.toml |
| Cursor | AGENTS.md e .cursor/rules/specdev.mdc | .agents/skills/ | .cursor/agents/specdev-*.md |
| Claude Code | CLAUDE.md importa AGENTS.md | .claude/skills/ gerado | .claude/agents/specdev-*.md |
| Outro cliente | Leia AGENTS.md e o catálogo explicitamente | Conforme suporte ao padrão | Requer adaptador nativo |

As cópias de skills para Claude são geradas a partir de .agents/; a origem
permanece única. Cursor também pode descobrir diretórios de compatibilidade.
Evite skills pessoais ou manuais de mesmo nome; confira a origem exibida pelo
cliente quando houver mais de uma definição. O kit não remove skills globais.

Papéis de leitura usam readonly no Cursor. Em Codex e Claude, a proibição de
edição está no prompt; não representa um sandbox separado.
Claude pode receber uma allowlist tools por papel, configurada explicitamente
no perfil. Isso reduz a superfície de ferramentas, sem criar sandbox separado
ou conceder aprovação. Codex pode receber model_reasoning_effort junto ao modelo;
o kit não traduz essa opção para Cursor ou Claude.
O kit não altera permissões, configurações globais, autenticação ou MCPs.
Modelos são herdados quando não configurados. Os clientes podem impor sua
própria precedência e restrições de conta.

## Fontes oficiais consultadas em 27/10/2026

- [Codex: skills e localização](https://learn.chatgpt.com/docs/build-skills)
- [Codex: instruções AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex: papéis personalizados](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Cursor: skills](https://cursor.com/docs/skills)
- [Cursor: subagents](https://cursor.com/docs/subagents)
- [Claude Code: skills](https://code.claude.com/docs/en/skills)
- [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code: memória e imports](https://code.claude.com/docs/en/memory)

A verificação automatizada cobre os formatos e efeitos em disco.
Smoke nos clientes reais precisa confirmar skills e papéis listados na sessão;
ele não foi executado como parte do bootstrap deste repositório.

O setup guiado é uma skill compartilhada em `.agents/skills/setup-project/`;
Claude recebe uma cópia gerada com suas referências e template. Ele depende das
capacidades de leitura, edição e diálogo do agente, sem exigir CLI ou doctor.
Outro cliente pode ler a skill e os recursos explicitamente pelo catálogo.
Suporte de descoberta automática e aplicação efetiva depende do cliente e da sessão.

Na auditoria local, explorer e reviewer foram usados no Codex. Isso não comprova
todos os papéis, opções de modelos, fluxos ou os clientes Cursor/Claude.
O comando doctor verifica somente configuração e disponibilidade local; não
substitui esse smoke. A suíte atual foi executada em Python 3.14; compatibilidade
com o mínimo 3.11 também depende de execução nessa versão, não só leitura de código.

Versão 0.2 preserva os perfis com IDs de modelo como strings e os reviews legados.
Novos reviews usam v2 com --require-evidence. Hashes de textos toleram LF/CRLF,
inclusive na migração de instalações 0.1. Veja [configuração](CONFIGURATION.md),
[review](REVIEW.md) e [retomada](WORKFLOWS.md).
