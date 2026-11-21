# Relatório da sessão · Produto 01 · Você tem terra. Falta capital? (21/11/2026)

Branch: `claude/zion-hotel-academy-produto-01-sul1ay`. **Nada publicado, nada enviado para aprovação, nenhum disparo, nenhuma campanha, R$ 0 de anúncio.** Funis, campanhas, Zaya, Clube, Land Bank e produtos existentes não foram tocados (só lidos).

## Entregas (1 a 8)
1. **Prévia da landing:** páginas A e B em rascunho no ClickMax: `https://infoprodutos-zion.clickmax.space/terra-capital-a` e `/terra-capital-b` (rascunho: o link só abre logado). As imagens e o vídeo da página vêm do site público, então **só aparecem depois que a branch for para a `main`**. Prévia local com imagens: `landing/dist/previa.html`; código: `landing/dist/clickmax.html`.
2. **Prévia da área de membros:** portal "Zion Hotel Academy" criado e **não publicado** (8 módulos, 23 aulas, curso desativado). O conteúdo das aulas é o portal do aluno (`docs/p/adbc67069af26ae0/terra-capital/`, com links `#aula-N`, `#ferramenta-x`). Prévia local: abrir `dist/index.html`.
3. **E-book finalizado:** `dist/Voce-tem-terra-falta-capital-Zion.pdf` (60 páginas, verificado: 60 páginas, sem transbordo de texto).
4. **Ferramentas funcionais:** 10 ferramentas no portal (patrimônio, lacuna, operação com cenário adverso, dívida Price/SAC com cobertura, parceria/arrendamento, checklist, prioridades 20·4·0,8, plano de 30 dias, mapa mental + mapa de desenvolvimento, Gerador de Dossiê em PDF) + backup do progresso.
5. **Checkout em ambiente de teste: NÃO foi possível.** As ofertas não estão aprovadas e o vendedor segue `pending` no ClickMax; testar pagamento exigiria cobrança real. As duas ofertas passam no diagnóstico (`incompleteReason` vazio). O fluxo pós-pagamento foi simulado em modelo testado (ver 6), o que **não substitui** a compra de teste.
6. **Relatório de rastreamento:** `RASTREAMENTO.md` (o que foi testado, o que não foi, passo a passo).
7. **Pendências audiovisuais:** abaixo.
8. **Checklist de publicação:** abaixo.

## Testes executados (resultado real)
| Teste | Resultado |
|---|---|
| `node tests/logic.test.js` (lógica financeira contra contas independentes) | 23 ok, 0 falhas |
| `node tests/rastreamento.test.js` (webhook, idempotência, reembolso, conciliação, UTM) | 11 ok, 0 falhas |
| `node tests/e2e.js` (Playwright: celular 390 px sem rolagem horizontal, 20 aulas abrem, cálculos, entradas vazias/negativas, persistência, PDF real baixado, backup/restauração, dossiê sem exemplos fictícios, eventos sem valores, console sem erros) | 26 ok, 0 falhas |
| E-book: renderização e checagem de transbordo | 60 páginas, nenhuma transborda |
| Landing: celular e desktop sem rolagem horizontal, nenhuma imagem quebrada (prévia local) | ok |
Não testado: vídeos (não existem), acessibilidade formal (WCAG) além de contraste/alvos de 44 px, navegadores além do Chromium, ClickMax em produção.
Observação: o jsPDF vem do cdnjs (bloqueado neste ambiente); o teste serviu o pacote npm.

## Pendências audiovisuais
- 20 microaulas: roteiros em `aulas/ROTEIROS.md` (25 a 50 s cada; ≈ 11 min no total). Gravar com legenda; validar duração.
- Vídeo de boas-vindas (≈36 s) e de encerramento (≈30 s): textos prontos, **aguardam Bruno** (gravar ou autorizar narração; direitos de voz e imagem).
- Fotos: usar só reais da Zion (retrato de Bruno e Zion Bubble Glamping); nenhuma imagem gerada como foto.
- Quando houver vídeos: preencher `VIDEOS = {n: url}` no `src/app.html`, rodar `build.py` e `empacotar.sh`.

## Checklist de publicação (só com "aprovado" de Bruno)
- [ ] Decidir: paleta (oficial do repositório × a do prompt) e sobreposição com os produtos existentes do tema.
- [ ] Revisão jurídica/financeira do conteúdo (guia e aulas) por profissional; frase da aula 14 (item 7 da auditoria).
- [ ] Merge da branch na `main` (publica o portal, o PDF e as imagens no GitHub Pages) e conferir os endereços (`/p/adbc67069af26ae0/terra-capital/`).
- [ ] Conferir as páginas A/B com imagens e vídeo no ar.
- [ ] Gravar vídeos (ou publicar sem vídeo, como está).
- [ ] Confirmar pixel e CAPI; configurar o rastreamento.
- [ ] Concluir a conta de vendedor no ClickMax (Carteira); sem isso nenhum checkout vende.
- [ ] Enviar as duas ofertas para aprovação (`offers_send_to_approval`) e aguardar `active`.
- [ ] Compra de teste, entrega, reembolso e conciliação (ver `RASTREAMENTO.md`).
- [ ] Ativar o curso e publicar o portal; publicar as páginas.
- [ ] Só então: campanha pausada, com o teto aprovado por Bruno.

## Onde está tudo
`producao/produto-01-terra-capital/`: `src/` (lógica, app, aulas), `tests/`, `ebook/`, `landing/`, `aulas/`, `comercial/`, `dist/`, `AUDITORIA.md`, `OFERTA.md`, `RASTREAMENTO.md`. Entrega: `docs/p/adbc67069af26ae0/terra-capital/` (`empacotar.sh`).
