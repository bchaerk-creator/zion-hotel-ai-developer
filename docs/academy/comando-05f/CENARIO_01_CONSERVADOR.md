# Cenário 1 · Empreendimento conservador

Comando 05F · 09/11/2026 · Valores **exclusivamente de teste**, não são parâmetros comerciais aprovados da Zion. Execução local da cópia da ZAIOS (commit `ec21ad5`), sem alterar nada.

Empreendimento pequeno, com baixa ocupação e pressão sobre os custos. Sem outras receitas: a base de gestão e royalties é a mesma nas duas regras (hospedagem = receita bruta).

## Entradas · C1

| Dado | Valor de teste | Como entrou na ZAIOS |
|---|---|---|
| Unidades | 3 | `unidades` = 3 |
| Diária média | R$ 450,00 | `diaria_*` em centavos |
| Ocupação média anual | 35,0% | `ocupacao_*` |
| Dias operacionais | 365 | Calendário fixo de 365 dias da ZAIOS |
| Outras receitas anuais | R$ 0,00 | `outras_pct` = 0,00000000 (outras ÷ diárias do regime) |
| Custo variável por estadia | R$ 85,00 | `custo_estadia` |
| Permanência média | 2,0 noites | `permanencia` |
| Custos fixos mensais | R$ 9.000,00 | `custo_fixo` no P6 e no P5 |
| Aluguel mensal | R$ 3.000,00 | `aluguel` |
| Gestão | 5% da receita de hospedagem | `gestao_pct` (a ZAIOS aplica sobre a receita bruta) |
| Royalties | 3% da receita de hospedagem | `royalty_pct` (idem) |
| Tributos sobre vendas | 8% da receita bruta | `deducoes_pct` |
| Investimento inicial | R$ 750.000,00 | 7 linhas do P5 (proporções do plano), contingência 0% |
| Capital de giro inicial | R$ 45.000,00 | Sem campo na ZAIOS: ela calcula o giro recomendado |
| Mês de abertura (adotado) | Janeiro | `mes_abertura`; mês do projeto sugerido pelo cronograma |

Outros campos exigidos pela ferramenta (valores adotados e justificativas): `PLANO_TESTES_COMPOSICAO.md`, seção 4.

## Comparação · C1 (72 campos)

Contagem: OK: 64 · DIVERGÊNCIA METODOLÓGICA: 2 · NÃO APLICÁVEL: 6.

Tolerâncias: R$ 0,01; frações, anos e noites 0,000001. Uma diferença ZAIOS − R2 da ordem de 1e-9 é ruído de ponto flutuante, abaixo da tolerância.

