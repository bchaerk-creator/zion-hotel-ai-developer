# Módulo 7 · Qualidade, reputação e plano de crescimento · Registro de produção (10/11/2026)

Último módulo da Jornada 2. Nada publicado no ClickMax, nada ativado, nenhum commit. Não alterei `docs/trilha2/index.html`, `RELATORIO.md`, `README.md`, `PLANO_G00.md` nem pastas de outros módulos: a ficha só **lê** as chaves `zion-t2-*` e os `logic.js` dos módulos 0 a 6.

## Arquivos publicados (`docs/trilha2/`)
| Item | Caminho |
|---|---|
| Ficha "O Montador do Plano de Gestão" (abertura + 5 telas + resultado em 5 partes, chave `zion-t2-qualidade`, selo, PDF jsPDF do Plano completo, próxima etapa) | `qualidade/index.html` + `qualidade/logic.js` (cópia de `src/logic.js`) |
| Planilha em branco e exemplo (6 abas) | `materiais/planilhas/Qualidade-e-Reputacao-Zion-EM-BRANCO.xlsx` e `-EXEMPLO.xlsx` |
| Resumo da aula (8 páginas A4: capa + 7) | `materiais/Modulo-7-Qualidade-resumo.pdf` |
| Prompt de IA | `materiais/Modulo-7-Prompt-de-IA.txt` |
| Aula em vídeo (6 min 53 s, 14 cenas, narração edge-tts pt-BR FranciscaNeural, fotos op05, op07, op08, op11, op12) | `videos/aula-qualidade.mp4` (26,3 MB) |
| Tutorial da ficha (4 min 23 s, 10 cenas, gravação real com cursor) | `videos/tutoriais/tutorial-ficha-qualidade.mp4` (9,7 MB) |
| Capas (foto op04, sem pessoas) | `capas/g7-h.jpg`, `g7-v.jpg`, `g7-c-aula.jpg`, `g7-c-faca.jpg`, `g7-c-resumo.jpg`, `g7-c-planilha.jpg` |

Pasta de produção: `PLANO.md`, `CHECKLIST.md` (teste das duas semanas, 10 itens), `ROTEIRO.md`, `PROMPT_IA.md`, `src/` (logic.js, build_planilha.py, build_resumo.py, render_pdf.js, build_capas.js), `tests/`, `video/` (aula.html, scenes-g07.js, spec-g07.json, make_video.py, record_h.js, shots.js, shot_xl.js, estado_exemplo.js, telas), `tutorial/` (gerar_tutorial.js, ficha-qualidade.json), `demonstracao/` (capturas do e2e no iPhone 13 e o PDF do Plano completo do exemplo). Mapa de fontes: `scratchpad/fontes/MAPA_FONTES_qualidade.md` (fora do repositório).

## Como o Montador funciona
- Lê do mesmo aparelho as chaves `zion-t2-marco-zero`, `-planejamento`, `-financas`, `-preco`, `-marketing`, `-pessoas`, `-compras`. **Pronta** = a chave tem o campo `pdf` (a ficha chegou ao PDF); **em andamento** = chave sem `pdf`; **ainda não feita** = sem chave, com o link da ficha.
- Carrega os sete `logic.js` um a um e captura o objeto global logo depois de cada carga (planejamento, preço e pessoas usam o mesmo nome `ZP`). Cada página entra no PDF resumida com os números da própria ficha; se uma lógica mudar ou faltar, entra um resumo mínimo, sem erro.
- Pré-preenche nome, e-mail, hospedagem e situação (qualquer ficha), nota, meta, escala e reunião (Módulo 1), nota mínima, dia do painel e início (Módulo 5) e a meta de venda direta (Módulo 3).
- Correções do molde aplicadas: `num("13.000")` = 13000 (Módulo 1); fonte redefinida depois de cada quebra de página do PDF (Módulos 1 e 5); títulos de seção sem ficar órfãos no pé da página.

## Testes (executados nesta sessão)
| Teste | Resultado |
|---|---|
| `node tests/test_logic.js` (exemplo, páginas lidas, pré-preenchimento, resumo das 7 páginas com os exemplos reais dos módulos 0 a 6, lógica quebrada, bloqueios e avisos, leitura do teste, datas, escala 10, quem vai abrir, vocabulário, cópia em docs) | 88 ok, 0 falhou |
| `node tests/e2e.js <saída> <jspdf>` (Playwright, iPhone 13, porta 8817: 5 páginas prontas + 1 em andamento + 1 faltando, todas as telas, bloqueios, ao vivo, resultado igual à lógica, PDF parcial e completo lidos com pdftotext, selo, persistência, continuar, aparelho novo com o botão do exemplo, quem vai abrir, desktop) | 64 ok, 0 falhou; sem erro de JavaScript; sem rolagem horizontal; PDF completo de 5 páginas (cerca de 40 KB) |
| `python3 -I tests/test_planilha.py docs/trilha2/materiais/planilhas` (recálculo no LibreOffice × conta independente: exemplo, em branco, bloqueios, escala 10, críticas fora do trimestre, painel, 7 leituras do teste, fases, virada do ano, ano bissexto) | 39 ok, 0 falhou |
| PDF do Plano (exemplo completo) | 5 páginas; fonte certa depois das quebras; sem título órfão (conferido em imagem) |
| Resumo PDF | 8 páginas; espaço livre medido acima do rodapé em todas (sem transbordo) |
| Vídeos | quadros conferidos (8 da aula, 12 do tutorial); cena das oito páginas compactada (a lista passava do rodapé); tutorial regravado depois de corrigir o "continuar de onde parei" que aparecia na primeira visita |
| Conformidade | sem "consultoria", "curso", "comunidade", "mentoria", "Airbnb"; sem travessões; sem siglas na tela; sem preço; exemplo rotulado; números iguais em lógica, planilha, roteiro, resumo e vídeo |

