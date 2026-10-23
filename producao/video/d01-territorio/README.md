# Aula 2 · Território · vídeo narrado

Monta o vídeo narrado da aula a partir do PDF dos slides (60 páginas, 16:9) e do `roteiro.md`.
Segue o prompt de produção do Bruno (23/10/2026): uma imagem por slide, narração por slide,
+0,8 s de respiro, +6 s nos slides [PAUSA], zoom lento de 100% a 104% nos slides [FOTO],
fade de 0,5 s entre slides, fala em -16 LUFS com pico de -1,5 dB, sem música.

## O que precisa estar nesta pasta
- `aula2-territorio.pdf`: no Google Slides, Arquivo › Fazer download › PDF.
- `demo-ferramenta.mp4` (opcional): gravação da ferramenta "Leitura do seu terreno" com Urubici. Entra no slide 48.
- Para a voz do Bruno: variável `ELEVENLABS_API_KEY` no ambiente e o ID da voz. Sem ela, usa a voz grátis `pt-BR-AntonioNeural`.

## Passo a passo
```bash
python3 aula.py slides aula2-territorio.pdf   # confere que saíram 60 imagens
python3 aula.py narrar --teste [--voz ID]     # só o slide 1: ouça e aprove antes de seguir
python3 aula.py narrar [--voz ID]             # os outros 59 (pula os que já existem; --refazer regrava)
python3 aula.py montar                        # gera tudo em saida/
```

Precisa de `ffmpeg`, `ffprobe`, `pdftoppm` e, para a voz grátis, `pip install edge-tts`.

## O que sai
- `saida/aula2-territorio-completa.mp4`: 1920×1080, 30 fps, H.264, AAC 48 kHz.
- `saida/blocos/bloco-1.mp4` a `bloco-7.mp4`: um por bloco, cortados pelos slides de abertura.
- `saida/aula2-territorio.srt`: legenda com o texto exato da fala, até 42 caracteres por linha, 2 linhas.
- `saida/relatorio.txt`: duração de cada slide, de cada bloco e do total, formato conferido com ffprobe e problemas.
- `saida/conferencia/`: 3 quadros dos primeiros 20 s de cada bloco.

## Para mudar o texto
Edite `roteiro.md` (o texto embaixo de cada título é o que a voz fala), apague o `audio/NN.mp3` daquele slide,
rode `narrar` e `montar` de novo.

## Ainda não feito
- Avatar HeyGen (opção C do prompt): fica para quando houver a chave e o ID do avatar.
