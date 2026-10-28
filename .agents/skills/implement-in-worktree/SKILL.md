---
name: implement-in-worktree
description: "Prepara uma worktree isolada e segue o fluxo de implementação de um ticket."
---

# Implementar em worktree

Leia perfil, plano e dependências. Se já estiver na worktree correta, siga
implement-ticket. Não recrie nem resete uma worktree existente.

Resolva branch por git.branch_pattern e base por git.base_branch.
Confira git worktree list para localizar checkouts existentes e evite usar uma
branch que já está ativa em outro lugar. Preserve o checkout principal.
Prefira o recurso nativo de worktree quando disponível; caso contrário, use Git
com diretório explícito acordado/derivado para a tarefa, fora dos arquivos de produto.

Faça fetch do remote/base quando necessário. Crie a worktree a partir da base
resolvida ou reutilize a branch existente sem reset. Não troque a branch do
checkout principal como etapa de preparação.

Confirme cwd, git branch --show-current e git worktree list antes de editar.
Use caminhos explícitos se o runtime não permitir mudar o diretório da sessão.
Verifique se .specdev e as skills estão presentes no checkout criado; se a
configuração só estava em mudanças não commitadas, prepare o kit ali sem copiar
arquivos de produto ou credenciais do checkout principal.

Siga implement-ticket pulando a criação de branch já concluída.
Defina portas, banco, filas e dados por worktree antes de iniciar serviços de UI
ou integração. Não suponha que compartilhar a infraestrutura é seguro.
O kit não provisiona slots de banco nem copia secrets automaticamente.
Entregue caminho, branch, validações e URLs produzidas. Remova/arquive a worktree
somente quando não for mais necessária e a ação estiver autorizada.
