# Diagnóstico · captação dos formulários nativos do Meta e recuperação do R$ 47 (27/11/2026)

Somente leitura. Nada foi criado, ativado, enviado ou alterado. Nenhum token ou link secreto foi exposto.

## 1. Como os leads dos formulários nativos entravam no CRM
- **Meta → Windsor → script da rotina horária → link de captura do ClickMax.** O Windsor (`facebook_leads`, página `576944608845537`) traz o lead; a rotina (`trig_01Uydzp4XuTKYuk8TPvxTWFM`, hoje PAUSADA) fazia um POST JSON no link de captura e depois aplicava tags e criava o cartão.
- **Link de captura:** é do tipo `https://api.clickmax.io/ingest/<ID>` (ClickMax › integrações › link de captação). O `<ID>` é um segredo: **não está no repositório nem no histórico desta sessão**. Existe como segredo `CLICKMAX_CAPTURE_LINK_URL` no projeto Lovable do site, que o usa no webhook do Asaas (`src/lib/clickmaxCaptura.server.ts`); o código só aceita `api.clickmax.io`/`api.clickmax.dev` com caminho `/ingest/<id>`. O script `ingest_E.py` e o `campos_inscricao.json` se perderam (estavam só no scratchpad).
- **Duplicados:** o link de captura cria ou atualiza o lead pelo mesmo e-mail ou telefone. `customFields` só são gravados na **criação**; em lead que já existe as respostas novas NÃO sobrescrevem. A rotina ainda checava `leads_check_duplicates` antes e guardava `meta_id` → `leadId` em `producao/clube/sync-meta-form/processados.json` (sem dados pessoais).
- **Campos aceitos pelo link:** `email, name, telephone, document, profession, city, state, instagram, birthday, address{}, customFields{nome|rótulo|id}, utmSource, utmMedium, utmCampaign, utmContent, utmTerm`.

## 2. O que já existe no ClickMax
| Item | Situação |
|---|---|
| Projeto | Infoprodutos Zion `8d1152a4…` (ofertas, ZC47). Projeto antigo `e1c7dc7a…` tem o fluxo "Entrada de Lead — Meta → CRM → Funil" (ativo; só o gatilho `crm.lead.captured.v1`, sem passos) |
| Pipeline de destino | Funil Zion `40529cf1…`, etapa "Leads de hoje" `50d19a87…`. Fluxo ativo "TAG AUTOMÁTICA · PREENCHEU FORMULÁRIO (META)" dispara ao entrar em coluna |
| Tags do Meta | `FORMS FACEBOOK NATIVO` `347d07c6…` (194), `META | FORM LAND BANK` `67e5114b…` (106), `META | FORM R$47 DIRETO` `820bf2d3…` (2), `META | FORM ZC47 TERRENO` `51399bf5…` (0), `META | FORM ZC47 POUSADA` `ecfa139f…` (0), `META | FORM CLUBE`, `META | FORM PARCEIRO` (0) |
| **Cuidado** | `INSCRIÇÃO 270 | LEAD DO FORMULÁRIO` `d3053721…` dispara o fluxo ATIVO "Inscrição 270 · Abertura" (modelo da Bela). **Não aplicar nos leads novos.** Os lembretes dia 2 e dia 5 estão fechados |
| Listas | Sem lista dedicada à captação atual. Listas antigas: "Trailer Trilha · leads do form Meta (Land Bank)" (77), "Dor · … (form Meta)" |
| Origem no CRM | Origens existentes: CxForms, CxPages, CxExternalPages, CxFlows, CxClub… |
| Mapeamento das respostas | Perdido com o script. O ClickMax tem o grupo de campos "Forms Meta" e campos `zc_*` (questionário). As perguntas dos dois formulários novos (`1627911948376725` terreno, `1127602653227754` pousada) **não puderam ser lidas daqui**: o Windsor devolveu 0 linhas nos últimos 3 dias para esses form_id (sem leads ainda, ou filtro sem dados) |
| Origem da campanha e do criativo | Windsor `facebook_leads` devolve `campaign_id, adset_name, ad_name, form_id, form_name`; **não devolve `ad_id`**. Convenção anterior: `utmSource=meta`, `utmMedium=paid`, `utmCampaign=<campanha>`, `utmContent=<ad_name>`, `utmTerm=<form_name>` |

