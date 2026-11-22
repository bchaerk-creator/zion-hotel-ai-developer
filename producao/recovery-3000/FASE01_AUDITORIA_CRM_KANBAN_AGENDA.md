# Zion Recovery 3000 · Fase 01 · Auditoria do CRM, Kanban e agenda comercial
Data de referência: 22/11/2026 · Somente leitura. Nenhum disparo, movimentação, exclusão, tag, automação, checkout, crédito, campanha, cancelamento ou produto foi alterado. Só o ecossistema Zion Collection foi consultado.
Complementa o `RELATORIO.md` de hoje (infraestrutura, funil de 14 dias e piloto).

## 1. Diagnóstico executivo
1. **Receita real comprovada no ClickMax: R$ 0.** As 5 transações da conta são todas de Bruno (mesmo comprador: R$ 97 de teste, R$ 47, R$ 19 e dois Pix de teste de R$ 97 e R$ 270 que não foram pagos). Tenho que corrigir o relatório anterior: quando eu disse "2 compradores e 3 vendas", eram testes seus. **Não existe nenhum cliente externo pagante nesta conta.**
2. **Os pagamentos do Asaas não estão visíveis para mim.** As tags "RAIOX | PAGOU R$270" (3), "LAND MEMBERS | RADAR · COMPROU" (3) e "MÉTODO | COMPROU TRILHA 1" (2) existem, mas não consigo confirmar pagamento por elas, e não tenho acesso ao Asaas. Sem extrato do Asaas, essas compras ficam **não comprovadas**.
3. **Nenhuma reunião está confirmada como realizada pelo sistema.** Na agenda do ClickMax há 0 reuniões com status "realizada". Das 58, 38 estão "agendadas" com data passada, sem desfecho. O Calendly (agenda antiga) tem pelo menos 100 reuniões passadas, também sem registro de comparecimento.
4. **O Kanban tem 11 funis e muita duplicação de cartões.** Somando os cartões dos funis há ~3.770 cartões para 2.837 contatos. Cinco funis estão arquivados (3.5 mil cartões antigos).
5. **A coluna "Comprou" do Funil Zion depende do Asaas e nunca disparou** (0 execuções). O pagamento do ClickMax (R$ 270 do Clube) não está ligado a ela.
6. **A coluna "Reunião feita" nunca recebeu cartão pelo sistema** (0 execuções do gatilho "reunião concluída"). O "feita" hoje só existe por tag manual.
7. **Infra de envio tem dois problemas graves** (já no relatório anterior): cobrança da assinatura recusada e WhatsApp com 58% de falha.
8. Arquitetura recomendada: **um Kanban principal segmentado (Funil Zion existente, reorganizado) + o pipeline de membros que já existe**, em vez de criar três funis novos. Detalhes na seção 7.

## 2. Quantidades reais por segmento
Fonte: contagens do ClickMax em 22/11/2026. Quando é por tag, está escrito.

| Segmento | Qtde | Critério |
|---|---|---|
| Contatos cadastrados | **2.837** | contagem do ClickMax (exclui mesclados) |
| Contatos únicos | **não medido** | a ferramenta de duplicados só compara um contato por vez; precisa de varredura por e-mail/telefone |
| Com telefone / com e-mail | 2.805 / 2.815 | filtros de campo preenchido |
| Entradas por mês | set 1.741 · out 933 · nov 163 | snapshot da conta |
| Clientes pagantes **externos** | **0 confirmados** | transações do ClickMax: só testes de Bruno |
| Nunca compraram | 2.837 (menos testes de Bruno: 2 contatos) | por exclusão do item acima; o Asaas fica de fora |
| E-mail inválido | 48 | filtro de status |
| Descadastrados | 3 e-mail · 0 WhatsApp | filtro de preferências |
| "Autorizados" | 2.837 / 2.834 | **padrão do sistema, não prova de aceite** |
| Entrada por formulário nativo do Meta | 194 | tag |
| Formulário Land Bank (Meta) | 106 | tag |
| Com diagnóstico (alto 18 · ajustes 34 · preparação 8) | 60 | tags DIAG |
| Já receberam disparo de terreno/triagem/operador | 1.605 | soma sem repetição de 4 tags |
| Origem dos leads | 8 origens (CxFlows, CxQuizzes, CxPages, CxForms, CxCalendar, CxExternalPages, CxClub, CxClients); contagem por origem **não levantada** | |

