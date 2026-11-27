# Teste comercial A/B (27/11) · estado da implementação (tudo PAUSADO)
Pedido: Campanha A venda direta (V17C + Carrossel 01, quente+remarketing, landing) e Campanha B formulário (V06 + Carrossel 02, formulário nativo → landing, LAL 1% + compatíveis). R$30+R$30/dia, 72 h. Sem evento de checkout (contaminado). Não tocar Bela/automações, campanhas de pousada/Airbnb, demais vídeos.
Decisões técnicas:
- A: OUTCOME_SALES não tem evento validado (Purchase não chega; IC contaminado) → A usa o mesmo evento validado da campanha fria ativa: Tráfego / LANDING_PAGE_VIEWS. Proposta de passar para Vendas+Purchase depois da CAPI.
- B: OUTCOME_LEADS, LEAD_GENERATION, destination ON_AD, formulário nativo; tela final abre a landing.
- Privacidade do formulário: https://bchaerk-creator.github.io/zion-hotel-ai-developer/land-members/privacidade/
- Vídeos: V17C 1758647026274663, V06 2410954612991521.
Progresso (IDs):
- Carrosséis 01 (a1-a5) e 02 (b1-b5) renderizados (car.html), publicados em docs/p/adbc67069af26ae0/zc47-videos/zc2-car-*.jpg e enviados ao Meta (hashes em carrossel-hashes.json).
- Formulário 1959234188381295 (ZC2 | FORM | Cadastro de área | 27-11), tela final abre /inscricao?utm_medium=lead_form&utm_campaign=zc2-b-formulario
- Campanha A 120250606891890016 (Tráfego, pausada); Campanha B 120250606931740016 (Leads, pausada)
- Conjunto A 120250606936870016 (LPV, R$30/dia, pausado, 7 públicos quentes); Conjunto B 120250607328680016 (Lead, R$30/dia, pausado, LAL1% + 2 de formulário, exclui os 7 do A)
- Anúncio A1 V17C 120250607336290016 (pausado)
- Anúncio A2 Carrossel 01 120250607339110016 (pausado)
- Anúncio B1 V06 120250607340000016 (pausado, formulário 1959234188381295)
- Anúncio B2 Carrossel 02 120250607343490016 (pausado)

## LANÇAMENTO 27/11 ~20:00 UTC (autorização de Bruno: "Pode usar esta autorização")
- Ligados: campanhas A 120250606891890016 e B 120250606931740016, conjuntos 120250606936870016 e 120250607328680016 (R$30/dia cada, fim 2026-11-30T20:00Z) e os 4 anúncios.
- Pausada: campanha fria ZC47 120250595856880016 (substituída pelo teste).
- Pendente: lead de teste do formulário (Bruno, ferramenta do Meta); frase do preço mantida "Adesão inicial R$ 47".
- 27/11 ~20:10 UTC: carrosséis A2 120250607339110016 e B2 120250607343490016 PAUSADOS (Bruno: nesta conversa só vídeos; carrosséis campeões são da outra conversa).
- Criados no conjunto A (pausados, a ligar): V15 120250607482070016, V14 120250607486500016, V12B 120250607539490016
- 27/11 ~20:20 UTC: V15 120250607482070016, V14 120250607486500016, V12B 120250607539490016 ATIVOS no conjunto A (utm_content a-v15/a-v14/a-v12b). Nesta conversa só vídeos.
## Situação atual
- A (R$30/dia, fim 30/11 20h UTC): V17C, V15, V14, V12B ativos; Carrossel 01 pausado.
- B (R$30/dia, fim 30/11 20h UTC): V06 ativo; Carrossel 02 pausado.
- 27/11: Campanha B 120250606931740016 PAUSADA até o lead de teste do formulário ser validado (orientação da auditoria GPT + teto global R$80/dia). A segue ativa (R$30/dia).
- Referência da fria anterior (Windsor, auditoria GPT): V15 R$3,77 / 209 impr / 19 cliques (9,09%) / 14 visitas; V17 original R$2,89 / 384 / 15 / 9; V17B R$0,68 / 58 / 5 / 4. Total R$7,65, 27 visitas, R$0,28 por visita. Amostra pequena; sem vencedor declarado.
- 27/11: conjunto B 120250607328680016 reduzido de R$30 para R$10/dia (campanha B segue PAUSADA). Só o V06 120250607340000016 fica ativo dentro de B; Carrossel 02 pausado. Religar B depois do lead de teste + "aprovado" do Bruno. Orçamento global planejado: A R$30 + B R$10 + carrosséis 3 e 4 R$40 (outra conversa) = R$80/dia.
- 27/11 (autorização final de Bruno): anúncio V06 120250607340000016 religado ao formulário Land Bank Terreno 1627911948376725 (o mesmo dos carrosséis de terreno), via update_ad (mesmo ID). Campanha B 120250606931740016 ATIVA, conjunto 120250607328680016 a R$10/dia (fim 30/11 20h UTC). Carrossel 02 segue pausado. Formulário 1959234188381295 fica sem uso (não arquivado).
