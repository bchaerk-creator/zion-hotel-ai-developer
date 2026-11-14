# 06 · E-mail de reativação da base antiga · diagnóstico e plano (13/11/2026)

Somente leitura. Nada foi enviado, criado ou alterado (Brevo e ClickMax). Só contagens, sem dados pessoais. "Não verificado" = não deu para ler.
Fontes: Brevo (conta, remetentes, domínios, listas, campanhas, modelos), ClickMax (workspace `e87e8ba9…`: leads, listas, segmentos, modelos, remetentes, broadcasts), repositório (`CLAUDE.md`, `producao/clube/ESTRATEGIA_FUNIL_97.md`, `REATIVACAO_DORES_BASE.md`, `REATIVACAO_POR_DOR.md`, `email/reativacao_clube.html`).

## RESUMO (10 linhas)
1. O ClickMax NÃO envia e-mail hoje: `email_sender_signatures_list` vazio, 0 broadcasts de e-mail, nenhuma caixa conectada. Três modelos prontos esperam remetente.
2. O Brevo ENVIA: 2 remetentes ativos e 2 domínios autenticados (`zionbubbleglamping.com`, `zionhotelmanagement.com`). Mas o plano Marketing Standard consta como **cancelado (29/10/2026)** e o crédito pago está em 0: o limite diário atual é **não verificado** (conta gratuita costuma ser 300/dia). Confirmar antes de qualquer plano de volume.
3. Base ClickMax: 2.775 contatos; **2.490 com e-mail válido**, 217 risky, 48 inválidos, 20 pendentes (sem e-mail). Enviáveis de verdade: ~2.490 (e só ~2.2xx se tirarmos descadastrados do Brevo; ver seção 2).
4. 2.354 dos 2.490 válidos (95%) são a "base antiga" importada por CSV; só ~77 vêm de formulário/páginas externas (Meta) e ~58 de outras origens. LGPD: **0** válidos com `lgpdApproved` marcado; a base é de contato comercial anterior, base legal = legítimo interesse + descadastro de 1 clique.
5. O Brevo já disparou 17 campanhas (jun a out, 33,9 mil envios): descadastro médio 0,54%, spam 0,065%, soft bounce 6%. A de 26/10 (Base Mestre) teve 0,10% de spam e 0,55% de descadastro: já no limite do que Gmail/Yahoo toleram (0,10%; ideal < 0,05%).
6. Recomendação: **Brevo como motor de envio** (reputação e histórico já existem, métricas de spam/bounce visíveis), com **ClickMax como CRM** (segmentos, tags, reunião/checkout). ClickMax só vira o motor se Bruno autenticar um domínio nele.
7. Plano: aquecimento em 3 semanas, 2 a 3 envios/dia só depois do dia 8, começando pelos 261 do Lote 1 e pelos que abriram nos últimos 90 dias.
8. Sequência de 5 e-mails: reativação, Club, produtos, parceria (sem promessa), última chamada com descadastro fácil. CTA = agendar reunião ou entrar no Club.
9. Paradas automáticas: descadastro > 1% por envio, spam > 0,10%, hard bounce > 2% ou soft > 8%.
10. Depende do Bruno: escolher remetente/domínio, confirmar plano Brevo, aprovar texto e dizer "aprovado" para disparar.

---

## 1. Estado do e-mail

