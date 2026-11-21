#!/bin/bash
# Monta o vídeo vertical de 30 s COM VOZ: dor 0-5 s, demonstração 5-20 s, entregáveis 20-27 s, chamada 27-30 s.
# Voz: locução sintética pt-BR (src/voz/s1..s4.mp3, gerada por tts_edge.py). Trocar por locução humana quando houver.
set -e; D="$(cd "$(dirname "$0")" && pwd)"; V="$D/dist/video"; Z="$D/src/voz"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$D/../landing/img/demo.mp4")
ffmpeg -y -loglevel error \
 -loop 1 -t 5 -i "$V/s1.png" -loop 1 -t 15 -i "$V/fundo.png" -i "$D/../landing/img/demo.mp4" -loop 1 -t 7 -i "$V/s3.png" -loop 1 -t 3 -i "$V/s4.png" \
 -i "$Z/s1.mp3" -i "$Z/s2.mp3" -i "$Z/s3.mp3" -i "$Z/s4.mp3" \
 -filter_complex "[2:v]trim=0:$DUR,setpts=(PTS-STARTPTS)*15/$DUR,scale=640:-1:flags=lanczos,fps=30[d];[1:v][d]overlay=(W-w)/2:330:shortest=1[demo];[0:v]fps=30[a];[3:v]fps=30[c];[4:v]fps=30[e];[a][demo][c][e]concat=n=4:v=1:a=0,format=yuv420p[v];\
[5:a]atempo=1.07,adelay=150|150[a1];[6:a]atempo=1.05,adelay=5200|5200[a2];[7:a]atempo=1.0,adelay=20200|20200[a3];[8:a]atempo=1.0,adelay=27600|27600[a4];[a1][a2][a3][a4]amix=inputs=4:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=7,atrim=0:30,apad=whole_dur=30[aud]" \
 -map "[v]" -map "[aud]" -c:v libx264 -crf 22 -c:a aac -b:a 160k -t 30 -movflags +faststart "$V/reels_30s_1080x1920.mp4"
ffprobe -v error -show_entries stream=codec_name,duration -show_entries format=duration -of csv=p=0 "$V/reels_30s_1080x1920.mp4"
