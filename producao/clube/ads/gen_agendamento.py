"""Cards 1080x1350 da campanha 'agendamento direto' (12/11/2026). Uso: python3 -I gen_agendamento.py <raiz-do-repo> <pasta-saida>"""
import sys
R,OUT=sys.argv[1],sys.argv[2]
T='''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:C;src:url(file://RR/docs/assets/fonts/cormorant.woff2)}
@font-face{font-family:A;src:url(file://RR/docs/assets/fonts/aventa.woff2)}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;background:#1B2117;font-family:A,sans-serif;color:#FEF5F0;position:relative;text-align:center}
.tag{position:absolute;left:290px;right:290px;top:48px;background:#FEF5F0;color:#1B2117;font-weight:800;font-size:40px;letter-spacing:.42em;text-indent:.42em;padding:14px 0 10px}
.h1{position:absolute;left:70px;right:70px;top:150px;font-weight:900;font-size:62px;line-height:1.08;text-transform:uppercase}
.h1.s{font-size:54px;top:152px;line-height:1.06}
.h1 em{font-style:italic;color:#C9B37E}
.h2{position:absolute;left:70px;right:70px;top:330px;font-family:C;font-style:italic;font-weight:500;font-size:84px;line-height:1;color:#C9B37E}
.photo{position:absolute;left:0;right:0;top:450px;height:560px;background:url(file://RR/docs/assets/PHOTO) center/cover}
.btn{position:absolute;left:70px;right:70px;top:1050px;background:#C9B37E;color:#1B2117;font-family:C;font-weight:600;font-size:64px;padding:22px 0 14px;border-radius:26px;text-transform:uppercase;letter-spacing:.05em}
.cap{position:absolute;left:90px;right:90px;top:1210px;font-size:36px;line-height:1.3;font-weight:600}
</style></head><body><div class="tag">GLAMPING</div><div class="h1">H1</div><div class="h2">H2</div><div class="photo"></div><div class="btn">BTN</div><div class="cap">CAP</div></body></html>'''
cards={
'card-02':('Quem disse que você precisa de um grande hotel para <em>começar?</em>','Comece pelo seu terreno.','operacoes/op05.webp','Saiba mais','Aprenda o passo a passo para transformar o seu terreno em um projeto de hospedagem'),
'card-03':('Tem um terreno em destino <em>turístico?</em>','Veja o que ele pode ser.','store/hero.webp','Saiba mais','Conheça os produtos da Zion e o passo a passo para colocar o seu projeto de hospedagem de pé'),
'card-04':('A Zion tem uma metodologia de <em>desenvolvimento.</em>','Do terreno ao projeto.','store/dentro.webp','Agende o diagnóstico','Possibilidades de parceria e investimentos, avaliadas caso a caso'),
}
for k,(h1,h2,ph,b,c) in cards.items():
    T2=T.replace('<div class="h1">','<div class="h1 s">') if k in ('card-02','card-04') else T
    open(f'{OUT}/{k}.html','w',encoding='utf-8').write(T2.replace('RR',R).replace('PHOTO',ph).replace('H1',h1).replace('H2',h2).replace('BTN',b).replace('CAP',c))
print('ok')
