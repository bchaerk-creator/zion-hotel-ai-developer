#!/usr/bin/env python3
"""Edição de Black Friday da Zion: o vídeo do casal com a camada gráfica de bf.html por cima.

  python3 editar.py <video.mov> --quadros 1,6,23,40,59   # conferir
  python3 editar.py <video.mov>                          # saida/Black Friday Zion - Reels.mp4 (1080x1920)
"""
import argparse, subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
# o chrome completo não tira captura neste ambiente; o headless shell da mesma versão tira
CHROMIUM = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell'
FPS = 30


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--quadros', default='')
    a = ap.parse_args()
    quadros, saida = AQUI / 'trabalho/quadros', AQUI / 'saida'
    quadros.mkdir(parents=True, exist_ok=True); saida.mkdir(exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROMIUM)
        pg = nav.new_page(viewport={'width': 1080, 'height': 1920})
        pg.goto((AQUI / "bf.html").as_uri(), wait_until="commit")  # arquivo local: o servidor HTTP travava neste ambiente
        pg.wait_for_function("window.pronto === true", timeout=60000, polling=100)
        print("página pronta", flush=True)
        total = pg.evaluate('window.DURACAO')
        tempos = [float(x) for x in a.quadros.split(',')] if a.quadros else [i / FPS for i in range(round(total * FPS))]
        for i, t in enumerate(tempos):
            pg.evaluate('t => window.seek(t)', t)
            pg.screenshot(path=str(quadros / f'{i:05d}.png'), omit_background=True)
        nav.close()

    fim = total - 57.03
    destino = saida / ('Black Friday Zion - conferencia.mp4' if a.quadros else 'Black Friday Zion - Reels.mp4')
    entrada_overlay = ['-framerate', str(FPS) if not a.quadros else '1', '-i', str(quadros / '%05d.png')]
    # o vídeo base, já esticado com o último quadro por baixo do cartão final, sai antes num arquivo próprio:
    # dentro do mesmo grafo do overlay o tpad não esticava a imagem
    base = AQUI / 'trabalho/base.mp4'
    if not a.quadros:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', a.video, '-vf',
                        f'scale=1080:1920:flags=lanczos,setsar=1,fps={FPS},tpad=stop_mode=clone:stop_duration={fim:.2f}',
                        '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-c:a', 'copy', str(base)], check=True)
    filtro = (f"[0:v][1:v]overlay=0:0[o];"
              f"[0:a]afade=t=out:st=55.6:d=1.4,apad,atrim=0:{total:.2f},loudnorm=I=-14:TP=-1.0:LRA=11[a]")
    if a.quadros:  # um quadro do vídeo para cada tempo pedido, com a camada por cima
        for i, t in enumerate(tempos):
            tv = min(t, 56.9)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(tv), '-i', a.video, '-i', str(quadros / f'{i:05d}.png'),
                            '-filter_complex', '[0:v]scale=1080:1920:flags=lanczos[v];[v][1:v]overlay=0:0',
                            '-frames:v', '1', str(saida / f'quadro-{t:05.1f}.jpg')], check=True)
        print('quadros em', saida)
        return
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(base), *entrada_overlay, '-filter_complex', filtro,
                    '-map', '[o]', '-map', '[a]', '-t', f'{total:.2f}', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium',
                    '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                    '-movflags', '+faststart', str(destino)], check=True)
    print(destino)


if __name__ == '__main__':
    main()
