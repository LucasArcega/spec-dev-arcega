# ClickUp

Use somente quando tracking.provider = clickup e o pedido autorizar a operação.
Use o conector autenticado disponível; nunca copie credenciais ou configure MCP
pessoal a partir de outro projeto.

Use tracking.list_id e o workspace fornecido pelo projeto. Se ainda faltarem,
faça a consulta de leitura necessária ou peça a informação antes da mutação.
Use o ID/URL explícito do plano; na ausência, exija correspondência única pelo
identificador do ticket. Não escolha a task mais parecida.

Descubra os status válidos. tracking.statuses mapeia intenções pending,
in_progress e done para nomes exatos; valide o mapeamento na lista antes de atualizar.
Sem mapeamento, exija um status inequívoco para a intenção; caso contrário, esclareça.
Releia a task após a alteração.

Para vincular PR, prefira comentário com a URL quando autorizado. Se comentário
não estiver disponível, preserve a descrição e prepare a mudança da seção Pull
Request; aplique só se a autorização abranger editar essa descrição.
Evite comentários duplicados e não dispare notify_all por padrão.
