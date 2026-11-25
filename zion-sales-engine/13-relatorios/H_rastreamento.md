# Auditoria H · Rastreamento de vendas: ClickMax × Ticto × Meta (SOMENTE LEITURA)

Data: 25/11/2026. Nada foi alterado (sem pixel, CAPI, webhook, página, oferta, campanha, automação, commit, pedido ou cobrança). Sem dados pessoais neste arquivo: compradores aparecem como "comprador A" (venda real de 24/11 17:48Z) e "comprador B" (venda real de 24/11 18:07Z). Sem tokens ou chaves.
Legenda: [E] evidência lida (ferramenta/código/doc) · [H] hipótese · [NC] não confirmado, com o jeito de confirmar.
Leia antes: C_pixel_capi.md, D_vendas_leads_financas.md, RELATORIO_FINAL.md (não repeti o que já estava lá).
Fontes novas desta rodada: `lead_activities_list(_by_lead)`, `visitors_lead_journey`, `visitors_attribution`, `visitors_conversion_funnel`, `dashboard_my_sales`, `sales_get_utms`, `offers_get`, Windsor (`url_tags`, janela 7d_click,1d_view), HTML público de /inscricao-47 (baixado em `scratchpad/h_rastreamento/dl/i47.html`), docs.clickmax.io (via `docs_pages_get`), developers.facebook.com (busca pública). A documentação pública da Ticto sobre pixel/UTM não apareceu na busca: ficou só o que o ClickMax documenta sobre a Ticto.

---

## 0. Resposta curta (o que está provado e o que não está)

1. **O Meta mostra Purchase = 0 em 20 a 25/11 em todas as campanhas** (Windsor, janela 7d clique + 1d visualização: `actions_purchase`, `actions_omni_purchase`, `actions_offsite_conversion_fb_pixel_purchase` e `action_values_omni_purchase` todos nulos). Havia 2 vendas reais pagas (R$ 97 cada, 24/11). [E]
2. **O ClickMax não registrou NENHUM evento de pixel em nenhum contato do workspace.** A atividade `ads.pixel.event` (que alimenta a aba "Eventos de pixel" da ficha do contato, navegador e servidor) volta vazia para o workspace inteiro, para os dois compradores reais e para o contato de testes do Bruno. [E] Leitura prudente [H]: nunca saiu evento de servidor (CAPI) por este workspace, ou o registro não é gravado. Só o Gerenciador de Eventos e a tela "Histórico de envio" do pixel decidem [NC, roteiro na seção 10].
3. **Por que as 2 vendas reais vieram sem UTM: não é erro de URL do anúncio.** As 3 URLs de anúncio pedidas têm UTM (seção 5). A venda do comprador A pertence a um visitante que tinha UTM Meta na primeira sessão, mas a venda guarda os parâmetros **da URL no momento em que o checkout abriu**, e a navegação dele passou por link de mensagem do WhatsApp (sem UTM). O comprador B não tem nenhum visitante ligado e a venda tem `linkCheckout` vazio: abriu o checkout fora de uma página medida. [E+H, seção 5]
4. **Pix gerado × Pix pago é distinguível no ClickMax** (eventos `checkout.pix.generated` e `checkout.transaction.paid`, 51 s e 91 s de intervalo nos dois compradores). O pixel precisa mandar `Purchase` só no segundo. Hoje não há prova de que isso acontece. [E+NC]
5. **A conciliação falha por quatro motivos somados:** nenhum Purchase chega ao Meta; a venda não carrega UTM, `sck`, `src` nem ID de anúncio; não há clique (fbclid/fbc) registrado nem para a visita com UTM Meta; e os dois compradores vieram por caminho que o Meta não atribui sozinho (formulário nativo → WhatsApp → link; link direto). [E+H]

---

## 1. Como o Purchase chega ao Meta hoje (item 1)

### 1.1 O que se sabe
| Pergunta | Resposta | Evidência |
|---|---|---|
| Quem dispara o Purchase de navegador? | O pixel que roda **dentro do iframe de checkout** `payments.clickmax.io/custom/<pageId>/<hash>`. A página-mãe não tem `fbq` | C_pixel_capi (Playwright, HTML) [E]; reconferido: o HTML de /inscricao-47 só contém `fbq("track","Purchase",…)` e `fbq("track","InitiateCheckout")` dentro de uma classe de checkout dormente |
| O ClickMax manda CAPI? | **Pode**, se o pixel tiver "Usar API de Conversão" e Token. Sem token, só navegador. Não dá para ler token nem a config por ferramenta | Doc `/guides/pixel-server-side-events`, `/guides/manage-pixels` [E]; leitura da config [NC] |
| A Ticto dispara pixel/CAPI para o Meta? | **Não há sinal.** Os compradores só têm eventos nativos `checkout.*`. Não existe atividade `ticto-webhook.*` em nenhum deles. A Ticto é o **processador de pagamento por trás do checkout nativo do ClickMax**: `offers_get` → `gatewayName: ticto`, `isExternalCheckout: false`; transações `TOP…/TPP…` com Pix emitido pela Adyen | `lead_activities_list_by_lead`, `offers_get` [E]. Se a Ticto tem pixel próprio configurado no painel dela: [NC] (só no painel Ticto) |
| Quando dispara? | Navegador: IC ao carregar o iframe (já provado). Servidor (CAPI): Purchase **na compra aprovada**, só 1ª cobrança (doc). No código embutido: Purchase ao **gerar** Pix/boleto/cartão | Doc + HTML [E]. Qual vale em produção: [NC] |
| Parâmetros | Doc: servidor leva e-mail, telefone, documento, endereço do checkout, "clique no anúncio" completado pelo contato, ID de navegador do pixel, mesmo identificador de contato em todos os eventos, mesmo `eventID` do navegador. Valor/moeda no SDK: `value = centavos/100`, `currency` BRL | Docs + `index.js` (C_pixel_capi §2.1) [E]. Valores efetivamente enviados: [NC] |

