# ZC2 · Vendas para públicos quentes e remarketing: plano e pendências (27/11)

Comando oficial "ZION COLLECTION 2". Conta `1271873041294684`, página `576944608845537`.
**Nada foi criado no Meta.** O próprio comando manda registrar a pendência e não improvisar quando um requisito essencial não puder ser validado. Dois estão nesse caso (itens 1 e 2 abaixo).

## Pendências que travam a criação
1. **O evento Purchase não chega ao Meta.** O checkout ClickMax/Ticto não carrega pixel (`fbq` indefinido) e houve 0 Purchase em 14 dias (ver `RASTREAMENTO_AUDITORIA.md`). Uma campanha de Vendas otimizada para Purchase, hoje, otimizaria para um evento que não existe. Para destravar: Etapa B (pixel + token da CAPI no painel do ClickMax, preenchidos pelo Bruno) e Etapa C (teste de compra autorizado).
2. **Não consigo ler as regras dos públicos.** O conector Windsor (`list_audiences`) confirmou 13 públicos (11 personalizados, 1 lookalike, 1 salvo), mas não devolveu regra, origem nem retenção. Sem isso não dá para separar "abriu o formulário" de "enviou o formulário" (Conjunto A), nem confirmar a sobreposição entre "Público Instagram" e "Zion Collection 365". Para destravar: prints de cada público no Gerenciador (Públicos → clicar no nome → aba de detalhes/regra).
3. **Não existe público de compradores para excluir.** Sem Purchase no pixel, não há como criar `ZC2 | PURCHASE | 180D`. Alternativa: lista de clientes exportada do ClickMax (exige base legal e autorização de uso; LGPD).
4. **InitiateCheckout no pixel `903918118859018`:** 149 eventos e 0 compras. É preciso conferir onde ele dispara. Se disparar na landing, o público "CHECKOUT 7D/30D" fica errado.
5. **Pixel padrão:** falta a escolha do Bruno entre o `903918118859018` (o único nos conjuntos desta conta) e o `1378530017570073` (o do site da Lovable).
6. **Teto de anúncio (CLAUDE.md):** venda quente e remarketing estão em R$ 0 até o Bruno aprovar um valor. O teto atual de R$ 30/dia vale só para a venda fria.
7. **Camila** aparece no V12b, no V14 e no V15: falta a autorização de imagem registrada.

## Estrutura pronta para criar (pausada) assim que 1 e 2 forem resolvidos
Todas as campanhas: objetivo Vendas, conversão no site, evento Purchase do pixel escolhido, Brasil, posicionamentos automáticos, Advantage+ público **desligado** (`advantage_audience=false`: o público personalizado é aplicado exatamente, sem expansão), orçamento por conjunto, destino `https://www.zionhotelgroup.com/inscricao` (landing da Plataforma R$ 47, adesão inicial) e UTMs:
`utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign={{campaign.id}}&utm_content={{ad.id}}&utm_term={{adset.id}}&utm_placement={{placement}}`
(a landing já repassa utm_* ao checkout; o ClickMax grava source/medium/campaign/content/term; `utm_placement` não é gravado na venda).

| Campanha | Conjunto | Públicos incluídos | Excluídos | Vídeos (narrativa) | Orçamento proposto |
|---|---|---|---|---|---|
| ZC2 \| VENDAS \| PÚBLICO QUENTE \| NOVOS VÍDEOS | Quente | Top Collection campeão `120250592796030016`, Collection campeão `120250592617440016`, Público Zion 90 `120250455830270016`, Base Zion Meta Email `120248288038180016` (se a origem e a autorização forem confirmadas) | compradores (pendente) | V17C (oferta direta), V18B | 50% |
| ZC2 \| VENDAS \| REMARKETING \| NOVOS VÍDEOS | A · Formulário | "Look a like formulário" `120250593835770016`, "Público similar personalizado" `120250592781330016` (**só depois de ver as regras**) | quente + compradores | V06, V17 longo sem a frase de investimento | 35% (A+B+C) |
| | B · Vídeo | Público vídeo novo `120250592676910016`, Público vídeo antigo `120250455897500016` | quente, A, compradores | V17C, V19B | |
| | C · Instagram | Público Instagram `120250592672940016` + Zion Collection 365 `120250455931010016` (juntos num conjunto só, porque têm o mesmo tamanho; confirmar se são o mesmo público) | quente, A, B, compradores | V17C, V12b/V14/V15 (só com autorização da Camila) | |
| ZC2 \| VENDAS \| LOOKALIKE TOP COLLECTION 1% | LAL 1% | Lookalike verdadeiro 1% `120250593921040016` (Brasil) | todos os personalizados acima + compradores | V17C, V18B, V19B | 15% |

Nome dos anúncios: `ZC2 | VENDAS | Vxx | NARRATIVA | PÚBLICO`.

**Sobre o orçamento:** os públicos quentes têm menos de 1.000 pessoas cada. Com essa base, uma diária acima de uns R$ 10 a R$ 15 tende a subir a frequência muito depressa. Recomendação inicial, quando aprovada: quente R$ 10/dia, remarketing R$ 7/dia, lookalike R$ 3/dia = R$ 20/dia. Isso **depende do "aprovado" do Bruno**, porque hoje esse teto é R$ 0.

## Públicos do pixel (seção 6), para criar depois que os eventos forem validados
`ZC2 | WEB | 7D/30D/90D` (PageView), `ZC2 | VIEW CONTENT | 30D`, `ZC2 | CHECKOUT | 7D/30D` (InitiateCheckout, só depois do item 4), `ZC2 | PURCHASE | 180D | POR PRODUTO` (só depois do item 1). A jornada de recuperação (24 h, 1-3 d, 4-7 d, 8-14 d, 15-30 d) usa essas janelas com exclusão em cascata. O Meta não garante a ordem de entrega.

## Vídeos disponíveis (já no Meta)
V17C `1758647026274663`, V18B `1701692388059393`, V19B `1166490412530693`, V12b `1474732087451477`, V14 `1731308185237106`, V15 `2731168944058732`, V17 longo `992717273453223`, V06 `2410954612991521`. Narrativas e riscos em `NARRATIVAS.md`.