| Grupo | Campo | Esperado independente (regra da ZAIOS, R2) | Esperado pela regra do comando (R1) | Valor ZAIOS | Diferença ZAIOS − R2 | Diferença ZAIOS − R1 | Classificação |
|---|---|---|---|---|---|---|---|
| Receita | Receita de hospedagem | R$ 172.462,50 | R$ 172.462,50 | R$ 172.462,50 | 2.9e-11 | — | OK |
| Receita | Diárias ocupadas (noites vendidas) | 383,25 | — | 383,25 | 1.1e-13 | — | OK |
| Receita | Estadias (derivado: custos variáveis ÷ custo por estadia) | 191,62 | — | 191,62 | 2.8e-14 | — | OK |
| Receita | Outras receitas | R$ 0,00 | R$ 0,00 | R$ 0,00 | 0 | — | OK |
| Receita | Receita bruta consolidada | R$ 172.462,50 | R$ 172.462,50 | R$ 172.462,50 | 2.9e-11 | — | OK |
| Receita | Ocupação média anual (ponderada pelos dias) | 35,0000% | — | 35,0000% | 1.1e-16 | — | OK |
| Deduções | Tributos sobre vendas (deduções) | R$ 13.797,00 | R$ 13.797,00 | R$ 13.797,00 | 1.8e-12 | — | OK |
| Despesas | Custos variáveis | R$ 16.288,12 | R$ 16.288,12 | R$ 16.288,12 | 1.8e-12 | — | OK |
| Despesas | Custos fixos | R$ 108.000,00 | R$ 108.000,00 | R$ 108.000,00 | 0 | — | OK |
| Despesas | Resultado operacional (antes dos custos do modelo) | R$ 34.377,37 | — | R$ 34.377,37 | -7.3e-12 | — | OK |
| Despesas | Aluguel (12 × mensal) | R$ 36.000,00 | R$ 36.000,00 | R$ 36.000,00 | 0 | — | OK |
| Despesas | Gestão + royalties (derivado: custos do modelo − aluguel) | R$ 13.797,00 | R$ 13.797,00 | R$ 13.797,00 | 1.8e-12 | — | OK |
| Despesas | Custos do modelo | R$ 49.797,00 | R$ 49.797,00 | R$ 49.797,00 | 0 | — | OK |
| EBITDA e geração | EBITDA do regime | R$ -15.419,63 | R$ -15.419,63 | R$ -15.419,63 | -9.1e-12 | — | OK |
| EBITDA e geração | Geração de caixa do regime | R$ -15.419,63 | R$ -15.419,63 | R$ -15.419,63 | -9.1e-12 | — | OK |
| EBITDA e geração | Receita bruta do 1º ano (rampa) | R$ 103.713,75 | — | R$ 103.713,75 | 1.5e-11 | — | OK |
| EBITDA e geração | EBITDA do 1º ano | R$ -66.675,64 | — | R$ -66.675,64 | 1.5e-11 | — | OK |
| EBITDA e geração | Geração do 1º ano | R$ -66.675,64 | — | R$ -66.675,64 | 1.5e-11 | — | OK |
| EBITDA e geração | Meses com geração negativa no regime | 12 | — | 12 | 0 | — | OK |
| EBITDA e geração | Pior mês do regime | R$ -2.136,30 | — | R$ -2.136,30 | -4.5e-13 | — | OK |
| EBITDA e geração | Margem operacional (antes dos custos do modelo) | 19,9332% | — | 19,9332% | -5.6e-17 | — | OK |
| EBITDA e geração | Régua de margem do P6 | apertada | — | apertada | — | — | OK |
| EBITDA e geração | Selo do P6 Receitas | Ajustar | — | Ajustar | — | — | OK |
| EBITDA e geração | Equilíbrio: contribuição por noite | R$ 335,50 | — | R$ 335,50 | -5.7e-14 | — | OK |
| EBITDA e geração | Equilíbrio: noites/ano | 429,21 | — | 429,21 | 5.7e-14 | — | OK |
| EBITDA e geração | Equilíbrio: ocupação | 39,1973% | — | 39,1973% | 5.6e-17 | — | OK |
| EBITDA e geração | Equilíbrio: folga de ocupação | -4,1973% | — | -4,1973% | 5.6e-17 | — | OK |
| Capital e fluxo de caixa | Capital investido (CAPEX) | R$ 750.000,00 | — | R$ 750.000,00 | 0 | — | OK |
| Capital e fluxo de caixa | Déficit acumulado da rampa | R$ 66.675,64 | — | R$ 66.675,64 | -1.5e-11 | — | OK |
| Capital e fluxo de caixa | Soma dos meses negativos do regime (giro) | R$ 15.419,63 | — | R$ 15.419,63 | 9.1e-12 | — | OK |
| Capital e fluxo de caixa | Capital de giro A (6 × fixo) | R$ 54.000,00 | — | R$ 54.000,00 | 0 | — | OK |
| Capital e fluxo de caixa | Capital de giro B | R$ 109.095,26 | — | R$ 109.095,26 | 1.5e-11 | — | OK |
| Capital e fluxo de caixa | Capital de giro usado | R$ 109.095,26 | R$ 45.000,00 | R$ 109.095,26 | 1.5e-11 | R$ 64.095,26 | DIVERGÊNCIA METODOLÓGICA |
| Capital e fluxo de caixa | Captação (CAPEX + giro) | R$ 859.095,26 | R$ 795.000,00 | R$ 859.095,26 | -1.2e-10 | R$ 64.095,26 | DIVERGÊNCIA METODOLÓGICA |
| Capital e fluxo de caixa | Mês do projeto em que abre | 10 | — | 10 | 0 | — | OK |
| Capital e fluxo de caixa | Menor saldo da curva (36 meses) | R$ 22.704,75 | — | R$ 22.704,75 | -2.9e-11 | — | OK |
| Capital e fluxo de caixa | Mês do menor saldo | 36 | — | 36 | 0 | — | OK |
| Capital e fluxo de caixa | Saldo no mês 36 | R$ 22.704,75 | — | R$ 22.704,75 | -2.9e-11 | — | OK |
| Capital e fluxo de caixa | Colchão (menor saldo ÷ CAPEX) | 3,0273% | — | 3,0273% | -3.8e-17 | — | OK |
| Capital e fluxo de caixa | Menor saldo com atraso de 6 meses | R$ 30.608,31 | — | R$ 30.608,31 | -4.4e-11 | — | OK |
| Indicadores | Retorno anual (geração ÷ CAPEX) | -2,0560% | -2,0560% | -2,0560% | -1.0e-17 | — | OK |
| Indicadores | Retorno do EBITDA | -2,0560% | — | -2,0560% | -1.0e-17 | — | OK |
| Indicadores | Payback simples (anos) | não calculado (nulo) | não calculado (nulo) | não calculado (nulo) | — | — | NÃO APLICÁVEL |
| Indicadores | Payback descontado (anos) | não calculado (nulo) | — | não calculado (nulo) | — | — | NÃO APLICÁVEL |
| Indicadores | Valor de saída (6 × EBITDA) | R$ -92.517,75 | — | R$ -92.517,75 | -4.4e-11 | — | OK |
| Indicadores | VPL sem saída (10%) | R$ -891.343,30 | R$ -891.343,30 | R$ -891.343,30 | 1.2e-10 | — | OK |
| Indicadores | VPL com saída | R$ -927.012,89 | — | R$ -927.012,89 | 1.2e-10 | — | OK |
| Indicadores | TIR sem saída | não calculado (nulo) | não calculado (nulo) | não calculado (nulo) | — | — | NÃO APLICÁVEL |
| Indicadores | TIR com saída | não calculado (nulo) | — | não calculado (nulo) | — | — | NÃO APLICÁVEL |
| Indicadores | Aviso de mais de uma TIR (com saída) | não | — | não | — | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Estresse interno: geração com receita 30% menor | R$ -67.158,38 | — | R$ -67.158,38 | -1.5e-11 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Estresse interno: CAPEX +25% | R$ 937.500,00 | — | R$ 937.500,00 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | VPL com CAPEX +25% | R$ -1.078.843,30 | — | R$ -1.078.843,30 | 2.3e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Payback com CAPEX +25% | não calculado (nulo) | — | não calculado (nulo) | — | — | NÃO APLICÁVEL |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.geracaoRegime | R$ -52.725,18 | — | R$ -52.725,18 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.geracaoAno1 | R$ -89.110,07 | — | R$ -89.110,07 | -1.5e-11 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.ebitdaRegime | R$ -52.725,18 | — | R$ -52.725,18 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.payback | não calculado (nulo) | — | não calculado (nulo) | — | — | NÃO APLICÁVEL |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.vplSem | R$ -1.107.050,58 | — | R$ -1.107.050,58 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.vplCom | R$ -1.229.017,62 | — | R$ -1.229.017,62 | -2.3e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.geracaoRegime | R$ 20.527,31 | — | R$ 20.527,31 | 1.8e-11 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.geracaoAno1 | R$ -45.058,23 | — | R$ -45.058,23 | 1.5e-11 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.ebitdaRegime | R$ 20.527,31 | — | R$ 20.527,31 | 1.8e-11 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.payback | 39,7317 anos | — | 39,7317 anos | -3.6e-14 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.vplSem | R$ -683.491,80 | — | R$ -683.491,80 | -1.2e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.vplCom | R$ -636.006,80 | — | R$ -636.006,80 | -1.2e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.diaria | R$ -975.108,81 | — | R$ -975.108,81 | 1.2e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.capex | R$ -966.343,30 | — | R$ -966.343,30 | 2.3e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.ocupacao | -96.569.073,2324% | — | -96.569.073,2324% | 1.2e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.fixo | R$ -957.704,62 | — | R$ -957.704,62 | -3.5e-10 | — | OK |
| Régua e decisão | Régua: 5 passos | redesenhar, redesenhar, redesenhar, redesenhar, ajustar | — | redesenhar, redesenhar, redesenhar, redesenhar, ajustar | — | — | OK |
| Régua e decisão | Régua: decisão | Redesenhar | — | Redesenhar | — | — | OK |