### 1.1 Brevo (lido)
| Item | Estado |
|---|---|
| Conta | ZION HOTEL GROUP INTERNATIONAL (e-mail da conta é Gmail de Bruno), fuso America/Sao_Paulo, relay SMTP habilitado, Marketing Automation habilitado. |
| Plano | `payAsYouGo` com 0 créditos; assinatura com início/fim 29/10/2026; vertical Marketing "Standard" com status **cancelled**. Plano atual e limite diário: **não verificado** (a API não mostra a cota do dia). Pelos envios de outubro (até 5.266 por campanha) havia plano pago; hoje parece ter voltado ao gratuito. |
| Remetentes | #1 "ZION HOTEL GROUP INTERNATIONAL" o Gmail pessoal do Bruno (ativo; Gmail como remetente é ruim para marketing: DMARC do Gmail reprova envio por terceiros) · #2 "Zion Bubble Glamping" `info@zionbubbleglamping.com` (ativo; é o usado em todas as campanhas). Não existe remetente em `zionhotelgroup.com` (domínio dos links do Club) nem em `zionhotelmanagement.com`. |
| Domínios | `zionbubbleglamping.com` autenticado e verificado (DNS, 26/06/2026, DNS na Wix) · `zionhotelmanagement.com` autenticado e verificado (DNS, 10/08/2026, Wix). A API informa "authenticated: true" (DKIM/código Brevo); registros SPF/DKIM/DMARC individuais e política DMARC: **não verificado** (`records: null`). `zionhotelgroup.com`: não listado. |
| Listas | BASE MESTRE ZION 5.666 · PRIMEIRO DISPARO 4.908 · LISTA 2025 RESERVAS 886 · ASKSUITE 2025 164 · Imobiliárias 1: 131 · BASE MESTRE . INÍCIO 0 · identified_contacts 0 · Sua primeira lista 1. Segmentos: nenhum. As listas são de hóspedes/reservas e de leads de glamping, não a base de terreno/parceria do ClickMax; o cruzamento entre as duas bases é **não verificado**. |
| Campanhas | 52 no total; 17 enviadas (tabela na seção 3). Rascunhos de "Noite Mágica". Nenhuma campanha do Club ou da parceria. |
| Modelos | 11 (todos de Noite Mágica/hotel bolha e 1 de Imobiliárias). Nenhum de Club, parceria ou terreno. |

### 1.2 ClickMax (lido)
- **Remetente:** `email_sender_signatures_list` = vazio (0 assinaturas, 0 confirmadas). Sem isso `flows_send_email` e broadcast por e-mail não saem. Não há broadcasts de e-mail (`broadcasts_list` canal e-mail = 0) e `account_snapshot` mostra `emailCampaigns.recent` vazio (zero histórico de e-mail no ClickMax; só WhatsApp/Gupshup: 482 envios, 21% de falha, e voz).
- **Como resolver (Bruno, 1 vez, ~30 min + propagação de DNS):** (a) escolher o domínio de envio (recomendo um subdomínio como `mail.zionhotelmanagement.com`, para isolar a reputação), (b) no ClickMax criar a assinatura (a assinatura é do tipo Postmark: precisa de verificação de domínio com DKIM e Return-Path, ou de confirmação por e-mail para endereço único), (c) pôr os registros no DNS (hoje na Wix), (d) conferir `confirmed: true` na lista. Alternativa rápida, mas pior: assinatura de endereço único (confirma por link) sem autenticar o domínio, o que derruba a entregabilidade. Não alterei nada; a ação é do Bruno.
- **Modelos do ClickMax (3, todos próprios, HTML completo):**
  1. "Clube · Reativação da base · E-mail 1 (clube + parceiro)" · assunto `{{name}}, abrimos uma porta nova para o seu terreno` · 4.966 caracteres (é o HTML de `producao/clube/email/reativacao_clube.html`).
  2. "Agendamento · Diagnóstico gratuito de parceria (reunião com a equipe Zion)" · 3.452.
  3. "Base antiga P1 · Operadores · E-mail 1 (diagnóstico de parceria)" · 3.488.
- **Listas/segmentos relevantes:** Lote 1 base quente 261 · Lote 2 restante 2.470 · BASE ANTIGA todos os contatos 2.772 (segmentos dinâmicos, taxa de engajamento 0 pois nunca houve e-mail); listas por dor (form Meta): capital 22, parceiro 31, por onde começar 9, medo de errar 12, Trailer Trilha 77; Sócios em potencial 9; Trilha A (já opera) 39; Parceria Zion · pendentes de agendamento 101.
- **Atenção:** Lote 1 + Lote 2 somam 2.731, mas válidos são 2.490. Os segmentos parecem não filtrar `emailStatus`. Antes de qualquer envio, acrescentar filtro `emailStatus = valid` (ou criar segmentos novos, o que fica para a sessão de execução).

