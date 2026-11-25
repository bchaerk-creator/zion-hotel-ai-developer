# Pacote de publicação · FASE 1 · venda fria da Mini Mentoria de Estruturação Zion (R$ 47)

ZION SALES DIRECTOR + CONVERSION + DATA + TRAFFIC · 25/11/2026 · **PROPOSTA para Bruno aprovar, passo a passo.** Nada aqui foi executado: nenhuma página publicada, nenhuma oferta, produto, turma, formulário ou campanha alterada ou criada (só leituras no ClickMax e GETs públicos). Repositório público: sem número real de gasto, venda, lead ou resultado; valores em R$ são **parâmetros e decisões**, não resultados.
Marcação: **[E]** evidência (lida ou executada nesta sessão, com data), **[H]** hipótese, **[NC]** não confirmado (diz como confirmar), **[BRUNO]** só Bruno decide ou executa.
Companheiro para o ChatGPT: [`HANDOFF_CHATGPT_FASE1.md`](HANDOFF_CHATGPT_FASE1.md). Aprovações: itens **M70 a M86** de `../13-relatorios/MATRIZ_ALTERACOES_APROVACAO.md` (seção "Fase 1").

## 0. Decisões de Bruno (25/11) que este pacote implementa
1. **Fase 1 = só VENDA FRIA**, teto **R$ 30/dia**. Sem captação, sem entrada por WhatsApp, sem venda quente nesta fase.
2. **Criativo:** Carrossel C de venda (10 cartões, `docs/ads/venda-carrossel-c/`) como principal, mais criativos de apoio de venda fria **baseados em campeões** (seção 5.4).
3. **Landing:** variante B v3 (rascunho `e0933e71-255e-4edc-bfec-92ba6a0121ac`, `/mini-mentoria-b-v3`). **Checkout limpo.**
4. **Compra de teste de Bruno** (Pix, com reembolso) **logo depois de publicar**, antes de qualquer gasto.
5. O `CLAUDE.md` será atualizado por Bruno: a nova redação da linha de teto está na seção 6 (não editei o arquivo).
6. **Sessão de Diagnóstico Estratégico:** só para **projetos qualificados, por solicitação** (Dossiê concluído, análise, agenda); **não** é bônus individual para todos. O anúncio não cita limite semanal (segue "sujeita à análise e à agenda"); o **limite semanal será definido depois da compra de teste**. Custo da sessão: `../08-financeiro/CUSTO_SESSAO_DIAGNOSTICO.md`.
7. **Campanha Purchase já criada pelo ChatGPT (`120250560823800016`): REAPROVEITAR, ajustar em vez de criar outra** (seção 5.2 e `HANDOFF_CHATGPT_FASE1.md`). Manifesto definitivo do Carrossel C: `docs/ads/venda-carrossel-c/manifesto.json` (10 cartões, URLs públicas, texto, UTM); este pacote o referencia e **não** o recria.

**Orçamento do teste (recalculado):** `T × D = R$ 30 × 14 = R$ 420` (parâmetros `T` e `D`; teto total = `T × D`). Substitui, para a Fase 1, o plano de R$ 60/dia e R$ 840 do funil híbrido (que fica como histórico). Aritmética sobre R$ 420 (líquido Pix R$ 44,51 [E]; CPA desejado preliminar R$ 31,16 [H]; limite de perda `k × CPA máx. = 3 × 44,51 = R$ 133,53`, `PROTOCOLO_VALIDACAO_14_DIAS.md` §6):
| Cálculo | Resultado |
|---|---|
| Compras para só empatar com a mídia (R$ 420 ÷ R$ 44,51) | 9,4, ou seja **10 compras** (antes de impostos e custos, que estão sem valor [NC]) |
| Compras para o CPA desejado (R$ 420 ÷ R$ 31,16) | 13,5, ou seja **14 compras** |
| Compras para `Nmin = 30` (protocolo) | exigiria CPA ≤ R$ 14: **inalcançável com R$ 420**; o veredito esperado é **descritivo/inconclusivo** (`PROTOCOLO_VALIDACAO_14_DIAS.md` §8) |
| Dia em que o limite de perda (R$ 133,53) é cruzado a R$ 30/dia | dia 5 (R$ 120 no fim do dia 4; R$ 150 no fim do dia 5) |
| Se as R$ 420 forem gastas e houver 10 compras | CPA ≤ R$ 42,00 (abaixo do líquido bruto); com 14 compras, CPA ≤ R$ 30,00 |
**Esses números NÃO incluem o custo da Sessão** (custo variável por comprador que solicitar e for aprovado; fórmula em `CUSTO_SESSAO_DIAGNOSTICO.md`: CPA máx. ajustado = R$ 44,51 − `s × a × custo por sessão` − demais custos). Com a política qualificada `s × a` é pequeno e controlável, mas não medido [NC]: o ponto de equilíbrio real é **maior** que 10 compras. Medir `s`, `a` e o tempo por sessão desde a primeira venda.

## 1. PRÉ-REQUISITOS: o que bloqueia o gasto e o que não bloqueia
Regra: **nenhum real é gasto antes de todos os itens "BLOQUEIA" estarem fechados e registrados no LOG** (checklist de ativação, seção 5.8).

### 1.1 BLOQUEIA o gasto
| # | Pré-requisito | Item da matriz | Estado em 25/11 |
|---|---|---|---|
| G1 | Teto e escopo por escrito e `CLAUDE.md` atualizado (seção 6) | M70 | pendente |
| G2 | **Correções do produto que contradizem a oferta nas primeiras telas do comprador.** O que corrigir e como está em `../15-correcoes-produto/` (outro agente prepara; **não duplico**; [NC: a pasta está em preparação, ainda sem README nem commit]). Lista mínima por impacto, vinda de `../13-relatorios/VISTORIA_ENTREGAVEIS.md` §5 e §10 (recomendação [H], Bruno decide): (a) vídeo de boas-vindas `fcf20da1…` com "Land Bank", "parcerias e investimentos" e "agenda com a equipe" (M43); (b) botão "Enviar ao Land Bank" e bloco "Banco de áreas" nas 8 fichas; (c) **envio de dados ao baixar o PDF**, que contradiz o texto "Nada é enviado" (LGPD); (d) "a equipe Zion monta o seu estudo" e "o dossiê vai para a equipe" (dossiê prévio e anexos) | M43 + M71 | pendente (patch em preparação) |
| G3 | **Artes e texto do Carrossel C alinhados à vistoria:** o cartão 6 ainda diz "9 módulos, 70 aulas e materiais" (`build.js` linha 52) e o texto primário de `COPIES.md` também; a landing e o checkout dizem "70 conteúdos" | M72 | pendente (só repositório) |
| G4 | **Landing B v3** com título e metadados corretos, **formulário da Sessão publicado**, **obrigado v3** com a URL real do formulário e **publicados**, nessa ordem | M73, M74, M75, M78 | pendente |
| G5 | **Checkout limpo:** nome, título e descrição (v3), nome do produto, capa 500×500, "Página de obrigado" | M76, M77 | pendente |
| G6 | **Rastreamento mínimo** (seção 4) e **compra de teste aprovada** (critérios R1 a R6 e R8, seção 4.3) | M79, M80 | pendente |
| G7 | **Campanha criada PAUSADA e conferida** (seção 5), na conta que Bruno confirmar | M81 | pendente |
| G8 | Dados de Bruno: conta de anúncios, Página e perfil do Instagram, forma de pagamento do Meta, **prazo de resposta da Sessão** (o formulário tem o marcador "X dias úteis (prazo a definir)" na tela de sucesso [E, `forms_get` 25/11]) | M74, M81 | pendente |
| G9 | Vendedor apto no dia da ativação: `canSell` true [E, `sellers_status` 25/11: banco aprovado, vendedor `pending`, `canSell` true]. Reconferir no dia (se `canSell` virar false, nenhum checkout vende) | checklist | conferir no dia |

