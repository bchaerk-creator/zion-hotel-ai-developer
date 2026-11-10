# Módulo 1 · Planejamento, metas e indicadores · Registro de produção (10/11/2026)

Entregável: **Painel de Gestão** (página 1 do Plano de Gestão). Nada publicado no ClickMax, nada ativado, nenhum commit. Nada fora de `producao/jornada2/01-planejamento/` e dos arquivos novos com o número 1 ou o slug `planejamento` em `docs/trilha2/`.

## Arquivos publicados (`docs/trilha2/`)
| Peça | Arquivo |
|---|---|
| Ficha "O meu Painel de Gestão" (abertura + 5 telas + resultado em 5 partes, selo, PDF, chave `zion-t2-planejamento`) | `planejamento/index.html` + `planejamento/logic.js` (cópia de `src/logic.js`) |
| Planilha em branco e exemplo (Comece aqui, Metas e donos, Painel 12 meses, Reunião semanal, Plano 6 semanas, Definições e rotina) | `materiais/planilhas/Painel-de-Gestao-Zion-EM-BRANCO.xlsx`, `...-EXEMPLO.xlsx` |
| Resumo da aula (capa + 7 páginas A4) | `materiais/Modulo-1-Planejamento-resumo.pdf` |
| Prompt de IA | `materiais/Modulo-1-Prompt-de-IA.txt` |
| Aula em vídeo (4 min 53 s, 12 cenas, narração edge-tts pt-BR FranciscaNeural) | `videos/aula-planejamento.mp4` |
| Tutorial da ficha (3 min 50 s, 10 cenas, gravação real com cursor) | `videos/tutoriais/tutorial-ficha-planejamento.mp4` |
| Capas | `capas/g1-h.jpg`, `g1-v.jpg`, `g1-c-aula.jpg`, `g1-c-faca.jpg`, `g1-c-resumo.jpg`, `g1-c-planilha.jpg` |

Pastas de trabalho dos vídeos apagadas. A página `docs/trilha2/index.html` não foi alterada (o integrador acrescenta o Módulo 1).

## Testes (executados nesta sessão)
| Teste | Resultado |
|---|---|
| `tests/test_logic.js` (Node: números, nível, exemplo, validações das 5 telas, 7 regras de atenção, plano, selo, leitura da Folha do Módulo 2) | 72 ok, 0 falhou |
| `tests/e2e.js` (Playwright, iPhone 13, porta 8811, jsPDF local: 5 telas, bloqueios, leituras = logic.js, PDF de 2 páginas, persistência, continuar de onde parei, botão do exemplo, importação da Folha Única, cenário com 5 alertas, desktop, sem erro de JavaScript, sem rolagem horizontal) | 66 ok, 0 falhou |
| `tests/test_planilha.py` (LibreOffice recalcula; conta independente em Python; exemplo, em branco e 19 cenários de bloqueio e leitura) | 38 ok, 0 falhou |
| Vídeos | Quadros conferidos (6 amostras da aula, 7 do tutorial); a foto op10 tinha uma pessoa e foi trocada pela op09 |
| PDFs | Resumo: 8 páginas sem transbordo (conferido em miniatura); PDF da ficha: 2 páginas, fonte correta após a quebra |
| Conformidade | Sem "consultoria", "curso", "comunidade", "mentoria", "Airbnb"; sem travessão nos textos; sem siglas na tela do membro; exemplo rotulado em todas as peças; números iguais em logic.js, planilha, roteiro, resumo e tutorial |

## Exemplo didático (dados fictícios, Cabanas do Vale, continuação do Marco Zero)
Outubro de 2026, 4 unidades, 124 noites disponíveis. Partida: ocupação 46,8%; diária R$ 280,00; resultado R$ 11.890,00 antes da retirada; nota 4,7 de 5; venda direta 30%. Metas para outubro de 2027: 50% (+3,2 pontos); R$ 300,00 (+7,1%); R$ 13.000,00 (+9,3%); 4,8 (+0,1 ponto); 40% (+10 pontos). As metas pedem 62 noites e R$ 18.600,00 de hospedagem; receita por noite disponível R$ 131,04 → R$ 150,00 (+14,5%). Donos: Ana nos cinco. Reunião: segunda-feira, 08:00, 30 minutos; primeira em 16/11/2026. Seis semanas: Módulo 2, Módulo 3, Módulo 4; compras para depois. Atenção: resultado sem a retirada. Ligação com o Módulo 2: com a Folha Única, resultado R$ 4.269,20 e ocupação de equilíbrio 28,5% (o botão da ficha importa esses números).

