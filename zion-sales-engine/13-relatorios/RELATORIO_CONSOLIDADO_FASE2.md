# Relatório consolidado · Auditoria técnica (Fase 2) · Zion Collection
Data: 25/11/2026. Modo: somente leitura e planejamento; nada foi alterado por esta etapa. Responsabilidades: Claude = auditoria técnica, infraestrutura, páginas, checkouts, produtos, integrações · ChatGPT = campanhas, tráfego, análise, escala · Bruno = aprovação final.
Evidência marcada [E]; hipótese [H]; não confirmado [NC]. Detalhes por prioridade nos arquivos: H_rastreamento.md, I_inventario_ofertas.md, G_validacao_duas_campanhas.md (criativos), J_paginas_ofertas_checkouts.md, RELATORIO_FINAL.md (fase 1) e HANDOFF_CHATGPT.md.

## 0. Resposta curta
1. Hoje não é possível provar qual anúncio vende: as 2 únicas vendas reais (R$ 97, 24/11) vieram sem UTM e o Meta registrou 0 compras. [E]
2. Nenhuma campanha otimiza para compra, e o evento "iniciou checkout" dispara no carregamento do checkout, não na intenção. [E]
3. R$ 47 e R$ 97 entregam o MESMO conteúdo (mesmo conteúdo 79d3e792: 9 módulos, 70 aulas). Não há diferença real de produto. [E]
4. Anúncios e páginas ativos hoje prometem coisas que a oferta não entrega (reunião, "entrará em contato", "receber investimentos", "parceiro/sócio"). [E]
5. Recomendação: consolidar em UMA oferta (Mini Mentoria R$ 47), corrigir o rastreamento ANTES de otimizar por Purchase, e reduzir o orçamento de R$ 110 para R$ 60/dia em duas campanhas da mesma oferta.

## 1. Prioridade 01 · Rastreamento (resumo; plano completo em H_rastreamento.md)
Estado [E/H]: gateway Ticto por trás do checkout nativo do ClickMax; pixel 903918118859018 (indício) roda no iframe, não nas páginas; ViewContent desligado nas 71 páginas; aba "Eventos de pixel" vazia no workspace (indício de que a CAPI nunca saiu por aqui [H]); token/pixel por oferta ilegíveis por MCP [NC]; código embutido chama Purchase ao gerar Pix e envia valor dividido por 100 duas vezes no postMessage [H, iframe bloqueado]; sem eventID [H]. Pix gerado × pago é distinguível no ClickMax (pending → paid em 51–91 s) [E].
UTM ausente: a causa não é URL de anúncio errada; comprador A comprou por link de WhatsApp sem UTM; comprador B sem origem; a venda grava a URL do momento do checkout. utm_content é o NOME do criativo; faltam utm_term/sck/ad_id/campaign_id/adset (só a LT47 os tinha). [E]
Requisitos e critério de aceite (R1–R8 no arquivo H): Purchase só após pago · value/currency · CAPI · deduplicação · campanha/conjunto/anúncio · UTM persistente · conciliação ≤10% · Pix gerado ≠ pago.
Plano (nada implementado): Fase 0 diagnóstico no painel (Bruno) → Fase 1 corrigir configuração nativa do ClickMax (token CAPI, Purchase navegador+servidor só com pago, IC após dados pessoais, pixel nas ofertas, url_tags padrão com ids, origem nos links de WhatsApp/Bela, tirar #pagar ou pôr UTM antes) → Fase 2 compra real de Bruno + reembolso → Fase 3 otimizar para Purchase (só com aprovado). Se falhar: Opção C, CAPI própria via webhook (event_id = nº do pedido, fbc/fbp). Prazo: reenviar as 2 compras reais ao Meta até 01/12.

## 2. Prioridade 02 · Inventário R$ 47 × R$ 97
| Item | Mini Mentoria R$ 47 | R$ 47 antiga | R$ 97 |
|---|---|---|---|
| Oferta | 0c71eeba (produto cbbb5fb1) | 668391e7 (produto 072083e8) | c298aaed (produto 072083e8) |
| Entrega | só turma nova 087479a3 (portal 3ef7a340) | turma nova + antiga 69345987 | turma nova + antiga |
| Conteúdo | 9 módulos, 70 aulas, 12 meses | idêntico | idêntico |
| Páginas | /mini-mentoria | /inscricao-47, /parceiro-zion, /inscricao-dossie | /inscricao, /inscricao-curta |
| Vendas | 0 | 1 (teste) | 3 (2 reais + 1 teste) |
Diferenças reais: o comprador de R$ 97 recebe só uma segunda porta de acesso (portal antigo) e uma página com promessa maior; nenhum simulador, suporte, comunidade, certificado ou reunião a mais. Os 11 simuladores bônus existem só na turma de R$ 270 e nenhuma oferta atual os entrega. Planilhas "EXEMPLO" não estão ligadas a aulas. A oferta 74a3f8c6 é duplicata sem uso. [E]
Cenários: A) manter R$ 47 e R$ 97 só se houver diferenciação real construída (ex.: bônus simuladores/planilhas exemplo conferidos); B) consolidar em R$ 47 e arquivar R$ 97 (recomendado); C) consolidar em R$ 97 com bônus/rampa. Riscos de B: 2 clientes reais de R$ 97 (manter acesso), mensagem de preço aos leads (exige aprovado), arquivar oferta só depois de confirmar que o acesso dos compradores continua.
Recomendação do auditor: B.

