# Funil de eventos (P0) · Mini Mentoria de Estruturação Zion

> **Atualização 25/11/2026 (funil híbrido): são 8 eventos.** Foram acrescentados **Lead** (antes de tudo) e **Reembolso** (depois de tudo). A tabela de 8 etapas, o proxy recomendado e o estado de cada evento estão no **§7**, que vale sobre as seções 1 a 6 (7 eventos, mantidas como histórico). A prova em ambiente de teste está em `VALIDACAO_EM_TESTE.md`.

Autor: DATA · 25/11/2026 · Cumpre a regra P0 de Bruno: **nenhum cliente chega ao checkout sem saber o que compra, quanto paga e o que recebe**, e a medição precisa separar quem **viu**, quem **demonstrou intenção qualificada**, quem **começou a comprar**, quem **gerou Pix**, quem **pagou** e quem **recebeu**.
Legenda: **[E]** confirmado em documentação oficial do ClickMax lida em 25/11/2026 ou em leitura de ferramenta · **[NC]** não confirmado (diz o teste que resolve) · **[H]** hipótese. Estado **ATUAL** = antes de qualquer correção; nada aqui foi aplicado em produção.
Parâmetros comuns a todo evento: `content_name` = "Mini Mentoria de Estruturação Zion", `content_ids` = `["mm47"]`, UTMs do `PADRAO_UTM.md`, `currency` = BRL. Valor sempre em **reais com ponto** (47.00), nunca em centavos.

## 1. Regras que valem para o funil inteiro
1. **Carregamento automático do iframe do checkout NÃO é intenção.** Hoje o evento de início de checkout dispara quando o iframe carrega [A: auditoria H], então ele mede visualização da página, não vontade de comprar.
2. **Pix gerado NÃO é Purchase.** Gerar Pix é intenção forte, não receita. Purchase só com pagamento aprovado (Pix pago ou cartão aprovado).
3. **Clique no CTA com preço = clique qualificado.** O botão padrão é "QUERO ACESSAR A PLATAFORMA POR R$47"; quem clica sabe o preço. Clique em botão que só rola a página (sem preço) **não** é qualificado.
4. **Um evento, um significado, um nome.** Eventos padrão da Meta só para o que eles significam (ViewContent = viu o conteúdo/oferta; InitiateCheckout = começou a comprar; Purchase = pagou). O que não tem nome padrão vira evento **custom** e não otimiza campanha.
5. **Anúncio não é vencedor só por CPC baixo ou muitos checkouts.** O objetivo é comprador.

## 2. Os 7 eventos

