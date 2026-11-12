# Auditoria · A Jornada do Desenvolvimento como experiência interativa

Data: 12/11/2026 · Escopo: somente leitura. Nada foi criado nem alterado, a não ser este arquivo.
Curso auditado: "Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso" (Marco Zero + Pilares 1 a 7 + Bônus de 11 ferramentas).
Fontes: `docs/trilha1/`, `docs/dossie/`, `docs/reuniao/`, `docs/MAPA_DAS_SESSOES.md`, `producao/mentoria-desenvolvimento-360/INVENTARIO.md`, `docs/zaios/`, e o código dos projetos Lovable "Zion Dossie Aulas" e "Zion Hospitality Platform" (lido, sem escrever nada).
Não testei as telas no navegador nesta auditoria: os números abaixo vêm da leitura do código.

## Resumo (10 linhas)
1. Já existe uma jornada interativa de verdade: 8 aulas em slides (Marco Zero e Pilares 1 a 7, de 66 a 70 telas cada) e 12 ferramentas "Faça agora" (uma pergunta por tela, cálculo, PDF).
2. Cada aula embute a ferramenta do mesmo bloco, e o botão "Próximo bloco" leva à aula seguinte (`_motor/jornada.js`). A ordem Marco Zero → P1 → ... → P7 já está amarrada no código.
3. O Pilar 7 junta as páginas 0 a 7 num Dossiê de Desenvolvimento em PDF, lendo o que as outras ferramentas salvaram no aparelho.
4. O progresso é salvo no aparelho (`localStorage`). O envio ao servidor só acontece quando o aluno gera o PDF ou toca em "Enviar ao Land Bank".
5. O servidor existe: grava cada página enviada na tabela `dossie_paginas` e repassa ao Airtable do Land Bank. Mas ele só grava e nunca devolve dados: não há tela que mostre "onde cada aluno está".
6. O mentor virtual existe (`/api/feedback`, com IA, 90 s de limite, veredito Avançar/Testar/Ajustar/Pausar), mas dá feedback ao aluno sobre uma ficha, não acompanha o aluno ao longo do curso.
7. O dossiê de 8 telas da pasta `docs/dossie` é outro produto (Land Bank): vai para a tabela `dossies_landbank` e alimenta o deck da reunião (`docs/reuniao`). Não se liga ao Dossiê dos Pilares.
8. O que cobre o pedido do Bruno: viabilidade da área, cálculo de ocupação, vendável e não vendável, as oito linhas de orçamento, retorno, capital. Tudo isso é por pergunta e cálculo, não por mapa nem por Sim/Não.
9. O que não existe: mapa interativo, bloco de Sim/Não da documentação (só uma lista de documentos), calculadora "quantas cabanas de X m² cabem", orçamento de infra por item, estrutura de retorno ao investidor, plano de lançamento, lista de tarefas pendentes, painel por aluno.
10. Riscos: o botão do PDF envia os dados do aluno sem aceite próprio; referências financeiras da Zion (R$ 129.000 por unidade, ocupação 50 e 65%, margem 40%) sem fonte citada; Trilha 1 com 43 ou 58 aulas ainda sem decisão do Bruno.

## 1. Tabela etapa × recursos
Legenda: **Tem**, **Parcial**, **Não tem**. Contagem de telas = seções `<section class="s ...">` da aula.

