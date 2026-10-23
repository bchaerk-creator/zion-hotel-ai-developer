#!/usr/bin/env python3
"""Monta o vídeo narrado de uma aula a partir do PDF dos slides e do roteiro.md.

Etapas (rode na pasta da aula):
  python3 aula.py slides aula2-territorio.pdf      # PDF -> slides/NN.png (1920x1080)
  python3 aula.py narrar --teste                   # só o slide 1, para aprovar a voz
  python3 aula.py narrar                           # audio/NN.mp3 para todos os slides
  python3 aula.py montar                           # clipes, blocos, vídeo completo, .srt e relatório

Voz: --motor kokoro (padrão) usa o Kokoro-82M aberto, rodando nesta máquina, voz --voz pm_alex
(ou pm_santa, pf_dora); na primeira vez baixa o modelo para modelos/. --motor elevenlabs usa
ELEVENLABS_API_KEY e --voz <id>. --motor edge usa edge-tts pt-BR-AntonioNeural a -5%.
Se existir demo-ferramenta.mp4, ela entra no slide 48.
"""
import argparse, json, os, re, subprocess, sys, textwrap, urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
FPS, W, H = 30, 1920, 1080
RESPIRO, PAUSA, FADE = 0.8, 6.0, 0.5
SLIDE_DEMO = 48


def sh(*cmd, capture=False):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"Falhou: {' '.join(map(str, cmd))[:300]}\n{r.stderr[-2000:]}")
    return r.stdout if capture else r.stderr


def duracao(arq):
    return float(sh('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', arq, capture=True))


def roteiro():
    slides, bloco = [], None
    texto = (AQUI / 'roteiro.md').read_text(encoding='utf-8')
    for parte in re.split(r'\n(?=### |\*\*\d\d · )', texto):
        m = re.match(r'### Bloco (\d+) · (.+)', parte)
        if m:
            bloco = int(m.group(1))
            continue
        m = re.match(r'\*\*(\d\d) · (.+?)\*\*(.*)\n(.+)', parte, re.S)
        if m:
            slides.append({'n': int(m.group(1)), 'titulo': m.group(2), 'bloco': bloco,
                           'foto': '[FOTO]' in m.group(3), 'pausa': '[PAUSA]' in m.group(3),
                           'texto': ' '.join(m.group(4).split())})
    assert [s['n'] for s in slides] == list(range(1, len(slides) + 1)), 'numeração do roteiro fora de ordem'
    return slides


# ---------- 1. slides ----------
def cmd_slides(a):
    pasta = AQUI / 'slides'
    pasta.mkdir(exist_ok=True)
    sh('pdftoppm', '-png', '-r', '150', '-scale-to-x', W, '-scale-to-y', H, a.pdf, pasta / 's')
    gerados = sorted(pasta.glob('s-*.png'), key=lambda p: int(p.stem.split('-')[1]))
    for p in gerados:
        p.rename(pasta / f"{int(p.stem.split('-')[1]):02d}.png")
    total, esperado = len(gerados), len(roteiro())
    print(f'{total} imagens em slides/')
    if total != esperado:
        sys.exit(f'O PDF tem {total} páginas e o roteiro tem {esperado} slides. Confira antes de seguir.')


# ---------- 2. narração ----------
def falar_elevenlabs(texto, voz, destino):
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{voz}?output_format=mp3_44100_128',
        data=json.dumps({'text': texto, 'model_id': 'eleven_multilingual_v2',
                         'voice_settings': {'stability': 0.5, 'similarity_boost': 0.8}}).encode(),
        headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=180) as r:
        destino.write_bytes(r.read())


def falar_edge(texto, destino):
    import asyncio
    import edge_tts
    asyncio.run(edge_tts.Communicate(texto, 'pt-BR-AntonioNeural', rate='-5%').save(str(destino)))


KOKORO = 'https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-multi-lang-v1_0.tar.bz2'
VOZES_KOKORO = ('af_alloy af_aoede af_bella af_heart af_jessica af_kore af_nicole af_nova af_river af_sarah af_sky '
                'am_adam am_echo am_eric am_fenrir am_liam am_michael am_onyx am_puck am_santa bf_alice bf_emma '
                'bf_isabella bf_lily bm_daniel bm_fable bm_george bm_lewis ef_dora em_alex ff_siwis hf_alpha hf_beta '
                'hm_omega hm_psi if_sara im_nicola jf_alpha jf_gongitsune jf_nezumi jf_tebukuro jm_kumo pf_dora '
                'pm_alex pm_santa zf_xiaobei zf_xiaoni zf_xiaoxiao zf_xiaoyi zm_yunjian zm_yunxi zm_yunxia '
                'zm_yunyang em_santa').split()


