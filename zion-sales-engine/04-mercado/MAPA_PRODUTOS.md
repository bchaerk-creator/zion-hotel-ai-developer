# MAPA DE PRODUTOS E PRIORIZAÇÃO · ZION MARKET · Fase 03

Agente: ZION MARKET. Data: 25/11/2026. Marcação: [E] evidência lida, [H] hipótese, [NC] não confirmado. Somente leitura: nada foi alterado em ClickMax, Meta ou produção.
Dados completos por produto (colunas, justificativa e risco): `mapa_produtos.csv` (40 linhas, 24 colunas).
Fontes: `producao/catalogo/CATALOGO.md`, `producao/low-ticket/MAPA_OPORTUNIDADES.md`, `CLAUDE.md` seção 4, auditorias I e K de 25/11 (ClickMax, leitura), `insights_top_offers` e analítica dos formulários (ClickMax, leitura agregada em 25/11).
**Dados reais** (vendas por oferta em R$, visitas, gasto) ficam fora do repositório público, no scratchpad da sessão. Aqui só faixas: compradores "0", "1" ou "1 a 3 (inclui testes [H])".

## 1. Visão em uma página
- [E] O catálogo tem cerca de 40 itens vendáveis ou em produção, em 6 faixas de preço (R$ 13, 19, 27, 47, 67/97, acima de 270). Poucos têm página no ar e oferta aprovada ao mesmo tempo.
- [E] Vendas pagas desde 01/09: 8 no total, em 6 ofertas, incluindo testes do próprio Bruno [H]. Nenhum order bump vendeu. Nenhuma venda veio de anúncio com compra registrada no Meta (rastreamento ainda não confirma compra).
- [E] Os maiores grupos de leads reais da Zion são de **donos de terreno e projetos** (Land Bank, diagnóstico, formulário R$ 270) e de **operadores** da base antiga. Anfitriões de Airbnb comuns quase não foram atingidos por anúncio da linha infoproduto [H].
- [H] Por isso o público já atingido casa melhor com os produtos R$ 47 de terreno/capital do que com as ferramentas R$ 19 de operação de Airbnb.

## 2. Inventário por segmento
Colunas completas no CSV. Aqui: preço, status, potencial de venda direta e risco. Critério do potencial (sem número de mercado): Alto = preço dentro do CPA viável + público já atingido + dor clara + demonstração; Médio = faltam 1 ou 2 desses; Baixo = faltam 3 ou mais, ou o produto não vende hoje, ou é nicho.

### desenvolvimento de hospedagem

| id | produto | preço | status | potencial direto | risco |
|---|---|---|---|---|---|
| KPC | Kit Primeira Cabana | R$ 47 | rascunho | Baixo | Não auditado |
| EB2 | E-book · Do Terreno ao Airbnb | R$ 13 | ativo | Baixo | CPA inviável em tráfego frio |
| TRL1 | Trilha 1 | R$ 970 | rascunho (oferta incompleta + SYNCERR) | Baixo | Preço alto sem prova |
| ETAPA | Etapa de Desenvolvimento · Plataforma | R$ 290 (12x na página) | pending_corrections | Baixo | Página publicada com oferta pendente |

### Airbnb

| id | produto | preço | status | potencial direto | risco |
|---|---|---|---|---|---|
| F01 | Ferramenta 01 · Planilha Diária Mínima | R$ 19 | rascunho | Médio | Não vende hoje; público Airbnb ainda não atingido por anúncio Zion |
| F11 | Ferramenta 11 · Kit de Mensagens de Chegada e Saída | R$ 19 | rascunho | Médio | Concorrência grátis; não vende hoje (página rascunho) |
| F12 | Ferramenta 12 · Checklist de Fotos e Comodidades do Anúncio | R$ 19 | ativo | Baixo | Sobreposição com Arsenal/ZC06 |
| ARS01 | Arsenal Interativo 01 · Seu Airbnb Está Vazio? | R$ 27 | rascunho | Médio | Não vende hoje |
| ZC06 | Zion Collection 06 · Seu Airbnb Está Vazio? (kit mestre) + bump Calendário comercial de 30 dias | R$ 47 (+ bump R$ 19) | rascunho (ofertas aprovadas) | Médio | Não vende hoje; sobreposição com Arsenal 01 e F12 |

