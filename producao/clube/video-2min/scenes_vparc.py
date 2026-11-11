import re,sys
V,R,OUT,FMT=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]   # FMT: wide | tall
page=open(f"{V}/page.html",encoding="utf-8").read()
svg=re.search(r'<svg viewBox="0 0 400 400".*?</svg>',page,re.S).group(0)
W,H=(1920,1080) if FMT=="wide" else (1080,1350)
base='''<style>@font-face{font-family:C;src:url(file://RR/docs/assets/fonts/cormorant.woff2)}@font-face{font-family:C;font-style:italic;src:url(file://RR/docs/assets/fonts/cormorant-italic.woff2)}@font-face{font-family:A;src:url(file://RR/docs/assets/fonts/aventa.woff2)}
*{margin:0;box-sizing:border-box}body{width:WWpx;height:HHpx;overflow:hidden;background:#1B2117;color:#FEF5F0;font-family:A,sans-serif;position:relative}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}.sh{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,6,5,.2),rgba(4,6,5,.82))}
.k{font-size:24px;letter-spacing:.28em;text-transform:uppercase;color:#C9B37E}
h1{font-family:C;font-weight:500;line-height:1.02;margin-top:16px}h1 em{font-style:italic;color:#C9B37E}
.lead{font-size:30px;margin-top:22px;color:rgba(254,245,240,.85);line-height:1.35}
.c{border:1px solid rgba(201,179,126,.6);border-radius:18px;padding:30px 26px;background:rgba(254,245,240,.05)}.c b{font-family:C;font-size:58px;color:#C9B37E;display:block;line-height:1}.c h3{font-family:C;font-weight:500;font-size:36px;margin-top:12px;line-height:1.1}.c p{font-size:21px;color:rgba(254,245,240,.78);margin-top:8px}
.facts div{border-left:3px solid #C9B37E;padding-left:18px}.facts b{font-family:C;font-weight:500;font-size:40px;display:block;line-height:1.05}.facts span{font-size:21px;color:rgba(254,245,240,.75)}
.btn{display:inline-block;margin-top:34px;background:#C9B37E;color:#1B2117;font-weight:600;font-size:36px;padding:24px 48px;border-radius:999px}
.bruno{position:absolute;object-fit:cover;object-position:35% 15%;border-radius:22px;border:2px solid #C9B37E;filter:brightness(1.15)}
</style>'''.replace("RR",R).replace("WW",str(W)).replace("HH",str(H))
if FMT=="wide":
    css=base+'''<style>.logo{position:absolute;right:90px;top:70px;width:200px}h1{font-size:88px}.cap{position:absolute;left:120px;right:120px;bottom:110px}.quote{position:absolute;left:120px;right:120px;top:50%;transform:translateY(-50%)}
    .head{position:absolute;left:120px;right:120px;top:110px}.grid{position:absolute;left:120px;right:120px;top:340px;display:grid;gap:22px}.g5{grid-template-columns:repeat(5,1fr)}.g4{grid-template-columns:repeat(4,1fr)}.c{min-height:400px}
    .ops{position:absolute;right:460px;top:300px}.ops svg{width:520px}.mapwrap{position:absolute}.facts{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:30px}
    .bruno{right:120px;bottom:100px;width:280px;height:350px}.cta{position:absolute;left:120px;right:120px;top:50%;transform:translateY(-50%);text-align:center}</style>'''
else:
    css=base+'''<style>.logo{position:absolute;left:72px;top:64px;width:170px}h1{font-size:72px}.cap{position:absolute;left:72px;right:72px;bottom:110px}.quote{position:absolute;left:72px;right:72px;top:50%;transform:translateY(-50%)}
    .head{position:absolute;left:72px;right:72px;top:190px}.grid{position:absolute;left:72px;right:72px;top:480px;display:grid;gap:18px;grid-template-columns:1fr 1fr}.c b{font-size:50px}.c h3{font-size:32px}
    .ops svg{width:560px;display:block;margin:0 auto}.mapwrap{position:absolute;left:72px;right:72px;top:560px}.facts{position:absolute;left:72px;right:72px;bottom:90px;display:grid;grid-template-columns:1fr 1fr;gap:24px}
    .bruno{right:72px;top:150px;width:220px;height:275px}.cta{position:absolute;left:72px;right:72px;top:50%;transform:translateY(-50%);text-align:center}</style>'''
