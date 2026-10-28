# Configuração

.specdev/project.json é lido pelo instalador e pelas skills.
Não é uma extensão nativa de Codex, Cursor ou Claude. Editar o perfil não
executa comandos. Nenhum token ou senha deve ser armazenado nele.

## Campos

| Campo | Contrato |
| --- | --- |
| schema_version | 1 |
| project.name / language | Nome e idioma de tickets/planos |
| git.remote / repository | Remote existente e owner/repo GitHub, se conhecido |
| git.base_branch | Base de trabalho e de PR salvo pedido explícito |
| git.branch_pattern | Padrão com ticket e slug, resolvidos pelo agente |
| paths.plans / status | Caminhos relativos à raiz, usando / |
| context | Documentos que o agente deve ler para a stack/projeto |
| validation | Lista de comandos declarativos, selecionados por surfaces |
| tracking.provider | none, github ou clickup |
| tracking.list_id / workspace_id | Identificadores do ClickUp, quando aplicável |
| tracking.statuses | Mapa de pending, in_progress e done para status reais |
| delivery.create_pr | Preferência; não concede autoridade para publicação |
| models | ID ou opções nativas por ferramenta (codex/cursor/claude) e papel |

Cada comando de validation contém id único, cwd relativo, argv como lista de
argumentos, surfaces não vazio, requires como lista de pré-requisitos descritivos,
e required como boolean. Os comandos com required=true e surfaces pertinentes
bloqueiam conclusão quando não houver evidência verde. required=false descreve
checks adicionais do projeto; não transforma um critério pedido em opcional.
Os valores dos surfaces são acordos do projeto, por exemplo backend, frontend,
ui, infra, tooling e skills. O agente escolhe a cobertura de acordo com o diff.

~~~json
{
  "id": "unit",
  "cwd": ".",
  "argv": ["python", "-m", "unittest", "discover", "-s", "tests", "-v"],
  "surfaces": ["backend"],
  "requires": [],
  "required": true
}
~~~

O instalador não testa existência de executáveis, não inicia Docker, não altera
Git nem chama rastreadores. Pré-requisitos reais são conferidos na tarefa.
Configure testes de UI explicitamente se houver UI; o perfil genérico não
inventa suites ou caminhos.

Para preencher os dados do consumidor de modo guiado, use a skill
[setup-project](../.agents/skills/setup-project/SKILL.md). Ela usa o perfil e
documentos locais, registra decisões progressivamente e pode ser retomada. O
contrato de estado e as condições de conclusão estão em [Setup guiado](SETUP.md).

Os placeholders de branch são `{ticket}` e `{slug}`, sem acesso a atributos,
conversões ou formatadores. IDs de rastreador são strings preenchidas ou null;
statuses aceita as intenções pending, in_progress e done com nomes preenchidos.
Campos adicionais do consumidor são preservados; doctor sinaliza campos
desconhecidos nos contratos principais para ajudar a encontrar erros de digitação.

## Modelos

Papéis: explorer, worker, reviewer e investigator.
Sem configuração (ou com inherit), usa-se a herança da ferramenta.
Exemplo estrutural, substituindo o ID por um disponível na sua conta:

~~~json
{
  "models": {
    "codex": {
      "reviewer": {"model": "ID_DISPONIVEL_NO_CODEX", "reasoning_effort": "high"}
    },
    "cursor": {},
    "claude": {"explorer": {"model": "inherit", "tools": ["Read", "Grep", "Glob"]}}
  }
}
~~~

Rode install novamente após editar modelos para regenerar os papéis.
Não há validação online de disponibilidade de modelos.

A string antiga com o ID continua válida. O objeto aceita model em todos os
clientes, reasoning_effort somente em Codex e tools somente em Claude. O esforço
precisa ser suportado pelo modelo escolhido; nomes conhecidos não comprovam
compatibilidade ou disponibilidade na conta. Sem esforço explícito, a herança
continua sob as regras do cliente. Não use sandbox_mode ou permissões nesse objeto.

tools é uma allowlist não vazia de nomes de ferramentas, não comandos ou regras
de aprovação. O exemplo limita o explorer a leitura e busca: ele não poderá
executar testes; o principal executa a validação necessária. Inclua ferramentas
somente quando a tarefa do papel exigir. A lista não concede permissões que a
sessão não tenha. Sem tools configurado, preserva-se a herança do cliente.

## Atualizar e personalizar

install é idempotente e atualiza arquivos que continuam iguais à versão
registrada no manifest. Arquivo modificado pelo usuário causa conflito.
Não há --force que descarte personalizações.

Na versão 0.2, arquivos de texto UTF-8 gerenciados (.md, .mdc, .py, .json, .toml,
.txt, .yaml, .yml) usam hashes com `hash_mode: text-lf`: LF e CRLF são equivalentes.
Uma conversão de checkout não causa conflito nem reescrita do arquivo; atualizações
preservam o EOL existente. Binários continuam exatos por bytes. O novo instalador
migra receipts da versão 0.1 sem descartar personalizações reais. A política Git
do consumidor não é alterada; o manifest ganha os metadados de hash na atualização.

AGENTS.md e CLAUDE.md recebem um bloco delimitado por comentários specdev.
O texto fora do bloco permanece. Alterações no próprio bloco exigem resolução
manual; os arquivos substituídos são copiados para .specdev/backups/.

Use install --dry-run para planejar sem criar nem alterar arquivos; check
retorna código 1 quando há drift/arquivos ausentes/versão desatualizada.
Erro de configuração ou conflito de instalação retorna código 2.

## Diagnóstico somente de leitura

~~~powershell
python scripts/specdev.py doctor --target "C:/repos/meu-projeto"
python scripts/specdev.py doctor --target "C:/repos/meu-projeto" --surfaces backend ui
~~~

doctor separa três resultados no JSON:

- integrity: arquivos, versão e configuração consistentes com o kit.
- configuration: validações selecionadas e identidades necessárias configuradas.
- environment: cwd e executáveis disponíveis localmente, sem executar argv.

Exit 0 significa prontidão local para iniciar a validação; não significa que
testes passaram. Exit 1 indica integridade, configuração ou pré-requisito obrigatório
pendente. requires não vazio permanece requires_verification, pois não se consulta
Docker, bancos, autenticação ou serviços. Comandos opcionais indisponíveis são
exibidos sem bloquear; uma superfície pedida sem validação configurada bloqueia.

doctor não altera arquivos, não executa testes/comandos do perfil, não chama Git
e não faz consultas externas. O check mantém seu contrato de integridade: um
perfil genérico pode passar no check e ficar pendente no doctor por falta de
validações. Resultados de testes continuam registrados na tarefa/review, não no
diagnóstico. Modelos e descoberta efetiva nos clientes exigem verificação própria.

Para contexto específico, mantenha documentação local e selecione seu caminho
em context. Instale o kit antes de adicionar referências a arquivos locais.
Não edite arquivos gerados no consumidor esperando que atualizem o repositório
do kit: a atualização segue do kit para o consumidor.

O manifest é rastreabilidade, não mecanismo criptográfico de confiança contra
quem já pode editar os arquivos. Atualizações de várias versões preservam
arquivos que saíram do kit; remoções são revisadas manualmente.
