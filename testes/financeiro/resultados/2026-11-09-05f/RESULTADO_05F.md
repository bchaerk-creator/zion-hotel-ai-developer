# Resultado da execução · Comando 05F

Gerado por `run_05f.js` em 2026-11-09T22:24:20.379Z. Tolerâncias: R$ 0,01; frações, anos e noites 0,000001.

Hashes SHA-256 das fontes da ZAIOS carregadas (cópia local, fora do repositório):

- `src/exercicios/capex-calculo.ts`: `b728645b2a0ae834`
- `src/exercicios/receitas-calculo.ts`: `c36e73513e0a0402`
- `src/exercicios/viabilidade-calculo.ts`: `2bcba2abb27a1e31`

Entradas: `84302e46101225a0` · Esperados: `0ac71978111d0b4f`

## Contagem

| Cenário | OK | DIVERGÊNCIA METODOLÓGICA | DIVERGÊNCIA MATEMÁTICA | NÃO APLICÁVEL |
|---|---|---|---|---|
| C1 | 64 | 2 | 0 | 6 |
| C2 | 62 | 10 | 0 | 0 |
| C3 | 62 | 10 | 0 | 0 |
| C3E | 61 | 10 | 0 | 1 |

## C1 · Conservador

| Campo | Esperado R2 (regra da ZAIOS) | Esperado R1 (regra do comando) | ZAIOS | Diferença (R2) | Diferença (R1) | Classificação |
|---|---|---|---|---|---|---|
| Receita de hospedagem | 172462.50 | 172462.50 | 172462.50 | 2.9e-11 | 0.000000 | OK |
| Diárias ocupadas (noites vendidas) | 383.25 | — | 383.25 | 1.1e-13 | — | OK |
| Outras receitas | 0 | 0 | 0 | 0.0e+0 | 0 | OK |
| Receita bruta consolidada | 172462.50 | 172462.50 | 172462.50 | 2.9e-11 | 0.000000 | OK |
| Tributos sobre vendas (deduções) | 13797.00 | 13797.00 | 13797 | 1.8e-12 | 0.000000 | OK |
| Custos variáveis | 16288.12 | 16288.12 | 16288.13 | 1.8e-12 | 0.000000 | OK |
| Estadias (derivado: custos variáveis ÷ custo por estadia) | 191.62 | — | 191.63 | 2.8e-14 | — | OK |
| Custos fixos | 108000 | 108000 | 108000 | 0.0e+0 | 0 | OK |
| Resultado operacional (antes dos custos do modelo) | 34377.37 | — | 34377.37 | -7.3e-12 | — | OK |
| Custos do modelo | 49797 | 49797 | 49797 | 0.0e+0 | 0 | OK |
| Aluguel (12 × mensal) | 36000 | 36000 | 36000 | 0.0e+0 | 0 | OK |
| Gestão + royalties (derivado: custos do modelo − aluguel) | 13797.00 | 13797.00 | 13797 | 1.8e-12 | 0.000000 | OK |
| EBITDA do regime | -15419.63 | -15419.63 | -15419.63 | -9.1e-12 | -0.000000 | OK |
| Geração de caixa do regime | -15419.63 | -15419.63 | -15419.63 | -9.1e-12 | -0.000000 | OK |
| Receita bruta do 1º ano (rampa) | 103713.75 | — | 103713.75 | 1.5e-11 | — | OK |
| EBITDA do 1º ano | -66675.64 | — | -66675.64 | 1.5e-11 | — | OK |
| Geração do 1º ano | -66675.64 | — | -66675.64 | 1.5e-11 | — | OK |
| Meses com geração negativa no regime | 12 | — | 12 | 0.0e+0 | — | OK |
| Pior mês do regime | -2136.30 | — | -2136.30 | -4.5e-13 | — | OK |
| Ocupação média anual (ponderada pelos dias) | 0.350000 | — | 0.350000 | 1.1e-16 | — | OK |
| Margem operacional (antes dos custos do modelo) | 0.199332 | — | 0.199332 | -5.6e-17 | — | OK |
| Régua de margem do P6 | apertada | — | apertada | — | — | OK |
| Selo do P6 Receitas | Ajustar | — | Ajustar | — | — | OK |
| Equilíbrio: contribuição por noite | 335.50 | — | 335.50 | -5.7e-14 | — | OK |
| Equilíbrio: noites/ano | 429.21 | — | 429.21 | 5.7e-14 | — | OK |
| Equilíbrio: ocupação | 0.391973 | — | 0.391973 | 5.6e-17 | — | OK |
| Equilíbrio: folga de ocupação | -0.041973 | — | -0.041973 | 5.6e-17 | — | OK |
| Capital investido (CAPEX) | 750000 | — | 750000 | 0.0e+0 | — | OK |
| Déficit acumulado da rampa | 66675.64 | — | 66675.64 | -1.5e-11 | — | OK |
| Soma dos meses negativos do regime (giro) | 15419.63 | — | 15419.63 | 9.1e-12 | — | OK |
| Capital de giro A (6 × fixo) | 54000 | — | 54000 | 0.0e+0 | — | OK |
| Capital de giro B | 109095.26 | — | 109095.26 | 1.5e-11 | — | OK |
| Capital de giro usado | 109095.26 | 45000 | 109095.26 | 1.5e-11 | 64095.26 | DIVERGÊNCIA METODOLÓGICA |
| Captação (CAPEX + giro) | 859095.26 | 795000 | 859095.26 | -1.2e-10 | 64095.26 | DIVERGÊNCIA METODOLÓGICA |
| Retorno anual (geração ÷ CAPEX) | -0.020560 | -0.020560 | -0.020560 | -1.0e-17 | -0.000000 | OK |
| Retorno do EBITDA | -0.020560 | — | -0.020560 | -1.0e-17 | — | OK |
| Payback simples (anos) | nulo | nulo | nulo | — | — | NÃO APLICÁVEL |
| Payback descontado (anos) | nulo | — | nulo | — | — | NÃO APLICÁVEL |
| Valor de saída (6 × EBITDA) | -92517.75 | — | -92517.75 | -4.4e-11 | — | OK |
| VPL sem saída (10%) | -891343.30 | -891343.30 | -891343.30 | 1.2e-10 | 0.000000 | OK |
| VPL com saída | -927012.89 | — | -927012.89 | 1.2e-10 | — | OK |
| TIR sem saída | nulo | nulo | nulo | — | — | NÃO APLICÁVEL |
| TIR com saída | nulo | — | nulo | — | — | NÃO APLICÁVEL |
| Aviso de mais de uma TIR (com saída) | false | — | false | — | — | OK |
| Mês do projeto em que abre | 10 | — | 10 | 0.0e+0 | — | OK |
| Menor saldo da curva (36 meses) | 22704.75 | — | 22704.75 | -2.9e-11 | — | OK |
| Mês do menor saldo | 36 | — | 36 | 0.0e+0 | — | OK |
| Saldo no mês 36 | 22704.75 | — | 22704.75 | -2.9e-11 | — | OK |
| Colchão (menor saldo ÷ CAPEX) | 0.030273 | — | 0.030273 | -3.8e-17 | — | OK |
| Menor saldo com atraso de 6 meses | 30608.31 | — | 30608.31 | -4.4e-11 | — | OK |
| Estresse interno: geração com receita 30% menor | -67158.38 | — | -67158.38 | -1.5e-11 | — | OK |
| Estresse interno: CAPEX +25% | 937500 | — | 937500 | 0.0e+0 | — | OK |
| VPL com CAPEX +25% | -1078843.30 | — | -1078843.30 | 2.3e-10 | — | OK |
| Payback com CAPEX +25% | nulo | — | nulo | — | — | NÃO APLICÁVEL |
| conservador.geracaoRegime | -52725.18 | — | -52725.18 | 0.0e+0 | — | OK |
| conservador.geracaoAno1 | -89110.07 | — | -89110.07 | -1.5e-11 | — | OK |
| conservador.ebitdaRegime | -52725.18 | — | -52725.18 | 0.0e+0 | — | OK |
| conservador.payback | nulo | — | nulo | — | — | NÃO APLICÁVEL |
| conservador.vplSem | -1107050.58 | — | -1107050.58 | 0.0e+0 | — | OK |
| conservador.vplCom | -1229017.62 | — | -1229017.62 | -2.3e-10 | — | OK |
| otimista.geracaoRegime | 20527.31 | — | 20527.31 | 1.8e-11 | — | OK |
| otimista.geracaoAno1 | -45058.23 | — | -45058.23 | 1.5e-11 | — | OK |
| otimista.ebitdaRegime | 20527.31 | — | 20527.31 | 1.8e-11 | — | OK |
| otimista.payback | 39.73 | — | 39.73 | -3.6e-14 | — | OK |
| otimista.vplSem | -683491.80 | — | -683491.80 | -1.2e-10 | — | OK |
| otimista.vplCom | -636006.80 | — | -636006.80 | -1.2e-10 | — | OK |
| sensibilidade.diaria | -975108.81 | — | -975108.81 | 1.2e-10 | — | OK |
| sensibilidade.capex | -966343.30 | — | -966343.30 | 2.3e-10 | — | OK |
| sensibilidade.ocupacao | -965690.73 | — | -965690.73 | 1.2e-10 | — | OK |
| sensibilidade.fixo | -957704.62 | — | -957704.62 | -3.5e-10 | — | OK |
| Régua: 5 passos | [redesenhar, redesenhar, redesenhar, redesenhar, ajustar] | — | [redesenhar, redesenhar, redesenhar, redesenhar, ajustar] | — | — | OK |
| Régua: decisão | Redesenhar | — | Redesenhar | — | — | OK |

