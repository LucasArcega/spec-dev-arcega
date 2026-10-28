<div align="center">

# Spec Dev Arcega

**Skills, agentes e fluxos de trabalho para desenvolver com contexto.**

Um kit orientado a especificações, adaptável ao seu projeto e à sua equipe.

`Python 3.11+` · `Biblioteca padrão` · `Codex` · `Cursor` · `Claude Code`

[Instalação](#instalação) · [Setup guiado](#5-configure-seu-projeto) · [Skills](#conheça-as-skills) · [Atualização](#atualize-o-kit) · [Ajuda](#solução-de-problemas)

</div>

---

O Spec Dev Arcega reúne instruções reutilizáveis para ajudar agentes a entender
o projeto, preparar planos, implementar, revisar e entregar mudanças. O kit nasceu
a partir de práticas do JourneyCore e mantém suas convenções específicas em um
[exemplo separado](../examples/journey-core/project.json).

Você pode usá-lo em projetos de diferentes linguagens e arquiteturas. As
particularidades do seu projeto ficam na configuração e nos documentos dele.

## Antes de começar

Você vai precisar de:

1. **Uma cópia deste repositório**, contendo `scripts/specdev.py` e a pasta `.agents/`.
2. **Python 3.11 ou superior** na máquina que executará o instalador. Não há dependências Python externas.
3. **Um projeto de destino**: a pasta onde você quer usar as skills e os agentes.
4. **Um agente compatível**, como Codex, Cursor ou Claude Code. Outros clientes podem ler as instruções compartilhadas pelo catálogo.

Confira sua versão do Python:

```bash
python --version
```

No macOS ou Linux, use `python3 --version` se o comando `python` não estiver
disponível. O Python é necessário para instalar e atualizar o kit; a conversa
do setup guiado usa as capacidades do agente.

## Instalação

### 1. Abra um terminal na pasta do kit

Todos os comandos a seguir são executados **na raiz deste repositório**, onde
está `scripts/specdev.py`. O destino é a pasta do projeto que receberá o kit.

Substitua o caminho de exemplo pelo caminho real. Mantenha as aspas se houver
espaços no nome de alguma pasta.

### 2. Simule a instalação

O modo `--dry-run` mostra o que seria criado ou atualizado e detecta conflitos.
Ele não grava arquivos no destino.

**Windows — PowerShell**

```powershell
python scripts/specdev.py install --target "C:/Projetos/meu-projeto" --profile generic --tools codex cursor claude --dry-run
```

**macOS / Linux**

```bash
python3 scripts/specdev.py install --target "/caminho/para/meu-projeto" --profile generic --tools codex cursor claude --dry-run
```

Os exemplos selecionam os três clientes. Você pode escolher somente os que usa,
por exemplo `--tools codex` ou `--tools cursor claude`. Se `--tools` for omitido
na primeira instalação, os três serão selecionados.

### 3. Instale o kit

Se a simulação estiver como esperado, execute o mesmo comando sem `--dry-run`:

**Windows — PowerShell**

```powershell
python scripts/specdev.py install --target "C:/Projetos/meu-projeto" --profile generic --tools codex cursor claude
```

**macOS / Linux**

```bash
python3 scripts/specdev.py install --target "/caminho/para/meu-projeto" --profile generic --tools codex cursor claude
```

O instalador preserva a configuração e as instruções existentes. Se encontrar
um arquivo gerenciado com alterações locais que não possa atualizar com
segurança, ele informa o conflito antes de gravar os arquivos planejados.

### 4. Abra o projeto no seu agente

Abra o **projeto de destino** no Codex, Cursor ou Claude Code e inicie uma nova
sessão. Confira se o cliente reconhece as skills e os agentes instalados.

| Cliente | Como o kit é disponibilizado |
| --- | --- |
| **Codex** | `AGENTS.md`, skills em `.agents/skills/` e agentes em `.codex/agents/`. |
| **Cursor** | `AGENTS.md`, regra em `.cursor/rules/`, skills compartilhadas e agentes em `.cursor/agents/`. |
| **Claude Code** | `CLAUDE.md`, cópias de skills em `.claude/skills/` e agentes em `.claude/agents/`. |
| **Outro agente** | Leia `AGENTS.md` e `.agents/CATALOG.md`; a descoberta automática depende do suporte do cliente. |

Consulte [Compatibilidade](COMPATIBILITY.md) para detalhes e limitações de
cada cliente.

### 5. Configure seu projeto

Peça ao agente:

> Use setup-project para conhecer e configurar este projeto.

A skill investiga os arquivos disponíveis, distingue fatos de hipóteses e faz
perguntas sobre o que falta. As respostas são registradas progressivamente; você
pode interromper e retomar a conversa depois.

O perfil **generic começa sem comandos de validação**. Configure os comandos,
diretórios e pré-requisitos reais do projeto antes de implementar tickets. O
agente pode ajudar nesse preenchimento; os comandos são declarativos e não são
executados pelo instalador.

Saiba mais em [Setup guiado](SETUP.md) e [Configuração](CONFIGURATION.md).

## Escolha um perfil

O perfil define um ponto de partida para `.specdev/project.json`. Se `--profile`
for omitido na primeira instalação, o padrão será `generic`.

| Perfil | Quando escolher | Ponto de partida |
| --- | --- | --- |
| `generic` | Qualquer stack ou arquitetura | Sem comandos de validação; configure-os para o projeto. |
| `python` | Projeto Python | Contexto Python e exemplo de validação com `unittest`. |
| `dotnet-angular` | Projeto com .NET e Angular | Contexto da stack e exemplos de build e testes. |

Revise os comandos e caminhos de cada perfil: são exemplos ajustáveis, não
detecção automática da arquitetura. Use `--profile` apenas na primeira
instalação; depois, edite `.specdev/project.json` no projeto consumidor.

## Conheça as skills

Peça uma skill pelo nome ou descreva a tarefa ao seu agente. As instruções
compartilhadas e os recursos de cada fluxo ficam em `.agents/skills/`.

| Skill | Para que serve |
| --- | --- |
| [`setup-project`](../.agents/skills/setup-project/SKILL.md) | Conhecer e configurar o projeto com perguntas guiadas. |
| [`write-ticket`](../.agents/skills/write-ticket/SKILL.md) | Escrever ou revisar tickets com critérios verificáveis. |
| [`enrich-plan`](../.agents/skills/enrich-plan/SKILL.md) | Investigar e completar o plano de um ticket. |
| [`implement-ticket`](../.agents/skills/implement-ticket/SKILL.md) | Implementar, revisar e validar um ticket até o handoff. |
| [`review-changes`](../.agents/skills/review-changes/SKILL.md) | Revisar mudanças com achados e evidências estruturados. |
| [`create-pr`](../.agents/skills/create-pr/SKILL.md) | Criar ou reutilizar um PR e vinculá-lo ao ticket quando autorizado. |
| [`merge-and-close`](../.agents/skills/merge-and-close/SKILL.md) | Fazer merge de um PR validado e concluir o ticket quando solicitado. |
| [`fast-merge`](../.agents/skills/fast-merge/SKILL.md) | Executar um merge direto quando solicitado explicitamente. |
| [`implement-in-worktree`](../.agents/skills/implement-in-worktree/SKILL.md) | Implementar uma tarefa em uma worktree isolada. |
| [`record-test`](../.agents/skills/record-test/SKILL.md) | Gravar um teste de interface solicitado. |

Alguns exemplos de pedidos:

> Use enrich-plan para preparar o plano do ticket 12.

> Use implement-ticket para implementar o plano 12-export-report.

> Use review-changes para revisar as mudanças desta branch.

Criar PR, publicar, fazer merge ou atualizar um rastreador depende da autorização
da tarefa. A existência de uma skill ou de uma configuração não dispara essas ações.

## O que fica no projeto

| Caminho | Finalidade |
| --- | --- |
| `.agents/` | Fonte compartilhada de skills, papéis, regras, templates, contextos e integrações. |
| `.specdev/project.json` | Configuração do projeto consumidor. |
| `.specdev/manifest.json` | Versão, clientes selecionados e hashes dos arquivos gerados. |
| `AGENTS.md` | Entrada compartilhada, com conteúdo local preservado. |
| `.codex/`, `.cursor/` e `.claude/` | Adaptadores dos clientes selecionados; Claude também recebe cópias das skills. |
| `CLAUDE.md` | Entrada do Claude Code, criada ou atualizada quando esse cliente é selecionado. |

Durante o setup guiado, o agente também pode criar
`.specdev/setup-state.json` para retomar a entrevista e um documento local de
contexto, como `docs/PROJECT_CONTEXT.md`. Esses arquivos pertencem ao projeto
consumidor. O instalador não os cria nem os gerencia.

O Git não é alterado pelo instalador. Para convenções compartilhadas pela equipe,
avalie versionar as entradas, skills, perfil e manifest. No projeto consumidor,
adicione `.specdev/backups/` e `.specdev/install.lock` ao `.gitignore`.

## Atualize o kit

Após atualizar sua cópia deste repositório, execute novamente a partir da raiz
do kit. Use o caminho do seu projeto e o mesmo comando Python da instalação.

```powershell
python scripts/specdev.py install --target "C:/Projetos/meu-projeto" --dry-run
python scripts/specdev.py install --target "C:/Projetos/meu-projeto"
python scripts/specdev.py check --target "C:/Projetos/meu-projeto"
```

No macOS/Linux, troque `python` por `python3` quando necessário e use o caminho
local do projeto. O perfil e os clientes já selecionados são preservados quando
as opções são omitidas. Para adicionar um cliente com `--tools`, informe o
conjunto completo, incluindo os clientes já instalados. A remoção de adaptadores
é manual; o instalador não apaga arquivos.

As atualizações criam backups em `.specdev/backups/` dos arquivos substituídos.
O planejamento detecta conflitos antes da escrita, mas uma falha de disco durante
a gravação pode deixar uma instalação parcial. Use os backups e o `check` para
identificar o que precisa ser restaurado. Evite instalações simultâneas no mesmo destino.

## Solução de problemas

| Situação | O que fazer |
| --- | --- |
| **Python não encontrado ou versão antiga** | Instale ou selecione Python 3.11+ e confira `python --version` ou `python3 --version`. |
| **O agente não encontra uma skill** | Abra uma nova sessão na raiz do projeto de destino, confira o cliente selecionado e consulte `.agents/CATALOG.md`. |
| **O destino já tem instruções ou arquivos gerados** | Execute `install --dry-run`, leia os conflitos e preserve as personalizações ao resolvê-los. |
| **O check aponta arquivos ausentes ou alterados** | Confira o resultado, execute uma simulação de instalação e resolva os conflitos antes de atualizar. |
| **O doctor indica validação ausente** | Configure os comandos e pré-requisitos reais em `.specdev/project.json`; o perfil genérico começa vazio. |
| **Alterei uma cópia em `.claude/`** | A fonte do kit é `.agents/`. Alterações na cópia gerada podem exigir resolução manual em uma atualização. |

Para conferir integridade e prontidão local, execute a partir da raiz do kit:

```powershell
python scripts/specdev.py check --target "C:/Projetos/meu-projeto"
python scripts/specdev.py doctor --target "C:/Projetos/meu-projeto"
```

`check` verifica integridade e versão. `doctor` também informa configuração
incompleta e disponibilidade local de diretórios e executáveis; ele não executa
os testes, acessa serviços ou comprova que uma validação passou.

## Documentação para aprofundar

- [Setup guiado e retomada](SETUP.md)
- [Configuração do projeto](CONFIGURATION.md)
- [Compatibilidade entre clientes](COMPATIBILITY.md)
- [Review com evidências](REVIEW.md)
- [Critérios, evidência e retomada de entregas](WORKFLOWS.md)
- [Origem e extração do JourneyCore](EXTRACTION.md)
- [Catálogo compartilhado de skills e papéis](../.agents/CATALOG.md)

Para validar alterações no próprio kit:

```bash
python -m unittest discover -s tests -v
python scripts/specdev.py validate
python scripts/specdev.py check --target .
```

Os testes verificam os formatos e o comportamento em disco. A descoberta e o
uso efetivo das skills precisam ser conferidos na sessão de cada cliente.