| Etapa | Aula interativa (telas) | Sim/Não ou formulário | Mapa interativo | Cálculo | Salva progresso | Mentor IA | PDF / ficha | Lista de tarefas |
|---|---|---|---|---|---|---|---|---|
| Marco Zero | Tem (68 telas, 24 de pergunta) | Parcial: 3 níveis "Com número / Tenho uma ideia / Não sei", não é Sim/Não | Não tem | Parcial: pontuação do diagnóstico | Aparelho | Não tem (só menção) | Tem: PDF do diagnóstico, ação de 7 dias | Parcial: uma "ação de sete dias" |
| Pilar 1 · Território | Tem (66; 9 perguntas da ficha) | Parcial: a pergunta "documentos na mão" é lista de marcar (matrícula, CAR, zona, consulta prévia); o resto é número | Não tem (o texto manda olhar o CAR e o mapa da prefeitura) | Tem: matrícula menos preservação, reserva, encosta, recuos, serviço = área útil; 3 limites de unidades | Aparelho | Tem (`FEEDBACK_URL`) | Tem: Ficha do Território em PDF | Parcial: cada "Não sei" vira tarefa, mas só aparece como alerta na ficha |
| Pilar 2 · Mercado | Tem (70) | Tem formulário (números, percentuais) | Não tem | Tem: comparáveis, mediana da diária, ocupação, curva do ano | Aparelho | Tem | Tem | Parcial |
| Pilar 3 · Produto | Tem (66) | Tem (escolha, múltipla, texto) | Não tem | Parcial: tipologia, área, diária hipótese | Aparelho | Tem | Tem | Parcial |
| Pilar 4 · Modelo de negócio | Tem (69) | Tem (11 escolhas, "pensa em vender?") | Não tem | Tem: venda x renda, cenários | Aparelho | Tem | Tem | Parcial |
| Pilar 5 · Masterplan | Tem (69; simuladores "cabe" e "apoio") | Tem (6 escolhas, 4 múltiplas) | Não tem (há figuras SVG fixas) | Tem: ocupação do terreno, teto da regra, vendável x não vendável, apoio; não converte m² em número de cabanas | Aparelho | Tem | Tem: Masterplan faseado em PDF | Parcial: gatilho escrito da fase dois |
| Pilar 6 · Pré-viabilidade | Tem (66; simuladores "margem" e "escada") | Parcial (moedas e percentuais) | Não tem | Tem: oito linhas do investimento (unidade, deck, luz, água e esgoto, mobiliário e enxoval, piso, licenças e projetos, contingência), infra à parte, giro, margem, 3 cenários, tempo de volta | Aparelho | Tem | Tem | Parcial |
| Pilar 7 · Capital e Dossiê | Tem (66) | Tem (`SIMNAO` nas 3 perguntas do capital, 8 escolhas) | Não tem | Tem: pedido em 5 linhas, limite de perda, participação ilustrativa de sócio, 6 fontes | Aparelho | Tem | Tem: Dossiê completo, páginas 0 a 7 | Parcial: plano de 90 dias e compromisso de 7 dias, só dentro do PDF |
| Bônus (11 ferramentas) | Não tem (são links externos, segundo `producao/catalogo/AUDITORIA_AREAS_MEMBROS.md`) | n/a | Não tem | n/a | n/a | Não tem | Depende da ferramenta | Não tem |
| Mapa de direcionamento (extra) | Parcial: 1 página com 43 caixas de marcar | Tem (caixas) | Não tem | Parcial: barra de progresso | Aparelho (`zion_mapa_v1`) | Não tem | Não tem | Tem, mas só local |

Observação sobre o Bônus: as ferramentas de venda de R$ 19 em `producao/utilitarios/` (05 Orçamento da Cabana, 15 Comparador de Fornecedores, 18 Manutenção Preventiva, 20 Treinamento do Primeiro Turno, 29 Custos de Experiências, 30 Briefing de Experiência) são produtos separados da escada de preços. Não encontrei no repositório a lista das 11 ferramentas do Bônus do curso; só a contagem. Precisa de conferência no ClickMax.

## 2. O progresso chega a um servidor?
**Resposta curta: só em parte, e só quando o aluno clica. O servidor grava, mas ninguém consegue ler por aluno.**