### 1.3 HTML do repositório (`producao/clube/email/`)
- Só existe `reativacao_clube.html` (≈5 KB, tabela 600 px, Arial, sem imagens, variável `{{name}}`, link de descadastro `{{unsubscribe_url}}`). Conteúdo: Club (formação em cinco etapas, sessão estratégica, produtos, radar do Land Bank; R$ 97 à vista ou 2x R$ 48,50, Pix ou cartão, reembolso em 7 dias) e bloco "parceiro Zion".
- Links: `zionhotelgroup.com/clube?utm_source=email&utm_medium=broadcast&utm_campaign=reativacao-clube` e `/parceiro?...reativacao-parceiro`. Falta `utm_content`/`utm_term` e o padrão do CLAUDE.md para Meta não se aplica (é e-mail), definir o padrão na seção 4.
- Pontos a corrigir antes de enviar: (i) o texto "acesso a produtos, investimentos e parcerias" tem de seguir a regra "sem promessa de investimento" (já tem a nota "sem garantia" no rodapé; reforçar acima da dobra); (ii) o rodapé não traz endereço físico (Brevo exige no rodapé; boa prática e CAN-SPAM; para o ClickMax: não verificado); (iii) a variável de descadastro é `{{unsubscribe_url}}` no ClickMax e `{{ unsubscribe }}` no Brevo: **não verificado** qual a sintaxe aceita em cada um, testar com e-mail de teste; (iv) o remetente do e-mail 1 diz "Você já falou com a Zion"; só é verdade para parte da base (ver seção 2).

## 2. Tamanho e qualidade da base (ClickMax, 13/11/2026)
| Medida | Contatos |
|---|---|
| Total de leads | **2.775** (Set +1.741, Out +933, Nov +101) |
| E-mail válido | **2.490** (89,7%) |
| Risky (descartável/catch-all/role) | 217 (7,8%) |
| Inválido | 48 (1,7%; inclui testes internos) |
| Pendente (sem e-mail, ex.: visitantes de webchat) | 20 (0,7%) |

Válidos por origem: **CxClients (importação CSV da base antiga) 2.354 (94,5%)** · CxExternalPages (formulário/página externa do Meta e diagnóstico) 77 · CxPages 39 · CxFlows 15 · CxCalendar 2 · CxClub 2 · CxQuizzes 1 · CxForms 0. A tag FORMS FACEBOOK NATIVO soma 194 contatos e META | FORM LAND BANK 101 (válidos entre eles: **não verificado**, pois o filtro por tag não foi cruzado com `emailStatus`).
Contagens de formulário Meta segundo o repositório (09/11): 478 leads únicos de 12/08 a 09/11; no ClickMax, só ~77 aparecem como válidos com origem de página externa, o restante está sob outra origem ou tag.
- **LGPD:** 0 dos 2.490 válidos tem `lgpdApproved` = true; não há consentimento explícito de marketing registrado. `emailConsentConfirmed` e preferências canceladas: não verificado (filtro `messagePreferencesCanceled` não aceita a consulta usada).
- **Duplicados:** não medido (existe `leads_check_duplicates`, não rodei para não varrer dados pessoais). Como o ClickMax deduplica por e-mail, a duplicidade interna tende a ser baixa; **duplicidade com o Brevo** (BASE MESTRE 5.666 e PRIMEIRO DISPARO 4.908) é provável e **não verificada**: quem já recebeu Noite Mágica da Zion Bubble 3 a 6 vezes em outubro está cansado do remetente.
- **Enviáveis de verdade:** 2.490 válidos, menos (a) descadastrados e reclamantes do Brevo (183 descadastros e 22 spam no histórico, não exportados nesta leitura), (b) contatos com tag de compra/cliente do Club (excluir quem já comprou), (c) os 217 risky (não enviar no início). Estimativa prudente: **~2.200 a 2.400**. "Base fria de 1.700" citada pelo Bruno: provavelmente = CxClients válidos que nunca interagiram; é o grupo mais arriscado.
- Registros de teste internos (e-mails `example.com`, contatos de Bruno) estão misturados; excluir por segmento antes de enviar.

## 3. Qual ferramenta usar

