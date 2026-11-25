# Plano executável de rastreamento · Fase 03 (P0)

Autor: DATA · 25/11/2026 · Substitui o "plano técnico" da auditoria H por correções, responsáveis, caminhos de menu, critérios de aceite e ordem de execução.
Legenda: **[E]** confirmado em documentação oficial lida nesta sessão (docs.clickmax.io, artigos citados) · **[A]** evidência da auditoria H (leitura de ferramentas) · **[H]** hipótese · **[NC]** não confirmado: o texto diz o que procurar e qual print mandar.
Limites desta sessão: o checkout real (`payments.clickmax.io`) e os painéis logados (ClickMax, Meta, Ticto) não são acessíveis ao ambiente. `developers.facebook.com` e os sites da Ticto estavam **bloqueados** na rede da sessão: o que for da Meta vem da auditoria H (que citou a documentação) ou está marcado [NC]; a Ticto não tem documentação oficial lida (só o que o ClickMax documenta sobre ela).
Governança: nada aqui foi aplicado. Alterar pixel, CAPI, webhook, UTM ou anúncio em produção exige "aprovado" de Bruno. Token nunca vai ao chat, ao Git ou a print.

Executores: **Bruno** (painel), **Claude** (texto, código, leitura, conferência), **ChatGPT** (segunda revisão do código e pesquisa da documentação da Ticto/Meta quando a rede da sessão bloqueia).
Tutorial passo a passo, com telas esquemáticas: `tutorial/index.html` (PDF: `tutorial/tutorial-rastreamento.pdf`). Os códigos A1…D9 abaixo apontam para ele.

## 0. Fluxo e onde cada coisa acontece
Anúncio (Meta, `url_tags`) → Página `…clickmax.space` (UTMs na URL) → Checkout embutido (iframe `payments.clickmax.io/custom/<pageId>/<hash>`, recebe **todos** os parâmetros da URL da página [A]) → Ticto (processa Pix/cartão por trás do checkout do ClickMax; `gatewayName: ticto` [A]) → ClickMax (venda `paid`, eventos `checkout.*`, entrega) → Meta (pixel no navegador + API de Conversões a partir do servidor do ClickMax).

Estado hoje [A]: Purchase atribuído = 0 nas campanhas; `ads.pixel.event` vazio no workspace; vendas reais recentes sem UTM, `sck`, `src` ou id de anúncio; só os anúncios LT47 têm o conjunto completo de parâmetros.

## 1. Quadro por requisito

### 1.1 Pixel e dataset
- **Correção:** confirmar que o pixel `903918118859018` está **Ativo**, é o mesmo dos conjuntos de anúncios, está marcado no **produto/oferta** (o checkout segue o pixel do produto/oferta, não o da página [E]) e sem "Código de teste" fora de testes [E]. No Meta, confirmar que o dataset exibido no Gerenciador de Eventos é o desse pixel [NC: o nome do menu de configurações do dataset muda; procure "Configurações" do conjunto de dados].
- **Quem:** Bruno lê e manda prints; Claude confere.
- **Menu:** ClickMax **Tráfego › Pixel e trackeamento** (no menu lateral, Tráfego fica em Marketing) → linha do pixel → **Ver detalhes** (lista as telas que usam o pixel: Produto, Oferta, Página…, e mostra "Credencial configurada/Sem credencial") [E]. Produto: abrir o produto → aba **Pixels** ("Pixels deste produto"); oferta: abrir o produto e depois a oferta ("Pixels desta oferta") [E]. Tutorial A1–A3, B1.
- **Aceite:** Ver detalhes lista o produto **e** a oferta de cada oferta vendida (R$ 47 Mini Mentoria, R$ 97, R$ 47 LT); "Credencial configurada"; campo Código de teste vazio; dataset do Meta = `903918118859018`.
- **Teste:** evento do checkout aparece no Gerenciador de Eventos (Testar eventos) ao abrir o checkout da página publicada (o preview do editor não rastreia [E]).