Evidência:
- Salvamento no aparelho, em todas as aulas e fichas: `window.localStorage.setItem(CHAVE, JSON.stringify(S))` (`docs/trilha1/pilar7/index.html`, função `salvar`). Chaves: `zion-t1-marco-zero`, `zion-t1-aula1` a `zion-t1-aula3`, uma por pilar.
- Envio ao servidor: `const ZION_WEBHOOK_URL = "https://zion-dossie-aulas.lovable.app/api/dossie"` em marco-zero, aula1 a aula3 e pilar4 a pilar7. Nas versões antigas `aula4`, `aula5` e `aula6` a constante é `""` (envio desligado).
- Quando o envio dispara: `try { gerarPDF(L); enviarParaZion(montarPayload(L)); ... }` (`aula1/index.html`, linha 1117). Ou seja, ao baixar o PDF. Há também o botão "Enviar ao Land Bank da Zion" (`docs/trilha1/_landbank.js`), com caixa de autorização.
- No servidor, `src/lib/dossie.ts` (Zion Dossie Aulas): aceita as 8 páginas `t1-marco-zero`, `t1-aula-1`... `t1-pilar-7`, grava em `dossie_paginas` (campos `pagina`, `email`, `nome`, `ip_hash`, `payload` jsonb) e repassa para um webhook do Airtable do Land Bank. O comentário do código diz: "só grava, nunca devolve dados guardados".
- Conclusão: o dado do aluno já chega ao Supabase da Zion Dossie Aulas, página por página, com e-mail. Falta (a) uma leitura segura por aluno, (b) envio automático a cada etapa concluída (hoje só ao gerar PDF), (c) identificar o aluno de forma segura (hoje é só o e-mail digitado, sem login).
- Por que não dá para ver "onde cada aluno está" hoje: não há tela de leitura, não há login do aluno, e o progresso das telas dos slides (qual slide ele parou) não é enviado em momento algum. O que se envia é o conteúdo da ficha, não o andamento. (O ClickMax tem `member_users_get_progress`, mas mede só vídeos e aulas assistidas, não as fichas.)
- A ZAIOS (zaios.lovable.app) é a única ferramenta com persistência por associado e login por link no e-mail. Cobre P1, P2, P3, P5, P6 (receitas e viabilidade), pendências, plano e dossiê com versões. Não tem P4 nem P7 e ainda não passou por teste humano (`docs/zaios/PASSAGEM_ESTADO_ATUAL.md`).

## 3. Como o dossiê é montado e para onde vai
Existem dois dossiês diferentes. Convém não misturar.

**A. Dossiê de Desenvolvimento (páginas 0 a 7, Trilha 1)**
- Página 0 = Marco Zero; 1 a 6 = fichas de cada pilar; 7 = Capital e Dossiê. Lista `PAGINAS` em `pilar7/index.html` com a chave local de cada uma.
- O Pilar 7 lê as chaves do aparelho (`carregarChave`), marca cada página como "feita" ou "a fazer", escolhe a "página mais fraca" e gera o PDF completo com jsPDF.
- Vai para: (1) PDF baixado; (2) `/api/dossie` (tabela `dossie_paginas` no Lovable "Zion Dossie Aulas"); (3) webhook do Airtable do Land Bank (`repassarDossieAirtable`); (4) formulário `zx-lead` do ClickMax, para registrar o aluno como lead (`zionLead`). Só a página 7 junta as outras: as demais páginas só existem no aparelho de quem fez.
- Importante: se o aluno trocar de celular ou computador, o Pilar 7 não acha as páginas.

**B. Dossiê prévio do Land Bank (`docs/dossie/index.html`)**
- 8 blocos, cerca de 45 perguntas: você e o projeto, a área, documentos, mercado, produto e investimento, valor da terra, fechamento, operação atual. Tem as perguntas de documentação que o Bruno quer (urbana ou rural, zoneamento consultado Sim/Ainda não, topografia Sim/Não, escritura, ônus, cadastros, energia, água, internet, esgoto, acesso, restrições).
- Salva em `localStorage` (`zlb_dossie_v1`) e envia ao `zionhotelgroup.com/api/public/dossie-landbank`.
- Esse endpoint (projeto "Zion Hospitality Platform", `src/lib/dossieLandbank.ts`) faz `upsert` em `dossies_landbank` por e-mail, guarda arquivos no bucket `dossies-landbank` e devolve um `token`. O deck de reunião (`docs/reuniao/`) lê o token no endereço e mostra o caso.
- Respondendo à pergunta: o dossiê B conversa com `dossies_landbank`. O dossiê A (páginas 0 a 7) **não** conversa com `dossies_landbank`; vai para `dossie_paginas` e para o Airtable. Os dois não se cruzam: o aluno que fez o Marco Zero e o Pilar 1 não tem o dossiê prévio preenchido, e vice-versa. (A única ponte é o nome e o e-mail que o dossiê B puxa de `zion-t1-marco-zero`, no mesmo navegador.)

