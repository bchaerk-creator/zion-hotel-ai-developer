# CRM da entrada por WhatsApp · origem, criativo, campanha e custo por conversa/venda

ZION FUNNEL + ZION TRAFFIC · 25/11/2026 · **PROPOSTA/ESTUDO. Só leitura** no ClickMax (documentação pública e inventário) e no Windsor; nada criado ou alterado. Repositório público: sem telefones, e-mails nem números reais.
Marcação: **[E]** evidência, **[H]** hipótese, **[NC]** não confirmado, **[APROVAÇÃO]**.
Fonte da documentação: páginas públicas do ClickMax lidas por `docs_search`/`docs_pages_get` ("O Clickmax sabe quando um contato chegou por um anúncio de WhatsApp?", "Como o Clickmax sabe quais leads e vendas vieram de cada anúncio?", "Como rastrear minhas vendas com o parâmetro src?"). `helpdesk_search` não devolveu artigo sobre o tema.

## 1. O que o ClickMax captura de uma conversa que nasce de anúncio click-to-WhatsApp [E, documentação]
- Quando a pessoa clica num anúncio do Meta com botão "Enviar mensagem" (WhatsApp) e **manda a primeira mensagem**, o Meta informa de qual anúncio ela veio, e o ClickMax **registra o clique no contato**. Automático a partir da conexão do canal: **não há o que ligar**, e **não precisa de página, link nem UTM**.
- Para cada clique ficam guardados no contato: **id do anúncio** (o do Gerenciador; em post impulsionado, o id do post), **título e link do anúncio** (quando o Meta envia), **horário do clique** (= da 1ª mensagem) e o **identificador do clique do WhatsApp** (`ctwa_clid`; o Instagram Direct não envia).
- Registro **por contato**, não por conversa: se voltar por outro anúncio, os dois cliques ficam guardados; mensagem duplicada do Meta não duplica o clique.
- Entra nos números do anúncio em **Tráfego → Desempenho** (leads, vendas, receita, CPL, CPA, ROAS do anúncio). Atribuição = **último anúncio clicado até 28 dias antes**, creditado no dia do clique; os últimos 90 dias ainda mudam com reembolso.
- Com o identificador do clique, as conversões do contato (conversa iniciada e eventos do CRM como oportunidade ganha) **podem voltar ao Meta** pela API de Conversões ligadas à conversa de origem [E documentação; ativação e configuração: **[NC]** no nosso workspace, pixel/CAPI ilegíveis por MCP].
- **Não registra:** anúncio em que o Meta não envia o id; links comuns `wa.me`/`ig.me`/QR (não vêm de anúncio); **conversa que chega em outro número** que não o conectado ao ClickMax (não passa pelo ClickMax).

## 2. A lacuna (o que NÃO vem sozinho)
1. **Sem UTM:** a conversa não tem `utm_source/medium/campaign/content`. O CRM sabe o **id do anúncio**; **nome do criativo, conjunto e campanha** vêm de outro lugar (Meta/Windsor: `ad_id` → `ad_name`, `adset_name`, `campaign`). É preciso uma **tabela de-para** `ad_id → vídeo 01/02`.
2. **Onde aparece no contato** (tela/campo, e se a API/MCP expõe: `leads_get`, `leads_xray`, `leads_origins`): **[NC]**, não testado porque não há conversa real ainda. Teste obrigatório antes de gastar (§6).
3. **Atribuição só inclui a janela de 28 dias e o último clique:** quem já teve outro anúncio antes é creditado ao último. Para "criativo que trouxe a conversa", usar o clique da 1ª mensagem.
4. **Quem compra por link enviado na conversa e depois abre o checkout em outro navegador/dispositivo** pode perder a ligação [H]: o ClickMax liga por contato, mas a venda grava os parâmetros **da URL do checkout** (aprendizado da auditoria: venda sem UTM mesmo com origem Meta).
5. **E-mail × telefone:** a conversa traz o **telefone**; a compra traz o **e-mail** (e telefone, se o checkout pedir [NC]). A ponte é o telefone normalizado ou o e-mail dado na conversa.
6. **Meta como fonte de contagem de "conversa iniciada":** o valor do Meta e o número de contatos criados no ClickMax **não serão iguais** (o Meta conta conversas por janela de 7 dias; o ClickMax conta contatos/cliques). Usar os dois, sem somar.
7. **O que acontece se a conversa chega no número errado:** se a Página do anúncio estiver ligada a um número que **não** é o conectado ao ClickMax, a conversa nunca entra no CRM (ver §4).