Histórico real do Brevo (17 campanhas enviadas, só dados agregados):
| Período | Envios | Entregues | Aberturas únicas | Hard bounce | Soft bounce | Descadastro | Spam |
|---|---|---|---|---|---|---|---|
| Total jun a out | 33.918 | 31.544 (93%) | 6.208 | 329 (1,0%) | 2.031 (6,0%) | 183 (0,54%) | 22 (0,065%) |
| 26/10 Base Mestre + Primeiro Disparo (~4.100) | 4.123 | 3.831 | 78 | 0 | 295 (7,2%) | 21 (0,51%) | 4 (0,10%) |
| 27/10 Base Mestre + Reservas 2025 | 4.920 | 4.620 | 935 | 0 | 297 | 20 (0,41%) | 2 |
| 09/08 "Funil 6K" Email 1 | 5.266 | 4.913 | 12 | 1 | 348 | 38 (0,72%) | 3 |
Obs.: as aberturas variam de 0,3% a 35% entre campanhas (provável efeito de rastreio de abertura/proteção de privacidade e de sinal de pasta de spam); não usar abertura como métrica principal, usar clique, resposta e reunião.

| Critério | ClickMax (broadcast por e-mail) | Brevo |
|---|---|---|
| Remetente hoje | **Nenhum** confirmado; precisa DNS | 2 remetentes ativos, 2 domínios autenticados |
| Limite | Créditos de mensagens do plano: em 08/11 havia 12.207/12.500 usados (renovou 09/11); custo por e-mail e limite de e-mail: **não verificado** | Plano pago cancelado em 29/10; limite diário atual **não verificado** (gratuito ≈ 300/dia, o que inviabiliza 2.400 contatos em poucos dias sem upgrade) |
| Entregabilidade | Sem histórico de e-mail: reputação zerada do remetente novo (precisa aquecer do zero) | Histórico de 34 mil envios; reputação do domínio `zionbubbleglamping.com` já exposta, com spam em 0,10% na última grande campanha |
| Métricas | `broadcasts_insights`, taxa de abertura/clique/bounce; spam e hard/soft detalhados: **não verificado** | Estatística global, por link e por domínio de destino; relatório de eventos |
| Vínculo com tags/funil | **Forte**: segmento por tag/dor/origem, tag no clique, cartão no pipeline, reunião na agenda nativa, checkout no mesmo sistema | Fraco: listas separadas, sem tag do ClickMax nem pipeline; seria preciso exportar listas e voltar o resultado por UTM |
| Descadastro | Preferência de mensagem do lead, no mesmo CRM | Lista de bloqueio própria do Brevo; precisa sincronizar manualmente com o ClickMax |
| Custo/operação | Já pago | Pode exigir upgrade |

**Recomendação:**
1. **Para o primeiro mês: Brevo envia, ClickMax qualifica.** Motivo: remetente e domínio autenticados já existem, reputação mensurável, e o ClickMax hoje não envia. Mas com **domínio diferente do da hospedagem**: usar `zionhotelmanagement.com` (ou subdomínio) em vez de `zionbubbleglamping.com`, para que uma reclamação sobre "terreno/parceria" não prejudique os e-mails de reserva da Zion Bubble. Exige criar o remetente no Brevo (ação do Bruno).
2. Cada clique leva a páginas do ClickMax (Club, `/parceiro`, agenda), onde o lead entra no CRM com UTM e tag. Quem responde, agenda ou compra vira exclusão automática dos próximos e-mails (atualizar a lista do Brevo por exportação manual diária; é o ponto frágil).
3. **Migrar para o ClickMax** quando houver remetente confirmado e domínio dedicado aquecido; é o ideal de longo prazo (um só sistema, descadastro sincronizado).
4. Se o plano do Brevo continuar gratuito (300/dia), o aquecimento da seção 4 já cabe no limite até o dia 10; depois exige upgrade ou ClickMax.

## 4. Plano de reativação

