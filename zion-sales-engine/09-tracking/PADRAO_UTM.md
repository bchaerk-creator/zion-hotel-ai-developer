# PADRÃO ÚNICO DE UTM, `sck` E IDS · ZION SALES ENGINE

Versão 1 · 25/11/2026 · Fonte única (A09 da auditoria da Fase 03). Todos os outros arquivos (criativos, A/B, handoff, tracking, funis) apontam para cá. Se houver divergência, vale este arquivo.

## 1. Regra de ouro
A URL do anúncio tem **duas partes que nunca se misturam**:
1. **URL de destino**, sem nenhum parâmetro e sem `#pagar`: `https://infoprodutos-zion.clickmax.space/mini-mentoria` (ou `-a`/`-b` no teste).
2. **Tags de URL** (`url_tags`), coladas **uma vez**, no campo "Parâmetros de URL" do anúncio no Gerenciador do Meta.

Colar a UTM na URL de destino **e** nas tags de URL duplica os parâmetros. Por isso `COPIES.md` e `manifesto.json` trazem a URL só de destino e o texto das tags em campo separado.

## 2. Texto das tags de URL (colar exatamente assim; o Meta preenche as `{{ }}`)
```
utm_source=meta&utm_medium=paid&utm_campaign=mm47&utm_content=<id do criativo>&utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}&adset_id={{adset.id}}
```

| Chave | Valor | Observação |
|---|---|---|
| `utm_source` | `meta` | fixo |
| `utm_medium` | `paid` | fixo |
| `utm_campaign` | `mm47` | **fixo para todos os anúncios da Mini Mentoria R$ 47; nunca muda entre criativos nem entre variantes**. Outro produto usa o próprio slug (ex.: `mm97` só se existir oferta separada). `CLAUDE.md` §6 diz `<produto>`: aqui, produto = `mm47` |
| `utm_content` | `<id do criativo>` | ex.: `mm47f3-c03-custo-escondido`. É o id do arquivo da arte |
| `utm_term` | `{{ad.id}}` | id do anúncio (macro do Meta) |
| `sck` | `{{campaign.id}}` | id da campanha, no campo `sck` que o ClickMax grava na venda |
| `ad_id`, `campaign_id`, `adset_id` | macros do Meta | gravados só se o ClickMax os guardar [NC: se aparecem como campo próprio na venda ou só dentro da URL] |

Não existe `src` nas tags de anúncio. `src` é do canal de mensagem (seção 5).

## 3. Variante de landing no teste A/B: **uma escolha só**
**Decisão: sufixo no `utm_content`: `<id do criativo>-varA` ou `<id do criativo>-varB`.** A chave `utm_variant` fica **descartada**; `utm_term` **não** carrega a variante.

Por quê:
1. `utm_content` é um campo que o ClickMax grava e exporta na venda [E]; uma chave nova como `utm_variant` pode não ser gravada [NC] e a venda perderia a variante.
2. `utm_term` precisa continuar sendo o id do anúncio, que é a chave de ligação com o Meta (conciliação R7).
3. O id do criativo continua legível no começo do valor: separar por prefixo é simples (`utm_content` termina em `-varA` ou `-varB`).
4. Como cada variante é um **anúncio separado** (destino `-a` ou `-b`), o `ad_id` também separa as variantes: segunda checagem, sem custo.

Exemplo A: destino `…/mini-mentoria-a`, tags com `utm_content=mm47f3-c08-oferta-47-varA`.
Exemplo B: destino `…/mini-mentoria-b`, tags com `utm_content=mm47f3-c08-oferta-47-varB`.
Fora do teste A/B, o `utm_content` não leva sufixo.

## 4. Antes do `#`
Parâmetros ficam **antes** de qualquer `#`. Depois do `#` o navegador não os trata como query. O destino do anúncio não usa `#pagar`.

## 5. Canais que não são anúncio
Mensagens de WhatsApp/Bela e e-mail: `utm_source=<canal>&utm_medium=<tipo>&utm_campaign=<fluxo>&utm_content=<mensagem>&src=<canal_origem>`. Isso grava a origem do **canal**; não atribui o anúncio original. Compra de teste: `utm_source=teste&utm_medium=manual&utm_campaign=mm47&utm_content=checklist`.

## 6. Consolidação do R$ 97
Anúncio que passar a apontar para `/mini-mentoria` usa o mesmo padrão (`utm_campaign=mm47`), não `mini-mentoria`.

## 7. Aceite
Uma compra de teste pelo link de um anúncio de teste deve gravar na venda `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` e `sck` (conferir com `sales_get_utms`). Sem isso a venda não é atribuível e o CPA é só limite superior.

## 8. Acréscimos P0 (25/11/2026): criativo, variante e seção da página (não quebram o padrão acima)
O padrão das seções 1 a 7 continua valendo sem mudança. Os acréscimos abaixo são **regras de preenchimento**, não chaves novas.

