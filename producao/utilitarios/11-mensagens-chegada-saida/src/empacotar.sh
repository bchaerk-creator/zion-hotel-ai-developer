#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta11-Kit-Mensagens-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta11-Kit-Mensagens-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Kit-Mensagens-Zion-EM-BRANCO.xlsx dist/Kit-Mensagens-Zion-EXEMPLO.xlsx dist/Mensagens-Modelo.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta11-Kit-Mensagens-Zion) > "$Z"; unzip -l "$Z" | tail -8