## 3. Como o lead vira contato com origem/criativo/campanha (3 camadas, uso combinado)
| Camada | Como funciona | Para quê | Status |
|---|---|---|---|
| **A. Clique do anúncio registrado pelo ClickMax** | automático (§1) | atribuição ao anúncio, CPL/CPA do ClickMax, devolução ao Meta | [E] doc; teste [NC] |
| **B. Mensagem pré-preenchida única por criativo** | frase diferente por vídeo (`VENDA_NO_WHATSAPP.md` §2); a 1ª mensagem recebida identifica o vídeo mesmo se o id do anúncio falhar | plano B de origem; regra de etiqueta por palavra | [H], simples |
| **C. Etiqueta por criativo** | `WA-ANUNCIO \| VIDEO 01/02` aplicada pelo atendente (manual na 1ª fase) ou por regra por palavra-chave/origem se existir [NC] | segmentar, medir coortes, excluir do público quente/frio | [APROVAÇÃO] criar |
Também: **parâmetro de referência no link do anúncio**: o botão de WhatsApp do anúncio **não** usa URL de site; UTM não se aplica. Se, em vez disso, algum anúncio usar **página-ponte → wa.me**, aí valem UTM e `src/sck` (§5), mas **perde-se o `ctwa_clid`** (link comum não é registrado como clique de anúncio). **Decisão recomendada: anúncio nativo "Enviar mensagem" (sem página-ponte).**
**Tabela de-para (a manter fora do Git se tiver ids de campanha)**: `ad_id` do Meta → `video01`/`video02`/conjunto/campanha, lida do Windsor (`ad_id`, `ad_name`, `adset_name`, `campaign`, `adset_destination_type`).

## 4. Pré-condição: número de WhatsApp conectado ao Meta [leitura realizada]
- **ClickMax:** `channel_instances_list`: número "Zion Collection" (WhatsApp API oficial/Gupshup) **conectado**, qualidade verde, limite 2.000 conversas/dia (TIER_2K); número "Pablito Ads" conectado (qualidade desconhecida). Canal Instagram em `pending`. [E]
- **Meta (Windsor facebook, conta Zion Collection 2):** `get_fields` expõe `adset_destination_type`, `adset_promoted_object`, `actions_onsite_conversion_messaging_conversation_started_7d`, `cost_per_action_type_onsite_conversion_messaging_conversation_started_7d`, `actions_onsite_conversion_messaging_first_reply`, `actions_onsite_conversion_total_messaging_connection`. [E]
- Leitura dos conjuntos (últimos 30 dias, só leitura): **existem conjuntos antigos com destino WhatsApp** (otimização "conversas", Página da Zion Collection): um "WhatsApp Direto - Teste" (sem número no objeto promovido) e outro, antigo, com **um número de WhatsApp no objeto promovido que não é o número "Zion Collection" conectado ao ClickMax** (não reproduzo o número). [E]
- **Conclusão:** há **evidência de que a Página já anunciou para WhatsApp**, mas **não consigo provar, por leitura, qual número está ligado à Página hoje nem se é o número do ClickMax**. **[NC]** (a vinculação Página ↔ número fica no painel Meta/WhatsApp Manager; Windsor só lê). **Bloqueio de ativação:** conferir no painel que o botão de WhatsApp do anúncio abre **o número "Zion Collection" conectado ao ClickMax**; se for o número antigo, as conversas **não entram no CRM** nem recebem atribuição.
- O conjunto antigo com número diferente indica risco real de **mandar conversa para o número errado** se alguém duplicar esse conjunto.

## 5. Link na conversa (UTM e src para a venda)
O link da landing v2/checkout enviado dentro da conversa deve levar parâmetros para não repetir o erro de vendas sem UTM:
`https://infoprodutos-zion.clickmax.space/{landing}?utm_source=whatsapp&utm_medium=conversa&utm_campaign=mm47-wa&utm_content=video01|video02&src=wa_video01|wa_video02` [padrão a alinhar com `../09-tracking/PADRAO_UTM.md`; `src`/`sck` conforme guia do ClickMax].
O atendente escolhe o link do vídeo certo (um link por criativo, **sem** dados da pessoa na URL). Redirecionamento curto do ClickMax (`redirect_links`) [NC] pode encurtar; criar = [APROVAÇÃO].
Persistência: a UTM só chega à venda se a URL do checkout a mantiver (ver `../09-tracking/`); testar com compra de teste interna antes de ativar.

