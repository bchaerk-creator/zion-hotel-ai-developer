# Cenário 2 · Empreendimento intermediário

Comando 05F · 09/11/2026 · Valores **exclusivamente de teste**, não são parâmetros comerciais aprovados da Zion. Execução local da cópia da ZAIOS (commit `ec21ad5`), sem alterar nada.

Múltiplas fontes de receita, sazonalidade e estrutura intermediária. Abertura em março, para testar a rampa fora de janeiro.

## Entradas · C2

| Dado | Valor de teste | Como entrou na ZAIOS |
|---|---|---|
| Unidades | 8 | `unidades` = 8 |
| Diária média | R$ 690,00 | `diaria_*` em centavos |
| Ocupação média anual | 58,0% | `ocupacao_*` |
| Dias operacionais | 365 | Calendário fixo de 365 dias da ZAIOS |
| Outras receitas anuais | R$ 180.000,00 | `outras_pct` = 0,15403257 (outras ÷ diárias do regime) |
| Custo variável por estadia | R$ 120,00 | `custo_estadia` |
| Permanência média | 2,5 noites | `permanencia` |
| Custos fixos mensais | R$ 28.000,00 | `custo_fixo` no P6 e no P5 |
| Aluguel mensal | R$ 8.000,00 | `aluguel` |
| Gestão | 7% da receita de hospedagem | `gestao_pct` (a ZAIOS aplica sobre a receita bruta) |
| Royalties | 4% da receita de hospedagem | `royalty_pct` (idem) |
| Tributos sobre vendas | 10% da receita bruta | `deducoes_pct` |
| Investimento inicial | R$ 2.100.000,00 | 7 linhas do P5 (proporções do plano), contingência 0% |
| Capital de giro inicial | R$ 120.000,00 | Sem campo na ZAIOS: ela calcula o giro recomendado |
| Mês de abertura (adotado) | Março | `mes_abertura`; mês do projeto sugerido pelo cronograma |

Outros campos exigidos pela ferramenta (valores adotados e justificativas): `PLANO_TESTES_COMPOSICAO.md`, seção 4.

## Comparação · C2 (72 campos)

Contagem: OK: 62 · DIVERGÊNCIA METODOLÓGICA: 10.

Tolerâncias: R$ 0,01; frações, anos e noites 0,000001. Uma diferença ZAIOS − R2 da ordem de 1e-9 é ruído de ponto flutuante, abaixo da tolerância.

