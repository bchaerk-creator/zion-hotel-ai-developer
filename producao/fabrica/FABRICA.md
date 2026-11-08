# Fábrica Educacional Zion 360° · Mapa, agentes, padrão de lição e plano do piloto

Comando 02 (GPT · Zion Hotel Academy) · 08/11/2026 · Documento para aprovação de Bruno. Nada foi produzido em escala; só leitura, auditoria, prompts e arquitetura. Jornada 1, produtos, ZAIOS, Land Bank, Zaya e automações não foram tocados.

## 0. Em uma página

- **Já existe** uma fábrica funcional, só que montada em três gerações: (1) a linha editorial da Mentoria Zion 360° (e-books de 120 páginas + aulas de 40 slides, 3 agentes, 1 skill, produção autônoma agendada, 52 unidades em fila), (2) a linha da Trilha 1 (fichas "Faça agora", aulas interativas, tutoriais em vídeo, planilhas, capas, ClickMax) e (3) a linha low ticket (planilhas e guias testados). A Jornada 2 (Entrega 1 do comando 01) juntou as três num padrão de lição completo e reprodutível.
- **Das oito funções pedidas, cinco já são executadas por scripts ou agentes** (roteirista, produtor audiovisual, construtor de ferramentas, revisor e testador, publicador ClickMax) de forma parcial; **duas existem só como skill ou prompt** (arquiteto pedagógico, designer editorial) e **uma não existe** (especialista hoteleiro como função separada: hoje o conhecimento vem do mapa de fontes feito por um subagente genérico).
- **Proposta:** oito agentes como prompts em `.claude/agents/` (três já existem) que compartilham os mesmos moldes, a mesma pasta por lição e o mesmo registro. A orquestração é feita pelo Claude Code, uma lição por sessão, com portões de qualidade entre as etapas (ADDIE). Nenhuma infraestrutura nova.
- **Padrão da lição:** Diagnosticar → Compreender → Observar → Executar → Validar → Entregar, mapeado nos nove itens do comando 01 e nos princípios de Merrill, Kolb, Knowles, domínio e aprendizagem cognitiva.
- **Piloto proposto:** Jornada 2 · Módulo 2 · "Finanças, fluxo de caixa e fechamento" (Gestão Financeira). Entregável: a Folha Única do mês com o custo por noite vendida, o ponto de equilíbrio e o número de corte. Plano técnico na seção 6.

---

## 1. O que já existe (auditoria da fábrica)

