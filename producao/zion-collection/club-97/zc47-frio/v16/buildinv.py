import subprocess,os
C=os.path.dirname(os.path.abspath(__file__)); S=C+'/..'
V15='/root/.claude/uploads/89510a0c-77b8-5d1e-a647-5c320f6806ef/85a7e38f-V15_preview_720p.mp4'
d9=C+'/clip_d9fc.mp4'; f3=C+'/clip_3f48.mp4'; MU=C+'/music16.wav'
b77=S+'/src/IMG_2377.MOV'; b79=S+'/src/IMG_2379.MOV'; b82=S+'/src/IMG_2382.MOV'; n6=S+'/src/n6.mp4'
# (src,a,b,gain,chip)
seg=[(V15,0.0,6.95,1,'i1'),(d9,10.4,15.4,0.35,None),(b77,15.6,20.6,1,'i2'),(n6,52.0,55.0,0,'i2'),
     (b79,41.3,47.95,1,'i3'),(b82,7.85,13.95,1,'i4'),(d9,30.35,42.25,1,'i5'),
     (f3,14.1,17.58,1,'i6'),(f3,19.05,24.5,1,'i6'),(f3,24.95,32.45,1,'i7'),(f3,32.6,39.45,1,'i8'),(f3,0.05,6.9,1,'i8')]
CARD=4.0
ins=[];fc=[];t=0;ov=[]
for i,(src,a,b,g,chip) in enumerate(seg):
    d=b-a;ins+=['-ss',str(a),'-t',str(d),'-i',src]
    fc.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=30,format=yuv420p,trim=0:{d},setpts=PTS-STARTPTS[v{i}]")
    if g>0: fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{d},asetpts=PTS-STARTPTS,volume={g},afade=t=in:d=0.04,afade=t=out:st={d-0.05}:d=0.05[a{i}]")
    else: fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{d}[a{i}]")
    if chip:
        if ov and ov[-1][0]==chip and abs(ov[-1][2]-t)<0.01: ov[-1]=(chip,ov[-1][1],t+d)
        else: ov.append((chip,t+0.25,t+d))
    t+=d
n=len(seg);ins+=['-loop','1','-t',str(CARD),'-i',C+'/v_card.png']
fc.append(f"[{n}:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p,fade=t=in:d=0.4[v{n}]");fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{CARD}[a{n}]")
T=t+CARD;fc.append(''.join(f'[v{i}][a{i}]' for i in range(n+1))+f"concat=n={n+1}:v=1:a=1[vc][ac]")
ov.insert(0,('tag',0,t))
k=n+1;prev='vc'
for j,(nm,s,e) in enumerate(ov):
    f=C+('/a_tag.png' if nm=='tag' else f'/v_{nm}.png')
    ins+=['-loop','1','-t',str(T),'-i',f]
    fc.append(f"[{k}:v]format=rgba,fade=t=in:st={s:.2f}:d=0.3:alpha=1,fade=t=out:st={max(s,e-0.3):.2f}:d=0.3:alpha=1[o{j}]")
    fc.append(f"[{prev}][o{j}]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[w{j}]");prev=f'w{j}';k+=1
ins+=['-i',MU]
fc.append(f"[ac]asplit=2[vo][sc];[{k}:a]volume=-12dB,afade=t=out:st={T-1.5}:d=1.5[m];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];[vo][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[au]")
out=C+'/cortes/ZION-INVESTIDOR-marca-e-potencial.mp4'
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fc),'-map',f'[{prev}]','-map','[au]','-t',str(T),'-c:v','libx264','-crf','24','-preset','medium','-c:a','aac','-b:a','128k','-movflags','+faststart',out],check=True)
print(round(T,1),[(o[0],round(o[1],1),round(o[2],1)) for o in ov])