| Grupo | Campo | Esperado independente (regra da ZAIOS, R2) | Esperado pela regra do comando (R1) | Valor ZAIOS | Diferença ZAIOS − R2 | Diferença ZAIOS − R1 | Classificação |
|---|---|---|---|---|---|---|---|
| Receita | Receita de hospedagem | R$ 1.168.584,00 | R$ 1.168.584,00 | R$ 1.168.584,00 | 0 | — | OK |
| Receita | Diárias ocupadas (noites vendidas) | 1.693,60 | — | 1.693,60 | 0 | — | OK |
| Receita | Estadias (derivado: custos variáveis ÷ custo por estadia) | 677,44 | — | 677,44 | 0 | — | OK |
| Receita | Outras receitas | R$ 180.000,00 | R$ 180.000,00 | R$ 180.000,00 | -5.8e-11 | — | OK |
| Receita | Receita bruta consolidada | R$ 1.348.584,00 | R$ 1.348.584,00 | R$ 1.348.584,00 | 0 | — | OK |
| Receita | Ocupação média anual (ponderada pelos dias) | 58,0000% | — | 58,0000% | 0 | — | OK |
| Deduções | Tributos sobre vendas (deduções) | R$ 134.858,40 | R$ 134.858,40 | R$ 134.858,40 | 0 | — | OK |
| Despesas | Custos variáveis | R$ 81.292,80 | R$ 81.292,80 | R$ 81.292,80 | 0 | — | OK |
| Despesas | Custos fixos | R$ 336.000,00 | R$ 336.000,00 | R$ 336.000,00 | 0 | — | OK |
| Despesas | Resultado operacional (antes dos custos do modelo) | R$ 796.432,80 | — | R$ 796.432,80 | -2.3e-10 | — | OK |
| Despesas | Aluguel (12 × mensal) | R$ 96.000,00 | R$ 96.000,00 | R$ 96.000,00 | 0 | — | OK |
| Despesas | Gestão + royalties (derivado: custos do modelo − aluguel) | R$ 148.344,24 | R$ 128.544,24 | R$ 148.344,24 | -2.9e-11 | R$ 19.800,00 | DIVERGÊNCIA METODOLÓGICA |
| Despesas | Custos do modelo | R$ 244.344,24 | R$ 224.544,24 | R$ 244.344,24 | -2.9e-11 | R$ 19.800,00 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA e geração | EBITDA do regime | R$ 552.088,56 | R$ 571.888,56 | R$ 552.088,56 | -1.2e-10 | R$ -19.800,00 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA e geração | Geração de caixa do regime | R$ 552.088,56 | R$ 571.888,56 | R$ 552.088,56 | -1.2e-10 | R$ -19.800,00 | DIVERGÊNCIA METODOLÓGICA |
| EBITDA e geração | Receita bruta do 1º ano (rampa) | R$ 830.337,88 | — | R$ 830.337,88 | 0 | — | OK |
| EBITDA e geração | EBITDA do 1º ano | R$ 173.914,06 | — | R$ 173.914,06 | 0 | — | OK |
| EBITDA e geração | Geração do 1º ano | R$ 173.914,06 | — | R$ 173.914,06 | 0 | — | OK |
| EBITDA e geração | Meses com geração negativa no regime | 0 | — | 0 | 0 | — | OK |
| EBITDA e geração | Pior mês do regime | R$ 21.176,61 | — | R$ 21.176,61 | -1.1e-11 | — | OK |
| EBITDA e geração | Margem operacional (antes dos custos do modelo) | 59,0570% | — | 59,0570% | -2.2e-16 | — | OK |
| EBITDA e geração | Régua de margem do P6 | boa | — | boa | — | — | OK |
| EBITDA e geração | Selo do P6 Receitas | Avançar | — | Avançar | — | — | OK |
| EBITDA e geração | Equilíbrio: contribuição por noite | R$ 581,06 | — | R$ 581,06 | -1.1e-13 | — | OK |
| EBITDA e geração | Equilíbrio: noites/ano | 743,46 | — | 743,46 | 1.1e-13 | — | OK |
| EBITDA e geração | Equilíbrio: ocupação | 25,4611% | — | 25,4611% | 5.6e-17 | — | OK |
| EBITDA e geração | Equilíbrio: folga de ocupação | 32,5389% | — | 32,5389% | -5.6e-17 | — | OK |
| Capital e fluxo de caixa | Capital investido (CAPEX) | R$ 2.100.000,00 | — | R$ 2.100.000,00 | 0 | — | OK |
| Capital e fluxo de caixa | Déficit acumulado da rampa | R$ 35.476,00 | — | R$ 35.476,00 | 0 | — | OK |
| Capital e fluxo de caixa | Soma dos meses negativos do regime (giro) | R$ 0,00 | — | R$ 0,00 | 0 | — | OK |
| Capital e fluxo de caixa | Capital de giro A (6 × fixo) | R$ 168.000,00 | — | R$ 168.000,00 | 0 | — | OK |
| Capital e fluxo de caixa | Capital de giro B | R$ 119.476,00 | — | R$ 119.476,00 | -1.5e-11 | — | OK |
| Capital e fluxo de caixa | Capital de giro usado | R$ 168.000,00 | R$ 120.000,00 | R$ 168.000,00 | 0 | R$ 48.000,00 | DIVERGÊNCIA METODOLÓGICA |
| Capital e fluxo de caixa | Captação (CAPEX + giro) | R$ 2.268.000,00 | R$ 2.220.000,00 | R$ 2.268.000,00 | 0 | R$ 48.000,00 | DIVERGÊNCIA METODOLÓGICA |
| Capital e fluxo de caixa | Mês do projeto em que abre | 10 | — | 10 | 0 | — | OK |
| Capital e fluxo de caixa | Menor saldo da curva (36 meses) | R$ 132.524,00 | — | R$ 132.524,00 | -2.9e-11 | — | OK |
| Capital e fluxo de caixa | Mês do menor saldo | 13 | — | 13 | 0 | — | OK |
| Capital e fluxo de caixa | Saldo no mês 36 | R$ 985.841,86 | — | R$ 985.841,86 | 2.3e-10 | — | OK |
| Capital e fluxo de caixa | Colchão (menor saldo ÷ CAPEX) | 6,3107% | — | 6,3107% | -1.4e-17 | — | OK |
| Capital e fluxo de caixa | Menor saldo com atraso de 6 meses | R$ 148.656,29 | — | R$ 148.656,29 | 0 | — | OK |
| Indicadores | Retorno anual (geração ÷ CAPEX) | 26,2899% | 27,2328% | 26,2899% | -1.1e-16 | -0,9429% | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Retorno do EBITDA | 26,2899% | — | 26,2899% | -1.1e-16 | — | OK |
| Indicadores | Payback simples (anos) | 4,4887 anos | 4,3466 anos | 4,4887 anos | 0 | 0,1421 anos | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | Payback descontado (anos) | 6,1387 anos | — | 6,1387 anos | 8.9e-16 | — | OK |
| Indicadores | Valor de saída (6 × EBITDA) | R$ 3.312.531,36 | — | R$ 3.312.531,36 | -9.3e-10 | — | OK |
| Indicadores | VPL sem saída (10%) | R$ 948.550,21 | R$ 1.063.295,43 | R$ 948.550,21 | -4.7e-10 | R$ -114.745,23 | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | VPL com saída | R$ 2.225.674,45 | — | R$ 2.225.674,45 | -9.3e-10 | — | OK |
| Indicadores | TIR sem saída | 18,7251% | 19,6995% | 18,7251% | -1.3e-13 | -0,9744% | DIVERGÊNCIA METODOLÓGICA |
| Indicadores | TIR com saída | 24,1441% | — | 24,1441% | 1.1e-13 | — | OK |
| Indicadores | Aviso de mais de uma TIR (com saída) | não | — | não | — | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Estresse interno: geração com receita 30% menor | R$ 147.513,36 | — | R$ 147.513,36 | -1.2e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Estresse interno: CAPEX +25% | R$ 2.625.000,00 | — | R$ 2.625.000,00 | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | VPL com CAPEX +25% | R$ 423.550,21 | — | R$ 423.550,21 | -8.7e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | Payback com CAPEX +25% | 5,4397 anos | — | 5,4397 anos | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.geracaoRegime | R$ 270.040,34 | — | R$ 270.040,34 | -5.8e-11 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.geracaoAno1 | R$ 253,90 | — | R$ 253,90 | -8.7e-12 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.ebitdaRegime | R$ 270.040,34 | — | R$ 270.040,34 | -5.8e-11 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.payback | 8,7757 anos | — | 8,7757 anos | 3.6e-15 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.vplSem | R$ -685.979,42 | — | R$ -685.979,42 | -3.5e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | conservador.vplCom | R$ -61.305,97 | — | R$ -61.305,97 | -7.3e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.geracaoRegime | R$ 822.220,70 | — | R$ 822.220,70 | 1.2e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.geracaoAno1 | R$ 340.237,37 | — | R$ 340.237,37 | -1.7e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.ebitdaRegime | R$ 822.220,70 | — | R$ 822.220,70 | 1.2e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.payback | 3,1403 anos | — | 3,1403 anos | 0 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.vplSem | R$ 2.514.023,61 | — | R$ 2.514.023,61 | 4.7e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | otimista.vplCom | R$ 4.416.033,65 | — | R$ 4.416.033,65 | 1.9e-09 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.diaria | R$ 331.138,98 | — | R$ 331.138,98 | 5.8e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.ocupacao | 37.824.988,9356% | — | 37.824.988,9356% | 1.7e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.capex | R$ 738.550,21 | — | R$ 738.550,21 | -7.0e-10 | — | OK |
| Cenários, sensibilidade e estresse internos da ZAIOS | sensibilidade.fixo | R$ 742.092,75 | — | R$ 742.092,75 | -8.1e-10 | — | OK |
| Régua e decisão | Régua: 5 passos | passa, passa, passa, passa, ajustar | — | passa, passa, passa, passa, ajustar | — | — | OK |
| Régua e decisão | Régua: decisão | Ajustar | — | Ajustar | — | — | OK |