### 1.1 Scripts e moldes
| Função | Onde | O que faz | Estado |
|---|---|---|---|
| Ficha interativa "Faça agora" | `docs/trilha1/<pasta>/`, molde copiado em `docs/trilha2/marco-zero/` + `producao/jornada2/00-marco-zero/src/logic.js` | Telas, salvamento no aparelho, feedback em 5 partes, PDF (jsPDF), critério de conclusão | Molde testado (lógica em Node + e2e no celular) |
| App interativo de 40 telas | `producao/academy01/arsenal/` (Arsenal 01) e bônus do Club (`docs/p/adbc67069af26ae0/zar-*`) | Mini mentorias com calculadoras e relatório PDF | Prontos, reutilizáveis como ferramentas |
| Planilhas testadas | `producao/low-ticket/01-diaria-minima/build_planilha.py`, `producao/utilitarios/*/src/build_planilha.py`, `producao/clube/planilhas/src/build.py`, `producao/jornada2/00-marco-zero/src/build_planilha.py` | openpyxl, duas versões (branco e exemplo), aba Comece aqui, amarelo/verde; teste no LibreOffice contra conta independente | Molde testado |
| Aula interativa (slides ao vivo) | `docs/trilha1/apresentacao/_motor/` (deck.js) e `producao/aula_simples/gerar.py` (40 slides a partir de JSON) | Dois motores: o da Trilha 1 (HTML livre, modo apresentador, simuladores) e o das aulas simples (JSON → 40 slides com escolha, marcar, calculadora, semáforo, V/F) | Prontos |
| E-book HTML de ~120 páginas | `docs/escola/<cod>/index.html`, skill `zion-learning-design` (`references/ebook.md`, `componentes-html.md`) | Capa, sumário, capítulos com diagramas SVG, ferramenta embutida, autoavaliação, rubrica | Pronto (Z00 a D06, F00 a F02) |
| Guia/resumo em PDF | `producao/utilitarios/17-checklist-limpeza/src/build_docs.py` + `render.js`; `producao/jornada2/00-marco-zero/src/build_resumo.py` + `render_pdf.js` | HTML com identidade Zion → PDF A4 via Playwright, controle de altura por página | Molde testado |
| Vídeo tutorial (gravação real) | `producao/clube/tutoriais-video/` (record.js, make.py, card.html, specs JSON) | Grava a ferramenta com cursor e destaques, narração edge-tts, corte por cena, ffmpeg | Pronto (12 tutoriais da Trilha 1 + 1 da Jornada 2) |
| Vídeo de cenas (aula, trailer) | `producao/clube/trailer-whatsapp/` (9:16) e `producao/jornada2/00-marco-zero/video/` (16:9) | Cenas em JS (foto, título, listas, caixas, telas), narração sintética, Playwright + ffmpeg | Pronto |
| Capas | `producao/ferramentas/gerar_capas.py` (escola), `producao/utilitarios/build_entrega.py` + `render_capas.js` (produtos), `producao/jornada2/00-marco-zero/src/build_capas.js` (módulo e aulas) | HTML → JPG/PNG com fontes e logo embutidos | Prontos |
| Publicação no ClickMax | Ferramentas MCP (`content_create`, `modules_create`, `lessons_create`, `lessons_toggle_enabled`, `lessons_update` com anexos, `classrooms_add_content`, `offers_*`, `pages_*`) | Conteúdo → módulo → aulas desativadas, anexos, capas por URL do GitHub Pages | Usado na Trilha 1, na escola e na Jornada 2 |
| Produção autônoma agendada | `producao/PROMPT_PRODUCAO_AUTONOMA.md`, `producao/fila.json`, `producao/RELATORIO.md` | Tarefa agendada escolhe o próximo módulo da fila, trava, produz plano → e-book → aula → ClickMax → registro; Airtable como registro | Pronto, pausado (fila com D e F feitos; E, M, L, G, O pendentes) |
| Hospedagem pública | `docs/` (GitHub Pages) | Fichas, PDFs, vídeos, capas, planilhas | Em uso |
| Rotinas de dados | sync horário Meta → ClickMax, relatório diário | Fora da fábrica educacional, mas mostram o padrão de rotina agendada | Em uso |

### 1.2 Agentes e skills
| Nome | Tipo | Papel hoje |
|---|---|---|
| `zion-redator-capitulo` | agente (.claude/agents) | Escreve capítulos de e-book em paralelo, a partir do mapa de fontes |
| `zion-designer-aula` | agente | Converte e-book aprovado em aula de 40 slides com notas |
| `zion-revisor-pedagogico` | agente (só leitura) | Audita contra fontes, ciência da aprendizagem e checklist; devolve lista priorizada |
| `zion-learning-design` | skill (repositório) | Fluxo de produção, 12 princípios de aprendizagem, padrões de e-book, aula, avaliação, componentes HTML, checklist de qualidade |
| `zion-editorial-ebook`, `zion-brand`, `zion-brand-system` | skills (plugin) | Identidade editorial e visual |
| `ecroi`, `op3lif`, `canon-zion`, `zion-mentor`, `zion-dre-viabilidade`, `zion-stress-test`, `venda-atomica`, `logica-inversa` | skills (plugin) | Narrativa de venda, método, cânone de conteúdo, finanças de viabilidade |
| subagente "mapa de fontes" | prompt ad hoc (comando 01) | Lê Drive e Notion e devolve o mapa de fontes (frameworks, citações, números rotulados, lacunas) sem copiar texto bruto |

### 1.3 Processo que já funciona
`fila.json` → plano editorial → mapa de fontes → e-book → aula → ClickMax (desativado) → `RELATORIO.md` com decisões para Bruno. Na Jornada 2 acrescentamos: ficha com lógica testada, planilha testada, vídeo da aula, tutorial, resumo, capas, demonstração mobile, `LIMITACOES.md`.

---

## 2. Matriz de agentes e responsabilidades

