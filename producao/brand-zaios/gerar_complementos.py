"""ZAIOS SYSTEM v1.1 · complementos: paleta (contraste WCAG e CMYK aproximado), tokens, favicon.ico e páginas HTML
das aplicações e do manual. Uso: python3 producao/brand-zaios/gerar_complementos.py <pasta do kit>"""
import sys, json, pathlib, base64
from PIL import Image
K = pathlib.Path(sys.argv[1]); M = json.loads((K / "manifesto.json").read_text())
P = M["paleta"]; RAIZ = pathlib.Path(__file__).resolve().parents[2]
NOMES = {"preto": "Preto profundo", "dourado": "Dourado premium", "marfim": "Marfim", "verde": "Verde Zion", "grafite": "Grafite"}
def rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def lum(h):
    def c(v): v /= 255; return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb(h); return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)
def contraste(a, b): la, lb = sorted([lum(a), lum(b)], reverse=True); return (la + 0.05) / (lb + 0.05)
def cmyk(h):
    r, g, b = [v / 255 for v in rgb(h)]; k = 1 - max(r, g, b)
    if k >= 1: return (0, 0, 0, 100)
    return tuple(round(100 * v) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k))
pares = [("dourado", "preto"), ("marfim", "preto"), ("preto", "marfim"), ("dourado", "verde"), ("marfim", "verde"), ("dourado", "grafite"), ("marfim", "grafite"), ("dourado", "marfim"), ("verde", "marfim")]
cont = [{"texto": a, "fundo": b, "razao": round(contraste(P[a], P[b]), 2), "AA_texto_normal": contraste(P[a], P[b]) >= 4.5, "AA_texto_grande": contraste(P[a], P[b]) >= 3} for a, b in pares]
paleta = [{"nome": NOMES[k], "token": f"--zaios-{k}", "hex": v, "rgb": rgb(v), "cmyk_aproximado": cmyk(v)} for k, v in P.items()]
(K / "paleta.json").write_text(json.dumps({"cores": paleta, "contrastes": cont, "nota": "CMYK calculado por conversão direta de RGB; validar com prova de cor na gráfica."}, ensure_ascii=False, indent=1))
(K / "tokens.css").write_text(":root {\n" + "".join(f"  --zaios-{k}: {v};\n" for k, v in P.items()) +
    '  --zaios-font: "Aventa", system-ui, sans-serif;\n  --zaios-font-weight-titulo: 700;\n  --zaios-font-weight-apoio: 500;\n  --zaios-respiro: 0.25; /* área livre = 1/4 da altura do símbolo */\n}\n')
(K / "tokens.json").write_text(json.dumps({"cor": P, "fonte": {"familia": "Aventa", "titulo": 700, "apoio": 500, "texto": 400}}, ensure_ascii=False, indent=1))
fav = [Image.open(K / "png" / f"zaios-favicon-{s}.png") for s in (16, 32, 48)]
fav[2].save(K / "zaios-favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=fav[:2])
for c in cont: print(c["texto"], "sobre", c["fundo"], c["razao"], "AA" if c["AA_texto_normal"] else ("AA grande" if c["AA_texto_grande"] else "só decorativo"))
