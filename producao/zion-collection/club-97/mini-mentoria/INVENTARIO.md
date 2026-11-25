# Inventário real · base para a "Mini Mentoria de Estruturação" (R$ 47)

Data da conferência: 25/11/2026. Sem dados pessoais. **Só leitura**: nada foi criado, ligado, ativado ou alterado no ClickMax, Meta, Airtable ou Lovable. A única escrita é este arquivo.

Regra de uso: só se anuncia o que está na coluna "disponível". O que está "parcial" ou "não existe" não entra em página, anúncio nem mensagem.

Como foi conferido: `portals_list`, `classrooms_list`, `classrooms_details`, `modules_list`, `forms_list/get`, `flows_list/get/structure_get`, `pipelines_list`, `tags_list`, `offers_get`, `sellers_status`, `pages_list`, `ai_agents_list` (ClickMax); `list_tables_for_base`, `list_automations`, `list_pages_for_base`, `get_form_schema` (Airtable); `list_workspaces` (Lovable). Os endereços públicos do GitHub Pages foram testados com HTTP (50 de 50 devolveram 200).

Limites desta conferência:
- Não assisti aos vídeos nem abri o conteúdo das aulas: o que está dito sobre cobertura vem do **título e da descrição** de módulos e aulas.
- Do ambiente de teste, `youtube.com`, `airtable.com` e `zion-plataforma.clickmax.space` ficam bloqueados (código 000). Logo, **17 vídeos do YouTube, os 2 formulários do Airtable e a tela de login do portal não foram abertos**.
- O módulo de objetos personalizados do ClickMax está desligado na conta (`custom-objects:read` negado). Não há "banco de áreas" dentro do ClickMax.
- Lovable: só listei os workspaces (1 workspace, 21 projetos). Não abri nenhum projeto; se houver cadastro de terrenos lá, não foi visto.
- Pixel/CAPI no Meta e no painel do ClickMax não são visíveis por estas ferramentas (ver seção 5).

---

## 0. Atenção antes de tudo (achados que mudam o plano)

1. **Nenhum fluxo está ligado à oferta de R$ 47** (`668391e7…`). O fluxo de compra aprovada `fcc14b4d…` filtra só a oferta de R$ 97 (`c298aaed…`) e está em rascunho. Hoje uma compra de R$ 47 recebe o acesso pela entrega da oferta, mas **não** recebe e-mail de boas-vindas, tag, card no funil "Inscritos", tarefa para a equipe nem link para a ficha.
2. **A oferta de R$ 47 ainda entrega nos dois portais** (antigo `a8e2157a…` / turma `69345987…` e novo `3ef7a340…` / turma `087479a3…`). Remover a entrega antiga só no painel.
3. **O checkout ainda não redireciona para `/obrigado-plataforma`** (pendência de Bruno no painel, conforme `lt47/LANDING_CHECKOUT.md`). Sem isso a ficha pós-compra depende do e-mail do fluxo, que está desligado.
4. **A Bela (agente de WhatsApp, ativo) está instruída a não oferecer o produto de R$ 47** e a falar de R$ 97 com link `/inscricao`. Se o R$ 47 virar a oferta principal, o texto dela precisa de revisão (com "aprovado" de Bruno).
5. **Nada na plataforma entrega "reunião", "mentoria" ou "acompanhamento"** hoje. A oferta de R$ 47 e o agente descrevem acesso à plataforma, sem reunião. O nome "Mini Mentoria" precisa ser decidido com cuidado: se sugerir acompanhamento ou reunião individual, **não bate com o que existe**. Se for só o nome do pacote de aulas e fichas, os 70 itens existentes sustentam.
6. **O módulo de "Bônus · Ferramentas" (11 simuladores) não está na turma nova.** Ele está só no conteúdo `fa9a6c54…` (portal Zion · Jornada do Desenvolvimento, turma "Estruturação · Etapa de Viabilidade…"). As páginas dos simuladores existem e estão no ar, mas **não são aulas da turma `087479a3…`**.

---

## 1. Portal e turma

### Portal
| Item | Valor |
|---|---|
| Portal | "Plataforma Zion Collection" `3ef7a340-0fcc-414a-8f3b-c9404c3b90f4` |
| Endereço | subdomínio `zion-plataforma` (publicado em 24/11 04:52 UTC) |
| Tema | escuro, destaque `#C9B37E`; primeiro acesso sem senha (`firstAccessWithoutPass` true) |
| Suporte | WhatsApp `wa.me/554861371061` (sem e-mail de suporte no portal) |
| Alunos no portal | 4 |
| Classrooms / conteúdos | 1 turma, 1 conteúdo |

