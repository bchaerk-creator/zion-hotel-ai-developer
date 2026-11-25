# LGPD, base legal, consentimentos e arquitetura de públicos · Funil híbrido da Mini Mentoria de Estruturação Zion

Agente: ZION MARKET (função de conformidade e arquitetura de públicos) · 25/11/2026.
**Este documento NÃO é parecer jurídico.** Tudo que for análise legal está marcado **[a validar por advogado]**. Marcação de evidência: [E] lido neste ambiente, [H] hipótese, [NC] não confirmado.
Nada foi criado, enviado, subido ou alterado no Meta, no ClickMax, no WhatsApp ou em produção. Sem dado pessoal e sem número real de gasto neste arquivo.

Base já escrita e reaproveitada (não repetida): `09-tracking/README.md` e `05-funis/README.md` (seções LGPD · A12), `10-trafego/PLANO_PROVA_FUNIL_DUAS_ETAPAS.md` (6.1 a 6.4, seção 7), `04-mercado/MAPA_PRODUTOS.md` (5.1).

## 0. Fontes oficiais: o que foi possível ler
Tentei ler a documentação oficial (data de tentativa: 25/11/2026). **A rede do ambiente bloqueou os três domínios**; nada abaixo foi confirmado lendo a fonte neste ambiente.

| Fonte oficial | URL tentada | Resultado | Uso neste documento |
|---|---|---|---|
| Termos de Públicos Personalizados da Meta | `https://www.facebook.com/legal/terms/customaudience` | **[NC]** domínio não resolve no ambiente (25/11/2026) | Seção 2.1 descreve o que costuma constar, **de memória**, marcado [NC]; Bruno/advogado conferem o texto vigente |
| ANPD, Guia orientativo de Legítimo Interesse | `https://www.gov.br/anpd/...` (guia de legítimo interesse) | **[NC]** domínio não resolve (25/11/2026) | Seção 1.2 usa a estrutura geral do teste de balanceamento, de memória [NC] |
| Lei 13.709/2018 (LGPD) | `https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm` | **[NC]** domínio não resolve (25/11/2026) | Artigos citados de memória: arts. 5º XII, 6º, 7º, 8º, 9º, 10, 15, 16, 18 e 37. **Conferir o texto antes de usar em política ou contrato** |
| Ajuda do Gerenciador de Anúncios (públicos, correspondência, mínimo) | `https://www.facebook.com/business/help/...` | **[NC]** mesmo bloqueio | Seção 3.4 marca tamanho mínimo e passo a passo como [NC] |

Se Bruno liberar esses domínios na rede da sessão, a leitura refeita leva poucos minutos e os [NC] da seção 0 podem ser fechados.

## 1. Base legal por finalidade e por origem do contato

### 1.1 Mapa resumido [a validar por advogado]
Origens: **(O1)** lead de formulário nativo do Meta captado com a captação corrigida; **(O2)** lead que já existe na base (captado antes, com outra promessa); **(O3)** comprador.

| Finalidade | O1 lead novo | O2 lead existente | O3 comprador | Base proposta [H] | Observação |
|---|---|---|---|---|---|
| Entregar o que foi pedido (acesso, confirmação, recibo, suporte) | n/a (ainda não comprou) | n/a | **Sim** | Execução de contrato / procedimentos preliminares (LGPD art. 7º, V) | Não depende de marketing. Não pode ser usada para empurrar outra oferta |
| Responder ao que o lead pediu no formulário (mensagem de boas-vindas ao cadastro gratuito) | **Sim** | **Parcial**: só se o formulário antigo previa esse contato | n/a | Procedimentos preliminares a pedido do titular (art. 7º, V) ou consentimento (art. 7º, I) | Só o que o formulário disse. Se o formulário antigo falava em "reunião", "equipe entrará em contato", **não cobre** a oferta nova sem transição |
| Comunicação comercial por e-mail (educação + oferta) | Sim, **com consentimento separado** (recomendado) | Só após transição honesta e opção clara de sair | Só se houver consentimento ou legítimo interesse documentado (produto similar, opção de sair em todo e-mail) | Consentimento (art. 7º, I e art. 8º) **preferido**; legítimo interesse (art. 7º, IX e art. 10) só com teste documentado | Ver 1.2 |
| Comunicação comercial por WhatsApp | Sim, **somente com consentimento específico para esse canal** | **Não presumir**; pedir de novo | Idem | Consentimento específico por canal [H] | Seção 2.2 |
| Personalização de publicidade: subir lista de e-mail/telefone em público personalizado do Meta | **Só com consentimento específico** (texto da seção 4.2) | **Não usar** sem nova base (seção 2.3) | **Exclusão** de compradores: possível por legítimo interesse documentado (evitar anúncio repetido a quem já comprou), com opção de oposição; **inclusão** (lookalike) só com consentimento [H] | Consentimento específico (inclusão); legítimo interesse (exclusão de quem já comprou) | Seção 2.1 |
| Medição de anúncios (pixel, CAPI com hash) | Pode ser legítimo interesse + aviso e, quando o Meta/navegador pedir, consentimento de cookies | Idem | Idem (e execução de contrato para conciliar a venda) | Legítimo interesse (medição) com aviso [H] | Mínimo de dados; ver `09-tracking/README.md` |

