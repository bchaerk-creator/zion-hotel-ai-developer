import sys
R,OUT=sys.argv[1],sys.argv[2]
tpl='''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:C;src:url(file://RR/docs/assets/fonts/cormorant.woff2)}@font-face{font-family:A;src:url(file://RR/docs/assets/fonts/aventa.woff2)}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden;background:#1E3A16;font-family:A,sans-serif;color:#fff;position:relative;text-align:center}
.tag{position:absolute;left:190px;right:190px;top:56px;background:#fff;color:#1E3A16;font-weight:800;font-size:54px;letter-spacing:.42em;padding:16px 0 12px;text-indent:.42em}
h1{position:absolute;left:60px;right:60px;top:190px;font-weight:900;font-size:58px;line-height:1.1;text-transform:uppercase;letter-spacing:.01em}
h1 em{font-style:italic}
.photo{position:absolute;left:0;right:0;top:__TOP__;height:__HPX__;background:url(file://RR/docs/assets/operacoes/op08.webp) center/cover}
.cab{position:absolute;right:30px;top:__CAB__;background:#1E3A16;color:#fff;font-family:C;font-size:50px;padding:22px 60px;border-radius:26px}
.btn{position:absolute;left:62px;right:62px;top:__BTNT__;background:#8C7A2C;color:#fff;font-family:C;font-weight:500;font-size:72px;padding:26px 0 18px;border-radius:26px;text-transform:uppercase;letter-spacing:.04em}
.cap{position:absolute;left:60px;right:60px;top:__CAPT__;font-weight:700;font-size:38px;line-height:1.2}
</style></head><body><div class="tag">GLAMPING</div><h1>__HEAD__</h1><div class="photo"></div><div class="cab">CABANA</div><div class="btn">__BTN__</div><div class="cap">__CAP__</div></body></html>'''
cards={
'clube':('Transforme seu terreno em um destino <em>turístico</em> e aprenda o passo a passo.','Entre para o clube','Tenha acesso aos melhores investimentos e aos melhores produtos para viabilizar o seu projeto',410,610,830,1070,1215),
'parceiro':('Transforme seu terreno em um destino <em>turístico.</em> Seja um parceiro Zion.','Parceiro Zion','Tenha acesso aos melhores investimentos e aos melhores produtos para viabilizar o seu projeto',410,610,830,1070,1215),
}
for k,(h,b,c,top,hp,cab,btn,cap) in cards.items():
    html=tpl.replace('RR',R).replace('__TOP__',f'{top}px').replace('__HPX__',f'{hp}px').replace('__CAB__',f'{cab}px').replace('__BTNT__',f'{btn}px').replace('__CAPT__',f'{cap}px').replace('__HEAD__',h).replace('__BTN__',b).replace('__CAP__',c)
    open(f'{OUT}/{k}.html','w',encoding='utf-8').write(html)
print('ok')