### donos de terreno

| id | produto | preço | status | potencial direto | risco |
|---|---|---|---|---|---|
| MM47 | Mini Mentoria de Estruturação | R$ 47 (líquido Pix R$ 44,51 [E]) | ativo | Alto | Rastreamento sem compra confirmada; promessa ampla; sem CPA real |
| ACE97 | Acesso à plataforma Zion Collection (R$ 97) | R$ 97 (líquido Pix R$ 87,73 [E]) | ativo (duplicado) | Médio | Duplicidade com MM47; CPA máximo maior mas 0 compras no Meta |
| ACE47 | Acesso à plataforma (R$ 47, clones 668391e7 e 74a3f8c6) | R$ 47 | ativo (redundante) | Baixo | Fragmenta a medição |
| TC-A | Você tem terra. Falta capital? (oferta A) | R$ 47 | ativo | Alto | Competir pelo mesmo público da MM47; promessa de capital exige cuidado (nunca prometer investimento) |
| TC-B | Você tem terra. Falta capital? (oferta B) | R$ 67 | ativo | Baixo | Dividir amostra pequena |
| KCAP | Kit de Captação (sócio/investidor) | R$ 47 | rascunho/sem página | Baixo | Sobrepõe Kit do Investidor da MM47 |
| EB3 | E-book · Terreno Parado Sócio | R$ 13 | ativo | Baixo | CPA inviável em tráfego frio |
| CLUB97 | Club Zion Collection · Kit de Captação + sessão estratégica (R$ 97) | R$ 97 | pending_corrections | Baixo | Promessa proibida |

### donos de pousada

| id | produto | preço | status | potencial direto | risco |
|---|---|---|---|---|---|
| MMPH | Mini Mentoria de Performance Hoteleira | R$ 47 | rascunho | Baixo | Produto sem entrega pronta no ar |

### gestão

| id | produto | preço | status | potencial direto | risco |
|---|---|---|---|---|---|
| F10 | Ferramenta 10 · Fechamento Mensal por Imóvel | R$ 19 | ativo | Médio | CPA máximo apertado (R$ 19) em tráfego frio |
| F15 | Ferramenta 15 · Comparador de Fornecedores | R$ 19 | ativo | Baixo | Pouca urgência |
| F16 | Ferramenta 16 · Kit Operacional de Parcerias | R$ 19 | ativo | Baixo | Risco jurídico de interpretação; nicho |
| F19 | Ferramenta 19 · Controle de Compras e Consumo Interno | R$ 19 | ativo | Baixo | Sobreposição com F13/F15 |

### operação

| id | produto | preço | status | potencial direto | risco |
|---|---|---|---|---|---|
| F13 | Ferramenta 13 · Controle de Enxoval e Reposição | R$ 19 | rascunho | Baixo | Nicho; não vende hoje |
| F14 | Ferramenta 14 · Quadro de Ocorrências e Manutenção | R$ 19 | rascunho | Baixo | Nicho; não vende hoje |
| F17 | Ferramenta 17 · Checklist de Limpeza, Inspeção e Liberação | R$ 19 | rascunho | Médio | Não vende hoje (página rascunho/SYNCERR) |
| F18 | Ferramenta 18 · Planner de Manutenção Preventiva | R$ 19 | rascunho | Baixo | Compra reativa |
| F20 | Ferramenta 20 · Kit de Treinamento do Primeiro Turno | R$ 19 | ativo | Médio | Nicho com equipe; compra pontual |

### performance

| id | produto | preço | status | potencial direto | risco |
|---|---|---|---|---|---|
| F22 | Ferramenta 22 · Planner de Campanhas para Períodos de Baixa Procura | R$ 19 | ativo | Médio | Sazonalidade: depende da época; sem promessa de ocupação |
| F24 | Ferramenta 24 · Assistente de IA para Atendimento | R$ 19 | ativo | Baixo | Depende de ferramenta externa; mudanças de modelo |

