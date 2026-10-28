# Evidência, conclusão e retomada

Os fluxos canônicos mantêm critérios, revisão e resultados ligados ao conteúdo
realmente analisado. O nível de registro acompanha o tamanho da tarefa.

## Critérios e validação

O [modelo de plano](../.agents/templates/PLAN.md) atribui IDs estáveis aos critérios.
A matriz de validação relaciona cada ID à implementação/teste e à evidência.
Enquanto o teste não foi executado, registre o resultado esperado e estado
pendente. Depois, substitua a expectativa por comando/artefato, resultado
observado e revisão coberta. Um teste verde sem cobertura do critério não o conclui.

Use [enrich-plan](../.agents/skills/enrich-plan/SKILL.md) para preparar os vínculos
e [implement-ticket](../.agents/skills/implement-ticket/SKILL.md) para mantê-los
durante a execução. Não crie testes que apenas procurem palavras nos documentos.

## Identidade da evidência

Registre base e head quando existirem, além da identidade do diff local ou de um
snapshot dos arquivos examinados. O SHA de HEAD sozinho não identifica alterações
não commitadas. Na ausência de commits, use um snapshot verificável e declare
essa condição, sem inventar um SHA.

Mudanças em head ou no conteúdo local exigem verificar o impacto sobre a evidência.
Invalide e repita review/testes afetados; não afirme cobertura da revisão nova com
resultado antigo. O [review](../.agents/skills/review-changes/SKILL.md) usa o contrato
v2 e a opção `--require-evidence` no validador para as novas revisões.

## Checkpoint proporcional

Para trabalho longo ou interrompido, registre no próprio plano:

- Último passo efetivamente concluído.
- Revisão e evidências correspondentes.
- Bloqueio real, ou ausência de bloqueio.
- Próxima ação concreta.
- Identificadores e estados de PR/ticket e commit de merge, quando existirem.

Ao retomar, releia os registros e consulte o estado atual antes de agir. Não
repita operações já concluídas nem trate intenção registrada como prova de sucesso.
Em tarefa pequena, essas informações podem ficar no handoff; não é necessário
criar um plano ou artefato adicional apenas para checkpoint.

## Merge e fechamento parcial

[merge-and-close](../.agents/skills/merge-and-close/SKILL.md) distingue PR aberto,
merged e fechado sem merge. Um PR já merged pode ter apenas fechamento de ticket
pendente: confirme sua identidade e commit e prossiga só com essa etapa autorizada.
Ticket já concluído não precisa de nova atualização. PR fechado sem merge é
bloqueio, não autorização para reabertura ou criação de outro PR.

Em PR aberto, vincule checks/reviews ao SHA de head e use merge condicional ao
SHA esperado quando a ferramenta o oferecer. Se head mudou, revalide. Sem essa
capacidade, faça a consulta imediatamente anterior à operação e declare o limite
de atomicidade. Se o projeto exigir garantia atômica, a ausência é bloqueio.

A atualização da base local pode ficar pendente se o checkout não permitir
fast-forward seguro. Relate esse estado separadamente do merge e do ticket.

## Merge direto

[fast-merge](../.agents/skills/fast-merge/SKILL.md) continua dispensando PR, CI e
rastreador quando explicitamente solicitado. A preparação verifica branch de
origem, HEAD, árvore limpa, remote e alvo. O fluxo registra o SHA remoto utilizado
no merge e publica o SHA resultante explicitamente, sem force.

Conflito ou estado inesperado interrompe a sequência. Preserve as alterações e
aguarde a decisão sobre resolução; não faça stash, reset, limpeza ou aborto como
efeito colateral. Após interrupção, confirme os estados local e remoto antes de
retomar, inclusive se a resposta do push não chegou.