### Turma (id conferido: `087479a3-9d6f-4e1f-a542-c47b347bf5ed`)
- Nome: "Plataforma de estruturação (R$ 97)" (o nome ainda diz R$ 97).
- Conteúdo único `79d3e792-7526-4d88-926e-60e401748f3e`, "Plataforma de estruturação Zion Collection", habilitado.
- Acesso: **12 meses** (`accessDuration` 12, `month`).
- **9 módulos, 70 aulas, todas habilitadas**. Tipos: 17 vídeos no YouTube (16 vídeos de pilar + 1 extra), 9 vídeos mp4 hospedados no GitHub Pages (boas-vindas e 8 tutoriais de ficha) e o restante PDFs e páginas interativas.
- Produto ligado à turma: "Zion Collection Club | Acesso à plataforma" `072083e8…`.

### Módulos e aulas (nomes exatos)
| # | Módulo | Aulas | O que cobre (pelo título/descrição) |
|---|---|---|---|
| 1 | Comece aqui · Onboarding | 3 | "Bem-vindo à plataforma Zion Collection" (vídeo mp4); "Monte o seu dossiê inicial" (`/dossie/`); "Suporte · Tire suas dúvidas aqui" (chat ClickMax) |
| 2 | Marco Zero · A visão de toda a jornada | 10 | Comece aqui (PDF); Mapa de direcionamento; Aula interativa; Vídeos 1 e 2; "Faça agora · O seu diagnóstico prévio"; E-book Vol. 1 (PDF); tutorial da Ficha do Marco Zero; **Kit de prompts do Dossiê**; **"Ficha do seu terreno: dados, fotos e documentos"** (formulário Airtable) |
| 3 | Pilar 1 · Território e destino | 8 | destino e chegada; chão, área e papéis; Ficha do Território; e-book; aprofundamento D01 (e-book + aula de 40 slides); tutorial |
| 4 | Pilar 2 · Mercado e demanda | 8 | comparáveis, diária, ocupação; curva do ano, quem paga, quantas cabem; Ficha do Mercado; e-book; aprofundamento D02; tutorial |
| 5 | Pilar 3 · Produto e tipologias | 8 | nicho, público, momento; estadia, promessa, unidade; Ficha do Produto; e-book; aprofundamento D03; tutorial |
| 6 | Pilar 4 · Modelo de negócio | 9 | modelo de renda; modelo de venda; extra "mapa dos modelos"; Modelo de Negócio; e-book; aprofundamento D04; tutorial |
| 7 | Pilar 5 · Masterplan faseado | 8 | masterplan, onde nunca construir; o que cabe, o que se vende, fase um; Masterplan faseado; e-book; aprofundamento D05 "Conceito, Posicionamento e Masterplan"; tutorial |
| 8 | Pilar 6 · Pré-viabilidade | 8 | custo do projeto; conta, três cenários, tempo de volta; Pré-viabilidade; e-book; **Planilha 1 · Orçamento de Abertura**; **Planilha de pré-viabilidade (Estudo de Massas)**; tutorial |
| 9 | Pilar 7 · Capital e Dossiê | 8 | de onde vem o capital; Dossiê e decisão; "Faça agora · O seu Dossiê de Desenvolvimento"; e-book; **Kit do Investidor**; **"Cadastre o seu terreno no banco de áreas da Zion"** (formulário Airtable); tutorial |

Todas as 50 URLs públicas (GitHub Pages) das aulas responderam 200 em 25/11. As planilhas na turma são as versões "EM BRANCO"; as versões "EXEMPLO" existem no repositório (também 200) mas **não estão ligadas a aula nenhuma**.

Observação sobre a leitura técnica: `classrooms_details` para esta turma devolve 82 mil caracteres; o resultado completo foi lido por arquivo. Uma primeira leitura de outro arquivo em cache mostrou a turma antiga "Estruturação · Etapa de Viabilidade…" (portal Jornada, 81 aulas); **a turma correta é a de 70 aulas acima**, confirmada por `classrooms_list` (`totalLessons` 70).

---

## 2. Os 7 temas × o que existe hoje

Legenda: **disponível** = há módulo/aula/ferramenta nomeada, no ar (HTTP 200), na turma de R$ 47. **parcial** = existe parte, ou existe fora da turma, ou sem aula dedicada. **não existe** = nada.

