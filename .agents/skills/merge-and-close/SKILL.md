---
name: merge-and-close
description: "Faz merge de um PR validado e fecha o ticket correspondente quando o usuário pedir essa entrega."
---

# Merge e fechamento

Use quando o usuário pedir merge e fechamento. Leia o perfil e as integrações.
A versão inicial usa GitHub para PR e GitHub/ClickUp/nenhum para tracking.

Confirme estado Git e a identidade exata de repositório, número do PR, head e base.
Não escolha commits nem altere arquivos pendentes como parte deste fluxo.
Resolva um único PR; se ainda não existir e a criação estiver autorizada,
siga create-pr e consulte novamente.

Releia o estado do PR antes de decidir o próximo passo:
- Aberto: registre o SHA de head analisado, valide mergeabilidade e checks/reviews
  obrigatórios dessa revisão. Se draft, converta para pronto somente dentro da
  entrega autorizada, depois de conferir as condições.
- Já merged: confirme repositório/head/base, data e commit de merge e a associação
  ao ticket. Pule o merge e prossiga somente com as etapas pendentes autorizadas.
- Fechado sem merge: registre o bloqueio; não reabra nem tente outro PR por conta própria.

Não use --admin, --force nem ignore proteções.

Antes do merge, resolva e leia um único ticket quando houver rastreador.
Evite merge que depois não possa ser associado ao ticket correto.
Somente para PR aberto, execute o método de merge adotado pelo projeto ou
especificado pelo usuário. Use a condição de SHA esperado quando a API/CLI disponível a
suportar. Se head mudar, invalide a aprovação anterior e revalide a revisão nova.
Sem operação condicional, releia head e checks imediatamente antes de mesclar e
registre que a verificação não é atômica; não prometa proteção contra corrida.
Se o projeto exigir essa garantia e a ferramenta não a oferecer, registre o bloqueio.
Para PR já merged, não execute esta operação novamente.
Releia o PR e confirme estado merged, data e commit.

Atualize a base local apenas se o checkout estiver limpo e a branch não estiver
em uso em outra worktree. Use fast-forward; se não puder, informe a pendência.
Releia o ticket e feche no status válido configurado apenas se ainda estiver
pendente. Se já estiver concluído, confirme o estado e não repita a atualização.
Se o merge já ocorreu e o fechamento falhou, informe os dois estados reais;
não repita o merge nem declare a entrega completa.

Registre no plano ou handoff PR/ticket, SHA validado e commit de merge, último
passo concluído, evidência, bloqueio e próxima ação. Uma retomada começa relendo
esses estados; atualizar a base local pode permanecer como pendência independente.
