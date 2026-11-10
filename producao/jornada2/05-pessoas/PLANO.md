# Jornada 2 · Gestão · Módulo 5 · Pessoas e organização das áreas · Plano da lição (G05)

Status: plano de produção (10/11/2026). Entregável: **Mapa de Pessoas e Alçadas** (página 5 do Plano de Gestão): quem faz o quê, até quanto cada um decide, e o plano de quatro semanas para tirar o dono do operacional. Não altera os módulos 0 e 2 nem ferramentas existentes; lê (sem alterar) a Folha Única do Módulo 2, se o membro já fez, para o teste de viabilidade da contratação.

## 1. A lição em uma frase
Aprenda o passo a passo para tirar a operação da sua cabeça: quem faz o quê, até quanto cada pessoa decide sem consultar você, e um plano de quatro semanas para entregar a primeira atividade.

## 2. Públicos e jornadas
- **Desenvolvedor** (vai abrir): desenha quem fará o quê antes do primeiro hóspede; as horas são previstas; o plano de quatro semanas vale para a primeira pessoa a treinar.
- **Gestor** (dono que opera): público central; mapa de hoje e saída da primeira atividade.
- **Operador** (cuida para outro dono): usa o mapa para combinar alçadas com o dono e o painel para prestar contas por exceção.
Jornada A (quero começar) e B (já opero): a abertura pergunta a situação e a ficha adapta os avisos.

## 3. Fontes Zion (mapa completo fora do repositório) e convenções
- **Panorama do Desenvolvimento Hoteleiro · Trilha B · G7 Governança e Indicadores**: «Estar presente não é gerir.»; governança como «rotinas, indicadores e alçadas que permite a operação funcionar sem o dono presente»; passo 04 «Escreva as alçadas. Até que valor cada pessoa decide sem consultar.»; exercício G7: alçadas por pessoa, em valor; o que quebraria primeiro se você sumisse por trinta dias.
- **Jornada do COMO · Etapa 10 "Como eu saio da operação?"**: P01 Inventário da Cabeça™ (40 a 80 linhas; diárias e simples, decisões sem critério e acessos costumam passar de 70%); P02 Mapa das Quatro Dependências™ (conhecimento, decisão, relação, acesso, com o que resolve e o prazo; acesso «esta semana»); P03 (dias de férias em 24 meses; última vez 7 dias sem atender); P05 Modelo de Procedimento Zion™ (seis blocos); P06 Tabela de Critérios™ (sete situações; alçada que começa baixa: «cem reais na primeira semana, trezentos no segundo mês»; registrar decisões: «treino, não controle»); P07 documento 14 «O mapa de quem faz o quê, com a alçada de cada pessoa»; P08 Perfil da Primeira Contratação™ (mais horas, menos julgamento; baixo, médio "parcial, com modelos", alto; três formatos; teste de viabilidade: equilíbrio acima de 70% → ajustar preço ou custo antes); P09 Plano de Quatro Semanas™ (sombra, acompanhada, sozinha com conferência, autonomia com alçada; conversa e sinal de cada semana; avaliação em três perguntas; «corrija depois, não durante»); P10 Painel de Acompanhamento™ (seis indicadores, dois ritmos, quatro exceções, quatro níveis de presença); P11 Escala de Resposta (citada no resumo); P12 e P13 remetem ao Módulo 7.
- **Bíblia Operacional Zion (Notion)**: seis setores (um manual por setor: hospitalidade e experiência; governança e limpeza; técnico e manutenção; gerencial e administrativo; comercial e reservas; cultura e branding); onboarding em seis etapas; rotina do gestor (diária, semanal com «definir e comunicar escala da semana seguinte», mensal com reunião de equipe).
- **Vocabulário para o membro:** "alçada" (explicada na primeira tela em que aparece: até quanto a pessoa decide sem consultar), "critério", "procedimento", "painel por exceção". Nomes com ™ só no resumo, como nomes da fonte. Sem siglas.
- **Convenções:** "Eu" (ou "eu mesma/eu mesmo") no campo "quem faz hoje" identifica o dono. Os setores da Bíblia viram o agrupamento das oito atividades da ficha (Técnico e manutenção = "Manutenção"; Cultura e branding = "Cultura e marca").

