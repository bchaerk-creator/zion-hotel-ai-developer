# Coloca o vídeo do avatar/apresentador numa bolinha redonda (canto inferior direito, borda dourada) sobre os quadros renderizados.
# Uso: python3 engine/bolinha.py <pasta_da_aula> <video_avatar.mp4> [cx cy]   (cx,cy = centro do rosto no vídeo do avatar, em px)
# Gera <pasta>/out_bolinha/%05d.jpg. Depois use encode.py apontando para essa pasta (ou renomeie) e use o áudio do avatar como voice.wav.
import sys, os, subprocess
from PIL import Image, ImageDraw, ImageFilter
D, V = sys.argv[1], sys.argv[2]; cx, cy = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (None, None)
os.makedirs(D+"/av", exist_ok=True); os.makedirs(D+"/out_bolinha", exist_ok=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",V,"-vf","fps=30","-q:v","2",D+"/av/%05d.jpg"], check=True)
DI = 300; X, Y = 1580, 700
mask = Image.new("L", (DI*2, DI*2), 0); ImageDraw.Draw(mask).ellipse((0,0,DI*2-1,DI*2-1), fill=255); mask = mask.resize((DI,DI), Image.LANCZOS)
ring = Image.new("RGBA", (DI+16, DI+16), (0,0,0,0)); ImageDraw.Draw(ring).ellipse((0,0,DI+15,DI+15), outline=(224,190,94,255), width=6)
sh = Image.new("RGBA", (DI+60, DI+60), (0,0,0,0)); ImageDraw.Draw(sh).ellipse((30,36,DI+30,DI+36), fill=(0,0,0,150)); sh = sh.filter(ImageFilter.GaussianBlur(14))
fr = sorted(os.listdir(D+"/out")); av = sorted(os.listdir(D+"/av"))
for k, f in enumerate(fr):
    bg = Image.open(f"{D}/out/{f}").convert("RGBA")
    if k < len(av):
        a = Image.open(f"{D}/av/{av[k]}").convert("RGB"); w, h = a.size; s = min(w, h)//2
        x0 = (cx if cx else w//2) - s; y0 = (cy if cy else h//3) - s//2
        x0 = max(0, min(w-2*s, x0)); y0 = max(0, min(h-2*s, y0))
        face = a.crop((x0, y0, x0+2*s, y0+2*s)).resize((DI,DI), Image.LANCZOS)
        bg.alpha_composite(sh, (X-30, Y-30)); bg.paste(face, (X, Y), mask); bg.alpha_composite(ring, (X-8, Y-8))
    bg.convert("RGB").save(f"{D}/out_bolinha/{f}", quality=92)
print("ok", len(fr))
