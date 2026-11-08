# Jornada 2 · Gestão (e base da Jornada 3 · Operação) · fábrica

Padrão de produção por módulo, igual à Jornada 1 e aos nove itens do comando 01. Nada aqui altera a Trilha 1 nem os conteúdos arquivados.

- `AUDITORIA.md` · como a Trilha 1 é montada, o estado real das Trilhas 2 a 4 no ClickMax, materiais reutilizáveis e o que o ClickMax suporta.
- `PLANO_G00.md` · plano editorial da Jornada 2 (8 módulos) e do módulo-piloto.
- `RELATORIO.md` · registro de cada entrega (arquivos, testes, ids no ClickMax, decisões para Bruno).
- `LIMITACOES.md` · limitações e proposta de persistência para o ZAIOS.
- `00-marco-zero/` · módulo-piloto:
  - `src/logic.js` lógica pura da ficha (copiada para `docs/trilha2/marco-zero/logic.js`), `src/build_planilha.py`, `src/build_resumo.py` + `src/render_pdf.js`, `src/build_capas.js`;
  - `tests/test_logic.js` (Node), `tests/e2e.js` (Playwright, celular, jsPDF local), `tests/test_planilha.py` (LibreOffice);
  - `video/` cenas, narração e gravação da aula 16:9 (`make_video.py`, `record_h.js`, `aula.html`, `scenes-g00.js`, `spec-g00.json`, `shots.js`, `shot_xl.js`);
  - `tutorial/` roteiro do tutorial da ficha (usa `producao/clube/tutoriais-video/make.py`);
  - `ROTEIRO.md` narração completa dos dois vídeos; `demonstracao/` capturas no celular.

## Como reproduzir o módulo-piloto
```
cd producao/jornada2/00-marco-zero
node tests/test_logic.js
python3 -I src/build_planilha.py ../../../docs/trilha2/materiais/planilhas && python3 -I tests/test_planilha.py ../../../docs/trilha2/materiais/planilhas
(cd ../../../docs && python3 -m http.server 8790 &)   # servidor local
node tests/e2e.js <pasta-saida> <caminho de jspdf.umd.min.js>
python3 -I src/build_resumo.py build && node src/render_pdf.js build/resumo.html ../../../docs/trilha2/materiais/Marco-Zero-Gestao-resumo.pdf
node src/build_capas.js ../../../docs/trilha2/capas
node video/shots.js && node video/shot_xl.js && python3 video/make_video.py video/spec-g00.json ../../../docs/trilha2/videos/aula-marco-zero-gestao.mp4
(cd ../../clube/tutoriais-video && python3 make.py ../../jornada2/00-marco-zero/tutorial/ficha-gestao-marco-zero.json ../../../docs/trilha2/videos/tutoriais/tutorial-ficha-gestao-marco-zero.mp4)
```
Depois de gerar os vídeos, apague as pastas de trabalho que ficam ao lado dos mp4 em `docs/trilha2/videos/` antes do commit.

## Próximos módulos (ordem)
1 Planejamento, metas e indicadores · 2 Finanças, fluxo de caixa e fechamento · 3 Preço, reservas e distribuição · 4 Marketing e vendas · 5 Pessoas e organização das áreas · 6 Compras, estoque e manutenção · 7 Qualidade, reputação e plano de crescimento. Cada um: pasta `0N-nome/` com a mesma estrutura, um mapa de fontes por subagente, e registro no `RELATORIO.md`.
