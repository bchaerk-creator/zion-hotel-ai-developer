# Módulo 4 · Marketing e vendas · Registro de produção (10/11/2026)

Entregável: **Marca e Captação** (página 4 do Plano de Gestão): marca em uma folha (para quem, promessa, prova, tom), lista própria de contatos com autorização e custo por reserva de cada canal, com a meta de venda direta. Nada publicado no ClickMax, nada ativado, nenhum commit. Nada fora de `producao/jornada2/04-marketing/` e dos arquivos novos com o número 4 ou o slug `marketing` em `docs/trilha2/`. O Kit de Mensagens (Ferramenta 11) foi reaproveitado sem alteração: a ficha e o resumo apontam para a página de vendas `https://infoprodutos-zion.clickmax.space/kit-mensagens` (decisão de 10/11/2026; antes, página de acesso `docs/p/adbc67069af26ae0/kit-mensagens-11/`).

## Arquivos publicados (`docs/trilha2/`)
| Peça | Arquivo |
|---|---|
| Ficha "A minha Marca e Captação" (abertura + 5 telas + resultado em 5 partes, selo, PDF, chave `zion-t2-marketing`) | `marketing/index.html` + `marketing/logic.js` (cópia de `src/logic.js`) |
| Planilha em branco e exemplo (Comece aqui, Marca em uma folha, Captação do mês, Lista própria, Captação 12 meses, Definições e rotina) | `materiais/planilhas/Plano-de-Captacao-Zion-EM-BRANCO.xlsx`, `...-EXEMPLO.xlsx` |
| Resumo da aula (capa + 8 páginas A4) | `materiais/Modulo-4-Marketing-resumo.pdf` |
| Prompt de IA | `materiais/Modulo-4-Prompt-de-IA.txt` |
| Aula em vídeo (5 min 01 s, 12 cenas, narração edge-tts pt-BR FranciscaNeural) | `videos/aula-marketing.mp4` |
| Tutorial da ficha (3 min 56 s, 10 cenas, gravação real com cursor) | `videos/tutoriais/tutorial-ficha-marketing.mp4` |
| Capas | `capas/g4-h.jpg`, `g4-v.jpg`, `g4-c-aula.jpg`, `g4-c-faca.jpg`, `g4-c-resumo.jpg`, `g4-c-planilha.jpg` |

Pastas de trabalho dos vídeos apagadas. A página `docs/trilha2/index.html` não foi alterada (o integrador acrescenta o Módulo 4).

## Testes (executados nesta sessão)
| Teste | Resultado |
|---|---|
| `tests/test_logic.js` (Node: números com a função `num` corrigida, nível, adjetivos genéricos, exemplo, validações das 5 telas, 10 regras de atenção em ordem, leitura do Painel do Módulo 1, plano, folha, selo) | 72 ok, 0 falhou |
| `tests/e2e.js` (Playwright, iPhone 13, porta 8814, jsPDF local: 5 telas, bloqueios, adicionar canal, "8.120" lido como oito mil, meta importada do Painel, resultado linha a linha = logic.js, PDF, selo, persistência, continuar de onde parei, botão do exemplo, cenário com 4 alertas, desktop, sem sigla, sem palavra proibida nem travessão na tela, sem erro de JavaScript, sem rolagem horizontal) | 58 ok, 0 falhou |
| `tests/test_planilha.py` (LibreOffice recalcula; conta independente em Python; exemplo, em branco e 27 cenários de bloqueio e leitura) | 51 ok, 0 falhou |
| Vídeos | Quadros conferidos (8 amostras da aula, 8 do tutorial); fotos op04, op09, op11, op12 sem pessoas; a op10 não foi usada |
| PDFs | Resumo: 9 páginas (capa + 8) sem transbordo (altura medida e miniaturas); PDF da ficha: 2 páginas, fonte correta depois da quebra (correção do Módulo 1 aplicada) |
| Conformidade | Sem "consultoria", "curso", "comunidade", "mentoria", "Airbnb"; sem travessão nos textos (o marcador de valor vazio "—" do molde virou "sem dado"); sem siglas na tela do membro; exemplo rotulado em todas as peças; números iguais em logic.js, planilha, roteiro, resumo, tutorial e Módulo 3 |

## Exemplo didático (dados fictícios, Cabanas do Vale, mesmo mês dos módulos 0 a 3)
Outubro de 2026, 25 reservas, R$ 16.240,00 de hospedagem. Plataforma A 12 reservas, R$ 8.120,00, 16% → R$ 1.299,20, R$ 108,27 por reserva; Plataforma B 5, R$ 3.248,00, 15% → R$ 487,20, R$ 97,44; Instagram com impulsionamento 2, R$ 1.120,00, gasto R$ 150 → R$ 75,00; Hóspede que volta 3, R$ 1.848,00 → R$ 0; Indicação 3, R$ 1.904,00 → R$ 0. Total R$ 1.936,40, **R$ 77,46 por reserva**, 11,9% da receita; comissão das plataformas 11,0% da receita total (Módulo 2). Venda direta **30,0%** (R$ 4.872,00; 8 de 25 reservas); meta **40% até 30/06/2027**: pede R$ 6.496,00 num mês igual e deixariam de sair **R$ 255,20** de comissão (igual ao Módulo 3). Lista: 64 contatos no celular, 0 autorizados, meta 120 em 12 meses → 10 por mês, 40% das 25 estadias. Promessa: "Duas noites a dois, com a lareira acesa e o vale na janela da cama, sem vizinho à vista." (4 de 4 testes, 4 de 5 pessoas entenderam). Atenção: lista sem autorização; guardada só no celular; nem todos entenderam a promessa. Primeiro check-in com o pedido de autorização: 20/11/2026.

