# Dicionário Financeiro Único Zion · Academy e ZAIOS

**Versão 0.4 · 09/11/2026 · NÃO homologado.**

Incorpora as seis decisões metodológicas aprovadas pelo Bruno: D1, D2, D3, D4, D7 e D11. Nenhuma ferramenta, fórmula ou plataforma foi alterada. A ZAIOS é a referência financeira central futura; a homologação das suas fórmulas está pendente.

---

## Regras do dicionário

1. **Fonte única.** Toda ferramenta da Zion usa estes nomes, definições e fórmulas: ZAIOS, mini mentorias, planilhas e Folha Única.
   - Ferramentas simplificadas podem **omitir** componentes, desde que digam qual omitiram.
   - Nunca podem **redefinir** um nome.
   - Escopos diferentes podem dar números diferentes, desde que as regras sejam compatíveis.
2. **Tipos de valor.** Todo número mostrado ao aluno tem um tipo:
   - **Informado:** digitado pelo aluno, sem documento.
   - **Comprovado:** vem de documento (extrato, nota, cotação, contrato, laudo) ou de medição real.
   - **Referencial:** "Referência Zion", ponto de partida ajustável, com faixa, fonte e data.
   - **Ilustrativo:** exemplo com dados fictícios.
   - **Calculado:** resultado de fórmula; herda o menor grau de confiança dos insumos.
3. **Status:**
   - **Metodologia:** aprovada (com o número da decisão), decidida v0 (registrada em `docs/zaios/PREMISSAS_FINANCEIRAS_E_VERIFICACOES.md`) ou proposta.
   - **Homologação:** não homologado (todos, nesta versão), homologado matematicamente ou homologado economicamente.
4. **Versões:**
   - 0.x: proposta.
   - 1.0: homologado.
   - 1.x: ajuste de referência.
   - 2.0: mudança de fórmula.

   Cada resultado guarda a versão usada.
5. **Unidades.**
   - R$: na ZAIOS, centavos inteiros; nas ferramentas simples, float com arredondamento só na tela, tolerância de R$ 0,01.
   - Percentuais: guardados como fração, mostrados em %.
   - Tempo: em anos ou meses, sempre dito.
6. **Sem dupla contagem.** Cada valor entra uma única vez na cascata:
   - deduções saem da receita;
   - quebra é custo variável;
   - pró-labore é custo fixo;
   - reserva de reposição sai depois do EBITDA;
   - distribuição de resultados sai do caixa, nunca do resultado.

**Fontes citadas:**
- ZAIOS `src/calc/FORMULAS.md` e `src/calc/viabilidade.ts` (lidos em 09/11/2026).
- Unidades F01, F02 e F03 do Método Zion 360°.
- Folha Única J2 (`producao/jornada2/02-financas/`, 08/11/2026).
- Glossário CoStar/STR (consulta de 08/11/2026).
- Decisões do Bruno de 08/11 e 09/11/2026.

---

## 1. Operação

