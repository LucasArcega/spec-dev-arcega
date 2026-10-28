---
name: create-pr
description: "Cria ou reutiliza PR da branch atual e vincula ao ticket configurado quando essa ação estiver autorizada."
---

# Criar pull request

Leia o perfil e .agents/integrations/github.md. Use o provedor de código
suportado nesta versão: GitHub. Outros provedores exigem um adaptador próprio.
Não mude o remote para atender a skill.

Confirme repositório, origem, base e arquivos da tarefa. Trabalhe com commits
pertinentes; não selecione nem descarte mudanças alheias.
Busque PR aberto com a identidade exata (repo/head/base) antes de criar.
Com múltiplas correspondências, esclareça; com uma, reutilize a URL.

Se necessário e autorizado, faça commit/push da branch para o remote validado.
Crie PR draft por padrão, com título descritivo e corpo contendo problema,
comportamento resultante e validação realmente executada.
Releia o PR e confirme URL, head e base.

Se tracking.provider for github ou clickup, leia a integração e resolva o ticket
por ID/URL explícito ou correspondência única. Adicione o vínculo só quando
autorizado, evitando duplicação. Sem conector, entregue o texto/link pendente
e registre que o vínculo não foi feito. Com none, entregue apenas o PR.
Não faça merge nem feche o ticket.