### 4.1 Segmentação (criar só com "aprovado"; todos com `emailStatus = valid`, excluindo compradores, descadastrados, risky e testes)
| Prioridade | Segmento | Tamanho aprox. | Uso |
|---|---|---|---|
| A (quente) | Lote 1 base quente (261) + quem tem tag de Land Bank/formulário Meta/Club/diagnóstico (≈ 190 a 280, sobreposição não verificada) | ~260 | E-mails 1 a 5 completos, primeiro a receber |
| B (dor) | Listas por dor do form Meta: capital 22, parceiro 31, por onde começar 9, medo de errar 12; Trailer 77 | ~150 (com sobreposição) | Mesmo roteiro, mas com abertura e assunto da dor |
| C (operadores) | Trilha A (já opera) 39 + Sócios em potencial 9 + tag DISPARO A1 · OPERADOR PARCERIA (586, validar) | 50 a 600 | E-mail de parceria entra mais cedo (E-mail 3 no lugar do 2) |
| D (restante antiga) | Restante dos CxClients válidos | ~1.900 a 2.100 | Só depois do aquecimento, apenas e-mails 1, 2 e 5 e sinal de engajamento (clicou/abriu) |
| X (não enviar) | risky 217, inválidos 48, pendentes 20, compradores, descadastrados, opt-out de mensagens, testes | | |
Cruzar dor e capital (recurso para estruturar: sim/parcial/não, do `REATIVACAO_DORES_BASE.md`): 63% citam dinheiro/sócio; a copy NÃO promete sócio nem investidor.

### 4.2 Cadência e aquecimento (2 a 3 envios por dia, mas só ao final)
O pedido de 2 a 3 e-mails por dia para a mesma pessoa não é recomendado; interpretar como **2 a 3 envios por dia no total** (lotes para segmentos diferentes ou e-mails diferentes para pessoas diferentes). Para a mesma pessoa: 1 e-mail a cada 2 a 3 dias.
| Fase | Dias | Envios/dia | Quem recebe | Condição para avançar |
|---|---|---|---|---|
| 0 | antes | 0 | | Remetente definido; SPF/DKIM/DMARC conferidos; teste em Gmail, Outlook e Yahoo (caixa de entrada, não spam); limite Brevo confirmado |
| 1 | 1 a 3 | 1 lote de 100 | Segmento A (somente os que clicaram/abriram em campanhas Brevo nos últimos 90 dias, se houver; senão Lote 1) | spam < 0,05%, descadastro < 1%, hard bounce < 1% |
| 2 | 4 a 7 | 2 lotes de 150 (manhã/tarde) | A restante + B | idem; ao menos 5 respostas ou cliques sem alerta |
| 3 | 8 a 14 | 2 lotes de 250 | C + D engajados | idem, soft bounce < 8% |
| 4 | 15 a 21 | 3 lotes de 300 a 400 (teto ~1.000/dia) | D restante (só o E-mail 1) | métricas estáveis 3 dias seguidos |
| 5 | 22+ | 2 a 3/dia conforme segmentos | sequência completa | |
Cada lote vai com intervalo (envio escalonado, 30 min entre lotes, como previsto em `ESTRATEGIA_FUNIL_97.md`). **Horário:** terça a quinta, 08h30 a 10h30 e 19h30 a 21h (horário de Brasília), nunca fim de semana nem antes das 8h; o histórico de outubro (envios às 19h e 21h) teve a maior abertura (20% a 35%).
Regra de ouro: reputação nova primeiro com quem conhece a Zion; a base fria só entra depois de 7 dias limpos.

### 4.3 Descadastro, LGPD e padrões de envio
- Rodapé com: razão social e endereço (Zion Hotel Group International, Florianópolis), motivo do contato ("você falou com a Zion sobre o seu terreno/hospedagem" só se for verdade para o segmento; para a base importada por CSV usar "você está na base de contatos da Zion Bubble Glamping" e dizer de onde veio), link de 1 clique "Não quero mais receber" e cabeçalho `List-Unsubscribe` (Brevo faz; ClickMax: não verificado).
- Descadastro: processar em até 24 h; no ClickMax cancelar preferência de mensagem (`leads_message_preferences_update`) e no Brevo bloquear; manter lista de supressão única.
- LGPD: base legal = legítimo interesse (contato comercial anterior), com teste de balanceamento anotado; só dado já existente, sem comprar lista, sem coletar mais nada no e-mail; atender pedidos de exclusão. Registrar no ClickMax a tag "origem: base antiga CSV".
- **UTM padrão:** `?utm_source=email&utm_medium=<brevo|clickmax>&utm_campaign=reativacao-base-nov26&utm_content=e<1-5>-<segmento A|B|C|D>&utm_term=<variante-assunto>`; manter `utm_source=email` do HTML atual e trocar `broadcast` por `utm_medium` real.
- Texto: português simples, voz "nós", assunto sem caixa alta/emoji/"grátis"/"urgente", texto curto, 1 CTA principal por e-mail, versão texto simples, imagem mínima (relação texto/imagem alta).

