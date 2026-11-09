# Matriz comparativa · Comando 05F

09/11/2026 · Comparação da composição da ZAIOS (commit `ec21ad5`, cópia local) com dois esperados calculados de forma independente:
- **R2:** a regra documentada da ZAIOS;
- **R1:** a regra do Comando 05F.

Detalhe de cada campo nos documentos de cenário.

## 1. Totais

| Execução | Campos | OK | Divergência matemática | Divergência metodológica | Limitação | Não aplicável |
|---|---|---|---|---|---|---|
| C1 | 72 | 64 | 0 | 2 | 0 | 6 |
| C2 | 72 | 62 | 0 | 10 | 0 | 0 |
| C3 | 72 | 62 | 0 | 10 | 0 | 0 |
| C3E | 72 | 61 | 0 | 10 | 0 | 1 |
| **Total** | **288** | **249** | **0** | **32** | **0** | **7** |

**Maior diferença absoluta entre a ZAIOS e R2:** 4.7e-09. É ruído de ponto flutuante, muito abaixo da tolerância (R$ 0,01 em dinheiro; 0,000001 em frações). Não houve diferença de arredondamento relevante, porque as entradas são exatas em centavos e a contingência é zero.

**Leitura das classificações:**
- **Divergência matemática: 0.** A composição calcula o que a regra documentada diz, nos 288 campos.
- **Divergência metodológica: 32.** Duas causas, ambas regras do comando que a ZAIOS não segue:
  - (a) gestão e royalties sobre a receita bruta, e não sobre a de hospedagem (C2, C3, C3E; em C1 não há outras receitas);
  - (b) capital de giro calculado pela ZAIOS, e não o informado (todos).
  - As outras divergências do mesmo cenário (EBITDA, geração, retorno, payback, VPL, TIR) são consequência delas.
- **Não aplicável: 7.** Payback, payback descontado e TIR sem troca de sinal: a ZAIOS também não apresenta número e mostra o motivo.
- **Limitações (fora da contagem por campo, porque são achados de apresentação ou de definição):** O8, O9, O10, O12 e a conversão das outras receitas. Ver `RESSALVAS_E_CLASSIFICACAO_05F.md`.

## 2. Tabela-resumo por cenário

### C1

| Grupo | Campo | Valor esperado independente (R2) | Valor esperado pela regra do comando (R1) | Valor ZAIOS | Diferença (ZAIOS − R2) | Classificação |
|---|---|---|---|---|---|---|
| Receita | Receita bruta consolidada | R$ 172.462,50 | R$ 172.462,50 | R$ 172.462,50 | 2.9e-11 | OK |
| Deduções | Tributos sobre vendas (deduções) | R$ 13.797,00 | R$ 13.797,00 | R$ 13.797,00 | 1.8e-12 | OK |
| Despesas | Custos variáveis | R$ 16.288,12 | R$ 16.288,12 | R$ 16.288,12 | 1.8e-12 | OK |
| Despesas | Custos fixos | R$ 108.000,00 | R$ 108.000,00 | R$ 108.000,00 | 0 | OK |
| Despesas | Custos do modelo | R$ 49.797,00 | R$ 49.797,00 | R$ 49.797,00 | 0 | OK |
| EBITDA | EBITDA do regime | R$ -15.419,63 | R$ -15.419,63 | R$ -15.419,63 | -9.1e-12 | OK |
| Fluxo de caixa | Geração do 1º ano | R$ -66.675,64 | — | R$ -66.675,64 | 1.5e-11 | OK |
| Fluxo de caixa | Capital de giro usado | R$ 109.095,26 | R$ 45.000,00 | R$ 109.095,26 | 1.5e-11 | DIVERGÊNCIA METODOLÓGICA |
| Fluxo de caixa | Captação (CAPEX + giro) | R$ 859.095,26 | R$ 795.000,00 | R$ 859.095,26 | -1.2e-10 | DIVERGÊNCIA METODOLÓGICA |
| Fluxo de caixa | Menor saldo da curva (36 meses) | R$ 22.704,75 | — | R$ 22.704,75 | -2.9e-11 | OK |
| Indicadores | Retorno anual (geração ÷ CAPEX) | -2,0560% | -2,0560% | -2,0560% | -1.0e-17 | OK |
| Indicadores | Payback simples (anos) | não calculado (nulo) | não calculado (nulo) | não calculado (nulo) | — | NÃO APLICÁVEL |
| Indicadores | VPL sem saída (10%) | R$ -891.343,30 | R$ -891.343,30 | R$ -891.343,30 | 1.2e-10 | OK |
| Indicadores | TIR sem saída | não calculado (nulo) | não calculado (nulo) | não calculado (nulo) | — | NÃO APLICÁVEL |
| Indicadores | Colchão (menor saldo ÷ CAPEX) | 3,0273% | — | 3,0273% | -3.8e-17 | OK |
| Indicadores | Régua: decisão | Redesenhar | — | Redesenhar | — | OK |