| # | Etapa | Nome padrão | O que dispara | Sistema | Parâmetros | Deduplicação | Estado ATUAL |
|---|---|---|---|---|---|---|---|
| 1 | Visualização da landing | `PageView` | Abrir a página de vendas publicada | Pixel no navegador (ClickMax insere); só navegador por desenho [E] | UTMs na URL; `fbc/fbp` do navegador | Contagem simples (não vai pela CAPI [E]) | **[E] funciona** em página publicada; preview do editor não rastreia [E] |
| 2 | Visualização da oferta | `ViewContent` (pixel) e `element_visible` (ClickMax) | A seção da oferta entra na tela, **ou** abrir a página separada de oferta | Ver §3: pixel só por página marcada "Página de conteúdo"; por seção só no ClickMax | `content_name`, `content_ids`, `value 47.00`, `currency BRL` (pixel: **[NC]** se o ClickMax aceita enviar esses parâmetros no ViewContent nativo) | `event_id` do navegador [NC] | **Desligado**: `pixelViewContent=false` nas páginas [E, leitura de `pages_get`]. Nada mede a oferta hoje |
| 3 | Clique no CTA com preço (**clique qualificado**) | custom `QualifiedCtaClick` (desejado) · `button_click` com `elementId` do CTA (ClickMax, existente) | Clique em qualquer botão cujo texto traz o preço | ClickMax mede `button_click` sem instalar nada [E]; **não há** caminho documentado para o pixel (§3) | `elementId` do botão (cta-0…cta-5); UTMs da sessão | Não aplicável (métrica interna) | **[E] mecanismo existe** (os 6 CTAs da página aparecem no mapa de gatilhos com `button_click`); **[NC]** se o painel de relatórios abre por botão. **Não chega ao Meta** |
| 4 | Início efetivo de checkout | `InitiateCheckout` | Visitante **informa nome e e-mail** no checkout | Pixel do ClickMax (navegador **e** servidor) com a opção "Só contar depois dos dados pessoais" [E] | `value`, `currency`; UTMs; `content_*` **[NC]** | Mesmo identificador no navegador e na CAPI; a Meta conta 1 [E] | **Errado**: dispara ao **carregar o iframe** [A]; a opção está desligada. Correção = tutorial A4 e E3 |
| 5 | Pix gerado | custom `PixGenerated` (opcional) · `pix_generated` (ClickMax, interno) | O checkout gera o QR/código Pix | ClickMax (evento interno e gatilho de automação "PIX gerado" [E]); para a Meta, **só** pelo receptor opcional `capi-webhook` (**desligado por padrão**) | `value 47.00`, `currency BRL`, `order_id`, `content_*`, UTMs | `event_id = pix-<id do pedido>` (distinto do Purchase) | O ClickMax **não** manda "Pix gerado" ao Meta como evento próprio [E: o vocabulário de 13 eventos não tem]; `AddPaymentInfo` ("escolheu a forma de pagamento") **não é** Pix gerado. Medição interna: vendas pendentes Pix [E] |
| 6 | Pagamento aprovado | `Purchase` | Venda `paid`: Pix pago ou cartão aprovado | Pixel (navegador) + CAPI do ClickMax (servidor) [E]; alternativa: `capi-webhook` **no lugar** da nativa | `value 47.00` (reais), `currency BRL`, `order_id`, `content_name`, `content_ids`, UTMs, `event_id` | Navegador e servidor com o **mesmo id** do ClickMax [E]; no receptor `event_id = id do pedido` + idempotência | **Só após pago** [E doc: "quando a compra é aprovada"]. Mas: Meta registrou **0 compras** das vendas reais de 24/11 (sem UTM e, provavelmente, sem token CAPI) [A]. Prova pendente: roteiro D/E. Regras de `value`/`event_id` do ClickMax nativo: **[NC]** até a compra de teste |
| 7 | Entrega do produto | custom `AccessDelivered` (opcional) · membro na turma e e-mail de acesso (ClickMax) | Compra aprovada → aluno na turma `087479a3…` + e-mail de acesso; marco forte: **primeiro acesso** ("Membro acessou a área" [E]) | ClickMax (turma, e-mail, área de membros); Meta só pelo receptor opcional (**desligado**) | `order_id`, UTMs, `content_*` | `event_id = access-<id>` | Entrega funciona por turma [A]; **não há evento de entrega** em nenhum sistema de anúncios. Medição = leitura da turma (`member_users_list_by_classroom`) cruzada com as vendas |

### Quem executa cada coisa
- **Já existe e não precisa de ação:** PageView (1), `button_click` interno (3, mecanismo), `pix_generated` interno (5), entrega (7).
- **Painel do ClickMax, Bruno ("aprovado")**: ligar "Só contar depois dos dados pessoais" (4); conferir Comprou com Pix e cartão e token CAPI (6); marcar "Página de conteúdo" **só** na página de oferta (2, §3 opção D).
- **Código pronto, desligado, só com "aprovado" + implantação**: `PixGenerated` e `AccessDelivered` no `capi-webhook` (5 e 7).

## 3. Como medir o clique qualificado e a visualização da oferta dentro das restrições do ClickMax