### 1.2 NÃO bloqueia o gasto da Fase 1 (pode andar em paralelo ou depois)
- **Entrada por WhatsApp, script de venda, diagnóstico gratuito, CRM de WhatsApp** (M62, M63, M64, M67, M69), **venda quente** (M55 quente), captação, educação por e-mail (M52), modelo de WhatsApp (M38), públicos por lista de leads (M39, M54).
- **Exclusão de compradores no Meta (M53):** desejável antes do dia 1, mas não bloqueia (o público frio é amplo e os compradores existentes são poucos [H]); se Bruno já tiver o público `EXCL | compradores MM47`, o ChatGPT aplica. Leads: **não** excluir por lista sem base legal (M39); exclusão de leads "quando tecnicamente possível" = só por público de engajamento do Meta, que ainda não existe (nada captado) [E].
- Páginas antigas (M44, M45), Terra-capital (M47), vídeos novos de Bruno (M66), teste A/B de landing (M28), painel (M58), fila de produtos (M59).
- Do vistoria §10, **não bloqueiam** [H]: descrições com "Land Bank" nos e-books ("caminhos possíveis, não promessas"), vídeo 16, cartão final do tutorial do Pilar 7, e-books de aprofundamento com "D06", nome da turma "(R$ 97)" [NC se o aluno vê], anexos do Kit do Investidor e planilhas EXEMPLO (a landing diz "guia das 6 peças"), 17 vídeos no YouTube (a landing não cita número), citações de "simulador" e "mentor de IA" nas descrições das fichas (Bruno decide se sobe para G2; a landing não os cita).
- **Recuperação das compras de 24/11 sem UTM (M10):** não bloqueia, mas tem **prazo próprio** (leitura B3 até 27/11, limite duro 01/12, `../09-tracking/recuperacao/RECUPERACAO_COMPRAS_SEM_UTM.md`). O passo B3 é o mesmo da seção 4 (Gerenciador de Eventos › Visão geral › evento Purchase): fazer junto.

## 2. Sequência de execução (resumo)
Cada passo só começa com a frase `aprovado: Mxx` de Bruno (silêncio não é aprovação; reverter também exige). Passos 2 a 4 podem andar em paralelo.
| Passo | Item | O que | Quem | Depende de |
|---|---|---|---|---|
| 1 | M70 | Teto R$ 30/dia, Fase 1, só venda fria; `CLAUDE.md` | Bruno decide e edita | nada |
| 2 | M71 (+ M43) | Correções do produto (`15-correcoes-produto`) | Claude executa | patch pronto |
| 3 | M72 | Ajustes de arte e texto do Carrossel C (repositório) | Claude | nada |
| 4 | M73 | Título, nome e descrição da página B v3 e do obrigado (rascunhos) | Claude | nada |
| 5 | M74 | Publicar o formulário da Sessão (prazo definido) | Claude | prazo de Bruno |
| 6 | M75 | Reimportar o obrigado v3 com a URL do formulário e publicar | Claude | M74 |
| 7 | M76 | `offers_update` (nome, título, descrição v3) | Claude | M74 |
| 8 | M77 | Painel: nome do produto, capa 500×500, "Página de obrigado" | Bruno | M75, M76 |
| 9 | M78 | Publicar a B v3 em `/mini-mentoria-b-v3` | Claude | M73, M76, M77, G2 |
| 10 | M79 | Rastreamento mínimo no painel | Bruno | M78 |
| 11 | M80 | **Compra de teste** Pix R$ 47 e reembolso | Bruno (Claude confere) | M78, M79 |
| 12 | M81 | **Conferir e ajustar a campanha existente `120250560823800016`** (PAUSADA); criar outra só se for incompatível | ChatGPT | M80 aprovado, M72, G8 |
| 13 | n/a | Conferência final de tudo pausado | ChatGPT e Claude | M81 |
| 14 | M82 | **Ativar** (início dos 14 dias) | Bruno aprova; ChatGPT ativa | checklist 5.8 |
| depois | M83 a M86 | Pausa por critério, Purchase, despublicar a v1, decisão do dia 14 | conforme seção | |

## 3. PUBLICAÇÃO da landing B v3, obrigado e formulário

### 3.1 Decisão de URL: publicar em `/mini-mentoria-b-v3` ou substituir `/mini-mentoria`
Estado lido em 25/11 [E]: `/mini-mentoria` (`be23f04a…`) está **no ar** (publicada em 25/11 03:51) com a v1 (botões "QUERO TRANSFORMAR MEU TERRENO", "cadastre seu terreno no banco de áreas da Zion", título "Zion Collection · Inscrição (Cadastro de Projetos)…"); a `/mini-mentoria-b-v3` devolve 404 (não publicada, `lastPublishedAt` null).
| Critério | **A · publicar o rascunho como `/mini-mentoria-b-v3`** (recomendada) | B · importar a v3 sobre `/mini-mentoria` |
|---|---|---|
| Efeito no que está no ar | nenhum: a v1 segue como está | **muda ao vivo na hora** (importar numa página publicada atualiza a versão no ar [E, lição do ClickMax]) |
| Reversão | `pages_unpublish` da v3 (imediato) | reimportar a v1 (exige o HTML da v1 guardado: `pages_clone` antes) |
| UTM e leitura | URL própria: toda visita em `-b-v3` é da Fase 1 | mistura visitas antigas com as da Fase 1 |
| Risco residual | a v1 (incompatível) continua acessível por links antigos [NC: onde existem] | a página nova vai ao ar antes de checkout, formulário e obrigado estarem prontos |
| Custo | URL com "-b-v3" visível (cosmético) | URL limpa |
**Recomendação: A.** Anúncios usam `https://infoprodutos-zion.clickmax.space/mini-mentoria-b-v3`. A v1 fica até migrar: depois que a Fase 1 estiver rodando e **sem link ativo apontando para ela** (conferir links de modelos de WhatsApp, Bela e anúncios pausados [NC]), propõe-se **despublicar** a v1 (M85). Não se importa nada em `be23f04a…`.
O `manifesto.json` do Carrossel C já aponta para a B v3 [E]; o `COPIES.md` e os arquivos do A1 ainda citam `/mini-mentoria` (v1): **vale a URL da B v3**.

### 3.2 M73 · Título e metadados da página (achado novo) · `aprovado: M73`
**Achado [E]:** o HTML publicado da v1 usa o **nome interno da página** como `<title>` e `og:title` ("Zion Collection · Inscrição (Cadastro de Projetos) (Copy) …") e `og:description` = "Página criada com Clickmax Pages". A B v3 tem `title` null e o nome interno herdado do mesmo clone: publicada assim, a aba do navegador e a **prévia do link no Meta** diriam "Inscrição (Cadastro de Projetos)", contradizendo a regra "não vendemos inscrição".
- **Chamadas exatas (só rascunhos, sem publicar):**
  1. `pages_update` `{workspaceId: e87e8ba9-37cf-4c54-9a97-3e4e1b01827a, pageId: e0933e71-255e-4edc-bfec-92ba6a0121ac, data: {name: "Mini Mentoria · Landing B v3"}}`
  2. `pages_update_config` mesmo `pageId`, `data: {title: "Mini Mentoria de Estruturação Zion | R$47", description: "Formação digital paga: aprenda o passo a passo para estruturar o seu empreendimento turístico. R$47, pagamento único, 12 meses de acesso, garantia de 7 dias."}`
  3. Obrigado `1a0aed43-2f82-4b0a-826f-0424e2def674`: `name` "Mini Mentoria · Obrigado v3"; `title` "Obrigado | Mini Mentoria de Estruturação Zion"; `description` "Compra confirmada. Veja como entrar na plataforma."