### identidade e vendas

| id | produto | preço | status | potencial direto | risco |
|---|---|---|---|---|---|
| F23 | Ferramenta 23 · Kit de Roteiros de Conteúdo e Vídeos | R$ 19 | ativo | Baixo | Concorrência grátis |

### glamping

| id | produto | preço | status | potencial direto | risco |
|---|---|---|---|---|---|
| F05 | Ferramenta 05 · Orçamento da Cabana | R$ 19 | rascunho | Médio | Orçamento depende de cotações do comprador; não prometer custo |
| F28 | Ferramenta 28 · Planner de Capacidade e Atendimento | R$ 19 | ativo | Baixo | Nicho |
| F29 | Ferramenta 29 · Calculadora de Custos de Experiências | R$ 19 | rascunho | Baixo | Nicho; não vende hoje |
| F30 | Ferramenta 30 · Gerador de Briefing de Experiência | R$ 19 | ativo | Baixo | Nicho |
| EB1 | E-book · Qual Cabana | R$ 13 | ativo | Baixo | CPA inviável em tráfego frio |
| GLAMP | Glamping, mais que uma hospedagem | R$ 27 | rascunho (oferta incompleta + SYNCERR) | Baixo | Não vende hoje |

### vários

| id | produto | preço | status | potencial direto | risco |
|---|---|---|---|---|---|
| COMBO | 3 combos de e-books | R$ 19 cada | rascunho | Baixo | Sem página |
| ZAR | Linha ZAR (20 produtos: A02 a A10, B01 a B10) | R$ 27 | rascunho (10 aprovados, 10 incompletos) | Baixo | Vitrine com links quebrados |
| ARQ | Linhas arquivadas: R$ 270/sessão 360 (8 ofertas), Trilhas A/2/3 e combo, Coleção 7 vol., Dossiê R$ 4.900, curso R$ 47 'Transforme seu terreno...' | R$ 47 a R$ 4.900 | arquivado | Baixo | Checkout de oferta arquivada com tráfego |
| TODO | A fazer (sem produção): ferramentas 02, 03, 04, 06, 07, 08, 09, 21, 25, 26, 27 e e-books da linha E01 a E10 | - | não produzido | Baixo | Dispersão |

Obs.: "donos de pousada" aparece como segmento principal só da Mini Mentoria de Performance Hoteleira (não auditada). Ferramentas 11, 13, 14, 17, 18 e 20 servem também a pousada e glamping (campo "público" do CSV).
Produtos de Land Bank, Zion Collection Club e Clube não entram no mapa (fora do escopo; "não mexer").

## 3. Filtros
### 3.1 Low Ticket Raiz (nome dado por Bruno; critérios dele: produto tangível, dor específica, compra simples, demonstração visual, entrega prática)
Pontuação 0/1 por critério, julgamento do agente [H] com regra: tangível = arquivo/ferramenta que o comprador abre; dor específica = uma tarefa nomeada; compra simples = promessa de uma frase, ticket até R$ 47, sem exigir configurar algo externo; demonstração = existe tela, planilha ou ficha que dá para mostrar em imagem; entrega prática = dá para usar no mesmo dia. Itens não auditados (Kit Primeira Cabana, Kit de Captação, Mini Mentoria de Performance Hoteleira, ZAR, Glamping, Club 97, combos) ficam sem nota [NC].

