# Relatório · Mini Mentoria de Performance Hoteleira (25/11/2026)

Branch `claude/mini-mentoria-performance-hoteleira-cf3mxj`. **Nada publicado, oferta não enviada para aprovação, nenhuma campanha ou formulário criado no Meta, R$ 0 de anúncio, nenhuma mensagem enviada.** Operações existentes (Mini Mentoria de Estruturação, Zaya, Clube, Land Bank, funis, Asaas) só lidas.

## Implementado
- **Plataforma** `dist/index.html` (arquivo único; fontes e logo Zion): ficha inicial, 7 módulos (roteiro, guia, formulário de 10 perguntas com "não sei" e "não se aplica", calculadora), feedback em 5 partes, diagnóstico, plano 7/30/60/90, dossiê em PDF, convite opcional, cópia de segurança.
- **Motor** `src/logic.js`: nota = soma das válidas ÷ (2 × válidas); cobertura sempre; NA fora; desconhecido ≠ zero; ocupação > 100% e denominador zero tratados; contribuição negativa explicada; plano com ação, motivo, responsável, prazo, indicador e evidência.
- **7 calculadoras:** posicionamento · ocupação e canais · diária e RevPAR · contribuição e equilíbrio (com cenário adverso e reposição) · capacidade e estoque · custo e retorno da expansão · necessidade de capital.
- **Editorial:** 7 guias de 34 páginas A5 (`ebook/dist/guia-N.pdf`), 7 capas premium 1080×1350 e na capa do PDF, com foto real da Zion e logo oficial.
- **Criativos:** 7 narrativas × 7 cards = 49 cards em `docs/ads/mm-performance/`, mesmas composições e fotos dos campeões, 49 copies aplicadas, telas reais com dados fictícios nos cards 5 a 7 (`anuncios/`).
- **Landing** (`landing/`): conversão low ticket, vídeo de demonstração real (23 s), 4 telas, dossiê de exemplo, checkout; rascunho no ClickMax.
- **ClickMax (rascunho):** produto, oferta, portal (não publicado), turma, 7 módulos, 7 aulas, entrega ligada, página. Ids em `OFERTA.md`.

## Testes executados (resultado real)
| Teste | Resultado |
|---|---|
| `node tests/logic.test.js` (contas à mão, extremos) | 21 ok, 0 falhas |
| `node tests/rastreamento.test.js` | 13 ok, 0 falhas |
| `node tests/e2e.js` (Playwright, celular 390 px, na cópia empacotada): 12 telas sem rolagem horizontal, feedback 5 partes com valores conferidos, 7 calculadoras com números conferidos, negativo e texto inválido, "não sei" sem nota, retomada após recarregar, isolamento entre perfis, consentimento desmarcado, PDF real baixado (9 seções, sem "undefined/NaN"), backup, restauração e arquivo inválido, console sem erros | 23 ok, 0 falhas |
| `python3 -I ebook/validar_conteudo.py` (7 guias: tamanhos, "Dados fictícios", termos proibidos) + renderização | 7 ok; nenhuma página transborda |
| `landing/teste_local.js`: celular e desktop sem rolagem horizontal, nenhuma imagem quebrada, 1 checkout | ok |
| Conferência visual: capas, cards, landing, telas | feita; ajustes aplicados |
Não testado: compra, Pix, cartão, webhook, Pixel/CAPI, Zaya, reembolso (vendedor `pending`; nada de cobrança real); outros navegadores além do Chromium; acessibilidade formal; ClickMax em produção; login (a plataforma não tem). O jsPDF vem do cdnjs (bloqueado aqui): o teste serviu o pacote npm.

## Pendências para Bruno (nada disso foi feito)
1. **Gravar as 7 aulas** (roteiros em `fontes/`; revisar grafia). Sem vídeo, a página só pode dizer "aulas guiadas". Preencher `src/videos.json` ({"1": url}) e rodar `empacotar.sh`.
2. **Decidir:** promessa do topo (a pedida × "Aprenda o passo a passo"); **prazo de acesso (assumi 12 meses)**; nome e preço perto da Mini Mentoria de Estruturação; gancho × conteúdo de 3 criativos; fotos reais nas capas (a regra do repositório pedia telas, você pediu fotos).
3. **Validar com a equipe:** pesos iguais, faixas 40/70, impacto/esforço e itens críticos (`src/meta.json`); revisão de um profissional nos itens de segurança, vigilância sanitária, licenças e jurídico dos guias.
4. **Merge na `main`** (publica plataforma, guias, imagens e cards no GitHub Pages) e então conferir a página no ClickMax com imagens.
5. **Concluir a conta de vendedor** e só então: enviar a oferta para aprovação (`incompleteReason` já vazio), publicar o portal e a página, produto/imagem do produto.
6. **Rastreamento real:** Asaas, webhook, Pixel/CAPI, fluxos/tags no ClickMax, Zaya (consentimento e opt-out), compra de teste e reembolso.
7. **Persistência no servidor e envio do dossiê à Zion** (hoje: dados no aparelho e envio manual por WhatsApp) exigem backend e revisão LGPD.
8. **Meta:** criar o formulário nativo (`anuncios/FORMULARIO_META.md`) e a campanha **pausada** no Windsor, conta a confirmar, só com "aprovado" e teto.
9. A Bela (WhatsApp) está instruída a não oferecer o produto de R$ 47 de estruturação; avaliar texto para este produto.
10. Skills do ClickMax locais estão com revisão diferente da publicada (`c40fdd3dc26c` × `f86020e0ba3e`): atualizar com `npx skills update -g`.
