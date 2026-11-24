# Aula 4 · CAPEX e receita · relatório (26/10/2026)

Arquivos: `aula4/ebook-aula4-capex-receita.txt` e `aula4/aula4-gravada.txt`. Os dois geradores rodam sem erro (`gen_ebook.py`: 10 seções, 30 campos, 15 quizzes; `gen_deck.py`: 39 slides, 7 seções). Não deu para ver os slides renderizados: o Playwright desta máquina não tem navegador instalado.

## E-book: 8 capítulos + 00 e ✓
00 Antes de começar (mapa, `@big`, "O que você leva", caminho, dúvidas, duas situações, como ler) · 01 O preço chegou pelo WhatsApp (a crença "o custo é a obra", 40,6% da área esquecida, os cinco erros, o palpite) · 02 CAPEX é tudo até o primeiro hóspede (componentes, terreno e giro à parte, régua de maturidade, folha de 8 linhas = vitória rápida) · 03 A área total e a infraestrutura invisível · 04 FF&E, OS&E, pré-abertura e contingência · 05 Ler como quem financia (CAPEX da Marina, sanidade, custo por chave, peso do terreno revisto, dinheiro no tempo) · 06 Cada modelo tem a sua conta (venda por unidade, por fração, renda; três cenários; mês a mês) · 07 Do faturamento ao que sobra (receita real, conta de uma linha, fixo, cascata, equilíbrio) · 08 A primeira metade do Dossiê 3 (página, veredito "testa", critério para parar, duas pessoas, Land Bank, compromisso de 7 dias, próxima aula) · ✓ (6 quizzes e glossário).

Palavras: 9.352 (wc no .txt; a Aula 1 tem 9.258). O gerador conta 10.023, porque inclui sumário e rótulos; na Aula 1 ele conta 9.816.

## Apresentação: 39 slides, 7 blocos, 3.520 palavras de fala (26,1 min a 135 ppm)
| Bloco | Slides | Palavras | Min |
|---|---|---|---|
| 1 · Abertura (capa, tres, jornada aqui 5, whatsapp, troca) | 5 | 372 | 2,8 |
| 2 · O que é CAPEX | 7 | 563 | 4,2 |
| 3 · O que fica no chão | 5 | 467 | 3,5 |
| 4 · O que equipa, opera e abre | 5 | 480 | 3,6 |
| 5 · Ler como quem financia | 5 | 476 | 3,5 |
| 6 · Quanto entra | 6 | 644 | 4,8 |
| 7 · A primeira metade do Dossiê 3 (… proxima, aqui 6) | 6 | 518 | 3,8 |

Há 3 quizzes com PAUSA: rouparia, ofurô e alavanca. Não tem slide `faca`, porque a aula não tem ferramenta. Cada foto foi usada uma vez só (11 fotos). O slide `infra` usa cards com `cols: 5`; vale conferir o layout quando renderizar.

## Contas conferidas (duas vezes)
- Área: 114 + 48 + 30 = 192 m². O que fica de fora: 78 m², 40,6% da área.
- Obra: 192 × 3.500 = 672.000 e 192 × 5.000 = 960.000. Diferença de 288.000. Por cabana de 54 m²: de 189.000 a 270.000.
- FF&E: de 120.000 a 240.000. OS&E: de 12.000 a 36.000. Pré-abertura: de 33.600 a 96.000.
- Base da contingência: 837.600 e 1.332.000. Contingência: 125.640 e 199.800, que dão 13,0% do CAPEX.
- CAPEX parcial: 963.240 e 1.531.800. Por cabana: 321.080 e 510.600. Rede: 33.333 por cabana com 3, 20.000 com 5.
- Percentuais de sanidade: 69,8/62,7; 12,5/15,7; 1,2/2,4; 3,5/6,3; 13,0/13,0.
- Infraestrutura: 100.000 vira 120.750 com pré-abertura de 5% e 126.500 com 10%.
- Peso do terreno sobre o CAPEX parcial: 600/1.563,24 = 38,4% e 600/2.131,8 = 28,1%.
- Cenários com 1.080 noites: 378 × 645 = 243.810; 415,8 × 645 = 268.191; 415,8 × 716 = 297.712,80.
- Mês a mês: 37.152, 23.220 e 12.771. Por estação: 111.456 + 92.880 + 63.855 = 268.191. No vale, 4.257 por cabana.
- Receita real: 222.598,53, ou 535,35 por noite. Contribuição: 408,90 por noite. Variável: 126,45 por noite, 52.577,91 no ano.
- Fixo: 10.500 + 1.400 + 1.100 = 13.000 por mês. Cascata: 170.020,62, depois 27.220,62 (10,2%), depois 14.020,62 (5,2%).
- Resultado mensal: +10.552,64, +1.720,40 e −4.903,78. Por estação: +31.657,92, +6.881,60 e −24.518,90.
- Equilíbrio: 381,5 noites, 35,3%, folga de 3,2 pontos.
- Cenário R$ 716: 467,12 por noite, 38.228,50 (12,8%), equilíbrio de 30,9%, folga de 7,6 pontos. Critério para parar: d = 687,75.
- Exemplo do Bruno: 10 × 500 mil = 5 milhões.

