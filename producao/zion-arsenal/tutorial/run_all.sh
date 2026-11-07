#!/bin/bash
# Gera voz e grava os tutoriais (3 em paralelo). Log em out/tutoriais/log-<ID>.txt
cd /home/user/zion-arsenal
one(){ id=$1; /tmp/claude-0/-home-user-zion-hotel-ai-developer/312d9b1e-220b-5865-9c6e-31457236f0ae/scratchpad/tts/venv/bin/python tutorial/tts.py tutorial/$id.json /tmp/claude-0/-home-user-zion-hotel-ai-developer/312d9b1e-220b-5865-9c6e-31457236f0ae/scratchpad/wav-$id /tmp/claude-0/-home-user-zion-hotel-ai-developer/312d9b1e-220b-5865-9c6e-31457236f0ae/scratchpad/voz/vits-piper-pt_BR-faber-medium/pt_BR-faber-medium.onnx /tmp/claude-0/-home-user-zion-hotel-ai-developer/312d9b1e-220b-5865-9c6e-31457236f0ae/scratchpad/tts/venv/bin/piper > out/tutoriais/log-$id.txt 2>&1 && timeout 900 node tutorial/record.js $id /tmp/claude-0/-home-user-zion-hotel-ai-developer/312d9b1e-220b-5865-9c6e-31457236f0ae/scratchpad/wav-$id >> out/tutoriais/log-$id.txt 2>&1; echo "$id fim $?"; }
export -f one
printf '%s\n' "$@" | xargs -P 3 -I{} bash -c 'one {}'