### 1.2 O que cada base cobre e o que NÃO cobre [a validar por advogado; estrutura de memória, [NC] frente à fonte oficial]
**Execução de contrato e procedimentos preliminares (art. 7º, V).** Cobre: dados necessários para vender e entregar (nome, e-mail, telefone se o checkout exigir), liberar acesso, emitir recibo, dar suporte, tratar reembolso. **Não cobre:** enviar novas ofertas, subir o contato para anúncios, perfilar para lookalike, nem cruzar com outras linhas de produto.

**Consentimento (arts. 7º, I e 8º).** Livre, informado, inequívoco, para finalidade determinada; autorizações genéricas são nulas; revogável a qualquer tempo, por procedimento gratuito e facilitado. Aqui: um consentimento **por finalidade** (comunicação comercial; personalização de publicidade), **não obrigatório** para o cadastro (o cadastro gratuito não pode ser condicionado a eles), caixa **desmarcada** por padrão. Guardar registro (data/hora, texto exato mostrado, versão, origem) fora do repositório público. **Não cobre** finalidades não descritas no texto.

**Legítimo interesse (arts. 7º, IX e 10).** Só para finalidade legítima, situação concreta, dados estritamente necessários, expectativa razoável do titular e salvaguardas. Teste de balanceamento em quatro perguntas, que devem ser **registradas por escrito** (modelo abaixo). Direito de **oposição** (art. 18, § 2º) precisa ser simples e respeitado em todos os canais. **Não cobre** o que o titular não esperaria (ex.: lead de formulário que prometia "consultoria" receber anúncio com lista subida ao Meta sem aviso), nem dado sensível, nem fluxos em que o titular já disse "não quero receber".

Modelo de registro do teste de balanceamento (um por finalidade; preencher com advogado):
1. **Finalidade legítima, situação concreta:** (ex.: evitar anunciar a Mini Mentoria a quem já a comprou).
2. **Necessidade:** quais dados mínimos (e-mail com hash) e por que não há meio menos invasivo (ex.: público por visita à página de obrigado dispensa lista).
3. **Expectativa e impacto ao titular:** o que a pessoa razoavelmente espera após comprar; risco (baixo: deixa de ver anúncio).
4. **Salvaguardas:** aviso na política de privacidade, canal de oposição, prazo de atendimento, hash, exclusão da lista quando houver pedido, retenção limitada.
Resultado: [a validar por advogado]. Sem esse registro, **não usar legítimo interesse** para a finalidade.

## 2. Tratamentos específicos

### 2.1 (a) E-mails e telefones de leads em públicos personalizados do Meta
- **O que acontece tecnicamente [H, conhecimento geral, [NC] frente à fonte]:** a lista (e-mail, telefone etc.) é normalizada e convertida em hash antes do envio (a ferramenta do Gerenciador faz o hash no navegador) e o Meta tenta correspondê-la a contas dele. Hash não anonimiza para a LGPD: continua sendo dado pessoal tratado pela Zion e compartilhado com o Meta (operador/controlador conforme o caso) [a validar por advogado].
- **Termos da Meta [NC, não lidos]:** os termos de públicos personalizados costumam exigir que o anunciante tenha **direito** de usar e compartilhar esses dados, que tenha dado aviso adequado aos titulares e obtido o consentimento exigido por lei, e que a Meta possa recusar listas sem essa base. **Bruno precisa ler e aceitar o texto vigente no Gerenciador (aceite dos termos na conta) antes de subir qualquer lista.**
- **Decisão proposta:**
  - **Inclusão (anunciar para leads):** somente leads com **consentimento específico de personalização de publicidade** (texto 4.2), registrado. Sem esse consentimento, o lead **não** vai à lista. Alternativa sem lista: público de **engajamento do próprio Meta** (abriu/enviou o formulário nativo, assistiu vídeo, visitou a página), que não exige subir contato (ver 3).
  - **Exclusão (não anunciar a quem já comprou):** preferir **público por evento** (visitantes da página de obrigado) a lista; se usar lista de compradores, só com teste de balanceamento registrado (1.2), aviso na política e opção de oposição [a validar por advogado].
  - **Nunca:** subir base antiga do SDR, Land Bank antigo, Bubble, corretores/operadores ou qualquer lista sem consentimento específico para este uso; nunca subir quem pediu para sair; nunca subir dado sensível; nunca usar o público para prometer algo que o cadastro não disse.
  - **Lookalike:** só depois de origem suficiente de compradores reais e com base legal confirmada (ver `HANDOFF_CHATGPT_FASE03.md` §7.4). Não criar agora.
- **Quem executa:** Bruno ou pessoa que ele designar, direto no Gerenciador (não há ação de público por API no Windsor, seção 3.1). Arquivo exportado fica fora do Git e é apagado após o envio.