### 1.2 O que NÃO está provado
- Nenhum evento de pixel enviado foi observado (o ambiente bloqueia `payments.clickmax.io`). Tudo acima de "disparo real" vem de código + docs + dados Meta.
- Se existe token de CAPI, se `Purchase` está filtrado por método de pagamento (Pix desmarcado), e qual pixel está em cada oferta: ver item 2.

### 1.3 Evidência nova que ajuda a decidir "Purchase no Pix gerado?"
- Em 24/11 houve 4 Pix gerados (2 reais + 2 testes) e o Meta recebeu **2 AddPaymentInfo** e **0 Purchase** (venda direta). O código dormente do HTML emitiria `Purchase` ao gerar o Pix. Se esse código estivesse ativo no iframe, qualquer Pix gerado por visitante vindo do anúncio apareceria como Purchase de navegador. [H] Isso favorece a leitura "o iframe usa o caminho novo do SDK (`pix_generated → AddPaymentInfo`) e não o `Purchase` no Pix gerado". Mas o Windsor só mostra o que o Meta **atribuiu a anúncios**; um Purchase sem atribuição aparece no Gerenciador de Eventos e não aqui. Confirmação só no Testar eventos (seção 10).

---

## 2. Onde o ClickMax configura pixel/CAPI/token e o que dá para ler (item 2)

| Nível | Onde fica | Leitura por ferramenta? |
|---|---|---|
| Cadastro do pixel (ID, apelido, projeto, token CAPI, "Código de teste", eventos por canal, filtro de método de pagamento do Purchase, "Só contar depois dos dados pessoais" no IC) | Tráfego > Pixel e trackeamento (conta/workspace) | **Não.** Nenhuma ferramenta MCP lê pixels, token ou histórico de envio |
| Quais telas usam o pixel | Marcação por tela: funil, página, domínio, **produto**, **oferta**, agenda, formulário, quiz, link de redirecionamento ("Pixels deste produto/oferta") | **Não.** `offers_get` (conferido nas ofertas R$ 97) não traz campo de pixel; `pages_get`/`checkouts_get` também não |
| Checkout (iframe) | Segue o pixel marcado em **produto/oferta** (doc: "evento aparece na página e não no checkout = pixel marcado no funil, não no produto") | Não |
| "Usar em tudo que eu criar" | Opção do cadastro | Não |

**Qual pixel está ligado a cada oferta (R$ 97 `c298aaed`, R$ 47 `668391e7`, Mini Mentoria `0c71eeba`): NÃO CONFIRMADO por ferramenta.** Indícios: os conjuntos de venda direta e LT47 têm `promoted_object.pixel_id = 903918118859018` e o Meta recebe PageView/IC desses cliques, então esse pixel dispara no iframe das páginas /inscricao-47 e /parceiro-zion (que usam a oferta `668391e7`) e /inscricao-curta (R$ 97). [H] Como confirmar: ClickMax > Produtos > produto "Zion Collection Club | Acesso à plataforma" > aba **Pixels**, e depois cada oferta; e Tráfego > Pixel e trackeamento > pixel 903918118859018 > **Ver detalhes** (lista de telas que o usam). A Mini Mentoria tem produto próprio: conferir a aba Pixels dele separadamente (nenhum anúncio ativo aponta para ela).

Também **não aparece nenhum registro `ads.pixel.event`**. Pela doc, esse é o histórico por contato (navegador e servidor, com status por envio). Zero registros no workspace inteiro reforça a hipótese "sem CAPI ativa" [H].

---

## 3. Pix gerado × Pix pago: eventos e status (item 3)

### 3.1 Linha do tempo real, nos dois compradores (evidência da ficha do contato) [E]
| Evento ClickMax | Comprador A (24/11) | Comprador B (24/11) |
|---|---|---|
| `checkout.attempt.v1` | 17:48:31 | 18:07:43 |
| `checkout.transaction.created.v1` (status `pending`, tipo `pix`) | 17:48:35 | 18:07:46 |
| `checkout.pix.generated.v1` | 17:48:35 | 18:07:46 |
| `checkout.transaction.paid.v1` | 17:50:06 (91 s depois) | 18:08:37 (51 s depois) |
| Expiração do Pix | 30 min depois da emissão (18:18Z / 18:37Z) | idem |

- A venda na lista de vendas fica `status: paid`; antes disso a transação está `pending` (enum de status de venda do ClickMax: canceled, chargedBack, dispute, failed, paid, pending, refunded, refunding, refund_rejected). **"waiting_payment" não é status do ClickMax**: é o evento `ticto-webhook.order.waiting_payment`, que só existe na integração de webhook de entrada da Ticto (usada para checkout Ticto externo, não para estas vendas). [E]
- Se o Pix vence: evento `pix.expired.v1`. Nas 4 ofertas pedidas, 20 a 25/11: 0 expirados, 0 Pix pendente (D §7.2). [E]
- A transação guarda `trackingId` (um por tentativa) e o número do pedido Ticto (`TOP…`) e da cobrança (`TPP…`). **Esses IDs são os candidatos a `event_id` de Purchase** (seção 7). [E]

