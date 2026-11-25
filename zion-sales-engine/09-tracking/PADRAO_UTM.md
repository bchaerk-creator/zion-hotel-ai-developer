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
