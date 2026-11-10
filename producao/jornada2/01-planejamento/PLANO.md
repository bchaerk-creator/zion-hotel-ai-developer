# Jornada 2 · Gestão · Módulo 1 · Planejamento, metas e indicadores · Plano da lição (G01)

Status: produzido em 10/11/2026 para revisão de Bruno. Entregável: **Painel de Gestão** (página 1 do Plano de Gestão). Nada publicado no ClickMax, nada ativado. Não altera o Marco Zero nem o Módulo 2; lê os dados que eles deixam no aparelho (nome, Folha Única) só para sugerir.

## 1. A lição em uma frase
Aprenda o passo a passo para montar o Painel de Gestão da sua hospedagem: cinco números, quem olha cada um, as metas para os próximos 12 meses e a reunião semanal de trinta minutos que mantém tudo vivo.

## 2. Públicos e jornadas
- **Desenvolvedor (vai abrir):** ponto de partida pode ficar todo em "não sei"; as metas valem para o primeiro ano de operação; a ficha avisa e pede para refazer o ponto de partida no primeiro mês aberto.
- **Gestor (dono que opera):** público central; usa o mês passado.
- **Operador (cuida para outro dono):** usa o painel para prestar contas; a pergunta "quem cuida da gestão" ativa o alerta de dono único quando há equipe.
- Jornada A (quero começar) e B (já opero) tratadas na abertura (situação) e pela regra "não sei é informação".

## 3. Fontes Zion (mapa completo fora do repositório)
- **Panorama do Desenvolvimento Hoteleiro, Trilha B, Pilar G7 · Governança e Indicadores** (espinha do módulo): "Estar presente não é gerir"; os quatro passos (cinco indicadores; quem olha cada um; reunião semanal de trinta minutos; alçadas); "Ocupação, diária média, resultado, nota e taxa de venda direta cobrem quase todo caso"; "Indicador sem dono não é acompanhado, é arquivado"; "Trinta minutos, mesmos cinco números, mesma hora"; erro comum "trocar indicador toda semana"; entregável "O Painel de Gestão com cinco indicadores, donos definidos e a rotina semanal marcada".
- **Panorama, plano de seis semanas** da Trilha B: semanas 1 e 2 o pilar mais fraco; 3 e 4 o que destrava o seguinte; 5 e 6 o que dá um número; o que deixo para depois, de propósito. "Escolha três e faça bem."
- **Panorama, G2** ("Um número, não uma intenção. E o prazo para chegar nele.") e **G6** (número de corte mensal; "Dá ao Pilar G7 os indicadores"); estudo de caso da Trilha B ("Ocupação é vaidade, margem é sobrevivência").
- **Jornada do COMO, Etapa 09:** ponto de equilíbrio como "meta visível no calendário" (Passo 09); rotina e "comparar com o mesmo mês do ano anterior, nunca com o mês passado"; no primeiro ano, a projeção como parâmetro (Passo 13).
- **Etapa 10, Passo 10 (Painel de Acompanhamento™):** acompanhamento por exceção; ocupação contra a projeção; ritmo semanal e mensal. Usado como contexto; o painel de seis indicadores da Etapa 10 é da fase de delegação (Módulo 5 e 7).
- **Bíblia Operacional (Notion), Manual Gerencial:** rotina semanal real do gestor (verificação financeira, avaliações, escala) e mensal (reunião com a equipe).
- **Marco Zero:** os cinco números do gestor e o exemplo Cabanas do Vale (área frágil 1 · Planejamento e metas; ação de 30 dias "meta de ocupação, diária e resultado para 12 meses").

**Reaproveitamento dos cinco números do Marco Zero:** o Marco Zero pergunta se o gestor sabe cinco números (entrou, sobrou, ocupação, diária, custo por noite). O painel usa os cinco do G7. Três coincidem (ocupação, diária média e resultado = "quanto sobrou"); "quanto entrou" e "custo por noite vendida" seguem na Folha Única (Módulo 2); nota e venda direta entram agora. A ficha diz isso na tela do ponto de partida e no resumo.