## C2 · Intermediário

| Campo | Esperado R2 (regra da ZAIOS) | Esperado R1 (regra do comando) | ZAIOS | Diferença (R2) | Diferença (R1) | Classificação |
|---|---|---|---|---|---|---|
| Receita de hospedagem | 1168584 | 1168584 | 1168584 | 0.0e+0 | 0 | OK |
| Diárias ocupadas (noites vendidas) | 1693.60 | — | 1693.60 | 0.0e+0 | — | OK |
| Outras receitas | 180000.00 | 180000 | 180000.00 | -5.8e-11 | -0.000000 | OK |
| Receita bruta consolidada | 1348584 | 1348584 | 1348584 | 0.0e+0 | 0 | OK |
| Tributos sobre vendas (deduções) | 134858.40 | 134858.40 | 134858.40 | 0.0e+0 | 0 | OK |
| Custos variáveis | 81292.80 | 81292.80 | 81292.80 | 0.0e+0 | 0 | OK |
| Estadias (derivado: custos variáveis ÷ custo por estadia) | 677.44 | — | 677.44 | 0.0e+0 | — | OK |
| Custos fixos | 336000 | 336000 | 336000 | 0.0e+0 | 0 | OK |
| Resultado operacional (antes dos custos do modelo) | 796432.80 | — | 796432.80 | -2.3e-10 | — | OK |
| Custos do modelo | 244344.24 | 224544.24 | 244344.24 | -2.9e-11 | 19800.00 | DIVERGÊNCIA METODOLÓGICA |
| Aluguel (12 × mensal) | 96000 | 96000 | 96000 | 0.0e+0 | 0 | OK |
| Gestão + royalties (derivado: custos do modelo − aluguel) | 148344.24 | 128544.24 | 148344.24 | -2.9e-11 | 19800.00 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA do regime | 552088.56 | 571888.56 | 552088.56 | -1.2e-10 | -19800 | DIVERGÊNCIA METODOLÓGICA |
| Geração de caixa do regime | 552088.56 | 571888.56 | 552088.56 | -1.2e-10 | -19800 | DIVERGÊNCIA METODOLÓGICA |
| Receita bruta do 1º ano (rampa) | 830337.88 | — | 830337.88 | 0.0e+0 | — | OK |
| EBITDA do 1º ano | 173914.06 | — | 173914.06 | 0.0e+0 | — | OK |
| Geração do 1º ano | 173914.06 | — | 173914.06 | 0.0e+0 | — | OK |
| Meses com geração negativa no regime | 0 | — | 0 | 0.0e+0 | — | OK |
| Pior mês do regime | 21176.61 | — | 21176.61 | -1.1e-11 | — | OK |
| Ocupação média anual (ponderada pelos dias) | 0.580000 | — | 0.580000 | 0.0e+0 | — | OK |
| Margem operacional (antes dos custos do modelo) | 0.590570 | — | 0.590570 | -2.2e-16 | — | OK |
| Régua de margem do P6 | boa | — | boa | — | — | OK |
| Selo do P6 Receitas | Avançar | — | Avançar | — | — | OK |
| Equilíbrio: contribuição por noite | 581.06 | — | 581.06 | -1.1e-13 | — | OK |
| Equilíbrio: noites/ano | 743.46 | — | 743.46 | 1.1e-13 | — | OK |
| Equilíbrio: ocupação | 0.254611 | — | 0.254611 | 5.6e-17 | — | OK |
| Equilíbrio: folga de ocupação | 0.325389 | — | 0.325389 | -5.6e-17 | — | OK |
| Capital investido (CAPEX) | 2100000 | — | 2100000 | 0.0e+0 | — | OK |
| Déficit acumulado da rampa | 35476.00 | — | 35476.00 | 0.0e+0 | — | OK |
| Soma dos meses negativos do regime (giro) | 0 | — | 0 | 0.0e+0 | — | OK |
| Capital de giro A (6 × fixo) | 168000 | — | 168000 | 0.0e+0 | — | OK |
| Capital de giro B | 119476.00 | — | 119476.00 | -1.5e-11 | — | OK |
| Capital de giro usado | 168000 | 120000 | 168000 | 0.0e+0 | 48000 | DIVERGÊNCIA METODOLÓGICA |
| Captação (CAPEX + giro) | 2268000 | 2220000 | 2268000 | 0.0e+0 | 48000 | DIVERGÊNCIA METODOLÓGICA |
| Retorno anual (geração ÷ CAPEX) | 0.262899 | 0.272328 | 0.262899 | -1.1e-16 | -0.009429 | DIVERGÊNCIA METODOLÓGICA |
| Retorno do EBITDA | 0.262899 | — | 0.262899 | -1.1e-16 | — | OK |
| Payback simples (anos) | 4.488726 | 4.346622 | 4.488726 | 0.0e+0 | 0.142104 | DIVERGÊNCIA METODOLÓGICA |
| Payback descontado (anos) | 6.138737 | — | 6.138737 | 8.9e-16 | — | OK |
| Valor de saída (6 × EBITDA) | 3312531.36 | — | 3312531.36 | -9.3e-10 | — | OK |
| VPL sem saída (10%) | 948550.21 | 1063295.43 | 948550.21 | -4.7e-10 | -114745.23 | DIVERGÊNCIA METODOLÓGICA |
| VPL com saída | 2225674.45 | — | 2225674.45 | -9.3e-10 | — | OK |
| TIR sem saída | 0.187251 | 0.196995 | 0.187251 | -1.3e-13 | -0.009744 | DIVERGÊNCIA METODOLÓGICA |
| TIR com saída | 0.241441 | — | 0.241441 | 1.1e-13 | — | OK |
| Aviso de mais de uma TIR (com saída) | false | — | false | — | — | OK |
| Mês do projeto em que abre | 10 | — | 10 | 0.0e+0 | — | OK |
| Menor saldo da curva (36 meses) | 132524.00 | — | 132524.00 | -2.9e-11 | — | OK |
| Mês do menor saldo | 13 | — | 13 | 0.0e+0 | — | OK |
| Saldo no mês 36 | 985841.86 | — | 985841.86 | 2.3e-10 | — | OK |
| Colchão (menor saldo ÷ CAPEX) | 0.063107 | — | 0.063107 | -1.4e-17 | — | OK |
| Menor saldo com atraso de 6 meses | 148656.29 | — | 148656.29 | 0.0e+0 | — | OK |
| Estresse interno: geração com receita 30% menor | 147513.36 | — | 147513.36 | -1.2e-10 | — | OK |
| Estresse interno: CAPEX +25% | 2625000 | — | 2625000 | 0.0e+0 | — | OK |
| VPL com CAPEX +25% | 423550.21 | — | 423550.21 | -8.7e-10 | — | OK |
| Payback com CAPEX +25% | 5.439661 | — | 5.439661 | 0.0e+0 | — | OK |
| conservador.geracaoRegime | 270040.34 | — | 270040.34 | -5.8e-11 | — | OK |
| conservador.geracaoAno1 | 253.90 | — | 253.90 | -8.7e-12 | — | OK |
| conservador.ebitdaRegime | 270040.34 | — | 270040.34 | -5.8e-11 | — | OK |
| conservador.payback | 8.775676 | — | 8.775676 | 3.6e-15 | — | OK |
| conservador.vplSem | -685979.42 | — | -685979.42 | -3.5e-10 | — | OK |
| conservador.vplCom | -61305.97 | — | -61305.97 | -7.3e-10 | — | OK |
| otimista.geracaoRegime | 822220.70 | — | 822220.70 | 1.2e-10 | — | OK |
| otimista.geracaoAno1 | 340237.37 | — | 340237.37 | -1.7e-10 | — | OK |
| otimista.ebitdaRegime | 822220.70 | — | 822220.70 | 1.2e-10 | — | OK |
| otimista.payback | 3.140256 | — | 3.140256 | 0.0e+0 | — | OK |
| otimista.vplSem | 2514023.61 | — | 2514023.61 | 4.7e-10 | — | OK |
| otimista.vplCom | 4416033.65 | — | 4416033.65 | 1.9e-9 | — | OK |
| sensibilidade.diaria | 331138.98 | — | 331138.98 | 5.8e-10 | — | OK |
| sensibilidade.ocupacao | 378249.89 | — | 378249.89 | 1.7e-10 | — | OK |
| sensibilidade.capex | 738550.21 | — | 738550.21 | -7.0e-10 | — | OK |
| sensibilidade.fixo | 742092.75 | — | 742092.75 | -8.1e-10 | — | OK |
| Régua: 5 passos | [passa, passa, passa, passa, ajustar] | — | [passa, passa, passa, passa, ajustar] | — | — | OK |
| Régua: decisão | Ajustar | — | Ajustar | — | — | OK |

