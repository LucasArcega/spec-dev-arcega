# Confiabilidade do kit e evolução dos contratos

**Identificador local:** kit-reliability
**Status:** Concluído localmente
**Branch:** main existente, sem commits; nenhuma publicação autorizada.
**Dependências:** nenhuma dependência externa nova.

## Escopo aceito

Corrigir os achados P2/P3 da auditoria e evoluir os itens 4 a 8 da resposta:
review rastreável, agentes, retomada de entregas, diagnóstico de configuração
e vínculo entre critérios e evidências. Preservar consumidores existentes,
fonte canônica, Python 3.11+ e biblioteca padrão.

## Critérios e evidência

| ID | Comportamento obrigatório | Implementação/teste | Evidência e revisão |
| --- | --- | --- | --- |
| AC1 | EOL equivalente não bloqueia instalação; edição real continua protegida | scripts/specdev.py; testes CRLF, legado e binário | Passou; suíte completa e review sem achados abertos |
| AC2 | Schema e validador de review concordam, com legado preservado | schema/validador; tests/test_review_contract.py | Passou; casos válidos/inválidos e regras interpretadas do schema |
| AC3 | Novos reviews registram escopo, checks e bloqueios | Review v2 e flag --require-evidence | Passou; testes de CLI, evidência, blockers e compatibilidade |
| AC4 | Agentes têm retorno/interrupção definidos e opções nativas suportadas | DELEGATION, roles, gerador e testes de opções | Passou; contratos revisados, TOML/frontmatter e isolamento por cliente testados |
| AC5 | Entrega retoma merge concluído e associa evidência ao conteúdo validado | Skills de implementação, merge e fast-merge | Passou na revisão de contratos; sem executar mutações externas |
| AC6 | Diagnóstico separa integridade, configuração e disponibilidade sem executar comandos | doctor e testes com snapshots/marker | Passou; PATH relativo ao cwd, marker não executado e arquivos preservados |
| AC7 | Planos ligam critérios a implementação/teste e evidência | Template PLAN, enrich-plan e WORKFLOW | Passou na revisão de contratos e no registro deste plano |

## Validação

- `python -m unittest discover -s tests -v`
- `python scripts/specdev.py validate`
- `python scripts/specdev.py check --target .`
- `python scripts/specdev.py doctor --target .`
- Review estruturado v2 contra snapshot anterior, pois o Git está sem commits.

Resultado em 27/10/2026: 49 testes passaram em Python 3.14.0 (44,999 s).
validate retornou nove skills; check sem issues/warnings; doctor com os três
grupos prontos e executed=false; install --dry-run retornou changed=[].
Adaptadores regenerados com backup pelo instalador. Revisão consolidada em
[review.json](review.json), validada com --require-evidence.

O TEMP/TMP padrão do sandbox apresentou acesso negado na auditoria; usar pasta
temporária gravável quando necessário. Isso não altera o resultado esperado
da suíte. Descoberta nos aplicativos não comprova todos os fluxos externos.

## Checkpoint

- Último passo confirmado: implementação, adaptação, revisão e validações concluídas.
- Conteúdo validado: snapshot SHA-256 em review.json; Git sem commits. Os hashes
  das duas revisões independentes foram reconferidos após a suíte completa.
- Bloqueios: nenhum conhecido.
- Próxima ação: handoff local; publicação, commit e merge não autorizados.

## Limites da validação

Python 3.11 e clientes Cursor/Claude não foram exercitados nesta mudança. Modelos
reais e allowlists foram verificados como configuração/formatos gerados, sem
consulta de disponibilidade na conta. Merge/fechamento foram revisados como
contratos; nenhuma operação real de GitHub ou rastreador foi executada.

## Fora do escopo

Corpus de avaliações comportamentais do item 3, novos provedores, novos papéis,
publicação, commit, merge e alterações no JourneyCore.