## Exemplo didático (Cabanas do Vale, dados fictícios, continuação dos módulos 0 a 6)
Nota **4,7 de 5** com **38 avaliações** (Plataforma A 24 · 4,7; Plataforma B 9 · 4,6; perfil no mapa 5 · 4,9 → 178,7 ÷ 38 = 4,70); **meta 4,8 até 31/10/2027** (Módulo 1); nota mínima 4,7 (Módulo 5). Uma avaliação de 3 → **4,66**. Taxa de avaliação **25 ÷ 72 = 34,7%** (abaixo de 40%). Concorrentes 4,6 (+0,1). Dimensão mais baixa: limpeza 4,6. Sete críticas no trimestre; "ralo do chuveiro com cheiro na cabana 3" **3 vezes** → ajuste até **30/11/2026**. Resposta média 40 min (máx. 60). Painel de 4 semanas: 2 exceções, 1 avaliação sem resposta. Rotina: segunda 08:00 (Módulo 1), painel na segunda (Módulo 5), Folha no dia 5, trimestrais 11/01, 11/04, 11/07, 11/10/2027, anual 08/11/2027. Plano de saída: Fase 1 16/11/2026 a 10/01/2027; Fase 2 11/01 a 07/03/2027; Fase 3 08/03 a 13/06/2027 (14 semanas); **teste 14/06 a 27/06/2027**; **7,4 meses**. Segunda unidade: **agora não, faltam 3 de 4**. Plano de crescimento: nota 4,7 → 4,8; **venda direta 30% → 40% até 30/06/2027** (Módulo 3).

## Plano das aulas no ClickMax (para o integrador; nada criado)
Módulo "7 · Qualidade, reputação e plano de crescimento" (posição 7, capas `g7-h.jpg` / `g7-v.jpg`), todas as aulas `enabled=false`:
1. **Aula em vídeo** (capa `g7-c-aula.jpg`): `videos/aula-qualidade.mp4`.
2. **Faça agora · O Montador do Plano de Gestão** (link externo `trilha2/qualidade/`, capa `g7-c-faca.jpg`), anexos: tutorial `videos/tutoriais/tutorial-ficha-qualidade.mp4`, as duas planilhas, `Modulo-7-Prompt-de-IA.txt`.
3. **Resumo** (documento `materiais/Modulo-7-Qualidade-resumo.pdf`, capa `g7-c-resumo.jpg`).
4. **Planilha · Qualidade e Reputação** (link + 2 anexos EM-BRANCO e EXEMPLO, capa `g7-c-planilha.jpg`).

## Decisões e pendências para o Bruno
1. **"Pilar 07 (reputação) da Trilha 1"**: no Panorama, o Pilar 07 da Trilha A é Lançamento, e o pilar "Reputação e Avaliações" da Trilha C não tem conteúdo. Usei o Volume 07 Lançamento (capítulo 18, Protocolo da Primeira Avaliação™) e a Etapa 07 (Sistema de Avaliações™). Confirmar.
2. **Página pronta = PDF gerado na ficha** (campo `pdf`). Critério de conclusão do módulo exige as sete páginas prontas no mesmo aparelho; o PDF do Plano sai mesmo com páginas faltando, marcadas "página ainda não feita". Quem trocou de aparelho precisa refazer as fichas (limitação do `localStorage`, ver `LIMITACOES.md`; a consolidação no servidor do ZAIOS resolveria).
3. **Convenções declaradas**: tolerância de 0,1 ponto (0,2 na escala de 10) para "nota mantida" no teste; "ocupação mantida" = maior ou igual à projetada; padrão mínimo como conjunto de regras das fontes; 15 min para avaliações e para a auditoria na rotina.
4. **Dependência dos outros módulos**: o resumo das páginas 4 e 6 usa os `logic.js` atuais de marketing e compras (que estavam em produção). Se o formato das chaves mudar, a página entra com resumo mínimo; o `tests/test_logic.js` acusa isso na hora.
5. **Capas**: como nos módulos anteriores, as fontes Cormorant e Aventa não carregam no `setContent` do Playwright e as capas saem com a fonte serifada de sistema. Vale corrigir em todas as capas da jornada de uma vez (embutir as fontes em base64 no `build_capas.js`).
6. Narração sintética (edge-tts); o `ROTEIRO.md` permite regravar. Player do ClickMax com mp4 direto: mesma pendência dos módulos anteriores. Integrador: incluir o Módulo 7 em `docs/trilha2/index.html` (link `qualidade/`, chave `zion-t2-qualidade`) e no `RELATORIO.md`.

## Lacunas de fonte
Sem conteúdo do pilar Reputação e Avaliações (Trilha C) no Panorama; sem número para "variação normal" da nota no teste; sem tempo definido para responder avaliações e para a auditoria; o nome "padrão mínimo" não existe nas fontes. Exemplos numéricos das fontes (receita por nota do Volume 07; 64%, 4,82 e R$ 9.800 da Etapa 10) não foram usados.
