#!/usr/bin/env python3
"""
Tratamento editorial de fotografias para o carrossel Zion.

Aplica uma gradação consistente (look cinematográfico, sóbrio, quente nas
sombras) a qualquer foto real fornecida, com recorte e redimensionamento
opcionais. Nunca gera imagem: só trata o que foi entregue.

Uso:
    python scripts/editorial_carousel/grade.py foto.jpg saida.jpg
    python scripts/editorial_carousel/grade.py foto.jpg saida.jpg --height 1350
    python scripts/editorial_carousel/grade.py foto.jpg saida.jpg --crop 0,450,890,2576
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# Parâmetros do look editorial Zion (discretos: a foto continua sendo a foto).
SATURATION = 0.86
CONTRAST = 1.08
WARM_R, WARM_B = 1.025, 0.965
BLACK_LIFT = -6          # aprofunda o preto rumo ao #040605
VIGNETTE = 0.20          # escurecimento máximo nas bordas
SHARPEN_WHEN_UPSCALED = 1.15


def grade(
    src: Path,
    dst: Path,
    crop: tuple[int, int, int, int] | None = None,
    height: int | None = None,
    quality: int = 90,
) -> Image.Image:
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if crop:
        im = im.crop(crop)

    upscaled = False
    if height and im.height != height:
        upscaled = height > im.height
        im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)

    im = ImageEnhance.Color(im).enhance(SATURATION)
    im = ImageEnhance.Contrast(im).enhance(CONTRAST)

    r, g, b = im.split()
    r = r.point(lambda v: min(255, max(0, round(v * WARM_R + BLACK_LIFT))))
    g = g.point(lambda v: min(255, max(0, round(v + BLACK_LIFT))))
    b = b.point(lambda v: min(255, max(0, round(v * WARM_B + BLACK_LIFT))))
    im = Image.merge("RGB", (r, g, b))

    im = _vignette(im, VIGNETTE)

    if upscaled:
        im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=round(SHARPEN_WHEN_UPSCALED * 60), threshold=2))

    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, quality=quality, optimize=True)
    return im


def _vignette(im: Image.Image, strength: float) -> Image.Image:
    """Vinheta radial suave, gerada em baixa resolução e ampliada."""
    w, h = im.size
    small = 128
    mask = Image.new("L", (small, small))
    px = mask.load()
    cx, cy = (small - 1) / 2, (small - 1) / 2
    for y in range(small):
        for x in range(small):
            d = (((x - cx) / cx) ** 2 + ((y - cy) / cy) ** 2) ** 0.5
            t = max(0.0, min(1.0, (d - 0.55) / 0.85))
            px[x, y] = round(255 * (1 - strength * t * t))
    mask = mask.resize((w, h), Image.BICUBIC)
    black = Image.new("RGB", (w, h), (4, 6, 5))
    return Image.composite(im, black, mask)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tratamento editorial de fotografia.")
    parser.add_argument("src", type=Path)
    parser.add_argument("dst", type=Path)
    parser.add_argument("--crop", type=str, default=None, help="left,top,right,bottom em pixels da original")
    parser.add_argument("--height", type=int, default=None, help="altura final em pixels")
    parser.add_argument("--quality", type=int, default=90)
    args = parser.parse_args(argv)
    crop = tuple(int(v) for v in args.crop.split(",")) if args.crop else None
    im = grade(args.src, args.dst, crop, args.height, args.quality)
    print(f"{args.dst} {im.size[0]}x{im.size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
