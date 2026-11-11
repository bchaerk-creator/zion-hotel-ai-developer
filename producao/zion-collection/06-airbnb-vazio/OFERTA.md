# Zion Collection 06 · Seu Airbnb Está Vazio? O Problema Pode Estar na Sua Oferta

**Status em 11/11/2026: produto completo em ambiente de teste, para aprovação de Bruno. Nada publicado, nada enviado para aprovação do ClickMax, nenhuma campanha.**
Auditoria do projeto e sobreposição com o Arsenal 01 (mesmo título, R$ 27): `../AUDITORIA.md`.

## 1. ClickMax (Bruno's Workspace › Infoprodutos Zion)
| Item | Id | Situação |
|---|---|---|
| Produto principal | `4b088fcf-7955-4074-8db8-d6d2a62fd966` | criado |
| Oferta principal R$ 47 | `75c27213-9c35-44c3-9825-9bbab1e6bafa` · checkout `QiaIwmZOFC` | `incomplete` (não enviada), `incompleteReason` vazio, sem erro de sincronização |
| Produto bump | `b14ae411-1a77-4d7c-9787-7af986b2c130` | criado |
| Oferta bump R$ 19 | `ef27848a-37cc-4804-9941-52ac87f8d9ef` · checkout `f0KLWuYxRC` | `incomplete` (não enviada), `incompleteReason` vazio |
| Landing | `14ab1a6a-34c0-44a8-892c-9bbd43ef079f` · `/seu-airbnb-esta-vazio` | **rascunho** (`lastPublishedAt` nulo), checkout embutido da oferta principal, bump ligado e opcional (desmarcado) |
| Entrega principal | link → `p/adbc67069af26ae0/zc06-airbnb-vazio/` | ligada à oferta principal |
| Entrega bump | link → `p/adbc67069af26ae0/zc06-calendario-30/` | ligada só à oferta do bump |

Padrão de oferta: pagamento único, Pix e cartão à vista, sem boleto, `ZIONACADEMY`, +55 48 6137-1061, e-mail de suporte da conta, reembolso 7 dias.
**A compra principal entrega tudo sozinha;** o bump é complementar.

## 2. Entregáveis
| Peça | Arquivo | Teste |
|---|---|---|
| E-book 60 p. (10 capítulos, 12 diagramas, fotos reais rotuladas, fichas, glossário) | `ebook/dist/Seu-Airbnb-Esta-Vazio-Zion-Collection.pdf` | 60 páginas, nenhuma transborda (`render_ebook.js`), varredura sem promessa |
| Diagnóstico Zion de Oferta (navegador) | `ferramenta/dist/diagnostico-zion-de-oferta.html` | lógica 34/34, navegador 26/26 (celular, PDF, CSV, impressão, salvamento, XSS) |
| Diagnóstico em planilha (em branco e exemplo) | `planilhas/dist/Diagnostico-*.xlsx` | LibreOffice: 14 cenários = regra independente = app |
| Bump: calendário 30 dias (PDF + 2 planilhas) | `bump/dist/` | datas, dias da semana, virada de mês, resumo (`test_planilhas.py`, 42/42 no total) |
| Aula introdutória (5:07, 1080p, legendada) + slides + SRT | `aula/dist/` | conferida visualmente |
| Videoaula prática (2:51, gravação real da ferramenta, legendada) | `aula/dist/Videoaula-Pratica-Diagnostico-Zion.mp4` | conferida visualmente |
| Teleprompter das duas aulas | `aula/TELEPROMPTER.md` | — |
| 5 criativos 1080×1350 + vídeo de 15 s | `criativos/dist/`, copies em `criativos/CRIATIVOS.md` | sem sobreposição de texto (`render_criativos.js`) |
| Landing | `landing/dist/clickmax.html` | `pages_validate_html` válido; celular sem rolagem lateral |
| Páginas de acesso + capas | `docs/p/adbc67069af26ae0/zc06-*` | 7/7 (links, noindex, celular, bump separado) |

## 3. Copy (ECROI) e promessa
Espelhamento: "Semanas inteiras livres e nenhuma pista do porquê." · Colapso: baixar a diária não conserta uma oferta confusa · Reenquadramento: calendário vazio é sintoma · Orientação: 7 notas com evidência → 3 prioridades → plano · Implementação: primeiro passo de hoje (foco 20% · 4% · 0,8%).
Promessa: "Aprenda o passo a passo para diagnosticar a sua oferta…". Sem promessa de reservas, ocupação ou renda; exemplos sempre "dados fictícios".

## 4. Rastreamento (plano; nada ativado)
- ClickMax já registra na landing: `page_viewed`, cliques nos 3 botões, `checkout_viewed`, `pix_generated`, `purchase_approved`, `purchase_declined`, `refund_*`, `chargeback`.
- **Falta (depende de Bruno):** pixel do Meta / API de conversões no projeto (não há pixel configurado para infoprodutos); `pixelViewContent` está desligado na página. Ao configurar: PageView e ViewContent na landing, InitiateCheckout em `checkout_viewed`, Purchase **só** em `purchase_approved`, com o id da transação como `event_id` (deduplicação navegador + servidor). Pix gerado ou pendente **não** conta como compra.
- UTMs dos anúncios: `utm_source=meta&utm_medium=paid&utm_campaign=zc06-airbnb-vazio&utm_content=<criativo>`.