| # | Tema | Status | O que existe (nome exato) | Ressalva |
|---|---|---|---|---|
| 1 | Potencial territorial | **disponível** | Módulo "Pilar 1 · Território e destino" (8 aulas); ferramenta "Faça agora · A sua Ficha do Território" (`/trilha1/aula1/`); "Aula interativa · Pilar 1"; "Aprofundamento · E-book completo: Território e Localização" e aula de 40 slides; Marco Zero com "O seu diagnóstico prévio" | A Ficha **organiza** os dados do terreno; **não calcula nem entrega nota/veredito de potencial**. O "Raio-X do Potencial Turístico" (`zar-b05`) existe no ar, mas **só como bônus fora da turma de R$ 47**. Não anunciar "avaliação de potencial". |
| 2 | Inteligência de mercado | **disponível** | Módulo "Pilar 2 · Mercado e demanda" (8 aulas); "Faça agora · A sua Ficha do Mercado" (`/trilha1/aula2/`); e-book e aula D02 "Mercado e Demanda" | É método para o aluno levantar comparáveis, diária, ocupação e curva do ano. **Não há base de dados de mercado nem relatório pronto**. Sem números de mercado em copy. |
| 3 | Conceito do empreendimento | **disponível** (sem módulo com esse nome) | "Pilar 3 · Produto e tipologias" (nicho, público, momento, promessa, unidade; "Faça agora · A sua Ficha do Produto") e "Pilar 5 · Masterplan faseado" com aprofundamento "Conceito, Posicionamento e Masterplan" | Não existe um módulo chamado "Conceito". O "Construtor de Projeto Turístico" (`zar-b03`) está só no bônus fora da turma. |
| 4 | Estruturação do projeto | **disponível** | "Pilar 4 · Modelo de negócio" (renda ou venda; "Faça agora · O seu Modelo de Negócio"); "Pilar 5 · Masterplan faseado" ("Faça agora · O seu Masterplan faseado"); "Monte o seu dossiê inicial" | Estruturação **jurídica/societária** (D06) e CAPEX/crédito (F01 a F06) existem como e-books, mas na turma "Biblioteca" do portal da Jornada, **não na turma de R$ 47**. |
| 5 | Viabilidade financeira | **disponível** | "Pilar 6 · Pré-viabilidade" (2 vídeos; "Faça agora · A sua Pré-viabilidade"); "Planilha 1 · Orçamento de Abertura"; "Planilha de pré-viabilidade (Estudo de Massas)" (EM BRANCO) | Tem **planilhas e fichas**, não consultoria financeira. Simuladores de ROI/payback ("Simulador de Viabilidade Econômica", "Simulador de Viabilidade Zion", "Calculadora de Implantação Turística", `zar-b08`, `zar-a09`, `zar-b06`) existem no ar, mas **fora da turma**. Sem promessa de retorno. |
| 6 | Preparação para potenciais investidores | **disponível** (parte em modelo) | "Pilar 7 · Capital e Dossiê" (vídeos "De onde vem o capital" e "O Dossiê e a decisão"; "Faça agora · O seu Dossiê de Desenvolvimento"); **Kit do Investidor** (teaser, one-pager, pitch, masterplan de viabilidade, plano conceitual e marca; arquivos `…-MODELO.pptx/docx`); "Kit de prompts do Dossiê" | O Kit do Investidor é **modelo para o aluno preencher**. "Zion Investor Ready" (`zar-b01`) e "Criador de Pitch e Dossiê Turístico" (`zar-b10`) existem no ar, fora da turma. Não prometer investidor. |
| 7 | Possibilidade de parceria com a Zion | **parcial** | Aula "Cadastre o seu terreno no banco de áreas da Zion" (formulário Airtable, com consentimento de privacidade e uma autorização opcional "caso a caso"); descrição do Pilar 7 ("conversar com a Zion, que avalia cada caso"); formulário pós-compra "Conte-nos sobre o seu terreno ou projeto" | Existe o **cadastro**, não existe aula, critério público, fluxo de avaliação nem fluxo de apresentação. Só pode ser dito "a Zion avalia cada caso; cadastro não garante parceria". **Não anunciar "parceria"** como entregável. |

---

## 3. Ferramentas, Dossiê, formulários, banco de áreas, obrigado

