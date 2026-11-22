import json,os
R=os.path.dirname(os.path.abspath(__file__)); F='file://'+os.path.abspath(R+'/../../assets/fonts'); L='file://'+os.path.abspath(R+'/../../brand/zion-logo-claro.png')
css=f'''<style>@font-face{{font-family:C;src:url({F}/cormorant.woff2)}}@font-face{{font-family:C;font-style:italic;src:url({F}/cormorant-italic.woff2)}}@font-face{{font-family:A;src:url({F}/aventa.woff2)}}
*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1080px;overflow:hidden;position:relative;font-family:A,sans-serif;color:#FEF5F0;background:#1B2117}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,6,5,.55) 0%,rgba(4,6,5,.10) 30%,rgba(4,6,5,.35) 55%,rgba(4,6,5,.92) 100%)}}
.top{{position:absolute;left:64px;right:64px;top:54px;display:flex;justify-content:space-between;align-items:center;font-size:19px;letter-spacing:.28em;text-transform:uppercase;color:rgba(254,245,240,.9)}}
.top img{{height:34px}}
.cap{{position:absolute;left:64px;right:64px;bottom:96px}}
.k{{font-size:21px;letter-spacing:.3em;text-transform:uppercase;color:#C9B37E;margin-bottom:20px}}
h1{{font-family:C;font-weight:500;font-size:74px;line-height:1.04}}h1 em{{font-style:italic;color:#C9B37E}}
p{{font-size:29px;line-height:1.4;color:rgba(254,245,240,.92);margin-top:20px}}
.foot{{position:absolute;left:64px;right:64px;bottom:40px;font-size:16px;color:rgba(254,245,240,.6)}}
.solid .cap{{bottom:auto;top:50%;transform:translateY(-50%)}}
.price{{font-family:C;font-size:150px;line-height:1;color:#C9B37E;margin:26px 0 8px}}
.btn{{display:inline-block;margin-top:30px;background:#C9B37E;color:#1B2117;font-weight:600;font-size:30px;padding:20px 38px;border-radius:999px}}
.leg{{position:absolute;right:64px;top:110px;font-size:15px;color:rgba(254,245,240,.75)}}</style>'''
T=[("Para quem tem terreno","Você tem um terreno em um <em>destino turístico</em>, mas não tem capital para desenvolver?",None),
("O ponto de partida","Seu terreno pode ter potencial turístico. Mas isso, sozinho, <em>não transforma a área em um negócio</em>.",None),
("O que costuma faltar","Sem projeto estruturado, orçamento e estudo de viabilidade, fica mais difícil <em>conversar com investidores</em>.",None),
("Quem somos","A Zion já opera experiências de hospedagem em destinos como <em>Urubici e Florianópolis</em>.",None),
("Inscrições abertas","Estamos recebendo inscrições de <em>terrenos e projetos turísticos</em> para conhecer novas oportunidades.",None),
("Como funciona","Apresente seu projeto e participe de uma <em>sessão estratégica</em> para entender possíveis caminhos.",None),
("A Zion quer conhecer sua oportunidade",None,None)]
SETS={'A':['a-bubble-deck.jpg','a-aerea-bubbles.jpg',None,'a-noite.jpg','a-por-do-sol.jpg','a-bubble-deck.jpg',None],
      'B':['b-aerea-topo.jpg','b-banheira.jpg','b-masterplan.jpg','b-interior.jpg','b-cama.jpg',None,None]}
POS={'a-bubble-deck.jpg':'center','b-banheira.jpg':'center 70%','b-cama.jpg':'center 80%','a-por-do-sol.jpg':'center top'}
foot="Cadastro e análise não garantem investimento, financiamento nem parceria. A Zion avalia cada caso."
for s,imgs in SETS.items():
    os.makedirs(f'{R}/_html',exist_ok=True)
    for i,(k,h,_) in enumerate(T):
        img=imgs[i]; cls='' if img else 'solid'
        body=''
        if img:
            zoom='background-size:170%;background-position:70% 40%;' if (s=='A' and i==5) else f'background-position:{POS.get(img,"center")};'
            body+=f'<div class="bg" style="background-image:url(file://{R}/src/{img});{zoom}"></div><div class="sh"></div>'
        body+=f'<div class="top"><img src="{L}"><span>{i+1}/7</span></div>'
        if img=='b-masterplan.jpg': body+='<div class="leg">Masterplan ilustrativo</div>'
        if i<6: body+=f'<div class="cap"><div class="k">{k}</div><h1>{h}</h1></div>'
        else: body+=f'<div class="cap"><div class="k">Zion Collection | Projetos &amp; Oportunidades</div><h1>A Zion quer conhecer <em>sua oportunidade</em>.</h1><div class="price">R$ 270</div><p>Inscrição única. Sessão estratégica individual de 45 minutos.</p><span class="btn">Cadastre seu terreno ou projeto</span></div>'
        body+=f'<div class="foot">{foot}</div>'
        open(f'{R}/_html/{s}{i+1}.html','w',encoding='utf-8').write(f'<!doctype html><html><head><meta charset=utf-8>{css}</head><body class="{cls}">{body}</body></html>')
print('ok')
