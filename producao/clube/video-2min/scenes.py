import re,sys
V,R=sys.argv[1],sys.argv[2]
page=open(f"{V}/page.html",encoding="utf-8").read()
m=re.search(r'<svg viewBox="0 0 400 400".*?</svg>',page,re.S)
svg=m.group(0) if m else "<div style='color:red'>SVG?</div>"
css='''<style>@font-face{font-family:C;src:url(file://RR/docs/assets/fonts/cormorant.woff2)}@font-face{font-family:C;font-style:italic;src:url(file://RR/docs/assets/fonts/cormorant-italic.woff2)}@font-face{font-family:A;src:url(file://RR/docs/assets/fonts/aventa.woff2)}
*{margin:0;box-sizing:border-box}body{width:1920px;height:1080px;overflow:hidden;background:#1B2117;color:#FEF5F0;font-family:A,sans-serif;position:relative}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,6,5,.15),rgba(4,6,5,.78))}
.cap{position:absolute;left:120px;right:120px;bottom:110px}.k{font-size:26px;letter-spacing:.28em;text-transform:uppercase;color:#C9B37E}
h1{font-family:C;font-weight:500;font-size:96px;line-height:1.02;margin-top:18px}h1 em{font-style:italic;color:#C9B37E}
.logo{position:absolute;right:90px;top:70px;width:200px}
.grid{position:absolute;left:120px;right:120px;top:330px;display:grid;grid-template-columns:repeat(5,1fr);gap:22px}.c{border:1px solid rgba(201,179,126,.6);border-radius:18px;padding:34px 28px;background:rgba(254,245,240,.05);min-height:420px}.c b{font-family:C;font-size:72px;color:#C9B37E;display:block;line-height:1}.c h3{font-family:C;font-weight:500;font-size:38px;margin-top:16px;line-height:1.1}.c p{font-size:22px;color:rgba(254,245,240,.78);margin-top:10px}
.ops{position:absolute;inset:0;display:grid;grid-template-columns:760px 1fr;align-items:center;padding:0 120px;gap:60px}.ops svg{width:760px;height:auto}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:28px}.facts div{border-left:3px solid #C9B37E;padding-left:20px}.facts b{font-family:C;font-weight:500;font-size:42px;display:block;line-height:1.05}.facts span{font-size:24px;color:rgba(254,245,240,.75)}
.cta{position:absolute;left:1040px;top:170px;width:760px;border:2px solid #C9B37E;border-radius:28px;padding:54px 56px;background:rgba(27,33,23,.93)}.cta .t{font-size:24px;letter-spacing:.24em;text-transform:uppercase;color:#C9B37E}.cta .p{font-family:C;font-size:92px;white-space:nowrap;line-height:1;color:#C9B37E;margin-top:14px}.cta small{font-size:30px;display:block;color:rgba(254,245,240,.85);margin-top:6px}.cta ul{list-style:none;margin-top:26px;font-size:30px;line-height:1.5}.cta li::before{content:"✓ ";color:#C9B37E}.cta .btn{display:inline-block;margin-top:34px;background:#C9B37E;color:#1B2117;font-weight:600;font-size:38px;padding:24px 48px;border-radius:999px}
.bruno{position:absolute;right:120px;bottom:100px;width:300px;height:375px;object-fit:cover;object-position:35% 15%;border-radius:22px;border:2px solid #C9B37E;filter:brightness(1.15)}
.quote{position:absolute;left:120px;right:120px;top:50%;transform:translateY(-50%)}
</style>'''.replace("RR",R)
logo=f'<img class="logo" src="file://{R}/docs/brand/zion-logo-claro.png">'
G=f"file://{R}/docs/"
scenes={
1:f'<div class="bg" style="background-image:url({G}assets/operacoes/op08.webp)"></div><div class="sh"></div>{logo}<div class="cap"><div class="k">Você tem o terreno</div><h1>De onde vem <em>o dinheiro?</em></h1></div>',
2:f'{logo}<div class="quote"><div class="k">O que ninguém te disse</div><h1>Investidor não coloca dinheiro em terreno.<br><em>Coloca em projeto que ele entende.</em></h1><p style="font-size:34px;margin-top:40px;color:rgba(254,245,240,.8)">Terreno parado não é falta de capital. É falta de projeto no papel.</p></div>',
3:f'{logo}<div class="ops"><div>{svg}</div><div style="padding-right:340px"><div class="k">Operações reais · desde 2020</div><h1 style="font-size:66px;margin:14px 0 30px">Seja você <em>o próximo destino.</em></h1><div class="facts"><div><b>Urubici e Florianópolis</b><span>unidades em operação</span></div><div><b>Mais de 23</b><span>destinos em desenvolvimento</span></div></div></div></div><img class="bruno" src="file://{R}/docs/zion-collection/hero-bruno-bolha.jpg">',
4:f'{logo}<div style="position:absolute;left:120px;top:110px"><div class="k">O caminho Zion</div><h1 style="font-size:78px">Cinco etapas, <em>nesta ordem.</em></h1></div><div class="grid"><div class="c"><b>01</b><h3>Potencial do terreno</h3><p>Localização, acessos, demanda</p></div><div class="c"><b>02</b><h3>Modelo de hospedagem</h3><p>Cabanas, pousada, hotel, glamping</p></div><div class="c"><b>03</b><h3>Números</h3><p>Investimento, receita, viabilidade</p></div><div class="c"><b>04</b><h3>Proposta</h3><p>Dossiê e plano de negócios</p></div><div class="c"><b>05</b><h3>Apresentação</h3><p>Sócio, investidor, Radar do Land Bank</p></div></div>',
5:f'<div class="bg" style="background-image:url({G}assets/store/noite.webp)"></div><div class="sh"></div>{logo}<div style="position:absolute;left:120px;top:200px;width:860px"><div class="k">Zion Collection Club</div><h1>Entre para o clube. <em>Seja você o próximo destino.</em></h1></div><div class="cta"><div class="t">Adesão ao clube</div><div class="p">2x de R$ 48,50</div><small>ou R$ 97 à vista</small><ul><li>Formação para estruturar o projeto</li><li>Sessão estratégica com a equipe Zion</li><li>Terreno no Radar do Land Bank</li></ul><span class="btn">Entre para o clube →</span></div>'}
for i,h in scenes.items():
    open(f"{V}/s{i}.html","w",encoding="utf-8").write("<!doctype html><html><head><meta charset=utf-8>"+css+"</head><body>"+h+"</body></html>")
print("ok", bool(m))