- **Antes/depois:** nome e título "…Inscrição (Cadastro de Projetos) (Copy)…" → nomes acima. **Risco:** nenhum em produção (rascunhos; conferir `lastPublishedAt` null antes e depois). **Reversão:** repetir com os nomes antigos (guardados acima). **Verificação:** `pages_get` mostra `name`, `title`; depois da publicação, `<title>` e `og:title` no HTML (3.6). Não vi o `<title>` final renderizado antes de publicar [NC]: confere-se após M78.

### 3.3 M74 · Formulário da Sessão de Diagnóstico Estratégico · `aprovado: M74 prazo de resposta ___ dias úteis`
Estado [E, `forms_get` 25/11]: formulário `aff270f4-0e83-4f4f-8b6f-f62ae00d1392`, `status` **draft**, sem página, funil nem domínio; `publicUrl` = `https://api.clickmax.io/forms/r1ESmIV-ntTr-ZWRsiInjgIR` (um GET devolveu 200 e o HTML do formulário, mesmo em rascunho; se **aceita envio** em rascunho: [NC], não testado e nada foi enviado). A tela de sucesso tem o marcador **"em até X dias úteis (prazo a definir)"**: **não pode ir ao ar assim**. O fluxo `ae20a311…` (confirmação por e-mail e etiqueta) está em rascunho (0 execuções) e continua assim: **sem e-mail de confirmação automático** até outro "aprovado".
- **O que muda:** (1) `forms_replace_schema` com o mesmo schema, trocando só `settings.successMessage` pelo prazo que Bruno informar (reversão: reenviar o texto atual); (2) `forms_update` `{id: aff270f4…, status: "active"}` (reversão: `status: "paused"`); (3) reler `forms_get` (status `active`, `publicUrl`) e abrir a URL.
- **Por que antes do obrigado e da oferta:** o obrigado (M75) e a descrição do checkout (M76) **prometem** a Sessão; o link precisa existir e funcionar.
- **Política (Bruno, 25/11):** a Sessão é só para projetos qualificados, por solicitação; o limite semanal é definido depois da compra de teste; até lá a equipe aprova com cautela e mede. Sugestão do financeiro para prazo e duração: resposta em até 5 dias úteis e 30 min por vídeo (a confirmar por Bruno). Não citar limite em anúncio, página nem checkout.
- **Operação:** quem lê as solicitações (`forms_submissions_list` do `aff270f4…`) e responde dentro do prazo prometido: **[BRUNO] indicar**. Sem responsável, não prometer prazo.
- **Risco:** formulário público recebe dado pessoal e link do Dossiê de qualquer pessoa que tenha a URL (não só compradores; o filtro é a análise manual). Consentimentos opcionais já estão separados e desmarcados; o texto de LGPD é o do próprio formulário (revisão jurídica: M39 [NC]).

### 3.4 M75 · Obrigado v3 com a URL real e publicação · `aprovado: M75`
Estado [E]: `1a0aed43…` é rascunho (`lastPublishedAt` null, sem oferta); o fonte tem o marcador `{{LINK_SOLICITACAO}}` no botão "SOLICITAR A SESSÃO (APÓS CONCLUIR O DOSSIÊ)". **Não publicar com o marcador.**
Ordem (dependência explícita): **M74 (formulário ativo) → M75 (importar e publicar o obrigado) → M77 (ligar o obrigado no checkout)**.
1. `python3 -I zion-sales-engine/07-landing-pages/mini-mentoria/obrigado-v3/build.py` e, fora do repositório, `sed 's#{{LINK_SOLICITACAO}}#https://api.clickmax.io/forms/r1ESmIV-ntTr-ZWRsiInjgIR#g' obrigado-v3/index.html > <scratchpad>/obrigado-final.html`. (Se `forms_get` mostrar outro `publicUrl` depois de ativar, usar o novo. Endereço mais curto por `pathSlug` ou domínio: [NC], não necessário.) Conferir `grep -c '{{' obrigado-final.html` = 0.
2. `pages_validate_html` (manifest `thank-you`) e `pages_import_html_draft` com `pageId 1a0aed43…`, manifest `thank-you`, **sem** `offerId` e **sem** `funnelId`.
3. `pages_publish` do obrigado; conferir `lastPublishedAt` não nulo (o publish pode devolver sucesso sem publicar [E]).
- **Antes/depois:** botão sem destino → botão abre o formulário; página 404 → no ar em `/obrigado-mini-mentoria`. **Risco:** baixo (ninguém chega lá sem pagar, até o M77 ligar). **Reversão:** `pages_unpublish`; reimportar o fonte com marcador não é necessário. **Verificação:** GET 200; `curl … | grep -c "api.clickmax.io/forms/r1ESmIV"` = 1; `grep -ci "R\$ *97\|R\$ *270\|land bank"` = 0; clicar no botão abre o formulário (Bruno, no celular).
- Pixel no obrigado: a venda vem do checkout, não da página; **não** marcar "Página de conteúdo" no obrigado (`FUNIL_DE_EVENTOS_P0.md` §3.3).

### 3.5 M78 · Publicar a B v3 · `aprovado: M78 publicar B v3 em /mini-mentoria-b-v3`
Pré-requisitos: M73, M76, M77 feitos; G2 resolvido; Bruno viu o rascunho no celular pelo painel ("Visualizar") [NC: o endereço do rascunho devolve 404 e o checkout é bloqueado neste ambiente, ninguém aqui viu o checkout renderizado].
- **Chamada:** `pages_publish` `{workspaceId, pageId: e0933e71-255e-4edc-bfec-92ba6a0121ac}`. **Não** reimportar nada (o fonte v3 já está importado; `pages_get` de 25/11 15:39 mostra a página válida com `offerId 0c71eeba…` e 2 CTAs com preço).
- **Antes/depois:** 404 → 200 em `/mini-mentoria-b-v3`; `/mini-mentoria` intocada.
- **Verificação (lastPublishedAt e HTML ao vivo):**
  1. `pages_get` → `lastPublishedAt` **não nulo**, posterior a "agora" menos alguns minutos. Se nulo: o publish não pegou; repetir uma vez; se persistir, parar e avisar Bruno (não importar de novo).
  2. `curl -s https://infoprodutos-zion.clickmax.space/mini-mentoria-b-v3 -o b.html` e conferir (resultados esperados; cada linha é um teste):
     - `grep -o "<title>[^<]*" b.html` = "Mini Mentoria de Estruturação Zion | R$47"; `og:title` igual; `og:description` ≠ "Página criada com Clickmax Pages".
     - `grep -c "QUERO ACESSAR A PLATAFORMA POR R\$47" b.html` ≥ 1; `grep -c "Formação paga" b.html` ≥ 1; `grep -c "70 conteúdos" b.html` ≥ 1.
     - `grep -c "payments.clickmax.io/custom/e0933e71-255e-4edc-bfec-92ba6a0121ac/yhyiqUB9OF" b.html` = 1 (na v1 o iframe aparece assim, com o id da própria página e o hash `yhyiqUB9OF` [E]). Se o id da página for outro, o checkout aponta para a página errada.
     - `grep -ci "inscri\|R\$ *97\|R\$ *270\|land bank\|70 aulas\|agendar\|taxa de" b.html` = 0.
     - `fbq` presente (pixel inserido pelo ClickMax [E na v1]).
  3. `pages_tracking_status` com o `pageId`: `lastPageViewAt` passa de null depois da 1ª visita (Bruno abre a URL uma vez em janela anônima).
  4. Bruno, no celular: topo mostra a faixa "Formação paga · Mini Mentoria Zion · R$47"; primeiro botão de pagamento só depois da oferta; nenhum botão no topo.
- **Risco:** visitas orgânicas sem anúncio podem comprar antes da compra de teste (é uma venda real: aceitar e reembolsar se for o caso). **Reversão:** `pages_unpublish` `e0933e71…` (a URL volta a 404; nada mais muda).

## 4. CHECKOUT, OFERTA e RASTREAMENTO

