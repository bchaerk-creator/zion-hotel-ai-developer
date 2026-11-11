"""Gera dist/diagnostico-zion-de-oferta.html (autocontido: fontes, logo e lógica embutidos; jsPDF via cdnjs).
Uso: python3 -I producao/zion-collection/06-airbnb-vazio/ferramenta/build.py"""
import base64, pathlib
A = pathlib.Path(__file__).resolve().parent
R = A.parents[3]
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
src = (A/"src/app.html").read_text()
subs = {"{{FONT_CORM}}": b64(R/"docs/assets/fonts/cormorant.woff2"), "{{FONT_CORM_I}}": b64(R/"docs/assets/fonts/cormorant-italic.woff2"),
        "{{FONT_AVENTA}}": b64(R/"docs/assets/fonts/aventa.woff2"), "{{LOGO}}": b64(R/"docs/brand/zion-logo-claro.png"), "{{LOGIC}}": (A/"src/logic.js").read_text()}
for k, v in subs.items(): src = src.replace(k, v)
assert "{{" not in src
head, rest = src.split("</style>", 1)
full = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + "</style>\n</head>\n<body>\n" + rest + "\n</body>\n</html>\n")
(A/"dist").mkdir(exist_ok=True); (A/"dist/diagnostico-zion-de-oferta.html").write_text(full)
print("dist/diagnostico-zion-de-oferta.html", len(full), "bytes")
