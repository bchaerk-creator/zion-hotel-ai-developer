# Zion Video Engine

Motor de vídeo das aulas da Zion Hospitality Academy (mentoria Airbnb de Sucesso).
Recebe a narração do Bruno (gravação real ou avatar HeyGen), recorta o apresentador, monta a cena
(painel 3D, chips, legendas, barra de progresso da trilha, crédito, pausas) e renderiza quadro a quadro.

> Este motor foi reconstruído nesta sessão a partir do prompt mestre, porque o pacote
> `zion-video-engine.zip` original não chegou aqui. Os scripts originais (`prep_vertical.py`,
> `sfx.py`, `transcribe_vad.py`, templates verticais e a biblioteca 3D completa) entram quando o
> pacote for colocado nesta pasta; os nomes e o formato `lessons/<id>/` já seguem o mesmo padrão.

## Instalação
```bash
pip install playwright sherpa-onnx soundfile onnxruntime pillow numpy scipy
npm install                      # three@0.160.0, topojson-client, world-atlas
mkdir -p models && cd models
curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx
curl -LO https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx
curl -L https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2 | tar xj
```
Precisa de ffmpeg com libx264 e rubberband.

## Uso (todo script recebe `--lesson <id>`, pasta `lessons/<id>/`)
```bash
python3 scripts/logos.py                                  # logo_cream.png e logo_green.png
python3 scripts/matte.py  --lesson p01-a01 --mesa 0.66    # fg/*.webp e anchors.json
python3 scripts/render.py --lesson p01-a01 --tempos 1,5,9 # folha de contato
python3 scripts/render.py --lesson p01-a01                # todos os quadros em out/
```
Na máquina do Bruno, `render.py --gpu` usa a placa de vídeo; rode vários processos com
`--inicio/--fim` e `--porta` diferentes para dividir a aula.

## O que existe hoje
- `scripts/comum.py`: caminhos relativos e o argumento `--lesson`.
- `scripts/logos.py`, `scripts/matte.py`, `scripts/render.py`.
- `templates/aula_16x9.html`: aula da área de membros (apresentador à direita, painel 3D à esquerda,
  chips, legenda, barra "Pilar 0X · Aula 0Y de 10", crédito, marca d'água, cartão de pausa).
- `lessons/teste/timeline.json`: exemplo do formato.
