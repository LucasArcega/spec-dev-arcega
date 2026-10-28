---
name: fast-merge
description: "Executa merge direto com Git quando o usuário pedir fast-merge ou merge sem PR e CI."
---

# Merge direto

Ative somente para pedido explícito de merge direto/fast-merge.
Leia git.remote e git.base_branch do perfil; um alvo explícito no pedido prevalece.
A origem é a branch atual. Este fluxo dispensa gates de PR, CI e rastreador;
não publique em outro destino ou com force.

Antes de mutar, confira cwd/repositório, branch de origem e SHA de HEAD. Exija
HEAD em uma branch e árvore limpa, incluindo arquivos não rastreados e ausência
de merge/rebase em andamento. Se não estiver limpa, registre o bloqueio; não faça
stash, commit automático, reset ou limpeza. Valide a identidade do remote e o
nome da branch alvo, sem trocar de remote nem deduzir outro destino.

Com remote e alvo resolvidos, execute sequencialmente, passando valores como
argumentos, sem construir comandos de shell com texto interpolado:
1. git fetch REMOTE
2. Resolva e registre o SHA de refs/remotes/REMOTE/ALVO. Se a referência não
   existir, pare. Confira novamente origem/HEAD/estado para detectar mudanças.
3. git merge --no-edit SHA_ALVO
4. Registre SHA_RESULTANTE e confirme que a branch de origem continua ativa e
   a árvore está limpa. git push REMOTE SHA_RESULTANTE:refs/heads/ALVO

Não faça checkout da base, não crie PR nem feche ticket.
Se houver conflito, não resolva e não aborte automaticamente. Mostre git status
e git diff --name-only --diff-filter=U; aguarde a decisão.
Se o push ou outro comando falhar, apresente o erro e pare; não repita em loop
nem use --force. Confirme a referência remota após o push e informe origem, alvo
e SHA publicado. Se houver interrupção, releia Git e o remote antes de retomar;
não repita um push já confirmado nem presuma sucesso de uma resposta ausente.
Autenticação e permissões da sessão continuam sendo respeitadas.
