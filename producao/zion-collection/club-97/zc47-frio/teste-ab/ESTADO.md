# Teste comercial A/B (27/11) · estado da implementação (tudo PAUSADO)
Pedido: Campanha A venda direta (V17C + Carrossel 01, quente+remarketing, landing) e Campanha B formulário (V06 + Carrossel 02, formulário nativo → landing, LAL 1% + compatíveis). R$30+R$30/dia, 72 h. Sem evento de checkout (contaminado). Não tocar Bela/automações, campanhas de pousada/Airbnb, demais vídeos.
Decisões técnicas:
- A: OUTCOME_SALES não tem evento validado (Purchase não chega; IC contaminado) → A usa o mesmo evento validado da campanha fria ativa: Tráfego / LANDING_PAGE_VIEWS. Proposta de passar para Vendas+Purchase depois da CAPI.
- B: OUTCOME_LEADS, LEAD_GENERATION, destination ON_AD, formulário nativo; tela final abre a landing.
- Privacidade do formulário: https://bchaerk-creator.github.io/zion-hotel-ai-developer/land-members/privacidade/
- Vídeos: V17C 1758647026274663, V06 2410954612991521.
Progresso (IDs):
- Carrosséis 01 (a1-a5) e 02 (b1-b5) renderizados (car.html), publicados em docs/p/adbc67069af26ae0/zc47-videos/zc2-car-*.jpg e enviados ao Meta (hashes em carrossel-hashes.json).