## 5. Checklist de QA
| Teste | Status |
|---|---|
| Ferramenta: notas 0, notas 5, vazios, inválidos, caracteres especiais, CSV, PDF, impressão, celular | **feito e passou** |
| Planilhas recalculadas no LibreOffice contra regra independente | **feito e passou** |
| Ferramenta e planilha dão o mesmo resultado | **feito e passou** |
| E-book sem transbordo, sem promessa, exemplos marcados | **feito e passou** |
| Páginas de acesso: links, celular, noindex, bump fora da principal | **feito e passou** |
| Landing validada pelo ClickMax e sem rolagem lateral | **feito e passou** |
| Ofertas sem bloqueio (`offers_get_incomplete_reason` vazio) | **feito** |
| Compra principal, compra com bump, Pix pendente, cartão recusado, estorno, reembolso, acesso indevido, idempotência de webhook | **não executado**: vendedor ClickMax `pending` e ofertas não aprovadas, então o checkout não processa pagamento. Roteiro pronto abaixo |
| Página de acesso no ar (GitHub Pages) | **depende do merge na `main`**; até lá a capa da landing e o link de entrega dão 404 |
| Excel e Google Sheets reais, celular físico | não testado |

Roteiro de compra para quando o vendedor e as ofertas estiverem ativos (valor baixo, cartão de Bruno, reembolsar em seguida): (1) compra só principal → e-mail com link `zc06-airbnb-vazio`, sem o calendário; (2) compra com bump → os dois links, total R$ 66; (3) Pix gerado e não pago → nenhum acesso, nada contado como venda; (4) cartão recusado → nenhum acesso; (5) reembolso → status `refund_completed` (o link é público e discreto: não há como revogar; registrar como risco aceito ou migrar para área de membros); (6) repetir o mesmo webhook → uma só venda no painel.

## 6. Preço, custos e indicadores
R$ 47 + bump opcional R$ 19 (ticket R$ 66 com bump). Custos por venda: taxa do ClickMax, impostos, reembolsos, mídia (quando houver). Indicadores: CTR, CPC, visitas, início de checkout, compra **confirmada**, CPA, taxa de aceite do bump, ticket médio, reembolsos, margem de contribuição.

## 7. Como reconstruir
```
python3 -I producao/zion-collection/06-airbnb-vazio/ebook/build_ebook.py && node producao/zion-collection/06-airbnb-vazio/ebook/render_ebook.js
python3 -I producao/zion-collection/06-airbnb-vazio/ferramenta/build.py && node .../ferramenta/tests/logic.test.js && node .../ferramenta/tests/e2e.js <saida> <jspdf.umd.min.js>
python3 -I .../planilhas/build_planilhas.py .../planilhas/dist && python3 -I .../planilhas/test_planilhas.py .../planilhas/dist
python3 -I .../bump/build_bump.py && node .../render_pdf.js .../bump/dist/calendario.html .../bump/dist/Calendario-Comercial-30-Dias-Zion.pdf
python3 -I .../aula/build_aula.py && node .../aula/render_slides.js && bash .../aula/render_video_aula.sh && bash .../aula/render_video_pratica.sh <jspdf>
python3 -I .../criativos/build_criativos.py && node .../criativos/render_criativos.js
python3 -I .../landing/build_landing.py
python3 -I .../entrega/build_entrega.py && node .../entrega/render_capas.js
```
jsPDF para os testes: `npm i jspdf@2.5.1` numa pasta temporária (o cdnjs é bloqueado aqui).

## 8. Pendências que dependem de Bruno
1. **Decidir a sobreposição com o Arsenal 01** (R$ 27, mesmo título): opção A, B ou outra (`../AUDITORIA.md`, seção 2).
2. Aprovar o produto (e-book, ferramenta, aulas, criativos, landing) ou pedir ajustes.
3. Narração das aulas: gravar com `aula/TELEPROMPTER.md` (Bruno ou locutor com voz licenciada). Hoje os vídeos são legendados, sem áudio; a videoaula prática tem 2:51 e chega a 12–20 min só com explicação narrada.
4. "Aprovado" para: merge na `main` (coloca a entrega no ar), envio das duas ofertas para aprovação do ClickMax, publicação da landing quando as ofertas estiverem ativas.
5. Conta de vendedor ClickMax (`pending`) e erro de sincronização das ofertas antigas (suporte ClickMax).
6. Pixel do Meta / API de conversões para infoprodutos; conta de anúncio e teto (hoje R$ 0).
7. Confirmar o uso de "Airbnb" no título dos anúncios (risco baixo de recusa; variante pronta).