| # | Função pedida | Já existe? | Como passa a funcionar | Entradas | Saídas | Prompt |
|---|---|---|---|---|---|---|
| 1 | Arquiteto pedagógico | Parcial (skill `zion-learning-design`, planos em `producao/planos/`) | Agente que escreve o plano da lição no padrão das seis etapas, objetivos observáveis, entregável, critério de domínio e versão autônoma/acompanhada | `fila.json`, mapa de fontes, plano da jornada | `PLANO_<cod>.md` | `.claude/agents/zion-arquiteto-pedagogico.md` (novo) |
| 2 | Especialista hoteleiro | Não (hoje é o subagente de fontes) | Agente que lê só fontes Zion (Drive, Notion, Panorama, Etapas) e devolve o mapa de fontes + verificação técnica do conteúdo (contas, práticas, termos) | ids das fontes, tema da lição | `MAPA_FONTES_<cod>.md` (fora do repositório), parecer técnico | `.claude/agents/zion-especialista-hoteleiro.md` (novo) |
| 3 | Roteirista de aulas | Parcial (`zion-designer-aula`, `aula_simples/gerar.py`, `ROTEIRO.md` da Jornada 2) | Agente que escreve roteiro do vídeo da aula (cenas + narração), roteiro do tutorial e o JSON das aulas interativas | plano, mapa de fontes | `ROTEIRO.md`, `scenes-*.js`, `spec-*.json`, `tutorial/*.json`, roteiro de 40 slides | `.claude/agents/zion-roteirista.md` (novo) |
| 4 | Produtor audiovisual | Sim, como scripts (`tutoriais-video/`, `trailer-whatsapp/`, `jornada2/.../video/`) | Rotina (não precisa de LLM): renderiza vídeo da aula e tutorial, confere quadros, remove pastas de trabalho | roteiros do item 3 | mp4 em `docs/<jornada>/videos/` | Checklist em `producao/fabrica/ROTINAS.md` |
| 5 | Construtor de ferramentas | Sim, como moldes (ficha, planilha, app) | Agente que implementa a lógica (`logic.js`) e a planilha a partir do plano, escreve os testes primeiro e só então a interface | plano (entradas, regras, saídas), molde | `src/logic.js`, `index.html`, `build_planilha.py`, `tests/*` | `.claude/agents/zion-construtor-ferramentas.md` (novo) |
| 6 | Designer editorial | Parcial (skills de marca; `build_resumo.py`, `build_capas.js`, `componentes-html.md`) | Agente que gera resumo em PDF, capas e cuida da identidade; não inventa layout novo, aplica os moldes | plano, roteiro, conteúdo revisado | PDF, capas, páginas | `.claude/agents/zion-designer-editorial.md` (novo) |
| 7 | Revisor e testador | Sim (`zion-revisor-pedagogico` + testes automatizados) | Agente de leitura + rotina de testes (Node, Playwright, LibreOffice, altura de páginas, quadros de vídeo) | tudo o que foi produzido | relatório priorizado + resultado dos testes | existente + `ROTINAS.md` |
| 8 | Publicador ClickMax | Sim, como ferramentas MCP | Agente que cria conteúdo/módulo/aulas desativadas, anexos e capas, confere `enabled=false` e registra ids; só ativa com "aprovado" | arquivos publicados no GitHub Pages | ids no `RELATORIO.md` | `.claude/agents/zion-publicador-clickmax.md` (novo) |

**Orquestração.** O Claude Code (sessão) é o orquestrador: lê `fila.json`, chama os agentes na ordem das etapas do ADDIE (seção 4), roda as rotinas e registra. Os agentes não falam entre si: trocam arquivos na pasta da lição. Um agente por etapa; o revisor pode rodar várias vezes.

**Compartilhamento de arquivos e padrões.** Toda lição vive em `producao/<jornada>/<nn-nome>/` com `PLANO.md`, `src/`, `tests/`, `video/`, `tutorial/`, `ROTEIRO.md`, `demonstracao/` e publica em `docs/<jornada>/`. Os moldes ficam onde estão (a Jornada 2 é o molde atual). Vocabulário, paleta, fontes, regras de promessa e de fontes estão no `CLAUDE.md`, na skill `zion-learning-design` e no `PLANO_G00.md`; todo prompt de agente começa mandando ler esses três.

---

## 3. O padrão de uma lição completa

