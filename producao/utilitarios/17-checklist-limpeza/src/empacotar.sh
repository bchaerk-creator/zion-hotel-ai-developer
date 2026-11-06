#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta17-Checklist-Limpeza-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta17-Checklist-Limpeza-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Checklist-Limpeza-Zion-EM-BRANCO.xlsx dist/Checklist-Limpeza-Zion-EXEMPLO.xlsx dist/Checklist-Imprimivel.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta17-Checklist-Limpeza-Zion) > "$Z"; unzip -l "$Z"
