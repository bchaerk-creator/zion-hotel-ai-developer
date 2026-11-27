# Auditoria do rastreamento · Zion Collection (27/11/2026)

Somente leitura. Nada foi alterado em código, webhook, pixel ou integração.

## Caminho atual da venda de R$ 47
Anúncio (Meta, Zion Collection 2) → `zionhotelgroup.com/inscricao` (Lovable, projeto "Zion Hospitality Platform", serve a página estática `docs/p/adbc67069af26ae0/landing-zc47/pagina.html`) → botão → `infoprodutos-zion.clickmax.space/checkout-zion-47` (página `cd0a67ec…`, oferta `668391e7…`, produto `072083e8…`, gateway **Ticto** do ClickMax) → pagamento → acesso (portais `a8e2157a…`/turma `69345987…` e `3ef7a340…`/turma `087479a3…`).

## Os 10 pontos
| # | Ponto | Situação encontrada | Evidência |
|---|---|---|---|
| 1 | Pixel e dataset | Dois pixels em uso: **`1378530017570073`** no site (Lovable, `MetaPixel.tsx`, só PageView na `/inscricao`) e `903918118859018` usado em conjuntos antigos (Produto 01). **Nenhum** no checkout de R$ 47. Falta Bruno confirmar no Gerenciador de Eventos qual dataset está ligado à conta Zion Collection 2 | Lovable `src/components/zion/MetaPixel.tsx`; navegador de teste no checkout: `fbq` indefinido |
| 2 | Webhooks de confirmação | Oferta de R$ 47 e as demais do ClickMax: confirmação interna do ClickMax/Ticto (gatilho `purchase_approved`). **Asaas não participa** desta oferta. O webhook Asaas existe no Lovable (`/api/public/asaas-webhook`, PAYMENT_CONFIRMED, deduplicação por payment.id) para Método, Dossiê e Land Bank | `offers_get` (gatewayName `ticto`); Lovable `docs/asaas-metodo-webhook.md` |
| 3 | API de Conversões | **Não configurada.** O ClickMax tem CAPI nativa (token no cadastro do pixel em Tráfego › Pixel e trackeamento); o Lovable não chama a API da Meta | docs ClickMax "pixel-server-side-events" e "manage-pixels"; grep sem `graph.facebook.com` |
| 4 | Identificação de anúncio | Só `utm_content` fixo por anúncio (`v17-terreno`). Sem id dinâmico do anúncio | link do anúncio |
| 5 | UTMs, fbp, fbc | **Quebrado no salto landing → checkout:** os 2 botões da landing apontam para o checkout **sem repassar** `utm_*` nem `fbclid`. `_fbp` não existe no domínio do checkout (sem pixel). O código do checkout sabe montar `fbc` a partir do `fbclid` se ele chegar na URL | `pagina.html` (hrefs puros, sem script) |
| 6 | Id único da transação | Existe no ClickMax (id da transação/venda); hoje não chega à Meta | — |
| 7 | Centavos → reais | Valores do ClickMax em centavos (`originalPrice` 4700). O código antigo embutido no checkout chama `fbq('track','Purchase',{value:e})` com `e` em centavos (ao repassar ao site divide por 100). Com pixel no checkout pelo código antigo, a Meta poderia receber R$ 4.700 | bundle do checkout |
| 8 | Deduplicação | ClickMax nativo manda o mesmo `event_id` no navegador e no servidor. Risco: disparar Purchase também pelo site/GTM | docs ClickMax |
| 9 | Purchase só após aprovação | No sistema nativo do ClickMax, Purchase = compra aprovada; Pix confirmado depois sai pelo servidor (exige token). Sem token, Pix pago fora da página **não** chega | docs ClickMax |
| 10 | Conciliação | Meta (Windsor) mostra **0 compras** em 14 dias em todas as campanhas, inclusive as de Vendas (R$ 97: 149 InitiateCheckout, 0 Purchase; LT47: 27 IC, 0 Purchase), embora o ClickMax registre vendas | Windsor `get_data` 27/11 |

Observação: os "InitiateCheckout" da Meta disparam na abertura do checkout embutido (≈ visitas), não medem intenção.

## Plano consolidado (para aprovação de Bruno; nada executado)
**Etapa A · urgente, baixo risco (código nosso, no repositório):** script de 10 linhas na `landing-zc47/pagina.html` que copia `utm_source, utm_medium, utm_campaign, utm_content, utm_term, utm_id, fbclid` da URL para os links do checkout. Sem isso, as vendas da campanha ativa chegam sem UTM.

**Etapa B · no painel do ClickMax (Bruno, porque exige o token da Meta; o token nunca vai para o chat):**
1. Tráfego › Pixel e trackeamento › Adicionar pixel: o dataset confirmado na etapa 1 (provável `1378530017570073`).
2. Usar API de Conversões: colar o token gerado no Gerenciador de Eventos, "Testar token".
3. Eventos: Comprou (Purchase) ligado no navegador e no servidor, **todas as formas de pagamento** (inclui Pix); Abriu o checkout com "Só contar depois dos dados pessoais".
4. Ligar o pixel ao produto `072083e8…` (aba Pixels: checkout de R$ 47 e R$ 97) e aos produtos das demais ofertas da Zion Collection (R$ 270, Mini Mentoria `cbbb5fb1…`).
5. Não instalar Purchase pelo site/GTM (evita duplicar).

**Etapa C · teste controlado:** com Código de teste no pixel: (a) gerar Pix e não pagar → **nenhum** Purchase; (b) pagar Pix de R$ 47 → 1 Purchase, valor 47,00 BRL, origem servidor + navegador deduplicados, com `fbc` quando veio de clique; (c) conferir o Histórico de envio no ClickMax; (d) limpar o Código de teste; (e) reembolsar a compra de teste.

**Etapa D · identificação por anúncio (na próxima campanha, para não reenviar o anúncio ativo à revisão):** `utm_id={{campaign.id}}&utm_term={{ad.id}}` além do `utm_content`.

**Etapa E · conciliação diária:** Meta (gasto, impressões, cliques, LPV) × ClickMax (pedidos, Pix gerado, pagos, reembolsos, por UTM) × repasse Ticto. CPA real = gasto ÷ pagamentos confirmados. Receita líquida por venda R$ 44,51.

**Depois da Etapa C validada:** proposta de campanha de Vendas (Compra) substituindo a de Tráfego, mesmo público, exclusões, R$ 30/dia dentro do teto, V17, landing e UTMs; uma campanha só no ar.
