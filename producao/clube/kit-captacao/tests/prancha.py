"""Prancha de conferência: capas, páginas do PDF e quadros extraídos dos vídeos com ffmpeg.
Uso: python3 -I tests/prancha.py <dist> <build> <saida.jpg>"""
import sys, pathlib, subprocess, tempfile
from PIL import Image, ImageDraw
dist, build, out = map(pathlib.Path, sys.argv[1:4]); tmp = pathlib.Path(tempfile.mkdtemp())
def quadros(mp4, ts, pref):
    fs = []
    for t in ts:
        f = tmp / f"{pref}_{t:05.1f}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(mp4), "-frames:v", "1", "-q:v", "3", str(f)], check=True); fs.append((f, f"{pref} {int(t//60)}:{int(t%60):02d}"))
    return fs
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)
dt, dv = dur(dist / "kit-captacao.mp4"), dur(dist / "kit-captacao-teaser.mp4")
tut = quadros(dist / "kit-captacao.mp4", [5, dt * .2, dt * .4, dt * .6, dt * .78, dt - 6], "tutorial")
tea = quadros(dist / "kit-captacao-teaser.mp4", [2, dv * .3, dv * .55, dv * .75, dv - 3], "teaser")
W = 2400; S = Image.new("RGB", (W, 2700), "#FEF5F0"); d = ImageDraw.Draw(S)
def cola(f, x, y, w, h, leg):
    im = Image.open(f).convert("RGB"); im.thumbnail((w, h)); S.paste(im, (x, y)); d.text((x, y + im.size[1] + 6), leg, fill="#1B2117"); return im.size
d.text((30, 20), "KIT INICIAL DE CAPTACAO · prancha de conferencia (capas, PDF, quadros dos videos)", fill="#8B714E")
cola(dist / "kit-captacao-h.jpg", 30, 60, 1280, 720, "kit-captacao-h.jpg 1280x720")
cola(dist / "kit-captacao-v.jpg", 1340, 60, 480, 720, "kit-captacao-v.jpg 720x1080")
pags = sorted((build / "png").glob("pag*.png"))
for k, i in enumerate([0, 4, 5, 10, 12, 15]):
    cola(pags[i], 30 + k * 395, 830, 380, 540, f"PDF pag. {i+1}")
for k, (f, leg) in enumerate(tut):
    cola(f, 30 + (k % 3) * 610, 1420 + (k // 3) * 380, 590, 332, leg)
for k, (f, leg) in enumerate(tea):
    cola(f, 1880 + (k % 2) * 260, 1420 + (k // 2) * 450 if k < 4 else 1420, 240, 427, leg) if k < 4 else None
f, leg = tea[4]; cola(f, 1880, 2330 - 0, 120, 213, leg)
S.save(out, quality=85); print("prancha", out, f"tutorial {dt:.1f}s, teaser {dv:.1f}s")