| Indicador | Definição | Fórmula (unidade) | Base | Premissas / referência | Fonte e data | Tipo | Status | Versão |
|---|---|---|---|---|---|---|---|---|
| Unidades | Quartos, cabanas ou casas à venda | informado (nº) | — | — | ZAIOS, 07/11/2026 | Informado | Metodologia v0 · não homologado | 0.1 |
| Dias abertos | Dias em que a unidade pode ser vendida | informado (dias); ano = 365, mês = dias reais | Calendário | Fevereiro com 28 dias | ZAIOS, 07/11/2026 | Informado | v0 · não homologado | 0.1 |
| Noites disponíveis | Capacidade de venda | unidades × dias abertos (noites) | — | — | CoStar/STR; ZAIOS | Calculado | v0 · não homologado | 0.1 |
| Noites vendidas | Noites efetivamente vendidas | informado ou noites disponíveis × ocupação (noites) | — | — | ZAIOS | Informado / calculado | v0 · não homologado | 0.1 |
| Ocupação | Parte da capacidade vendida | noites vendidas ÷ noites disponíveis (%) | — | — | CoStar/STR | Calculado | v0 · não homologado | 0.1 |
| Estadia média | Noites por reserva | noites vendidas ÷ estadias (noites) | — | 2 noites só como estimativa, se faltar dado | J2; ZAIOS | Calculado / referencial | Proposta · não homologado | 0.1 |
| Sazonalidade | Ocupação e diária por temporada | por mês: alta, média, baixa | Calendário | — | ZAIOS P6 (F02) | Informado | v0 · não homologado | 0.1 |
| Rampa | Ocupação do 1º ano sobre o regime | 40% (meses 1–3), 50% (4–6), 75% (7–12) (%) | Ocupação do regime | Validar por tipo de hospedagem | F02; ZAIOS | Referencial | v0 · não homologado | 0.1 |

## 2. Receita

| Indicador | Definição | Fórmula (unidade) | Base | Premissas / referência | Fonte e data | Tipo | Status | Versão |
|---|---|---|---|---|---|---|---|---|
| Diária média (ADR) | Receita de hospedagem por noite vendida | receita de hospedagem ÷ noites vendidas (R$) | — | — | CoStar/STR | Calculado | v0 · não homologado | 0.1 |
| Receita de hospedagem realizada | Diárias efetivamente vendidas, antes de descontos, comissões e impostos; **sem taxa de limpeza** | noites vendidas × diária média (R$) | — | Taxa de limpeza fora (decisão de 08/11) | ZAIOS; J2 | Calculado / comprovado | v0 · não homologado | 0.1 |
| Outras receitas | Alimentação, experiências, extras; excedente da taxa de limpeza (leitura J2) | informado ou % das diárias (R$) | — | D14 pendente | ZAIOS; J2 | Informado | Proposta · não homologado | 0.1 |
| Receita bruta realizada | Hospedagem + outras receitas efetivamente realizadas | soma (R$) | — | — | ZAIOS | Calculado / comprovado | v0 · não homologado | 0.1 |
| RevPAR | Receita de hospedagem por noite disponível | receita de hospedagem ÷ noites disponíveis = ADR × ocupação (R$) | — | — | CoStar/STR | Calculado | v0 · não homologado | 0.1 |
| TRevPAR | Receita total por noite disponível | receita bruta ÷ noites disponíveis (R$) | — | — | CoStar/STR | Calculado | v0 · não homologado | 0.1 |

## 3. Deduções e receita real

| Indicador | Definição | Fórmula (unidade) | Base | Premissas / referência | Fonte e data | Tipo | Status | Versão |
|---|---|---|---|---|---|---|---|---|
| Deduções | O que sai antes de a receita chegar: descontos, comissões, processamento, imposto sobre a receita, cancelamentos | soma dos componentes, ou receita bruta × % (R$) | Receita bruta | Referência 17% (15% comissões, processamento e impostos + 2% cancelamentos), ajustável por regime tributário e canal. **Não inclui quebra nem reserva** | F02; J2; decisão de 08/11 | Referencial / comprovado | v0 · não homologado | 0.1 |
| Receita real (líquida) | O que de fato chega | receita bruta − deduções (R$) | — | — | ZAIOS; J2 | Calculado | v0 · não homologado | 0.1 |

## 4. Custos e resultado