### Ferramentas e fichas (todas dentro da turma de R$ 47)
Fichas "Faça agora" (HTML interativo no GitHub Pages): Marco Zero (diagnóstico prévio, `/trilha1/marco-zero/`), Território (`aula1`), Mercado (`aula2`), Produto (`aula3`), Modelo de Negócio (`pilar4`), Masterplan faseado (`pilar5`), Pré-viabilidade (`pilar6`), Dossiê de Desenvolvimento (`pilar7`). Mais 7 aulas interativas por pilar, tutoriais em vídeo por ficha, 2 planilhas xlsx em branco, Kit do Investidor (modelos) e Kit de prompts do Dossiê.

As fichas `aula1` e `pilar7` enviam as páginas geradas por webhook (`ZION_WEBHOOK_URL`) para o Airtable (automação "Página do Dossiê chegou do curso", **implantada**). Não testei o envio.

### Gerador de Dossiê
- Existe como **páginas do Dossiê por pilar**: cada ficha vira uma página; "Faça agora · O seu Dossiê de Desenvolvimento" fecha as sete páginas; o Pilar 7 usa jsPDF para gerar PDF.
- Existe também `/dossie/` ("Monte o seu dossiê inicial"), formulário com autorização de uso das informações.
- No Airtable há campos que contam as páginas (0 a 7) e marcam "Dossiê completo", mas as automações que ligam página→membro, "Marcar dossiê completo" e "Aviso de terreno enviado" estão **não implantadas**.
- Não existe "Gerador de Dossiê" como uma ferramenta única com nome próprio na turma; o que existe é o conjunto acima.

### Formulários (ClickMax `forms_list`: 22 formulários)
Relevantes para a plataforma:
| Formulário | Id | Status | Envios | Observação |
|---|---|---|---|---|
| Zion Collection · Ficha do inscrito (pós-compra R$ 97) | `75ee0a3a-b17b-4fcf-be66-8eb97f6064ad` | ativo | 1 | 5 passos de múltipla escolha; grava campos do lead (perfil, localização, área, objetivo, infraestrutura, documentação, valor da área, impedimento, preparo para investidor); tag de origem `ficha-inscrito-plataforma`; `triggerAutomation` **falso** (não dispara fluxo); conclusão leva a `zion-plataforma.clickmax.space` |
| Diagnóstico gratuito Zion · Formulário de qualificação | `34d1196b…` | ativo | 6 | outro produto |
| Club Zion Collection · Ficha de adesão (Jornada) | `7495df8b…` | ativo | 11 | linha antiga |
| Qualificação · Estruturação do terreno (reunião Zion) | `5c51d939…` | rascunho | 0 | |
| Investidores · Interesse em investir | `5afa9bc9…` | rascunho | 0 | **possível base** do lado "investidor", não é da plataforma |
| Parceiro Zion · Situação do terreno ou da hospedagem | `290a86d7…` | ativo (quiz) | 2 | |
| Pilar 01 · Território — Leitura do seu terreno | `6f58f46c…` | ativo (quiz) | 0 | existe, **não está ligado à turma** |

Formulários que a turma de R$ 47 realmente usa: os dois **formulários do Airtable** dentro das aulas ("Ficha do seu terreno: dados, fotos e documentos" e "Cadastre o seu terreno no banco de áreas da Zion"), mais o formulário ClickMax pós-compra (acessado pelo e-mail/obrigado, não por aula).

**Não existe:** formulário de pedido de autorização para apresentar o terreno à Zion ou a parceiros dentro do ClickMax, nem ficha de "classificação de potencial comercial".

### Cadastro / banco de áreas de terrenos
- **Vive no Airtable**, base `appNazhHg9mqWAt9h` "ZION LAND BANK | Gestão de Garantias Imobiliárias", tabela **Imóveis** (campos "LM · …").
- Dados do terreno: nome, município, UF, zona, tamanho, situação (matrícula), CAR, o que pensa fazer, mapa, acesso, distância, energia, água, internet, o que já existe.
- Documentos (anexos): matrícula/escritura, CAR, laudo, fotos/mapa/planta, vídeo do terreno, PDFs do Dossiê, planilhas preenchidas, Kit do Investidor.
- Projeto: modelo pretendido, CAPEX estimado, pedido de capital, "o que busca da Zion".
- **Consentimentos:** (a) `LM · Aceite` (obrigatório no formulário "Cadastro do terreno · banco de áreas da Zion") e `Autorização · inscrição Collection` (formulário "Zion Collection · Inscrição do seu terreno ou projeto"); (b) **`LM · Apresentar só com autorização caso a caso`** (opcional, separado). **Sem a marcação (b), o terreno não é apresentado a ninguém.** Este é o ponto de apoio para o passo 6 da jornada.
- Triagem por IA: campos `LM · IA · Status/Parecer/Pendências`; automação "Análise automática do cadastro" **implantada**: roda quando o aceite está marcado e manda e-mail ao membro. Não conferi o texto desse e-mail nem se ele cita "potencial".
- Outras tabelas (Proprietários, Operações, Oportunidades comerciais com "Permissão de contato" e "Data de autorização", Contrapartes e parceiros, Histórico e integrações) existem. Não contei registros.
- Três formulários do Airtable com o mesmo destino (Imóveis): "Cadastro do terreno · banco de áreas da Zion" (`pageylHbg89JNYm81`, o que está na aula do Pilar 7), "Zion Collection · Inscrição do seu terreno ou projeto" (`pagyB6989L0Vs4dYs`, o que está na aula do Marco Zero) e versões antigas (v2, v3, Land Members).
- ClickMax: objetos personalizados **desligados**. Repositório: sem cadastro de terrenos. Lovable: não verificado a fundo.

