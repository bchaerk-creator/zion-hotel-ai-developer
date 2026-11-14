# 03 · Auditoria de OFERTA, COPY dos criativos e ZAYA (somente leitura) · 13/11/2026

Nada foi criado, alterado, ativado, publicado, enviado ou apagado (ClickMax, Meta, site). Fontes: repositório, ClickMax (workspace `e87e8ba9…`, só leitura) e Windsor (conta Zion Collection 2 `1271873041294684`, só nomes e gasto). "Não verificado" = não deu para confirmar com os dados acessíveis.

## RESUMO (10 linhas)
1. Há **quatro "ofertas vigentes" ao mesmo tempo**: (a) funil "★ EM USO AGORA": reunião e venda de Mentoria R$ 2.900 / Trilha+Clube R$ 490 / Land Bank R$ 270; (b) Clube R$ 97 por compra direta (anúncios e checkout ClickMax); (c) decisão de 11/11 noite: "não existe inscrição de R$ 97", clube R$ 970 só na reunião; (d) 12/11: Jornada do Desenvolvimento R$ 970 em até 12x (link Asaas), página sem preço.
2. O grupo "★ EM USO AGORA" (pipeline `40529cf1`, descrição "desde 05/11") **está desatualizado** em relação a 11/11 e 12/11, e a Zaya opera em **outro pipeline** (`24ee754c`, "Parceria Zion").
3. Anúncios com R$ 97 no nome (campanha "Clube R$ 97 → landing [10/11]", conjunto "Landing INSCRIÇÃO R$97" do Parceiro) tiveram gasto até 11/11; em 12/11 só há gasto nas campanhas de Diagnóstico/Reunião e Parceiro (formulário). Status atual de cada campanha: não verificado (Windsor não traz status).
4. Copy dos criativos: promessa de ganho financeiro não aparece, mas há **quatro pontos de risco** contra o CLAUDE.md (seção 4): "até R$ 400 mil por ano em uma única cabana", "pool de investidores", "maior clube de glamping do Brasil", "ter investimentos e parceria" (detalhe na seção 2).
5. A **Zaya (v56, publicada 10/11)** está alinhada ao objetivo "levar à reunião, sem preço", mas **contradiz** a base: o Club R$ 97, o Kit R$ 97/47 e a Jornada R$ 970 existem e ela é proibida de falar deles. Cita "mais de 23 destinos" (não verificado em arquivo) e usa o link da agenda direto.
6. A base de conhecimento (5 PDFs de 03/11 + 1 FAQ de 12/11) **não é legível pela API**; os nomes ("Land Bank", "Prompt v3") indicam conteúdo da era R$ 97/R$ 270. Risco de desatualização: não verificado.
7. Corte de R$ 5 mil: **saiu da persona** (v56 diz "não filtra por dinheiro"), mas **continua** em 2 fluxos em rascunho, em 2 etapas do pipeline "★" e na pergunta 5 do quiz.
8. Crédito de IA, 30 dias: 358 decisões, 217 execuções de modelo, 159.248 tokens de entrada e 39.955 de saída (claude-sonnet-4-6). Só 56 (26%) usaram ferramenta do CRM; na amostra das 100 respostas mais recentes, 58 não usaram nenhuma. Custo em R$ ou créditos: não verificado.
9. Maior vazamento verificável é **WhatsApp, não IA**: no fluxo do menu do Club, 74 de 101 execuções falharam, 69 mensagens com "insufficient credits"; 52 dos 53 follow-ups da Zaya falharam (AxiosError 400).
10. Já existe boa parte do chatbot determinístico (menu `zion_destino_turistico` com 6 botões, fluxos de botão, templates de agendamento/lembrete). Falta ligar a Zaya só ao "caso aberto" e trocar o menu por um que reflita a oferta nova. Proposta de oferta única na seção 5, com decisões do Bruno marcadas.

---

## 1. LINHA DO TEMPO DAS OFERTAS

Fontes principais: `producao/catalogo/VARREDURA_NOMES_E_PRECOS.md` (12/11), `docs/academy/comando-05a/ARQUITETURA_COMERCIAL.md` (09/11), `producao/mentoria-desenvolvimento-360/INVENTARIO.md` (09/11), `producao/clube/OFERTA_CLUBE_ENTRADA.md` (10–11/11), `producao/clube/ESTRATEGIA_FUNIL_97.md` (11–12/11), `producao/clube/diagnostico/README.md` (11/11), `producao/clube/REATIVACAO_POR_DOR.md` (09/11), `producao/catalogo/FLUXO_ADESAO_CLUBE.md` (12/11), `CLAUDE.md`, pipelines do ClickMax.

