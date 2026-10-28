---
name: record-test
description: "Grava vídeo da execução de um teste de UI solicitado usando o runner disponível, especialmente Playwright."
---

# Gravar teste

Leia perfil e configuração real do runner. Resolva um spec e o projeto do teste;
pergunte se faltar a identidade. Não grave a suite inteira como efeito colateral.
Verifique serviços, credenciais de teste e versão mínima exigida pelo projeto;
não fixe Node, portas, pasta ou project vindos de outro repositório.

Em Playwright, video é configuração de use; não suponha uma flag --video.
Use o mecanismo por ambiente já existente, ou uma configuração temporária que
estenda a real e habilite vídeo nessa execução. Não deixe video=on permanente
nem altere a configuração de produto para cumprir um pedido de gravação.

Execute o spec no cwd correto. Registre o início e o diretório de saída.
Localize o WebM realmente criado nessa rodada, distinguindo o teste pedido de
setup/login e retries. Não reutilize um vídeo antigo como evidência.
Se o teste falhar mas houver vídeo, entregue o arquivo com o resultado de falha.
Sem gravação produzida, informe o motivo sem inventar um artifact.

Retorne link Markdown para o caminho absoluto e resultado observado.
Não commite vídeos, relatórios, estado autenticado ou credenciais.
Se o runner não suportar gravação disponível, informe a limitação.
