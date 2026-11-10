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

## 10/11/2026 · Entrega 3 · Módulos 1, 3, 4, 5, 6 e 7 e integração da Jornada 2

Os seis módulos restantes foram produzidos cada um na sua pasta, com o mesmo padrão do Módulo 2 (ficha + planilha em branco e exemplo + aula em vídeo + tutorial da ficha + resumo em PDF + prompt de IA + capas). Detalhes, testes e pendências de cada um no respectivo `REGISTRO.md`. Todos os arquivos públicos já estão em `origin/main` (GitHub Pages, `docs/trilha2/`); cada URL usada no ClickMax respondeu 200 antes da criação.

| Módulo | Entregável (página do Plano) | Ficha e chave local | Planilha | Registro | Testes (lógica / e2e / planilha) |
|---|---|---|---|---|---|
| 1 · Planejamento, metas e indicadores | Painel de Gestão (p. 1) | `planejamento/` · `zion-t2-planejamento` | Painel de Gestão | `01-planejamento/REGISTRO.md` | 72 / 66 / 38 |
| 3 · Preço, reservas e distribuição | Tabela de Preço e Canais (p. 3) | `preco/` · `zion-t2-preco` | Tabela de Preço e Canais | `03-preco/REGISTRO.md` | 75 / 61 / 43 |
| 4 · Marketing e vendas | Marca e Captação (p. 4) | `marketing/` · `zion-t2-marketing` | Plano de Captação | `04-marketing/REGISTRO.md` | 72 / 58 / 51 |
| 5 · Pessoas e organização das áreas | Mapa de Pessoas e Alçadas (p. 5) | `pessoas/` · `zion-t2-pessoas` | Tarefas, Escala e Alçadas | `05-pessoas/REGISTRO.md` | 85 / 63 / 41 |
| 6 · Compras, estoque e manutenção | Matriz de Compras e Manutenção (p. 6) | `compras/` · `zion-t2-compras` | Matriz de Compras e Manutenção | `06-compras/REGISTRO.md` | 76 / 60 / 74 |
| 7 · Qualidade, reputação e plano de crescimento | Montador do Plano de Gestão (Plano completo em PDF) | `qualidade/` · `zion-t2-qualidade` | Qualidade e Reputação | `07-qualidade/REGISTRO.md` | 88 / 64 / 39 |

Exemplo didático único (Cabanas do Vale, dados fictícios) atravessa os oito módulos com os mesmos números (Folha de outubro de 2026: resultado 4.269,20; ocupação de equilíbrio 28,5%; venda direta 30% com meta de 40% até 30/06/2027; comissão média 11,0%).

### Página de ferramentas (`docs/trilha2/index.html`)
Atualizada: os oito itens (Marco Zero e Módulos 1 a 7) agora são links para as fichas, cada um com a sua chave local para a marca "Feita / Em andamento" (`zion-t2-marco-zero`, `-planejamento`, `-financas`, `-preco`, `-marketing`, `-pessoas`, `-compras`, `-qualidade`); um bloco de materiais por módulo (planilhas em branco e exemplo, resumo, prompt de IA e tutorial da ficha). Todos os links relativos conferidos contra os arquivos.

### ClickMax (conteúdo Jornada 2 `f1d16209-776d-45c0-a57a-de1c8ce7dd41`, turma "Jornada 2 · Gestão")
Mesmo molde e mesma liberação do Módulo 2 publicado: módulos e aulas `DAYS_AFTER_PURCHASE` sem prazo (liberados na hora), aulas `enabled=true`, `startAutomatically=false`, comentários ligados, avaliações só nas aulas de vídeo e Faça agora; capa horizontal em cada aula; vídeo apontando para o mp4 público no GitHub Pages (como o Módulo 2). Módulos novos com capa horizontal e vertical. Ordem final: Marco Zero, 1, 2, 3, 4, 5, 6, 7 (Marco Zero e Módulo 2 só mudaram de posição).

| Módulo | id | Aulas (4 em cada: vídeo, Faça agora com 5 anexos, resumo PDF, planilha com 2 anexos) |
|---|---|---|
| 1 · Planejamento | `7ed5bd04-b6e4-410e-850b-0777f9d24ef3` | vídeo `9141e861-…`, Faça agora `b20a4a7a-…`, resumo `109ad47d-…`, planilha `3e51caa1-…` |
| 3 · Preço | `7ce82c79-0af5-4d96-83e9-8754d4676183` | `3ac29b8d-…`, `1e975eef-…`, `76f4f71b-…`, `43d229cc-…` |
| 4 · Marketing | `b2889c4d-c784-41ee-990f-79b261577890` | `0c83ca54-…`, `90019d3d-…` (6 anexos: inclui o Kit de Mensagens, Ferramenta 11), `58402aa0-…`, `e7f953e5-…` |
| 5 · Pessoas | `3de01223-9ee4-4db4-a7ae-e9dc3326ef0c` | `f90436c3-…`, `c27ec0f6-…`, `4d2d667f-…`, `f9bb3323-…` |
| 6 · Compras | `4862fff3-7a07-4209-a788-4370e6e6553c` | `4cdf1533-…`, `9ff48944-…`, `1c6c1e9a-…`, `f7110b47-…` |
| 7 · Qualidade | `ac130f16-1142-45cd-b517-f2cfbf5aaf92` | `d004fba7-…`, `d27ab0e0-…`, `6acc0483-…`, `7601a3e7-…` |

Nenhuma oferta, preço, checkout, e-mail, WhatsApp ou membro criado ou alterado. O conteúdo `a28341aa-…` da mesma turma não foi tocado.

### Pendências e decisões para Bruno (consolidadas dos registros)
1. **Player mp4 do ClickMax**: todas as aulas em vídeo apontam para o mp4 direto (como o Marco Zero e o Módulo 2). Se o player não tocar, subir no YouTube não listado e trocar a URL das oito aulas.
2. **Descrição do conteúdo no ClickMax** ainda diz "Já liberados: Marco Zero do Gestor e Módulo 2"; atualizar para os oito módulos (não alterada nesta entrega).
3. **Reserva de manutenção 3% (Módulo 6) × reserva de reposição 4% (Módulo 2)**: decidir um número único.
4. **Links para produtos vendidos à parte**: o Módulo 4 aponta para o Kit de Mensagens (Ferramenta 11, também anexado no ClickMax conforme o plano do registro), o Módulo 3 para o Precificador (A02) e a Ferramenta 01, o Módulo 6 para as Ferramentas 13, 14 e 18. Confirmar se a Jornada 2 pode apontar para elas.
5. Cinco indicadores fixos e regra da meta para o mesmo mês daqui a 12 meses (Módulo 1); "Pilar 07 reputação" × Volume 07 Lançamento (Módulo 7); temas trabalhistas remetidos ao contador (Módulo 5).
6. Capas da jornada saem com a fonte serifada do sistema (Cormorant e Aventa não carregam no gerador); corrigir todas de uma vez embutindo as fontes no `build_capas.js`.
7. Correções de molde ainda não levadas ao Módulo 2: `num("13.000")` lido como 13 e fonte do PDF depois da quebra de página (`docs/trilha2/financas/logic.js`).
8. Foto `op10` tem uma pessoa e está listada no `CLAUDE.md` como sem pessoas.
9. Narração sintética em todas as aulas e tutoriais; regravação possível pelos `ROTEIRO.md`.
10. Persistência só no aparelho: o Montador do Módulo 7 só junta as páginas feitas no mesmo navegador (proposta de consolidação no ZAIOS em `LIMITACOES.md`).
