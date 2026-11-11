# Vídeo de 2 minutos · Zion Collection Club (versão 3, 11/11/2026)

Foco: a dor e o troféu, não o processo. Sem preço. Duração: 71 s. Narração provisória sintética (edge-tts, pt-BR-AntonioNeural); para trocar pela voz do Bruno, gravar os cinco blocos como n1..n5.mp3 e rodar `build2.sh`.

| # | Cena | Narração |
|---|---|---|
| 1 | Trecho do filme oficial · "Referência em glamping no Brasil" | Com mais de vinte anos no mercado internacional e cinco anos no Brasil, desde 2020, a Zion é referência no setor de glamping no país. Estamos buscando novos parceiros e pessoas que queiram entrar nesse setor e aprender a faturar com hospedagem. |
| 2 | Foto real da bolha · "O que falta é o caminho" (dor) | Você tem o terreno, a vontade e a ideia. O que falta é o caminho: por onde começar, com quem contar e como transformar isso em um destino que recebe hóspedes e gera receita. |
| 3 | Quatro cartões: conhecimento, melhores produtos, acesso a investimentos, parcerias e investidores (troféu) | Dentro do Zion Collection Club você ganha o que precisa para chegar lá: conhecimento, acesso aos melhores produtos do mercado, acesso a investimentos e a possibilidade de fazer parcerias e receber investidores. O seu terreno entra no Radar do Land Bank, e o capital pode vir da própria Zion ou do pool de investidores que a Zion reúne. |
| 4 | Mapa do Brasil com bolhas + foto do Bruno · "O maior clube de glamping do Brasil" | O nosso clube é o maior clube de glamping do Brasil, referência no setor. A Zion está em busca dos melhores destinos por todo o país. O seu pode ser o próximo destino da nossa expansão. |
| 5 | Foto noturna · "Transforme seu terreno em um destino turístico" | Entre para o clube. Transforme seu terreno em um destino turístico e faça parte dessa oportunidade. |

Decisões do Bruno (11/11): "melhores produtos do mercado", "referência", "acesso a investimentos" e "maior clube de glamping do Brasil" entram como ele pediu; usei "clube" no lugar de "comunidade". "Pode vir" (capital) e "possibilidade" (parcerias) ficam para não prometer resultado.

Como gerar: `python3 -I scenes3.py <pasta com page.html> <raiz do repo> <saída> wide|tall` → capturas Playwright (cena 1 com fundo transparente) → `bash build2.sh w 1920x1080 clube-2min.mp4` e `bash build2.sh t 1080x1350 clube-2min-4x5.mp4`.
