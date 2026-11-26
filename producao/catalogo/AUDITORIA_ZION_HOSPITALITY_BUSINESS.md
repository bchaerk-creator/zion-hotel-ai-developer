---
title: "Zion Hospitality Business · Comando 01"
subtitle: "Auditoria e arquitetura · relatório somente leitura"
date: "26/11/2026"
---

# Como foi feito

A auditoria olhou quatro fontes, sempre só lendo:
- **ClickMax:** só ferramentas de leitura (listas, consultas, documentação oficial).
- **Repositório:** contagem e abertura de amostras de cada grupo.
- **Google Drive:** busca e metadados, sem abrir o conteúdo dos arquivos.
- **Notion:** busca e leitura dos títulos.

**Nada foi criado, alterado, publicado, apagado ou ativado.** Dados de clientes e leads não entram neste relatório.

**Não deu para verificar:**
- as aulas da Trilha 1 no YouTube e o portal externo (os dois domínios são bloqueados neste ambiente);
- o código da ZAIOS (está no Lovable);
- o conteúdo dos PDFs do Drive;
- o motivo das ofertas em `pending_corrections`.

> **Correções ao resumo de 26/11 (`PROMPT_5_MENTORIAS.md`):**
> 1. A Jornada 2 · Gestão está **completa**: 8 módulos, testados em 10/11, com 32 aulas habilitadas no ClickMax. Não está em "2 de 8".
> 2. Os **17 e-books do Método Zion 360°** (Z00 a Z02, D00 a D06, F00 a F06, de 86 a 141 páginas cada, com decks de 40 slides) não estavam no resumo. Eles já cobrem vários temas pedidos como "novos": D05 Conceito e Masterplan, D06 Jurídico e Land Bank, F05 Crédito, F06 Sócios e Captação.
> 3. O Produto 01 já tem 22 vídeos (narração sintética).
> 4. **A conta vende.** O vendedor está `pending`, mas `canSell` é verdadeiro e houve R$ 868 em vendas pelo checkout do ClickMax de 26/10 a 26/11. A regra do `CLAUDE.md` que diz "nenhum checkout vende" está desatualizada.

---

# 1. Inventário real dos ativos

## 1.1 ClickMax (26/11/2026)

**Conta**
- **Vendedor:** `pending` (KYC enviado em 06/11). Conta bancária aprovada. `canSell` é verdadeiro. Gateway: Ticto.
- **Totais:** 2.914 contatos, 74 produtos, 9 funis e 123 automações (20 ativas).
- **Projetos:**
  - Infoprodutos Zion: 79 páginas, 31 fluxos;
  - Zion Reservas: 8 páginas;
  - Projeto de Bruno: 46 páginas, 88 fluxos, 20 disparos.

**Ofertas**
- 45 aprovadas, 16 arquivadas, 13 incompletas e 3 em `pending_corrections`.
- **Nenhuma é recorrente.** A conta nunca teve assinatura (MRR, assinantes e trial estão em 0).
- **23 ofertas têm erro de sincronização** ("Token inválido ou ausente"). Seis delas estão aprovadas: ferramentas 17, 11, 13, 14, 29 e 18.
- **Em `pending_corrections`:** Mini Mentoria de Estruturação (R$ 47, a única liberada para anúncio na Fase 1), Etapa de Desenvolvimento · Plataforma (R$ 290) e Club · Kit de Captação (R$ 97). O motivo da correção não aparece pela API.
- **Ofertas com transação:** só 6, entre elas a Ferramenta 20, o Produto 01 A, a Sessão Zion 360 e as ofertas do Club.

**Portais (6)**

