# Zion Investors · mapa das automações (proposta; NADA criado nem ativado no ClickMax)

Estado em 28/11/2026, só leitura. Master V2 e comando do carrossel prevalecem sobre instruções antigas.

## Fluxo (três ações paralelas, disparadas pelo envio válido, sem esperar clique, resposta ou visita)
```
Meta Ads → formulário nativo gratuito → tela de conclusão → /oportunidades
Visitante direto → formulário web (docs/investidores) ─────────────┐
                                                                    ▼
                         webhook único (id da submissão = idempotência)
                                                                    ▼
   1. CRM ClickMax: criar/atualizar lead (chave = telefone normalizado E.164), campos, tags, origem
   2. Bela · WhatsApp 01 (final 1061, ClickMax/Gupshup): modelo aprovado com link da landing + link do WhatsApp 02
   3. Tarefa/fila prioritária para o comercial (WhatsApp 02) + aviso ao responsável
   (landing institucional: já é a página; a tela de conclusão mostra os dois canais)
```
Regras: não marcar "enviado" só por tag (registrar envio, entrega, resposta, tarefa, atendimento, reunião); pausar follow-up quando houver atendimento humano, recusa ou descadastro; não enviar duas mensagens concorrentes (Zaya, Bela de R$ 97 e fluxos antigos) ao mesmo contato.

## Inventário real (ClickMax, 28/11)
| Item | Estado | Decisão proposta |
|---|---|---|
| WhatsApp 01 | Zion Collection, final 1061, Gupshup, qualidade GREEN, TIER_2K (confirmado por Bruno) | Disparo da Bela |
| WhatsApp 02 | **Não identificado.** Outro canal conectado: Pablito Ads (final 4588). A Bela cita suporte +55 48 98872-9883, que não é canal do ClickMax | **Bruno confirma o número e se é número de atendimento humano** |
| Zaya `db450d9a…` | Ativa, v57; leva à reunião de diagnóstico; sem preço | **Não alterar** |
| Bela `a8a076d4…` | Ativa, SDR inbound do acesso de R$ 97; **proíbe oferecer reunião** e prospecção de investidor | **Não alterar.** Resposta de lead investidor cairia nela: precisa de regra de roteamento |
| Bela `adf143ae…` | Rascunho antigo (Clube R$ 270) | Não usar |
| Fluxos | Não há fluxo com "Bela" no nome | Criar fluxo novo (rascunho) |
| Formulário `5afa9bc9…` | Rascunho antigo "Investidores · Interesse em investir": **pergunta faixa de valor** | Não reutilizar |
| Tags | `INVESTIDOR`, `CLUB \| BUBBLE · COM INVESTIDOR`, `DISPARO …` existem; nenhuma `ZI_*` | Criar as `ZI_*` |

## Decisão recomendada sobre a Bela (você deixou em aberto)
Criar **um agente novo "Bela · Investidores" em rascunho** (persona própria: reunião gratuita, sem preço, sem promessa, sem faixa de capital, respeitando as regras do Master V2), mais fluxo e modelo novos. Motivo: mudar a Bela ativa quebraria a venda de R$ 97 (que hoje proíbe reunião). Roteamento por tag `ZI_NOVO_LEAD`/`ZI_BELA_DISPARO` só entra em vigor com "aprovado" e sem pausar a Bela atual para os outros leads. Zaya permanece como está; não há duplicação de contatos (chave única por telefone).

## Itens a criar (todos como rascunho; ativar só com "aprovado" de Bruno, comercial e jurídico)
- Tags: ZI_NOVO_LEAD, ZI_ORIGEM_META, ZI_ORIGEM_WEB, ZI_BELA_DISPARO, ZI_ATENDIMENTO_PRIORITARIO, ZI_PERFIL_ADERENTE, ZI_REUNIAO_AGENDADA, ZI_EM_NEGOCIACAO.
- Campos: destino, prazo, preferência, intenção declarada, origem/anúncio/formulário, consentimento (texto, versão, data). **Sem campo de capital** na captura inicial.
- Formulário web → webhook do ClickMax (a página já envia JSON; falta só a URL em `ZION_CONFIG.ENDPOINT`).
- Modelo WhatsApp (Bela, categoria utilitária/marketing a definir) com `{{nome}}`, `{{link_landing}}`, `{{link_whatsapp_prioritario}}`. **Envio para análise da Meta é ação externa: só com "aprovado".**
- Fluxo: gatilho = lead criado com consentimento → tag → modelo (via 1061) → tarefa prioritária → notificação do responsável. Travas: respondeu, atendimento humano, recusa, descadastro.
- Pipeline/etapas no CRM e SLA operacional sugerido: notificação imediata e contato humano em até 5 min em horário comercial, sujeito à capacidade.