### Página `/obrigado-plataforma`
- Id `d7166fc3-4f27-483b-8d9e-ca636c7facf0`, tipo `thankYou`, **publicada** (24/11 18:29 UTC), HTTP 200 em 25/11, 2 visualizações no total.
- Dois botões: "Entrar na plataforma" e "Conte-nos sobre o seu terreno ou projeto" (este abre o formulário em link separado: não foi possível embutir). Sem oferta ligada (`offerId` null); o checkout não redireciona para ela.
- Texto de apoio e tarefas do fluxo ainda citam **R$ 97** ("pagou o acesso de R$ 97"): conferir antes de usar com R$ 47.

---

## 4. Jornada interna de 10 passos × o que existe

Entidades que existem no ClickMax e podem sustentar a jornada:
- Pipeline **"Inscritos · Plataforma Zion Collection"** `8b4405c0-f50a-40ba-abfd-11ab80e1ec41` (é pipeline, não funil; `funnels_get` não o encontra). 6 etapas: 1 Comprou · falta preencher a ficha; 2 Ficha preenchida; 3 Em avaliação pela Zion; 4 Precisa de investimento; 5 Quer fazer sozinho; 6 Sem retorno · acompanhar. 2 cards, ambos na etapa 1. **Sem automação de entrada.**
- Etapa "8 · Comprou o acesso à plataforma" no pipeline "Funil Zion · Novo lead → Reunião → Venda" (`40529cf1…`).
- Tags: "CLUB 97 | COMPROU" `b552bd62…`, "CLUB 97 | FICHA PREENCHIDA" `54c06a96…`, "CLUB 97 | PIX NÃO PAGO", "CLUB 97 | CHECKOUT ABANDONADO" (nenhuma atribuída a leads hoje: `leadsCount` 0). Há também tags de potencial do Diagnóstico ("DIAG | POTENCIAL ALTO" 18 leads, "DIAG | POTENCIAL COM AJUSTES" 34) e "POSSÍVEL PARCEIRO ZION" (14), que pertencem ao diagnóstico antigo, **não à plataforma**.
- Fluxos da plataforma: ver tabela.
- Bela (agente, ativa) e Zaya (ativa, linha antiga de diagnóstico/reunião).

