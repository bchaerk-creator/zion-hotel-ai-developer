# Módulo 3 · Preço, reservas e distribuição · Registro de produção

10/11/2026. Nada publicado no ClickMax, nada ativado, nenhum commit. Entregável: **Tabela de Preço e Canais** (página 3 do Plano de Gestão). Não alterei `docs/trilha2/index.html`, `RELATORIO.md`, `README.md`, `PLANO_G00.md`, outros módulos, o Precificador (A02) nem a Ferramenta 01.

## Arquivos publicados (`docs/trilha2/`)
| Item | Caminho |
|---|---|
| Ficha "A minha Tabela de Preço e Canais" (6 telas + resultado em 5 partes, critério com selo, PDF, próxima etapa; chave `zion-t2-preco`) | `preco/index.html` + `preco/logic.js` (cópia de `src/logic.js`; a ficha também carrega `../financas/logic.js` só para ler a Folha do Módulo 2) |
| Planilhas (8 abas: Comece aqui, Custo e Referência, Mapa de Canais, Piso, Calendário 12 meses, Datas de pico, Resumo, Checklist da revisão) | `materiais/planilhas/Tabela-de-Preco-e-Canais-Zion-EM-BRANCO.xlsx` e `-EXEMPLO.xlsx` |
| Resumo da aula (9 páginas A4: capa + 8) | `materiais/Modulo-3-Preco-resumo.pdf` |
| Prompt de IA | `materiais/Modulo-3-Prompt-de-IA.txt` |
| Aula em vídeo (6 min 11 s, 13 cenas, narração edge-tts pt-BR FranciscaNeural, fotos op05, op07, op08, op09, op11, op12) | `videos/aula-preco.mp4` (27,7 MB) |
| Tutorial da ficha (4 min 20 s, 11 cenas, gravação real com cursor) | `videos/tutoriais/tutorial-ficha-preco.mp4` (8,7 MB) |
| Capas | `capas/g3-h.jpg`, `g3-v.jpg`, `g3-c-aula.jpg`, `g3-c-faca.jpg`, `g3-c-resumo.jpg`, `g3-c-planilha.jpg` |

Pasta de produção: `PLANO.md`, `CHECKLIST.md`, `ROTEIRO.md`, `PROMPT_IA.md`, `src/` (logic.js, build_planilha.py, build_resumo.py, render_pdf.js, build_capas.js), `tests/`, `video/`, `tutorial/`, `demonstracao/` (10 capturas do e2e no iPhone 13 e um PDF da ficha com o exemplo). As pastas de trabalho dos vídeos foram apagadas.

## Testes (executados nesta sessão)
| Teste | Resultado |
|---|---|
| `tests/test_logic.js` (Node: exemplo, calendário real e bissexto, vírgula, 25 bloqueios e avisos, 9 causas na ordem, bordas) | 75 ok, 0 falhou |
| `tests/e2e.js` (Playwright, iPhone 13, porta 8813, jsPDF local: 6 telas, importação da Folha do Módulo 2, adicionar e remover canal, bloqueios, resultado linha a linha contra logic.js, PDF, selo, persistência, continuar, exemplo pelo botão, cenário de preço fixo, desktop, sem rolagem horizontal, sem erro de JavaScript) | 61 ok, 0 falhou |
| `tests/test_planilha.py` (recálculo no LibreOffice × conta independente em Python com `calendar`; exemplo, versão em branco, 8 bloqueios, 11 causas e bordas, calendário que começa em julho e atravessa fevereiro bissexto, custo por reserva) | 43 ok, 0 falhou |
| Quadros dos vídeos (8 amostras da aula, 14 do tutorial) e páginas do PDF (altura de cada página conferida; sem transbordo) | conferidos |
| Conformidade (vocabulário proibido, travessões, siglas na tela, promessas; números iguais em lógica, planilha, roteiro, resumo e vídeo) | sem achados |

Reproduzir: `node tests/test_logic.js`; `python3 -I src/build_planilha.py ../../../docs/trilha2/materiais/planilhas && python3 -I tests/test_planilha.py ../../../docs/trilha2/materiais/planilhas`; `(cd ../../../docs && python3 -m http.server 8813 &)`; `node tests/e2e.js <saida> <jspdf.umd.min.js>`; `python3 -I src/build_resumo.py build && node src/render_pdf.js build/resumo.html ../../../docs/trilha2/materiais/Modulo-3-Preco-resumo.pdf`; `node src/build_capas.js ../../../docs/trilha2/capas`; `node video/shots.js && node video/shot_xl.js <html da planilha exportado pelo LibreOffice> && python3 video/make_video.py video/spec-g03.json ../../../docs/trilha2/videos/aula-preco.mp4`; `(cd ../../clube/tutoriais-video && python3 make.py ../../jornada2/03-preco/tutorial/ficha-preco.json ../../../docs/trilha2/videos/tutoriais/tutorial-ficha-preco.mp4)`.

