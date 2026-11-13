#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta19-Controle-Compras-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta19-Controle-Compras-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Controle-Compras-Zion-EM-BRANCO.xlsx dist/Controle-Compras-Zion-EXEMPLO.xlsx dist/Folha-de-Compras.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta19-Controle-Compras-Zion) > "$Z"; unzip -l "$Z"
