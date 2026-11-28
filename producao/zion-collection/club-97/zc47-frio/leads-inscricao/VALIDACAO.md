# ZION COLLECTION | LEADS | INSCRIÇÃO PLATAFORMA · validação (28/11) · TUDO PAUSADO

## IDs
- Campanha `120250619219380016` · Cadastros · ABO · pausada
- Conjunto 01 Público aberto `120250619220460016` · R$ 30/dia · Brasil 25–65 · Advantage+ público OFF · pausado
  - V15 `120250619229810016` · V12B `120250619230000016` · Carrossel campeão `120250619230960016`
- Conjunto 02 Lookalike 1% `120250619221780016` · R$ 30/dia · LAL `120250593921040016` ("Público similar (1%) - Público Top Collection campeão", Brasil) · Advantage+ OFF · expansão de lookalike e de personalizado = 0 · pausado
  - V15 `120250619234630016` · V12B `120250619235230016` · Carrossel campeão `120250619235470016`
- Formulário novo `1341552788042214` "ZC2 | Desenvolvimento e Expansão | Inscrição Plataforma V1" (maior intenção, PT-BR). Formulários antigos preservados.

## Criativos (iguais nos dois conjuntos)
- V15: vídeo `2731168944058732` (mesmo do anúncio campeão `120250607482070016`); V12b: vídeo `1474732087451477` (mesmo do `120250607539490016`).
- Carrossel campeão: os 7 cartões originais `docs/ads/zc47-carrossel/zc47-card-1..7.png` (os mesmos do anúncio `120250606477690016`), por URL pública; títulos dos cartões escritos a partir das artes. O criativo `1417382006855324` não pôde ser reaproveitado porque leva o formulário antigo (Land Bank).
- Texto único, título "Seu terreno pode ser o próximo destino da Zion", botão "Cadastre-se", formulário novo, posicionamentos automáticos, otimização por cadastro.

## Formulário: o que está nele
Introdução (texto do comando) + 12 perguntas com as alternativas do comando + nome, telefone, e-mail. Pergunta 12 diz "R$ 47 (pagamento único)": confirmado no ClickMax (oferta 668391e7 não recorrente, Pix/cartão à vista).
Botão final: abre `https://wa.me/5548988729883` (+55 48 98872-9883) com a mensagem "Olá! Preenchi o formulário Zion Collection e quero fazer minha inscrição na plataforma."
Política de privacidade: página "Privacidade Zion Land Members" (GitHub Pages, verificada). `zionhotelgroup.com/privacidade` não pôde ser conferida daqui.

## Pendências e divergências (antes de ativar)
1. **Público aberto × regra permanente** de Bruno ("nenhuma campanha com público totalmente aberto"). O conjunto 01 foi criado como o comando pede, pausado; precisa de decisão explícita.
2. **Tela final:** o conector não permite escrever o texto da tela de agradecimento nem o rótulo do botão (fica o padrão do Meta, com o botão levando ao WhatsApp). O Meta não deixa editar formulário depois de criado: para ter o texto "Queremos conhecer seu terreno…", duplicar o formulário no Gerenciador, editar a tela final e trocar nos 6 anúncios.
3. **WhatsApp 9883 não é canal do ClickMax** (MAPA_AUTOMACOES: canal 01 = final 1061 no ClickMax; 98872-9883 = link wa.me fora do ClickMax). Se a Zaya roda no ClickMax, ela não responde no 9883. Confirmar onde a Zaya atende.
4. **Integração Meta → ClickMax:** existe a automação "TAG AUTOMÁTICA · PREENCHEU FORMULÁRIO (META)" (16 execuções). Conferir no ClickMax se o formulário novo está ligado à integração e se as 12 respostas chegam; só um lead de teste comprova.
5. **Classificação A/B/C/D no CRM:** regras propostas abaixo; criar ou ativar automação no ClickMax depende do "aprovado" de Bruno.
6. **Lead de teste:** ferramenta de teste do Meta (developers.facebook.com/tools/lead-ads-testing) com o login de Bruno.
7. **Rastreamento de pagamento:** pagamentos chegam ao ClickMax pela Ticto (não Asaas) na oferta 668391e7; nenhuma venda real até 28/11 (só o teste reembolsado). Purchase ainda não chega ao Meta (Etapa B/C).
8. **Orçamento:** Collection R$ 60/dia (30 + 30). Hoje ainda estão ativas outras campanhas (B formulário, C3/C4 carrosséis, Land Bank Diagnóstico, Zion Investors ×2); as pausas seletivas ficam com o ChatGPT, como no comando.

## Classificação proposta (respostas → perfil)
- **A · Alta intenção e capital próprio:** Q01 com terreno/operação + Q08 ≥ "Até R$ 50 mil" + Q10 "Sim, compreendo e quero participar" + Q12 "Sim, quero realizar minha inscrição agora".
- **B · Propriedade com potencial de parceria:** Q01 com terreno + Q08 "Tenho o terreno, mas não tenho capital" + Q10 sim + Q12 sim (agora ou conhecer primeiro).
- **C · Interessado em formação:** Q10 ou Q12 = "Sim, …conhecer a plataforma primeiro", ou Q09 = "Adquirir conhecimento…".
- **D · Baixa intenção:** Q10 "Não tenho interesse", ou Q11 "Não estou disposto", ou Q12 "Não estou disposto a investir".

## Correção estratégica (28/11) · conjunto 01
| | Antes | Depois |
|---|---|---|
| Nome | ZC \| INSCRIÇÃO \| 01 PÚBLICO ABERTO \| BR 25-65 | 01 \| PÚBLICO HISTÓRICO CAMPEÃO \| BRASIL |
| Local | Brasil (moradores e recentes) | igual |
| Idade | 25–65 | igual |
| Detalhado | nenhum (aberto) | 1 grupo flexible_spec: interesse Investimentos imobiliários 6003446239080 · cargo Empresário 108611555829523 · comportamentos Frequent international travelers 6022788483583 e Recently Detected iPhone 14 Devices 6320095650783 (mesmo grupo dos conjuntos 120248809131940016, 120250113155280016, 120250521780340016 e 120250522198120016) |
| Advantage+ público | desligado | desligado |
| Posicionamentos | automáticos | automáticos (iguais ao conjunto 02) |
| Orçamento | R$ 30/dia | R$ 30/dia |
O Meta aceitou os 4 critérios (ainda disponíveis). Conjunto 02, anúncios, criativos e formulário sem alteração. Tudo pausado.

## Atendimento (correção de Bruno)
Zaya não existe mais; a agente é a Bela. +55 48 98872-9883 = equipe comercial humana, fora do ClickMax (não conectar).
Frente 01: formulário → botão final → WhatsApp 9883 → equipe humana → inscrição. Frente 02: formulário → ClickMax CRM → Bela (complementar).
Evitar abordagem dupla (proposta, depende de "aprovado"): etiqueta "Em atendimento humano · 9883" no lead; a Bela só aborda leads sem essa etiqueta e com espera de algumas horas após o cadastro.