| Portal | Turmas | Cursos | Membros | Estado |
|---|---|---|---|---|
| Zion · Jornada do Desenvolvimento | 11 (7 de arquivo) | 9 | 14 | publicado |
| Zion Collection | 7 | 8 | 11 | publicado |
| Plataforma Zion Collection | 1 | 1 | 5 | publicado em 24/11 |
| Zion Land Bank | 1 | 2 | 7 | publicado |
| Zion Hotel Academy (Produto 01) | 1 | 1 | 1 | publicado |
| Mini Mentoria de Performance Hoteleira | 1 | 1 | 1 | não publicado |

**Cursos (22, sendo 18 habilitados)**
- **Aulas por tipo:** 187 links externos, 73 vídeos, 43 documentos e 9 textos.
- **Trilha 1 · Desenvolvimento:** 10 módulos e 83 aulas (82 habilitadas), em 5 turmas de 3 portais.
- **Plataforma de estruturação Zion Collection:** cópia da Trilha 1 sem os bônus (9 módulos, 70 itens). É a Mini Mentoria de R$ 47.
- **Jornada 2 · Gestão:** 8 módulos e 32 aulas, todas habilitadas.
- **Panorama Marco Zero** (12 aulas, 8 habilitadas) e **Biblioteca Z/D/F** (18 módulos, 36 aulas, 21 habilitadas).
- **Operação, Branding/Marketing e Vendas não têm curso.** Os cursos "Arquivo · Trilha 2/3/4" têm 7 módulos vazios cada. Os bônus de Operação, Branding, Vendas e Gestão têm só 2 ou 3 aulas cada.

**Outros recursos**
- **Páginas:** 133, das quais 49 já foram publicadas em algum momento.
- **Formulários e quizzes:** 23 (13 ativos), com 57 respostas.
- **Agentes de IA:** Bela (ativa no WhatsApp) e Zaya (ativa, sem canal), mais 2 em rascunho.
- **Comunidades:** nenhuma. O módulo de webinars está desligado.

## 1.2 Repositório

| Grupo | Quantidade real | Estado | Mentoria |
|---|---|---|---|
| **Jornada 2 · Gestão** | 8 fichas HTML, 16 planilhas, 8 resumos em PDF, 8 prompts de IA, 8 aulas em mp4 (4 a 7 min) e 8 tutoriais | **Pronto e testado** (narração sintética) | 2. Os Módulos 3 e 4 servem também a 5 e 4; os Módulos 5 e 6 servem a 3 |
| **Trilha 1 · materiais** | 8 e-books (28 a 83 p.), deck de 47 p., 4 planilhas, Kit do Investidor (modelos) | Pronto, sem teste formal | 1 |
| **Trilha 1 · aulas interativas** | 16 decks HTML (8 de aula ao vivo e 8 de prévia) | Pronto, com auditoria registrada | 1 |
| **Trilha 1 · fichas "Faça agora"** | 13 fichas com PDF e envio de anexos | Pronto. Os anexos dependem do servidor Lovable "Zion Dossie Aulas" | 1 |
| **Trilha 1 · vídeos** | 16 aulas no YouTube e 12 tutoriais em mp4 | Tutoriais prontos; as aulas do YouTube não foram conferidas | 1 |
| **Método Zion 360° · e-books** | 17 (Z00 a Z02, D00 a D06, F00 a F06), de 86 a 141 p. cada | Rascunho avançado, "pronto para revisão", sem aprovação de Bruno | 1 (Z e D), 2 (F); o D05 serve também a 4 |
| **Método Zion 360° · decks** | 17 decks de 40 slides e 16 roteiros de aula | Rascunho; nenhum vídeo | 1 e 2 |
| **Método Zion 360° · pilares E, M, L, G, O** | 35 unidades | **Só ementa** | E→1, M→4, L→5, G→2 (a Jornada 2 substitui), O→3 |
| **Mini mentorias A01 a A10 e B01 a B10** | 20 apps de 40 telas, 20 tutoriais, 19 vídeos verticais | Pronto e testado (1.196 checagens) | A: 2, 3, 4, 5; B: 1 |
| **"Seu Airbnb Está Vazio?"** | 3 versões: A01, Arsenal 01 e ZC06 (e-book de 60 p., 2 vídeos, diagnóstico, calendário de 30 dias) | Pronto. Compra não testada | 5 |
| **Produto 01 "Você tem terra. Falta capital?"** | Guia de 60 p., 20 microaulas, 10 ferramentas, 22 vídeos | Pronto e testado. Licença da voz sintética pendente | 1 |
| **E-books de R$ 13** | 3 PDFs (27 a 30 p.) e 15 anexos | Pronto, sem teste registrado | 1 |
| **Ferramentas de R$ 19** | 19 ferramentas, 36 planilhas | Pronto e testado | 2, 3, 4, 5 |
| **Kit de Captação** | Guia de 16 p., Mapa das Fontes, vídeo de 9 min | Pronto | 1 |
| **E-book "Glamping, muito mais que uma hospedagem"** | 61 p. | Pronto, não revisado | 1 |
| **ZAIOS** | Jornadas de Desenvolvimento e Operação, Dossiê | Não validada com pessoas | 1, 2, 3 |
| **Vídeos** | 146 mp4 (75 educacionais e 71 comerciais), cerca de 1,2 GB | Todas as aulas conferidas usam narração sintética; nenhuma foi gravada por Bruno | — |
| **Material comercial** | Mais de 600 criativos e landings, deck de vendas de 19 slides, Zion Sales Engine (225 documentos internos) | Rascunho, documentação interna | Comercial e 5 |

