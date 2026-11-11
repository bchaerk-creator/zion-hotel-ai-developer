#!/bin/bash
# Monta o ZIP exclusivo do produto a partir de dist/. Uso: bash src/empacotar.sh
set -e; cd "$(dirname "$0")/.."
Z=dist/Ferramenta30-Briefing-Experiencia-Zion.zip; T=$(mktemp -d); P="$T/Ferramenta30-Briefing-Experiencia-Zion"; mkdir -p "$P"
cp src/LEIA-ME.txt dist/Briefing-Experiencia-Zion-EM-BRANCO.xlsx dist/Briefing-Experiencia-Zion-EXEMPLO.xlsx dist/Mensagens-Modelo-Experiencia.pdf dist/Guia-Aprenda-o-Passo-a-Passo.pdf "$P/"
rm -f "$Z"; (cd "$T" && zip -qr - Ferramenta30-Briefing-Experiencia-Zion) > "$Z"; unzip -l "$Z"
