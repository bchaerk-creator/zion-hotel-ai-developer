# Tutoriais em vídeo das ferramentas da Trilha

Vídeos de 1280×720, narração em português (voz neural pt-BR-Francisca via edge-tts), gravação real da ferramenta com cursor e destaques, capas de abertura e fechamento.

- `specs/*.json`: roteiro de cada vídeo (cenas com `say` e `actions`: goto, card, show, click, type, scroll, text).
- `record.js`: grava a tela com Playwright (uma gravação contínua, cena a cena).
- `make.py`: gera a narração, grava, corta por cena e junta com ffmpeg. Uso: `python3 make.py specs/kit.json out/tutorial-kit.mp4` com um servidor local servindo `docs/` na porta 8790 e, para as planilhas, o HTML exportado do xlsx pelo LibreOffice.
- Publicados em `docs/trilha1/videos/tutoriais/` e anexados às aulas no ClickMax.
