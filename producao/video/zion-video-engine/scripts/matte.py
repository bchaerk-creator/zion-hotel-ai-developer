#!/usr/bin/env python3
"""Recorta o apresentador do fundo com Robust Video Matting e rastreia a cabeça.

Entrada: lessons/<id>/source.mp4 (ou source.jpg/png para teste com foto).
Saída:   lessons/<id>/fg/NNNNN.webp (RGBA) e anchors.json [{f, top, cx}] em pixels do quadro.
Estado recorrente zerado a cada corte (lista --cortes em segundos).
"""
import json
import subprocess
import numpy as np
import onnxruntime as ort
from PIL import Image
from comum import MODELOS, args_aula


def extra(ap):
    ap.add_argument('--cortes', default='', help='tempos de corte em segundos, separados por vírgula')
    ap.add_argument('--fps', type=float, default=30)
    ap.add_argument('--mesa', type=float, default=0, help='fração da altura abaixo da qual fica opaco (mesa na frente)')


def quadros(pasta, fps):
    for nome in ('source.jpg', 'source.png'):
        if (pasta / nome).exists():
            yield np.asarray(Image.open(pasta / nome).convert('RGB'))
            return
    src = pasta / 'source.mp4'
    info = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                           '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip().split(',')
    w, h = map(int, info)
    proc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src, '-vf', f'fps={fps}', '-f', 'rawvideo',
                             '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        buf = proc.stdout.read(w * h * 3)
        if len(buf) < w * h * 3:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)


def main():
    a = args_aula('Recorte do apresentador (RVM) e anchors da cabeça', extra)
    sess = ort.InferenceSession(str(MODELOS / 'rvm_mobilenetv3_fp32.onnx'), providers=['CPUExecutionProvider'])
    cortes = {round(float(c) * a.fps) for c in a.cortes.split(',') if c}
    fg = a.pasta / 'fg'
    fg.mkdir(exist_ok=True)
    anchors, rec = [], None
    for i, rgb in enumerate(quadros(a.pasta, a.fps)):
        if rec is None or i in cortes:
            rec = [np.zeros((1, 1, 1, 1), np.float32)] * 4
        src = (rgb.astype(np.float32) / 255).transpose(2, 0, 1)[None]
        fgr, pha, *rec = sess.run(None, {'src': src, 'r1i': rec[0], 'r2i': rec[1], 'r3i': rec[2], 'r4i': rec[3],
                                         'downsample_ratio': np.array([0.375], np.float32)})
        alfa = pha[0, 0]
        if a.mesa:
            alfa[int(alfa.shape[0] * a.mesa):] = 1.0
        rgba = np.dstack([rgb, (alfa * 255).astype(np.uint8)])
        Image.fromarray(rgba, 'RGBA').save(fg / f'{i:05d}.webp', quality=88)
        linhas = np.where((alfa > 0.5).sum(1) > 8)[0]
        top = int(linhas[0]) if len(linhas) else 0
        faixa = alfa[top:top + max(40, alfa.shape[0] // 8)]
        cols = np.where(faixa.sum(0) > 2)[0]
        cx = int(cols.mean()) if len(cols) else alfa.shape[1] // 2
        anchors.append({'f': i, 'top': top, 'cx': cx, 'w': int(alfa.shape[1]), 'h': int(alfa.shape[0])})
        if i % 100 == 0:
            print(f'quadro {i}')
    (a.pasta / 'anchors.json').write_text(json.dumps(anchors))
    print(f'{len(anchors)} quadros recortados em {fg}')


if __name__ == '__main__':
    main()
