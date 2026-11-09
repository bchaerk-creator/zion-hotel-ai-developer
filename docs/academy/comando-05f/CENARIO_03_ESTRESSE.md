# Cenário 3 · Maior porte e estresse financeiro

Comando 05F · 09/11/2026 · Valores **exclusivamente de teste**, não são parâmetros comerciais aprovados da Zion. Execução local da cópia da ZAIOS (commit `ec21ad5`), sem alterar nada.

Execução base (C3) e uma segunda execução do mesmo cenário com estresse (C3E): ocupação −20% (62% → 49,6%), diária −10% (R$ 950 → R$ 855), custos fixos +15% (R$ 95.000 → R$ 109.250, também no P5) e custo por estadia +10% (R$ 160 → R$ 176). O resto ficou constante: outras receitas mantidas em R$ 480.000, com o `outras_pct` recalculado. **Não é um quarto cenário.** Abertura em outubro.

## Entradas · C3

| Dado | Valor de teste | Como entrou na ZAIOS |
|---|---|---|
| Unidades | 20 | `unidades` = 20 |
| Diária média | R$ 950,00 | `diaria_*` em centavos |
| Ocupação média anual | 62,0% | `ocupacao_*` |
| Dias operacionais | 365 | Calendário fixo de 365 dias da ZAIOS |
| Outras receitas anuais | R$ 480.000,00 | `outras_pct` = 0,11163570 (outras ÷ diárias do regime) |
| Custo variável por estadia | R$ 160,00 | `custo_estadia` |
| Permanência média | 3,0 noites | `permanencia` |
| Custos fixos mensais | R$ 95.000,00 | `custo_fixo` no P6 e no P5 |
| Aluguel mensal | R$ 30.000,00 | `aluguel` |
| Gestão | 8% da receita de hospedagem | `gestao_pct` (a ZAIOS aplica sobre a receita bruta) |
| Royalties | 5% da receita de hospedagem | `royalty_pct` (idem) |
| Tributos sobre vendas | 12% da receita bruta | `deducoes_pct` |
| Investimento inicial | R$ 6.800.000,00 | 7 linhas do P5 (proporções do plano), contingência 0% |
| Capital de giro inicial | R$ 420.000,00 | Sem campo na ZAIOS: ela calcula o giro recomendado |
| Mês de abertura (adotado) | Outubro | `mes_abertura`; mês do projeto sugerido pelo cronograma |

Outros campos exigidos pela ferramenta (valores adotados e justificativas): `PLANO_TESTES_COMPOSICAO.md`, seção 4.

## Comparação · C3 (72 campos)

Contagem: OK: 62 · DIVERGÊNCIA METODOLÓGICA: 10.

Tolerâncias: R$ 0,01; frações, anos e noites 0,000001. Uma diferença ZAIOS − R2 da ordem de 1e-9 é ruído de ponto flutuante, abaixo da tolerância.

