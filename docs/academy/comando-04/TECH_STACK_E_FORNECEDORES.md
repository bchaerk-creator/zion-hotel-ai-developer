# Comando 04 · C e D · Zion Tech Stack e matriz de fornecedores

Data da consulta: 08/11/2026. **Pesquisa, não recomendação comercial.**

**Limite da verificação:** nesta sessão a rede bloqueou a abertura dos sites (fornecedores, Meta, Planalto, STJ). Os dados vieram de buscas indexadas restritas aos domínios oficiais sempre que possível. Legenda:
- **(O)**: trecho de página oficial do fornecedor, da plataforma ou do governo.
- **(V)**: declaração do próprio fornecedor sobre selo ou parceria, não conferida na lista oficial da OTA.
- **(T)**: site de terceiro.
- **NV**: não verificado.

**Antes de virar aula, cada preço e cada integração deve ser conferido no navegador e registrado com data.**

Exceção: as funções do ClickMax foram lidas na documentação oficial e, em parte, conferidas na conta da Zion (canais, agentes e funis), só em leitura.

---

## C. Zion Tech Stack: como funciona

**Princípio:** ninguém precisa de PMS, channel manager, CRM e agente de IA ao mesmo tempo. O membro começa pelo que é nativo e grátis (recursos do Airbnb e da Booking, WhatsApp Business, planilha Zion). Ele sobe de nível quando aparece um **gatilho** concreto, e nunca por moda.

| Categoria | Nível 1 · 1 unidade, orçamento baixo | Nível 2 · 2 a 10 unidades | Nível 3 · multiunidade com equipe | Gatilho para subir |
|---|---|---|---|---|
| Calendário e canais | iCal nativo entre Airbnb e Booking, aceitando o atraso (Airbnb importa a cada 3 h (O); na Booking não é tempo real e não funciona junto com conexão XML (O)) | Channel manager por API | Channel manager certificado + motor de reservas | Mais de 2 canais, ou uma reserva duplicada, ou mais de 1 unidade |
| PMS | Planilha Zion + extranets | PMS simples | PMS com permissões, financeiro e FNRH por API | Equipe com mais de 2 pessoas, ou mais de 3 unidades, ou obrigação de FNRH com volume |
| Venda direta | Link do WhatsApp + página simples + Pix manual | Site com motor de reservas | Motor de reservas + CRM + campanhas | Mais de 20% das reservas por indicação ou recompra |
| WhatsApp comercial | WhatsApp Business app (etiquetas, respostas rápidas, catálogo, saudação e ausência) (O) | API oficial via plataforma (multiatendente) | API oficial + CRM + agente de IA com passagem para humano | Mais de 30 consultas por semana, ou mais de 1 atendente |
| CRM e follow-up | Planilha de oportunidades Zion (7 etapas) | CRM com pipeline e cadência | CRM integrado ao WhatsApp e ao PMS | Perda de propostas sem retorno; mais de 50 oportunidades por mês |
| Agente de IA | Não usar. Respostas rápidas e roteiro | Agente para dúvidas frequentes, com passagem para humano | Agente de qualificação e follow-up com base de conhecimento | Volume que o humano não responde em até 15 min no horário comercial |
| Automação operacional | Mensagens programadas do Airbnb (O), checklist impresso, grupo de WhatsApp da limpeza | Ferramenta de tarefas e limpeza, fechadura com senha | Inspeções, manutenção e fechaduras integradas ao PMS | Mais de 1 prestador de limpeza, ou check-in sem presença |
| Preço e indicadores | Planilha Zion (ocupação, diária média, RevPAR) + Preço Inteligente do Airbnb com mínimo e máximo (O) | Precificação dinâmica | Revenue + BI | Mais de 3 unidades, ou temporadas e eventos frequentes |

### Indicadores (definições oficiais)

Glossário CoStar/STR (O):
- **Ocupação** = unidades vendidas ÷ unidades disponíveis.
- **Diária média (ADR)** = receita de hospedagem ÷ unidades vendidas.
- **RevPAR** = receita de hospedagem ÷ unidades disponíveis (= ocupação × ADR).
- **TRevPAR** = receita total ÷ unidades disponíveis.

