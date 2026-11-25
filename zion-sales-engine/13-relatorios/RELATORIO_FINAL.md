# Auditoria crítica de conversão e vendas · Zion Collection 2
Data: 25/11/2026 · Modo: somente leitura (nenhuma campanha, página, checkout, pixel, automação ou CRM foi alterado pela auditoria) · Conta Meta 1271873041294684
Fontes: A_anuncios.md, B_paginas_checkout.md, C_pixel_capi.md, D_vendas_leads_financas.md (mesma pasta). [E] = evidência lida; [H] = hipótese.

Observação de transparência: antes da ordem de congelar, o bloco "O que você recebe em cada etapa" foi publicado em /inscricao-47, /inscricao-curta, /parceiro-zion e /mini-mentoria (01:37Z de 25/11). A auditoria leu a versão no ar. Bruno autorizou essa mudança antes do congelamento.

---

## 1. Resumo executivo
- Em 24/11 a conta gastou ~R$ 152 (parcial no cache) e o ClickMax registrou **2 vendas reais, ambas R$ 97 (Pix)**. O Meta registrou **0 compras** em todas as campanhas. [E]
- **Nenhuma campanha otimiza para compra.** A venda direta otimiza InitiateCheckout; a LT47 otimiza ViewContent, evento que **não dispara** (as páginas têm ViewContent desligado, Meta mostrou 0). [E]
- O "iniciou checkout" do Meta **dispara ao carregar o checkout embutido**, sem clique: acompanha as visitas (89 LPV / 96 IC). Não mede intenção. [E: código + dados]
- As 2 vendas reais **não têm UTM**: impossível atribuir criativo ou campanha. [E]
- O ClickMax **não enxerga** o que acontece dentro do checkout da Ticto (recusa, Pix expirado, abandono). O gateway é **Ticto, não Asaas**. [E]
- O tráfego pago tem sujeira: ~40% dos visitantes de 24/11 eram tráfego de servidor (sessão ≤3 s); Audience Network consome a maior parte do gasto dos melhores vídeos com CPM de R$ 240–268. [E/H]
- Os textos das páginas e os preços não estão alinhados com os anúncios: a campanha rotulada "R$ 97" leva a uma página de R$ 47; páginas abrem como "cadastro de parceiro", não como compra. [E]

