# Zion Investors × plataforma Zion Collection: regras para não misturar (28/11/2026)

Duas frentes distintas, com públicos, promessas e mensagens diferentes:
| | Plataforma Zion Collection | Zion Investors |
|---|---|---|
| Público | dono de terreno, operador, quem quer estruturar projeto | quem quer conhecer a expansão e investir |
| O que é | acesso pago à plataforma (R$ 47 / R$ 97), com portal, fichas e dossiê | cadastro gratuito + apresentação empresarial gratuita |
| Página | `infoprodutos-zion.clickmax.space/inscricao`, `zionhotelgroup.com/inscricao` | `zionhotelgroup.com/oportunidades` |
| Agente | Bela `a8a076d4…` (vende R$ 97, **proíbe reunião**), Zaya (reunião de diagnóstico) | Bela · Investidores `ac23f31d…` (rascunho) |
| Nunca aparece | reunião, investidor, sócio, "investir" | preço, checkout, plataforma, Clube, Land Bank, ferramentas |

## Pontos de contato encontrados (ClickMax, só leitura)
1. **Mesmo WhatsApp 1061.** A Bela de R$ 97 (posto ativo) recebe todas as respostas do número. Resposta de investidor cairia nela e levaria o link de pagamento. **Regra:** roteamento por etiqueta `ZI_BELA_DISPARO`/`ZI_NOVO_LEAD` para a Bela de Investidores só com "aprovado"; até lá, nenhum disparo.
2. **Funil SDR / pipeline "1 · Desenvolvimento Zion"** (fluxos "Entrada de Lead — Meta → CRM → Funil" e "TAG AUTOMÁTICA · PREENCHEU FORMULÁRIO (META)", que aplica `FORMS FACEBOOK NATIVO`). **Regra:** lead de investidor **não** entra nesses pipelines; criar pipeline e projeto próprios "Zion Investors". O fluxo rascunho `cd2fa28f…` caiu no projeto padrão; mover para o projeto de investidores antes de montar.
3. **Gatilho `crm.lead.captured.v1`** (fluxos "Entrada de Lead — Meta → CRM → Funil" e "NM · Caminho A", este preso a um funil próprio). **Regra:** o gatilho do fluxo de investidores deve ser restrito pela origem `ZI_ORIGEM_*` ou pelo webhook próprio, nunca pelo gatilho geral de lead capturado.
4. **Sincronização horária Meta → ClickMax** (`producao/clube/sync-meta-form/`) atende só o formulário "Land Bank | Diagnóstico do terreno" e aplica `META | FORM LAND BANK`. **Regra:** o formulário nativo de investidores do Meta **não** entra nessa rotina; precisa de ingestão própria que aplique só `ZI_ORIGEM_META` + `ZI_NOVO_LEAD`.
5. **Agenda e lembretes:** "Lembretes da reunião · Zaya" e "Alerta · Reunião Land Bank agendada" disparam em qualquer `crm.scheduling.booked`. **Regra:** a reunião de investidores não usa a agenda do Land Bank nem a de diagnóstico; agenda própria, ou marcação pela equipe com tarefa, sem esses gatilhos.
6. **Etiquetas existentes** (`INVESTIDOR`, `CLUB | BUBBLE · COM INVESTIDOR`, `DISPARO …`, `COMPROU`, `CLUB 97 | COMPROU`, `ZC | …`) pertencem a outras frentes. Investors usa só `ZI_*`.
7. **Um contato, uma conversa ativa.** Quem já está na sequência de R$ 97 ou já comprou (`COMPROU`, `CLUB 97 | COMPROU`) **não recebe** o disparo de investidores: vira tarefa para o humano decidir. O inverso também: quem tem `ZI_*` ativo não entra em abertura de R$ 97.
8. **Dedupe por telefone (`merge`):** o mesmo número pode ser dono de terreno e investidor. O cadastro de investidor só **acrescenta** `ZI_*` e campos próprios; não sobrescreve campos da plataforma nem o card dela.

## No conteúdo (verificado)
- Página `docs/investidores/index.html`: nenhuma menção a plataforma, Clube, Land Bank, ferramentas, preço ou checkout (teste automatizado), e nenhum link para `/raio-x`, `/inscricao` ou `/metodo-zion`.
- Carrossel: sem preço e sem plataforma; destino = formulário de investidores.
- Bela · Investidores: não oferece produto/plataforma; quem quer plataforma ou Bubble é redirecionado (loja) ou passado à equipe.
- Operações de Urubici e Florianópolis (opções de investimento/venda): **fora** deste funil, em fluxo e lista próprios, depois.

## O que falta fazer antes de ligar
Projeto e pipeline "Zion Investors"; mover o fluxo rascunho; restringir gatilhos conforme acima; ingestão própria do Meta; agenda própria; roteamento da resposta no 1061; teste com contatos internos (nunca com leads reais) e aprovação comercial e jurídica.