| Grupo | Campo | Esperado independente (regra da ZAIOS, R2) | Esperado pela regra do comando (R1) | Valor ZAIOS | Diferença ZAIOS − R2 | Diferença ZAIOS − R1 | Classificação |
|---|---|---|---|---|---|---|---|
| Receita | Receita de hospedagem | R$ 4.299.700,00 | R$ 4.299.700,00 | R$ 4.299.700,00 | 0 | — | OK |
| Receita | Diárias ocupadas (noites vendidas) | 4.526 | — | 4.526 | 0 | — | OK |
| Receita | Estadias (derivado: custos variáveis ÷ custo por estadia) | 1.508,67 | — | 1.508,67 | 0 | — | OK |
| Receita | Outras receitas | R$ 480.000,00 | R$ 480.000,00 | R$ 480.000,00 | 0 | — | OK |
| Receita | Receita bruta consolidada | R$ 4.779.700,00 | R$ 4.779.700,00 | R$ 4.779.700,00 | 9.3e-10 | — | OK |
| Receita | Ocupação média anual (ponderada pelos dias) | 62,0000% | — | 62,0000% | 0 | — | OK |
| Deduções | Tributos sobre vendas (deduções) | R$ 573.564,00 | R$ 573.564,00 | R$ 573.564,00 | 0 | — | OK |
| Despesas | Custos variáveis | R$ 241.386,67 | R$ 241.386,67 | R$ 241.386,67 | -2.9e-11 | — | OK |
| Despesas | Custos fixos | R$ 1.140.000,00 | R$ 1.140.000,00 | R$ 1.140.000,00 | 0 | — | OK |
| Despesas | Resultado operacional (antes dos custos do modelo) | R$ 2.824.749,33 | — | R$ 2.824.749,33 | -9.3e-10 | — | OK |
| Despesas | Aluguel (12 × mensal) | R$ 360.000,00 | R$ 360.000,00 | R$ 360.000,00 | 0 | — | OK |
| Despesas | Gestão + royalties (derivado: custos do modelo − aluguel) | R$ 621.361,00 | R$ 558.961,00 | R$ 621.361,00 | 0 | R$ 62.400,00 | DIVERGÊNCIA METODOLÓGICA |
| Despesas | Custos do modelo | R$ 981.361,00 | R$ 918.961,00 | R$ 981.361,00 | 0 | R$ 62.400,00 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA e geração | EBITDA do regime | R$ 1.843.388,33 | R$ 1.905.788,33 | R$ 1.843.388,33 | -4.7e-10 | R$ -62.400,00 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA e geração | Geração de caixa do regime | R$ 1.843.388,33 | R$ 1.905.788,33 | R$ 1.843.388,33 | -4.7e-10 | R$ -62.400,00 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA e geração | Receita bruta do 1º ano (rampa) | R$ 2.868.474,75 | — | R$ 2.868.474,75 | -4.7e-10 | — | OK |
| EBITDA e geração | EBITDA do 1º ano | R$ 506.491,00 | — | R$ 506.491,00 | -1.2e-10 | — | OK |
| EBITDA e geração | Geração do 1º ano | R$ 506.491,00 | — | R$ 506.491,00 | -1.2e-10 | — | OK |
| EBITDA e geração | Meses com geração negativa no regime | 0 | — | 0 | 0 | — | OK |
| EBITDA e geração | Pior mês do regime | R$ 131.479,11 | — | R$ 131.479,11 | -2.9e-11 | — | OK |
| EBITDA e geração | Margem operacional (antes dos custos do modelo) | 59,0989% | — | 59,0989% | -2.2e-16 | — | OK |
| EBITDA e geração | Régua de margem do P6 | boa | — | boa | — | — | OK |
| EBITDA e geração | Selo do P6 Receitas | Avançar | — | Avançar | — | — | OK |
| EBITDA e geração | Equilíbrio: contribuição por noite | R$ 738,71 | — | R$ 738,71 | 0 | — | OK |
| EBITDA e geração | Equilíbrio: noites/ano | 2.030,57 | — | 2.030,57 | 0 | — | OK |
| EBITDA e geração | Equilíbrio: ocupação | 27,8161% | — | 27,8161% | 0 | — | OK |
| EBITDA e geração | Equilíbrio: folga de ocupação | 34,1839% | — | 34,1839% | 0 | — | OK |
| Capital e fluxo de caixa | Capital investido (CAPEX) | R$ 6.800.000,00 | — | R$ 6.800.000,00 | 0 | — | OK |
| Capital e fluxo de caixa | Déficit acumulado da rampa | R$ 37.913,18 | — | R$ 37.913,18 | -1.5e-11 | — | OK |
| Capital e fluxo de caixa | Soma dos meses negativos do regime (giro) | R$ 0,00 | — | R$ 0,00 | 0 | — | OK |
| Capital e fluxo de caixa | Capital de giro A (6 × fixo) | R$ 570.000,00 | — | R$ 570.000,00 | 0 | — | OK |
| Capital e fluxo de caixa | Capital de giro B | R$ 322.913,18 | — | R$ 322.913,18 | 0 | — | OK |
| Capital e fluxo de caixa | Capital de giro usado | R$ 570.000,00 | R$ 420.000,00 | R$ 570.000,00 | 0 | R$ 150.000,00 | DIVERGÊNCIA METODOLÓGICA |
| Capital e fluxo de caixa | Captação (CAPEX + giro) | R$ 7.370.000,00 | R$ 7.220.000,00 | R$ 7.370.000,00 | 0 | R$ 150.000,00 | DIVERGÊNCIA METODOLÓGICA |
| Capital e fluxo de caixa | Mês do projeto em que abre | 10 | — | 10 | 0 | — | OK |
| Capital e fluxo de caixa | Menor saldo da curva (36 meses) | R$ 532.086,82 | — | R$ 532.086,82 | -1.2e-10 | — | OK |
| Capital e fluxo de caixa | Mês do menor saldo | 12 | — | 12 | 0 | — | OK |
| Capital e fluxo de caixa | Saldo no mês 36 | R$ 3.387.596,39 | — | R$ 3.387.596,39 | -2.3e-09 | — | OK |
| Capital e fluxo de caixa | Colchão (menor saldo ÷ CAPEX) | 7,8248% | — | 7,8248% | -1.4e-17 | — | OK |
| Capital e fluxo de caixa | Menor saldo com atraso de 6 meses | R$ 528.422,84 | — | R$ 528.422,84 | -1.2e-10 | — | OK |
| Indicadores | Retorno anual (geração ÷ CAPEX) | 27,1087% | 28,0263% | 27,1087% | -1.1e-16 | -0,9176% | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Retorno do EBITDA | 27,1087% | — | 27,1087% | -1.1e-16 | — | OK |
| Indicadores | Payback simples (anos) | 4,4141 anos | 4,2827 anos | 4,4141 anos | 8.9e-16 | 0,1314 anos | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Payback descontado (anos) | 5,9874 anos | — | 5,9874 anos | 2.7e-15 | — | OK |
| Indicadores | Valor de saída (6 × EBITDA) | R$ 11.060.330,00 | — | R$ 11.060.330,00 | -3.7e-09 | — | OK |
| Indicadores | VPL sem saída (10%) | R$ 3.311.462,10 | R$ 3.672.199,95 | R$ 3.311.462,10 | -3.3e-09 | R$ -360.737,85 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | VPL com saída | R$ 7.575.698,11 | — | R$ 7.575.698,11 | -4.7e-09 | — | OK |
| Indicadores | TIR sem saída | 19,2814% | 20,2117% | 19,2814% | -2.8e-13 | -0,9303% | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | TIR com saída | 24,6544% | — | 24,6544% | 3.7e-14 | — | OK |
| Indicadores | Aviso de mais de uma TIR (com saída) | não | — | não | — | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Estresse interno: geração com receita 30% menor | R$ 409.478,33 | — | R$ 409.478,33 | -5.2e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Estresse interno: CAPEX +25% | R$ 8.500.000,00 | — | R$ 8.500.000,00 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | VPL com CAPEX +25% | R$ 1.611.462,10 | — | R$ 1.611.462,10 | -3.0e-09 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Payback com CAPEX +25% | 5,3363 anos | — | 5,3363 anos | 8.9e-16 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.geracaoRegime | R$ 887.928,67 | — | R$ 887.928,67 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.geracaoAno1 | R$ -66.915,69 | — | R$ -66.915,69 | -1.0e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.ebitdaRegime | R$ 887.928,67 | — | R$ 887.928,67 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.payback | 8,7336 anos | — | 8,7336 anos | 1.8e-15 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.vplSem | R$ -2.212.103,04 | — | R$ -2.212.103,04 | -4.7e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.vplCom | R$ -158.093,41 | — | R$ -158.093,41 | -7.3e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.geracaoRegime | R$ 2.757.145,71 | — | R$ 2.757.145,71 | 9.3e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.geracaoAno1 | R$ 1.054.870,60 | — | R$ 1.054.870,60 | 7.0e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.ebitdaRegime | R$ 2.757.145,71 | — | R$ 2.757.145,71 | 9.3e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.payback | 3,0837 anos | — | 3,0837 anos | -8.9e-16 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.vplSem | R$ 8.593.944,00 | — | R$ 8.593.944,00 | 1.9e-09 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.vplCom | R$ 14.971.938,15 | — | R$ 14.971.938,15 | 3.7e-09 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.diaria | R$ 1.239.083,86 | — | R$ 1.239.083,86 | -2.1e-09 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.ocupacao | 137.863.082,6363% | — | 137.863.082,6363% | 9.3e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.fixo | R$ 2.610.981,45 | — | R$ 2.610.981,45 | -1.4e-09 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.capex | R$ 2.631.462,10 | — | R$ 2.631.462,10 | -2.3e-09 | — | OK |
| Régua e decisão | Régua: 5 passos | passa, passa, passa, passa, ajustar | — | passa, passa, passa, passa, ajustar | — | — | OK |
| Régua e decisão | Régua: decisão | Ajustar | — | Ajustar | — | — | OK |