## Decisões tomadas (detalhe no PLANO.md §11)
1. Folha de marca com quatro linhas obrigatórias (para quem, promessa, prova, tom) e uma opcional (o que nunca fazemos); a Etapa 05 tem nove linhas e o resumo remete a ela.
2. Custo por reserva inclui a comissão da plataforma (elaboração a partir do G2); taxa de cartão e imposto ficam na Folha Única (Módulo 2).
3. Venda direta pela receita (definição do Módulo 1); a planilha mostra também pela parte das reservas (Etapa 07).
4. Exemplo com venda direta 30% → 40% até 30/06/2027, seguindo a correção de coerência do integrador (o pedido original falava em 12% → 20%). A meta tem data, como no Módulo 3.
5. Sem régua de mercado: os percentuais de "composição saudável" da Etapa 07 ficaram de fora.
6. A ficha lê (não grava) a meta de venda direta do Painel (`zion-t2-planejamento`) e alerta se as duas metas diferem.
7. Fontes além do PLANO_G00 §4: Etapas 05 e 07 da Jornada do COMO (são fontes Zion e dão "para quem", "tom", a base de hóspedes e os quatro contatos do ano).

## Pendências e decisões para o Bruno
1. Aprovar a folha de marca em quatro linhas (ou exigir as nove da Etapa 05 nesta jornada).
2. Aprovar a comissão dentro do custo por reserva (a fonte diz só "quanto você gastou").
3. Autorização de contato: as fontes falam em "autorização explícita", sem tratar de lei de proteção de dados nem das regras das plataformas. O módulo pede conferir as regras da plataforma e procurar profissional habilitado; vale uma revisão jurídica da frase de autorização sugerida.
4. Narração sintética; regravação possível pelo `ROTEIRO.md`.
5. **Para o integrador:** o Módulo 1 ainda mostra venda direta 12% → 20% (vai ser ajustado para 30% → 40%, segundo a mensagem do integrador); com o Painel antigo no aparelho, a ficha deste módulo mostra o alerta "Meta diferente do seu Painel de Gestão", que é o comportamento esperado. O link "../materiais/planilhas/" aponta para uma pasta sem página de índice (igual aos Módulos 1 e 2).
6. Lacunas de fonte: número da meta de venda direta e do tamanho da lista; custo de aquisição por canal sem fórmula; lei de proteção de dados. Notion (Scripts de Atendimento) não consultado: a base real já está no Kit 11.

## Plano das aulas no ClickMax (para quando houver autorização; tudo desativado)
Módulo "Módulo 4 · Marketing e vendas" (posição 4 no conteúdo Jornada 2 `f1d16209-776d-45c0-a57a-de1c8ce7dd41`), capa `capas/g4-h.jpg` (vertical `g4-v.jpg`).
| Ordem | Aula | Tipo | Conteúdo e anexos | Capa |
|---|---|---|---|---|
| 1 | Aula em vídeo · Marca, lista própria e custo por reserva | vídeo | `videos/aula-marketing.mp4` | `g4-c-aula.jpg` |
| 2 | Faça agora · A minha Marca e Captação | link externo | `trilha2/marketing/` + anexos: tutorial `tutorial-ficha-marketing.mp4`, as duas planilhas, `Modulo-4-Prompt-de-IA.txt`, link do Kit de Mensagens (Ferramenta 11) | `g4-c-faca.jpg` |
| 3 | Resumo da aula | documento | `materiais/Modulo-4-Marketing-resumo.pdf` | `g4-c-resumo.jpg` |
| 4 | Planilha · Plano de Captação | link + 2 anexos | `Plano-de-Captacao-Zion-EM-BRANCO.xlsx`, `...-EXEMPLO.xlsx` | `g4-c-planilha.jpg` |

## Como reproduzir
```
cd producao/jornada2/04-marketing
node tests/test_logic.js
python3 -I src/build_planilha.py ../../../docs/trilha2/materiais/planilhas && python3 -I tests/test_planilha.py ../../../docs/trilha2/materiais/planilhas
cp src/logic.js ../../../docs/trilha2/marketing/logic.js
(cd ../../../docs && python3 -m http.server 8814 &)
node tests/e2e.js <pasta-saida> <caminho de jspdf.umd.min.js>
python3 -I src/build_resumo.py build && node src/render_pdf.js build/resumo.html ../../../docs/trilha2/materiais/Modulo-4-Marketing-resumo.pdf
node src/build_capas.js ../../../docs/trilha2/capas
(vídeos: ver ROTEIRO.md, "Como regerar")
```
Demonstração no celular: `demonstracao/` (capturas do e2e e o PDF do exemplo).

## Decisões do Bruno aplicadas em 10/11/2026
- **Kit de Mensagens (Ferramenta 11) aponta para a página de vendas** `https://infoprodutos-zion.clickmax.space/kit-mensagens` na ficha (tela 2 e complementos) e no resumo, com o texto "vendido à parte na loja Zion". No ClickMax, o anexo "Kit de Mensagens (Ferramenta 11)" da aula Faça agora (`90019d3d-…`, anexo `90cb3e82-…`) ainda aponta para a página de acesso: trocar pela URL acima (não alterado aqui).