**`utm_content` = `<criativo>-<variante>`** (a variante é do criativo/promessa, não da página):
- `<criativo>` = id do arquivo da arte ou vídeo (ex.: `mm47f3-c03-custo-escondido`).
- `-varA` / `-varB` (seção 3) = **variante de landing** no teste A/B. Quando o criativo também tem variantes de texto/promessa, use `-v1`, `-v2` **antes** do sufixo de landing: `mm47f3-c03-v2-varB`. Ordem fixa: `criativo` `-v<n>` (opcional) `-varA|varB` (opcional). Nada de espaço, maiúscula ou acento.
- Formato de vídeo/carrossel: o sufixo de formato vai no id do criativo (`...-vid`, `...-car`), nunca em outra chave.

**Parâmetro de página/seção: só se fizer sentido, e por âncora, não por chave nova.**
- Quando o destino do anúncio é uma seção específica (ex.: a oferta), use a **âncora depois da query**: `https://.../mini-mentoria?utm_...#oferta`. A âncora **não** vai ao servidor nem ao ClickMax; ela só rola a página [H]. Serve para o visitante cair no ponto certo, **não** para medir. Para medir, veja `FUNIL_DE_EVENTOS_P0.md` (clique no CTA e visualização da oferta por elemento marcado).
- Se um dia for preciso gravar a seção na venda, a chave seria `utm_term` ou `utm_content`? **Não**: ambas já têm dono (ad id e criativo). Uma chave nova (`sec=`) só entra se a venda a gravar [NC: testar com compra de teste] e **só depois de Bruno aprovar**. Hoje: **não use**.
- Padrão de quem **não** vem de anúncio mas passa pela oferta (ex.: botão de e-mail ou WhatsApp para a oferta): `utm_source=<canal>&utm_medium=<tipo>&utm_campaign=mm47&utm_content=<mensagem>-oferta` (o `-oferta` no fim do `utm_content` diz que o link já cai na seção da oferta).

**O que dá para obter SEM script (nada instalado):** [E = documentação lida; NC = a confirmar na compra de teste]
| Dado | Sem script | Limite |
|---|---|---|
| UTM, `sck`, ids na venda | O ClickMax grava a URL do momento em que o checkout abre; os parâmetros precisam estar na URL da página nessa hora [E/A] | Se o visitante sai e volta por link sem UTM, perde (por isso o snippet é proposta) |
| Origem da visita (canal, utm) em análises | `visitors_analytics` e `visitors_attribution` agrupam por canal e UTM; o canal usa a **primeira sessão** do visitante [E] | Depende da UTM estar na URL da primeira visita |
| Clique em CTA | O ClickMax mede `button_click` com o `elementId` do botão nas páginas publicadas, sem instalar nada [E]; os CTAs da página aparecem no mapa de gatilhos com `button_click` [E] | O dado fica no ClickMax (visitantes/funil), **não** vai ao Meta como evento próprio [NC se aparece por CTA nos relatórios] |
| Visualização da oferta | Marcar a seção com `data-cx-track="visible"` gera `element_visible` com o id do elemento [E, SDK]; ou usar página separada de oferta marcada "Página de conteúdo" (ViewContent) [E] | Se o importador de página mantém o atributo: [NC] |
| `fbc`/`fbp` | O ClickMax completa a CAPI com o clique no anúncio que o contato tem [E] | Quando a compra volta sem clique registrado, fica sem |
| Persistência entre sessões e aparelhos | Não há | Só o snippet (mesmo navegador) ou o lead identificado no ClickMax (e-mail) resolvem; entre aparelhos só com identificação |

`snippets/persistir-utm.js` continua **proposta, não instalada** (aprovação de Bruno, aviso de privacidade atualizado, teste em página de teste). O padrão de UTM acima funciona sem ele.

## 9. Funil híbrido (25/11/2026): `utm_campaign` por CAMINHO, `utm_content` por criativo, coorte por etiqueta
**Esta seção atualiza as seções 2, 3 e 6 para o funil de dois caminhos e vale sobre elas onde houver conflito.** Motivo: `lead_comprador.py` precisa separar **captação, venda quente e venda fria** só pela UTM, e hoje `utm_campaign=mm47` não separa nada. O produto deixa de ir na UTM enquanto houver **um** produto anunciado (a venda já diz a oferta: `offerId`).

| Chave | Valor | Quando |
|---|---|---|
| `utm_source` | `meta` | todo anúncio. No formulário nativo do Meta o ClickMax grava `facebook` [E, leitura de contatos recentes]: aceitar os dois como Meta |
| `utm_medium` | `paid` (venda) · `lead_ads` (captação por formulário nativo) | fixo |
| `utm_campaign` | **`captacao`** · **`venda-quente`** · **`venda-fria`** | **caminho**, nunca o nome do produto nem da campanha. Vale o mesmo valor em todas as campanhas daquele caminho |
| `utm_content` | `<id do criativo>` (sem espaço, maiúscula, acento nem `|`), mais `-v<n>`/`-varA|varB` do §8 | ex.: `mm47-c03-custo-escondido-vid` |
| `utm_term` | `{{ad.id}}` | venda (site). Na captação por formulário nativo vem o texto que o ClickMax grava [E]: ver abaixo |
| `sck` | `{{campaign.id}}` | venda (site) |