## Sazonalidade utilizada

A ZAIOS trabalha com **3 temporadas** (diária e ocupação por temporada). Ela não tem multiplicadores mensais. Distribuição adotada:

| Mês | Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Temporada | alta | alta | média | baixa | baixa | baixa | alta | média | baixa | média | média | alta |
| Ocupação | 75% | 75% | 58% | 41% | 41% | 41% | 75% | 58% | 41% | 58% | 58% | 75% |
| Dias | 31 | 28 | 31 | 30 | 31 | 30 | 31 | 31 | 30 | 31 | 30 | 31 |

- **Média ponderada pelos dias:** (121 × 0,75 + 123 × 0,58 + 121 × 0,41) ÷ 365 = 211,70 ÷ 365 = **58,0000%**.
  - A ZAIOS reproduz a mesma ocupação média anual: 58,0000%.
- A média aritmética simples dos 12 meses também dá 58%, **só porque** a alta e a baixa têm o mesmo número de dias (121) e desvios simétricos (±17 p.p.). Em outra distribuição as duas médias seriam diferentes. O cálculo usa sempre os dias de cada mês.
- A diária de R$ 690 é a mesma nas três temporadas, para que a diária média anual seja exatamente R$ 690.

## Efeito da sazonalidade (controle independente)

O controle sem sazonalidade foi calculado só no Python, para ilustrar o efeito. A mecânica mês a mês da ZAIOS foi conferida pelos campos que dependem do mês (pior mês, 1º ano, giro B, curva), todos OK.

