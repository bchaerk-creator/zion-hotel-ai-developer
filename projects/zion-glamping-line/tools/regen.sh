#!/usr/bin/env bash
# Regenera toda a linha (desenhos, DXF, 3D, renders, cadernos, PDFs) a partir de geometry.py.
# Uso: bash tools/regen.sh [--no-render]   (a partir da raiz projects/zion-glamping-line)
set -e
cd "$(dirname "$0")"
export NODE_PATH=/opt/node22/lib/node_modules
echo "== desenhos"; python3 drawings_cocoon.py && python3 drawings_zenith.py && python3 iso.py && python3 details.py && python3 drawings_extra.py && python3 exploded.py
echo "== pranchas PA + DXF"; python3 pa_sheets.py && python3 lodge_family.py && python3 capsule.py && python3 export_dxf.py > /dev/null
if [[ "$1" != "--no-render" ]]; then
  echo "== 3D + renders"; python3 build_viewer.py && node render.js
  echo "== renders web (1400 px) e deck (sem interface), com a marca Zion"; python3 brand_renders.py
fi
echo "== caderno técnico"; python3 build_dossier.py && python3 build_dossier.py --web && python3 build_dossier.py --inline
echo "== product book"; python3 build_product_book.py && python3 build_product_book.py --web && python3 build_product_book.py --inline
echo "== projeto arquitetônico + apresentação"; python3 build_projeto_arquitetonico.py && python3 build_projeto_arquitetonico.py --inline && python3 build_apresentacao.py && python3 build_catalogo.py
echo "== PDFs"
node export_pdf.js ../_print_ZION_CASULO_SAFARI_Caderno_Tecnico.html ../ZION_CASULO_SAFARI_Caderno_Tecnico.pdf
node export_pdf.js ../_print_ZION_ARCHITECTURAL_PRODUCT_BOOK.html ../ZION_ARCHITECTURAL_PRODUCT_BOOK.pdf
node export_pdf.js ../ZION_PROJETO_ARQUITETONICO.html ../ZION_PROJETO_ARQUITETONICO.pdf
node export_pdf.js ../ZION_PROJETO_ARQUITETONICO_Apresentacao.html ../ZION_PROJETO_ARQUITETONICO_Apresentacao.pdf
node export_pdf.js ../ZION_CATALOGO_LINHA.html ../ZION_CATALOGO_LINHA.pdf
python3 pdf_leve.py ../ZION_ARCHITECTURAL_PRODUCT_BOOK.pdf ../ZION_ARCHITECTURAL_PRODUCT_BOOK_leve.pdf
rm -f ../_print_*.html
echo "== ok"
