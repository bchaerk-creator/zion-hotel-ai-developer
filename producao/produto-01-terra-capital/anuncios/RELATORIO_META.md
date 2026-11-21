# Relatório de configuração Meta · Produto 01 (21/11/2026)

**Estado: preparado, NADA criado no Meta.** Não alterei campanhas existentes, não publiquei anúncios e não iniciei gasto (R$ 0). Os parâmetros estão prontos em `meta_payloads.json` (tudo `paused`) e os criativos, copies e vídeo estão prontos. A criação dentro do Meta ficou parada por bloqueios que só você resolve (seção 6); fazer só a casca da campanha agora deixaria objetos incompletos na conta.

## 1. O que foi entregue
| Item | Onde |
|---|---|
| 6 anúncios 1080×1350 (um card = um anúncio) | `dist/feed/` |
| 6 adaptações 9:16 (Stories/Reels), card inteiro, sem esticar nem cortar, topo e base livres para a interface do Meta | `dist/stories/` |
| Vídeo vertical de 30 s (dor 0–5 s, demonstração real 5–20 s, entregáveis 20–27 s, chamada 27–30 s), silencioso, com texto na tela | `dist/video/reels_30s_1080x1920.mp4` |
| Card 04 com a **ferramenta real** no lugar da tela ilustrada | `dist/feed/anuncio_04_*` (captura em `src/tela-real-notebook.png`) |
| Copies, título, descrição e UTM por anúncio | `COPIES.md` |
| Parâmetros prontos de campanha, 3 conjuntos e 7 anúncios | `meta_payloads.json` (gerado de `anuncios.json`) |
| Testes | `tests/anuncios.test.js`: 13 ok, 0 falhas (medidas, termos proibidos, UTMs únicas, orçamento 40/40/20, tudo pausado) |
Os arquivos já estão no site em `docs/p/adbc67069af26ae0/terra-capital/anuncios/` (URL pública só depois do merge, necessária para o Meta buscar as imagens).

## 2. Ajustes feitos nos criativos (e por quê)
Li `PROMPT_E_ESTRATEGIA.md` por inteiro. Logo e design oficiais preservados; só troquei texto onde a política do Meta ou as regras do repositório pediam.
| Card | Texto original na imagem | Problema | Versão usada |
|---|---|---|---|
| 01 | "Você tem um terreno, mas falta capital?" | Afirma/insinua condição financeira pessoal (política de atributos pessoais do Meta) | "Tem um terreno em destino turístico? Aprenda a planejar o projeto." |
| 02 | "Sua matrícula pode ser a ponte para o seu próximo negócio." | Sugere resultado | "Documentação, riscos e alternativas: organize antes de decidir. Material educativo. Não é oferta de crédito." |
| 03 | "Você entra com a terra. Como encontrar quem entre com o capital?" | Afirma posse do terreno e sugere achar investidor | "Uma proposta clara para potenciais parceiros." |
| 04 | "Quanto dinheiro você precisa…?" + tela com R$ 780.000, faturamento e payback de 3,6 anos | Números ilustrativos que parecem resultado | Título neutro + **tela real** da ferramenta (R$ 200.000 de lacuna, dados fictícios, com faixa "Exemplo com dados fictícios") |
| 05, 06 | — | Sem problema de texto | Mantidos |
Todos levam "Imagem ilustrativa" no canto: as fotos dos cards são imagens geradas (incluindo as pessoas) e **não** são fotos da Zion; as copies não as apresentam como clientes, equipe ou caso real.
Nome do produto nas copies: troquei "mini mentoria" por "jornada", como na landing.
**Ponto que não consegui corrigir:** o card 02 mostra um documento "Matrícula de imóvel" com brasão, que imita documento oficial (imagem gerada). Pode gerar revisão. Recomendo trocar a arte; enquanto isso, o card 02 é o primeiro a deixar de fora se o Meta recusar.