## Entradas · C3E

| Dado | Valor de teste | Como entrou na ZAIOS |
|---|---|---|
| Unidades | 20 | `unidades` = 20 |
| Diária média | R$ 855,00 | `diaria_*` em centavos |
| Ocupação média anual | 49,6% | `ocupacao_*` |
| Dias operacionais | 365 | Calendário fixo de 365 dias da ZAIOS |
| Outras receitas anuais | R$ 480.000,00 | `outras_pct` = 0,15504958 (outras ÷ diárias do regime) |
| Custo variável por estadia | R$ 176,00 | `custo_estadia` |
| Permanência média | 3,0 noites | `permanencia` |
| Custos fixos mensais | R$ 109.250,00 | `custo_fixo` no P6 e no P5 |
| Aluguel mensal | R$ 30.000,00 | `aluguel` |
| Gestão | 8% da receita de hospedagem | `gestao_pct` (a ZAIOS aplica sobre a receita bruta) |
| Royalties | 5% da receita de hospedagem | `royalty_pct` (idem) |
| Tributos sobre vendas | 12% da receita bruta | `deducoes_pct` |
| Investimento inicial | R$ 6.800.000,00 | 7 linhas do P5 (proporções do plano), contingência 0% |
| Capital de giro inicial | R$ 420.000,00 | Sem campo na ZAIOS: ela calcula o giro recomendado |
| Mês de abertura (adotado) | Outubro | `mes_abertura`; mês do projeto sugerido pelo cronograma |

