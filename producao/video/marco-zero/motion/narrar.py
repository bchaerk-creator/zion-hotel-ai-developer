#!/usr/bin/env python3
"""Narra frases com o Kokoro (pm_alex) e grava o áudio e os tempos de cada frase e palavra.
Com --clonar, troca o timbre pela voz do Bruno (clonar.py). PRONUNCIA corrige só a fala; a legenda mantém o texto.
Uso: python3 narrar.py [--velocidade 0.9] <saida-sem-extensao> "frase 1" "frase 2" ...  ->  <saida>.wav e <saida>.json
"""
import json, re, sys
from pathlib import Path
import numpy as np, soundfile as sf
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'd01-territorio'))
import aula  # noqa: E402

aula.AQUI = Path(__file__).resolve().parents[2] / 'd01-territorio'
args = sys.argv[1:]
velocidade, clonar = 1.0, '--clonar' in args
args = [x for x in args if x != '--clonar']
if args[0] == '--velocidade':
    velocidade, args = float(args[1]), args[2:]
# como o modelo lê palavras de fora; a troca vale só para a voz, palavra por palavra
PRONUNCIA = {'Zion': 'Záion', 'Group': 'Grúpi'}
falado = lambda f: ' '.join(PRONUNCIA.get(re.sub(r'\W', '', w), None) and w.replace(re.sub(r'\W', '', w), PRONUNCIA[re.sub(r'\W', '', w)]) or w for w in f.split())
saida, frases = args[0], args[1:]
k = aula.kokoro()
sr, gap, t = 24000, 0.22, 0.5
partes, tempos = [np.zeros(int(t * sr), np.float32)], []
for f in frases:
    a, _ = k.create(falado(f), voice='pm_alex', speed=velocidade, lang='pt-br')
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 240): idx[-1] + 480]
    d = len(a) / sr
    pal = f.split(); pesos = [len(re.sub(r'\W', '', p)) + 2 for p in pal]; acc = 0; palavras = []
    for p, w in zip(pal, pesos):
        palavras.append({'p': p, 't': round(t + d * acc / sum(pesos), 3)}); acc += w
    tempos.append({'frase': f, 'a': round(t, 3), 'b': round(t + d, 3), 'palavras': palavras})
    partes += [a, np.zeros(int(gap * sr), np.float32)]; t += d + gap
partes.append(np.zeros(int(1.0 * sr), np.float32))
sf.write(saida + '.wav', np.concatenate(partes), sr)
if clonar:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from clonar import clonar as trocar_timbre
    sf.write(saida + '-kokoro.wav', np.concatenate(partes), sr)
    trocar_timbre(saida + '-kokoro.wav', saida + '.wav')
json.dump({'total': round(t + 1.0, 2), 'frases': tempos}, open(saida + '.json', 'w'), ensure_ascii=False, indent=1)
for x in tempos:
    print(f"{x['a']:6.2f} {x['b']:6.2f}  {x['frase']}")
print('total', round(t + 1.0, 2))
