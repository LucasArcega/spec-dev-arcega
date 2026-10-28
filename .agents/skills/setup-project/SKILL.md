---
name: setup-project
description: "Investiga e configura o kit em um projeto, com perguntas guiadas e retomada do setup."
---

# Configurar o projeto

Use para iniciar, continuar ou revisar o setup do kit no projeto consumidor. O
agente conduz a conversa e usa as capacidades de leitura e edição disponíveis;
terminal, Python, doctor e clientes específicos não são pré-requisitos.

## Investigar e conversar

1. Leia as instruções locais, `.specdev/project.json`, os documentos já
   selecionados em `context` e, se existir, `.specdev/setup-state.json`. Se o kit
   ou perfil estiver ausente, informe a etapa de instalação ou o bloqueio; não
   fabrique uma configuração parcial. Identifique também a documentação e os
   arquivos relevantes ao projeto sem ler credenciais nem executar comandos.
2. Separe fatos verificados com fonte, decisões confirmadas pelo usuário e
   hipóteses. Valores padrão de perfil e exemplos são hipóteses, não confirmações.
   Compare estado, arquivos e pedido atual; retome sem repetir respostas ainda
   válidas. Para setup completo, avalie cada ID de [references/questions.md](references/questions.md);
   para pedido delimitado, avalie os IDs pertinentes e declare os não avaliados.
   Registre as lacunas e os campos aplicáveis, sem impor uma entrevista fixa.
3. Apresente o que descobriu e pergunte uma decisão material por vez, com uma
   sugestão quando houver evidência. Incorpore informação já dada; nunca invente
   confirmação, repositório, IDs, comandos, capacidade, ambiente ou resultados.
   Se o usuário não souber ou interromper, registre a pendência e a próxima
   pergunta; não transforme ausência de resposta em confirmação.

## Registrar e retomar

Registre progressivamente os fatos e decisões confirmados em `.specdev/project.json`
e no contexto local. O caminho sugerido é `docs/PROJECT_CONTEXT.md`; use outro
caminho relativo ao projeto quando for o adotado ou acordado. Para um documento
novo, adapte [assets/project-context.md](assets/project-context.md) apenas às
seções aplicáveis. Se já existir, leia e preserve o conteúdo: integre somente
trechos pertinentes ou combine outro caminho, sem presumir propriedade do arquivo.
Acrescente o documento selecionado a `context` uma única vez, depois de existir.
Preserve outros campos, contextos, comentários e instruções locais; não edite
arquivos gerados nem substitua o perfil inteiro. Não registre tokens, senhas,
conteúdo de credenciais ou dados sensíveis no contexto, perfil ou estado.

Mantenha `.specdev/setup-state.json` como arquivo do consumidor, nunca gerenciado
pelo manifest. Crie-o apenas se ausente; atualize campos conhecidos preservando
extensões. O contrato v1 é:

```json
{
  "schema_version": 1,
  "status": "in_progress",
  "context_path": "docs/PROJECT_CONTEXT.md",
  "scope": ["product.purpose"],
  "decisions": {
    "product.purpose": {"status": "pending", "source": "a esclarecer"}
  },
  "pending": ["product.purpose"],
  "next_question": "Qual problema o projeto resolve?",
  "verification": {
    "configuration": "pendente",
    "availability": "não verificada",
    "execution": "nenhum comando executado"
  }
}
```