## Exemplo didático (dados fictícios, Cabanas do Vale, coerente com os módulos 0 e 2)
- Da Folha do Módulo 2: custo variável por noite 28,32; custo por noite vendida 153,03; diária praticada 280; 2,32 noites por estadia; receita de hospedagem 16.240.
- Canais: Plataforma A 50% (16%), Plataforma B 20% (15%), venda direta 30% (0%); pagamento 1,5%, imposto 6%. Comissão média **11,0%** (= Módulo 2). Líquido por noite na referência 229,50 / 232,50 / 277,50; depois do variável 201,18 / 204,18 / 249,18.
- Referência: média de 5 concorrentes (sem 270 e 360) = **300**.
- Piso: custo da noite na Plataforma A 153,03 ÷ 0,765 = **200,04**; margem 10% → 220,04; **piso escrito 225** (75% da referência). Limite do variável 37,02.
- Faixas 225 / 270 / 300 / 450 / 660; noites 84 / 122 / 99 / 44 / 16 = 365 (2027). Picos: Carnaval 660, Corpus Christi 570, Festival de inverno 600, Réveillon 720 (mínimo 5). Outubro 279,68 (≈ diária de 280 da Folha). **Diária média do calendário 305,92**.
- Meta de venda direta 30% → **40% até 30/06/2027**; comissão que deixaria de sair num mês ≈ **255,20** (conta, não previsão).
- Causa principal: **venda direta sem motor de reservas**.

## Decisões tomadas
1. Entregável com nome próprio "Tabela de Preço e Canais" (une a Tabela de Pricing do G3 e o Mapa de Canais do G2).
2. Ordem das telas: custo → canais → referência → piso → calendário → picos e meta, porque o piso precisa das deduções do canal mais caro (G2 define o custo que o G3 cobre).
3. Fórmula do piso (elaboração declarada): (custo por noite vendida + custo por reserva ÷ noites) ÷ (1 − deduções do canal mais caro) × (1 + margem mínima). Piso abaixo do custo é aviso e causa principal, não bloqueio; piso acima da referência bloqueia.
4. Calendário mensal (12 linhas × meio de semana e fim de semana) no lugar das 52 semanas da Etapa 08, para caber no celular; datas de pico em linhas próprias. Convenções: fim de semana = noites de sexta e sábado; noites de pico saem primeiro do meio de semana.
5. A ficha não mostra "receita potencial a 100%" (a Etapa 08 calcula): só a diária média das diárias-alvo, sempre com "não é previsão".
6. Precificador (A02) e Ferramenta 01 aparecem como complementos por link, sem alteração.

## Pendências e decisões para o Bruno
1. **153,03 × 153,04**: a ficha do Módulo 2 mostra R$ 153,04 (153,0414 sem arredondar), enquanto o plano, o resumo e o relatório do Módulo 2 dizem 153,03 (28,32 + 124,72 arredondados). Este módulo usa 153,03, como pedido; o botão "Trazer da Folha" traz 153,04. Sugestão: o integrador decide se o Módulo 2 passa a citar 153,04 ou se a ficha do Módulo 2 arredonda os dois termos.
2. **Links para produtos pagos**: o resultado da ficha aponta para o Precificador (bônus, `p/adbc67069af26ae0/zar-a02/`) e para a planilha da Ferramenta 01 (`p/adbc67069af26ae0/planilha-01/`), que são entregas de produtos vendidos. Confirmar se a Jornada 2 pode apontar para eles ou se o link deve ir para a página de vendas.
3. **Foto op10**: o `CLAUDE.md` lista op10 como sem pessoas, mas o corte vertical mostra uma pessoa na banheira. Não usei op10 (as capas usam op12, como o Módulo 2). Vale corrigir a lista do `CLAUDE.md`.
4. Integrador: incluir o Módulo 3 em `docs/trilha2/index.html` (link `preco/`, chave `zion-t2-preco`, materiais) e no `RELATORIO.md`.
5. Narração sintética; regravação possível com o `ROTEIRO.md`. No tutorial, o campo de data aparece no formato do navegador de gravação (mm/dd/aaaa), como nos tutoriais anteriores.

## Lacunas das fontes
Sem percentual de margem mínima nem fórmula do piso; sem régua para comissão média; sem número de meta de venda direta (a ficha só exige meta acima da atual e com prazo). Os exemplos numéricos da Etapa 08 (referência R$ 560) não foram usados. Mapa de fontes: `scratchpad/fontes/MAPA_FONTES_preco.md` (fora do repositório).

## Plano das aulas no ClickMax (para o integrador; nada criado)
Módulo "3 · Preço, reservas e distribuição" (posição 3), todas as aulas `enabled=false`:
1. **Aula em vídeo** · tipo vídeo · `videos/aula-preco.mp4` · capa `g3-c-aula.jpg`.
2. **Faça agora · A minha Tabela de Preço e Canais** · link externo `trilha2/preco/` · capa `g3-c-faca.jpg` · anexos: tutorial (`videos/tutoriais/tutorial-ficha-preco.mp4`), as duas planilhas, o prompt de IA.
3. **Resumo** · documento `materiais/Modulo-3-Preco-resumo.pdf` · capa `g3-c-resumo.jpg`.
4. **Planilha · Tabela de Preço e Canais** · link + 2 anexos (em branco e exemplo) · capa `g3-c-planilha.jpg`.
Capas do módulo: `g3-h.jpg` e `g3-v.jpg`.
