# Vídeo de 2 minutos · Zion Collection Club (versão 2, 11/11/2026)

Tema: como o clube funciona e as suas etapas. Sem preço. Duração: 79 s. Narração provisória sintética (edge-tts, pt-BR-AntonioNeural); para trocar pela voz do Bruno, gravar os cinco blocos como n1..n5.mp3 e rodar `build2.sh`.

| # | Cena | Narração |
|---|---|---|
| 1 | Trecho do filme oficial + "O seu destino pode ser o próximo" | A Zion é referência em hospedagens na natureza e em hospedagens de experiência. Desenvolvemos, gerimos e operamos as nossas unidades desde 2020, e estamos em busca dos melhores destinos por todo o Brasil. O seu pode ser o próximo. |
| 2 | Quatro cartões: formação, sessão estratégica, produtos, Radar do Land Bank | O Zion Collection Club é a porta de entrada. Dentro do clube você entende mais sobre o setor, se prepara para ele e tem acesso aos melhores produtos do mercado: a formação, uma sessão estratégica de direcionamento inicial com a nossa equipe e o Radar do Land Bank. |
| 3 | Cinco etapas | Como funciona: em cinco etapas, nesta ordem. Potencial do terreno, modelo de hospedagem, números, proposta e apresentação. Cada etapa produz um documento. No fim, o seu projeto está pronto para ser apresentado. |
| 4 | Mapa do Brasil com bolhas + foto do Bruno | E de onde vem o capital? Com o projeto no radar, ele pode vir da própria Zion, que avalia novas sedes pelo Brasil, ou do pool de investidores e parceiros que a Zion reúne. O clube abre o caminho para o parceiro, o sócio ou o investidor certo. |
| 5 | Foto noturna + "Entre para o clube" (sem preço) | A Zion está em busca dos melhores destinos por todo o Brasil, e o seu pode ser o próximo. Entre para o clube e faça parte dessa oportunidade. |

Observação: "pode vir" e "possíveis investimentos" são de propósito, para não prometer capital. "Melhores produtos do mercado" e "referência" foram decisão do Bruno (11/11).

Como gerar: `python3 -I scenes2.py <pasta com page.html> <raiz do repo> <saída> wide|tall` → capturas Playwright (cena 1 com fundo transparente) → `bash build2.sh w 1920x1080 clube-2min.mp4` e `bash build2.sh t 1080x1350 clube-2min-4x5.mp4`.
