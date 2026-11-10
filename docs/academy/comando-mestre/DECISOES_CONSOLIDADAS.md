# Decisões consolidadas · Comando Mestre

10/11/2026 · Fontes: Comando 05G-A (O8 a O14, aprovadas em 09/11), respostas do Bruno em 10/11 (P-O8 a P-O14 aprovadas, reserva de 3 meses) e Comando Mestre (O7 e B08 como diretrizes; A09 como proposta provisória). **Nenhuma aprovação anterior foi inventada**: onde a regra não pôde ser inferida, a escolha feita está marcada como **premissa provisória** e listada na seção 3.

## 1. Regras implementadas

| Decisão | Regra implementada | Onde |
|---|---|---|
| **O8 + P-O8** | O P6 não dá selo de aprovação. Selo "Indicação preliminar" com três leituras: **negativa** (margem operacional abaixo de 10%, abaixo do equilíbrio ou EBITDA negativo), **atenção** (margem EBITDA abaixo de 10%), **positiva** (demais). Texto fixo: "indicação inicial, subordinada à análise financeira completa". Margem operacional (antes dos custos do modelo) e margem EBITDA (depois) com nomes distintos. A régua de margem continua como indicador, não como selo. Conflito entre a indicação do P6 e a decisão da Viabilidade aparece como alerta; prevalece a análise completa | P6 e Viabilidade |
| **O9** | Valor de saída por múltiplo = MAX(0, múltiplo × EBITDA do regime). Com EBITDA negativo, saída zero e aviso; dívidas, obrigações e custos de encerramento ficam fora | Viabilidade |
| **O10 + P-O10a** | Curva de caixa de 120 meses: meses 1 a 36 em detalhe, anos 4 a 10 pelo saldo de fim de ano. Primeiro mês negativo, menor saldo em 36 meses e em 10 anos, capital adicional = maior saldo negativo. VPL e TIR continuam anuais (desconto no fim do ano), com os meses agregados em blocos de 12 a partir da abertura | Viabilidade |
| **P-O10b + P-O10c** | Atraso de 6 meses dentro do horizonte fixo: o CAPEX segue o cronograma original; durante o atraso ficam **o aluguel e as taxas em valor fixo** (premissa provisória). Mostra receita não realizada, custos mantidos, perda de saldo em 10 anos e perda de VPL. Se o menor saldo melhorar com o atraso, o texto explica que é efeito de calendário e não melhora o projeto | Viabilidade |
| **O11 + P-O11** | Gestão e royalty com bases independentes: % da receita de hospedagem, % da receita bruta total ou valor fixo mensal. Campo "definida em contrato"; sem contrato, aparece como hipótese, com base e percentual. Sem escolha, vale a regra anterior (% da receita bruta). No equilíbrio, taxas em % entram na contribuição por noite e taxas fixas nos custos fixos | P6 |
| **O12 + P-O12** | Três números separados: (1) necessidade técnica = déficit acumulado da rampa + meses negativos do regime; (2) reserva operacional = meses de reserva (padrão **3**, configurável de 0 a 24) × (custos fixos com retirada + aluguel + taxas fixas + outras obrigações fixas), cada uma uma vez; (3) disponível, na Viabilidade. Capital de giro necessário = (1) + (2). O antigo "maior entre A (6 × fixo) e B" deixa de definir o resultado; A continua visível só como referência anterior. Aluguel incluído no custo fixo: alerta e uma contagem no giro | P6 |
| **O13 + P-O13** | Campo "capital próprio disponível para o giro". Diferença = disponível − necessário; déficit entra em alerta, pendência e captação adicional; excedente é informado. O disponível não reduz o necessário e não muda a curva técnica nem a captação | Viabilidade |
| **O14 + P-O14** | Categorias: **A** por noite ocupada (e o antigo % das diárias, que continua valendo como A); **B** ticket × percentual de adesão × estadias; **C** valor anual nos meses escolhidos (padrão: 12 meses iguais), sem rampa por padrão (configurável). Custo próprio de cada categoria (% da receita dela). Alíquota própria das complementares (vazio = a mesma das deduções). A e B seguem ocupação, rampa e cenários; C não. No equilíbrio, a contribuição líquida de C abate os custos fixos | P6 |
| **O7** | Na G2, "Impostos sobre a receita" é dedução, fora das despesas variáveis; "Tributos e taxas fixos" (IPTU, alvarás) é despesa fixa. Total de despesas e resultado não mudam. Lançamentos antigos da categoria "impostos" passam a ser lidos como impostos sobre a receita | G2 |
| **B08** | Dois indicadores: equilíbrio operacional (sem tratar a reserva como dedução, regra D2-C) e equilíbrio de caixa (com a reserva guardada) | Arsenal, branch de desenvolvimento |
| **A09** (provisória) | Calendário real: 365 dias, ou 366 com ano de referência bissexto; noites por mês viram opcionais e ficam limitadas aos dias reais | Arsenal, branch de desenvolvimento |

