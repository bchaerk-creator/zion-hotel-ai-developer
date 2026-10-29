# Zion Exercícios · Trilha 1 · especificação das 12 páginas

Uma página por aula do app "Zion Exercícios" (Lovable). Cada página abre pelo QR do slide "Faça agora" e do e-book e, na aula ao vivo, pelo link curto colado no chat e mostrado na tela. Este pacote é só especificação: nada foi publicado, enviado, nem tocado no ClickMax ou no Lovable.

Fontes usadas (só estas): `auditoria-marco-zero-escada.md` e os slides `diag360`, `diagnostico`, `calculadora` (com `ficha`, `perfis`, `pergunta`, `vitrine`, `ordem`) do Marco Zero; `auditoria-aula-2-escada.md`; `auditoria-aula-N-*.md`, `aula-NN-*.txt` e `ebook-NN-*.txt` das Aulas 3 a 12; `BRIEF-producao-trilha1.md`.

## As 12 páginas

O link curto segue o padrão `trilha-aula` (de `1-1` a `1-12`), sem acento, fácil de digitar e de ditar. O `nome_curto` dá o título legível da página. O domínio do app ainda não existe: troque `[domínio do app]` pelo endereço final antes de colar.

| Aula | Slug | nome_curto | Título | Campos | Cálculos da página (sem IA) | Página do Dossiê | Texto para colar no chat da aula ao vivo |
|---|---|---|---|---|---|---|---|
| 1 | `1-1` | marco-zero | Marco Zero · O seu diagnóstico prévio | 13 | Quantas das cinco perguntas responde; a ficha em uma linha; por onde começar pela nota de 21 pontos; ocupação imaginada contra a régua | Página 0 · A ficha de entrada | Faça o exercício agora: [domínio do app]/1-1 |
| 2 | `1-2` | territorio | Território · Quanto do seu terreno vira negócio | 14 | Área usável e %; os três preços; capacidade (menor dos quatro limites) e o limite que manda; quanto o terreno parece mais barato; peso do terreno; documentos que faltam; Não sei | Página 1 · Diagnóstico de Território | Faça o exercício agora: [domínio do app]/1-2 |
| 3 | `1-3` | mercado | Mercado · Quem paga, quanto e quando | 14 | Conta da semana (ocupação, diária média, por noite disponível); fim de semana × semana; amplitude; ocupação do ano e régua; erro do mês cheio; receita bruta por unidade (não é retorno); mês fraco; absorção (quantas cabem); alerta acima de 65% | Página 2 · Estudo de Mercado | Faça o exercício agora: [domínio do app]/1-3 |
| 4 | `1-4` | produto | Produto · O que você vende, e para quem | 14 | Lista negra na frase; momento nos quatro requisitos; três provas; faixa de tamanho; mix; hipótese de diária contra a região | Página 3 · Conceito de Produto | Faça o exercício agora: [domínio do app]/1-4 |
| 5 | `1-5` | modelo | Modelo de negócio · Quem opera, e como ganha | 14 | Operar sozinho acima de quatro unidades; as três decisões do dono; adequação; valorização como premissa; informalidade; requisitos para licenciar | Página 4 · Modelo de Negócio | Faça o exercício agora: [domínio do app]/1-5 |
| 6 | `1-6` | masterplan | Masterplan · O terreno inteiro, no tempo | 14 | Apoio sobre a área fechada (15% a 25%); rede contra o projeto completo; os três gestos do nunca; itens de apoio sem decisão; gatilho | Página 5 · Masterplan Faseado | Faça o exercício agora: [domínio do app]/1-6 |
| 7 | `1-7` | capex | CAPEX · Quanto custa abrir a porta | 14 | Área total e área esquecida; obra; FF&E e OS&E; pré-abertura; contingência e CAPEX (piso e teto); sanidade; contingência e fatores de risco; custo por unidade; teto para o briefing; degrau de maturidade | Página 6 · Mapa do CAPEX | Faça o exercício agora: [domínio do app]/1-7 |
| 8 | `1-8` | receitas | Receitas e custos · Quanto entra, quanto sobra | 14 | Noites; receita bruta e real; variável por noite; contribuição por noite; fixo completo; cascata e margem; meses que não fecham; equilíbrio e folga; custo por diária vendida; diária para 10% de margem; taxa que empata | Página 7 · Modelo de Receitas e Custos | Faça o exercício agora: [domínio do app]/1-8 |
| 9 | `1-9` | viabilidade | Viabilidade · Vale a pena, e o caixa atravessa? | 14 | Regime mês a mês; ano 1 com a rampa; ano 1 contra regime; retorno simples; giro pelas duas regras; reserva de sazonalidade; curva de 24 meses e fôlego; colchão; payback; conservador e otimista; diária que faz o conservador fechar; ruptura; hierarquia da dor | Página 8 · Estudo de Viabilidade | Faça o exercício agora: [domínio do app]/1-9 |
| 10 | `1-10` | capital | Capital e captação · A nota do projeto | 14 | Três perguntas do capital; Zion Score de Investimento; regra do conservador; reforço do colchão; Régua do Quanto Captar; participação de quem aporta | Página 9 · A nota do projeto e a estrutura de capital | Faça o exercício agora: [domínio do app]/1-10 |
| 11 | `1-11` | lancamento | Lançamento · Abrir com público, preço e reputação | 14 | Data das vendas; datas de trás para frente; vendas antes da obra; abertura contra a alta; tamanho da lista; custo da promoção; alertas de preço e de data | Página 10 · O plano de lançamento | Faça o exercício agora: [domínio do app]/1-11 |
| 12 | `1-12` | dossie | Dossiê final · O diagnóstico completo | 14 | Contagem dos vereditos; veredito do projeto pela página mais fraca; páginas que dão o ritmo; páginas completas; as quatro etapas | Dossiê final · capa e diagnóstico completo | Faça o exercício agora: [domínio do app]/1-12 |