### 3.1 O que a pesquisa por leitura encontrou
Fontes: `docs.clickmax.io` (guias de eventos do pixel, escolha de pixels por tela, eventos personalizados, Browser SDK, gatilhos), `funnels_page_triggers_catalog`, `pages_get` do rascunho `f690b2c4…`.
1. **Os gatilhos de página (`button_click`, `scroll`, `time_on_page`, `page_viewed`) existem**, e o `triggerMap` do rascunho lista `page_viewed, scroll, time_on_page, exit_intent` e, nos 6 CTAs, `button_click` e `link_click` [E, leitura]. **Mas eles são gatilhos de funil: movem o contato para a próxima etapa do canvas e não iniciam automações** [E, `reference/automation-triggers`]. **Não existe, em nenhuma documentação ou catálogo lido, uma ação "disparar evento do pixel" ligada a esses gatilhos.** Resposta direta: **não, o ClickMax não deixa configurar "scroll até a seção → ViewContent" nem "clique no botão → evento custom no pixel" por menu** [E por ausência em: eventos do pixel, escolha de pixels por tela, custom events, catálogo de gatilhos; ressalva: a interface logada pode ter algo que a documentação não cita, **[NC]** conferir com print do painel do funil, passo E5].
2. **O Browser SDK mede sozinho** `button_click` (com `elementId`), `scroll` (limiar de 75% por padrão), `element_visible`, `page_view`, `initiate_checkout`, `purchase*`, `pix_generated` e outros, nas páginas publicadas, sem instalar nada [E, `reference/events`]. Para virar gatilho/medida, o elemento precisa estar marcado (`.cm-checkout-button`, `data-cx-track="click"`, `data-cx-track="visible"`); **só `<button>`/`<a>` comum não dispara** [E, `reference/browser-sdk/tracking`]. Esses dados ficam **no ClickMax** (análise de visitantes e funil), não no pixel.
3. **Eventos personalizados no pixel** (`cxs('track', ...)`) exigem script; o importador de página **remove todo `<script>`** [lição do ClickMax, regras comuns]. Portanto o caminho "evento custom `QualifiedCtaClick` no pixel da Meta" **não está disponível sem script** e o script não pode ser colado na página importada.
4. **Pixel `ViewContent`**: só nasce se a página estiver marcada **"Página de conteúdo"** (Configurações da Página › Scripts, ou, no canvas do funil, configurações da etapa › Rastreamento). A marcação faz o evento disparar **quando a página abre**, não na rolagem; é o campo `pixelViewContent` (hoje `false`). "Marque as páginas de venda e de conteúdo que você anuncia. Não marque obrigado, checkout nem captura" [E, `guides/pixel-scopes`]. ViewContent só sai pelo navegador [E].
5. **Link de redirecionamento com pixel** (Marketing › Redirecionamentos › Escolher pixels deste link): o clique passa por uma tela em branco e dispara um evento, mas a lista de eventos é **só ViewContent, Contact ou Lead** (o guia cita InitiateCheckout numa tabela, a tela lista três) [E]. Não existe evento "clique qualificado", e marcar um clique de CTA como Lead ensina o algoritmo errado (o próprio guia avisa) [E].
6. **Não testado ao vivo:** se o importador mantém `data-cx-track="visible"` e se o relatório por botão aparece no painel. Para testar sem risco seria preciso importar em página nova de rascunho; não fiz nesta sessão (economia e governança). Fica como passo E5 e E6 do tutorial **[NC]**.

### 3.2 Alternativas comparadas