### 3.2 O que significa "pix_generated = 4 e purchase_approved = 4 em 24/11, todos pagos"
- É a contagem de **visitantes distintos** do funil de analytics. Nesse funil, cada etapa conta quem chegou nela **ou em qualquer etapa posterior** (por isso form_view = form_submit = initiate_checkout = 322–323 em 24/11: é artefato, não comportamento). Então "4 e 4" quer dizer: nenhum Pix gerado ficou sem pagamento **entre quem foi medido**. [E, ferramenta `visitors_conversion_funnel`: page_view 365 → … → purchase_approved 4]
- Corresponde às vendas: 4 pagas em 24/11 (2 reais + 2 testes do Bruno). Zero Pix gerado e não pago em 24/11 é plausível para tráfego muito pequeno e Pix pago em ~1 a 2 minutos, mas **amostra de 4 não prova nada** sobre conversão Pix gerado → pago. [INF]
- Limite: tentativas que morrem dentro do processamento da Ticto (cartão recusado, antifraude, Pix gerado e expirado dentro do checkout deles) só aparecem no ClickMax se a Ticto repassar. [NC] Como confirmar: extrato Ticto de 22 a 25/11 com todos os status.

---

## 4. Valor e moeda (item 5)

[E] Código embutido da página (HTML baixado de /inscricao-47, ~273 KB):
- Navegador: `trackPurchaseEvent(e){ fbq("track","Purchase",{value:e,currency:"BRL"}); postToParent({type:"purchase",value:e/100}) }`.
- Quem chama: `handlePixResponse`, `handleBoletoResponse`, `handleCreditResponse` com `trackPurchaseEvent(totalAmount/100)`. Se `totalAmount` vem em centavos (o ClickMax guarda centavos: `saleValue: 9700`), então `fbq` recebe **97** (correto) e o `postMessage` leva **0,97** (`97/100`): **divisão por 100 duas vezes** nesse caminho. Isso só importa se o iframe de produção usar esse código e se a página-mãe repassar o valor ao pixel dela (a página-mãe não tem pixel; o SDK aceita `value` ≤ 20000 e passa a `fbq trackSingle`). Hipótese, não observada. [H]
- Caminho do SDK (o que o doc descreve): `value = amountCents/100`, `currency` padrão BRL. [E, código]
- Nas vendas: `saleValue` 9700 e 4700 em centavos, `currency BRL`; doc de CAPI exige envio em reais com `currency`. [E]
- Meta: `action_values_omni_purchase` nulo, então **não há valor recebido para comparar**. Valor/moeda efetivamente recebidos: [NC]; verificar no Testar eventos (campo `value` e `currency` do Purchase de teste, esperado 47,00 ou 97,00 BRL).

Meta (doc oficial): na API de Conversões, `event_name`, `event_time` e `user_data` são obrigatórios; `event_id` é recomendado; valor e moeda vão em `custom_data` (para Purchase o Meta espera os dois, a tabela de parâmetros que li não os marca como obrigatórios: conferir a doc vigente antes de implementar). Fonte: developers.facebook.com, Server Event Parameters.

---

## 5. Por que as vendas reais vieram sem UTM (item 4)

### 5.1 URLs reais dos anúncios (Windsor, `url_tags`) [E]
| Anúncio | utm_source/medium | utm_campaign | utm_content | utm_term | sck | ad_id/campaign_id |
|---|---|---|---|---|---|---|
| 120250538593890016 VIDEO 01 NARRATIVA | meta / paid | plataforma47_vendas | video01 | **não tem** | **não tem** | **não tem** |
| 120250554660270016 VIDEO 02 LONGA | meta / paid | plataforma47_vendas | video02_longa | **não tem** | **não tem** | **não tem** |
| 120250554662510016 VIDEO 02 CURTA | meta / paid | plataforma47_vendas | video02_curta | **não tem** | **não tem** | **não tem** |
| Conjunto LT47 (5 anúncios) | meta / paid | lt47 | nome do criativo | `{{ad.id}}` | `{{campaign.id}}` | `ad_id={{ad.id}}`, `campaign_id={{campaign.id}}` |
| Form R$ 47 direto | meta / paid | form47direto | video02 / carrosselC9 | não | não | não |
| **Form R$ 270 (9 anúncios, campanha 120250521777310016)** | `url_tags` **nulo** | | | | | |
- Os anúncios de venda direta usam `utm_content` com **nome** do criativo, não `{{ad.id}}`. Pela doc do ClickMax ("A marcação usa só o nome ... funciona até alguém renomear") isso liga a venda ao anúncio por nome, mas não a um ID, e **não há `utm_term`, `sck`, `ad_id` nem `campaign_id`**. Só a LT47 tem o conjunto completo. [E]
- A campanha de formulário R$ 270 não tem `url_tags` (é formulário nativo; a UTM `inscricao-270` vem do caminho depois do formulário, que a ferramenta não mostra). [E+NC]
- Os criativos "curta" apontam para `/inscricao-47#pagar`. Ao colar `?utm_...` depois de um `#pagar` o navegador pode tratar a UTM como parte do fragmento e não da query: [H], teste simples (abrir o link do anúncio com a UTM e ver se `location.search` carrega os parâmetros). Não verificado.

