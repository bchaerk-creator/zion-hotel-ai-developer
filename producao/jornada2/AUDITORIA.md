# Jornada 2 · Gestão e Jornada 3 · Operação · Auditoria da estrutura existente

Data: 08/11/2026. Comando 01 do GPT (Zion Hotel Academy). Nada do que está listado aqui foi alterado.

## 1. Como a Jornada 1 · Desenvolvimento está montada (o padrão a seguir)

**ClickMax.** Portal "Zion Hospitality Business" (mentoria-zion). Conteúdo "Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso" (id `fa9a6c54…`), 9 módulos e 58 aulas, ligado às turmas "Transforme Seu Terreno…" (3 membros) e "Turma Fundadores" e também ao portal do Land Bank (turma "Candidatos", 6 membros). Módulos: Marco Zero, Pilares 1 a 7, Bônus Ferramentas Zion Collection Club.

**Padrão de cada módulo (aulas, nesta ordem):**
1. `external_link` "Aula interativa · …" → `docs/trilha1/apresentacao/<x>-aula/` (motor próprio `_motor/deck.js`, 1920×1080 com modo celular).
2. `video` "Vídeo N · Bloco 1" e "Vídeo N+1 · Bloco 2" → YouTube (não listado).
3. `external_link` "Faça agora · …" → ficha interativa em `docs/trilha1/<pasta>/` (salva no aparelho, PDF com jsPDF, feedback em partes), com anexos: tutorial em vídeo (`docs/trilha1/videos/tutoriais/*.mp4`, 1280×720), slides e e-book.
4. `document` "E-book · … (PDF)" → `docs/trilha1/materiais/*.pdf`.
O Marco Zero tem ainda "Comece aqui" (PDF) e o Mapa de direcionamento.

**Fichas "Faça agora" (molde):** HTML único, Inter + Playfair, paleta verde `#16261C` / creme / dourado, telas com barra de progresso, três apoios por pergunta (por que perguntamos, onde conseguir, exemplo ilustrativo "Marina"), estado em `localStorage` (`zion-t1-*`), resultado com leitura, ponto frágil, ação de 7 dias e PDF. As fichas da Trilha 1 também enviam a página do Dossiê ao Land Bank (`_landbank.js`, webhook Lovable e formulário do ClickMax). **Na Jornada 2 esse envio não é usado:** a gestão não é um pedido de avaliação de terreno, e o comando pede documentar a persistência para o ZAIOS.

**Capas:** `docs/trilha1/capas/` (curso, módulos h/v, aulas). **Vídeos:** tutoriais gerados por `producao/clube/tutoriais-video/` (Playwright + edge-tts + ffmpeg); trailers e vídeos narrados por `producao/clube/trailer-whatsapp/` (cenas em JS, 1080×1920).

**Planilhas:** `producao/clube/planilhas/src/build.py` (Orçamento de Abertura, Estudo de Massas) e `producao/low-ticket/01-diaria-minima/build_planilha.py` (molde de planilha testada no LibreOffice).

## 2. Estado real das Trilhas 2, 3 e 4 no ClickMax

| Item | Estado | Decisão para a Jornada 2 |
|---|---|---|
| Turma "Arquivo · Trilha 2 · Gestão" (`294be538…`) | sem conteúdo ligado, 1 membro, produtos "Trilha 2 · Gestão" e "Combo Mentoria Zion · As 3 trilhas" | Não tocar. É arquivo com produto antigo associado. |
| Conteúdo "Arquivo · Trilha 2 · Gestão" (`02363489…`) | 7 módulos sem aulas: CAPEX, Receitas e modelo de venda, Custos/P&L/forecast, Viabilidade, Estrutura jurídica, Capital e captação, Lançamento | É a parte **financeira do desenvolvimento**, não gestão de hospedagem em operação. Já coberta pela Jornada 1 (Pilares 4, 6 e 7). Não reaproveitar como Jornada 2. |
| Turma "Arquivo · Trilha 3 · Operação" (`0da5717a…`) e conteúdo "Arquivo · Trilha 3 · Operação hoteleira" (`1d07adf7…`) | 7 módulos sem aulas: Operação do zero, Estrutura online, Estrutura física e departamentos, Pessoas, Manualização, Gestão de gastos, Orçamento/forecast | Boa espinha para a **Jornada 3 · Operação** (módulos 1 a 5) e para dois módulos da Jornada 2 (gastos e orçamento). Reaproveitar como referência, criando conteúdo novo. |
| Conteúdo "Arquivo · Trilha 4 · Aceleração de vendas" (`1775d90d…`) | 7 módulos sem aulas | Fonte para o módulo de Marketing e vendas da Jornada 2. |
| Bônus "Trilha Gestão · Ferramentas Zion Collection Club" (`a28341aa…`) | 3 aulas: Precificador Inteligente, Calculadora de Custos e Rentabilidade, Calculadora de Receitas Extras (apps em `docs/p/adbc67069af26ae0/zar-a02, a03, a08`) | Reaproveitar nos módulos 2 e 3 da Jornada 2 como ferramentas. |
| Bônus "Trilha Operação · Ferramentas" (`2036a7b8…`) | 2 aulas: Auditor Inteligente da Experiência, Organizador Operacional (zar-a06, a10) | Reaproveitar na Jornada 3. |
| "Panorama do Desenvolvimento Hoteleiro · Marco Zero" (`03aa8ff9…`, 12 aulas) | ativo no portal do Land Bank | Fonte: Trilha B (Gestão) do Panorama é a espinha da Jornada 2. |