| Indicador | Definição | Fórmula (unidade) | Base | Premissas / referência | Fonte e data | Tipo | Status | Versão |
|---|---|---|---|---|---|---|---|---|
| Custo variável | Sai com cada noite ou estadia vendida | noites × custo por noite + estadias × custo por estadia + quebra e perdas (R$) | — | Ferramenta simples pode ter um componente só, com rótulo (D9 pendente) | ZAIOS; J2 | Informado / calculado | v0 · não homologado | 0.1 |
| **Quebra e perdas** | Louça, toalhas, controles e decoração que quebram ou somem; **custo variável operacional** | valor real medido (R$); sem medição: receita de hospedagem realizada × % (R$) | **Receita efetivamente realizada com hospedagem** | Referência provisória ajustável **1%**. **Prioridade para valores reais medidos.** Não entra nas deduções nem nas reservas. Ferramenta que não calcula deve dizer "resultado antes de quebra e perdas" | F02; J2; **Decisão D3-A, 09/11/2026** | Comprovado (medido) ou referencial | **Aprovada D3-A** · não homologado | 0.4 |
| Margem de contribuição | O que sobra para pagar os custos fixos | receita real − custos variáveis (R$) | — | — | ZAIOS; J2 | Calculado | v0 · não homologado | 0.1 |
| **Pró-labore** | Remuneração do trabalho do proprietário na operação; **custo fixo**, entra antes do resultado operacional | horas por semana × valor da hora × 4,33, ou valor fixo definido (R$/mês) | — | Referência R$ 40/hora. Ferramenta sem esse campo: "resultado antes do seu pró-labore" | F02; J2; **Decisão D4, 09/11/2026** | Informado / referencial | **Aprovada D4** · não homologado | 0.2 |
| Custos fixos | Saem com casa cheia ou vazia; incluem o pró-labore | soma (R$) | — | — | ZAIOS; J2 | Informado / calculado | v0 · não homologado | 0.1 |
| Resultado operacional | O que sobra da operação | margem de contribuição − custos fixos (R$) | — | — | ZAIOS; J2 | Calculado | v0 · não homologado | 0.1 |
| Margem operacional | — | resultado operacional ÷ receita bruta (%) | Receita bruta | Régua: ≥ 30% boa; 20–30% viável; 10–20% apertada; < 10% não fecha | F02; ZAIOS | Calculado | v0 · não homologado | 0.1 |
| Custos do modelo | Aluguel, taxa de gestão, royalty | aluguel + receita bruta × (gestão + royalty) (R$) | Receita bruta | — | ZAIOS | Informado / calculado | v0 · não homologado | 0.1 |
| EBITDA | Resultado antes de juros, impostos sobre o lucro, depreciação e amortização | resultado operacional − custos do modelo (R$) | — | — | ZAIOS | Calculado | v0 · não homologado | 0.1 |
| **Reserva de reposição** | Dinheiro guardado para trocar bens que se desgastam (colchões, enxoval de longa duração, eletros, ar-condicionado). **Não é dedução nem custo variável** | receita bruta realizada × % (R$), abaixo do EBITDA | **Receita bruta efetivamente realizada** | Referência provisória **4%**, faixa ajustável **3% a 6%**, validar por tipo de hospedagem. Sai uma única vez | F02; J2; **Decisão D2-C, 09/11/2026** | Referencial | **Aprovada D2-C** · não homologado | 0.2 |
| **Reserva de emergência** | Caixa separado para meses de baixa e imprevistos; **diferente da reserva de reposição**, nunca somado a ela | meta em meses de custo fixo (meses) | Custo fixo mensal | Meta a definir | **Decisão D2-C, 09/11/2026** | Referencial (meta) | **Aprovada D2-C** (separação) · meta pendente | 0.2 |
| Geração de caixa | O que a operação gera de caixa | EBITDA − reserva de reposição (R$) | — | — | ZAIOS | Calculado | v0 · não homologado | 0.1 |
| **Distribuição de resultados** | Parte que o proprietário retira **depois** de custos, pró-labore e reservas; **não é custo** | decisão do proprietário, limitada ao caixa disponível (R$) | Caixa disponível | — | **Decisão D4, 09/11/2026** | Informado | **Aprovada D4** · não homologado | 0.2 |
| **Caixa disponível** | Dinheiro livre depois da operação, das reservas e da distribuição | saldo inicial + geração de caixa − reserva de emergência separada − distribuição de resultados (R$) | — | — | **Decisão D4, 09/11/2026** | Calculado | **Aprovada D4** · não homologado | 0.2 |
| Equilíbrio (noites) | Noites que empatam o resultado | (custos fixos + aluguel) ÷ contribuição por noite (noites) | — | Sem dado se a contribuição for ≤ 0 | ZAIOS | Calculado | v0 · não homologado | 0.1 |
| Ocupação de equilíbrio | — | equilíbrio ÷ noites disponíveis (%) | — | — | ZAIOS | Calculado | v0 · não homologado | 0.1 |
| Meses de fôlego | Quantos meses o caixa paga os fixos | (saldo + reservas separadas) ÷ custo fixo do mês (meses) | Custo fixo | < 2 risco; 4–6 confortável | J2 | Calculado | Proposta (D12 pendente, convive com "cobertura da reserva" da ZAIOS G2) · não homologado | 0.1 |