def kokoro():
    """Carrega o Kokoro-82M (pip install kokoro-onnx soundfile); baixa o modelo na primeira vez."""
    import numpy as np
    from kokoro_onnx import Kokoro
    pasta = AQUI / 'modelos'
    modelo = pasta / 'kokoro-multi-lang-v1_0'
    if not (modelo / 'model.onnx').exists():
        pasta.mkdir(exist_ok=True)
        print('baixando o modelo Kokoro (cerca de 350 MB)...')
        subprocess.run(f"curl -sSL '{KOKORO}' | tar xj -C '{pasta}'", shell=True, check=True)
    vozes = pasta / 'kokoro-vozes.npz'
    if not vozes.exists():
        v = np.fromfile(modelo / 'voices.bin', dtype=np.float32).reshape(len(VOZES_KOKORO), 510, 1, 256)
        np.savez(vozes, **{n: v[i] for i, n in enumerate(VOZES_KOKORO)})
    return Kokoro(str(modelo / 'model.onnx'), str(vozes))


def falar_kokoro(motor, texto, voz, velocidade, destino):
    import soundfile as sf
    audio, taxa = motor.create(texto, voice=voz, speed=velocidade, lang='pt-br')
    wav = destino.with_suffix('.wav')
    sf.write(wav, audio, taxa)
    sh('ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-b:a', '192k', destino)
    wav.unlink()


def cmd_narrar(a):
    pasta = AQUI / 'audio'
    pasta.mkdir(exist_ok=True)
    if a.motor == 'elevenlabs' and not (os.environ.get('ELEVENLABS_API_KEY') and a.voz):
        sys.exit('ElevenLabs precisa de ELEVENLABS_API_KEY no ambiente e do ID da voz em --voz <id>.')
    voz = a.voz or 'pm_alex'
    motor = kokoro() if a.motor == 'kokoro' else None
    alvo = [s for s in roteiro() if not a.teste or s['n'] == 1]
    for s in alvo:
        destino = pasta / f"{s['n']:02d}.mp3"
        if destino.exists() and not a.refazer:
            continue
        if a.motor == 'kokoro':
            falar_kokoro(motor, s['texto'], voz, a.velocidade, destino)
        elif a.motor == 'elevenlabs':
            falar_elevenlabs(s['texto'], a.voz, destino)
        else:
            falar_edge(s['texto'], destino)
        print(f"{destino.name}  {duracao(destino):6.1f} s  {s['titulo']}")
    print('voz:', {'kokoro': f'Kokoro {voz} velocidade {a.velocidade}', 'elevenlabs': f'ElevenLabs {a.voz}',
                   'edge': 'edge-tts pt-BR-AntonioNeural -5%'}[a.motor])


