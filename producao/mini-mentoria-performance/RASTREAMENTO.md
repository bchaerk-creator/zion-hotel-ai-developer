# Rastreamento e CRM · Mini Mentoria de Performance Hoteleira (modelo testado, não em produção)

`comercial/rastreamento.js` + `tests/rastreamento.test.js` (13 testes, 0 falhas) fixam as regras que o fluxo real (Asaas, ClickMax, CRM, Zaya) precisa cumprir.

| Regra | Testado no modelo |
|---|---|
| IDs: lead, anúncio, campanha, SKU (`MMPH-47`), pedido, pagamento, usuário; UTMs | sim |
| Webhook assinado e idempotente; evento fora de ordem ignorado | sim |
| `Purchase` só com pagamento confirmado; `event_id` igual no Pixel e na CAPI (deduplicação); sem dado pessoal nem resposta do diagnóstico | sim |
| Pendente/criado não libera acesso nem gera Purchase; reembolso revoga acesso | sim |
| Etapas do CRM: lead → checkout → pago → acesso → diagnóstico → dossiê → autorização → reunião → proposta | sim |
| Diagnóstico e dossiê só contam depois do acesso pago | sim |
| Zaya: só com consentimento e sem opt-out; entrega do produto não depende de contato comercial | sim |
| Conciliação ClickMax × Asaas (status, valor, ausências) | sim |
| CPL, CPA, receita líquida, conclusão, oportunidades por criativo; divisão por zero vira vazio | sim |

**Não testado (depende de Bruno):** compra real (vendedor `pending`), webhook real do Asaas, Pixel/CAPI no Meta, fluxos e tags no ClickMax, Zaya real, reembolso real. O que se mede de verdade vem do ClickMax e do Asaas, conciliado.
