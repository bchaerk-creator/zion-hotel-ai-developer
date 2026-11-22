# Operação Zion Recovery 3000 · Relatório para aprovação estratégica
Data: 22/11/2026 · Escopo: só Zion Collection (workspace Bruno's Workspace) · Fases 1 a 4 · **nada foi enviado, comprado, publicado, alterado ou ativado.**

## 0. Resumo em dez linhas
1. A base tem **2.837 contatos**, não 3.000. Em 15 dias de dados do ClickMax, só 3 produtos têm venda (R$ 97 + R$ 47 + R$ 19 brutos) e a carteira tem R$ 144,57 disponíveis.
2. **Risco nº 1: a assinatura do ClickMax está com pagamento recusado** (plano Professional, R$ 697/mês; cartão final 6448). Há nova tentativa automática hoje, 22/11 às 15h01 (Brasília), e o prazo final é 04/12. Sem resolver, o envio pode parar.
3. **Risco nº 2: o WhatsApp falhou em massa.** O disparo de 16/11 para 589 operadores teve **580 falhas e 0 entregas**. No total histórico, 672 mensagens falharam e só 300 contatos receberam entrega. A causa não aparece nas ferramentas; precisa ser descoberta antes de qualquer lote.
4. **E-mail tem baixa resposta:** 163 e-mails de campanha, abertura 3,7% (com 10 bounces, 6–9% por lote). Além disso, 48 e-mails estão marcados como inválidos.
5. A **permissão de comunicação não prova consentimento**: 2.837 de 2.837 contatos aparecem como "autorizados", o que parece ser o padrão do sistema. Só 3 descadastraram no e-mail e 0 no WhatsApp.
6. **A Zaya hoje contradiz a nova estratégia**: o prompt dela convida para reunião gratuita e proíbe falar de preço ou enviar checkout. Precisa ser reescrita antes do funil (não toquei nela).
7. A oferta de R$ 270 **já existe e está aprovada** (adesão ao Clube com Sessão de onboarding e estratégia, oferta `f16e61ac…`, checkout `5q1Ndy1cIS`) e a automação de pós-compra está ativa. Não precisa criar oferta nova.
8. Existem **99 templates de WhatsApp aprovados** no número Zion Collection (qualidade GREEN, limite 2 mil contatos por dia). Dá para reaproveitar boas-vindas, carrinho e Pix pendente. Os de venda do clube nova ainda precisam ser criados e aprovados pela Meta.
9. Recomendo um **piloto de 200 contatos** só depois de resolver os itens 2 e 3, e com meta realista: o histórico não sustenta prometer que o piloto se paga.
10. Decisões que preciso de você estão na seção 7.

## 1. Fase 1 · Auditoria da base (somente leitura)

### 1.1 Números confirmados
| Item | Quantidade | Fonte |
|---|---|---|
| Contatos (excluindo mesclados) | **2.837** | contagem do ClickMax |
| Com telefone | 2.805 | filtro de telefone preenchido |
| Com e-mail | 2.815 | filtro de e-mail preenchido |
| Entrada por mês | set 1.741 · out 933 · nov 163 | snapshot da conta |
| Compraram (qualquer produto) | **2** (filtro de compras), 3 vendas no painel | contagem de compras e dashboard |
| Marcados como "autorizados" para mensagem | 2.837 WhatsApp · 2.834 e-mail | filtro de preferências (ver ressalva) |
| Descadastrados | 0 WhatsApp · **3** e-mail | filtro de preferências |
| E-mail marcado inválido | **48** | filtro de status do e-mail |
| Com tag "REUNIÃO REALIZADA" | 16 | tag |
| Com tag "REUNIÃO | AGENDADA" | 5 + 3 (duas tags com o mesmo nome) | tag |
| Com diagnóstico (alto 18 · ajustes 34 · preparação 8) | **60** (contagem sem repetição) | tags DIAG |
| Cadastrados pelo formulário nativo do Meta | 194 | tag FORMS FACEBOOK NATIVO |
| Do formulário Land Bank (Meta) | 106 | tag META \| FORM LAND BANK |
| Já receberam algum disparo de terreno/triagem/operador | 1.605 (soma sem repetição de 4 tags) | tags de disparo |
| Compraram "Raio-X R$ 270" | 3 | tag RAIOX \| PAGOU R$270 |
| Land Members · Radar comprou | 3 | tag |
| Compraram Trilha 1 | 2 | tag |
| Dono de terra de mais de 50 mil m² | 4 | tag |
| Capital de R$ 400 mil a R$ 3 mi / acima de R$ 3 mi | 18 / 10 | tags |
| Pediram "não quer receber" no funil de terreno | 0 | tag |
| Entregas de WhatsApp com sucesso / falha (histórico) | 300 / 672 contatos | marcas do sistema |
| Reuniões agendadas | 58 reuniões, 40 contatos | agenda do pipeline |

### 1.2 Reuniões (58)
- 38 "agendadas" no passado e **nunca fechadas** (nem "realizada" nem "faltou"): a agenda precisa ser conciliada antes de falar em no-show.
- 5 futuras · 14 canceladas · 1 faltou (no_show).
- Com isso, **o número de "agendamentos sem comparecimento" não é confiável hoje**: o sistema marca 1, a realidade pode ser até 38.

### 1.3 O que não consegui medir
| Pedido | Situação |
|---|---|
| Contatos duplicados | A ferramenta de duplicados não foi usada (é uma varredura pesada). Vou rodar na fase de preparo do lote, só leitura. |
| Proprietários de terreno sem capital | Tags de faixa de capital estão zeradas (0 em quase todas); a resposta está nos campos do formulário (`investimento`, `falta_papel_meta`). Precisa de consulta pelos campos personalizados. |
| Interessados em Bubble | As tags de Bubble têm 0 a 1 contato ("CLUB \| BUBBLE"); a base de Bubble de 2026 está vazia. A lista "ZION_01_VENDA_ATIVO_BUBBLE" também tem 0. Não há segmento de Bubble utilizável hoje. |
| Histórico de mensagens por contato | Só por amostragem. Existe por contato, mas não em massa. |
| Origem dos leads | 8 origens: CxFlows, CxQuizzes, CxPages, CxForms, CxCalendar, CxExternalPages, CxClub, CxClients. Contagem por origem não levantada. |

### 1.4 Ressalva importante sobre consentimento
O ClickMax marca 2.837 de 2.837 contatos como "autorizados". Isso mostra o **padrão do sistema, não um aceite registrado**. Os contatos vieram de formulários do Meta, páginas e quizzes (interesse declarado), o que sustenta um contato comercial relacionado, mas não é opt-in explícito para WhatsApp. Recomendo: toda mensagem com saída clara ("responda SAIR para não receber mais"), quem respondeu "SAIR/PARAR/não quero" sai de todas as sequências, e o piloto começa só com quem já interagiu (formulário, resposta, reunião, diagnóstico).

## 2. Fase 2 · Infraestrutura ClickMax

| Recurso | Situação |
|---|---|
| **Plano** | Professional (R$ 697/mês). **Pagamento recusado em 09/11**, 2 tentativas, próxima hoje 15h01, prazo 04/12. Contatos: 1.108 contabilizados de 30.000 no limite. |
| **Créditos** | Pacote 12.500 + 20.000 extras = 32.500; usados 21.865; **restam 10.635**. O custo por mensagem em créditos não é exposto pelas ferramentas; precisa ser confirmado antes (ver seção 6). |
| **WhatsApp** | Número **Zion Collection** `554861371061` ao vivo, qualidade GREEN, limite 2 mil contatos por dia (Meta TIER_2K). Há outro número, "Pablito Ads", que **não será usado** (restrição). Total de 99 templates aprovados, 25 rascunhos. |
| **E-mail** | Envio funcionando por campanha. Nenhuma caixa de e-mail corporativa conectada (só remetente do ClickMax). Histórico: 20 campanhas, 163 envios, abertura 3,7%, bounce 6,8%. |
| **SMS / voz / Instagram** | Voz usada em 16 envios (áudio de Bruno, abertura 87,5%). SMS e Instagram: não usados. |
| **Automações** | 100 no total. Há uma ativa para o pós-compra da adesão de R$ 270 (2 tags + 1 tarefa, sem mensagem). |
| **Segmentação** | Disponível: tags, listas, filtros por campos, por engajamento de e-mail e por evento do sistema. Dá para montar o lote de 200 sem exportar nada. |
| **Checkout** | Oferta de R$ 270 aprovada, Pix e cartão à vista. Vendedor ainda "em análise" na conta, mas as ofertas já vendem (houve 3 vendas). |
| **Área de membros** | 4 portais; o Clube tem as duas turmas já ligadas à oferta. |
| **Zaya (IA)** | Ativa no WhatsApp, 99 conversas, 31 escaladas. **Prompt atual conflita** (ver seção 0, item 6). Existe também um rascunho "Social Seller · Limpeza da base" parado. |
| **Rastreio de compras Asaas** | O Asaas grava as compras no ClickMax por webhook do site (Lovable). Se o site ficar sem crédito/atualização, essa trilha fica sem manutenção. Para a nova oferta **não depende do Asaas**: o checkout é do ClickMax. |

### Ativos reaproveitáveis
- Oferta, checkout, página e automação de R$ 270 (prontos).
- Templates aprovados: `zion_clube_boas_vindas` (utilidade), `zion_clube_carrinho`, `zion_clube_pix_pendente` (utilidade), `zion_clube_form_1/2/3`, `zion_club_ecossistema`, `zion_conheca_a_zion`, `zion_nao_agora`. Atenção: `zion_clube_downsell_47` traz preço de R$ 47: **não usar**.
- Áudios e vídeos autorais de Bruno: a base tem envios de voz com 87,5% de abertura; o canal funciona.
- Listas de disparo anteriores (P1 a P4, corretores), úteis só como segmento de exclusão (quem já recebeu).

## 3. Fase 3 · Funil ECROI de 14 dias (6 contatos principais)

Todos os caminhos levam à página de apresentação do Clube e ao checkout de R$ 270. Sem reunião individual gratuita. Sem promessa de reservas, renda, investimento ou valorização.

| # | Dia | Canal | Papel ECROI | Conteúdo (resumo) |
|---|---|---|---|---|
| 1 | D0 | WhatsApp (template) + e-mail | **Espelhamento** | Reconhece o interesse que a pessoa mostrou no formulário ("você nos disse que tem terreno em ..."). Apresenta a mudança: a Zion passou a atender dentro do Clube. Link para a página. |
| 2 | D2 | E-mail com vídeo curto de Bruno | **Colapso de crença** | O que o Clube inclui, em 8 itens. Vídeo de Bruno explicando como as sessões e as áreas funcionam. |
| 3 | D4 | WhatsApp (áudio de Bruno, quando houver janela) | **Reencadramento** | "Tem pergunta antes de entrar?" Resposta rápida sobre acesso de 12 meses e sessão de onboarding. |
| 4 | D7 | E-mail | **Inevitabilidade** | Passo a passo de como é o primeiro mês dentro do Clube. Sem urgência falsa. |
| 5 | D10 | WhatsApp | **Resultado viral** | Convite para quem ainda tem dúvida: responder aqui. Quem responder vai para atendimento humano. |
| 6 | D13 | E-mail + WhatsApp | **Custo invisível** | Último contato claro: "se agora não é o momento, tudo bem". Sem desconto, sem bônus novo. |

### Regras de parada
- **Pagamento confirmado** (evento do checkout) → sai das mensagens de venda e entra na jornada de boas-vindas já existente.
- **Respostas negativas** ("não quero", "sair", "parar", "descadastrar") → sai de todos os canais conforme a preferência do contato e recebe a tag de saída.
- **Resposta com dúvida** → vai para atendimento humano (Bruno ou equipe). A Zaya só entra depois de reescrita.
- Contato com reunião já agendada → fora do lote.
- Quem comprou algo antes ou está em negociação → fora do lote.
- Nenhuma mensagem entre 22h e 8h.

### O que precisa ser criado (só depois de aprovado)
- 3 a 4 templates de WhatsApp de venda do Clube (aprovação da Meta leva de horas a dias) e 3 e-mails, com os vídeos de Bruno.
- Ajuste da Zaya: sem reunião gratuita; pode explicar o Clube e mandar o link; escala dúvidas para humano.
- Automação do funil de 14 dias (criada **desligada** e testada com os contatos de Bruno antes de qualquer lote).

## 4. Fase 4 · Piloto de 200 contatos

### 4.1 Critérios de seleção
- Tem telefone válido **e** e-mail válido (os 48 inválidos saem).
- Já demonstrou interesse por ação própria (formulário do Meta, diagnóstico, resposta ao WhatsApp ou reunião), nunca só por importação.
- Sem compra anterior, sem reunião futura, sem tag de atendimento humano, sem pedido de saída.
- Fora do universo "Pablito Ads" e "Zion Bubble".
- Prioridade: os 60 com diagnóstico, depois os 194 do formulário nativo e os 106 do Land Bank, depois quem respondeu a disparos.
- O lote exato (200 nomes) só sai depois da aprovação, como lista em rascunho para você ver.

### 4.2 Estrutura de acompanhamento
Planilha de acompanhamento pronta em `producao/recovery-3000/ACOMPANHAMENTO_PILOTO.csv`, com uma linha por dia e por canal. Onde cada número vem:

| Indicador | Origem |
|---|---|
| Mensagens entregues | status da campanha/automação (ClickMax) |
| Aberturas | e-mail: campanha; WhatsApp: leitura da mensagem |
| Cliques | links rastreados (UTM `recovery3000`) |
| Respostas | conversas do WhatsApp e do e-mail |
| Visitas à página | analytics da página (visitantes únicos) |
| Checkouts iniciados | evento do checkout |
| Pagamentos confirmados | transações da oferta de R$ 270 |
| Reembolsos | transações |
| Custo por aquisição | custo do envio ÷ pagamentos confirmados |
| Receita líquida | pagamento menos taxas e reembolsos |
| Descadastramentos | preferências de mensagem |
| Cadastros no Land Bank | tag/ficha do Land Bank (a definir com a origem do cadastro) |

UTM padrão: `utm_source=zion&utm_medium=whatsapp|email&utm_campaign=recovery3000&utm_content=d0|d2|d4|d7|d10|d13`.

### 4.3 Custos estimados (a confirmar antes de gastar)
**O ClickMax não expõe o custo por mensagem em créditos nas ferramentas.** Por isso, o quadro abaixo é uma **estimativa com premissas explícitas**, não um orçamento:

| Item | Premissa | Piloto (200) | Operação completa (~2.800) |
|---|---|---|---|
| WhatsApp (3 mensagens de marketing por contato, só ao que tiver janela e número válido) | a confirmar na Gupshup/ClickMax o preço por template de marketing no Brasil | 600 mensagens | 8.400 mensagens |
| E-mail (3 por contato) | dentro do plano; não consome crédito de WhatsApp | 600 | 8.400 |
| Créditos disponíveis | 10.635 restantes | cobre o piloto se 1 mensagem = 1 a 5 créditos (a confirmar) | **só cobre se 1 mensagem for 1 crédito** |
| Assinatura | R$ 697/mês, hoje com pagamento recusado | custo fixo existente | custo fixo existente |
| Vídeos/áudios de Bruno | sem custo de envio; tempo de Bruno | 3 gravações | as mesmas |
| Anúncios | **R$ 0** (teto atual) | R$ 0 | R$ 0 |

### 4.4 Expectativa realista (hipótese, não promessa)
Referências do próprio histórico: e-mail abre ~4–5% e clica ~1%; WhatsApp falhou em mais da metade. Com 200 contatos, cenários de **hipótese** de conversão:
| Conversão | Vendas | Receita bruta |
|---|---|---|
| 0,5% | 1 | R$ 270 |
| 1% | 2 | R$ 540 |
| 2% | 4 | R$ 1.080 |

Com o histórico atual, **o piloto serve para medir e aprender, não para financiar tráfego**. Financiar anúncios só faz sentido depois de ver conversão real em 200 contatos.

## 5. Riscos e pontos de atenção
1. **Cobrança do ClickMax recusada**: resolver o cartão (você) antes de qualquer envio. Hoje 15h01 há nova tentativa automática.
2. **Falha em massa do WhatsApp**: investigar a causa (número com problema, modelo, qualidade, bloqueio de contatos). Sem isso, o funil perde metade do alcance.
3. **Reputação de e-mail**: 6–9% de bounce. Limpar os 48 inválidos e começar pequeno.
4. **LGPD**: consentimento padrão não é prova; incluir saída clara em toda mensagem e honrar na hora.
5. **Zaya contraditória**: reescrever o prompt antes de ligar (sem reunião gratuita, sem preço proibido).
6. **Agenda desconciliada** (38 reuniões passadas abertas): atrapalha qualquer leitura de no-show.
7. **Conflito de marca**: o Clube deve ser apresentado como adesão com sessão incluída, sem promessa de investimento, parceria ou valorização (regra do projeto).
8. **Disciplina de separação**: o funil usa só o número Zion Collection; o número Pablito Ads e as contas de anúncio da Zion Bubble, Pablito e Bruno Ads não são tocados.

## 6. O que eu preciso antes de executar
- Preço por mensagem de WhatsApp de marketing na sua Gupshup/ClickMax e quanto vale 1 crédito (ou um print do extrato de créditos).
- Se o cartão do ClickMax já foi atualizado.
- Se existe opt-in registrado em algum formulário que eu não vi (por exemplo, texto de consentimento no formulário do Meta).
- Quais vídeos/áudios de Bruno já existem e podem ser usados.

## 7. Decisões para sua aprovação
1. **Aprova o piloto de 200 contatos** com os critérios acima? (recomendado: sim, depois de resolver cartão e WhatsApp)
2. **Aprova reescrever o prompt da Zaya** (sem reunião gratuita, com o Clube) em rascunho, para você ler?
3. **Aprova criar, desligados, os templates de WhatsApp e os 3 e-mails** para eu mostrar o texto antes de submeter à Meta?
4. **Aprova conciliar a agenda** (marcar as 38 reuniões passadas como realizadas ou faltou) com a sua confirmação, caso a caso?
5. **Aprova eu investigar a falha do WhatsApp** (somente leitura) antes de qualquer lote?

Sem "aprovado" seu, nada acima é executado.
