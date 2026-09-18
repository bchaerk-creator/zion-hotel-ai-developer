#!/usr/bin/env python3
"""
Renderizador do carrossel editorial Zion.

Lê uma especificação JSON (gerada pelo Diretor Editorial — ver
`src/prompts/editorial_carousel.py`), monta um HTML autocontido com os cards
em 1080x1350 (4:5, formato nativo de carrossel do Instagram) e captura cada
card como JPG via Playwright/Chromium.

Uso:
    python scripts/editorial_carousel/render.py carrosseis/001-exemplo.json
    python scripts/editorial_carousel/render.py spec.json --out output/carrossel --quality 92
    python scripts/editorial_carousel/render.py spec.json --no-capture   # só o HTML

Fotografias: `image.src` aceita caminho relativo ao JSON ou absoluto. Sem
`src`, o card renderiza um slot editorial marcado "fotografia real a inserir"
com o briefing da foto — nunca uma imagem de banco.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import os
import re
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FONTS_DIR = ROOT / "docs" / "assets" / "fonts"

CARD_W, CARD_H = 1080, 1350
MIN_CARDS, MAX_CARDS = 6, 10

LAYOUTS = {
    "cover",
    "typographic",
    "photo-quote",
    "portrait",
    "insight",
    "destination",
    "press",
    "manifesto",
    "emotional",
    "positioning",
    "cta",
}

FONT_FILES = [
    "playfair-regular",
    "playfair-medium",
    "playfair-italic",
    "hanken-light",
    "hanken-regular",
    "hanken-medium",
    "hanken-light-italic",
]

DEFAULT_BRAND = {
    "name": "ZION GLAMPING COLLECTION",
    "tagline": "SOUL LUXURY RETREATS",
    "handle": "@brunochaerkofc",
}


class SpecError(ValueError):
    """Especificação de carrossel inválida."""


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    if path.suffix == ".woff2":
        mime = "font/woff2"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def rich_text(text: str | None) -> str:
    """Escapa HTML e converte *itálico* em <em>, quebras de linha em <br>."""
    if not text:
        return ""
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped, flags=re.S)
    return escaped.replace("\n", "<br>")


def topographic_svg(seed: int = 7) -> str:
    """Curvas de nível em areia sobre fundo escuro: o slot editorial padrão."""
    import math

    paths = []
    rng = seed * 9973
    for i in range(14):
        rng = (rng * 1103515245 + 12345) % (2**31)
        phase = (rng % 1000) / 1000 * math.tau
        amp = 40 + (i * 11) % 70
        y0 = -80 + i * 115
        pts = []
        for x in range(-40, CARD_W + 41, 40):
            y = y0 + amp * math.sin(x / 260 + phase) + (amp / 2) * math.sin(x / 90 + phase * 1.7)
            pts.append(f"{x},{y:.1f}")
        paths.append(
            f'<path d="M{" L".join(pts)}" fill="none" stroke="#DED6BF" '
            f'stroke-width="1" stroke-opacity="{0.22 + (i % 3) * 0.08:.2f}"/>'
        )
    return (
        f'<svg class="topo" viewBox="0 0 {CARD_W} {CARD_H}" preserveAspectRatio="xMidYMid slice" '
        f'xmlns="http://www.w3.org/2000/svg">{"".join(paths)}</svg>'
    )


# --------------------------------------------------------------------------- #
# Spec
# --------------------------------------------------------------------------- #
def load_spec(spec_path: Path) -> dict:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    validate_spec(spec)

    brand = dict(DEFAULT_BRAND)
    brand.update(spec.get("brand") or {})
    spec["brand"] = brand
    spec.setdefault("edition", "Edição 01")
    spec.setdefault("date_label", "")
    spec.setdefault("theme", spec["slug"])
    brand.setdefault("logo_data", None)
    if brand.get("logo"):
        logo = Path(brand["logo"])
        if not logo.is_absolute():
            logo = (spec_path.parent / logo).resolve()
        if not logo.exists():
            raise SpecError(f"Logo não encontrado: {brand['logo']}")
        brand["logo_data"] = data_uri(logo)

    for card in spec["cards"]:
        for key in ("kicker", "headline", "subhead", "body", "footnote", "pause", "function"):
            card.setdefault(key, "")
        card.setdefault("meta", None)
        card.setdefault("stats", None)
        card.setdefault("items", None)
        card.setdefault("image", None)
        if card["meta"] is not None:
            for key in ("name", "role"):
                card["meta"].setdefault(key, "")
            card["meta"].setdefault("facts", [])
            card["meta"]["name_html"] = rich_text(card["meta"]["name"])
        if card["image"] is not None:
            for key in ("src", "brief", "credit", "data", "position", "scale"):
                card["image"].setdefault(key, None)
        card["headline_html"] = rich_text(card.get("headline"))
        card["subhead_html"] = rich_text(card.get("subhead"))
        card["body_html"] = rich_text(card.get("body"))
        image = card.get("image")
        if image and image.get("src"):
            src = Path(image["src"])
            if not src.is_absolute():
                src = (spec_path.parent / src).resolve()
            if not src.exists():
                raise SpecError(f"Fotografia não encontrada: {image['src']}")
            image["data"] = data_uri(src)
    return spec


def validate_spec(spec: dict) -> None:
    if not isinstance(spec, dict):
        raise SpecError("A especificação deve ser um objeto JSON.")
    if not spec.get("slug"):
        raise SpecError("Campo obrigatório ausente: slug")
    cards = spec.get("cards")
    if not isinstance(cards, list) or not (MIN_CARDS <= len(cards) <= MAX_CARDS):
        raise SpecError(f"O carrossel precisa ter entre {MIN_CARDS} e {MAX_CARDS} cards.")

    previous = None
    for i, card in enumerate(cards, start=1):
        layout = card.get("layout")
        if layout not in LAYOUTS:
            raise SpecError(f"Card {i}: layout inválido '{layout}'. Válidos: {sorted(LAYOUTS)}")
        if layout == previous:
            raise SpecError(f"Card {i}: layout '{layout}' repetido em sequência.")
        previous = layout
        if not card.get("headline") and not (card.get("meta") or {}).get("name"):
            raise SpecError(f"Card {i}: headline obrigatória.")
        if layout == "portrait" and not card.get("meta"):
            raise SpecError(f"Card {i}: layout 'portrait' exige 'meta' (name, role, facts).")
        if layout == "insight" and not card.get("stats") and not card.get("body"):
            raise SpecError(f"Card {i}: layout 'insight' exige 'stats' ou 'body'.")
        if layout == "press" and not (card.get("image") or {}).get("src"):
            raise SpecError(f"Card {i}: layout 'press' exige fotografia real em image.src.")
        if layout == "positioning" and not card.get("items"):
            raise SpecError(f"Card {i}: layout 'positioning' exige 'items'.")

    if cards[0]["layout"] != "cover":
        raise SpecError("O card 1 deve usar o layout 'cover'.")
    if cards[-1]["layout"] != "cta":
        raise SpecError("O último card deve usar o layout 'cta'.")


# --------------------------------------------------------------------------- #
# Render
# --------------------------------------------------------------------------- #
def render_html(spec: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(HERE)),
        autoescape=True,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    fonts = {}
    for name in FONT_FILES:
        path = FONTS_DIR / f"{name}.woff2"
        if not path.exists():
            raise FileNotFoundError(f"Fonte ausente: {path}")
        fonts[name] = data_uri(path)
    template = env.get_template("template.html.j2")
    return template.render(spec=spec, fonts=fonts, topo=topographic_svg())


def capture(html_path: Path, out_dir: Path, quality: int, scale: int) -> list[Path]:
    from playwright.sync_api import sync_playwright

    outputs: list[Path] = []
    launch_kwargs: dict = {}
    executable = os.environ.get("ZION_CHROMIUM_PATH") or os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
    if not executable and Path("/opt/pw-browsers/chromium").exists():
        executable = "/opt/pw-browsers/chromium"
    if executable:
        launch_kwargs["executable_path"] = executable
    with sync_playwright() as p:
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page(
            viewport={"width": CARD_W + 96, "height": CARD_H + 96},
            device_scale_factor=scale,
        )
        page.goto(html_path.resolve().as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(600)
        cards = page.query_selector_all(".card")
        for card in cards:
            index = card.get_attribute("data-card")
            target = out_dir / f"card_{index}.jpg"
            card.screenshot(path=str(target), type="jpeg", quality=quality)
            outputs.append(target)
        browser.close()
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Renderiza um carrossel editorial Zion.")
    parser.add_argument("spec", type=Path, help="arquivo JSON da especificação")
    parser.add_argument("--out", type=Path, default=None, help="pasta de saída (padrão: output/editorial/<slug>)")
    parser.add_argument("--quality", type=int, default=90, help="qualidade JPEG (padrão 90)")
    parser.add_argument("--scale", type=int, default=1, help="fator de escala (1 = 1080x1350, 2 = 2160x2700)")
    parser.add_argument("--no-capture", action="store_true", help="gera apenas o HTML de preview")
    args = parser.parse_args(argv)

    try:
        spec = load_spec(args.spec)
    except (SpecError, json.JSONDecodeError, FileNotFoundError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2

    out_dir = args.out or (ROOT / "output" / "editorial" / spec["slug"])
    out_dir.mkdir(parents=True, exist_ok=True)

    html_path = out_dir / "preview.html"
    html_path.write_text(render_html(spec), encoding="utf-8")
    print(f"html  → {html_path}")

    if args.no_capture:
        return 0

    for path in capture(html_path, out_dir, args.quality, args.scale):
        print(f"card  → {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