## 4. O que o Bruno pediu e NÃO existe
| Pedido | Situação |
|---|---|
| Sim/Não da documentação (matrícula, prefeitura, plano diretor, rural ou urbano, documento ambiental, água, luz, acessos) | **Parcial.** O Dossiê B (Land Bank) tem a maior parte, mas é um funil de captação. Na Trilha 1 só há "documentos na mão" (4 caixas). Falta um bloco Sim/Não único, em ordem de leigo, que mude o resto da aula conforme a resposta. Documento ambiental (licença) quase não aparece (0 menções em aula1 e no slide do Pilar 1). |
| Mapa interativo (estrada, água...) | **Não existe.** Nenhum uso de Leaflet, OpenStreetMap ou Google Maps. Só figuras SVG fixas (`pilar1-aula/figuras/10-acesso-legal.svg`, `18-energia.svg` etc.) e texto mandando o aluno olhar o mapa do CAR. |
| Calculadora de masterplan em cabanas (ex.: 10.000 m², cabanas de 50 m²) | **Não existe nessa forma.** O Pilar 1 faz área útil e 3 limites, o Pilar 5 mede quanto do terreno o desenho ocupa. Nenhum campo recebe "m² por cabana" e devolve "cabem N". O número de unidades é digitado pelo aluno. |
| Áreas vendáveis e não vendáveis | **Existe como conceito e conta no Pilar 5** (exemplo Marina: 114 m² vendáveis em 144 m² fechados, cerca de 79%), mas não por m² de terreno nem com preço da infra. |
| Preço da infraestrutura | **Parcial.** Pilar 6: luz e água por unidade e "Infraestrutura comum" como valor único, à parte, em branco por padrão. Não há planilha de infra por item (vias, rede elétrica, esgoto, portaria). |
| Orçamento de móveis, construção, enxoval, licenciamento | **Parcial, melhor cobertura do pedido.** As oito linhas do Pilar 6 cobrem unidade, deck, luz, água e esgoto, mobiliário e enxoval, piso, licenças e projetos, contingência. Também há a planilha `Orcamento-de-Abertura-Zion` em `materiais/planilhas`. Falta uma única tela de orçamento que some tudo por categoria como o Bruno descreveu. |
| Estrutura de aporte e retorno ao investidor | **Parcial.** Pilar 7: pedido em 5 linhas, 6 fontes de capital, participação "numa conta ilustrativa". Não há tabela de retorno ao investidor, nem divisão de resultado, nem prazo de devolução por investidor. |
| Plano de lançamento | **Não existe.** Há `docs/lancamento/` e o plano de 90 dias dentro do PDF do Pilar 7, mas nada interativo sobre lançar o empreendimento. |
| Tarefas pendentes do aluno | **Não existe como lista viva.** Há só: "Não sei vira tarefa" (alerta dentro da ficha), "ação de 7 dias", "90 dias" (dentro do PDF) e o Mapa de direcionamento com 43 caixas, local. Nada junta tudo num painel do aluno com prazo e estado. |
| IA por aluno (onde está cada um, para cobrar na reunião de onboarding) | **Não existe.** O `/api/feedback` responde sobre uma ficha, não guarda histórico por aluno. Nenhuma tabela relaciona aluno, etapa e pendências. |
| Material de aula ao vivo reaproveitado | **Existe em parte.** As aulas em slides têm barra e navegação por teclado (`_motor/deck.js`) e `docs/reuniao/` mostra um caso ao vivo. Falta um modo "ao vivo" (sem salvar respostas do apresentador, com exemplo fictício carregado). |

