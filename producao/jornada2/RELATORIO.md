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

## 08/11/2026 · Entrega 2 · Módulo 2 "Finanças, fluxo de caixa e fechamento" (Folha Única do Mês)

Produzido com a Fábrica Educacional Zion 360° (arquiteto → construtor → roteirista → rotinas de vídeo → designer → revisão → publicador). Pasta: `producao/jornada2/02-financas/`.

### Arquivos publicados (GitHub Pages, `docs/trilha2/`)
- Ficha "A minha Folha Única do Mês": `financas/index.html` + `financas/logic.js` (chave local `zion-t2-financas`; 8 telas; cascata, 4 indicadores, leituras pelas réguas, causa principal, 3 prioridades, plano de ação, PDF).
- Planilhas: `materiais/planilhas/Folha-Unica-do-Mes-Zion-EM-BRANCO.xlsx` e `-EXEMPLO.xlsx` (abas Comece aqui, Parâmetros, Folha do Mês, Caixa 12 meses, Histórico, Checklist).
- Resumo da aula: `materiais/Modulo-2-Financas-resumo.pdf` (8 páginas A4, citações com fonte, exemplo rotulado como fictício).
- Prompt de IA: `materiais/Modulo-2-Prompt-de-IA.txt`.
- Vídeo da aula: `videos/aula-financas.mp4` (6:39, 13 cenas, narração sintética pt-BR, foto op11 sem pessoas).
- Tutorial da ficha: `videos/tutoriais/tutorial-ficha-financas.mp4` (4:36, gravação automática da ficha; regravado três vezes até percorrer as 7 telas e fechar no exemplo, 4.269,20).
- Capas: `capas/g2-h.jpg`, `g2-v.jpg`, `g2-c-aula.jpg`, `g2-c-faca.jpg`, `g2-c-resumo.jpg`, `g2-c-planilha.jpg`.
- Página de ferramentas `index.html` atualizada com o Módulo 2 e os materiais.

### Testes (todos executados nesta sessão)
| Teste | Resultado |
|---|---|
| `tests/test_logic.js` (Node, lógica pura, exemplo Cabanas do Vale, réguas, prioridades, conclusão, modo da retirada) | 92 ok, 0 falhou |
| `tests/e2e.js` (Playwright, iPhone 13, 8 telas, persistência, PDF, exemplo) | 52 ok, 0 falhou |
| `tests/test_planilha.py` (recálculo no LibreOffice × conta independente) | 49 ok, 0 falhou |
| Revisão de conformidade (vocabulário, promessas, 17%/1% como referência ajustável, limpeza como repasse, números iguais em lógica/roteiro/resumo, sem travessões) | sem achados bloqueantes |

Exemplo didático (dados fictícios): deduções 3.654,40; receita real 12.585,60; variáveis 2.062,40; margem de contribuição 11.503,20; fixos 7.234,00; resultado operacional 4.269,20; reserva 542,62; geração de caixa 3.726,58; custo por noite vendida 153,03; ponto de equilíbrio 35,4 noites; ocupação de equilíbrio 28,5%; fôlego 1,9 meses.

### ClickMax (rascunhos, tudo desativado; conteúdo Jornada 2 `f1d16209-776d-45c0-a57a-de1c8ce7dd41`, availableForSale=false)
- Módulo 2 · Finanças, fluxo de caixa e fechamento: `3496fb39-270c-4355-a33f-905bfd76522a` (posição 2).
- Aula em vídeo: `c1b2421e-c5a2-4339-b28f-18cd4e8edebc` (enabled=false).
- Faça agora (link + 5 anexos: ficha, tutorial, 2 planilhas, prompt): `b0922529-df5e-49c6-a6e7-7079e9bd58bb` (enabled=false).
- Resumo (PDF): `638ef9ff-406c-47d7-bc46-ef807af7db6a` (enabled=false).
- Planilha (link + 2 anexos): `6440a510-7118-4ac8-8ba6-05eb1409643d` (enabled=false).
- Nenhuma turma ligada; Trilha 1, conteúdos "Arquivo", Land Bank, Zaya e automações intactos.

### Correções feitas na revisão
- Ficha: quando o modo da retirada não estava gravado, a tela mostrava "Calcular por horas" marcado mas a lógica tratava como "Informar o valor" e zerava a retirada. Corrigido em `logic.js` com dois testes novos.
- Tutorial da Folha: o preenchimento automático não respondia as quatro perguntas Sim/Não (ficava preso na abertura) e marcava "Decidi retirada zero"; cena 1 e cena 5 agora são explícitas.
- Tutoriais do Marco Zero e da Folha: abertura dizia "Club Zion Collection · Trilha de Desenvolvimento"; agora diz "Jornada de Gestão".

### Decisões e pendências
- `PREMISSAS_FINANCEIRAS_E_VERIFICACOES.md` e `DECISOES.md` citados no comando não existem no repositório; as convenções vieram de `producao/planos/F02.md` e da Etapa 09 e estão declaradas na seção 11 do `PLANO.md`.
- Turma de revisão para Bruno: viável (classrooms_create + classrooms_add_content + member_users_add_to_classroom), mas adicionar o usuário-membro de Bruno (já existente) altera um recurso ativo; aguarda "aprovado".
- Player de mp4 no ClickMax: a aula aponta para o mp4 público; se o player não aceitar mp4 direto, subir no YouTube (não listado) e trocar a URL.
- Narração sintética (edge-tts); Bruno pode regravar com a própria voz usando o `ROTEIRO.md`.
- Persistência fora do aparelho (ZAIOS): a ficha salva só no navegador; a proposta de registro de parâmetros e persistência está em `LIMITACOES.md`.