| Passo | Já existe | Status | Falta |
|---|---|---|---|
| 1. Liberar acesso | Entrega da oferta (membership nas duas turmas); fluxo `fcc14b4d` concede a turma nova (`grantClassroomAccess`) | Entrega da oferta: **ativa** (acesso criado sozinho nas 2 compras reais de R$ 97, 1–2 min). Fluxo `fcc14b4d`: **rascunho, nunca executado**, gatilho só da oferta de R$ 97 | Gatilho para a oferta de R$ 47; remover a entrega do portal antigo (painel); teste de execução do fluxo; na oferta R$ 47 o ciclo pagamento→acesso **não está provado de forma independente** |
| 2. Orientar | E-mail de boas-vindas dentro do `fcc14b4d` ("acesso chegou", 3 passos, link do obrigado); módulo "Comece aqui · Onboarding" com vídeo de boas-vindas; Bela orienta o pós-compra | E-mail: **rascunho** (fluxo desligado); onboarding: **ativo** na turma; Bela: **ativa** | Revisar textos (R$ 97→47); WhatsApp pós-compra `clube_pos_compra` não existe; checkout sem redirecionamento ao obrigado |
| 3. Disponibilizar conteúdos | Turma com 9 módulos e 70 aulas habilitadas; liberação "DAYS_AFTER_PURCHASE" sem prazo (todas liberam na compra) | **ativo** | Decidir o que da turma entra na "Mini Mentoria" e o que fica fora; bônus de simuladores fora da turma; planilhas EXEMPLO sem aula |
| 4. Formulários | ClickMax `75ee0a3a…` (ficha do inscrito, **ativo**, sem automação); 2 formulários Airtable em aulas; formulário `/dossie/` | **ativo**, porém soltos | Ligar resposta → tag "FICHA PREENCHIDA" e → etapa 2 do pipeline (hoje `triggerAutomation` falso); ficha embutida no obrigado (validação do ClickMax impediu) |
| 5. Gerar dossiê | Fichas por pilar geram páginas; PDF no Pilar 7; webhook → Airtable "Página do Dossiê chegou do curso" | Fichas/PDF: **ativos**; webhook Airtable: **implantado**; "Ligar página ao membro" e "Marcar dossiê completo": **não implantados** | Teste ponta a ponta (aluno gera → chega no Airtable → "Dossiê completo"); aviso ao aluno quando completo; não há gatilho no ClickMax para "dossiê completo" (a tag `DOSSIÊ | COMPLETO` existe, com 0 leads, e o fluxo antigo `e8307aee` é rascunho) |
| 6. Pedir autorização para apresentar à Zion | Checkbox opcional no Airtable "LM · Apresentar só com autorização caso a caso" + tabela "Oportunidades comerciais" com "Permissão de contato", "Data de autorização", "Fonte do consentimento" | Campos: **existem**; processo: **não existe** | Fluxo/mensagem pedindo autorização por escrito, caso a caso; registro da data e do texto aceito; nenhuma automação faz isso hoje; a ficha ClickMax pós-compra **não** tem esse consentimento |
| 7. Cadastrar o terreno após autorização | Formulário Airtable na aula do Pilar 7 e na do Marco Zero | **ativo**, mas o cadastro é feito **pelo próprio aluno, antes de qualquer autorização** (o aceite de privacidade é separado da autorização de apresentação) | Definir a ordem real (aluno cadastra por conta própria × Zion cadastra depois de autorizar); separar "cadastro no banco" de "apresentação a terceiros" na copy |
| 8. Notificar equipe | `fcc14b4d` cria tarefa "Conferir acesso e ficha do inscrito"; Airtable "Zion Collection · Aviso de terreno enviado" (e-mail ao Bruno); fluxos antigos `68a7b4ae` e `dbff4d83` avisam em outras ofertas | Tarefa: **rascunho**; aviso Airtable: **não implantado**; os dois fluxos antigos: **ativos, mas de outras ofertas** | Aviso para a oferta de R$ 47 e para "ficha preenchida"/"terreno cadastrado"; definir quem recebe e por qual canal |
| 9. Classificar potencial comercial | Etapas do pipeline "3 Em avaliação", "4 Precisa de investimento", "5 Quer fazer sozinho", "6 Sem retorno"; no Airtable "LM · IA · Status/Parecer" | Etapas: **existem, sem regra**; IA do Airtable: **ativa para o Land Members**, sem conferir se classifica potencial comercial | Critério escrito de classificação (quem decide, com quais campos); regra ou fluxo que move cards; temperatura/score do ClickMax não configurados para isso (não verificado) |
| 10. Encaminhar oportunidades a contato/reunião | Agenda "Equipe Zion", pipeline "Reuniões agendadas · Zion", fluxos de lembrete e no-show (ativos para a linha de diagnóstico); Bela/Zaya | Ativos para a linha **antiga** de reunião; Bela: **não oferece reunião** por instrução | Fluxo/tarefa que leve do status "oportunidade" para contato humano; texto da Bela e da página consistentes com "sem reunião" (ou decisão de reabrir reunião só para casos selecionados); mensagem de convite sem promessa |

Fluxos de recuperação da plataforma (todos **rascunho, só tag, sem mensagem**): `01b4967a…` (Pix gerado e não pago) e `deb2de62…` (checkout abandonado). Existem outros rascunhos antigos para R$ 97 (`575dd0b9`, `11e8b263`, `c5092264`) que dependem de modelos de WhatsApp.
Fluxo `bc86b069…` ("Inscrição 270 · Abertura", **ativo**, 80 execuções) e `c84db4a6…` ("Club 97 · Nova oportunidade", **ativo**, 32 execuções) foram usados para disparos de R$ 97; não são pós-compra.
Fluxo ativo `68a7b4ae…` e `dbff4d83…`: pós-compra de outras ofertas ("Inscrição de Terreno ou Projeto", "Consultoria Zion 360"), com 0 e 1 execução; **conferir que não disparam na oferta de R$ 47** (os filtros não são de R$ 47, pelo que li de `fcc14b4d`; não abri esses dois).

