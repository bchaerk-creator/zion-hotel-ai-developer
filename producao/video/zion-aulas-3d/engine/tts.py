# Narração provisória local (voz sintética). Uso: python3 -I engine/tts.py <pasta_da_aula> <pasta_do_modelo_piper>
# Lê <pasta>/script.json [[bloco, cue|null, texto, pausa_depois]]; "[PAUSE n]" cria silêncio de n s (pausas interativas).
# Gera <pasta>/voice.wav (48 kHz estéreo, -16 LUFS) e <pasta>/marks.json {marks, cues, total}.
import sys, json, glob, numpy as np, soundfile as sf, subprocess
D, M = sys.argv[1], sys.argv[2].rstrip('/') + '/'
# O sherpa-onnx 2.0 devolve áudio vazio com os modelos Piper; a voz sai pelo pacote piper (mesmo modelo .onnx).
from piper import PiperVoice, SynthesisConfig
voz = PiperVoice.load(glob.glob(M+"*.onnx")[0])
def gerar(texto, speed=0.95):
    return np.concatenate([c.audio_float_array for c in voz.synthesize(texto, syn_config=SynthesisConfig(length_scale=1/speed))])
segs = json.load(open(D+"/script.json")); t = 0.6; sr = voz.config.sample_rate; pieces = []; cues = {}; marks = []
for fala, cue, text, gap in segs:
    if text.startswith("[PAUSE"):
        dur = float(text.split()[1].rstrip("]")); cues[cue] = round(t, 3); t += dur; continue
    x = gerar(text).astype(np.float32)
    idx = np.where(np.abs(x) > 0.01)[0]; x = x[max(0, idx[0]-150):idx[-1]+300]
    if cue: cues[cue] = round(t, 3)
    marks.append([round(t, 3), round(t+len(x)/sr, 3), text, fala]); pieces.append((t, x)); t += len(x)/sr + gap
T = t + 1.0; buf = np.zeros(int(T*sr)+sr, dtype=np.float32)
for s, x in pieces: i = int(s*sr); buf[i:i+len(x)] += x
sf.write(D+"/voice_raw.wav", buf, sr)
subprocess.run(["ffmpeg","-v","error","-y","-i",D+"/voice_raw.wav","-af","loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000","-ac","2",D+"/voice.wav"], check=True)
json.dump({"marks": marks, "cues": cues, "total": round(T, 3)}, open(D+"/marks.json","w"), ensure_ascii=False, indent=1)
print("total", round(T, 2))