## 3. Asaas e o evento Purchase (dataset 903918118859018)
- A oferta de R$ 47 e a de R$ 97 usam o gateway **Ticto do ClickMax**; o Asaas **não** participa delas. O webhook Asaas do site (`/api/public/asaas-webhook`) só cuida de Land Bank (R$ 270), Método, Dossiê e consultoria, com `PAYMENT_CONFIRMED`/`PAYMENT_RECEIVED`.
- **Dá para alimentar o Purchase pelo Asaas, com ressalvas:** (a) o site hoje não chama a API de Conversões (nenhum `graph.facebook.com`); (b) o webhook já deduplica por `payment.id` (claim), então o `event_id` pode ser `asaas_<payment.id>`; (c) `value` já vem em reais (número), moeda BRL; (d) o e-mail e o telefone vêm do cliente Asaas (dá para enviar com hash); (e) **sem `fbc`/`fbp`**, a atribuição ao anúncio fica fraca, a menos que o clique seja guardado no lead (UTM e `fbclid`) e recuperado pelo e-mail; (f) precisa de token da API de Conversões como segredo do Lovable (Bruno cola, nunca no chat); (g) não disparar Purchase no navegador para esses produtos, para não duplicar.
- **Para R$ 47/R$ 97 o caminho certo é a API de Conversões nativa do ClickMax** (Etapa B do plano de rastreamento), com o pixel `903918118859018`. Não criar uma segunda via pelo Asaas para a mesma venda.

## 4. Recuperação da oferta de R$ 47 (PROPOSTA · nada criado nem ligado)
Estado atual: não existe recuperação do R$ 47. Existem: "Inscrição 270 · Recuperação de pagamento" (ATIVA, só para a oferta de R$ 270 `3a86e24c…`, 1 mensagem 30 min depois), e rascunhos do "Clube R$ 97" (modelos `zion_clube_carrinho`, `zion_clube_downsell_47`, `zion_clube_pix_pendente`, que citam a oferta antiga). Hoje o fluxo do R$ 47 só aplica a etiqueta `ZC | NÃO CONCLUIU A COMPRA`, sem mensagem.

Regras propostas: gatilhos `cart.abandonment.v1` e `pix.expired.v1` da oferta `668391e7…`; parar ao confirmar a compra; no máximo 1 sequência a cada 7 dias por contato; enviar só entre 8h e 21h (Brasília); respeitar "SAIR"; sem urgência falsa, sem promessa de resultado.

**Sequência A · abriu o checkout e não concluiu**
1. **+30 min** · modelo já aprovado `inscricao_nao_concluida`: "Olá, {{1}}! Aqui é a Bela, da equipe Zion. / Vimos que você começou a inscrição do seu terreno ou projeto na Zion Collection e não concluiu. Ficou alguma dúvida sobre a inscrição ou sobre o pagamento? / Se quiser, responda esta mensagem que eu te ajudo. Para retomar, é só usar o botão abaixo. / [Concluir inscrição] · Para não receber mais mensagens, responda SAIR."
2. **+24 h** · modelo novo `zc47_retomar_24h` (precisa aprovação da Meta): "Olá, {{1}}! Aqui é a Bela, da equipe Zion. / Passando para saber se você conseguiu concluir a sua inscrição na plataforma Zion Collection. O acesso é de R$ 47, pagamento único, no Pix ou no cartão, com reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor. / Se ficou alguma dúvida, responda esta mensagem. / [Concluir inscrição] · Para não receber mais mensagens, responda SAIR."
3. **+72 h** (última) · modelo novo `zc47_ultima`: "Olá, {{1}}! Esta é a nossa última mensagem sobre a sua inscrição. / Se ela ainda faz sentido para o seu terreno ou projeto, o botão abaixo leva direto ao pagamento. Se não, tudo bem, não vamos insistir. / [Concluir inscrição] · Para não receber mais mensagens, responda SAIR."

**Sequência B · gerou o Pix e não pagou (ou o Pix expirou)**
1. **+30 min** · modelo novo `zc47_pix_pendente` (aprovação da Meta): "Olá, {{1}}! Aqui é a Bela, da equipe Zion. / Você gerou o Pix da inscrição na plataforma Zion Collection (R$ 47) e ainda não vimos o pagamento. Se o código expirou ou deu algum problema, é só gerar outro pelo botão abaixo. Se travou em algum passo, responda aqui que eu ajudo. / [Gerar novo Pix] · Para não receber mais mensagens, responda SAIR."
2. **+24 h** · mesmo `zc47_retomar_24h`.
3. **+72 h** · mesmo `zc47_ultima`.

Botões: todos para `https://www.zionhotelgroup.com/inscricao`.

## 5. Pendências para implementar (só depois da aprovação do diagnóstico)
1. O link de captura NÃO deve ir pelo chat. Bruno guarda o link como segredo do ambiente (Configurações do ambiente › segredos) ou indica qual link do ClickMax usar; a rotina lê da variável.
2. Recriar o script de ingestão com: duplicado por e-mail/telefone, UTMs a partir do Windsor, tag `META | FORM ZC47 TERRENO`/`POUSADA` (nunca `d3053721…`), cartão em "Leads de hoje", `processados.json`.
3. Ler as perguntas dos dois formulários novos (Gerenciador de Anúncios › Formulários) para montar o mapeamento em campos personalizados.
4. Aprovação dos 3 modelos novos de WhatsApp na Meta e do texto acima.
