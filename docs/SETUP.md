# Setup guiado do projeto

Após instalar o kit, abra o projeto consumidor em um agente e peça, por exemplo:

> Use setup-project para conhecer e configurar este projeto.

A skill canônica está em [setup-project](../.agents/skills/setup-project/SKILL.md).
O agente investiga a documentação e os arquivos relevantes, distingue fatos
verificados de hipóteses e pergunta uma decisão relevante por vez. Ele registra
as respostas progressivamente e retoma de onde parou. O roteiro em
[questions.md](../.agents/skills/setup-project/references/questions.md) organiza
as decisões por assunto, sem impor uma lista fixa de perguntas.

O fluxo depende de capacidades de leitura, edição e diálogo, não de um cliente,
terminal, Python ou comando específico. Ele pode consultar ferramentas locais
disponíveis, incluindo doctor, quando isso ajudar. Não executa validações apenas
porque foram encontradas no perfil; disponibilidade e execução são registradas
separadamente. Se o kit ou perfil ainda não estiver instalado, informe a etapa
de instalação. O instalador do kit continua usando Python 3.11+.

## Arquivos do consumidor

| Arquivo | Uso |
| --- | --- |
| `.specdev/project.json` | Configuração operacional confirmada: caminhos, validações, Git e integrações aplicáveis. |
| `docs/PROJECT_CONTEXT.md` | Caminho sugerido para informações próprias do projeto; outro caminho local pode ser utilizado. |
| `.specdev/setup-state.json` | Checkpoint de progresso da entrevista, pertencente ao consumidor. |

O instalador distribui a skill, a referência e o template, mas não cria o contexto
ou checkpoint do projeto. A skill os cria ou atualiza durante o setup solicitado.
Ela preserva a configuração local e documentos existentes. Quando usa um
documento local de contexto, acrescenta o caminho ao array `context` depois de o
arquivo existir, sem duplicar entradas. Se o documento sugerido já existir, o
agente lê e preserva seu conteúdo e combina outro caminho quando necessário.

O [template de contexto](../.agents/skills/setup-project/assets/project-context.md)
é adaptado apenas às seções úteis. Não armazene credenciais ou valores de segredos
no perfil, contexto ou checkpoint. A configuração de conexões e permissões do
cliente continua sob responsabilidade da sessão.

## Retomada e estados

O checkpoint v1 guarda `schema_version`, `status`, `context_path`, `scope`,
`decisions`, `pending`, `next_question` e `verification`. `scope` identifica
as decisões do pedido; as demais não são consideradas avaliadas em um setup
parcial. As decisões têm um ID estável, estado e fonte resumida. Os valores
confirmados ficam no perfil ou contexto, evitando duplicá-los no checkpoint.

- `confirmed`: resposta do usuário ou fato diretamente verificado, com fonte.
- `inferred`: hipótese, ainda pendente de confirmação.
- `pending`: decisão ainda não resolvida.
- `not_applicable`: decisão explicitamente não aplicável ou comprovada como tal.

`pending` lista os IDs aplicáveis ainda pendentes ou inferidos; `next_question`
guarda a próxima pergunta ou `null`. `verification` registra em texto o estado
da configuração, a disponibilidade observada e o que foi executado. Isso não
transforma uma hipótese em fato nem um comando configurado em teste executado.
Quando um ID agrupa vários campos, todos os campos aplicáveis precisam estar
confirmados, verificados ou expressamente considerados não aplicáveis antes de
resolver o grupo. O agente preserva os campos já conhecidos e mantém pendentes
os demais; confirmações parciais não concluem o ID inteiro.

Na retomada, o agente relê estado e arquivos, reconciliando divergências sem
apagar alterações locais. Versão desconhecida, estado inválido ou caminho inseguro
interrompem a edição afetada, preservando os dados para resolução. A conclusão
exige decisões do escopo resolvidas, nenhuma pendência e configuração estruturalmente
conferida. Disponibilidade de serviços e execução de testes são relatadas conforme
o observado; não são requisitos automáticos para concluir a configuração.

## Compatibilidade

O instalador fornece a fonte compartilhada para Codex e Cursor e gera a cópia para
Claude Code com os mesmos recursos. Outro cliente pode ler a skill pelo catálogo
e seguir seu contrato com as capacidades disponíveis. O reconhecimento automático
e a execução real dependem da versão e da sessão de cada cliente; confira-os no
ambiente em que o kit será utilizado.