## O que tirei ou mudei das fontes antigas
- As referências antigas foram renumeradas: 2 e 3 viraram Aula 1, 4 e 5 viraram Aula 2, 6 virou Aula 3, 9 e 10 viraram Aula 5. "Sexta" e "sétima página do Dossiê" viraram "primeira metade do Dossiê 3". Tirei a "Ordem Zion em quatro etapas".
- Lançamento: "campanha de lançamento" virou "divulgação da abertura". Tirei "pré-venda" da unidade-modelo e acrescentei uma frase dizendo que divulgar e vender é Trilha 2.
- Saíram das fontes: as 7 caixas `[HISTÓRIA DO BRUNO]`; a pendência da taxa de gestão ("taxa que empata", 6,3% e 29,5%); o exemplo da pousada em julho; as tabelas das seis perguntas do terreno, dos cinco fatores da contingência, das fronteiras, da ordem do desembolso e das cinco palavras (viraram texto curto); o RevPAR; as quatro disciplinas; o custo por diária vendida; a dupla regra da pré-abertura.
- Acrescentado a partir da seção 10 das notas: a projeção por modelo (unidade, fração, renda) e os três cenários.

## Pendências para confirmar com o Bruno
1. **Cenário conservador**: o premissa de 35% (o piso da faixa da régua da Aula 1, em que a Marina cai) é construção minha, feita com números das fontes. Se ele preferir outra regra, recalcular.
2. **Cenário otimista**: os R$ 716 vêm da antiga Aula 4. Lá eles estavam "pendente de confirmação", e a Aula 2 nova precisa manter esse número.
3. **Multipropriedade**: as fontes não trazem número de frações nem valor de fração; a Marco Zero diz "conforme o mercado". Falta saber o que é o "dá 10x" das notas.
4. **"Taxa de rentabilidade"**: as notas falam nisso, mas deixei para a Aula 5.
5. **Caso Zion de Urubici** (sem luz, água e internet, e a infraestrutura entrando na conta antes da obra): está na fala do slide `varia`, marcado "confirmar com o Bruno".
6. **Coerência com as Aulas 2 e 3 em produção**: esta aula usa o escopo da Marina da antiga Aula 6 (3 cabanas de 38 + 16 m², apoio de 30 m², rede para 5, 5 vagas, 120 m de caminho, deck na crista) e as decisões da antiga Aula 4/5 (banheira, lareira, cesta das sete, opera ela mesma com uma pessoa local, lavanderia terceirizada). Os autores das Aulas 2 e 3 precisam manter esses números.

## Divergências de número
- **27% (Aula 1) e o CAPEX**: 600 ÷ 0,27 dá um investimento total implícito de cerca de R$ 2,22 milhões. Com o CAPEX parcial, o terreno pesa de 28,1% a 38,4%. O peso cai quando infraestrutura, projetos e giro entram, mas os 27% só fecham se essas três linhas somarem cerca de R$ 659 mil sobre o piso, ou cerca de R$ 90 mil sobre o teto. No e-book (cap. 5), os 27% aparecem como "estimado".
- **365 dias e meses de 30 dias**: a Aula 1 dá R$ 272.109 com 365 dias e esta aula dá R$ 268.191 com meses de 30 dias. A diferença de 1,4% está declarada no e-book, como na fonte.
- Nada contradiz os números da Marina na Aula 1: R$ 600 mil, R$ 645, 38,5%, 3 cabanas agora e infraestrutura para 5.
