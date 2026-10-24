#!/usr/bin/env python3
"""Renderiza quadros de uma aula: sobe um servidor HTTP na raiz do motor, abre o template e
chama window.render(t, frame) para cada quadro, salvando lessons/<id>/out/NNNNN.jpg.

Uso: python3 scripts/render.py --lesson p01-a01 [--tempos 1,4,8] [--inicio 0 --fim 300] [--porta 8765]
--tempos gera só esses instantes (folha de contato); sem ele, renderiza do quadro --inicio ao --fim.
"""
import functools
import http.server
import json
import threading
from playwright.sync_api import sync_playwright
from comum import RAIZ, args_aula, chromium_path


def extra(ap):
    ap.add_argument('--template', default='aula_16x9.html')
    ap.add_argument('--tempos', default='')
    ap.add_argument('--inicio', type=int, default=0)
    ap.add_argument('--fim', type=int, default=None)
    ap.add_argument('--fps', type=float, default=30)
    ap.add_argument('--porta', type=int, default=8765)
    ap.add_argument('--gpu', action='store_true', help='usar a GPU da máquina em vez do SwiftShader')


def main():
    a = args_aula('Render de quadros da aula', extra)
    class Silencioso(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *x):
            pass
    Handler = functools.partial(Silencioso, directory=str(RAIZ))
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', a.porta), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    out = a.pasta / 'out'
    out.mkdir(exist_ok=True)
    tl = json.loads((a.pasta / 'timeline.json').read_text())
    if a.tempos:
        alvo = [(float(t), round(float(t) * a.fps)) for t in a.tempos.split(',')]
    else:
        fim = a.fim if a.fim is not None else round(tl['total'] * a.fps)
        alvo = [(f / a.fps, f) for f in range(a.inicio, fim)]
    flags = [] if a.gpu else ['--use-angle=swiftshader', '--enable-unsafe-swiftshader']
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=chromium_path(), args=flags)
        pg = nav.new_page(viewport={'width': 1920, 'height': 1080})
        pg.on('console', lambda m: print('[página]', m.text) if m.type == 'error' else None)
        pg.goto(f'http://127.0.0.1:{a.porta}/templates/{a.template}?lesson={a.lesson}')
        pg.wait_for_function('window.render && window.pronto')
        pg.evaluate('window.pronto')
        for t, f in alvo:
            pg.evaluate('([t, f]) => window.render(t, f)', [t, f])
            nome = out / (f't{t:07.2f}.jpg' if a.tempos else f'{f:05d}.jpg')
            pg.screenshot(path=str(nome), type='jpeg', quality=92)
            if a.tempos:
                print(nome)
        sfx = pg.evaluate('window.SFX')
        (a.pasta / f'sfx_{alvo[0][1]:05d}.json').write_text(json.dumps(sfx))
        nav.close()
    srv.shutdown()


if __name__ == '__main__':
    main()