## 1.3 Drive e Notion

| Fonte | O que existe | Estado | Mentoria |
|---|---|---|---|
| Drive · Biblioteca Trilha A | Volumes A01 a A11 (pdf) e versão diagramada de outubro dos volumes 01 a 07 | Parece a versão final | 1 (A08 também 3 e 5; A09 também 4; A10 também 2) |
| Drive · Jornada do COMO | 10 etapas em pdf, de "Se é para mim" a "Como eu saio da operação" | Parece final | 1 a 5 |
| Drive · Panorama e "A Ordem das Coisas" | 2 pdf | Parece final | 1 |
| Drive · Manual Oficial do Método Zion 360°, Programa e Apresentação Oficial | Documentos-base (jun./jul.) | Fonte | todas |
| Drive · rascunhos editáveis dos e-books | 8 docs (jul.) | Fonte | 1 |
| Drive · roteiros de aula | Só Aula 00 e Aula 01 (60 slides cada) | Parcial | 1 |
| Drive · Trilha B · Gestão | Só o índice. **Os 9 volumes não foram encontrados** | Lacuna | 2 |
| Drive · manuais comerciais | Manual e Playbook da SDR, WhatsApp, GoHighLevel, Reservas, "Frases proibidas" | Fonte | 5 |
| Drive · gestão | Manual Mestre de Execução e Manual Oficial · Zion Hotel Management | Fonte | 2 e 3 |
| Drive · glamping | ZION DNA™ · Manual Mestre de Glamping | Fonte | 1 e 3 |
| Drive · branding | Formação Conceitual e Comercial, Primal Branding aplicado à Zion, Hotel Marketing, Google Ads para pousadas | Fonte | 4 |
| Drive · série ZHP | Documentos 1 a 8 (viabilidade, conceito, masterplan, governança), com muitos duplicados | Fonte | 1 e 2 |
| Drive · vídeos | Cerca de 100 brutos de campanha e obra. O único vídeo do método tem **0 bytes**. As pastas de gravação de aulas aparecem vazias | Não são aulas | 4 e 5 (criativos) |
| Drive · estrutura de pastas | "ZION 360° Developer Mastery" e "Zion Hospitality Academy" | Só pastas vazias | — |
| Notion · Bíblia Operacional Zion | 6 manuais (Governança e Limpeza, Técnico e Manutenção, Hospitalidade e Experiência, Gerencial, Comercial e Reservas, Cultura e Branding), Onboarding, Biblioteca de Vídeos V01 a V44 (YouTube), Brand Standards e cerca de 12 procedimentos | A fonte mais completa de operação | 3 (Comercial: 5; Cultura: 4) |

