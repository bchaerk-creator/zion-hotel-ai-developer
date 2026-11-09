# Ressalvas e classificação · Comando 05F

09/11/2026 · **Proposta para revisão do Bruno.** Não é homologação definitiva, metodológica nem econômica. Não altera nenhuma classificação anterior sem aprovação. O 05E (`ATUALIZACAO_RESSALVAS_H1_H2.md`) continua valendo como estava.

## 1. Ressalvas que permanecem abertas (nenhuma foi encerrada)

| Ressalva | Situação após o 05F | Evidência nova do 05F |
|---|---|---|
| **Integridade:** sem hash obtido na fonte original da ZAIOS | Aberta | Mesmo commit `ec21ad5`; hashes da cópia iguais aos do 05E; a ZAIOS não foi conectada ao GitHub (por instrução) |
| **Veredito antecipado** | Aberta | A viabilidade mostra Redesenhar/Ajustar, e o P6 mostra Avançar/Ajustar, sem trava de homologação (C1 a C3E) |
| **B08:** reserva no cálculo do equilíbrio (O3) | Aberta | — (o B08 não faz parte do 05F) |
| **A09:** gestão nas deduções (O2) | Aberta | — |
| **A09:** até 31 noites por mês e 372 dias por ano (D5) | Aberta | — |
| **O6:** valores em R$ x percentuais de aluguel, gestão e marca na Folha J2 | Aberta | Relacionada à O11 (base da gestão e dos royalties) |
| **O7:** impostos como despesa variável na G2 | Aberta | — |
| **B06:** regra de referência sem documento externo | Aberta | — |
| **H4:** parâmetros de referência e limites da régua | Aberta | A taxa de 10%, o múltiplo de 6×, o colchão de 10% e os limites de 8/12 anos foram usados só como hipóteses de teste |
| **D5 a D14:** decisões metodológicas pendentes | Abertas | D8 (payback estendido de 83,39 anos no C3E conservador); D10 (cenários internos); D14 (outras receitas) |
| **Reserva de 3% a 5%** (aprovada 3–6%, D2-C) | Aberta | Reserva = 0% nos cenários (não informada). A faixa não foi exercitada |

## 2. Novas observações (para classificar; nenhuma corrigida)

| # | Observação | Onde apareceu | Natureza proposta |
|---|---|---|---|
| **O8** | A **margem operacional** e a **régua de margem** do P6 (boa/viável/apertada) são calculadas **antes** de aluguel, gestão e royalties. O selo do P6 pode dizer "Avançar" enquanto a viabilidade, na mesma jornada, diz "Redesenhar" | C1 (margem 19,93% "apertada", EBITDA negativo); C3E (margem 45,40% "boa", selo Avançar, decisão Redesenhar) | Apresentação. Risco de leitura indevida. Ligada ao veredito antecipado e à D11-A |
| **O9** | **Valor de saída negativo:** com EBITDA < 0, 6 × EBITDA vira um valor de venda negativo, somado ao ano 10. O VPL com saída fica pior que sem saída | C1 (−R$ 92.517,75) | Metodologia (D7-C não trata o caso) |
| **O10** | **Horizonte de 36 meses** na curva e no colchão: (a) a queima contínua de caixa depois do mês 36 não aparece (C1); (b) o teste de "atraso de 6 meses" pode **melhorar** o menor saldo, porque tira meses deficitários da janela | C1, C2, C3E | Limitação de leitura (horizonte) |
| **O11** | **Base de gestão e royalties:** a ZAIOS usa a receita bruta (inclui outras receitas); o comando usou a receita de hospedagem. Diferença = (gestão + royalty) × outras receitas | C2 (R$ 19.800/ano; VPL −R$ 114.745,23); C3 e C3E (R$ 62.400/ano; VPL −R$ 360.737,85) | Metodologia (a decidir; afeta EBITDA, VPL, TIR e payback) |
| **O12** | O **giro A** (6 × custo fixo) **não inclui o aluguel** mensal | C1 (R$ 54.000 sem aluguel x R$ 72.000 com aluguel) | Metodologia (a classificar). Sem efeito nos cenários, porque o giro B prevaleceu ou o A já era maior |
| **O13** | Não há campo para **capital de giro informado**: a ZAIOS sempre calcula o recomendado | Todos. No C1, o informado (R$ 45.000) deixaria a curva negativa; a ZAIOS recomenda R$ 109.095,26 | Metodologia (decisão de produto) |
| **O14** | **Outras receitas como % das diárias:** acompanham a ocupação mês a mês, a rampa do 1º ano e os cenários. Valores fixos em R$ exigem recalcular o percentual (como no estresse) | C2, C3, C3E | Limitação (D14) |

