# Resultado da suíte de homologação financeira (T1 a T12)

Gerado em 2026-11-09T06:16:24.838Z · Plano: PLANO_TESTES_HOMOLOGACAO.md v0.2 (09/11/2026) · Dicionário: DICIONARIO_FINANCEIRO.md v0.4 (09/11/2026)

**Nada foi homologado por esta execução.** OK significa só que a fórmula reproduz o valor esperado do plano.

## Dependências

| Dependência | Disponível | Observação |
|---|---|---|
| zaios | não | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| arsenal | sim |  |
| folha | sim |  |
| folha+zaios | não | Precisa da Folha J2 e da ZAIOS. |
| zaiosComp | não | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| f05 | sim |  |

## Contagem

| Status | Casos |
|---|---|
| NÃO EXECUTADO (dependência ausente) | 115 |
| OK | 84 |
| LIMITAÇÃO CONFIRMADA (decisão pendente) | 5 |
| DIVERGÊNCIA CONFIRMADA | 18 |
| PENDENTE DE VALIDAÇÃO ECONÔMICA | 15 |

## Casos

| ID | Teste | Ferramenta | Indicador | Decisão | Tipo | Esperado | Obtido | Status | Nota |
|---|---|---|---|---|---|---|---|---|---|
| T1-ZAIOS-01 | T1 | ZAIOS | Receita bruta/ano | v0 | formula | 282948 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T1-ZAIOS-02 | T1 | ZAIOS | Receita real | v0 | formula | 234846.84 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T1-ZAIOS-03 | T1 | ZAIOS | Resultado operacional | v0 | formula | 129558.84 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T1-ZAIOS-04 | T1 | ZAIOS | Ocupação de equilíbrio | v0 | formula | 0.1357 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T1-ZAIOS-05 | T1 | ZAIOS | VPL a 10% | v0 | formula | -103917.01 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T1-ZAIOS-06 | T1 | ZAIOS | TIR | v0 | formula | 0.0724 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T1-ZAIOS-07 | T1 | ZAIOS | Payback simples | v0 | formula | 6.95 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T1-ZAIOS-08 | T1 | ZAIOS | Payback descontado (não ocorre em 10 anos) | v0 | formula | — | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T1-ZAIOS-09 | T1 | ZAIOS | Retorno anual sobre o investimento | D1 | formula | 0.144 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T1-ZAIOS-10 | T1 | ZAIOS | Retorno acumulado em 10 anos | D1 | divergencia | 0.4395 | — | NÃO EXECUTADO (dependência ausente) | A ZAIOS não calcula o retorno acumulado (aderência parcial à D1). |
| T1-B08-01 | T1 | B08 | Receita bruta/ano | v0 | formula | 282948 | 282948 | OK |  |
| T1-B08-02 | T1 | B08 | Receita real | v0 | formula | 234846.84 | 234846.84 | OK |  |
| T1-B08-03 | T1 | B08 | Resultado operacional | v0 | formula | 129558.84 | 129558.84 | OK |  |
| T1-B08-04 | T1 | B08 | Ocupação de equilíbrio | v0 | formula | 0.1357 | 0.135742 | OK |  |
| T1-B08-05 | T1 | B08 | VPL a 10% | v0 | formula | -103917.01 | -103917.013483 | OK |  |
| T1-B08-06 | T1 | B08 | TIR | v0 | formula | 0.0724 | 0.07239 | OK |  |
| T1-B08-07 | T1 | B08 | Payback simples | v0 | formula | 6.95 | 6.946651 | OK |  |
| T1-B08-08 | T1 | B08 | Payback descontado (não ocorre em 10 anos) | v0 | formula | — | — | OK |  |
| T1-B08-09 | T1 | B08 | Retorno anual (valor) | D1 | formula | 0.144 | 0.143954 | OK |  |
| T1-B08-10 | T1 | B08 | Retorno acumulado em 10 anos (valor) | D1 | formula | 0.4395 | 0.439543 | OK |  |
| T1-A09-01 | T1 | A09 | Receita bruta/ano (365 dias) | v0 | formula | 282948 | 282948 | OK |  |
| T1-A09-02 | T1 | A09 | Receita real | v0 | formula | 234846.84 | 234846.84 | OK |  |
| T1-A09-03 | T1 | A09 | Resultado operacional | v0 | formula | 129558.84 | 129558.84 | OK |  |
| T1-A09-04 | T1 | A09 | Ocupação de equilíbrio | v0 | formula | 0.1357 | 0.135742 | OK |  |
| T1-A09-05 | T1 | A09 | Payback (simplificado, sem rampa) | v0 | formula | 6.95 | 6.946651 | OK |  |
| T1-A09-06 | T1 | A09 | Retorno anual (valor) | D1 | formula | 0.144 | 0.143954 | OK |  |
| T1-A09-07 | T1 | A09 | Receita bruta/ano com o campo como a interface permite (30 noites × 12) | D5 (pendente) | limitacao | 282948 | 279072 | LIMITAÇÃO CONFIRMADA (decisão pendente) | O campo de noites por mês é inteiro: 360 dias no máximo. |
| T2-ZAIOS-S1 | T2 | ZAIOS | Resultado operacional (regime) (sem rampa) | v0 | formula | 126729.36 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-S2 | T2 | ZAIOS | Geração de caixa (regime) (sem rampa) | v0 | formula | 118240.92 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-S3 | T2 | ZAIOS | Geração do 1º ano (sem rampa) | v0 | formula | 118240.92 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-S4 | T2 | ZAIOS | VPL a 10% (sem rampa) | v0 | formula | -173460.73 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-S5 | T2 | ZAIOS | TIR (sem rampa) | v0 | formula | 0.053 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-S6 | T2 | ZAIOS | Payback simples (sem rampa) | v0 | formula | 7.61 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-S7 | T2 | ZAIOS | VPL com saída 6× EBITDA (sem rampa) | v0 | formula | 119697.19 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-R1 | T2 | ZAIOS | Resultado operacional (regime) (com rampa) | v0 | formula | 126729.36 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-R2 | T2 | ZAIOS | Geração de caixa (regime) (com rampa) | v0 | formula | 118240.92 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-R3 | T2 | ZAIOS | Geração do 1º ano (com rampa) | v0 | formula | 42405.16 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-R4 | T2 | ZAIOS | VPL a 10% (com rampa) | v0 | formula | -242402.34 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-R5 | T2 | ZAIOS | TIR (com rampa) | v0 | formula | 0.0371 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-R6 | T2 | ZAIOS | Payback simples (com rampa) | v0 | formula | 8.25 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T2-ZAIOS-R7 | T2 | ZAIOS | VPL com saída 6× EBITDA (com rampa) | v0 | formula | 50755.59 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F01-01 | T3 | ZAIOS | F01 · CAPEX com contingência de 25% da base | v0 | formula | 1237400 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F02-01 | T3 | ZAIOS | F02 · Receita real | v0 | formula | 234846.84 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F02-02 | T3 | ZAIOS | F02 · Resultado operacional | v0 | formula | 108846.84 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F02-03 | T3 | ZAIOS | F02 · Equilíbrio em noites | v0 | formula | 223.25 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F02-04 | T3 | ZAIOS | F02 · Ocupação de equilíbrio (20,4%) | v0 | formula | 0.204 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F03-C1-1 | T3 | ZAIOS | F03 caso 1 · VPL a 10% | v0 | formula | -1110447.78 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F03-C1-2 | T3 | ZAIOS | F03 caso 1 · Payback simples estendido (38,6 anos) | v0 | formula | 38.6 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F03-C1-3 | T3 | ZAIOS | F03 caso 1 · TIR com saída 6× (−8,4%) | v0 | formula | -0.084 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F03-C2-1 | T3 | ZAIOS | F03 caso 2 · Payback simples | v0 | formula | 5.75 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F03-C2-2 | T3 | ZAIOS | F03 caso 2 · Payback descontado | v0 | formula | 8.82 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F03-C2-3 | T3 | ZAIOS | F03 caso 2 · VPL sem saída | v0 | formula | 92549.78 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T3-F03-C2-4 | T3 | ZAIOS | F03 caso 2 · VPL com saída 6× | v0 | formula | 624599.52 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T4-B06-01 | T4 | B06 | CAPEX (perfil oficial iniciante) | v0 | formula | 449500 | 449500 | OK |  |
| T4-B06-02 | T4 | B06 | Cenário intermediário (perfil iniciante) | v0 | formula | 524450 | 524450 | OK |  |
| T4-B06-03 | T4 | B06 | Cenário conservador (perfil iniciante) | v0 | formula | 598617.5 | 598617.5 | OK |  |
| T4-B06-04 | T4 | B06 | Contingência fora do capital de giro (intermediário − giro = CAPEX × (1 + contingência)) | v0 | formula | 0 | -0 | OK |  |
| T4-B06-05 | T4 | B06 | Contingência sobre as linhas do F01 (base ZAIOS: infra + obra + apoio = 182.500) | D6 (pendente) | limitacao | 182500 | 263725 | LIMITAÇÃO CONFIRMADA (decisão pendente) | O B06 aplica a contingência sobre todo o CAPEX (inclui projeto e equipamentos). |
| T4-F05-01 | T4 | F05 | Subtotal do exemplo | v0 | formula | 197040 | 197040 | OK |  |
| T4-F05-02 | T4 | F05 | Reserva para imprevistos (contingência) do exemplo | v0 | formula | 19704 | 19704 | OK |  |
| T4-F05-03 | T4 | F05 | Total com reserva do exemplo | v0 | formula | 216744 | 216744 | OK |  |
| T5-J2-01 | T5 | Folha J2 | Receita real − custos variáveis = margem de contribuição | v0 | formula | 0 | 0 | OK |  |
| T5-J2-02 | T5 | Folha J2 | Margem de contribuição − fixos = resultado operacional | v0 | formula | 0 | 0 | OK |  |
| T5-J2-03 | T5 | Folha J2 | Resultado operacional − custos do modelo = EBITDA | v0 | formula | 0 | 0 | OK |  |
| T5-J2-04 | T5 | Folha J2 | EBITDA − reserva de reposição = geração de caixa | v0 | formula | 0 | 0 | OK |  |
| T5-J2-05 | T5 | Folha J2 × ZAIOS | Pró-labore 20 h × R$ 40 × 4,33 igual nas duas | D4 | formula | 0 | — | NÃO EXECUTADO (dependência ausente) | Precisa da Folha J2 e da ZAIOS. |
| T6-ZAIOS-01 | T6 | ZAIOS | TIR inexistente quando o fluxo não muda de sinal | v0 | formula | — | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T6-ZAIOS-02 | T6 | ZAIOS | Aviso de mais de uma TIR com duas trocas de sinal | v0 | formula | true | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T6-ZAIOS-03 | T6 | ZAIOS | Payback acima do horizonte marcado como estendido | v0 | formula | true | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T6-ZAIOS-04 | T6 | ZAIOS | Sem equilíbrio quando a diária é menor que o custo variável | v0 | formula | — | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T6-ZAIOS-05 | T6 | ZAIOS | Sem equilíbrio com ocupação 0% | v0 | formula | — | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T6-ZAIOS-06 | T6 | ZAIOS | Geração do regime negativa: não se paga | v0 | formula | — | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T6-B08-01 | T6 | B08 | Payback acima de 10 anos com valor estendido (padrão proposto) | D8 (pendente) | limitacao | número acima de 10 | — | LIMITAÇÃO CONFIRMADA (decisão pendente) | O B08 devolve nulo acima de 10 anos. |
| T7-ZAIOS-01 | T7 | ZAIOS | Conservador · receita bruta (diária 612, ocupação 30,4%) | D11-A | formula | 203722.56 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-02 | T7 | ZAIOS | Conservador · geração de caixa | D11-A | formula | 70459.32 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-03 | T7 | ZAIOS | Valor de saída no ano 10 (6× EBITDA) | D11-A | formula | 777353.04 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-04 | T7 | ZAIOS | Valor presente da saída | D11-A | formula | 299703.25 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-05 | T7 | ZAIOS | VPL com saída | D11-A | formula | 195786.24 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-06 | T7 | ZAIOS | Resultado dos 5 critérios (o 5º não avaliável no T1) | D11-A | formula | [passa, passa, passa, ajustar, nao_avaliado] | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-07 | T7 | ZAIOS | Borda · payback de 8,00 anos passa | D11-A | formula | passa | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-08 | T7 | ZAIOS | Borda · payback de 12,00 anos pede ajuste | D11-A | formula | ajustar | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-09 | T7 | ZAIOS | Borda · payback acima de 12 pede redesenho | D11-A | formula | redesenhar | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-10 | T7 | ZAIOS | Borda · colchão de 10% passa | D11-A | formula | passa | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-11 | T7 | ZAIOS | Borda · déficit igual a 3 × fixo pede ajuste | D11-A | formula | ajustar | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-12 | T7 | ZAIOS | Borda · déficit acima de 3 × fixo pede redesenho | D11-A | formula | redesenhar | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-13 | T7 | ZAIOS | Leitura: um 'redesenhar' dá Redesenhar; só 'ajustar' dá Ajustar; tudo 'passa' dá Avançar | D11-A | formula | [Redesenhar, Ajustar, Avançar] | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T7-ZAIOS-14 | T7 | ZAIOS | Apresentação com 4 de 5 critérios: sinal parcial, sem veredito | D11-A | divergencia | 4 de 5 critérios avaliados. Sinal parcial, não representa aprovação do projeto. | — | NÃO EXECUTADO (dependência ausente) | A ZAIOS calcula o veredito com qualquer quantidade de passos e não tem trava de homologação. |
| T7-B08-01 | T7 | B08 | Mostra 'X de 5 critérios avaliados. Sinal parcial…' | D11-A | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T7-A09-01 | T7 | A09 | Mostra 'X de 5 critérios avaliados. Sinal parcial…' | D11-A | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T7-A09-02 | T7 | A09 | Metas pessoais (prazo e retorno desejados) em bloco separado da Régua Zion | D11-A | divergencia | true | false | DIVERGÊNCIA CONFIRMADA | Hoje os avisos de meta aparecem misturados aos demais. |
| T8-B08-01 | T8 | B08 | Quebra e perdas: campo próprio ou rótulo 'Resultado antes de quebra e perdas' | D3-A | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T8-B08-02 | T8 | B08 | Pró-labore: campo próprio ou rótulo 'Resultado antes do seu pró-labore' | D4 | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T8-B08-03 | T8 | B08 | Sem 'ROI' sem qualificador (usa 'retorno anual' / 'retorno acumulado em 10 anos') | D1 | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T8-A09-01 | T8 | A09 | Quebra e perdas: campo próprio ou rótulo 'Resultado antes de quebra e perdas' | D3-A | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T8-A09-02 | T8 | A09 | Pró-labore: campo próprio ou rótulo 'Resultado antes do seu pró-labore' | D4 | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T8-A09-03 | T8 | A09 | Sem 'ROI' sem qualificador (usa 'retorno anual' / 'retorno acumulado em 10 anos') | D1 | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T8-A09-04 | T8 | A09 | Reserva de reposição: campo próprio ou rótulo 'Antes da reserva de reposição' | D2-C | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T8-B08-04 | T8 | B08 | Valor de saída com método identificado (múltiplo do EBITDA, avaliação patrimonial ou valor informado) | D7-C | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T9-ZAIOS-01 | T9 | ZAIOS | Deduções (17%) sem quebra nem reserva | v0 | formula | 48101.16 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T9-ZAIOS-02 | T9 | ZAIOS | Quebra de 1% como custo variável | D3-A | formula | 2829.48 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T9-ZAIOS-03 | T9 | ZAIOS | Resultado operacional com quebra | D3-A | formula | 126729.36 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T9-ZAIOS-04 | T9 | ZAIOS | Reserva de 4% da receita bruta (informada) abaixo do EBITDA | D2-C | formula | 11317.92 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T9-ZAIOS-05 | T9 | ZAIOS | Geração de caixa (a cascata fecha, reserva sai uma vez) | D2-C | formula | 115411.44 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T9-ZAIOS-06 | T9 | ZAIOS | Referência da reserva de reposição = 4% | D2-C | divergencia | 0.04 | — | NÃO EXECUTADO (dependência ausente) | A ZAIOS usa 3% (REF_RESERVA). |
| T9-ZAIOS-07 | T9 | ZAIOS | Faixa da reserva de reposição = 3% a 6% | D2-C | divergencia | [0.03, 0.06] | — | NÃO EXECUTADO (dependência ausente) | A ZAIOS usa 3% a 5% (RESERVA_FAIXA). Achado novo deste comando. |
| T9-ZAIOS-08 | T9 | ZAIOS | Aceita quebra medida em R$ (prioridade ao valor real) | D3-A | divergencia | true | — | NÃO EXECUTADO (dependência ausente) | O P6 só aceita a quebra em percentual. |
| T9-J2-01 | T9 | Folha J2 | Referência da reserva = 4%, faixa 3% a 6% | D2-C | formula | [4, 3, 6] | [4, 3, 6] | OK |  |
| T9-J2-02 | T9 | Folha J2 | Reserva = 4% da receita bruta realizada (exemplo: 4% × 17.220,00 = 688,80) | D2-C | divergencia | 688.8 | 542.624 | DIVERGÊNCIA CONFIRMADA | A Folha aplica 4% sobre a receita real (542,62). |
| T9-J2-03 | T9 | Folha J2 | Quebra sem medição = 1% da receita de hospedagem (162,40) | D3-A | formula | 162.4 | 162.4 | OK |  |
| T9-J2-04 | T9 | Folha J2 | Quebra medida em R$ tem prioridade (informada 150,00) | D3-A | formula | 150 | 150 | OK |  |
| T9-J2-05 | T9 | Folha J2 | Deduções não contêm quebra (650 + 18,5% × 16.240 = 3.654,40) | D3-A | formula | 3654.4 | 3654.4 | OK |  |
| T9-B08-01 | T9 | B08 | Reserva de 4% fora das deduções (deduções continuam 48.101,16) | D2-C | divergencia | 48101.16 | 59419.08 | DIVERGÊNCIA CONFIRMADA | O B08 soma a reserva às deduções. |
| T9-B08-02 | T9 | B08 | Quebra como custo variável disponível | D3-A | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T9-A09-01 | T9 | A09 | Quebra como custo variável disponível | D3-A | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T10-ZAIOS-01 | T10 | ZAIOS | Pró-labore 20 h × R$ 40 × 4,33 por mês | D4 | formula | 3464 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T10-ZAIOS-02 | T10 | ZAIOS | Pró-labore por ano | D4 | formula | 41568 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T10-ZAIOS-03 | T10 | ZAIOS | Resultado operacional do T1 com pró-labore como custo fixo | D4 | formula | 87990.84 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T10-ZAIOS-04 | T10 | ZAIOS | Distribuição de resultados e caixa disponível separados do resultado | D4 | divergencia | true | — | NÃO EXECUTADO (dependência ausente) | A ZAIOS não tem distribuição nem caixa disponível. |
| T10-J2-01 | T10 | Folha J2 | Pró-labore do exemplo (20 h × R$ 40 × 4,33) | D4 | formula | 3464 | 3464 | OK |  |
| T10-J2-02 | T10 | Folha J2 | Distribuição de resultados com nome próprio, fora do resultado | D4 | divergencia | true | false | DIVERGÊNCIA CONFIRMADA | A Folha tem pró-labore e bloco de caixa, mas não nomeia a distribuição. |
| T11-ZAIOS-01 | T11 | ZAIOS | Método 1 · 6× EBITDA de 129.558,84 | D7-C | formula | 777353.04 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| T11-ZAIOS-02 | T11 | ZAIOS | Métodos 2 e 3 (avaliação patrimonial, valor informado) e valor líquido de custos, tributos e obrigações | D7-C | divergencia | true | — | NÃO EXECUTADO (dependência ausente) | A ZAIOS só tem o múltiplo do EBITDA. |
| T11-ZAIOS-03 | T11 | ZAIOS | Valor líquido com custo de venda ilustrativo de 6% (antes de tributos) | D7-C | divergencia | 730711.86 | — | NÃO EXECUTADO (dependência ausente) | Sem função de valor líquido; o custo de 6% é ilustrativo. |
| T11-B08-01 | T11 | B08 | Saída aceita múltiplo do EBITDA (residual hoje em % do investimento, até 100%) | D7-C | divergencia | true | false | DIVERGÊNCIA CONFIRMADA |  |
| T12-01 | T12 | todas | Deduções sobre a receita | v0 | economico | 0.17 | Folha J2: 0.17 | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-02 | T12 | todas | Quebra e perdas | D3-A | economico | 0.01 | Folha J2: 0.01 | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-03 | T12 | todas | Reserva de reposição | D2-C | economico | 0.04 (faixa [0.03, 0.06]) | Folha J2: 0.04 | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-04 | T12 | todas | Valor da hora do pró-labore (R$) | D4 | economico | 40 | Folha J2 (exemplo): 40 | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-05 | T12 | todas | Rampa do 1º ano (meses 1–3, 4–6, 7–12) | v0 | economico | [0.4, 0.5, 0.75] | — | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-06 | T12 | todas | OS&E sobre FF&E | v0 | economico | 0.12 (faixa [0.1, 0.15]) | — | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-07 | T12 | todas | Pré-abertura sobre a base | v0 | economico | 0.05 (faixa [0.05, 0.1]) | — | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-08 | T12 | todas | Contingência primeira obra | v0 | economico | [0.2, 0.25] | — | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-09 | T12 | todas | Contingência com experiência | v0 | economico | [0.1, 0.15] | — | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-10 | T12 | todas | Cenário conservador (diária, ocupação) | D10 pendente | economico | [-0.1, -0.2] | — | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-11 | T12 | todas | Cenário otimista (diária, ocupação) | D10 pendente | economico | [0.1, 0.15] | — | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-12 | T12 | todas | Múltiplo de saída (método 1) | D7-C | economico | 6 | — | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-13 | T12 | todas | Régua: payback passa / ajustar (anos) | D11-A | economico | [8, 12] | — | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-14 | T12 | todas | Régua: colchão mínimo sobre o CAPEX | D11-A | economico | 0.1 | — | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| T12-15 | T12 | todas | Régua: déficit conservador aceito (meses de fixo) | D11-A | economico | 3 | — | PENDENTE DE VALIDAÇÃO ECONÔMICA |  |
| C-B08-R-fc1 | C | B08 | Fluxo do ano 1 (rampa 25%→40% em 3 anos, reajuste 5%, extras 10%) | v0 | formula | 43042.5 | 43042.5 | OK |  |
| C-B08-R-vpl | C | B08 | VPL a 12% | v0 | formula | -502004.793594 | -502004.793594 | OK |  |
| C-B08-R-tir | C | B08 | TIR | v0 | formula | 0.022371 | 0.022371 | OK |  |
| C-B08-R-paybackS | C | B08 | Payback simples | v0 | formula | 9.053656 | 9.053656 | OK |  |
| C-B08-R-paybackD | C | B08 | Payback descontado (não ocorre em 10 anos) | v0 | formula | — | — | OK |  |
| C-B08-R-roi10 | C | B08 | Retorno acumulado em 10 anos (valor) | v0 | formula | 0.150318 | 0.150318 | OK |  |
| C-B08-V-vpl | C | B08 | VPL a 12% com valor residual de 50% | D7-C (método residual) | formula | -308820.85164 | -308820.85164 | OK |  |
| C-B08-V-tir | C | B08 | TIR com valor residual | D7-C (método residual) | formula | 0.071789 | 0.071789 | OK |  |
| C-B08-V-roi10 | C | B08 | Retorno acumulado com residual (valor) | D7-C (método residual) | formula | 0.650318 | 0.650318 | OK |  |
| C-B08-V-paybackS | C | B08 | Payback simples (o residual não entra) | D7-C (método residual) | formula | 9.053656 | 9.053656 | OK |  |
| C-B08-E-1 | C | B08 | Ocupação de equilíbrio sem reserva | v0 | formula | 0.135742 | 0.135742 | OK |  |
| C-B08-E-2 | C | B08 | Ocupação de equilíbrio com reserva de 4%, pela regra aprovada (reserva fora das deduções não muda o equilíbrio) | D2-C (O3) | divergencia | 0.135742 | 0.143818 | DIVERGÊNCIA CONFIRMADA | O B08 trata a reserva como dedução e eleva o equilíbrio. |
| C-B08-E-3 | C | B08 | Ocupação de equilíbrio com reserva de 4% como dedução (conferência da conta atual) | v0 | formula | 0.143818 | 0.143818 | OK |  |
| C-A09-P-1 | C | A09 | Investimento total com contingência de 10% | v0 | formula | 748000 | 748000 | OK |  |
| C-A09-P-recBruta | C | A09 | Receita bruta com extras de R$ 1.000/mês | v0 | formula | 190200 | 190200 | OK |  |
| C-A09-P-ded | C | A09 | Deduções (comissão 12% + imposto 6% + gestão 10%) | v0 | formula | 53256 | 53256 | OK |  |
| C-A09-P-resultado | C | A09 | Resultado do ano | v0 | formula | 21504 | 21504 | OK |  |
| C-A09-P-roi | C | A09 | Retorno anual (valor) | v0 | formula | 0.028749 | 0.028749 | OK |  |
| C-A09-P-payback | C | A09 | Payback simplificado (34,8 anos, sem limite) | v0 | formula | 34.784226 | 34.784226 | OK |  |
| C-A09-G-1 | C | A09 | Resultado operacional antes da taxa de gestão (dicionário: gestão é custo do modelo) | O2 (a classificar) | limitacao | 40524 | 21504 | LIMITAÇÃO CONFIRMADA (decisão pendente) | O A09 desconta a gestão nas deduções; o 'resultado' equivale a um EBITDA. |
| C-A09-D-1 | C | A09 | Receita com o máximo do campo (31 noites × 12 = 372 dias) igual à de 365 dias | D5 (pendente) | limitacao | 282948 | 288374.4 | LIMITAÇÃO CONFIRMADA (decisão pendente) | Com 31 noites/mês o ano tem 372 dias; com 30, 360. |
| C-A09-D-2 | C | A09 | Conferência: 31 × 12 noites calculam como definido | v0 | formula | 288374.4 | 288374.4 | OK |  |
| C-B06-iniciante-capex | C | B06 | CAPEX · perfil iniciante | v0 | formula | 449500 | 449500 | OK |  |
| C-B06-iniciante-inter | C | B06 | Cenário intermediário (contingência fora do giro) · perfil iniciante | v0 | formula | 524450 | 524450 | OK |  |
| C-B06-iniciante-cons | C | B06 | Cenário conservador (variação × contingência) · perfil iniciante | v0 | formula | 598617.5 | 598617.5 | OK |  |
| C-B06-iniciante-giro | C | B06 | Capital de giro (fixo × meses) · perfil iniciante | v0 | formula | 30000 | 30000 | OK |  |
| C-B06-iniciante-desembMes | C | B06 | Desembolso mensal · perfil iniciante | v0 | formula | 61806.25 | 61806.25 | OK |  |
| C-B06-iniciante-m2 | C | B06 | Custo por m² da unidade · perfil iniciante | v0 | formula | 4000 | 4000 | OK |  |
| C-B06-intermediario-capex | C | B06 | CAPEX · perfil intermediario | v0 | formula | 722000 | 722000 | OK |  |
| C-B06-intermediario-inter | C | B06 | Cenário intermediário (contingência fora do giro) · perfil intermediario | v0 | formula | 844640 | 844640 | OK |  |
| C-B06-intermediario-cons | C | B06 | Cenário conservador (variação × contingência) · perfil intermediario | v0 | formula | 1006368 | 1006368 | OK |  |
| C-B06-intermediario-giro | C | B06 | Capital de giro (fixo × meses) · perfil intermediario | v0 | formula | 36000 | 36000 | OK |  |
| C-B06-intermediario-desembMes | C | B06 | Desembolso mensal · perfil intermediario | v0 | formula | 80864 | 80864 | OK |  |
| C-B06-intermediario-m2 | C | B06 | Custo por m² da unidade · perfil intermediario | v0 | formula | 3607.142857 | 3607.142857 | OK |  |
| C-B06-incompleto-extremo-capex | C | B06 | CAPEX · perfil incompleto-extremo | v0 | formula | 52000 | 52000 | OK |  |
| C-B06-incompleto-extremo-inter | C | B06 | Cenário intermediário (contingência fora do giro) · perfil incompleto-extremo | v0 | formula | 52000 | 52000 | OK |  |
| C-B06-incompleto-extremo-cons | C | B06 | Cenário conservador (variação × contingência) · perfil incompleto-extremo | v0 | formula | 52000 | 52000 | OK |  |
| C-B06-incompleto-extremo-giro | C | B06 | Capital de giro (fixo × meses) · perfil incompleto-extremo | v0 | formula | 0 | 0 | OK |  |
| C-B06-incompleto-extremo-desembMes | C | B06 | Desembolso mensal · perfil incompleto-extremo | v0 | formula | 52000 | 52000 | OK |  |
| C-F05-1 | C | F05 | Diferença verba − total (exemplo) | v0 | formula | -16744 | -16744 | OK |  |
| C-F05-2 | C | F05 | Custo por m² de área interna (exemplo) | v0 | formula | 7224.8 | 7224.8 | OK |  |
| C-F05-3 | C | F05 | Custo por m² de área total, interna + deck (exemplo) | v0 | formula | 5160.571429 | 5160.571429 | OK |  |
| C-F05-4 | C | F05 | Versão em branco: subtotal zero e leitura de espera | v0 | formula | [0, Ainda não há itens com cotação] | [0, Ainda não há itens com cotação] | OK |  |
| C-J2-I-noitesDisponiveis | C | Folha J2 | Noites disponíveis (4 × 31) | v0 | formula | 124 | 124 | OK |  |
| C-J2-I-ocupacao | C | Folha J2 | Ocupação | v0 | formula | 0.467742 | 0.467742 | OK |  |
| C-J2-I-diariaMediaBruta | C | Folha J2 | Diária média bruta | v0 | formula | 280 | 280 | OK |  |
| C-J2-I-margemPorNoite | C | Folha J2 | Margem por noite | v0 | formula | 188.675862 | 188.675862 | OK |  |
| C-J2-I-pontoEquilibrioNoites | C | Folha J2 | Ponto de equilíbrio (noites) | v0 | formula | 35.372834 | 35.372834 | OK |  |
| C-J2-I-saldoFinal | C | Folha J2 | Saldo final do caixa | v0 | formula | 13620 | 13620 | OK |  |
| C-J2-I-mesesFolego | C | Folha J2 | Meses de fôlego | v0 | formula | 1.882776 | 1.882776 | OK |  |
| C-J2-M-custosModelo | C | Folha J2 | Custos do modelo (aluguel 800 + gestão 1.200 + marca 300) | v0 | formula | 2300 | 2300 | OK |  |
| C-J2-M-ebitda | C | Folha J2 | EBITDA com custos do modelo | v0 | formula | 1969.2 | 1969.2 | OK |  |
| C-J2-M-geracaoCaixa | C | Folha J2 | Geração de caixa com custos do modelo | v0 | formula | 1426.576 | 1426.576 | OK |  |
| C-J2-M-mesesFolego | C | Folha J2 | Meses de fôlego com custos do modelo | v0 | formula | 1.428571 | 1.428571 | OK |  |
| C-J2-M-pontoEquilibrioNoites | C | Folha J2 | Ponto de equilíbrio com custos do modelo | v0 | formula | 47.563053 | 47.563053 | OK |  |
| C-ZAIOS-M-custosModelo | C | ZAIOS | Custos do modelo (aluguel R$ 1.000/mês + gestão 10% + royalty 3%) | v0 | formula | 48783.24 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| C-ZAIOS-M-ebitda | C | ZAIOS | EBITDA com custos do modelo | v0 | formula | 77946.12 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| C-ZAIOS-M-geracaoCaixa | C | ZAIOS | Geração de caixa com custos do modelo e reserva de 4% | v0 | formula | 66628.2 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| C-ZAIOS-M-resultadoOperacional | C | ZAIOS | Resultado operacional (antes dos custos do modelo) | v0 | formula | 126729.36 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| C-ZAIOS-O-receitaBruta | C | ZAIOS | Receita bruta com outras receitas de 10% | v0 | formula | 311242.8 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| C-ZAIOS-O-custosVariaveis | C | ZAIOS | Custos variáveis com custo por estadia (R$ 60, permanência 2,5) | v0 | formula | 43274.4 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| C-ZAIOS-O-resultadoOperacional | C | ZAIOS | Resultado operacional com outras receitas e estadia | v0 | formula | 143057.124 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| C-ZAIOS-S-1 | C | ZAIOS | Receita bruta com sazonalidade (alta dez–fev, baixa abr–jun) | v0 | formula | 315736.8 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| C-ZAIOS-S-2 | C | ZAIOS | Resultado operacional com sazonalidade | v0 | formula | 155952.744 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| C-ZAIOS-C-mesAberturaProjeto | C | ZAIOS (composição) | Mês de abertura sugerido pelo cronograma do P5 | v0 | formula | 10 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-geracaoAno1 | C | ZAIOS (composição) | Geração do 1º ano (rampa a partir de janeiro) | v0 | formula | 15229.812 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-geracaoRegime | C | ZAIOS (composição) | Geração do ano de regime | v0 | formula | 108846.84 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-giro | C | ZAIOS (composição) | Capital de giro recomendado (o maior entre A = 6 × fixo e B) | v0 | formula | 63000 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-captacao | C | ZAIOS (composição) | Captação = CAPEX + capital de giro | v0 | formula | 1300400 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-retorno | C | ZAIOS (composição) | Retorno anual sobre o investimento | v0 | formula | 0.087964 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-vplSem | C | ZAIOS (composição) | VPL sem saída a 10% | v0 | formula | -653689.676467 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-vplCom | C | ZAIOS (composição) | VPL com saída 6× EBITDA | v0 | formula | -401898.664041 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-payback | C | ZAIOS (composição) | Payback simples (estendido) | v0 | formula | 12.228348 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-conservador | C | ZAIOS (composição) | Geração do regime no cenário conservador | v0 | formula | 43089.7248 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-estresseReceita | C | ZAIOS (composição) | Estresse: geração com receita 30% menor | v0 | formula | 23962.44 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-capexMaior | C | ZAIOS (composição) | Estresse: CAPEX 25% maior | v0 | formula | 1546750 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-menorSaldo | C | ZAIOS (composição) | Menor saldo da curva de caixa com a contingência usada | v0 | formula | 52438.404 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-colchao | C | ZAIOS (composição) | Colchão = menor saldo ÷ CAPEX | v0 | formula | 0.042378 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-passos | C | ZAIOS (composição) | Resultado dos 5 passos | D11-A (lógica) | formula | [passa, passa, redesenhar, redesenhar, ajustar] | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-decisao | C | ZAIOS (composição) | Decisão pela regra dos 5 passos | D11-A (lógica) | formula | Redesenhar | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-ZAIOS-C-veredito | C | ZAIOS (composição) | Veredito só após homologação (o selo hoje é exibido) | D11-A | divergencia | sem selo antes da homologação | — | NÃO EXECUTADO (dependência ausente) | calcularViabilidade devolve o selo Avançar/Ajustar/Redesenhar sem trava de homologação. |
| C-G2-receitaBruta | C | ZAIOS (G2) | G2 · Receita bruta (centavos) | v0 | formula | 130000 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G2-comissoes | C | ZAIOS (G2) | G2 · Comissões (centavos) | v0 | formula | 13000 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G2-receitaLiquida | C | ZAIOS (G2) | G2 · Receita líquida de distribuição (centavos) | v0 | formula | 117000 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G2-fixas | C | ZAIOS (G2) | G2 · Despesas fixas (centavos) | v0 | formula | 30000 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G2-variaveis | C | ZAIOS (G2) | G2 · Despesas variáveis sem comissões (centavos) | v0 | formula | 7000 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G2-despesas | C | ZAIOS (G2) | G2 · Despesas totais (centavos) | v0 | formula | 50000 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G2-resultado | C | ZAIOS (G2) | G2 · Resultado gerencial (centavos) | v0 | formula | 80000 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G2-margem | C | ZAIOS (G2) | G2 · Margem gerencial (80.000 ÷ 130.000) | v0 | formula | 0.615385 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G2-cobertura | C | ZAIOS (G2) | G2 · Cobertura da reserva (90.000 ÷ média de 20.000, 30.000, 40.000) | v0 (D12 pendente) | formula | 3 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G3-noitesDisponiveis | C | ZAIOS (G3) | G3 · Noites disponíveis (2 × 30) | v0 | formula | 60 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G3-ocupacao | C | ZAIOS (G3) | G3 · Ocupação (20 ÷ 60) | v0 | formula | 0.333333 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G3-diariaMedia | C | ZAIOS (G3) | G3 · Diária média (hospedagem 100.000 ÷ 20, sem taxa de limpeza) | v0 | formula | 5000 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G3-revpar | C | ZAIOS (G3) | G3 · RevPAR (100.000 ÷ 60) | v0 | formula | 1666.666667 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G3-trevpar | C | ZAIOS (G3) | G3 · TRevPAR (130.000 ÷ 60) | v0 | formula | 2166.666667 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G3-despesaPorNoite | C | ZAIOS (G3) | G3 · Despesa por noite vendida (50.000 ÷ 20) | v0 | formula | 2500 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G3-bissexto | C | ZAIOS (G3) | Dias de fevereiro de 2028 (ano bissexto) | v0 | formula | 29 | — | NÃO EXECUTADO (dependência ausente) | Variável ZAIOS_SRC_DIR não definida ou sem pasta src/ (cópia local da raiz do projeto ZAIOS). |
| C-G2-impostos | C | ZAIOS (G2) | Impostos sobre a receita tratados como dedução (dicionário), não como despesa variável | O7 (a classificar) | limitacao | deducao | — | NÃO EXECUTADO (dependência ausente) | Na G2 a categoria 'impostos' tem natureza variável. |
