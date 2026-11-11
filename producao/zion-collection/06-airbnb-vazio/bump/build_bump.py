"""PDF imprimível do Calendário comercial de 30 dias (order bump). Uso: python3 -I bump/build_bump.py  → bump/dist/calendario.html"""
import html, pathlib, sys
A = pathlib.Path(__file__).resolve().parent; R = A.parents[3]
sys.path.insert(0, str(A)); from acoes import ACOES, SEMANAS, semana
E = lambda s: html.escape(str(s)); U = lambda p: (R / p).as_uri()
css = f"""@font-face{{font-family:Cormorant;src:url({U('docs/assets/fonts/cormorant.woff2')})}}@font-face{{font-family:Cormorant;font-style:italic;src:url({U('docs/assets/fonts/cormorant-italic.woff2')})}}
@font-face{{font-family:Aventa;src:url({U('docs/assets/fonts/aventa.woff2')})}}@page{{size:210mm 297mm;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:Aventa,sans-serif;color:#1d211b;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:210mm;height:297mm;overflow:hidden;position:relative;background:#FEF5F0;padding:14mm 14mm 12mm;break-after:page}}
h1,h2{{font-family:Cormorant,serif;font-weight:400;margin:0;color:#1B2117}}.k{{font-size:7.5pt;letter-spacing:.24em;text-transform:uppercase;color:#8B714E}}
.capa{{background:radial-gradient(120% 80% at 70% 20%,#26301f,#1B2117 45%,#040605);color:#DED6BF}}.capa h1{{color:#C9B37E;font-size:56pt;line-height:1;margin:10mm 0 6mm}}
.capa .k{{color:#C9B37E}}.capa p{{font-size:11pt;line-height:1.6;max-width:150mm}}.capa .num{{font-family:Cormorant,serif;font-style:italic;font-size:170pt;line-height:.8;color:#C9B37E;opacity:.18;position:absolute;right:10mm;bottom:18mm}}
.sem{{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:10mm}}.sem div{{border-top:.3mm solid rgba(201,179,126,.5);padding-top:3mm;font-size:10pt}}.sem b{{display:block;font-family:Cormorant,serif;font-size:15pt;color:#FEF5F0;font-weight:400}}
.dia{{display:grid;grid-template-columns:13mm 1fr 30mm;gap:3mm;border-bottom:.25mm solid #DED6BF;padding:2.3mm 0;font-size:8.6pt;line-height:1.38;break-inside:avoid}}
.dia .n{{font-family:Cormorant,serif;font-size:21pt;color:#8B714E;line-height:1}}.dia .d{{font-size:6.8pt;letter-spacing:.12em;text-transform:uppercase;color:#8B714E}}
.dia .obs{{font-size:7.2pt;color:#6b6250}}.box{{display:flex;flex-direction:column;gap:1.2mm;font-size:7.2pt;color:#6b6250}}.box i{{display:inline-block;width:3.4mm;height:3.4mm;border:.3mm solid #8B714E;vertical-align:-0.7mm;margin-right:1.2mm}}
.box span.l{{border-bottom:.25mm solid #C9B8A0;height:4.5mm}}.st{{background:#1B2117;color:#FEF5F0;font-size:7.5pt;letter-spacing:.2em;text-transform:uppercase;padding:1.8mm 3mm;margin:3mm 0 0}}
.rod{{position:absolute;bottom:7mm;left:14mm;right:14mm;font-size:7pt;color:#8B714E;display:flex;justify-content:space-between}}"""
pgs = [f"""<section class="pg capa" data-n="1"><img src="{U('docs/brand/zion-logo-claro.png')}" style="height:12mm"><p class="k" style="margin-top:22mm">Zion Collection · Complemento do Produto 06</p>
<h1>Calendário comercial de 30 dias</h1><p>Uma ação por dia, de 15 a 60 minutos, para colocar em prática o diagnóstico da sua oferta. Marque o que fez, anote o que observou e use os dias de revisão para recuperar o que ficou para trás.</p>
<div class="sem">{''.join(f'<div><b>{"Semana " + str(k) if k < 5 else "Dias 29 e 30"}</b>{E(v)}</div>' for k, v in SEMANAS.items())}<div><b>Antes de começar</b>Escreva a data do seu dia 1 e tenha o Diagnóstico Zion de Oferta aberto.</div></div>
<p style="font-size:8.5pt;margin-top:12mm;color:#C9B37E">Complemento opcional do guia “Seu Airbnb Está Vazio?”. Confira as regras atuais da sua plataforma antes de mudar tarifas, fotos ou políticas. Material educativo: resultados dependem do contexto e da execução. Dados do exemplo da planilha são fictícios.</p>
<div class="num">30</div></section>"""]
def bloco(ds, n):
    out, cur = "", None
    for d, dim, acao, mins, obs in ds:
        if semana(d) != cur: cur = semana(d); out += f'<div class="st">{"Semana " + str(cur) if cur < 5 else "Fechamento"} · {E(SEMANAS[cur])}</div>'
        out += f'<div class="dia"><div><div class="n">{d:02d}</div><div class="d">{mins} min</div></div><div><b>{E(dim)}</b> · {E(acao)}<div class="obs">Observar: {E(obs)}</div></div><div class="box"><span><i></i>Feito em ___/___</span><span class="l"></span></div></div>'
    return f'<section class="pg" data-n="{n}"><p class="k">Calendário comercial de 30 dias</p><h2 style="font-size:24pt;margin:1mm 0 1mm">Dias {ds[0][0]} a {ds[-1][0]}</h2>{out}<div class="rod"><span>Zion Hotel Group International · material educativo</span><span>{n:02d}</span></div></section>'
pgs += [bloco(ACOES[0:10], 2), bloco(ACOES[10:20], 3), bloco(ACOES[20:30], 4)]
(A / "dist").mkdir(exist_ok=True); (A / "dist/calendario.html").write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Calendário comercial de 30 dias</title><style>{css}</style></head><body>{"".join(pgs)}</body></html>')
print("bump/dist/calendario.html", len(pgs), "páginas")