| Data (fonte) | Oferta / preço | O que aconteceu |
|---|---|---|
| Antes de 09/11 (ARQUITETURA_COMERCIAL §3.2) | Mentoria Zion 360° Trilha A R$ 15.900; Trilha 2 e 3 R$ 297; Combo 3 trilhas R$ 890; Estruturação Dossiê; Coleção 7 volumes; Aula R$ 47 | Produtos **arquivados** no ClickMax. Ficam só como histórico. |
| Set–out (VARREDURA §1, §2 itens 12–15) | Turma Fundadores 6x R$ 549 (R$ 3.294); Mentoria em Grupo 12x R$ 302,09 / R$ 2.784 (20% off sobre R$ 3.480); Acompanhamento 12x R$ 510,43; Premium 12x R$ 1.031,27 | Ainda **no ar** em `/hub` (Lovable) e `docs/lancamento/`. A própria varredura marca "20% off" e "crédito de R$ 47" como risco (preço "de"/bônus sem base). |
| Out (INVENTARIO §1.8; VARREDURA §1) | **Land Bank inscrição R$ 97** (modelo antigo) e **Jornada/Inscrição R$ 270** (Asaas `zrhq…`, 6x R$ 45; Land Members + Radar) | Zaya vendia "Club Zion Collection Base R$ 270". R$ 97 "encerrado"; R$ 270 = Club Base na prática (ARQUITETURA_COMERCIAL §3.1). |
| 29–30/10 (fluxos ClickMax) | **Consultoria prévia R$ 490** (Asaas `r053…`, 10x R$ 49) + **Jornada R$ 270** nos templates `zion_terreno_caminhos` / `zion_land_caminhos` (aprovados) | "Funil Terreno · 1 Clicou Jornada R$ 270" fechado em 04/11; "2 Consultoria R$ 490" em rascunho. |
| 01/11 | **Raio-X** (diagnóstico prévio **gratuito**) → oferta R$ 270 por e-mail D0/D1/D3/D7 | Fluxos "Raio-X · 1..5" em **rascunho**. Página `docs/raio-x` mostra "R$ 97" com link que cobra R$ 270 (VARREDURA risco 1). |
| 03/11 | Campanha "FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO" | Início do funil de reunião. Zaya publicada com Land Bank (PDFs de 03/11). |
| 05/11 (pipeline `40529cf1`, grupo ★) | **★ EM USO AGORA**: reunião estratégica sem custo, venda na reunião de **Mentoria R$ 2.900, Trilha+Clube R$ 490 ou Inscrição Land Bank R$ 270** | Desenho do funil "atual". Mentoria R$ 2.900 e Trilha+Clube R$ 490 **não têm oferta no ClickMax** e tags de compra com 0 (ARQUITETURA_COMERCIAL §3.1). |
| 09/11 (decisão Bruno) | Arquitetura C: Club (assinatura), ferramentas R$ 19 / mini mentorias R$ 27 vendidas separado, Mentoria 360° premium independente (**sem preço, aguarda Blueprint**), Club Master R$ 980 e Pro R$ 2.900 "em pausa" | Pro R$ 2.900 = mesmo preço da "Mentoria R$ 2.900" (colisão apontada em §3.1 e §3 conflito 8 do MAPA). |
| 09/11 | Funil de reativação por dor: vídeo → formulário → reunião (capital > R$ 100 mil) ou **R$ 97 para entrar na reunião** | `REATIVACAO_POR_DOR.md`; 6 modelos em rascunho, nada enviado. |
| 10/11 | **Kit Inicial de Captação R$ 97** (Club, entrada) | MAPA linha 41; oferta ClickMax `5b89a932`. |
| 10/11 | **Club Zion Collection R$ 97 (2x R$ 48,50)** como oferta de entrada; R$ 270 "some da página" | `OFERTA_CLUBE_ENTRADA.md` §2 ("não anunciar de R$ 270 por R$ 97"). Conta do próprio arquivo: a entrada não paga a mídia sozinha; fecha no degrau seguinte (premissas rotuladas). |
| 11/11 | Campanhas **Clube R$ 97 [10/11]** (compra direta) e **Parceiro Zion** (conjunto "formulário" e conjunto "INSCRIÇÃO R$97") no ar; Diagnóstico e CLUB · D pausadas 12/11 ~00h55 | `OFERTA_CLUBE_ENTRADA.md` (11/11), Windsor (gasto em 11/11). |
| 11/11 tarde | "Diagnóstico grátis → reunião → venda na reunião" (Bruno): oferta feita na reunião, não no chat; quiz de 5 perguntas + agenda | `diagnostico/README.md`. |
| **11/11 noite (decisão Bruno)** | **"Não existe inscrição de R$ 97."** Clube vendido na reunião por **R$ 970**; nenhum preço público até Bruno aprovar a narrativa. Oferta R$ 97 `72924971…` **arquivada**; "Zaya reescrita para levar todos à reunião" | `diagnostico/README.md`, bloco "Decisão de Bruno (11/11/2026)". Substitui R$ 97 e, na prática, o desenho de 05/11. |
| 12/11 | Downsell **Kit Inicial de Captação R$ 47** (oferta `50fd0b0a…`, enviada para aprovação) | `ESTRATEGIA_FUNIL_97.md` (12/11 01h45). Convive com o Kit R$ 97 (MAPA linha 41 diz "R$ 97 voltou para pending_corrections"). |
| 12/11 | **Jornada do Desenvolvimento R$ 970 em até 12x** (Asaas `sd9u8uluy0urc2ye`, Trilha 1 gravada); página sem preço; ficha de adesão → pagamento → pipeline `a7216b13` | `FLUXO_ADESAO_CLUBE.md`, `VARREDURA_NOMES_E_PRECOS.md`. **Primeiro pagamento real desse link: não verificado** ("webhook nunca recebeu"). Parcelas: slide diz até 10x, Bruno diz 12x. |
| 12–13/11 | Infoprodutos R$ 19 (ferramentas), R$ 27 (Arsenal, mini mentorias), R$ 47 (Zion Collection 06) | `CLAUDE.md` §4. Vendedor ClickMax `pending`: nenhum checkout nativo vende. |