### 3.1 Seis etapas (para o membro) e o que cada agente entrega
| Etapa | O que o membro faz | Base pedagógica | Peça da lição | Quem produz |
|---|---|---|---|---|
| **Diagnosticar** | Responde onde está no tema da lição (3 a 5 perguntas) e vê o que vai ganhar | Knowles (adulto parte do problema real e da experiência); Merrill (ativação) | Abertura da ficha + primeira cena do vídeo ("a sua situação") | Arquiteto + Construtor |
| **Compreender** | Vê o problema e a solução explicados com um exemplo didático | Merrill (demonstração); carga cognitiva; ECROI na abertura (espelhamento, colapso de crença) | Vídeo da aula (4 a 6 min) + resumo em PDF | Roteirista + Produtor + Designer |
| **Observar** | Vê a ferramenta sendo usada do começo ao fim com dados fictícios | Aprendizagem cognitiva (modelagem); Kolb (observação reflexiva) | Tutorial em vídeo + exemplo preenchido na planilha | Roteirista + Produtor |
| **Executar** | Faz com os próprios números | Merrill (aplicação); Kolb (experimentação ativa) | Ficha "Faça agora" + planilha ou calculadora | Construtor |
| **Validar** | Recebe o feedback em cinco partes e confere o critério de conclusão | Domínio (critério objetivo, feedback elaborado, repetir até cumprir) | Resultado da ficha: resultado, significado, atenção, o que fazer, como verificar + selo "pronto para avançar" | Construtor + Revisor |
| **Entregar** | Baixa o entregável e sabe qual é o próximo passo | Merrill (integração); Kolb (conceituação) | PDF do entregável (uma página do Plano) + orientação da próxima etapa | Construtor + Designer |

Mapeamento com os nove itens do comando 01: vídeo (Compreender), texto resumido (Compreender), exemplo aplicado (Compreender e Observar), exercício "Faça agora" (Executar), planilha/calculadora/checklist/prompt (Executar), tutorial (Observar), entregável exportável (Entregar), critério de conclusão (Validar), próxima etapa (Entregar).

### 3.2 Regras fixas da lição
- Uma lição = um entregável utilizável (uma página do Plano da jornada). Sem entregável, não é lição.
- Objetivos com verbos observáveis; a ficha mede exatamente esses objetivos (alinhamento objetivos → avaliação → conteúdo).
- Duas jornadas (quero começar / já opero) e os três públicos do comando 01 (desenvolvedor, gestor, operador) tratados na abertura.
- Exemplo didático sempre rotulado; números só das fontes ou inventados e declarados; sem promessa de resultado; sem preço em vídeo.
- Linguagem das aulas simples: sem sigla na tela, frases curtas, "você".
- Critério de domínio: a lição só conta como concluída quando o entregável existe (PDF) e a ação ou conta pedida está feita, com verificação declarada.
- Duração alvo: 4 a 6 min de vídeo, 8 a 12 min de ficha, 10 a 20 min de planilha; resumo de 6 a 8 páginas.

### 3.3 Metodologias existentes, integradas e não renomeadas
- **Método Zion 360°**: dá a ordem dos pilares, os entregáveis (Dossiê, Folha Única, Manual Mínimo…) e as fontes.
- **ECROI**: abertura e fechamento do vídeo e do resumo (espelhar, derrubar a crença, reenquadrar, mostrar a inevitabilidade do caminho, resultado educacional). Fora das telas de execução.
- **OP3D / OP3LIF®**: usado como lente nas lições de operação e gestão (operação, performance, pessoas, liderança, inovação e futuro) quando a fonte o traz; nome mantido como está nas fontes e na skill `op3lif`.
- Andragogia, Merrill, Kolb, domínio, aprendizagem cognitiva e ADDIE entram como **critérios de desenho e de processo**, nomeados só nos documentos internos, nunca na tela do membro.

---

## 4. Controle de qualidade (ADDIE com portões)