---

## 5. Rastreamento

| Item | Situação | Fonte |
|---|---|---|
| Pixel Meta `903918118859018` | Existe no repositório e foi usado em anúncios (Produto 01) por decisão de Bruno. **Nenhuma página do ClickMax o carrega** (a `/parceiro-zion` não tem `fbevents.js`/`fbq`; `pixelViewContent` false também no obrigado). **Não verifiquei no Gerenciador de Eventos** | `LANDING_CHECKOUT.md` §4; `pages_list` |
| Conversions API (CAPI) | **Não configurada** (consta como lacuna em `AUDITORIA.md`, `RASTREAMENTO.md`, `LANDING_CHECKOUT.md`). Existe só um modelo testado em Node (Produto 01) | repositório |
| Purchase | O script do checkout nativo chama `fbq('track','Purchase')` no Pix **gerado** (pendente), não na confirmação, **se** houver `fbq`. Hoje não há `fbq`, então nada dispara | `LANDING_CHECKOUT.md` |
| Webhooks | Webhook do Airtable recebe páginas do Dossiê (implantado). No ClickMax, gatilhos `checkout.transaction.paid.v1`, `checkout.pix.generated.v1`, `cart.abandonment.v1` existem nos fluxos. O fluxo de compra aprovada (`fcc14b4d`) só escuta a oferta de R$ 97. Webhooks de gateway para fora: não vi nenhum configurado | `flows_get`, Airtable |
| Gateway | **Ticto** (`gatewayName` "ticto" na oferta e no vendedor), checkout nativo do ClickMax. **Asaas não participa** deste caminho (existe fluxo Asaas `69c42dbf`, rascunho, de outra linha) | `offers_get`, `sellers_status` |
| Vendedor | `canSell` true; banco `approved`; `sellerStatus` ainda **pending** | `sellers_status` |
| UTM na venda | O checkout guarda `utmSource, utmMedium, utmCampaign, utmContent, utmTerm, src, sck`. A página repassa os parâmetros ao checkout (testado só no iframe). **Gravação na venda não provada com venda real de R$ 47** (a única venda é de teste sem UTM). `ad_id`/`campaign_id` não são campos da venda | `LANDING_CHECKOUT.md` §4 |
| Páginas | `/parceiro-zion` (R$ 47, publicada, checkout embutido), `/inscricao-47` (91 views em 7 dias), `/obrigado-plataforma` (2 views) | `LANDING_CHECKOUT.md`, `pages_list` |
| Zaya | Agente ativo (v57, 98 conversas), roteiro de **reunião de diagnóstico**, não vende e não cita preço; modelo `claude-sonnet-4-6`. **Substituída em parte pela Bela** (nome antigo) | `ai_agents_list` |
| Bela | Duas versões: "Bela" ativa `a8a076d4…` (SDR da Zion Collection, WhatsApp, R$ 97, sem reunião, 27 conversas) e "Bela" rascunho `adf143ae…` (versão R$ 270, não usar) | `ai_agents_list` |
| CRM | ClickMax: 11 pipelines (Inscritos plataforma, Funil Zion, Alunos Zion 7 etapas etc.), tags, campos personalizados do grupo "Forms Meta" alimentados pelo formulário. Airtable: base Land Bank (imóveis, oportunidades, histórico). **Não há ponte automática ClickMax↔Airtable** (só pelo e-mail digitado nos formulários) | `pipelines_list`, Airtable |
| Meta (campanhas) | Não consultado por regra. Pelos registros do repositório, LT47 tem campanha `120250557994600016` ligada desde 24/11 23:09Z (R$ 30/dia, aprovada por Bruno); o teto de CLAUDE.md fala de R$ 0 e esse registro mostra que foi **alterado por aprovação posterior** | `OFERTA.md` |

Taxas (leitura anterior, não refeita): venda de R$ 47 no Pix = taxa R$ 2,49, líquido R$ 44,51 (1 venda de base; cartão desconhecido).

---

## 6. Lacunas, em ordem de importância

Marcadas com **(R)** quando podem ser montadas só como rascunho, sem ligar nada; **(B)** quando dependem de Bruno no painel ou de decisão.