### Vigente segundo cada fonte
- **Funil "★ EM USO AGORA"** (pipeline `40529cf1`, atualizado 10/11, 104 cards, 7 em "3b · Liguei, não atendeu"): reunião sem custo → venda na reunião de **Mentoria R$ 2.900 / Trilha+Clube R$ 490 / Land Bank R$ 270**. Etapas "Formulário · R$ 5 mil ou mais → agendar" e "menos de R$ 5 mil → nutrir" mantêm o corte de R$ 5 mil.
- **Anúncios (Windsor, 11–12/11):** "Diagnóstico → Reunião [03/11 e 11/11]" (form → agenda), "Parceiro Zion … Form → Reunião [11/11]", "Clube R$ 97 → landing [10/11]" e "CLUB · D link direto [06/11]". Gasto em 12/11 só em Diagnóstico (R$ 7,58), Parceiro formulário (R$ 3,03) e Reunião (R$ 1,77). Nenhuma linha em 13/11 até a consulta.
- **Decisão mais recente do Bruno (11/11 noite e 12/11):** reunião como porta; clube/Jornada R$ 970 só na conversa; R$ 97 não existe.
- **Zaya:** reunião, sem preço (persona v56).

### CONTRADIÇÕES
1. **R$ 97 existe ou não existe.** Checkout ClickMax e `/clube` (10–11/11), templates aprovados `zion_inscricao_passos` e `zion_o_que_recebe` ("2x de R$ 48,50 ou R$ 97"), fluxo ativo "Pagamento inscrição R$ 97 confirmado → agenda da sessão" (`08a59f14`), conjunto "INSCRIÇÃO R$97", Kit R$ 97 (MAPA) **x** decisão de 11/11 noite e a oferta `72924971` arquivada. `diagnostico/README.md` lista onde ainda aparece.
2. **R$ 970 é Jornada (Trilha 1 gravada) ou Club?** `diagnostico/README.md` fala "inscrição do clube … por R$ 970 … na reunião"; `FLUXO_ADESAO_CLUBE.md` e a VARREDURA chamam o mesmo R$ 970 de "Jornada do Desenvolvimento". A VARREDURA (item 19) ainda aponta "Zion Start R$ 970" como colisão.
3. **R$ 270** ("Jornada" em `zion_terreno_caminhos`, Land Members, Inscrição Land Bank no pipeline ★) **x** R$ 970 (mesma palavra "Jornada").
4. **R$ 2.900**: "Mentoria" do pipeline ★ **x** Club Pro (mesmo preço, em pausa) **x** Mentoria 360° (sem preço, aguarda Blueprint).
5. **R$ 490**: "Trilha + Clube" **x** "Consultoria prévia" (dois produtos, um preço).
6. **R$ 47**: Kit de Captação R$ 47 (12/11) **x** Kit R$ 97 (10/11); R$ 47 também é "Aula 47" (Asaas) e Zion Collection 06.
7. **43 ou 58 aulas** (MAPA conflito 7; `OFERTA_CLUBE_ENTRADA.md` §3 diz 43; mesmo arquivo, registro de 11/11, diz 58).
8. **Três "clubes"**: Club Zion Collection (R$ 97/R$ 970), Land Members (R$ 270 + Radar), Club Base/Master/Pro (R$ 270/980/2.900).
9. **Corte de R$ 5 mil**: persona v56 "não filtra por dinheiro" **x** fluxos `86c40978`/`212684a2`, etapas do pipeline ★ e quiz pergunta 5 ("investiria até R$ 5 mil").
10. **Pipelines**: Zaya trabalha em `24ee754c` (Parceria Zion), o grupo ★ é `40529cf1`, e 12/11 criou `a7216b13` (Adesão). Três "funis em uso".

---

## 2. PROMESSAS E COPY DOS CRIATIVOS ATIVOS

Regra de comparação (CLAUDE.md §1): sem promessa de renda/investimento/valorização, sem números de mercado ou resultados inventados, sem urgência/bônus falsos, promessa "Aprenda o passo a passo para …". O texto do criativo não é legível pelo Windsor; abaixo, o texto-fonte do repositório.

### 2.1 Land Bank · Diagnóstico (campanha "FORM → DIAGNÓSTICO GRÁTIS → REUNIÃO [03/11]")
- **Promessa (`diagnostico/README.md`, "Copy do anúncio"):** "Descubra o potencial do seu terreno. Faça o diagnóstico gratuito: 8 perguntas, e a equipe Zion devolve em que ponto o seu projeto está e qual é o próximo passo." Lista do que recebe ao entrar no clube: formação em 5 etapas, sessão estratégica, "acesso aos melhores produtos de glamping do Brasil", terreno no Radar do Land Bank "e a possibilidade de parceria e investimento". Fecha com "Com mais de 20 anos no mercado internacional e 5 no Brasil, a Zion é referência em glamping no país".
- **Frase oficial de Bruno (11/11):** "Receba acesso e tenha a possibilidade de ter investimentos e parceria com a Zion."
- **Checagem:** (+) diagnóstico gratuito, "possibilidade", sem preço. (−) "melhores produtos de glamping do Brasil", "referência no país" e "20 anos internacional e 5 no Brasil" sem fonte registrada (MAPA §3 conflito 6 pede que Bruno confirme números canônicos); "ter investimentos" soa mais forte que "avaliar". (−) o anúncio "ainda cita R$ 97" na página de resultado/checkout, conforme decisão de 11/11.

