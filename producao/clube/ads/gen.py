import sys,json
R=sys.argv[1]; OUT=sys.argv[2]
G=f"file://{R}/docs/"
css=f'''<style>@font-face{{font-family:C;src:url(file://{R}/docs/assets/fonts/cormorant.woff2)}}@font-face{{font-family:C;font-style:italic;src:url(file://{R}/docs/assets/fonts/cormorant-italic.woff2)}}@font-face{{font-family:A;src:url(file://{R}/docs/assets/fonts/aventa.woff2)}}
*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1350px;overflow:hidden;position:relative;font-family:A,sans-serif;color:#FEF5F0;background:#1B2117}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,6,5,.25) 0%,rgba(4,6,5,.05) 35%,rgba(4,6,5,.55) 62%,rgba(4,6,5,.92) 100%)}}
.top{{position:absolute;left:64px;right:64px;top:56px;display:flex;justify-content:space-between;font-size:20px;letter-spacing:.3em;text-transform:uppercase;color:rgba(254,245,240,.85)}}
.cap{{position:absolute;left:64px;right:64px;bottom:120px}}.k{{font-size:22px;letter-spacing:.3em;text-transform:uppercase;color:#C9B37E;margin-bottom:18px}}
h1{{font-family:C;font-weight:500;font-size:84px;line-height:1.02}}h1 em{{font-style:italic;color:#C9B37E}}
p{{font-size:28px;line-height:1.4;color:rgba(254,245,240,.88);margin-top:18px}}
.list{{margin-top:22px;display:grid;grid-template-columns:230px 1fr;row-gap:12px;font-size:25px}}.list b{{font-family:C;color:#C9B37E;font-weight:500;font-size:28px}}
.btn{{display:inline-block;margin-top:26px;background:#C9B37E;color:#1B2117;font-weight:600;font-size:28px;padding:18px 34px;border-radius:12px}}
.foot{{position:absolute;left:64px;right:64px;bottom:50px;font-size:17px;color:rgba(254,245,240,.6)}}</style>'''
cards=json.load(open(sys.argv[3],encoding='utf-8'))
for i,c in enumerate(cards):
    body=f'<div class="bg" style="background-image:url({G}{c["img"]})"></div><div class="sh"></div><div class="top"><span>{c["brand"]}</span><span>{i+1}/{len(cards)}</span></div><div class="cap"><div class="k">{c["k"]}</div><h1>{c["h"]}</h1>'
    if c.get("p"): body+=f'<p>{c["p"]}</p>'
    if c.get("list"): body+='<div class="list">'+''.join(f'<b>{a}</b><span>{b}</span>' for a,b in c["list"])+'</div>'
    if c.get("btn"): body+=f'<span class="btn">{c["btn"]}</span>'
    body+=f'</div><div class="foot">{c.get("foot","A Zion avalia cada caso. Parcerias e investimentos são possíveis caminhos, sem garantia.")}</div>'
    open(f"{OUT}/c{i+1}.html","w",encoding="utf-8").write("<!doctype html><html><head><meta charset=utf-8>"+css+"</head><body>"+body+"</body></html>")
print("ok",len(cards))