**Histórico de atendimento, mensagens e pagamentos por contato:** existe por contato (conversas, atividades, pagamentos), mas não saiu em massa pelas ferramentas. Dá para extrair por amostra ou por lote definido.

## 3. Agenda comercial, grupos A a I
Sistemas cruzados: **agenda do ClickMax** (58 reuniões, 40 contatos), **Calendly** da conta Zion Glamping Collection (≥ 100 reuniões entre mar e nov/2026, mais antigas ainda numa próxima página), **pipelines** (colunas de reunião) e **tags**. Não classifiquei nenhuma reunião como realizada só porque a data passou.

| Grupo | Qtde | Critério usado |
|---|---|---|
| **A. Realizaram reunião** | **0 confirmadas pelo sistema** · 16 "declaradas" (tag e lista "REUNIÃO REALIZADA", marcadas à mão) · 2 no quadro "Reuniões" ("3 · Reunião feita") · 1 no funil SDR antigo | Só conta como confirmada se o status da agenda for "realizada" ou houver gravação/nota de desfecho. Nada disso existe hoje. As 16 são afirmação humana, não confirmação. |
| **B. Agendaram e não compareceram** | **1** (agenda ClickMax, status "faltou") + 1 no funil SDR antigo | Só status explícito de falta. O Calendly não foi cruzado para faltas. |
| **C. Reunião passada sem confirmação** | **38 reuniões / 32 contatos** (ClickMax, status "agendada" com data até 20/11) · mais ≥ 100 eventos passados no Calendly | Data passada + status ainda "agendada" ou sem desfecho. Esse é o grupo que precisa de conciliação manual. |
| **D. Reuniões futuras** | **5 contatos** (ClickMax, de 22 a 24/11, status "agendada"). Calendly: nenhum evento futuro na primeira página | Status "agendada" com data futura. |
| **E. Nunca agendaram** | **até ~2.790** | 2.837 menos os 40 da agenda do ClickMax, **ainda sem descontar os convidados do Calendly** (falta cruzar e-mail). Número provisório. |
| **F. Mais de uma reunião** | **4 contatos** (ClickMax, contando só reuniões não canceladas; 6 contando canceladas) | contatos com 2 ou mais reuniões. Calendly não cruzado. |
| **G. Receberam proposta** | **não medido** (módulo de propostas não consultado). Aproximação por colunas: 4 em "7 · Oferta feita" + 4 em "6a · Link de adesão enviado" = 8 cartões | proxy, não prova |
| **H. Interessados sem capital** | **5** na coluna "Dor · Sem capital" · 14 com a tag "menos de R$ 5 mil · nutrir" · 12 em "Formulário · menos de R$ 5 mil" | declaração em formulário/qualificação; não verifica capital real |
| **I. Capacidade de comprar uma Bubble** | **28 declarados** (tags "capital R$ 400 mil a R$ 3 mi" = 18 e "acima de R$ 3 mi" = 10); 1 em "Formulário · R$ 5 mil ou mais → agendar" | só autodeclaração em formulário; **nenhum comprovado** |

### Critérios de confirmação que eu recomendo adotar
Uma reunião só é **"realizada"** quando houver pelo menos um destes: status "realizada" na agenda, gravação, nota de resultado, ou confirmação de Bruno caso a caso. Sem isso, fica em "status a confirmar".

## 4. Kanban atual

### 4.1 Funis (11)
| Funil | Estado | Cartões | Observação |
|---|---|---|---|
| **Funil Zion · Novo lead → Reunião → Venda** | **ativo** | 171 | principal; 21 colunas; 16 automações gerenciadas |
| Alunos Zion · Comprou → Acesso → Estudando | ativo | 0 | vazio, sem automação |
| Reuniões agendadas · Zion | ativo | 9 | espelho de reuniões; sem automação |
| Club Zion Collection · Adesão → Pagamento → Membro | ativo | 4 | 4 na coluna "preencheu a ficha" |
| Venda de imóveis · Florianópolis e Urubici | ativo | 6 | só imóveis; não misturar |
| Reserva Direta Zion | ativo | 32 | hospedagem, **fora do escopo** |
| Base antiga · Reativação → Reunião | arquivado | 1.657 | 5 colunas de disparo P1 a P4 |
| FUNIL SDR | arquivado | 1.735 | 1.548 em "base antiga" |
| Parceria Zion | arquivado | 109 | espelho da mentoria |
| 0 · LIGAÇÕES BRUNO | arquivado | 40 | fila de ligação |
| Funil Terreno · Zion Collection | arquivado | 4 | |

