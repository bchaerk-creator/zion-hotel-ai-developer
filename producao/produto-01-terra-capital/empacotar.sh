#!/bin/bash
# Copia os entregáveis para o site (docs/p/.../terra-capital/). Só vira público quando a branch for para a main (aprovação de Bruno).
set -e
R="$(cd "$(dirname "$0")/../.." && pwd)"; P="$R/producao/produto-01-terra-capital"; D="$R/docs/p/adbc67069af26ae0/terra-capital"
python3 -I "$P/build.py" && python3 -I "$P/ebook/build_ebook.py" && node "$P/ebook/render_ebook.js"
mkdir -p "$D/img"; cp "$P/dist/index.html" "$D/index.html"; cp "$P/dist/Voce-tem-terra-falta-capital-Zion.pdf" "$D/"
cp "$P"/landing/img/*.jpg "$P"/landing/img/demo.mp4 "$D/img/"
echo "ok: $D"; ls -la "$D" "$D/img" | head -30
