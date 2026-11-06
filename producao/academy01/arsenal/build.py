"""Gera dist/index.html (página completa, isolada) e, opcionalmente, uma versão-fragmento para pré-visualização.
Uso: python3 -I producao/academy01/arsenal/build.py [saida-fragmento.html]"""
import base64, sys, pathlib
A = pathlib.Path(__file__).resolve().parent
R = A.parents[2]
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
src = (A/"src/app.html").read_text()
subs = {
  "{{FONT_CORM}}": b64(R/"docs/assets/fonts/cormorant.woff2"),
  "{{FONT_CORM_I}}": b64(R/"docs/assets/fonts/cormorant-italic.woff2"),
  "{{FONT_AVENTA}}": b64(R/"docs/assets/fonts/aventa.woff2"),
  "{{LOGO}}": b64(R/"docs/brand/zion-logo-claro.png"),
  "{{IMG_CAPA}}": b64(A/"src/img/capa.webp"),
  "{{IMG_AEREA}}": b64(A/"src/img/aerea.webp"),
  "{{LOGIC}}": (A/"src/logic.js").read_text(),
}
for k, v in subs.items(): src = src.replace(k, v)
assert "{{" not in src, "placeholder sem substituir"
head, rest = src.split("</style>", 1)
full = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + "</style>\n</head>\n<body>\n" + rest + "\n</body>\n</html>\n")
(A/"dist").mkdir(exist_ok=True); (A/"dist/index.html").write_text(full)
if len(sys.argv) > 1: pathlib.Path(sys.argv[1]).write_text(src)
print("dist/index.html", len(full), "bytes")