Outros campos exigidos pela ferramenta (valores adotados e justificativas): `PLANO_TESTES_COMPOSICAO.md`, seção 4.

## Comparação · C3E (72 campos)

Contagem: OK: 61 · DIVERGÊNCIA METODOLÓGICA: 10 · NÃO APLICÁVEL: 1.

Tolerâncias: R$ 0,01; frações, anos e noites 0,000001. Uma diferença ZAIOS − R2 da ordem de 1e-9 é ruído de ponto flutuante, abaixo da tolerância.

| Grupo | Campo | Esperado independente (regra da ZAIOS, R2) | Esperado pela regra do comando (R1) | Valor ZAIOS | Diferença ZAIOS − R2 | Diferença ZAIOS − R1 | Classificação |
|---|---|---|---|---|---|---|---|
| Receita | Receita de hospedagem | R$ 3.095.784,00 | R$ 3.095.784,00 | R$ 3.095.784,00 | 0 | — | OK |
| Receita | Diárias ocupadas (noites vendidas) | 3.620,80 | — | 3.620,80 | -4.5e-13 | — | OK |
| Receita | Estadias (derivado: custos variáveis ÷ custo por estadia) | 1.206,93 | — | 1.206,93 | 0 | — | OK |
| Receita | Outras receitas | R$ 480.000,00 | R$ 480.000,00 | R$ 480.000,00 | 5.8e-11 | — | OK |
| Receita | Receita bruta consolidada | R$ 3.575.784,00 | R$ 3.575.784,00 | R$ 3.575.784,00 | 4.7e-10 | — | OK |
| Receita | Ocupação média anual (ponderada pelos dias) | 49,6000% | — | 49,6000% | -1.1e-16 | — | OK |
| Deduções | Tributos sobre vendas (deduções) | R$ 429.094,08 | R$ 429.094,08 | R$ 429.094,08 | 5.8e-11 | — | OK |
| Despesas | Custos variáveis | R$ 212.420,27 | R$ 212.420,27 | R$ 212.420,27 | 2.9e-11 | — | OK |
| Despesas | Custos fixos | R$ 1.311.000,00 | R$ 1.311.000,00 | R$ 1.311.000,00 | 0 | — | OK |
| Despesas | Resultado operacional (antes dos custos do modelo) | R$ 1.623.269,65 | — | R$ 1.623.269,65 | 2.3e-10 | — | OK |
| Despesas | Aluguel (12 × mensal) | R$ 360.000,00 | R$ 360.000,00 | R$ 360.000,00 | 0 | — | OK |
| Despesas | Gestão + royalties (derivado: custos do modelo − aluguel) | R$ 464.851,92 | R$ 402.451,92 | R$ 464.851,92 | -5.8e-11 | R$ 62.400,00 | DIVERGÊNCIA METODOLÓGICA |
| Despesas | Custos do modelo | R$ 824.851,92 | R$ 762.451,92 | R$ 824.851,92 | 0 | R$ 62.400,00 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA e geração | EBITDA do regime | R$ 798.417,73 | R$ 860.817,73 | R$ 798.417,73 | 2.3e-10 | R$ -62.400,00 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA e geração | Geração de caixa do regime | R$ 798.417,73 | R$ 860.817,73 | R$ 798.417,73 | 2.3e-10 | R$ -62.400,00 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA e geração | Receita bruta do 1º ano (rampa) | R$ 2.145.960,23 | — | R$ 2.145.960,23 | 0 | — | OK |
| EBITDA e geração | EBITDA do 1º ano | R$ -189.011,08 | — | R$ -189.011,08 | 5.8e-11 | — | OK |
| EBITDA e geração | Geração do 1º ano | R$ -189.011,08 | — | R$ -189.011,08 | 5.8e-11 | — | OK |
| EBITDA e geração | Meses com geração negativa no regime | 0 | — | 0 | 0 | — | OK |
| EBITDA e geração | Pior mês do regime | R$ 50.184,79 | — | R$ 50.184,79 | 2.9e-11 | — | OK |
| EBITDA e geração | Margem operacional (antes dos custos do modelo) | 45,3962% | — | 45,3962% | 0 | — | OK |
| EBITDA e geração | Régua de margem do P6 | boa | — | boa | — | — | OK |
| EBITDA e geração | Selo do P6 Receitas | Avançar | — | Avançar | — | — | OK |
| EBITDA e geração | Equilíbrio: contribuição por noite | R$ 682,01 | — | R$ 682,01 | 2.3e-13 | — | OK |
| EBITDA e geração | Equilíbrio: noites/ano | 2.450,11 | — | 2.450,11 | -9.1e-13 | — | OK |
| EBITDA e geração | Equilíbrio: ocupação | 33,5632% | — | 33,5632% | -1.1e-16 | — | OK |
| EBITDA e geração | Equilíbrio: folga de ocupação | 16,0368% | — | 16,0368% | 0 | — | OK |
| Capital e fluxo de caixa | Capital investido (CAPEX) | R$ 6.800.000,00 | — | R$ 6.800.000,00 | 0 | — | OK |
| Capital e fluxo de caixa | Déficit acumulado da rampa | R$ 282.079,81 | — | R$ 282.079,81 | -5.8e-11 | — | OK |
| Capital e fluxo de caixa | Soma dos meses negativos do regime (giro) | R$ 0,00 | — | R$ 0,00 | 0 | — | OK |
| Capital e fluxo de caixa | Capital de giro A (6 × fixo) | R$ 655.500,00 | — | R$ 655.500,00 | 0 | — | OK |
| Capital e fluxo de caixa | Capital de giro B | R$ 609.829,81 | — | R$ 609.829,81 | -1.2e-10 | — | OK |
| Capital e fluxo de caixa | Capital de giro usado | R$ 655.500,00 | R$ 420.000,00 | R$ 655.500,00 | 0 | R$ 235.500,00 | DIVERGÊNCIA METODOLÓGICA |
| Capital e fluxo de caixa | Captação (CAPEX + giro) | R$ 7.455.500,00 | R$ 7.220.000,00 | R$ 7.455.500,00 | 0 | R$ 235.500,00 | DIVERGÊNCIA METODOLÓGICA |
| Capital e fluxo de caixa | Mês do projeto em que abre | 10 | — | 10 | 0 | — | OK |
| Capital e fluxo de caixa | Menor saldo da curva (36 meses) | R$ 373.420,19 | — | R$ 373.420,19 | 5.8e-11 | — | OK |
| Capital e fluxo de caixa | Mês do menor saldo | 15 | — | 15 | 0 | — | OK |
| Capital e fluxo de caixa | Saldo no mês 36 | R$ 1.469.585,23 | — | R$ 1.469.585,23 | 1.2e-09 | — | OK |
| Capital e fluxo de caixa | Colchão (menor saldo ÷ CAPEX) | 5,4915% | — | 5,4915% | 1.4e-17 | — | OK |
| Capital e fluxo de caixa | Menor saldo com atraso de 6 meses | R$ 377.479,51 | — | R$ 377.479,51 | 1.2e-10 | — | OK |
| Indicadores | Retorno anual (geração ÷ CAPEX) | 11,7414% | 12,6591% | 11,7414% | 2.8e-17 | -0,9176% | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Retorno do EBITDA | 11,7414% | — | 11,7414% | 2.8e-17 | — | OK |
| Indicadores | Payback simples (anos) | 9,7536 anos | 9,0755 anos | 9,7536 anos | -3.6e-15 | 0,6780 anos | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Payback descontado (anos) | não calculado (nulo) | — | não calculado (nulo) | — | — | NÃO APLICÁVEL |
| Indicadores | Valor de saída (6 × EBITDA) | R$ 4.790.506,40 | — | R$ 4.790.506,40 | 9.3e-10 | — | OK |
| Indicadores | VPL sem saída (10%) | R$ -2.791.731,22 | R$ -2.430.993,37 | R$ -2.791.731,22 | 9.3e-10 | R$ -360.737,85 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | VPL com saída | R$ -944.783,62 | — | R$ -944.783,62 | 1.2e-09 | — | OK |
| Indicadores | TIR sem saída | 0,4671% | 1,8485% | 0,4671% | -8.6e-14 | -1,3814% | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | TIR com saída | 7,6898% | — | 7,6898% | -5.9e-14 | — | OK |
| Indicadores | Aviso de mais de uma TIR (com saída) | não | — | não | — | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Estresse interno: geração com receita 30% menor | R$ -274.317,47 | — | R$ -274.317,47 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Estresse interno: CAPEX +25% | R$ 8.500.000,00 | — | R$ 8.500.000,00 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | VPL com CAPEX +25% | R$ -4.491.731,22 | — | R$ -4.491.731,22 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Payback com CAPEX +25% | 11,8828 anos | — | 11,8828 anos | -5.3e-15 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.geracaoRegime | R$ 89.987,15 | — | R$ 89.987,15 | 2.9e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.geracaoAno1 | R$ -614.166,48 | — | R$ -614.166,48 | 1.2e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.ebitdaRegime | R$ 89.987,15 | — | R$ 89.987,15 | 2.9e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.payback | 83,3914 anos | — | 83,3914 anos | -3.4e-13 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.vplSem | R$ -6.887.207,60 | — | R$ -6.887.207,60 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.vplCom | R$ -6.679.043,96 | — | R$ -6.679.043,96 | 9.3e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.geracaoRegime | R$ 1.477.241,76 | — | R$ 1.477.241,76 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.geracaoAno1 | R$ 218.376,32 | — | R$ 218.376,32 | 1.2e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.ebitdaRegime | R$ 1.477.241,76 | — | R$ 1.477.241,76 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.payback | 5,4553 anos | — | 5,4553 anos | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.vplSem | R$ 1.132.588,02 | — | R$ 1.132.588,02 | -4.7e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.vplCom | R$ 4.549.831,91 | — | R$ 4.549.831,91 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.diaria | R$ -4.342.116,59 | — | R$ -4.342.116,59 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.ocupacao | -421.931.526,1359% | — | -421.931.526,1359% | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.fixo | R$ -3.597.283,97 | — | R$ -3.597.283,97 | 9.3e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.capex | R$ -3.471.731,22 | — | R$ -3.471.731,22 | 4.7e-10 | — | OK |
| Régua e decisão | Régua: 5 passos | passa, passa, ajustar, redesenhar, ajustar | — | passa, passa, ajustar, redesenhar, ajustar | — | — | OK |
| Régua e decisão | Régua: decisão | Redesenhar | — | Redesenhar | — | — | OK |