## C3 · Maior porte

| Campo | Esperado R2 (regra da ZAIOS) | Esperado R1 (regra do comando) | ZAIOS | Diferença (R2) | Diferença (R1) | Classificação |
|---|---|---|---|---|---|---|
| Receita de hospedagem | 4299700 | 4299700 | 4299700 | 0.0e+0 | 0 | OK |
| Diárias ocupadas (noites vendidas) | 4526 | — | 4526 | 0.0e+0 | — | OK |
| Outras receitas | 480000 | 480000 | 480000 | 0.0e+0 | 0 | OK |
| Receita bruta consolidada | 4779700 | 4779700 | 4779700.00 | 9.3e-10 | 0.000000 | OK |
| Tributos sobre vendas (deduções) | 573564 | 573564 | 573564 | 0.0e+0 | 0 | OK |
| Custos variáveis | 241386.67 | 241386.67 | 241386.67 | -2.9e-11 | -0.000000 | OK |
| Estadias (derivado: custos variáveis ÷ custo por estadia) | 1508.67 | — | 1508.67 | 0.0e+0 | — | OK |
| Custos fixos | 1140000 | 1140000 | 1140000 | 0.0e+0 | 0 | OK |
| Resultado operacional (antes dos custos do modelo) | 2824749.33 | — | 2824749.33 | -9.3e-10 | — | OK |
| Custos do modelo | 981361 | 918961 | 981361 | 0.0e+0 | 62400 | DIVERGÊNCIA METODOLÓGICA |
| Aluguel (12 × mensal) | 360000 | 360000 | 360000 | 0.0e+0 | 0 | OK |
| Gestão + royalties (derivado: custos do modelo − aluguel) | 621361 | 558961 | 621361 | 0.0e+0 | 62400 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA do regime | 1843388.33 | 1905788.33 | 1843388.33 | -4.7e-10 | -62400.00 | DIVERGÊNCIA METODOLÓGICA |
| Geração de caixa do regime | 1843388.33 | 1905788.33 | 1843388.33 | -4.7e-10 | -62400.00 | DIVERGÊNCIA METODOLÓGICA |
| Receita bruta do 1º ano (rampa) | 2868474.75 | — | 2868474.75 | -4.7e-10 | — | OK |
| EBITDA do 1º ano | 506491.00 | — | 506491.00 | -1.2e-10 | — | OK |
| Geração do 1º ano | 506491.00 | — | 506491.00 | -1.2e-10 | — | OK |
| Meses com geração negativa no regime | 0 | — | 0 | 0.0e+0 | — | OK |
| Pior mês do regime | 131479.11 | — | 131479.11 | -2.9e-11 | — | OK |
| Ocupação média anual (ponderada pelos dias) | 0.620000 | — | 0.620000 | 0.0e+0 | — | OK |
| Margem operacional (antes dos custos do modelo) | 0.590989 | — | 0.590989 | -2.2e-16 | — | OK |
| Régua de margem do P6 | boa | — | boa | — | — | OK |
| Selo do P6 Receitas | Avançar | — | Avançar | — | — | OK |
| Equilíbrio: contribuição por noite | 738.71 | — | 738.71 | 0.0e+0 | — | OK |
| Equilíbrio: noites/ano | 2030.57 | — | 2030.57 | 0.0e+0 | — | OK |
| Equilíbrio: ocupação | 0.278161 | — | 0.278161 | 0.0e+0 | — | OK |
| Equilíbrio: folga de ocupação | 0.341839 | — | 0.341839 | 0.0e+0 | — | OK |
| Capital investido (CAPEX) | 6800000 | — | 6800000 | 0.0e+0 | — | OK |
| Déficit acumulado da rampa | 37913.18 | — | 37913.18 | -1.5e-11 | — | OK |
| Soma dos meses negativos do regime (giro) | 0 | — | 0 | 0.0e+0 | — | OK |
| Capital de giro A (6 × fixo) | 570000 | — | 570000 | 0.0e+0 | — | OK |
| Capital de giro B | 322913.18 | — | 322913.18 | 0.0e+0 | — | OK |
| Capital de giro usado | 570000 | 420000 | 570000 | 0.0e+0 | 150000 | DIVERGÊNCIA METODOLÓGICA |
| Captação (CAPEX + giro) | 7370000 | 7220000 | 7370000 | 0.0e+0 | 150000 | DIVERGÊNCIA METODOLÓGICA |
| Retorno anual (geração ÷ CAPEX) | 0.271087 | 0.280263 | 0.271087 | -1.1e-16 | -0.009176 | DIVERGÊNCIA METODOLÓGICA |
| Retorno do EBITDA | 0.271087 | — | 0.271087 | -1.1e-16 | — | OK |
| Payback simples (anos) | 4.414098 | 4.282663 | 4.414098 | 8.9e-16 | 0.131436 | DIVERGÊNCIA METODOLÓGICA |
| Payback descontado (anos) | 5.987434 | — | 5.987434 | 2.7e-15 | — | OK |
| Valor de saída (6 × EBITDA) | 11060330.00 | — | 11060330 | -3.7e-9 | — | OK |
| VPL sem saída (10%) | 3311462.10 | 3672199.95 | 3311462.10 | -3.3e-9 | -360737.85 | DIVERGÊNCIA METODOLÓGICA |
| VPL com saída | 7575698.11 | — | 7575698.11 | -4.7e-9 | — | OK |
| TIR sem saída | 0.192814 | 0.202117 | 0.192814 | -2.8e-13 | -0.009303 | DIVERGÊNCIA METODOLÓGICA |
| TIR com saída | 0.246544 | — | 0.246544 | 3.7e-14 | — | OK |
| Aviso de mais de uma TIR (com saída) | false | — | false | — | — | OK |
| Mês do projeto em que abre | 10 | — | 10 | 0.0e+0 | — | OK |
| Menor saldo da curva (36 meses) | 532086.82 | — | 532086.82 | -1.2e-10 | — | OK |
| Mês do menor saldo | 12 | — | 12 | 0.0e+0 | — | OK |
| Saldo no mês 36 | 3387596.39 | — | 3387596.39 | -2.3e-9 | — | OK |
| Colchão (menor saldo ÷ CAPEX) | 0.078248 | — | 0.078248 | -1.4e-17 | — | OK |
| Menor saldo com atraso de 6 meses | 528422.84 | — | 528422.84 | -1.2e-10 | — | OK |
| Estresse interno: geração com receita 30% menor | 409478.33 | — | 409478.33 | -5.2e-10 | — | OK |
| Estresse interno: CAPEX +25% | 8500000 | — | 8500000 | 0.0e+0 | — | OK |
| VPL com CAPEX +25% | 1611462.10 | — | 1611462.10 | -3.0e-9 | — | OK |
| Payback com CAPEX +25% | 5.336313 | — | 5.336313 | 8.9e-16 | — | OK |
| conservador.geracaoRegime | 887928.67 | — | 887928.67 | 0.0e+0 | — | OK |
| conservador.geracaoAno1 | -66915.69 | — | -66915.69 | -1.0e-10 | — | OK |
| conservador.ebitdaRegime | 887928.67 | — | 887928.67 | 0.0e+0 | — | OK |
| conservador.payback | 8.733634 | — | 8.733634 | 1.8e-15 | — | OK |
| conservador.vplSem | -2212103.04 | — | -2212103.04 | -4.7e-10 | — | OK |
| conservador.vplCom | -158093.41 | — | -158093.41 | -7.3e-10 | — | OK |
| otimista.geracaoRegime | 2757145.71 | — | 2757145.71 | 9.3e-10 | — | OK |
| otimista.geracaoAno1 | 1054870.60 | — | 1054870.60 | 7.0e-10 | — | OK |
| otimista.ebitdaRegime | 2757145.71 | — | 2757145.71 | 9.3e-10 | — | OK |
| otimista.payback | 3.083724 | — | 3.083724 | -8.9e-16 | — | OK |
| otimista.vplSem | 8593944.00 | — | 8593944.00 | 1.9e-9 | — | OK |
| otimista.vplCom | 14971938.15 | — | 14971938.15 | 3.7e-9 | — | OK |
| sensibilidade.diaria | 1239083.86 | — | 1239083.86 | -2.1e-9 | — | OK |
| sensibilidade.ocupacao | 1378630.83 | — | 1378630.83 | 9.3e-10 | — | OK |
| sensibilidade.fixo | 2610981.45 | — | 2610981.45 | -1.4e-9 | — | OK |
| sensibilidade.capex | 2631462.10 | — | 2631462.10 | -2.3e-9 | — | OK |
| Régua: 5 passos | [passa, passa, passa, passa, ajustar] | — | [passa, passa, passa, passa, ajustar] | — | — | OK |
| Régua: decisão | Ajustar | — | Ajustar | — | — | OK |