## 6. Teste obrigatório antes de qualquer gasto (sem dinheiro de anúncio)
1. Bruno (ou membro da equipe) manda mensagem ao número "Zion Collection" de um celular de teste **por um link `wa.me`** → confirmar que o contato aparece no ClickMax (e que **não** gera atribuição de anúncio, conforme doc).
2. Com a campanha C1 **ativada com orçamento mínimo e aprovado** (ou uma pré-visualização de anúncio com "enviar mensagem" no próprio dispositivo [NC se permite]), clicar e mandar a 1ª mensagem → ver: contato criado? clique de anúncio registrado (id do anúncio, título, horário, `ctwa_clid`)? aparece em Tráfego → Desempenho? onde e com qual nome? (`leads_get`/`leads_xray`/MCP).
3. Confirmar se **Bela/Zaya/fluxos** disparam algo para esse contato (conflito, `../10-trafego/ESTRUTURA_NOVA_COLLECTION.md` §7).
4. Confirmar o que o checkout/compra de teste grava (UTM/`src`, telefone, e-mail) → `sales_get_utms`.
Registro do teste: no LOG, sem dados pessoais.

## 7. Como medir (custo por conversa → qualificada → venda)
Definições (todas por **coorte de dia de entrada**; sem números reais no Git):
| Métrica | Numerador/fonte | Denominador |
|---|---|---|
| **Custo por conversa iniciada (Meta)** | gasto do conjunto C1 (Windsor `spend`) ÷ `actions_onsite_conversion_messaging_conversation_started_7d` | n/a |
| **Custo por contato criado com clique de anúncio (ClickMax)** | gasto ÷ contatos com clique registrado (Tráfego → Desempenho "Leads" do anúncio) | n/a |
| **Custo por conversa qualificada** | gasto ÷ contatos com etiqueta `WA \| QUALIFICADO` (ou critério §4 do processo) | n/a |
| **Custo por venda (CPA do caminho WhatsApp)** | gasto C1 ÷ compradores únicos **conciliados** com contato WA (pagamento aprovado) | n/a |
| Taxas | conversa→qualificada, qualificada→oferta enviada, oferta→compra, conversa→compra D+1/D+7/D+14 | por criativo (vídeo 01 × 02) |
| Tempo até a compra | data da 1ª mensagem → pagamento aprovado | mediana |
"CPL" no WhatsApp **deixa de existir como no formulário**: o equivalente é **custo por conversa iniciada** (e, melhor, **por conversa qualificada**). Não comparar CPL de formulário com custo por conversa (naturezas diferentes; conversa custa menos, mas converte diferente).
Painel: o dashboard (`../12-dashboard/`) precisa de uma seção "WhatsApp" [NC: não alterei]; até lá, planilha do modelo v3 com as colunas acima (fora do Git se houver dado real).

## 8. Como cruzar com compras
- **Chave primária: telefone normalizado** (só dígitos, DDI 55 + DDD + número, tratando o 9º dígito) **e e-mail normalizado** (minúsculas, sem espaços). A comparação nunca presume correspondência quando houver divergência (regra do funil híbrido).
- Fontes: contatos WA (`leads_search`/`leads_get`, etiqueta de origem) × vendas aprovadas (`buyers_purchases_list`, `sales_get_buyer`, `leads_payments`, `sales_get_utms`).
- Reaproveitar `../09-tracking/conciliacao/lead_comprador.py` (testada, 14 testes), acrescentando a chave telefone [mudança a fazer: não alterei o script]. Compra sem origem fica **"não atribuída"**; compra que combina por telefone e e-mail = **conciliada**; combina só por um = **provável** (marcada, não conta como atribuída).
- **Compradores existentes** (R$ 97 já vendidos e demais) **excluídos** do público de venda e do atendimento comercial de venda.
- Sem duplicidade com os caminhos de carrossel: um comprador conta uma vez; se veio por WA e por carrossel, regra: **último clique** do ClickMax (28 dias) e anotar o conflito.
- Devolver ao Meta (compra e qualificada) por `ctwa_clid`/CAPI: possível pelo ClickMax [E doc]; **ativar = [APROVAÇÃO]** e só depois de provar o evento de compra aprovada (`../09-tracking/`).

## 9. LGPD
O lead que **inicia a conversa** fornece telefone e mensagem por iniciativa própria; não coletar mais do que necessário; **consentimento separado** para comunicação comercial futura e para personalização de anúncio, sem condicionar a conversa (`../10-trafego/LGPD_BASE_LEGAL_E_PUBLICOS.md`). O pedido de parar vira etiqueta `WA | PARAR COMUNICACAO` e exclusão de envios. Validação jurídica: [NC].

## 10. Resumo executivo
- **Captura:** o ClickMax registra o clique do anúncio de WhatsApp (id do anúncio, título, horário, `ctwa_clid`) **sem UTM**; atribui ao anúncio no Tráfego.
- **Lacuna:** nome do criativo/campanha (de-para por `ad_id`), UTM (inexistente), onde ver o dado no contato [NC], número conectado × número da Página [NC], ponte telefone × e-mail.
- **Medir:** custo por conversa iniciada → qualificada → venda, por vídeo e por coorte.
- **Antes de gastar:** teste de §6 e conferência do número.
