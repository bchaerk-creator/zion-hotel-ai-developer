"""Gera slides 16:9 (HTML), teleprompter (MD), legendas SRT e o plano de tempos da Aula introdutória.
Tempo de cada slide = palavras da fala ÷ 2,2 palavras/s + 2 s de respiro (ritmo de leitura em voz alta).
Uso: python3 -I aula/build_aula.py"""
import html, json, pathlib, sys
A = pathlib.Path(__file__).resolve().parent; R = A.parents[3]
sys.path.insert(0, str(A)); from roteiro import AULA, PRATICA
E = lambda s: html.escape(str(s)); U = lambda p: (R / p).as_uri()
D = A / "dist"; D.mkdir(exist_ok=True)
WPS, RESP = 2.2, 2.0

def tc(s):
    ms = int(round(s * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

def quebrar(fala, maxp=12):
    """Divide a fala em legendas de até ~12 palavras, respeitando pontuação."""
    out, cur = [], []
    for w in fala.split():
        cur.append(w)
        if len(cur) >= maxp or (len(cur) >= 6 and w[-1] in ".:?!"):
            out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    return out

def srt_de(blocos):
    """blocos: [(inicio, duracao, fala)] → texto SRT com legendas proporcionais ao número de palavras."""
    linhas, n = [], 1
    for ini, dur, fala in blocos:
        partes = quebrar(fala); total = sum(len(p.split()) for p in partes); t = ini + 0.4; util = dur - 0.8
        for p in partes:
            d = util * len(p.split()) / total
            linhas += [str(n), f"{tc(t)} --> {tc(t + d - 0.05)}", p, ""]; n += 1; t += d
    return "\n".join(linhas)

# tempos
tempos, t = [], 0.0
for s in AULA["slides"]:
    d = round(len(s["fala"].split()) / WPS + RESP, 1); tempos.append((t, d)); t += d
(D / "aula01_tempos.json").write_text(json.dumps([{"slide": i + 1, "inicio": a, "duracao": b} for i, (a, b) in enumerate(tempos)], indent=1))
(D / "aula01.srt").write_text(srt_de([(a, b, s["fala"]) for (a, b), s in zip(tempos, AULA["slides"])]))

# slides
css = f"""@font-face{{font-family:Cormorant;src:url({U('docs/assets/fonts/cormorant.woff2')})}}@font-face{{font-family:Cormorant;font-style:italic;src:url({U('docs/assets/fonts/cormorant-italic.woff2')})}}
@font-face{{font-family:Aventa;src:url({U('docs/assets/fonts/aventa.woff2')})}}@page{{size:1920px 1080px;margin:0}}*{{box-sizing:border-box}}body{{margin:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.s{{width:1920px;height:1080px;position:relative;overflow:hidden;background:radial-gradient(110% 90% at 80% 10%,#26301f 0%,#1B2117 48%,#040605 100%);color:#DED6BF;font-family:Aventa,sans-serif;break-after:page}}
.logo{{position:absolute;top:70px;left:110px;height:52px}}.cont{{position:absolute;top:96px;right:110px;font-size:22px;letter-spacing:.2em;color:#C9B37E}}
.k{{position:absolute;top:250px;left:110px;font-size:24px;letter-spacing:.3em;text-transform:uppercase;color:#C9B37E}}
h1{{position:absolute;top:300px;left:110px;width:1150px;font-family:Cormorant,serif;font-weight:400;font-size:96px;line-height:1.02;color:#FEF5F0;margin:0}}
ul{{position:absolute;left:110px;top:540px;width:1200px;list-style:none;padding:0;margin:0}}li{{font-size:36px;line-height:1.35;padding:14px 0 14px 44px;position:relative;border-top:1px solid rgba(201,179,126,.25)}}
li:before{{content:"";position:absolute;left:0;top:34px;width:20px;height:2px;background:#C9B37E}}
.lado{{position:absolute;right:120px;top:230px;width:470px}}.num{{position:absolute;right:110px;top:120px;font-family:Cormorant,serif;font-style:italic;font-size:260px;line-height:.8;color:#C9B37E;opacity:.16}}
.rod{{position:absolute;left:110px;top:150px;font-size:16px;letter-spacing:.14em;color:rgba(201,179,126,.7);text-transform:uppercase}}
.tel{{width:430px;height:640px;border-radius:40px;border:10px solid #0b0e09;box-shadow:0 0 0 2px #C9B37E,0 40px 80px rgba(0,0,0,.5);background-size:cover;background-position:top center}}
.dims{{position:absolute;left:110px;top:540px;width:1700px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}.dims div{{border:1px solid rgba(201,179,126,.4);border-radius:16px;padding:22px;font-size:30px;color:#FEF5F0;min-height:120px}}.dims b{{display:block;font-family:Cormorant,serif;font-style:italic;font-size:40px;color:#C9B37E;font-weight:400}}"""
imgs = {5: "tela-notas.jpg", 6: "tela-resultado.jpg", 7: "tela-resultado.jpg", 8: "tela-plano.jpg"}
dims = ["Fotos e apresentação", "Título e descrição", "Preço e posicionamento", "Diferenciais e experiência", "Avaliações e confiança", "Atendimento e comunicação", "Conforto e infraestrutura"]
secs = []
for i, s in enumerate(AULA["slides"], 1):
    corpo = ""
    if i == 4:
        corpo = '<div class="dims">' + "".join(f"<div><b>{j + 1:02d}</b>{E(d)}</div>" for j, d in enumerate(dims)) + "</div>"
    else:
        larg = "1150px" if i in imgs else "1500px"
        corpo = f'<ul style="width:{larg}">' + "".join(f"<li>{E(p)}</li>" for p in s["pontos"]) + "</ul>"
        if i in imgs: corpo += f'<div class="lado"><div class="tel" style="background-image:url({(A.parent / "ebook/img" / imgs[i]).as_uri()})"></div></div>'
    h1w = "style=\"width:1150px\"" if i in imgs else "style=\"width:1600px\""
    secs.append(f'<section class="s" data-n="{i}"><img class="logo" src="{U("docs/brand/zion-logo-claro.png")}"><div class="cont">{i:02d} / 10</div><div class="k">{E(s["kicker"])}</div><h1 {h1w}>{E(s["titulo"])}</h1>{corpo}'
                f'{"" if i in imgs else f"<div class=num>{i:02d}</div>"}<div class="rod">Zion Collection · Seu Airbnb Está Vazio?{" · exemplo com dados fictícios" if i == 6 else ""}</div></section>')
(D / "slides.html").write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{E(AULA["titulo"])}</title><style>{css}</style></head><body>{"".join(secs)}</body></html>')

# teleprompter
md = [f"# {AULA['titulo']}", "", "Teleprompter para gravação (Bruno ou locutor com voz licenciada). Leia em ritmo de conversa; cada bloco corresponde a um slide.", ""]
for i, ((a, d), s) in enumerate(zip(tempos, AULA["slides"]), 1):
    md += [f"## Slide {i:02d} · {s['kicker']} · {s['titulo']}  ({tc(a)[3:8]} · {d:.0f} s)", "", s["fala"], ""]
md += [f"Duração total estimada: {t / 60:.1f} min.", "", "---", "", "# Videoaula prática · Diagnóstico Zion de Oferta na prática", "",
       "A gravação de tela já está pronta (`dist/videoaula_pratica.mp4`, legendada). Grave a narração abaixo por cima, no mesmo ritmo.", ""]
for k, (cid, tit, fala) in enumerate(PRATICA, 1): md += [f"## {k:02d} · {tit}", "", fala, ""]
(A / "TELEPROMPTER.md").write_text("\n".join(md))
print(f"aula: {len(secs)} slides, {t / 60:.1f} min; dist/slides.html, dist/aula01.srt, TELEPROMPTER.md")