### 2.2 Reunião / Form Agendamento (campanha "[LAND BANK][LEADS][DIAGNÓSTICO GRÁTIS → REUNIÃO] [11/11]", anúncios "REUNIÃO · … · Form Agendamento")
- **Promessa (`diagnostico/README.md`):** "Faça o seu diagnóstico gratuito aqui mesmo, em 8 perguntas, e já agende uma conversa com a nossa equipe. Seja um parceiro Zion e aprenda o passo a passo." Tela final: "Na conversa, a equipe Zion olha o seu terreno, mostra o caminho e as formas de entrar." Template `zion_agende_reuniao` (aprovado): "isso abre a possibilidade de futuras parcerias e investimentos … reunião estratégica, sem custo".
- **Checagem:** (+) promessa de passo a passo, sem preço, sem número. (−) "Seja um parceiro Zion" como chamada pode ser lido como oferta de parceria garantida; mitigado por "A Zion avalia cada caso" (presente no Parceiro, não confirmada neste texto). "Diagnóstico … em 8 perguntas" **x** quiz de 5 perguntas + formulário Meta (inconsistência de contagem).

### 2.3 Parceiro Zion (campanha "PARCEIRO ZION · … Form → Reunião · 11/11"; `producao/clube/ads/COPY_PARCEIRO.md`, v2 sem preço)
- **Promessa:** "Transforme seu terreno em um destino turístico e aprenda o passo a passo entrando no Zion Collection Club … Seja um parceiro da Zion Collection … Pare de vender quartos. Comece a vender experiência." Modelo: "você entra com a área e a infraestrutura … A Zion entra com a bubble, a marca e a reputação, o sistema e a gestão das reservas, a formação da equipe … Quem opera é um gerente local, contratado e formado pela Zion." Fecha com "Seja o próximo destino. A Zion avalia cada caso."
- **Checagem:**
  - **Risco alto:** "A Zion … chega a faturar **até R$ 400 mil por ano em uma única cabana**, somando hospedagem, gastronomia e experiências." Tem a ressalva ("resultado da nossa própria operação desde 2020, não uma promessa para o seu caso"), mas é número de resultado sem fonte registrada no repositório (MAPA conflito 6 diz que números da Bubble não foram confirmados por Bruno). CLAUDE.md §1: "nada de números de mercado, resultados". Não verificado se Bruno confirmou.
  - **Risco alto:** "a investimentos: seu local no Radar do Land Bank, com a própria Zion e o **pool de investidores que a Zion reúne**" e "melhores produtos de glamping do Brasil" (sem fonte). Sugere acesso a capital; CLAUDE.md §1 proíbe promessa de investimento.
  - **Risco médio:** "estamos em plena expansão por todo o Brasil" e "Zion Glamping Store" (fatos não confirmados em arquivo desta auditoria); "reunião estratégica inicial … para viabilizar o seu projeto" (promessa de viabilizar).
  - (+) sem preço, com "A Zion avalia cada caso".
  - Variante "INSCRIÇÃO R$97": **contradiz** a decisão de 11/11 (não existe R$ 97).

### 2.4 Club (campanhas "Clube R$ 97 → landing [10/11]" e "CLUB · D [06/11]"; `OFERTA_CLUBE_ENTRADA.md`)
- **Promessa:** "Transforme seu terreno em um destino turístico. Aprenda o passo a passo com a Zion…" com "acesso a investimentos", "melhores produtos do mercado", "referência" e **"maior clube de glamping do Brasil"** (inseridos por decisão de Bruno em 11/11); vídeo v3 "dor e troféu, sem preço"; landing com preço 2x R$ 48,50 e "Próxima masterclass ao vivo: quinta-feira, 20h" (evento semanal, urgência real segundo o arquivo).
- **Checagem:**
  - **Risco alto:** "maior clube de glamping do Brasil" é superlativo sem fonte (CLAUDE.md: sem números de mercado). "acesso a investimentos" é promessa de capital.
  - **Contradição:** o preço R$ 97 aparece na landing e no checkout; decisão de 11/11 noite diz que não existe.
  - (+) "garantia de 7 dias" é o CDC (permitido); "acesso liberado na hora" foi testado (compra de teste Pix R$ 97, 11/11).
  - Previsão de conversão e break-even em `OFERTA_CLUBE_ENTRADA.md` está rotulada como premissa (ok), mas usa "2 a 5% dos leads compram" de blogs (direcional).

### 2.5 Templates de WhatsApp aprovados que reforçam as mesmas promessas
- `zion_clube_form_1`: "…Radar do Land Bank, onde a Zion e **investidores olham os terrenos inscritos**" (risco médio: sugere visibilidade a investidores).
- `zion_terreno_caminhos` / `zion_land_caminhos` (aprovados): "Jornada R$ 270 · Consultoria R$ 490 · Mentoria em grupo/individual · A Zion faz o plano completo para você" e "como uma hospedagem de sucesso fatura" (promessa implícita de resultado). Obsoletos (VARREDURA item 21).

---

## 3. ZAYA

**Fonte:** `ai_agents_get`, `ai_agents_knowledge_list`, `ai_agents_deployments_get`, `ai_sdr_overview` (30 dias, America/Sao_Paulo), `ai_sdr_decisions_list`.

