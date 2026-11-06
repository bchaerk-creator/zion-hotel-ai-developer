#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta13-Controle-Enxoval-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta13-Controle-Enxoval-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Controle-Enxoval-Zion-EM-BRANCO.xlsx dist/Controle-Enxoval-Zion-EXEMPLO.xlsx dist/Ficha-de-Contagem.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta13-Controle-Enxoval-Zion) > "$Z"; unzip -l "$Z"