## Mensagens (texto do Master V2, a revisar pelo jurídico)
- WhatsApp 01 (Bela): "Olá, {{nome}}! Aqui é a Bela, da Zion Hotel Group International. Recebemos seu interesse em conhecer nosso modelo de negócio. Conheça nossas operações e visão de expansão: {{link_landing}}. Para conversar diretamente com nossa equipe comercial, acesse {{link_whatsapp_prioritario}}. A apresentação é gratuita."
- WhatsApp 02 (prioridade): "Olá, {{nome}}! Recebemos suas informações e gostaríamos de conhecer seus objetivos empresariais. Podemos agendar uma apresentação gratuita do modelo de negócio Zion? Qual horário funciona melhor para você?"

## Riscos e conflitos a decidir
1. Bela de R$ 97 e Zaya respondem no mesmo número (1061): sem roteamento, o investidor recebe resposta de venda.
2. Pixel: o Lovable injeta PageView em `/oportunidades`; nenhum evento de lead será disparado sem aprovação, e nunca com faixa de capital.
3. `robots.txt` do Lovable bloqueia `/oportunidades` (ok para indexação; não afeta anúncio).
4. Jurídico: oferta de "investir capital", venda de operações e participação em operações atuais (CVM 86/88/160). Reunião privada não sana oferta pública irregular.
5. Números do carrossel (+266 mil, +23, +20, +6): ver `docs/ads/investidores-carrossel/PENDENCIAS.md`.

## ATUALIZAÇÃO 28/11 · decisões de Bruno e rascunhos criados no ClickMax
**Decisões:** WhatsApp 01 = final 1061 (ClickMax); WhatsApp 02 = +55 48 98872-9883 (link wa.me, fora do ClickMax); agente novo em rascunho; vídeo só após Bruno conferir o áudio; página fala só de expansão (sem "operações à venda"); pergunta 5 mantida; carrossel só com números documentados (+23 destinos, +20 anos, desde 2020, +260 mil seguidores; fotos originais do campeão mantidas; print do Instagram ainda pendente).

