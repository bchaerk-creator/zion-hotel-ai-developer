import json,os,re,shutil,sys
S=os.path.abspath('..'); R=S+'/reels'; LAB=S+'/lab/'
d=json.load(open(LAB+'final_cards.json'))
base=open(R+'/ov0.html').read()
def ital(t):
    return t
for k in sys.argv[1:]:
    v=d[k]; out=f'c{k}'; os.makedirs(out,exist_ok=True)
    for f in ['aventa.woff2','cormorant-italic.woff2','cormorant.woff2','logo.png','static.html','end.html','music.wav','render.py','shot.js']:
        shutil.copy(R+'/'+f,out+'/'+f)
    pairs=[(o,t) for o,t in zip(v['order'],v['titles']) if t.lower() not in('reserve agora',) and 'zion' not in t.lower()[:0]]
    pairs=pairs[:6]
    sc=[]
    for i,(o,t) in enumerate(pairs):
        words=t.split()
        if len(t)>24:
            m=len(words)//2; t=' '.join(words[:m])+'<br>'+' '.join(words[m:])
        html=re.sub(r'<div class=t>.*?</div>',f'<div class=t>{t}</div>',base,flags=re.S)
        open(f'{out}/ov{i}.html','w').write(html)
        sc.append({'jpg':f'jpg/{o}.jpg','fx':0.5,'text':t})
    json.dump(sc,open(f'{out}/scenes.json','w'),ensure_ascii=False)
    s=open(out+'/shot.js').read().replace('Array(7)',f'Array({len(sc)})'); open(out+'/shot.js','w').write(s)
    r=open(out+'/render.py').read()
    r=r.replace("D=[3.4,2.6,2.6,2.6,2.6,2.8,2.6]",f"D=[3.4]+[2.6]*{len(sc)-2}+[2.8]").replace("'reels.mp4'","'out.mp4'").replace("LAB='../lab/'","LAB='../../lab/'")
    open(out+'/render.py','w').write(r)
    print(k,[p[0] for p in pairs])
