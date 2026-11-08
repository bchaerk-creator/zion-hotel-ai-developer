# Jornada 2 · Gestão · Relatório de produção

Leitura para Bruno e para o GPT (estratégia). Nada publicado, nada ativado, nenhuma estrutura existente alterada. Comando 01 · Entrega 1 (auditoria + módulo-piloto).

## 08/11/2026 · Entrega 1 · Auditoria e módulo-piloto "Marco Zero · O gestor e o diagnóstico"

**Auditoria:** `producao/jornada2/AUDITORIA.md`. Achado principal: as Trilhas 2 e 3 existem no ClickMax só como turmas vazias e conteúdos "Arquivo" com módulos sem aulas (a "Trilha 2" arquivada é a parte financeira do desenvolvimento, não gestão em operação). A Jornada 2 nasce como conteúdo novo, sem ligação a turmas com membros.

**Plano editorial:** `producao/jornada2/PLANO_G00.md` (8 módulos, entregável por módulo, fontes Zion, decisões de vocabulário, proposta de produção dos módulos 1 a 7 e da Jornada 3).

**Módulo-piloto (arquivos públicos em `docs/trilha2/`):**
| Item | Onde | Teste |
|---|---|---|
| Ficha "Faça agora · O seu Diagnóstico de Gestão" (6 telas, resultado em 5 partes, ação de 30 dias, critério de conclusão, PDF, salva no aparelho) | `docs/trilha2/marco-zero/` (lógica em `producao/jornada2/00-marco-zero/src/logic.js`) | 23 testes de lógica (Node) e 30 de ponta a ponta no iPhone 13 (Playwright, jsPDF servido localmente): todos passaram. Sem erro de JavaScript, sem rolagem horizontal, PDF de 10 KB gerado, estado persiste após recarregar. |
| Planilha Painel do Mês (em branco e exemplo), abas Comece aqui, Painel, Histórico, Rotina | `docs/trilha2/materiais/planilhas/` (`src/build_planilha.py`) | 22 testes contra conta independente após recálculo no LibreOffice: todos passaram (inclui bloqueios: célula vazia, negativo, unidades zero, noites acima das disponíveis; divisão por zero; leitura empate/abaixo do custo). |
| Aula em vídeo (16:9, 3 min 46, 11 cenas, narração sintética pt-BR) | `docs/trilha2/videos/aula-marco-zero-gestao.mp4` (cenas em `video/`, roteiro em `ROTEIRO.md`) | Quadros conferidos visualmente (6 amostras). |
| Tutorial da ficha (1280×720, gravação real com cursor, 2 min 47) | `docs/trilha2/videos/tutoriais/tutorial-ficha-gestao-marco-zero.mp4` (`tutorial/*.json`) | Quadros conferidos; passo da data corrigido e regravado. |
| Resumo da aula (PDF, 7 páginas: três ofícios, cinco números, rotina mínima, oito áreas, exemplo didático, critério de conclusão, próxima etapa) | `docs/trilha2/materiais/Marco-Zero-Gestao-resumo.pdf` (`src/build_resumo.py` + `render_pdf.js`) | Altura de cada página conferida (sem transbordo). |
| Capas do módulo (h/v) e das 4 aulas | `docs/trilha2/capas/` (`src/build_capas.js`) | Conferidas visualmente. |
| Página das ferramentas da Jornada 2 | `docs/trilha2/` | Marca "Feita / Em andamento" lida do aparelho. |
| Demonstração no celular | `producao/jornada2/00-marco-zero/demonstracao/` | Capturas do teste e2e. |

**Fontes:** mapa de fontes do G00 em arquivo de trabalho fora do repositório (Panorama Trilha B, Etapas 09 e 10, Manual 360°, Bíblia Operacional no Notion). Citações literais usadas na aula e no resumo estão referenciadas no `ROTEIRO.md`. Nenhum número real da Zion; exemplo "Cabanas do Vale" marcado como fictício em todas as peças.

**ClickMax (rascunhos, tudo desativado, não à venda, sem turma):**
- Conteúdo "Jornada 2 · Gestão · Aprenda o passo a passo para gerir a sua hospedagem": `f1d16209-776d-45c0-a57a-de1c8ce7dd41` (`availableForSale=false`).
- Módulo "Marco Zero · O gestor e o diagnóstico": `3253c8e3-c621-44ea-921c-da6d532827a1`.
- Aulas (todas `enabled=false`, `startAutomatically=false`): Aula em vídeo `e8689f8b-b550-4625-b81c-8539f46a068a` (tipo vídeo, URL do mp4; conferir se o player do ClickMax aceita mp4 direto, senão trocar para YouTube não listado como na Trilha 1); Faça agora `b2a99643-a20b-4735-98c8-2129acc72ff6` (link externo + 4 anexos: ficha, tutorial, planilhas); Resumo `698afd84-4801-4010-81c7-e4a4e6881bbd` (documento); Planilha `75c9b77e-08ca-4a03-aa8e-d43d3d3eb889` (link + 2 anexos).
- As capas e os arquivos apontam para o GitHub Pages; ficam visíveis depois do push.

**Limitações e proposta para o ZAIOS:** `producao/jornada2/LIMITACOES.md` (persistência só no aparelho, sem envio de dados, critério de conclusão vive na ficha; proposta de endpoint, consentimento, recuperação por e-mail e consolidação do Plano).

**Decisões para Bruno:**
1. Aprovar o padrão do módulo (ficha + planilha + aula em vídeo + tutorial + resumo) antes de produzir os módulos 1 a 7.
2. Narração: manter a voz sintética ou regravar com a sua voz pelo roteiro.
3. Vídeo da aula: hospedar o mp4 no site (como está) ou subir no YouTube não listado (padrão da Trilha 1).
4. Ligar o conteúdo a uma turma de revisão (nova, sem alunos) para você ver como membro, ou revisar pelo painel.
5. Nome comercial: "Jornada 2 · Gestão" (como o comando) ou "Trilha 2 · Gestão" (como a Trilha 1 chama a si mesma).
6. Preços de pacotes (Profissional e Premium) e o acompanhamento de R$ 2.900 seguem como proposta, sem oferta criada.