| id | produto | tangível | dor específica | compra simples | demo visual | entrega prática | total /5 |
|---|---|---|---|---|---|---|---|
| F01 | Ferramenta 01 · Planilha Diária Mínima | 1 | 1 | 1 | 1 | 1 | 5 |
| F05 | Ferramenta 05 · Orçamento da Cabana | 1 | 1 | 1 | 1 | 1 | 5 |
| F10 | Ferramenta 10 · Fechamento Mensal por Imóvel | 1 | 1 | 1 | 1 | 1 | 5 |
| F11 | Ferramenta 11 · Kit de Mensagens de Chegada e Saída | 1 | 1 | 1 | 1 | 1 | 5 |
| F13 | Ferramenta 13 · Controle de Enxoval e Reposição | 1 | 1 | 1 | 1 | 1 | 5 |
| F14 | Ferramenta 14 · Quadro de Ocorrências e Manutenção | 1 | 1 | 1 | 1 | 1 | 5 |
| F17 | Ferramenta 17 · Checklist de Limpeza, Inspeção e Liberação | 1 | 1 | 1 | 1 | 1 | 5 |
| F18 | Ferramenta 18 · Planner de Manutenção Preventiva | 1 | 1 | 1 | 1 | 1 | 5 |
| F20 | Ferramenta 20 · Kit de Treinamento do Primeiro Turno | 1 | 1 | 1 | 1 | 1 | 5 |
| F22 | Ferramenta 22 · Planner de Campanhas para Períodos de Baixa Procura | 1 | 1 | 1 | 1 | 1 | 5 |
| F29 | Ferramenta 29 · Calculadora de Custos de Experiências | 1 | 1 | 1 | 1 | 1 | 5 |
| ARS01 | Arsenal Interativo 01 · Seu Airbnb Está Vazio? | 1 | 1 | 1 | 1 | 1 | 5 |
| F12 | Ferramenta 12 · Checklist de Fotos e Comodidades do Anúncio | 1 | 1 | 1 | 0 | 1 | 4 |
| F15 | Ferramenta 15 · Comparador de Fornecedores | 1 | 0 | 1 | 1 | 1 | 4 |
| F16 | Ferramenta 16 · Kit Operacional de Parcerias | 1 | 1 | 1 | 0 | 1 | 4 |
| F19 | Ferramenta 19 · Controle de Compras e Consumo Interno | 1 | 0 | 1 | 1 | 1 | 4 |
| F23 | Ferramenta 23 · Kit de Roteiros de Conteúdo e Vídeos | 1 | 1 | 1 | 0 | 1 | 4 |
| F28 | Ferramenta 28 · Planner de Capacidade e Atendimento | 1 | 0 | 1 | 1 | 1 | 4 |
| TC-A | Você tem terra. Falta capital? (oferta A) | 1 | 1 | 1 | 0 | 1 | 4 |
| TC-B | Você tem terra. Falta capital? (oferta B) | 1 | 1 | 1 | 0 | 1 | 4 |
| ZC06 | Zion Collection 06 · Seu Airbnb Está Vazio? (kit mestre) + bump Calend | 1 | 1 | 0 | 1 | 1 | 4 |
| F24 | Ferramenta 24 · Assistente de IA para Atendimento | 1 | 1 | 0 | 1 | 0 | 3 |
| F30 | Ferramenta 30 · Gerador de Briefing de Experiência | 1 | 0 | 1 | 0 | 1 | 3 |
| MM47 | Mini Mentoria de Estruturação | 1 | 1 | 0 | 1 | 0 | 3 |
| ACE97 | Acesso à plataforma Zion Collection (R$ 97) | 1 | 1 | 0 | 1 | 0 | 3 |
| ACE47 | Acesso à plataforma (R$ 47, clones 668391e7 e 74a3f8c6) | 1 | 1 | 0 | 1 | 0 | 3 |
| EB1 | E-book · Qual Cabana | 1 | 1 | 1 | 0 | 0 | 3 |
| EB2 | E-book · Do Terreno ao Airbnb | 1 | 1 | 1 | 0 | 0 | 3 |
| EB3 | E-book · Terreno Parado Sócio | 1 | 1 | 1 | 0 | 0 | 3 |
| TRL1 | Trilha 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| ETAPA | Etapa de Desenvolvimento · Plataforma | 1 | 0 | 0 | 0 | 0 | 1 |

Leitura: o critério sozinho **não separa** as ferramentas prontas (muitas com 5/5); separa as ferramentas dos cursos (Mini Mentoria 3/5 por compra menos simples e entrega não imediata). Por isso o ranking da seção 4 usa também CPA viável, público atingido e se a oferta vende hoje.

