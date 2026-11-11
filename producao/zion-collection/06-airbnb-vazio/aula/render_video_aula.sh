#!/bin/bash
# Monta a Aula 01 (slides + legendas gravadas). Uso: bash aula/render_video_aula.sh  (a partir da pasta do produto)
set -e; cd "$(dirname "$0")/dist"
python3 -I -c "
import json;t=json.load(open('aula01_tempos.json'))
f=open('concat.txt','w')
for x in t: f.write(f\"file 'png/slide{x['slide']:02d}.png'\nduration {x['duracao']}\n\")
f.write(f\"file 'png/slide{t[-1]['slide']:02d}.png'\n\")"
ESTILO="FontName=Aventa Variable,FontSize=13,Bold=0,PrimaryColour=&H00F0F5FE,OutlineColour=&H90050604,BorderStyle=3,BackColour=&H90050604,Outline=3,Shadow=0,MarginV=22"
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i concat.txt -vf "fps=30,format=yuv420p,subtitles=aula01.srt:fontsdir=../fonts:force_style='$ESTILO'" -c:v libx264 -preset medium -crf 20 -movflags +faststart -an Aula01-Por-que-seu-calendario-esta-vazio.mp4
rm concat.txt
