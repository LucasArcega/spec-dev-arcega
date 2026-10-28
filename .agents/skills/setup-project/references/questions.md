# Decisões para setup

Use este mapa para localizar lacunas, não como questionário obrigatório. Prefira
fontes existentes e respostas já fornecidas. IDs permanecem estáveis na retomada;
para projetos com múltiplos componentes, use um sufixo estável escolhido a partir
do componente real, por exemplo `validation.commands.api`.

| ID | Quando verificar/perguntar | Destino confirmado |
| --- | --- | --- |
| `product.identity` | Nome do projeto está ausente ou é apenas valor padrão sem confirmação | Perfil: `project.name` |
| `product.purpose` | Objetivo, público e termos de domínio não estão claros | Contexto local: produto |
| `product.language` | Idioma de tickets e planos não está decidido | Perfil: `project.language` |
| `architecture.structure` | Componentes, responsabilidades ou fronteiras não estão claros | Contexto local: arquitetura |
| `architecture.context` | Existem convenções de stack/projeto que os agentes precisam ler | Perfil: `context`; documento local |
| `environment.setup` | Preparação, dependências ou serviços necessários não estão documentados | Contexto local: ambiente |
| `validation.commands` | Comandos, escopo, diretórios ou pré-requisitos de validação não estão definidos | Perfil: `validation`; contexto se necessário |
| `delivery.git` | Remote, base, padrão de branch ou repositório não estão definidos para o projeto | Perfil: `git` |
| `delivery.plans` | Caminhos de planos/estado não correspondem a uma convenção confirmada | Perfil: `paths` |
| `delivery.tracking` | Provedor, identificação ou status aplicáveis estão indefinidos | Perfil: `tracking` |
| `delivery.pr` | Preferência de PR importa para a equipe e não foi decidida | Perfil: `delivery.create_pr` |
| `agents.models` | Há necessidade explícita de escolhas por ferramenta/papel | Perfil: `models` |
| `agents.conventions` | Há instruções específicas e confirmadas para agentes | Contexto local ou instruções locais existentes |

Para cada decisão aplicável, identifique fonte e resultado esperado; se o projeto
não precisar dela, registre `not_applicable` após evidência ou resposta explícita.
Não peça IDs de rastreador, status ou configurações de integração quando não
houver provedor; uma preferência padrão como `none` ainda requer confirmação se
não houver evidência de que representa a decisão do projeto. Não solicite modelos
quando herança atender à equipe. O escopo do pedido pode limitar a entrevista;
indique o que não foi avaliado em vez de preencher lacunas com suposições.

## Decisões com vários campos

O status de cada ID resume todos os seus campos aplicáveis. Para cada campo,
guarde a origem resumida em `source`: resposta do usuário ou fonte diretamente
verificada. Um campo opcional só é não aplicável quando isso tiver evidência ou
for explicitamente informado; `null` ou ausência isolada não comprova isso.
Registre os campos confirmados nos destinos próprios e preserve-os durante a
retomada. Liste em `source` também os campos ainda pendentes, sem expor valores
sensíveis. Se qualquer campo estiver em hipótese ou pendente, mantenha o ID como
`inferred` ou `pending`, incluído na lista `pending`, e pergunte uma decisão por
vez. Marque o ID `confirmed` quando todos os campos aplicáveis estiverem
confirmados e os demais forem comprovadamente não aplicáveis; só use
`not_applicable` para o ID inteiro quando nenhum dos seus campos se aplicar.

Na retomada, reavalie cada campo de IDs compostos mesmo quando o estado anterior
os marque como `confirmed`. Por exemplo, `source: "README e contexto"` não
comprova, por si só, que objetivo, público e termos foram resolvidos. Releia as
fontes reais e registre a origem de cada campo comprovado em `source`; sinalize
os demais como pendentes ou hipóteses. Se faltar evidência para algum campo,
reclassifique `product.purpose` como `pending` ou `inferred`, inclua o ID em
`pending` e atualize a próxima pergunta e o status geral. Preserve as respostas
e arquivos existentes, e pergunte apenas pelo campo ainda não resolvido.

Por exemplo, em `delivery.git` avalie `remote`, `base_branch`, `branch_pattern` e
`repository` separadamente. Se apenas a base foi verificada, a origem e o padrão
continuam pendentes. O repositório pode ser não aplicável quando confirmado que o
projeto não usa GitHub; não o infira a partir de `repository: null`. Registre a
base no perfil, mantenha `delivery.git` pendente e peça uma das decisões restantes.
Uma fonte possível é `base_branch: arquivo local verificado; remote e
branch_pattern: pendentes; repository: não aplicável, confirmado pelo usuário`.

Em `product.purpose`, avalie objetivo, público e termos do domínio separadamente.
Se o objetivo foi verificado, mas o público ainda é desconhecido, registre o
objetivo no contexto e mantenha o ID pendente. Os termos só são não aplicáveis se
isso foi confirmado ou verificado; não conclua que não existem por ausência de
documentação. `source` pode registrar `objetivo: documentação verificada;
público: pendente; termos: não aplicáveis, confirmado pelo usuário`. Pergunte
então sobre o público, sem repetir o objetivo já confirmado.

Para validações, descubra o comportamento pretendido e registre cada comando
somente quando confirmado: `id`, `cwd` relativo à raiz, `argv` em lista,
`surfaces`, `requires` e `required`. Preserve comandos existentes e seus IDs;
antes de alterar ou substituir um comando que conflita com a descoberta, esclareça
a divergência. A mera presença de um arquivo de projeto não comprova que um
comando funciona. Não execute os comandos só para coletar essa configuração.

## Contrato do perfil

O kit instalado fornece `.specdev/project.json` com `schema_version: 1` e as
seções `project`, `git`, `paths`, `context`, `validation`, `tracking`, `delivery`
e `models`. Preserve chaves desconhecidas e valores existentes. `project` requer
nome e idioma; `git` contém remote, base e padrão de branch com placeholders
`{ticket}` e `{slug}` quando usados. Caminhos de `paths`, `context` e cwd das
validações são relativos à raiz do projeto, sem `..`; selecione apenas arquivos
de contexto existentes. `tracking.provider` aceita `none`, `github` ou `clickup`;
IDs, quando aplicáveis, são strings, e `statuses` mapeia pending, in_progress e
done a nomes reais. `delivery.create_pr` é boolean e não autoriza publicação.
`models` agrupa opções por cliente/papel; preserve herança enquanto não houver
necessidade confirmada de override. Não invente opções ou capacidades do cliente.

Para cada comando, `argv` contém argumentos separados e não vazios; `surfaces` é
lista não vazia, `requires` é lista de pré-requisitos e `required` é boolean.
Um array vazio de validation indica cobertura ainda não configurada. Compare as
informações com os arquivos reais e o pedido, sem assumir que a validade
estrutural prova que ferramentas, dependências ou serviços estão disponíveis.

Exemplo de pergunta contextual: “Encontrei uma suíte de integração separada da
unitária. A documentação menciona banco. A equipe usa um banco isolado ao rodá-la?”
Se a fonte ou o pré-requisito ainda não for conhecido, apresente-o como hipótese.
Adapte perguntas ao idioma do perfil e às informações já disponíveis.
