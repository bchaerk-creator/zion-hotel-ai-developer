import subprocess,sys,os
C=os.path.dirname(os.path.abspath(__file__)); d9=C+'/clip_d9fc.mp4'; f3=C+'/clip_3f48.mp4'; MU=C+'/music16.wav'
CUTS={
 'A1-bubble-completa':dict(title='t1',seg=[(d9,22.6,32.45),(f3,0.05,6.9)],pills=[('cama',25.6),('deco',26.24),('banh',27.92),('jac',29.6),('hot',30.48)],cta=1),
 'A2-deck-de-madeira':dict(title='t2',seg=[(d9,0.15,10.6),(f3,32.6,39.45)],pills=[('ref',2.72),('deck',5.12),('bub',8.0)],cta=1),
 'A3-experiencia-natureza':dict(title='t3',seg=[(d9,32.55,42.25),(f3,24.95,32.45)],pills=[('exp',35.52),('nat',36.96),('loc',38.64)],cta=1),
 'A4-reservas-marketing':dict(title='t4',seg=[(f3,14.1,17.58),(f3,19.05,24.5),(f3,0.05,6.9)],pills=[('res',20.4),('mkt',20.96),('neg',22.88)],cta=2),
}
CARD=3.8
def build(name,c):
    ins=[];fc=[];t=0;st=[]
    for i,(src,a,b) in enumerate(c['seg']):
        d=b-a;ins+=['-ss',str(a),'-t',str(d),'-i',src];st.append((src,a,b,t))
        fc.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=30,format=yuv420p,trim=0:{d},setpts=PTS-STARTPTS[v{i}]")
        fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{d},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={d-0.05}:d=0.05[a{i}]");t+=d
    n=len(c['seg']);ins+=['-loop','1','-t',str(CARD),'-i',C+'/a_card.png']
    fc.append(f"[{n}:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p,fade=t=in:d=0.4[v{n}]");fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{CARD}[a{n}]")
    T=t+CARD;fc.append(''.join(f'[v{i}][a{i}]' for i in range(n+1))+f"concat=n={n+1}:v=1:a=1[vc][ac]")
    def rel(src_t):  # map source time of first matching segment to output
        for src,a,b,o in st:
            if a<=src_t<=b: return o+src_t-a
    ctaStart=st[-c['cta']][3]
    ov=[('tag',0,t),('title_'+c['title'],0.2,ctaStart)]
    P=c['pills']
    for j,(p,s) in enumerate(P):
        s0=rel(s); e0=rel(P[j+1][1]) if j+1<len(P) else min(s0+2.2,ctaStart)
        ov.append(('p_'+p,s0,min(e0,s0+2.2)))
    ov.append(('strip',ctaStart,t))
    k=n+1;prev='vc'
    for j,(nm,s,e) in enumerate(ov):
        f=C+('/a_'+nm.replace('title_','')+'.png')
        ins+=['-loop','1','-t',str(T),'-i',f]
        fc.append(f"[{k}:v]format=rgba,fade=t=in:st={s:.2f}:d=0.25:alpha=1,fade=t=out:st={max(s,e-0.25):.2f}:d=0.25:alpha=1[o{j}]")
        fc.append(f"[{prev}][o{j}]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[w{j}]");prev=f'w{j}';k+=1
    ins+=['-i',MU]
    fc.append(f"[ac]asplit=2[vo][sc];[{k}:a]volume=-13dB,afade=t=out:st={T-1.5}:d=1.5[m];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];[vo][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[au]")
    out=C+f'/cortes/ZION-{name}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fc),'-map',f'[{prev}]','-map','[au]','-t',str(T),'-vf' if False else '-c:v','libx264','-crf','24','-preset','medium','-c:a','aac','-b:a','128k','-movflags','+faststart',out],check=True)
    print(name,round(T,1))
os.makedirs(C+'/cortes',exist_ok=True)
for k,v in CUTS.items(): build(k,v)