### 4.1 M76 · `offers_update` da oferta `0c71eeba-2654-432c-9701-0a31e6113a08` · `aprovado: M76`
**Conferência contra a leitura ATUAL** (`offers_get`, 25/11) [E]: `status approved`, `hash yhyiqUB9OF`, `gatewayName ticto`, `incompleteReason []`, `providerSyncError {}`, `originalPrice 4700`, Pix e cartão 1x (boleto off, sem recorrência), `limitToRefund 7`, `softDescriptor ZIONACADEMY`, `supportPhone +55 48 6137-1061`, `showTimer/showCoupon false`, `checkoutPlugins/socialProof/banners null`, `checkoutImageSource product`, imagem do produto = placeholder genérico, 1 entrega `internal_membership` (portal `3ef7a340…`, turma `087479a3…`), `productName` "Mini Mentoria de Estruturação", `hasTransaction` false para a oferta (nenhuma venda da oferta de R$ 47 ainda) [E, `products_get`]. A descrição atual é exatamente o texto de reversão de `CHECKOUT_LIMPO_MM47.md` §7 (sem a Sessão, "sem reunião"): **o payload de `CHECKOUT_LIMPO_MM47.md` §3 parte da base certa.**
**Ajuste desta sessão:** a frase da Sessão ganhou "só para projetos qualificados" (decisão de Bruno, 25/11); por isso a descrição acima difere em 1 trecho do payload de `CHECKOUT_LIMPO_MM47.md` §3 e **prevalece** sobre ele.
**Achado na conferência:** `offers_update` é **substituição total**. A leitura atual traz `externalId "O668752CD"` (id da oferta no gateway) e as listas vazias `allowedEmails`, `crmListIds`/`requiredOfferIds`, `coproductions`. O payload de `CHECKOUT_LIMPO_MM47.md` **não** os envia. Enviar `externalId` junto é a escolha segura (omiti-lo pode zerar o vínculo com o gateway [H, o esquema aceita `externalId: null`]). Payload final = o do arquivo + estas 4 chaves:
```json
{
  "workspaceId": "e87e8ba9-37cf-4c54-9a97-3e4e1b01827a",
  "id": "0c71eeba-2654-432c-9701-0a31e6113a08",
  "name": "Mini Mentoria de Estruturação Zion",
  "checkoutTitle": "Mini Mentoria de Estruturação Zion",
  "description": "Formação digital autônoma para estruturar um empreendimento turístico no seu terreno: 9 módulos e 70 conteúdos (vídeo-aulas e 8 tutoriais em vídeo, 8 fichas interativas, 8 e-books em PDF, 2 planilhas de cálculo com fórmulas, Kit do Investidor com guia das 6 peças, 9 comandos de IA e Dossiê para baixar em PDF). Acesso por 12 meses. Pagamento único de R$47, sem mensalidade. Pix ou cartão à vista. Reembolso em 7 dias. Etapa opcional depois de concluir o Dossiê: solicitação da Sessão de Diagnóstico Estratégico, gratuita, só para projetos qualificados, sujeita à análise e à agenda. Não há atendimento individual contínuo. Parceria e investimento não são garantidos.",
  "type": "course", "productType": "internal", "productClass": "Curso", "productCategory": "Negócios e Carreira",
  "currency": "BRL", "originalPrice": 4700, "newPrice": null, "defaultInstallment": 1,
  "paymentConfig": {"pix": {"active": true}, "boleto": {"active": false}, "credit": {"active": true, "installments": 1}, "recurrence": null},
  "limitToRefund": 7, "supportPhone": "+55 48 6137-1061", "softDescriptor": "ZIONACADEMY",
  "requiredAddress": false, "showDescription": true, "showTimer": false, "timerMinutes": 10, "showCoupon": false,
  "highlightInstallment": false, "passPlatformFee": false, "allowAffiliateResale": true,
  "audience": "everyone", "requiredOffersMatch": "any", "checkoutImageSource": "product",
  "bannerDesktop": null, "bannerMobile": null, "socialProof": null, "checkoutPlugins": null,
  "country": "BR", "language": "pt", "offerSupportEmailId": null,
  "externalId": "O668752CD", "allowedEmails": [], "crmListIds": [], "requiredOfferIds": [], "coproductions": []
}
```
Validação do payload contra o esquema da ferramenta (lido em 25/11): todos os campos existem e respeitam os limites (descrição ~665 caracteres, máximo 1000; `checkoutTitle` 34, máximo 120; `softDescriptor` 11, máximo 15). `offerSupportEmailId: null` mantém o e-mail de suporte padrão da conta (o endereço não é copiado para o repositório). `confirmRepublish` só vale para site Max Design e não se aplica [NC se algum site Max Design usa esta oferta: nenhuma página lida é Max Design].
- **Muda para o comprador:** nome do item no checkout (e nos e-mails do sistema de quem comprar depois), título e descrição. **Não muda:** preço, hash, entrega, acessos, gateway.
- **Antes/depois:** "Mini Mentoria de Estruturação" + descrição "sem reunião" → "Mini Mentoria de Estruturação Zion" + descrição v3 com a Sessão opcional.
- **Risco:** (1) oferta `approved` pode voltar a revisão [NC] → ler `status`/`canSell` logo depois (se sair de `approved`, **não** publicar nada, avisar Bruno); (2) o checkout da v1 (`/mini-mentoria`, no ar) também passa a mostrar o nome novo e a Sessão: aceitável; (3) a descrição promete a Sessão: só depois do M74.
- **Verificação:** `offers_get` e comparar campo a campo com a leitura de 25/11: só `name`, `checkoutTitle` e `description` mudam; `hash` `yhyiqUB9OF`, `status approved`, `externalId`, `deliverables`, `thumbnail`, `paymentConfig`, `supportPhone`, `softDescriptor` iguais; `incompleteReason []`; `providerSyncError {}`; `offers_get_incomplete_reason` vazio.
- **Reversão:** reenviar o mesmo payload com `name` "Mini Mentoria de Estruturação", `checkoutTitle` null e a descrição anterior (texto em `CHECKOUT_LIMPO_MM47.md` §7). Acessos de compradores não dependem do nome.

### 4.2 M77 · Painel (Bruno): nome do produto, capa 500×500 e página de obrigado · `aprovado: M77`
Não existe `products_update` nem upload de imagem por ferramenta: **só o painel** [E: `CHECKOUT_LIMPO_MM47.md` §1; `offers_set_product_image` só aceita URL do armazenamento do ClickMax].
| Onde | O que fazer | Antes → depois | Verificação | Reversão |
|---|---|---|---|---|
| ClickMax › **Produtos** › Mini Mentoria › editar produto (rótulo exato do menu: [NC]) | Nome do produto `cbbb5fb1-550f-4a8d-b269-5122c17b7780` | "Mini Mentoria de Estruturação" → **"Mini Mentoria de Estruturação Zion"** | `products_get` mostra o nome novo | reeditar |
| mesmo local, imagem do produto | Enviar `zion-sales-engine/08-checkouts/capa/capa-500.jpg` (JPG 500×500, abaixo de 2 MB [E: arquivo conferido, 500×500]); URL pública do arquivo no site, se precisar baixar: `https://bchaerk-creator.github.io/zion-hotel-ai-developer/` + caminho de `docs/` (o arquivo está em `zion-sales-engine/`, **não** em `docs/`, então a URL pública **não existe**: baixar do repositório ou me pedir cópia em `docs/p/…`) | placeholder genérico → capa | `offers_get` → `thumbnail` ≠ `product-placeholder.png` | reenviar outra imagem |
| ClickMax › produto › oferta › **Configurações do checkout** › **Página de obrigado** [E, docs.clickmax.io/features/sales/checkout: "a URL para onde o comprador vai após pagar; em branco, cai na página padrão"] | Colar `https://infoprodutos-zion.clickmax.space/obrigado-mini-mentoria` (já publicada no M75) | vazio (padrão do ClickMax) → obrigado v3 | **teste de compra (M80)**; "Visualizar checkout" abre a prévia (docs) | apagar o campo (volta ao padrão) |
- **Onde ver o nome no checkout:** botão **Visualizar checkout** (Configurações do checkout) e a prévia no **celular real** (4G, janela anônima). O checkout em si é o iframe `payments.clickmax.io`, **bloqueado neste ambiente**: ninguém aqui o viu renderizado [NC]. Bruno confere: nome "Mini Mentoria de Estruturação Zion", R$ 47, descrição legível, Pix e cartão à vista, sem cronômetro, sem endereço, imagem da capa; envia print.
- Se o checkout mostrar o nome do **produto** e não o da **oferta** [NC], é por isso que os dois nomes são igualados.

