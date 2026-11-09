"""ZAIOS SYSTEM · Brand Kit v1.1 · gerador dos logotipos em SVG (texto convertido em curvas).
Símbolo: Z original de três barras da Zion Hotel Group International, vetorizado a partir de docs/brand/zion-logo-escuro.png
(Z de 240 px no original; vértices nas bordas dos pixels, precisão de ±0,5 px, ou 0,2% da altura).
Tipografia: Aventa Variable original (docs/assets/fonts/aventa.woff2), instanciada em Bold (700) e Medium (500).
Uso: python3 producao/brand-zaios/gerar_kit.py <pasta de saída>"""
import sys, json, pathlib, io
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

RAIZ = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "kit"); OUT.mkdir(parents=True, exist_ok=True)
FONTE = RAIZ / "docs/assets/fonts/aventa.woff2"

PALETA = {"preto": "#090909", "dourado": "#D4AF67", "marfim": "#E8DFCD", "verde": "#173B32", "grafite": "#242424"}
DESCRICAO = "A plataforma de inteligência para desenvolvimento, gestão e operação hoteleira."
DESCRICAO_2L = ["A plataforma de inteligência para", "desenvolvimento, gestão e operação hoteleira."]

# Z oficial em grade de 240 × 240 (origem no canto superior esquerdo). Duas peças: barras superior e central (unidas por um ponto) e barra inferior.
S = 240
Z_PECAS = [
    [(0, 0), (240, 0), (240, 30), (224, 30), (180, 60), (0, 60)],                      # barra superior com o corte diagonal
    [(180, 60), (240, 60), (240, 150), (119, 150), (74, 180), (0, 180)],                # barra central e diagonal
    [(240, 165), (240, 240), (0, 240), (0, 210), (180, 210)],                           # barra inferior com o corte diagonal
]
def z_path(x, y, s):
    k = s / S
    return " ".join("M" + " L".join(f"{x + px * k:.3f},{y + py * k:.3f}" for px, py in p) + " Z" for p in Z_PECAS)

_fontes = {}
def fonte(peso):
    if peso not in _fontes:
        f = TTFont(str(FONTE)); _fontes[peso] = instancer.instantiateVariableFont(f, {"wght": peso})
    return _fontes[peso]

def texto(t, peso, cap, track=0.0):
    """Converte o texto em caminho SVG. cap = altura das maiúsculas em px. track = espaçamento extra em fração do em.
    Devolve (path d relativo à linha de base em y=0, largura). Sem kerning (o espaçamento é o das larguras da fonte)."""
    f = fonte(peso); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f["head"].unitsPerEm
    caph = getattr(f["OS/2"], "sCapHeight", 0) or 0.7 * upm
    esc = cap / caph; x = 0.0; partes = []
    for i, ch in enumerate(t):
        g = cmap.get(ord(ch)); 
        if g is None: raise ValueError(f"Glifo ausente: {ch!r}")
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (esc, 0, 0, -esc, x, 0)))
        d = pen.getCommands()
        if d: partes.append(d)
        x += gs[g].width * esc + (track * upm * esc if i < len(t) - 1 else 0)
    return " ".join(partes), x

def svg(w, h, corpo, fundo=None):
    bg = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{fundo}"/>' if fundo else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">{bg}{corpo}</svg>\n'

X = S / 4  # área de respiro = 1/4 da altura do símbolo (a altura da barra superior)

def horizontal(cor_z, cor_txt, cor_linha, descricao, cor_desc=None):
    gap = 0.20 * S
    zaios, wz = texto("ZAIOS", 700, 0.42 * S, 0.02)
    system, ws = texto("SYSTEM", 500, 0.115 * S, 0.40)
    xl = X + S + gap; xt = xl + gap
    # bloco ZAIOS + SYSTEM centralizado na altura do símbolo
    bloco = 0.42 * S + 0.14 * S + 0.115 * S; y0 = X + (S - bloco) / 2
    yb1 = y0 + 0.42 * S; yb2 = yb1 + 0.14 * S + 0.115 * S
    w = xt + max(wz, ws) + X; corpo = []
    corpo.append(f'<path fill="{cor_z}" d="{z_path(X, X, S)}"/>')
    corpo.append(f'<rect x="{xl - 1.5:.3f}" y="{X:.3f}" width="3" height="{S:.3f}" fill="{cor_linha}"/>')  # linha limitada à altura do símbolo
    corpo.append(f'<path fill="{cor_txt}" transform="translate({xt:.3f},{yb1:.3f})" d="{zaios}"/>')
    corpo.append(f'<path fill="{cor_txt}" transform="translate({xt + 3:.3f},{yb2:.3f})" d="{system}"/>')
    h = X + S + X
    if descricao:
        desc, wd = texto(DESCRICAO, 500, 0.075 * S, 0.0)
        yd = X + S + 0.55 * X + 0.075 * S   # faixa própria, abaixo do símbolo e da linha, sem cruzar nenhum elemento
        corpo.append(f'<path fill="{cor_desc or cor_txt}" transform="translate({X:.3f},{yd:.3f})" d="{desc}"/>')
        w = max(w, X + wd + X); h = yd + X
    return w, h, "".join(corpo)