| Fase | Entrega | Portão (o que precisa estar verdadeiro para seguir) | Quem verifica |
|---|---|---|---|
| **Análise** | Mapa de fontes + plano da lição | Fontes só Zion; lacunas declaradas; objetivos observáveis; entregável definido; versão autônoma e acompanhada descritas | Especialista + Arquiteto; Bruno aprova o plano da jornada uma vez |
| **Desenho** | Regras da ferramenta (entradas, cálculo, faixas, ações, critério) e roteiro | Toda regra é testável; cada afirmação do roteiro tem fonte ou é rotulada como exemplo | Revisor (leitura) |
| **Desenvolvimento** | Lógica + testes, interface, planilha, vídeo, tutorial, resumo, capas | Testes de lógica (Node) e de planilha (LibreOffice) 100% verdes; e2e no celular sem erro de JS, sem rolagem horizontal, PDF gerado, estado persiste; páginas do PDF sem transbordo; quadros do vídeo conferidos; sem pessoas em fotos sem autorização | Rotinas automáticas + Revisor |
| **Implementação** | Rascunhos no ClickMax | Conteúdo não à venda, aulas `enabled=false`, anexos e capas corretos, nenhuma turma com membros ligada; `RELATORIO.md` atualizado; commit e push | Publicador; Bruno ativa |
| **Avaliação** | Dados de uso | Conclusões, tempo, dúvidas nos comentários, notas de revisão; ajustes entram como nova versão da lição | Orquestrador, mensal |

Checklists: `zion-learning-design/references/checklist-qualidade.md` (conteúdo, aprendizagem, forma) + lista da Jornada 2 (`producao/jornada2/RELATORIO.md`). Toda lição guarda os resultados dos testes no relatório (quantos passaram, o que falhou e foi corrigido).

---

## 5. Organização no ClickMax
- **Um conteúdo por jornada** ("Jornada 2 · Gestão", id `f1d16209…`; Jornada 3 e Formação quando aprovadas). Não à venda até Bruno aprovar.
- **Um módulo por lição**, na ordem do plano, com capa h/v e descrição que diz o entregável.
- **Quatro aulas por módulo, sempre na mesma ordem:** Aula em vídeo (tipo vídeo) → Faça agora (link externo, anexos: ficha, tutorial, planilha) → Resumo (documento PDF) → Planilha/ferramenta (link + anexos). Comentários ligados no Faça agora (dúvidas do membro viram insumo da Avaliação).
- **Turmas:** "Jornada 2 · Gestão · Membros" (autônomo) e "Acompanhamento Zion 360° · Turma N" (acompanhado), as duas com o mesmo conteúdo; a diferença está no calendário do portal (encontros), nos comentários respondidos pela equipe e nos marcos de revisão. Nenhuma turma é criada antes do "aprovado".
- **Liberação:** módulos liberados em dias após a compra para a turma autônoma (ritmo sugerido: 1 módulo por semana) e por data para a turma acompanhada (calendário de 12 semanas).
- **Tags/campos** (propostos, para medir conclusão sem persistência externa): tag por lição concluída aplicada pela equipe no acompanhamento; para o autônomo, o progresso de aula do ClickMax + o PDF que o membro guarda. Persistência real só no ZAIOS (seção 8).
- Os conteúdos "Arquivo · Trilha 2/3/4" e a Trilha 1 ficam intocados.

---

## 6. Módulo-piloto · Gestão Financeira (Jornada 2 · Módulo 2 · Finanças, fluxo de caixa e fechamento)

**Por que este:** é o pilar que "dá um número" (regra do Panorama: comece por ele), tem as fontes mais completas (Etapa 09 inteira + G6) e reaproveita três ferramentas prontas.

**Entregável:** a **Folha Única do mês** (página 2 do Plano de Gestão): receita real, custo variável por noite, custo fixo do mês (com a retirada do dono), custo por noite vendida, margem de contribuição, ponto de equilíbrio em noites e em ocupação, meses de fôlego e o número de corte. Em PDF, com a leitura e a ação de 30 dias.

**Objetivos (verbos observáveis):** distinguir caixa, resultado e patrimônio; calcular a receita real a partir do bruto; separar custo variável de fixo e incluir a retirada; calcular custo por noite vendida e ponto de equilíbrio; decidir sobre um desconto pela regra das três faixas; produzir a Folha Única com uma decisão.