**Não encontrados:**
- o "Blueprint Mestre" da Mentoria de Desenvolvimento;
- os volumes da Trilha B;
- qualquer arquivo com o nome "Zion Hospitality Business";
- aulas gravadas.

---

# 2. Diagnóstico técnico do ClickMax

| # | Funcionalidade | Classificação | Evidência e observação |
|---|---|---|---|
| 1 | Portal central com 3 níveis | **Nativo** | Um portal com uma turma por plano. Turma aceita vários produtos |
| 2 | 3 produtos com 2 ofertas cada | **Nativo** | Produto aceita várias ofertas |
| 3 | Assinatura mensal e anual | **Nativo** | `paymentConfig.recurrence`: mensal a anual, mínimo R$ 5. Cartão e Pix Automático; boleto não |
| 4 | Parcelamento do anual e renovação | **Nativo** | Anual em até 12x; mensal só à vista. Renova automaticamente até o cancelamento |
| 5 | Período gratuito | **Nativo** | 7, 14, 30, 60, 90 ou 180 dias, uma vez por comprador e produto |
| 6 | Upgrade e downgrade | **Não suportado nativamente** (sem cobrança proporcional) | **Contorno:** comprar o outro plano e um fluxo tira o acesso antigo e cancela a assinatura antiga. **Hipótese a testar:** com os 3 planos como ofertas de um só produto, a nova compra pode continuar a mesma assinatura |
| 7 | Controle de acesso por plano | **Nativo** | Entrega por turma ou por curso, com curso bloqueado e botão de compra |
| 8 | Compartilhar cursos entre planos sem duplicar | **Nativo** | Já acontece: a Trilha 1 está em 5 turmas |
| 9 | Liberação e bloqueio automáticos | **Nativo** (cancelamento) e **por automação** (inadimplência) | Gatilho de fatura recusada e ações de dar e tirar acesso à turma. Não verificado se a inadimplência bloqueia sozinha |
| 10 | Apresentações interativas nas aulas | **Desenvolvimento externo**, ligado por link (nativo) | As aulas aceitam vídeo, link, documento e texto. Embutir HTML na aula não foi verificado; hoje 187 aulas usam link externo |
| 11 | Formulários com dados guardados por aluno | **Parcial ou externo** | Formulários nativos gravam no contato, mas não há ficha que o aluno retome. Persistência real hoje: aparelho do aluno ou ZAIOS. Os objetos personalizados do ClickMax podem servir via API |
| 12 | Calculadoras e simuladores | **Desenvolvimento externo** | HTML e planilhas fora do ClickMax, ligados por link |
| 13 | Integração com a ZAIOS | **Por integração** | Gatilho de webhook recebido, ação de requisição HTTP e API pública v0 (marcada como instável, limite de 100 requisições a cada 10 s) |
| 14 | Dossiês personalizados | **Desenvolvimento externo** | Hoje saem na ZAIOS e nas fichas da Trilha 1 |
| 15 | Progresso do aluno | **Nativo** | Progresso por curso, gatilhos de aula, módulo e curso concluídos, certificado. Não verificado como a aula de link externo conta |
| 16 | APIs, webhooks e automações | **Nativo** | Gatilhos de assinatura (criada, cancelada, fatura paga ou recusada, trial), de checkout e de membros. Ações de dar e tirar acesso, tags e HTTP |
| 17 | Conciliação de pagamentos, assinaturas e permissões | **Nativo** (pagamentos e assinaturas) e **externo** (permissões na ZAIOS) | Painel de assinaturas (MRR, churn, inadimplência) e relatório de transações. A ZAIOS precisa de webhook |

