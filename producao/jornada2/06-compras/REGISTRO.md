# Módulo 6 · Compras, estoque e manutenção · Registro de produção

10/11/2026. Nada publicado no ClickMax, nada ativado, nenhum commit. Entregável: **Matriz de Compras e Manutenção** (página 6 do Plano de Gestão): Matriz de Compras (itens críticos por valor, três cotações, consumo por noite e por hóspede, contrato), estoque mínimo e ponto de pedido, e calendário de manutenção preventiva de 12 meses com a reserva de manutenção. Não alterei `docs/trilha2/index.html`, `RELATORIO.md`, `README.md`, `PLANO_G00.md`, outros módulos nem as Ferramentas 13, 14 e 18.

## Arquivos publicados (`docs/trilha2/`)
| Item | Caminho |
|---|---|
| Ficha "A minha Matriz de Compras e Manutenção" (abertura + 5 telas + resultado em 5 partes, critério com selo, PDF, próxima etapa; chave `zion-t2-compras`) | `compras/index.html` + `compras/logic.js` (cópia de `src/logic.js`; a ficha também carrega `../financas/logic.js` só para ler a Folha do Módulo 2) |
| Planilhas (6 abas: Comece aqui, Matriz de Compras, Estoque, Manutenção 12 meses, Rotina e checklist, Resumo) | `materiais/planilhas/Matriz-de-Compras-e-Manutencao-Zion-EM-BRANCO.xlsx` e `-EXEMPLO.xlsx` |
| Resumo da aula (9 páginas A4: capa + 8) | `materiais/Modulo-6-Compras-resumo.pdf` |
| Prompt de IA | `materiais/Modulo-6-Prompt-de-IA.txt` |
| Aula em vídeo (5 min 58 s, 13 cenas, narração edge-tts pt-BR FranciscaNeural, fotos op04, op05, op07, op08, op09; op10 não usada) | `videos/aula-compras.mp4` (24,2 MB) |
| Tutorial da ficha (4 min 23 s, 11 cenas, gravação real com cursor) | `videos/tutoriais/tutorial-ficha-compras.mp4` (9,2 MB) |
| Capas (foto op11, sem pessoas) | `capas/g6-h.jpg`, `g6-v.jpg`, `g6-c-aula.jpg`, `g6-c-faca.jpg`, `g6-c-resumo.jpg`, `g6-c-planilha.jpg` |

Pasta de produção: `PLANO.md`, `CHECKLIST.md`, `ROTEIRO.md`, `PROMPT_IA.md`, `REGISTRO.md`, `src/` (logic.js, build_planilha.py, build_resumo.py, render_pdf.js, build_capas.js), `tests/` (test_logic.js, e2e.js, test_planilha.py), `video/`, `tutorial/`, `demonstracao/` (capturas do e2e no iPhone 13 e o PDF da ficha com o exemplo). As pastas de trabalho dos vídeos foram apagadas.

## Testes (executados nesta sessão)
| Teste | Resultado |
|---|---|
| `tests/test_logic.js` (Node: leitura de números com a correção do Módulo 1, exemplo completo, coerência com a Folha do Módulo 2, validações das cinco telas, as 8 regras de atenção, calendário que atravessa o ano, arredondamento do ponto de pedido, bordas) | 76 ok, 0 falhou |
| `tests/e2e.js` (Playwright, iPhone 13, porta 8816, jsPDF local: 5 telas, importação da Folha do Módulo 2, bloqueios e avisos, adicionar e remover itens, casa cheia e reserva que não cobre ao vivo, resultado item a item e mês a mês contra logic.js, PDF, selo, persistência, continuar, exemplo pelo botão, cenário "dentro das regras", desktop, sem rolagem horizontal, sem erro de JavaScript) | 60 ok, 0 falhou |
| `tests/test_planilha.py` (recálculo no LibreOffice × conta independente em Python: exemplo, versão em branco, 12 cenários (calendário de julho a junho, deck na casa cheia, reserva que não cobre, duas cotações, sem ronda, sem rotina, tudo resolvido, um mês só, estoque com decimais e zerado, frequências atravessando o ano, Matriz acima da Folha) e 4 bloqueios) | 74 ok, 0 falhou |
| PDF da ficha (3 páginas; fonte do texto correta depois de cada quebra de página, correção do Módulo 1) e resumo (9 páginas; altura de cada página conferida, sem transbordo) | conferidos |
| Quadros dos vídeos (9 amostras da aula, 6 do tutorial; a cena dos números grandes foi corrigida e a aula regravada) | conferidos |
| Conformidade (vocabulário proibido, travessões, siglas na tela, promessas; números iguais em lógica, planilha, roteiro, resumo, vídeo e tutorial) | sem achados |

