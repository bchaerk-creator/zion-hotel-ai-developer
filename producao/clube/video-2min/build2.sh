set -e
# uso: build2.sh <dir w|t> <WxH> <saida>
D=$1; SZ=$2; OUT=$3; W=${SZ%x*}; H=${SZ#*x}
P=0.7
read D1 D2 D3 D4 D5 < <(python3 -c "import json;d=json.load(open('dur.json'));print(*[round(x+$P,2) for x in d])")
Z="x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=${SZ}:fps=30"
# cena 1: filme (trecho 8s) escurecido + texto
ffmpeg -y -v error -ss 8 -t $D1 -i ../filme.mp4 -i $D/s1.png -filter_complex "[0:v]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,eq=brightness=-0.2:saturation=0.85,fps=30[f];[f][1:v]overlay=0:0,format=yuv420p" -an -c:v libx264 -preset fast -crf 20 $D/c1.mp4
ffmpeg -y -v error -loop 1 -i $D/s2.png -t $D2 -filter_complex "zoompan=z='1+0.0006*in':d=1:$Z,format=yuv420p" -c:v libx264 -preset fast -crf 20 $D/c2.mp4
ffmpeg -y -v error -loop 1 -i $D/s3.png -t $D3 -filter_complex "zoompan=z='1+0.0006*in':d=1:$Z,format=yuv420p" -c:v libx264 -preset fast -crf 20 $D/c3.mp4
ffmpeg -y -v error -loop 1 -i $D/s4.png -t $D4 -filter_complex "zoompan=z='1+0.0008*in':d=1:$Z,format=yuv420p" -c:v libx264 -preset fast -crf 20 $D/c4.mp4
ffmpeg -y -v error -loop 1 -i $D/s5.png -t $D5 -filter_complex "zoompan=z='1+0.001*in':d=1:$Z,format=yuv420p" -c:v libx264 -preset fast -crf 20 $D/c5.mp4
O1=$(python3 -c "print($D1-0.6)"); O2=$(python3 -c "print($D1+$D2-1.2)"); O3=$(python3 -c "print($D1+$D2+$D3-1.8)"); O4=$(python3 -c "print($D1+$D2+$D3+$D4-2.4)"); FO=$(python3 -c "print($D1+$D2+$D3+$D4+$D5-2.4-1.0)")
ffmpeg -y -v error -i $D/c1.mp4 -i $D/c2.mp4 -i $D/c3.mp4 -i $D/c4.mp4 -i $D/c5.mp4 -filter_complex "[0][1]xfade=transition=fade:duration=0.6:offset=$O1[a];[a][2]xfade=transition=fade:duration=0.6:offset=$O2[b];[b][3]xfade=transition=fade:duration=0.6:offset=$O3[c];[c][4]xfade=transition=fade:duration=0.6:offset=$O4,fade=t=out:st=$FO:d=1.0" -c:v libx264 -preset fast -crf 20 -an $D/video.mp4
S2=$(python3 -c "print(int(($D1-0.6)*1000))"); S3=$(python3 -c "print(int(($D1+$D2-1.2)*1000))"); S4=$(python3 -c "print(int(($D1+$D2+$D3-1.8)*1000))"); S5=$(python3 -c "print(int(($D1+$D2+$D3+$D4-2.4)*1000))")
[ -f narr.m4a ] || ffmpeg -y -v error -i n1.mp3 -i n2.mp3 -i n3.mp3 -i n4.mp3 -i n5.mp3 -filter_complex "[0]adelay=400|400[a0];[1]adelay=$S2|$S2[a1];[2]adelay=$S3|$S3[a2];[3]adelay=$S4|$S4[a3];[4]adelay=$S5|$S5[a4];[a0][a1][a2][a3][a4]amix=inputs=5:normalize=0,loudnorm=I=-16:TP=-1.5" -ar 48000 narr.m4a
ffmpeg -y -v error -i $D/video.mp4 -i narr.m4a -c:v libx264 -preset medium -crf 24 -c:a aac -b:a 160k -shortest -movflags +faststart $OUT
ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 $OUT; ls -la $OUT
