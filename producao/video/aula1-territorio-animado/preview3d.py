#!/usr/bin/env python3
"""Grava a prévia 3D (preview3d.html, Fala 1 do V01) com WebGL por software.

  python3 preview3d.py --quadros 3,8,15,19   # conferir
  python3 preview3d.py                       # saida/previa-3d.mp4
"""
import argparse, functools, http.server, subprocess, threading
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CHROMIUM = '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'
FPS = 30


class Quieto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x):
        pass


ap = argparse.ArgumentParser(); ap.add_argument('--quadros', default=''); a = ap.parse_args()
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 8840), functools.partial(Quieto, directory=str(AQUI)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
from playwright.sync_api import sync_playwright
(AQUI / 'saida/conferencia').mkdir(parents=True, exist_ok=True)
mudo = AQUI / 'trabalho' / 'previa-3d-mudo.mp4'
with sync_playwright() as p:
    nav = p.chromium.launch(executable_path=CHROMIUM, args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader',
                                                            '--ignore-gpu-blocklist'])
    pg = nav.new_page(viewport={'width': 1920, 'height': 1080})
    pg.on('console', lambda m: print('[página]', m.text) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:8840/preview3d.html')
    pg.wait_for_function('window.pronto3d === true', timeout=120000)
    if a.quadros:
        for t in (float(x) for x in a.quadros.split(',')):
            pg.evaluate('t => window.seek(t)', t)
            pg.screenshot(path=str(AQUI / 'saida/conferencia' / f'3d-{t:05.1f}.jpg'), type='jpeg', quality=88)
    else:
        enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg',
                                '-i', '-', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', str(mudo)], stdin=subprocess.PIPE)
        for i in range(round(20.6 * FPS)):
            pg.evaluate('t => window.seek(t)', i / FPS)
            enc.stdin.write(pg.screenshot(type='jpeg', quality=92))
        enc.stdin.close(); enc.wait()
    nav.close()
srv.shutdown()
if not a.quadros:
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(mudo), '-i', str(AQUI / 'audio/V01.wav'), '-map', '0:v', '-map', '1:a',
                    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                    '-shortest', '-movflags', '+faststart', str(AQUI / 'saida/previa-3d.mp4')], check=True)
    print(AQUI / 'saida/previa-3d.mp4')
