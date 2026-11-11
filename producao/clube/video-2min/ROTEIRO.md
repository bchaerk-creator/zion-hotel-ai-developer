# Vídeo de 2 minutos · Zion Collection Club

Estrutura (espelho → quebra de crença → prova → mecanismo → próximo passo). Duração: 74 s. Narração provisória sintética (edge-tts, pt-BR-AntonioNeural); trocar pela voz do Bruno gravando os cinco blocos abaixo e rodando `build.sh` com os novos n1..n5.mp3.

| # | Cena | Narração |
|---|---|---|
| 1 | Foto real da bolha (op08) | Você tem o terreno. Já imaginou as cabanas, a pousada, a bolha no meio da mata. E parou na mesma pergunta de todo mundo: de onde vem o dinheiro? |
| 2 | Trecho do filme oficial, escurecido | Investidor não coloca dinheiro em terreno. Coloca em projeto que ele entende. Terreno parado não é falta de capital. É falta de projeto no papel. |
| 3 | Mapa do Brasil com bolhas + Urubici/Florianópolis + foto do Bruno | A Zion desenvolve, gere e opera hospedagens desde 2020, em Urubici e Florianópolis, e está desenvolvendo mais de 23 destinos pelo Brasil. O caminho que ensinamos é o que usamos nas nossas unidades. |
| 4 | Cinco cartões (potencial, modelo, números, proposta, apresentação) | São cinco etapas, nesta ordem: potencial do terreno, modelo de hospedagem, números, proposta e apresentação. Cada etapa produz um documento. No fim, o seu Dossiê, pronto para um sócio, um investidor ou a própria Zion olhar. |
| 5 | Foto noturna + bloco de oferta (2x de R$ 48,50 / R$ 97) | No Zion Collection Club você aprende as cinco etapas, inscreve o seu terreno no Radar do Land Bank e faz a sessão estratégica com a nossa equipe. Duas vezes de quarenta e oito e cinquenta. Entre para o clube. Seja você o próximo destino. |

Como gerar: `python3 -I scenes.py <pasta> <raiz do repositório>` → capturas Playwright 1920×1080 → `bash build.sh` (ffmpeg). Sem promessas de resultado; "mais de 23 destinos" vem do próprio texto da landing.
