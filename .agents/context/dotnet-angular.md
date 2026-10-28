# Perfil .NET e Angular

Leia este arquivo somente se selecionado por context. Caminhos, versões,
comandos e convenções concretas vêm do perfil e do código existente.

## Backend

Preserve o sentido de dependências das camadas já adotadas. Quando o projeto usa
Clean Architecture, a aplicação depende de abstrações; infraestrutura implementa
essas abstrações. Controllers tratam HTTP e delegam regras de negócio.
Use constantes de status, validação de domínio nas factories/métodos de atualização,
NRT, async e CancellationToken seguindo os padrões existentes.
Organize entidades por contexto; não mova arquivos como refatoração incidental.
Defina o dono do commit da unidade de trabalho; não adicione SaveChanges em cada
repositório se o projeto usa commit coordenado. Evite carregar tabelas para bulk
delete e preserve filtros de tenant. Migrations exigem validação com banco real
quando alterarem persistência relevante.

## Frontend

Siga a versão e os padrões reais do app: standalone, templates estritos, control
flow moderno, inject e OnPush onde compatíveis. Use teardown de subscriptions
e mantenha regras/HTTP nos serviços existentes.
Inspecione inputs, outputs e defaults antes de reutilizar componentes.
Valide overlays realmente abertos em desktop/mobile, além da página subjacente.
Se o produto usa ngx-translate, mantenha as chaves em todos os idiomas configurados.
Não imponha i18n ou dark mode a um produto que não oferece esses recursos.

## Ambiente e testes

Distinga testes unitários de integração com Docker e testes de UI.
Rebuild de imagem e exercício da rota alterada são necessários para comprovar
código em execução quando containers forem atualizados. Credenciais ficam em
secrets/ambiente. Portas e dados por worktree precisam de isolamento explícito.
