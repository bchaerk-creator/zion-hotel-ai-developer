#!/usr/bin/env python3
"""Narra um vídeo do roteiro.json e grava o tempo de cada palavra, para a animação entrar na palavra certa.

  python3 narrar.py V01        ->  audio/V01.wav e audio/V01.json

Voz: Kokoro pm_alex (0,85), frase a frase; ou Google pt-BR, um pedido por trecho. O tempo de cada trecho é exato; dentro do trecho,
cada palavra recebe o tempo pelo peso das letras. Com audio/V01.m4a (a voz do Bruno), use alinhar.py no lugar.
"""
import json, re, subprocess, sys, unicodedata, urllib.parse, urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MOTOR = 'kokoro'  # a voz aprovada pelo Bruno: Kokoro pm_alex, 0,85, frase a frase. 'google' fica como alternativa.
PRONUNCIA = {'Zion': 'Záion', 'Group': 'Grúpi', 'Bubble': 'Bâbol'}
_K = None


def kokoro():
    global _K
    if _K is None:
        sys.path.insert(0, str(AQUI.parent / 'd01-territorio'))
        import aula
        aula.AQUI = AQUI.parent / 'd01-territorio'
        _K = aula.kokoro()
    return _K  # só a voz; a legenda mantém o texto
INICIO, ENTRE_FALAS, FIM = 0.6, 0.8, 1.5


def sh(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def duracao(arq):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(arq)],
                                capture_output=True, text=True, check=True).stdout)


def falado(t):
    return re.sub(r'\b(' + '|'.join(PRONUNCIA) + r')\b', lambda m: PRONUNCIA[m.group(1)], t)


def trechos(texto):
    """Google: frases e vírgulas (trecho curto, tempo de palavra mais preciso). Kokoro: frase inteira, com respiro."""
    if MOTOR == 'kokoro':
        return [(f, 0.45) for f in re.split(r'(?<=[.?!])\s+', texto.strip())]
    saida = []
    for frase in re.split(r'(?<=[.?!])\s+', texto.strip()):
        partes = re.split(r'(?<=[,;:])\s+', frase)
        for i, p in enumerate(partes):
            saida.append((p, 0.36 if i == len(partes) - 1 else 0.1))
    return saida


def plano(p):
    t = unicodedata.normalize('NFD', p.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in t if unicodedata.category(c) != 'Mn'))


def main(vid):
    roteiro = json.loads((AQUI / 'roteiro.json').read_text(encoding='utf-8'))[vid]
    trab = AQUI / 'trabalho' / vid
    trab.mkdir(parents=True, exist_ok=True)
    (AQUI / 'audio').mkdir(exist_ok=True)
    sh('ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', INICIO, trab / 'sil0.wav')
    lista, t, falas, k = ["file 'sil0.wav'"], INICIO, [], 0
    for nf, fala in enumerate(roteiro['falas']):
        palavras, ini = [], t
        for texto, pausa in trechos(fala['texto']):
            k += 1
            wav = trab / f'{k:03d}.wav'
            if MOTOR == 'kokoro':
                import numpy as np, soundfile as sf
                audio, taxa = kokoro().create(falado(texto), voice='pm_alex', speed=0.85, lang='pt-br')
                idx = np.where(np.abs(audio) > 0.01)[0]
                sf.write(wav, audio[max(0, idx[0] - 240): idx[-1] + 600], taxa)
            else:
                mp3 = trab / f'{k:03d}.mp3'
                url = 'https://translate.googleapis.com/translate_tts?' + urllib.parse.urlencode(
                    {'client': 'gtx', 'ie': 'UTF-8', 'tl': 'pt-BR', 'q': falado(texto)})
                mp3.write_bytes(urllib.request.urlopen(url, timeout=60).read())
                sh('ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-af',
                   'silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
                   'silenceremove=start_periods=1:start_threshold=-45dB,areverse', '-ar', '24000', '-ac', '1', wav)
            d = duracao(wav)
            pal = texto.split()
            peso = [len(plano(p)) + 1.5 for p in pal]
            acc = 0
            for p, w in zip(pal, peso):
                palavras.append({'p': p, 'a': round(t + d * acc / sum(peso), 3), 'b': round(t + d * (acc + w) / sum(peso), 3)})
                acc += w
            lista.append(f"file '{wav.name}'")
            t += d
            depois = pausa
            if texto is trechos(fala['texto'])[-1][0]:
                depois = 0
            if depois:
                sh('ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', depois,
                   trab / f'p{k:03d}.wav')
                lista.append(f"file 'p{k:03d}.wav'")
                t += depois
        fim_fala = t
        segura = fala.get('pausa', 0) + (ENTRE_FALAS if nf < len(roteiro['falas']) - 1 else roteiro.get('fim', FIM))
        sh('ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', segura,
           trab / f'f{nf}.wav')
        lista.append(f"file 'f{nf}.wav'")
        t += segura
        falas.append({'n': nf + 1, 'a': round(ini, 3), 'b': round(fim_fala, 3), 'pausa': fala.get('pausa', 0),
                      'texto': fala['texto'], 'palavras': palavras})
    (trab / 'lista.txt').write_text('\n'.join(lista))
    sh('ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', trab / 'lista.txt', '-ar', '48000',
       AQUI / 'audio' / f'{vid}.wav')
    total = duracao(AQUI / 'audio' / f'{vid}.wav')
    dados = {'video': vid, 'titulo': roteiro['titulo'], 'bloco': roteiro['bloco'], 'total': round(total, 3), 'falas': falas}
    (AQUI / 'audio' / f'{vid}.json').write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding='utf-8')
    for f in falas:
        print(f"fala {f['n']}: {f['a']:6.2f} a {f['b']:6.2f} s{'  [PAUSA]' if f['pausa'] else ''}")
    print(f'total {total:.1f} s')


if __name__ == '__main__':
    main(sys.argv[1])
