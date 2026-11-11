set -e
# uso: buildN.sh <dir> <WxH> <saida> <offset do filme em s>
D=$1; SZ=$2; OUT=$3; FO=${4:-20}; W=${SZ%x*}; H=${SZ#*x}; P=0.7
mapfile -t DUR < <(python3 -c "import json;[print(round(x+$P,2)) for x in json.load(open('dur.json'))]")
N=${#DUR[@]}
Z="x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=${SZ}:fps=30"
ffmpeg -y -v error -ss $FO -t ${DUR[0]} -i ../filme.mp4 -i $D/s1.png -filter_complex "[0:v]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,eq=brightness=-0.2:saturation=0.85,fps=30[f];[f][1:v]overlay=0:0,format=yuv420p" -an -c:v libx264 -preset fast -crf 20 $D/c1.mp4
for ((i=2;i<=N;i++)); do ffmpeg -y -v error -loop 1 -i $D/s$i.png -t ${DUR[$((i-1))]} -filter_complex "zoompan=z='1+0.0007*in':d=1:$Z,format=yuv420p" -c:v libx264 -preset fast -crf 20 $D/c$i.mp4; done
# xfade em cadeia
INPUTS=""; for ((i=1;i<=N;i++)); do INPUTS="$INPUTS -i $D/c$i.mp4"; done
FILTER=""; prev="[0]"; acc=0; OFFS=()
for ((i=1;i<N;i++)); do acc=$(python3 -c "print(round($acc+${DUR[$((i-1))]}-0.6,2))"); OFFS+=($acc); lab="[x$i]"; [ $i -eq $((N-1)) ] && lab=""; FILTER="$FILTER$prev[$i]xfade=transition=fade:duration=0.6:offset=$acc$lab"; [ -n "$lab" ] && FILTER="$FILTER;"; prev=$lab; done
TOTAL=$(python3 -c "import json;print(round(sum(x+$P for x in json.load(open('dur.json')))-0.6*($N-1),2))")
ffmpeg -y -v error $INPUTS -filter_complex "$FILTER,fade=t=out:st=$(python3 -c "print($TOTAL-1.0)"):d=1.0" -c:v libx264 -preset fast -crf 20 -an $D/video.mp4
# áudio
AIN=""; AF=""; MIX=""; for ((i=1;i<=N;i++)); do AIN="$AIN -i n$i.mp3"; if [ $i -eq 1 ]; then ms=400; else ms=$(python3 -c "print(int(${OFFS[$((i-2))]}*1000))"); fi; AF="$AF[$((i-1))]adelay=$ms|$ms[a$i];"; MIX="$MIX[a$i]"; done
[ -f narr.m4a ] || ffmpeg -y -v error $AIN -filter_complex "${AF}${MIX}amix=inputs=$N:normalize=0,loudnorm=I=-16:TP=-1.5" -ar 48000 narr.m4a
ffmpeg -y -v error -i $D/video.mp4 -i narr.m4a -c:v libx264 -preset medium -crf 24 -c:a aac -b:a 160k -shortest -movflags +faststart $OUT
ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT; ls -la $OUT
