---
name: enrich-plan
description: "Analisa e completa planos de um ticket sem implementar código, criar branch ou abrir PR."
---

# Enriquecer plano

Leia .specdev/project.json e .agents/rules/WORKFLOW.md.
Resolva o identificador e a pasta dentro de paths.plans. Se houver múltiplos
candidatos, esclareça a identidade antes de editar.
Leia o README, os planos existentes, paths.status quando existir e o código
real dos serviços, endpoints, componentes e testes envolvidos.

Mapeie critérios ausentes, decisões abertas, dependências, riscos e validação.
Pergunte uma decisão de escopo por vez, com sugestão, antes de gravar critérios
que dependam dessa decisão. Continue a investigação independente.

Use .agents/templates/:
- README com contexto, branch, estado, prioridade e dependências verificadas,
  critérios com IDs estáveis, referências existentes, validação e exclusões.
- BACKEND.md e FRONTEND.md separados quando houver ambas as superfícies.
- PLAYWRIGHT.md para UI com Playwright; TESTS.md para outro runner.
  Inclua comportamento real, estados transitórios, responsividade e temas suportados.

Adapte o formato ao projeto. Campos sem fonte ficam explicitamente não definidos;
não transforme hipóteses em fatos. Só cite caminhos verificados.
Relacione cada critério a implementação/teste planejado e à evidência esperada.
Antes da execução, use estado pendente e descreva o resultado esperado; não
preencha a evidência como se o teste já tivesse passado. Para trabalho longo,
prepare checkpoint com último passo, revisão/evidência, bloqueio e próxima ação;
preserve registros existentes ao enriquecer um plano em andamento.
Delegação segue .agents/rules/DELEGATION.md e separa investigações independentes.
O principal decide e edita o plano.

Valide links, critérios, fronteira de escopo e os comandos no perfil/código.
Entregue arquivos e decisões. Não crie branch, código de produto, commit,
PR nem status de implementação concluída neste fluxo.