### 2.2 (b) Mensagens comerciais por WhatsApp e e-mail
**WhatsApp (modelo de marketing) [H, [NC] frente à política oficial]:**
- Mensagem iniciada pela empresa fora da janela de atendimento usa **modelo aprovado**, classificado como marketing ou utilidade; modelo de marketing exige **opt-in** do destinatário para receber mensagens da empresa nesse canal, e o WhatsApp pede que o usuário possa **sair**.
- Regra Zion: **só enviar a quem deu consentimento específico para WhatsApp** (texto 4.1 marca o canal). Telefone informado no formulário **não** é consentimento para marketing por WhatsApp. Boas-vindas ao cadastro gratuito, no máximo uma mensagem, apenas para quem marcou o canal [H].
- Todo modelo traz instrução simples de saída ("Responda SAIR"); tratar o SAIR em até 24 h (prazo interno [H]) e marcar a etiqueta de **não contatar**. Pedido de sair vale para **todos** os fluxos (e-mail e WhatsApp), salvo mensagens transacionais de uma compra.
- O modelo ativo `clube_plataforma_d0` (R$ 97, banco de áreas) **não deve ser usado** com a captação nova; o substituto proposto está em `05-funis/MM47_WHATSAPP_TEXTOS_PROPOSTOS.md` e depende de aprovação de Bruno e do Meta. Pausar o fluxo `bc86b069` até lá é decisão de Bruno.
- Frequência e volume: baixa; denúncias e bloqueios reduzem a qualidade do número [H].

**E-mail:**
- E-mail transacional (acesso, recibo): sem consentimento de marketing.
- E-mail de educação e oferta: consentimento do texto 4.1 (preferido) ou legítimo interesse documentado para compradores [a validar por advogado]. Todo e-mail: identificação do remetente, motivo do recebimento, link de descadastro de um clique, e-mail de suporte de **domínio da empresa** (hoje é e-mail pessoal: pendência de Bruno).
- Não enviar e-mail comercial a lead que **não** marcou consentimento comercial; para esses, só a mensagem de confirmação do cadastro gratuito e conteúdo diretamente pedido [H, [a validar por advogado]].

### 2.3 (c) Leads antigos captados com outra promessa
Leads de formulários antigos (R$ 270, Land Bank, diagnóstico, "reunião", "avaliação") foram captados com **finalidade e expectativa diferentes**. Ao reaproveitá-los:
1. **O que muda:** a finalidade nova (vender formação digital de R$ 47) é diferente da original; o consentimento antigo "receber contato da equipe sobre o meu projeto" **não cobre** públicos personalizados nem marketing de outra linha [a validar por advogado]. A expectativa do titular (reunião/atendimento) não existe mais: precisa de **transição honesta** (texto 4.3), sem apresentar a oferta "como se nada tivesse acontecido".
2. **Recomendação:**
   - **Não subir lista antiga em público personalizado** sem nova base (consentimento específico obtido de novo).
   - **Primeira rodada: usar só engajamento do próprio Meta** (abriu/enviou formulário nativo, vídeos, visitantes da página), que não envolve subir contato.
   - Mensagem de transição **uma única vez**, por **e-mail** (não WhatsApp, salvo quem já tiver consentimento de canal), com opção clara de sair; quem sair entra na lista de supressão. Só com "aprovado" de Bruno e revisão jurídica do texto [a validar por advogado].
   - Quem responder à transição marcando o consentimento da seção 4 passa a ser tratado como O1.
   - Excluir sempre: quem pediu para sair, leads de outras linhas sem relação (Bubble, Noite Mágica, SDR), corretores/operadores, equipe, compradores.
3. **Ordem de grandeza:** a base existente de leads de formulários é de poucas centenas de contatos e **quase não tem compras** [E, agregado no scratchpad, sem número neste arquivo]. Além de risco legal, a lista pequena e com taxa de correspondência menor que 100% tende a não atingir o tamanho mínimo útil do Meta (seção 3.4).

### 2.4 (d) Retenção, minimização e direitos do titular [a validar por advogado]
- **Minimização:** captar só nome, e-mail e, se a finalidade pedir, telefone (campo opcional quando o canal for e-mail). Nada de CPF, endereço, dado sensível ou localização do terreno no cadastro. Perguntas qualificadoras (ex.: "tem terreno?") são opcionais e não condicionam o cadastro.
- **Retenção (prazos propostos [H], advogado confirma):**
  - Lead sem compra e sem interação: eliminar ou anonimizar em até 12 meses após o último contato.
  - Quem revogou consentimento ou pediu para sair: manter só o **mínimo para a supressão** (e-mail com hash na lista "não contatar") e o registro da base legal pelo prazo de defesa.
  - Comprador: prazo necessário para obrigações fiscais, defesa em reembolso e suporte; depois eliminar ou anonimizar.
  - Listas exportadas para o Meta: apagar o arquivo local logo após o envio; remover/atualizar o público quando o titular se opuser ou ao fim da campanha.