**IA por plano:** os agentes funcionam no WhatsApp, Instagram, Telegram e Webchat, e os fluxos podem consultá-los. **Não há assistente de IA dentro da área de membros.** Uma IA por plano exige webchat ou WhatsApp liberado por tag de plano, ou a ZAIOS.

**Bloqueios comerciais atuais:**
- vendedor `pending`, embora venda;
- 23 ofertas com erro de sincronização;
- 3 ofertas em `pending_corrections`, entre elas a da Fase 1 de anúncios;
- **recorrência nunca testada com o gateway Ticto**;
- a regra do `CLAUDE.md` "pagamento único, sem recorrência", que precisa mudar por decisão de Bruno.

---

# 3. Arquitetura recomendada para os três planos

**Princípio:** um portal novo e separado, a **Zion Hospitality Business**. Ele não mexe nos portais atuais, nem no Clube, nem no Land Bank. Os cursos entram uma vez e são compartilhados entre as turmas dos planos.

**Estrutura**
- **Portal:** Zion Hospitality Business (novo).
- **Cursos:** um por mentoria (5), mais um curso "Biblioteca" e um curso "Ferramentas".
- **Turmas:** Basic, Master e Pro. Cada turma recebe os cursos e níveis do plano.
- **Produtos e ofertas,** duas opções:
  - **Opção A, como pedido:** 3 produtos (Basic, Master, Pro) com 2 ofertas cada (mensal e anual). A troca de plano fica manual ou por automação.
  - **Opção B, recomendada para testar primeiro:** 1 produto com 6 ofertas. Pela documentação de trial, a compra de outra oferta do mesmo produto pode continuar a mesma assinatura, o que facilitaria upgrade e downgrade. **Precisa de teste com valor mínimo antes de decidir.**
- **Preços:**
  - Basic: R$ 47 por mês ou R$ 324 por ano (R$ 27 por mês);
  - Master: R$ 97 ou R$ 804 (R$ 67 por mês), a aprovar;
  - Pro: R$ 197 ou R$ 1.764 (R$ 147 por mês), a aprovar.

  O anual pode ser parcelado em até 12x, e o mensal é só à vista.
- **Automações:**
  1. Compra aprovada dá acesso à turma do plano.
  2. Cancelamento: o ClickMax mantém o acesso até o fim do período pago.
  3. Fatura recusada gera aviso e tag, e o acesso é retirado depois de N dias (decisão de Bruno).
  4. Troca de plano tira a turma antiga e cancela a assinatura antiga (se a Opção B não resolver).
  5. Webhook para a ZAIOS com o plano do aluno.
- **Fora do ClickMax:**
  - apresentações interativas, fichas, calculadoras e dossiês, no GitHub Pages ou na ZAIOS;
  - IA no WhatsApp ou webchat, liberada por tag.

**Atenção:** o GitHub Pages é público. Qualquer pessoa com o link abre as ferramentas, porque o endereço é discreto, não protegido. Para um diferencial pago real (Master e Pro), as ferramentas premium precisam ficar atrás de login, na ZAIOS ou em outro sistema.

---

# 4. Mapa de permissões por assinatura (proposta)

| Recurso | Basic | Master | Pro |
|---|---|---|---|
| As 5 mentorias (aulas, e-books, apresentações) | ✓ | ✓ | ✓ |
| Exercícios e fichas "Faça agora" (salvas no aparelho) | ✓ | ✓ | ✓ |
| Biblioteca (Método 360°, volumes, e-books de aprofundamento) | parte | ✓ | ✓ |
| Ferramentas de R$ 19 e mini mentorias A/B (planilhas e apps) | 5 escolhidas | ✓ | ✓ |
| ZAIOS (simulador, dossiê guardado na conta) | — | ✓ | ✓ |
| IA de apoio (WhatsApp ou webchat, por tag) | — | uso limitado | ✓ |
| Dossiê personalizado e revisão | — | — | ✓ |
| Assistência: encontro coletivo mensal | — | ✓ | ✓ |
| Assistência: sessão individual ou revisão de projeto | — | — | ✓ (ex.: 1 por trimestre) |
| Certificado por mentoria | ✓ | ✓ | ✓ |