### 3.2 OP3D e Pareto em cascata (aplicação provisória)
Bruno ainda **não** forneceu o conteúdo detalhado de OP3D nem de Pareto em cascata. Não foi inventado significado de nenhuma sigla nem etapa. O que se aplicou foi **apenas o princípio Pareto geral** (poucos itens concentram a maior parte do resultado), como regra de priorização: concentrar a fila de tráfego em 1 a 3 produtos e segurar o resto. **Esta aplicação é provisória e não é OP3D nem Pareto em cascata.** Evidência que sustenta o princípio aqui: das 6 ofertas com venda, 4 são de R$ 47 a R$ 97 do mesmo público (terreno); as 11 ferramentas R$ 19 publicadas somam 1 venda (que pode ser teste) [E, contagem no scratchpad].

Perguntas que Bruno precisa responder para refinar:
1. **OP3D:** o que cada letra/número representa? É um filtro de produto, de oferta ou de público? Quais são os critérios e como se pontua?
2. **OP3D:** é aplicado antes de produzir (decide o que fazer) ou depois (decide o que escalar)?
3. **Pareto em cascata:** qual é a unidade da cascata (produto, público, anúncio, criativo, etapa do funil)? Quantos níveis?
4. **Pareto em cascata:** qual a métrica que ordena (vendas, margem, CPA, número de leads)? Qual o corte (por exemplo, o que conta como "poucos")?
5. Há exemplo de aplicação feito por Bruno (um produto já classificado) que sirva de gabarito?
6. Os três filtros (Low Ticket Raiz, OP3D, Pareto em cascata) têm ordem fixa? Um produto reprovado em um é eliminado?

## 4. Ranking de potencial de venda direta por tráfego pago
### 4.1 CPA máximo viável (ponto de equilíbrio, antes de impostos e custos variáveis)
Fórmula: `CPA máximo = líquido por venda − impostos − custos variáveis`, com `líquido = preço − taxa do meio de pagamento`.
- **R$ 47:** líquido no Pix R$ 44,51 [E, fornecido por Bruno]. CPA de equilíbrio = R$ 44,51 menos impostos/custos (valor não definido: parâmetro).
- **R$ 97:** líquido Pix R$ 87,73 [E]. A taxa dos dois preços não segue uma regra única (R$ 2,49 em R$ 47 e R$ 9,27 em R$ 97), então **não dá para extrapolar para R$ 13, 19 e 27**.
- **R$ 13, 19 e 27: líquido [NC].** Simulação rotulada, não é dado: cenário A (taxa fixa R$ 2,49) e cenário B (taxa proporcional 5,3%, que é 2,49/47).

| Preço | Cenário A (taxa fixa R$ 2,49) | Cenário B (5,3%) | Fonte |
|---|---|---|---|
| R$ 13 | R$ 10,51 | R$ 12,31 | simulação [H] |
| R$ 19 | R$ 16,51 | R$ 17,99 | simulação [H] |
| R$ 27 | R$ 24,51 | R$ 25,57 | simulação [H] |
| R$ 47 | R$ 44,51 | (R$ 44,51) | [E] |
| R$ 97 | R$ 87,73 | - | [E] |

Leitura: um CPA de equilíbrio menor que R$ 18 em tráfego frio é um teto apertado para os tickets baixos; **não há CPA real** (0 compras confirmadas no Meta) [E], então qualquer afirmação sobre ser viável ou não é [H] até haver dado. Quem decide o CPA-alvo é o ZION FINANCE.

