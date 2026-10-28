<div align="center">

# Spec Dev Arcega

**Um kit de skills e agentes para trabalhar com o seu projeto.**

Do planejamento à entrega, seguindo o contexto e as regras da sua equipe.

`Codex` · `Cursor` · `Claude Code` · `outras ferramentas compatíveis`

</div>

---

## Instale com uma mensagem

Abra o projeto que receberá o kit no seu agente e envie:

```text
Leia https://github.com/LucasArcega/spec-dev-arcega/blob/main/INSTALL.md e instale o kit neste projeto.
Depois, inicie o setup guiado.
```

O agente vai localizar o kit, conferir o projeto, simular a instalação e
aplicar as alterações. Depois, vai fazer algumas perguntas para conhecer o
projeto e preencher a configuração com você.

> **Acesso ao kit:** o agente precisa acessar este repositório ou uma cópia local
> completa. Se não conseguir localizar a origem, ele pedirá o caminho ou o endereço.

O instalador requer **Python 3.11+** na máquina que fará a instalação. O setup
guiado usa as capacidades do agente e não depende de um cliente específico.

## O que acontece depois?

| Etapa | Seu agente cuida de |
| --- | --- |
| **Instalar** | Confere a origem e o destino, simula e instala o kit. |
| **Conhecer** | Lê a documentação e as convenções do projeto. |
| **Perguntar** | Pergunta o que precisa ser definido, uma decisão por vez. |
| **Configurar** | Registra as respostas e permite retomar o setup depois. |
| **Conferir** | Verifica a instalação e informa o que ficou pendente. |

O perfil `generic` começa sem comandos de validação. Durante o setup, o agente
ajuda a registrar os comandos e pré-requisitos reais do projeto. O instalador
não executa esses comandos automaticamente.

## Como usar as skills

Depois da instalação, você pode pedir as tarefas em linguagem natural ou citar
o nome da skill para deixar o fluxo mais claro. Os exemplos abaixo são mensagens
para enviar **no chat do agente**. Troque os números e caminhos pelos do seu
projeto; eles não são comandos de terminal.

| Skill | Quando usar | Exemplo de pedido |
| --- | --- | --- |
| [`setup-project`](.agents/skills/setup-project/SKILL.md) | Configurar o projeto ou continuar o setup. | `Use setup-project para configurar este projeto.` |
| [`write-ticket`](.agents/skills/write-ticket/SKILL.md) | Redigir ou revisar um ticket. | `Use write-ticket para redigir um ticket sobre exportação de relatórios.` |
| [`enrich-plan`](.agents/skills/enrich-plan/SKILL.md) | Investigar e completar o plano de um ticket. | `Use enrich-plan para preparar o plano do ticket 12.` |
| [`implement-ticket`](.agents/skills/implement-ticket/SKILL.md) | Implementar o plano, revisar e validar. | `Use implement-ticket para implementar o plano do ticket 12.` |
| [`implement-in-worktree`](.agents/skills/implement-in-worktree/SKILL.md) | Fazer a implementação em uma worktree isolada. | `Use implement-in-worktree para implementar o ticket 12.` |
| [`review-changes`](.agents/skills/review-changes/SKILL.md) | Revisar alterações e apontar problemas. | `Use review-changes para revisar as alterações desta branch.` |
| [`create-pr`](.agents/skills/create-pr/SKILL.md) | Criar ou reutilizar um PR e vincular o ticket, quando solicitado. | `Use create-pr para abrir o PR desta branch e vincular o ticket 12.` |
| [`merge-and-close`](.agents/skills/merge-and-close/SKILL.md) | Fazer merge do PR validado e fechar o ticket. | `Use merge-and-close para fazer merge do PR 34 e fechar o ticket 12.` |
| [`fast-merge`](.agents/skills/fast-merge/SKILL.md) | Fazer merge direto, sem PR ou CI, quando isso for pedido. | `Use fast-merge para fazer merge direto da branch atual em develop.` |
| [`record-test`](.agents/skills/record-test/SKILL.md) | Gravar um teste de interface específico. | `Use record-test para gravar o teste em caminho/do/spec.` |

Para continuar uma configuração interrompida, peça:

```text
Use setup-project para continuar o setup de onde paramos.
```

Um fluxo comum é preparar o plano com `enrich-plan`, implementar com
`implement-ticket` e, quando estiver pronto para entrega, pedir o `create-pr`
ou o `merge-and-close`. O `fast-merge` é para o caso em que você quer pedir
**merge direto**, dispensando PR e CI.

O `enrich-plan` prepara o plano sem implementar o código. O `implement-ticket`
vai até revisão, validação e handoff; commit, push e PR dependem do pedido.
As skills de PR e merge usam GitHub nesta versão. O vínculo e o fechamento do
ticket dependem do rastreador configurado e da operação solicitada.