**Criado no ClickMax (workspace Bruno's Workspace), tudo RASCUNHO, nada ativo, nada enviado, nenhum lead tocado:**
| Item | ID | Estado |
|---|---|---|
| Tags ZI_NOVO_LEAD, ZI_ORIGEM_META, ZI_ORIGEM_WEB, ZI_BELA_DISPARO, ZI_ATENDIMENTO_PRIORITARIO, ZI_PERFIL_ADERENTE, ZI_REUNIAO_AGENDADA, ZI_EM_NEGOCIACAO | `046bec8d…`, `1ad1e6c3…`, `dcf3c47d…`, `945023c0…`, `fb0eb2b0…`, `c2a26139…`, `f4a002fc…`, `1a2b4d07…` | criadas |
| Agente "Bela · Investidores (rascunho)" | `ac23f31d-2c64-42e3-87e3-f9ebb70a9dc5` | `draft`, sem publicação nem posto; escolta de 3 regras |
| Modelo WhatsApp `investidores_boas_vindas` (UTILITY, pt_BR, canal 1061) | `814a0a86-9ff5-4f21-bdd5-a3bf202f8ac1` | `draft` local, **não enviado à Meta**; Bruno e jurídico revisam antes do `gupshup_templates_submit` (categoria UTILITY pode ser reclassificada para MARKETING pela Meta) |
| Fluxo "Zion Investors · cadastro → CRM + Bela + fila prioritária (rascunho)" | `cd2fa28f-ab95-499c-a872-dee83e8dd151` | `draft` **vazio**: faltam gatilho (webhook do site / formulário Meta), passos e travas |

**Ainda não feito:** gatilho webhook e passos do fluxo; campos personalizados (destino, prazo, preferência, intenção declarada, consentimento); ligação do `ZION_CONFIG.ENDPOINT`; tarefa prioritária e aviso ao responsável; roteamento de respostas da Bela atual (R$ 97) para a nova; nenhum teste real de disparo (exige "aprovado").

## Regra de escopo (Bruno, 28/11): só expansão e investimentos
As opções de investimento ou venda das operações de Urubici e Florianópolis ficam **à parte**: não aparecem na página, no formulário, no carrossel nem nas mensagens. Urubici e Florianópolis aparecem apenas como prova de que o modelo já funciona. Formulário passou a 8 perguntas: saiu "operações existentes / novas / ambas" e a de destino virou região de interesse (Sul / outras regiões / qualquer destino / ainda não sei), **proposta minha, a confirmar**. Para o canal de conversa sobre as operações, criar depois um fluxo/lista separado, com aprovação e revisão jurídica próprias.

## ATUALIZAÇÃO 28/11 (noite, 2) · landing publicada, formulário do Meta e estrutura no ClickMax
**Landing publicada com "aprovado" de Bruno** (merge na `main`, sem campanha e sem disparo): origem `https://bchaerk-creator.github.io/zion-hotel-ai-developer/investidores/` conferida no ar (título, fonte, imagens, 390 px sem rolagem lateral); link para o Meta: **https://www.zionhotelgroup.com/oportunidades** (o wrapper do Lovable busca a origem a cada 30 s; este ambiente não alcança o domínio `www`, conferir no celular). Carrossel **fora** da página pública até o print do Instagram e o jurídico.
**Formulário nativo do Meta (v1, ARQUIVADO; vigente é o `1177931711576787`):** `1143109468438825`, página Zion Glamping Collection `576944608845537`, conta de anúncios Zion Collection 2. 8 perguntas + autorização de WhatsApp (Sim/Não) + nome, telefone, cidade, estado; "Higher intent" ligado; privacidade `zionhotelgroup.com/privacidade`; botão final → `/oportunidades`; sem preço, sem faixa de capital. O Meta não deixa editar: para mudar, criar outro e arquivar este com `set_lead_form_status`. **A autorização é uma pergunta: o fluxo só pode disparar quando `autoriza_whatsapp` = "Sim, autorizo".**
**ClickMax (tudo rascunho/inativo):**
| Item | ID |
|---|---|
| Projeto "Zion Investors" | `1809f361-924d-4150-a0b6-b3ca89a00b1b` |
| Pipeline "Zion Investors" (Novo cadastro, Contato feito, Apresentação agendada, Apresentação realizada, Em negociação, Sem interesse / descartado) | `05a8c52d-b761-46be-8df1-67de797e8e8e` |
| Fluxo (movido para o projeto; ainda sem gatilho e passos) | `cd2fa28f-ab95-499c-a872-dee83e8dd151` |
| Campos: ZI Destino, ZI Prazo, ZI Intenção declarada, ZI Respostas, ZI Consentimento | `526b84cb…`, `ca60c820…`, `355af2ce…`, `94db7a99…`, `1f9eb0fd…` |
| Modelo `investidores_boas_vindas` agora **MARKETING** (botão "Sair"), draft, não enviado à Meta | `814a0a86…` |
**Falta:** gatilho webhook e passos do fluxo (tags, modelo, tarefa, aviso ao Bruno); URL do webhook na landing; agenda própria de investidores; roteamento da resposta no 1061; ingestão do formulário do Meta (sem usar a sincronização do Land Bank); campanha (nada criado, teto R$ 0 para esta frente); evento de lead no pixel; carrossel na página.

## ATUALIZAÇÃO 28/11 (noite, 3) · chamada única
Chamada oficial (Bruno): **"Quem disse que você tem que construir um grande hotel para começar a faturar com hospedagem? Seja um investidor da Zion."** Aplicada na landing (H1, descrição, botão "Seja um investidor da Zion", título do formulário), no cartão 1 do carrossel e no cartão de abertura do formulário do Meta. A página se chama **Investidores** (como no menu do site; rota `/oportunidades`).
**Formulário do Meta vigente: `1177931711576787`** (v2, mesma chamada). O `1143109468438825` foi **arquivado** (nunca vinculado a anúncio). Atenção jurídica: "começar a faturar com hospedagem" é frase de resultado financeiro; está na landing pública por decisão de Bruno e vai no pacote de revisão (CVM 86/88/160, Código de Defesa do Consumidor e regras de publicidade do Meta para serviços financeiros).
