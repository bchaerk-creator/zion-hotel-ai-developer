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
