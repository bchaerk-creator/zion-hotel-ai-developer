#!/usr/bin/env python3
"""Aula 1 · Marco Zero em 7 vídeos de até 7:00, a partir do slides.pdf e do ROTEIRO de prompt-videos.md.

  python3 a1.py narrar [--videos 1-7] [--teste] [--velocidade 0.9]   # audio/PP.mp3 com o Kokoro (voz pm_alex)
  python3 a1.py montar [--videos 1-7]                                # vídeos, verticais, legendas e relatório
  python3 a1.py narrar --motor heygen --teste                        # página 01 com a voz do HeyGen (HEYGEN_API_KEY)
  python3 a1.py tudo                                                 # HeyGen nas 51 páginas e remonta tudo

Slides: pdftoppm -png -r 150 -scale-to-x 1920 -scale-to-y 1080 slides.pdf slides/p
Regras: página = áudio + 0,8 s; [PAUSA] +5 s com "pause e anote"; [FOTO] zoom de 100% a 104%;
fade de 0,4 s; selo "Aula 1 · Marco Zero · N de 7" até 4 s; "Próximo vídeo" nos 2 s finais (menos no 7);
fala em -16 LUFS / -1,5 dBTP; nenhum vídeo passa de 7:00 (se passar, avisa, não corta).
"""
import argparse, json, os, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
# Reaproveita voz, volume e legenda da montagem da Aula 2 (producao/video/d01-territorio/aula.py).
sys.path.insert(0, str(AQUI.parent / 'd01-territorio'))
import aula  # noqa: E402
from aula import sh, duracao, legendas, tempo_srt  # noqa: E402