### 1.2 API de Conversões (CAPI)
- **Correção:** no cadastro do pixel ligar **Usar API de Conversão**, colar o **Token de acesso** (gerado no Meta pelo Bruno, direto no painel, nunca no chat), **Testar token** (envia evento de teste, não conta) [E]. Sem token, o evento sai só pelo navegador: "o caso mais comum de 'o Meta não recebeu minha venda no Pix'" [E].
- **Quem:** Bruno (gera o token no Meta, cola no ClickMax). Claude: confere depois pelo Histórico de envio e pela ficha do contato.
- **Menu:** ClickMax pixel → menu de ações → **Editar** → bloco **API de Conversões da Meta** (Token de acesso, **Testar token**, Código de teste) [E]. Se já existe token: aparece **Token guardado** com **Trocar token**/**Remover** [E]. Tutorial A2–A3.
- **Aceite:** "Testar token" sem "Token recusado"; Histórico de envio com linhas **Enviado**; ficha do contato de teste > aba **Eventos de pixel** com Servidor · enviado [E].
- **Teste:** tutorial D (compra de teste).

### 1.3 Webhooks
- **Correção:** hoje nenhum webhook de saída serve ao Meta e não é preciso, **se a CAPI nativa funcionar**. Só criar webhook se a opção A falhar (ver §4, opção C). O caminho documentado: webhook de **entrega** da oferta com payload personalizado (variáveis `{{id}}`, `{{transaction.amount}}`, `{{buyerEmail}}`, `{{utm.*}}`…, valores em centavos) ou integração de **saída** `SALE_MADE`/`REFUND_MADE` (autenticada pelo cabeçalho `cm-token`, sem HMAC; 3 tentativas; desativa após 15 falhas seguidas) [E].
- **Quem:** Bruno cria no painel; Claude entrega o código e o JSON do payload (`capi-webhook/README.md`).
- **Menu:** produto → oferta → entrega do tipo webhook → URL, método, **Adicionar autenticação personalizada?**, **Selecione os eventos para disparo**, **Personalizar payload deste evento**, **Enviar teste**, **Ver payload** [E]; ou **Integrações › Adicionar integração › Criar webhook de saída** [E]. Quais eventos a lista de entrega oferece (transação paga? reembolso?): [NC] print.
- **Aceite:** Enviar teste devolve `200`; Ver payload mostra o JSON e a resposta `{"status":...}` do receptor.
- **Ticto:** o ClickMax já recebe a Ticto por webhook (Ticto › **Tictools › Webhooks › + Adicionar**, versão 2.0, JSON) [E, para integração de entrada]; não é necessário apontar a Ticto para o nosso receptor.

### 1.4 Purchase somente após pagamento aprovado
- **Correção:** (a) pixel > evento **Comprou**: ligar **No navegador** e **Pelo servidor**, e em **Formas de pagamento** marcar **Pix e cartão** (venda paga por forma desmarcada não gera evento) [E]; (b) a CAPI do ClickMax envia Purchase "quando a compra é aprovada" e confirma Pix "horas depois, com o visitante longe do site" [E]; (c) o código dormente da página poderia disparar `Purchase` ao **gerar** o Pix [A/H]: provar no teste que gerar o Pix **não** cria Purchase.
- **Quem:** Bruno (liga/confere), Claude (confere nos prints).
- **Menu:** Editar o pixel → passo/seção **Eventos** → linha **Comprou** → interruptores **No navegador**/**Pelo servidor** e **Formas de pagamento** [E]. Tutorial A4, B2, D5–D7.
- **Aceite (R1, R8):** Pix gerado e NÃO pago: no Testar eventos aparece AddPaymentInfo e **nenhum Purchase**; Pix pago: exatamente **1** Purchase em até 5 min; o Histórico de envio mostra Purchase "Enviado" e nada de Purchase para o Pix gerado.
- **Teste:** tutorial D5 (Pix gerado) e D6 (Pix pago). Se aparecer Purchase no D5: defeito confirmado → opção C com o ClickMax em "só navegador desligado" (ver §4).

### 1.5 InitiateCheckout só após início efetivo de compra
- **Correção:** no evento **Abriu o checkout**, ligar **Só contar depois dos dados pessoais** (o evento espera nome e e-mail) [E]. Hoje o IC dispara ao carregar o iframe, então IC ≈ visualização da landing [A].
- **Atenção (decisão de Bruno):** a opção **Ativar eventos novos** muda o nome de `InitiateCheckout` para `AddToCart` e de `Lead` para `Schedule`/etc. Se campanhas otimizam pelo nome antigo, revisar antes [E]. Não clique em "Ativar eventos novos" sem avisar o time de anúncios.
- **Quem:** Bruno. **Menu:** Editar o pixel → evento **Abriu o checkout** → **Só contar depois dos dados pessoais** [E]. Tutorial A4.
- **Aceite:** abrir o checkout sem preencher nada não gera IC no Testar eventos; preencher nome e e-mail gera 1 IC. IC deixa de ser ≈ visualização da página nos relatórios.
- **Teste:** tutorial D3–D4.