O kit também inclui papéis de agentes, regras e templates. A fonte compartilhada
fica em `.agents/`; cada cliente recebe os formatos disponíveis para ele.
Veja o [catálogo completo](.agents/CATALOG.md).

## Comandos do instalador

O caminho mais simples é pedir ao agente para seguir o [INSTALL.md](INSTALL.md).
Se precisar rodar os comandos você mesmo, abra um terminal **na pasta do Spec Dev**,
onde está `scripts/specdev.py`, e troque o caminho pelo projeto de destino.

Os exemplos usam `python`. No macOS/Linux, use `python3` se esse for o comando
disponível. O instalador precisa de Python 3.11 ou superior.

### Instalar pela primeira vez

Primeiro, simule a instalação para conferir os arquivos e possíveis conflitos:

```powershell
python scripts/specdev.py install --target "C:/Projetos/meu-projeto" --profile generic --tools codex cursor claude --dry-run
```

Se estiver tudo certo, rode o mesmo comando sem `--dry-run`:

```powershell
python scripts/specdev.py install --target "C:/Projetos/meu-projeto" --profile generic --tools codex cursor claude
```

No macOS/Linux, substitua o destino por um caminho do sistema, como
`/caminho/para/meu-projeto`. As opções funcionam assim:

| Opção | Para que serve |
| --- | --- |
| `--target` | Caminho do projeto que vai receber o kit. Use aspas se houver espaços. |
| `--profile` | Perfil inicial: `generic`, `python` ou `dotnet-angular`. Use só na primeira instalação. |
| `--tools` | Clientes a instalar: `codex`, `cursor` e/ou `claude`. Se omitido na primeira instalação, instala os três. |
| `--dry-run` | Mostra o que mudaria e aponta conflitos, sem gravar arquivos no destino. |

Os perfis são pontos de partida. O `generic` não vem com comandos de validação;
`python` e `dotnet-angular` trazem exemplos que precisam ser ajustados ao projeto.

### Conferir a instalação

```powershell
python scripts/specdev.py check --target "C:/Projetos/meu-projeto"
python scripts/specdev.py doctor --target "C:/Projetos/meu-projeto"
```

O `check` confere arquivos gerados, configuração e versão. O `doctor` também
aponta configuração incompleta, diretórios ou executáveis ausentes e pré-requisitos
que precisam ser verificados. Ele não executa os testes do projeto.

Se quiser conferir apenas algumas superfícies configuradas, use por exemplo:

```powershell
python scripts/specdev.py doctor --target "C:/Projetos/meu-projeto" --surfaces backend frontend
```

### Atualizar ou adicionar clientes

Depois de atualizar sua cópia do Spec Dev, simule e aplique a atualização:

```powershell
python scripts/specdev.py install --target "C:/Projetos/meu-projeto" --dry-run
python scripts/specdev.py install --target "C:/Projetos/meu-projeto"
```

Sem `--profile` e `--tools`, o instalador preserva o perfil e os clientes já
selecionados. Para adicionar um cliente com `--tools`, inclua também os que já
estavam instalados. Por exemplo, se o projeto já usa Codex e Cursor e você quer
adicionar Claude:

```powershell
python scripts/specdev.py install --target "C:/Projetos/meu-projeto" --tools codex cursor claude --dry-run
python scripts/specdev.py install --target "C:/Projetos/meu-projeto" --tools codex cursor claude
```

Se aparecer um conflito, confira o arquivo indicado e preserve as alterações
locais. As atualizações criam backups em `.specdev/backups/`; a remoção de
adaptadores é manual. Veja o [guia de instalação](docs/INSTALACAO-MANUAL.md)
para mais detalhes e solução de problemas.

### Validar o próprio kit

Para conferir as skills e os perfis da cópia do Spec Dev que você está usando:

```powershell
python scripts/specdev.py validate
```

Esse comando verifica o kit na pasta atual. Para conferir uma instalação em
outro projeto, use `check --target` como mostrado acima. A lista de comandos e
opções também está disponível com `python scripts/specdev.py --help`.

## Precisa de mais detalhes?

- [Instalação manual, perfis e solução de problemas](docs/INSTALACAO-MANUAL.md)
- [Setup guiado e retomada](docs/SETUP.md)
- [Configuração do projeto](docs/CONFIGURATION.md)
- [Compatibilidade entre clientes](docs/COMPATIBILITY.md)
- [Review com evidências](docs/REVIEW.md)
- [Critérios, evidência e retomada de entregas](docs/WORKFLOWS.md)
- [Origem e extração do JourneyCore](docs/EXTRACTION.md)

O Spec Dev Arcega nasceu a partir de práticas do JourneyCore. Seus fluxos
compartilhados podem ser adaptados a projetos de outras stacks e arquiteturas.