## 3. Políticas verificadas (fontes do Meta, leitura de hoje)
- **Atributos pessoais:** anúncios não podem afirmar ou insinuar atributos da pessoa, incluindo situação financeira. Motivo dos textos neutros acima. Fonte: Meta, "Violações de privacidade e atributos pessoais".
- **Produtos e serviços financeiros:** em 14/01/2025 a categoria especial `FINANCIAL_PRODUCTS_SERVICES` substituiu a de crédito; ela restringe segmentação (e lookalike). A autoidentificação é exigida para anunciantes dos EUA, Canadá e partes da Europa; **Brasil não aparece na lista que li**, e não achei exigência específica para o Brasil. Fonte: documentação de desenvolvedores do Meta e Padrões de Publicidade.
- **Minha leitura (não é garantia):** o Produto 01 é **educacional**, não oferece crédito, então **não declarei categoria especial**. O Meta pode classificar diferente na revisão. Se isso acontecer, a segmentação por lookalike e idade fica limitada e o plano vira Advantage+ aberto + remarketing. **Confirme no Gerenciador/Business Manager** (Brasil e verificação de anunciante) antes de ativar.
- Exemplos de "regra do anúncio" que respeito: sem crédito garantido, sócio ou retorno garantido; sem depoimento; sem dado patrimonial ao Meta.

## 4. Auditoria da conta Zion Collection 2 (`1271873041294684`, somente leitura)
- **Existe uma campanha ATIVA gastando:** "[LAND BANK][LEADS][FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO] [03/11]" (conjunto "BRASIL · Investidor/Empresário 25-65 · Diagnóstico" ativo; R$ 623,35 nos últimos 30 dias). O `CLAUDE.md` diz "campanhas só pausadas, teto R$ 0". **Não toquei**; se esse gasto não foi autorizado por você, vale pausar. As outras 13 campanhas dos últimos 30 dias estão pausadas.
- **Sobreposição de público:** os conjuntos existentes usam "Investidor/Empresário 25-65"; o remarketing vai alcançar parte do mesmo público. O Produto 01 foi desenhado com exclusão de compradores.
- **Públicos existentes (ids lidos de um conjunto de remarketing):** Público Zion 90 `120250455830270016`, Público vídeo `120250455897500016`, Zion collection 365 `120250455931010016`. Já usados no remarketing do Land Bank; confirme que a origem das listas é autorizada (LGPD).
- **Página usada nos conjuntos existentes:** `576944608845537` (consta no Windsor como "Zion Glamping Collection"). Confirme se é a página certa para este anúncio.
- **Pixel:** nenhum conjunto da conta otimiza por conversão, então não há pixel para reaproveitar na conta. O pixel `903918118859018` citado em docs do repositório é de outro contexto. **Preciso do id confirmado.**
- **Permissões da ferramenta (Windsor):** cria e pausa campanhas, conjuntos e anúncios; **não** lê pixels, públicos, identidades verificadas nem cria públicos lookalike; `create_ad_image` exige upload manual (usarei `image_url` pública).

