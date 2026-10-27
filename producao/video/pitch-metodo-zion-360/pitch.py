#!/usr/bin/env python3
"""Pitch · Método Zion 360°: dois vídeos (um por bloco) com os slides do PDF, narração e legenda palavra por palavra.

  python3 pitch.py narrar            # audio/SS.wav e audio/SS.json por slide (voz provisória Piper faber)
  python3 pitch.py montar [--video 1]  # saida/<data> - Pitch Bloco N - <título> - Zion.mp4 e .srt

Regras do prompt: troca de slide quando a fala da cena começa; zoom lento de 5% em 6 s; legenda creme com a palavra
falada em dourado no terço inferior; rodapé legal no último quadro do vídeo 2. Sem avatar (a bolinha entra quando
houver o vídeo do avatar falando o mesmo texto) e sem música (não há trilha livre de direitos na pasta).
"""
import argparse, datetime, json, re, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
VOZ = Path('/tmp/claude-0/-home-user-zion-hotel-ai-developer/a14ad55f-1246-5b84-bca0-f41e7f42a881/scratchpad/voz/'
           'vits-piper-pt_BR-faber-medium/pt_BR-faber-medium.onnx')
PRONUNCIA = {'Zion': 'Záion', 'Bubble': 'Bâbol', 'Uber': 'Úber', 'Hotel Cast': 'Hotel Kést'}
FPS, FADE, RESPIRO_FRASE, FIM_CENA = 30, 0.4, 0.32, 0.55
RODAPE = ('Conteúdo educacional. Não é oferta de investimento nem promessa de renda, retorno, ocupação, crédito ou '
          'sociedade. A Zion avalia cada caso.')


def sh(*c):
    subprocess.run([str(x) for x in c], check=True)


def duracao(arq):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(arq)],
                                capture_output=True, text=True, check=True).stdout)


def falado(t):
    for a, b in PRONUNCIA.items():
        t = re.sub(r'\b' + a + r'\b', b, t)
    return t


def cmd_narrar(a):
    import numpy as np, soundfile as sf
    from piper import PiperVoice, SynthesisConfig
    voz = PiperVoice.load(str(VOZ))
    sr = voz.config.sample_rate
    (AQUI / 'audio').mkdir(exist_ok=True)
    for v in json.loads((AQUI / 'roteiro.json').read_text(encoding='utf-8'))['videos']:
        for c in v['cenas']:
            destino = AQUI / 'audio' / f"{c['slide']:02d}.wav"
            if destino.exists() and not a.refazer:
                continue
            partes, palavras, t = [], [], 0.0
            for frase in re.split(r'(?<=[.?!:;])\s+', c['texto']):
                x = np.concatenate([k.audio_float_array for k in voz.synthesize(
                    falado(frase), syn_config=SynthesisConfig(length_scale=1 / 0.95))]).astype(np.float32)
                i = np.where(np.abs(x) > 0.01)[0]
                x = x[max(0, i[0] - 150): i[-1] + 300]
                d = len(x) / sr
                pal = frase.split()
                peso = [len(re.sub(r'\W', '', p)) + 1.5 for p in pal]
                acc = 0
                for p, w in zip(pal, peso):
                    palavras.append({'p': p, 'a': round(t + d * acc / sum(peso), 3), 'b': round(t + d * (acc + w) / sum(peso), 3)})
                    acc += w
                partes += [x, np.zeros(int(RESPIRO_FRASE * sr), np.float32)]
                t += d + RESPIRO_FRASE
            sf.write(destino, np.concatenate(partes[:-1]), sr)
            destino.with_suffix('.json').write_text(json.dumps(palavras, ensure_ascii=False), encoding='utf-8')
            print(destino.name, f'{t:5.1f} s')


def ass_tempo(t):
    return f'{int(t // 3600)}:{int(t // 60 % 60):02d}:{t % 60:05.2f}'


def legendas_ass(palavras, destino, rodape=None):
    """Blocos de até 2 linhas e 42 caracteres por linha; a palavra que está sendo falada fica dourada."""
    linhas = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1920', 'PlayResY: 1080', 'WrapStyle: 2', '',
              '[V4+ Styles]',
              'Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, '
              'Outline, Shadow, Alignment, MarginL, MarginR, MarginV',
              'Style: L,Inter SemiBold,44,&H00E8F1F5,&H401C2616,&H401C2616,0,0,3,16,0,2,200,200,70',  # caixa (estilo 3): a cor vem do contorno
              'Style: R,Inter,22,&H00BCCFD9,&H00000000,&H00000000,0,0,1,0,0,2,160,160,28', '',
              '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    blocos, atual = [], []
    for w in palavras:
        teste = ' '.join(x['p'] for x in atual + [w])
        quebra = atual and (len(teste) > 84 or atual[-1]['p'][-1] in '.?!' and len(teste) > 40)
        if quebra:
            blocos.append(atual); atual = []
        atual.append(w)
    if atual:
        blocos.append(atual)
    srt = []
    for b in blocos:
        textos = [x['p'] for x in b]
        meio = len(' '.join(textos)) > 42
        corte = 0
        if meio:
            total, corte = 0, len(textos)
            for k, p in enumerate(textos):
                total += len(p) + 1
                if total > len(' '.join(textos)) / 2:
                    corte = k + 1; break
        for k, w in enumerate(b):
            fim = b[k + 1]['a'] if k + 1 < len(b) else w['b'] + 0.25
            partes = []
            for j, p in enumerate(textos):
                partes.append(('{\\c&H5EBEE0&}' + p + '{\\c&HE8F1F5&}') if j == k else p)
                if meio and j == corte - 1 and j < len(textos) - 1:
                    partes.append('\\N')
            linhas.append(f"Dialogue: 0,{ass_tempo(w['a'])},{ass_tempo(fim)},L,,0,0,0,,"
                          + ' '.join(partes).replace(' \\N ', '\\N'))
        txt = ' '.join(textos[:corte]) + ('\n' + ' '.join(textos[corte:]) if meio else '')
        srt.append((b[0]['a'], b[-1]['b'] + 0.25, txt))
    if rodape:
        linhas.append(f'Dialogue: 1,{ass_tempo(rodape[0])},{ass_tempo(rodape[1])},R,,0,0,0,,{{\\fad(400,0)}}{RODAPE}')
    destino.write_text('\n'.join(linhas) + '\n', encoding='utf-8')
    return srt