## 5. Qualidade e risco (confira em CLAUDE.md, seção 1)
1. **Envio sem aceite próprio.** O botão do PDF chama `enviarParaZion` junto com `gerarPDF` e manda nome e e-mail ao servidor sem caixa de autorização (a caixa só existe no bloco "Enviar ao Land Bank"). O texto de cabeçalho do código ainda diz "Nada é enviado". Recomendo corrigir texto e criar aceite antes de qualquer painel por aluno.
2. **Números de referência sem fonte.** Pilar 6: `REF = { l_unidade: 129000, l_deck: 15000, l_luz: 10000, l_agua: 8500, l_mobilia: 25915, ... ocup_base: 50, ocup_otim: 65, margem: 40 }`, apresentados como "Referência da Zion". São da operação da Zion? Se forem, é preciso citar a origem e a data; se forem estimativa, precisam sair ou ser marcados como tal. A régua "de 5 a 8 anos: bom" para tempo de volta (`pilar6/index.html`, linha 314) também precisa de fonte ou de rótulo "regra prática".
3. **Exemplo da Marina.** Está marcado "Exemplo ilustrativo", o que atende à regra. A regra pede a expressão "dados fictícios"; vale padronizar.
4. **Promessas.** Nas aulas, os termos de risco aparecem como aviso ("Leitura do método, não promessa", rodapé do Pilar 7). Não achei promessa de renda ou ocupação. A palavra "garantia" no Pilar 7 (27 usos) é sobre garantia e aval do crédito, não promessa. Mas o título "Projeto de Hospedagem de Sucesso" e "Do terreno ao negócio que funciona" merecem revisão jurídica, porque o curso diz mais do que "Aprenda o passo a passo".
5. **Número de aulas.** A Zaya e as páginas dizem 43; o ClickMax tem 58 ativas. Decisão do Bruno pendente (`docs/MAPA_DAS_SESSOES.md`).
6. **Aulas 4 a 6 antigas** (`aula4`, `aula5`, `aula6`) coexistem com `pilar4` a `pilar7` e têm envio desligado. Devem ser tratadas como legado.
7. **Dependências externas.** jsPDF pelo cdnjs, vídeos pelo YouTube (`youtube-nocookie`), e três endereços `lovable.app`. Se o Lovable mudar de endereço, todas as fichas quebram em silêncio, porque os erros só vão ao console.
8. **Links.** Não encontrei link quebrado óbvio por leitura; os links relativos (`../aula1/`, `../_motor/`) batem com as pastas. Não fiz teste de rede.
9. **Modelo de IA do mentor.** `mentor-ia.ts` chama o modelo `openai/gpt-6-astra` pelo gateway da Lovable, e o texto do sistema diz "nunca prometa renda, retorno, ocupação, crédito ou sociedade". A saída traz `proxima_acao` com responsável, prazo e evidência, que é um bom ponto de partida para tarefas.

## 6. O que já temos x o que falta x o que reaproveitar

**O que já temos**
- 8 aulas em slides (66 a 70 telas) e 12 fichas "Faça agora" com cálculo, salvamento local e PDF.
- Navegação em ordem entre as aulas (`jornada.js`).
- Dossiê A (PDF 0 a 7) e Dossiê B (Land Bank com token e deck de reunião).
- Servidor `/api/dossie` e `/api/feedback` com limite por IP e por e-mail, e tabela `dossie_paginas`.
- Mentor virtual com formato fixo (resumo, ponto frágil, veredito, próxima ação, critério para parar).
- ZAIOS com login, pendências, plano e dossiê com versões, para P1, P2, P3, P5, P6.
- Pipeline do Land Bank no ClickMax e a Zaya (SDR) para a conversa de onboarding.
- Mapa de direcionamento com 43 tarefas, planilhas de orçamento e estudo de massas, kit do investidor.

**O que falta**
- Bloco de Sim/Não de documentação, com desvio conforme a resposta.
- Mapa interativo (estrada, água, luz, restrições).
- Calculadora de masterplan que converta m² em número de cabanas, com áreas vendáveis e não vendáveis.
- Tela única de orçamento por categoria (infra, móveis, construção, enxoval, licenciamento).
- Estrutura de aporte e retorno ao investidor.
- Plano de lançamento.
- Lista de tarefas viva com prazo e estado.
- Identidade segura do aluno (login ou link com token) e painel de acompanhamento por aluno.
- Envio automático de progresso a cada etapa, com aceite.
- Modo aula ao vivo.

