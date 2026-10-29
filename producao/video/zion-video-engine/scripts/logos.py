#!/usr/bin/env python3
"""Gera assets/logos/logo_cream.png e logo_green.png a partir do logo branco com transparência."""
import sys
from PIL import Image
from comum import ASSETS, CORES, RAIZ

origem = sys.argv[1] if len(sys.argv) > 1 else RAIZ.parent.parent.parent / 'docs/escola/marco-zero/assets/logo.png'
logo = Image.open(origem).convert('RGBA')
alfa = logo.getchannel('A')
for nome, cor in (('cream', CORES['cream']), ('green', CORES['moss'])):
    rgb = tuple(int(cor[i:i + 2], 16) for i in (1, 3, 5))
    saida = Image.new('RGBA', logo.size, rgb + (0,))
    saida.putalpha(alfa)
    destino = ASSETS / 'logos' / f'logo_{nome}.png'
    saida.save(destino)
    print(destino)