def srt_tempo(t):
    return f'{int(t // 3600):02d}:{int(t // 60 % 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}'


def cmd_montar(a):
    trab, saida = AQUI / 'trabalho', AQUI / 'saida'
    trab.mkdir(exist_ok=True); saida.mkdir(exist_ok=True)
    hoje = datetime.date.today().isoformat()
    for v in json.loads((AQUI / 'roteiro.json').read_text(encoding='utf-8'))['videos']:
        if a.video and v['n'] != a.video:
            continue
        clipes, palavras, t = [], [], 0.0
        for k, c in enumerate(v['cenas']):
            voz = AQUI / 'audio' / f"{c['slide']:02d}.wav"
            fala = duracao(voz)
            dur = fala + FIM_CENA + (FADE if k < len(v['cenas']) - 1 else 0)
            if v['n'] == 2 and k == len(v['cenas']) - 1:
                dur += 4.0  # o último quadro segura com o rodapé
            q = round(dur * FPS)
            clipe = trab / f"c{c['slide']:02d}.mp4"
            zoom = f"min(1.05,1+0.05*on/{6 * FPS})"
            sh('ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', FPS,
               '-i', AQUI / 'slides' / f"s-{c['slide']:02d}.png", '-i', voz, '-filter_complex',
               f"[0:v]scale=3840:2160,zoompan=z='{zoom}':d={q}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={FPS},"
               f"setsar=1[v];[1:a]aresample=48000,apad[a]", '-map', '[v]', '-map', '[a]', '-t', f'{dur:.3f}',
               '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p',
               '-c:a', 'pcm_s16le', '-ac', '2', clipe)
            for w in json.loads(voz.with_suffix('.json').read_text(encoding='utf-8')):
                palavras.append({'p': w['p'], 'a': round(t + w['a'], 3), 'b': round(t + w['b'], 3)})
            clipes.append((clipe, dur))
            t += dur - (FADE if k < len(v['cenas']) - 1 else 0)
        total = t
        # junta com fade de 0,4 s entre os slides
        entradas, filtros, vv, aa, comp = [], [], '[0:v]', '[0:a]', clipes[0][1]
        for c, _ in clipes:
            entradas += ['-i', c]
        for k in range(1, len(clipes)):
            off = comp - FADE
            filtros += [f'{vv}[{k}:v]xfade=transition=fade:duration={FADE}:offset={off:.3f}[v{k}]',
                        f'{aa}[{k}:a]acrossfade=d={FADE}[a{k}]']
            vv, aa = f'[v{k}]', f'[a{k}]'
            comp = off + clipes[k][1]
        bruto = trab / f"pitch{v['n']}-bruto.mkv"
        sh('ffmpeg', '-y', '-loglevel', 'error', *entradas, '-filter_complex', ';'.join(filtros), '-map', vv, '-map', aa,
           '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', bruto)
        ass = trab / f"pitch{v['n']}.ass"
        srt = legendas_ass(palavras, ass, rodape=(total - 4.0, total) if v['n'] == 2 else None)
        titulo = v['titulo'].split('·')[1].strip()
        nome = f"{hoje} - Pitch Bloco {v['n']} - {titulo} - Zion"
        final = saida / f'{nome}.mp4'
        sh('ffmpeg', '-y', '-loglevel', 'error', '-i', bruto, '-vf', f"ass='{ass}'", '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
           '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', FPS,
           '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', final)
        (saida / f'{nome}.srt').write_text('\n'.join(f'{i}\n{srt_tempo(x)} --> {srt_tempo(y)}\n{z}\n'
                                                     for i, (x, y, z) in enumerate(srt, 1)), encoding='utf-8')
        d = duracao(final)
        print(f'{final.name}: {int(d // 60)}:{d % 60:04.1f}' + ('  PASSOU de 7:00' if d > 420 else ''))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('narrar'); p.add_argument('--refazer', action='store_true'); p.set_defaults(f=cmd_narrar)
    p = sub.add_parser('montar'); p.add_argument('--video', type=int, default=0); p.set_defaults(f=cmd_montar)
    a = ap.parse_args()
    a.f(a)
