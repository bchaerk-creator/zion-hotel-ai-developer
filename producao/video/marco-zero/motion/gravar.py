#!/usr/bin/env python3
"""Grava uma cena animada (window.seek) quadro a quadro e monta o MP4 com a narração.

Uso: python3 gravar.py mz01.html [--tempos 3,8,15] [--saida MZ01-motion.mp4]
Serve producao/video por HTTP (a cena usa o Three.js e as fontes do zion-video-engine).
"""
import argparse, functools, http.server, subprocess, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent  # producao/video
CHROMIUM = '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'

ap = argparse.ArgumentParser()
ap.add_argument('cena'); ap.add_argument('--tempos', default=''); ap.add_argument('--saida', default='')
ap.add_argument('--porta', type=int, default=8811); ap.add_argument('--fps', type=int, default=30)
a = ap.parse_args()


class Quieto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x):
        pass


srv = http.server.ThreadingHTTPServer(('127.0.0.1', a.porta), functools.partial(Quieto, directory=str(RAIZ)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
quadros = AQUI / 'quadros'
quadros.mkdir(exist_ok=True)
with sync_playwright() as p:
    nav = p.chromium.launch(executable_path=CHROMIUM, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    pg = nav.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('console', lambda m: print('[página]', m.text) if m.type == 'error' else None)
    pg.goto(f'http://127.0.0.1:{a.porta}/{AQUI.relative_to(RAIZ)}/{a.cena}')
    pg.wait_for_function('window.seek && window.pronto'); pg.evaluate('window.pronto')
    dur = pg.evaluate('window.DURACAO')
    alvo = [float(x) for x in a.tempos.split(',')] if a.tempos else [i / a.fps for i in range(int(dur * a.fps))]
    for i, t in enumerate(alvo):
        pg.evaluate('t => window.seek(t)', t)
        nome = quadros / (f'prev-{t:05.2f}.png' if a.tempos else f'{i:05d}.png')
        pg.screenshot(path=str(nome))
        if a.tempos:
            print(nome)
    nav.close()
srv.shutdown()

if not a.tempos:
    saida = AQUI / (a.saida or Path(a.cena).stem + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(a.fps), '-i', str(quadros / '%05d.png'),
                    '-i', str(AQUI / 'narracao.wav'), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:v', 'libx264', '-crf', '19',
                    '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                    '-shortest', '-movflags', '+faststart', str(saida)], check=True)
    print(saida)