## 4. Objetivos (verbos observáveis)
1. Explicar por que "estar presente não é gerir" e o que é governança na fonte (compreender).
2. Nomear os cinco indicadores do G7 e calcular cada um a partir do mês passado (lembrar, aplicar).
3. Escrever uma meta numérica para o mesmo mês daqui a 12 meses em cada indicador e ler a variação (aplicar, avaliar).
4. Conferir a meta de ocupação contra a ocupação de equilíbrio e a meta de resultado contra o número de corte (analisar).
5. Atribuir um dono a cada indicador e marcar a reunião semanal (dia, hora, 30 minutos) (criar).
6. Escolher três pilares para as próximas seis semanas e o que fica para depois (avaliar, criar).

## 5. As seis etapas
| Etapa | Peça | Duração |
|---|---|---|
| Diagnosticar | Abertura da ficha: situação, quem cuida da gestão, 4 perguntas Sim/Não → nível do painel (1 a 4) | 1 min |
| Compreender | Aula em vídeo (12 cenas, cerca de 5 min) + resumo em PDF (7 páginas) | 5 min + leitura |
| Observar | Tutorial da ficha com o exemplo Cabanas do Vale | cerca de 3 min |
| Executar | Ficha "O meu Painel de Gestão" (5 telas) + planilha "Painel de Gestão" | 15 a 20 min |
| Validar | Resultado em cinco partes + critério de conclusão (selo) | 2 min |
| Entregar | PDF do Painel (página 1 do Plano de Gestão) + próxima etapa (Módulo 2) + prompt de IA | 2 min |

## 6. Regras da ferramenta (testáveis, `src/logic.js`)

### 6.1 Entradas
- Abertura: `nome`, `email`, `hospedagem`, `situacao` (abrir, dono, operador), `quem` (so, dupla, equipe), `diag` {painel, metas, donos, reuniao} Sim/Não.
- Ponto de partida: `mesBase` (texto), `dias` (28 a 31), `unidades` (1 a 999), `base_ocupacao` (0 a 100), `base_diaria` (≥ 0), `base_resultado` (aceita negativo), `resultadoSemRetirada` (booleano), `base_nota` (0 até a escala), `escalaNota` (5 ou 10), `base_vendaDireta` (0 a 100). Os cinco valores aceitam vazio ("não sei").
- Metas: `meta_*` obrigatórias nos cinco, mesmas faixas; ocupação e diária maiores que zero; resultado aceita negativo (reduzir prejuízo). Opcionais: `ocupacaoEquilibrio` (0 a 100) e `numeroCorte` (R$).
- Donos: `dono_*` (pelo menos 2 letras cada).
- Reunião: `reuniaoDia` (segunda a domingo), `reuniaoHora` (HH:MM), `reuniaoDuracao` (10 a 120; acima de 30, aviso da fonte), `reuniaoQuem`, `reuniaoOnde`, `sumisse` (opcional, ponte para o Módulo 5).
- Seis semanas: `s12`, `s34`, `s56` (módulos 2 a 7 ou Jornada 3; obrigatórios e diferentes), `s12Por`, `s34Por`, `s56Por` (opcionais), `depois` (aviso se vazio).
- Números aceitam "1.234,56", "13.000" (ponto de milhar), "4.7" (ponto decimal) e "R$"/"%".

### 6.2 Cálculo
- `noitesDisponiveis = dias × unidades`.
- Por indicador: `variacao = meta − base` (se base informada); `variacaoPct = variacao ÷ |base|` (se base ≠ 0); situação = acima, igual, abaixo, sem-base.
- `noitesMeta = metaOcupação/100 × noitesDisponíveis`; `receitaMeta = noitesMeta × metaDiária`.
- `variacaoReceita = (metaOcupação × metaDiária) ÷ (baseOcupação × baseDiária) − 1` (receita por noite disponível; elaboração aritmética).
- `sabidos` = quantos pontos de partida foram informados (0 a 5).
- Nível do painel: número de "sim" nas 4 perguntas → nível 1 (0 ou 1 sim) a 4 (elaboração declarada; nomes: Sem painel, Números soltos, Quase lá, Painel com rotina).