- **Direitos (art. 18):** confirmação do tratamento, acesso, correção, anonimização/eliminação, portabilidade, informação sobre compartilhamento (com o Meta, o ClickMax, o gateway), revogação do consentimento. Canal: e-mail de suporte de domínio da empresa (pendente). Prazo interno de resposta [H]: 15 dias. Registrar pedidos e o que foi enviado ao Meta para poder responder.
- **Revogação na prática:** (i) e-mail: link de descadastro; (ii) WhatsApp: "SAIR"; (iii) publicidade personalizada: pedir por e-mail; a Zion remove o contato do público e da lista no próximo ciclo (semanal) e confirma; o titular também controla anúncios nas preferências da própria conta Meta [NC].
- **Registro das operações (art. 37)** e relatório de impacto: avaliar com advogado se cabe [NC].
- **Política de privacidade:** precisa descrever, em português simples, finalidades separadas, compartilhamento com Meta (pixel, CAPI, públicos), ClickMax, gateway, retenção e canal de direitos. Pendência M20 da `13-relatorios/MATRIZ_ALTERACOES_APROVACAO.md`. **Os textos da seção 4 só podem ir ao ar com essa política atualizada e linkada.**

## 3. Arquitetura de públicos (somente projeto; nada criado)

### 3.1 O que o Windsor/Meta permite por API e o que depende do Gerenciador
Verificado em 25/11/2026 com `list_actions` do conector `facebook` [E]: existem ações de campanha, conjunto e anúncio (criar, pausar, ativar, arquivar, apagar, orçamento), `create_lead_form`, `set_lead_form_status`, `search_targeting`, `search_locations`, `duplicate_adset`, `update_adset` (aceita `targeting` e `extra_params`), upload de imagem/vídeo. **Não existe nenhuma ação de público personalizado** (criar, subir lista, público de engajamento, lookalike, listar ou excluir públicos) [E].

| Item | Pelo Windsor | Só pelo Gerenciador / Bruno |
|---|---|---|
| Criar o formulário nativo com política de privacidade e texto | `create_lead_form` (sem edição depois; para mudar, cria outro e arquiva o antigo) [E]. **Atenção:** o schema aceita `questions`, `privacy_policy_url`, `context_card`; **não** mostra campo para caixa de consentimento própria: confirmar [NC] se a "pergunta de consentimento" é possível via pergunta CUSTOM de múltipla escolha | Revisão visual do formulário no Gerenciador |
| Aplicar público de exclusão/inclusão **já existente** no conjunto | `update_adset` ou `create_adset` com `targeting.custom_audiences` / `excluded_custom_audiences` **[H]**: o parâmetro `targeting` é um objeto livre da Graph API, mas o `list_actions` não documenta esses campos. **Teste com campanha pausada e leitura posterior; não afirmar que funciona antes de testar** [NC]. Não há como obter o **id** de um público pelo Windsor (sem ação de listar públicos); Bruno copia o id no Gerenciador | Aplicar manualmente no conjunto |
| Criar público personalizado (lista de clientes, engajamento, visitantes do site, vídeo, lookalike) | **Não** | **Sim** |
| Aceitar os termos de públicos personalizados da conta | **Não** | **Sim** (Bruno) |
| Ver tamanho estimado do público, sobreposição entre públicos | **Não** (leitura de entrega por anúncio existe em `get_data`; tamanho de público não) [H] | **Sim** (Gerenciador de Públicos, ferramenta de sobreposição) |
| Verificar que a exclusão foi aplicada | Leitura do `targeting` do conjunto via `get_data`, se o campo estiver exposto [NC] | Conferir em "Editar conjunto > Público > Excluir" e no preview |

Conclusão: **públicos e exclusões são criados e conferidos por Bruno (ou quem ele designar) no Gerenciador de Anúncios**; o ChatGPT/executor só poderá anexá-los ao conjunto depois que o id existir e se o teste de `targeting` por API funcionar. Fica como tutorial.

### 3.2 Públicos (desenho)
**Quente (campanha de venda quente)** [inclusão]
- Q-a. **Engajamento do formulário nativo do Meta**: abriu e não enviou; enviou (ex.: últimos 90 dias). Não exige lista. [Gerenciador]
- Q-b. **Visitantes de `/mini-mentoria`** (e das v2 quando publicadas), 30 dias, via pixel. [H: o pixel do ClickMax roda no iframe do checkout e o ViewContent está desligado; **conferir se o pixel registra a visita à página** antes de contar com esse público] [NC]
- Q-c. **Engajamento de vídeo** 50% ou ThruPlay dos Vídeos 01 e 02, 30 dias. [Gerenciador]
- Q-d. **Leads elegíveis por lista** (só com consentimento de personalização, texto 4.2). Primeira rodada: **não usar** (poucos elegíveis e risco legal, seção 2.3).

