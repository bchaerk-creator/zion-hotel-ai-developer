# -*- coding: utf-8 -*-
"""Renders para web (1400 px) e para o deck (sem a interface do visualizador), com a marca Zion (símbolo oficial) no canto inferior direito.
Parte sempre dos PNG originais em <produto>/renders/*.png, por isso pode ser rodado quantas vezes for preciso sem acumular marcas.
Uso: python3 brand_renders.py [cocoon zenith lodge capsule ...]"""
import glob, io, os, sys
import pymupdf
from PIL import Image
from svgkit import zion_symbol_svg

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def mark_image(size, color):
    """símbolo Z rasterizado com fundo transparente (PIL RGBA)."""
    svg = zion_symbol_svg(size, color)
    doc = pymupdf.open(stream=svg.encode(), filetype="svg")
    pix = doc[0].get_pixmap(alpha=True, matrix=pymupdf.Matrix(1, 1))
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")

def stamp(im, frac=0.052, margin=0.028):
    """aplica a marca (creme com sombra suave) no canto inferior direito."""
    w, h = im.size; size = max(28, round(w * frac)); m = round(w * margin)
    shadow = mark_image(size, "#040605"); mark = mark_image(size, "#FEF5F0")
    a = shadow.split()[3].point(lambda v: int(v * 0.45)); shadow.putalpha(a)
    out = im.convert("RGBA")
    x, y = w - size - m, h - size - m
    out.alpha_composite(shadow, (x + 2, y + 2)); out.alpha_composite(mark, (x, y))
    return out.convert("RGB")

def build(products):
    for p in products:
        src = sorted(glob.glob(os.path.join(ROOT, p, "renders", "*.png")))
        if not src: continue
        os.makedirs(os.path.join(ROOT, p, "renders", "web", "deck"), exist_ok=True)
        for f in src:
            im = Image.open(f).convert("RGB"); w, h = im.size
            im = im.resize((1400, round(h * 1400 / w)), Image.LANCZOS)
            base = os.path.basename(f).replace(".png", ".jpg")
            stamp(im).save(os.path.join(ROOT, p, "renders", "web", base), quality=82, optimize=True)
            deck = im.crop((0, 92, 1400, im.size[1] - 48))
            stamp(deck).save(os.path.join(ROOT, p, "renders", "web", "deck", base), quality=86)
        print(p, len(src), "renders com marca")

if __name__ == "__main__":
    build(sys.argv[1:] or ["cocoon", "zenith", "lodge", "capsule", "cocoon_s"])
