# Comando 01 · Auditoria e arquitetura da Fábrica Educacional Zion 360°

Data: 08/11/2026 · Executor: Claude Code · Responsável: Bruno Chaerk · Status: **relatório para avaliação**.
Só leitura e planejamento: nada foi criado, publicado ou alterado no ClickMax, na ZAIOS, no Lovable, no Notion ou no site. Nenhum crédito Lovable foi gasto.

O roteiro de teste da ZAIOS é referência de validação humana. **Ele ainda não foi executado.** Nada neste relatório trata a ZAIOS como validada.

---

## 1. O que já está pronto

| Bloco | Evidência |
|---|---|
| **Jornada 1 · Desenvolvimento** no ClickMax | Curso com 9 módulos (Marco Zero, Pilares 1 a 7, Bônus) e 58 aulas, em 2 turmas. Cada pilar segue o mesmo molde: aula interativa (link), 2 vídeos de cerca de 6 minutos (YouTube não listado), "Faça agora" (ficha que gera a página do Dossiê) e e-book em PDF |
| Materiais da Jornada 1 | `docs/trilha1/`: 12 fichas interativas, 16 apresentações, 10 PDFs, 12 tutoriais em vídeo, 12 trailers, 2 planilhas, Kit do Investidor (modelos .pptx e .docx) |
| Método Zion 360° | 17 de 52 unidades com e-book e aula de 40 slides (Z00–Z02, D00–D06, F00–F06) em `docs/escola/`. Todas "pronto para revisão": **nenhuma aprovada** |
| Sistema pedagógico | Skill `.claude/skills/zion-learning-design/`: desenho reverso com Bloom, 12 princípios com evidência (prática de recuperação, espaçamento, codificação dupla, carga cognitiva, exemplos resolvidos, feedback), 9 eventos de Gagné, avaliação por nível, checklist de qualidade |
| Agentes de produção | `.claude/agents/`: redator de capítulo, designer de aula (40 slides), revisor pedagógico (só leitura) |
| Fila de produção | `producao/fila.json` (51 módulos, trava por sessão) + `producao/PROMPT_PRODUCAO_AUTONOMA.md` |
| Ferramentas interativas | 20 mini mentorias (A01–A10, B01–B10) no motor `producao/zion-arsenal/app/`, com 1.196 verificações de navegador (A01, A02, A03, A06 e A07 rodadas de novo hoje: 295 de 295) |
| Planilhas utilitárias | 6 prontas (01, 11, 13, 14, 17, 29), com versão em branco e com exemplo, guia e PDF imprimível. Testadas hoje recalculando no LibreOffice contra uma regra independente (01, 11, 13, 14, 17: 109 de 109) |
| Fábrica de vídeo | 3 geradores sem custo e sem API paga: roteiro JSON → voz sintética → gravação da tela real com Playwright → ffmpeg |
| Capas, páginas de acesso, PDFs | `producao/utilitarios/build_entrega.py` + `render_capas.js`, `build_docs.py` + `render.js`, `producao/ferramentas/gerar_capas.py` |
| ZAIOS | 13 exercícios e ferramentas, motor de cálculo testado (396 testes), Dossiê em PDF. **Falta o teste humano** |
| Premissas e decisões | `docs/zaios/PREMISSAS_FINANCEIRAS_E_VERIFICACOES.md` e `DECISOES.md`: premissas decididas para a versão 0, uma regra só entre material e ZAIOS |
| Bíblia Operacional Zion | No Notion (não no repositório): manuais de Governança e Limpeza, Técnico e Manutenção, Gerencial e Administrativo, Hospitalidade e Experiência, Onboarding e uma Biblioteca de Vídeos da operação real (numerados V01 em diante) |

## 2. O que está incompleto

