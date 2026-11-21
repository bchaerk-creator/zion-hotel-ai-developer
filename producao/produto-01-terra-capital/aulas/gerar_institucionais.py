"""Vídeos de boas-vindas e de encerramento (1280x720, voz sintética, terceira pessoa: a voz NÃO se apresenta como Bruno).
Uso: python aulas/gerar_institucionais.py -> aulas/dist/boas-vindas.mp4 e encerramento.mp4"""
import asyncio, json, os, pathlib, ssl, subprocess
A = pathlib.Path(__file__).resolve().parent; P = A.parent; R = P.parents[1]; W = A/".work"; D = A/"dist"; W.mkdir(exist_ok=True)
V = {"boas-vindas": [
  ("Boas-vindas à Zion Hotel Academy.", "Boas-vindas à Zion Hotel Academy.", "titulo", None),
  ("A Zion Hotel Group International é um grupo de desenvolvimento hoteleiro, fundado por Bruno Chaerk.", None, "foto", "docs/assets/bruno/palco-azul.webp|Bruno Chaerk, founder e CEO"),
  ("Se você tem um terreno e não tem capital para investir, esta jornada foi feita para você.", None, "texto", None),
  ("Aqui você aprende o passo a passo para organizar o seu projeto: quanto falta, o que precisa estar documentado, que caminhos existem para completar o capital e como apresentar tudo com clareza.", "Você aprende o passo a passo para organizar o projeto: quanto falta, o que documentar, que caminhos existem e como apresentar.", "foto", "docs/assets/operacoes/op09.webp|Foto real · Zion Bubble Glamping"),
  ("A Zion está em plena expansão e abre a oportunidade de estruturar projetos, e também a possibilidade de criar investimentos e parcerias.", None, "texto", None),
  ("Cada aula tem cerca de um minuto e uma tarefa curta, com a ferramenta aberta logo abaixo. Comece pela aula um.", "Cada aula tem cerca de um minuto e uma tarefa curta. Comece pela aula 1.", "texto", None)],
 "encerramento": [
  ("Você chegou ao fim da jornada.", None, "titulo", None),
  ("Agora você tem uma lacuna de capital calculada, um cenário ruim testado, um checklist com pendências visíveis e um dossiê preliminar.", None, "texto", None),
  ("O próximo passo é levar esse material a um advogado, a um contador e, quando estiver claro, a possíveis parceiros.", None, "texto", None),
  ("Revise o seu plano todo mês. O patrimônio é um ponto de partida. O projeto precisa mostrar demanda, viabilidade e capacidade de execução.", None, "foto", "docs/assets/operacoes/op09.webp|Foto real · Zion Bubble Glamping"),
  ("Obrigado por fazer este caminho com a Zion.", None, "titulo", None)]}
segs = [dict(v=v, k=k, voz=s[0], tela=s[1] or s[0], tipo=s[2], img=s[3]) for v, ss in V.items() for k, s in enumerate(ss)]
json.dump(dict(segs=segs, R=str(R)), open(W/"inst.json", "w"), ensure_ascii=False)
async def tts():
    import aiohttp, edge_tts
    for x in segs:
        f = W/f'{x["v"]}_{x["k"]}.mp3'
        if f.exists() and f.stat().st_size > 2000: continue
        for t in range(4):
            try:
                c = aiohttp.TCPConnector(ssl=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt"))
                await edge_tts.Communicate(x["voz"], "pt-BR-AntonioNeural", proxy=os.environ.get("HTTPS_PROXY"), connector=c).save(str(f)); break
            except Exception: await asyncio.sleep(3 + 3 * t)
        else: raise SystemExit("TTS falhou")
asyncio.run(tts())
subprocess.run(["node", str(A/"render_slides_inst.js")], check=True)
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]).decode())
for v in V:
    ss = [x for x in segs if x["v"] == v]; ins = []; fil = []
    for i, x in enumerate(ss):
        mp3 = W/f'{v}_{x["k"]}.mp3'; d = dur(mp3) + (1.2 if i == len(ss) - 1 else 0.5)
        ins += ["-loop", "1", "-t", f"{d:.3f}", "-i", str(W/f'{v}_{x["k"]}.png'), "-i", str(mp3)]
        fil.append(f"[{2*i}:v]fps=25,format=yuv420p[v{i}];[{2*i+1}:a]aresample=44100,apad=whole_dur={d:.3f},atrim=0:{d:.3f}[a{i}]")
    cat = "".join(f"[v{i}][a{i}]" for i in range(len(ss))) + f"concat=n={len(ss)}:v=1:a=1[v][a0];[a0]loudnorm=I=-16:TP=-1.5:LRA=7[a]"
    out = D/f"{v}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(fil) + ";" + cat, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-tune", "stillimage", "-crf", "24", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out)], check=True)
    print(v, round(dur(out), 1), "s", out.stat().st_size // 1024, "KB")
