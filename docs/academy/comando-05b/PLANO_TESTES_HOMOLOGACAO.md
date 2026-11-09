# Plano de testes e homologação financeira · Academy e ZAIOS

Versão 0.2 · 09/11/2026 · Comando 05B · **Protocolo de homologação, não executado.** Alinhado ao dicionário v0.4 (decisões D1, D2-C, D3-A, D4, D7-C, D11-A). Os resultados abaixo vêm da auditoria de 09/11; a homologação formal depende do "aprovado" do Bruno.

## 1. Objetivo

Garantir que todas as ferramentas da Zion sigam o dicionário financeiro (`DICIONARIO_FINANCEIRO.md`):
- Em premissas iguais, dão o mesmo número quando o escopo é igual.
- Explicam a diferença quando o escopo é diferente.

A homologação da ZAIOS como referência central é a etapa 1: as outras ferramentas são conferidas contra ela.

## 2. Etapas

1. **Homologar a ZAIOS v0:**
   - Rodar os casos de referência abaixo.
   - O Bruno (com o contador, se quiser) confere premissas e resultados.
   - Aprovar como dicionário v1.0.
2. **Conferir cada ferramenta** contra os cenários equivalentes. Para cada uma: passa, diferença legítima (rotulada) ou erro (correção proposta).
3. **Aplicar as correções aprovadas, uma por vez.** Cada correção vem com:
   - teste novo que falha antes e passa depois;
   - relatório;
   - versão do dicionário.
4. **Regressão:** a cada mudança, os testes de todas as ferramentas rodam de novo.

## 3. Cenários de teste (dados fictícios)

### T1 · Z-base (premissas aceitas por todas as ferramentas de resultado)

- **Operação:** 3 unidades; diária R$ 680; ocupação 38%; 365 dias; sem sazonalidade, rampa ou reajuste.
- **Custos:** deduções 17%; variável R$ 80/noite; fixo R$ 6.000/mês; sem quebra, retirada ou reserva.
- **Investimento:** R$ 900.000 sem contingência; taxa 10%; 10 anos; sem saída.

| Resultado esperado | Valor | Tolerância |
|---|---|---|
| Receita bruta/ano | 282.948,00 | R$ 0,01 |
| Receita real | 234.846,84 | R$ 0,01 |
| Resultado operacional | 129.558,84 | R$ 0,01 |
| Ocupação de equilíbrio | 13,57% | 0,01 p.p. |
| VPL a 10% | −103.917,01 | R$ 0,01 |
| TIR | 7,24% | 0,01 p.p. |
| Payback simples | 6,95 anos | 0,01 ano |
| Payback descontado | não ocorre em 10 anos | — |
| Retorno anual | 14,40% | 0,01 p.p. |
| Retorno acumulado 10 anos | 43,95% | 0,01 p.p. |

**Resultado da auditoria de 09/11:**
- ZAIOS (regra) e B08: passam todos.
- A09: passa com 365 dias; o campo inteiro de noites por mês impede 365 (limitação D5).

### T2 · Z-completo (regras Zion completas)

T1 + quebra de 1% + reserva de reposição de 3% da receita bruta + rampa do 1º ano (40/50/75%), calendário real.

| Resultado esperado (ZAIOS) | Sem rampa | Com rampa |
|---|---|---|
| Resultado operacional (regime) | 126.729,36 | 126.729,36 |
| Geração de caixa (regime) | 118.240,92 | 118.240,92 |
| Geração do 1º ano | 118.240,92 | 42.405,16 |
| VPL a 10% | −173.460,73 | −242.402,34 |
| TIR | 5,30% | 3,71% |
| Payback simples | 7,61 | 8,25 |
| VPL com saída 6× EBITDA | +119.697,19 | +50.755,59 |

Aplica-se à ZAIOS e, depois das correções D2, D3 e D7, ao B08. A09 e Folha J2 só nas partes que tiverem.

### T3 · Casos de referência F01, F02 e F03 (já usados na ZAIOS)