| Indicador | C2 com sazonalidade | Controle sem sazonalidade (58% todo mês) | Efeito |
|---|---|---|---|
| Receita bruta do regime | R$ 1.348.584,00 | R$ 1.348.584,00 | R$ 0,00 |
| EBITDA do regime | R$ 552.088,56 | R$ 552.088,56 | R$ 0,00 |
| Pior mês do regime | R$ 21.176,61 | R$ 39.491,73 | R$ -18.315,11 |
| Geração do 1º ano (abertura em março) | R$ 173.914,06 | R$ 157.239,88 | R$ 16.674,19 |
| Capital de giro B | R$ 119.476,00 | R$ 92.782,30 | R$ 26.693,69 |
| Capital de giro usado | R$ 168.000,00 | R$ 168.000,00 | R$ 0,00 |
| Menor saldo da curva | R$ 132.524,00 | R$ 159.217,70 | R$ -26.693,69 |
| Colchão | 6,3107% | 7,5818% | -1,2711 p.p. |
| VPL sem saída | R$ 948.550,21 | R$ 933.391,86 | R$ 15.158,35 |

A receita e o EBITDA anuais não mudam, porque a ocupação ponderada é a mesma. O que muda é a distribuição no tempo:
- 1º ano: a rampa cai em meses de temporadas diferentes;
- pior mês;
- curva de caixa;
- colchão.

## Leitura econômica

**Matemática:** os 72 campos conferem com a regra documentada da ZAIOS.

**Divergências metodológicas (10), todas com a mesma causa: duas regras do comando que a ZAIOS não segue.**

1. **Base de gestão e royalties (nova observação O11).**
   - O comando aplica 11% (7% + 4%) sobre a **receita de hospedagem**. A ZAIOS aplica sobre a **receita bruta**, que inclui as outras receitas.
   - Diferença: 11% × R$ 180.000 = **R$ 19.800/ano** a mais de custos do modelo na ZAIOS.
   - Efeito em cascata:
     - EBITDA R$ 552.088,56 x R$ 571.888,56;
     - retorno 26,29% x 27,23%;
     - payback 4,49 x 4,35 anos;
     - VPL R$ 948.550,21 x R$ 1.063.295,43 (−R$ 114.745,23);
     - TIR 18,73% x 19,70%.
   - A ZAIOS é a mais conservadora das duas. A decisão não muda (Ajustar nas duas).
2. **Capital de giro.**
   - A ZAIOS calcula R$ 168.000 (giro A = 6 × R$ 28.000, maior que o giro B de R$ 119.476). O comando informa R$ 120.000.
   - Captação: R$ 2.268.000 x R$ 2.220.000.

**Coerência com as outras receitas:** a inclusão de R$ 180.000 aumenta, de forma proporcional e coerente:
- os tributos (+R$ 18.000, 10%);
- os custos do modelo (+R$ 19.800, pela regra da ZAIOS);
- o EBITDA, pelo líquido.

Os custos variáveis não mudam: são por estadia.

Duas limitações da conversão:
- **as outras receitas acompanham a ocupação mês a mês e a rampa do 1º ano**, porque na ZAIOS são % das diárias;
- a mesma alíquota de 10% sobre todas as fontes é só hipótese de teste (D14).

**O resultado faz sentido?** Sim.
- Margem operacional de 59,06% e EBITDA de 40,94% da receita.
- Equilíbrio em 25,46% de ocupação, com folga de 32,54 p.p.
- Payback de 4,49 anos e TIR de 18,73%, acima da taxa de 10%.
- A régua decide **Ajustar** só por causa do colchão de 6,31%, abaixo do limite provisório de 10% (H4).

Atenção: no **cenário conservador interno** (diária −10%, ocupação −20%), o VPL sem saída fica **negativo** (−R$ 685.979,42) e o payback vai a 8,78 anos. O passo 2 passa porque olha só se a geração é positiva. Ao mesmo tempo, o P6 mostra o selo **"Avançar"**: é o veredito antecipado (risco já registrado), e o leitor vê dois selos diferentes (O8).


## Evidência

- Execução: `testes/financeiro/resultados/2026-11-09-05f/resultado_05f.json` e `RESULTADO_05F.md`.
- Esperados: `testes/financeiro/independente/esperados_05f.json`, gerados por `composicao_05f_referencia.py`.
- Entradas: `testes/financeiro/composicao_05f/cenarios_05f.json`.
