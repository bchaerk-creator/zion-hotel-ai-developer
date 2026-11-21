#!/bin/bash
# Monta o vídeo vertical de 30 s (silencioso, com texto na tela): dor 0-5 s, demonstração 5-20 s, entregáveis 20-27 s, chamada 27-30 s.
set -e; D="$(cd "$(dirname "$0")" && pwd)"; V="$D/dist/video"
ffmpeg -y -loglevel error \
 -loop 1 -t 5 -i "$V/s1.png" -loop 1 -t 15 -i "$V/fundo.png" -i "$D/../landing/img/demo.mp4" -loop 1 -t 7 -i "$V/s3.png" -loop 1 -t 3 -i "$V/s4.png" \
 -filter_complex "[2:v]trim=0:19.800000,setpts=(PTS-STARTPTS)*15/19.800000,scale=640:-1:flags=lanczos,fps=30[d];[1:v][d]overlay=(W-w)/2:330:shortest=1[demo];[0:v]fps=30[a];[3:v]fps=30[c];[4:v]fps=30[e];[a][demo][c][e]concat=n=4:v=1:a=0,format=yuv420p[v]" \
 -map "[v]" -c:v libx264 -crf 22 -movflags +faststart "$V/reels_30s_1080x1920.mp4"
ffprobe -v error -show_entries stream=width,height,duration,codec_name -of csv=p=0 "$V/reels_30s_1080x1920.mp4"
for t in 2 10 17 24 28.5; do ffmpeg -y -loglevel error -ss $t -i "$V/reels_30s_1080x1920.mp4" -frames:v 1 "$V/frame_$t.png"; done