## 3. Prioridade 03 · Inventário dos criativos (detalhe e ids em G_validacao_duas_campanhas.md)
- Pronto para venda direta: MM47-03 (creative_id 4254761594656807); LT47-01 e 02 (4481706062097990, 1704992391203624) com ressalva de frases de parceria.
- Aproveitável com copy nova: vídeos de vendas (1550506153791834, 1690587456078920, 2151933725406637, 1137580725675043, 2474773346265039: tirar "taxa", "agendar conversa", "entrará em contato", "suporte da equipe"); carrosséis 10 A/B (1044622645286567, 1417353493503684); LT47-03/04/05 (1726599222390803, 1143295985331615, 972968655597476); Curso Terreno (3324408417751938, 1851690215857684; destino antigo); Form 47 (2640402549807923, 1143005531761496).
- Edição de vídeo/arte [H, a confirmar]: campeões da captação R$ 270 (2305015426733583, 1171238248662600, 1485278267092837), vídeo de 2 min do clube.
- Incompatível: captação R$ 270 (9 criativos citam R$ 270 e "sessão de 45 min com Bruno"), Land Bank, Parceiro, Urubici/Floripa, clube R$ 97 antigo, versões do Club com reunião semanal e mentor; e-book de julho/agosto citam diária de R$ 1.571, ocupação e Booking (promessa de resultado: incompatível).
- Lacunas: o que os vídeos FALAM não foi verificado (sem transcrição local); várias artes classificadas só por nome/texto; 4 dos 5 anúncios da Mini Mentoria sem creative_id no Windsor (cache). Próximo passo sugerido: ler cada vídeo/arte campeão (Bruno aprova baixar/transcrever).

## 4. Prioridade 04 · Páginas, ofertas e checkouts (detalhe em J_paginas_ofertas_checkouts.md)
71 páginas (62 venda, 4 obrigado, 3 checkout, 1 quiz, 1 captura; 28 publicadas, 43 rascunho); 64 produtos, 67 ofertas; pixelViewContent falso em todas; 17 ofertas com erro de sincronização do gateway (nenhuma ligada a página publicada); hash do checkout bate com a oferta em 27 de 27 páginas publicadas com iframe.
P0: J-01 /curso-terreno-destino-turistico (207 visitas em 7 dias) liga oferta de R$ 47 ARQUIVADA (não vende); J-02 /etapa-desenvolvimento liga oferta de R$ 290 em pending_corrections (preço obsoleto).
P1: J-03 /club e /club/planos com R$ 270/980/2.900 e Asaas (só relatar: regra do Club); J-04 vitrine com 20 links para rascunhos (404); J-05 R$ 47 e R$ 97 com a mesma entrega; J-06 sem pós-compra ativo para as ofertas que vendem.
P2/P3: seis páginas de inscrição clonadas para três ofertas; oferta órfã 74a3f8c6; portal Mini Mentoria de Performance não publicado; title nulo em 69/71; nenhuma página de obrigado ligada a checkout.
Proposta (para aprovação): manter /inscricao-47, /parceiro-zion, /mini-mentoria, /terra-capital-a/b, /obrigado-plataforma; consolidar /inscricao e /inscricao-curta; despublicar /inscricao-dossie, /curso-terreno-destino-turistico, /etapa-desenvolvimento, /club, /club/planos, /zion-collection-club; arquivar ofertas 74a3f8c6 e as obsoletas, e fluxos R$ 270; escolher portal canônico; ativar pós-compra para as ofertas vigentes.

