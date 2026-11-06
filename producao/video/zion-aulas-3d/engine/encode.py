# Junta quadros + voz + efeitos e gera o MP4 final. Uso: python3 engine/encode.py <pasta_da_aula> "<Título do arquivo>"
import sys, os, subprocess
D, NAME = sys.argv[1], sys.argv[2]; n = len([f for f in os.listdir(D+"/out") if f.endswith(".jpg")]); T = round(n/30, 2)
os.makedirs(D+"/saida", exist_ok=True); out = f"{D}/saida/{NAME}.mp4"
subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",D+"/out/%05d.jpg","-i",D+"/voice.wav","-i",D+"/sfx.wav","-filter_complex",
 f"[2:a]aresample=48000,aformat=channel_layouts=stereo[s];[1:a][s]amix=inputs=2:normalize=0,apad,loudnorm=I=-16:TP=-1.5:LRA=11,atrim=0:{T}[a]",
 "-map","0:v","-map","[a]","-c:v","libx264","-crf","19","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",out], check=True)
print(out, T)
