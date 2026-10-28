# GitHub

Use quando a tarefa autorizar uma ação de GitHub. Prefira o conector disponível;
use gh autenticado como alternativa. Obtenha owner/repo de git.repository quando
preenchido e confira o remote configurado. Se ausente, derive do remote e valide.
Nunca substitua silenciosamente um remote.

Para PR, resolva branch de origem e base a partir da tarefa e do perfil. Antes de
criar, procure PR existente com origem, base e repositório exatos. Atualize apenas
se isso fizer parte do pedido. Evite PRs duplicados.
Use descrição com problema, mudança observável e validação. Em gh, preserve
multilinhas com --body-file em vez de construir comandos com texto interpolado.
Após criar, releia o PR e confirme origem/base/URL.

Tickets GitHub exigem repositório e número exatos. Para vínculo e fechamento,
confira a identidade; não use similaridade de título como autorização.
Para merge, siga merge-and-close. Não use bypass de proteção, --admin ou --force.

O kit não configura tokens, conexões, remotes ou permissões. Ferramenta indisponível
é uma limitação a reportar; não simule resultado.