### 3.1 Configuração
- Agente `db450d9a…`, ativo, **v56 publicada em 10/11 20:05** (atualizada 11/11 19:48), claude-sonnet-4-6, temperatura 0,3, papel `sdr_inbound`, canal WhatsApp via Gupshup, número "Zion Collection" `96346b98…`. Propósito no cadastro: "Leva todos os contatos à reunião de diagnóstico prévio com a equipe Zion, sem falar de preço".
- `tools: []` e `escalation: []` no cadastro; as ferramentas efetivamente usadas (abaixo) vêm do posto, não do agente. `knowledgeStoreId` nulo.
- **Posto (deployment) `a3852ba2…` "Zaya · WhatsApp":** autopilot, pipeline `24ee754c` (Parceria Zion), etapa 1 "Leads novos", atendente `5e212de6…`, até 20 turnos, silêncio de 720 min para follow-up, até 4 follow-ups com template `zion_followup_duvida` (UTILITY), pode aplicar tags, criar tarefas e **agendar reuniões**; não cria propostas nem compromissos; rotinas manhã/noite **desligadas**; sem calendário de horário comercial (`businessHoursCalendarId` nulo; o horário "8h–20h" está só no texto da persona).
- **Instruções (resumo):** objetivo único, reunião de diagnóstico e comparecimento; "não vende, não fala de preço, não filtra por dinheiro"; até 2 frases por mensagem; 6 perguntas (perfil, local, documentação, desejo, dor, decisor), 2–3 bastam; agenda nativa com 2 horários ou link `app.clickmax.io/book/projeto-de-bruno-25763216/…`; tags TRIAGEM | ZAYA ASSUMIR / QUALIFICADO / CONDICIONAL, REUNIÃO | AGENDADA / CONFIRMADA / REAGENDAR, OBJEÇÃO | NÃO AGORA; no-show em 3 etapas; objeções em tons; não fala "consultoria" nem "curso" (diz "trilha"); quem já comprou: agradece e escala.
- **Base de conhecimento (6 itens, todos `synced`, sem erro):** 5 PDFs de 03/11, `Zaya-Prompt-v3-Land-Bank.pdf`, `Zaya-Base-de-Conhecimento-Land-Bank.pdf`, `Land bank`, `Zaya-Base-de-Conhecimento-Land-Bank-1.pdf` (duplicado), `Zaya-Guia-da-Bubble-Zion.pdf`; 1 FAQ de 12/11 ("perseguição até a reunião e base antiga": 2 perguntas sobre follow-up e base antiga). **O conteúdo dos PDFs não é devolvido pela API: não verificado.** Há dois PDFs de nome quase igual e um "Prompt v3" que pode conflitar com a persona v56.
- **Canais:** só WhatsApp (Gupshup), um número.

### 3.2 Uso (30 dias, 28/10 a 12/11)
| Métrica | Valor |
|---|---|
| Decisões / leads | 358 / 78 |
| Respondeu (spoke) | 212 (média 1,72 rodadas nas 100 mais recentes) |
| Execuções de modelo | 217 (56 com ferramenta; 74% só conversa, na amostra de 100: 58 sem ferramenta) |
| Tokens (entrada / saída) | 159.248 / 39.955 (se o total inclui cache: não verificado) |
| Escaladas para humano | 24 (20 `provider_failure`, 4 `model_escalated`) |
| Silenciadas | 28 (24 `awaiting_human`, 4 `human_attendant`) |
| Erros | 88 (68 `turn_failed` em follow-up, "AxiosError 400", rodadas 0) |
| Adiadas `turn_busy` | 25 |
| Latência | p50 15,3 s, p95 26,4 s (espera do lead p95 25,7 s) |
| Ferramentas | `registrar_qualificacao` 31 (1 erro), `aplicar_tag` 27, `consultar_agenda` 24 (4 erros), `criar_tarefa` 7, `registrar_nota` 6 (1 pulada), `registrar_oportunidade` 5 (3 puladas por falta de pipeline), `escalar_para_humano` 5, **`agendar_reuniao` 2**, `consultar_reuniao` 1, `encerrar_conversa` 1 |
| Follow-ups | enviados 1, **falharam 52**, cancelados 26 (24 porque o lead respondeu) |
| Cadastro do agente | 79 conversas, 24 escaladas, 1 resolvida |

Pico de 31/10 (80 respostas, 27 erros, 11 escaladas) coincide com o disparo "Land Members · Disparo inscrição" (173 contatos, ativo). "Custo/uso de crédito de IA" em R$ ou créditos: **não visível** pela API (`wallet_statement` é do vendedor, não do crédito de IA).

### 3.3 Comparação ponto a ponto