## 2. Mapa das campanhas e destinos (ativas em 24/11)
| Campanha | Anúncios | Otimiza | Destino | Preço que cobra |
|---|---|---|---|---|
| [VENDAS][PLATAFORMA R$97] 120250538576770016 | 5 ativos (3 prospecção, 2 remarketing) | INITIATED_CHECKOUT, pixel 903918118859018 | /inscricao-47 (os 2 "curta" em /inscricao-47#pagar) | **R$ 47** (rótulo diz R$ 97) |
| FORM R$ 47 DIRETO 120250557420830016 | 2 | LEAD_GENERATION (formulário nativo 1162157206297031, sem pixel) | formulário → página R$ 47 | R$ 47 |
| LT47 120250557994600016 | 5 | CONTENT_VIEW (evento que não dispara), Advantage Audience | /parceiro-zion | R$ 47 |
Pausadas com gasto recente: formulário R$ 270 (~R$ 209 em 7 dias), Land Bank, Urubici, Floripa, Curso Terreno R$ 47. Posicionamentos são todos automáticos. Nenhuma campanha otimiza para Purchase.

## 3. Funil real
24/11, ClickMax (projeto): 321 visitantes (183 BR, 140 US = tráfego de servidor, 0 lead, 0 compra) → 283 "initiate_checkout" (evento de carregamento) → 4 Pix gerados → 4 pagos (2 reais, 2 testes do Bruno).
Conversão visita → Pix: 0,62% sem testes (2/321); 1,09% só Brasil. Pix gerado → pago: 100%.
Captação R$ 270 (22–24/11): 85 leads Meta → 80 no CRM (94%) → 80 mensagens de abertura (74 entregues, 6 falhas) → nenhuma venda atribuível. A maior perda está entre a leitura da abertura e o pagamento (não rastreável) e entre a visita e o Pix.

## 4. Landing pages
| Página | Oferta / preço | O que o cliente vê |
|---|---|---|
| /inscricao | R$ 97 | frases "receber investimentos na sua área"; sem bloco novo |
| /inscricao-curta | R$ 97 | abre como cadastro de parceiro, sem preço no topo, "tenha acesso a possibilidades de parceria e investimento" |
| /inscricao-47 | R$ 47 | H1 "Queremos te conhecer… Seja um parceiro Zion", sem preço no topo, "vamos agendar uma conversa" (contradiz "sem reunião") |
| /parceiro-zion | R$ 47 | promessa "Aprenda o passo a passo", 70 aulas, 12 meses, prints reais; sem preço na 1ª dobra |
| /mini-mentoria | R$ 47 (produto próprio) | mais clara; preço na 1ª dobra do celular |
| /inscricao-dossie | R$ 47 | igual /inscricao-47; quase sem tráfego |
Todas respondem 200, sem redirecionamento, CTAs em #pagar, #pagar rola ao checkout no celular, UTMs chegam ao iframe, sem R$ 270/R$ 970 e sem cruzamento de preço. Nenhuma usa "login/senha"; nenhuma mostra exemplo de entregável preenchido; títulos internos com "(Copy)". [E]
Entrega: as ofertas de R$ 97 e R$ 47 entregam as mesmas duas turmas (a R$ 47 não é produto diferente); só a Mini Mentoria entrega só a turma nova.

## 5. CTAs
Todos os anúncios de site usam LEARN_MORE ("Saiba mais"); o Carrossel C do formulário R$ 47 usa SIGN_UP. Botões das páginas: "FAÇA A SUA INSCRIÇÃO" (/inscricao-47, /inscricao-curta), "QUERO COMEÇAR MEU PROJETO"/"QUERO ME INSCREVER AGORA" (/parceiro-zion), "QUERO TRANSFORMAR MEU TERRENO" (/mini-mentoria). Alinhamento parcial: "Saiba mais" leva a páginas que pedem inscrição e pagamento; pior nos 2 anúncios que caem direto em #pagar. O botão do anúncio vem de lista fixa do Meta; o texto personalizado vai na arte e na landing. Hipóteses de teste (não aplicadas): Saiba mais × Cadastre-se × Comprar agora × Acessar agora × Começar meu projeto. [H]

## 6. Pixel e CAPI
Provado [E]: as 4 páginas-mãe não têm fbevents.js/fbq/GTM; só o rastreador do ClickMax (/__clickmax/tr: page_view e scroll). O pixel 903918118859018 roda no iframe de pagamento. InitiateCheckout dispara na inicialização do checkout (sem clique; confirmado pelo código e pela documentação do ClickMax). IC não tem trava de uma vez por carregamento (duplicidade possível por desenho; não observada). Código embutido chama fbq Purchase ao gerar Pix/boleto/cartão (contradiz a documentação "compra aprovada"); está dormente na página-mãe. ViewContent desligado nas 4 páginas. Valor pode chegar dividido por 100 duas vezes se o iframe usar o postMessage.
Meta 24/11: venda direta R$ 69,98 · 125 cliques · 89 LPV · IC 96 · AddPaymentInfo 2 · Purchase 0. LT47 R$ 16,98 · 34 cliques · 24 LPV · IC 24 · Purchase 0. Form R$ 47 R$ 10,64 · 0 LPV.
Hipóteses [H]: Purchase pode estar saindo no Pix gerado dentro do iframe; CAPI pode estar sem token/desligada (nenhuma ferramenta mostra); ClickMax registra 2 purchase_approved e Meta 0.
Não verificável aqui: o que o iframe dispara de fato e o que a Meta recebeu (proxy bloqueia payments.clickmax.io). Verificação proposta na seção 13.

## 7. Checkout
Não verificado: o domínio de pagamento retorna 403 neste ambiente. Verificado: iframe presente com o hash certo em todas as páginas; carga da página 0,9–1,7 s; sem exceção JavaScript. Não verificado: campos obrigatórios, validação, Pix e cartão na tela, preço final com taxas, selos de confiança, redirecionamento pós-pagamento, e-mail de acesso. A compra real de teste do Bruno (Pix R$ 47, 24/11 19:12Z) existe, mas sem registro de observação da tela. O checkout ainda não redireciona para /obrigado-plataforma (pendência de painel).

## 8. Conciliação ClickMax × gateway
Gateway: **Ticto** em todas as ofertas e vendas. Asaas só aparece em um fluxo rascunho sem execuções.
Vendas 20–25/11: 8 registros (nenhum pendente, recusado, cancelado ou reembolsado): 2 reais R$ 97 Pix (24/11 17:48Z e 18:07Z), 5 pagos + 1 falho do Bruno (testes). R$ 97: 3 pagas; R$ 47: 1 (teste); Mini Mentoria: 0.
UTM/anúncio: 0 das 2 vendas reais têm UTM. Se a causa é a URL do anúncio sem UTM ou a Ticto não devolver, não foi determinado.
O ClickMax só recebe da Ticto o que ela repassa: abandono/recusa/Pix expirado ficam invisíveis. Falta o extrato da Ticto (22–25/11).
Tags de compra/abandono/Pix não pago: 0 leads. Fluxos de pós-compra, Pix não pago e abandono do R$ 97: rascunho, 0 execuções. Os 2 compradores têm usuário de membros criado; não sei se o e-mail de acesso chegou.

## 9. Jornada dos leads (22–24/11)
Formulário R$ 270: 85 leads → 80 no CRM (80 únicos). Abertura: 80 envios, 46 visualizadas, 26 entregues, 2 enviadas, 6 falhas (códigos Meta 130472 e 131026). Bela: ~27–30 conversas, 92 decisões, 6 passagens a humano, 4 erros de provedor, 0 follow-ups. Só 14 visitantes chegaram pela utm inscricao-270 (esse lead vem pelo WhatsApp).
Incoerência de mensagem: 53 leads receberam abertura com R$ 270 e "sessão de 45 min com Bruno"; 27 receberam R$ 97 e "sem reunião". A Zaya continua ativa com reunião grátis e sem preço, no mesmo número da Bela. O fluxo "Club 97 · Nova oportunidade" usa "Seja um parceiro Zion".
Formulário R$ 47 direto: 0 leads no Meta; 1 no facebook_leads (25/11 01:42Z).
[H] Formulários antigos da conta citam R$ 350 mil de faturamento por bubble e rentabilidade de 30–35% a.a.; não foi confirmado se estão em anúncios ativos.

## 10. Engenharia financeira
Taxas comprovadas: R$ 19 e R$ 47 pagam R$ 2,49 fixos; R$ 97 paga R$ 9,27; R$ 270 paga R$ 21,36 (batem com 6,99% + R$ 2,49: inferência). Cartão: sem dado.
Líquido: R$ 47 → R$ 44,51; R$ 97 → R$ 87,73.
Margem de contribuição = líquido − i × preço − c (i = imposto, c = custos variáveis; produto digital marginal; imposto e custos de WhatsApp/IA sem valor definido). CPA máximo com i=0 e c=0: R$ 44,51 (R$ 47) e R$ 87,73 (R$ 97). Equilíbrio: 1 venda por R$ 44,51 / R$ 87,73 investidos.
Gasto Meta 22–24/11: R$ 341,63 (captação R$ 270: R$ 209,71 → R$ 2,47/lead; venda direta 24/11: R$ 69,95; LT47: R$ 16,96; form R$ 47: R$ 10,48; Curso Terreno R$ 47 22/11: R$ 34,53).
CAC real: não comprovável sem UTM. Cenários (hipótese): R$ 34,98 se as 2 vendas vieram da venda direta; R$ 104,86 se da captação; R$ 78,66 com todo o gasto de 24/11; R$ 170,82 com todo o gasto de 22–24/11. Resultado de mídia 22–24/11: −R$ 166,17 (i=0, c=0).
Custo por visita BR: R$ 0,86. Custo por Pix gerado: R$ 39,33 com testes, R$ 78,66 sem.
Simulação (rotulada): cobrir R$ 209,71 da captação exige 3 vendas de R$ 97 (2,8% dos 85 leads) ou 5 de R$ 47 (5,5%).

## 11. Problemas por prioridade
**P0 (impedem comprar ou comprometem o rastreamento)**
1. Meta sem sinal de compra. Evidência: 2 vendas reais, Meta 0; vendas sem UTM; nenhuma campanha otimiza Purchase. Causa: comprovada (sem UTM/atribuição) + hipótese (CAPI). Impacto: algoritmo não aprende, CAC incomprovável. Correção: UTM por anúncio garantida, evento de intenção real, CAPI com event_id. Esforço: médio. Validação: Testar eventos + venda com UTM.
2. LT47 otimiza ViewContent, que não dispara. Evidência: pixelViewContent false, Meta 0 ViewContent. Causa: comprovada. Impacto: entrega sem aprendizado. Correção: ligar ViewContent ou trocar objetivo. Esforço: baixo. (Risco que já havia sido sinalizado antes da ativação.)
3. Ponto cego do checkout (Ticto). Sem recusa/Pix expirado/abandono, não se sabe se há atrito de pagamento. Correção: extrato Ticto + teste real. Esforço: baixo (Bruno).
4. Pós-compra todo em rascunho: compradores recebem acesso, mas sem e-mail, tag, card ou tarefa. Correção: validar e ligar com "aprovado". Esforço: médio.
**P1 (perda alta de conversão)**
5. IC dispara no carregamento: custo por checkout e funil do Meta inflados. Causa comprovada. Correção: otimizar por evento de intenção.
6. Audience Network: 75% e 86% do gasto dos Vídeos 02 longa e curta, CPM ~R$ 240–268, CTR improvável. Causa: provável. Correção: excluir/posicionamento manual (precisa de "aprovado").
7. Tráfego de servidor ~40% das visitas distorce taxa de conversão. Correção: filtrar na análise.
8. Rótulo "R$ 97" × destino R$ 47; entrega igual nas duas ofertas. Correção: alinhar nomes e decidir o que cada preço entrega.
9. Páginas abrem como "cadastro de parceiro", sem preço e sem prova tangível no topo. Correção: promessa específica ("Aprenda o passo a passo") e preço na 1ª dobra (como /mini-mentoria).
10. Mensagens incoerentes (R$ 270/"45 min com Bruno" × R$ 97 × reunião da Zaya).
11. Sem exclusão de compradores nem do remarketing na prospecção.
**P2 (clareza e experiência)**
12. "Agendar uma conversa" em /inscricao-47 e /inscricao-dossie contradiz "sem reunião".
13. Frases que podem soar como garantia de capital/investidor ("receber investimentos na sua área", "possibilidades de parceria e investimento").
14. Sem "login/senha" explicados nem exemplos de entregável preenchido.
15. Títulos internos com "(Copy)"; oferta 74a3f8c6 chamada "Mini Mentoria" no produto errado.
16. CTA "Saiba mais" vs páginas de inscrição e pagamento.
**P3**
17. Testes de CTA; countdownjs@latest sem versão fixa; Jost/Google Fonts não verificado.

## 12. Plano de ação recomendado (nada aplicado; só após consenso)
1. Medição primeiro: (a) conferir no Gerenciador de Eventos o que o iframe dispara; (b) extrato da Ticto; (c) garantir UTM em todos os anúncios e sua gravação na venda; (d) decidir evento de otimização (intenção ou compra) e CAPI.
2. Teste real de compra (celular, Pix e cartão, com reembolso) por oferta que recebe tráfego.
3. Limpeza de mídia: excluir Audience Network, excluir compradores, rever o conjunto da LT47.
4. Alinhar oferta e promessa: um preço, um nome e uma entrega por campanha; resolver o rótulo "R$ 97".
5. Páginas: promessa específica e preço na 1ª dobra; remover "agendar conversa" onde não existe reunião; revisar frases de capital/investimento.
6. Mensagens: unificar Bela/Zaya/abertura com a oferta vigente.
7. Só então escalar orçamento.

## 13. Perguntas que dependem de Bruno
1. Autoriza uma compra real de teste (e reembolso) por oferta? Ou prefere só enviar prints do checkout?
2. Pode puxar o extrato da Ticto de 22 a 25/11 (todos os status, recusas, UTMs)?
3. Pode abrir Gerenciador de Eventos > Testar eventos e enviar o resultado (PageView/IC no carregamento; Purchase no Pix gerado; token CAPI)?
4. Mantém a LT47 ligada enquanto otimiza ViewContent (evento que não dispara), ou pausa até corrigir?
5. Autoriza excluir Audience Network e excluir compradores (campanhas existentes)?
6. R$ 97 e R$ 47 devem entregar coisas diferentes? Qual preço fica como oferta principal?
7. Autoriza revisar o texto da Bela e da Zaya e ligar os fluxos de pós-compra (depois de teste)?
8. Os formulários antigos com "R$ 350 mil por bubble" estão em anúncios? Se sim, pausar?

## Resposta à pergunta central
Não estamos vendendo porque o cliente não deseja, não compreende, tem dificuldade para pagar, ou porque o sistema não registra? **O que está provado:** o sistema não registra nem otimiza por compra (2 vendas reais, Meta 0, sem UTM, evento errado) e o funil do Meta mede carregamento, não intenção. **O que está sugerido por evidência:** a oferta é pouco clara nas páginas que recebem tráfego (abrem como cadastro de parceiro, sem preço no topo; rótulo e destino não batem). **O que não dá para afirmar:** dificuldade de pagamento (a Ticto não repassa) e falta de desejo (amostra de 2 vendas em 183 visitantes reais do Brasil não permite concluir). A causa mais provável é uma combinação de medição quebrada com oferta/entrada pouco clara; a hipótese "ninguém quer" não tem evidência a favor nem contra.