## 2. Pendências antigas resolvidas tecnicamente

| Pendência | Resolução | Situação |
|---|---|---|
| **D5** (A09) | Dias: calendário real (acima). Fixos × 12 com menos meses de operação: **não alterado** | Dias resolvidos (provisório). Fixos: depende de decisão (ver 3) |
| **D6** contingência | Padrão do dicionário: obra e infraestrutura, nunca sobre o giro (já é assim na ZAIOS P5). Ferramentas simples: rótulo "base simplificada" | Recomendação; ferramentas não alteradas |
| **D8** payback | Mantido: payback simples estendido pelo regime e marcado "estendido"; descontado só dentro dos 10 anos | Sem mudança; coerente com a O10 |
| **D9** | Custo por noite e por estadia já existem na ZAIOS; A e B têm custo próprio | Resolvido |
| **D10** cenários | Mantidos os da ZAIOS (−10% diária e −20% ocupação; +10% e +15%). A categoria C não varia com a ocupação | Parâmetro H4 |
| **D11-A** | A O8 resolve na ZAIOS P6 (indicação, não veredito) | Resolvido na ZAIOS |
| **D12** | Dois conceitos com nomes distintos no dicionário: "meses de fôlego" (Folha J2) e "cobertura da reserva" (G2) | Recomendação documental |
| **D13** | Centavos, sem arredondar até a tela, em todo código novo | Resolvido |
| **D14** | Alíquota própria das complementares; taxa de limpeza segue fora da hospedagem (decisão de 08/11) e pode ser lançada como categoria A ou B | Resolvido em parte; alíquota por fonte é do contador |
| **B06** | Sem documento de origem da regra de referência | Bloqueado |
| **H4** | Todos os parâmetros continuam constantes nomeadas no código, sem valor novo inventado | Decisão do Bruno |

## 3. Decisões que não puderam ser inferidas (premissas provisórias)

| # | Premissa adotada | Alternativa | Quem decide |
|---|---|---|---|
| 1 | Custos mantidos no atraso = aluguel + taxas em valor fixo (sem custo fixo operacional nem pró-labore) | Manter também parte ou todo o custo fixo | Bruno |
| 2 | Categoria C não segue a rampa nem os cenários de ocupação (configurável por projeto) | Rampa própria para C | Bruno |
| 3 | Necessidade técnica do giro = déficit da rampa + meses negativos do regime (componentes já existentes), e não o menor saldo da curva de 120 meses | Usar a curva de caixa diretamente (circular: a curva depende da captação) | Bruno |
| 4 | P5 mantém a "estimativa preliminar" de 6 × custo fixo, rotulada como preliminar; o P6 calcula o necessário | Trocar para 3 meses no P5 | Bruno |
| 5 | Indicação "atenção" quando a margem EBITDA fica abaixo de 10% | Outro limite | Bruno (H4) |
| 6 | A09: calendário real proporcional aos meses de operação (365 × meses ÷ 12); fixos continuam × 12 | Fixos proporcionais, ou dias abertos por mês | Bruno |
| 7 | Reserva de reposição: faixa da ZAIOS mantida em 3–5% e padrão 3% (D2-C aprovou 3–6% e 4%) | Aplicar a D2-C, mudando o resultado de projetos salvos com o padrão | Bruno (aprovado; falta autorizar o efeito) |