| | O que mede | Chega ao Meta? | Prós | Contras | Veredito |
|---|---|---|---|---|---|
| **(a) Clique no CTA medido pelo SDK** (`button_click` + `elementId` dos 6 CTAs, já listados no mapa) | Clique qualificado por botão (cta-0…cta-5, todos com preço no texto) | **Não** (fica no ClickMax) | Zero código, zero publicação, já existe [E]; dá taxa clique/visita e quais botões convertem | Não alimenta otimização do Meta; **[NC]** se o relatório separa por botão; leitura por `visitors_*`/funil, não por menu simples | **Adotar como métrica principal do clique qualificado** (análise e conciliação) |
| **(b) Âncora `#oferta` + UTM** | Nada (âncora não vai ao servidor [H]) | Não | Boa para o visitante cair na oferta | **Não mede**; só rola a página; não use como evento | Usar só para navegação; nunca como métrica |
| **(c) "Abriu o checkout" com "Só contar depois dos dados pessoais"** (A4) | Início **efetivo** de checkout (nome e e-mail informados) | **Sim** (InitiateCheckout, navegador e servidor) | Um clique no painel; corrige o erro do iframe; alimenta o Meta com evento de intenção real [E] | É intenção **mais tardia** que o clique no CTA (mede quem preencheu); cai a contagem (isso é o objetivo); opção "Ativar eventos novos" mudaria o nome para AddToCart, **não clicar** sem aviso [E] | **Adotar já** como proxy de início efetivo e como evento de otimização futura |
| **(d) Página intermediária de oferta** (landing → CTA com preço → página nova com a oferta e o checkout, marcada "Página de conteúdo") | PageView da oferta + **ViewContent = chegou à oferta por clique** (cada visita à oferta é um clique qualificado); checkout só abre depois do clique | **Sim** (ViewContent pelo navegador; InitiateCheckout fica significativo) | Único caminho **100% por menu** que leva "viu a oferta" ao Meta; separa curioso de comprador; combina com a regra P0 (clique antes do checkout) | Uma página nova a manter; a UTM precisa **atravessar** o link entre páginas **[NC]** (no ClickMax o link de etapa do funil pode levar à próxima etapa e ignorar o `href` [E]; testar se a query é preservada); ViewContent no navegador sofre bloqueadores; muda o teste A/B (duas rotas); **só em páginas NOVAS** (nada sobre `/mini-mentoria` e afins) | **Recomendado como evolução** depois de (a) e (c) estarem provados |
| (e) Link de redirecionamento com ViewContent no CTA | Clique do CTA como ViewContent | Sim, mas com **significado errado** | Sem script | Passa por tela em branco; UTM/ids macros do anúncio precisam estar no destino; polui ViewContent; `{{ad.id}}` não é preenchido pelo ClickMax | **Não recomendado** |
| (f) Script (`cxs('track')` ou pixel manual) | Qualquer evento | Sim | Total controle | O importador remove `<script>`; só em "Configurações da Página › Scripts" com "aprovado"; risco de contagem em dobro | **Fora do escopo** sem aprovação; `snippets/persistir-utm.js` segue proposta |

### 3.3 Recomendação (ordem de execução, tudo por Bruno/ChatGPT no painel, com "aprovado")
1. **Agora (zero risco para as páginas):** (c) ligar "Só contar depois dos dados pessoais" no pixel; medir o **clique qualificado** por (a), lendo `button_click` por CTA no ClickMax. Visualização da oferta: marcar a **seção da oferta** com `data-cx-track="visible"` **na próxima versão da página nova** (não nas existentes) e ler `element_visible` [NC se o importador mantém o atributo].
2. **Em seguida, em página nova (rascunho, não ligada):** (d) com landing → oferta, "Página de conteúdo" só na oferta. Aí `ViewContent` = visualização da oferta no Meta.
3. **Deixar desligado:** `PixGenerated` e `AccessDelivered` (receptor), até haver motivo (campanha otimizada por Purchase e necessidade de medir abandono de Pix pela Meta).
4. **Nunca:** contar o carregamento do iframe como intenção; chamar Pix gerado de compra; marcar a página de checkout ou de obrigado como "Página de conteúdo".

## 4. Taxas e indicadores do funil (como ler)
`oferta/visita` · `clique CTA/visita` · `checkout efetivo/clique CTA` · `aprovado/checkout efetivo` · `entregue/aprovado` · custo por visita, por clique qualificado, por checkout efetivo, CPA, receita líquida (R$ 44,51 por Pix de R$ 47 antes de impostos e custos variáveis) e reembolsos. Uma etapa maior que a anterior não é "boa notícia": é erro de medição (a conciliação lista o motivo). Planilha e script: `conciliacao/` (`--funil`).

## 5. Estado atual em uma linha por etapa
1 PageView **[E] ok** · 2 oferta **desligado** · 3 clique CTA **medível no ClickMax, não no Meta** · 4 InitiateCheckout **errado (iframe)** · 5 Pix gerado **só interno** · 6 Purchase **só pago, mas 0 chegou ao Meta nas vendas reais** · 7 entrega **funciona, sem evento**.