| Tema | Oferta vigente / copy dos criativos | O que a Zaya diz | Situação |
|---|---|---|---|
| Objetivo | Reunião (decisão 11/11) | Reunião, sem preço | **OK** |
| Preço do Club | R$ 970 só na reunião (11/11); R$ 97 arquivado; R$ 270 antigo | "Nunca diga valor"; "a equipe apresenta o valor na reunião" | **OK com a decisão**, mas quem já viu R$ 97 na landing/checkout/WhatsApp (templates aprovados) recebe silêncio sobre o preço |
| Quem comprou | tags "LAND BANK \| INSCRIÇÃO R$97 PAGA", "COMPROU \| …" | agradece e escala | **OK** (cobre tag R$ 97 e Land Members) |
| Jornada do Desenvolvimento R$ 970 / Kit R$ 47 e R$ 97 / ferramentas R$ 19 | Existem desde 10–12/11 | Não menciona, e é proibida de oferecer "produto, inscrição, kit" | **Falta**: sem rota para quem quer comprar direto ou pede "só a trilha"; tudo vira escalada |
| "Mais de 23 destinos", "dois primeiros glampings pioneiros de referência" | Criativos: "20 anos no mercado internacional e 5 no Brasil", "referência" | Usa "mais de 23 destinos" e "pioneiros" | **Não verificado** (23 não aparece em arquivo lido); persona proíbe "boa demanda" mas afirma pioneirismo |
| Promessa de parceria/investimento | Criativos: "possibilidade de parceria e investimento", "pool de investidores", "melhores produtos" | "Nunca prometa… a Zion avalia cada caso" | **Mais conservadora que o anúncio**: o lead chega com expectativa de investimento e a Zaya precisa desmentir. Alinhar criativo, não a Zaya |
| Corte de qualificação | Pipeline ★ e quiz: R$ 5 mil | "Não filtra por dinheiro" | **Contradição entre sistemas**; também o `Leads novos · <R$ 5 mil` (rascunho) deixaria a Zaya agindo diferente por fluxo |
| Parceria operador (infra) vs terreno | Parceiro Zion: "entra com a área e a infraestrutura; Zion com a bubble e a gestão" | Abertura fala só de "terreno" e "parceria possível" | **Falta** um parágrafo do modelo Parceiro (perfil operador/infra), e o FAQ de 12/11 só cobre base antiga |
| Aulas da trilha | 58 no ClickMax, 43 em textos | Não cita número | **OK** (persona v56 evita) |
| Agenda | Agenda nativa 45 min, 14h–17h30 úteis, **sem link de vídeo** gerado (09/11) | "30 minutos"? (persona não diz duração; `zion_reuniao_qualificado` diz 45; Zaya "fala 30" segundo REATIVACAO §6) | **Divergência de duração** e link de reunião sem Meet: não verificado se foi corrigido |
| Horário | Silêncio 22h–8h (funil de lembretes) | "antes das 8h e depois das 20h" | Janelas diferentes (8–20 x 8–22) |
| Calendly | Proibido | Proibido | **OK** |
| Follow-up | Template `zion_followup_duvida` | 4 follow-ups | **Quebrado**: 52 de 53 falharam (AxiosError 400; causa não verificada, possível crédito/template) |

### 3.4 O que falta na Zaya (propostas, sem executar)
1. Atualizar o posto/persona para as ofertas decididas (sem tocar o "sem preço" se Bruno mantiver).
2. Excluir da base os PDFs duplicados e conferir o conteúdo do "Prompt v3".
3. Unificar o corte (R$ 5 mil) e a duração da reunião.
4. Decidir se quem pede "só a trilha/kit" é escalado ou recebe link (hoje, escalado).
5. Corrigir o follow-up (não verificado o motivo do 400).

---

## 4. CHATBOT POR BOTÕES E QUANDO A ZAYA ENTRA

### 4.1 Onde o crédito de IA é gasto sem necessidade (só dados verificáveis)
- 217 execuções em 30 dias; 56 (26%) usaram ferramenta; na amostra das 100 respostas mais recentes (04/11 a 12/11), **58 foram só conversa**. Conversa sem ferramenta é, em tese, o tipo de turno que um menu resolve (confirmar, dar o link da agenda, agradecer). **Natureza do conteúdo desses 58 turnos: não verificado** (a API não devolve o texto).
- Só **2** `agendar_reuniao` e 24 `consultar_agenda` no mês: a maior parte do uso de IA não termina em reunião (cadastro do agente: 79 conversas, 1 resolvida).
- 20 escaladas por `provider_failure` e 68 follow-ups com erro: crédito/tempo gastos sem resultado.
- 25 `turn_busy` e latência p50 de 15 s: o lead espera para respostas simples.
- Lembrete: **WhatsApp** também consome crédito (60 por mensagem, saldo de 873 em 10/11, `AUTOMACAO_FORM_SEM_COMPRA.md`) e já acabou: no fluxo do menu do Club (`a90448b6`) 74 de 101 execuções falharam; 69 mensagens "insufficient credits" (última em 11/11 11:24).

### 4.2 Arquitetura proposta (fluxo determinístico no ClickMax)
Princípio: **botão resolve, texto livre vai para a Zaya só quando o botão não basta**.

```
Entrada (anúncio, formulário Meta, quiz, clique-para-WhatsApp)
  → Fluxo 0 · Boas-vindas + menu (template com botões, 1 mensagem)
       [Quero agendar]  → agenda nativa (botão de link)  → tag AGENDADA → lembretes (templates)
       [Como funciona]  → vídeo/página (1 mensagem) + botão [Agendar]
       [Quero parceria] → mensagem do modelo Parceiro (fixa) + [Agendar]
       [Tenho uma dúvida] → Zaya entra (caso aberto)
       [Agora não / Não quero receber] → tag + silêncio (sem IA)
  → Sem resposta em 48h → lembrete fixo (template) → última chamada fixa (72h)
  → Reunião: confirmação, lembretes (véspera, manhã, 1h, 15 min), no-show, reagendar (templates, sem IA)
Zaya entra SOMENTE:
  - texto livre fora do menu / "tenho uma dúvida";
  - objeção real (preço, golpe, sócio, tempo);
  - remarcação negociada;
  Zaya sai (escala/encerra) após agendar ou ao ver tag de compra.
```
Regras de contenção: limite de 6 turnos de IA por lead antes de oferecer a agenda por botão; follow-up por template fixo (sem modelo); IA nunca responde a clique de botão; horário de silêncio por fluxo.

