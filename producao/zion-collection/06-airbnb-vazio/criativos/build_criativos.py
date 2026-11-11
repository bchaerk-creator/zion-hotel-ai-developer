"""Cinco criativos 1080×1350 do Produto 06 (dor, quebra de crença, demonstração, erro comum, autoridade).
Sem foto de hospedagem no topo; a foto real da Zion entra só no criativo de autoridade, com legenda.
Uso: python3 -I criativos/build_criativos.py && node criativos/render_criativos.js"""
import html, pathlib
A = pathlib.Path(__file__).resolve().parent; P = A.parent; R = A.parents[3]
E = html.escape; U = lambda p: (R / p).as_uri(); IMG = lambda f: (P / "ebook/img" / f).as_uri()
css = f"""@font-face{{font-family:Cormorant;src:url({U('docs/assets/fonts/cormorant.woff2')})}}@font-face{{font-family:Cormorant;font-style:italic;src:url({U('docs/assets/fonts/cormorant-italic.woff2')})}}
@font-face{{font-family:Aventa;src:url({U('docs/assets/fonts/aventa.woff2')})}}*{{box-sizing:border-box}}body{{margin:0;background:#333}}
.c{{width:1080px;height:1350px;position:relative;overflow:hidden;background:radial-gradient(120% 80% at 75% 15%,#27311f 0%,#1B2117 46%,#040605 100%);color:#DED6BF;font-family:Aventa,sans-serif;margin-bottom:20px}}
.logo{{position:absolute;top:60px;left:70px;height:46px}}.k{{position:absolute;top:150px;left:70px;font-size:22px;letter-spacing:.26em;text-transform:uppercase;color:#C9B37E}}
h1{{position:absolute;top:196px;left:70px;right:70px;font-family:Cormorant,serif;font-weight:400;font-size:92px;line-height:1;color:#FEF5F0;margin:0}}h1 em{{color:#C9B37E}}
.sub{{position:absolute;left:70px;right:70px;font-size:32px;line-height:1.4}}
.cta{{position:absolute;left:70px;right:70px;bottom:120px;display:flex;align-items:center;justify-content:space-between;background:#C9B37E;color:#040605;border-radius:999px;padding:28px 40px;font-size:32px;font-weight:600}}
.cta span{{font-family:Cormorant,serif;font-size:40px;font-weight:600}}
.rod{{position:absolute;left:70px;right:70px;bottom:50px;display:flex;justify-content:space-between;font-size:17px;letter-spacing:.12em;text-transform:uppercase;color:rgba(201,179,126,.8)}}
.tel{{position:absolute;border-radius:46px;border:12px solid #0b0e09;box-shadow:0 0 0 2px #C9B37E,0 40px 90px rgba(0,0,0,.6);background-size:cover;background-position:top center}}
.cal{{position:absolute;left:70px;right:70px;top:640px;display:grid;grid-template-columns:repeat(7,1fr);gap:12px}}.cal div{{height:74px;border-radius:12px;border:1px solid rgba(222,214,191,.25);display:grid;place-items:center;font-size:24px;color:rgba(222,214,191,.6)}}
.cal div.v{{background:#C9B37E;color:#040605;border-color:#C9B37E}}
.tach{{position:absolute;left:70px;right:70px;top:610px}}.tach div{{border-top:1px solid rgba(201,179,126,.35);padding:26px 0;font-size:40px;display:flex;justify-content:space-between}}
.tach s{{color:rgba(222,214,191,.5)}}.tach b{{color:#FEF5F0;font-weight:400;font-family:Cormorant,serif;font-size:50px}}
.ab{{position:absolute;left:70px;right:70px;top:650px}}.ab .l{{font-size:20px;letter-spacing:.2em;text-transform:uppercase;color:#C9B37E;margin:0 0 10px}}
.ab .x{{border:1px solid rgba(222,214,191,.3);border-radius:18px;padding:26px 30px;font-size:38px;margin:0 0 26px}}.ab .x.ruim{{color:rgba(222,214,191,.55);text-decoration:line-through}}.ab .x.bom{{border-color:#C9B37E;color:#FEF5F0}}
.foto{{position:absolute;left:70px;right:70px;top:560px;height:390px;border-radius:20px;background-size:cover;background-position:center}}.leg{{position:absolute;left:70px;top:960px;font-size:18px;color:rgba(222,214,191,.65)}}
.passos{{position:absolute;left:70px;right:70px;top:1010px;display:flex;justify-content:space-between;font-size:26px;color:#FEF5F0}}.passos i{{color:#C9B37E;font-style:normal}}"""
ROD = '<div class="rod"><span>Para Airbnb, casas, apartamentos, pousadas e glampings</span><span>Material educativo</span></div>'
CTA = '<div class="cta">Aprenda o passo a passo <span>R$ 47</span></div>'
LOGO = f'<img class="logo" src="{U("docs/brand/zion-logo-claro.png")}">'
vend = {3, 4, 9, 10, 17, 24}
cards = {
 "c1-dor": f"""{LOGO}<div class="k">Seu Airbnb está vazio?</div><h1>Seu calendário tem <em>muitas datas livres?</em></h1>
<div class="sub" style="top:470px">Antes de baixar a diária, descubra o que está afastando o hóspede.</div>
<div class="cal">{''.join(f'<div class="{"v" if d in vend else ""}">{d}</div>' for d in range(1, 29))}</div>{CTA}{ROD}""",
 "c2-crenca": f"""{LOGO}<div class="k">Quebra de crença</div><h1>Baixar o preço <em>nem sempre resolve.</em></h1>
<div class="sub" style="top:470px">O hóspede compara fotos, título, avaliações e a sua resposta. Não só a diária.</div>
<div class="tach"><div><s>Baixar a diária no escuro</s></div><div><b>Rever a oferta com evidência</b></div><div><b>Escolher 3 prioridades</b></div><div><b>Medir antes e depois</b></div></div>{CTA}{ROD}""",
 "c3-demo": f"""{LOGO}<div class="k">Demonstração</div><h1 style="right:440px;font-size:84px">Veja a sua oferta em <em>7 notas.</em></h1>
<div class="sub" style="top:560px;right:450px">Diagnóstico Zion de Oferta: notas de 0 a 5 com evidência, as 3 prioridades e um plano de ação.</div>
<div class="sub" style="top:900px;right:450px;font-size:22px;color:#C9B37E">Tela real da ferramenta · exemplo com dados fictícios</div>
<div class="tel" style="right:60px;top:170px;width:380px;height:820px;background-image:url({IMG('tela-resultado.jpg')})"></div>{CTA}{ROD}""",
 "c4-erro": f"""{LOGO}<div class="k">Erro comum</div><h1>Título bonito <em>que não diz nada.</em></h1>
<div class="sub" style="top:470px">O título precisa dizer para quem é e o que tem de diferente. Adjetivo não é informação.</div>
<div class="ab"><p class="l">Antes</p><div class="x ruim">Lindo apê aconchegante</div><p class="l">Depois</p><div class="x bom">Apê para casal a 5 min da praia, com varanda</div><p class="l" style="color:rgba(222,214,191,.6)">Exemplo ilustrativo</p></div>{CTA}{ROD}""",
 "v3-fundo": f"""{LOGO}<div class="k">Demonstração · tela real</div><h1 style="font-size:72px">Veja a sua oferta em <em>7 notas.</em></h1><div class="sub" style="top:1068px;font-size:20px;color:#C9B37E">Exemplo com dados fictícios</div>{CTA}{ROD}""",
 "c5-autoridade": f"""{LOGO}<div class="k">De onde vem o método</div><h1 style="font-size:80px">Da rotina das unidades Zion <em>para a sua hospedagem.</em></h1>
<div class="foto" style="background-image:url({IMG('op05.jpg')})"></div><div class="leg">Foto real · Zion Bubble Glamping (SC)</div>
<div class="passos"><span>Diagnóstico</span><i>→</i><span>Prioridade</span><i>→</i><span>Ação</span><i>→</i><span>Medição</span></div>{CTA}{ROD}""",
}
(A / "dist").mkdir(exist_ok=True)
(A / "dist/criativos.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>' + "".join(f'<section class="c" id="{k}">{v}</section>' for k, v in cards.items()) + "</body></html>")
print(len(cards), "criativos")
