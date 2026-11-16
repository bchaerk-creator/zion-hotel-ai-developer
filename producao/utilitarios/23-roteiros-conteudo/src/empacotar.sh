#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta23-Roteiros-Conteudo-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta23-Roteiros-Conteudo-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Roteiros-Conteudo-Zion-EM-BRANCO.xlsx dist/Roteiros-Conteudo-Zion-EXEMPLO.xlsx dist/Roteiros-Modelo.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta23-Roteiros-Conteudo-Zion) > "$Z"; unzip -l "$Z"