### 1.6 Deduplicação
- **Correção:** pela doc do ClickMax, navegador e servidor mandam o **mesmo identificador de evento** e a Meta conta uma conversão [E]. Regra da Meta: mesmo `event_name` e mesmo `event_id`, janela de 48 h; `event_id` recomendado; número do pedido serve de `event_id` [A, citando developers.facebook.com]. Só duplica se houver **outra fonte**: tag no GTM, código de pixel colado à mão em Scripts, ou nosso receptor ligado junto com o Purchase nativo (ids diferentes) [E, §4 do README do receptor].
- **Quem:** Bruno confere; Claude lê.
- **Menu:** Meta Gerenciador de Eventos → dataset → **Visão geral** → evento Purchase (origem Navegador/Servidor) e a seção de **Deduplicação**; **Diagnóstico** [NC: nomes exatos dos cartões na versão atual]. Tutorial B3–B6.
- **Aceite (R4):** Purchase de teste aparece como Navegador + Servidor com o **mesmo `event_id`** e conta 1; nenhum alerta de duplicidade ou de `event_id` ausente em Diagnóstico.
- **Teste:** tutorial D6 (anotar `event_id` do navegador e do servidor).

### 1.7 UTMs (padrão definitivo; fonte única em `PADRAO_UTM.md`, que prevalece em caso de divergência)
- **Padrão de `url_tags` (todos os anúncios, nível do anúncio):**
```
utm_source=meta&utm_medium=paid&utm_campaign=mm47&utm_content=<id do criativo>&utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}&adset_id={{adset.id}}
```
  `mm47` = slug fixo da oferta R$ 47 (um por oferta; nunca muda entre criativos nem variantes), `<id do criativo>` = id do arquivo da arte (ex.: `mm47f3-c03-custo-escondido`). Variante de landing no teste A/B: sufixo `-varA`/`-varB` no `utm_content` (`PADRAO_UTM.md` §3). As macros `{{ad.id}}`, `{{campaign.id}}`, `{{adset.id}}` são preenchidas pelo Meta [A: LT47 já usa `{{ad.id}}`/`{{campaign.id}}`]. Sem `src` nos anúncios (o `src` fica livre para canal, abaixo).
- **Regras de URL:**
  - **Parâmetros ANTES do `#`**: `https://…/inscricao-47?utm_…#pagar`. Depois de `#` o navegador não os trata como query e a página não os repassa [H, teste D2]. Preferir tirar o `#pagar` dos destinos dos anúncios.
  - **Iframe/checkout:** a página repassa ao iframe todos os parâmetros da URL em que está e a URL completa [A]. Logo: (1) a UTM tem de estar na URL da **página de vendas** quando o comprador abre o checkout; (2) não colar UTM no link do iframe; (3) links internos entre páginas devem levar a mesma query; (4) o campo `src`/`sck` só é gravado se o parâmetro existia na URL no momento da abertura [E].
  - **Links de WhatsApp/Bela e mensagens** (`link.clickmax.io`, aberturas, recuperação): `?utm_source=whatsapp&utm_medium=bela&utm_campaign=<fluxo>&src=whatsapp_bela` (e `…&utm_content=<mensagem>`). Isso grava a **origem do canal** na venda. **Não** se atribui o anúncio original: ele só pode aparecer se o parâmetro vier no link, o que exige variável do lead na mensagem [NC: procure, no editor de mensagem, variável de UTM/origem do lead; mande print]. Sem isso, a venda fica "canal: WhatsApp (Bela)" e o anúncio de primeira visita só existe como **evidência secundária** na jornada do visitante (rotulada assim em relatório).
  - **Persistência (R6):** a venda guarda a URL do momento do checkout [E]. Proposta `snippets/persistir-utm.js` (primeiro toque por 30 dias no mesmo navegador, devolve só o que falta, não sobrescreve o canal): testado localmente (6 testes, Playwright), **não instalado**; depende de o campo de código personalizado da página aceitar o script (**Configurações da Página › Scripts** [E]) e de teste na página real [NC]. Não cruza aparelhos.
- **Quem:** Claude entrega o texto e o snippet; Bruno aprova e cola `url_tags` no Gerenciador de Anúncios (anúncio ativo ou nova revisão: só com "aprovado"); Bruno cola o snippet.
- **Menu Meta (url_tags):** Gerenciador de Anúncios → editar o **anúncio** → seção de rastreamento → **Parâmetros de URL** [NC: rótulo exato da versão atual; procure por "Parâmetros de URL"]. Tutorial B7.
- **Aceite (R5, R6):** compra de teste a partir do link de anúncio de teste grava na venda `utm_source/medium/campaign/content/term`, `sck` (e `ad_id`/`campaign_id`/`adset_id`, se o corpo do webhook/CSV os mostrar [NC]); compra por link de mensagem grava a origem do canal.
- **Teste:** tutorial D2 e D8.

