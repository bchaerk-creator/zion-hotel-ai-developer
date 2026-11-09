# Matriz dos testes complementares

Comando 05E · 09/11/2026 · Testes separados da produção (`testes/financeiro/casos/c01_complementares.js` e `c02_zaios_complementares.js`). Nenhuma fórmula ou ferramenta foi alterada.

## Como ler

- **Esperado:** vem de um cálculo independente.
  - `testes/financeiro/independente/complementares_referencia.py` gera `esperados_complementares.json`. É escrito em Python e não importa nem executa código das ferramentas.
  - Para G2/G3, o esperado são os exemplos documentados no FORMULAS.md da ZAIOS, que é texto e não código.
- **Observado:** o que a ferramenta devolve quando é executada sem alteração.
- **Tolerância:**
  - R$ 0,01 para valores em reais;
  - 0,0001 para frações (0,01 p.p.);
  - 0,01 ano;
  - 0,001 mês no fôlego;
  - meio centavo nos valores em centavos da G2/G3;
  - igualdade exata nos textos e listas.
- **Tipo:**
  - **fórmula:** confere a matemática;
  - **divergência:** a matemática está certa, mas difere da metodologia aprovada;
  - **limitação:** depende de uma decisão pendente ou de uma classificação ainda não feita.
- **Independência:**
  - **Total:** fórmula tirada do dicionário ou da documentação da ferramenta.
  - **Parcial:** a fórmula foi descrita a partir da leitura do código no Comando 05B e reimplementada em outra linguagem, com entradas novas. Prova que o código faz o que diz, mas não que a regra está certa.

Os valores observados, caso a caso, estão em `RESULTADOS_EVIDENCIAS.md`.

## 1. ZAIOS