Fórmulas operacionais (sem fonte oficial; usar as definições do dicionário único da Zion):
- **Custo por reserva** = gasto comercial ÷ reservas.
- **Conversão** = reservas ÷ consultas.
- **Margem operacional** = resultado operacional ÷ receita.

Os nomes e as fórmulas devem ser iguais aos da ZAIOS (G3 Indicadores).

---

## D. Matriz comparativa de fornecedores

### D1. PMS e channel manager

| Ferramenta | Público | Funções verificadas | Integrações (Airbnb / Booking) | Preço público (08/11/26) | Limitações | Nível | Fonte |
|---|---|---|---|---|---|---|---|
| Stays (BR) | Temporada, de anfitrião a administradora | Channel manager, calendário, preço, pagamento (cartão); site a partir do Professional | Airbnb Preferred+ (V); Booking Premier (V) | Super Host R$ 79/mês + 2% por reserva; Professional R$ 149 + 1,9%; Agency R$ 249 + 1,7%; implantação à parte (O) | Pix e FNRH nativos: NV | 1–3 | stays.net/precos |
| Hospedin (BR) | Pousadas e pequenos hotéis | PMS; FNRH Digital com envio automático (módulo pago) (O) | Channel manager à parte; status oficial NV | Jade (1–10 UHs) a partir de R$ 59,90/mês (O); teste de 10 dias | Preço do channel manager desatualizado | 1–2 | conheca.hospedin.com/fnrh-digital |
| HQBeds (BR) | Hostels, pousadas, temporada | PMS, channel manager, motor de reservas, Pix automático (O) | Status oficial NV | Sob consulta (T diverge) | Taxa de setup (T) | 1–2 | ajuda.hqbeds.com.br |
| Omnibees (BR) | Hotéis e pousadas maiores | CRS, channel manager, motor de reservas, yield, link de pagamento | Booking Premier (trecho da lista oficial) | Sob consulta | Pix no motor NV | 3 | omnibees.com |
| Desbravador (BR) | Hotéis médios e grandes | PMS; FNRH por API (O) | — | Sob consulta | — | 3 | desbravador.com.br |
| Cloudbeds | Hotéis, pousadas, hostels | PMS, channel manager e motor de reservas no plano One; FNRH via app parceiro (O) | Airbnb Preferred (2024) | Sem preço oficial (T: ~US$ 150 a 1.000/mês) | Pix para hóspede não encontrado | 2–3 | myfrontdesk.cloudbeds.com |
| Little Hotelier | Pequenos hotéis | Calendário, channel manager (SiteMinder), app | Herda da SiteMinder | NV em BRL | — | 2 | capterra (T) |
| Hostaway | Gestores profissionais | PMS, channel manager, site, fechaduras | Airbnb Preferred+ e Booking Premier Plus (V) | Sob consulta (T: mínimo de ~5 unidades) | Português NV | 3 | hostaway.com |
| Guesty Lite | 1 a 3 anúncios | Channel manager, caixa de entrada única, site direto | Airbnb Preferred+ (V) | A partir de US$ 9/anúncio/mês + 1% (O) | Cobrança em dólar | 1 | guesty.com/pricing |
| Smoobu | Temporada pequena e média | PMS, channel manager, site, mensagens | Airbnb Preferred (V); Booking Premier Plus (V) | T: €29 a €35 por unidade/mês | Sem português na interface (O) | 1–2 | support.smoobu.com |
| Lodgify | Temporada com venda direta | Site, channel manager, pagamentos | Airbnb Preferred+ (V); Booking Premier (V) | T: US$ 18 a 85/mês (1 imóvel) | Taxa por reserva com dados conflitantes | 1–2 | lodgify.com |
| Hospitable | 1 a 50+ unidades | Mensagens automáticas, channel manager, preço, fechaduras (O) | Airbnb Preferred+ e Booking Premier Plus (V) | Essentials grátis; Host US$ 29; Professional US$ 59; Mogul US$ 99 (O) | Fechaduras só a partir do Professional; português NV | 1–2 | help.hospitable.com |
| Channex | Vendido a PMS (white-label) | Channel manager | Airbnb Preferred+ (página regional, data incerta) | US$ 130/mês + US$ 0,50 por unidade de temporada (O) | Exige integrador | — | channex.io/pricing |
| "Hospeda" | Ambíguo: há dois produtos com o nome | NV | NV | NV | Identidade a confirmar | — | pms.hospeda.io ; hospedasoft.com.br |

