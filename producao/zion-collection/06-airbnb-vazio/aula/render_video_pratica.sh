#!/bin/bash
# Grava e monta a videoaula prática. Uso: bash aula/render_video_pratica.sh <jspdf.umd.min.js>
set -e; cd "$(dirname "$0")/.."; node aula/gravar_pratica.js "$1"; cd aula/dist
ESTILO="FontName=Aventa Variable,FontSize=13,Bold=0,PrimaryColour=&H00F0F5FE,OutlineColour=&H90050604,BorderStyle=3,BackColour=&H90050604,Outline=3,Shadow=0,MarginV=22"
ffmpeg -hide_banner -loglevel error -y -i pratica_raw.webm -vf "fps=30,format=yuv420p,subtitles=videoaula_pratica.srt:fontsdir=../fonts:force_style='$ESTILO'" -c:v libx264 -preset medium -crf 21 -movflags +faststart -an Videoaula-Pratica-Diagnostico-Zion.mp4
rm pratica_raw.webm
