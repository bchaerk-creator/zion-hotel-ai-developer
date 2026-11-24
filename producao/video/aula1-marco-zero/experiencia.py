#!/usr/bin/env python3
"""Aula 1 em formato de experiência: o slide continua o mesmo, mas a câmera vai até o que está sendo falado,
o ponto ganha destaque, a legenda acompanha a fala, as perguntas aparecem para o aluno e as pausas viram
"sua vez" com cronômetro.

  python3 experiencia.py preparar --videos 1      # trabalho/exp/V01.json + V01.wav (precisa de audio/NN.mp3 e .json)
  python3 experiencia.py gravar --videos 1        # saida/experiencia/V01 - ....mp4
  python3 experiencia.py gravar --videos 1 --quadros 3,40,95   # só alguns quadros para conferir

Os tempos de cada trecho falado vêm de audio/NN.json (a1.py narrar, motor google).
"""
import argparse, functools, http.server, json, re, subprocess, sys, threading, unicodedata
from difflib import SequenceMatcher
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import a1  # noqa: E402
from a1 import aula, sh, duracao, tempo_srt, ENC_V, ENC_A, FPS, RESPIRO, PAUSA, LIMITE  # noqa: E402

ESCALA = 1920 / 1440  # o PDF tem 1440x810 pontos
CHROMIUM = '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'


def plano(txt):
    """Só letras, sem acento e sem espaço: o PDF tem espaçamento quebrado entre as letras."""
    t = unicodedata.normalize('NFD', txt.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in t if unicodedata.category(c) != 'Mn'))


def regioes(pdf, n):
    """Cartões (retângulos desenhados) com o texto de dentro, blocos de texto soltos e fotos, em pixels 1920x1080."""
    pg = pdf[n - 1]
    area = pg.rect.width * pg.rect.height
    cartoes = [d['rect'] for d in pg.get_drawings()
               if 0.008 * area < d['rect'].width * d['rect'].height < 0.4 * area]
    palavras = pg.get_text('words')
    dentro = lambda w, r: r.x0 - 2 <= (w[0] + w[2]) / 2 <= r.x1 + 2 and r.y0 - 2 <= (w[1] + w[3]) / 2 <= r.y1 + 2
    saida = []
    for r in cartoes:
        txt = ''.join(w[4] for w in palavras if dentro(w, r))
        saida.append({'caixa': [r.x0, r.y0, r.x1, r.y1], 'texto': plano(txt)})
    for b in pg.get_text('dict')['blocks']:
        x0, y0, x1, y1 = b['bbox']
        if y1 < 60 or y0 > 720:  # selo do bloco no topo e rodapé
            continue
        if b['type'] == 1:
            if (x1 - x0) * (y1 - y0) < 0.6 * area:
                saida.append({'caixa': [x0, y0, x1, y1], 'texto': '', 'foto': True})
            continue
        ws = [w for w in palavras if x0 - 1 <= (w[0] + w[2]) / 2 <= x1 + 1 and y0 - 1 <= (w[1] + w[3]) / 2 <= y1 + 1
              and not any(dentro(w, r) for r in cartoes)]
        if ws:
            saida.append({'caixa': [min(w[0] for w in ws), min(w[1] for w in ws), max(w[2] for w in ws),
                                    max(w[3] for w in ws)], 'texto': plano(''.join(w[4] for w in ws))})
    for r in saida:
        r['caixa'] = [round(v * ESCALA) for v in r['caixa']]
    return [r for r in saida if r['texto'] or r.get('foto')]


def foco(trecho, regs):
    """A região cujo texto mais se parece com o trecho falado (ou nenhuma)."""
    c = plano(trecho)
    melhor, nota = None, 0
    for r in regs:
        if not r['texto']:
            continue
        blocos = SequenceMatcher(None, c, r['texto'], autojunk=False).get_matching_blocks()
        total = sum(m.size for m in blocos if m.size >= 4)
        if total >= max(8, min(16, 0.5 * min(len(c), len(r['texto'])))) and total > nota:
            melhor, nota = r, total
    return melhor['caixa'] if melhor else None