FPS, W, H = 30, 1920, 1080
RESPIRO, PAUSA, FADE, LIMITE = 0.8, 5.0, 0.4, 420.0
FONTE = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
OURO, VERDE = '0xE0BE5E', '0x16261C'
ENC_V = ['-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS)]
ENC_A = ['-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2']


def roteiro():
    videos, atual = [], None
    for parte in re.split(r'\n(?=### |\*\*Página )', (AQUI / 'prompt-videos.md').read_text(encoding='utf-8')):
        m = re.match(r'### Vídeo (\d+) de 7 · (.+?)(?: \(cerca de [\d:]+\))?\n', parte)
        if m:
            atual = {'n': int(m.group(1)), 'titulo': m.group(2).strip(), 'paginas': []}
            videos.append(atual)
            continue
        m = re.match(r'\*\*Página (\d\d) · (.+?)\*\*([^\n]*)\n(.+)', parte, re.S)
        if m:
            atual['paginas'].append({'p': int(m.group(1)), 'nome': m.group(2).strip(), 'foto': '[FOTO]' in m.group(3),
                                     'pausa': '[PAUSA]' in m.group(3), 'texto': ' '.join(m.group(4).split('\n\n')[0].replace('FIM DO PROMPT', '').split())})
    assert [v['n'] for v in videos] == list(range(1, 8)), 'vídeos fora de ordem'
    return videos


# como o modelo lê nomes de fora; a troca vale só para a voz (a legenda mantém o texto)
PRONUNCIA = {'Zion': 'Záion', 'Group': 'Grúpi', 'Bubble': 'Bâbol'}


def falado(texto):
    return re.sub(r'\b(' + '|'.join(PRONUNCIA) + r')\b', lambda m: PRONUNCIA[m.group(1)], texto)


def falar(motor, texto, voz, velocidade, destino, respiro=0.45):
    """Uma frase por vez, com um respiro entre elas: a fala fica mais calma sem arrastar as palavras."""
    import numpy as np, soundfile as sf
    partes = []
    for frase in re.split(r'(?<=[.?!])\s+', texto):
        audio, taxa = motor.create(falado(frase), voice=voz, speed=velocidade, lang='pt-br')
        idx = np.where(np.abs(audio) > 0.01)[0]
        partes += [audio[max(0, idx[0] - 240): idx[-1] + 600], np.zeros(int(respiro * taxa), np.float32)]
    wav = destino.with_suffix('.wav')
    sf.write(wav, np.concatenate(partes[:-1]), taxa)
    sh('ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-b:a', '192k', destino)
    wav.unlink()


def faixa(txt):
    if not txt:
        return list(range(1, 8))
    a, _, b = txt.partition('-')
    return list(range(int(a), int(b or a) + 1))


VOZ_HEYGEN = '7d5dfb068b534baa996aef0ab3468a8d'


def heygen(caminho, corpo):
    import urllib.request, urllib.error
    req = urllib.request.Request('https://api.heygen.com' + caminho, data=json.dumps(corpo).encode(), method='POST',
                                 headers={'X-Api-Key': os.environ['HEYGEN_API_KEY'], 'Content-Type': 'application/json',
                                          'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {'erro': e.code, 'corpo': e.read().decode(errors='replace')[:400]}


def falar_heygen(texto, voz_id, destino):
    """HeyGen: tenta a API de fala atual (v3) e cai para a antiga (v1); baixa o áudio e grava em mp3."""
    import urllib.request
    texto = falado(texto)
    tentativas = [('/v3/voices/speech', {'text': texto, 'voice_id': voz_id}),
                  ('/v1/audio/text_to_speech', {'text': texto, 'voice_id': voz_id})]
    erros = []
    for caminho, corpo in tentativas:
        r = heygen(caminho, corpo)
        url = (r.get('data') or {}).get('audio_url') or r.get('audio_url')
        if url:
            bruto = destino.with_suffix('.heygen')
            urllib.request.urlretrieve(url, bruto)
            sh('ffmpeg', '-y', '-loglevel', 'error', '-i', bruto, '-ar', '48000', '-b:a', '192k', destino)
            bruto.unlink()
            return
        erros.append(f'{caminho}: {r}')
    sys.exit('HeyGen não devolveu áudio.\n' + '\n'.join(erros))


def trechos(texto, limite=190):
    """Corta em frases e, se preciso, em vírgulas, sem passar do limite de caracteres por pedido."""
    saida = []
    for frase in re.split(r'(?<=[.?!])\s+', texto):
        partes, atual = re.split(r'(?<=[,;:])\s+', frase), ''
        for parte in partes:
            if atual and len(atual) + len(parte) + 1 > limite:
                saida.append((atual, 0.12)); atual = parte
            else:
                atual = f'{atual} {parte}'.strip()
        saida.append((atual, 0.38))
    return saida


def falar_google(texto, destino):
    """Voz do Google em pt-BR, trecho a trecho, com respiros entre frases."""
    import urllib.parse, urllib.request
    trab = destino.parent / f'.{destino.stem}'
    trab.mkdir(exist_ok=True)
    lista, tempos, t0 = [], [], 0.0
    originais = trechos(texto)
    for i, (t, pausa) in enumerate(trechos(falado(texto))):
        mp3 = trab / f'{i:03d}.mp3'
        url = 'https://translate.googleapis.com/translate_tts?' + urllib.parse.urlencode(
            {'client': 'gtx', 'ie': 'UTF-8', 'tl': 'pt-BR', 'q': t})
        mp3.write_bytes(urllib.request.urlopen(url, timeout=60).read())
        wav = trab / f'{i:03d}.wav'
        sh('ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-af',
           f'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,'
           f'areverse,apad=pad_dur={pausa}', '-ar', '24000', '-ac', '1', wav)
        lista.append(f"file '{wav.name}'")
        d = duracao(wav)
        tempos.append({'a': round(t0, 3), 'b': round(t0 + d - pausa, 3), 'texto': originais[i][0]})
        t0 += d
    destino.with_suffix('.json').write_text(json.dumps(tempos, ensure_ascii=False, indent=1), encoding='utf-8')
    (trab / 'lista.txt').write_text('\n'.join(lista))
    sh('ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', trab / 'lista.txt', '-b:a', '192k', destino)
    for f in trab.iterdir():
        f.unlink()
    trab.rmdir()


def cmd_narrar(a):
    pasta = AQUI / 'audio'
    pasta.mkdir(exist_ok=True)
    if a.motor == 'google':
        pass
    elif a.motor == 'heygen':
        voz_id = a.voz if a.voz != 'pm_alex' else os.environ.get('HEYGEN_VOICE_ID') or VOZ_HEYGEN
        if not os.environ.get('HEYGEN_API_KEY'):
            sys.exit('Falta a variável HEYGEN_API_KEY nas configurações do ambiente.')
    else:
        aula.AQUI = AQUI.parent / 'd01-territorio'  # o modelo Kokoro já baixado fica lá em modelos/
        motor = aula.kokoro()
    for v in roteiro():
        if v['n'] not in faixa(a.videos):
            continue
        for pg in v['paginas']:
            if a.teste and pg['p'] != 1:
                continue
            destino = pasta / f"{pg['p']:02d}.mp3"
            if destino.exists() and not a.refazer:
                continue
            if a.motor == 'google':
                falar_google(pg['texto'], destino)
            elif a.motor == 'heygen':
                falar_heygen(pg['texto'], voz_id, destino)
            else:
                falar(motor, pg['texto'], a.voz, a.velocidade, destino)
            print(f"{destino.name} {duracao(destino):6.1f} s  vídeo {v['n']} · {pg['nome']}")


def clipe(pg, voz, destino):
    fala = duracao(voz)
    dur = fala + RESPIRO + (PAUSA if pg['pausa'] else 0)
    q = round(dur * FPS)
    if pg['foto']:
        video = (f"scale={W * 2}:{H * 2},zoompan=z='1+0.04*on/{q}':d={q}:x='iw/2-(iw/zoom/2)':"
                 f"y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},setsar=1")
    else:
        video = f'scale={W}:{H},setsar=1,fps={FPS}'
    sh('ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', FPS, '-i', AQUI / 'slides' / f"p-{pg['p']:02d}.png",
       '-i', voz, '-filter_complex', f'[0:v]{video}[v];[1:a]apad[a]', '-map', '[v]', '-map', '[a]',
       '-t', f'{dur:.3f}', *ENC_V, *ENC_A, destino)
    return duracao(destino), fala


def juntar(clipes, duracoes, destino):
    entradas, filtros, inicios = [], [], [0.0]
    for c in clipes:
        entradas += ['-i', c]
    v, au, comp = '[0:v]', '[0:a]', duracoes[0]
    for k in range(1, len(clipes)):
        off = comp - FADE
        filtros += [f'{v}[{k}:v]xfade=transition=fade:duration={FADE}:offset={off:.3f}[v{k}]',
                    f'{au}[{k}:a]acrossfade=d={FADE}[a{k}]']
        v, au = f'[v{k}]', f'[a{k}]'
        inicios.append(off)
        comp = off + duracoes[k]
    args = ['-filter_complex', ';'.join(filtros), '-map', v, '-map', au] if filtros else ['-map', '0:v', '-map', '0:a']
    sh('ffmpeg', '-y', '-loglevel', 'error', *entradas, *args, *ENC_V, *ENC_A, destino)
    return inicios


def texto_tela(nome, conteudo):
    arq = AQUI / 'trabalho/txt' / f'{nome}.txt'
    arq.write_text(conteudo, encoding='utf-8')
    return arq


def sobreposicoes(v, inicios, info, total, proximo):
    """Selo, 'pause e anote' e 'Próximo vídeo' com drawtext (texto em arquivo, sem escapar acento)."""
    caixa = f"fontfile={FONTE}:box=1:boxcolor={VERDE}@0.8"
    selo = texto_tela(f"selo{v['n']:02d}", f"Aula 1 · Marco Zero · {v['n']} de 7")
    f = [f"drawtext={caixa}:boxborderw=16:textfile={selo}:fontsize=28:fontcolor={OURO}:x=56:y=48:"
         f"alpha='if(lt(t,3.6),1,max(0,(4-t)/0.4))':enable='lt(t,4)'"]
    pausa = texto_tela('pausa', 'pause e anote')
    for pg, ini in zip(v['paginas'], inicios):
        if pg['pausa']:
            a = ini + info[pg['p']]['fala'] + 0.3
            b = min(ini + info[pg['p']]['dur'] - FADE, total - 2 if proximo else total)
            f.append(f"drawtext={caixa}:boxborderw=14:textfile={pausa}:fontsize=32:fontcolor={OURO}:x=56:y=h-110:"
                     f"alpha='min(1,(t-{a:.2f})/0.3)':enable='between(t,{a:.2f},{b:.2f})'")
    if proximo:
        prox = texto_tela(f"prox{v['n']:02d}", f'Próximo vídeo: {proximo}')
        a = total - 2
        f.append(f"drawtext={caixa}:boxborderw=20:textfile={prox}:fontsize=40:fontcolor=0xF5F1E8:x=(w-text_w)/2:y=h-140:"
                 f"alpha='min(1,(t-{a:.2f})/0.3)':enable='gte(t,{a:.2f})'")
    return ','.join(f)


def ass(blocos, destino):
    """Legenda .ass em pixels do quadro vertical (o .srt não fixa o tamanho da fonte)."""
    tempo = lambda t: f'{int(t // 3600)}:{int(t // 60 % 60):02d}:{t % 60:05.2f}'
    linhas = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1080', 'PlayResY: 1920', '',
              '[V4+ Styles]',
              'Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, '
              'Outline, Shadow, Alignment, MarginL, MarginR, MarginV',
              'Style: Default,Inter SemiBold,48,&H00FFFFFF,&H00000000,&H00000000,0,0,1,0,0,8,70,70,1310', '',
              '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    linhas += [f"Dialogue: 0,{tempo(a)},{tempo(b)},Default,,0,0,0,,{t.replace(chr(10), chr(92) + 'N')}" for a, b, t in blocos]
    destino.write_text('\n'.join(linhas) + '\n', encoding='utf-8')


def vertical(origem, legenda_ass, destino):
    """1080x1920: fundo verde-escuro, vídeo no centro e legenda queimada logo abaixo, até 2 linhas."""
    filtro = f"[0:v]scale=1080:-2,pad=1080:1920:0:(1920-ih)/2:color={VERDE},ass='{legenda_ass}'[v]"
    sh('ffmpeg', '-y', '-loglevel', 'error', '-i', origem, '-filter_complex', filtro, '-map', '[v]', '-map', '0:a',
       *ENC_V, '-c:a', 'copy', '-movflags', '+faststart', destino)


def cmd_montar(a):
    videos = roteiro()
    alvo = [v for v in videos if v['n'] in faixa(a.videos)]
    faltam = [pg['p'] for v in alvo for pg in v['paginas']
              if not (AQUI / 'audio' / f"{pg['p']:02d}.mp3").exists() or not (AQUI / 'slides' / f"p-{pg['p']:02d}.png").exists()]
    if faltam:
        sys.exit(f'Faltam slide ou áudio das páginas {faltam}')
    for p in ('trabalho/voz', 'trabalho/clipes', 'trabalho/txt', 'saida/videos', 'saida/verticais',
              'saida/legendas', 'saida/conferencia'):
        (AQUI / p).mkdir(parents=True, exist_ok=True)

    rel, problemas = ['RELATÓRIO · Aula 1 · Marco Zero em 7 vídeos', ''], []
    for v in alvo:
        info = {}
        for pg in v['paginas']:
            voz = AQUI / 'trabalho/voz' / f"{pg['p']:02d}.wav"
            aula.normalizar(AQUI / 'audio' / f"{pg['p']:02d}.mp3", voz)
            dur, fala = clipe(pg, voz, AQUI / 'trabalho/clipes' / f"{pg['p']:02d}.mp4")
            info[pg['p']] = {'dur': dur, 'fala': fala}
        bruto = AQUI / 'trabalho' / f"mz{v['n']:02d}-bruto.mp4"
        inicios = juntar([AQUI / 'trabalho/clipes' / f"{pg['p']:02d}.mp4" for pg in v['paginas']],
                         [info[pg['p']]['dur'] for pg in v['paginas']], bruto)
        total = duracao(bruto)
        proximo = videos[v['n']]['titulo'] if v['n'] < 7 else None
        marcado = AQUI / 'trabalho' / f"mz{v['n']:02d}-marcado.mp4"
        sh('ffmpeg', '-y', '-loglevel', 'error', '-i', bruto, '-vf', sobreposicoes(v, inicios, info, total, proximo),
           *ENC_V, '-c:a', 'copy', marcado)
        nome = f"V{v['n']:02d} - {v['titulo']}"
        final = AQUI / 'saida/videos' / f'{nome}.mp4'
        aula.normalizar(marcado, final, video=True)

        srt = AQUI / 'saida/legendas' / f"V{v['n']:02d}.srt"
        blocos = []
        for pg, ini in zip(v['paginas'], inicios):
            blocos += legendas(pg['texto'], ini, ini + info[pg['p']]['fala'])
        srt.write_text('\n'.join(f'{i}\n{tempo_srt(x)} --> {tempo_srt(y)}\n{t}\n' for i, (x, y, t) in enumerate(blocos, 1)),
                       encoding='utf-8')
        legenda_ass = AQUI / 'trabalho' / f"mz{v['n']:02d}.ass"
        ass(blocos, legenda_ass)
        vertical(final, legenda_ass, AQUI / 'saida/verticais' / f'{nome}.mp4')

        for t in (0.5, 2.0, 3.5):
            sh('ffmpeg', '-y', '-loglevel', 'error', '-ss', t, '-i', final, '-frames:v', 1, '-vf', 'scale=640:-1',
               AQUI / 'saida/conferencia' / f"V{v['n']:02d}-{t:.1f}s.png")

        dur_final = duracao(final)
        rel.append(f"V{v['n']:02d} · {v['titulo']} · {int(dur_final // 60)}:{dur_final % 60:04.1f}")
        for pg in v['paginas']:
            marcas = ' '.join(m for m, ok in (('[FOTO]', pg['foto']), ('[PAUSA]', pg['pausa'])) if ok)
            rel.append(f"   pág. {pg['p']:02d} {pg['nome']:<12} fala {info[pg['p']]['fala']:5.1f} s  clipe {info[pg['p']]['dur']:5.1f} s  {marcas}")
        if dur_final > LIMITE:
            problemas.append(f"V{v['n']:02d} passou de 7:00 por {dur_final - LIMITE:.1f} s (não cortei nem acelerei).")
        for arq in (final, AQUI / 'saida/verticais' / f'{nome}.mp4'):
            p = json.loads(sh('ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name,width,height,r_frame_rate,sample_rate',
                              '-of', 'json', arq, capture=True))['streams']
            vv = next(s for s in p if 'width' in s); aa = next(s for s in p if 'sample_rate' in s)
            esperado = (1920, 1080) if 'videos' in str(arq) else (1080, 1920)
            if (vv['width'], vv['height']) != esperado or vv['r_frame_rate'] != '30/1' or aa['sample_rate'] != '48000' \
                    or vv['codec_name'] != 'h264' or aa['codec_name'] != 'aac':
                problemas.append(f'Formato fora do pedido: {arq.name} {vv} {aa}')
        print(rel[-len(v['paginas']) - 1])
    rel += ['', 'Problemas: ' + ('nenhum' if not problemas else ''), *problemas]
    (AQUI / 'saida/relatorio.txt').write_text('\n'.join(rel) + '\n', encoding='utf-8')
    print('\n'.join(rel[-(len(problemas) + 1):]))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('narrar'); p.add_argument('--videos', default=''); p.add_argument('--voz', default='pm_alex')
    p.add_argument('--velocidade', type=float, default=0.85)
    p.add_argument('--motor', choices=['google', 'kokoro', 'heygen'], default='google')
    p.add_argument('--teste', action='store_true'); p.add_argument('--refazer', action='store_true'); p.set_defaults(f=cmd_narrar)
    p = sub.add_parser('montar'); p.add_argument('--videos', default=''); p.set_defaults(f=cmd_montar)
    p = sub.add_parser('tudo', help='narra de novo (HeyGen) e remonta os 7 vídeos')
    p.add_argument('--videos', default=''); p.add_argument('--voz', default='pm_alex')
    p.set_defaults(f=lambda a: (cmd_narrar(argparse.Namespace(videos=a.videos, voz=a.voz, velocidade=1.0, motor='heygen',
                                                              teste=False, refazer=True)), cmd_montar(a)))
    a = ap.parse_args()
    a.f(a)
