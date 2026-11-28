import subprocess,json,os
S=os.path.dirname(os.path.abspath(__file__))+'/..'
U='/root/.claude/uploads/89510a0c-77b8-5d1e-a647-5c320f6806ef/85a7e38f-V15_preview_720p.mp4'
d9=S+'/cam/clip_d9fc.mp4'; f3=S+'/cam/clip_3f48.mp4'; b82=S+'/src/IMG_2382.MOV'; b79=S+'/src/IMG_2379.MOV'; n6=S+'/src/n6.mp4'
# (src, a, b, audio_gain, label)
seg=[(U,0.0,6.95,1,'emo_open'),(d9,10.4,17.0,0.35,'emo'),(b82,7.85,13.95,1,'exp1'),(n6,52.0,55.5,0,'exp_aer'),(b79,41.3,47.95,1,'exp2'),
     (d9,0.15,10.6,1,'mod1'),(d9,22.6,42.25,1,'mod2'),(f3,14.1,17.58,1,'eco1'),(f3,19.05,24.5,1,'eco2'),(f3,24.95,32.45,1,'eco3'),
     (f3,32.6,39.45,1,'inv'),(f3,0.05,6.9,1,'cta1'),(f3,39.6,44.6,0.35,'cta2')]
CARD=4.5
ins=[];fc=[];t=0;times={}
for i,(src,a,b,g,lab) in enumerate(seg):
    d=b-a; ins+=['-ss',str(a),'-t',str(d),'-i',src]
    fc.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=30,format=yuv420p,trim=0:{d},setpts=PTS-STARTPTS[v{i}]")
    if g>0: fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{d},asetpts=PTS-STARTPTS,volume={g},afade=t=in:d=0.04,afade=t=out:st={d-0.05}:d=0.05[a{i}]")
    else: fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{d}[a{i}]")
    times[lab]=(t,t+d); t+=d
n=len(seg); ci=n
ins+=['-loop','1','-t',str(CARD),'-i',S+'/cam/o_card.png']
fc.append(f"[{ci}:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p,fade=t=in:d=0.5[v{ci}]"); fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{CARD}[a{ci}]")
times['card']=(t,t+CARD); T=t+CARD
fc.append(''.join(f'[v{i}][a{i}]' for i in range(n+1))+f"concat=n={n+1}:v=1:a=1[vc][ac]")
ov={'tag':(0,times['cta2'][1]),'emo':(times['emo'][0]+0.3,times['emo'][1]),'exp':(times['exp_aer'][0],times['exp_aer'][1]+0.2),
    'mod':(times['mod1'][0]+5.4,times['mod1'][1]),'eco':(times['eco1'][0],times['eco2'][1]),'strip':(times['eco1'][0],times['cta2'][1]),'cta':(times['cta2'][0]+0.2,times['cta2'][1])}
k=n+1;prev='vc'
for j,(name,(s,e)) in enumerate(ov.items()):
    ins+=['-loop','1','-t',str(T),'-i',S+f'/cam/o_{name}.png']
    fc.append(f"[{k}:v]format=rgba,fade=t=in:st={s}:d=0.35:alpha=1,fade=t=out:st={e-0.35}:d=0.35:alpha=1[o{j}]")
    fc.append(f"[{prev}][o{j}]overlay=0:0:enable='between(t,{s},{e})'[w{j}]"); prev=f'w{j}'; k+=1
mu=S+'/cam/music16.wav'
ins+=['-i',mu]
fc.append(f"[ac]asplit=2[vo][sc];[{k}:a]volume=-13dB[m];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md];[vo][md]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[au]")
cmd=['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fc),'-map',f'[{prev}]','-map','[au]','-t',str(T),'-c:v','libx264','-crf','22','-preset','medium','-c:a','aac','-b:a','160k','-movflags','+faststart',S+'/cam/zc47-v16b-investidores.mp4']
subprocess.run(cmd,check=True); print(json.dumps({k:[round(a,2),round(b,2)] for k,(a,b) in times.items()}),'total',round(T,2))
