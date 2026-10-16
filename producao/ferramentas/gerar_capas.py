import re,json,asyncio,html
from playwright.async_api import async_playwright
R='/home/claude/zion-hotel-ai-developer/'
src=open(R+'docs/escola/f02/index.html').read()
fonts='\n'.join(re.findall(r'@font-face\{.*?\}',src[:200000],re.S))
d=json.load(open(R+'producao/fila.json'))
mods=[{'codigo':'Z00','titulo':'O Universo dos Negócios de Hospedagem','pilar':'Base'}]+d['modulos']
PIL={'Z':'Base da formação','D':'Pilar D · Desenvolver','F':'Pilar F · Financiar','E':'Pilar E · Implantar','M':'Pilar M · Marca e Experiência','L':'Pilar L · Vender','G':'Pilar G · Gerir','O':'Pilar O · Operar'}
def title_html(t):
    w=t.split(' '); 
    if len(w)<=2: return html.escape(t)
    k=max(1,len(w)-2) if len(w)>3 else len(w)-1
    # emphasize last word(s) after split
    a=' '.join(w[:k]); b=' '.join(w[k:])
    return html.escape(a)+' <em>'+html.escape(b)+'</em>'
def page(m,W,H,vert):
    num=m['codigo'][1:]; pil=PIL[m['codigo'][0]]
    giant=int(H*0.95) if not vert else int(W*0.95)
    tsize= (62 if len(m['titulo'])<40 else 52) if not vert else (64 if len(m['titulo'])<40 else 54)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:#1B2117;color:#FEF5F0;font-family:Aventa,sans-serif;position:relative;overflow:hidden;font-variant-numeric:lining-nums;font-feature-settings:"lnum" 1}}
.c,h1,.g{{font-variant-numeric:lining-nums;font-feature-settings:"lnum" 1}}
.g{{position:absolute;right:{-int(W*0.03)}px;bottom:{-int(giant*0.22)}px;font:400 {giant}px/1 'Playfair Display',serif;color:#C9A84C;opacity:.13;letter-spacing:-.02em}}
.w{{position:absolute;left:{int(W*0.07)}px;right:{int(W*0.07)}px;top:{int(H*0.11)}px}}
.k{{font-size:{15 if not vert else 17}px;letter-spacing:.24em;text-transform:uppercase;color:#C9A84C;font-weight:700}}
.k span{{display:block;color:#FEF5F0;opacity:.75;margin-top:10px;letter-spacing:.18em;font-weight:400}}
.c{{margin-top:{int(H*0.08) if not vert else int(H*0.18)}px;font:700 {int(tsize*0.42)}px Aventa,sans-serif;color:#C9A84C;letter-spacing:.14em}}
h1{{margin-top:14px;font:400 {tsize}px/1.08 'Playfair Display',serif;max-width:{int(W*0.8) if not vert else int(W*0.86)}px}}
h1 em{{font-style:italic;color:#C9A84C}}
.r{{width:90px;height:2px;background:#C9A84C;margin-top:28px}}
.f{{position:absolute;left:{int(W*0.07)}px;bottom:{int(H*0.08)}px;font-size:{14 if not vert else 16}px;letter-spacing:.2em;text-transform:uppercase;opacity:.8}}
</style></head><body><div class="g">{num}</div><div class="w"><div class="k">Zion Hospitality Business School<span>Mentoria Zion 360° · {html.escape(pil)}</span></div>
<div class="c">{m['codigo']}</div><h1>{title_html(m['titulo'])}</h1><div class="r"></div></div>
<div class="f">Da Ideia ao Negócio. Da Hospedagem ao Destino.</div></body></html>'''
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for vert,(W,H),suf in [(False,(1280,720),'h'),(True,(800,1200),'v')]:
      pg=await b.new_page(viewport={'width':W,'height':H})
      for m in mods:
        await pg.set_content(page(m,W,H,vert)); await pg.wait_for_timeout(120)
        await pg.screenshot(path=R+f"docs/escola/capas/{m['codigo'].lower()}-{suf}.png")
      await pg.close()
    await b.close()
import os; os.makedirs(R+'docs/escola/capas',exist_ok=True)
asyncio.run(main()); print(len(mods))
