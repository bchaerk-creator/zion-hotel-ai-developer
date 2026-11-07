#!/bin/bash
# Captura telas e grava os vídeos de apresentação (3 em paralelo). Log em out/promo/<ID>/log.txt
cd /home/user/zion-arsenal
one(){ id=$1; mkdir -p out/promo/$id; node promo/shots.js $id > out/promo/$id/log.txt 2>&1 && timeout 600 node promo/make.js $id >> out/promo/$id/log.txt 2>&1; echo "$id fim $?"; }
export -f one
printf '%s\n' "$@" | xargs -P 3 -I{} bash -c 'one {}'