**Exclusões (valem para quente e fria)**
- X1. **Compradores** da Mini Mentoria, do legado R$ 97 e de qualquer oferta da turma. Preferir **visitantes da página de obrigado** (evento); complementar com lista de compradores só com teste de balanceamento registrado.
- X2. **Equipe e testes** (lista pequena de e-mails internos, fora do Git).
- X3. **Grupo de controle (holdout)** do plano de prova (`PLANO_PROVA_FUNIL_DUAS_ETAPAS.md` 3.5): contatos sorteados que **não** recebem a campanha quente. Se o holdout for por lista, exige a mesma base legal; **sem lista elegível, não há holdout por lista**, e a leitura causal da quente fica limitada [H].
- X4. **Quem pediu para sair** de comunicação ou de publicidade (lista de supressão).
- X5. **Leads de outras linhas** (Bubble, Noite Mágica, SDR, corretores/operadores): só excluíveis por lista; **só subir se houver base** para essa finalidade de exclusão; caso contrário, aceitar a sobreposição e registrar [a validar por advogado].

**Frio (campanha de venda fria)**
- Brasil amplo, adultos; sem público personalizado de inclusão. Exclui X1 a X5, e **também os públicos de inclusão do quente** (Q-a a Q-c) para sobreposição zero. A exclusão de **todos os leads por lista** depende da base legal (mesmo teste de 2.1); sem ela, excluir só por **engajamento do Meta** e aceitar que um lead antigo possa ver o anúncio frio, registrando o limite [H].

**Captação (campanha de formulário)**
- Frio/aberto, Brasil, sem lista. Exclui compradores (X1) e equipe.

### 3.3 Passo a passo curto (Gerenciador de Anúncios) [NC frente à ajuda oficial; interface pode mudar]
Responsável: Bruno. Fazer com campanhas **pausadas**.
1. Gerenciador de Anúncios > **Públicos** > aceitar os termos de públicos personalizados da conta (ler o texto).
2. **Criar público > Personalizado > Engajamento > Formulário de cadastro**: escolher o formulário, "abriu, mas não enviou" e "enviou"; período 90 dias; nomear `Q-a-form-abriu` e `Q-a-form-enviou`.
3. **Criar público > Personalizado > Site** (pixel `903918118859018`): URL contém `/mini-mentoria`, 30 dias; nomear `Q-b-visita-MM`. Outro com URL contém `/obrigado-mini-mentoria` (e a antiga `/obrigado-plataforma`), 180 dias; nomear `X1-compradores-obrigado`.
4. **Criar público > Personalizado > Engajamento > Vídeo**: Vídeos 01 e 02, 50% assistido ou ThruPlay, 30 dias; nomear `Q-c-video`.
5. **Compradores por lista** (opcional, só após teste de balanceamento): **Lista de clientes**, arquivo exportado do ClickMax, mapear e-mail e telefone, aceitar o hash feito pelo Meta; **apagar o arquivo**; nomear `X1-compradores-lista`.
6. Em cada conjunto: **Público > Públicos personalizados > Incluir / Excluir** conforme 3.2. Desligar "Advantage+ audience" na fase de teste (controle de variável) [H].
7. **Ferramenta de sobreposição** (Públicos > selecionar dois ou mais > Ações > Mostrar sobreposição): conferir quente × frio.

### 3.4 Limites e riscos
- **Tamanho mínimo [NC, não lido na ajuda oficial]:** o Meta exige um número mínimo de pessoas **correspondidas** para um público entregar (de memória, na casa de uma centena), e públicos pequenos entregam mal, cansam rápido (frequência) e o custo sobe. Públicos de engajamento recém-criados nascem pequenos e só se acumulam **a partir da criação** (não retroagem além do que o Meta já registrou para a página/pixel). Se o aviso de "público pequeno" aparecer, **não completar com frio** (contamina a comparação); usar o orçamento no conjunto frio ou esperar (`PLANO_PROVA` 6.2).
- **Correspondência de lista:** nunca é 100% (e-mail diferente da conta Meta); contar com perda grande [H].
- **Sobreposição e canibalização:** quente e fria no mesmo leilão competem; usar exclusões mútuas, criativos diferentes e conferir a cada 3 a 4 dias.
- **Dados do pixel:** o domínio do checkout é bloqueado no ambiente; Q-b e X1 por evento dependem de a página de obrigado estar publicada e de o checkout redirecionar para ela [BRUNO].
- **Políticas de anúncio:** não usar atributo pessoal ("você tem terreno parado") como afirmação sobre a pessoa; manter promessa "Aprenda o passo a passo para..." [E, CLAUDE.md].

