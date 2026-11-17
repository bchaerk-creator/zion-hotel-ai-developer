#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta16-Parcerias-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta16-Parcerias-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Parcerias-Zion-EM-BRANCO.xlsx dist/Parcerias-Zion-EXEMPLO.xlsx dist/Ficha-de-Acordo-com-Parceiro.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta16-Parcerias-Zion) > "$Z"; unzip -l "$Z"
