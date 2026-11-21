"""Gera dist/index.html (portal do aluno, arquivo único). Uso: python3 -I producao/produto-01-terra-capital/build.py"""
import base64, json, pathlib
A = pathlib.Path(__file__).resolve().parent; R = A.parents[1]
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
src = (A/"src/app.html").read_text()
subs = {"{{FONT_CORM}}": b64(R/"docs/assets/fonts/cormorant.woff2"), "{{FONT_CORM_I}}": b64(R/"docs/assets/fonts/cormorant-italic.woff2"),
        "{{FONT_AVENTA}}": b64(R/"docs/assets/fonts/aventa.woff2"), "{{LOGO}}": b64(R/"docs/brand/zion-logo-claro.png"),
        "{{LOGIC}}": (A/"src/logic.js").read_text(), "{{AULAS}}": json.dumps(json.load(open(A/"src/aulas.json")), ensure_ascii=False)}
for k in sorted(subs, key=len, reverse=True): src = src.replace(k, subs[k])
assert "{{" not in src
head, rest = src.split("</style>", 1)
full = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="robots" content="noindex">\n<title>Você tem terra. Falta capital? · Zion Hotel Academy</title>\n'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>\n'
        + head + "</style>\n</head>\n<body>\n" + rest + "\n</body>\n</html>\n")
(A/"dist").mkdir(exist_ok=True); (A/"dist/index.html").write_text(full); print("dist/index.html", len(full))
