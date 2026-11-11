# Oferta de entrada do Zion Collection · decisão para rodar (10/11/2026)

## 1. A conta (premissas rotuladas)
- CPL real dos últimos 7 dias: R$ 5,82 (formulário Meta). 30 leads/dia = 900 leads e R$ 5.240 de mídia por mês.
- Premissa: taxas de checkout + impostos ≈ 12% do preço (ajustável).
- Referência de mercado para oferta de impulso: 2 a 5% dos leads compram (blogs de funil; direcional).

| Entrada | Líquido/venda | Equilíbrio só no front | Conv. 3% (27 vendas) | Conv. 5% (45 vendas) | Conv. 8% (72 vendas) |
|---|---|---|---|---|---|
| R$ 47 | R$ 41 | 14,1% dos leads | R$ 1.117 (−R$ 4.121) | R$ 1.861 (−R$ 3.377) | R$ 2.978 (−R$ 2.260) |
| R$ 97 | R$ 85 | 6,8% dos leads | R$ 2.305 (−R$ 2.933) | R$ 3.841 (−R$ 1.397) | R$ 6.146 (+R$ 908) |

Leitura: **a entrada não paga a mídia sozinha em nenhum preço realista.** A R$ 47 precisa de 14% de conversão; a R$ 97, de 7%. O clube de entrada é oferta de liquidação: serve para transformar lead em comprador e levar à sessão. A conta fecha no degrau seguinte.
- Back-end por 100 compradores (premissa): 10% fecham Master R$ 980 = +R$ 8.624 líquidos; 5% fecham Pro R$ 2.900 = +R$ 12.760. Somados, ≈ R$ 214 líquidos por comprador do clube, contra CAC de R$ 116 a 194. **É isso que fecha a conta.**
- Caminho alternativo a testar em paralelo: campanha de compra direta na landing (sem formulário). Premissa CPC R$ 1,50 e página convertendo 1 a 3% → custo por venda de R$ 50 a 150. A R$ 97 fecha no front a partir de 2% de conversão da página.

## 2. Decisão de preço
- **Entrada a R$ 97 (2x de R$ 48,50).** Está no limite superior da faixa de impulso, mas o líquido por venda e o equilíbrio (6,8%) são o dobro melhores que a R$ 47. Oferta de R$ 47 só como teste B se a conversão a R$ 97 ficar abaixo de 2% por 7 dias ou 100 cliques.
- Não anunciar "de R$ 270 por R$ 97" (preço "de" falso é proibido). O R$ 270 some da página de entrada.

## 3. O que o clube de entrada inclui (acesso completo ao degrau, sem metade de trilha)
Por R$ 97, acesso anual a: Trilha de Desenvolvimento completa (Marco Zero + 7 pilares, 43 aulas), planilhas e ferramentas de cada pilar, Dossiê do terreno, área de membros com masterclass ao vivo, sessão de direcionamento inicial (grátis na inscrição) e terreno inscrito no Land Bank.
Por que não travar metade da trilha: quem paga R$ 97 e encontra cadeado na aula 22 pede reembolso e não vai à sessão. A trilha 1 inteira é o produto da promessa "aprenda o passo a passo". O desbloqueio vem em cima, não dentro.

## 4. Escada de desbloqueios (o que se vende depois, sem mexer no que existe)
| Degrau | Preço | O que libera | Quando aparece |
|---|---|---|---|
| Ferramentas avulsas | R$ 19 a 27 | planilhas utilitárias do catálogo (já existem no ClickMax) | dentro da área de membros, por pilar |
| Módulos da Jornada de Gestão | R$ 47 cada | Marco Zero de Gestão, Finanças (prontos), próximos módulos | ao concluir a trilha 1 e na sessão |
| Master | R$ 980 (12x R$ 81,67) | trilhas de gestão, operação e vendas, aulas ao vivo | na sessão de direcionamento |
| Pro | R$ 2.900 (12x R$ 241,67) | tudo + acompanhamento semanal | na sessão, para quem tem recurso |
| Mentoria / parceria | sob análise | Zion no projeto | reunião com o Bruno |

