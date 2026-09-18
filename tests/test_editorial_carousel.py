"""
Testes do carrossel editorial Zion: prompt, validação de especificação e
renderização do HTML (sem navegador).
"""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
RENDER_PY = ROOT / "scripts" / "editorial_carousel" / "render.py"
SPEC_DIR = ROOT / "scripts" / "editorial_carousel" / "carrosseis"


def _load_render_module():
    spec = importlib.util.spec_from_file_location("zion_editorial_render", RENDER_PY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def render():
    return _load_render_module()


def test_prompt_exported():
    from src.prompts import PROMPT_EDITORIAL_CAROUSEL, CARD_FUNCTIONS, CARD_LAYOUTS

    assert "Diretor Editorial" in PROMPT_EDITORIAL_CAROUSEL
    assert "NÃO COMECE VENDENDO" in PROMPT_EDITORIAL_CAROUSEL
    assert "Playfair Display" in PROMPT_EDITORIAL_CAROUSEL
    assert "Hanken Grotesk" in PROMPT_EDITORIAL_CAROUSEL
    assert len(CARD_FUNCTIONS) == 10
    assert len(CARD_LAYOUTS) == 11


def test_layouts_match_between_prompt_and_renderer(render):
    from src.prompts import CARD_LAYOUTS

    assert set(CARD_LAYOUTS) == render.LAYOUTS


def test_rich_text_italics_and_breaks(render):
    assert render.rich_text("vai *muito além* de\nhospedagem") == "vai <em>muito além</em> de<br>hospedagem"
    assert render.rich_text("<b>x</b>") == "&lt;b&gt;x&lt;/b&gt;"
    assert render.rich_text(None) == ""


def _minimal_cards():
    return [
        {"layout": "cover", "headline": "Capa", "image": {"src": None, "brief": "foto"}},
        {"layout": "typographic", "headline": "Antes.", "subhead": "Agora."},
        {"layout": "photo-quote", "headline": "Frase.", "image": {"brief": "foto"}},
        {"layout": "manifesto", "headline": "Manifesto."},
        {"layout": "emotional", "headline": "Desejo.", "image": {"brief": "foto"}},
        {"layout": "cta", "headline": "Convite."},
    ]


def test_validate_minimal_spec(render):
    render.validate_spec({"slug": "teste", "cards": _minimal_cards()})


@pytest.mark.parametrize(
    "mutation, message",
    [
        (lambda c: c[:5], "entre 6 e 10"),
        (lambda c: c + [{"layout": "cta", "headline": "x"}] * 5, "entre 6 e 10"),
        (lambda c: [{"layout": "manifesto", "headline": "x"}] + c[1:], "card 1"),
        (lambda c: c[:-1] + [{"layout": "manifesto", "headline": "x"}], "último card"),
        (lambda c: c[:1] + [{"layout": "cover", "headline": "x"}] + c[1:], "repetido"),
        (lambda c: c[:1] + [{"layout": "canva", "headline": "x"}] + c[1:], "layout inválido"),
        (lambda c: c[:1] + [{"layout": "portrait", "headline": "x"}] + c[1:], "exige 'meta'"),
        (lambda c: c[:1] + [{"layout": "insight", "headline": "x"}] + c[1:], "exige 'stats'"),
        (lambda c: c[:1] + [{"layout": "positioning", "headline": "x"}] + c[1:], "exige 'items'"),
        (lambda c: c[:1] + [{"layout": "press", "headline": "x", "image": {"brief": "x"}}] + c[1:], "exige fotografia real"),
    ],
)
def test_validate_rejects_bad_specs(render, mutation, message):
    with pytest.raises(render.SpecError, match=message):
        render.validate_spec({"slug": "teste", "cards": mutation(_minimal_cards())})


def test_example_specs_render_to_html(render):
    specs = sorted(SPEC_DIR.glob("*.json"))
    assert specs, "nenhuma especificação de exemplo encontrada"
    for path in specs:
        spec = render.load_spec(path)
        html = render.render_html(spec)
        assert html.count('class="card ') == len(spec["cards"])
        assert "Playfair Display" in html and "Hanken Grotesk" in html
        assert "data:font/woff2;base64," in html
        # sem foto real, o slot é marcado explicitamente para não ser publicado por engano
        assert "Fotografia real a inserir" in html


def test_missing_photo_is_an_error(render, tmp_path):
    cards = _minimal_cards()
    cards[0]["image"] = {"src": "nao-existe.jpg", "brief": "x"}
    path = tmp_path / "spec.json"
    path.write_text(json.dumps({"slug": "t", "cards": cards}), encoding="utf-8")
    with pytest.raises(render.SpecError, match="não encontrada"):
        render.load_spec(path)


def test_real_photo_is_embedded(render, tmp_path):
    photo = tmp_path / "bruno.png"
    photo.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 16)
    cards = _minimal_cards()
    cards[0]["image"] = {"src": "bruno.png", "brief": "retrato"}
    path = tmp_path / "spec.json"
    path.write_text(json.dumps({"slug": "t", "cards": cards}), encoding="utf-8")
    spec = render.load_spec(path)
    assert spec["cards"][0]["image"]["data"].startswith("data:image/png;base64,")
    html = render.render_html(spec)
    assert '<img src="data:image/png;base64,' in html