### 4.3 Fluxos e modelos existentes que já servem
| Peça | Estado | Observação |
|---|---|---|
| `Club · Lead do formulário Meta → Zaya abre a conversa (menu) + lembrete em 48h` (`a90448b6`, ativo, 101 execuções) | Ativo | Tag `META \| FORM LAND BANK` → template `zion_destino_turistico` (6 botões: Quero aprender, Inscrever meu terreno, Inscrever meu projeto, Comprar uma Bubble, Quero ser parceiro, Não quero receber) → 48h → `zion_terreno_lembrete`. Entrega 92%, abertura 54%, clique 33% dos 24 enviados; **74 falhas por crédito**. O menu é de 3 produtos antigos: reescrever. |
| `Funil Land Members · Fazer parte do clube → página do clube` (`b28ba703`, 25 execuções), `· Comprar uma Bubble → Glamping Store` (`9cfb8d6b`, 9), `· Inscrever meu projeto → link` (`c5658d80`, 2) | Ativos | Tratam o clique do botão sem IA. |
| `Funil Terreno · 4 Falar com a equipe → aviso` (`ce384dbd`, 5), `· 5 Não quero receber / Agora não`, `· 6 Agora não → só etiqueta` | Ativos | Saída/escala sem IA. |
| `Funil Terreno · Menu de parceiros (1 a 4) → tag e aviso` (`5eca2173`), `Boas-vindas e menu de gatilhos` (`f524a310`), `0 Disparo (menu)` (`549f7f99`) | **Rascunho** (o `5eca2173` está vazio, sem passos) | Moldes aproveitáveis. |
| `Leads novos · chamou no WhatsApp → Zaya` (`0c37f32b`) | Rascunho, 1 passo | Hoje entregaria toda mensagem à Zaya: oposto da proposta. |
| `Leads novos · resposta menos de R$ 5 mil / R$ 5 mil+` (`212684a2`, `86c40978`) | Rascunho | Corte de R$ 5 mil: contradiz a persona v56. |
| Pós-agendamento: `Lembretes da reunião · Zaya (lead)`, `No-show · reunião → Zaya remarca`, `Teste A · Lead Meta → convite Zaya` (grupo ★), `Alerta · Reunião Land Bank agendada` (ativo, 21 execuções) | Rascunho (exceto alerta) | Estrutura pronta; ativar com "aprovado". |
| `Objeção · Não agora → sequência de reativação (72h)`, `Objeção · Quero saber mais → Zion por dentro` | Ativos | Resposta de botão sem IA. |
| `Clube · Lead do formulário (terreno) / Parceiro … sem compra → 3 toques` (`5a8e7d04`, `de4a391a`) + templates `zion_clube_form_1/2/3`, `zion_parceiro_form_1/2/3` | Rascunho fluxo, **templates aprovados** | Sequência pronta, com R$ 0 de preço. |
| Templates aprovados de agendamento: `zion_agende_reuniao`, `zion_pos_audio_agendar`, `zion_ativ_resp_agendar`, `zion_sessao_agendar`, `zion_reuniao_hoje`, `zion_reuniao_15min`, `zion_faltou_reuniao`, `zion_convite_reuniao`, `zion_pos_reuniao`; devolutiva `zion_diag_*` e `*_v2` | Aprovados | Rascunhos: `zion_reagendar`, `zion_lembrete_reuniao`, `zion_reuniao_qualificado`. |
| Agenda nativa "Equipe Zion" 45 min | Ativa | Sem link de vídeo (09/11): confirmar. |
| `Diagnóstico · Devolutiva · Alto/Ajustes/Em preparação` (3 fluxos) | Rascunho | Tag DIAG → WhatsApp → e-mail (templates v2 aprovados). |
| Quiz "5 perguntas + agenda" (`1e8726ee…`), formulário de alinhamento (`61490f4e…`) | Ativos | Qualificação determinística já existe (pontuação 0–10). |

### 4.4 O que falta
1. **Menu novo** (template com botões) alinhado à oferta única: hoje `zion_destino_turistico` e `zion_terreno_caminhos` citam Bubble, Jornada R$ 270, Consultoria R$ 490, mentorias; exige novo template e aprovação da Meta (não editar os aprovados).
2. **Roteador de clique de botão** do novo menu (um fluxo por botão, como os Land Members) e **a regra "Zaya só no 'Tenho uma dúvida'"**.
3. **Ativar lembretes/no-show/reagendar** (rascunhos) e criar `reagendar` aprovado; link do Meet na agenda.
4. **Follow-up fixo por template** em vez do follow-up da Zaya (hoje 52/53 com erro).
5. **Créditos de WhatsApp** (já esgotados) e limite de turnos da IA.
6. **Unificar o corte** (R$ 5 mil ou nenhum) e remover duplicidade de pipelines.
7. Conteúdo do menu "Como funciona" (vídeo "Como funciona" já existe: `docs/ads/parceiro/parceiro-2min-4x5.mp4`, vídeo v3 do clube).
Tudo isso é proposta; nada foi criado.

