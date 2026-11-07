# Guia de autoria · mini mentorias Zion Arsenal

Cada produto é **um arquivo** `app/products/<ID>.js` que chama `ZA.register({...})`, mais um arquivo de testes `tests/profiles/<ID>.json`.
O motor (`app/engine.js`) **não deve ser editado** por quem escreve produtos. Se faltar algum recurso, registre isso no relatório.

**Referência obrigatória:** `app/products/A02.js` (produto completo e testado). Copie a estrutura dele.

## Estrutura fixa (validada por `ZA.validateConfig`)
- `intro`: exatamente 3 telas, com `kind` igual a `mirror` (Espelhamento), `collapse` (Colapso de crença) e `start` (promessa + campos iniciais). A tela `start` coleta pelo menos `nome` e `propriedade` (nome da hospedagem/terra/projeto), que aparecem no relatório.
- `pillars`: exatamente 7. Cada um com 5 telas, nesta ordem: `learn`, `compare`, `form`, `feedback`, `apply`.
  - `learn`: `{title, body (HTML), example (HTML)}`, para ensinar o conceito com um exemplo numérico ou prático.
  - `compare`: `{title, intro?, cols:[{h, type:'bad'|'good'|undefined, items:[...]}]}`, para errado × certo, opção A × B etc.
  - `form`: o exercício do pilar (há 7 exercícios). `{title, intro, fields:[...]}`, com pelo menos 1 campo.
  - `feedback`: `{title, metrics:(s,c)=>[...], feedback:(s,c)=>[{lv:'ok'|'warn'|'bad'|'info', t:'HTML'}]}`. O texto deve reagir aos dados.
  - `apply`: `{title, intro?, actions:[{id:'aX_n', text}]}`, com 3 ações marcáveis (o motor acrescenta o campo "minha ação").
- O motor acrescenta a tela 39 (consolidação) e a tela 40 (relatório), totalizando **40 telas**.
- Funções obrigatórias: `compute(s)`, `metrics(s,c)`, `priorities(s,c)` e `report(s,c)`.

## Campos (`fields`)
`{id, label, type, required, min, max, step, unit, help, placeholder, allowUnknown, options:[{v,l,d?}], validate:(v,s)=>'msg'|''}`
- Tipos: `number`, `money`, `percent` (0–100 por padrão), `text`, `textarea`, `select`, `radio`, `checks` (array), `scale` (1–5, `ends:['ruim','ótimo']`) e `list` (linhas `{name,value}` com `preset:[...]`, para listas de custos).
- `allowUnknown: true` mostra a opção "Não sei", e o campo fica como dado ausente (o relatório avisa). Use em dados que o cliente pode não ter.
- IDs de campo são **únicos no produto inteiro**, em snake_case.
- Negativos são bloqueados por padrão (min 0). Percentual fora de 0–100 é bloqueado.

## Acesso aos dados nas funções
`s.n(id, padrao)` retorna um número (ou o padrão se vazio/"não sei"); `s.t(id)` retorna texto; `s.v[id]` dá o valor bruto (arrays em `checks`/`list`); `s.has(id)` diz se há valor; `s.unknown(id)` diz se o cliente marcou "não sei"; `s.checked(actionId)`.
Utilitários: `ZA.fmt.brl/brl0/pct/num/meses`, `ZA.listSum(rows)`, `ZA.safeDiv(a,b)`, `ZA.clamp`, `ZA.esc` (**sempre** escape texto digitado pelo usuário antes de colocar em HTML), `ZA.table(head, rows, numCols)`, `ZA.op3d(items)`.
`compute` precisa ser **robusto a dados ausentes**: nunca produzir NaN, Infinity ou `undefined` visíveis. Use padrões explícitos e mostre "—" quando não houver dado.

## Métricas e origem do dado
Cada métrica: `{label, value:'string formatada', tag}`, com `tag` ∈ `informado`, `calculado`, `estimativa`, `hipotese`, `recomendacao`, `externo`.
Diferencie sempre: dado informado pelo cliente, resultado calculado, estimativa/hipótese (premissa assumida) e recomendação.
**Nunca inventar números de mercado.** Referências como "faixa comum" devem ser apresentadas como orientativas e marcadas `estimativa`, ou o cliente deve informar o dado. Não use dados externos não verificados.

## OP3D (`priorities`)
Retorne uma lista de candidatos `{title, why, score (1–10)}`, cada um ativado por condições nos dados. Inclua de 8 a 15 candidatos possíveis, para que o motor tenha o que priorizar. O motor ordena e monta Nível 1 (20%), Nível 2 (4%) e Nível 3 (a ação essencial).

## Relatório (`report`)
Retorne `{sections:[{title, html}], plan:'HTML'}`. O motor já inclui: cabeçalho, indicadores (`metrics`), OP3D, ações marcadas, pontos de atenção, dados ausentes e o aviso legal (`disclaimer` do produto).
- Inclua uma seção "Premissas utilizadas" (tabela com valor e origem).
- Produtos financeiros (A03, A08, A09, B06, B08, B09 etc.) devem mostrar **três cenários: Conservador, Intermediário, Otimista**, com premissas explícitas.
- `plan` é um roteiro de 30 dias (ou por etapas) montado a partir das prioridades OP3D (veja A02).

## Regras de conteúdo (obrigatórias)
- ECROI: espelhamento → colapso → reconhecimento (diagnóstico) → orientação (passo a passo) → implementação (exercícios e relatório).
- Português do Brasil, linguagem direta e próxima do público, sem jargão desnecessário.
- **Não prometer**: reservas, faturamento, lucro, retorno, captação de investidores, aprovação de licenças. Use "preliminar", "orientativo", "estimativa".
- Nada de depoimentos, casos reais inventados ou estatísticas de mercado não verificadas. Exemplos usam números ilustrativos e são declarados como tal ("Exemplo:").
- Questões jurídicas, ambientais e contratuais (terrenos, sociedades, licenças): orientar a buscar profissional habilitado (advogado, contador, engenheiro), sem dar parecer.
- Conteúdo específico do produto, sem texto genérico repetido entre pilares.
- O `disclaimer` do produto deve ser específico (ex.: B01: "não garante captação de investimento").

## Testes
Crie `tests/profiles/<ID>.json` com 3 perfis (veja `tests/profiles/A02.json`):
1. `iniciante`: dados simples e completos;
2. `intermediario`: dados mais ricos (roda em viewport de celular);
3. extremo/incompleto: vários campos em `unknown` (apenas campos com `allowUnknown`), valores-limite e `actionsPerPillar: 0`.
- `values` cobre todos os campos obrigatórios não marcados como desconhecidos. Para `list`, informe o array de `{name,value}`.
- `expect`: pelo menos 3 valores de `compute` por perfil, **calculados à mão por você** (não copie a saída do código), para provar que as fórmulas estão corretas.
- `reportContains`: textos que devem aparecer no relatório.

Rode: `node tests/run.js <ID>` (a partir de `/home/user/zion-arsenal`). O produto só está pronto com **100% dos checks ok**. A saída fica em `tests/out/<ID>/` (PDFs, screenshots, `resultado.txt`).