### 4.2 Ranking (critérios: CPA viável, demonstração visual, clareza da dor, público já atingido, oferta que vende hoje)
| # | Produto | Preço | Teto de equilíbrio | Demo | Dor clara | Público atingido | Vende hoje? | Veredito |
|---|---|---|---|---|---|---|---|---|
| 1 | Mini Mentoria de Estruturação | R$ 47 | R$ 44,51 [E] | sim (telas reais) | média (promessa ampla) | sim (terreno) | sim, mas sem compra confirmada no Meta | **Fila de tráfego** (já ligada; manter e medir) |
| 2 | Você tem terra. Falta capital? (A) | R$ 47 | R$ 44,51 [E] | parcial | alta (coincide com o relato dos leads) | sim (terreno) | sim | **Fila de tráfego, como teste contra a MM47**, só depois de resolver o rastreamento; não rodar os dois no mesmo público ao mesmo tempo (disputa de leilão) |
| 3 | Zion Collection 06 (+ bump R$ 19) | R$ 47 (+19) | R$ 44,51 [E] (bump: [NC]) | sim (Diagnóstico) | alta (calendário vazio) | não (Airbnb) | não (página rascunho) | **Próximo da fila**, condicionado a Bruno aprovar a publicação da página; é a única porta para o público Airbnb |
| 4 | Arsenal 01 | R$ 27 | [NC] | sim | alta | não | não (oferta incompleta) | Manter fora até a oferta ficar completa; degrau da escada |
| 5 | Ferramentas R$ 19 mais fortes (10, 17, 22, 11, 01) | R$ 19 | [NC] (sim. A/B acima) | sim | alta | parcial | 10 e 22 sim; 17, 11, 01 não | Só orgânico/CRM/pós-compra; teste pago apenas se Bruno aprovar e depois de rastreamento |
| 6 | Demais ferramentas R$ 19, e-books R$ 13 | R$ 13/19 | [NC] | variável | média/baixa | não | variável | Não anunciar |

### 4.3 Recomendação
- **Fila de tráfego (1 a 3):** (1) Mini Mentoria R$ 47, já ligada; (2) Você tem terra. Falta capital? A, como teste de dor mais literal contra a MM47; (3) ZC06 quando a página for publicada. Qualquer ativação, orçamento ou pausa exige "aprovado" de Bruno; este agente não altera nada.
- **Só orgânico, CRM e pós-compra:** as ferramentas de R$ 19 (úteis como bump e pós-compra), Arsenal 01 (enquanto a oferta estiver incompleta), e-books de R$ 13 (isca), Kit de Captação (downsell do público terreno), Trilha e Etapa (público aquecido).
- **NÃO escalar:**
  - R$ 97 e os clones de R$ 47: mesmo conteúdo, medição fragmentada.
  - Linha ZAR (R$ 27, 20 produtos sem venda e sem página no ar).
  - Qualquer produto cuja oferta esteja incompleta ou com erro de sincronização (o checkout não vende).
  - Etapa de Desenvolvimento R$ 290 e oferta R$ 97 com sessão (pending_corrections; promessa de sessão é proibida).
  - Ferramentas e e-books em tráfego frio enquanto o teto de equilíbrio for incerto.
  - Qualquer campanha antes de o rastreamento registrar compra (decisão de DATA/TRAFFIC).

## 5. Pesquisa de mercado (somente com fonte e data)
- **Não foi feita busca nova na web nesta fase** (economia de créditos; nenhum dado do cliente foi enviado a serviço externo). As fontes abaixo foram lidas na pesquisa de 06/11/2026 do `MAPA_OPORTUNIDADES.md` e **não foram relidas hoje**; confirmar link e data antes de usar em anúncio.
- [E, fonte lida em 06/11/2026] A taxa do Airbnb para o anfitrião varia conforme o modelo (cerca de 3% na taxa dividida, cerca de 16% na taxa única no Brasil, segundo PriceLabs): a confusão de precificação existe. https://hello.pricelabs.co/pt-br/blog/qual-a-taxa-do-airbnb/
- [E, 06/11/2026] Existem planilhas pagas de controle para Airbnb em inglês (Financial Aha, Etsy), sem as particularidades do Brasil.
- [E, 06/11/2026] Modelos de mensagem de hospedagem são oferecidos grátis por plataformas como isca (Hostfully, Stays): concorrência grátis para a Ferramenta 11.
- [E, 06/11/2026] Sebrae: turismo rural começa pelo planejamento e pela escolha da atividade, com exigências de regularização (e-book Sebrae "Preparando sua Propriedade Rural").
- [E, 06/11/2026] Não há orçamento em reais para construir glamping ou bubble nas fontes consultadas (preços estrangeiros e antigos).
- **Tamanho de mercado, demanda por produto, ticket médio do concorrente, volume de busca: [NC]. Não há número neste mapa.**