Achados que **não** são problema:
- o tratamento de resultado negativo e de indicadores indefinidos: o payback mostra "Não se paga.", o descontado "Não se paga em 10 anos." e a TIR "Não existe TIR para este fluxo.";
- o retorno anual negativo é exibido com o sinal.

## 3. Critérios para H1 aplicados à composição

| Critério (Comando 05F, seção 11) | Situação |
|---|---|
| Regra de referência suficientemente definida | **Sim** para a mecânica (Dicionário v0.4 + FORMULAS.md). **Não** para as convenções O8, O9, O11, O12, O13, O14 e D8, D10, D14 |
| Resultado independente reproduzível | **Sim.** Python sem código da ZAIOS. Entradas, script e esperados versionados |
| Cobertura compatível com o escopo | **Parcial.** 5 execuções integradas (05E + 05F). Faltam pró-labore, reserva, quebra e contingência > 0 combinados, além de outras taxas e múltiplos |
| Sem divergência matemática não resolvida | **Sim.** 0 em 288 campos (e 0 nos 17 do 05E) |
| Evidência documentada | **Sim** (este diretório + `resultados/2026-11-09-05f/`) |
| Integridade da origem | **Não comprovada** (condição de todas as classificações da ZAIOS) |

## 4. Proposta de classificação

| Grupo | 05E | Proposta 05F | Fundamento |
|---|---|---|---|
| **Camada de composição, como um todo** | H2 (cenário único) | **H2 (mantida)** | As lacunas relevantes continuam: integridade, uma transcrição, combinações sem cobertura (pró-labore, reserva, quebra), convenções não aprovadas (O8 a O14) |
| Demonstrativo do regime e do 1º ano via composição (receita, outras, tributos, variáveis por estadia, fixos, aluguel, gestão, royalties, EBITDA, sazonalidade, abertura em qualquer mês) | dentro da composição (H2) | **H1 proposto** (matemática), condicionado à integridade | 0 divergência matemática em 4 execuções. Limitação O11 (base de gestão e royalties) registrada |
| Capital de giro A/B, déficit da rampa e captação | H2 | **H1 proposto** (mecânica) | Confere em 5 execuções, inclusive com meses negativos. Ressalvas O12 e O13 |
| Fluxo de 10 anos, VPL sem saída, TIR, payback simples dentro do horizonte, retorno anual | H2 | **H1 proposto** | Confere, inclusive com resultado negativo e indefinido |
| VPL e TIR com saída | H2 | **H2** | O9 (saída negativa) e D7-C |
| Payback estendido e descontado | H2 | **H2** | D8 pendente |
| Curva de 36 meses e colchão | H2 | **H1 proposto** (mecânica) com **ressalva O10** na interpretação | A conta confere. A leitura depende do horizonte |
| Cenários internos, sensibilidade, estresse interno, atraso | H2 | **H1 proposto** (mecânica) | Confere. Os percentuais (−10%/−20%, +10%/+15%, −30%, +25%, 6 meses) são H4, e D10 está pendente |
| Régua de 5 passos (lógica) | H1 (05D) | **H1** (sem mudança) | Confere em 5 execuções. Os limites são H4 |
| Selo do P6 e régua de margem | não classificado | **H2** | O8 + veredito antecipado |
| Parâmetros e limites | H4 | **H4** | Sem mudança |

**Leitura:**
- Um H1 proposto aqui diz só que **a conta está certa para a cópia testada, segundo a regra documentada**.
- Não homologa a ZAIOS como plataforma, não aprova a metodologia e não diz nada sobre a viabilidade de nenhum empreendimento.
