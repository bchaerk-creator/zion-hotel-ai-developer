import numpy as np, wave, sys
sr=44100; dur=float(sys.argv[1]); n=int(sr*dur); t=np.arange(n)/sr
rng=np.random.default_rng(7)
def hz(m): return 440*2**((m-69)/12)
chords=[[57,60,64,69],[53,57,60,65],[48,55,60,64],[55,59,62,67]]  # Am F C G
L=np.zeros(n);R=np.zeros(n)
seg=6.0
for i in range(int(dur//seg)+1):
    ch=chords[i%4]; s=int(i*seg*sr); e=min(n,int((i+1)*seg*sr+1.5*sr)); tt=np.arange(e-s)/sr
    env=np.minimum(1,tt/1.6)*np.exp(-np.maximum(0,tt-seg)*1.8)
    for m in ch:
        for dt,pan in ((-0.25,-0.5),(0.25,0.5)):
            f=hz(m-12)*2**(dt/100)
            w=np.sin(2*np.pi*f*tt)+0.35*np.sin(2*np.pi*2*f*tt)+0.12*np.sin(2*np.pi*3*f*tt)
            lfo=0.85+0.15*np.sin(2*np.pi*0.18*tt+m)
            sig=0.05*w*env*lfo
            L[s:e]+=sig*(1-pan)/2*1.2; R[s:e]+=sig*(1+pan)/2*1.2
# arpejo suave
beat=60/72*0.5
k=0
while k*beat<dur:
    ch=chords[int((k*beat)//seg)%4]; m=ch[[1,2,3,2,1,3,2,0][k%8]]+12
    st=int(k*beat*sr); ln=int(1.4*sr); e=min(n,st+ln); tt=np.arange(e-st)/sr
    f=hz(m); w=np.sin(2*np.pi*f*tt)+0.25*np.sin(2*np.pi*2*f*tt)
    env=(1-np.exp(-tt*80))*np.exp(-tt*3.2); sig=0.07*w*env
    pan=0.5+0.35*np.sin(k*1.7); L[st:e]+=sig*(1-pan); R[st:e]+=sig*pan; k+=1
# reverb
def tail(sd):
    r=np.random.default_rng(sd); m=int(2.2*sr); x=r.standard_normal(m)*np.exp(-np.arange(m)/sr*2.4); return x/np.sqrt((x**2).sum())
from numpy.fft import rfft, irfft
def conv(x,h):
    N=len(x)+len(h); X=rfft(x,N); H=rfft(h,N); return irfft(X*H,N)[:len(x)]
wl=conv(L,tail(1))*0.9+L*0.6; wr=conv(R,tail(2))*0.9+R*0.6
fi=np.minimum(1,t/1.2); fo=np.minimum(1,np.maximum(0,(dur-t)/2.2)); g=fi*fo
wl*=g; wr*=g
pk=max(abs(wl).max(),abs(wr).max()); wl/=pk; wr/=pk; wl*=0.6; wr*=0.6
a=np.stack([wl,wr],1); a=(a*32767).astype(np.int16)
with wave.open('music.wav','w') as f: f.setnchannels(2); f.setsampwidth(2); f.setframerate(sr); f.writeframes(a.tobytes())
print('music ok',dur)