### 1.8 IDs de campanha, conjunto e anúncio
- **Correção:** o padrão acima já os carrega (`utm_term`=ad id, `sck`=campaign id, `ad_id`, `campaign_id`, `adset_id`). Hoje só LT47 tem tudo, os de venda direta usam nome no `utm_content`, a campanha R$ 270 não tem `url_tags` [A]. O ClickMax guarda UTM, `src` e `sck` na venda; `ad_id`/`campaign_id`/`adset_id` [NC: se aparecem como campos próprios na venda ou só dentro da URL do checkout `linkCheckout`; conferir no CSV/JSON da venda de teste]. Se só vierem na URL, o receptor e a conciliação leem `utm_term` e `sck` como ids (só quando numéricos).
- **Quem:** Bruno (anúncios), Claude (conferência na venda de teste).
- **Aceite (R5):** venda de teste mostra ids; o Meta atribui o Purchase ao anúncio em 24 a 48 h [A].
- **Teste:** tutorial D8–D9.

### 1.9 Valor e moeda
- **Correção:** o ClickMax guarda centavos (`9700`) e a CAPI deve enviar **reais com `currency`** [A]. Risco: divisão dupla (o código dormente da página manda `value/100` no `postMessage`: 0,97) [A/H]. Nada a configurar no painel; **provar no teste**.
- **Quem:** Claude confere o print; Bruno tira o print.
- **Menu:** Meta → Testar eventos → clicar no evento Purchase → parâmetros (`value`, `currency`) [NC: o layout do painel de detalhes muda]. Tutorial B3, D6.
- **Aceite (R2):** Purchase de teste com `value` = valor da oferta (47,00 ou 97,00, **nunca** 0,47/0,97/4700/9700) e `currency` = BRL.
- **Código:** `capi-webhook` divide por 100 uma única vez, barra fora da faixa `MIN_VALUE`–`MAX_VALUE` e valor não inteiro em centavos (testes automáticos).

### 1.10 Conciliação
- **Correção:** rotina diária ClickMax × Ticto × Meta com tolerância ±10% (R7). Ferramenta pronta: `conciliacao/conciliar.py` + modelos. Enquanto R1–R6 não passarem, a diferença esperada é grande e **explicada**: sem Purchase no Meta, sem UTM, sem fbc.
- **Quem:** Claude roda com os CSVs que Bruno exporta (fora do repositório); Bruno exporta.
- **Menu:** ClickMax **Vendas** → filtros/exportação (colunas `src`, `sck` e UTMs entram no CSV [E]); Ticto: extrato de vendas com todos os status [NC: tutorial C1]; Meta: Gerenciador de Anúncios, relatório por dia/campanha, colunas Compras e Valor de conversão de compras.
- **Aceite (R7):** diferença de compras ≤ 10% por dia e por campanha (ou diferença explicada venda a venda); ClickMax × Ticto sem divergência de status/valor.

### 1.11 Reembolsos
- **Correção:** reembolso não pode gerar Purchase novo nem some compra do Meta (a Meta não tem "Purchase negativo": **[NC]**, conferir na documentação vigente). Registrar sempre (venda `refunded`/`refunding` no ClickMax; evento `REFUND_MADE`); no código, reembolso é registrado e, **se ligado**, vira o evento próprio `ZionRefund`, nunca `Purchase`. Na conciliação, reembolsada conta como paga (foi paga) e é listada à parte.
- **Quem:** Bruno reembolsa a compra de teste (ClickMax/Ticto, 7 dias, CDC); Claude confere que não houve novo Purchase.
- **Aceite (R8, parte final):** após o reembolso de teste, o Histórico de envio e o Testar eventos não mostram Purchase novo; a venda aparece `refunded`.
- **Teste:** tutorial D9. **Nunca remover acessos de compradores reais**; no teste, Bruno decide sobre o acesso do contato de teste.

### 1.12 Entrega dos acessos
- **Correção:** verificar o caminho completo, do pagamento confirmado até o acesso (regra do projeto: uma tag isolada não comprova entrega). Entrega da Mini Mentoria: turma `087479a3…` do portal `3ef7a340…` [A].
- **Quem:** Bruno faz a compra de teste e abre o e-mail; Claude confere por leitura (membro da turma, link de acesso enviado).
- **Aceite:** em até alguns minutos após o Pix pago, o contato de teste vira membro da turma, recebe o link de acesso e consegue abrir a aula; ao reembolsar, Bruno decide se remove (somente o contato de teste).
- **Teste:** tutorial D7 e D10.