### 3.5 Checklist para confirmar que as exclusões foram aplicadas
Fazer antes de ativar e a cada 3 a 4 dias. Marcar com data e quem conferiu (sem contagem de pessoas que identifique alguém).
- [ ] Termos de públicos personalizados aceitos na conta (Bruno).
- [ ] Todos os públicos de 3.3 existem, com nome padronizado e data de criação anotada.
- [ ] Cada conjunto de **venda quente** abre em "Editar > Público" com `X1`, `X2`, `X3` (se houver) e `X4` em **Excluir**.
- [ ] Cada conjunto de **venda fria** abre com `X1` a `X5` e com `Q-a`, `Q-b`, `Q-c` em **Excluir**.
- [ ] O conjunto de **captação** exclui `X1` e `X2`.
- [ ] Ferramenta de sobreposição: quente × frio **zero ou próximo de zero**; registrar o resultado.
- [ ] Tamanho estimado dos públicos acima do aviso "público pequeno" (senão decidir pela regra de 3.4).
- [ ] Pré-visualização e entrega: nenhum anúncio de venda fria entregue a pessoa da lista de compradores (teste com a conta de Bruno, que é comprador de teste, **em ambiente que ele controle**; não usar dado de terceiros).
- [ ] Se aplicado por API: leitura do `targeting` do conjunto confirma `custom_audiences` e `excluded_custom_audiences` com os ids certos [NC se o campo não estiver exposto].
- [ ] Lista de supressão atualizada na data; ninguém que pediu para sair ficou em público de inclusão.
- [ ] Registro no `LOG` e no relatório semanal: data da última atualização de cada público.

## 4. Textos de consentimento (separados, não obrigatórios, opt-in desmarcado) [a validar por advogado]
Regras para todos: cada consentimento tem **caixa própria, desmarcada por padrão**; o **cadastro gratuito funciona sem marcar nenhuma**; link para a política de privacidade (`{URL_POLITICA_PRIVACIDADE}`, pendência M20); explica como revogar; sem urgência, sem promessa, sem "ao enviar você concorda com tudo". Alinhar o enunciado de tela com `06-criativos/CAPTACAO_CORRIGIDA.md` (CREATIVE, em elaboração em paralelo; **no momento da escrita ele ainda não existia no repositório**, então este arquivo traz só os blocos de consentimento e o CREATIVE traz a tela). Conferir os dois antes de publicar o formulário.

Observação sobre o formulário nativo do Meta [H, [NC]]: o limite de texto do formulário é curto e a política de privacidade é um link obrigatório; um item de consentimento pode ser uma pergunta de múltipla escolha opcional (CUSTOM) ou uma caixa de consentimento própria do Gerenciador. Testar no Gerenciador qual formato o Meta permite e se a pergunta pode ser **não obrigatória**. Se não for possível ter consentimento opcional no formulário nativo, **coletar os consentimentos na página de agradecimento ou no primeiro e-mail**, e tratar o lead só como cadastro gratuito até lá.

### 4.1 Consentimento (i) · Comunicação comercial por WhatsApp e e-mail
**Versão curta (formulário nativo do Meta):**
> ☐ Quero receber novidades e ofertas da Zion por e-mail e WhatsApp. (Opcional. Você pode sair quando quiser.)
> Política de privacidade: {URL_POLITICA_PRIVACIDADE}

Se a caixa permitir só uma linha, usar:
> ☐ Aceito receber mensagens comerciais da Zion por e-mail e WhatsApp. Opcional.

Se houver espaço para separar canais (preferível, pois consentimento é por canal):
> ☐ Quero receber ofertas e conteúdo da Zion por **e-mail**. (opcional)
> ☐ Quero receber ofertas e conteúdo da Zion por **WhatsApp**. (opcional)

**Versão longa (página):**
> **Mensagens e ofertas da Zion (opcional)**
> ☐ Quero receber da Zion, por **e-mail**, conteúdo sobre estruturação de empreendimentos de hospedagem e ofertas dos nossos produtos pagos, como a Mini Mentoria de Estruturação Zion.
> ☐ Quero receber as mesmas mensagens por **WhatsApp**, no número que informei.
> Marcar é opcional e **não é necessário para fazer o cadastro gratuito**. Usaremos seu nome, e-mail e telefone só para enviar essas mensagens. Você pode parar quando quiser: em todo e-mail há um link para sair e, no WhatsApp, basta responder SAIR. Também pode pedir por {EMAIL_SUPORTE_DOMINIO_ZION}. Saiba mais na [Política de Privacidade]({URL_POLITICA_PRIVACIDADE}).

### 4.2 Consentimento (ii) · Personalização de publicidade
**Versão curta (formulário nativo do Meta):**
> ☐ Autorizo a Zion a usar meu e-mail e telefone para me mostrar anúncios no Facebook e Instagram, por meio de plataformas de anúncio. (Opcional.)
> Política de privacidade: {URL_POLITICA_PRIVACIDADE}

**Versão longa (página):**
> **Anúncios mais relevantes (opcional)**
> ☐ Autorizo a Zion a usar meu e-mail e meu telefone, **em formato protegido (hash)**, para criar públicos de anúncio no Meta (Facebook e Instagram), tanto para **mostrar** anúncios da Zion a mim quanto para **não** mostrar anúncios de um produto que eu já comprei.
> Isso é opcional e **não é necessário para o cadastro gratuito**. Esse uso envolve compartilhar dados protegidos com o Meta, que também trata os dados conforme os termos dele. Você pode retirar a autorização quando quiser, pedindo por {EMAIL_SUPORTE_DOMINIO_ZION}; removeremos você dos públicos no próximo ciclo de atualização (até 7 dias [H]). Saiba mais na [Política de Privacidade]({URL_POLITICA_PRIVACIDADE}).