**Ajuste de coerência (pedido do integrador, 10/11/2026):** venda direta de partida 12% → 30% e meta 20% → 40% (+10 pontos), para bater com o Módulo 3 (Plataforma A 50% com 16%, Plataforma B 20% com 15%; comissão média 11,0%; meta de 40% até 30/06/2027). Na planilha, o mesmo mês do ano anterior passou a 24% (outubro de 2025) e 26% (novembro de 2025), com novembro de 2026 em 31%; as reuniões registram 30% e 31%. Regerados: logic.js, testes, planilhas, resumo, vídeo da aula, tutorial e capturas da demonstração.

## Decisões tomadas (detalhe no PLANO.md §11)
1. Cinco indicadores fixos do G7 (ocupação, diária média, resultado, nota, venda direta); os cinco do Marco Zero ficam ligados por uma explicação (três coincidem; "quanto entrou" e "custo por noite" seguem na Folha).
2. Meta para o mesmo mês daqui a 12 meses (regra da Etapa 09), sem régua de "meta realista": as fontes não definem método.
3. Resultado com a retirada (definição da Folha Única); quem ainda não fez a Folha marca "antes da retirada" e recebe alerta.
4. Nota e venda direta com definição-padrão de hotelaria, declarada.
5. Alçadas ficam para o Módulo 5; aqui só a pergunta "o que quebraria se você sumisse por 30 dias".
6. A ficha lê (não grava) a Folha Única do Módulo 2 pelo `../financas/logic.js`.

## Pendências e decisões para o Bruno
1. Aprovar os cinco indicadores fixos ou permitir trocar um deles (por exemplo, custo por noite vendida no lugar da venda direta, para quem só vende por plataforma).
2. Aprovar a regra "meta para o mesmo mês daqui a 12 meses" ou preferir metas como média dos 12 meses.
3. Narração sintética; regravação possível pelo `ROTEIRO.md`.
4. **Achados fora desta pasta (não alterados, para o integrador ou o dono do Módulo 2):** (a) a ficha do Módulo 2 (`docs/trilha2/financas/logic.js`, função `num`) lê "13.000" como 13; corrigido aqui no Módulo 1 com teste; (b) o PDF da ficha do Módulo 2 tem o mesmo problema que corrigi aqui: depois de uma quebra de página, o texto sai em fonte 8 porque o rodapé muda o tamanho; (c) `docs/assets/operacoes/op10.webp` mostra uma pessoa na banheira, mas o `CLAUDE.md` a lista entre as fotos sem pessoas.
5. O link "../materiais/planilhas/" da ficha aponta para uma pasta sem página de índice (igual ao Módulo 2); o integrador pode apontar para a página de ferramentas.
6. Lacunas de fonte: método de meta; definição operacional de nota e venda direta; duração e pauta da reunião só parcialmente na fonte (30 minutos, mesmos cinco números, mesma hora).

## Plano das aulas no ClickMax (para quando houver autorização; tudo desativado)
Módulo "Módulo 1 · Planejamento, metas e indicadores" (posição 1 no conteúdo Jornada 2 `f1d16209-776d-45c0-a57a-de1c8ce7dd41`), capa `capas/g1-h.jpg` (vertical `g1-v.jpg`).
| Ordem | Aula | Tipo | Conteúdo e anexos | Capa |
|---|---|---|---|---|
| 1 | Aula em vídeo · O Painel de Gestão | vídeo | `videos/aula-planejamento.mp4` | `g1-c-aula.jpg` |
| 2 | Faça agora · O meu Painel de Gestão | link externo | `trilha2/planejamento/` + anexos: tutorial `tutorial-ficha-planejamento.mp4`, as duas planilhas, `Modulo-1-Prompt-de-IA.txt` | `g1-c-faca.jpg` |
| 3 | Resumo da aula | documento | `materiais/Modulo-1-Planejamento-resumo.pdf` | `g1-c-resumo.jpg` |
| 4 | Planilha · Painel de Gestão | link + 2 anexos | `Painel-de-Gestao-Zion-EM-BRANCO.xlsx`, `...-EXEMPLO.xlsx` | `g1-c-planilha.jpg` |

## Como reproduzir
```
cd producao/jornada2/01-planejamento
node tests/test_logic.js
python3 -I src/build_planilha.py ../../../docs/trilha2/materiais/planilhas && python3 -I tests/test_planilha.py ../../../docs/trilha2/materiais/planilhas
cp src/logic.js ../../../docs/trilha2/planejamento/logic.js
(cd ../../../docs && python3 -m http.server 8811 &)
node tests/e2e.js <pasta-saida> <caminho de jspdf.umd.min.js>
python3 -I src/build_resumo.py build && node src/render_pdf.js build/resumo.html ../../../docs/trilha2/materiais/Modulo-1-Planejamento-resumo.pdf
node src/build_capas.js ../../../docs/trilha2/capas
(vídeos: ver ROTEIRO.md, "Como regerar")
```
Demonstração no celular: `demonstracao/` (capturas do e2e e o PDF do exemplo).
