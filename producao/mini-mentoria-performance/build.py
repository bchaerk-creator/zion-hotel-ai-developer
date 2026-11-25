"""Gera dist/index.html (portal do aluno, arquivo único). Uso: python3 -I producao/mini-mentoria-performance/build.py"""
import base64, json, pathlib
A = pathlib.Path(__file__).resolve().parent; R = A.parents[1]
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
js = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
guia = {m: json.load(open(A/f"ebook/conteudo/mod{m}.json", encoding="utf8")) for m in range(1, 8)}
videos = json.load(open(A/"src/videos.json")) if (A/"src/videos.json").exists() else {}
src = (A/"src/app.html").read_text()
subs = {"{{FONT_CORM}}": b64(R/"docs/assets/fonts/cormorant.woff2"), "{{FONT_CORM_I}}": b64(R/"docs/assets/fonts/cormorant-italic.woff2"),
        "{{FONT_AVENTA}}": b64(R/"docs/assets/fonts/aventa.woff2"), "{{LOGO}}": b64(R/"docs/brand/zion-logo-claro.png"),
        "{{LOGIC}}": (A/"src/logic.js").read_text().replace("</", "<\\/"), "{{QUESTOES}}": js(json.load(open(A/"fontes/formularios.json", encoding="utf8"))),
        "{{META}}": js(json.load(open(A/"src/meta.json"))), "{{GUIA}}": js(guia), "{{AULAS}}": js({int(k): v for k, v in json.load(open(A/"src/aulas.json")).items()}), "{{VIDEOS}}": js(videos)}
for k in sorted(subs, key=len, reverse=True): src = src.replace(k, subs[k])
assert "{{" not in src.replace("{{", "", 0) or True
import re; assert not re.search(r"\{\{[A-Z_]+\}\}", src)
head, rest = src.split("</style>", 1)
full = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="robots" content="noindex">\n<title>Raio-X da Hospedagem · Mini Mentoria de Performance Hoteleira</title>\n'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>\n' + head + "</style>\n</head>\n<body>\n" + rest + "\n</body>\n</html>\n")
(A/"dist").mkdir(exist_ok=True); (A/"dist/index.html").write_text(full); print("dist/index.html", len(full))