---

## 5. PROPOSTA DE OFERTA ÚNICA E ESCADA (só fatos existentes; ver marcações)

### 5.1 Posicionamento (uma frase)
> **Somos a Zion, operadora de glamping (Zion Bubble, em Urubici e Florianópolis); temos método, ferramentas e uma equipe que olha o seu terreno ou a sua hospedagem; oferecemos uma reunião sem custo e, a partir dela, o passo a passo para transformar o seu terreno em um destino turístico, sem prometer renda, investimento ou parceria: a Zion avalia cada caso.**

Fatos que sustentam: Zion Bubble Urubici/Florianópolis e fotos reais (`CLAUDE.md` §2); reunião de diagnóstico sem custo e agenda ativa (`REATIVACAO_POR_DOR.md` §5–6); Trilha 1 e área de membros com 58 aulas no ClickMax (`OFERTA_CLUBE_ENTRADA.md`, registro de 11/11); ferramentas R$ 19, Arsenal R$ 27, kits (`CLAUDE.md` §4, MAPA); Land Bank/Radar como benefício (`ARQUITETURA_COMERCIAL.md` §3.1).
Não usar até Bruno confirmar: "20 anos", "até R$ 400 mil por cabana", "pool de investidores", "maior clube", "23 destinos" (ver 2.3, 2.4, 3.3).

### 5.2 Escada (proposta; **cada item marcado [B] depende de decisão do Bruno**)
| Degrau | Preço (fonte) | O que entrega | Estado |
|---|---|---|---|
| 0 · Diagnóstico gratuito → reunião de 45 min | R$ 0 | Quiz/formulário, devolutiva, agenda nativa | Existe. **[B] duração e quem conduz** (`diagnostico/README.md`, pendente) |
| 1 · Ferramentas | R$ 19 (`CLAUDE.md`) | 11 ferramentas com oferta; vendedor pendente | Existe, **não vende** até o vendedor |
| 2 · Arsenal / Zion Collection 06 / Kit de Captação | R$ 27 / R$ 47 / **R$ 47 ou R$ 97 [B]** | Mini mentorias, kit mestre, kit | Existem em rascunho; **[B] qual Kit: R$ 47 (12/11) ou R$ 97 (10/11)** |
| 3 · **Jornada do Desenvolvimento** (Club Zion Collection) | **R$ 970 em até 12x** (Asaas `sd9u…`) | Trilha 1 gravada, exercícios, ferramentas, Land Bank/Radar como benefício, acesso por 12 meses | Link pronto; **[B] confirmar que "R$ 970 do clube" e "R$ 970 da Jornada" são o mesmo produto; [B] o que inclui (sessão com Bruno?); [B] parcelas (10x ou 12x); primeiro pagamento real não testado** |
| 4 · Mentoria de Desenvolvimento 360° (premium) | **Sem preço** | 12 semanas, 8 módulos (Comando 05A) | Não existe; aguarda o Blueprint. **[B] preço; descontinuar "Mentoria R$ 2.900" e "Trilha+Clube R$ 490" do pipeline ★** |

Fora da escada pública (decisão pendente do Bruno): R$ 97 (arquivado em 11/11), R$ 270 Land Members/Jornada antiga, Consultoria R$ 490, Club Master R$ 980, Club Pro R$ 2.900, Zion Start R$ 970, Turma Fundadores (**[B] arquivar ou manter cada um**, já pedido na VARREDURA §3).

### 5.3 Efeitos práticos (se Bruno aprovar)
- Um único caminho de anúncio: criativo → formulário Meta/quiz → agenda; preço só na reunião (como decidido em 11/11).
- Criativos: tirar os quatro termos de risco (2.3/2.4) e os conjuntos "INSCRIÇÃO R$ 97".
- Zaya + menu: seção 4.
- Pipelines: escolher um (`24ee754c` ou `40529cf1`) para a Zaya e para os relatórios; arquivar o outro.

### 5.4 Decisões do Bruno (lista direta)
1. R$ 970: é o clube, a Jornada, ou os dois com o mesmo conteúdo?
2. Kit de Captação: R$ 47 ou R$ 97?
3. Números canônicos (20 anos, R$ 400 mil por cabana, 23 destinos, "maior clube", "pool de investidores").
4. Corte de R$ 5 mil: manter ou remover (e como a Zaya trata quem tem pouco capital).
5. Mentoria R$ 2.900 / Trilha+Clube R$ 490 / Land Bank R$ 270 no pipeline ★: encerrar?
6. Duração da reunião (30 ou 45 min) e link de vídeo na agenda.
7. Autorizar novo menu de botões e limite de turnos da Zaya.
8. Créditos de WhatsApp e confirmação do motivo do AxiosError 400 nos follow-ups.

## Limites desta auditoria
- Texto dos PDFs de conhecimento da Zaya e das mensagens do menu: não retornam pela API. Status ativo/pausado atual das campanhas Meta: não verificado (só gasto). Windsor sem dados de 13/11 na consulta. Asaas não consultado. Lovable (site) não consultado nesta sessão; os preços do site vêm da VARREDURA de 12/11.