### C2

| Grupo | Campo | Valor esperado independente (R2) | Valor esperado pela regra do comando (R1) | Valor ZAIOS | Diferença (ZAIOS − R2) | Classificação |
|---|---|---|---|---|---|---|
| Receita | Receita bruta consolidada | R$ 1.348.584,00 | R$ 1.348.584,00 | R$ 1.348.584,00 | 0 | OK |
| Deduções | Tributos sobre vendas (deduções) | R$ 134.858,40 | R$ 134.858,40 | R$ 134.858,40 | 0 | OK |
| Despesas | Custos variáveis | R$ 81.292,80 | R$ 81.292,80 | R$ 81.292,80 | 0 | OK |
| Despesas | Custos fixos | R$ 336.000,00 | R$ 336.000,00 | R$ 336.000,00 | 0 | OK |
| Despesas | Custos do modelo | R$ 244.344,24 | R$ 224.544,24 | R$ 244.344,24 | -2.9e-11 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA | EBITDA do regime | R$ 552.088,56 | R$ 571.888,56 | R$ 552.088,56 | -1.2e-10 | DIVERGÊNCIA METODOLÓGICA |
| Fluxo de caixa | Geração do 1º ano | R$ 173.914,06 | — | R$ 173.914,06 | 0 | OK |
| Fluxo de caixa | Capital de giro usado | R$ 168.000,00 | R$ 120.000,00 | R$ 168.000,00 | 0 | DIVERGÊNCIA METODOLÓGICA |
| Fluxo de caixa | Captação (CAPEX + giro) | R$ 2.268.000,00 | R$ 2.220.000,00 | R$ 2.268.000,00 | 0 | DIVERGÊNCIA METODOLÓGICA |
| Fluxo de caixa | Menor saldo da curva (36 meses) | R$ 132.524,00 | — | R$ 132.524,00 | -2.9e-11 | OK |
| Indicadores | Retorno anual (geração ÷ CAPEX) | 26,2899% | 27,2328% | 26,2899% | -1.1e-16 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Payback simples (anos) | 4,4887 anos | 4,3466 anos | 4,4887 anos | 0 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | VPL sem saída (10%) | R$ 948.550,21 | R$ 1.063.295,43 | R$ 948.550,21 | -4.7e-10 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | TIR sem saída | 18,7251% | 19,6995% | 18,7251% | -1.3e-13 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Colchão (menor saldo ÷ CAPEX) | 6,3107% | — | 6,3107% | -1.4e-17 | OK |
| Indicadores | Régua: decisão | Ajustar | — | Ajustar | — | OK |

### C3

| Grupo | Campo | Valor esperado independente (R2) | Valor esperado pela regra do comando (R1) | Valor ZAIOS | Diferença (ZAIOS − R2) | Classificação |
|---|---|---|---|---|---|---|
| Receita | Receita bruta consolidada | R$ 4.779.700,00 | R$ 4.779.700,00 | R$ 4.779.700,00 | 9.3e-10 | OK |
| Deduções | Tributos sobre vendas (deduções) | R$ 573.564,00 | R$ 573.564,00 | R$ 573.564,00 | 0 | OK |
| Despesas | Custos variáveis | R$ 241.386,67 | R$ 241.386,67 | R$ 241.386,67 | -2.9e-11 | OK |
| Despesas | Custos fixos | R$ 1.140.000,00 | R$ 1.140.000,00 | R$ 1.140.000,00 | 0 | OK |
| Despesas | Custos do modelo | R$ 981.361,00 | R$ 918.961,00 | R$ 981.361,00 | 0 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA | EBITDA do regime | R$ 1.843.388,33 | R$ 1.905.788,33 | R$ 1.843.388,33 | -4.7e-10 | DIVERGÊNCIA METODOLÓGICA |
| Fluxo de caixa | Geração do 1º ano | R$ 506.491,00 | — | R$ 506.491,00 | -1.2e-10 | OK |
| Fluxo de caixa | Capital de giro usado | R$ 570.000,00 | R$ 420.000,00 | R$ 570.000,00 | 0 | DIVERGÊNCIA METODOLÓGICA |
| Fluxo de caixa | Captação (CAPEX + giro) | R$ 7.370.000,00 | R$ 7.220.000,00 | R$ 7.370.000,00 | 0 | DIVERGÊNCIA METODOLÓGICA |
| Fluxo de caixa | Menor saldo da curva (36 meses) | R$ 532.086,82 | — | R$ 532.086,82 | -1.2e-10 | OK |
| Indicadores | Retorno anual (geração ÷ CAPEX) | 27,1087% | 28,0263% | 27,1087% | -1.1e-16 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Payback simples (anos) | 4,4141 anos | 4,2827 anos | 4,4141 anos | 8.9e-16 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | VPL sem saída (10%) | R$ 3.311.462,10 | R$ 3.672.199,95 | R$ 3.311.462,10 | -3.3e-09 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | TIR sem saída | 19,2814% | 20,2117% | 19,2814% | -2.8e-13 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Colchão (menor saldo ÷ CAPEX) | 7,8248% | — | 7,8248% | -1.4e-17 | OK |
| Indicadores | Régua: decisão | Ajustar | — | Ajustar | — | OK |

