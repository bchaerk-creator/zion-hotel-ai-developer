import json, subprocess, numpy as np
from PIL import Image
W,H,FPS=1080,1920,30
sc=json.load(open('scenes.json')); LAB='../lab/'
D=[3.4,2.6,2.6,2.6,2.6,2.8,2.6]; T=0.5; END=4.8
starts=[0.0]
for i in range(1,len(D)): starts.append(starts[-1]+D[i-1]-T)
end_start=starts[-1]+D[-1]-T; total=end_start+END
print('inicio das cenas',[round(x,2) for x in starts],'quadro final',round(end_start,2),'total',round(total,2))
src=[Image.open(LAB+s['jpg']).convert('RGB') for s in sc]
ovl=[np.asarray(Image.open(f'ov{i}.png').convert('RGBA'),dtype=np.float32)/255 for i in range(len(sc))]
stat=np.asarray(Image.open('static.png').convert('RGBA'),dtype=np.float32)/255
endimg=np.asarray(Image.open('end.png').convert('RGB'),dtype=np.float32)
def photo(i,t):  # t em segundos desde o inicio da cena
    im=src[i]; w,h=im.size; r=w/h
    if r>9/16: cw,ch=h*9/16,h
    else: cw,ch=w,w*16/9
    p=min(max(t/(D[i]+T),0),1); z=1.0+0.10*p
    cw/=z; ch/=z
    fx=sc[i]['fx']; cx=(w-cw)*fx+ (0.0 if i%2==0 else 0) ; cy=(h-ch)*(0.5-0.06*p if i%2==0 else 0.45+0.04*p)
    out=im.resize((W,H),Image.LANCZOS,box=(cx,cy,cx+cw,cy+ch))
    return np.asarray(out,dtype=np.float32)
def fade(t,a,b,c,d):  # sobe a->b, desce c->d
    if t<=a or t>=d: return 0.0
    if t<b: return (t-a)/(b-a)
    if t<=c: return 1.0
    return (d-t)/(d-c)
cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i','music.wav',
 '-af','loudnorm=I=-16:TP=-1.5:LRA=7','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart','reels.mp4']
pr=subprocess.Popen(cmd,stdin=subprocess.PIPE)
nf=int(total*FPS)
for f in range(nf):
    t=f/FPS
    # cena ativa(s)
    frame=None
    act=[i for i in range(len(sc)) if starts[i]<=t<starts[i]+D[i]]
    if not act: act=[len(sc)-1]
    cur=act[-1]
    base=photo(cur,t-starts[cur])
    if len(act)==2:
        a,b=act; alpha=min(1,(t-starts[b])/T)
        base=photo(a,t-starts[a])*(1-alpha)+photo(b,t-starts[b])*alpha
    # gradiente+logo
    ea=min(1,max(0,(t-end_start)/T)) if t>=end_start else 0.0
    sa=stat[...,3:4]*(1-ea)
    base=base*(1-sa)+stat[...,:3]*255*sa
    # texto das cenas
    for i in range(len(sc)):
        ts=t-starts[i]
        a=fade(ts,0.35,0.75,D[i]-0.55,D[i]-0.15)
        if a>0:
            oa=ovl[i][...,3:4]*a; base=base*(1-oa)+ovl[i][...,:3]*255*oa
    if t>=end_start:
        base=base*(1-ea)+endimg*ea
    pr.stdin.write(np.clip(base,0,255).astype(np.uint8).tobytes())
pr.stdin.close(); pr.wait(); print('frames',nf,'ok')