Toda página termina com o rodapé: "Leitura do método, não promessa. Conteúdo educacional. Não é oferta de investimento nem promessa de renda, retorno, crédito ou sociedade."

## Como ler cada JSON (para quem constrói no Lovable)

- `campos`: `{id, rotulo, tipo, opcoes?, ajuda, obrigatorio, aceita_nao_sei}`. Tipos: `texto`, `numero`, `moeda`, `percentual`, `escolha`, `multipla`, `escala1a5`. `opcoes` é uma lista `{valor, rotulo}`; onde faz sentido, a última é `{"valor": "nao_sei", "rotulo": "Não sei"}`. Em campos numéricos, `aceita_nao_sei: true` pede um botão "Não sei" ao lado; a resposta grava `"nao_sei"`. Extras opcionais: `unidade`, `minimo`, `maximo` e `formato: "data"` (Aula 11).
- `calculos`: contas feitas na própria página, sem IA, na ordem da lista. Cada uma tem `formula` (pseudocódigo com os `id` dos campos e de cálculos anteriores), `leitura` (a régua da fonte), `se_nao_sei` (o que fazer quando falta dado) e `fonte`. O último cálculo de cada aula, `veredito_sugerido`, aplica as `regras_veredito`.
- `prompt_ia`: o prompt de sistema. A IA recebe `{"respostas": {...}, "calculos": {...}}` e devolve só JSON: `{resumo, pontos_fortes[], ponto_fragil, veredito, criterio_para_parar, proxima_acao{acao, responsavel, prazo, evidencia}, perguntas_em_aberto[]}`. Ela pode ser mais cautelosa que `veredito_sugerido`, nunca mais otimista. Na Aula 1, o veredito é `nao_se_aplica` (a fonte não dá veredito para a página 0).
- `saida_dossie`: o título da página do Dossiê que o resultado preenche. `pendente_bruno` repete, por aula, o que está na lista abaixo.

## O que precisa de decisão do Bruno

### Em todas as páginas
1. **O domínio do app** para o link curto (`[domínio do app]/1-N`) e o texto exato para colar no chat.
2. **Os quatro vereditos ligados às réguas.** As fontes dão as réguas e o veredito da Marina, mas raramente dizem "abaixo de X é testar". A página traduz assim, e cada tradução está em `regras_veredito`: Aula 2, os quatro caminhos (seguir, investigar, renegociar, trocar); Aula 3, as três saídas (seguir com condições, mudar algo, parar); Aula 8, a régua da margem (abaixo de 10% = testar; 10% a 20% = ajustar; 20% ou mais com folga de 10 pontos = avançar); Aulas 9 e 10, as regras do conservador e as faixas da nota; Aula 12, a ordem pausar > testar > ajustar > avançar.
3. **Rodapé**: a regra da trilha também cita "ocupação"; o rodapé pedido não cita. Manter como está ou acrescentar.