1. **(B) Nome e promessa da "Mini Mentoria".** Hoje só existe acesso a plataforma, fichas, planilhas e kits. Não existe mentoria, reunião ou acompanhamento. Definir se o nome é só rótulo do pacote, e alinhar página, anúncios, Bela e e-mails. Sem isso, qualquer copy "mentoria" promete o que não há.
2. **(R) Fluxo de compra aprovada para a oferta de R$ 47.** Clonar `fcc14b4d` em rascunho com `offerId` `668391e7…`, textos sem "R$ 97" e tarefa ajustada. Ligar só com "aprovado" e depois de teste. (Alternativa: ampliar o gatilho do `fcc14b4d`, que é mexer em fluxo existente; preferir clonar.)
3. **(B) Entrega e redirecionamento da oferta de R$ 47 no painel:** remover a entrega do portal antigo; redirecionar o checkout para `/obrigado-plataforma`; renomear a turma "Plataforma de estruturação (R$ 97)".
4. **(R) Ficha → etiqueta → etapa do pipeline.** Fluxo em rascunho: formulário `75ee0a3a…` respondido → tag "CLUB 97 | FICHA PREENCHIDA" + mover para "2 · Ficha preenchida". Requer ligar `triggerAutomation` no formulário (mexe em formulário existente: pedir "aprovado").
5. **(R) Texto e fluxo de pedido de autorização** para apresentar o terreno à Zion ou a parceiros, caso a caso, com registro de data e redação aceita (Airtable já tem os campos). Rascunho de texto + desenho do fluxo; nada enviado.
6. **(R) Critério escrito de classificação de potencial comercial** (campos do formulário × etapas 3 a 6 do pipeline), em documento. Hoje as etapas existem sem regra. Sem promessa ao aluno.
7. **(R) Aviso à equipe** por "terreno cadastrado" e "ficha preenchida" para a oferta de R$ 47 (rascunho no ClickMax; automação do Airtable "Aviso de terreno enviado" está não implantada, depende de Bruno).
8. **(R/B) Decidir quais ferramentas entram na turma de R$ 47.** Os 11 simuladores do bônus e as planilhas EXEMPLO existem, mas não são aulas da turma. Para anunciar "simuladores", teriam que ser adicionados como aulas (mexe em turma: "aprovado").
9. **(B) Tema 7, parceria:** não há aula nem critério. Só falar de "cadastro no banco de áreas, a Zion avalia cada caso". Revisar com Bruno o limite do que se diz sobre parceria e apresentação a investidores.
10. **(B) Rastreamento:** pixel `903918118859018` em páginas do ClickMax, CAPI e regra de Purchase (confirmado, não Pix gerado); prova de gravação de UTM na venda com a primeira venda real de anúncio; conferir tudo no Gerenciador de Eventos.
11. **(B) Bela e Zaya:** a Bela ativa proíbe oferecer o produto de R$ 47 e fala em R$ 97; revisar. Zaya segue na linha de reunião e não deve receber esse público.
12. **(R) Recuperação (Pix e carrinho)** da oferta de R$ 47: rascunhos só de tag existem para R$ 97; faltam textos e modelos de WhatsApp aprovados (nada de envio sem "aprovado").
13. **(R) Testes:** execução de teste do fluxo com lead de teste; compra real de R$ 47 ponta a ponta (pagamento→acesso→e-mail→tag→card→tarefa); teste do envio de uma ficha para o Airtable e da marcação "Dossiê completo". Hoje nenhum desses está provado para a oferta de R$ 47.
14. **(R) Revisão visual no celular** da turma (a leitura aqui foi por dados, não por tela) e abertura dos 17 vídeos do YouTube, dos 2 formulários Airtable e do login do portal fora deste ambiente.
15. **(B) Conta de vendedor ainda "pending"** no ClickMax (já registrado em CLAUDE.md).

### O que dá para montar só como rascunho, sem ligar nada
- Cópia do fluxo de compra aprovada para R$ 47 (itens 2 e 12), com mensagens e tarefa revisadas.
- Fluxo de ficha preenchida → tag/etapa (item 4), sem ligar o formulário.
- Documento do critério de classificação (item 6) e texto do pedido de autorização (item 5).
- Rascunho de e-mail e de tarefa de aviso à equipe.
- Texto-base da página/oferta "Mini Mentoria" usando só os 70 itens da seção 1 e os temas "disponível" da seção 2 (tema 7 só como cadastro).
- Roteiro de teste de ponta a ponta para Bruno executar.

Nada acima foi criado nesta sessão; é só o que **pode** ser montado depois, com a regra de CLAUDE.md (sem ligar, sem disparar, sem gastar).
