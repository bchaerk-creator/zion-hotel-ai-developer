import json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
import sys
C = sys.argv[1]
SR = 48000
rng = np.random.default_rng(11)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x)
def env(n, a, d):  # attack/decay in seconds
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d); return e
def N(sec): return rng.standard_normal(int(sec * SR))

def key():
    n = int(.07 * SR)
    click = bp(N(.07), 1800, 6500) * env(n, .0005, .006) * 1.2
    thock = bp(N(.07), 150, 900) * env(n, .001, .018) * .9
    f = rng.uniform(.8, 1.2)
    return (click + thock) * f * .5
def shutter():
    out = np.zeros(int(.35 * SR))
    for st, g in [(0, 1), (.075, .8)]:
        i = int(st * SR); n = int(.09 * SR)
        s = bp(N(.09), 1200, 9000) * env(n, .0003, .012) * g
        s += bp(N(.09), 300, 1200) * env(n, .001, .03) * g * .7
        out[i:i + n] += s
    t = np.arange(len(out)) / SR
    out += np.sin(2 * np.pi * 3100 * t) * np.exp(-t / .02) * .08
    return out * .9
def whoosh(dur=.55, soft=False):
    n = int(dur * SR); x = N(dur); t = np.arange(n) / SR
    y = np.zeros(n); seg = 512
    for i in range(0, n, seg):  # sweeping band
        p = i / n; fc = 400 + 3500 * np.sin(np.pi * p)
        y[i:i + seg] = bp(x[max(0, i - 2048):i + seg], fc * .6, fc * 1.5)[-len(x[i:i + seg]):]
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return y * e * (.35 if soft else .6)
def pop():
    n = int(.09 * SR); t = np.arange(n) / SR
    f = 700 * np.exp(-t / .03) + 260
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .025) * .35
def blip():
    n = int(.08 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 980 * t) + .4 * np.sin(2 * np.pi * 1960 * t)) * np.exp(-t / .02) * .18
def tick():
    n = int(.12 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 520 * t) * np.exp(-t / .04) * .3 + bp(N(.12), 2000, 6000) * env(n, .0003, .004) * .3)
def boom():
    n = int(1.2 * SR); t = np.arange(n) / SR
    f = 75 * np.exp(-t / .5) + 38
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .45) * .55

GEN = {"key": key, "shutter": shutter, "whoosh": whoosh, "whoosh_in": lambda: whoosh(.7, True), "pop": pop, "blip": blip, "tick": tick}
voice, vsr = sf.read(C + "/voice.wav"); assert vsr == SR
L = len(voice) + SR
mix = np.zeros(L)
ev = json.load(open(C + "/sfx_all.json"))
GEN["boom"] = boom
seen = set()
for e in ev:
    k = (e["type"], round(e["t"], 2))
    if k in seen: continue
    seen.add(k)
    s = GEN[e["type"]]() * e["vol"]
    i = int(e["t"] * SR); j = min(L, i + len(s)); mix[i:j] += s[:j - i]
print("events", len(seen))
sf.write(C + "/sfx.wav", np.clip(mix, -1, 1), SR)
