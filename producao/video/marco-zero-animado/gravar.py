#!/usr/bin/env python3
"""Grava um vídeo animado (VNN.html + audio/VNN.wav) quadro a quadro e monta as entregas.

  python3 gravar.py V01 --quadros 2,20,45,80,99,104   # só alguns quadros, para conferir
  python3 gravar.py V01                               # saida/V01-abertura.mp4, legenda, vertical
"""
import argparse, functools, http.server, json, subprocess, sys, threading
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / 'd01-territorio'))
import aula  # noqa: E402  (normalizar em -16 LUFS / -1,5 dBTP e quebra de legenda)

FPS, LIMITE = 30, 420
CHROMIUM = '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'
ENC_V = ['-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS)]


class Quieto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x):
        pass


def ass(blocos, destino):
    tempo = lambda t: f'{int(t // 3600)}:{int(t // 60 % 60):02d}:{t % 60:05.2f}'
    linhas = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1080', 'PlayResY: 1920', '', '[V4+ Styles]',
              'Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, '
              'Outline, Shadow, Alignment, MarginL, MarginR, MarginV',
              'Style: Default,Inter SemiBold,48,&H00FFFFFF,&H00000000,&H00000000,0,0,1,0,0,8,70,70,1310', '',
              '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    linhas += [f"Dialogue: 0,{tempo(a)},{tempo(b)},Default,,0,0,0,,{t.replace(chr(10), chr(92) + 'N')}" for a, b, t in blocos]
    destino.write_text('\n'.join(linhas) + '\n', encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video'); ap.add_argument('--quadros', default=''); ap.add_argument('--porta', type=int, default=8830)
    a = ap.parse_args()
    roteiro = json.loads((AQUI / 'roteiro.json').read_text(encoding='utf-8'))[a.video]
    dados = json.loads((AQUI / 'audio' / f'{a.video}.json').read_text(encoding='utf-8'))
    trab = AQUI / 'trabalho' / a.video
    trab.mkdir(parents=True, exist_ok=True)
    for p in ('saida/legendas', 'saida/verticais', 'saida/conferencia'):
        (AQUI / p).mkdir(parents=True, exist_ok=True)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', a.porta), functools.partial(Quieto, directory=str(AQUI)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    from playwright.sync_api import sync_playwright
    mudo = trab / 'mudo.mp4'
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROMIUM)
        pg = nav.new_page(viewport={'width': 1920, 'height': 1080})
        pg.on('console', lambda m: print('[página]', m.text) if m.type == 'error' else None)
        pg.goto(f'http://127.0.0.1:{a.porta}/{a.video}.html')
        pg.wait_for_function('window.pronto === true', timeout=60000)
        if a.quadros:
            for t in (float(x) for x in a.quadros.split(',')):
                pg.evaluate('t => window.seek(t)', t)
                destino = AQUI / 'saida/conferencia' / f'{a.video}-{t:06.1f}s.jpg'
                pg.screenshot(path=str(destino), type='jpeg', quality=88)
                print(destino)
            nav.close(); srv.shutdown()
            return
        enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS),
                                '-c:v', 'mjpeg', '-i', '-', *ENC_V, str(mudo)], stdin=subprocess.PIPE)
        for i in range(round(dados['total'] * FPS)):
            pg.evaluate('t => window.seek(t)', i / FPS)
            enc.stdin.write(pg.screenshot(type='jpeg', quality=92))
        enc.stdin.close(); enc.wait()
        nav.close()
    srv.shutdown()

    nome = f"{a.video}-{roteiro['slug']}"
    junto = trab / 'junto.mp4'
    aula.sh('ffmpeg', '-y', '-loglevel', 'error', '-i', mudo, '-i', AQUI / 'audio' / f'{a.video}.wav', '-map', '0:v',
            '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-shortest', junto)
    final = AQUI / 'saida' / f'{nome}.mp4'
    aula.normalizar(junto, final, video=True)

    blocos = []
    for f in dados['falas']:
        frases, atual = [], []
        for w in f['palavras']:
            atual.append(w)
            if w['p'][-1] in '.?!':
                frases.append(atual); atual = []
        if atual:
            frases.append(atual)
        for fr in frases:
            blocos += aula.legendas(' '.join(w['p'] for w in fr), fr[0]['a'], fr[-1]['b'])
    (AQUI / 'saida/legendas' / f'{a.video}.srt').write_text(
        '\n'.join(f'{i}\n{aula.tempo_srt(x)} --> {aula.tempo_srt(y)}\n{t}\n' for i, (x, y, t) in enumerate(blocos, 1)),
        encoding='utf-8')
    ass(blocos, trab / 'vertical.ass')
    aula.sh('ffmpeg', '-y', '-loglevel', 'error', '-i', final, '-filter_complex',
            f"[0:v]scale=1080:-2,pad=1080:1920:0:(1920-ih)/2:color=0x16261C,ass='{trab / 'vertical.ass'}'[v]",
            '-map', '[v]', '-map', '0:a', *ENC_V, '-c:a', 'copy', '-movflags', '+faststart',
            AQUI / 'saida/verticais' / f'{nome}.mp4')
    d = aula.duracao(final)
    print(f'{final.name}: {int(d // 60)}:{d % 60:04.1f}' + (f'  PASSOU de 7:00 por {d - LIMITE:.1f} s' if d > LIMITE else ''))


if __name__ == '__main__':
    main()
