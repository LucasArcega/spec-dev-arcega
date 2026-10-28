---
name: write-ticket
description: "Cria ou revisa tickets com motivação e critérios verificáveis no rastreador configurado ou em documentação local."
---

# Escrever ticket

Leia .specdev/project.json e .agents/rules/WORKFLOW.md.
Identifique o problema, o público, o resultado e o rastreador autorizado.
Consulte contexto disponível antes de pedir informação.

Antes de redigir, esclareça decisões importantes ainda abertas, uma por vez,
com uma sugestão. Não peça novamente o que o pedido ou o projeto já decidiu.
Não invente prioridade, dependência, estimativa ou identificador.

Use o idioma do perfil e escreva:

- Título curto com o padrão do projeto.
- Por quê: problema e valor em uma ou duas frases.
- User story quando o resultado afeta usuários finais.
- Critérios de aceite obrigatórios, observáveis e pass/fail.
- Contexto técnico curto com contratos/caminhos reais quando necessário.
- Fora do escopo para exclusões relevantes.

Se o pedido é apenas redigir, entregue o texto. Para criar/editar no rastreador,
leia a integração pertinente e execute somente a operação autorizada.
Com tracking.provider = none, use o arquivo local definido na tarefa.
Confirme a criação/edição relendo o resultado e entregue arquivo ou URL.