### 5.2 O que a página faz com os parâmetros [E]
HTML da página, rotina do checkout embutido: `for ([n,r] of new URLSearchParams(location.search)) iframe.src.searchParams.set(n,r)` e também `currentPageUrl = location.href`. **Ou seja, a página repassa ao iframe TODOS os parâmetros da URL em que está, e a URL completa.** Doc `/guides/track-conversions-with-src`: "O campo aparece vazio na venda: confira se o parâmetro estava na URL **no momento em que o comprador abriu o checkout**". Doc do bloco Ticto: UTMs, `src`, `sck` seguem ao checkout; há um `TODO(verify)` da própria doc: confirmar numa compra real que a Ticto devolve o `sck` no webhook (`query_params`). Isso é só para o bloco Ticto externo, mas mostra que a devolução do `sck` pela Ticto ainda não foi verificada nem pelo ClickMax. [E]

### 5.3 Os dados das 8 vendas (campos de UTM) [E]
| Venda (UTC) | Valor | utmSource/Medium/Campaign/Content/Term | src | sck |
|---|---|---|---|---|
| 20/11 18:53 (teste Bruno) | 19 | nulo | nulo | nulo |
| 21/11 02:29 (R$270, falhou) | 270 | **site / pagina / agendamento-diagnostico** | nulo | nulo |
| 21/11 11:18 (teste) | 47 | nulo | nulo | nulo |
| 22/11 20:47 (teste) | 270 | nulo | nulo | nulo |
| 24/11 03:42 (teste) | 97 | nulo | nulo | nulo |
| 24/11 17:48 (REAL, comprador A) | 97 | nulo (7 campos nulos em `sales_get_utms`) | nulo | nulo |
| 24/11 18:07 (REAL, comprador B) | 97 | nulo (idem) | nulo | nulo |
| 24/11 19:12 (teste Bruno, R$47) | 47 | nulo | nulo | nulo |

- **A venda do teste do Bruno de 24/11 19:12Z não tem UTM**, e o histórico de visitas do contato de testes mostra que ele sempre entra direto (canal `direct`, sem UTM, pela página `/etapa-desenvolvimento`). Então esse teste **não prova** nada sobre o repasse de UTM: ele não usou um link com UTM. [E]
- A venda de 21/11 02:29 **tem UTM** (`site/pagina/agendamento-diagnostico`): é a única prova de que **o ClickMax grava UTM na venda quando a URL do checkout traz UTM**. [E] Portanto o mecanismo existe e funciona nesse caso.

### 5.4 O caminho real de cada comprador real [E+H]
- **Comprador A (17:48Z):** `visitors_lead_journey` mostra 3 dispositivos ligados. O visitante que fez o checkout (`form_submit`, ligado às 17:47:54) teve a **primeira sessão às 17:39 pelo canal facebook, `utm_source=meta`, `utm_medium=paid`, `utm_campaign=inscricao-270`, página /inscricao, sem ID de clique (`clickIds` vazio)**. Antes, às 17:42, houve cliques em um **link de mensagem** (`link.clickmax.io/pikl0zyE`, canal "direct", sem UTM) e já em 23/11 14:29 e 15:59 (mesmo link). A transação guarda `linkCheckout = .../inscricao` **sem query**. Conclusão [H]: o comprador veio do formulário R$ 270 → WhatsApp (mensagem com link) → /inscricao; na hora de abrir o checkout a URL não tinha UTM (link da mensagem), e a venda guarda só a URL corrente. A UTM Meta existe no analytics de sessão, **não na venda**.
- **Comprador B (18:07Z):** `visitors_lead_journey` volta **vazio** (nenhum visitante ligado ao contato), e a transação tem `linkCheckout` **vazio**. [E] Hipótese [H]: abriu o checkout por um link direto da oferta (sem página-mãe medida), por exemplo link de pagamento enviado em conversa. Origem real: [NC]; perguntar ao comprador ou checar a conversa dele na Bela.
- Ambos pagaram no Pix; nenhum evento de pixel foi registrado para eles. [E]

### 5.5 Resumo: por que a venda sai sem UTM
| Causa | Evidência | Peso |
|---|---|---|
| A venda grava a URL do momento do checkout, não a primeira origem do visitante | Doc `/guides/track-conversions-with-src`; comprador A tinha UTM na 1ª sessão e venda nula | Alta [E+H] |
| Caminho de mensagem/WhatsApp e link direto, sem UTM | Jornada A (link de mensagem), B (sem visitante, `linkCheckout` vazio) | Alta [E] |
| Anúncios sem `utm_term`/`sck`/ID | `url_tags` de venda direta e de formulário | Média: não explica "tudo nulo", mas impede casar com campanha/conjunto/anúncio [E] |
| `#pagar` pode engolir a UTM | Anúncios "curta" | Baixa-média [H] |
| A Ticto não devolve `sck`/UTM | Doc ClickMax: `TODO(verify)` | [NC]. Se a venda de 21/11 gravou UTM, o ClickMax guarda do lado dele; a Ticto parece não ser necessária para isso |
| Falta de fbclid | `clickIds: []` mesmo na visita Meta (comprador A) | O ClickMax **não está guardando clique do Meta** (ou o link não o trouxe). Sem fbc o CAPI perde a melhor chave de atribuição [E+H] |

---

## 6. Parâmetros nativos da Ticto (`src`, `sck`, `utm_*`) e o mapeamento ClickMax (item 4, parte final)