logo=f'<img class="logo" src="file://{R}/docs/brand/zion-logo-claro.png">'
G=f"file://{R}/docs/"
bruno=f'<img class="bruno" src="file://{R}/docs/zion-collection/hero-bruno-bolha.jpg">'
etapas='<div class="c"><b>01</b><h3>Potencial do terreno</h3><p>Localização, acessos, demanda</p></div><div class="c"><b>02</b><h3>Modelo de hospedagem</h3><p>Cabanas, pousada, hotel, glamping</p></div><div class="c"><b>03</b><h3>Números</h3><p>Investimento, receita, viabilidade</p></div><div class="c"><b>04</b><h3>Proposta</h3><p>Dossiê e plano de negócios</p></div><div class="c"'+(' style="grid-column:1/3"' if FMT=="tall" else '')+'><b>05</b><h3>Apresentação</h3><p>Pronto para parceiro, sócio ou investidor</p></div>'
clube='<div class="c"><b>01</b><h3>Conhecimento</h3><p>Formação e sessão estratégica com a equipe Zion</p></div><div class="c"><b>02</b><h3>Melhores produtos</h3><p>Acesso aos melhores produtos do mercado</p></div><div class="c"><b>03</b><h3>Acesso a investimentos</h3><p>Seu terreno no Radar do Land Bank</p></div><div class="c"><b>04</b><h3>Parcerias e investidores</h3><p>Capital da própria Zion ou do pool de investidores</p></div>'
if FMT=="wide":
    mapa=f'{logo}<div class="ops"><div>{svg}</div><div style="padding-right:300px"><div class="k">O maior clube de glamping do Brasil</div><h1 style="font-size:64px">O seu pode ser <em>o próximo destino.</em></h1><div class="facts"><div><b>Referência no setor</b><span>em busca dos melhores destinos do país</span></div><div><b>Expansão Zion</b><span>novas sedes por todo o Brasil</span></div></div></div></div>{bruno}'
else:
    mapa=f'{logo}<div class="head" style="right:320px"><div class="k">O maior clube de glamping do Brasil</div><h1 style="font-size:60px">O seu pode ser <em>o próximo destino.</em></h1></div><div class="mapwrap ops">{svg}</div><div class="facts"><div><b>Referência no setor</b><span>em busca dos melhores destinos do país</span></div><div><b>Expansão Zion</b><span>novas sedes por todo o Brasil</span></div></div>{bruno}'
scenes={
1:f'<div class="cap"><div class="k">Seja um parceiro Zion</div><h1>Tem hospedagem ou terreno com infraestrutura? <em>É assim que funciona.</em></h1></div>',
2:f'{logo}<div class="head"><div class="k">Você entra com</div><h1 style="font-size:{"78" if FMT=="wide" else "64"}px">A área <em>e a infraestrutura.</em></h1></div><div class="grid g4"><div class="c"><b>01</b><h3>Deck de madeira</h3><p>De cada unidade</p></div><div class="c"><b>02</b><h3>Luz e água</h3><p>Instalação elétrica e hidráulica</p></div><div class="c"><b>03</b><h3>Internet e fossa</h3><p>Conexão e esgoto</p></div><div class="c"><b>04</b><h3>Mobília</h3><p>Da unidade e das áreas comuns</p></div></div>',
3:f'{logo}<div class="head"><div class="k">A Zion entra com</div><h1 style="font-size:{"78" if FMT=="wide" else "64"}px">A cabana, a marca <em>e a gestão.</em></h1></div><div class="grid g4"><div class="c"><b>01</b><h3>A cabana</h3><p>Bubble ou cabana do padrão Zion</p></div><div class="c"><b>02</b><h3>Marca e reputação</h3><p>O nome que o hóspede já procura</p></div><div class="c"><b>03</b><h3>Reservas</h3><p>Sistema, canais e gestão das reservas</p></div><div class="c"><b>04</b><h3>Formação</h3><p>Equipe treinada no padrão Zion</p></div></div>',
4:f'{logo}<div class="head" style="right:320px"><div class="k">Quem opera?</div><h1 style="font-size:{"66" if FMT=="wide" else "58"}px">Um gerente local, <em>contratado e formado pela Zion.</em></h1><p class="lead">Dentro dos padrões das nossas unidades, em Urubici e Florianópolis.</p></div><div class="mapwrap ops">{svg}</div>{bruno}',
5:f'{logo}<div class="head"><div class="k">Quanto fatura? Quanto você ganha?</div><h1 style="font-size:{"78" if FMT=="wide" else "64"}px">A projeção do seu local, <em>estruturada junto.</em></h1></div><div class="grid g4"><div class="c"><b>01</b><h3>Quantas cabanas cabem</h3><p>No seu local</p></div><div class="c"><b>02</b><h3>Quanto cada lado entra</h3><p>Você e a Zion</p></div><div class="c"><b>03</b><h3>A conta do seu caso</h3><p>Receita, custo e divisão</p></div><div class="c"><b>04</b><h3>Montada na reunião</h3><p>Com a equipe Zion</p></div></div>',
6:f'<div class="bg" style="background-image:url({G}assets/store/noite.webp)"></div><div class="sh"></div>{logo}<div class="cta"><div class="k">Quer saber mais?</div><h1>Entre para o clube <em>e vire parceiro da Zion.</em></h1><p class="lead">Nós vamos te ajudar.</p><span class="btn">Quero ser parceiro →</span></div>'}
for i,h in scenes.items():
    open(f"{OUT}/s{i}.html","w",encoding="utf-8").write("<!doctype html><html><head><meta charset=utf-8>"+css+"</head><body>"+h+"</body></html>")
print("ok",FMT)