Tudo nesta tabela é proposta. Quantidades, limites de IA e sessões dependem de Bruno.

---

# 5. Experiência do aluno (proposta)

1. **Entrada:** boas-vindas, ficha de diagnóstico e "por onde começar". O diagnóstico aponta a mentoria de partida: tenho terra, quero construir, já opero, quero vender mais.
2. **Trilha:** cada mentoria é um conjunto de minicursos curtos.

   Cada minicurso ensina uma tarefa real com:
   - vídeo de 2 a 3 minutos;
   - apresentação interativa;
   - exercício;
   - formulário;
   - ferramenta;
   - página do dossiê.

   Na Desenvolvimento, a ordem segue o princípio "antes de construir, entender": território, demanda, conceito e marca, produto, projeto e dinheiro, construção.
3. **Aprofundamento:** o e-book de 30 a 60 páginas e a biblioteca, opcionais.
4. **Domínio:** critério de conclusão observável em cada minicurso (o aluno tem um entregável na mão). O certificado sai quando todos os entregáveis da mentoria estão feitos.
5. **Projeto:** o dossiê do aluno junta as páginas de todos os minicursos. É a "aprendizagem baseada em projetos" aplicada ao negócio dele.
6. **Ritmo:** microlearning de 10 a 20 minutos por sessão. Avisos por WhatsApp só com consentimento e "aprovado" de Bruno.
7. **ECROI** só na página de vendas e na abertura e no fechamento das mentorias. Sem pressão comercial nas aulas.

---

# 6. Reaproveitamento

**A. Conteúdo essencial da formação**
- **1 Desenvolvimento:**
  - Trilha 1 (82 aulas, 16 decks, 13 fichas, 8 e-books);
  - e-books D00 a D06 (depois da revisão);
  - Produto 01;
  - B01 a B10;
  - volumes A01 a A07 de outubro e Jornada do COMO.
- **2 Gestão:**
  - Jornada 2 completa (8 módulos);
  - e-books F00 a F06 (depois da revisão);
  - ferramentas 01, 10, 15, 19.
- **3 Operação:**
  - ferramentas 11, 13, 14, 16, 17, 18, 20, 24, 28, 29, 30;
  - Bíblia Operacional (Notion) como fonte;
  - Módulos 5 e 6 da Jornada 2.
- **4 Conceito, Branding e Marketing:**
  - Módulo 4 da Jornada 2 (Marca e Captação);
  - D05 Conceito e Masterplan;
  - A04, A05;
  - ferramentas 12, 23.
- **5 Aceleração de Vendas:**
  - Módulo 3 da Jornada 2 (Preço e Canais);
  - a versão escolhida de "Seu Airbnb Está Vazio?";
  - A01, A02, A07, A08;
  - ferramentas 01, 11, 22.

**B. Biblioteca de bônus e aprofundamento**
- e-books Z00 a Z02;
- volumes A08 a A11, Panorama, "A Ordem das Coisas";
- e-books de R$ 13;
- e-book Glamping;
- Kit de Captação;
- manuais comerciais e de branding do Drive (adaptados).

**C. Ferramentas práticas de implementação**
- 19 ferramentas de R$ 19;
- 20 apps A/B;
- 16 planilhas da Jornada 2;
- 10 ferramentas do Produto 01;
- ZAIOS;
- planilhas da Trilha 1.