## 5. Investimento

| Indicador | Definição | Fórmula (unidade) | Base | Premissas / referência | Fonte e data | Tipo | Status | Versão |
|---|---|---|---|---|---|---|---|---|
| CAPEX | Investimento para implantar | linhas (terreno e infraestrutura, projeto e licenças, obra, apoio e áreas comuns, FF&E, OS&E, pré-abertura) + contingência (R$) | — | — | F01; ZAIOS P5 | Informado / comprovado (cotações) | v0 · não homologado | 0.1 |
| OS&E | Enxoval, louça, utensílios | FF&E × % (R$) | FF&E | Referência 12% (faixa 10–15%) | F01; ZAIOS | Referencial | v0 · não homologado | 0.1 |
| Pré-abertura | Gastos antes de abrir | base × % (R$) | Infraestrutura + obra + apoio | Referência 5% (faixa 5–10%) | F01; ZAIOS | Referencial | v0 · não homologado | 0.1 |
| Contingência | Margem para imprevistos de obra | base × % (R$); nunca sobre o capital de giro | Infraestrutura + obra + apoio (ZAIOS) | 20–25% primeira obra; 10–15% com experiência. Base nas ferramentas simples: D6 pendente | F01; ZAIOS | Referencial | v0 · não homologado (D6 pendente) | 0.1 |
| Capital de giro | Caixa para operar até a receita estabilizar | o maior entre (A) 6 × fixo sem pró-labore e (B) déficit da rampa + sazonalidade + 3 × fixo com pró-labore (R$) | Custos fixos | — | F02; ZAIOS | Calculado | v0 · não homologado | 0.1 |
| Necessidade total | Tudo o que o projeto precisa | CAPEX + capital de giro (R$) | — | — | ZAIOS | Calculado | v0 · não homologado | 0.1 |

## 6. Viabilidade