## Antes e depois do estresse

| Indicador | C3 base | C3E estresse | Variação |
|---|---|---|---|
| Receita bruta | R$ 4.779.700,00 | R$ 3.575.784,00 | −R$ 1.203.916,00 (−25,19%) |
| Custos fixos | R$ 1.140.000,00 | R$ 1.311.000,00 | +R$ 171.000,00 |
| Custos variáveis | R$ 241.386,67 | R$ 212.420,27 | −R$ 28.966,40 (menos estadias, cada uma mais cara) |
| EBITDA do regime | R$ 1.843.388,33 | R$ 798.417,73 | −R$ 1.044.970,60 (−56,69%) |
| Geração do 1º ano | R$ 506.491,00 | **−R$ 189.011,08** | — |
| Capital de giro (ZAIOS) | R$ 570.000,00 | R$ 655.500,00 | +R$ 85.500,00 (giro A, pelo fixo maior) |
| Menor saldo da curva | R$ 532.086,82 (mês 12) | R$ 373.420,19 (mês 15) | −R$ 158.666,63 |
| Colchão | 7,82% | 5,49% | −2,33 p.p. |
| Retorno anual | 27,11% | 11,74% | −15,37 p.p. |
| Payback simples | 4,41 anos | 9,75 anos | +5,34 anos |
| Payback descontado | 5,99 anos | não se paga em 10 anos | — |
| VPL sem saída | R$ 3.311.462,10 | **−R$ 2.791.731,22** | −R$ 6.103.193,32 |
| TIR sem saída | 19,28% | 0,47% | — |
| Régua (5 passos) | passa, passa, passa, passa, ajustar | passa, passa, ajustar, redesenhar, ajustar | — |
| Decisão | Ajustar | **Redesenhar** | — |