**D. Duplicados a consolidar (escolher um dono)**
1. "Seu Airbnb Está Vazio?": A01 × Arsenal 01 × ZC06.
2. Trilha 1 em 3 lugares: Trilha 1 × Mini Mentoria R$ 47 × Arquivo/Biblioteca.
3. E-books dos pilares da Trilha 1 × D00 a D06.
4. Preço: Ferramenta 01 × A02 × Módulo 3.
5. Fechamento: Ferramenta 10 × Módulo 2 × F02 e F04.
6. Sócio e captação: Produto 01 × B01, B02, B04, B10 × Kit de Captação × F06 × e-book "Terreno parado".
7. Orçamento: B06 × Ferramenta 05 × e-book "Qual cabana".
8. Pilar G × Jornada 2: a Jornada 2 vale.
9. Arquivos repetidos no Drive (A01, planilhas de onboarding, PDFs da série ZHP).

**E. A produzir ou corrigir**
- Ver a seção 7.
- Corrigir também:
  - o vídeo de 0 bytes do método;
  - a licença das vozes sintéticas;
  - os números da Bubble não confirmados (usados no simulador e no deck).

---

# 7. Conteúdos que faltam

**1 Desenvolvimento**
- Minicursos novos: Território, Demanda e Conceito e marca (encaixar na Trilha 1 e no D01 a D05), Tipos de hospedagem, Hotel de renda × venda, Incorporação, Primeira cabana, Glamping com o caso Zion.
- Pilar E (implantação e obra).
- Ferramentas 02, 03, 04, 06 e 07.
- Vídeos dos e-books D.

**2 Gestão**
- Aprovação dos e-books F e encaixe do F02 e F04 sem duplicar a Jornada 2.

**3 Operação**
- **A mentoria inteira em formato de aula** (O00 a O06 é só ementa).
- Aulas que amarram as ferramentas na rotina (antes da chegada, estadia, saída, semana, mês), a partir da Bíblia Operacional.

**4 Conceito, Branding e Marketing**
- Pilar M (M00 a M06 é só ementa).
- E-book "Pare de vender paredes e comece a vender experiência".
- Identidade visual e tom; conteúdo e redes.

**5 Aceleração de Vendas**
- Pilar L (L00 a L06 é só ementa).
- "Calendário vazio é falta de estratégia" (reaproveitar a versão escolhida).
- Venda direta pelo WhatsApp, CRM e reserva direta (fontes: manuais de SDR do Drive e Zion Sales Engine).
- Receita extra por hóspede.

**Plataforma**
- Portal novo, boas-vindas, diagnóstico de entrada.
- Fichas com dados guardados na conta.
- Dossiê consolidado.
- Proteção das ferramentas premium.
- Vídeos gravados por Bruno.

---

# 8. Riscos técnicos e comerciais

1. **Assinatura nunca testada na conta:** com o Ticto e o histórico de erros de token, é preciso testar compra, renovação, recusa e cancelamento com valor mínimo antes de lançar.
2. **Troca de plano sem proporcional:** risco de cobrança dupla ou acesso errado se a troca não for bem desenhada.
3. **Ferramentas em link público:** quem tiver o link acessa sem pagar, o que tira o valor do Master e do Pro.
4. **Persistência por aluno:** fichas salvas só no aparelho se perdem quando o aluno troca de celular. A ZAIOS resolve, mas ainda não foi validada com pessoas.
5. **API do ClickMax marcada como instável:** a integração com a ZAIOS pode quebrar.
6. **Duplicidade e confusão de oferta:** a mesma promessa em vários produtos e preços (R$ 19, 27, 47, 97, 290) pode canibalizar a assinatura.
7. **Conteúdo jurídico e de crédito** (estrutura para sócio, incorporação, CVM, linhas de crédito): precisa de revisão profissional e linguagem educativa.
8. **Vozes sintéticas sem licença registrada** e nenhuma aula gravada por Bruno: risco de percepção de qualidade e de direito de uso.
9. **Números da Bubble não confirmados** circulando em simulador e deck.
10. **Churn:** em assinatura low ticket, sem rotina de uso o aluno cancela. A experiência precisa entregar algo novo todo mês.
11. **Regras atuais do `CLAUDE.md`** ("pagamento único, sem recorrência" e "vendedor pendente = não vende") precisam ser atualizadas por Bruno antes da execução.
12. **Pendências comerciais em aberto:** `pending_corrections` sem motivo visível, 23 ofertas com erro de sincronização e cadastro de vendedor pendente.

