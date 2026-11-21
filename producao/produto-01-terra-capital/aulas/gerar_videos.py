"""Gera os 20 vídeos narrados das microaulas (1280x720, voz sintética pt-BR, texto na tela, tela real da ferramenta).
Uso (python com edge-tts instalado): python aulas/gerar_videos.py   -> aulas/dist/aula-NN.mp4
Voz: pt-BR-AntonioNeural (mesma do anúncio; licença comercial a confirmar). Trocar por gravação humana quando houver."""
import asyncio, json, os, pathlib, re, ssl, subprocess, sys
A = pathlib.Path(__file__).resolve().parent; P = A.parent; W = A/".work"; D = A/"dist"; W.mkdir(exist_ok=True); D.mkdir(exist_ok=True)
J = json.load(open(P/"src/aulas.json")); PIL = {p["n"]: p["nome"] for p in J["pilares"]}
def falar(t):  # texto para a voz: valores por extenso o suficiente para a leitura sair certa
    t = re.sub(r"R\$\s?(\d+(?:[.,]\d+)?) mil", r"\1 mil reais", t); t = re.sub(r"R\$\s?(\d+(?:\.\d{3})*)", r"\1 reais", t)
    return t.replace("CAPEX", "cápex").replace("CET", "C.E.T.").replace("SAC", "sác").replace("Fungetur", "Fungetúr").replace("CVM", "C.V.M.").replace(";", ",")
segs = []
for a in J["aulas"]:
    fr = [x for x in re.split(r"(?<=[.;])\s+", a["texto"]) if x]; cards = [" ".join(fr[i:i+2]) for i in range(0, len(fr), 2)]
    s = [dict(tipo="abre", tela=a["pergunta"], sub=a["titulo"], voz=f'Aula {a["n"]}. {a["titulo"]}. {a["pergunta"]}')]
    s += [dict(tipo="card", n=i+1, tela=c, voz=falar(c)) for i, c in enumerate(cards)]
    s.append(dict(tipo="tarefa", tela=a["acao"], ferramenta=a["ferramenta"], voz="Agora, coloque em prática. " + falar(a["acao"])))
    for k, x in enumerate(s): x.update(aula=a["n"], k=k, pilar=a["pilar"], pnome=PIL[a["pilar"]])
    segs += s
json.dump(segs, open(W/"segs.json", "w"), ensure_ascii=False)
async def tts():
    import aiohttp, edge_tts
    sem = asyncio.Semaphore(4)
    async def um(x):
        f = W/f'a{x["aula"]:02d}_{x["k"]}.mp3'
        if f.exists() and f.stat().st_size > 2000: return
        async with sem:
            for tent in range(4):
                try:
                    conn = aiohttp.TCPConnector(ssl=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt"))
                    await edge_tts.Communicate(x["voz"], "pt-BR-AntonioNeural", proxy=os.environ.get("HTTPS_PROXY"), connector=conn).save(str(f)); return
                except Exception as e:
                    await asyncio.sleep(2 + tent * 3)
            raise SystemExit(f"TTS falhou: aula {x['aula']} seg {x['k']}")
    await asyncio.gather(*[um(x) for x in segs])
asyncio.run(tts()); print("voz ok:", len(segs), "trechos")
subprocess.run(["node", str(A/"render_slides_aulas.js")], check=True)
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]).decode())
rel = []
for a in J["aulas"]:
    ss = [x for x in segs if x["aula"] == a["n"]]; ins = []; fil = []; t = 0
    for i, x in enumerate(ss):
        mp3 = W/f'a{x["aula"]:02d}_{x["k"]}.mp3'; d = dur(mp3) + (1.2 if x["tipo"] == "tarefa" else 0.45)
        ins += ["-loop", "1", "-t", f"{d:.3f}", "-i", str(W/f'a{x["aula"]:02d}_{x["k"]}.png'), "-i", str(mp3)]
        fil.append(f"[{2*i}:v]fps=25,format=yuv420p[v{i}];[{2*i+1}:a]aresample=44100,apad=whole_dur={d:.3f},atrim=0:{d:.3f}[a{i}]"); t += d
    cat = "".join(f"[v{i}][a{i}]" for i in range(len(ss))) + f"concat=n={len(ss)}:v=1:a=1[v][a0];[a0]loudnorm=I=-16:TP=-1.5:LRA=7[a]"
    out = D/f'aula-{a["n"]:02d}.mp4'
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(fil) + ";" + cat, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-tune", "stillimage", "-crf", "24", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out)], check=True)
    rel.append((a["n"], round(dur(out), 1), out.stat().st_size // 1024))
print("\n".join(f"aula {n:02d}: {d}s {k} KB" for n, d, k in rel)); print("total:", round(sum(d for _, d, _ in rel) / 60, 1), "min")
