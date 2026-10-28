# Delegação por complexidade

O principal mantém escopo, arquitetura, contratos compartilhados, integração,
decisões de Git, validação final, estado de planos e handoff.

| Classe | Critério | Conduta |
| --- | --- | --- |
| S0 | Tarefa local, pequena e acoplada | Execute no principal. |
| S1 | Pergunta objetiva de leitura sobre um subsistema | Use specdev-explorer se houver trabalho independente e ganho real. |
| S2 | Implementação delimitada, contrato decidido, arquivos exclusivos | Use specdev-worker para a parte delimitada. |
| S3 | Arquitetura, múltiplas camadas, segurança, migração ou risco de dados | Principal decide e integra; delegue somente evidência ou partes S2. |

Delegue apenas com objetivo concreto, saída verificável, responsabilidade
exclusiva e trabalho que possa avançar independentemente. Não delegue o ticket
inteiro nem a mesma investigação a mais de um agente.

## Papéis e modelos

Os papéis canônicos estão em .agents/roles/. O instalador os converte para os
formatos disponíveis em cada ferramenta. specdev-reviewer revisa; o investigador
é reservado para comportamento desconhecido ou divergente, sem causa estabelecida.
Papéis de leitura não editam. Essa é uma instrução; isolamento de permissões
depende da ferramenta e da sessão.

Por padrão, o modelo é herdado. Overrides por ferramenta e papel ficam em models.
O formato antigo com ID como string permanece válido. Codex também aceita
model e reasoning_effort; configure esforço compatível ao trocar de modelo.
Claude aceita uma allowlist tools por papel, sem conceder permissões adicionais.
Restrinja ferramentas somente quando isso preservar a tarefa e a validação
necessárias. Não traduza essas opções para clientes que não as suportam.
Não traduza IDs de modelo entre fornecedores. Se um modelo solicitado não estiver
disponível, informe a limitação e execute sequencialmente quando viável; não crie
um agente apenas para trocar de modelo. Use apenas opções de contexto e paralelismo
suportadas pelo runtime. Não force um número de agentes pelo número de pastas.

## Contrato de delegação

Antes de cada spawn, forneça:

- Objetivo e classificação S1, S2 ou S3 com justificativa.
- Papel e configurações suportadas pela ferramenta.
- Arquivos ou responsabilidade permitidos; declare read-only quando pertinente.
- Contratos já decididos e critérios aplicáveis.
- Saída esperada e comando/evidência de verificação.
- Restrições: sem operações de Git, serviços externos, mudança de escopo ou
  conclusão de planos fora da responsabilidade recebida.
- Coordenação: você não está sozinho; não reverta mudanças alheias, adapte o
  trabalho ao estado atual e reporte conflitos. Não edite arquivos de outro responsável.

Dois workers não editam o mesmo arquivo nem o mesmo componente lógico.
O principal mantém trabalho não sobreposto, revisa cada entrega e roda os
checks finais. Sem delegação disponível, preserve o processo sequencialmente.

## Retorno e interrupção

Cada agente retorna, em formato proporcional à tarefa: resultado observado,
arquivos lidos ou alterados, evidência (comando/resultado ou caminho/linha),
bloqueios/limitações e próxima ação. Distingua teste executado de teste apenas lido.
O worker indica alterações incompletas; papéis de leitura não afirmam ter corrigido.

Em falha, interrupção ou conflito, pare as mutações da parte afetada e reporte
o último passo confirmado, arquivos que podem estar parciais e o que falta validar.
Não desfaça mudanças para simular limpeza nem assuma que cancelamento reverteu
arquivos. O principal confere o estado real antes de reatribuir ou encerrar;
preserva no plano o checkpoint quando necessário e segue sequencialmente se
não houver benefício ou capacidade para nova delegação.