## 5. Prioridade 05 · Economia e consolidação (R$ 110 → R$ 60/dia)
Hoje ligado (R$ 110/dia): Mini Mentoria R$ 30 (tráfego/LPV) + venda direta "R$ 97" R$ 50 (vende R$ 47; copy com "agendar conversa"; Audience Network consome a maior parte) + formulário R$ 47 R$ 30 (1 lead).
Proposta de configuração (duas campanhas, UM produto):
- Campanha 01 · Mini Mentoria carrosséis (5 narrativas): R$ 30/dia.
- Campanha 02 · Mini Mentoria vídeos campeões (Vídeo 02 curta e longa, copy reescrita sem taxa/reunião/contato, destino /mini-mentoria, UTM completa): R$ 30/dia, substitui a venda direta antiga.
- Pausar: venda direta antiga (R$ 50), formulário R$ 47 (R$ 30). Total R$ 60/dia (−R$ 50/dia).
- Campanha "R$ 97" separada não se justifica enquanto o conteúdo for idêntico; só faria sentido com diferenciação real (cenários A/C).
- Otimização: enquanto o Purchase não estiver provado, manter Tráfego/LPV ou evento de intenção e medir venda no ClickMax por UTM; só depois da Fase 2 criar conjunto novo otimizando Purchase (evitar reiniciar aprendizado em conjunto antigo). Excluir Audience Network e compradores (público de exclusão) nas campanhas novas.
- Teto de custo por venda: líquido R$ 44,51 (R$ 47 Pix) antes de imposto; CAC real hoje incomprovável (cenários R$ 35 a R$ 105).
Efeito: R$ 60/dia = R$ 1.800/mês; o ponto de equilíbrio exige ~1,35 venda/dia de R$ 47 líquidos de R$ 44,51 se CPA = R$ 44,51 (simulação, sem imposto).

## 6. Implementação única e organizada (proposta de ordem; nada executado)
Etapa 0 (Bruno, 1–2 h): painel ClickMax (pixel/CAPI/histórico de envio), Gerenciador de Eventos (Testar eventos, Diagnóstico), extrato da Ticto 22–25/11, origem dos 2 compradores, confirmar pixel na Ticto.
Etapa 1 (Claude + Bruno): corrigir config nativa de rastreamento; padronizar url_tags com ids; origem nos links de WhatsApp/Bela; tirar #pagar ou pôr UTM antes.
Etapa 2 (Bruno + Claude): compra real (Pix e cartão) por oferta, reembolso, conciliação e critérios R1–R8.
Etapa 3 (Claude, com aprovado): limpeza de páginas (despublicar/consolidar/arquivar), retirar promessas de reunião/contato/investimento, renomear turmas, remover portal antigo, pós-compra ativo, redirecionamento ao obrigado, título das páginas.
Etapa 4 (ChatGPT, com aprovado): reestruturar campanhas em R$ 60/dia (duas campanhas, uma oferta), copy nova para vídeos, exclusões, Purchase após Etapa 2.
Etapa 5: análise semanal e escala.
Ação imediata sugerida (precisa de aprovado de Bruno, baixo risco): pausar a venda direta antiga e o formulário R$ 47 já agora, pois os anúncios ativos prometem "agendar uma conversa/entrará em contato" e a Mini Mentoria cobre o mesmo destino.

## 7. Perguntas para Bruno
1. Aprova consolidar na Mini Mentoria R$ 47 e arquivar o R$ 97 (mantendo o acesso dos 2 clientes)? Ou prefere manter dois produtos com bônus real?
2. Aprova pausar agora a venda direta antiga e o formulário R$ 47?
3. Pode executar a Etapa 0 (painel, Testar eventos, extrato Ticto)?
4. Autoriza a compra real de teste com reembolso, por oferta?
5. Aprova despublicar/consolidar as páginas listadas (inclui /curso-terreno-destino-turistico, que recebe tráfego e não vende)?
6. Aprova tirar das páginas as frases de reunião/contato/"receber investimentos", e rever o nome "Mentoria"?
7. Mensagem aos 2 compradores de R$ 97 e aos leads sobre a mudança: quer? (exige aprovado)
8. Quem executa o quê: Claude (infra/páginas/checkout) e ChatGPT (campanhas): confirmar.

## Limites desta auditoria
Checkout real bloqueado no ambiente (payments.clickmax.io 403): campos, Pix/cartão na tela, e-mail de acesso e redirecionamento pós-compra não verificados; CAPI, dataset, pixel por oferta e token ilegíveis por MCP; cache do Windsor atrasa; vídeos não ouvidos; artes não lidas; Hotmart não conectada.