## 5. A página de membresia de alta conversão (pesquisa + nossas regras)
1. Topo: frase do lead + "aprenda o passo a passo" + preço grande (2x de R$ 48,50) + botão. Cabe na tela do celular.
2. Prova real no primeiro scroll: operação desde 2020, fotos e vídeo. Sem depoimento inventado; quando houver membros falando, entram.
3. "O que tem dentro": os seis entregáveis em blocos, com imagem da área de membros, e **com que frequência entra conteúdo novo** (masterclass semanal, módulos novos ao longo do ano).
4. Sessão de direcionamento inicial em destaque como ganho da inscrição.
5. Tabela de níveis curta (Base agora; Master e Pro como próximos degraus), um botão por nível.
6. Objeções em 3 linhas: sem capital, terreno pequeno, só posse, não entendo de hotelaria, já tenho pousada.
7. Garantia real: reembolso em 7 dias (CDC). Pix e cartão. Acesso liberado após confirmação.
8. 300 a 500 palavras na versão de anúncio; um botão repetido três vezes, mesmo texto da arte.
9. Checkout em um passo, três campos, Pix.
10. Pixel + UTM por criativo; evento de compra na página de obrigado.

## 6. Para rodar hoje (ordem)
1. Bruno: link do Asaas "Inscrição Club Zion Collection · R$ 97 · 2x" com a tag LAND BANK | INSCRIÇÃO R$97 PAGA no webhook (o fluxo de liberação já existe).
2. Eu: troco o link na landing, publico a versão curta da página (anúncio) e deixo a longa como /zion-collection.
3. Bruno: formulário v2 com os gatilhos (producao/clube/FORMULARIO_META_GATILHOS.md).
4. Eu: anúncio pausado com carrossel campeão + card 8 → landing; conjunto B de compra direta → landing. Ativação com "aprovado" e teto diário.
5. Medir por 7 dias: CPL, conversão lead→compra, compra→sessão, sessão→Master/Pro. Decidir R$ 47 só com esses dados.

## Registro · 11/11/2026 (sessão de lançamento)
- Landing nova publicada em `docs/zion-collection/` (GitHub Pages, sem noindex), com filme oficial, tours, vídeo de 2 minutos e checkout `https://payments.clickmax.io/v_4pU5zNYj`.
- Vídeo 2 min: `docs/zion-collection-club/video/clube-2min.mp4` (16:9) e `docs/ads/clube-narrativa/clube-2min-4x5.mp4` (4:5). Narração provisória sintética; fonte em `producao/clube/video-2min/`.
- Criativos 1080×1350 na narrativa (espelho → crença → prova → mecanismo → próximo passo): `docs/ads/clube-narrativa/01..05.jpg`.
- Meta (conta 1271873041294684), tudo **pausado**: campanha `120250330194890016` → conjunto `120250331856590016` (R$ 30/dia, BR 25–65, mesmo público do Diagnóstico, visualizações da landing) → anúncio carrossel `120250331865540016` e anúncio de vídeo (id no resumo da sessão). Vídeo na conta: `1044832475285192`. Ativação só com "aprovado" de Bruno.
- Rota no site (zionhotelgroup.com/clube) ainda não existe: exige uma mensagem ao agente da Lovable (consome créditos). Aguarda aprovação.

### Atualização 11/11 · versão 2 (pedido do Bruno)
- Vídeo refeito: "como funciona o clube e as suas etapas", sem preço; o capital "pode vir da própria Zion ou do pool de investidores e parceiros". Arquivos substituídos nos mesmos caminhos. Vídeo na conta Meta: `4079419749029366`.
- Anúncios v1 renomeados como DESCARTADO (ids `120250331865540016` e `120250331873620016`), continuam pausados. Novos anúncios, pausados, no mesmo conjunto `120250331856590016`: carrossel v2 `120250331912530016` e vídeo v2 (id no resumo da sessão).
- Copy dos anúncios: "Transforme seu terreno em um destino turístico. Aprenda o passo a passo com a Zion…", com "melhores produtos do mercado" e "referência" por decisão do Bruno.

### Atualização 11/11 · versão 3 (aprovada pelo Bruno: "agora ficou bom")
- Vídeo v3 (71 s, dor e troféu, sem preço) nos mesmos caminhos; vídeo na conta Meta `1805169497317625`.
- Anúncios v3, pausados, no conjunto `120250331856590016`: carrossel `120250331969970016` e vídeo `120250331971600016`. v1 e v2 renomeados DESCARTADO.
- Textos com "acesso a investimentos", "melhores produtos do mercado", "referência" e "maior clube de glamping do Brasil" por decisão do Bruno.