### 6.3 Leituras (sem régua de mercado)
1. Quantos números do ponto de partida o membro sabe ("não sei" não impede).
2. O que as metas pedem: noites e receita de hospedagem no mês de chegada, e a variação contra o ponto de partida.
3. A meta vale para o mesmo mês daqui a 12 meses; comparar junho com junho (Etapa 09).

### 6.4 Atenção (ordem)
1. `semRetirada`: resultado antes da retirada → refazer no Módulo 2.
2. `equilibrio`: meta de ocupação < ocupação de equilíbrio.
3. `corte`: meta de resultado < número de corte.
4. `semBase`: indicadores sem ponto de partida → anotar na primeira reunião.
5. `abaixo`: meta menor que o ponto de partida → pode ser decisão (estudo de caso), escrever o porquê.
6. `donoUnico`: há dupla ou equipe e os cinco donos são a mesma pessoa.
7. `longa`: reunião acima de 30 minutos.
Sempre: o erro comum do G7 ("não troque de indicador antes de 12 semanas; o valor vem da série histórica"; 12 semanas = um trimestre, a "tendência do trimestre" da fonte).

### 6.5 O que fazer e como verificar
- Plano sugerido (editável): 1. marcar a reunião (dia, hora, minutos, mesmos cinco números); 2. se houver "não sei", anotar a base na primeira reunião; depois, semanas 1-2, 3-4 e 5-6 com o pilar e o primeiro exercício.
- Como verificar: em quatro semanas, a aba Reunião semanal tem quatro linhas com os mesmos cinco números e um dono em cada; no fim das seis semanas, os três pilares com o exercício feito; daqui a 12 meses, comparar o mesmo mês com a meta.

### 6.6 Critério de conclusão (selo)
Painel completo (situação, quem, cinco metas, cinco donos, reunião com dia, hora e duração, três pilares diferentes), plano com 10 letras ou mais, data da primeira reunião e PDF baixado.

## 7. Telas da ficha "O meu Painel de Gestão"
0 Abertura → 1 O ponto de partida (com botão "usar os números da minha Folha Única" quando o Módulo 2 já foi feito no aparelho) → 2 As metas de 12 meses (com o ponto de partida ao lado e as duas conferências opcionais) → 3 Quem olha cada número → 4 A reunião semanal (pauta fixa de quatro itens) → 5 O plano de seis semanas → Resultado: painel, leituras, atenção, erro comum, seis semanas, plano editável com data, critério de conclusão, PDF, próxima etapa (Módulo 2). Chave local `zion-t2-planejamento`.

## 8. Planilha "Painel de Gestão" (openpyxl, em branco e exemplo)
Abas: Comece aqui · Metas e donos (mês de partida, noites disponíveis, escala da nota, cinco indicadores com partida, meta, dono, variação, leitura, número no mês de chegada e "meta atingida?"; o que as metas pedem; conferências de equilíbrio e corte; "Situação dos dados" que aponta o primeiro problema) · Painel 12 meses (realizado × mesmo mês do ano anterior ou projeção → Melhorou, Igual, Piorou; quantos melhoraram) · Reunião semanal (dia, hora, minutos, pauta, 13 semanas, contagem e leitura das quatro semanas) · Plano 6 semanas (três pilares, por quê, primeiro exercício, feito?, o que fica para depois, conferência de pilar repetido) · Definições e rotina.