- Doc ClickMax: `src` e `sck` são aceitos "exatamente como as outras plataformas de checkout", gravados na venda no momento da compra e devolvidos em webhooks de saída e CSV; **a plataforma não inventa origem** (campo vazio se o link não trouxe). Cada valor tem até 255 caracteres. [E]
- Na venda via Ticto (bloco externo), o ClickMax compõe o `sck` como `cmp_<página>|<sck do link>` e o repassa; nas vendas do checkout nativo usado aqui, o campo `src/sck` aparece em `sales_get_utms` (todos nulos nas 2 reais). [E]
- Parâmetros próprios da Ticto, documentação pública: **não consegui** localizar documentação oficial pública da Ticto sobre `src/sck/utm` ou pixel (a busca devolveu só terceiros). [NC] Como confirmar: painel Ticto > Tictools > Webhooks (payload com `query_params`) e suporte da Ticto.

---

## 7. Deduplicação (item 6)

- Doc ClickMax: mesmo identificador de evento no navegador e na CAPI, e a Meta conta uma conversão. O SDK usa `eventID` derivado de `evento-sourceId-serviceId`. [E]
- Regra da Meta (doc oficial): a deduplicação exige **mesmo `event_name` e mesmo `event_id`** em navegador e servidor, dentro de 48 h; com os dois chegando em ~5 min a Meta prefere o do navegador; `event_id` recomendado; para compra, número do pedido serve como `event_id`. [E]
- No código embutido do HTML, `fbq("track","Purchase",{value,currency})` **sem `eventID`** (só o `trackSingle` do SDK leva). Se o iframe usar esse caminho, o navegador e a CAPI **não deduplicam** e o Purchase conta em dobro quando a CAPI for ligada. [H, só se o código dormente for o ativo]
- Mesmo `value`: só dá para conferir no Gerenciador de Eventos (Visão geral > Deduplicação). [NC]

---

## 8. Identificação de campanha/conjunto/anúncio e atribuição Meta (item 7)

### 8.1 Campos que chegam e que não chegam à venda
| Campo | Chega à venda? |
|---|---|
| utm_source / medium / campaign | Só se estiver na URL no momento do checkout (nas 2 vendas reais: não) |
| utm_content (criativo) | Idem; nome do criativo, não ID, na venda direta |
| utm_term = {{ad.id}} | Só LT47 tem o parâmetro no anúncio; nenhuma venda de LT47 existe |
| sck = {{campaign.id}} | Só LT47 |
| ad_id, campaign_id | Só LT47 |
| conjunto (adset) | **Nenhum anúncio manda `{{adset.id}}`** |
| fbclid / fbc / fbp | `clickIds: []` na visita Meta do comprador A; `_fbp/_fbc` não existem na página-mãe (sem pixel nela) [E] |
| referrer | Visita A: referrer = a própria página; B: nada |
| createdLead | O iframe recebe `createdLead=true/false` (lead criado no funil antes do checkout); valor nas vendas: [NC] |

### 8.2 Como o Meta atribui e por que a conciliação falha
- Janela das campanhas de venda: clique 7 dias (C_pixel_capi §7); pedido de leitura com 7d_click,1d_view retornou os mesmos zeros. [E]
- O Meta só atribui Purchase a anúncio quando o evento (navegador ou CAPI) chega **com chave de correspondência**: fbc/fbp (clique e navegador) ou e-mail/telefone/CPF em hash (`user_data`). Nesta conta:
  1. Nenhum Purchase foi observado (seção 1). 
  2. O comprador A veio de **anúncio de formulário nativo** (campanha "FORM INSCRIÇÃO → LANDING → R$ 270", atribuição do Meta não definida, sem `url_tags`), depois por WhatsApp. Esse caminho só casa se o CAPI mandar e-mail/telefone iguais aos do formulário. [H]
  3. O comprador B não tem visitante ligado. [E]
  4. Sem `utm_term`/`sck`/IDs, nem o ClickMax consegue dizer qual anúncio. [E]
- Conversão IC ≈ LPV continua: IC é carregamento do checkout (C §9). Em 24/11 a venda direta passou de 96 para **111 IC** e 91 LPV na leitura de hoje (o Meta revisa números por 2 a 3 dias). [E]

---

## 9. Conciliação 20 a 25/11 (item 8)

### 9.1 Vendas confirmadas no ClickMax (sem dados pessoais)
| Data (UTC) | Oferta | Valor | Origem | Real? | Meta Purchase |
|---|---|---|---|---|---|
| 24/11 17:48 | R$ 97 (c298aaed) | 97,00 | Meta (form R$ 270) → WhatsApp → /inscricao | **Real** | 0 |
| 24/11 18:07 | R$ 97 (c298aaed) | 97,00 | Desconhecida (sem visitante, sem URL) | **Real** | 0 |
| 24/11 03:42 | R$ 97 | 97,00 | Teste Bruno | Não | n/a |
| 24/11 19:12 | R$ 47 (668391e7) | 47,00 | Teste Bruno | Não | n/a |
| 22/11 20:47 | Clube R$ 270 | 270,00 | Teste Bruno | Não | n/a |
| 21/11 11:18 | Terra/Capital A R$ 47 | 47,00 | Teste Bruno | Não | n/a |
| 20/11 18:53 | Ferramenta 20 R$ 19 | 19,00 | Teste Bruno | Não | n/a |
| 21/11 02:29 | Clube R$ 270 | 270,00 | **falhou** | Não | n/a |
- Reais: **2 vendas, R$ 194,00 bruto, R$ 175,46 líquido (taxa 9,27 por venda)**. 25/11: nenhuma venda (consulta de hoje). Cartão, reembolso, chargeback: 0. [E]