### Réguas que não estavam na fonte (o cálculo ficou de fora ou só recebe o número)
4. **Aula 1**: a fórmula da calculadora "quanto a espera já custou" e os 21 pontos do diagnóstico não estão nas fontes desta tarefa. A página só recebe o número da calculadora e a nota que o aluno já tem.
5. **Aula 1**: a página 0 não tem veredito nem critério para parar na fonte; a IA devolve "não se aplica" e a etapa de início.
6. **Aula 2**: a escala de pontos da ferramenta "Leitura do seu terreno" (11 perguntas) não está nas fontes; a página só recebe o caminho escolhido. A conta da água ficou fora para caber em 14 campos.
7. **Aula 3**: o teto da régua de ocupação, 65% (Marco Zero) ou 70% (D02). A página usa 65%. A amplitude entre 2 e 3 não tem leitura na fonte.
8. **Aula 5**: não há número mínimo de horas em horário de hóspede; a página só registra se as horas anotadas cobrem esse horário. Taxa de gestão não tem faixa nas fontes e não aparece.
9. **Aula 6**: a base da régua de apoio (15% a 25%) é a área fechada, escolha do e-book, porque a fonte não define "área construída total".
10. **Aula 7**: infraestrutura e projetos não têm faixa (ficam em branco até a cotação); a base da contingência (15% sobre a soma das outras linhas ou a régua da Etapa 02); deck pela mesma faixa por m²; "somar fatores de risco" lido como dois ou mais.
11. **Aula 8**: custos ilustrativos do e-book F02 (R$ 60 por noite, R$ 120 por estadia, fixos de R$ 10.500): a página não preenche nada por padrão.
12. **Aula 9**: o limite entre conservador "levemente" e "muito" negativo não tem número; a página mostra a razão conservador ÷ base e a IA julga. VPL e TIR ficam fora (sem taxa declarada). O giro é arredondado para cima a múltiplo de R$ 500, como no exemplo.
13. **Aula 10**: o Zion Score de Investimento tem critérios e faixas, mas não tem escala de pontos; a página só soma se o aluno der as cinco notas, e a IA trata nota sem critério como em branco. TIR sem taxa. Qual faixa de EBITDA vale (tradicional ou enxuto premium). Custo da captação calculado como percentual do que se capta.
14. **Aula 11**: o Zion Score de Lançamento não foi calculado (a Marina "não se aplica" e boa parte dele é Trilha 2).

### Exercícios cujo veredito depende de decisão pendente
15. **Aula 12 · o "final da Marina"**: o exercício não depende dele (o veredito é do projeto do aluno), e o prompt proíbe a IA de contar como a história da Marina termina. Se o Bruno escolher um final positivo, nada muda nesta página.
16. **Aulas 11 e 12 · a forma do teste de preço** (lista, pré-venda reembolsável ou outra). Sem a decisão, a página não ensina o teste, e a IA responde que é decisão aberta da trilha, com advogado e contador se envolver dinheiro de hóspede. Isso pesa nos vereditos "testar" das Aulas 8 a 12, que todos apontam para esse teste.
17. **Aula 11 · data de abertura**: começo da alta (Etapa 02) ou de quatro a oito semanas antes (Volume 7). A página mostra as duas leituras. Também: trinta reservas na primeira janela para três unidades.
18. **Aula 4 · hipótese de R$ 716** da Marina segue pendente; a página só compara a hipótese do aluno com a região. **Ponte com a Zion Glamping Store**: a condição de aluno não está confirmada; o prompt usa só "fale com a Zion; a Zion avalia".
19. **Vereditos e critérios da Marina** usados como molde, todos marcados "confirmar" nas auditorias: Aula 2 (testa), 4 (avança, preço em teste), 5 (avança), 6 (avança), 7 (avança), 8 (testa, cerca de R$ 688), 9 (testa, cerca de R$ 800), 10 (testa, e não capta), 11 (testa, e prepara sem gastar).
20. **Pontes com a Zion** nos prompts (Land Bank Zion nas Aulas 2 e 3, Zion Hotel Management nas Aulas 5 e 8): sempre "a Zion avalia cada caso", sem condição. Confirmar se a Zion Hotel Management pode ser citada a alunos da Trilha 1.

## Conferências feitas
- Os 12 arquivos passam em `python3 -m json.tool`.
- Nenhum travessão (nem em dash, nem en dash) nos 13 arquivos.
- Nenhum nome proibido pelo brief.
- Nenhuma promessa: as palavras renda, retorno, ocupação, crédito e sociedade aparecem só em regras de "nunca prometer", em rótulos de cálculo marcados "não é retorno" ou no rodapé.
- As contas do exemplo da Marina foram refeitas com as fórmulas destes arquivos e batem com os e-books (por exemplo, Aula 9: ano 1 de -R$ 60.943,02, giro de R$ 124.500, menor saldo de R$ 63.556,98, payback de 74 anos, conservador de -R$ 37.576,83, diária de R$ 798,07; Aula 8: diária de R$ 687,75 para 10% de margem).