### 4.4 Sequência de 5 e-mails (cada pessoa recebe 1 a cada 2 a 3 dias)
Regras comuns: sem número de mercado, sem depoimento, sem renda, ocupação, retorno, valorização ou investimento garantido, sem escassez falsa. Exemplos marcados "dados fictícios". Autorização permanente de CLAUDE.md não cobre disparo: **só com "aprovado"**.

| # | Dia | Objetivo | Assunto (A/B) | Esqueleto | CTA |
|---|---|---|---|---|---|
| 1 | D0 | Reativar: lembrar quem somos e por que a pessoa está recebendo | A: `{{name}}, ainda faz sentido para o seu terreno?` · B: `Uma pergunta sobre o seu projeto` | 1 parágrafo de contexto (de onde a Zion conhece o contato, operamos desde 2020 em Urubici e Florianópolis); 1 pergunta sobre a dor dominante (dinheiro/sócio, por onde começar, será que meu terreno serve); 2 opções: "responder este e-mail" ou link de 1 clique "Tenho interesse"; descadastro visível | Responder ou clicar em "Quero conversar" (leva à página de agenda; tag `REAT | E1 CLIQUE`) |
| 2 | D3 | Apresentar o **Zion Collection Club** como o caminho para aprender o passo a passo | A: `O passo a passo que a Zion usa nas unidades` · B: `Por onde começar, na ordem certa` | Reaproveitar `reativacao_clube.html` enxuto: cinco etapas, sessão estratégica, produtos, Radar do Land Bank; R$ 97 à vista ou 2x R$ 48,50, Pix ou cartão, reembolso em 7 dias; "é conteúdo educacional, não garante resultado" | Entrar no Club (`/clube` com UTM) |
| 3 | D6 | Produtos de entrada: ferramentas R$ 19, Arsenal R$ 27, kit R$ 47, para quem ainda não quer o Club | A: `Ferramentas prontas para organizar o seu projeto` · B: `Comece pequeno: R$ 19 a R$ 47` | 3 produtos mais próximos da dor do segmento (ex.: Orçamento da Cabana, Calculadora de Custos, Arsenal) com 1 linha cada, promessa "aprenda o passo a passo para…"; reembolso 7 dias; dados fictícios nos exemplos | Ver o produto (páginas do ClickMax, UTM do produto) |
| 4 | D9 | **Possibilidade de parceria/investimento, sem promessa**: a Zion avalia cada caso; conversa de diagnóstico de 30 a 45 min | A: `Conversa de diagnóstico com a equipe Zion` · B: `Seu terreno e a possibilidade de parceria` | O que a Zion faz e o que NÃO promete (nenhum sócio, investimento, retorno, renda ou valorização é garantido; parceria só se o projeto fizer sentido para as duas partes); como funciona a conversa (olhamos área, documentação, estágio e capital disponível); para quem já opera: conversa de operador para operador; quem não tem recurso: estruturar o projeto antes (Club) | **Agendar reunião** (agenda nativa do ClickMax, tag `REAT | AGENDOU`) |
| 5 | D12 | Última chamada gentil + limpeza da base | A: `{{name}}, vamos manter o contato?` · B: `Último aviso sobre este assunto` (sem urgência falsa) | Resumo de 3 linhas (conversa, Club, produtos); "se não for o momento, tudo bem: clique em Não quero mais receber e paramos"; quem não interagir nos 5 e-mails vira "frio" e sai da lista de envio por 90 dias | Agendar reunião **ou** entrar no Club (dois botões iguais em destaque) |
Regras de saída: quem clicar em agenda/compra/respondeu sai da sequência e recebe o fluxo de reunião (`zion_reuniao_qualificado`) por WhatsApp; só um canal por vez por pessoa (não disparar e-mail e WhatsApp no mesmo dia para o mesmo lead).