### 9.2 Meta por campanha (Windsor, janela 7d_click,1d_view, conta 1271873041294684)
| Campanha | Gasto 20–25/11 (R$) | Cliques | LPV | IC | AddPaymentInfo | Purchase | Valor |
|---|---|---|---|---|---|---|---|
| [VENDAS][PLATAFORMA R$97] 120250538576770016 (24/11: 70,19; 25/11: 49,06 parcial) | 119,25 | 245 | 127 | 152 | 2 | **0** | 0 |
| [ZC2][SALES][LT47][PARCEIRO ZION] 120250557994600016 | 17,38 | 36 | 27 | 28 | 0 | **0** | 0 |
| [FORM R$ 270] 120250521777310016 | 209,86 | 436 | 3 | 0 | 0 | **0** | 0 |
| [FORM R$ 47 DIRETO] 120250557420830016 | 13,68 | 26 | 1 | 0 | 0 | **0** | 0 |
| [CURSO TERRENO R$ 47] 120250498726810016 (pausada) | 63,97 | 230 | 137 | 0 | 0 | **0** | 0 |
| [LAND BANK] 120250113109820016 (pausada) | 79,75 | 87 | 8 | 0 | 0 | **0** | 0 |
| **Total** | **503,89** | | | | | **0** | **0** |

### 9.3 Diferença
- ClickMax: 2 compras reais, R$ 194,00. Meta: 0 compras, R$ 0,00. **Diferença: 2 compras (100%) e R$ 194,00 sem atribuição.**
- **Custo por venda real** (gasto 20–25/11 ÷ 2): R$ 251,95 (todas as campanhas), R$ 104,93 (só formulário R$ 270 se as 2 vendas viessem dele), R$ 59,63 (só venda direta). Hipóteses; a origem do comprador B é [NC]. Faturamento bruto R$ 194,00 contra R$ 503,89 de gasto.
- Resultado de mídia 20–25/11 (líquido 175,46 − gasto 503,89): **−R$ 328,43**. Não é lucro; é só mídia vs. receita líquida, sem custos de produto/Bela.

---

## 10. O que o Gerenciador de Eventos precisa mostrar e roteiro para o Bruno (item 9)

### 10.1 O que um rastreamento saudável mostra
| Tela | Esperado |
|---|---|
| Testar eventos (navegador) | PageView e InitiateCheckout (ou AddToCart) ao abrir a página; AddPaymentInfo ao gerar o Pix; **Purchase só depois do Pix pago** |
| Testar eventos (servidor) | Purchase com "Servidor", `value` e `currency BRL`, `event_id` igual ao do navegador (badge "Desduplicado") |
| Visão geral | Purchase com "Navegador e Servidor", ou só "Servidor" para Pix |
| Diagnóstico | Sem alerta de "Parâmetros ausentes (value/currency)", "Eventos duplicados", "event_id ausente" |
| Qualidade de correspondência (EMQ) | Purchase com nota 6 ou mais (e-mail + telefone + fbp/fbc) |
| Deduplicação | Taxa de eventos desduplicados próxima de 100% dos Purchase que vêm das duas pontas |

### 10.2 Roteiro passo a passo (Bruno, sem custo de anúncio; a única cobrança é a compra de teste, reembolsável)
1. **Ver a configuração (só leitura).** ClickMax > Tráfego > Pixel e trackeamento > pixel 903918118859018. Anote: token guardado? "Usar API de Conversão" ligada? Eventos: Comprou (navegador/servidor), filtro de Formas de pagamento (Pix marcado?), "Abriu o checkout" com "Só contar depois dos dados pessoais"? Abra **Histórico de envio** e anote as linhas de 24/11 (Enviado / Não enviado, e o motivo). Abra **Ver detalhes** e anote em quais produtos/ofertas/páginas ele está marcado.
2. **Produto/oferta.** Produtos > Zion Collection Club > aba Pixels e cada oferta (R$ 97 e R$ 47) e Mini Mentoria: quais pixels aparecem.
3. **Testar eventos no Meta.** Gerenciador de Eventos > o conjunto de dados do pixel 903918118859018 > Testar eventos. Copie o "código de teste" e **não** o cole no ClickMax sem avisar (enquanto o código de teste estiver no pixel, os eventos não contam como conversão).
4. **Abrir sem rolar e sem clicar** a página de venda em janela anônima e no celular, colando o link **com UTM completa** (inclusive o link `...#pagar`). Esperado: PageView e IC/AddToCart. Anotar se `location.search` manteve as UTMs.
5. **Gerar o Pix e NÃO pagar.** Esperado: AddPaymentInfo. **Se aparecer Purchase aqui, é o defeito "Purchase no Pix gerado".** Anotar `value` e `currency`.
6. **Pagar o Pix (oferta de teste de menor valor, com reembolso depois).** Esperado: Purchase **depois**, com `value = 47,00` (ou o valor da oferta usada) e BRL, vindo por Servidor (e por Navegador se ele ainda estiver aberto). Anotar o `event_id` do navegador e do servidor.
7. **Conferir no ClickMax** a ficha do contato de teste > aba **Eventos de pixel**: deve listar o Purchase com status Enviado. Hoje essa aba/atividade está vazia no workspace.
8. **Diagnóstico e Visão geral.** Anotar: método de conexão, deduplicação, EMQ do Purchase.
9. **Reembolsar a compra de teste** pelo ClickMax/Ticto (7 dias, CDC) e conferir que o reembolso não gera outro Purchase.
10. Mandar para o Claude: prints do passo 1, 3, 5, 6, 8.

