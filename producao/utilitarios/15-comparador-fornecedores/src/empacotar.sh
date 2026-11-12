#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta15-Comparador-Fornecedores-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta15-Comparador-Fornecedores-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Comparador-Fornecedores-Zion-EM-BRANCO.xlsx dist/Comparador-Fornecedores-Zion-EXEMPLO.xlsx dist/Roteiro-de-Cotacao.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta15-Comparador-Fornecedores-Zion) > "$Z"; unzip -l "$Z"
