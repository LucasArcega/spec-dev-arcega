# Setup guiado e independente de cliente

**Identificador local:** setup-project  
**Estado:** Concluído localmente  
**Dependências:** kit instalado no projeto consumidor; capacidades de leitura,
edição e diálogo do agente. Terminal e ferramentas externas são opcionais.

## Por quê e escopo

Permitir que um agente investigue um projeto, pergunte pelas decisões relevantes
que faltam e registre progressivamente as particularidades no consumidor. A
mesma definição canônica deve funcionar nos clientes suportados e poder ser lida
por outros agentes; o instalador mantém seus formatos e dados existentes.

| Critério | Implementação e validação | Evidência e estado |
| --- | --- | --- |
| AC-01 — Setup descobre contexto e pergunta uma decisão por vez, distinguindo fatos, hipóteses e respostas | Skill e roteiro de perguntas | Passou: entrevista isolada e revisão, incluindo IDs com vários campos |
| AC-02 — Configuração, contexto e checkpoint pertencem ao consumidor, preservam dados e permitem retomada | Skill, template e cenário isolado | Passou: retomadas preservaram respostas e contexto; confirmação parcial reaberta |
| AC-03 — Fluxo independente de editor, CLI e doctor; comandos declarativos não executam automaticamente | Skill e cenário isolado | Passou: cenário dispensou doctor, Python e comandos do projeto; contrato revisado |
| AC-04 — Instalador distribui skill e recursos sem criar estado/contexto do consumidor | Testes em diretórios temporários | Passou: teste de distribuição para os três adaptadores e ausência dos arquivos locais |
| AC-05 — Atualizações preservam checkpoint, contexto local e perfil existente | Testes em diretórios temporários | Passou: teste de atualização de skill e cópia Claude sem alterar dados locais |
| AC-06 — Catálogo, documentação e adaptadores indicam a nova capacidade | Geração, validate e check | Passou: 10 skills, check íntegro e dry-run sem alterações |

## Validação

- Teste de uso independente em consumidor temporário, sem serviços externos.
- `python -m unittest discover -s tests -v`.
- `python scripts/specdev.py validate` e `python scripts/specdev.py check --target .`.
- Revisão do conjunto efetivo de arquivos e estado gerado.

Resultado em 27/10/2026: 51 testes passaram em Python 3.14.0 (38,148 s).
validate retornou dez skills; check sem issues/warnings; install --dry-run sem
alterações; validador de skill passou. A avaliação independente incluiu duas
retomadas em projeto temporário e verificou preservação de dados. A revisão
identificou e acompanhou a correção de um P2 em decisões compostas; a nova
revisão e o teste de retomada não apresentaram achados abertos.

## Checkpoint

**Último passo:** implementação, distribuição, revisão e validação concluídas.  
**Revisão/evidências:** [review.json](review.json); snapshot identificado por
hash, pois o repositório não tem commits.  
**Bloqueio:** nenhum conhecido.  
**Próxima ação:** handoff local; publicar ou commitar depende de pedido próprio.

## Limitações

O teste de entrevista foi feito com agentes na sessão Codex, usando um projeto
fictício e respostas simuladas; não substitui smoke de uso em Cursor e Claude.
Os testes automatizados rodaram em Python 3.14; Python 3.11 não foi exercitado.

## Fora do escopo

Execução automática do setup no projeto deste kit, novas integrações externas,
publicação, commit, merge ou alteração de credenciais.
