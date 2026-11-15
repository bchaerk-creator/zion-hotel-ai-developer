#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta22-Campanhas-Baixa-Procura-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta22-Campanhas-Baixa-Procura-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Campanhas-Baixa-Procura-Zion-EM-BRANCO.xlsx dist/Campanhas-Baixa-Procura-Zion-EXEMPLO.xlsx dist/Ficha-de-Campanha.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta22-Campanhas-Baixa-Procura-Zion) > "$Z"; unzip -l "$Z"