## 6. O que depende de aprovação
| Ação | Quem e onde | Reversão |
|---|---|---|
| Ligar "Só contar depois dos dados pessoais" | Bruno, ClickMax › pixel › Editar › Abriu o checkout | Desligar o interruptor |
| Token CAPI, Comprou com Pix e cartão | Bruno, ClickMax › pixel › Editar | Remover token / desmarcar |
| "Página de conteúdo" na página de oferta nova | Bruno, ClickMax › página › Scripts | Desligar a chave (vale na hora) |
| Página de oferta nova (rascunho) | Agente de páginas, **só página nova** | Não publicar |
| Implantar `capi-webhook` e ligar `SEND_PIX_GENERATED` / `SEND_ACCESS_DELIVERED` | Bruno + hospedagem, após compra de teste | Variáveis `false`; desligar o webhook |
| Qualquer script na página | Bruno, "aprovado" explícito | Remover o script |


## 7. Funil de 8 eventos (v2, 25/11/2026): Lead e Reembolso entram

Dois caminhos usam a mesma Mini Mentoria R$ 47: **quente** (anúncio de captação → formulário → CRM → educação → remarketing → landing → checkout) e **frio** (anúncio de venda direta → landing → checkout). Os 8 eventos valem nos dois; o que muda é o **ponto de entrada** (Lead só existe no quente) e a **atribuição** (`PADRAO_UTM.md` §9; `conciliacao/lead_comprador.py`).
Legenda: **[E]** evidência (leitura nesta sessão ou documentação lida) · **[H]** hipótese · **[NC]** não confirmado.

| # | Evento | Sistema (onde nasce) | Nome | Parâmetros | Deduplicação | Estado atual | Quem executa |
|---|---|---|---|---|---|---|---|
| 1 | **Lead** (envio do formulário de captação) | Formulário nativo do Meta (anúncio de cadastro) → ClickMax (contato). O Meta conta o Lead **na origem**; o ClickMax grava o contato e, no formulário próprio do ClickMax, existe o campo `pixelLeadEvent` [E, `forms_list`] | `Lead` (padrão Meta) | Origem do lead = `utm_source=facebook`, `utm_medium=lead_ads`, `utm_campaign` (nome da campanha), `utm_content` (nome do anúncio/criativo), data de entrada (coorte) [E, leitura de contato recente] | Um Lead por envio; o contato do ClickMax é único por e-mail. **Não** enviar Lead também por CAPI para o mesmo envio (duplicaria) [H] | **Funciona** na origem: os contatos recentes chegam com origem, campanha e criativo [E]. Lacunas: sem `sck`/`src`, sem ids numéricos de campanha/anúncio, sem etiqueta de coorte (ver `ARQUITETURA_DE_PUBLICOS.md` §2) | Meta/ChatGPT (anúncio) e Bruno (etiquetas, "aprovado"); medição: `lead_comprador.py` |
| 2 | **Visita** | Pixel no navegador (ClickMax insere na página publicada) | `PageView` | UTMs da URL; `fbc/fbp` | Contagem simples (só navegador) [E] | **[E] funciona** em página publicada | Nada a fazer |
| 3 | **Visualização da oferta** | `element_visible` (ClickMax, seção da oferta marcada) ou `ViewContent` (página de oferta separada marcada "Página de conteúdo") | `element_visible` / `ViewContent` | `content_name`, `content_ids=["mm47"]`, `value 47.00`, `BRL` (ViewContent: [NC] se o nativo aceita) | `event_id` do navegador [NC] | **Desligado** (`pixelViewContent=false`) [E] | Agente de páginas (página NOVA) + Bruno (chave "Página de conteúdo") |
| 4 | **Clique no CTA com preço** | ClickMax, `button_click` com `elementId` do botão (SDK, sem script) | `button_click` (interno; custom `QualifiedCtaClick` só com script, **fora do escopo**) | `elementId` cta-0…cta-5; UTMs da sessão | Não se aplica | **Mecanismo existe** [E]; relatório por botão [NC]. Não chega ao Meta | Leitura por `visitors_*`/funil (DATA) |
| 5 | **Início efetivo de checkout** | Pixel do ClickMax (navegador e servidor) com "Só contar depois dos dados pessoais" | `InitiateCheckout` | `value`, `currency`; UTMs | Mesmo id navegador/servidor; Meta conta 1 [E] | **Errado hoje**: dispara ao **carregar o iframe**, a opção está desligada [E, auditoria H]. **Não use como indicador** até ligar a opção e provar (tutorial A4 e E3) | Bruno (painel ClickMax, "aprovado") |
| 6 | **Pix gerado** | ClickMax `pix_generated` (interno); Meta só pelo receptor opcional | `PixGenerated` (custom, **desligado**) | `value`, `BRL`, `order_id`, UTMs; `event_id=pix-<pedido>` | Id próprio, distinto do Purchase | Só interno [E]. Provado no teste local: **nunca vira Purchase** | Bruno + hospedagem, só se for preciso medir abandono de Pix |
| 7 | **Compra aprovada** | Pixel + CAPI do ClickMax (nativo) **ou** `capi-webhook` (alternativa, **no lugar** do nativo) | `Purchase` | `value` em **reais** (47.00), `BRL`, `order_id`, `content_name`, `content_ids`, UTMs, `event_id` = **id do pedido** | Navegador + servidor com o mesmo id (nativo); no receptor, idempotência por `event_id` (provado: reentrega = 1 envio) | **Só após pago** [E doc]; porém o Meta registrou 0 compras das vendas reais de 24/11 (sem UTM e sem token CAPI legível) [E, auditoria]. Receptor pronto e provado em teste local | Bruno (token/Comprou Pix e cartão); implantar o receptor só se o nativo falhar |
| 8 | **Reembolso** | ClickMax (venda `refunded`; webhook de reembolso) → receptor registra | Registro interno; evento custom `ZionRefund` **opcional e desligado** (nunca `Purchase`, nunca negativo) | `order_id`, `value`, `BRL`; `event_id=refund-<pedido>` | Um registro por pedido (provado: 2ª notificação = `duplicate`) | O receptor registra sem enviar Purchase [provado em teste local]. No ClickMax a venda muda para `refunded` [E]. Na conciliação o comprador reembolsado é **marcado**, não apagado | DATA (conciliação); Bruno só decide ligar `SEND_REFUND_EVENT` |

