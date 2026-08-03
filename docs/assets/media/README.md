# Mídia do site

## hero.mp4 — vídeo de fundo do hero

Coloque aqui o arquivo `hero.mp4` (ou `hero.webm`) e o site liga o vídeo automaticamente
(com overlay escuro de 55%, conforme brand guideline). Sem o arquivo,
o hero mantém as linhas topográficas animadas.

**Especificação recomendada:**
- Duração: 10 a 25s em loop (sem cortes bruscos entre fim e início)
- Resolução: 1920x1080 (ou 1440x810), sem áudio
- Compressão: H.264, CRF 28-30, ~4-8 MB
- Conteúdo: drone lento sobre a operação, bubble ao anoitecer, natureza

**Receita ffmpeg:**
```
ffmpeg -i original.mp4 -t 20 -vf "scale=1920:-2" -an -c:v libx264 -crf 29 -preset slow -movflags +faststart hero.mp4
```

Sugestões do Drive da Zion: "Urubici Bubble Night - Vários.mov",
"ZION GLAMPING COLLECTION.mp4" ou os clipes de drone de julho/2026.