| Indicador | Definição | Fórmula (unidade) | Base | Premissas / referência | Fonte e data | Tipo | Status | Versão |
|---|---|---|---|---|---|---|---|---|
| Horizonte | Período do fluxo | 10 anos | — | — | F03 | Referencial | v0 · não homologado | 0.1 |
| Fluxo do projeto | Ano 0 = −CAPEX; ano 1 = geração do 1º ano; anos 2–10 = geração do regime | (R$/ano) | Geração de caixa | Moeda constante, sem inflação | ZAIOS | Calculado | v0 · não homologado | 0.1 |
| Taxa de desconto | Custo do dinheiro do aluno + prêmio de risco | informada (% a.a.) | — | **Sem valor sugerido pela Zion** | Decisão de 08/11/2026 | Informado | v0 · não homologado | 0.1 |
| VPL | Valor presente do fluxo | Σ fluxo_t ÷ (1 + taxa)^t, fluxos no fim do ano (R$) | Fluxo | Mostrar **com e sem valor de saída** | F03; ZAIOS | Calculado | v0 · não homologado | 0.1 |
| TIR | Taxa que zera o VPL | bisseção (% a.a.); aviso se houver mais de uma troca de sinal | Fluxo | — | F03; ZAIOS | Calculado | v0 · não homologado | 0.1 |
| Payback simples | Quando o acumulado vira positivo | acumulado com fração (anos); além do horizonte, estendido pelo regime e marcado "estendido" | Fluxo | D8 pendente | ZAIOS | Calculado | Proposta · não homologado | 0.1 |
| Payback descontado | Idem com fluxos descontados | (anos), só dentro do horizonte | Fluxo descontado | — | ZAIOS | Calculado | v0 · não homologado | 0.1 |
| Payback simplificado | Atalho sem rampa | investimento ÷ resultado anual (anos) | — | Rótulo obrigatório | A09 | Calculado | Proposta · não homologado | 0.1 |
| **Retorno anual sobre o investimento** | Geração de um ano de regime sobre o investimento | geração de caixa do regime ÷ investimento total (% a.a.) | Investimento total | Substitui "ROI" sem qualificador | **Decisão D1, 09/11/2026** | Calculado | **Aprovada D1** · não homologado | 0.2 |
| **Retorno acumulado em 10 anos** | Ganho total sobre o investimento no horizonte | (Σ fluxos dos anos 1 a 10 − investimento) ÷ investimento (%); com valor de saída, mostrar as duas versões | Investimento total | — | **Decisão D1, 09/11/2026** | Calculado | **Aprovada D1** · não homologado | 0.2 |
| **Valor de saída** | Valor estimado de venda do ativo no fim do horizonte; sempre à parte, ao lado do cenário **sem venda** | três métodos, sempre identificados: (1) múltiplo do EBITDA = múltiplo × EBITDA do regime; (2) avaliação patrimonial (laudo do imóvel e benfeitorias); (3) valor estimado informado, com a fonte. **Valor líquido** = valor bruto − custos de venda − tributos − obrigações (R$) | EBITDA do regime (método 1) | Referência 6× só para o método 1 | **Decisão D7-C, 09/11/2026** | Referencial (1), comprovado (2), informado (3) | **Aprovada D7-C** · não homologado | 0.3 |
| Cenários | Variações de diária e ocupação | conservador: diária −10%, ocupação −20%; otimista: +10%, +15% (%) | Cenário base | D10 pendente | ZAIOS | Referencial | Proposta · não homologado | 0.1 |

## 7. Régua Única de Viabilidade Zion (Decisão D11-A, 09/11/2026)

**Status:** metodologia aprovada conceitualmente · **não homologada** · versão 0.4.

| # | Critério | O que avalia | Limites atuais (**provisórios**, versão 0 da ZAIOS) |
|---|---|---|---|
| 1 | **Geração de caixa operacional** | A operação gera caixa no regime | Passa se ≥ 0; senão, redesenhar |
| 2 | **Resistência ao cenário conservador** | Com diária −10% e ocupação −20%, o caixa aguenta | Passa se a geração for ≥ 0; ajustar se o déficit for de até 3 × custo fixo mensal com pró-labore; senão, redesenhar |
| 3 | **Prazo de recuperação do investimento** | Payback simples | Passa até 8 anos; ajustar até 12; redesenhar acima de 12 ou se não se pagar |
| 4 | **Criação de valor** | VPL **com e sem** saída | Passa se o VPL sem saída for ≥ 0; ajustar se for negativo sem saída e positivo com saída; redesenhar se for negativo nos dois |
| 5 | **Segurança financeira e colchão de caixa** | Menor saldo da curva de caixa (com a contingência usada) ÷ CAPEX | Passa se for ≥ 10%; ajustar entre 0% e 10%; redesenhar se for negativo |