### C3E

| Grupo | Campo | Valor esperado independente (R2) | Valor esperado pela regra do comando (R1) | Valor ZAIOS | Diferença (ZAIOS − R2) | Classificação |
|---|---|---|---|---|---|---|
| Receita | Receita bruta consolidada | R$ 3.575.784,00 | R$ 3.575.784,00 | R$ 3.575.784,00 | 4.7e-10 | OK |
| Deduções | Tributos sobre vendas (deduções) | R$ 429.094,08 | R$ 429.094,08 | R$ 429.094,08 | 5.8e-11 | OK |
| Despesas | Custos variáveis | R$ 212.420,27 | R$ 212.420,27 | R$ 212.420,27 | 2.9e-11 | OK |
| Despesas | Custos fixos | R$ 1.311.000,00 | R$ 1.311.000,00 | R$ 1.311.000,00 | 0 | OK |
| Despesas | Custos do modelo | R$ 824.851,92 | R$ 762.451,92 | R$ 824.851,92 | 0 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA | EBITDA do regime | R$ 798.417,73 | R$ 860.817,73 | R$ 798.417,73 | 2.3e-10 | DIVERGÊNCIA METODOLÓGICA |
| Fluxo de caixa | Geração do 1º ano | R$ -189.011,08 | — | R$ -189.011,08 | 5.8e-11 | OK |
| Fluxo de caixa | Capital de giro usado | R$ 655.500,00 | R$ 420.000,00 | R$ 655.500,00 | 0 | DIVERGÊNCIA METODOLÓGICA |
| Fluxo de caixa | Captação (CAPEX + giro) | R$ 7.455.500,00 | R$ 7.220.000,00 | R$ 7.455.500,00 | 0 | DIVERGÊNCIA METODOLÓGICA |
| Fluxo de caixa | Menor saldo da curva (36 meses) | R$ 373.420,19 | — | R$ 373.420,19 | 5.8e-11 | OK |
| Indicadores | Retorno anual (geração ÷ CAPEX) | 11,7414% | 12,6591% | 11,7414% | 2.8e-17 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Payback simples (anos) | 9,7536 anos | 9,0755 anos | 9,7536 anos | -3.6e-15 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | VPL sem saída (10%) | R$ -2.791.731,22 | R$ -2.430.993,37 | R$ -2.791.731,22 | 9.3e-10 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | TIR sem saída | 0,4671% | 1,8485% | 0,4671% | -8.6e-14 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Colchão (menor saldo ÷ CAPEX) | 5,4915% | — | 5,4915% | 1.4e-17 | OK |
| Indicadores | Régua: decisão | Redesenhar | — | Redesenhar | — | OK |

## 3. Cobertura acumulada da camada de composição

| Condição | 05E | 05F |
|---|---|---|
| Cenários integrados (P5 → P6 → Viabilidade) | 1 | +4 execuções (3 cenários + 1 estresse) |
| Abertura fora de janeiro | Não | Março e outubro |
| Sazonalidade passando pela composição | Não | Sim (C2) |
| Outras receitas passando pela composição | Não | Sim (C2, C3, C3E) |
| Custo por estadia e permanência | Não | Sim |
| Aluguel, gestão e royalties passando pela composição | Não | Sim |
| Resultado negativo (EBITDA < 0, sem payback nem TIR) | Não | Sim (C1) |
| Meses negativos no regime (giro B pela sazonalidade) | Não | Sim (C1: 12 meses) |
| Sensibilidade (4 itens) e cenário otimista | Não | Sim |
| Atraso de 6 meses | Não | Sim |
| Contingência > 0 | Sim (25%) | Não (0%, por definição do comando) |
| Pró-labore, reserva de reposição, quebra > 0 pela composição | Não | **Não** (lacuna) |
| Taxa de desconto e múltiplo diferentes de 10% e 6× | Não | **Não** (lacuna) |
