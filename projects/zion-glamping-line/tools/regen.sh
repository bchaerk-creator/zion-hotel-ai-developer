#!/usr/bin/env bash
# Regenera toda a linha (desenhos, DXF, 3D, renders, cadernos, PDFs) a partir de geometry.py.
# Uso: bash tools/regen.sh [--no-render]   (a partir da raiz projects/zion-glamping-line)
set -e
cd "$(dirname "$0")"
export NODE_PATH=/opt/node22/lib/node_modules
echo "== desenhos"; python3 drawings_cocoon.py && python3 drawings_zenith.py && python3 iso.py && python3 details.py && python3 drawings_extra.py && python3 exploded.py
echo "== pranchas PA + DXF"; python3 pa_sheets.py && python3 lodge_family.py && python3 capsule.py && python3 interiores_cocoon.py && python3 export_dxf.py > /dev/null
if [[ "$1" != "--no-render" ]]; then
  echo "== 3D + renders"; python3 build_viewer.py && node render.js
  echo "== renders web (1400 px) e deck (sem interface), com a marca Zion"; python3 brand_renders.py
  echo "== vídeo de órbita 3D do Casulo"; node turntable.js --model cocoon --seconds 14
fi
echo "== caderno técnico"; python3 build_dossier.py && python3 build_dossier.py --web && python3 build_dossier.py --inline
echo "== product book"; python3 build_product_book.py && python3 build_product_book.py --web && python3 build_product_book.py --inline
echo "== projeto arquitetônico + apresentação"; python3 build_projeto_arquitetonico.py && python3 build_projeto_arquitetonico.py --inline && python3 build_apresentacao.py && python3 build_catalogo.py && python3 referencias.py && python3 build_brief.py && python3 build_conceito.py && python3 build_tecnico.py && python3 build_interiores.py
echo "== lonas (padrões de corte) e lotes"; python3 lona.py && python3 build_lotes.py
echo "== PDFs"
node export_pdf.js ../_print_ZION_CASULO_SAFARI_Caderno_Tecnico.html ../ZION_CASULO_SAFARI_Caderno_Tecnico.pdf
node export_pdf.js ../_print_ZION_ARCHITECTURAL_PRODUCT_BOOK.html ../ZION_ARCHITECTURAL_PRODUCT_BOOK.pdf
node export_pdf.js ../ZION_PROJETO_ARQUITETONICO.html ../ZION_PROJETO_ARQUITETONICO.pdf
node export_pdf.js ../ZION_PROJETO_ARQUITETONICO_Apresentacao.html ../ZION_PROJETO_ARQUITETONICO_Apresentacao.pdf
node export_pdf.js ../ZION_CATALOGO_LINHA.html ../ZION_CATALOGO_LINHA.pdf
node export_pdf.js ../interno/ZION_REFERENCIAS_NOMASTRA_H23_H28.html ../interno/ZION_REFERENCIAS_NOMASTRA_H23_H28.pdf
node export_pdf.js ../00_BRIEFING/ZG-BRF-001_ZION_CABIN_DESIGN_BRIEF.html ../00_BRIEFING/ZG-BRF-001_ZION_CABIN_DESIGN_BRIEF.pdf
node export_pdf.js ../02_CONCEITO/ZG-ARQ-001_Documento_Conceitual_Visual.html ../02_CONCEITO/ZG-ARQ-001_Documento_Conceitual_Visual.pdf
node export_pdf.js ../03_TECNICO/ZG-TEC-001_Documento_Tecnico.html ../03_TECNICO/ZG-TEC-001_Documento_Tecnico.pdf
node export_pdf.js ../04_INTERIORES/ZC-INT-001_Projeto_Interiores_Casulo.html ../04_INTERIORES/ZC-INT-001_Projeto_Interiores_Casulo.pdf
for f in ../06_LOTES/*.html; do node export_pdf.js "$f" "${f%.html}.pdf"; done
python3 pdf_leve.py ../ZION_ARCHITECTURAL_PRODUCT_BOOK.pdf ../ZION_ARCHITECTURAL_PRODUCT_BOOK_leve.pdf
rm -f ../_print_*.html
echo "== ok"