1. **Jornadas 2 e 3 não têm conteúdo.** As unidades G00–G06 e O00–O06 estão "pendente" na fila e não têm plano editorial (`producao/planos/` só tem D, F, Z e T00).
2. **No ClickMax, as turmas e os produtos "Trilha 2 · Gestão", "Trilha 3 · Operação" e o Combo estão arquivados**, sem aulas.
3. **POPs não existem.** Há checklists e planilhas, mas nenhum procedimento operacional escrito.
4. **Vídeo-aula narrada a partir de slides não existe.** Os geradores fazem tutorial de ferramenta e trailer, não a aula.
5. **Fábrica de vídeo não é portátil.** O gerador com voz Piper aponta para pastas de outra sessão e o Piper não está instalado. O gerador com edge-tts depende de um serviço gratuito da Microsoft, sem garantia.
6. **Scripts de montagem do e-book e de exportação em PDF não estão no repositório.** Foram escritos a cada sessão.
7. **Templates para membros:** não há modelos de prompt de IA; só os modelos do Kit do Investidor e as mensagens do Kit 11.
8. **Nomes divergentes na Jornada 1:** pilares com nomes diferentes nos e-books, no ClickMax e no índice de ferramentas; páginas de venda falam em 43 aulas e o ClickMax tem 58.
9. **Os 17 e-books do Método 360° aguardam revisão.**
10. **A conta de vendedor do ClickMax segue em análise** (conferido hoje): nenhum checkout vende.

## 3. Agentes e funções que já existem

| Função pedida | O que já existe | Situação |
|---|---|---|
| 1 Arquiteto pedagógico | Skill zion-learning-design, planos editoriais, fila, mapa do Ciclo 01 | Existe como processo, sem agente. Falta a lição de 6 passos e os planos G e O |
| 2 Especialista hoteleiro | Nada como agente. O conhecimento está na Bíblia Operacional (Notion) e no Bruno | Falta |
| 3 Roteirista de aulas | Redator de capítulo, designer de aula, `producao/aula_simples/` (17 roteiros JSON) | Existe para e-book e slides. Falta roteiro de vídeo curto |
| 4 Produtor audiovisual | `producao/clube/tutoriais-video/`, `producao/zion-arsenal/tutorial/`, `producao/zion-arsenal/promo/`, `producao/clube/trailer-whatsapp/` | Existe como script. Precisa virar um só, portátil |
| 5 Construtor de ferramentas | Motor do Arsenal + `docs/AUTHORING.md`, moldes de planilha (`build_planilha.py`), fichas da Trilha 1 | Existe e está testado |
| 6 Designer editorial | Designer de aula, CSS do Z00, `build_docs.py`, `build_entrega.py`, capas | Existe. Falta guardar o montador do e-book |
| 7 Revisor e testador | Revisor pedagógico, checklist de qualidade, `tests/run.js`, `test_planilha.py` | Existe. Falta checagem automática de harmonia com a ZAIOS |
| 8 Publicador ClickMax | Receitas no `CLAUDE.md` §3 e §5 e no prompt de produção; registro de ids em `OFERTA.md` e `control/` | Existe como receita manual pela sessão principal. Não precisa de agente |

Também existe `src/` (um aplicativo de linha de comando em Python com agentes OpenAI e um "Zion Score"). Nenhum script de produção usa esse código. **Não deve ser reaproveitado**, para não criar uma segunda pontuação (decisão de 08/11: Zion Score fora da ZAIOS).

## 4. Agentes que realmente precisamos criar

Oito agentes independentes seriam redundantes. A sessão principal já orquestra, e cinco das oito funções existem. Proposta: **2 agentes novos, 1 agente ampliado e 2 scripts.**

| Novo | Tipo | Por quê |
|---|---|---|
| `zion-arquiteto-modulo` | Agente | Transforma uma unidade G ou O em plano de módulo: objetivo de cada lição nos 6 passos, entregável, ferramenta, critério de domínio, ligação com o pilar da ZAIOS e com o dicionário único. Hoje isso é refeito a cada sessão |
| `zion-curador-fontes` | Agente (só leitura) | Faz o papel do especialista hoteleiro: lê a Bíblia Operacional e os manuais e devolve fichas de fonte anonimizadas (procedimento, padrão, erro comum, vídeo de apoio), com a marca "a validar pelo Bruno". Não publica nada |
| `zion-designer-aula` ampliado | Agente existente | Ganha o modo "roteiro de vídeo curto" (6 a 8 minutos, por cena), no lugar de um roteirista novo |
| `producao/fabrica/video` | Script | Junta os três geradores num só, com caminhos relativos, voz instalada no projeto e três saídas: vídeo-aula a partir de slides, tutorial de ferramenta e corte vertical |
| `producao/fabrica/checar` | Script | Testador único: links, leitura em 360 px e 1280 px, linguagem proibida, números contra o dicionário único e as premissas, presença dos 6 passos |

Os demais (construtor de ferramentas, designer editorial, publicador) seguem como moldes e receitas já testados.

## 5. Metodologia recomendada e como aplicar

As seis referências pedidas não aparecem no repositório hoje. Elas se encaixam no que já existe sem trocar nada:

| Referência | Onde entra | Já existe algo parecido? |
|---|---|---|
| **ADDIE** | O processo da fábrica: Análise (curador + plano), Desenho (arquiteto), Desenvolvimento (redator, designer, vídeo, ferramenta), Implementação (ClickMax), Avaliação (testador + teste com membros + indicadores) | Sim: os 7 passos da skill já são um ADDIE. Basta nomear e acrescentar a Avaliação depois de publicar |
| **Andragogia (Knowles)** | Cada lição parte de um problema real do membro, mostra por que importa e deixa o membro escolher o caminho (perfil Começar ou Crescer, "Não sei" aceito) | Sim: as Jornadas A e B da skill e o "Não sei" da ZAIOS |
| **Primeiros Princípios de Merrill** | A espinha da lição: problema real → ativação → demonstração → aplicação → integração | Parcial: Gagné já cobre ativação e demonstração |
| **Kolb** | O ciclo dentro da lição: experiência (diagnóstico), reflexão, conceito, experimentação (executar na própria hospedagem) | Não |
| **Cognitive Apprenticeship** | Modelar (vídeo mostrando o especialista fazendo), treinar (exercício guiado com dica), retirar o apoio (o membro faz sozinho no próprio caso) | Sim: exemplos resolvidos e retirada gradual estão na skill |
| **Aprendizagem por domínio** | Cada lição tem critério de domínio. Quem não atinge volta ao passo indicado, sem avançar | Não. Só os vereditos da ZAIOS |

ECROI continua só na abertura e no fechamento dos materiais de venda e do e-book, nunca dentro da lição (regra atual). OP3D continua como método de priorização nos dossiês. Os sete pilares e as 52 unidades não mudam.

## 6. Padrão obrigatório de cada lição

**Diagnosticar → Compreender → Observar → Executar → Validar → Entregar**

| Passo | O que o membro faz | Formato padrão | Base |
|---|---|---|---|
| 1 Diagnosticar | Responde de 3 a 5 perguntas sobre a própria hospedagem e vê onde está | Quiz curto ou ficha (ou o pilar da ZAIOS, quando existir) | Andragogia, Merrill (ativação), Kolb (experiência), pré-teste do domínio |
| 2 Compreender | Entende o conceito e o porquê | Vídeo de 6 a 8 minutos + trecho do e-book | Merrill (demonstração), codificação dupla, carga cognitiva |
| 3 Observar | Vê o procedimento feito por inteiro, num caso de exemplo (dados fictícios) | Tutorial gravado da ferramenta ou do POP, exemplo resolvido | Cognitive apprenticeship (modelar) |
| 4 Executar | Faz no próprio caso | Planilha, checklist, template ou ferramenta | Merrill (aplicação), Kolb (experimentação), treino com dica |
| 5 Validar | Confere se fez certo | Critério de domínio: checklist de autoavaliação ou quiz com 80% de acerto, ou o veredito da ZAIOS | Aprendizagem por domínio, prática de recuperação, feedback |
| 6 Entregar | Sai com um entregável concreto e o próximo passo | PDF, POP preenchido, planilha do mês, página do Dossiê | Merrill (integração), Kolb (conceito aplicado) |

Regras de cada lição:
- Uma lição resolve **um** problema e gera **um** entregável. Duração total: de 20 a 40 minutos, incluindo a execução.
- Ficha da lição com: código (ex.: `O03-L2`), unidade do Método 360°, pilar da ZAIOS ligado, entregável, critério de domínio, fontes e versão das premissas.
- Números só do dicionário único (seção 10). Exemplos marcados como dados fictícios. Sem promessa de resultado.
- Módulo = 4 a 6 lições + revisão espaçada (quiz do módulo anterior) + entregável final do módulo.

Isso convive com o padrão atual: a aula de 40 slides e o e-book de cerca de 120 páginas continuam como material de referência do módulo e base dos encontros do acompanhamento. A lição de 6 passos é a unidade de estudo autônomo.

## 7. Como produzir vídeos, planilhas, templates e exercícios

