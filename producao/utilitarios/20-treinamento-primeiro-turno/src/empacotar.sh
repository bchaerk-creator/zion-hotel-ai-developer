#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta20-Treinamento-Primeiro-Turno-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta20-Treinamento-Primeiro-Turno-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Treinamento-Primeiro-Turno-Zion-EM-BRANCO.xlsx dist/Treinamento-Primeiro-Turno-Zion-EXEMPLO.xlsx dist/Ficha-do-Primeiro-Turno.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta20-Treinamento-Primeiro-Turno-Zion) > "$Z"; unzip -l "$Z"