| Caso | Esperado |
|---|---|
| F01 CAPEX | 1.237.400 (infra 250.000; projeto 70.000; obra 390.000; apoio 90.000; FF&E 195.000; OS&E 12%; pré-abertura 5% da base; contingência 25% da base) |
| F02 Receitas | 3 unidades, diária 680, ocupação 38%, deduções 17%, fixo 10.500/mês → receita real 234.846,84; resultado operacional 108.846,84; equilíbrio 223,25 noites (20,4%) |
| F03 Caso 1 | VPL −1.110.447,78; payback 38,6 anos; TIR com saída −8,4% → Redesenhar |
| F03 Caso 2 | Payback 5,75; descontado 8,82; VPL sem saída 92.549,78; com saída 624.599,52 |

### T4 · Orçamento (B06, F05, ZAIOS P5)

Escopo diferente, então não se espera o mesmo total. Testa-se a regra:
- contingência fora do capital de giro (B06 e ZAIOS);
- contingência e reserva explicadas no texto (F05);
- custo por unidade e custo por m² com as mesmas fórmulas.

Casos:
- Perfis oficiais do B06 (capex 449.500; intermediário 524.450; conservador 598.617,50).
- Exemplo da F05 (subtotal 197.040; reserva 19.704; total 216.744).
- F01 na ZAIOS.

### T5 · Folha Única J2 x ZAIOS G2/G3 (mês real)

Mesmo mês lançado nas duas. Devem coincidir:
- receita bruta, deduções, receita real;
- custos, resultado operacional;
- diária média, RevPAR, custo por noite.

Diferenças legítimas: meses de fôlego x cobertura da reserva (D12) e taxa de limpeza (D14).

### T6 · Limites e erros

- Ocupação 0% e 100%.
- Diária menor que o custo variável (sem equilíbrio).
- Fixo zero.
- Investimento zero.
- Fluxo sem troca de sinal (sem TIR).
- Fluxo com duas trocas (aviso de várias TIR).
- Payback acima de 10 anos (estendido x nulo).
- Campos "não sei".
- Diária "500.50" e unidades "2,5" (leitura de número).


### T7 · Régua Única de Viabilidade (D11-A)

Sobre o cenário T1, com saída de 6× EBITDA para o critério 4:

| Critério | Valor esperado | Resultado esperado |
|---|---|---|
| 1 · Geração de caixa operacional | 129.558,84 ≥ 0 | Passa |
| 2 · Conservador (diária 612, ocupação 30,4%) | receita bruta 203.722,56; geração 70.459,32 ≥ 0 | Passa |
| 3 · Prazo de recuperação | payback 6,95 anos ≤ 8 | Passa |
| 4 · Criação de valor | VPL sem saída −103.917,01; com saída (777.353,04 no ano 10; valor presente 299.703,25) +195.786,24 | Ajustar |
| 5 · Colchão | depende da curva de caixa (captação e cronograma), que o T1 não define | **Não avaliado** |
| **Apresentação esperada** | **"4 de 5 critérios avaliados. Sinal parcial, não representa aprovação do projeto."** | Sem Avançar, Ajustar ou Redesenhar |

Também testar:
- os cinco critérios avaliados mostram o veredito **só quando a flag de homologação estiver ligada**;
- um "redesenhar" → Redesenhar; só "ajustar" → Ajustar; tudo passando → Avançar;
- as bordas: payback de 8,00 e de 12,00; colchão de 10%; déficit igual a 3 × fixo;
- as metas do A09 aparecem num bloco separado e não mudam a contagem de critérios.

### T8 · Indicadores omitidos nas ferramentas simplificadas

Para cada ferramenta, conferir que o que ela não calcula aparece com o rótulo do dicionário:

| Omissão | Rótulo exigido | B08 hoje | A09 hoje |
|---|---|---|---|
| Quebra e perdas | "Resultado antes de quebra e perdas" | ausente, sem rótulo | ausente, sem rótulo |
| Pró-labore | "Resultado antes do seu pró-labore" | ausente, sem rótulo | ausente, sem rótulo |
| Reserva de reposição | "Antes da reserva de reposição" | dentro das deduções | ausente, sem rótulo |
| Critérios da régua | "X de 5 critérios avaliados…" | ausente | ausente |
| Valor de saída | método identificado + resultado sem venda | residual sem método | N/A |

### T9 · Reserva de reposição e quebra sem dupla contagem (D2-C, D3-A)

T1 + quebra de 1% (referência) + reserva de 4% da receita bruta realizada:

| Linha | Esperado |
|---|---|
| Deduções (17%) | 48.101,16 (**não** contém quebra nem reserva) |
| Quebra e perdas (custo variável) | 2.829,48 |
| Resultado operacional | 126.729,36 |
| Reserva de reposição (abaixo do EBITDA) | 11.317,92 |
| Geração de caixa | 115.411,44 |

Também testar:
- quebra **medida** em R$ (ex.: 1.900,00) substitui a referência e aparece como "comprovado";
- faixa da reserva de 3% a 6% aceita, fora dela com aviso;
- reserva de emergência **não** reduz a geração de caixa: só o caixa disponível;
- a soma da cascata fecha (bruta − deduções − variáveis − fixos − modelo − reserva = geração).

### T10 · Pró-labore, distribuição e caixa disponível (D4)

| Caso | Esperado |
|---|---|
| Pró-labore 20 h × R$ 40 × 4,33 | 3.464,00/mês = 41.568,00/ano, como custo fixo |
| Resultado operacional (T1 com pró-labore) | 129.558,84 − 41.568,00 = 87.990,84 |
| Distribuição de resultados de R$ 30.000 | **Não** muda o resultado nem a geração; reduz o caixa disponível em 30.000 |
| Distribuição maior que o caixa disponível | Aviso ("distribuição acima do caixa disponível") |
| Pró-labore zero decidido | Aceito com a marcação consciente (padrão da Folha J2); em branco = pendência |

### T11 · Métodos de valor de saída (D7-C)

| Caso | Esperado |
|---|---|
| Método 1, múltiplo 6× EBITDA de 129.558,84 | Valor bruto 777.353,04, rotulado "múltiplo do EBITDA" |
| Custo de venda ilustrativo de 6% | 46.641,18 → líquido antes de tributos 730.711,86 (**exemplo com dados fictícios**; percentual real a definir) |
| Tributos e obrigações | Campos próprios; sem referência Zion até a orientação de contador ou advogado |
| Método 2, avaliação patrimonial | Valor informado do laudo, rotulado "avaliação patrimonial", tipo "comprovado" |
| Método 3, valor estimado informado | Rotulado "valor informado pelo aluno", com a fonte |
| Todos | VPL e retorno acumulado mostrados **sem venda** e **com venda**, lado a lado |

### T12 · Validação dos limites por tipo de hospedagem

Não é teste de fórmula, é validação econômica. Para cada tipo (glamping/bubble, cabana, chalé, pousada, apartamento) e porte (1, 2–10, mais de 10 unidades):
- reunir evidências (dados reais da Zion, mercado, literatura);
- confirmar ou ajustar: reserva 4% (3–6%), quebra 1%, deduções 17%, rampa, cenários, múltiplo 6×, limites da régua (8 e 12 anos, colchão de 10%, 3 meses).

Registrar cada referência com fonte, data e versão no dicionário.

## 3A. Cenários equivalentes por ferramenta

