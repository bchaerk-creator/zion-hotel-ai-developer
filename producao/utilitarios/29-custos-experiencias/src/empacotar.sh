#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta29-Custos-Experiencias-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta29-Custos-Experiencias-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Custos-Experiencias-Zion-EM-BRANCO.xlsx dist/Custos-Experiencias-Zion-EXEMPLO.xlsx dist/Ficha-da-Experiencia.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta29-Custos-Experiencias-Zion) > "$Z"; unzip -l "$Z"