**Seis etapas:**
1. Diagnosticar: 4 perguntas (separa conta pessoal da hospedagem? sabe o custo por noite? tem reserva para a baixa? a retirada tem valor fixo?) → nível da Linha de Separação (1 a 4) e ganho esperado.
2. Compreender: vídeo de 5 min (três contas; seis causas de "faturar muito e não sobrar"; custo variável × fixo; custo por noite; ponto de equilíbrio; regra do desconto) + resumo de 8 páginas.
3. Observar: tutorial da calculadora e da planilha com o exemplo "Cabanas do Vale" (continuidade do Marco Zero).
4. Executar: ficha "A minha Folha Única" (entradas guiadas com "por que", "onde conseguir" e exemplo) + planilha "Folha Única e Fluxo de 12 meses" (abas Comece aqui, Receita real, Custos, Folha Única, Fluxo 12 meses, Reservas).
5. Validar: feedback em 5 partes (resultado: custo por noite × diária média; significado: faixa da ocupação de equilíbrio, 45 a 65% saudável, acima de 70% alerta, pela fonte; atenção: a causa principal entre as seis; o que fazer: a ação de 30 dias na ordem da fonte (duodécimo das anuais → reserva de sazonalidade → retirada → diária e custo); como verificar).
6. Entregar: PDF da Folha Única + próxima etapa (Módulo 3 · Preço).

**Ferramentas reaproveitadas:** Ferramenta 01 · Diária Mínima (lógica de taxa, limpeza por estadia e meta), bônus "Calculadora de Custos e Rentabilidade" (zar-a03) e "Calculadora de Receitas Extras" (zar-a08) apontados como complementos; Painel do Mês do Marco Zero como entrada.

**Plano técnico (uma sessão, cerca de um dia de produção):**
| Passo | Agente/rotina | Saída | Teste |
|---|---|---|---|
| 1 | Especialista hoteleiro | `MAPA_FONTES_G02.md` (Etapa 09 passos 01 a 13; Panorama G6; Notion rotina financeira) | lista de lacunas |
| 2 | Arquiteto pedagógico | `PLANO.md` (objetivos, regras de cálculo, faixas, ações, critério, versão acompanhada) | revisão de Bruno opcional |
| 3 | Construtor | `src/logic.js` (receita real, custo variável/fixo, custo por noite, margem, ponto de equilíbrio, ocupação de equilíbrio, fôlego, causa principal, faixa do desconto) + `tests/test_logic.js` escritos antes da interface | ≥ 30 testes, inclusive bordas (zero noites, taxa 100%, estadia de 1 noite) |
| 4 | Construtor | `build_planilha.py` + `tests/test_planilha.py` | recálculo no LibreOffice, ≥ 25 testes |
| 5 | Construtor | `docs/trilha2/financas/index.html` (ficha, molde do Marco Zero) | e2e no iPhone 13 (≥ 30 verificações), PDF, persistência |
| 6 | Roteirista | `ROTEIRO.md`, `scenes-g02.js`, `spec-g02.json`, `tutorial/ficha-financas.json` | leitura do revisor (fontes e promessas) |
| 7 | Produtor (rotina) | `aula-financas.mp4` (16:9), `tutorial-ficha-financas.mp4` | quadros conferidos, pastas de trabalho apagadas |
| 8 | Designer editorial | resumo PDF, capas h/v e das 4 aulas | altura das páginas, fontes embutidas |
| 9 | Revisor | relatório priorizado; correções aplicadas; testes rodados de novo | tudo verde |
| 10 | Publicador | módulo 2 no conteúdo `f1d16209…`, 4 aulas desativadas, anexos; `RELATORIO.md`; commit e push | `enabled=false` conferido |

---

## 7. A mesma lição para o membro autônomo e para o acompanhamento Zion 360°

| Camada | Autônomo (R$ 270 por jornada, proposta) | Acompanhamento Zion 360° (R$ 2.900, proposta, 12 semanas) |
|---|---|---|
| Conteúdo e ferramentas | Idênticos | Idênticos |
| Ritmo | 1 módulo por semana liberado, sem prazo | Calendário de 12 semanas no portal (8 módulos + 4 semanas de aplicação e revisão) |
| Modelagem (aprendizagem cognitiva) | Tutorial em vídeo e exemplo didático | + encontro semanal em grupo: a equipe Zion resolve um caso real anonimizado ao vivo com a ferramenta |
| Treino e apoio | Feedback automático da ficha | + comentário da equipe no entregável em três marcos (semanas 2, 6 e 12), com a rubrica da skill (coerência 40, justificativa 30, riscos 20, clareza 10) |
| Retirada gradual do apoio | Não se aplica | Semanas 1 a 4 com revisão de todo entregável; 5 a 8 só nos marcos; 9 a 12 o membro apresenta o plano e recebe o parecer final |
| Critério de conclusão | Selo da ficha + PDF | Selo + revisão aprovada da equipe no marco |
| O que não se promete | Resultado, renda, retorno | Idem; nem acompanhamento individual ilimitado, aprovação de projeto, financiamento ou parceria |