Nota: a **exclusão** de quem já comprou pode ter base própria (legítimo interesse, 2.1), mas o texto acima já a menciona para transparência; advogado decide se mantém junto ou separa.

### 4.3 Texto de transição para leads existentes (honesto) · e-mail, uma vez, só com "aprovado" de Bruno e revisão jurídica
Não promete reunião, parceria ou investimento. Não é anúncio nem lista subida ao Meta.
> **Assunto:** O que mudou na Zion (e como sair, se preferir)
>
> Olá, {{nome}}.
> Há um tempo você deixou seus dados em um formulário da Zion. Queremos ser claros sobre o que fazemos hoje.
> A Zion oferece a **Mini Mentoria de Estruturação Zion**: uma formação digital, **sem reunião e sem atendimento individual**. Por **R$ 47**, em pagamento único, você tem acesso à plataforma digital com 9 módulos com 70 aulas e materiais para aprender o passo a passo de estruturar o seu projeto. Parcerias e investimentos não fazem parte da compra.
> Você **não precisa fazer nada**. Se quiser saber mais, esta é a página com preço e conteúdo: {URL_MINI_MENTORIA}.
> Se preferir **não receber mais mensagens da Zion**, [clique aqui para sair]({LINK_DESCADASTRO}) ou responda este e-mail com SAIR. Seus dados seguem a nossa [Política de Privacidade]({URL_POLITICA_PRIVACIDADE}).
> Se quiser receber conteúdo e ofertas por e-mail daqui para frente, pode [confirmar aqui]({LINK_CONSENTIMENTO_EMAIL}).

Condições: enviar só a quem **não** pediu para sair e **não** é comprador; sem pixel de rastreio abusivo; registrar envio e saídas; não repetir. Para leads com histórico de outra linha (Bubble, SDR), **não enviar** (finalidade diferente) [a validar por advogado].

### 4.4 Rodapé de preço e condições da Mini Mentoria (página de venda, anúncio de venda e e-mail de oferta)
Todos os fatos já estabelecidos e verificados (`08-checkouts/ENTREGAVEIS_VERIFICADOS.md`); conferir antes de publicar.
> **Mini Mentoria de Estruturação Zion** · formação digital autônoma.
> **R$ 47**, pagamento único, **sem mensalidade**. Pix ou cartão de crédito à vista.
> Acesso à plataforma digital: 9 módulos, com 70 aulas e materiais: aulas gravadas, fichas "Faça agora", e-books por pilar, 2 planilhas de cálculo em branco, Kit do Investidor (modelos), kit de prompts e Dossiê com PDF.
> **Garantia de 7 dias**: se não for para você, peça o reembolso em até 7 dias após a compra.
> Não inclui reunião, atendimento individual, consultoria, investimento, parceria nem rede de investidores. Não promete reservas, ocupação, renda, aprovação de projeto ou captação de recurso. Resultados dependem da aplicação e de fatores externos.
> O cadastro gratuito não é necessário para comprar. Seus dados são tratados conforme a [Política de Privacidade]({URL_POLITICA_PRIVACIDADE}).

(Rodapé de **captação**, uma linha, para a arte e a tela do formulário, a alinhar com o CREATIVE: "Cadastro gratuito. Existem formações pagas, como a Mini Mentoria de R$ 47, que você só compra se quiser.")

## 5. Mercado: os públicos certos? (reavaliação curta, sem repetir `04-mercado`)
Base: `04-mercado/MAPA_PRODUTOS.md` §1 e §5.1 e agregados dos leads (sem nomes, no scratchpad). Amostra de formulário **pequena (menos de 20 respostas completas)**: direcional [H], nunca conclusão. **Nenhum número de mercado** foi usado [NC].

**Leitura:**
- O alvo definido (dono de terreno que quer estruturar o primeiro empreendimento) **bate com os leads reais**: a dor mais repetida é "tenho terra, falta capital", a maioria diz ter terreno regularizado, horizonte "3 a 6 meses" [E, amostra pequena]. Ou seja, a captação e as duas vendas **miram o público certo em intenção**.
- **Riscos de público** [H]: (1) o conjunto antigo de venda usou comportamentos genéricos de aparelho e viagem internacional e interesse em espanhol, que **não** identificam dono de terreno; (2) a base existente mistura donos de terreno com **operadores/corretores** da base antiga: no quente, isso dilui; (3) o nome "capital/investidor" atrai **curiosos de investimento** que não têm terreno; (4) anfitriões de Airbnb estão **sem amostra** [NC] e não são o alvo desta oferta.
- **Quente e fria miram a mesma pessoa em estágios diferentes**, o que é coerente, desde que a quente seja realmente quente (engajou) e a fria não seja o mesmo público.