## 4. Objetivos (verbos observáveis)
1. Distinguir as quatro dependências (conhecimento, decisão, relação, acesso) e dizer o que resolve cada uma e em que prazo (compreender).
2. Mapear quem faz cada uma das oito atividades da hospedagem, com as horas do dono e o julgamento exigido (analisar).
3. Escolher a primeira atividade a delegar pela regra da fonte (mais horas, menos julgamento) e o formato da contratação (avaliar).
4. Escrever a regra e a alçada de pelo menos cinco das sete situações da tabela de critérios (criar).
5. Definir o painel por exceção: seis indicadores, ritmo semanal e mensal, e as quatro exceções com valores (aplicar).
6. Montar o plano de quatro semanas com datas, cobertura de falta e avaliação do primeiro mês, e exportar o mapa em PDF (criar).

## 5. As seis etapas
| Etapa | Peça | Duração |
|---|---|---|
| Diagnosticar | Abertura: situação, unidades, pessoas, dias de férias em 24 meses, última vez 7 dias sem atender | 1 min |
| Compreender | Aula em vídeo (13 cenas, cerca de 7 min) + resumo em PDF (8 páginas) | 7 min + leitura |
| Observar | Tutorial da ficha com o exemplo Cabanas do Vale (continuação dos módulos 0 e 2) | 4 min |
| Executar | Ficha "O meu Mapa de Pessoas e Alçadas" (5 telas) + planilha "Tarefas, Escala e Alçadas" (Comece aqui, Tarefas, Alçadas, Escala, Plano 4 semanas, Painel por exceção) | 20 a 30 min |
| Validar | Resultado em cinco partes + sete itens prontos + selo | 3 min |
| Entregar | PDF do mapa e do plano (página 5 do Plano de Gestão) + próxima etapa (Módulo 6) + prompt de IA para revisar as alçadas | 2 min |

## 6. Regras da ferramenta (testáveis; `src/logic.js`)
### 6.1 Entradas
Abertura: `situacao` (abrir, dono, operador), `unidades` (inteiro ≥ 1), `equipeHoje` e `feriasDias` (opcionais, ≥ 0), `seteDias` (nunca, mais de 12 meses, nos últimos 12).
Tela 1: `dep.{conhecimento, decisao, relacao, acesso}` (fraca, média, forte); `acessoData` (data, pedida se acesso não é fraca: aviso, não bloqueio); inventário opcional `invTotal`, `invSimples`, `invDecisao`, `invAcesso` (as três classes não passam do total).
Tela 2: para as oito atividades, `resp` (obrigatório), `horas` do dono por semana (0 a 100; vazio = 0), `julg` (baixo, médio, alto; vem marcado com a sugestão da fonte: limpeza e check-in baixo; mensagens médio; compras, financeiro e preço alto; manutenção e avaliações médio, por elaboração declarada).
Tela 3: para as sete situações, `quem`, `regra`, `alcada` (R$, opcional, ≥ 0); `alcadaInicial` (obrigatória, > 0) e `alcada2mes` (opcional; aviso se menor que a inicial).
Tela 4: `notaMin` (0 a 10), `gastoPct` (0 a 100), `diaSemanal`, `nivel` (1 a 4) obrigatórios; `quemEnvia` e `conversaMensal` opcionais.
Tela 5: `ativPlano` (já vem com a sugestão), `pessoa`, `formato`, `inicio` (data válida), `cobertura` obrigatórios; `custoMes`, `equilibrio` (quando não há Folha Única), `preAcesso`, `preProc`, `preCrit`, `tempoLivre` opcionais. Avisos de formato: meio período com menos de 4 unidades; integral com menos de 6.