### 4.3 M79 e M80 · RASTREAMENTO mínimo e COMPRA DE TESTE
**Fontes:** `../09-tracking/PLANO_EXECUTAVEL.md`, `FUNIL_DE_EVENTOS_P0.md` §7 (8 eventos), `VALIDACAO_EM_TESTE.md` §5, `PADRAO_UTM.md` §9. Menu verificado: `docs.clickmax.io/guides/manage-pixels` ("Tráfego › Pixel e trackeamento"; Tráfego fica dentro de Marketing).

**M79 · Rastreamento mínimo (Bruno, painel) · `aprovado: M79`** (tutorial A1 a A4, B1 a B3, em `../09-tracking/tutorial/`):
1. **Pixel `903918118859018` ativo e ligado à tela certa:** Tráfego › Pixel e trackeamento › linha do pixel › **Ver detalhes**: devem constar o **Produto**, a **Oferta** e a **página B v3** (depois de publicada) [E, docs `pixel-scopes`/`pixel-details`]. Se a B v3 (clone) **não** constar, marcar o pixel em Configurações da Página › Scripts (ou aba Script da página) [NC: pixel herdado pelo clone]. Credencial configurada. Prova de que a página dispara: `pages_tracking_status` e o Testar eventos do Meta (o preview do editor **não** rastreia [E]).
2. **API de Conversões:** Editar o pixel › bloco **API de Conversões da Meta** › colar o **token** (gerado por Bruno no Meta; **nunca** no chat, no Git ou em print) › **Testar token** (não conta como compra). Se já houver "Token guardado", só **Testar**. Sem token o Purchase de Pix pode não chegar ao Meta (é o caso mais comum [E, doc]).
3. **Evento Comprou:** interruptores **No navegador** e **Pelo servidor** ligados e, em **Formas de pagamento**, **Pix e cartão** marcados.
4. **Abriu o checkout:** ligar **Só contar depois dos dados pessoais** (hoje o evento dispara ao carregar o iframe, então não mede intenção [E, auditoria]). **NÃO clicar em "Ativar eventos novos"** (renomeia `InitiateCheckout` para `AddToCart`).
5. **Código de teste:** preencher o do Gerenciador de Eventos (aba Testar eventos) **só durante a compra de teste** (enquanto preenchido, os eventos aparecem na aba de testes e **não contam como conversão** [E, doc]); **limpar antes de ativar** (item do checklist 5.8). Assim a compra de teste não vira "Purchase real" no Meta.
6. **Passo B3 (Gerenciador de Eventos › Visão geral):** período da primeira compra real até hoje, evento Purchase: existe? Origem, valor, moeda (também serve ao prazo de 01/12 das compras de 24/11).
7. **url_tags / UTM** (seção 5.5) ficam no anúncio; o destino não leva parâmetros nem `#`.
- **Reversão:** desligar a opção do item 4; remover token; religar o que desligou (print do estado antes de mexer). **Risco:** mexe na medição de tudo; evento enviado ao Meta não se desfaz.

**M80 · Roteiro da COMPRA DE TESTE (Bruno compra, Claude confere) · `aprovado: M80 compra de teste Pix R$ 47 e reembolso`**
Condições: M76 a M79 feitos, código de teste preenchido, receptor `capi-webhook` **não** ligado (um só caminho de Purchase). Compra de **uma** unidade, dados do próprio Bruno, Pix. Celular, janela anônima, sem bloqueador de anúncios. Abrir **um link com UTM de teste** (ids numéricos fictícios, para exercitar o padrão do §9 sem poluir a campanha):
```
https://infoprodutos-zion.clickmax.space/mini-mentoria-b-v3?utm_source=teste&utm_medium=manual&utm_campaign=teste-venda-fria&utm_content=mm47-vc-carrossel-c-venda&utm_term=111&sck=222&ad_id=111&campaign_id=222&adset_id=333
```
| # | Passo | O que verificar (tabela de 8 eventos, `FUNIL_DE_EVENTOS_P0.md` §7) | Como (e quem) | Aceite |
|---|---|---|---|---|
| 1 | Abrir o link; ver a UTM na barra | **Visita** (`PageView`) | Testar eventos do Meta (Bruno, print); `pages_tracking_status` (Claude) | PageView aparece; `lastPageViewAt` preenchido |
| 2 | Rolar até a oferta (não clicar) | Visualização da oferta: **desligada** (`pixelViewContent` false) | sem verificação no Meta | registrado como "sem medida"; proxy = clique no CTA |
| 3 | Clicar em **QUERO ACESSAR A PLATAFORMA POR R$47** | **Clique no CTA com preço** (`button_click`, `cta-0` ou `cta-1`) | ClickMax, leitura de visitantes/funil (Claude: `visitors_*`) [NC se o relatório separa por botão] | ClickMax registra o clique; **não** chega ao Meta |
| 4 | Abrir o checkout **sem preencher nada** por 30 s | **Início efetivo de checkout:** nenhum `InitiateCheckout` ainda | Testar eventos (Bruno) | **nenhum** IC antes de nome e e-mail (se o item 4 do M79 estiver ligado) |
| 5 | Informar nome e e-mail | `InitiateCheckout` | Testar eventos | **1** IC |
| 6 | Escolher Pix e **gerar o Pix, sem pagar**, esperar 2 min | **Pix gerado** ≠ Purchase | Testar eventos; Vendas (venda `pending`); Claude: `transactions_list`/`sales_get_utms` | **nenhum Purchase**; venda pendente com UTMs |
| 7 | **Pagar o Pix (R$ 47)** | **Compra aprovada** (`Purchase`) | Testar eventos; Histórico de envio do pixel; Claude: `sales_get_utms`, `sales_get_details` | **1** Purchase em até 5 min; `value` 47,00 (nunca 0,47 / 4700); `currency` BRL; origem Servidor (e Navegador, **mesmo** `event_id`); Histórico "Enviado" |
| 8 | Ver a venda no ClickMax | UTM gravada | `sales_get_utms` | `utm_source=teste`, `utm_medium=manual`, `utm_campaign=teste-venda-fria`, `utm_content`, `utm_term`, `sck` gravados; ids de anúncio, campanha e conjunto como campo ou só dentro da URL [NC: anotar qual] |
| 9 | Depois do pagamento | **Obrigado** | Bruno (print) | cai em `/obrigado-mini-mentoria`, sem R$ 97, R$ 270 nem "reunião" fora da Sessão opcional; botão da Sessão abre o formulário (**não enviar**) |
| 10 | Esperar | **E-mail de acesso**; **entrega** | Bruno abre a caixa de entrada; Claude: `member_users_get_by_lead`, `member_users_list_by_classroom` | e-mail de acesso chega [NC, nunca provado]; contato vira membro da turma `087479a3…` |
| 11 | Entrar na plataforma | **Login e primeiro acesso** (`firstAccessWithoutPass` true [E]) | Bruno (print) | entra sem criar senha [NC]; abre o Onboarding e uma aula; **anotar** se a 1ª aula ainda mostra "Land Bank" (G2) |
| 12 | **Reembolsar** a compra de teste (Bruno no painel, Minhas Vendas, ou `transactions_refund` com "aprovado" expresso) | **Reembolso** | Claude: venda `refunded`; Testar eventos | status `refunded`; **nenhum Purchase novo**; (se o receptor estiver ligado, `refund_registered`) |
| 13 | Decidir o acesso do contato de teste | n/a | Bruno | só o contato de teste; **nunca** remover acesso de comprador real |
| 14 | **Limpar o código de teste** do pixel | n/a | Bruno | campo vazio (confere pela tela do pixel) |
Critérios (`PLANO_EXECUTAVEL.md` §5): **R1** Purchase só após pago (passos 6 e 7), **R2** valor e moeda (7), **R3** CAPI funcionando (7), **R4** deduplicação (7, mesmo `event_id`), **R5** ids de campanha/anúncio na venda (8), **R6** UTM na venda (8), **R8** Pix gerado ≠ pago e reembolso sem novo Purchase (6 e 12). **R7** (conciliação ≤ 10%) fica para o dia 1.
- **Se o passo 6 mostrar Purchase ao gerar o Pix, ou o passo 7 não mostrar Purchase de servidor:** defeito confirmado. Não ativar. Opção C do `PLANO_EXECUTAVEL.md` §2 (receptor `capi-webhook`, desligando o Purchase nativo), com novo "aprovado".
- **Cartão não será testado** (decisão de Bruno: Pix). Risco aberto: status e taxa do cartão sem prova [NC]; Purchase de cartão depende de **Formas de pagamento: cartão marcado** no pixel (M79 item 3). Pode-se fazer um teste de cartão depois, com novo "aprovado".
- **Reembolso:** depois de reembolsar, a venda de teste fica fora do CPA (`is_test`/UTM `teste`); o Meta **não** desconta o Purchase (não existe Purchase negativo [NC]); com o código de teste preenchido, nem entrou na contagem.
- **Risco geral do teste:** é compra real (R$ 47 sai e volta; a taxa fixa do gateway de R$ 2,49 pode **não** ser devolvida no reembolso [NC]). **Reversão:** reembolso.