---

## 11. PLANO TÉCNICO DE CORREÇÃO (não implementado)

### 11.1 Requisitos e estado atual
| Requisito | Estado hoje |
|---|---|
| R1 Purchase só após pagamento aprovado | Não comprovado; hoje 0 Purchase chegam; o código embutido dispara ao gerar o Pix |
| R2 value e currency corretos | Não observado; risco de divisão dupla por 100 no caminho de `postMessage` |
| R3 CAPI funcionando | Sem evidência; 0 registros `ads.pixel.event` no workspace |
| R4 Deduplicação | Doc diz que há; código embutido sem `eventID`; sem teste |
| R5 Campanha/conjunto/anúncio na venda | Falta ID de anúncio (venda direta), conjunto, fbclid; só LT47 tem `ad_id/campaign_id/sck` |
| R6 Persistência das UTMs | A venda guarda só a URL do checkout; a primeira origem do visitante não vai para a venda |
| R7 Conciliação | Impossível sem R1, R3, R5, R6 |
| R8 Pix gerado ≠ Pix pago | Eventos separados existem no ClickMax; falta garantir no Meta |

### 11.2 Opções
| Opção | O que é | Prós | Contras/riscos | Esforço | Executa |
|---|---|---|---|---|---|
| **A. Corrigir a configuração nativa do ClickMax (recomendada primeiro)** | Verificar/ligar token CAPI e "Usar API de Conversão" no pixel; garantir Purchase ligado em navegador e servidor com Pix marcado; "Só contar depois dos dados pessoais" no IC; pixel marcado no produto/oferta; tirar o "Código de teste"; padronizar `url_tags` com `utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}&utm_content` com ID; ligar ViewContent se for otimizar para ele; **ligar a mesma marcação em links de mensagem/Bela** | Menor esforço; dedup, `event_id` e CAPI já são do ClickMax; mantém a Ticto como está | Depende de o ClickMax gravar corretamente (hoje 0 pixel events); sem fbc se a página não guardar o clique; venda grava só URL do checkout | Baixo: 1 a 2 h de painel + 1 compra de teste | Bruno (painel ClickMax e Meta), Claude (roteiro, texto das `url_tags`, conferência de leitura) |
| **B. Pixel direto + Purchase pela Ticto** | Colocar o pixel/CAPI nativo da Ticto (se existir no painel dela) e desligar o do ClickMax para Purchase | Evento na origem do pagamento | Duplicidade com o ClickMax; Ticto é processador por trás do ClickMax: o pixel Ticto pode nem existir para esse fluxo; perde UTM; sem prova de que o painel Ticto está acessível | Médio | Bruno (painel Ticto), ChatGPT (pesquisa de doc), Claude |
| **C. CAPI própria via webhook (ClickMax/Ticto → servidor)** | Servidor mínimo que recebe o webhook de saída de `checkout.transaction.paid` (e Pix gerado, se quiser), monta `user_data` com hash, `event_id = trackingId` ou nº do pedido, `fbc/fbp` guardados na sessão, `value` em reais e `BRL`, e chama a API de Conversões | Controle total (valor, moeda, `event_id`, `external_id`, fbc/fbp, `action_source: website`); permite reenvio e log próprio; ouro para conciliar | Precisa de hospedagem, guarda de token (Bruno cola, nunca no chat), LGPD e manutenção; risco de duplicar com a CAPI do ClickMax (resolver desligando uma, ou mesmo `event_id`); precisa de gravar fbc/fbp na página | Alto: 1 a 3 dias + testes | Claude (código/teste local), Bruno (token, hospedagem, aprovação), ChatGPT (revisão) |
| **D. GTM server-side** | Contêiner GTM web + servidor que recebe `dataLayer` | Padrão de mercado | O checkout fica no iframe do ClickMax (sem dataLayer da página-mãe do pagamento); custo de servidor; ClickMax não expõe `purchase` ao GTM da página sem valor (doc: "O pixel da página recebe a compra aprovada sem valor" no bloco Ticto) | Alto | Claude + Bruno |
| **E. Plano B de contingência** | Sem mexer em pixel: casar venda do ClickMax com anúncio por link de rastreio por criativo (`utm_content` com ID) e pesquisa pós-compra ("onde você viu?") e conciliar em planilha | Funciona hoje | Não ensina o algoritmo do Meta; manual | Baixo | Claude, Bruno |

### 11.3 Recomendação
1. **Fase 0 (hoje, sem custo):** diagnóstico do roteiro 10.2 passos 1 a 3 (só leitura). Decide A ou C.
2. **Fase 1 = Opção A** (corrigir config nativa + padronizar `url_tags` e links de mensagem). É a única que o Bruno resolve sozinho em horas.
3. **Fase 2:** teste com compra real do Bruno + reembolso (roteiro 10.2). Se o Purchase aprovado chegar por Servidor, com value/currency/event_id certos, **parar aqui**. Se não chegar, ir para **Opção C** (CAPI própria via webhook) mantendo o ClickMax só como fonte do evento.
4. **Fase 3 (só depois de Purchase estável):** trocar a otimização das campanhas para Purchase e ligar de novo o gasto (exige "aprovado" do Bruno; teto atual R$ 0, tudo pausado por regra do projeto; este plano não toca em campanha).
5. **Não** adotar B e D agora: dependem de acesso/estrutura que não foi confirmado e acrescentam duplicidade.