### 4.2 Colunas do Funil Zion (21) e contagem
Leads de hoje 19 · Atacar hoje (ontem) 5 · Acumulados 41 · Dor sem capital 5 · Dor quer mentoria 4 · Dor quer parceiro/investidor 8 · Dor não sabe por onde começar 2 · Formulário ≥ R$ 5 mil 1 · Formulário < R$ 5 mil 12 · 2 Zaya qualificando 11 · 3 Ligar hoje (Bruno) 28 · 3b Liguei/áudio 5 (R$ 27.000 de valor lançado) · 4 Já pagou (modelo antigo) 1 · 5 Reunião agendada 20 · 5a Reuniões de hoje 1 · 5b No-show 0 · 6 Reunião feita 0 · 6a Link de adesão enviado 4 · 7 Oferta feita 4 · 8 Comprou 0 · Agora não 0.

### 4.3 Automações do Funil Zion (gerenciadas pelo pipeline)
| Automação | Gatilho | Execuções |
|---|---|---|
| Entrada: Novo lead | tag aplicada / mensagem recebida da Zaya | 106 + 48 |
| Passagem: reunião agendada | agendamento criado | 46 (última 22/11 00h09) |
| Passagem: reunião feita | reunião concluída | **0** |
| Passagem: no-show (da coluna "pagou o Kit R$ 270") | falta registrada | 1 |
| Tarefa: registrar resultado da reunião | atraso em "Reunião feita" | 8 |
| Entrada: Diagnóstico concluído | lead capturado | 0 |
| Entrada: Pagamento pendente | tag | 0 |
| **Passagem: 8 · Comprou** | **pagamento confirmado no Asaas** | **0** |
| Passagem: Agora não · nutrir | tag | 1 |

### 4.4 Nativo do ClickMax × depende de integração externa
| Nativo | Depende de externo |
|---|---|
| Pipelines, colunas, cartões, tags, listas, segmentos | **Asaas** (webhook do site Lovable → ClickMax): tags e coluna "Comprou" antigas |
| Agenda ("Equipe Zion"), agendamento público, lembretes | **Calendly**: agenda antiga, sem integração com o CRM |
| Checkout, oferta, área de membros, automação de pós-compra | **Meta** (formulários, via Windsor.ai e rotina horária) |
| WhatsApp pela Gupshup (embutida), e-mail, voz, Zaya | **Lovable** (site, páginas e webhooks): sem crédito hoje |

### 4.5 Inconsistências e riscos
1. **Cartões duplicados entre funis.** ~3.770 cartões para 2.837 contatos: o mesmo contato está em 2 ou 3 funis (base antiga, SDR, Funil Zion). Não mover em massa sem antes mapear.
2. **Coluna "Comprou" amarrada ao Asaas.** A compra do Clube de R$ 270 (ClickMax/Ticto) não move cartão nenhum. A automação de pós-compra só coloca tags e cria tarefa.
3. **"Reunião feita" depende de status que ninguém marca.** 0 execuções.
4. **38 reuniões passadas sem desfecho** e 4 cartões na coluna "Reuniões agendadas · Zion" parados em "Passou do horário".
5. **Textos antigos nos funis**: a descrição do Funil Zion ainda fala em "reunião estratégica sem custo" e em R$ 2.900/R$ 490/R$ 270 (Land Bank), que já não representam a oferta.
6. **Tags com o mesmo nome** ("REUNIÃO | AGENDADA" aparece duas vezes) e **133 das 198 tags com 0 contatos**, o que confunde segmentações.
7. **Perda de histórico**: mover o cartão preserva histórico; excluir/recriar não. Nunca recriar contatos por etapa.
8. **A virada diária do Kanban** (que você aprovou) está parada por negativa do sistema de permissões; o board do dia está acumulando.