## 5. CAMPANHA FRIA (o ChatGPT cria PAUSADA; ver `HANDOFF_CHATGPT_FASE1.md`)

### 5.1 Objetivo e otimização
- **Campanha de Vendas com evento Purchase** (pixel `903918118859018`), a que o ChatGPT já criou (`120250560823800016`, seção 5.2). Isso só é seguro porque **a ativação (M82) exige a compra de teste aprovada** (R1 a R4 e R8): o Purchase estará provado antes do primeiro real gasto. **Não** otimizar por início de checkout (evento antigo disparava no carregamento) nem por ViewContent (desligado). Fonte da verdade da venda: **ClickMax por UTM**, não o Meta.
- **Plano B (só se a compra de teste reprovar Purchase, R1 a R4):** não ativar a campanha de Purchase. Com novo "aprovado", criar campanha **Tráfego** otimizada por **Visualizações da página de destino**, mesmo teto, e tratar a Fase 1 como medição de visitas até o Purchase ser corrigido.
- Limite honesto [H]: com R$ 30/dia e CPA perto do líquido, saem poucas compras por semana; o Meta pode ficar em **aprendizado limitado**. **Não editar todo dia** (cada edição reinicia o aprendizado e invalida a leitura). Pausar é a única mudança prevista no meio do teste.

### 5.2 Estrutura
| Nível | Especificação |
|---|---|
| Conta | **Zion Collection 2** (`1271873041294684`) [BRUNO confirma]. **Não tocar** nas campanhas da Zion Bubble nem nas demais da Collection (todas pausadas) |
| Campanha | **Reaproveitar `120250560823800016`** (criada pelo ChatGPT; **o Windsor não a retorna [NC]**: conferir no Gerenciador). Lista de conferência e **"ajustar em vez de criar outra"** em `HANDOFF_CHATGPT_FASE1.md` §2. Estado **PAUSED**. Nome: se ainda não tiver leads nem vendas, ajustar para `venda-fria \| AAAA-MM-DD` (padrão `PADRAO_UTM.md` §9); o `utm_campaign=venda-fria` vem das tags, não do nome. **Limite de gasto da campanha R$ 420** como trava extra [NC: provavelmente só no Gerenciador] |
| Conjunto (1) | `fria-brasil-feed`. **Orçamento diário R$ 30 no conjunto** (ABO). Início só na ativação (M82); **data de término** = 14 dias depois da ativação [H] |
| Público | **Brasil amplo, Advantage+ público** (decisão de Bruno), sem interesses; idade como sugestão 25 a 65 [H]; registrar a escolha única |
| Exclusões | **Compradores** (`EXCL \| compradores MM47`, M53) **se já existir**; leads: **só por engajamento do Meta**, que não existe ainda; **não** subir lista de leads sem base legal (M39). Conferir `adset_targeting` pela leitura depois de criado [E, campo legível no Windsor] |
| Posicionamentos | **Manual: Facebook Feed e Instagram Feed.** Sem Stories, Reels, Audience Network, Messenger, Marketplace, busca nem coluna direita (arte 4:5 de 1080×1350 foi feita para feed). Advantage+ posicionamentos **desligado** |
| Anúncios | seção 5.4. Nome do anúncio = id do criativo (único na campanha) |
| Aprimoramentos | **Desligar** os "aprimoramentos criativos" automáticos do Advantage+ (música, filtros, variações de texto, recortes), porque alteram a arte e o texto aprovados; **desligar** "anúncios de vários anunciantes" [H] |
| Rastreamento | pixel `903918118859018`; vendas por **Purchase**; tags de URL da seção 5.5 |

### 5.3 Orçamento e leitura
Teto `T = R$ 30/dia`; `D = 14`; total R$ 420 (seção 0). **Conjuntos sem anúncio ativo contam como "configurados".** Soma de tudo ativo na conta Zion Collection 2 **do funil da Mini Mentoria** ≤ R$ 30/dia; nada mais ativo (confirmar por leitura na ativação). Campanhas da Zion Bubble ficam fora, sem tocar (M01: escopo do teto só para a Mini Mentoria [BRUNO confirma em M70]).