Reproduzir (de `producao/jornada2/06-compras`): `node tests/test_logic.js`; `python3 -I src/build_planilha.py ../../../docs/trilha2/materiais/planilhas && python3 -I tests/test_planilha.py ../../../docs/trilha2/materiais/planilhas`; `cp src/logic.js ../../../docs/trilha2/compras/logic.js`; `(cd ../../../docs && python3 -m http.server 8816 &)`; `node tests/e2e.js <saida> <jspdf.umd.min.js>`; `python3 -I src/build_resumo.py build && node src/render_pdf.js build/resumo.html ../../../docs/trilha2/materiais/Modulo-6-Compras-resumo.pdf`; `node src/build_capas.js ../../../docs/trilha2/capas`; `node video/shots.js && node video/shot_xl.js <html da planilha EXEMPLO exportado pelo LibreOffice> && python3 video/make_video.py video/spec-g06.json ../../../docs/trilha2/videos/aula-compras.mp4`; `(cd ../../clube/tutoriais-video && python3 make.py ../../jornada2/06-compras/tutorial/ficha-compras.json ../../../docs/trilha2/videos/tutoriais/tutorial-ficha-compras.mp4)`.

## Exemplo didático (dados fictícios, Cabanas do Vale, coerente com os módulos 0, 2 e 3)
- Três meses: 174 noites vendidas (58 por mês, como a Folha de outubro do Módulo 2), 150 hóspedes, 4 unidades; custo variável por noite da Folha **R$ 28,32**.
- Matriz por valor (gasto em 3 meses): café e cestas 1.260 (vendido à parte; = custo das outras receitas da Folha, 420 por mês), lavanderia 900, amenidades 780, gás 720, reposição de enxoval 240 = **R$ 3.900**. A Matriz abre linhas da Folha: enxoval 380 = lavanderia 300 + reposição 80; amenidades 260; energia 340 = gás 240 + elétrica 100.
- Itens variáveis **R$ 15,17 por noite vendida** = **53,6%** dos R$ 28,32 (resto 13,15: limpeza por estadia, energia elétrica, quebra). Por hóspede: amenidades R$ 5,20. Mês cheio (4 × 30): **R$ 1.820,69**.
- Três cotações em todos; diferença para a menor, na mesma quantidade: 112,50 + 120 + 112,50 + 48 + 44 = **R$ 437,00** no período, **R$ 1.748,00** em doze meses (conta, não previsão). Gás sem contrato; três a fechar até 31/03/2027.
- Estoque (segurança 7 dias): papel higiênico 100 por mês, entrega 5, hoje 30 → mínimo 24, ponto de pedido 40, **pedir 110**; kit, botijão e café ok. Enxoval **2,5 jogos por cama** (faltam 2).
- Calendário 2027: 9 tarefas, **17 ocorrências, R$ 3.690**; mês mais pesado novembro (R$ 1.330, na baixa); casa cheia jun, jul, ago, dez sem tarefa pesada. **Reserva de 3%** da receita real de R$ 13.565,60 = **R$ 406,97 por mês, R$ 4.883,62 no ano**; cobre todos os meses; sobra **R$ 1.193,62**.
- Causa principal: **compra recorrente sem contrato** (gás). Prioridades: contrato, pedido do papel, enxoval. Nível 1 "Compra no susto".

## Decisões tomadas
1. Entregável com nome próprio "Matriz de Compras e Manutenção" (a Matriz de Compras do G5 mais o calendário do ano da Etapa 10), página 6 do Plano.
2. Consumo por noite vendida como número principal (a fonte define "por diária vendida") e por hóspede como segunda coluna; conferência com o custo variável por noite da Folha, que amarra o módulo ao Módulo 2.
3. Ponto de pedido e estoque mínimo pela definição-padrão de gestão de estoque, declarada na ficha, na planilha e no resumo (a fonte só manda acionar o fornecedor no mínimo e contar toda segunda-feira).
4. Calendário mensal por frequência (mensal a anual); a ronda diária fica na tela de rotina, fora do calendário; regra "manutenção pesada fora da casa cheia" tirada da regra do projeto da Bíblia ("trabalhar em baixa ocupação").
5. A diferença para a menor cotação aparece sempre como "conta com os seus números, não previsão".
6. Matriz em cartões no resultado (a tabela de 6 colunas não cabia no celular).
7. A correção do `num` ("13.000" = treze mil) e a do PDF (estilo reaplicado depois da quebra de página) do Módulo 1 foram aplicadas e testadas.