# ---------- 3. montagem ----------
def normalizar(origem, destino, video=False):
    """Loudnorm em duas passadas: -16 LUFS integrado, pico -1,5 dBTP. Com video=True copia o vídeo."""
    alvo = 'I=-16:TP=-1.5:LRA=11'
    medida = sh('ffmpeg', '-hide_banner', '-i', origem, '-af', f'loudnorm={alvo}:print_format=json', '-f', 'null', '-')
    m = json.loads(medida[medida.rindex('{'):])
    filtro = (f"loudnorm={alvo}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
              f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    extra = ['-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart'] if video else []
    sh('ffmpeg', '-y', '-loglevel', 'error', '-i', origem, '-af', filtro, '-ar', '48000', '-ac', '2', *extra, destino)


def clipe(s, voz, destino):
    fala = duracao(voz)
    demo = AQUI / 'demo-ferramenta.mp4'
    enc = ['-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', FPS,
           '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2']
    if s['n'] == SLIDE_DEMO and demo.exists():
        dur = max(duracao(demo), fala + RESPIRO)
        filtro = (f'[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,'
                  f'setsar=1,fps={FPS},tpad=stop_mode=clone:stop_duration={dur}[v];'
                  f"[0:a]aresample=48000,volume=enable='lt(t,{fala:.3f})':volume=0[d];"
                  f'[1:a][d]amix=inputs=2:normalize=0:duration=longest,apad[a]')
        sh('ffmpeg', '-y', '-loglevel', 'error', '-i', demo, '-i', voz, '-filter_complex', filtro,
           '-map', '[v]', '-map', '[a]', '-t', f'{dur:.3f}', *enc, destino)
        return dur, fala
    dur = fala + RESPIRO + (PAUSA if s['pausa'] else 0)
    quadros = round(dur * FPS)
    if s['foto']:  # Ken Burns de 100% a 104%; escala em 4K antes para o zoom não tremer
        video = (f"scale={W * 2}:{H * 2},zoompan=z='1+0.04*on/{quadros}':d={quadros}:"
                 f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},setsar=1")
    else:
        video = f'scale={W}:{H},setsar=1,fps={FPS}'
    sh('ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', FPS, '-i', AQUI / 'slides' / f"{s['n']:02d}.png",
       '-i', voz, '-filter_complex', f'[0:v]{video}[v];[1:a]apad[a]', '-map', '[v]', '-map', '[a]',
       '-t', f'{dur:.3f}', *enc, destino)
    return dur, fala


def juntar_bloco(clipes, duracoes, destino):
    """Encadeia os clipes com fade de 0,5 s; devolve o início de cada clipe dentro do bloco."""
    entradas, filtros, inicios = [], [], [0.0]
    for c in clipes:
        entradas += ['-i', c]
    v, a, comp = '[0:v]', '[0:a]', duracoes[0]
    for k in range(1, len(clipes)):
        off = comp - FADE
        filtros.append(f'{v}[{k}:v]xfade=transition=fade:duration={FADE}:offset={off:.3f}[v{k}]')
        filtros.append(f'{a}[{k}:a]acrossfade=d={FADE}[a{k}]')
        v, a = f'[v{k}]', f'[a{k}]'
        inicios.append(off)
        comp = off + duracoes[k]
    args = ['-filter_complex', ';'.join(filtros), '-map', v, '-map', a] if filtros else ['-map', '0:v', '-map', '0:a']
    sh('ffmpeg', '-y', '-loglevel', 'error', *entradas, *args,
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', FPS,
       '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', destino)
    return inicios


def legendas(texto, ini, fim):
    """Divide a fala em legendas de até 2 linhas de 42 caracteres, com tempo proporcional ao texto."""
    blocos = []
    for frase in re.split(r'(?<=[.?!:])\s+', texto):
        linhas = textwrap.wrap(frase, 42)
        blocos += ['\n'.join(linhas[i:i + 2]) for i in range(0, len(linhas), 2)]
    total = sum(len(b) for b in blocos)
    saida, t = [], ini
    for b in blocos:
        d = (fim - ini) * len(b) / total
        saida.append((t, t + d, b))
        t += d
    return saida


def tempo_srt(t):
    ms = round(t * 1000)
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'


def cmd_montar(a):
    slides = roteiro()
    faltam = [s['n'] for s in slides if not (AQUI / 'slides' / f"{s['n']:02d}.png").exists()
              or not (AQUI / 'audio' / f"{s['n']:02d}.mp3").exists()]
    if faltam:
        sys.exit(f'Faltam slide ou áudio para: {faltam}')
    for p in ('trabalho/voz', 'trabalho/clipes', 'saida/blocos', 'saida/conferencia'):
        (AQUI / p).mkdir(parents=True, exist_ok=True)

    info = {}
    for s in slides:
        voz = AQUI / 'trabalho/voz' / f"{s['n']:02d}.wav"
        normalizar(AQUI / 'audio' / f"{s['n']:02d}.mp3", voz)
        dur, fala = clipe(s, voz, AQUI / 'trabalho/clipes' / f"{s['n']:02d}.mp4")
        info[s['n']] = {'dur': duracao(AQUI / 'trabalho/clipes' / f"{s['n']:02d}.mp4"), 'fala': fala}
        print(f"clipe {s['n']:02d}  {info[s['n']]['dur']:6.1f} s")

    blocos, srt, inicio_bloco = [], [], 0.0
    for b in sorted({s['bloco'] for s in slides}):
        doBloco = [s for s in slides if s['bloco'] == b]
        destino = AQUI / 'saida/blocos' / f'bloco-{b}.mp4'
        bruto = AQUI / 'trabalho' / f'bloco-{b}.mp4'
        inicios = juntar_bloco([AQUI / 'trabalho/clipes' / f"{s['n']:02d}.mp4" for s in doBloco],
                               [info[s['n']]['dur'] for s in doBloco], bruto)
        normalizar(bruto, destino, video=True)
        for s, i in zip(doBloco, inicios):
            ini = inicio_bloco + i
            srt += legendas(s['texto'], ini, ini + info[s['n']]['fala'])
        d = duracao(destino)
        blocos.append((b, destino, d, doBloco))
        inicio_bloco += d
        print(f'bloco {b}  {d / 60:5.1f} min')

    lista = AQUI / 'trabalho/blocos.txt'
    lista.write_text(''.join(f"file '{d}'\n" for _, d, _, _ in blocos))
    completo = AQUI / 'saida/aula2-territorio-completa.mp4'
    sh('ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lista, '-c', 'copy',
       '-movflags', '+faststart', completo)
    (AQUI / 'saida/aula2-territorio.srt').write_text(
        '\n'.join(f'{i}\n{tempo_srt(a)} --> {tempo_srt(b)}\n{t}\n' for i, (a, b, t) in enumerate(srt, 1)), encoding='utf-8')

    # conferência: 3 quadros dos primeiros 20 s de cada bloco
    for b, destino, d, _ in blocos:
        for t in (min(t, int(d) - 1) for t in (2, 10, 18)):
            sh('ffmpeg', '-y', '-loglevel', 'error', '-ss', t, '-i', destino, '-frames:v', 1, '-vf', 'scale=640:-1',
               AQUI / 'saida/conferencia' / f'bloco-{b}-{t:02d}s.png')

    problemas, rel = [], ['RELATÓRIO · Aula 2 · Território', '']
    for arq in [completo] + [d for _, d, _, _ in blocos]:
        p = json.loads(sh('ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name,width,height,r_frame_rate,sample_rate',
                          '-show_entries', 'format=duration', '-of', 'json', arq, capture=True))
        v = next(s for s in p['streams'] if 'width' in s)
        au = next(s for s in p['streams'] if 'sample_rate' in s)
        linha = (f"{arq.name}: {v['width']}x{v['height']} {v['r_frame_rate']} fps {v['codec_name']} / "
                 f"{au['codec_name']} {au['sample_rate']} Hz / {float(p['format']['duration']) / 60:.2f} min")
        rel.append(linha)
        if (v['width'], v['height'], v['r_frame_rate'], v['codec_name'], au['codec_name'], au['sample_rate']) != (W, H, f'{FPS}/1', 'h264', 'aac', '48000'):
            problemas.append('Formato fora do pedido: ' + linha)
    rel += ['', f'Clipes gerados: {len(info)} de {len(slides)}', '']
    for b, _, d, doBloco in blocos:
        rel.append(f'Bloco {b}: {d / 60:.2f} min')
        for s in doBloco:
            marcas = ' '.join(m for m, ok in (('[FOTO]', s['foto']), ('[PAUSA]', s['pausa'])) if ok)
            rel.append(f"  {s['n']:02d} {s['titulo']:<34} fala {info[s['n']]['fala']:6.1f} s  clipe {info[s['n']]['dur']:6.1f} s  {marcas}")
    rel.append(f'\nTotal: {duracao(completo) / 60:.2f} min')
    if not (AQUI / 'demo-ferramenta.mp4').exists():
        rel.append('Slide 48: sem demo-ferramenta.mp4, usado o slide com narração.')
    if len(info) != len(slides):
        problemas.append('Número de clipes diferente do número de slides.')
    rel += ['', 'Problemas: ' + ('nenhum' if not problemas else ''), *problemas]
    (AQUI / 'saida/relatorio.txt').write_text('\n'.join(rel) + '\n', encoding='utf-8')
    print('\n'.join(rel))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('slides'); p.add_argument('pdf'); p.set_defaults(f=cmd_slides)
    p = sub.add_parser('narrar'); p.add_argument('--voz'); p.add_argument('--teste', action='store_true')
    p.add_argument('--motor', choices=['kokoro', 'elevenlabs', 'edge'], default='kokoro')
    p.add_argument('--velocidade', type=float, default=1.0)
    p.add_argument('--refazer', action='store_true'); p.set_defaults(f=cmd_narrar)
    p = sub.add_parser('montar'); p.set_defaults(f=cmd_montar)
    a = ap.parse_args()
    a.f(a)
