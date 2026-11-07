# Zion Arsenal · ponto de retomada (06/11/2026)

## Pronto e testado
- Motor interativo `app/engine.js` + 20 mini mentorias `app/products/A01..B10.js` (40 telas, 7 pilares, 7 exercícios cada).
- `node tests/run.js all` → 20/20 produtos, 1.196 checks ok (3 perfis por produto, valores conferidos à mão, PDF, mobile, persistência).
- ClickMax (projeto Infoprodutos Zion): 19 produtos novos A02–B10 a R$ 27 (IDs em `control/clickmax.json`); A01 pré-existente reaproveitado, sem alterações.
- Rascunhos ClickMax: landing `/zar-a02` (checkout vinculado) e vitrine `/zion-arsenal`.
- Demo em vídeo real: `node tests/demo.js A02` (gera 9:16 e 4:5).

## Decisões de Bruno
- Hospedagem das ferramentas: GitHub Pages em `docs/p/adbc67069af26ae0/<produto>/`. O import via MCP da ClickMax remove JavaScript (testado e despublicado).
- Meta Ads: conta Zion Collection 2 (campanhas só pausadas).

## Próximos passos
1. Esclarecer a correção "Zion Arsenal → Zion Collection" (onde aplicar).
2. Ajustar `app/engine.css` e as landings às cores oficiais do CLAUDE.md (#040605, #1B2117, #FEF5F0, #DED6BF, #8B714E, #C9B37E; Cormorant + Jost) e dar cor explícita aos spans.
3. Publicar as 20 ferramentas em `docs/p/adbc67069af26ae0/zar-xxx/` (`scripts/bundle.js`) e ligar as entregas (`offers_add_link_delivery`).
4. 18 landings restantes, área de membros, funis, automações, criativos, e-books, Gamma, campanhas pausadas.
5. Vendedor ClickMax ainda em análise: nenhum checkout vende.
6. Apagar a página técnica `/zar-teste-script` (rascunho, despublicada).
