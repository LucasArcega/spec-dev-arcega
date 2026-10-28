# Acordos compartilhados

Leia o perfil em .specdev/project.json e as instruções específicas do projeto.
O perfil é um contrato deste kit, não uma configuração nativa do editor.
Campos do perfil descrevem opções; não concedem autorização nem executam ações.

## Escopo e contexto

- Use a skill pertinente em .agents/skills/. Não carregue todas as skills,
  regras de stack e documentos de uma vez. Consulte .agents/CATALOG.md.
- Trabalhe apenas no pedido e nos critérios aceitos. Sugestões ficam fora do
  plano até serem aceitas. Não inclua tarefas opcionais nos critérios.
- Resolva caminhos a partir da raiz do projeto. Leia somente os documentos
  selecionados em context; convenções adicionais do projeto continuam válidas.
- Antes de editar contratos, leia código e testes reais. Não invente caminhos,
  prioridade, dependências, endpoints, capacidades de ferramenta ou resultados.
- Quando uma decisão ausente mudar o escopo, esclareça uma questão por vez,
  com uma sugestão. Continue o trabalho independente; não repita perguntas já resolvidas.

## Planejamento e implementação

- Use paths.plans e paths.status para localizar planos e dependências.
  O padrão de branch vem de git.branch_pattern, com ticket e slug resolvidos.
- Separe BACKEND.md e FRONTEND.md quando as duas superfícies existirem.
  Para UI, registre em PLAYWRIGHT.md (ou TESTS.md para outro runner) os fluxos,
  estados transitórios, erros, loading, responsividade e temas oferecidos pelo produto.
- Dark mode só é exigível em um produto que oferece esse tema.
  A tecnologia e a arquitetura do JourneyCore não se tornam requisitos de outros projetos.
- Cada critério precisa de ID estável, comportamento observável e evidência de
  validação. Relacione critério, implementação/teste e resultado no plano.
  Use .agents/templates/ como modelos, preenchendo apenas seções aplicáveis.
- Antes de implementar, confirme dependências e o estado Git. Preserve mudanças
  existentes. Não faça stash, reset, limpeza, checkout forçado ou refatoração incidental.

## Validação e conclusão

- Selecione validation pelos surfaces alterados. Execute os comandos pertinentes
  no cwd indicado, usando argv como argumentos e o shell apropriado ao ambiente.
  Não execute strings de configuração com eval.
- Valide dependências de ambiente em requires. Integração, serviços em execução e
  validação de UI dependem do escopo. Não rode suites amplas a cada iteração.
- Comandos são declarativos: o instalador nunca os executa.
  O agente verifica se fazem sentido para a tarefa e registra comando, resultado e limitação.
- Para código executável alterado, faça revisão com evidências antes da entrega.
  Use review-changes com o contrato de evidência atual e --require-evidence.
  Registre base/head e a identidade das mudanças locais analisadas; só o SHA de
  HEAD não identifica o working tree. Se o conteúdo ou a revisão mudar, reavalie
  a cobertura e invalide/reexecute as evidências afetadas antes da conclusão.
  Documentação simples não exige processo pesado nem testes que apenas conferem
  palavras no texto.
- Estado concluído exige critérios obrigatórios e validações pertinentes verdes.
  Falha ou ausência de ambiente obrigatório permanece como bloqueio documentado;
  não afirme que testes passaram sem execução.
- Atualização de imagem exige rebuild e exercício da rota/fluxo alterado;
  um processo healthy não comprova presença do código atual.
- O handoff informa arquivos, comportamento, validações e pendências reais.
  Use o idioma de project.language para tickets e planos.
- Em trabalho longo ou interrompido, registre no plano o último passo concluído,
  a revisão e suas evidências, bloqueio e próxima ação; inclua estados reais de
  PR/ticket quando existirem. Ao retomar, releia esse registro e o estado atual.
  Não repita mutações concluídas nem reutilize evidência de conteúdo alterado.
  Para tarefa pequena, mantenha esse registro no handoff, sem criar artefatos extras.

## Integrações e autoridade

- Leia .agents/integrations/github.md ou clickup.md somente ao usar o serviço.
  tracking.provider = none permite trabalhar com planos locais.
- Criar PR, comentar, atualizar status ou publicar depende do escopo autorizado;
  habilitar um provedor no perfil não dispara essas operações.
- delivery.create_pr expressa uma preferência. Respeite a autorização da tarefa.
  Merge e fechamento exigem pedido explícito; fast-merge só atende esse modo explícito.
- Não copie tokens, senhas, arquivos de credenciais, MCPs pessoais ou configurações
  de permissões entre projetos. Use os mecanismos de autenticação disponíveis.
