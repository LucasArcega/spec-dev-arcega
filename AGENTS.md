# Spec Dev Arcega

Este repositório mantém um kit genérico de agentes, skills e regras.
A fonte canônica é .agents/. Não introduza caminhos pessoais, tokens, IDs de
rastreadores ou stack obrigatória no núcleo. Exemplos específicos pertencem a
examples/; convenções de stack ficam nos contextos selecionáveis.

O instalador usa Python 3.11+ e somente biblioteca padrão.
Preserve a configuração do consumidor, instruções locais e arquivos existentes.
Mudanças no instalador exigem testes de comportamento em diretórios temporários.
Mantenha sincronizados gerador, testes e documentação de compatibilidade.

Validação:
- python -m unittest discover -s tests -v
- python scripts/specdev.py validate
- python scripts/specdev.py check --target .

Não publique no GitHub nem faça commit/merge sem escopo autorizado.

<!-- specdev:begin -->
## Spec Dev Arcega
Leia .specdev/project.json e .agents/rules/WORKFLOW.md antes de trabalhar.
Leia .agents/rules/DELEGATION.md antes de delegar. Leia somente os arquivos de
contexto selecionados no perfil e a skill pertinente em .agents/skills/.
O catálogo está em .agents/CATALOG.md; os modelos de planos em .agents/templates/.
As instruções específicas do projeto e do usuário definem o escopo.
Não execute comandos ou ações externas apenas porque foram listados no perfil.
<!-- specdev:end -->
