"""Gera duas versões da landing:
 dist/clickmax.html  -> para importar no ClickMax (fotos servidas pelo site Zion no GitHub Pages)
 <saida>             -> pré-visualização autocontida (fotos embutidas)
Uso: python3 -I producao/academy01/landing/build.py <saida-previa.html>"""
import base64, io, sys, pathlib
from PIL import Image
A = pathlib.Path(__file__).resolve().parent; R = A.parents[2]
BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
IMGS = {"op01":"assets/operacoes/op01.webp","op04":"assets/operacoes/op04.webp","op05":"assets/operacoes/op05.webp",
        "op06":"assets/operacoes/op06.webp","op08":"assets/operacoes/op08.webp","op10":"assets/operacoes/op10.webp",
        "op12":"assets/operacoes/op12.webp","op14":"assets/operacoes/op14.webp","noturna":"assets/store/noturna.webp",
        "logo":"brand/zion-logo-claro.png"}
src = (A/"src/landing.html").read_text()
def embutir(rel):
    p = R/"docs"/rel
    if p.suffix == ".png": return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
    im = Image.open(p).convert("RGB"); im.thumbnail((1000, 1000)); b = io.BytesIO(); im.save(b, "WEBP", quality=60)
    return "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
web, prev = src, src
for k, rel in IMGS.items():
    assert (R/"docs"/rel).exists(), rel
    web = web.replace("{{IMG:%s}}" % k, BASE + rel); prev = prev.replace("{{IMG:%s}}" % k, embutir(rel))
assert "{{" not in web and "{{" not in prev
# ClickMax recebe só o corpo: sem <title>/<meta> de pré-visualização
corpo = web.split("</style>", 1)
fontes = '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">\n'
estilo = corpo[0][corpo[0].index("<style>"):] + "</style>"
(A/"dist").mkdir(exist_ok=True); (A/"dist/clickmax.html").write_text(fontes + estilo + corpo[1])
if len(sys.argv) > 1: pathlib.Path(sys.argv[1]).write_text(prev)
print("clickmax.html", len(fontes + estilo + corpo[1]), "| prévia", len(prev))
