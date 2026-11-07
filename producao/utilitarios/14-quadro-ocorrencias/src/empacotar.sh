#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta14-Quadro-Ocorrencias-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta14-Quadro-Ocorrencias-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Quadro-Ocorrencias-Zion-EM-BRANCO.xlsx dist/Quadro-Ocorrencias-Zion-EXEMPLO.xlsx dist/Ficha-de-Ronda.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta14-Quadro-Ocorrencias-Zion) > "$Z"; unzip -l "$Z"
