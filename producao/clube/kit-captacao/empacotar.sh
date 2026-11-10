#!/usr/bin/env bash
# Gera tudo e copia os entregáveis para a pasta pública discreta. Uso: bash producao/clube/kit-captacao/empacotar.sh
# (os vídeos levam cerca de 12 minutos; para pular, rode com SEM_VIDEO=1)
set -euo pipefail
cd "$(dirname "$0")"
DEST=../../../docs/p/adbc67069af26ae0/kit-captacao
mkdir -p dist build "$DEST"
python3 -I src/build_planilha.py dist
python3 -I tests/test_planilha.py dist
python3 -I src/build_guia.py build
node src/render_pdf.js build/guia.html dist/Kit-Inicial-Captacao-Zion.pdf build/png
node src/build_capas.js dist
if [ -z "${SEM_VIDEO:-}" ]; then
  python3 video/make_video.py video/spec-kit.json build/video/kit-captacao.mp4
  python3 video/make_video.py video/spec-teaser.json build/teaser/kit-captacao-teaser.mp4
  cp build/video/kit-captacao.mp4 build/teaser/kit-captacao-teaser.mp4 dist/
fi
cp dist/Kit-Inicial-Captacao-Zion.pdf dist/Mapa-das-Fontes-de-Capital-Zion-EM-BRANCO.xlsx dist/Mapa-das-Fontes-de-Capital-Zion-EXEMPLO.xlsx \
   dist/kit-captacao-h.jpg dist/kit-captacao-v.jpg dist/kit-captacao.mp4 dist/kit-captacao-teaser.mp4 src/index.html "$DEST"/
echo "copiado para $DEST"
