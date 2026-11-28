# Auditoria da plataforma ClickMax (somente leitura)

Data da leitura: 28/11/2026. Workspace `e87e8ba9-37cf-4c54-9a97-3e4e1b01827a` (Bruno's Workspace).
Só foram usadas ferramentas de leitura (get, list, overview). Nada foi criado, editado, apagado, ativado ou enviado. Nenhum dado pessoal de lead foi impresso.
Regra deste relatório: só consta o que foi lido nas ferramentas. O que não foi achado está como "não comprovado".

## 0. Conta de vendedor (contexto)

| Item | Leitura |
|---|---|
| `sellerStatus` | `pending` (em análise) |
| `bankAccountStatus` | `approved`, sem motivo de recusa |
| `canSell` / `canAffiliate` | true / true |
| Gateway | ticto |

Ponto de atenção: o vendedor segue `pending`. O `CLAUDE.md` diz que, com vendedor pendente, nenhum checkout vende. Esta auditoria não fez compra de teste, então venda real **não comprovada**.

## 1. Oferta R$ 47 `668391e7-f4a8-4bd3-a212-deba406f8a7a`

| Item | Condição real lida |
|---|---|
| Nome da oferta | Zion Collection Club \| Acesso à plataforma (R$ 47) |
| Produto | `072083e8-88c6-46bd-9e6c-5b851b6ac1c4` · "Zion Collection Club \| Acesso à plataforma" (internal, tipo curso) |
| Preço | R$ 47,00 (`originalPrice` 4700, BRL). `newPrice` vazio, sem preço "de" |
| Tipo de pagamento | Único. `isRecurrent` false, `recurrence` null |
| Meios | Pix ativo; cartão ativo em 1x (`installments` 1); boleto desligado |
| Prazo de acesso (texto da descrição) | "liberado após a confirmação do pagamento e ativo por 12 meses a partir da liberação" |
| Reembolso | `limitToRefund` 7 dias; descrição diz "Reembolso em 7 dias" |
| Status | `approved`; `incompleteReason` vazio; `providerSyncError` vazio |
| Soft descriptor / telefone / e-mail de suporte | ZIONACADEMY / +55 48 6137-1061 / e-mail da conta (campo `supportEmail` preenchido; não reproduzido aqui) |
| Checkout | hash `z3a0AEkvRl`, checkout interno, sem timer, sem cupom |
| Banner/imagem | `thumbnail` é o placeholder do ClickMax; sem banner desktop/mobile; sem imagens de checkout (não comprovado que a capa do produto foi aplicada) |
| Entregáveis | 2, ambos `internal_membership` (área de membros) |
| Portal/turma 1 | portal `a8e2157a…` (Zion Collection), turma `69345987-7679-41e5-8e66-27281afa6892` |
| Portal/turma 2 | portal `3ef7a340…` (Plataforma Zion Collection), turma `087479a3-9d6f-4e1f-a542-c47b347bf5ed` |
| Coprodução / afiliados | sem coprodução; `allowAffiliateResale` true |

O que a descrição promete: acesso individual à plataforma; Marco Zero; sete pilares; aulas interativas e vídeos; fichas e ferramentas; planilhas de orçamento e viabilidade; Dossiê de Desenvolvimento para baixar em PDF; etapa opcional de solicitação da Sessão de Diagnóstico Estratégico (gratuita, só para projetos qualificados, sujeita a análise e agenda). Diz que não há atendimento individual contínuo e que parceria e investimento não são garantidos.

Divergência a observar: o id de turma que veio no pedido (`69345987-7679-41e1-…`) não existe. O id real, ligado à oferta, termina em `41e5-8e66-27281afa6892`. Usei o real.

Outra observação: esta é a oferta Club R$ 47. A Mini Mentoria `0c71eeba…` citada no `CLAUDE.md` é outra oferta e não foi lida nesta auditoria.

## 2. Portais da plataforma

### 2.1 Os dois portais

| Item | Portal `3ef7a340…` | Portal `a8e2157a…` |
|---|---|---|
| Nome | Plataforma Zion Collection | Zion Collection |
| Endereço | subdomínio `zion-plataforma` | subdomínio `zion-collection` |
| Publicado | sim (24/11/2026) | sim (11/11/2026) |
| Turma lida | "Plataforma de estruturação (R$ 97)" `087479a3…` | "Zion Collection Club · Plataforma (R$ 97)" `69345987…41e5…` |
| Cursos ligados | 1 (`79d3e792-7526-4d88-926e-60e401748f3e`, nome vazio) | o mesmo curso `79d3e792…` |
| Tema | Dark, destaque dourado `#C9B37E` | Dark, destaque dourado `#C9B37E` |
| Login | primeiro acesso sem senha: sim; senha simples: sim; 2FA: não; OTP WhatsApp: não | igual |
| Suporte do portal | WhatsApp `wa.me/554861371061` | igual |

Achado: as duas turmas usam o **mesmo curso** (`79d3e792…`), com os mesmos 9 módulos e 75 aulas. O conteúdo é idêntico nos dois portais. Os nomes das turmas ainda dizem "R$ 97", embora a oferta lida seja de R$ 47.

Área tipo "Meu Projeto": **não existe** como módulo ou aula nos dois portais. O mais próximo são as aulas "Faça agora" e o "Monte o seu dossiê inicial" (ver tabela abaixo). `navConfig` está nulo nos dois portais (sem menu personalizado) e `suggestedContentEnabled` está desligado.

### 2.2 Módulos e aulas (iguais nos dois portais)

Todas as 75 aulas estão `enabled: true`. Tipos: vídeo, documento (PDF/XLSX) e link externo. Nenhuma aula do tipo texto. Nenhuma aula tem corpo de texto (`content` vazio).

| Módulo | Aulas | O que tem (nome resumido · tipo) |
|---|---|---|
| 1 Comece aqui · Onboarding | 4 | Boas-vindas (vídeo mp4 no GitHub Pages); questionário "Conte para a Zion sobre você e a sua área" (link, formulário ClickMax `f4522f48…`); "Monte o seu dossiê inicial" (link `/dossie/`); Suporte (link do chat `54c75883…`) |
| 2 Marco Zero | 11 | PDF "Comece aqui"; mapa de direcionamento (link); tutorial em vídeo; aula interativa (link); vídeos 1 e 2 (YouTube); "Faça agora · diagnóstico prévio" (link); e-book PDF; tutorial da ficha; kit de prompts do Dossiê (link); "Ficha do seu terreno: dados, fotos e documentos" (link Airtable) |
| 3 Pilar 1 Território | 8 | aula interativa; vídeos 3 e 4; "Faça agora · Ficha do Território"; e-book PDF; aprofundamento (e-book e 40 slides, links); tutorial |
| 4 Pilar 2 Mercado | 8 | mesma estrutura (vídeos 5 e 6) |
| 5 Pilar 3 Produto | 8 | mesma estrutura (vídeos 7 e 8) |
| 6 Pilar 4 Modelo de negócio | 9 | mesma estrutura (vídeos 9, 10 e extra) |
| 7 Pilar 5 Masterplan | 8 | mesma estrutura (vídeos 11 e 12) |
| 8 Pilar 6 Pré-viabilidade | 10 | aula interativa; vídeos 13 e 14; "Faça agora"; tutoriais; e-book; Planilha 1 Orçamento de Abertura (XLSX); planilha de pré-viabilidade (XLSX) |
| 9 Pilar 7 Capital e Dossiê | 9 | aula interativa; vídeos 15 e 16; "Faça agora · Dossiê"; tutorial; e-book; Kit do Investidor (link); tutorial; "Cadastre o seu terreno no banco de áreas da Zion" (link Airtable) |

Observações sobre os links: quase tudo está hospedado em `bchaerk-creator.github.io/zion-hotel-ai-developer/...` (repositório visível no GitHub), vídeos em YouTube (`youtu.be`), e dois formulários em Airtable (`appNazhHg9mqWAt9h`, páginas `pagyB6989L0Vs4dYs` e `pageylHbg89JNYm81`). Os links não foram abertos nesta auditoria.

### 2.3 Tabela de recursos

| Recurso | Descrição | Benefício para o cliente | Onde fica | Funciona (comprovado?) | Pendência |
|---|---|---|---|---|---|
| Vídeo de boas-vindas | mp4 de apresentação da plataforma | Entende como usar | Módulo 1, aula 1 | Aula ativa e com URL. Reprodução não testada | Testar o mp4 no portal |
| Questionário "Conte para a Zion…" | Formulário ClickMax `f4522f48…`, 16 campos | Zion conhece a área; cliente é cadastrado | Módulo 1, aula 2 (link externo) | Formulário `active`; **0 respostas** registradas. Não comprovado de ponta a ponta | Fazer um envio de teste e conferir tags e etapa |
| "Monte o seu dossiê inicial" | App web estático (`/dossie/`) | Constrói o Dossiê e baixa em PDF | Módulo 1, aula 3 | Link cadastrado; app não aberto aqui | Testar; confirmar onde o cliente guarda os dados (provável salvamento local no navegador: não comprovado) |
| Chat de suporte | Webchat "Suporte · Clube Zion Land" `5f3517c3…` | Tirar dúvidas | Módulo 1, aula 4 | Canal `live`. Atendimento humano não comprovado | Definir quem responde e horário |
| Marco Zero (vídeos, e-book, aula interativa, diagnóstico) | 11 aulas | Ponto de partida e diagnóstico prévio | Módulo 2 | Aulas ativas; reprodução não testada | Testar links |
| Fichas "Faça agora" (Pilares 1 a 7) | Páginas estáticas em `/trilha1/...` | Preenche a ficha de cada pilar | Primeira ou quarta aula de cada pilar | Links cadastrados; não abertos | Testar; confirmar como o resultado vira o Dossiê |
| Ficha do terreno (dados, fotos, documentos) | Formulário Airtable | Único recurso lido que aceita anexo, segundo o título da aula | Módulo 2, aula 11 | Aula ativa. O formulário Airtable não foi lido | Conferir campos e destino no Airtable; ver nota sobre documentos na seção 3 |
| E-books em PDF (Marco Zero e Pilares 1 a 7) | PDFs no GitHub Pages | Leitura e consulta | Módulos 2 a 9 | Links cadastrados; não abertos | Testar |
| Aprofundamentos (e-book e 40 slides, Pilares 1 a 5) | Links em `/escola/d01..d05/` | Estudo mais fundo | Módulos 3 a 7 | Links cadastrados; não abertos | Testar |
| Planilhas de orçamento e viabilidade | 2 XLSX em branco | Faz a conta do próprio caso | Módulo 8 | Links cadastrados; não abertos | Testar download |
| Kit de prompts do Dossiê | Página em `p/adbc…/kit-prompts-dossie/` | Usa ChatGPT ou Claude com as fichas | Módulo 2, aula 10 | Link cadastrado | Testar |
| Kit do Investidor | Página com teaser, one-pager, pitch etc. | Material para apresentar o projeto | Módulo 9, aula 7 | Link cadastrado | Testar; revisar promessas |
| Cadastro no banco de áreas | Formulário Airtable | Zion conhece e avalia o terreno | Módulo 9, aula 9 | Aula ativa | Conferir destino das respostas e LGPD |
| Tutoriais em vídeo | mp4 por ficha e planilha | Passo a passo | Vários módulos | Links cadastrados; não testados | Testar |
| Área "Meu Projeto" | Não existe | n/d | n/d | **Não comprovado / inexistente** | Decidir se será criada |
| Progresso, certificado, comentários | Portal tem comentários ligados (limite 50 por dia, sem publicação automática) | Interação e acompanhamento | Portal | Configuração lida; uso não comprovado | n/d |

## 3. Formulários do ClickMax ligados à plataforma

Nenhum dos três formulários tem campo de arquivo, foto ou anexo. Os tipos de campo lidos são só e-mail, telefone, seleção, texto e texto longo. Em toda a lista de 24 formulários, também não apareceu campo do tipo arquivo (tipos vistos: email, phone, select, text, textarea, multi, switch). Anexo de foto ou documento, portanto, **só existe fora do ClickMax** (formulário Airtable da ficha do terreno, não lido).

| Formulário | Campos | Texto aberto | Anexo | Para onde vão as respostas |
|---|---|---|---|---|
| `75ee0a3a…` Ficha do inscrito (pós-compra R$ 97) · ativo · 1 resposta | 10: e-mail (obrigatório); perfil, área, objetivo, infraestrutura, documentação, valor da área, impedimento, apresentação a investidor (todos seleção, opcionais); localização (texto) | 1 campo: localização (só cidade e estado) | Não | Cria ou mescla o lead por e-mail. E-mail vai para o campo do lead; os demais vão para campos personalizados (`perfil_area`, `localizacao`, `area`, `objetivo_projeto_meta`, `infraestrutura_meta`, `documentacao_meta`, `valor_area_meta`, `impedimento_meta`, `apresentacao_investidor_meta`). Origem `ficha-inscrito-plataforma`. Sem tag aplicada e sem pipeline. `triggerAutomation` desligado. Final: botão "Entrar na plataforma" para `zion-plataforma.clickmax.space` |
| `f4522f48…` ZC47 Conheça você e a sua área · ativo · 0 respostas | 16: nome, e-mail, WhatsApp (obrigatórios); cidade/UF; perfil; Instagram; área; documentação; titular; infraestrutura que tem; o que falta; projeto; dificuldade; o que deseja; o que espera; formação; parceria | 6 campos de texto livre: cidade/UF, Instagram, área, infraestrutura que tem, o que falta, o que deseja, o que espera (3 deles em texto longo) | Não. O texto do formulário diz "Não envie documentos nesta etapa" | Nome, e-mail e telefone para o lead; os demais para campos personalizados `zc_*` (cidade_uf, perfil, instagram, area, documentacao, titular, infra_tem, infra_falta, projeto, dificuldade, deseja, espera, formacao, parceria). Aplica 1 tag (`1453313b…`). Cria card no pipeline "Inscritos · Plataforma Zion Collection", etapa "2 · Ficha preenchida". LGPD obrigatório. `triggerAutomation` ligado; push no navegador ligado |
| `7495df8b…` Ficha de adesão ao Club (Jornada) · ativo · 11 respostas | 5: nome, e-mail, WhatsApp (obrigatórios); localização; perfil | 2: nome e localização | Não | Lead + campos `localizacao` e `perfil_area`. Aplica 1 tag (`d200f176…`). Cria card no pipeline "Club Zion Collection · Adesão → Pagamento → Membro", etapa 1. Depois redireciona para um link de pagamento do Asaas (`redirectUrl`). LGPD obrigatório |

Pontos de atenção:
- O mapeamento do telefone do formulário `7495df8b…` usa o alvo `telephone`, enquanto o `f4522f48…` usa `phone`. Qual está certo não foi verificado.
- A ficha `75ee0a3a…` serve ao formato de R$ 97 (texto do próprio formulário). Se ela continua ligada ao fluxo de R$ 47, não foi comprovado.
- Existe também o formulário `aff270f4…` "MM47 · Solicitação da Sessão de Diagnóstico Estratégico" (ativo, 0 respostas, campos incluem texto longo e switch). Não foi lido em detalhe.
- Total de formulários: 24 (ativos, rascunhos, quizzes).

## 4. Agentes de IA

Existem **4 agentes**, e a Bela existe em duas versões.

| Agente | Id | Estado | Modelo | Base de conhecimento | Canal |
|---|---|---|---|---|---|
| **Bela (SDR, venda R$ 97)** | `a8a076d4…` | **active** (publicada 23/11/2026, versão 1) | `claude-sonnet-5`, temperatura 0,3 | 5 fontes, **39 perguntas e respostas** | WhatsApp, número Zion Collection `96346b98…` (via posto "Bela · WhatsApp") |
| Bela (rascunho, Clube R$ 270) | `adf143ae…` | **draft**, nunca publicada | `claude-sonnet-4-6`, 0,3 | 1 fonte, **22 perguntas e respostas** | nenhum |
| Social Seller Zion · Limpeza da base | `42065d48…` | draft | `claude-sonnet-4-6` | 0 fontes | nenhum |
| Zaya | `db450d9a…` | **active** (versão 57) | `claude-sonnet-4-6` | 0 fontes | `channels` vazio no agente |

Detalhes da Bela ativa:
- Posto único `a3852ba2…` "Bela · WhatsApp": papel `sdr_inbound`, modo `autopilot`, `status: active`, canal WhatsApp Zion Collection, funil `40529cf1…` (Funil Zion), etapa "2 · Zaya qualificando". Máximo de 20 turnos. Follow-up por silêncio configurado em 720 min, mas `maxFollowUpAttempts` é 0. Rotinas da manhã e da noite desligadas. Não agenda reunião (`allowScheduleMeetings` false).
- Base de conhecimento (todas `synced`): "Plataforma Zion Collection · acesso R$ 97" (29 itens), "PRIORIDADE · Convite oficial" (3), "PRIORIDADE · Como a Zion avalia" (2), "PRIORIDADE · O que a pessoa constrói na plataforma" (3), "PRIORIDADE · Prazo de acesso" (2). Total 39.
- Tudo na Bela ativa trata a venda como **R$ 97** em `/inscricao`, sem reunião. **Nada na base cita o R$ 47** nem a Mini Mentoria. Se a máquina de vendas for de R$ 47, a Bela precisa de conteúdo novo (não alterado aqui).
- A persona manda citar "12 meses" ao enviar o link, mas uma pergunta de prioridade na base diz para não citar o prazo sem ser perguntada. As duas instruções se contradizem.
- Escalações ativas na Bela: 6 (pessoa, pagou sem acesso, Bubble, negociação, reunião marcada, reativação).
- Ferramentas usadas nos últimos 30 dias: aplicar tag, registrar qualificação, nota, tarefa, consultar agenda, escalar, encerrar, registrar oportunidade, agendar reunião.

Desempenho nos últimos 30 dias (`ai_sdr_overview`, todas as versões juntas): 571 decisões; 348 entregas; 344 respostas; 38 passadas a humano; 61 silenciadas; 112 erros (80 `turn_failed`); follow-ups: 63 falharam, 27 cancelados, 0 enviados. Na Bela de R$ 97 especificamente: 131 decisões, 85 entregas, 3 erros, 35 leads, última atividade 27/11/2026.

Chaves de IA: uma chave Anthropic `active` (id `1fd81150…`, usada pela Bela). A outra (`8aeb3601…`, usada pela Zaya e pela Social Seller) está **`invalid`** (401 "invalid x-api-key"). Isso é coerente com os 109 erros do posto quando operava a Zaya e com a última atividade da Zaya em 21/11. Zaya segue com status "active", mas sem canal próprio e com chave inválida.

Modelos disponíveis na chave: **não consultado** (`ai_agents_models_list` não foi chamado).

## 5. Pipeline Funil Zion `40529cf1-6a35-4fde-a314-d2ebe9aab061`

Nome: "Funil Zion · Novo lead → Reunião → Venda". 29 etapas, 265 cards abertos, R$ 41.400 em aberto. É o funil do modelo com reunião (Mentoria R$ 2.900 etc.), ainda com a Zaya na descrição.

### 5.1 Etapas atuais (nome · id · cards)

| # | Etapa | Id | Cards |
|---|---|---|---|
| 0 | Leads de hoje | `50d19a87-4c52-41e1-81be-bcfba8d3f7f9` | 5 |
| 1 | Janela aberta · responder agora | `70265e33-ea33-4ef3-998d-1451733f8ebf` | 1 |
| 2 | Janela fechada · ligar | `442ccf98-0999-4375-a951-9233b520fbba` | 100 |
| 3 | Leads do dia anterior | `07e26e78-c8c9-4141-a646-2badeae37193` | 2 |
| 4 | Ativação 1 | `66349b39-815f-444f-be41-89dc437db434` | 5 |
| 5 | Ativação 2 | `fc76e15f-6f16-4396-8743-08765f880333` | 0 |
| 6 | Ativação 3 | `83faa73d-740c-497a-acd5-93781b84813b` | 0 |
| 7 | Não respondeu / Acumulados | `8c424dee-1892-4573-bceb-727915d0f2fc` | 86 |
| 8 | Precisa de investimento | `9cdfa8dd-f64e-47dc-bdf6-4a1dd8d1897f` | 13 |
| 9 | Quer fazer sozinho | `e035f88c-afdc-4caf-82e8-4d935dd6c26a` | 2 |
| 10 | Outros | `713bef1f-1276-4688-9185-5023ae4cc9c3` | 4 |
| 11 | 2 · Zaya qualificando | `6f7810b5-ae92-4a51-afbb-c31d661681f7` | 11 |
| 12 | 5 · Reunião agendada | `018b18e0-2c7f-4dbe-9943-8e87249ac8ca` | 20 |
| 13 | 5a · Reuniões de hoje | `ac0c4e70-078f-4906-8bb3-1c14671b9226` | 0 |
| 14 | 6 · Reunião feita | `31ca4e88-bc34-4f55-8e81-0251d806a5a1` | 9 |
| 15 | 8 · Comprou o acesso à plataforma | `887a445d-b158-4f4f-bd9b-7e08a4d591cb` | 5 |
| 16 | Formulário · R$ 5 mil ou mais → agendar | `9000d5eb-d8ec-4d49-a37c-84476aeea170` | 1 |
| 17 | 4 · Já pagou (modelo antigo) · agendar | `98eaf4bc-09cd-404b-800e-3cff4253b101` | 1 |
| 18 | 5b · No-show · reagendar | `5a0e9648-ce4a-442d-affe-18d5767aad86` | 0 |
| 19 | 6a · Link de adesão enviado | `1104b792-6084-4313-af62-cec39cb2e702` | 0 |
| 20 | 7 · Oferta feita · follow-up Zaya | `7b98ea9f-2381-4c0c-b6a8-f536a923eed4` | 0 |
| 21 | Agora não · nutrir | `7f02dea3-dee3-4103-b121-c508ae187310` | 0 |
| 22 a 28 | 7 etapas "(antigo)": Dor · Sem capital; Dor · Quer mentoria; Dor · Quer parceiro ou investidor; Dor · Não sabe por onde começar; Formulário · menos de R$ 5 mil → nutrir; 3b · Liguei, não atendeu → mandei áudio; 3 · Ligar hoje (Bruno) | `ed1cecf9…`, `245cd35c…`, `1a68fc26…`, `295ef5bf…`, `b8f47e7e…`, `13617297…`, `384c6663…` | 0 cada |

### 5.2 Comparação com as 17 etapas propostas

| # | Etapa proposta | Funil Zion (equivalente existente ou faltante) |
|---|---|---|
| 1 | novo lead | Existe: "Leads de hoje" e "Leads do dia anterior" |
| 2 | lead qualificado | Parcial: "2 · Zaya qualificando" (qualificando, não qualificado); "Formulário · R$ 5 mil ou mais → agendar" é um filtro do modelo antigo |
| 3 | primeiro contato Bella | Parcial: "2 · Zaya qualificando" faz esse papel, mas com o nome da Zaya. Etapa com nome Bela: faltante |
| 4 | plataforma apresentada | Faltante. Mais próximo: "7 · Oferta feita · follow-up Zaya" (modelo antigo, 0 cards) |
| 5 | produto demonstrado | Faltante |
| 6 | interessado | Faltante |
| 7 | objeção identificada | Parcial: "Precisa de investimento", "Quer fazer sozinho", "Outros" (classificam o motivo, não a objeção) |
| 8 | checkout acessado | Faltante |
| 9 | pagamento pendente | Faltante |
| 10 | recuperação | Parcial: "Não respondeu / Acumulados" (86), "Ativação 1 a 3" |
| 11 | compra confirmada | Existe: "8 · Comprou o acesso à plataforma" (5 cards, R$ 4.700 no total) |
| 12 | plataforma acessada | Faltante neste funil. Existe em outro pipeline: "Alunos Zion" etapa "3 · Fez o primeiro acesso" |
| 13 | projeto em estruturação | Faltante neste funil. Existe em "Mentorados Zion" etapa "3 · Estruturando o projeto" (0 cards) e, em parte, em "Inscritos" etapa "3 · Em avaliação pela Zion" |
| 14 | dossiê concluído | Faltante neste funil. Existe em "Mentorados Zion" etapa "4 · Dossiê concluído" (0 cards) |
| 15 | projeto apresentado | Faltante. Mais próximo: "Mentorados Zion" etapa "5 · Sessão de Diagnóstico solicitada" |
| 16 | nutrição | Existe: "Agora não · nutrir" (0 cards) |
| 17 | encerrado ou descadastrado | Faltante. Nenhuma etapa de descadastro. O funil só tem "Outros" |

Resumo: 3 existem, 4 parciais, 10 faltantes, das quais 4 (12 a 15) existem em outros pipelines.

### 5.3 Pipeline "Inscritos · Plataforma Zion Collection" `8b4405c0-f50a-40ba-abfd-11ab80e1ec41`

Descrição: quem comprou o acesso de R$ 97 pelo checkout direto; criado desligado, sem automação de entrada. 6 etapas, 5 cards (todos na etapa 1), R$ 14.400 em aberto.

| Etapa existente | Id | Cards |
|---|---|---|
| 1 · Comprou · falta preencher a ficha | `779d2fa8-ed04-451c-a8a7-b4f32e5703f8` | 5 |
| 2 · Ficha preenchida | `909d9585-0395-4c9e-af5c-a6582bfdb93c` | 0 |
| 3 · Em avaliação pela Zion | `f8621613-b319-45dc-99f6-d11c9be27576` | 0 |
| 4 · Precisa de investimento | `b8918fcb-0517-492b-974f-0dd028208b4e` | 0 |
| 5 · Quer fazer sozinho | `56d78879-6bcd-439a-a257-f83c55c077ca` | 0 |
| 6 · Sem retorno · acompanhar | `1fa17b3d-463a-42ae-ba27-e9faed13e535` | 0 |

| # | Etapa proposta | Equivalente em "Inscritos" |
|---|---|---|
| 1 a 10 | novo lead, qualificado, primeiro contato Bella, plataforma apresentada, produto demonstrado, interessado, objeção, checkout acessado, pagamento pendente, recuperação | Faltante (o pipeline só começa depois da compra). Parcial só para 7: etapas 4 e 5 classificam o perfil, não a objeção |
| 11 | compra confirmada | Parcial: etapa 1 "Comprou · falta preencher a ficha" (mistura compra e ficha pendente) |
| 12 | plataforma acessada | Faltante |
| 13 | projeto em estruturação | Parcial: etapas 2 "Ficha preenchida" e 3 "Em avaliação pela Zion" |
| 14 | dossiê concluído | Faltante |
| 15 | projeto apresentado | Faltante |
| 16 | nutrição | Parcial: etapa 6 "Sem retorno · acompanhar" |
| 17 | encerrado ou descadastrado | Faltante |

Outros pipelines ativos que podem servir a partes do ciclo pós-compra (lidos, não alterados): "Mentorados Zion" `57448d6d…` (8 etapas, criado 26/11, 0 cards, sem automação); "Alunos Zion" `5f7000a7…` (7 etapas, 0 cards); "Club Zion Collection · Adesão → Pagamento → Membro" `a7216b13…` (5 etapas, 4 cards).

## 6. Fluxos que mandam mensagem a lead e canais

### 6.1 Fluxos ativos que enviam mensagem (WhatsApp)

Total de fluxos em modo ativo: 43. Pelos filtros de número de WhatsApp e de texto de mensagem, 8 têm passo de envio. **Nenhum fluxo ativo usa e-mail** (filtro pelo remetente verificado voltou vazio) e nenhum envia SMS que eu tenha comprovado.

| Fluxo | Gatilho | Modelo | Estado | Execuções |
|---|---|---|---|---|
| Club 97 · Nova oportunidade (24/11 09h30) `c84db4a6…` | manual | `clube_nova_oport_d1` (vídeo da plataforma, inscrição R$ 97), segundo o objetivo do fluxo | active | 32 |
| Reunião de hoje · Lembrete 1h antes · 14:00 / 15:00 / 16:00 / 17:00 (4 fluxos) | manual | `lembrete_reuniao_1h` | active | 1 cada |
| Lembretes da reunião · Zaya (lead) `16be7020…` | agendamento criado ou remarcado | 2 envios com espera (modelos não lidos) | active | 23 (20 contatos) |
| Funil Terreno · 4 Falar com a equipe → aviso `ce384dbd…` | botão de modelo | confirmação ao lead + aviso à equipe (modelo não lido) | active (objetivo diz "Rascunho") | 5 |
| Funil Terreno · 5 Não quero receber / Agora não `56545fb9…` | botão de modelo | confirmação ao lead (modelo não lido) | active (objetivo diz "Rascunho") | 0 |

Os fluxos da máquina de R$ 47 e R$ 97 (ZC47: pagamento confirmado, não concluiu a compra, questionário, dossiê) **não enviam mensagem ao lead**: o próprio nome diz "alerta + tarefa" ou "só etiqueta", e nenhum apareceu nos filtros de envio. Todos com 0 execuções, ou seja, **nunca disparados**: não comprovados em produção.

Observação: o fluxo `Club 97 · Nova oportunidade` mostra 32 execuções em 24/11. Os demais envios manuais já ocorreram. Nenhum envio novo foi feito por esta auditoria.

### 6.2 Canais

| Canal | Estado lido |
|---|---|
| WhatsApp **Zion Collection** `96346b98…` (+55 48 6137-1061) | `live`, `CONNECTED`, qualidade **GREEN**, verificado (business), teto de mensagens TIER_2K |
| WhatsApp "Pablito Ads" (`5511955054588`) | `live`, `CONNECTED`, qualidade UNKNOWN, TIER_2K (não é da máquina de vendas, só listado) |
| Webchat "Suporte · Clube Zion Land" `5f3517c3…` | `live` |
| Instagram | 1 canal `pending`, sem nome (não conectado) |
| Telegram | nenhum |
| **Caixa de e-mail conectada** (IMAP/SMTP) | **Nenhuma**. Não há canal `email` na lista |
| Domínio `zionhotelgroup.com` | e-mail configurado e **verificado** (`postmarkVerified` true), não pausado |
| Domínio `zionbubbleglamping.com` | **não verificado** (`postmarkVerified` false) |
| Remetente verificado | 1: "Zion Hotel Group" `contato@zionhotelgroup.com`, confirmado, não revogado, responder para o e-mail do Bruno |

Modelos de WhatsApp (Gupshup) do número Zion Collection: 145 no total; 116 aprovados, 27 em rascunho, 1 rejeitado, 1 com falha, 0 pendentes. Existem aprovados `zc47_pix_pendente`, `zc47_ultima`, `zc47_retomar_24h`, `clube_plataforma_d0`, `inscricao_novo_d0`, `inscricao_confirmada`, entre outros (lista completa não reproduzida). O conteúdo dos modelos zc47 não foi lido, portanto não se sabe se estão de acordo com a oferta de R$ 47.

## 7. Recursos nativos que servem à máquina de vendas

| Recurso | Estado lido | Observação |
|---|---|---|
| SDR de IA (`ai_sdr_overview`) | **Ligado.** Bela ativa em autopilot no WhatsApp Zion Collection | 30 dias: 571 decisões, 112 erros; ver seção 4 |
| Segmentos dinâmicos | **Disponível e em uso.** 24 segmentos | 15 com prefixo `[HIB]` criados em 25/11 (ex.: Origem Meta 254 leads; Coorte desde 23/11 80; Interesse 81; Compra aprovada MM47 0; Pagamento pendente 0; Checkout 0; Reembolso 0; Exclusão compradores da plataforma 6; Quente elegível 79). Mais segmentos de reativação e pré-diagnóstico. Atualização feita em 27/11 |
| Temperatura de lead | **Disponível.** Configuração padrão "Lançamento" (limites morno 30, quente 60, janela 14 dias). Registro criado em 28/11 01:54, sem modelo personalizado e sem pesos próprios | Nunca foi calibrada. Para ticket baixo existe o modelo pronto "Low ticket" (não aplicado) |
| Lead score (por critérios) | **Desligado** (`enabled` false), **0 regras** | Nenhum lead tem pontuação |
| Links rastreáveis (redirect links) | **Disponível, nenhum criado** (0 links) | Nenhum domínio de redirecionamento foi listado nesta auditoria |
| Analytics / dashboards (Insights) | **Disponível e em uso.** 10 dashboards salvos, incluindo "Funil Club · Visão 360", "Comando Comercial · Zion", "Raio-X · Hoje" | Não foram rodados. Nenhum dashboard específico da oferta R$ 47 foi identificado |
| Observabilidade da IA | Disponível (`ai_sdr_overview`, caminho `/settings/connections/ai-agents/observability`) | Funcionou |
| Agente com webhook / HTTP tools, rotinas | Não consultado | n/d |
| Rastreio de página (pixel de página) | Não consultado | n/d |

## 8. Resumo (10 linhas)

1. A oferta R$ 47 `668391e7…` está `approved`, sem erro de sincronização, pagamento único (Pix e cartão 1x), reembolso 7 dias, acesso de 12 meses, entrega em área de membros.
2. O vendedor continua `pending`; venda real e entrega ponta a ponta não foram comprovadas.
3. Os dois portais publicados usam o mesmo curso (9 módulos, 75 aulas, todas ativas): o conteúdo está duplicado, e as turmas ainda se chamam "R$ 97".
4. Não existe área "Meu Projeto". O mais perto é o dossiê inicial e as fichas "Faça agora", hospedadas no GitHub Pages.
5. Nenhum formulário do ClickMax aceita foto ou arquivo; o único com anexo citado é o da ficha do terreno, no Airtable (não lido).
6. A Bela ativa existe (WhatsApp Zion Collection, autopilot, claude-sonnet-5, 39 perguntas e respostas), mas todo o conteúdo dela vende R$ 97; o R$ 47 não aparece nela.
7. A Zaya segue "active", com chave de IA inválida (401); a Bela de R$ 270 e a Social Seller são rascunhos.
8. O Funil Zion tem 29 etapas e cobre 3 das 17 propostas (novo lead, compra confirmada, nutrição); 4 parciais; 10 faltantes (checkout, pagamento pendente, descadastro entre elas). O pipeline "Inscritos" cobre ainda menos.
9. Canais: WhatsApp Zion Collection saudável (GREEN, TIER_2K); e-mail só por `contato@zionhotelgroup.com` verificado; nenhuma caixa de e-mail conectada; nenhum fluxo ativo envia e-mail.
10. Nativos: SDR de IA e segmentos ligados; temperatura só no padrão; lead score desligado; links rastreáveis zero; os fluxos ZC47 existem, mas têm 0 execuções.

## 9. O que NÃO consegui comprovar

- Venda e acesso reais de ponta a ponta (nenhuma compra de teste; vendedor `pending`).
- Se os links das aulas (GitHub Pages, YouTube, Airtable) abrem e funcionam: nenhum foi aberto.
- Onde o app do dossiê e as fichas "Faça agora" guardam os dados do cliente.
- Campos e destino dos dois formulários Airtable (ficha do terreno e banco de áreas).
- Respostas dos formulários `f4522f48…` (0) e `aff270f4…` (0): nunca testados.
- Conteúdo dos modelos de WhatsApp `zc47_*` e se combinam com a oferta de R$ 47.
- Conteúdo dos modelos usados nos fluxos de lembrete e do Funil Terreno.
- Execução dos fluxos ZC47 (todos com 0 execuções).
- Modelos de IA disponíveis na chave da Bela (`ai_agents_models_list` não chamado).
- A oferta Mini Mentoria `0c71eeba…` do `CLAUDE.md` (não lida nesta auditoria).
- Quem atende o chat de suporte do portal e em que horário.
- Domínios de redirecionamento para links rastreáveis, pixel de página e HTTP tools do agente.