| Entregável | Como produzir | Molde | Teste |
|---|---|---|---|
| Vídeo explicativo (passo 2) | Slides HTML da lição → narração por cena → gravação → MP4 720p | `aula_simples/gerar.py` + gerador de tutorial | Duração, áudio, legibilidade, revisão humana do roteiro |
| Tutorial (passo 3) | Roteiro gerado da própria ferramenta → gravação da tela real | `zion-arsenal/tutorial/` | Mesmo do anterior |
| Planilha e calculadora | `openpyxl`, aba "Comece aqui", amarelo para preencher e verde para calcular, versão em branco e com exemplo | `utilitarios/17-checklist-limpeza/` | Recálculo no LibreOffice contra regra independente |
| Template editável (POP, mensagem, checklist) | Documento .docx e PDF imprimível a partir de um modelo único de POP | `build_docs.py` + `render.js` | Leitura em celular e impressão A4 |
| Prompt de IA para o membro | Prompt com contexto, dados que o membro preenche, formato de resposta e limites (sem promessa, mandar ao profissional quando legal ou tributário) | Novo, curto | Rodar o prompt em 3 casos fictícios e conferir a saída |
| Exercício interativo | Motor do Arsenal ou ficha da Trilha 1; quando o tema existir na ZAIOS, apontar para o pilar e não duplicar | `zion-arsenal/app/` | `tests/run.js` |
| Quiz de domínio | Perguntas por nível de Bloom, uma certa por questão, feedback | `references/avaliacao.md` | Validação automática (uma resposta certa) |
| Dossiê exportável | PDF do entregável da lição; na Jornada 1 já existe; na ZAIOS, o Dossiê | Fichas da Trilha 1 | Abrir o PDF e conferir |

Voz: hoje as vozes são sintéticas (Piper e edge-tts). A Jornada 1 tem vídeos de aula com outra origem (YouTube, cerca de 6 minutos). A escolha entre voz sintética e voz do Bruno é decisão pendente (seção E).

## 8. Hospedagem e organização no ClickMax

O que a Jornada 1 já faz e funciona:
- Aula do tipo **link externo** para a aula interativa e as fichas (no site, GitHub Pages).
- Aula do tipo **vídeo** apontando para YouTube não listado.
- Aula do tipo **documento** para o PDF do e-book.
- O **mesmo curso dentro de duas turmas** (o ClickMax permite um conteúdo em várias turmas).

Proposta para as Jornadas 2 e 3:
- **Cursos novos**, sem reativar nem mexer nos arquivados: "Jornada 2 · Gestão" e "Jornada 3 · Operação". Um módulo por unidade do Método 360°, uma aula do ClickMax por passo da lição quando o passo for um arquivo ou um vídeo, ou uma aula "Lição completa" em link quando a lição for interativa.
- Arquivos (planilhas, PDFs, POPs) no site em pasta própria com `noindex`, como os utilitários. Vídeos no YouTube não listado, como a Jornada 1. **Subir no YouTube depende do Bruno** (não há ferramenta de upload aqui).
- Nome de cada aula com o código da lição (`O03-L2 · ...`), para a futura ligação com a ZAIOS.
- Nada é criado no ClickMax antes do Comando que autorizar.

## 9. Mesmo material para a jornada autônoma e para o acompanhamento

Um conteúdo, várias turmas:

| Produto | Turma | Conteúdo |
|---|---|---|
| Jornada autônoma (Gestão ou Operação) | Uma turma por jornada | O curso da jornada |
| Formação completa | Uma turma | Os três cursos |
| Acompanhamento Zion 360° | Uma turma | Os três cursos + um curso "Acompanhamento" com agenda, gravações dos encontros e um espaço de entrega dos entregáveis para revisão da equipe Zion |

O acompanhamento não ganha material diferente. Ganha encontros, orientação e revisão dos mesmos entregáveis. Assim uma atualização no curso vale para todos.

## 10. Compatibilidade futura com a ZAIOS

1. **Dicionário único** (`docs/academy/DICIONARIO.md` + versão em JSON): nomes de pilares, indicadores, vereditos (Avançar, Testar, Ajustar, Pausar, Redesenhar), categorias de lançamento do G2, premissas e sua versão. Material e ZAIOS leem a mesma fonte, e o testador barra número ou nome fora dele.
2. **Código de lição estável** (`G04-L3`) ligado à unidade do Método 360° e ao pilar da ZAIOS. É a chave para o botão "Fazer na ZAIOS" e para gravar o progresso depois.
3. **Ferramenta da Academy não duplica a ZAIOS:** se o pilar existe na ZAIOS, a lição aponta para ele; a planilha fica como alternativa para quem não usa a plataforma, com as mesmas fórmulas e rótulos.
4. **Sem segunda pontuação:** o critério de domínio da lição mede aprendizagem (acertou ou não); o veredito da ZAIOS mede o negócio. Não existe "Zion Score" na Academy.
5. A ZAIOS não é alterada nesta etapa.

