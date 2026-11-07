# Gera um WAV por trecho de narração com Piper. Uso: python tts.py roteiro.json pasta_saida modelo.onnx piper_bin
import json, sys, os, subprocess, wave
rot, out, model, piper = sys.argv[1:5]
os.makedirs(out, exist_ok=True); dur = {}
for seg in json.load(open(rot, encoding="utf-8"))["segments"]:
    p = f"{out}/{seg['id']}.wav"
    subprocess.run([piper, "-m", model, "-f", p, "--length-scale", "1.0", "--sentence-silence", "0.25"], input=seg["say"].encode("utf-8"), check=True, capture_output=True)
    with wave.open(p) as w: dur[seg["id"]] = w.getnframes() / w.getframerate()
json.dump(dur, open(f"{out}/duracoes.json", "w"), indent=1)
print("ok", len(dur), "trechos", round(sum(dur.values()), 1), "s")