Listas oficiais para conferir antes de qualquer aula: diretório de parceiros de software do Airbnb e a lista 2026 da Booking.com (Premier e Premier Plus). Nenhuma das duas foi lida completa nesta sessão.

### D2. WhatsApp, CRM e IA

| Categoria | Ferramenta | Público | Funções verificadas | Integrações | Preço público (08/11/26) | Limitações | Nível | Fonte |
|---|---|---|---|---|---|---|---|---|
| Canal | WhatsApp Business app | 1 unidade | Catálogo, etiquetas, até 50 respostas rápidas, saudação e ausência, vários aparelhos (O) | Coexistência com a API em alguns CRMs | Grátis | Sem API própria | 1 | faq.whatsapp.com |
| Canal | WhatsApp Business Platform (Cloud API) | Via plataforma | Cobrança por mensagem desde 01/07/2025; fora da janela de 24 h, só template aprovado (O). **Desde 01/10/2026, mensagens de serviço cobradas depois de 1.000 grátis por número por mês (O)** | — | Utilidade/autenticação US$ 0,0068 (07/2026, O); BRL: NV | Exige plataforma ou desenvolvedor | 2–3 | developers.facebook.com (pricing) |
| Plataforma | ClickMax | Zion e membros | Funis, motivo de perda obrigatório, cadência e follow-up automático no WhatsApp, webhooks, API oficial, coexistência com o app, automações, agentes de IA, broadcast com template, formulários, área de membros, webinários, checkout com Pix (O, docs) | WhatsApp via Gupshup (conferido na conta) | Preço: não encontrado | Opção de WhatsApp Web não oficial existe, com aviso de risco de banimento | 2–3 | docs.clickmax.io |
| CRM | RD Station CRM | PME BR | Funil, lembretes | Extensão para WhatsApp Web (não é API) | Free até 4 usuários (O); pagos divergentes | — | 1–2 | rdstation.com |
| CRM | Pipedrive | PME | Pipeline, WhatsApp na caixa de vendas | API Meta (possível beta) | US$ 14 a 79 por assento (anual) (O) | Templates só de texto | 2 | pipedrive.com |
| CRM | Kommo | PME | Funis, bots, agente de IA com passagem para humano | Cloud API direta | US$ 25/35/45 por usuário (O, blog) | IA não disponível para novos clientes do plano Base | 2 | kommo.com |
| CRM | HubSpot | PME–grande | CRM grátis | WhatsApp nativo só nos planos Pro/Enterprise (O) | Free sem WhatsApp | — | 3 | hubspot.com |
| CRM | Agendor | PME B2B BR | CRM + chat com API oficial (O) | Coexistência com o app | Free 3 usuários; Pro R$ 59/usuário; Chat R$ 312/mês (O) | Foco B2B | 2 | agendor.com.br |
| IA hotel | AskFlow Agents (Asksuite) | Hotéis | Agentes da consulta ao pós-estadia (V) | Cloudbeds, Opera; exige API verificada | Sob consulta | Afirmações do próprio fornecedor | 3 | asksuite.com/askflowagents |
| IA | Manychat | PME | WhatsApp no Pro, com IA | Repassa a tarifa Meta | US$ 29 anual / US$ 39 mensal (O) | — | 2 | manychat.com/pricing |
| Plataforma | Twilio / 360dialog | Desenvolvedores | API | — | Twilio US$ 0,005/mensagem; 360dialog €49/número/mês (O) | Exige desenvolvedor | 3 | twilio.com ; 360dialog.com |
| Não oficial | Z-API (WhatsApp Web) | — | Usa o protocolo do WhatsApp Web (O, documentação do fornecedor) | QR code | NV | **Risco de banimento: a Zion não ensina como solução** | — | developer.z-api.io |

**Regras do WhatsApp que limitam o que a Zion ensina:**
1. **Opt-in claro, com o nome da empresa, e saída respeitada** (O). Nada de mensagem sem consentimento.
2. **Automação permitida, mas sempre com caminho rápido para uma pessoa** (O).
3. **Termos de 2025/2026:** proíbem provedores cuja oferta principal é IA de uso geral. O assistente da própria empresa para os próprios clientes é permitido (O, seção 4.7). No Brasil, o CADE suspendeu a regra por medida preventiva, mantida em 04/03/2026. Não afeta o caso de uma pousada.
4. **Pela API, "responder é grátis" deixou de ser verdade** depois de 1.000 mensagens de serviço por número por mês (desde 01/10/2026).
5. **LGPD:** base legal (art. 7º) e opt-out fácil, conforme o guia de legítimo interesse da ANPD.