### 5.4 Criativos
| Papel | id (= nome do anúncio = `utm_content`) | Fonte | Estado |
|---|---|---|---|
| **Principal** | `mm47-vc-carrossel-c-venda` (Carrossel C de venda, **10 cartões** 1080×1350) | **`docs/ads/venda-carrossel-c/manifesto.json`** (definitivo: 10 URLs públicas, texto primário, título, descrição, `url_tags`, destino B v3). **Não recriar**; o ChatGPT copia do manifesto | arte final; **1 ajuste pendente (M72):** o `build.js` (linha 52) ainda desenha no cartão 6 "9 módulos, 70 aulas e materiais" (a landing, o checkout e o texto dizem "70 conteúdos"); cartões 2 e 7 usam imagens do campeão de origem não verificada (legenda "ilustrativa") |
| **Apoio** (baseado em campeão) | `mm47-va1-dor-direta-venda` (Curso Terreno A1 v2 convertido em venda, 5 cartões) | `docs/ads/venda-a1/` (`COPIES.md`, `manifesto.json`, `carrossel-a1-venda-1..5.png`) | texto limpo na checagem; **falta o prefixo "Formação digital paga, R$ 47:"** na primeira linha (texto abaixo); destino lá é a v1: usar a B v3 |
| Reserva (**não sobe na Fase 1**) | `mm47p0-vp0-a3-saiba-o-custo` (versão P0 do campeão A3 v2) | `docs/ads/mm47-p0/` | **não está pronta:** o texto diz "Sem reunião e sem atendimento individual", "70 aulas e materiais" e "Kit do Investidor (guia e modelos)", que contradizem a oferta v3; precisa de nova versão do CREATIVE |
Os demais de venda fria do pacote v4 (F3 a F6) **não** entram: F2 e F3 foram substituídos pelas peças de campeões originais (v5) e F4 a F6 não são baseados em campeões [E, `PACOTE_PARA_CHATGPT_v4.md`]. Vídeos novos de Bruno: M66, fora da Fase 1.
**Texto do Carrossel C:** o do manifesto (abre com "Formação digital paga, R$ 47: Mini Mentoria de Estruturação Zion.", "70 conteúdos", Sessão "sujeita à análise e à agenda"). Ponto a aprovar por Bruno (M72): a frase "Ao concluir o Dossiê, você pode solicitar a Sessão…" segue a política "só projetos qualificados, por solicitação"; se ele quiser a palavra "qualificados" no anúncio, o texto do manifesto muda no repositório, não aqui. O manifesto traz 786 caracteres (a primeira linha visível tem 66).
**Texto do apoio A1** (= `COPIES.md` com o prefixo; **o ChatGPT usa este bloco**):
```
Formação digital paga, R$ 47: tem terreno, mas não tem capital? Aprenda o passo a passo para estruturar o seu projeto. Mini Mentoria de Estruturação Zion: aulas gravadas, fichas “Faça agora”, e-books por pilar, 2 planilhas em branco, Kit do Investidor e Dossiê em PDF. R$ 47, pagamento único, 12 meses de acesso, garantia de 7 dias.
```
Título `Mini Mentoria Zion · R$47` · Descrição `Pagamento único · Pix ou cartão · garantia de 7 dias` · Botão do Meta **Saiba mais** (a chamada personalizada fica na arte e na primeira linha). Termos proibidos (R$ 97, R$ 270, inscri, taxa, sócio, consultoria, Land Bank, agendar) ausentes nos dois textos [E, relido]; rodar o `check_termos.py` do CREATIVE no M72.

### 5.5 URLs e UTM (`PADRAO_UTM.md` §9, vale sobre os manifestos antigos)
Destino do anúncio, **sem parâmetros e sem `#`**: `https://infoprodutos-zion.clickmax.space/mini-mentoria-b-v3`. Tags no campo **Parâmetros de URL** do anúncio [NC: rótulo exato no Gerenciador], coladas uma vez, macros exatamente assim:
```
utm_source=meta&utm_medium=paid&utm_campaign=venda-fria&utm_content=<id do criativo>&utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}&adset_id={{adset.id}}
```
Carrossel C (idêntico ao `url_tags` do manifesto): `utm_content=mm47-vc-carrossel-c-venda` · A1: `utm_content=mm47-va1-dor-direta-venda`. `utm_campaign=venda-fria` (caminho; nunca o nome do produto). Sem sufixo `-varA/-varB` (não há teste A/B de landing). Aceite antes de ligar: a compra de teste (M80) grava `utm_*` e `sck`.

### 5.6 Conjuntos e testes de qualidade da entrega (o que o ChatGPT confere pausado)
Pré-visualização por posicionamento (Facebook Feed e Instagram Feed): cada cartão legível no celular; primeira linha "Formação digital paga, R$ 47:" aparece antes do "mais"; botão "Saiba mais"; link abre `/mini-mentoria-b-v3`; título da prévia do link = "Mini Mentoria de Estruturação Zion | R$47" (depende do M73); nenhum Audience Network; orçamento do conjunto R$ 30; estado PAUSED em campanha, conjunto e anúncios; leitura pelo Windsor confirma `PAUSED`.

### 5.7 Critérios de escala, pausa e continuação (Fase 1, R$ 30/dia, ligados a `PROTOCOLO_VALIDACAO_14_DIAS.md`)
Parâmetros (Bruno ajusta em M70/M60): `T` R$ 30; `D` 14; `k` 3 [H]; CPA máx. R$ 44,51 (líquido Pix, antes de impostos e custos [NC]); CPA desejado R$ 31,16 [H]; limite de reembolso 10% [H]. **Todo critério abaixo só PROPÕE; pausar e ativar exigem "aprovado".** Contagem de compras **só por UTM `venda-fria` no ClickMax**, sem testes e sem equipe; venda sem UTM = "não atribuída" (não entra no CPA da fria; reportar à parte). Faturamento não é lucro.
| Situação | Critério | Ação proposta |
|---|---|---|
| **Limite de perda** | gasto acumulado ≥ R$ 133,53 (`k × CPA máx.`, ≈ dia 5) **sem nenhuma compra atribuída**, com rastreamento íntegro | propor **pausar** (M83); relatório "interrompido por limite de perda, amostra insuficiente para concluir" |
| Rastreamento quebrado | Purchase duplicado; venda com UTM de `venda-fria` ausente em mais de `U` das vendas; `InitiateCheckout` voltando a disparar no carregamento; token recusado | corrigir **antes** de ler qualquer CPA; se houver gasto, propor pausar |
| Entrega/qualidade do tráfego | reprovação do anúncio; visualizações da página ÷ cliques (leitura do Meta) muito baixas (sinal de página lenta ou clique acidental; regra prática [H], limite proposto 70%, Bruno ajusta); custo por visualização da página subindo dia após dia sem mudança | propor pausar o anúncio ou conferir a página; sem decisão de mérito antes da amostra |
| Reembolso | reembolso em 7 dias acima de 10% com amostra mínima de compradores | propor pausar |
| Promessa fora do produto | comentário ou mensagem pedindo reunião, investimento, parceria, "cadastro" | revisar texto e arte; propor pausar o anúncio |
| Fim do teste | gasto chega a R$ 420 ou dia 14 | **o teste acaba**; sem novo gasto sem novo "aprovado" (M86) |
**Leitura no fim dos 14 dias** (janela de atribuição: até 7 dias depois do último gasto, **sem gasto adicional**), por **compras atribuídas `N`** (com as R$ 420 gastas: CPA = 420 ÷ N):
| `N` | CPA | Veredito | Recomendação (decide Bruno) |
|---|---|---|---|
| ≥ 14 | ≤ R$ 30,00 | positivo, abaixo do CPA desejado (ainda **provisório**: impostos, custos e reembolso sem valor [NC]) | **continuar/ampliar** em degraus de até 20% do orçamento, a cada 3 a 4 dias, com "aprovado" a cada degrau e novo `T` em M70 (**escalar além de R$ 30/dia exige novo teto**) |
| 10 a 13 | R$ 30,01 a R$ 42,00 | marginal: cobre o líquido bruto, mas sem folga | **manter** o orçamento (ou novo teste de 14 dias), corrigir criativo, página ou checkout, e reler |
| 1 a 9 | acima de R$ 42,00 | abaixo do ponto de equilíbrio bruto | **não escalar**; diagnosticar (custo por visita, conversão da landing, clique no CTA, checkout efetivo, Pix gerado × pago); decidir encerrar ou novo teste com orçamento novo |
| 0 | n/a | sem compra atribuída | **pausar/encerrar**; conferir se a UTM chegou à venda (rastreamento) antes de culpar o anúncio |
**Amostra e prova.** Com R$ 420 não se alcança `Nmin = 30` (exigiria CPA ≤ R$ 14). O resultado da Fase 1 é **descritivo**: CPA observado e taxas (visita → clique no CTA → checkout efetivo → Pix gerado → pago) com intervalo (Wilson 95%; com zero compras em `n` visitas, limite superior ≈ 3 ÷ `n`). **Nunca** declarar "vencedor" ou comparar criativos pelo menor CPA de poucas compras, por CPC baixo ou por muitos checkouts (o objetivo é comprador). Duas peças de anúncio em R$ 30/dia não dão base para dizer qual criativo é melhor: o Meta concentrará o gasto. Ponto de equilíbrio de conversão (hipotético, só para orientar a leitura): `r* = custo por visualização da página ÷ R$ 44,51`; por exemplo, custo por visualização de R$ 0,50, R$ 1,00 ou R$ 2,00 exige conversão visita → compra de ao menos 1,1%, 2,2% ou 4,5% (valores **hipotéticos**; a taxa real vem do ClickMax).
**Cadência:** diária (gasto × teto, estado, reprovação, entrega, vendas e Pix por `utm_campaign` e `utm_content`, venda sem UTM à parte; **sem decisão de mérito**); a cada 3 a 4 dias (entrega por anúncio, posicionamento, frequência, custo por visualização da página); semanal (relatório de decisão com amostra e intervalo). Nenhuma alteração de criativo, público, página ou checkout no meio do teste (se inevitável, registrar e tratar como novo teste).