### 4.5 Métricas e paradas
Medir por envio e por segmento, nas primeiras 24 h, antes do próximo lote:
| Métrica | Verde | Alerta (reduz volume pela metade) | **Parada (pausar tudo, revisar)** |
|---|---|---|---|
| Descadastro | < 0,5% | 0,5 a 1% | **> 1%** |
| Spam/reclamação | < 0,05% | 0,05 a 0,10% | **> 0,10%** (limite Gmail/Yahoo: 0,30%) |
| Hard bounce | < 1% | 1 a 2% | **> 2%** |
| Soft bounce | < 5% | 5 a 8% | **> 8%** |
| Queda de entrega no Gmail/Outlook | | | Teste de caixa de entrada indo para spam em 2 provedores |
Metas de sucesso (referência, não promessa): cliques e respostas por lote; agendamentos de reunião por 100 enviados; vendas por UTM comparadas ao custo (faturamento não é lucro). Acompanhar também resposta por WhatsApp.

## 5. O que precisa do Bruno e riscos

### 5.1 Decisões e ações do Bruno
1. **Remetente e domínio:** escolher o que envia (recomendo `contato@`/`bruno@` em `zionhotelmanagement.com` ou subdomínio). Criar o remetente no Brevo (ou assinatura no ClickMax + registros DNS na Wix). O e-mail do Gmail (o Gmail pessoal do Bruno) não deve ser o remetente de marketing.
2. **Plano do Brevo:** confirmar se o plano continua gratuito (limite diário) ou se renova o Marketing; passar o limite diário real.
3. **DMARC:** conferir o registro `_dmarc` de `zionhotelmanagement.com` (começar com `p=none` e relatório) e corrigir o que faltar.
4. **Aprovar o texto** dos 5 e-mails (rascunhos serão feitos depois, em modelo do Brevo e do ClickMax) e o endereço/razão social do rodapé.
5. **"aprovado"** para: criar segmentos/listas, programar a campanha pausada e disparar cada fase (CLAUDE.md: disparo de mensagens exige "aprovado"; gasto de anúncio continua em R$ 0).
6. Decidir a quem a reunião é oferecida (Bruno ou equipe) e a agenda (nativa do ClickMax) e se o e-mail 4 pode citar "parceria" no assunto.

### 5.2 Riscos
- **Reputação do domínio:** `zionbubbleglamping.com` já teve spam de 0,10% e descadastro de 0,5% por envio em outubro, com 3 a 6 e-mails de glamping em 10 dias para a mesma base. Usar esse domínio para falar de terreno/parceria arrisca os e-mails de reserva e de hóspedes. Por isso, domínio separado.
- **Base fria (~1.700 a 2.100 contatos):** importação CSV sem opt-in registrado (LGPD 0%). Alto risco de reclamação e de armadilhas de spam (spam traps) em lista antiga; o aquecimento e a exclusão de risky/inválidos reduzem, não eliminam. Se a lista for do tipo "clientes" de pousadas/imobiliárias, a expectativa de contato é baixa.
- **Cansaço de remetente:** a mesma pessoa pode ter recebido 3 a 6 campanhas da Zion Bubble em outubro (cruzamento não verificado); pausar 7 dias para esses.
- **Promessa regulatória:** assunto ou corpo que sugira sócio/investimento/retorno viola o CLAUDE.md e pode gerar problema com a CVM/consumidor. Usar sempre "possibilidade, avaliada caso a caso, sem garantia".
- **Limite e custo do envio:** Brevo gratuito pode atrasar; ClickMax sem histórico começa do zero e depende de DNS.
- **Dois sistemas:** o descadastro em um não bloqueia o outro; manter lista de supressão única e conferir diariamente.
- **Medição:** aberturas do histórico variam muito (proteção de privacidade); decisões por cliques, respostas e reuniões.
- **Dados lidos que não foram conferidos:** limite diário real do Brevo, registros DNS individuais (SPF/DKIM/DMARC), cruzamento ClickMax x Brevo, duplicados, sintaxe de descadastro, custo de e-mail no ClickMax, tags de opt-out.

Última atualização: 13/11/2026 (sessão de diagnóstico, somente leitura).
