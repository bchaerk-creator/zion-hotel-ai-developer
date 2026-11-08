#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta05-Orcamento-Cabana-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta05-Orcamento-Cabana-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Orcamento-Cabana-Zion-EM-BRANCO.xlsx dist/Orcamento-Cabana-Zion-EXEMPLO.xlsx dist/Ficha-de-Cotacao.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta05-Orcamento-Cabana-Zion) > "$Z"; unzip -l "$Z"
