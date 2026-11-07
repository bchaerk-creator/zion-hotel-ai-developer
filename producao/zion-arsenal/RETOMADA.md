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

## Atualização 07/11/2026
- Paleta e fontes oficiais aplicadas (1.196 testes continuam ok).
- 20 ferramentas publicadas e verificadas no ar (20/20): `docs/p/adbc67069af26ae0/zar-a01..zar-b10/`.
- Entregas por link ligadas nas 19 ofertas novas (A02–B10). A01: oferta antiga mantida com a entrega `arsenal-01` (trocar só com aprovação).
- Bloqueio restante das ofertas: apenas `sellerStatus`.

## Nome (07/11/2026)
- Novo nome: **Zion Collection Club**, slogan **Hotel Business Academy** (substitui "Zion Arsenal"). Aplicado nas 20 ferramentas, nas 19 ofertas/produtos, na landing do A02 e na vitrine (agora `/zion-collection-club`). Códigos internos ZAR-xxx e pastas `zar-xxx` mantidos.

## Tutoriais e bônus (07/11/2026)
- 20 tutoriais narrados (voz Piper pt-BR + cursor, ~2min10s cada) em `docs/p/adbc67069af26ae0/tutoriais/zar-xxx-tutorial.mp4`.
- Tutorial anexado às 21 aulas de bônus e acrescentado como 2ª entrega nas 19 ofertas novas.
- Bônus nas 5 trilhas: Desenvolvimento (módulo 9 da Trilha 1, 11 aulas) e cursos de bônus de Gestão, Operação, Aceleração de Vendas e Identidade e Branding (sem turma ainda). IDs em `control/clickmax.json`.

## Landings (07/11/2026)
- 19 landings simples (6 blocos) em rascunho no ClickMax, `/zar-a02` … `/zar-b10`, cada uma com o checkout da sua oferta (conferido: 19/19 com a oferta certa). IDs em `control/landings.json`; copy em `landings/<ID>.json`. Números da demonstração tirados da ferramenta real (perfil 1), com aviso de dados fictícios.
- A01 sem landing nova (oferta antiga; depende de aprovado).
- Publicação: só quando a oferta estiver ativa (vendedor ainda em análise).

## Próximos passos
1. ~~Nome~~ resolvido: Zion Collection Club · Hotel Business Academy.
2. Ajustar `app/engine.css` e as landings às cores oficiais do CLAUDE.md (#040605, #1B2117, #FEF5F0, #DED6BF, #8B714E, #C9B37E; Cormorant + Jost) e dar cor explícita aos spans.
3. ~~Publicar as 20 ferramentas e ligar as entregas~~ (feito em 07/11).
4. ~~18 landings~~ feitas (07/11). Faltam: vídeo de apresentação no topo de cada landing, capas, funis, automações, criativos, e-books, Gamma, campanhas pausadas.
5. Vendedor ClickMax ainda em análise: nenhum checkout vende.
6. Apagar a página técnica `/zar-teste-script` (rascunho, despublicada).
