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