| Grupo | Entradas | Fórmula de referência | Esperado (independente) | Casos | Independência | Limitações |
|---|---|---|---|---|---|---|
| **Custos do modelo e EBITDA** (aluguel, gestão, royalty) | Z-base (3 unid., R$ 680, 38%, deduções 17%, R$ 80/noite, fixo R$ 6.000) + quebra 1% + reserva 4% + aluguel R$ 1.000/mês + gestão 10% + royalty 3% | Custos do modelo = aluguel × 12 + receita bruta × (gestão + royalty); EBITDA = resultado operacional − custos do modelo; geração = EBITDA − reserva | custos 48.783,24; EBITDA 77.946,12; geração 66.628,20; resultado operacional 126.729,36 | 4 | Total (dicionário v0.4) | Um cenário; base da gestão e do royalty = receita bruta |
| **Outras receitas e custo por estadia** | Z-base + outras receitas 10% + R$ 60 por estadia, permanência média 2,5 | Bruta = diárias × 1,10; estadias = noites ÷ 2,5; custo variável = noites × 80 + estadias × 60 | bruta 311.242,80; variáveis 43.274,40; operacional 143.057,124 | 3 | Total | D9 e D14 pendentes (noite ou estadia; taxa de limpeza) |
| **Sazonalidade** | Alta dez–fev (R$ 900, 60%), média (R$ 680, 38%), baixa abr–jun (R$ 500, 20%) | Soma mês a mês com os dias reais de cada mês | bruta 315.736,80; operacional 155.952,744 | 2 | Total | — |
| **Composição: integração com as entradas** | Entradas dos testes da própria ZAIOS (P5: 3 unidades, CAPEX F01, contingência 25%, terreno R$ 200.000; P6: R$ 680, 38%, deduções 17%, fixo R$ 10.500; taxa 10%, múltiplo 6×) passadas por `calcularCapex` → `lerMapaCapex` → `calcularViabilidade` | Cronograma do P5 → mês sugerido; rampa 40/50/75% a partir da abertura | mês sugerido 10 | 1 | Total | Cenário único |
| **Primeiro ano de operação** | idem, abertura em janeiro | Geração do 1º ano = Σ meses com fator de rampa | 15.229,812 | 1 | Total | Sem pró-labore no cenário |
| **Capital de giro** | idem | A = 6 × fixo; B = maior déficit acumulado do 1º ano + meses negativos do regime + 3 × fixo; recomendado = o maior | 63.000 (A; B = 42.061,60) | 1 | Total | — |
| **Captação** | idem | CAPEX com contingência (1.237.400) + capital de giro recomendado | 1.300.400 | 1 | Total | Sem financiamento de terceiros (a ZAIOS não modela dívida) |
| **Curva de caixa e colchão** | idem | Saldo de 36 meses: captação no mês 1 − desembolsos do CAPEX nas janelas do cronograma − contingência nos meses 5 a 8 + geração a partir da abertura; colchão = menor saldo ÷ CAPEX | menor saldo 52.438,404; colchão 4,24% | 2 | Total | Limite de 10% é H4 |
| **Retorno, VPL, payback, cenários e estresse** | idem | Dicionário v0.4 (retorno anual; VPL fim do ano; payback estendido; conservador −10% diária e −20% ocupação; receita −30%; CAPEX +25%) | retorno 8,80%; VPL −653.689,68 e −401.898,66; payback 12,23; conservador 43.089,72; estresse 23.962,44 e 1.546.750 | 7 | Total | Cenários são H4 (D10) |
| **Régua (5 passos) e veredito** | idem | D11-A: 5 critérios; decisão pela regra | passos [passa, passa, redesenhar, redesenhar, ajustar]; decisão Redesenhar | 2 + 1 divergência | Total | **O selo aparece sem trava de homologação** (risco já registrado) |
| **G2: resultado e reserva** | Lançamentos do exemplo do FORMULAS.md: hospedagem 100.000, limpeza 10.000, extras 20.000; comissões 13.000, equipe 30.000, limpeza 7.000 (centavos) | Bruta = Σ receitas; resultado = bruta − despesas; margem = resultado ÷ bruta; cobertura = reserva ÷ média das fixas dos últimos 3 meses com lançamento | 130.000; 80.000; 0,6154; cobertura 3 | 9 | Total (documentação) | D12 pendente (fôlego x cobertura) |
| **G3: indicadores** | 2 unidades, 30 dias, 20 noites vendidas | Noites disp. = unid. × dias; ocupação; diária = hospedagem ÷ vendidas; RevPAR; TRevPAR; despesa por noite | 60; 0,3333; 5.000; 1.666,67; 2.166,67; 2.500 | 7 | Total (documentação) | Diária sem taxa de limpeza (convenção da ZAIOS; D14) |
| **G2: impostos** | Categoria "impostos" | Dicionário: tributos sobre a receita são dedução | dedução | 1 limitação | — | **Nova observação O7:** a G2 trata impostos como despesa variável |

## 2. B08 · Simulador de Viabilidade

| Grupo | Entradas | Fórmula de referência | Esperado | Casos | Independência | Limitações |
|---|---|---|---|---|---|---|
| **VPL, TIR, payback com rampa e reajuste** | Investimento 1.200.000; 4 unidades; 365 noites; diária 500 com reajuste de 5% ao ano; extras 10%; ocupação 25% → 40% em 3 anos; fixo 90.000; R$ 70/noite; comissão 15%; imposto 6%; taxa 12% | VPL com fluxos no fim de cada ano; TIR por bissecção; payback com interpolação linear | fluxo do ano 1 43.042,50; VPL −502.004,79; TIR 2,24%; payback 9,05; descontado nulo; retorno acumulado 15,03% | 6 | Parcial (fluxo); total (VPL, TIR e payback são definições-padrão) | Payback descontado nulo acima de 10 anos (D8) |
| **Valor residual** | idem + residual de 50% do investimento no ano 10 | Residual somado ao fluxo do ano 10 | VPL −308.820,85; TIR 7,18%; retorno 65,03%; payback igual | 4 | idem | Residual em % é divergência D7-C (já registrada) |
| **Equilíbrio sem e com reserva** | Cenário acima, ano de regime | Ocupação de equilíbrio = fixos ÷ (noites × margem por noite) | sem reserva 13,57%; com reserva como dedução 14,38% | 2 fórmula + 1 divergência | Total | **O3:** a regra aprovada (D2-C) tira a reserva das deduções, e aí o equilíbrio seria 13,57% |

## 3. A09 · Simulador de Viabilidade (cabana)