---

# 9. Estimativa de esforço

Estimativa em sessões de trabalho do Claude Code (uma sessão é cerca de um dia de rodada). Não conta gravação de vídeo, revisão jurídica nem aprovações de Bruno e do ClickMax.

| Bloco | Esforço estimado |
|---|---|
| Teste de assinatura de ponta a ponta (oferta de teste, valor mínimo, fluxos) | 1 a 2 sessões, mais uma compra real de Bruno |
| Portal, turmas, produtos, ofertas e automações dos 3 planos (em rascunho) | 2 a 3 sessões |
| Consolidar duplicados e montar as mentorias 1 e 2 a partir do que existe | 3 a 5 sessões |
| Mentoria 3 Operação (7 minicursos a partir das ferramentas e da Bíblia) | 6 a 8 sessões |
| Mentoria 4 Branding (5 a 6 minicursos, incluindo o e-book da experiência) | 5 a 7 sessões |
| Mentoria 5 Vendas (5 a 6 minicursos) | 5 a 7 sessões |
| Minicursos novos da Desenvolvimento (cerca de 8) | 8 a 12 sessões |
| Dossiê consolidado e fichas com dados na conta (ZAIOS ou objetos do ClickMax) | 4 a 8 sessões, dependendo da escolha |
| Proteção das ferramentas premium | 2 a 4 sessões |
| **Total aproximado** | **36 a 56 sessões**, em paralelo com gravação e revisões |

---

# 10. Perguntas para Bruno antes da execução

1. **Preços:** aprovar Master (R$ 97 / R$ 804) e Pro (R$ 197 / R$ 1.764)? Haverá período gratuito? De quantos dias?
2. **Regras:** autorizar a mudança de "pagamento único, sem recorrência" para assinatura nesta plataforma?
3. **Estrutura:** 3 produtos × 2 ofertas (como pedido) ou testar antes 1 produto × 6 ofertas para facilitar a troca de plano?
4. **Inadimplência:** quantos dias depois da cobrança recusada o acesso é retirado?
5. **Diferenças entre planos:** o que exatamente Basic, Master e Pro recebem (mapa da seção 4)? Quantas ferramentas no Basic? Quanta IA no Master? Que assistência no Pro?
6. **Produtos atuais:** o que acontece com Clube, Mini Mentoria R$ 47, Produto 01, Arsenal, ferramentas de R$ 19 e e-books de R$ 13? Continuam vendidos à parte, viram bônus ou saem de venda? E quem já comprou?
7. **Duplicados:** qual versão fica em cada caso da seção 6.D?
8. **ZAIOS:** será a área das ferramentas e do dossiê com login (Master e Pro)? Quando é o teste fechado com pessoas?
9. **Conteúdo:** aprovar os e-books Z, D e F, que estão prontos para revisão? Liberar os volumes A01 a A11 e os manuais do Drive como fonte?
10. **Vídeos:** quem grava as aulas (Bruno, equipe, narração sintética com licença)? Onde (Urubici, Florianópolis)?
11. **Números da Bubble:** quais são os oficiais, para usar como caso?
12. **Revisão profissional:** quem revisa os temas jurídicos e de crédito?
13. **Prioridade:** por qual mentoria começar? A sugestão é testar a assinatura primeiro e depois montar Desenvolvimento e Gestão, que já existem quase inteiras.
14. **Pendências do ClickMax:** pedir ao suporte o motivo das ofertas em `pending_corrections`, a correção do erro de sincronização e a situação do cadastro de vendedor.

---

*Relatório somente leitura. Implementação apenas depois da validação conjunta entre Bruno, ChatGPT e Claude Code.*
