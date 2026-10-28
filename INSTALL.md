# Instalação do Spec Dev Arcega para agentes

Este arquivo orienta um agente a instalar o kit em um projeto consumidor. Siga
o pedido do usuário, as instruções do projeto e as permissões da sessão. O kit
não concede autoridade para publicar, commitar, fazer merge ou usar rastreadores.

## 1. Identifique destino e origem

- O **destino** é a raiz do projeto que o usuário pediu para configurar. Se o
  projeto estiver aberto na sessão, use sua raiz; respeite outro destino explícito.
  Se houver mais de um destino possível, esclareça antes de instalar.
- A **origem** é uma cópia completa do Spec Dev Arcega contendo este arquivo,
  `kit.json`, `profiles/`, `.agents/` e `scripts/specdev.py`. Se este arquivo foi
  lido de uma cópia local completa, use essa raiz. Se foi recebido por link,
  obtenha a mesma revisão do repositório que contém o arquivo usando os meios
  disponíveis na sessão. Uma cópia apenas deste `.md` não contém o instalador.
- Se a origem completa não estiver acessível ou não puder ser identificada pelo
  link, peça o caminho de uma cópia ou o endereço do repositório do kit. Não
  confunda o repositório de destino com o de origem nem invente URLs ou revisões.
- Leia as instruções locais do destino e confira o estado dos arquivos existentes.
  Preserve configuração, instruções, credenciais e alterações do projeto.

## 2. Prepare a instalação

O instalador requer Python 3.11 ou superior e usa apenas a biblioteca padrão.
Identifique um executável disponível (`python`, `python3` ou equivalente) e
confira sua versão. Se estiver indisponível, informe o bloqueio; não instale nem
altere runtimes do sistema por conta própria.

Para a primeira instalação, use o perfil `generic`, salvo se o usuário tiver
escolhido outro perfil existente. Por padrão, omita `--tools`: o instalador
seleciona Codex, Cursor e Claude. Se o usuário especificar clientes, passe-os em
`--tools`. Em projeto já configurado, não use `--profile`; preserve o perfil
existente. Em atualização, omitir `--tools` mantém os clientes registrados;
para adicionar clientes, informe todos os já instalados e os novos.

## 3. Instale e confira

Execute o script **a partir da raiz da origem**, com o caminho absoluto do
destino. Passe os caminhos e argumentos separadamente conforme o ambiente; não
use `eval` nem construa comandos de shell com conteúdo não confiável.

1. Execute `install --target DESTINO` com as opções escolhidas e `--dry-run`.
2. Se houver conflito, leia a mensagem, preserve os arquivos e resolva o que
   estiver autorizado. Não use reset, limpeza, substituição forçada ou edição
   de arquivos gerenciados para contornar a proteção.
3. Se a simulação estiver sem conflitos, execute o mesmo `install` sem `--dry-run`.
4. Execute `check --target DESTINO`. Confirme o resultado e informe qualquer
   aviso, inclusive ausência de validações configuradas no perfil `generic`.

Em termos de argumentos, os comandos são equivalentes a:

```text
PYTHON scripts/specdev.py install --target DESTINO --profile generic --dry-run
PYTHON scripts/specdev.py install --target DESTINO --profile generic
PYTHON scripts/specdev.py check --target DESTINO
```

`PYTHON` e `DESTINO` representam o executável e o caminho resolvidos; eles não
são valores literais. Inclua `--profile` somente na primeira instalação e
`--tools` apenas quando necessário, conforme a etapa anterior. O instalador
preserva o perfil existente e não executa os comandos declarados nele.

## 4. Configure o projeto quando solicitado

Se o pedido incluir configuração ou setup guiado, leia no **destino**
`.agents/skills/setup-project/SKILL.md` e siga o fluxo: investigue o projeto,
faça perguntas sobre decisões relevantes e registre as respostas progressivamente.
A configuração e o checkpoint pertencem ao projeto consumidor. A skill pode ser
lida diretamente mesmo se a lista de skills da sessão ainda não tiver sido atualizada.

O perfil `generic` começa sem comandos de validação. Isso é uma pendência de
configuração, não um teste aprovado. O `doctor` é opcional para a instalação e
para o setup; ele não executa testes nem comprova que o projeto está funcional.

Ao terminar, informe origem e destino, clientes selecionados, resultado do
`check`, arquivos instalados ou conflitos, avisos e a próxima ação. Distinga
instalação concluída de setup ainda em andamento. Não afirme que um cliente
descobriu a skill automaticamente ou que testes passaram sem evidência.