**Conclusão:** a Trilha 2 não tem como "receber" aulas no conteúdo arquivado sem mexer no que existe. A Jornada 2 nasce como **conteúdo novo** ("Jornada 2 · Gestão", não à venda), com módulos e aulas **desativadas**, sem ligação a turmas com membros até Bruno aprovar.

## 3. Materiais reutilizáveis para Gestão e Operação

- Ferramentas prontas (R$ 19, catálogo): 01 Diária Mínima (preço e controle do mês), 17 Checklist de limpeza, inspeção e liberação, 11 Kit de mensagens de chegada e saída, 13 Controle de enxoval, 14 Quadro de ocorrências e manutenção, 29 Calculadora de custos de experiências. Todas com planilha testada, guia PDF e página.
- Bônus do Club (apps): Precificador, Custos e Rentabilidade, Receitas Extras, Auditor da Experiência, Organizador Operacional.
- Fontes Zion para gestão (mapa em arquivo de trabalho, fora do repositório): Panorama (Trilha B: G1 Marca, G2 Distribuição, G3 Preço, G4 Captação, G5 Compras, G6 Finanças, G7 Governança, Painel de Gestão com 5 indicadores e reunião semanal de 30 min); Jornada do COMO Etapa 09 "Como sei se estou lucrando" (13 passos, Folha Única, custo por diária vendida, ponto de equilíbrio, reserva de sazonalidade); Etapa 10 "Como saio da operação" (Inventário da Cabeça, quatro dependências, Manual Mínimo, Plano de Saída); Manual Oficial do Método Zion 360° (mentalidade, OP3LIF®); Bíblia Operacional Zion no Notion (rotina do gestor, 6 setores, onboarding em 6 etapas, manual de governança e limpeza).
- Linha editorial anterior (Mentoria Zion 360°, 52 unidades): planos e e-books D00 a D06 e F00 a F02 em `producao/planos/` e `docs/escola/`; os pilares G (Gerir, G00 a G06) e O (Operar, O00 a O06) estão na fila sem produção. A Jornada 2 segue a ordem desses pilares com a linguagem simples das aulas da Trilha 1.

## 4. Funcionalidades do ClickMax para automação educacional (conferido pela API)

| Precisamos de | ClickMax suporta direto? | Como fazemos |
|---|---|---|
| Aulas de vídeo, texto, documento, link externo, banner | Sim (`type` da aula) | Vídeo no YouTube não listado ou arquivo mp4 no site |
| Anexos por aula (materiais) | Sim | PDF, planilhas e links do site |
| Formulários guiados, calculadoras, checklists interativos | Não dentro da aula | HTML próprio no site (fichas "Faça agora"), aberto por link externo |
| Exportar PDF do entregável | Não | jsPDF na ficha |
| Salvar progresso do exercício | Só o progresso da aula (assistida ou não) | `localStorage` no aparelho do aluno (limitação: não migra de aparelho, não chega à equipe Zion) |
| Consolidar entregáveis do membro | Não | Proposta para o ZAIOS em `LIMITACOES.md` |
| Comentários e avaliações da aula | Sim | Ligados nas aulas |
| Liberação por data ou dias após a compra | Sim | `releaseType` por módulo e aula |