## Leitura econômica

**Matemática:** C3 tem 72 de 72 campos conferindo com a regra documentada; C3E também tem 72 de 72. Não há divergência matemática.

**Divergências metodológicas** (10 em cada execução), com as mesmas causas do cenário 2:
- **gestão e royalties sobre a receita bruta** (O11): 13% × R$ 480.000 = R$ 62.400/ano a mais. O VPL fica −R$ 360.737,85 em relação à regra do comando, nas duas execuções;
- **capital de giro calculado**: R$ 570.000 e R$ 655.500, contra o informado de R$ 420.000.

**Os indicadores refletem o estresse?** Sim:
- receita −25%, EBITDA −57% (a alavancagem dos custos fixos e do aluguel aparece corretamente);
- 1º ano negativo, déficit da rampa de R$ 282.079,81;
- VPL negativo, TIR abaixo da taxa, payback descontado fora do horizonte;
- decisão Redesenhar.

**Indicadores indefinidos:** o payback descontado do C3E vem nulo, com o motivo "Não se paga em 10 anos.". É o tratamento correto.

**Pontos de atenção (nenhum é erro de conta):**

| # | Achado | Risco | Classificação |
|---|---|---|---|
| O8 | No C3E, o P6 mostra **"Avançar"** e a régua de margem marca **"boa"** (margem operacional de 45,40%, **antes** de aluguel, gestão e royalties). A viabilidade, na mesma tela, decide **Redesenhar**. O EBITDA real é de 22,33% da receita | Dois selos opostos. O do P6 pode ser lido como aprovação | LIMITAÇÃO (apresentação) + risco do veredito antecipado |
| D8 | O cenário conservador interno, aplicado sobre o estresse, dá payback simples **estendido de 83,39 anos** | Número exibido como payback, sem limite (D8 pendente) | LIMITAÇÃO (D8) |
| O10 | O teste de **atraso de 6 meses** mostra menor saldo de R$ 377.479,51, **maior** que sem atraso (R$ 373.420,19). No C1 e no C2 acontece o mesmo | Com o horizonte fixo de 36 meses, o atraso tira meses de operação deficitária da janela, e o "estresse" parece melhorar o caixa | LIMITAÇÃO (horizonte) |
| — | Com o giro informado (R$ 420.000), o menor saldo do C3E cai para R$ 151.904,63 (colchão de 2,23%) | O giro do comando ficaria abaixo da regra da ZAIOS (giro A = 6 × fixo = R$ 655.500) | DIVERGÊNCIA METODOLÓGICA (giro) |

**Reserva e colchão:**
- A reserva de reposição foi **0%** (não informada no comando). A geração de caixa é igual ao EBITDA, e a regra D2-C (4%) e a faixa de 3–5% da ZAIOS **não foram exercitadas**.
- O colchão foi calculado com contingência 0%, então a curva "com contingência usada" é igual à "sem".


## Evidência

- Execução: `testes/financeiro/resultados/2026-11-09-05f/resultado_05f.json` e `RESULTADO_05F.md`.
- Esperados: `testes/financeiro/independente/esperados_05f.json`, gerados por `composicao_05f_referencia.py`.
- Entradas: `testes/financeiro/composicao_05f/cenarios_05f.json`.
