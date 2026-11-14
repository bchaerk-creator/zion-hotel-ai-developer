#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta12-Fotos-Comodidades-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta12-Fotos-Comodidades-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Fotos-Comodidades-Zion-EM-BRANCO.xlsx dist/Fotos-Comodidades-Zion-EXEMPLO.xlsx dist/Roteiro-do-Dia-das-Fotos.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta12-Fotos-Comodidades-Zion) > "$Z"; unzip -l "$Z"