### 11.4 Passos detalhados da Opção A (checklist)
1. Anotar o estado atual (screenshots) antes de qualquer mudança.
2. Pixel 903918118859018: confirmar Token (colado pelo Bruno no painel, nunca no chat); "Usar API de Conversão" ligada; "Testar token" ok; "Código de teste" vazio fora do teste.
3. Evento "Comprou": navegador e servidor ligados; Formas de pagamento com **Pix e cartão** marcados.
4. Evento "Abriu o checkout": ligar "Só contar depois dos dados pessoais" (IC passa a medir intenção).
5. Marcar o pixel no **produto/oferta** (R$ 97, R$ 47, Mini Mentoria) e conferir em "Ver detalhes".
6. Padronizar `url_tags` de todos os anúncios (ID no `utm_content`, `utm_term={{ad.id}}`, `sck={{campaign.id}}`, `ad_id`, `campaign_id`, e `adset_id={{adset.id}}`), e remover `#pagar` dos destinos ou colocar a UTM antes do `#`.
7. Links de mensagem (Bela, aberturas, `link.clickmax.io`): acrescentar `utm_source/medium/campaign` e um `src` próprio ("whatsapp_bela") para a venda carregar **origem do canal**; o ID do anúncio original só dá para ligar se a Meta/ClickMax guardar `ad_id` do lead (campo do formulário/CRM): hipótese a testar.
8. Fazer o roteiro 10.2 e anotar os resultados.

### 11.5 Critérios de aceite por requisito
| Requisito | Critério de aceite (como provar) |
|---|---|
| R1 Purchase só após pagamento aprovado | No Testar eventos: gerar Pix e **não pagar** não produz Purchase; pagar produz exatamente 1 Purchase em até 5 min. Histórico de envio do pixel mostra "Enviado" para o `checkout.transaction.paid` e nada para `pix.generated` como Purchase |
| R2 value e currency | O Purchase de teste mostra `value` igual ao da venda no ClickMax (97,00 ou 47,00, nunca 0,97 nem 9700) e `currency=BRL` |
| R3 CAPI funcionando | Testar eventos mostra o Purchase "Servidor"; aba "Eventos de pixel" do contato lista o envio; Visão geral mostra "Servidor"; `ads.pixel.event` deixa de voltar vazio |
| R4 Deduplicação | Visão geral > Deduplicação mostra Purchase desduplicado; um Purchase de navegador + um de servidor com o mesmo `event_id` contam **1** |
| R5 Campanha/conjunto/anúncio | Uma compra de teste feita a partir de um anúncio de teste (link com as `url_tags` novas) grava na venda `utm_content`, `utm_term`, `sck` (e `ad_id`/`campaign_id`, se mapeados) e o Meta atribui o Purchase ao anúncio em até 24 a 48 h |
| R6 Persistência de UTMs | Compra com link de mensagem (sem UTM do anúncio) ainda grava a origem do canal (`src`), e a venda mostra UTM mesmo quando o comprador volta por outro link no mesmo dia (teste real de Bruno em 2 sessões) |
| R7 Conciliação | Tabela diária ClickMax × Meta com diferença de compras ≤ 10% por campanha (ou diferença explicada: venda sem clique de anúncio), usando UTMs/IDs da própria venda |
| R8 Pix gerado ≠ Pix pago | Pix gerado vira AddPaymentInfo, Pix pago vira Purchase; contagens do Meta: Purchase ≤ Pix pagos do ClickMax e AddPaymentInfo ≥ Pix gerados; reembolso não gera novo Purchase |

### 11.6 Riscos gerais
- Ligar a CAPI sem desligar caminho duplicado pode contar Purchase em dobro (usar o mesmo `event_id`).
- Mudar o evento de otimização das campanhas muda a base de aprendizado: só com "aprovado" de Bruno.
- Teste com pagamento real é necessário (Pix de R$ 47 menos taxas, reembolsável), não se simula Pix pago.
- O Meta só aceita eventos de até 7 dias: a CAPI atrasada não corrige o passado.
- Os 2 Purchase reais de 24/11 só poderiam ser reenviados ao Meta até 01/12 (limite de 7 dias do `event_time`). Reenviar manualmente (CAPI própria com `event_time` real) só é útil se feito até 01/12 e se tiver chave de correspondência: avaliar com Bruno (é mexer no pixel, exige "aprovado").

---

## 12. Pendências e perguntas ao Bruno (nada foi feito sem "aprovado")
1. Executar o roteiro 10.2 (ao menos passos 1 a 3) e mandar prints.
2. Extrato da Ticto 22 a 25/11 (todos os status, motivo de recusa, `query_params`/UTMs recebidas, nº do pedido).
3. Confirmar se existe pixel/CAPI no painel da Ticto para esse produto.
4. Como o comprador B recebeu o link do checkout (link direto?), e se o comprador A veio do formulário R$ 270.
5. Aprovar mudanças de `url_tags` (os anúncios estão ativos; mexer em anúncio exige "aprovado").

## 13. Efeitos colaterais desta auditoria
Somente leituras (docs, vendas, atividades por contato, jornada de visitante, Windsor, 1 download público de HTML). Nenhuma escrita em ClickMax, Meta ou Windsor; nenhum evento de pixel foi disparado; nenhuma venda criada. Esta rodada não repetiu visitas de navegador.