### 5.1 Linguagem e dores recorrentes nos leads reais (agregado, sem nomes; detalhe no scratchpad)
Fonte: formulário nativo "Ativação · Filtro" do ClickMax, leitura agregada em 25/11/2026, amostra pequena (menos de 20 respostas completas) [E]; leve como [H] direcional, não como conclusão.
- A maioria escolheu "sem capital" como o que trava, e declarou "sem reserva" para começar.
- A maioria disse ter terreno regularizado; uma parte relevante, com pendência.
- Horizonte de início mais citado: "3 a 6 meses"; uma minoria, "neste mês".
- Poucos escolheram falar com a equipe no passo de agendamento: a maior queda do formulário está nesse passo.
- Implicação [H]: a dor "tenho terra e falta capital" é a mais repetida entre quem respondeu; a promessa permitida continua "Aprenda o passo a passo para ...", sem prometer capital nem investimento.
- Leads de anfitriões de Airbnb: **sem amostra** nos formulários lidos [NC].

## 6. Escada de produtos (visão de mercado; o desenho de funil é do ZION FUNNEL, não duplicado)
| Degrau | O que resolve sozinho | Situação |
|---|---|---|
| R$ 13 · E-books | Entender um tema em minutos (isca) | ativos, sem venda; só como entrada orgânica |
| R$ 19 · Ferramentas | Uma tarefa por planilha ou kit | 11 no ar, 7 em rascunho com erro de sincronização |
| R$ 27 · Arsenal 01 | Diagnóstico do anúncio e plano de 30 dias | oferta incompleta (não vende) |
| R$ 47 · Mini Mentoria / Terra-Capital A / ZC06 | Estruturar o projeto (terreno) ou a oferta do anúncio (Airbnb) | MM47 e TC-A no ar; ZC06 em rascunho |
| R$ 67 · Terra-Capital B | variante de preço do mesmo produto | teste A×B, não é degrau |
| R$ 97 · Acesso plataforma | mesmo conteúdo da MM47 | não é degrau (duplicado) |
| R$ 290 a R$ 970 · Etapa, Trilha | aprofundamento para público aquecido | incompletos/pendentes; não vender agora |

Candidatos a order bump, upsell e downsell **entre o que já existe** (sem criar nada; configuração fica com FUNNEL e exige "aprovado"):
- **Bump da ZC06:** Calendário comercial de 30 dias R$ 19 (já existe como oferta ef27848a). Nenhum bump vendeu até hoje [E]; se está de fato ligado ao checkout é [NC].
- **Bump da MM47 ou da TC-A:** uma ferramenta de R$ 19 de maior demonstração (10 Fechamento Mensal ou 22 Campanhas na baixa), que já está no ar; ou nenhuma, para não competir com a compra de R$ 47. Decisão de FUNNEL/FINANCE.
- **Downsell do público terreno:** Kit de Captação R$ 47 (já usado no modelo de mensagem de downsell) ou e-book Terreno Parado Sócio R$ 13.
- **Upsell para quem comprou MM47:** nenhum degrau acima está pronto (Etapa e Trilha pendentes); não ofertar até Bruno decidir.
- **Pós-compra do Arsenal/ZC06:** ferramentas 12, 11 e 22 (mesma dor, execução).

## 7. Pendências e o que depende de Bruno
- Fornecer o conteúdo de OP3D e Pareto em cascata (perguntas na seção 3.2) para trocar a aplicação provisória.
- Decidir a consolidação de R$ 97 e clones R$ 47 (hoje fragmentam a medição).
- Aprovar (ou não) a publicação da página da ZC06 e qualquer mudança na fila de tráfego.
- Resolver o erro de sincronização do gateway nas ofertas de 01/11 e a oferta incompleta do Arsenal 01.
- Auditar os não auditados (Kit Primeira Cabana, Kit de Captação, MM Performance Hoteleira, ZAR, Glamping) antes de priorizar.
- Conferir os links de pesquisa de 06/11 antes de usar em copy.