**Ajustes recomendados (lista curta, [H] a validar por teste, uma variável por vez):**
1. **Geografia:** Brasil inteiro na primeira rodada (a oferta é digital). Em segunda rodada, testar **estados/regiões** com apelo de turismo de natureza (Sul e Sudeste serranos, litoral) via `search_locations`, mas só por evidência de onde os leads reais estão (agregar por estado no ClickMax, sem nomes) [NC: não lido nos formulários]. Evitar raio por cidade (não se sabe onde está o terreno).
2. **Idade:** manter 30 a 65+ como aposta, não 25 a 65+: dono de terreno e quem busca capital costuma estar na faixa adulta [H, sem dado]. **Medir a idade dos leads e dos compradores** (relatório por faixa do Gerenciador) após a primeira semana e ajustar; não restringir antes de ter dado.
3. **Interesses (testar disponibilidade no seletor, `search_targeting`):** imóveis e terrenos, empreendedorismo, ecoturismo/turismo rural, hospedagem alternativa, construção civil/arquitetura rural. **Retirar** comportamentos de aparelho, viagem internacional e interesse em espanhol. Separar em conjuntos **interesse × aberto** só se o orçamento permitir; no teto proposto, **um** conjunto frio por vez [H].
4. **Qualificação na captação:** pergunta **opcional** "Você tem terreno ou imóvel?" no formulário reduz curiosos sem condicionar o cadastro; ler a distribuição, não filtrar [H]. Evitar pergunta sobre renda ou reserva (dado sensível econômico, atrito, risco de promessa implícita).
5. **Não segmentar** por situação financeira, dívida, endividamento ou atributo pessoal (políticas do Meta; categoria financeira) [H, [NC]].
6. **Excluir** operadores/corretores da lista quente (X5) quando houver base legal para a lista de exclusão.
7. **Não ampliar** para Airbnb comum nesta oferta; a escada R$ 19 e o Arsenal têm outro público (`MAPA_PRODUTOS.md` §6).

## 6. O que depende de aprovação (quem executa, onde, reversão)
| # | Ação | Quem | Onde | Reversão |
|---|---|---|---|---|
| L1 | Validar este documento e os textos da seção 4 com **advogado** | Bruno | Fora do sistema | n/a |
| L2 | Atualizar e publicar a **política de privacidade** (finalidades separadas, Meta, ClickMax, gateway, retenção, canal de direitos) e definir **e-mail de suporte de domínio da empresa** | Bruno + advogado | Site/ClickMax (M20) | Reverter o texto |
| L3 | Incluir os consentimentos 4.1 e 4.2 no formulário nativo (criar **novo** formulário; o Meta não edita) e conferir no Gerenciador se podem ser opcionais | Bruno ou ChatGPT com "aprovado" | Meta (formulário) | Arquivar o formulário (`set_lead_form_status`) |
| L4 | Aceitar os termos de públicos personalizados e criar os públicos de 3.3 | Bruno | Gerenciador de Anúncios | Excluir o público |
| L5 | Subir **qualquer lista** de contatos (leads ou compradores) | Bruno | Gerenciador | Excluir o público e apagar o arquivo local |
| L6 | Enviar o e-mail de transição (4.3) | Bruno, com revisão jurídica | ClickMax/Brevo | Não há desfazer envio; por isso revisão antes |
| L7 | Submeter modelos de WhatsApp de marketing e disparar | Bruno | Gupshup/Meta | Pausar modelo ou fluxo |
| L8 | Aplicar exclusões nos conjuntos (manual ou por `update_adset` após teste) | Bruno ou ChatGPT com "aprovado" | Meta | Remover a exclusão |
| L9 | Instalar `persistir-utm.js` | Bruno | ClickMax | Remover o script; só depois de L2 |

## 7. Pendências e [NC]
- **[NC]** Termos de públicos personalizados da Meta, guia de legítimo interesse da ANPD, texto da LGPD e ajuda do Gerenciador: **não lidos** (rede bloqueou `facebook.com`, `gov.br` e `planalto.gov.br`, 25/11/2026). Liberar os domínios na sessão fecha estes itens.
- **[NC]** Se o formulário nativo do Meta aceita consentimento opcional e separado (via `create_lead_form` ou Gerenciador).
- **[NC]** Se `update_adset`/`create_adset` aceitam `custom_audiences` e `excluded_custom_audiences` no `targeting` pelo Windsor (testar com conjunto pausado e leitura posterior).
- **[NC]** Tamanho mínimo de público e taxa de correspondência na conta de Bruno.
- **[NC]** Se o pixel registra a visita a `/mini-mentoria` fora do iframe.
- **[NC]** Distribuição de idade e estado dos leads e compradores (não lida; depende do relatório do Gerenciador e do ClickMax).
- **[NC]** `06-criativos/CAPTACAO_CORRIGIDA.md` ainda não existia ao fechar este arquivo: alinhar a tela do formulário com os blocos 4.1, 4.2 e o rodapé de captação.