### 6.2 Cálculo
- `horasTotal` e horas por julgamento. `primeira` e `segunda`: entre as atividades com horas > 0 e julgamento baixo ou médio, ordena baixo antes de médio e, dentro de cada um, por mais horas; empate: a primeira da lista; alto nunca entra. Sem candidata: "comece pelos critérios".
- Dono = `resp` "Eu", "eu mesma" ou "eu mesmo". `setoresSoDono`: setores em que todas as atividades são do dono.
- `depMaisForte`: maior força; empate na ordem decisão, acesso, conhecimento, relação (elaboração declarada: a fonte chama a de decisão de "a mais incapacitante" e manda resolver a de acesso primeiro).
- Inventário: `parteRapida = (simples + decisão + acesso) ÷ total`; leitura compara com 70% (régua da fonte).
- `criteriosEscritos`: regras com 10 letras ou mais (na planilha: 10 caracteres ou mais). `alcadasPorPessoa`: maior alçada informada por quem decide.
- Semanas: semana k vai de `inicio + 7(k−1)` a `inicio + 7(k−1) + 6`; avaliação em `inicio + 27`.
- `horasLiberadas` = horas da atividade do plano; `parteLiberada` = ÷ `horasTotal`.
- Teste de viabilidade: com a Folha Única (Módulo 2) no aparelho e `custoMes` informado, `ocupação de equilíbrio depois = max(0, (fixo total do mês + custoMes − margem das outras receitas) ÷ margem por noite) ÷ noites disponíveis`; acima de 70% = "sim" (fonte, P08). Sem a Folha, vale a resposta do membro.
- **Itens prontos (contagem, não nota; elaboração declarada):** 1 acesso fraco ou com data; 2 oito atividades com responsável; 3 pelo menos cinco regras; 4 alçada inicial > 0; 5 nota mínima, percentual e dia da leitura; 6 atividade, pessoa e cobertura; 7 data de início válida.

### 6.3 Leituras e atenção (só a fonte)
Leituras: horas por julgamento; primeira a delegar e a regra; setores só do dono; dependência mais forte com o que resolve e o prazo; inventário × 70%; regras escritas; nível de presença (texto da fonte).
Atenção, nesta ordem: nunca ficou 7 dias sem atender (a mais urgente das dez etapas); acesso não fraco (risco de continuidade); nível 2 (supervisionar tudo não é delegar); equilíbrio acima de 70% (ajustar preço ou custo antes); "não sei" (fazer a conta no Módulo 2); cada pré-requisito que falta; regras que faltam; formato incompatível com o número de unidades; sempre: não pular da semana 1 para a 4.

### 6.4 Critério de conclusão (selo)
Os sete itens prontos e o PDF baixado. O selo "Pronto para avançar" aparece na ficha; antes disso, a ficha lista o que falta.

## 7. Telas da ficha "O meu Mapa de Pessoas e Alçadas"
0 Abertura → 1 O que só você sabe (quatro dependências, data do acesso, inventário) → 2 Quem faz o quê (oito atividades por setor) → 3 Até quanto cada um decide (sete situações, alçada inicial e do segundo mês) → 4 Como acompanhar de fora (seis indicadores, quatro exceções, ritmos, nível de presença) → 5 As quatro semanas (atividade, pessoa, formato, início, cobertura, custo, viabilidade, antes da semana 1, tempo que sobra) → Resultado: mapa com alçada, indicadores, tabela de critérios, leituras, atenção, as quatro semanas com datas, antes da semana 1, integração em seis etapas, painel por exceção, avaliação, itens prontos, selo, PDF, próxima etapa (Módulo 6). Cada campo com exemplo (Cabanas do Vale). Chave local `zion-t2-pessoas`; nome e hospedagem lidos de `zion-t2-financas` ou `zion-t2-marco-zero`.

## 8. Planilha "Tarefas, Escala e Alçadas" (openpyxl, em branco e exemplo)
Abas: Comece aqui · Tarefas (oito atividades, setor, quem faz, horas, julgamento; entra na contratação; total e horas por julgamento; primeira a delegar; atividades e setores só seus; situação dos dados) · Alçadas (sete situações: quem decide, decide sozinho quando, consulta quando, alçada, revisar em; regras escritas; alçada inicial e do segundo mês; situação) · Escala (quatro funções × sete dias; dias sem ninguém; turnos por pessoa; quem substitui; situação) · Plano 4 semanas (datas pela data de início; sinal de cada semana; avaliação em três perguntas; antes da semana 1) · Painel por exceção (doze semanas, seis indicadores mais decisões fora da alçada e ocorrências de segurança; leitura "exceção" ou "relatório semanal"). Testes no LibreOffice contra conta independente.