## 5. Auditoria das ferramentas de follow-up
(Resumo; detalhes no `RELATORIO.md`.)
| Item | Situação |
|---|---|
| E-mail | funciona; abertura 3,7%; bounce 6–9%; 48 inválidos |
| WhatsApp | número Zion Collection GREEN, limite 2 mil/dia, 99 templates aprovados; **580 de 580 falharam** em 16/11; 58% de falha histórica; causa desconhecida |
| Zaya | ativa; prompt oferece reunião gratuita e proíbe checkout (conflita com a nova oferta) |
| Automações | 100 no total (47 ativas) |
| Tags / segmentos / remarketing | disponíveis; segmento por engajamento de e-mail e por evento do sistema |
| Créditos | 10.635 restantes de 32.500; custo por mensagem não exposto |
| Entregabilidade | e-mail: 6–9% de bounce; WhatsApp: ruim |
| Descadastramento | por preferência de contato; 3 e-mail, 0 WhatsApp |
| Parada após compra | possível por evento de pagamento; **a nova automação de pós-compra não interrompe mensagens de venda**, pois não envia nenhuma; a sequência de recuperação precisa ter condição "comprou" própria |

### Custo para 200, 500, 1.000 e 3.000 contatos elegíveis
O preço por mensagem não é exposto pelas ferramentas, então mostro o **volume** e a **fórmula**. Custo = mensagens × preço unitário confirmado.

| Contatos | WhatsApp (3 por contato) | E-mail (3 por contato) | Observação |
|---|---|---|---|
| 200 | 600 | 600 | 1 dia de limite da Meta |
| 500 | 1.500 | 1.500 | 1 dia de limite da Meta |
| 1.000 | 3.000 | 3.000 | exige 2 dias de limite |
| 3.000 (base inteira) | 9.000 | 9.000 | 5 dias de limite; **só 2.805 têm telefone** |

Exemplo **hipotético**, só para ilustrar a conta, com preço unitário de R$ 0,30: 600 mensagens = R$ 180; 1.500 = R$ 450; 3.000 = R$ 900; 9.000 = R$ 2.700. **Esse preço não é dado confirmado**: preciso do valor real da Gupshup/ClickMax para fechar o orçamento. O limite de 2 mil por dia e os 10.635 créditos restantes também só se convertem em custo depois dessa confirmação.

## 6. Auditoria financeira
| Pergunta | Consigo identificar? | Como / limite |
|---|---|---|
| Quem nunca comprou | **Sim** | 2.837 menos os 2 contatos de Bruno (testes) para ClickMax; Asaas fora |
| Quem iniciou checkout | **Parcialmente** | transações com status pendente/falhou: só 2 (Bruno). Início de checkout sem Pix gerado não aparece em transação; precisaria da leitura de visitantes por página |
| Pagamento pendente | **Sim** | 0 hoje no ClickMax (o Pix de teste de R$ 270 passou a "falhou") |
| Pagamento confirmado | **Sim, só ClickMax** | 3 pagas, todas de Bruno (R$ 97 teste, R$ 47, R$ 19). **Asaas: não verificável por mim** |
| Reembolso | **Sim** | 0 no ClickMax |
| Produto adquirido | **Sim** | cada transação traz oferta/produto |
| Origem comercial da compra | **Parcial** | transações trazem UTM; só a de R$ 270 de teste tem UTM (`site/pagina/agendamento-diagnostico`). As demais não têm |

**Regra adotada:** não usei tags como prova de pagamento. Onde só há tag (Asaas), a compra aparece como "não comprovada".
Sugestão: você exporta o extrato do Asaas (CSV, sem dados de cartão) para eu conciliar por e-mail/CPF, em leitura.

## 7. Arquitetura recomendada
### Comparação
| Opção | Prós | Contras |
|---|---|---|
| **A. Três funis novos e separados** (como você propôs) | visão limpa por etapa do negócio | exige mover cartões entre funis; **risco de duplicar cartões**, já alto; cada funil precisa das próprias automações |
| **B. Um Kanban principal segmentado + pipeline de membros existente** (recomendada) | reaproveita o Funil Zion (171 cartões vivos) e o pipeline "Alunos Zion"; um cartão por contato; menos migração | exige renomear/reorganizar colunas (em rascunho, com aprovação) |
| C. Tudo em um único funil | simples | mistura recuperação, venda nova e membros; relatórios confusos |

