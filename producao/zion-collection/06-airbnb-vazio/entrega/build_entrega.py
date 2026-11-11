"""Copia os entregáveis finais do Produto 06 e do bump para docs/p/adbc67069af26ae0/ e gera capa (1080×1080) e página de acesso.
O bump fica em pasta separada: quem compra só o produto principal não recebe o link do calendário.
Uso: python3 -I producao/zion-collection/06-airbnb-vazio/entrega/build_entrega.py && node producao/zion-collection/06-airbnb-vazio/entrega/render_capas.js"""
import html, json, pathlib, shutil
A = pathlib.Path(__file__).resolve().parent; P6 = A.parent; R = A.parents[3]
DST = R / "docs/p/adbc67069af26ae0"; E = html.escape
PUBLICO = "Para Airbnb, casas, apartamentos, pousadas e glampings"
FONTES = "".join(f'@font-face{{font-family:{n};src:url({(R / "docs/assets/fonts" / f).as_uri()})}}' for n, f in (("Cormorant", "cormorant.woff2"), ("Aventa", "aventa.woff2")))

PRODUTOS = [
    dict(pasta="zc06-airbnb-vazio", kicker="Zion Collection · Produto 06", titulo="Seu Airbnb Está Vazio?", sub="O problema pode estar na sua oferta",
         promessa="Aprenda o passo a passo para diagnosticar a sua oferta, escolher as três prioridades que mais pesam na decisão do hóspede e montar um plano de 30 dias com responsável, prazo e indicador.",
         itens=["E-book de 60 páginas", "Diagnóstico Zion de Oferta", "Aula e videoaula prática", "Planilhas e fichas"],
         telas=["ebook/img/tela-notas.jpg", "ebook/img/tela-resultado.jpg"],
         arquivos=[("ebook/dist/Seu-Airbnb-Esta-Vazio-Zion-Collection.pdf", "Seu-Airbnb-Esta-Vazio-Zion-Collection.pdf", "E-book · Seu Airbnb Está Vazio?", "PDF · 60 páginas · comece por aqui", True),
                   ("aula/dist/Aula01-Por-que-seu-calendario-esta-vazio.mp4", "Aula01-Por-que-seu-calendario-esta-vazio.mp4", "Aula introdutória", "Vídeo · 5 min · legendado", False),
                   ("ferramenta/dist/diagnostico-zion-de-oferta.html", "diagnostico-zion-de-oferta.html", "Diagnóstico Zion de Oferta", "Abre no navegador do celular ou computador · salva só no seu aparelho", False),
                   ("aula/dist/Videoaula-Pratica-Diagnostico-Zion.mp4", "Videoaula-Pratica-Diagnostico-Zion.mp4", "Videoaula prática", "Vídeo · a ferramenta passo a passo · legendado", False),
                   ("planilhas/dist/Diagnostico-Zion-de-Oferta-EM-BRANCO.xlsx", "Diagnostico-Zion-de-Oferta-EM-BRANCO.xlsx", "Diagnóstico em planilha · em branco", "Excel, Google Sheets ou LibreOffice", True),
                   ("planilhas/dist/Diagnostico-Zion-de-Oferta-EXEMPLO.xlsx", "Diagnostico-Zion-de-Oferta-EXEMPLO.xlsx", "Diagnóstico em planilha · exemplo", "Dados fictícios", True),
                   ("aula/dist/Aula01-Slides.pdf", "Aula01-Slides.pdf", "Slides da aula", "PDF · 10 slides", True)],
         passos=["Assista à aula introdutória (5 minutos).", "Leia o e-book na ordem; faça o exercício de cada capítulo.", "No capítulo 8, abra o Diagnóstico Zion de Oferta e dê as sete notas com evidência.", "Monte o plano, execute a prioridade 1 nesta semana e refaça o diagnóstico em 30 dias."]),
    dict(pasta="zc06-calendario-30", kicker="Complemento do Produto 06", titulo="Calendário comercial de 30 dias", sub="Uma ação por dia para colocar a sua oferta em prática",
         promessa="Aprenda o passo a passo para transformar o diagnóstico em 30 dias de ações curtas, de 15 a 60 minutos, com o que observar em cada uma.",
         itens=["30 ações já escritas", "Datas automáticas", "Resumo por semana", "Versão para imprimir"],
         telas=None,
         arquivos=[("bump/dist/Calendario-Comercial-30-Dias-Zion.pdf", "Calendario-Comercial-30-Dias-Zion.pdf", "Calendário para imprimir", "PDF · 4 páginas", True),
                   ("planilhas/dist/Calendario-Comercial-30-Dias-EM-BRANCO.xlsx", "Calendario-Comercial-30-Dias-EM-BRANCO.xlsx", "Planilha · em branco", "Escreva a data do dia 1 e siga", True),
                   ("planilhas/dist/Calendario-Comercial-30-Dias-EXEMPLO.xlsx", "Calendario-Comercial-30-Dias-EXEMPLO.xlsx", "Planilha · exemplo", "Dados fictícios", True)],
         passos=["Escreva na planilha a data do seu dia 1.", "Faça a ação do dia e marque Feito = Sim.", "Anote o que observou; use os dias de revisão para recuperar o que ficou para trás.", "No dia 29, refaça o Diagnóstico Zion de Oferta e compare."]),
]