def cmd_preparar(a):
    import pymupdf
    pdf = pymupdf.open(AQUI / 'slides.pdf')
    pasta = AQUI / 'trabalho/exp'
    (pasta / 'voz').mkdir(parents=True, exist_ok=True)
    videos = a1.roteiro()
    for v in videos:
        if v['n'] not in a1.faixa(a.videos):
            continue
        paginas, lista, t = [], [], 0.0
        for pg in v['paginas']:
            voz = pasta / 'voz' / f"{pg['p']:02d}.wav"
            aula.normalizar(AQUI / 'audio' / f"{pg['p']:02d}.mp3", voz)
            fala = duracao(voz)
            dur = fala + RESPIRO + (PAUSA if pg['pausa'] else 0)
            preso = pasta / 'voz' / f"{pg['p']:02d}-pagina.wav"
            sh('ffmpeg', '-y', '-loglevel', 'error', '-i', voz, '-af', 'apad', '-t', f'{dur:.3f}', '-ar', '48000', '-ac', '2', preso)
            lista.append(f"file '{preso.name}'")
            regs = regioes(pdf, pg['p'])
            trechos = json.loads((AQUI / 'audio' / f"{pg['p']:02d}.json").read_text(encoding='utf-8'))
            for tr in trechos:
                tr['foco'] = foco(tr['texto'], regs)
            paginas.append({'p': pg['p'], 'img': f"slides/p-{pg['p']:02d}.png", 'ini': round(t, 3), 'dur': round(dur, 3),
                            'fala': round(fala, 3), 'pausa': pg['pausa'], 'foto': pg['foto'], 'trechos': trechos})
            t += dur
        (pasta / 'voz' / f"lista{v['n']:02d}.txt").write_text('\n'.join(lista))
        sh('ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', pasta / 'voz' / f"lista{v['n']:02d}.txt",
           pasta / f"V{v['n']:02d}.wav")
        proximo = videos[v['n']]['titulo'] if v['n'] < 7 else ''
        dados = {'n': v['n'], 'titulo': v['titulo'], 'proximo': proximo, 'total': round(t, 3), 'paginas': paginas}
        (pasta / f"V{v['n']:02d}.json").write_text(json.dumps(dados, ensure_ascii=False), encoding='utf-8')
        focos = sum(1 for p in paginas for tr in p['trechos'] if tr['foco'])
        print(f"V{v['n']:02d} {v['titulo']}: {t / 60:.0f}:{t % 60:04.1f}, {focos} destaques em "
              f"{sum(len(p['trechos']) for p in paginas)} trechos")


class Quieto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x):
        pass


def cmd_gravar(a):
    from playwright.sync_api import sync_playwright
    porta = 8820
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', porta), functools.partial(Quieto, directory=str(AQUI)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    (AQUI / 'saida/experiencia').mkdir(parents=True, exist_ok=True)
    (AQUI / 'saida/conferencia').mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROMIUM)
        for n in a1.faixa(a.videos):
            dados = json.loads((AQUI / f'trabalho/exp/V{n:02d}.json').read_text(encoding='utf-8'))
            pg = nav.new_page(viewport={'width': 1920, 'height': 1080})
            pg.on('console', lambda m: print('[página]', m.text) if m.type == 'error' else None)
            pg.goto(f'http://127.0.0.1:{porta}/experiencia.html?v={n:02d}')
            pg.wait_for_function('window.pronto === true', timeout=60000)
            if a.quadros:
                for t in (float(x) for x in a.quadros.split(',')):
                    pg.evaluate('t => window.seek(t)', t)
                    destino = AQUI / 'saida/conferencia' / f'EXP{n:02d}-{t:06.1f}s.jpg'
                    pg.screenshot(path=str(destino), type='jpeg', quality=88)
                    print(destino)
                pg.close()
                continue
            nome = f"V{n:02d} - {dados['titulo']}"
            mudo = AQUI / 'trabalho/exp' / f'V{n:02d}-mudo.mp4'
            enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS),
                                    '-c:v', 'mjpeg', '-i', '-', *ENC_V, str(mudo)], stdin=subprocess.PIPE)
            quadros = round(dados['total'] * FPS)
            for i in range(quadros):
                pg.evaluate('t => window.seek(t)', i / FPS)
                enc.stdin.write(pg.screenshot(type='jpeg', quality=92))
                if i % (FPS * 30) == 0:
                    print(f'  V{n:02d} {i / FPS:6.0f} s de {dados["total"]:.0f} s', flush=True)
            enc.stdin.close(); enc.wait()
            pg.close()
            junto = AQUI / 'trabalho/exp' / f'V{n:02d}-junto.mp4'
            sh('ffmpeg', '-y', '-loglevel', 'error', '-i', mudo, '-i', AQUI / 'trabalho/exp' / f'V{n:02d}.wav',
               '-map', '0:v', '-map', '1:a', '-c:v', 'copy', *ENC_A, '-shortest', junto)
            final = AQUI / 'saida/experiencia' / f'{nome}.mp4'
            aula.normalizar(junto, final, video=True)
            blocos = []
            for p_ in dados['paginas']:
                for tr in p_['trechos']:
                    blocos += aula.legendas(tr['texto'], p_['ini'] + tr['a'], p_['ini'] + tr['b'])
            (AQUI / 'saida/experiencia' / f'V{n:02d}.srt').write_text(
                '\n'.join(f'{i}\n{tempo_srt(x)} --> {tempo_srt(y)}\n{t}\n' for i, (x, y, t) in enumerate(blocos, 1)),
                encoding='utf-8')
            d = duracao(final)
            aviso = f'  PASSOU de 7:00 por {d - LIMITE:.1f} s (não cortei nem acelerei)' if d > LIMITE else ''
            print(f'{final.name}: {int(d // 60)}:{d % 60:04.1f}{aviso}')
        nav.close()
    srv.shutdown()


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('preparar'); p.add_argument('--videos', default=''); p.set_defaults(f=cmd_preparar)
    p = sub.add_parser('gravar'); p.add_argument('--videos', default=''); p.add_argument('--quadros', default='')
    p.set_defaults(f=cmd_gravar)
    a = ap.parse_args()
    a.f(a)
