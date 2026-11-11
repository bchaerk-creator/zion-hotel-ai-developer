set -e
P=0.7   # pausa depois de cada fala
D1=12.5; D2=12.9; D3=15.1; D4=18.7; D5=18.2
# cena 1: foto com zoom lento
ffmpeg -y -v error -loop 1 -i s1.png -t $D1 -filter_complex "zoompan=z='1+0.0015*in':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,format=yuv420p" -c:v libx264 -preset fast -crf 20 c1.mp4
# cena 2: filme (trecho 8s-21s) escurecido + texto
ffmpeg -y -v error -ss 8 -t $D2 -i filme.mp4 -i s2.png -filter_complex "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=brightness=-0.25:saturation=0.8,fps=30[f];[f][1:v]overlay=0:0,format=yuv420p" -an -c:v libx264 -preset fast -crf 20 c2.mp4
# cena 3: mapa
ffmpeg -y -v error -loop 1 -i s3.png -t $D3 -filter_complex "zoompan=z='1+0.0008*in':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,format=yuv420p" -c:v libx264 -preset fast -crf 20 c3.mp4
# cena 4: etapas
ffmpeg -y -v error -loop 1 -i s4.png -t $D4 -filter_complex "zoompan=z='1+0.0006*in':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,format=yuv420p" -c:v libx264 -preset fast -crf 20 c4.mp4
# cena 5: oferta
ffmpeg -y -v error -loop 1 -i s5.png -t $D5 -filter_complex "zoompan=z='1+0.001*in':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,format=yuv420p" -c:v libx264 -preset fast -crf 20 c5.mp4
# vídeo com transições (xfade 0.6s)
O1=$(python3 -c "print($D1-0.6)"); O2=$(python3 -c "print($D1+$D2-1.2)"); O3=$(python3 -c "print($D1+$D2+$D3-1.8)"); O4=$(python3 -c "print($D1+$D2+$D3+$D4-2.4)")
ffmpeg -y -v error -i c1.mp4 -i c2.mp4 -i c3.mp4 -i c4.mp4 -i c5.mp4 -filter_complex "[0][1]xfade=transition=fade:duration=0.6:offset=$O1[a];[a][2]xfade=transition=fade:duration=0.6:offset=$O2[b];[b][3]xfade=transition=fade:duration=0.6:offset=$O3[c];[c][4]xfade=transition=fade:duration=0.6:offset=$O4,fade=t=out:st=$(python3 -c "print($D1+$D2+$D3+$D4+$D5-2.4-1.0)"):d=1.0" -c:v libx264 -preset fast -crf 20 -an video.mp4
# áudio: cada narração começa no início da sua cena (cena N começa em soma(D)-0.6*(N-1))
S2=$(python3 -c "print(int(($D1-0.6)*1000))"); S3=$(python3 -c "print(int(($D1+$D2-1.2)*1000))"); S4=$(python3 -c "print(int(($D1+$D2+$D3-1.8)*1000))"); S5=$(python3 -c "print(int(($D1+$D2+$D3+$D4-2.4)*1000))")
ffmpeg -y -v error -i n1.mp3 -i n2.mp3 -i n3.mp3 -i n4.mp3 -i n5.mp3 -filter_complex "[0]adelay=400|400[a0];[1]adelay=$S2|$S2[a1];[2]adelay=$S3|$S3[a2];[3]adelay=$S4|$S4[a3];[4]adelay=$S5|$S5[a4];[a0][a1][a2][a3][a4]amix=inputs=5:normalize=0,loudnorm=I=-16:TP=-1.5" -ar 48000 narr.m4a
ffmpeg -y -v error -i video.mp4 -i narr.m4a -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart clube-2min.mp4
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height -of csv=p=0 clube-2min.mp4; ls -la clube-2min.mp4