def capa_html(p):
    lis = "".join(f"<li>{E(i)}</li>" for i in p["itens"])
    if p["telas"]:
        t1, t2 = [(P6 / x).as_uri() for x in p["telas"]]
        vis = f'<img class="tela t1" src="{t1}"><img class="tela t2" src="{t2}">'
    else:
        dias = "".join(f'<div class="{"f" if d in (1, 2, 3, 5, 8) else ""}">{d}</div>' for d in range(1, 31))
        vis = f'<div class="cal">{dias}</div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTES}
*{{box-sizing:border-box;margin:0}}body{{width:1080px;height:1080px;overflow:hidden;font-family:Aventa,sans-serif;color:#FEF5F0;background:radial-gradient(circle at 78% 40%,#2c3524 0%,#1B2117 55%,#121610 100%);position:relative}}
.logo{{position:absolute;top:64px;left:72px;height:52px}}.txt{{position:absolute;left:72px;top:180px;width:520px}}
.k{{font-size:20px;letter-spacing:.22em;text-transform:uppercase;color:#C9B37E;margin-bottom:22px}}h1{{font-family:Cormorant,serif;font-weight:400;font-size:84px;line-height:1;margin-bottom:16px;color:#C9B37E}}
.s{{font-family:Cormorant,serif;font-style:italic;font-size:34px;line-height:1.15;margin-bottom:34px}}ul{{list-style:none;padding:0}}li{{font-size:25px;color:#DED6BF;padding:0 0 14px 30px;position:relative}}
li:before{{content:"";position:absolute;left:0;top:11px;width:12px;height:12px;background:#C9B37E;border-radius:2px}}
.pub{{position:absolute;left:72px;right:72px;bottom:60px;border-top:1px solid rgba(201,179,126,.45);padding-top:22px;font-size:24px;color:#C9B37E}}
.tela{{position:absolute;width:300px;height:640px;object-fit:cover;object-position:top;border-radius:32px;border:9px solid #0b0e09;box-shadow:0 0 0 2px #C9B37E,0 30px 60px rgba(0,0,0,.55)}}
.t1{{left:600px;top:170px;transform:rotate(-5deg);opacity:.85}}.t2{{left:730px;top:230px;transform:rotate(4deg)}}
.cal{{position:absolute;left:640px;top:200px;width:370px;display:grid;grid-template-columns:repeat(5,1fr);gap:10px}}.cal div{{height:62px;border:1px solid rgba(222,214,191,.3);border-radius:10px;display:grid;place-items:center;font-size:22px;color:#DED6BF}}.cal div.f{{background:#C9B37E;color:#040605}}
</style></head><body><img class="logo" src="{(R / 'docs/brand/zion-logo-claro.png').as_uri()}">
<div class="txt"><div class="k">{E(p['kicker'])}</div><h1>{E(p['titulo'])}</h1><div class="s">{E(p['sub'])}</div><ul>{lis}</ul></div>{vis}
<div class="pub">{PUBLICO}</div></body></html>"""


def acesso_html(p):
    arqs = "".join(f'<a class="arq" href="{nome}"{" download" if dl else ""}><span class="n">{i}</span><span class="t"><b>{E(t)}</b><small>{E(d)}</small></span><span class="b">{"Baixar" if dl else "Abrir"}</span></a>'
                   for i, (_, nome, t, d, dl) in enumerate(p["arquivos"], 1))
    passos = "".join(f"<li>{E(s)}</li>" for s in p["passos"])
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>{E(p['titulo'])} · Seu acesso</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<style>:root{{--musgo:#1B2117;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--ouro:#C9B37E}}*{{box-sizing:border-box}}
body{{margin:0;background:var(--creme);color:var(--musgo);font-family:Jost,Arial,sans-serif;font-size:17px;line-height:1.55}}.wrap{{max-width:680px;margin:0 auto;padding:0 16px 48px}}
.capa{{width:100%;aspect-ratio:1/1;object-fit:cover;display:block;border-radius:0 0 14px 14px;margin:0 auto 26px;max-width:680px}}
h1{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;font-size:clamp(32px,7vw,44px);line-height:1.08;margin:0 0 12px}}.k{{font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--terra);font-weight:600;margin-bottom:8px}}
h2{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;font-size:28px;margin:34px 0 12px}}
.arq{{display:flex;align-items:center;gap:14px;background:#fff;border:1px solid var(--areia);border-radius:12px;padding:14px;margin:10px 0;text-decoration:none;color:var(--musgo)}}
.arq .n{{flex:0 0 36px;height:36px;border-radius:50%;background:var(--musgo);color:var(--creme);display:grid;place-items:center;font-weight:600}}.arq .t{{flex:1;display:flex;flex-direction:column}}.arq small{{color:#6b6656;font-size:14px}}
.arq .b{{background:var(--ouro);color:#040605;font-weight:600;font-size:14px;padding:8px 14px;border-radius:6px}}ol li{{margin-bottom:8px}}.nota{{font-size:14px;color:#6b6656;border-top:1px solid var(--areia);padding-top:16px;margin-top:34px}}
</style></head><body><img class="capa" src="capa.jpg" alt="Capa: {E(p['titulo'])}">
<div class="wrap"><div class="k">{E(p['kicker'])} · Seu acesso</div><h1>{E(p['titulo'])}</h1><p>{E(p['promessa'])}</p><p style="color:#8B714E;font-weight:600">{PUBLICO}.</p>
<h2>Seus materiais</h2>{arqs}<h2>Por onde começar</h2><ol>{passos}</ol>
<p class="nota">Guarde este link: ele é o seu acesso. As planilhas funcionam no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice; a ferramenta abre direto no navegador.<br>
Dúvidas: WhatsApp +55 48 6137-1061. Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor. Material educativo da Zion Hotel Group International: não garante reservas, ocupação nem faturamento.</p></div></body></html>"""


build = A / ".build"; build.mkdir(exist_ok=True); jobs = []
for p in PRODUTOS:
    d = DST / p["pasta"]; d.mkdir(parents=True, exist_ok=True)
    for src, nome, *_ in p["arquivos"]:
        s = P6 / src; assert s.exists(), s; shutil.copy2(s, d / nome)
    (d / "index.html").write_text(acesso_html(p), encoding="utf-8")
    (build / f"{p['pasta']}.html").write_text(capa_html(p), encoding="utf-8"); jobs.append([str(build / f"{p['pasta']}.html"), str(d / "capa.jpg")])
(build / "jobs.json").write_text(json.dumps(jobs)); print("ok", [p["pasta"] for p in PRODUTOS])