Na ficha, uma única diferença técnica: um campo opcional "turma" (lido do link de acesso) que muda o texto de "próxima etapa" (autônomo: "siga para o módulo X"; acompanhado: "leve este PDF ao encontro da semana N"). Sem envio de dados até o ZAIOS existir.

---

## 8. Limitações técnicas a resolver
1. **Persistência dos entregáveis**: só no aparelho; sem consolidação nem visão da equipe. Proposta em `producao/jornada2/LIMITACOES.md` (endpoint no ZAIOS, consentimento, recuperação por e-mail). É o que destrava o acompanhamento em escala.
2. **Player de vídeo do ClickMax**: a Trilha 1 usa YouTube não listado; a Jornada 2 apontou o mp4 do site. Conferir no portal; se não tocar, subir no YouTube (manual, sem custo).
3. **Narração sintética**: aceitável para piloto; Bruno pode regravar com o roteiro. Áudio humano exige gravação dele.
4. **Fontes privadas**: Drive e Notion lidos por subagente; o texto bruto nunca entra no repositório público. Lacunas (RevPAR, DRE linha a linha, tributação, PMS) precisam de nova fonte ou de redação marcada como elaboração.
5. **Ambiente**: Unsplash e cdnjs bloqueados nos testes (jsPDF servido localmente); GitHub Pages é público (endereços discretos, não secretos); créditos de WhatsApp do ClickMax e do Lovable fora desta fábrica.
6. **Tamanho do repositório**: vídeos de 6 a 20 MB por lição; 8 lições por jornada cabem, mas convém mover os vídeos para YouTube não listado ou Drive quando passar de uns 300 MB.
7. **Conta de vendedor pendente**: nenhuma oferta vende até a aprovação; a fábrica produz, mas a monetização espera.

## 9. O que pode ser automatizado sem custo adicional
- Geração e teste de lógica, planilhas, PDFs, capas e vídeos (scripts existentes, só tempo de máquina).
- Criação de módulo e aulas no ClickMax, anexos, desativação e registro (ferramentas MCP).
- Mapa de fontes por subagente e revisão pedagógica por agente de leitura.
- Fila e trava de produção (`fila.json`), relatório e commit (padrão já em uso).
- Rotina agendada de produção (uma lição por execução), como a produção autônoma da escola, **só depois da validação do piloto** e com "aprovado".
- Com custo: gravação humana, YouTube com miniaturas personalizadas (manual), persistência no ZAIOS (desenvolvimento), créditos de WhatsApp para avisos.

## 10. Como medir conclusão e qualidade
**Conclusão (por lição):** critério objetivo na ficha (entregável gerado + ação ou conta feita + verificação declarada) → selo. No ClickMax: progresso de aula e, no acompanhamento, tag "Lição N · entregue" aplicada pela equipe após a revisão. Indicadores: % de membros com PDF gerado (declarado nos comentários ou visto no marco), tempo médio até concluir, módulos iniciados × concluídos.

**Qualidade do entregável:** rubrica 40/30/20/10 (coerência, justificativa, riscos, clareza) aplicada pela equipe no acompanhamento; no autônomo, autoavaliação de 4 perguntas no fim da ficha (proposta para as próximas lições).

**Qualidade da lição (fábrica):** testes 100% verdes antes de publicar; zero achados bloqueantes do revisor; dúvidas recorrentes nos comentários viram ajuste na versão seguinte; nota média da aula no ClickMax (avaliações ligadas).

**Resultado de aprendizagem:** o Diagnóstico de Gestão repetido no fim da jornada (mesma ficha, módulo 7) mostra a mudança de nível por área: é a medida de domínio da jornada inteira, sem prometer resultado financeiro.

---

## 11. O que depende de Bruno para a produção começar
1. Aprovar o padrão da lição (seção 3) e a matriz de agentes (seção 2).
2. Aprovar o piloto de Gestão Financeira como Módulo 2 da Jornada 2 (ou indicar outro).
3. Decidir vídeo no site ou YouTube não listado, e narração sintética ou própria.
4. Confirmar os nomes comerciais (Jornada × Trilha) e os preços como proposta.
5. Dar o "aprovado" para a sessão de produção do piloto (uma sessão, rascunhos desativados no ClickMax).