def vertical(cor_z, cor_txt, cor_linha, descricao, cor_desc=None):
    zaios, wz = texto("ZAIOS", 700, 0.36 * S, 0.02)
    system, ws = texto("SYSTEM", 500, 0.10 * S, 0.40)
    linhas = [texto(l, 500, 0.07 * S, 0.0) for l in DESCRICAO_2L] if descricao else []
    larg = max([S, wz, ws] + [l[1] for l in linhas]); w = larg + 2 * X; cx = w / 2
    corpo = [f'<path fill="{cor_z}" d="{z_path(cx - S / 2, X, S)}"/>']
    yl = X + S + 0.16 * S
    corpo.append(f'<rect x="{cx - 0.25 * S:.3f}" y="{yl - 1.5:.3f}" width="{0.5 * S:.3f}" height="3" fill="{cor_linha}"/>')  # linha horizontal curta
    yb1 = yl + 0.16 * S + 0.36 * S; yb2 = yb1 + 0.12 * S + 0.10 * S
    corpo.append(f'<path fill="{cor_txt}" transform="translate({cx - wz / 2:.3f},{yb1:.3f})" d="{zaios}"/>')
    corpo.append(f'<path fill="{cor_txt}" transform="translate({cx - ws / 2 + 3:.3f},{yb2:.3f})" d="{system}"/>')
    h = yb2 + X
    if linhas:
        y = yb2 + 0.55 * X + 0.07 * S
        for d, wl in linhas:
            corpo.append(f'<path fill="{cor_desc or cor_txt}" transform="translate({cx - wl / 2:.3f},{y:.3f})" d="{d}"/>'); y += 0.07 * S * 1.9
        h = y - 0.07 * S * 1.9 + X
    return w, h, "".join(corpo)

def simbolo(cor, fundo=None, pad=X):
    w = S + 2 * pad; return w, w, f'<path fill="{cor}" d="{z_path(pad, pad, S)}"/>'

P = PALETA
VERSOES = {
    # nome: (função, cor do Z, cor do texto, cor da linha, descrição?, fundo, cor da descrição)
    "principal": [("fundo-preto", P["dourado"], P["dourado"], P["dourado"], P["preto"], P["marfim"]),
                  ("fundo-verde", P["dourado"], P["marfim"], P["dourado"], P["verde"], P["marfim"]),
                  ("fundo-marfim", P["preto"], P["preto"], P["dourado"], P["marfim"], P["grafite"]),
                  ("transparente-dourado", P["dourado"], P["dourado"], P["dourado"], None, P["marfim"]),
                  ("transparente-preto", P["preto"], P["preto"], P["preto"], None, P["grafite"]),
                  ("mono-branco", "#FFFFFF", "#FFFFFF", "#FFFFFF", None, "#FFFFFF"),
                  ("mono-preto", P["preto"], P["preto"], P["preto"], None, P["preto"])],
}
manifesto = []
def grava(nome, w, h, corpo, fundo):
    (OUT / "svg").mkdir(exist_ok=True)
    (OUT / "svg" / f"{nome}.svg").write_text(svg(w, h, corpo, fundo)); manifesto.append({"arquivo": f"svg/{nome}.svg", "largura": round(w), "altura": round(h), "fundo": fundo or "transparente"})

for tipo, func in [("horizontal", horizontal), ("vertical", vertical)]:
    for com_desc, suf in [(True, "com-descricao"), (False, "reduzida")]:
        for var, cz, ct, cl, fundo, cd in VERSOES["principal"]:
            w, h, corpo = func(cz, ct, cl, com_desc, cd)
            grava(f"zaios-system-{tipo}-{suf}-{var}", w, h, corpo, fundo)
for var, cor, fundo in [("dourado-fundo-preto", P["dourado"], P["preto"]), ("dourado-fundo-verde", P["dourado"], P["verde"]), ("preto-fundo-marfim", P["preto"], P["marfim"]),
                        ("transparente-dourado", P["dourado"], None), ("transparente-preto", P["preto"], None), ("mono-branco", "#FFFFFF", None)]:
    w, h, corpo = simbolo(cor); grava(f"zaios-simbolo-{var}", w, h, corpo, fundo)
# ícones de aplicativo (quadrado; o Z ocupa 50% do lado, margem segura para máscaras arredondadas)
for var, cor, fundo in [("preto-dourado", P["dourado"], P["preto"]), ("verde-dourado", P["dourado"], P["verde"]), ("marfim-preto", P["preto"], P["marfim"])]:
    lado = 1024; s = 512; o = (lado - s) / 2
    grava(f"zaios-icone-app-{var}", lado, lado, f'<path fill="{cor}" d="{z_path(o, o, s)}"/>', fundo)
# favicon (Z grande, margem mínima, para leitura em 16 px)
lado = 512; s = 432; o = (lado - s) / 2
grava("zaios-favicon", lado, lado, f'<rect width="512" height="512" rx="72" fill="{P["preto"]}"/><path fill="{P["dourado"]}" d="{z_path(o, o, s)}"/>', None)
(OUT / "manifesto.json").write_text(json.dumps({"paleta": PALETA, "descricao": DESCRICAO, "arquivos": manifesto}, ensure_ascii=False, indent=1))
print(len(manifesto), "SVG gerados")