### 7.1 Regras que não mudam
1. **Purchase só depois de aprovado** (`paid`/`approved`). Pix gerado, pendente, autorizado e `paid_pending` nunca. Provado em `VALIDACAO_EM_TESTE.md`.
2. **O `InitiateCheckout` atual NÃO é indicador confiável**: dispara no carregamento do iframe. Não calcule "custo por checkout" com ele nem otimize campanha por ele hoje.
3. **Lead não é Purchase e Reembolso não é Purchase negativo.** Reembolso reduz a receita líquida na conciliação (e no financeiro), não "apaga" a venda do Meta.
4. **Dedupe:** um evento, um `event_id`; o id do Purchase é o id do pedido; Pix e reembolso têm prefixo próprio.

### 7.2 Proxy recomendado do funil (enquanto o `InitiateCheckout` não for corrigido e provado)
| Etapa do funil | Proxy hoje | Onde ler |
|---|---|---|
| Interesse qualificado | **Cliques por botão do ClickMax** (`button_click` dos CTAs com preço, ids cta-0…cta-5) | ClickMax, visitantes/funil [E mecanismo; relatório por botão NC] |
| Início efetivo de checkout | **"Só contar depois dos dados pessoais"** ligado (A4): o `InitiateCheckout` passa a contar só quem informou nome e e-mail | Histórico de envio do pixel e Gerenciador de Eventos (após ligar) |
| Intenção forte | Pix gerado (venda `pending` Pix no ClickMax) | Vendas |
| Receita | Venda `paid` do ClickMax conciliada com o gateway | `conciliar.py` |
Até a opção estar ligada, **use cliques por botão como proxy de intenção** e rotule "proxy"; o custo por checkout efetivo só entra no painel depois do passo A4 e de uma compra de teste (E3).

### 7.3 Quem decide o quê
- **Executa sem aprovação:** leitura, conciliação, testes locais (feito).
- **Precisa de "aprovado" de Bruno:** ligar a opção de dados pessoais (A4), token CAPI, "Página de conteúdo", implantar o receptor, ligar `PixGenerated`/`ZionRefund`, etiquetas de coorte, criar públicos no Meta.
