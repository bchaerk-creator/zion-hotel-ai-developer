# Landing única, checkout e rastreamento · venda direta R$ 47

24/11/2026 (noite). Sem dados pessoais. Nada de outros produtos, páginas, ofertas ou preços foi alterado. Nenhum anúncio ligado, nenhuma campanha Meta tocada.

## 1. Inventário (reaproveitado)
| Item | Id / endereço | Situação conferida hoje |
|---|---|---|
| Oferta R$ 47 | `668391e7-f4a8-4bd3-a212-deba406f8a7a` · checkout `z3a0AEkvRl` | `approved`; `originalPrice` 4700; pagamento único, Pix e cartão 1x, boleto desligado, sem recorrência; `ZIONACADEMY`; suporte +55 48 6137-1061; reembolso 7 dias; gateway `ticto`; `incompleteReason` vazio. É a oferta certa (produto "Zion Collection Club \| Acesso à plataforma"; a Zion Collection 06 é outro produto). |
| Entrega | portal `3ef7a340…` turma `087479a3…` + portal antigo `a8e2157a…` turma `69345987…` | Turma `087479a3…`: 1 conteúdo, 9 módulos, 70 aulas, acesso de 12 meses configurado. Portal antigo: Bruno remove no painel. |
| Vendedor | `sellers_status` | `canSell` true, banco `approved`, vendedor ainda `pending`. |
| Páginas R$ 47 | `/inscricao-47` `fb1e89b9…` (91 views em 7 dias), `/inscricao-dossie` `828beb3b…` (0 views) | Mantidas como estão. |
| Obrigado | `/obrigado-plataforma` `d7166fc3…` | 1 view. O checkout da oferta ainda não redireciona para ela (pendência de Bruno). |
| Vídeo | `docs/zion-collection/club/video/plataforma-v02.mp4` (8:36) + `poster.jpg` | Público (HTTP 200) em `https://bchaerk-creator.github.io/zion-hotel-ai-developer/zion-collection/club/video/`. Usado na página. |
| Capturas reais | `docs/zion-collection/club/telas/*.jpg` (aula, mapa, previab, raiox, diagnostico, implantacao, agendar) | Usadas 4 delas, em molduras simples de celular. |
| Fotos reais sem pessoas | `club/fotos/bolha-aerea.jpg`, `bolha-interior.jpg` | Usadas. |
| Fluxo `fcc14b4d`, tags, formulário pós-compra | ver `../OFERTA.md` | Não mexidos (fluxo continua desligado). |

**Descrição "Acesso por 12 meses":** não está errada. A turma `087479a3…` tem `accessDuration` 12 meses. Não alterei a oferta. A página afirma 12 meses.

## 2. Criado
- Página nova **/parceiro-zion**, id `066b2cb9-62fe-4815-8410-3895ac5d29a1` (clone de `/inscricao-dossie`, reimportada com o `offerId` correto), **publicada** em 24/11 21:2x UTC.
  - URL: https://infoprodutos-zion.clickmax.space/parceiro-zion
  - Checkout: embutido na própria página (`<div data-cx-checkout>`), iframe `payments.clickmax.io/custom/066b2cb9…/z3a0AEkvRl`, oferta R$ 47. Os 2 botões levam a `#pagar`.
  - Seções: hero, problem, solution (x2), offer (vídeo, 4 capturas reais, lista só do que existe: 9 módulos e 70 aulas, fichas e ferramentas, planilhas de orçamento e viabilidade, Dossiê, banco de áreas), social-proof (Zion Bubble Glamping Urubici e Florianópolis, fotos reais com legenda), cta (preço, 12 meses, Pix/cartão, suporte, reembolso 7 dias, aviso "o valor corresponde ao acesso ao produto digital, não garante parceria ou investimento"), faq.
  - Sem depoimentos, números de mercado, urgência, preço "de", reunião ou WhatsApp como etapa.