`status` geral é `in_progress`, `blocked` ou `complete`. Cada decisão usa um ID
estável da referência e status `confirmed`, `inferred`, `pending` ou
`not_applicable`, com fonte resumida sem segredos. `confirmed` exige confirmação
do usuário ou fato diretamente verificado; indique a origem em `source`.
`scope` é a lista dos IDs estáveis abrangidos pelo pedido. Em setup completo,
registre todos os IDs do mapa; em setup parcial, apenas os escolhidos. IDs ainda
não avaliados ficam `pending`, não desaparecem da lista. Na retomada, use esse
escopo persistido; amplie-o somente se o pedido atual incluir novas decisões.
Quando um ID agrupar vários campos, confirme cada campo aplicável por resposta
do usuário ou fato verificado, ou registre sua não aplicabilidade com evidência.
Uma única fonte para um campo não confirma os demais. Marque o ID `confirmed`
somente quando todos os campos tiverem sido resolvidos dessa forma; use
`not_applicable` para o ID somente quando todo o grupo não se aplicar.
Enquanto restar campo pendente ou em hipótese, mantenha o ID `pending` ou
`inferred` e em `pending`; pergunte uma decisão por vez. Aplique os campos já
confirmados aos destinos apropriados e registre em `source` as origens e pendências
por campo, sem valores sensíveis; veja os exemplos em `references/questions.md`.
`inferred` não autoriza gravar a hipótese como fato. Registre valores confirmados
nos arquivos próprios, não replique respostas sensíveis no estado. `pending`
contém IDs aplicáveis ainda `pending` ou `inferred`; `next_question` é a próxima
pergunta em texto ou `null` quando não houver. Atualize o checkpoint após cada
resposta e antes de aguardar. Em `verification`, registre resultado ou limitação
de estrutura, disponibilidade e execução, sem dados sensíveis. Os três campos
são textos livres, não uma enumeração de resultados. Se não puder gravar, informe
a limitação e continue somente no escopo possível.

Antes de cada alteração, releia o alvo; se mudou desde a leitura, reconcilie sem
apagar alterações alheias. Se o estado estiver inválido, usar versão desconhecida,
apontar para caminho inseguro ou divergir dos arquivos, preserve-o, relate o
problema e resolva a divergência antes da edição afetada. Não reinicie por reset.
Na retomada, valide novamente as fontes e os campos registrados; a existência de
um checkpoint não comprova que os arquivos continuem iguais.
Para cada ID composto do escopo, inclusive os já marcados `confirmed` ou
`not_applicable`, confira cada campo aplicável nas fontes e destinos reais antes
de manter seu status e antes de concluir. Uma `source` genérica citando apenas
documentos não prova que todos os campos foram resolvidos: registre nela a
origem ou pendência de cada campo, sem dados sensíveis. Se algum campo ainda não
estiver comprovado ou explicitamente não aplicável, reclassifique o ID como
`pending` ou `inferred`, inclua-o em `pending` e ajuste `next_question` e o
status geral para `in_progress` ou `blocked`. Preserve dados existentes e não
repita perguntas sobre campos cuja evidência continua válida.
O caminho do contexto deve permanecer relativo à raiz autorizada, sem `..`, e
não pode atravessar link/junction que redirecione a leitura ou edição para fora.

## Conferir e entregar

Confira o perfil contra o contrato resumido em [references/questions.md](references/questions.md), a
existência dos contextos selecionados, IDs únicos, caminhos e argumentos de cada
validação. Se houver documentação local de configuração, consulte-a também.
Registre no checkpoint o que está **configurado**, o que teve disponibilidade
efetivamente verificada e o que foi **executado**, com resultado ou limitação.
Escolha verificações adequadas às capacidades disponíveis. O doctor pode ajudar
quando disponível; sua ausência não bloqueia o setup. Não execute comandos
declarativos apenas porque estão no perfil nem suponha que serviços estão ativos.

Marque `complete` somente quando todos os IDs do escopo tiverem sido avaliados,
as decisões aplicáveis estiverem confirmadas ou explicitamente `not_applicable`,
sem IDs pendentes, e a estrutura estiver coerente e tiver sido conferida.
Registre resultado ou limitação para cada tipo de verificação. Uma hipótese não confirmada,
conflito ou decisão indispensável ausente mantém o setup pendente/bloqueado.
Se não houver capacidade para conferir a estrutura do perfil e os caminhos,
registre a limitação e mantenha `in_progress` ou `blocked`. Disponibilidade de
serviços e execução de testes não são pré-requisitos de conclusão do setup.
Conclusão do setup de configuração não afirma que testes passaram ou que serviços
estão disponíveis. Entregue arquivos alterados, decisões, verificações realizadas,
limitações e próxima ação. Operações externas dependem do pedido correspondente.