### Recomendo a opção B, com 3 "raias" no mesmo ecossistema
1. **Funil 01 · Recovery 3000** → usar o **Funil Zion** atual, reorganizando colunas existentes: Acumulados · Reuniões realizadas (só confirmadas) · Não compareceram · **Status a confirmar** (as 38) · Reuniões futuras · Em recuperação · Interessados · Checkout pendente · Compra confirmada. Muitas colunas já existem ("5 Reunião agendada", "5b No-show", "6 Reunião feita", "8 Comprou").
2. **Funil 02 · Cold Sales** → **um segundo pipeline novo**, só para leads novos que entram **depois** de 22/11 (novo lead → apresentação → follow-up → checkout iniciado → pagamento pendente → compra). Cartão novo só para quem não existe no Funil 01.
3. **Funil 03 · Members e Land Bank** → **reaproveitar "Alunos Zion"** (mudando colunas) ou "Club Zion Collection · Adesão → Membro": novo membro → boas-vindas → cadastro territorial → documentação pendente → diagnóstico preliminar → sessão agendada → sessão realizada → oportunidade qualificada → em estruturação.

### Regras para não duplicar nem perder histórico
- **Um contato = um cartão por funil**; a ferramenta de "adicionar a funil" já ignora quem tem cartão naquele funil.
- **Mover cartão preserva histórico**; nunca excluir/recriar.
- Passar de um funil para outro por **transferência de cartão**, não por cópia.
- Antes de qualquer migração: foto (export) dos cartões e das tags; migração em lote pequeno (10 a 20 cartões) com conferência.
- Compra confirmada (evento do checkout do ClickMax) move o cartão do Funil 01/02 para o 03.

## 8. Ativos reaproveitáveis
Oferta, página e automação de R$ 270; Funil Zion e suas automações de reunião; 99 templates aprovados; número Zion Collection; pipeline de membros; Zaya (após reescrita); lista "Leads da semana"; segmentos e tags de diagnóstico.

## 9. Plano de organização do CRM (proposto, só depois de aprovado)
1. **Conciliar a agenda** (sem alterar status ainda): lista das 38 reuniões passadas e das 16 "declaradas" para você marcar em bloco: realizada, faltou ou não aconteceu.
2. **Conciliar compras**: extrato do Asaas contra e-mail/CPF.
3. **Mapear duplicados**: varredura de e-mail e telefone, em leitura, gerando relatório.
4. **Corrigir a ligação "compra → coluna"** com o evento do ClickMax, em rascunho.
5. **Reorganizar colunas do Funil Zion** (renomear e acrescentar) em rascunho, para você ver.
6. **Limpar tags** duplicadas ou sem contatos: só depois de verificar que nenhuma automação as usa.
7. Retomar a virada diária do Kanban só depois do passo 5.

## 10. Pontos que precisam de aprovação
1. Opção B (um Kanban principal + membros) em vez de três funis novos?
2. Autorizar a leitura dos convidados do Calendly (e-mails) para cruzar com o CRM?
3. Você envia o extrato do Asaas para conciliar compras?
4. Aprova a regra de "reunião realizada" só com confirmação (status, nota ou sua palavra)?
5. Aprova eu preparar, em rascunho, a lista das 38 reuniões para você classificar?
6. Autoriza eu mapear duplicados (leitura)?

## 11. Proposta de piloto comercial
Igual ao `RELATORIO.md`, com duas correções vindas desta auditoria:
- O piloto de 200 usa **só quem tem desfecho conhecido ou interesse recente**, e exclui os 5 com reunião futura e os 4 com mais de uma reunião.
- A medição de vendas usa **só pagamentos do ClickMax**, já que o Asaas não é verificável por mim. Receita é contada com pagamento confirmado, nunca por tag.
- Antes do piloto: cartão do ClickMax, causa da falha do WhatsApp e reescrita da Zaya.

## 12. O que não consegui medir
- Contatos duplicados (precisa de varredura).
- Calendly: cruzar convidados com o CRM (as próximas páginas e os e-mails).
- Propostas comerciais (módulo não consultado).
- Pagamentos do Asaas.
- Contagem por origem.
- Capital real dos interessados (só autodeclaração).
- Histórico de mensagens por contato em massa.