## Pendências e decisões para o Bruno
1. **Reserva de 3% × 4%**: este módulo usa 3% (pedido do integrador; é o mínimo da faixa de 3% a 6% da Etapa 09), mas a Folha do Módulo 2 separa 4% da receita real como reserva de reposição (R$ 542,62). Os dois números convivem no exemplo das Cabanas. Decidir se o Módulo 2 passa a 3% ou se este módulo sobe para 4% (muda `reservaPct` no `EXEMPLO`, na planilha e nos textos: com 4%, reserva de R$ 542,62 por mês e R$ 6.511,49 no ano).
2. **Links para produtos pagos**: a ficha (tela de rotina e resultado) aponta para as Ferramentas 13, 14 e 18 em `docs/p/adbc67069af26ae0/` (páginas de acesso de produtos vendidos a R$ 19). Confirmar se a Jornada 2 pode apontar para elas ou se o link deve ir para a página de vendas.
3. **Foto op10**: tem uma pessoa e não foi usada (capas com op11; vídeo com op04, op05, op07, op08, op09). Vale corrigir a lista do `CLAUDE.md`.
4. Integrador: incluir o Módulo 6 em `docs/trilha2/index.html` (link `compras/`, chave `zion-t2-compras`, materiais) e no `RELATORIO.md`.
5. Narração sintética; regravação possível com o `ROTEIRO.md`. No tutorial, os campos de data aparecem no formato do navegador de gravação (mm/dd/aaaa), como nos tutoriais anteriores.

## Lacunas das fontes
Sem definição de estoque mínimo ou ponto de pedido; sem frequências de manutenção além da ronda diária e das frequências de pragas e dedetização da Bíblia; o pilar O4 Manutenção e Ativos aparece só pelo nome no Panorama extraído; sem prazo de contrato nem periodicidade de cotação. A Bíblia está em construção (protocolos e planilha de estoque "a inserir"); usei só o que está escrito. Mapa de fontes: `scratchpad/fontes/MAPA_FONTES_compras.md` (fora do repositório).

## Plano das aulas no ClickMax (para o integrador; nada criado)
Módulo "6 · Compras, estoque e manutenção" (posição 6), todas as aulas `enabled=false`, capas do módulo `g6-h.jpg` e `g6-v.jpg`:
1. **Aula em vídeo · Compras, estoque e manutenção** · tipo vídeo · `videos/aula-compras.mp4` · capa `g6-c-aula.jpg`.
2. **Faça agora · A minha Matriz de Compras e Manutenção** · link externo `trilha2/compras/` · capa `g6-c-faca.jpg` · anexos: tutorial (`videos/tutoriais/tutorial-ficha-compras.mp4`), as duas planilhas, o prompt de IA.
3. **Resumo** · documento `materiais/Modulo-6-Compras-resumo.pdf` · capa `g6-c-resumo.jpg`.
4. **Planilha · Matriz de Compras e Manutenção** · link + 2 anexos (em branco e exemplo) · capa `g6-c-planilha.jpg`.

## Decisões do Bruno aplicadas em 10/11/2026
- **Reserva única de 3%** em toda a Jornada 2: a Folha do Módulo 2 passou a 3% (reserva de reposição R$ 406,97, a mesma reserva de manutenção deste módulo). Pendência 1 resolvida; nada muda neste módulo.
- **Ferramentas pagas apontam para a página de vendas** (pendência 2): Ferramenta 13 → `https://infoprodutos-zion.clickmax.space/controle-enxoval`; Ferramenta 14 → `https://infoprodutos-zion.clickmax.space/quadro-ocorrencias`; Ferramenta 18 → `https://infoprodutos-zion.clickmax.space/manutencao-preventiva`, na ficha, no resumo e nas notas da planilha, com o texto "vendida(s) à parte na loja Zion".