## 9. Exemplo didático (dados fictícios, conferidos duas vezes)
Cabanas do Vale, 4 unidades, a dona opera; trabalham com ela uma diarista (paga por estadia, como na Folha do Módulo 2) e um auxiliar de manutenção. Férias em 24 meses: 0; nunca ficou 7 dias sem atender. Dependências: conhecimento média, decisão forte, relação média, acesso forte (acessos marcados para sábado, 14/11/2026). Inventário: 52 linhas, 18 diárias e simples, 14 decisões sem critério, 9 acessos → 41 (78,8%) de resolução rápida.
Horas da dona por semana (total 20, igual às 20 h da Conta da Retirada do Módulo 2): limpeza 0 (diarista, baixo); check-in e check-out 5 (eu, baixo); mensagens 6 (eu, médio); manutenção 1 (auxiliar, médio); compras 2, financeiro 2, preço 2 (eu, alto); avaliações 2 (eu, médio). Baixo 5 · médio 9 · alto 6. Primeira a delegar: **check-in e check-out**; depois, mensagens. Seis atividades só da dona; **4 de 6 setores** dependem só dela (hospitalidade, gerencial, comercial, cultura).
Critérios: 6 de 7 escritos (falta erro de calendário); cortesia até R$ 42 (15% da diária média de R$ 280 dos módulos 0 e 2); manutenção e compra até R$ 100; **alçada inicial R$ 100, segundo mês R$ 300**. Painel: nota mínima 4,7; gasto 10% acima; leitura na segunda-feira; conversa na primeira segunda do mês; nível 1 Operando.
Plano: check-in e check-out para a diarista (que já faz a limpeza), diarista por estadia, início **16/11/2026**: semana 1 de 16 a 22/11, semana 2 de 23 a 29/11, semana 3 de 30/11 a 06/12, semana 4 de 07 a 13/12; **avaliação em 13/12/2026**. Cobertura: a dona, nas folgas da diarista. **5 horas por semana saem da dona (25%)**. Custo a mais R$ 500 por mês: com a Folha do Módulo 2, a ocupação de equilíbrio vai de **28,5% para 30,7%** ((7.234 + 500 − 560) ÷ 188,68 = 38,0 noites de 124), abaixo de 70%. Antes da semana 1: tabela de critérios pronta; acessos e procedimento ainda não. Sete de sete itens prontos; falta só o PDF.
Planilha de exemplo: as mesmas tarefas e alçadas; escala com a dona em 17 turnos, diarista 6, auxiliar 3 e 2 turnos de manutenção sem ninguém no fim de semana; painel com 4 semanas fictícias e 2 exceções (gasto 12,5% acima na semana 2; nota 4,6 na semana 3).

## 10. Versão autônoma e acompanhada
Mesmo conteúdo. No acompanhamento, a equipe Zion revisa o mapa e o plano no marco da semana 6 com a rubrica (coerência 40, justificativa 30, riscos 20, clareza 10), e a data da avaliação do primeiro mês vira compromisso do encontro.

## 11. Lacunas das fontes e decisões
- A fonte não dá fórmula para somar horas de julgamento médio: ficam como "parcial, com modelos" (palavra da fonte), sem somar ao que sai.
- O "plano de quatro semanas para tirar o dono do operacional" usa o Plano de Quatro Semanas™ (treino da primeira contratação, P09), precedido do que a fonte pede antes (acessos, procedimento escrito, tabela de critérios). A saída completa da operação (6 a 8 meses, teste das duas semanas) fica para o Módulo 7.
- "Itens prontos" é contagem de itens, não nota; a Jornada 2 só tem nota no Marco Zero.
- Julgamento sugerido de manutenção e avaliações (médio) é elaboração; a fonte só classifica limpeza, check-in, mensagens, compras, preço e financeiro.
- O desempate da dependência mais forte é elaboração declarada (seção 6.2).
- A escala semanal: a fonte pede «definir e comunicar escala da semana seguinte» e «quem substitui se a pessoa faltar»; a grade de quatro funções × sete dias é elaboração.
- O Panorama lista o pilar "Pessoas e Cultura" na Trilha C sem conteúdo próprio; os manuais setoriais da Bíblia estão em grande parte "aguardando". Nenhum nome real da equipe Zion é usado.
- Temas trabalhistas (contrato, encargos, diarista × vínculo) ficam fora: a planilha e o resumo remetem ao contador.
