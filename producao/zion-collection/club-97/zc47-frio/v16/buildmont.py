import subprocess,os
C=os.path.dirname(os.path.abspath(__file__)); d9=C+'/clip_d9fc.mp4'; f3=C+'/clip_3f48.mp4'; MU=C+'/music16.wav'
# narrativa: deck (A2) -> bubble completa (A1) -> experiência (A3) -> chamada (investir em experiências, seja investidor, junte-se a uma marca)
seg=[(d9,0.15,10.6,'t2'),(d9,22.6,32.45,'t1'),(d9,32.55,42.25,'t3'),(f3,24.95,32.45,None),(f3,32.6,39.45,None),(f3,0.05,6.9,None)]
pills=[('ref',2.72,0),('deck',5.12,0),('bub',8.0,0),('cama',25.6,1),('deco',26.24,1),('banh',27.92,1),('jac',29.6,1),('hot',30.48,1),('exp',35.52,2),('nat',36.96,2),('loc',38.64,2)]
CARD=4.0
ins=[];fc=[];t=0;offs=[]
for i,(src,a,b,_) in enumerate(seg):
    d=b-a;ins+=['-ss',str(a),'-t',str(d),'-i',src];offs.append(t)
    fc.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=30,format=yuv420p,trim=0:{d},setpts=PTS-STARTPTS[v{i}]")
    fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{d},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={d-0.05}:d=0.05[a{i}]");t+=d
n=len(seg);ins+=['-loop','1','-t',str(CARD),'-i',C+'/a_card.png']
fc.append(f"[{n}:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p,fade=t=in:d=0.4[v{n}]");fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{CARD}[a{n}]")
T=t+CARD;fc.append(''.join(f'[v{i}][a{i}]' for i in range(n+1))+f"concat=n={n+1}:v=1:a=1[vc][ac]")
ov=[('tag',0,t)]
for i,(src,a,b,ti) in enumerate(seg):
    if ti: ov.append((ti,offs[i]+0.2,offs[i]+(b-a)-0.1))
for j,(p,s,si) in enumerate(pills):
    s0=offs[si]+s-seg[si][1]; nxt=pills[j+1] if j+1<len(pills) and pills[j+1][2]==si else None
    e0=offs[si]+nxt[1]-seg[si][1] if nxt else min(s0+2.2,offs[si]+seg[si][2]-seg[si][1]-0.1)
    ov.append(('p_'+p,s0,min(e0,s0+2.2)))
ov.append(('strip',offs[3],t))
k=n+1;prev='vc'
for j,(nm,s,e) in enumerate(ov):
    ins+=['-loop','1','-t',str(T),'-i',C+f'/a_{nm}.png']
    fc.append(f"[{k}:v]format=rgba,fade=t=in:st={s:.2f}:d=0.25:alpha=1,fade=t=out:st={max(s,e-0.25):.2f}:d=0.25:alpha=1[o{j}]")
    fc.append(f"[{prev}][o{j}]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[w{j}]");prev=f'w{j}';k+=1
ins+=['-i',MU]
fc.append(f"[ac]asplit=2[vo][sc];[{k}:a]volume=-13dB,afade=t=out:st={T-1.5}:d=1.5[m];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];[vo][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[au]")
out=C+'/cortes/ZION-M1-montagem-atributos.mp4'
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fc),'-map',f'[{prev}]','-map','[au]','-t',str(T),'-c:v','libx264','-crf','24','-preset','medium','-c:a','aac','-b:a','128k','-movflags','+faststart',out],check=True)
print(round(T,1))