## 5. Estrutura proposta (R$ 100/dia, sujeita a "aprovado")
Campanha de **Vendas** · site · evento **Purchase** · destino: landing + checkout ClickMax (sem formulário) · posicionamentos Advantage+ · botão "Saiba mais" · atribuição 7 dias clique + 1 dia visualização.
| Conjunto | Público | Orçamento | Observação |
|---|---|---|---|
| Lookalike 1% | Semelhante a leads qualificados (fonte a definir) | R$ 40 | Só se elegível e se houver fonte com volume; **não identifiquei a lista de "leads qualificados"** |
| Aberto Advantage+ | Brasil, 25–55 sugerido | R$ 40 | Meta amplia o público |
| Remarketing | Os 3 públicos existentes | R$ 20 | Leads, visitantes e engajados |
Exclusão em todos: compradores do produto (público a criar depois da 1ª venda). Os 6 anúncios + o vídeo entram em cada conjunto.
**Alerta de volume (importante):** com CPA alvo de R$ 20–30, R$ 100/dia gera cerca de 3 a 5 compras por dia no total, ou 1 a 2 por conjunto. Isso é pouco para o Meta otimizar por Purchase em três conjuntos ao mesmo tempo (a referência usual é algo como 50 conversões por semana por conjunto). **Recomendo simplificar:** Fase 1 só com Aberto Advantage+ (R$ 70) + remarketing (R$ 30), ou testar um conjunto por vez. Decisão sua.
**Teste de preço (fase 2):** só depois de escolher criativo. A/B do Meta com dois conjuntos iguais, um para a página A (R$ 47) e outro para a B (R$ 67), mesmos entregáveis. Medir por receita líquida por real investido, não só por conversão.
**Meta de CPA vs. economia:** com R$ 47 e 150 compradores/mês, o CPA máximo que paga os fixos é R$ 29,95 (R$ 46,95 com R$ 67). Abaixo de ~75 compradores/mês os fixos de R$ 1.500 não fecham em nenhum dos preços (tabela em `../OFERTA.md`). O CPL de R$ 7 não é CPA. Taxa de clique→compra necessária = custo por clique ÷ CPA (exemplo hipotético: clique de R$ 1 e CPA de R$ 30 exigem 3,3%; o custo por clique real é desconhecido).
Sugestão de parada (proposta, não regra do Meta): pausar um conjunto que gaste R$ 90 (3× o CPA alvo) sem nenhuma compra confirmada; revisar semanalmente.

## 6. Bloqueios para criar no Meta (preciso de você)
1. **"Aprovado"** para criar a campanha em rascunho (pausada) e para o orçamento.
2. **Pixel de Purchase** confirmado (e conta correta).
3. **Landing no ar:** as páginas A/B estão em rascunho no ClickMax; enquanto não forem publicadas, o anúncio não tem destino válido. Isso depende de: merge da branch na `main` (imagens e vídeo públicos), conta de vendedor ClickMax `pending`, oferta aprovada e `active`. O Meta também não revisa direito um destino que não abre.
4. **Página do Facebook** confirmada (`576944608845537`?) e, se o Meta exigir, **identidade verificada** do anunciante (ids do Business Manager).
5. **Fonte do lookalike** (lista de leads qualificados) e **público de compradores** para exclusão: criar no Gerenciador (a ferramenta não cria públicos).
6. **Conversions API:** token e configuração; evento de compra só depois de pagamento confirmado Asaas/ClickMax (modelo e testes em `../RASTREAMENTO.md`).
7. Decidir sobre os dois pontos de risco: card 02 (documento) e classificação de categoria financeira.

## 7. Rastreamento e conciliação (estado real)
Pixel, CAPI, webhooks, pagamentos Asaas, conciliação e deduplicação **não foram validados com eventos reais** (não há compra possível ainda). Estão especificados e testados em modelo (`../RASTREAMENTO.md`, 11 testes). UTM por anúncio: `utm_source=meta&utm_medium=paid&utm_campaign=p01_terra_capital&utm_content=<criativo>&utm_id={{campaign.id}}&utm_term={{adset.name}}`; versão de preço pela página (A47/B67) e pela oferta. Eventos: ViewContent, InitiateCheckout, Purchase só com pagamento confirmado, `event_id` = `p01_terra_capital:purchase:<paymentId>`. Nada de dado financeiro ou patrimonial vai ao Meta.

## 8. Passo a passo depois do "aprovado" (eu executo)
1. Substituir os marcadores `<...>` em `meta_payloads.json` (pixel, campanha, públicos).
2. `create_campaign` → `create_adset` (um por vez) → `create_ad_video` + `create_ad` (7 anúncios), tudo pausado; conferir no Meta.
3. Você revisa as prévias no Gerenciador. Só com novo "aprovado": ativar conjunto a conjunto (a ferramenta mostra uma prévia e pede confirmação antes de qualquer item que gaste).