## C3E · Maior porte com estresse

| Campo | Esperado R2 (regra da ZAIOS) | Esperado R1 (regra do comando) | ZAIOS | Diferença (R2) | Diferença (R1) | Classificação |
|---|---|---|---|---|---|---|
| Receita de hospedagem | 3095784 | 3095784 | 3095784 | 0.0e+0 | 0 | OK |
| Diárias ocupadas (noites vendidas) | 3620.80 | — | 3620.80 | -4.5e-13 | — | OK |
| Outras receitas | 480000 | 480000 | 480000.00 | 5.8e-11 | 0.000000 | OK |
| Receita bruta consolidada | 3575784 | 3575784 | 3575784.00 | 4.7e-10 | 0.000000 | OK |
| Tributos sobre vendas (deduções) | 429094.08 | 429094.08 | 429094.08 | 5.8e-11 | 0.000000 | OK |
| Custos variáveis | 212420.27 | 212420.27 | 212420.27 | 2.9e-11 | 0.000000 | OK |
| Estadias (derivado: custos variáveis ÷ custo por estadia) | 1206.93 | — | 1206.93 | 0.0e+0 | — | OK |
| Custos fixos | 1311000 | 1311000 | 1311000 | 0.0e+0 | 0 | OK |
| Resultado operacional (antes dos custos do modelo) | 1623269.65 | — | 1623269.65 | 2.3e-10 | — | OK |
| Custos do modelo | 824851.92 | 762451.92 | 824851.92 | 0.0e+0 | 62400 | DIVERGÊNCIA METODOLÓGICA |
| Aluguel (12 × mensal) | 360000 | 360000 | 360000 | 0.0e+0 | 0 | OK |
| Gestão + royalties (derivado: custos do modelo − aluguel) | 464851.92 | 402451.92 | 464851.92 | -5.8e-11 | 62400 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA do regime | 798417.73 | 860817.73 | 798417.73 | 2.3e-10 | -62400.00 | DIVERGÊNCIA METODOLÓGICA |
| Geração de caixa do regime | 798417.73 | 860817.73 | 798417.73 | 2.3e-10 | -62400.00 | DIVERGÊNCIA METODOLÓGICA |
| Receita bruta do 1º ano (rampa) | 2145960.23 | — | 2145960.23 | 0.0e+0 | — | OK |
| EBITDA do 1º ano | -189011.08 | — | -189011.08 | 5.8e-11 | — | OK |
| Geração do 1º ano | -189011.08 | — | -189011.08 | 5.8e-11 | — | OK |
| Meses com geração negativa no regime | 0 | — | 0 | 0.0e+0 | — | OK |
| Pior mês do regime | 50184.79 | — | 50184.79 | 2.9e-11 | — | OK |
| Ocupação média anual (ponderada pelos dias) | 0.496000 | — | 0.496000 | -1.1e-16 | — | OK |
| Margem operacional (antes dos custos do modelo) | 0.453962 | — | 0.453962 | 0.0e+0 | — | OK |
| Régua de margem do P6 | boa | — | boa | — | — | OK |
| Selo do P6 Receitas | Avançar | — | Avançar | — | — | OK |
| Equilíbrio: contribuição por noite | 682.01 | — | 682.01 | 2.3e-13 | — | OK |
| Equilíbrio: noites/ano | 2450.11 | — | 2450.11 | -9.1e-13 | — | OK |
| Equilíbrio: ocupação | 0.335632 | — | 0.335632 | -1.1e-16 | — | OK |
| Equilíbrio: folga de ocupação | 0.160368 | — | 0.160368 | 0.0e+0 | — | OK |
| Capital investido (CAPEX) | 6800000 | — | 6800000 | 0.0e+0 | — | OK |
| Déficit acumulado da rampa | 282079.81 | — | 282079.81 | -5.8e-11 | — | OK |
| Soma dos meses negativos do regime (giro) | 0 | — | 0 | 0.0e+0 | — | OK |
| Capital de giro A (6 × fixo) | 655500 | — | 655500 | 0.0e+0 | — | OK |
| Capital de giro B | 609829.81 | — | 609829.81 | -1.2e-10 | — | OK |
| Capital de giro usado | 655500 | 420000 | 655500 | 0.0e+0 | 235500 | DIVERGÊNCIA METODOLÓGICA |
| Captação (CAPEX + giro) | 7455500 | 7220000 | 7455500 | 0.0e+0 | 235500 | DIVERGÊNCIA METODOLÓGICA |
| Retorno anual (geração ÷ CAPEX) | 0.117414 | 0.126591 | 0.117414 | 2.8e-17 | -0.009176 | DIVERGÊNCIA METODOLÓGICA |
| Retorno do EBITDA | 0.117414 | — | 0.117414 | 2.8e-17 | — | OK |
| Payback simples (anos) | 9.753577 | 9.075534 | 9.753577 | -3.6e-15 | 0.678043 | DIVERGÊNCIA METODOLÓGICA |
| Payback descontado (anos) | nulo | — | nulo | — | — | NÃO APLICÁVEL |
| Valor de saída (6 × EBITDA) | 4790506.40 | — | 4790506.40 | 9.3e-10 | — | OK |
| VPL sem saída (10%) | -2791731.22 | -2430993.37 | -2791731.22 | 9.3e-10 | -360737.85 | DIVERGÊNCIA METODOLÓGICA |
| VPL com saída | -944783.62 | — | -944783.62 | 1.2e-9 | — | OK |
| TIR sem saída | 0.004671 | 0.018485 | 0.004671 | -8.6e-14 | -0.013814 | DIVERGÊNCIA METODOLÓGICA |
| TIR com saída | 0.076898 | — | 0.076898 | -5.9e-14 | — | OK |
| Aviso de mais de uma TIR (com saída) | false | — | false | — | — | OK |
| Mês do projeto em que abre | 10 | — | 10 | 0.0e+0 | — | OK |
| Menor saldo da curva (36 meses) | 373420.19 | — | 373420.19 | 5.8e-11 | — | OK |
| Mês do menor saldo | 15 | — | 15 | 0.0e+0 | — | OK |
| Saldo no mês 36 | 1469585.23 | — | 1469585.23 | 1.2e-9 | — | OK |
| Colchão (menor saldo ÷ CAPEX) | 0.054915 | — | 0.054915 | 1.4e-17 | — | OK |
| Menor saldo com atraso de 6 meses | 377479.51 | — | 377479.51 | 1.2e-10 | — | OK |
| Estresse interno: geração com receita 30% menor | -274317.47 | — | -274317.47 | 0.0e+0 | — | OK |
| Estresse interno: CAPEX +25% | 8500000 | — | 8500000 | 0.0e+0 | — | OK |
| VPL com CAPEX +25% | -4491731.22 | — | -4491731.22 | 0.0e+0 | — | OK |
| Payback com CAPEX +25% | 11.88 | — | 11.88 | -5.3e-15 | — | OK |
| conservador.geracaoRegime | 89987.15 | — | 89987.15 | 2.9e-10 | — | OK |
| conservador.geracaoAno1 | -614166.48 | — | -614166.48 | 1.2e-10 | — | OK |
| conservador.ebitdaRegime | 89987.15 | — | 89987.15 | 2.9e-10 | — | OK |
| conservador.payback | 83.39 | — | 83.39 | -3.4e-13 | — | OK |
| conservador.vplSem | -6887207.60 | — | -6887207.60 | 0.0e+0 | — | OK |
| conservador.vplCom | -6679043.96 | — | -6679043.96 | 9.3e-10 | — | OK |
| otimista.geracaoRegime | 1477241.76 | — | 1477241.76 | 0.0e+0 | — | OK |
| otimista.geracaoAno1 | 218376.32 | — | 218376.32 | 1.2e-10 | — | OK |
| otimista.ebitdaRegime | 1477241.76 | — | 1477241.76 | 0.0e+0 | — | OK |
| otimista.payback | 5.455346 | — | 5.455346 | 0.0e+0 | — | OK |
| otimista.vplSem | 1132588.02 | — | 1132588.02 | -4.7e-10 | — | OK |
| otimista.vplCom | 4549831.91 | — | 4549831.91 | 0.0e+0 | — | OK |
| sensibilidade.diaria | -4342116.59 | — | -4342116.59 | 0.0e+0 | — | OK |
| sensibilidade.ocupacao | -4219315.26 | — | -4219315.26 | 0.0e+0 | — | OK |
| sensibilidade.fixo | -3597283.97 | — | -3597283.97 | 9.3e-10 | — | OK |
| sensibilidade.capex | -3471731.22 | — | -3471731.22 | 4.7e-10 | — | OK |
| Régua: 5 passos | [passa, passa, ajustar, redesenhar, ajustar] | — | [passa, passa, ajustar, redesenhar, ajustar] | — | — | OK |
| Régua: decisão | Redesenhar | — | Redesenhar | — | — | OK |
