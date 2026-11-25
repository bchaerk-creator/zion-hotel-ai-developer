#!/bin/bash
# Copia os entregáveis para o site (docs/p/.../mini-mentoria-performance/). Só vira público quando a branch for para a main (aprovação de Bruno).
set -e
R="$(cd "$(dirname "$0")/../.." && pwd)"; P="$R/producao/mini-mentoria-performance"; D="$R/docs/p/adbc67069af26ae0/mini-mentoria-performance"
python3 -I "$P/build.py" && python3 -I "$P/ebook/build_ebook.py" >/dev/null && node "$P/ebook/render_ebook.js" >/dev/null && python3 -I "$P/landing/build.py"
mkdir -p "$D/img"; cp "$P/dist/index.html" "$D/index.html"
for m in 1 2 3 4 5 6 7; do cp "$P/ebook/dist/guia-$m.pdf" "$D/guia-$m.pdf"; done
cp "$P"/landing/img/*.jpg "$P"/landing/img/demo.mp4 "$D/img/"
echo "ok: $D"; du -sh "$D"