### 9.1 URLs de tags (venda quente e venda fria; colar uma vez no anúncio, sem repetir na URL de destino)
```
venda quente: utm_source=meta&utm_medium=paid&utm_campaign=venda-quente&utm_content=<criativo>&utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}&adset_id={{adset.id}}
venda fria  : utm_source=meta&utm_medium=paid&utm_campaign=venda-fria&utm_content=<criativo>&utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}&adset_id={{adset.id}}
```
**Captação (formulário nativo do Meta):** o ClickMax **não usa as tags de URL**; ele grava o **nome da campanha** em `utm_campaign` e o **nome do anúncio** em `utm_content` [E: contato recente: `utm_campaign` = nome da campanha, `utm_content` = nome do anúncio, `utm_medium=lead_ads`, `utm_source=facebook`]. Portanto, para a captação, **o padrão é de nomenclatura no Meta**:
- **Nome da campanha** de captação = `captacao | AAAA-MM-DD` (o `captacao` no início; a data é a de criação/coorte).
- **Nome do anúncio** = `<id do criativo>` no mesmo formato do `utm_content` (ex.: `mm47-c03-custo-escondido-car`).
- Renomear no Meta **depois** de gerar leads quebra a ligação (o lead guarda o nome antigo). Crie campanha/anúncio **novos** com o nome certo; **não renomeie** os existentes. [H: o ClickMax copia o nome no momento do envio do lead.]
- Enquanto os nomes antigos existirem (ex.: `ZC2 | INSCRICAO 270 | CARROSSEL C | ...`), `lead_comprador.py` aceita o `utm_content` como está; o `captacao` só é exigido nas campanhas novas.

### 9.2 Etiquetas de coorte (CRM)
Uma etiqueta por **data de entrada e caminho**: `COORTE | AAAA-MM-DD | captacao`. Aplicar:
- **Retroativa, sem automação:** `tags_batch_apply_to_leads` com os leads do filtro `createdAt` do dia e `utmCampaign` da captação (escrita no CRM: **"aprovado" de Bruno**).
- **Daqui em diante:** passo do fluxo de boas-vindas **em rascunho** (nada ativado sem aprovação).
- A coorte também sai **sem etiqueta**, pelo filtro `createdAt` (é o que `lead_comprador.py` usa); a etiqueta serve para exclusão e segmentação (`ARQUITETURA_DE_PUBLICOS.md`).
- A etiqueta existente `INSCRIÇÃO 270 | LEAD DO FORMULÁRIO` é **por formulário** (nome legado "270"): não é coorte.

### 9.3 Lacunas lidas em 25/11/2026 que impedem hoje medir CPL por criativo e coorte (e o que fecha cada uma)
| # | Lacuna [E = lido nesta sessão] | Efeito | Correção |
|---|---|---|---|
| 1 | O lead grava **nomes**, sem id de campanha, conjunto ou anúncio; `src` e `sck` vazios [E] | Ligação com o gasto do Meta só **por nome** | Nomenclatura do §9.1; ligar por nome com conferência de duplicidade |
| 2 | Nome de anúncio **repetido com ad_id diferente** na conta (ex.: o mesmo anúncio em dois conjuntos) [E, Windsor] | Gasto/leads de dois anúncios se misturam por nome | Nome único por anúncio **dentro da campanha**, ou somar os dois ids de propósito |
| 3 | Na campanha "Form R$47 direto" o `utm_campaign` gravado (`FORM R$47 DIRETO`) **não é igual** ao nome da campanha no Meta [E] | Join por nome falha nessa campanha | Pelo §9.1, nome de campanha novo = `captacao | data`; para a antiga, de-para manual |
| 4 | `utm_campaign` mistura **nomes e ids numéricos** em contatos antigos [E, lista de valores] | Agrupar por campanha exige normalizar | Só dados novos; não retrabalhar o histórico |
| 5 | Origem do contato é `CxExternalPages`, não `MetaLeadAds` [E] | Não dá para isolar leads de anúncio por origem | Filtrar por `utm_medium=lead_ads` + `utm_campaign` |
| 6 | **Sem etiqueta de coorte**; a etiqueta existente é por formulário [E] | Coorte só pelo filtro de data | Etiqueta do §9.2 (opcional) |
| 7 | `leads_export_csv` **não tem colunas de UTM** [E] | Export em massa perde criativo | Um export por criativo (filtro `utmContent`) ou leitura por `leads_get` |
| 8 | O formulário nativo do Meta **não aparece** em `forms_list` (só formulários próprios do ClickMax) [E] | `forms_submissions_list` não serve para esses leads | Medir por contato (tag/UTM), não por formulário |
| 9 | Contato de captação com `lgpdApproved=false` e `emailConsent` vazio, mas preferências de mensagem todas **ligadas** por padrão [E, contato recente] | Consentimento não registrado: afeta público personalizado e disparos | Textos separados de consentimento (comunicação × publicidade) **antes** de usar a base; ver `ARQUITETURA_DE_PUBLICOS.md` §4 |
| 10 | As vendas reais de 24/11 vieram **sem UTM** [E, auditoria] | Compra sem origem: "não atribuída" | Só com UTM na venda (compra de teste, §7) ou lead por e-mail |