## 2. Opção C em uma tela: quando e como
Só se o roteiro D mostrar que o Purchase pago **não** chega por Servidor, ou que gerar Pix cria Purchase. Código pronto e testado (25 testes automáticos) em `capi-webhook/`. Ao ligar: **desligar o Purchase nativo** do ClickMax (navegador e servidor), porque o `event_id` do navegador do ClickMax não é o id da transação e o Meta contaria duas compras. Reverter: religar os interruptores. Passo a passo e checklist de segurança: `capi-webhook/README.md`.

## 3. Recuperação das compras reais sem UTM
Ver `recuperacao/RECUPERACAO_COMPRAS_SEM_UTM.md` (passo 0: confirmar se o Meta realmente não tem; envio de teste antes do real; prazo = hora do pagamento de cada compra + 7 dias, com 1 dia de margem; sem atribuir a anúncio sem dado). Roda o `reenviar_compras.py` em dry-run por padrão.

## 4. Ordem de execução
| Dia | Fase | O que | Quem | Altera produção? |
|---|---|---|---|---|
| Hoje e amanhã | 0 · Leitura | Tutorial A1–A5, B1–B3, C1–C3: prints (estado do pixel, histórico de envio, eventos desde a primeira compra real, extrato Ticto) + passo 0 da recuperação | Bruno → Claude | Não |
| até pagamento + 7 dias (1 dia de margem) | 0b · Recuperação | Se o Meta não tem Purchase dessas compras: dry-run → teste → real (aprovado) | Bruno | Sim, só Purchase dessas compras |
| Em seguida | 1 · Opção A | Token/CAPI, Comprou com Pix e cartão, IC após dados pessoais, pixel no produto/oferta, código de teste vazio | Bruno | **Sim (aprovado)** |
| Em seguida | 1b · UTM | `url_tags` padrão nos anúncios, links de WhatsApp com UTM de canal, `#pagar` | Bruno + Claude | **Sim (aprovado)** |
| Depois da fase 1 | 2 · Compra de teste | Roteiro D (Pix e cartão, reembolso) com critérios R1–R8 | Bruno → Claude | Compra real reembolsável |
| Se a fase 2 falhar | 3 · Opção C | Implantar receptor, desligar Purchase nativo, repetir o roteiro | Bruno + Claude + ChatGPT (revisão) | **Sim (aprovado)** |
| Depois | 4 · Operação | Conciliação diária; trocar otimização para Purchase só com "aprovado" (teto de gasto segue como definido) | Claude / Bruno | Sim para a troca |

Critério para considerar o rastreamento pronto: R1–R8 aprovados no teste (tutorial D), sem alerta em Diagnóstico, e conciliação ≤ 10% ou explicada.

## 5. Critérios R1–R8 (resumo)
R1 Purchase só após pago · R2 value/currency corretos · R3 CAPI funcionando · R4 deduplicação · R5 campanha/conjunto/anúncio na venda · R6 UTM persistente · R7 conciliação ≤ 10% · R8 Pix gerado ≠ pago (e reembolso sem novo Purchase). Tabela completa com como provar: tutorial D, seção "Critérios".

## 6. O que ficou [NC] e quem resolve
| Item | Como resolver |
|---|---|
| Nomes de campos de `clickmax-out` e `ticto` no corpo | Botão "Enviar teste" do ClickMax / webhook de teste da Ticto; ajustar `FIELD_MAP_JSON` (Claude) |
| Eventos disponíveis na lista de entrega webhook da oferta | Print da lista (Bruno) |
| Menus do Meta (Diagnóstico, Deduplicação, EMQ, configurações do dataset, Parâmetros de URL) | Tutorial B diz o que procurar; Bruno envia print do que encontrar; ChatGPT pode conferir a documentação da Meta (rede da sessão bloqueia) |
| Documentação oficial da Ticto (webhook, pixel, UTM) | ChatGPT/Bruno junto ao suporte da Ticto; extrato (tutorial C) |
| Versão vigente da Graph API para o receptor | Conferir na documentação da Meta antes de ligar (`META_GRAPH_VERSION`) |
| Ad/Campaign/Adset ids como campo da venda | Venda de teste com `url_tags` novas; CSV de vendas |
| Snippet de persistência na página real | Teste em página de teste antes de qualquer página no ar |