**O que reaproveitar**
- Motor de slides `_motor/deck.js` e `deck.css`, e `jornada.js` como esqueleto da ordem.
- Estrutura de perguntas das fichas (`QUESTOES`: tipo, explica, porque, onde, ondeCurto), que já gera "Não sei vira tarefa".
- As 4 caixas de documentos do Pilar 1 como semente do bloco Sim/Não.
- Simuladores do Pilar 5 (`cabe`, `apoio`) e do Pilar 6 (`margem`, `escada`) e as oito linhas de custo.
- Pilar 7 como montador do dossiê (`PAGINAS`, `montarPayload`).
- `dossies_landbank` + `docs/reuniao/` (token, leitura pública restrita) como modelo do painel por aluno.
- `/api/feedback` e o formato JSON da IA, já com `proxima_acao`, como gerador de tarefas.
- ZAIOS: login, pendências, plano e versões do dossiê. Antes de construir do zero, decidir com o Bruno se o painel por aluno nasce na ZAIOS ou em `dossie_paginas`.
- Perguntas do Dossiê B (documentos, infraestrutura, restrições) como base do bloco Sim/Não.

## 7. PROPOSTA de ordem de construção (PROPOSTA, depende de "aprovado" de Bruno)
Nada abaixo foi iniciado. Cada etapa seria uma sessão, em rascunho, sem mexer nos produtos existentes (crie turma e página novas, como pede o INVENTARIO).

**Fase 0 · Decisões (antes de construir)**
1. Bruno decide: painel por aluno na ZAIOS ou em `dossie_paginas`; número oficial de aulas (43 ou 58); texto de aceite e fonte dos números de referência.
2. Corrigir o aceite do botão do PDF e a legenda das referências (pequeno, corrige risco).

**Fase 1 · Desenvolvimento (o que o Bruno descreveu, nesta ordem)**
3. **Base comum de progresso**: identidade do aluno por link com token (modelo `dossies_landbank`), envio automático por etapa com aceite, e lista de tarefas viva (aproveitando `proxima_acao` e "Não sei vira tarefa"). Tudo depende disso.
4. **Marco Zero**: trocar o diagnóstico para Sim/Não em ordem de leigo, e criar o primeiro painel de tarefas.
5. **Pilar 1 · Território**: bloco Sim/Não de documentação (matrícula, prefeitura, plano diretor, rural ou urbano, documento ambiental, água, luz, acessos) e mapa interativo. Para o mapa, escolher biblioteca e fonte de dados sem inventar informação; dados fictícios no exemplo.
6. **Pilar 2 · Mercado** e **Pilar 3 · Produto**: ligar às tarefas; poucas mudanças de conteúdo.
7. **Pilar 4 · Modelo de negócio**: ligar às tarefas.
8. **Pilar 5 · Masterplan**: calculadora m² para número de cabanas, área vendável e não vendável, com o exemplo de 10.000 m² e cabana de 50 m² marcado como "dados fictícios".
9. **Pilar 6 · Pré-viabilidade**: tela única de orçamento (infraestrutura, móveis, construção, enxoval, licenciamento) somando as oito linhas.
10. **Pilar 7 · Capital e Dossiê**: estrutura de aporte e retorno ao investidor (sem promessa), plano de lançamento, e dossiê final com a lista de tarefas pendentes dentro.
11. **Bônus**: conferir as 11 ferramentas no ClickMax e trocar link solto por entrada dentro da jornada.
12. **Painel de acompanhamento e IA por aluno**: leitura segura por aluno (etapa atual, tarefas atrasadas, última atividade), com resumo gerado pela IA para a reunião de onboarding. Só depois de 3 a 10 estarem enviando dados.
13. **Modo aula ao vivo**: reaproveita as mesmas telas com exemplo fictício e sem salvar.

**Fase 2 · Gestão (depois)**
14. Seguir o plano já existente da Jornada 2 (`producao/jornada2/`, `docs/trilha2/`), reaproveitando a base de progresso, tarefas e painel da Fase 1. Antes, decidir o desenho (8 módulos x 6 módulos com Acelerador de Vendas, item 1 das decisões do mapa).

**Fase 3 · Operação (por último)**
15. Operação começa pela unidade O03 (limpeza) e O02 (recepção), com as ferramentas 17, 13 e 11, como já sugerido em `docs/zaios/AUDITORIA_ACADEMY_ZAIOS.md`.

Dependências: 3 antes de 4 a 13; 5 antes de 8; 8 antes de 9; 9 antes de 10; 12 só com dados chegando.