## 9. Exemplo didático (dados fictícios, conferidos duas vezes)
Cabanas do Vale, 4 unidades, dona que opera sozinha (Ana). Continuação do Marco Zero: a área frágil foi 1 · Planejamento e metas e ela ainda não fez a Folha Única. Mês de partida outubro de 2026, 31 dias, 124 noites disponíveis.
- Ponto de partida (do Painel do Mês do Marco Zero): ocupação 46,8% (58 de 124); diária média R$ 280,00; resultado R$ 11.890,00 **antes da retirada**; nota 4,7 de 5; venda direta 12%. Sabe 5 de 5.
- Metas (outubro de 2027): ocupação 50% (+3,2 pontos); diária R$ 300,00 (+R$ 20,00, +7,1%); resultado R$ 13.000,00 (+R$ 1.110,00, +9,3%); nota 4,8 (+0,1 ponto, +2,1%); venda direta 20% (+8 pontos).
- O que as metas pedem: 50% × 124 = 62 noites; 62 × R$ 300 = R$ 18.600,00 de hospedagem; receita por noite disponível de R$ 131,04 (46,8% × 280) para R$ 150,00 (50% × 300): +14,5%.
- Donos: Ana nos cinco. Reunião: segunda-feira, 08:00, 30 minutos, "Ana, sozinha, com a planilha".
- Seis semanas: 1-2 Módulo 2 · Finanças (fechar outubro e lançar a retirada); 3-4 Módulo 3 · Preço (piso antes de subir para R$ 300); 5-6 Módulo 4 · Marketing e vendas (anotar o canal de cada reserva). Depois, de propósito: compras e estoque.
- Atenção: só "resultado sem a sua retirada". Primeira reunião: 16/11/2026.
- Planilha, aba Painel 12 meses (fictício): outubro de 2026 contra outubro de 2025 (41,9%; R$ 265; R$ 10.400; 4,6; 8%) → cinco "Melhorou"; novembro de 2026 (38,3%; R$ 285; R$ 8.950; 4,8; 14%) contra novembro de 2025 (40,0%; R$ 270; R$ 9.300; 4,6; 9%) → Piorou, Melhorou, Piorou, Melhorou, Melhorou (3 melhoraram). Reunião semanal: duas linhas (16/11 e 23/11).
- Coerência com o Módulo 2: quando a Ana fizer a Folha, o resultado de outubro com a retirada é R$ 4.269,20 e a ocupação de equilíbrio 28,5%; o botão "usar a minha Folha Única" traz esses números e a meta de resultado precisa ser refeita (é o que a atenção pede).

## 10. Versão autônoma e acompanhada
Mesmo conteúdo. No acompanhamento Zion 360°, a equipe Zion revisa o Painel no marco da semana 2 (metas, donos, reunião marcada) e a primeira reunião semanal registrada vira compromisso do encontro.

## 11. Decisões e lacunas declaradas
- **As fontes não definem como fixar a meta de 12 meses.** Decisão: meta para o mesmo mês daqui a 12 meses (aplica a regra da Etapa 09) e leituras só aritméticas, sem dizer o que é "meta realista".
- **Nota e taxa de venda direta** não têm definição operacional nas fontes: definição-padrão de hotelaria, dita como tal (nota do principal canal, sempre o mesmo; venda direta como parte da receita de hospedagem, coerente com o mix por receita do G2).
- **Resultado:** definição da Folha Única (com a retirada); o membro que ainda não fez a Folha marca "antes da retirada" e recebe o alerta.
- **Alçadas (G7, passo 04)** e "o que quebraria se você sumisse" ficam para o Módulo 5; aqui só a pergunta opcional, registrada no PDF.
- **Pauta de quatro itens da reunião** é elaboração (a fonte diz trinta minutos, mesmos cinco números, mesma hora).
- **Nível do painel** é elaboração (4 perguntas), sem nota.
- **Interface com o Módulo 2:** a ficha carrega `../financas/logic.js` para ler a Folha Única do aparelho; não grava nada na chave do Módulo 2.
