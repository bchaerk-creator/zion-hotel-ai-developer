"""Uso: python3 make_trailer.py <spec.json> <saida.mp4>  (vertical 1080x1920, narração edge-tts)"""
import json, sys, os, subprocess, asyncio, pathlib, shutil
import edge_tts
spec = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2]); work = out.with_suffix(""); work.mkdir(parents=True, exist_ok=True)
voice = spec.get("voice", "pt-BR-FranciscaNeural"); rate = spec.get("rate", "-2%")
HERE = pathlib.Path(__file__).parent
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip() or 0)
async def tts():
    for i, sc in enumerate(spec["scenes"]):
        mp3 = work / f"s{i:02d}.mp3"
        if not mp3.exists():
            await edge_tts.Communicate(sc["say"], voice, rate=rate, proxy=os.environ.get("HTTPS_PROXY")).save(str(mp3))
        sc["audio_ms"] = int(dur(mp3) * 1000); sc["minMs"] = sc["audio_ms"] + int(sc.get("tail_ms", 700)) + 350
asyncio.run(tts())
rec = work / "rec.json"; json.dump({"scenes": spec["scenes"]}, open(rec, "w"), ensure_ascii=False)
shutil.rmtree(work / "rec", ignore_errors=True)
subprocess.run(["node", str(HERE / "record_v.js"), str(rec), str(work / "rec")], check=True)
TJ = json.load(open(work / "rec" / "timings.json")); tim = TJ["scenes"]; VID = TJ["video"]
parts = []
for t, sc in zip(tim, spec["scenes"]):
    i = t["i"]; vms = t["ms"]; seg_ms = max(vms, sc["minMs"]); seg = work / f"seg{i:02d}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t['start_ms']/1000:.3f}", "-t", f"{vms/1000:.3f}", "-i", VID, "-i", str(work / f"s{i:02d}.mp3"), "-filter_complex",
        f"[0:v]scale=1080:1920,fps=30,tpad=stop_mode=clone:stop_duration={max(0,(seg_ms-vms)/1000):.2f},setpts=PTS-STARTPTS[v];[1:a]adelay=350|350,apad,atrim=0:{seg_ms/1000:.2f},asetpts=PTS-STARTPTS[a]",
        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "1", str(seg)], check=True)
    parts.append(seg)
lst = work / "list.txt"; lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
print("pronto:", out, f"{dur(out):.1f}s", f"{out.stat().st_size/1e6:.1f} MB")
