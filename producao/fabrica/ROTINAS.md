# Fábrica Educacional Zion 360° · Rotinas (sem LLM)

Comandos que o orquestrador roda em cada lição, a partir da pasta da lição `producao/<jornada>/<nn-nome>/`. Servem de "produtor audiovisual" e de "testador" automáticos. Todos já existem e foram usados na Jornada 2.

## Testes (portão de desenvolvimento)
```
node tests/test_logic.js                                    # lógica pura
python3 -I src/build_planilha.py ../../../docs/<jornada>/materiais/planilhas
python3 -I tests/test_planilha.py ../../../docs/<jornada>/materiais/planilhas   # recálculo no LibreOffice
(cd ../../../docs && nohup python3 -m http.server 8790 >/dev/null 2>&1 &)
node tests/e2e.js <pasta-saida> <caminho/jspdf.umd.min.js>  # celular, PDF, persistência, capturas
```
Pronto quando: "0 falhou" nos três e capturas conferidas.

## Materiais
```
python3 -I src/build_resumo.py build && node src/render_pdf.js build/resumo.html ../../../docs/<jornada>/materiais/<Cod>-resumo.pdf
node build/alt.js   # (opcional) altura de cada página ≤ 297 mm
node src/build_capas.js ../../../docs/<jornada>/capas
```

## Vídeos
```
node video/shots.js && node video/shot_xl.js                # telas da ficha e da planilha
python3 video/make_video.py video/spec-<cod>.json ../../../docs/<jornada>/videos/aula-<cod>.mp4
(cd ../../clube/tutoriais-video && python3 make.py ../../<jornada>/<pasta>/tutorial/<ficha>.json ../../../docs/<jornada>/videos/tutoriais/tutorial-<ficha>.mp4)
rm -rf ../../../docs/<jornada>/videos/aula-<cod> ../../../docs/<jornada>/videos/tutoriais/tutorial-<ficha>   # pastas de trabalho
ffmpeg -ss 30 -i <mp4> -frames:v 1 quadro.png                # conferir quadros (3 a 6 amostras)
```
Narração: edge-tts via `HTTPS_PROXY`; fotos: `docs/assets/operacoes/` sem pessoas.

## Publicação e registro
- Commit e push (sem dados pessoais, sem texto bruto de fontes, sem pastas de trabalho).
- Agente publicador cria módulo e aulas desativadas e registra ids no `RELATORIO.md`.

## Ordem de uma sessão de lição
especialista (mapa de fontes) → arquiteto (plano) → construtor (lógica + testes → ficha → e2e → planilha + teste) → roteirista (roteiros) → rotinas de vídeo → designer (resumo, capas, página) → revisor (relatório; correções; testes de novo) → publicador (rascunhos) → relatório para Bruno.