- Fonte: `build.py` (reaproveita o CSS de `../landing/build.py`) → `index.html`.
- Observação: o topo leva foto de hospedagem (pedido expresso do prompt), o que difere da regra geral do CLAUDE.md para páginas de ferramentas.

## 3. Testes (Playwright)
Feitos:
- HTML local, 390×844 e 1366×800: sem overflow da página, 0 imagens quebradas, 0 `<span>`, 8 seções marcadas, 2 CTAs `#pagar`, 1 checkout, sem erro de página. Revisão visual de topo e meio no celular.
- Página no ar: título/H1 corretos; CTAs `QUERO COMEÇAR MEU PROJETO` e `QUERO ME INSCREVER AGORA` → `#pagar`; o iframe do checkout aponta para o hash `z3a0AEkvRl` (R$ 47). Mesmo comportamento da `/inscricao-47`, que vende. "R$ 47" no texto, sem "270" nem "R$ 97".
- Com `?utm_source=meta&utm_medium=paid&utm_campaign=lt47&utm_content=...&ad_id=...&campaign_id=...` na página: o iframe do checkout recebe todos os parâmetros.
- Scripts: `teste_local.js`, `teste_ao_vivo.js`, `teste_utm.js`, `teste_overflow.js`.

Não feitos / com ressalva:
- O domínio `payments.clickmax.io` é bloqueado neste ambiente (`ERR_TUNNEL_CONNECTION_FAILED`): **não vi o formulário de pagamento renderizado nem o "R$ 47" dentro dele**. A garantia é indireta (hash e oferta corretos; mesma oferta da página que já vendeu). A página foi publicada antes dessa conferência visual, porque o iframe só existe publicada. Bruno confere no celular.
- Pagamento Pix/cartão não testado. Ciclo pagamento → acesso comprovado com as compras reais de R$ 97 (24/11): acesso criado na turma em cerca de 1 a 2 minutos. Na oferta R$ 47 existe 1 venda paga hoje (Pix, do próprio Bruno, que já tinha acesso desde antes), então o ciclo desta oferta específica não está provado de forma independente; a oferta tem as duas entregas ligadas.
- 1ª carga da página no celular mediu uma vez `scrollWidth` 1280 (carga fria); 4 repetições seguintes deram 390. Reavaliar se Bruno notar rolagem lateral.
- Aviso do validador: CTAs com 2 rótulos (pedido expresso), cores fora da paleta do workspace e slots de imagem não marcados (usei fotos reais por URL pública).

## 4. Rastreamento
- `pages_tracking_status`: `/parceiro-zion` 0 views (nova); `/inscricao-47` 91; `/inscricao-dossie` 0; `/obrigado-plataforma` 1.
- **Pixel/CAPI:** `pixelViewContent` false; o HTML da página não carrega `fbevents.js` nem define `fbq`. Hoje **nenhum evento do Pixel dispara pelo navegador** e o MCP não mostra pixel/CAPI configurado (conferir em Eventos do Meta e nas configurações do projeto no painel).
- **Purchase:** o script do checkout nativo do ClickMax embutido na página chama `fbq('track','Purchase')` quando existir `fbq`, e o chama em `handlePixResponse` (Pix **gerado**, ainda pendente) e em `handleBoletoResponse`, não na confirmação. Se um pixel for instalado na página, o Purchase contaria Pix pendente. (Ressalva: li o código da página; o checkout em iframe tem código próprio que não consegui abrir.) O mapa de gatilhos separa `pix_generated` de `purchase_approved`, então a automação pode distinguir.
- **UTMs:** a página repassa os parâmetros ao iframe. A venda guarda `utmSource, utmMedium, utmCampaign, utmContent, utmTerm, src, sck` (`sales_get_utms`; filtros em `dashboard_my_sales`; valores antigos de `utm_content` e `utm_term` aparecem no autocomplete de pagamentos). `ad_id` e `campaign_id` não são campos da venda: chegam só no iframe e na URL da página. A venda de R$ 47 existente não tem UTM (compra de teste sem parâmetros), então a gravação da UTM na venda desta oferta **não foi provada com venda real**.
- **Padrão proposto** (url_tags em cada anúncio, tudo pausado até "aprovado"):
  `utm_source=meta&utm_medium=paid&utm_campaign=lt47&utm_content=<NOME>&utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}`
  `utm_term={{ad.id}}` e `sck={{campaign.id}}` existem para o id ficar gravado na venda; `ad_id`/`campaign_id` seguem o seu pedido, para a URL e o iframe.
  Nomes: `ZC2-LT47-01-PARCEIRO`, `ZC2-LT47-02-TERRENO`, `ZC2-LT47-03-SOCIO`, `ZC2-LT47-04-CAPITAL`, `ZC2-LT47-05-INVESTIDOR` (02 a 04 são sugestão; só 01 e 05 vieram no pedido).
