# MÉTODO ZION 360° · deck de 19 slides (rascunho local)

Construído em 16/11/2026 a partir dos artefatos "ZION 360" e "Clube Zion Collection" e do site institucional. Nada publicado, nada enviado, nenhum sistema existente alterado. Abrir: `apresentacao/index.html` (setas ou toque; N mostra as notas do apresentador).

## Ordem
1 Capa · 2 Zion · 3 Bruno · 4 Cases (fotos reais) · 5 Dados reais · 6–10 ECROI (espelhamento, confronto, reconhecimento, orientação, implementação) · 11–12 jornada 3D · 13 troféu + dossiê · 14 sete conquistas / 20 entregáveis · 15 cenário hipotético · 16 o que o Clube é e não é · 17 oferta · 18 próximo passo · 19 fechamento. (O slide de faixas públicas de custo saiu em 16/11/2026, por decisão de Bruno: só 1 de 6 linhas tinha fonte. Ver BRIEFING_PESQUISA_SLIDE16.md.)

## Testes (`tests/test_deck.js`, Playwright, executado)
19 slides; contador e navegação em desktop e celular; cena 3D reage ao clique; slide 14 soma 20; sem erro de página ou recurso; sem "ZAI 360", "155.000", "69%" ou "49.000". Capturas em `tests/shots/`.
Aviso conhecido: no celular em pé, slides 9, 10 e 12 têm elementos além da borda (deck é 16:9, pensado para tela cheia ou projeção).

## O que NÃO é verdade ainda (para Bruno decidir)
1. **3D:** não existe motor 3D no repositório, no Lovable nem nos artefatos. A jornada é uma cena em CSS 3D (isométrica, 7 pontos). Se existir outro sistema 3D, preciso do acesso.
2. **Slide 14:** resolvido. Bruno validou em 16/11/2026 a lista de 20 entregáveis (3+3+3+3+3+3+2) derivada do campo "no Clube" de cada pilar do artefato.
3. **Faixas de custo:** slide removido (decisão de Bruno, 16/11/2026). Valores só voltam com fonte, data, escopo e comparabilidade, conferidos por Bruno.
4. **Slide 17 (oferta):** resolvido em 16/11/2026. Bruno aprovou a narrativa e o parcelamento em 12x. O slide mostra 12x de R$ 80,83, valor total R$ 970 e 12 meses de acesso (970 ÷ 12 = 80,83 arredondado), sem dizer "sem juros". A decisão de 11/11 de não mostrar o R$ 970 em páginas, anúncios e mensagens fica suspensa só para este deck; para página, anúncio e mensagem vale a aprovação específica de cada peça.
5. **Slides 2 e 5:** números (+23 destinos, notas Booking/Airbnb/Expedia/Google, 260 mil seguidores) vêm do site. Conferir data antes de usar.
6. **Escopo do pilar 6:** parceria aparece só como alternativa, "Zion pode ser a primeira possível parceira", sem garantia. Revisão jurídica (CVM/LGPD) antes de usar com leads.