| Teste | ZAIOS | B08 | A09 | B06 | F05 | Folha J2 |
|---|---|---|---|---|---|---|
| T1 Z-base | Sim | Sim | Sim (limitação de 360 dias, D5) | — | — | — |
| T2 Z-completo | Sim | Depois de D2/D3/D4 | Parcial | — | — | — |
| T3 F01–F03 | Sim | F03 (viabilidade) | — | F01 (estrutura de custos) | — | F02 (mês) |
| T4 Orçamento | P5 | — | Investimento | Sim | Sim | — |
| T5 Mês real | G2/G3 | — | — | — | — | Sim |
| T6 Limites | Sim | Sim | Sim | Sim | Sim | Sim |
| T7 Régua | Sim (5 critérios) | Parcial (critérios 1, 3, 4) | Parcial (1, 3) | — | — | — |
| T8 Omissões | — | Sim | Sim | Sim | Sim | Sim |
| T9 Reserva e quebra | Sim | Sim | Sim | — | — | Sim |
| T10 Pró-labore e caixa | Sim | Sim | Sim | — | — | Sim |
| T11 Saída | Sim | Sim | — | — | — | — |
| T12 Limites por tipo | Validação econômica, não por ferramenta | | | | | |

## 3B. O que pode ser homologado matematicamente e o que exige validação econômica

| Homologação matemática (fórmula certa com os insumos dados) | Validação econômica ou evidência de mercado (o número de referência é adequado?) |
|---|---|
| Noites, ocupação, ADR, RevPAR, TRevPAR | Deduções de 17% por regime tributário e canal |
| Receita bruta, deduções, receita real | Quebra de 1% por tipo de hospedagem |
| Quebra (mecânica), custo variável, margem de contribuição | Reserva de 4% (3–6%) por tipo e idade do ativo |
| Pró-labore (mecânica), custos fixos, resultado operacional, EBITDA | Valor da hora de R$ 40 do pró-labore |
| Reserva (mecânica), geração de caixa, caixa disponível | Rampa 40/50/75% |
| CAPEX, OS&E, pré-abertura, contingência (mecânica), capital de giro | OS&E 12%, pré-abertura 5%, contingência 20–25% e 10–15% |
| VPL, TIR, paybacks, retorno anual, retorno acumulado | Cenários conservador e otimista (−10/−20, +10/+15) |
| Valor de saída método 1 (mecânica), valor líquido (soma) | Múltiplo 6×; custos de venda; tributos (profissional habilitado) |
| Régua: lógica dos 5 critérios e da leitura | Limites da régua: 8 e 12 anos, colchão de 10%, 3 meses de fixo |
| Equilíbrio e ocupação de equilíbrio | Meta da reserva de emergência |

A homologação matemática pode ser feita com os testes T1 a T11. A econômica depende do T12 e de evidências.

## 4. Critérios de homologação

Uma ferramenta é homologada quando:
1. Passa T1 (ou declara a limitação com rótulo, como o A09) e os testes T7 a T11 do seu escopo.
2. Passa os cenários do seu escopo (T2 a T5).
3. Usa os nomes e rótulos do dicionário (seção 7 dele).
4. Mostra o tipo de cada valor (ilustrativo, referencial, comprovado, calculado).
5. Tem testes automáticos versionados no repositório.
6. Mostra a régua conforme a D11-A (sinal parcial ou veredito só após homologação) e os rótulos de omissão.

**Situação em 09/11/2026:** nenhuma ferramenta está homologada. A ZAIOS v0 e o B08 passam T1. O A09 passa T1 com ressalva (D5). B06 e F05 têm testes próprios passando (59 de 59 e 33 de 33) e aguardam T4.

## 5. Responsáveis

| Ferramenta | Sessão | Testes existentes |
|---|---|---|
| ZAIOS | ZAIOS platform development | 396 testes (Vitest) no Lovable |
| B06, B08, A09 | Zion Arsenal | `producao/zion-arsenal/tests/profiles/*.json` + `tests/run.js` |
| F05 | Zion infoprodutos catálogo | `producao/utilitarios/05-orcamento-cabana/tests/test_planilha.py` |
| Folha Única J2 | Marketing da Zion install | `producao/jornada2/02-financas/tests/` |

Os cenários T1 a T11 devem virar arquivos de teste no formato de cada ferramenta, **depois do "aprovado"**.