- **Lacunas:** (1) sem pixel na página, o Meta não otimiza por compra; usar tráfego/engajamento e medir venda no ClickMax por `utm_content`/`utm_term`. (2) Se instalar pixel e CAPI juntos, o Purchase nativo não traz `eventID`: sem deduplicação; evitar Purchase pelo navegador e mandar compra aprovada (gatilho `purchase_approved`) por CAPI. (3) Webhook Asaas não entra neste caminho: a oferta usa gateway `ticto` do ClickMax. (4) Gravação de UTM na venda a provar na 1ª venda com anúncio.

## 5. CPA máximo (venda de R$ 47, Pix)
Taxas reais lidas em `transactions_get` e `wallet_statement` (vendas pagas, mesmo workspace):
| Venda | Taxa ClickMax | Líquido |
|---|---|---|
| R$ 47 Pix (esta oferta) | R$ 2,49 | **R$ 44,51** |
| R$ 19 Pix (ferramenta) | R$ 2,49 | R$ 16,51 |
| R$ 97 Pix (oferta anterior) | R$ 9,28 | R$ 87,72 |
| R$ 270 Pix | R$ 21,37 | R$ 248,63 |
A taxa não é proporcional: no R$ 47 foi fixa de R$ 2,49 (5,3%). **Não há venda aprovada no cartão no workspace**, então a taxa do cartão é desconhecida. Base é 1 venda de R$ 47: confirmar nas próximas.

Teto de CPA = líquido − imposto − reembolsos. Imposto como variável `i` (% sobre o faturamento de R$ 47; sem alíquota assumida):
- `CPA de equilíbrio = 44,51 − 47 × i`. Exemplos só para ilustrar: i = 0 → R$ 44,51; i = 6% → R$ 41,69; i = 10% → R$ 39,81.
- Para ter lucro, subtraia a margem desejada. Reembolso em 7 dias devolve o valor (a taxa de R$ 2,49 pode não voltar): descontar a taxa de reembolso real.
- Custo de mídia do Meta em dólar/impostos do cartão do anúncio não entram nessa conta.

## 6. O que falta / depende de Bruno
1. Conferir no celular o checkout em `/parceiro-zion` (R$ 47, Pix e cartão) e fazer 1 compra real.
2. Painel: redirecionar o checkout da oferta para `/obrigado-plataforma`; remover a entrega do portal antigo; decidir sobre as páginas `/inscricao-47` e `/inscricao-dossie` (mantidas).
3. Pixel/CAPI no Meta e no projeto (e decisão sobre o Purchase de Pix pendente).
4. "Aprovado" para anúncios (teto R$ 0, só pausados), fluxos de compra aprovada e de recuperação (desligados), e disparos.
5. Imagem do produto da oferta (só pelo painel).
6. Nota: a skill do ClickMax carregada tem revisão `c40fdd3dc26c`, diferente da publicada `f86020e0ba3e`; atualizar com `/plugin marketplace update clickmax-skills` (plugin) ou `npx skills update -g`.