| Grupo | Entradas | Fórmula de referência | Esperado | Casos | Independência | Limitações |
|---|---|---|---|---|---|---|
| **Payback em novo cenário** | 2 unidades; investimento 600.000 + infra 80.000; contingência 10%; diária 550; ocupação 45%; 30 noites × 12; extras R$ 1.000/mês; fixos 8.000/mês; estadia R$ 150, média 2,5; comissão 12%; imposto 6%; gestão 10% | Payback simplificado = investimento total ÷ resultado anual | investimento 748.000; bruta 190.200; deduções 53.256; resultado 21.504; retorno 2,87%; payback 34,78 | 6 | Parcial | Payback estático, sem limite de horizonte (D8, O4) |
| **Gestão** | idem | Dicionário: gestão é custo do modelo, abaixo do resultado operacional | resultado antes da gestão 40.524 | 1 limitação | Total | **O2** |
| **Limite de 360 dias** | 31 noites/mês (máximo do campo) | 31 × 12 = 372 noites/ano | receita com 365 dias 282.948; conta da ferramenta 288.374,40 | 1 limitação + 1 fórmula | Total | **D5.** Correção do 05D: o campo aceita até 31, então o ano pode ter 372 dias (não "no máximo 360") |

## 4. B06, F05 e Folha J2

| Ferramenta e grupo | Entradas | Fórmula de referência | Esperado | Casos | Independência | Limitações |
|---|---|---|---|---|---|---|
| **B06 · três perfis** (iniciante, intermediário, incompleto-extremo) | Perfis de teste da própria ferramenta (`tests/profiles/B06.json`) | CAPEX = Σ itens; giro = fixo × meses; intermediário = CAPEX × (1 + contingência) + giro; conservador = CAPEX × (1 + variação) × (1 + contingência) + giro; desembolso mensal = CAPEX × (1 + contingência) ÷ prazo; custo/m² = (unidade + frete) ÷ área | Iniciante: 449.500; 524.450; 598.617,50; 30.000; 61.806,25; 4.000/m². Intermediário: 722.000; 844.640; 1.006.368; 36.000; 80.864; 3.607,14/m². Incompleto: 52.000 em todos; giro 0 | 17 | **Parcial** (a regra vem do código; não há documento-fonte) | D6: base da contingência |
| **F05 · diferença e R$/m²** | Planilha de exemplo publicada, recalculada no LibreOffice (cópia temporária) | Diferença = verba − total; R$/m² interna = total ÷ área interna; total = ÷ (interna + deck) | −16.744; 7.224,80; 5.160,57 | 3 | Total | — |
| **F05 · versão em branco** | Planilha em branco | Subtotal zero e mensagem de espera | 0; "Ainda não há itens com cotação" | 1 | Total | — |
| **Folha J2 · indicadores, fôlego, equilíbrio, caixa** | Exemplo oficial da ferramenta (4 unidades, mês de 31 dias) | Dicionário v0.4 e definições da Jornada 2 | noites 124; ocupação 46,77%; diária 280; margem 188,68 por noite; equilíbrio 35,37 noites; saldo final 13.620; fôlego 1,88 mês | 7 | Total | D12 (fôlego x cobertura) |
| **Folha J2 · custos do modelo** | Exemplo + aluguel R$ 800, gestão R$ 1.200, marca R$ 300 | EBITDA = operacional − custos do modelo | custos 2.300; EBITDA 1.969,20; geração 1.426,58; fôlego 1,43; equilíbrio 47,56 noites | 5 | Total | **Nova observação O6:** a Folha recebe esses custos em R$, e o dicionário os descreve como % da receita |

## 5. Totais

| | Casos | OK | Divergência | Limitação |
|---|---|---|---|---|
| ZAIOS (primitivas, composição, G2, G3) | 43 | 41 | 1 | 1 |
| B08 | 13 | 12 | 1 | 0 |
| A09 | 9 | 7 | 0 | 2 |
| B06 | 17 | 17 | 0 | 0 |
| F05 | 4 | 4 | 0 | 0 |
| Folha J2 | 12 | 12 | 0 | 0 |
| **Total complementar** | **98** | **93** | **2** | **3** |

**Falhas matemáticas: zero.**
