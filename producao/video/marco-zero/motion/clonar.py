#!/usr/bin/env python3
"""Troca o timbre de uma narração pela voz do Bruno (kNN-VC), mantendo a duração exata.

Uso: python3 clonar.py entrada.wav saida.wav [--topk 4]
Amostra da voz: ../gravacoes/bruno_ref.wav (fala limpa do Bruno, 16 kHz).
Modelo: código de github.com/bshall/knn-vc em modelos/knn-vc e pesos em ~/.cache/torch/hub/checkpoints
(WavLM-Large.pt e prematch_g_02500000.pt, dos releases v0.1 do mesmo repositório).
"""
import subprocess, sys, tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
KNN = AQUI / 'modelos' / 'knn-vc'
REF = AQUI.parent / 'gravacoes' / 'bruno_ref.wav'


def clonar(entrada, saida, topk=4):
    import torch, torchaudio
    sys.path.insert(0, str(KNN))
    from hubconf import knn_vc
    m = knn_vc(pretrained=True, progress=False, prematched=True, device='cpu')
    with tempfile.TemporaryDirectory() as tmp:
        src16 = Path(tmp) / 'src16.wav'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(entrada), '-ar', '16000', '-ac', '1', str(src16)], check=True)
        n_in = torchaudio.info(str(src16)).num_frames
        out = m.match(m.get_features(str(src16)), m.get_matching_set([str(REF)]), topk=topk)
        # o vocoder devolve múltiplos de 320 amostras: completa ou corta para a duração original
        out = torch.nn.functional.pad(out, (0, max(0, n_in - out.shape[-1])))[:n_in]
        conv = Path(tmp) / 'conv16.wav'
        torchaudio.save(str(conv), out[None], 16000)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(conv), '-af', 'highpass=f=70', '-ar', '48000', str(saida)], check=True)


if __name__ == '__main__':
    args = sys.argv[1:]
    topk = int(args[args.index('--topk') + 1]) if '--topk' in args else 4
    clonar(args[0], args[1], topk)
    print(args[1])
