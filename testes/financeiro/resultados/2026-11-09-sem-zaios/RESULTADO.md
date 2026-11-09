# Resultado da suíte de homologação financeira (T1 a T12)

Gerado em 2026-11-09T03:51:43.659Z · Plano: PLANO_TESTES_HOMOLOGACAO.md v0.2 (09/11/2026) · Dicionário: DICIONARIO_FINANCEIRO.md v0.4 (09/11/2026)

**Nada foi homologado por esta execução.** OK significa só que a fórmula reproduz o valor esperado do plano.

## Dependências

| Dependência | Disponível | Observação |
|---|---|---|
| zaios | não | Variável ZAIOS_CALC_DIR não definida (cópia local de src/calc da ZAIOS). |
| arsenal | sim |  |
| folha | sim |  |
| folha+zaios | não | Precisa da Folha J2 e da ZAIOS. |
| f05 | sim |  |

## Contagem

| Status | Casos |
|---|---|
| NÃO EXECUTADO (dependência ausente) | 72 |
| OK | 32 |
| LIMITAÇÃO CONFIRMADA (decisão pendente) | 3 |
| DIVERGÊNCIA CONFIRMADA | 17 |
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
