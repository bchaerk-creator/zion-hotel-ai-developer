#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta18-Manutencao-Preventiva-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta18-Manutencao-Preventiva-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Manutencao-Preventiva-Zion-EM-BRANCO.xlsx dist/Manutencao-Preventiva-Zion-EXEMPLO.xlsx dist/Ficha-de-Ronda-Preventiva.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta18-Manutencao-Preventiva-Zion) > "$Z"; unzip -l "$Z"
