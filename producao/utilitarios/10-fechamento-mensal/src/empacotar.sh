#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta10-Fechamento-Mensal-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta10-Fechamento-Mensal-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Fechamento-Mensal-Zion-EM-BRANCO.xlsx dist/Fechamento-Mensal-Zion-EXEMPLO.xlsx dist/Folha-de-Fechamento.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta10-Fechamento-Mensal-Zion) > "$Z"; unzip -l "$Z" | tail -1