**Regras de apresentação:**
1. **Ferramentas simplificadas** mostram só os critérios que conseguem calcular, com os outros identificados como **"não avaliado"**. Exemplo obrigatório de texto: *"3 de 5 critérios avaliados. Sinal parcial, não representa aprovação do projeto."*
2. **Avançar, Ajustar e Redesenhar** só aparecem quando **os cinco critérios** forem avaliados, e **só depois da homologação** da metodologia. Leitura: um "redesenhar" em qualquer critério dá Redesenhar; senão, um "ajustar" dá Ajustar; os cinco passando dão Avançar.
3. As **metas individuais do A09** (prazo e retorno desejados pelo aluno) ficam **separadas** da Régua Zion, num bloco "comparado com a sua meta".
4. Os limites são **provisórios** e precisam de validação por **tipo de hospedagem, porte e perfil** do empreendimento.
5. **Nenhuma classificação constitui garantia de viabilidade, financiamento ou retorno.**

## 8. Rótulos obrigatórios em qualquer ferramenta

- "Cenários, não promessas." junto de qualquer projeção.
- "Referência Zion (ajustável)", com a versão do dicionário.
- "Resultado antes do seu pró-labore", quando a ferramenta não tiver pró-labore.
- "Resultado antes de quebra e perdas", quando a ferramenta não calcular quebra.
- "Valor de saída: estimativa, mostrada à parte", com o **método** e o resultado **sem venda** ao lado.
- "X de 5 critérios avaliados. Sinal parcial, não representa aprovação do projeto.", em ferramentas simplificadas.
- "Exemplo com dados fictícios", em exemplos.
- Nunca: "retorno garantido", "renda passiva", "captação assegurada", "acesso a investidores", "ROI" sem qualificador.

## 9. Decisões ainda pendentes (não incorporadas como aprovadas)

| Divergência | Tema |
|---|---|
| D5 | Dias inteiros e fixos × 12 no A09 |
| D6 | Base da contingência nas ferramentas simples |
| D8 | Payback acima do horizonte |
| D9 | Custo variável por noite ou por estadia |
| D10 | Cenários de referência |
| D12 | Meses de fôlego x cobertura da reserva |
| D13 | Moeda em float x centavos |
| D14 | Taxa de limpeza e outras receitas |

Detalhes em `AUDITORIA_COMERCIAL_FINANCEIRA.md`, seção 7.

## Registro de versões

| Versão | Data | Mudança |
|---|---|---|
| 0.1 | 09/11/2026 | Proposta inicial (Comando 05B), a partir da ZAIOS v0, da Folha Única J2, de B06, B08, A09 e F05 |
| 0.2 | 09/11/2026 | Aprovadas pelo Bruno: D1 (retorno anual x acumulado em 10 anos), D2-C (reserva de reposição 4% provisória sobre a receita bruta realizada, faixa 3–6%, separada da reserva de emergência, sem dupla dedução, validar por tipo de hospedagem), D4 (pró-labore x distribuição de resultados x caixa disponível). Nenhuma ferramenta alterada |
| 0.3 | 09/11/2026 | Aprovada pelo Bruno: D7-C (valor de saída por múltiplo do EBITDA, avaliação patrimonial ou valor estimado informado; sempre com o método identificado, o cenário sem venda e o valor líquido de custos, tributos e obrigações). Nenhuma ferramenta alterada |
| 0.4 | 09/11/2026 | Consolidação das seis decisões. Incorporadas D3-A (quebra e perdas como custo variável operacional sobre a receita realizada com hospedagem, referência provisória 1%, prioridade para valores medidos, rótulo quando não calculada, sem dupla contagem) e D11-A (Régua Única de Viabilidade com cinco critérios, sinal parcial nas ferramentas simplificadas, veredito só com os cinco critérios e após homologação, metas do A09 separadas, limites provisórios). Tabelas com nome, definição, fórmula e unidade, base, premissas, fonte e data, tipo de valor, status e versão. Nenhuma ferramenta alterada |
