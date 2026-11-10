# Módulo 5 · Pessoas e organização das áreas · Registro de produção (10/11/2026)

Nada publicado no ClickMax, nada ativado, nenhum commit. Não alterei `docs/trilha2/index.html`, `RELATORIO.md`, `README.md`, `PLANO_G00.md` nem pastas de outros módulos (a ficha só **lê** `docs/trilha2/financas/logic.js` e a chave local `zion-t2-financas`).

## Arquivos publicados (`docs/trilha2/`)
| Item | Caminho |
|---|---|
| Ficha "O meu Mapa de Pessoas e Alçadas" (5 telas + resultado, chave `zion-t2-pessoas`, selo, PDF jsPDF, próxima etapa) | `pessoas/index.html` + `pessoas/logic.js` (cópia de `src/logic.js`) |
| Planilha em branco e exemplo | `materiais/planilhas/Tarefas-Escala-e-Alcadas-Zion-EM-BRANCO.xlsx` e `-EXEMPLO.xlsx` |
| Resumo da aula (8 páginas A4) | `materiais/Modulo-5-Pessoas-resumo.pdf` |
| Prompt de IA | `materiais/Modulo-5-Prompt-de-IA.txt` |
| Aula em vídeo (6:54, 13 cenas, narração edge-tts pt-BR) | `videos/aula-pessoas.mp4` |
| Tutorial da ficha (4:23, gravação real com cursor) | `videos/tutoriais/tutorial-ficha-pessoas.mp4` |
| Capas | `capas/g5-h.jpg`, `g5-v.jpg`, `g5-c-aula.jpg`, `g5-c-faca.jpg`, `g5-c-resumo.jpg`, `g5-c-planilha.jpg` |

Fontes de produção nesta pasta: `PLANO.md`, `CHECKLIST.md`, `ROTEIRO.md`, `PROMPT_IA.md`, `src/` (logic.js, build_planilha.py, build_resumo.py, render_pdf.js, build_capas.js), `tests/`, `video/` (aula.html, scenes-g05.js, spec-g05.json, make_video.py, record_h.js, shots.js, shot_xl.js, telas), `tutorial/ficha-pessoas.json`, `demonstracao/` (capturas do e2e no iPhone 13 e o PDF gerado). Pastas de trabalho dos vídeos apagadas. Mapa de fontes fora do repositório.

## Testes (executados nesta sessão)
| Teste | Resultado |
|---|---|
| `node tests/test_logic.js` (lógica, exemplo, regra da primeira contratação, alçadas, painel, plano, viabilidade com a Folha do Módulo 2, vazio, vocabulário) | 85 ok, 0 falhou |
| `node tests/e2e.js <saída> <jspdf>` (Playwright, iPhone 13, servidor na porta 8815: todas as telas, bloqueios, avisos, resultado igual à lógica, PDF, selo, persistência, continuar de onde parei, sem a Folha, botão do exemplo, desktop) | 63 ok, 0 falhou; sem erro de JavaScript; sem rolagem horizontal; PDF de 26,7 KB (3 páginas, conferidas) |
| `python3 -I tests/test_planilha.py docs/trilha2/materiais/planilhas` (recálculo no LibreOffice × conta independente: exemplo, em branco, 5 cenários de tarefas, bloqueios, alçadas, escala, plano com virada de ano, painel) | 41 ok, 0 falhou |
| Resumo PDF | 8 páginas; altura de cada página medida abaixo do rodapé (sem transbordo) |
| Vídeos | quadros conferidos (10 da aula, 10 do tutorial); foto op10 trocada por op11 (tinha uma pessoa); cena "Faça agora" corrigida (texto encostava no rodapé) e regravada |
| Conformidade | sem "consultoria", "curso", "comunidade", "mentoria", "Airbnb"; sem travessões nos textos do membro; sem siglas na tela; sem preço; exemplo rotulado; números iguais em lógica, planilha, roteiro e resumo |

## Exemplo didático (Cabanas do Vale, dados fictícios, continuação dos módulos 0 e 2)
4 unidades; a dona opera com uma diarista (por estadia) e um auxiliar de manutenção; 0 dias de férias em 24 meses; nunca ficou 7 dias sem atender. Dependências: decisão e acesso fortes (acessos em 14/11/2026). Inventário 52 linhas, 41 (78,8%) de resolução rápida. **20 h da dona por semana** (= 20 h da Conta da Retirada do Módulo 2): baixo 5 · médio 9 · alto 6. Primeira a delegar: **check-in e check-out** (5 h, 25%); depois, mensagens. 4 de 6 setores só da dona. 6 de 7 regras escritas; cortesia até R$ 42 (15% da diária de R$ 280); **alçada inicial R$ 100 → R$ 300** no segundo mês. Painel: nota mínima 4,7; gasto 10%; leitura na segunda-feira; nível 1. Plano: diarista por estadia, início **16/11/2026**, semanas até 13/12, **avaliação 13/12/2026**; custo a mais R$ 500 → ocupação de equilíbrio **28,5% → 30,7%** (abaixo de 70%). Planilha de exemplo: escala com 2 turnos sem ninguém; painel com 2 exceções em 4 semanas.

## Plano das aulas no ClickMax (para o integrador; nada criado)
Módulo "Módulo 5 · Pessoas e organização das áreas" (posição 5, capa `g5-h.jpg` / `g5-v.jpg`), todas as aulas desativadas:
1. **Aula em vídeo** (capa `g5-c-aula.jpg`): `videos/aula-pessoas.mp4`.
2. **Faça agora** (link externo `trilha2/pessoas/`, capa `g5-c-faca.jpg`), anexos: tutorial `videos/tutoriais/tutorial-ficha-pessoas.mp4`, as duas planilhas, `Modulo-5-Prompt-de-IA.txt`.
3. **Resumo** (documento `Modulo-5-Pessoas-resumo.pdf`, capa `g5-c-resumo.jpg`).
4. **Planilha** (link + 2 anexos EM-BRANCO e EXEMPLO, capa `g5-c-planilha.jpg`).

## Decisões e pendências para o Bruno
1. O "plano de quatro semanas" é o Plano de Quatro Semanas™ da Etapa 10 (treino da primeira pessoa), precedido de acessos, procedimento e tabela de critérios. A saída completa (teste das duas semanas, plano de 6 a 8 meses) ficou para o Módulo 7. Confirmar.
2. "Sete itens prontos" é contagem, não nota (a Jornada 2 só tem nota no Marco Zero).
3. Julgamento médio sugerido para manutenção e avaliações é elaboração (a fonte não classifica essas duas).
4. A ficha lê a Folha Única do Módulo 2 no mesmo aparelho para o teste de viabilidade; sem ela, pergunta ao membro.
5. Temas trabalhistas (contrato, encargos, vínculo de diarista) ficam fora e remetidos ao contador. Validar se quer uma aula específica.
6. Narração sintética; o `ROTEIRO.md` permite regravar. Player do ClickMax com mp4 direto: mesma pendência dos módulos anteriores.
7. A página `docs/trilha2/index.html` ainda não lista o Módulo 5 (tarefa do integrador).

## Lacunas de fonte
- O Panorama cita o pilar "Pessoas e Cultura" (Trilha C) sem conteúdo próprio; os manuais setoriais da Bíblia Operacional estão em grande parte "aguardando" e não há tabela de alçadas nem escala preenchida no Notion.
- Nenhuma fonte define fórmula para horas de julgamento médio, desempate entre dependências, nem formato de grade da escala semanal (elaborações declaradas no `PLANO.md`, seção 11).
- Nenhum nome real da equipe Zion foi usado.