## 11. Riscos, custos e bloqueios

| Tipo | Item | Efeito |
|---|---|---|
| **Comercial** | **R$ 270 já é o preço do plano Base do Club Zion Collection e da inscrição Club + Land Bank.** **R$ 2.900 já é o plano Pro do Club, que também tem acompanhamento semanal** (páginas `docs/club-zion-collection/` e `docs/land-members/`) | Risco alto de confusão com as ofertas existentes. Precisa de decisão (seção E) |
| Comercial | No ClickMax existe a oferta "Trilha 1 · Desenvolvimento" a R$ 297 (incompleta) e as Trilhas 2 e 3 e o Combo (R$ 297 e R$ 890) arquivados | Uma Jornada a R$ 270 convive com uma Trilha 1 a R$ 297. Não alterar; decidir o que vale |
| Nome | "Trilha" (ClickMax), "Jornada" (ZAIOS: Desenvolvimento e Operação), "Jornada A e B" (perfis na skill) e "6 jornadas" (página de lançamento) | Confusão de nomes. Proposta: Jornada para o produto; perfis viram "Começar" e "Crescer" |
| Bloqueio | Conta de vendedor do ClickMax em análise | Nada vende, mesmo pronto |
| Bloqueio | Upload no YouTube só pelo Bruno | Vídeo pronto não entra no ClickMax sem ele |
| Bloqueio | Teste fechado da ZAIOS não feito | A Academy não pode apontar para a ZAIOS como validada |
| Conteúdo | Bíblia Operacional no Notion com vídeos da operação real e roteiros com campos de nome | Uso só interno, anonimizado e validado; vídeos com pessoas exigem autorização delas |
| Conteúdo | 17 e-books sem revisão | Não usar trechos deles como aprovados |
| Técnico | Fábrica de vídeo com caminhos fixos e voz não instalada; edge-tts depende de serviço gratuito | Primeiro trabalho técnico do próximo comando |
| Técnico | Site no GitHub Pages: repositório público (endereço discreto, não secreto), limite de 100 MB por arquivo | Vídeos nunca no site; só no YouTube |
| Custo | Lovable: zero nesta fase. ClickMax: dentro do plano atual. Vídeo: zero (voz sintética local). O custo real é tempo de sessão do Claude e tempo de revisão do Bruno | Estimativa por lição: 1 sessão de produção + 30 a 45 minutos de revisão do Bruno |

## 12. Primeiro módulo-piloto

**Recomendado: O03 · Limpeza, inspeção e liberação da unidade (Jornada 3 · Operação).**

Por quê:
1. **Mais material pronto e testado:** Checklist de Limpeza 17 (31 de 31), Controle de Enxoval 13 (18 de 18) e o Manual de Governança e Limpeza da Bíblia, com vídeos da rotina real, incluindo um de limpeza completa.
2. **Entregável muito concreto:** o membro sai com o POP de limpeza da própria unidade e o checklist ajustado à casa dele.
3. **Não depende das premissas financeiras nem do teste da ZAIOS:** a ZAIOS não tem pilar de Operação, então não há conflito nem duplicação.
4. **Dor do público inicial** (aluguel por temporada, cabanas, glampings, pequenas pousadas). Na própria Biblioteca de Vídeos da Zion, o vídeo de limpeza completa é descrito como o que "resolve a principal reclamação da Zion". Não usamos número de mercado.

A recomendação anterior (G04 financeiro) fica para depois: depende do G2 testado por pessoas e das premissas na prática.

---

## Matriz de componentes

