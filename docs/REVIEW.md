# Contrato de revisão

Novas revisões usam `schema_version: 2` e o schema em
`.agents/skills/review-changes/references/review.schema.json`. O validador Python
interpreta diretamente esse contrato com a biblioteca padrão; não mantém uma
segunda definição das regras de conteúdo e de veredito.

## Evidência v2

Exemplo estrutural; substitua identidades, comandos e evidências pelos reais:

~~~json
{
  "schema_version": 2,
  "summary": "Revisão dos arquivos listados, sem achados relevantes.",
  "verdict": "approve",
  "scope": {
    "base": "SHA_BASE_VERIFICADO",
    "head": "SHA_HEAD_VERIFICADO",
    "files": ["src/arquivo.py"]
  },
  "checks": [
    {
      "cwd": ".",
      "argv": ["python", "-m", "unittest", "discover", "-s", "tests", "-v"],
      "status": "passed",
      "evidence": "Comando executado; registrar resultado real e artifact quando houver."
    }
  ],
  "limitations": [],
  "blockers": [],
  "findings": []
}
~~~

`scope` exige base, head e uma lista de arquivos não vazia. Para mudanças locais,
inclua uma identidade explícita como `working-tree:IDENTIDADE_DO_SNAPSHOT`,
registrada com os arquivos inspecionados. Em repositório sem commits, declare
`unborn` para a base e identifique o snapshot local. Nomes de branch sozinhos
podem mudar e não comprovam qual conteúdo foi revisado. Se o conteúdo mudar,
reavalie a revisão e os checks afetados antes de reutilizar a evidência.

Cada check informa diretório, argumentos separados, estado e evidência textual.
`passed` e `failed` exigem execução observada; `not_run` informa por que não foi
executado. Ler o código de um teste não equivale a executá-lo. Uma revisão sem
comandos aplicáveis pode ter `checks: []`, com a limitação explicada quando
pertinente. Não crie comandos fictícios para preencher o documento.

- `approve`: sem P1/P2, blockers ou checks failed/not_run; P3 é permitido.
- `request_changes`: ao menos um achado P1/P2 com condição e consequência.
- `blocked`: ao menos um blocker, por exemplo ambiente obrigatório indisponível.

`limitations` descreve limites de cobertura; `blockers` descreve impedimentos
que inviabilizam concluir a revisão. Ambos usam listas de textos não vazios ou
listas vazias. Findings mantêm severity, file, line, title e body.

~~~powershell
python .agents/skills/review-changes/scripts/validate_review.py review.json --require-evidence
~~~

## Compatibilidade e limites

O formato legado exato `summary/verdict/findings` continua aceito sem
`--require-evidence`, inclusive `request_changes` vazio como antes. A flag exige
v2; o legado não atende à evidência das novas revisões. Aprovação com P1/P2 é
rejeitada nos dois formatos, também pelo schema publicado.

Strings precisam conter algo além dos caracteres Unicode White_Space listados
explicitamente no schema. Linhas seguem a semântica de inteiro do JSON Schema:
`1.0` representa o inteiro 1 e é aceito; booleanos, frações e valores não finitos
são rejeitados. Campos desconhecidos são rejeitados.

O validador implementa somente os recursos usados pelo schema empacotado, com
referências locais. Não é um motor JSON Schema de uso geral. Alterações no
schema que usem outro recurso exigem suporte e testes correspondentes.

Validade do documento não comprova existência de caminhos, linha correta,
autenticidade de revisão/execução nem suficiência de cobertura. O principal
confere essas evidências antes da entrega. O validador não executa comandos,
acessa Git, consulta serviços nem escreve no projeto.