### 5.8 Checklist de ativação (M82; **somente com `aprovado: M82 ativar venda-fria, teto R$ 30 por dia, Fase 1, início em AAAA-MM-DD`**)
Tudo marcado e registrado no LOG, na ordem:
- [ ] M70 aprovado e `CLAUDE.md` atualizado com a redação da seção 6.
- [ ] G2 (correções do produto) e G3 (arte e texto) fechados; G8 respondido.
- [ ] Landing B v3 **no ar**: `lastPublishedAt` preenchido, `<title>`/`og:title` corretos, iframe do checkout com o id da B v3, 0 termos proibidos (seção 3.5).
- [ ] Oferta `approved`, `canSell` true (`sellers_status` **no dia**), nome e descrição v3, capa, "Página de obrigado" ligada; `offers_get_incomplete_reason` vazio.
- [ ] Formulário da Sessão **ativo**, prazo definido, responsável nomeado.
- [ ] Compra de teste **aprovada** (R1 a R6, R8), reembolsada, e **código de teste do pixel LIMPO** (senão os eventos não contam como conversão).
- [ ] Campanha `120250560823800016` **conferida e ajustada** pela lista do `HANDOFF_CHATGPT_FASE1.md` §2 (**nenhuma campanha duplicada**); campanha, conjunto e anúncios **PAUSED**; destino `…/mini-mentoria-b-v3` sem parâmetros e sem `#`; tags de URL com `venda-fria`; botão "Saiba mais"; sem Audience Network; orçamento R$ 30; limite de gasto da campanha R$ 420 (se aplicável); aprimoramentos automáticos desligados; pré-visualização conferida por Bruno.
- [ ] Nada mais ativo no funil da Mini Mentoria; campanhas da Zion Bubble intocadas; as pausadas continuam pausadas (leitura Windsor `PAUSED`).
- [ ] Meta: forma de pagamento da conta válida e sem bloqueio [NC, Bruno].
- [ ] Ativar de **manhã (horário de Brasília)** para o dia 1 não ter orçamento diluído; registrar data de início; agendar a leitura diária.
- **Reversão:** `aprovado: M83 pausar` (pausa campanha; nada se apaga). **Efeito de pausar:** o gasto para na hora; o aprendizado do Meta reinicia ao religar.

### 5.9 Critérios que NÃO foram definidos (peço a Bruno em M70/M60)
`k` (3), limite de reembolso (10%), imposto e custos variáveis (sem valor [NC]), taxa do cartão [NC]. Enquanto estiverem em [H]/[NC], CPA máximo e margem são **teto superior**, não lucro.

## 6. CLAUDE.md · redação proposta para a linha de teto (Bruno aplica; eu **não editei** o arquivo)
Linha atual (§1, regras inegociáveis): "**Continua exigindo "aprovado" de Bruno:** gastar com anúncio (teto atual: R$ 0; campanhas só pausadas), disparar mensagens para leads, ativar automações, mexer em qualquer coisa que já existe."
**Nova redação (substituir só o trecho entre parênteses e acrescentar a sub-regra):**
> **Continua exigindo "aprovado" de Bruno:** gastar com anúncio, disparar mensagens para leads, ativar automações, mexer em qualquer coisa que já existe.
> - **Teto de anúncio (decisão de Bruno, 25/11/2026): Fase 1 · somente venda fria da Mini Mentoria de Estruturação Zion (R$ 47), até R$ 30 por dia e R$ 420 em 14 dias**, na conta de anúncios que Bruno confirmar. **Fora disso o teto continua R$ 0** (captação, venda quente, WhatsApp, outros produtos, outras contas, aumento de orçamento e prorrogação). **Campanhas e anúncios nascem sempre pausados**; ativar, aumentar orçamento, religar ou trocar o otimizador só com `aprovado: Mxx` de Bruno (itens M70 a M86 da matriz). O gasto só começa depois do checklist de ativação do `PACOTE_PUBLICACAO_FASE1.md`. Não tocar nas campanhas da Zion Bubble. Pausar por critério de segurança pode ser proposto a qualquer momento (M83).
Ajustes de consistência sugeridos no mesmo arquivo (opcionais): em §6 "Criação de campanha", trocar "dentro do orçamento máximo do prompt" por "dentro do teto da sub-regra acima"; em §3 (status do ClickMax) acrescentar a data em que a B v3, o formulário e o obrigado forem publicados.

## 7. Riscos abertos
1. **Checkout nunca visto renderizado** (iframe bloqueado aqui): nome, descrição, capa e "Página de obrigado" só se provam no celular de Bruno e na compra de teste [NC].
2. **Ciclo compra → e-mail de acesso → login nunca provado** para esta oferta; a compra de teste prova ou reprova. A oferta não tem venda própria ainda (`hasTransaction` false). O gateway já vendeu R$ 97 em 24/11, então Pix funciona em geral [E, auditoria].
3. **Purchase no Meta:** 0 compras registradas nas vendas de 24/11 (sem UTM e, provavelmente, sem token) [E, auditoria]; se a compra de teste falhar em R1 a R4, a campanha de Purchase não é ativada e vale o plano B (seção 5.1, M84).
4. **`offers_update` em oferta `approved`** pode forçar nova revisão [NC] e `externalId`/listas vazias podem ser zerados por substituição total (mitigado com as 4 chaves extras, seção 4.1).
5. **v1 `/mini-mentoria` continua no ar** com "cadastre seu terreno no banco de áreas" até M85; usa o mesmo checkout (que passa a mostrar o nome e a descrição novos).
6. **Formulário da Sessão público** e **Sessão prometida** na landing, no carrossel e no checkout: exige responsável e prazo reais; fluxo de confirmação continua em rascunho.
7. **Conteúdo da turma** com Land Bank, envio de dados e "equipe Zion" (G2): se o patch não sair, o gasto não deve começar; Bruno decide se aceita o risco (reembolso em 7 dias não resolve LGPD).
8. **Amostra:** R$ 420 não prova nada estatisticamente; a Fase 1 é descritiva. Cartão não testado. Imposto, custos e reembolso sem valor.
9. **Artes:** cartões 2 e 6 do Carrossel C com imagens de origem não verificada; cartão 6 com "70 aulas" (M72); título da página no HTML publicado só se confere depois do M78.
10. **Conta de anúncios, Página, Instagram e pagamento do Meta** não confirmados por mim [NC]; o Windsor não cria públicos e pode não definir limite de gasto de campanha ou tags de URL (Gerenciador).
11. **`sellerStatus` pending** com `canSell` true: reconferir no dia da ativação.

## 8. O que dá para reverter e como (resumo)
| Item | Reversão |
|---|---|
| M73 nomes e títulos | repetir com os valores antigos (seção 3.2) |
| M74 formulário | `status: paused`; `successMessage` anterior |
| M75 obrigado | `pages_unpublish` |
| M76 oferta | payload de reversão (`CHECKOUT_LIMPO_MM47.md` §7) |
| M77 painel | reeditar nome; reenviar imagem; apagar o campo da página de obrigado |
| M78 B v3 | `pages_unpublish e0933e71…` |
| M79 rastreamento | desligar opção, remover token, religar interruptores (print do estado antes) |
| M80 compra de teste | reembolso |
| M81/M82 campanha | pausar; arquivar com novo "aprovado" |