| Componente | Já existe? | Localização | Reutilização | Falta produzir | Dependências |
|---|---|---|---|---|---|
| Jornada 1 (58 aulas) | Sim | ClickMax (curso da Trilha 1) + `docs/trilha1/` | Preservar como está | Nada | — |
| Molde de módulo da Jornada 1 | Sim | Estrutura dos pilares no ClickMax | Base do molde das Jornadas 2 e 3 | Adaptar aos 6 passos | — |
| Sistema pedagógico | Sim | `.claude/skills/zion-learning-design/` | Total | Acrescentar Merrill, Kolb, andragogia, domínio, apprenticeship e a lição de 6 passos | Aprovação do Bruno |
| Agentes de texto e aula | Sim (3) | `.claude/agents/` | Total | Modo "roteiro de vídeo" no designer | — |
| Arquiteto de módulo | Não | — | — | Agente novo | Lição de 6 passos aprovada |
| Curador de fontes | Não | — | — | Agente novo (só leitura) | Acesso ao Notion; regra de anonimização |
| Fila de produção | Sim | `producao/fila.json` | Total | Entradas G e O no formato novo | Plano do piloto |
| Planos editoriais G e O | Não | — | — | 14 planos | Curador de fontes |
| Bíblia Operacional | Sim (Notion) | Notion: Bíblia Operacional Zion | Fonte interna | Fichas de fonte anonimizadas | Validação do Bruno |
| Gerador de vídeo | Sim (3, não portáteis) | `producao/clube/tutoriais-video/`, `producao/zion-arsenal/tutorial/`, `promo/` | Juntar | `producao/fabrica/video` + vídeo-aula a partir de slides | Escolha da voz |
| Vídeos tutoriais A01, A02, A03, A06, A07 | Sim | Pasta de entregáveis do site | Como bônus, como na Jornada 1 (módulo "Bônus · Ferramentas Zion Collection Club") | — | Decisão de 08/11 sobre o nome nos vídeos |
| Planilhas utilitárias | Sim (6) | `producao/utilitarios/`, `producao/low-ticket/` | Total | Novas só se a lição pedir | — |
| Mini mentorias interativas | Sim (20) | `producao/zion-arsenal/` | Como bônus ou passo 4 | — | — |
| POPs | Não | — | — | Modelo único de POP + POPs do piloto | Bíblia, curador |
| Templates para membros | Parcial | Kit do Investidor, Kit 11 | Parcial | Modelos de POP e de prompt de IA | Lição de 6 passos |
| Prompts de IA para membros | Não | — | — | Biblioteca curta, testada | Regras de linguagem |
| Quiz de domínio | Parcial | `references/avaliacao.md` | Total | Quizzes por lição | Plano do módulo |
| Montador de e-book e PDF | Não guardado | — | — | Guardar script em `producao/fabrica/` | — |
| Testador de harmonia | Não | — | — | `producao/fabrica/checar` | Dicionário único |
| Dicionário único | Não (as regras estão espalhadas) | `PREMISSAS…`, `DECISOES.md`, `src/calc` da ZAIOS | Fonte | `docs/academy/DICIONARIO.md` + JSON | — |
| Capas e páginas de acesso | Sim | `producao/utilitarios/build_entrega.py`, `producao/ferramentas/gerar_capas.py` | Total | Corrigir caminhos fixos | — |
| ClickMax: cursos das Jornadas 2 e 3 | Não (só arquivados) | — | — | Cursos novos | Comando autorizando; vendedor aprovado para vender |
| ClickMax: produtos e ofertas novos | Não | — | — | Jornada, Formação, Acompanhamento | Decisão de preço e nome |
| ZAIOS | Sim | zaios.lovable.app | Ligação por código de lição | Nada nesta etapa | Teste fechado |
| `src/` (agentes Python e Zion Score) | Sim | `src/` | **Não reutilizar** | — | — |

---

## D. Próximo comando sugerido

**Comando 02 · Lição-piloto O03-L1 de ponta a ponta, sem publicar.**

Entregas:
1. Dicionário único v0 (`docs/academy/DICIONARIO.md` + JSON) com os nomes, indicadores, vereditos e premissas já decididos.
2. Padrão da lição de 6 passos acrescentado à skill (sem mudar o que existe).
3. Plano do módulo O03 (4 a 6 lições) e ficha completa da lição O03-L1.
4. Lição O03-L1 completa em rascunho local: diagnóstico, vídeo explicativo, tutorial, POP de limpeza (modelo + exemplo com dados fictícios), checklist adaptado a partir do 17, quiz de domínio e entregável em PDF.
5. `producao/fabrica/video` portátil (gera o vídeo da lição) e `producao/fabrica/checar` (roda na lição).

Critérios de conclusão:
- O testador passa sem erro: links, leitura em 360 e 1280 px, linguagem, números contra o dicionário, 6 passos presentes.
- O vídeo tem imagem e áudio, de 6 a 8 minutos, e foi gerado do zero por um único comando a partir do repositório.
- O quiz tem exatamente uma resposta certa por questão e critério de domínio de 80%.
- Fontes da Bíblia usadas estão anonimizadas e listadas para validação do Bruno.
- Nada publicado no ClickMax, no YouTube ou no site; ZAIOS e Lovable intocados; nenhum crédito Lovable.