## Leitura econômica

**Matemática:** os 72 campos conferem com a regra documentada. Os indicadores sem sentido neste cenário não recebem número:
- payback: "Não se paga.";
- payback descontado: "Não se paga em 10 anos.";
- TIR: "Não existe TIR para este fluxo.".

Esse é o tratamento correto de resultado negativo.

**O resultado faz sentido?** Sim, na essência.
- O EBITDA do regime é **negativo: −R$ 15.419,63**, cerca de −8,9% da receita.
- A ocupação de equilíbrio, com aluguel, gestão e royalties, é 39,20%, contra 35% previstos.
- A régua decide **Redesenhar**: 4 passos em "redesenhar" e o colchão em "ajustar".

**Pontos de atenção na apresentação** (nenhum é erro de conta):

| # | Achado | Por que importa | Classificação |
|---|---|---|---|
| O8 | A **margem operacional** de 19,93% é calculada **antes** de aluguel, gestão e royalties e aparece na régua como "apertada". O EBITDA é negativo | Um leitor pode concluir que a operação "fecha, apertada", quando o resultado depois dos custos do modelo é prejuízo. O selo do P6 ficou "Ajustar" porque a folga do equilíbrio é negativa, não por causa da margem | LIMITAÇÃO (apresentação) |
| O9 | O **valor de saída** = 6 × EBITDA negativo = **−R$ 92.517,75**, somado ao ano 10. O VPL com saída (−R$ 927.012,89) fica pior que sem saída | Um múltiplo de EBITDA negativo não representa preço de venda. A D7-C não trata o caso | DIVERGÊNCIA METODOLÓGICA em potencial (D7-C, a classificar) |
| O10 | A curva de 36 meses termina no menor saldo (R$ 22.704,75 no mês 36), que continua caindo, e o colchão sai em "ajustar" (3,03%) | O caixa se esgota depois do horizonte. O colchão positivo não captura a queima contínua. A decisão geral já é Redesenhar, então aqui não há conclusão indevida | LIMITAÇÃO (horizonte) |
| — | O **retorno anual** negativo (−2,06%) aparece como número | É coerente (geração ÷ CAPEX), desde que exibido com o sinal | OK |
| — | Com o **capital de giro informado** (R$ 45.000), a curva fica negativa (−R$ 41.390,51) e o colchão vira −5,52% (passo 5 em "redesenhar"). A ZAIOS não aceita o giro informado e recomenda R$ 109.095,26 (giro B = déficit da rampa R$ 66.675,64 + meses negativos R$ 15.419,63 + 3 × fixo R$ 27.000) | O giro informado não cobre o déficit do 1º ano. A ZAIOS é mais prudente que o dado de teste | DIVERGÊNCIA METODOLÓGICA (giro calculado x informado) |
| O12 | O giro A = 6 × fixo **não inclui o aluguel** (R$ 3.000/mês): R$ 54.000 em vez de R$ 72.000 | O aluguel é um custo fixo mensal, mas fica fora da base do giro A. Aqui o giro B prevalece, então não muda o resultado | Observação (a classificar) |


## Evidência

- Execução: `testes/financeiro/resultados/2026-11-09-05f/resultado_05f.json` e `RESULTADO_05F.md`.
- Esperados: `testes/financeiro/independente/esperados_05f.json`, gerados por `composicao_05f_referencia.py`.
- Entradas: `testes/financeiro/composicao_05f/cenarios_05f.json`.