### D3. Automação operacional e preço

| Categoria | Ferramenta | Funções verificadas | Integrações | Preço público (08/11/26) | Limitações | Nível | Fonte |
|---|---|---|---|---|---|---|---|
| Registro de hóspedes | FNRH Digital (MTur) | Registro obrigatório desde 20/04/2026 para quem tem Cadastur; API para PMS (O) | API do MTur | Grátis | Exige gov.br + Cadastur; aplicação à pessoa física: NV | 1–3 | gov.br/turismo ; serpro.gov.br |
| Check-in online | Chekin | Envio à FNRH, 14 dias de teste (O) | 50+ PMS | Sob consulta | — | 2–3 | chekin.com |
| Fechadura | Intelbras (linha com app) | Senhas pelo app; gestão remota exige hub (O, manual) | Integração com PMS: NV | NV | — | 1–2 | intelbras |
| Fechadura | Yale (BR) | App; senha temporária com hub (O) | Modelos dos EUA integram com Hospitable e Hostaway; modelos BR: NV | NV | Hub à parte | 1–2 | yalehome.com.br |
| Fechadura | igloohome / Nuki / TTLock | PIN offline, gateway | Hospitable, Hostaway (O) | NV | Venda oficial no BR: NV | 2–3 | help.hospitable.com |
| Limpeza e tarefas | Breezeway | Tarefas e inspeções | — | A partir de US$ 19/mês (menos de 5 imóveis); 1º imóvel grátis (O) | Português NV | 2–3 | breezeway.io |
| Limpeza | Turno | Agenda e pagamento da limpeza | — | T: 1 imóvel grátis, ~US$ 10/imóvel | Brasil NV | 2 | (T) |
| Mensagens | Airbnb · mensagens programadas | Gatilhos por reserva, check-in e check-out (O) | Nativo | Grátis | Só no Airbnb | 1 | airbnb.com/help/article/2897 |
| Avaliação | Link e QR do Google | Pedido de avaliação; incentivo proibido (O) | — | Grátis | — | 1 | support.google.com/business |
| Preço | Preço Inteligente do Airbnb | Ajuste dentro do mínimo e do máximo (O) | Nativo | Grátis | Só no Airbnb | 1 | airbnb.com/help/article/1168 |
| Preço | Booking (promoções, Genius) | Descontos e promoções (O) | Nativo | Custo = desconto | — | 1 | partner.booking.com |
| Preço | PriceLabs | Preço dinâmico, painel de mercado (O) | Muitos PMS | Brasil: R$ 47,50/mês no 1º anúncio, ou 1% da receita; 30 dias de teste (O) | Taxas extras por canal | 2–3 | help.pricelabs.co |
| Preço | Beyond / Wheelhouse | Preço dinâmico | — | T: ~1% da receita | Brasil NV | 3 | (T) |

---

## Aplicação na metodologia Zion

| Nível | O que a aula ensina | O que a Zion entrega pronto |
|---|---|---|
| 1 | Usar bem o que já é grátis: iCal, recursos nativos das OTAs, WhatsApp Business, planilha, checklist | Planilhas e checklists (01, 11, 13, 14, 17), roteiro de WhatsApp, planilha de oportunidades |
| 2 | Escolher e configurar um PMS ou channel manager, um CRM e uma ferramenta de preço, com critérios e custo total | Comparador de custo total, checklist de implantação, roteiro de migração |
| 3 | Integrar, dar permissões, medir e decidir sobre IA | Roteiro de seleção (RFP simples), checklist de segurança e LGPD, painel de indicadores |

**Regra para tutoriais:**
- **Tutorial genérico** (o fluxo, sem marca): é o padrão.
- **Tutorial de fornecedor:** só da conta de teste da própria Zion, sem reproduzir material protegido, com a data da versão e o aviso de que a interface muda.
- A Zion não recebe comissão sem dizer isso ao membro (decisão pendente).
