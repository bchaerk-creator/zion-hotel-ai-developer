# Auditoria I · Inventário e comparação das ofertas (Mini Mentoria R$ 47 × R$ 97)

Data: 25/11/2026. SOMENTE LEITURA: nada foi criado, alterado, ligado ou enviado no ClickMax, e nenhum commit. Sem dados pessoais de compradores neste arquivo (só contagens).

Legenda: **[EV]** = evidência lida agora (ferramenta ou texto público); **[HIP]** = hipótese ou julgamento do auditor, a confirmar.

Fontes: `offers_get` (4 ofertas), `products_get` (2 produtos), `portals_get` (2 portais), `classrooms_list` (2 portais), `classrooms_details` (turma nova, turma antiga e a turma R$ 270), `dashboard_my_sales` (4 ofertas), `pages_list` + texto público das 6 páginas (curl em 25/11), `INVENTARIO.md` do repositório. Os vídeos do YouTube, os formulários do Airtable e o login do portal não foram abertos (bloqueados no ambiente). O que se diz do conteúdo das aulas vem de título e descrição.

---

## 0. Achados principais (leia primeiro)

1. **[EV] As duas turmas "nova" e "antiga" entregam EXATAMENTE o mesmo conteúdo.** Ambas apontam para o mesmo conteúdo `79d3e792-7526-4d88-926e-60e401748f3e` ("Plataforma de estruturação Zion Collection"): 9 módulos, 70 aulas, mesmos ids de aula, mesma ordem, mesmos links (comparação campo a campo: idênticos). Muda só o portal (endereço, nome, imagem de login). Logo, **R$ 47 e R$ 97 entregam o mesmo conteúdo**; a diferença real é de preço, de nome/descrição da oferta e da promessa das páginas.
2. **[EV] Os acessos não são iguais por oferta:**
   - Mini Mentoria (`0c71eeba`, produto próprio `cbbb5fb1`): 1 entrega, só portal novo (`zion-plataforma`).
   - R$ 47 antiga (`668391e7`), R$ 97 (`c298aaed`) e intermediária (`74a3f8c6`): 2 entregas cada, portal antigo (`zion-collection`) **e** portal novo, mesmo conteúdo nos dois.
3. **[EV] A oferta "intermediária" `74a3f8c6` é uma duplicata sem uso:** nome "Mini Mentoria de Estruturação", R$ 47, mesma descrição da Mini Mentoria, mas pendurada no produto do R$ 97 (`072083e8`), com 2 entregas, **sem página ligada e sem nenhuma venda** (`hasTransaction` false).
4. **[EV] Vendas reais:** nas 4 ofertas há 4 vendas pagas no total: 3 de R$ 97 (2 de clientes reais; 1 do próprio Bruno, teste) e 1 de R$ 47 antiga (Bruno, teste, 24/11). Mini Mentoria `0c71eeba` e intermediária: 0 vendas. Sem reembolso, estorno ou cancelamento registrado. Gateway Ticto em todas.
5. **[EV] O texto das páginas de R$ 97 promete mais do que a oferta entrega** (ver seção 5). A página `/inscricao` diz que a inscrição "abre a oportunidade de você ser nosso parceiro e receber investimentos na sua área" e que a plataforma serve "para conhecermos o potencial do seu terreno". Nada na turma avalia potencial, e a descrição da própria oferta diz "cadastro e análise não garantem investimento, financiamento nem parceria".
6. **[EV] Três páginas de R$ 47 prometem conversa/contato da equipe** ("vamos agendar uma conversa. A nossa equipe entrará em contato com você"), enquanto a descrição da oferta e a FAQ da `/mini-mentoria` dizem "sem acompanhamento individual e sem reunião". Contradição interna.
7. **[EV] O nome "Mini Mentoria" não corresponde ao que se entrega:** é um curso gravado (`productClass` "Curso"). A própria página escreve "Não há acompanhamento individual nem reunião".

---

## 1. Ofertas lado a lado

| Item | (a) Mini Mentoria R$ 47 | (b) R$ 47 antiga | (c) R$ 97 | (d) Intermediária R$ 47 |
|---|---|---|---|---|
| Id da oferta | `0c71eeba-2654-432c-9701-0a31e6113a08` | `668391e7-f4a8-4bd3-a212-deba406f8a7a` | `c298aaed-88ac-46dd-b6f3-f3c07ae08513` | `74a3f8c6-fc1d-4aa8-9ac9-7769a1c49aa5` |
| Produto (id) | `cbbb5fb1-550f-4a8d-b269-5122c17b7780` | `072083e8-88c6-46bd-9e6c-5b851b6ac1c4` | `072083e8-…` (mesmo da b) | `072083e8-…` (mesmo da b e c) |
| Nome do produto | Mini Mentoria de Estruturação | Zion Collection Club \| Acesso à plataforma | idem b | idem b |
| Nome da oferta | Mini Mentoria de Estruturação | Zion Collection Club \| Acesso à plataforma (R$ 47) | Zion Collection Club \| Acesso à plataforma | Mini Mentoria de Estruturação |
| Principal (`isMain`) | sim | não | sim (do produto 072083e8) | não |
| Preço | R$ 47,00 | R$ 47,00 | R$ 97,00 | R$ 47,00 |
| Tipo / classe | course / Curso | course / Curso | course / Curso | course / Curso |
| Pagamento | único; Pix + cartão 1x; boleto desligado; sem recorrência | idem | idem | idem |
| Checkout | `payments.clickmax.io/yhyiqUB9OF` | `…/z3a0AEkvRl` | `…/1ApwIsdYSy` | `…/lbpKjFcTMy` |
| Status | approved | approved | approved | approved |
| Gateway | ticto (sem erro de sincronização, `incompleteReason` vazio) | idem | idem | idem |
| Soft descriptor / suporte | ZIONACADEMY · [telefone de suporte omitido] · e-mail da conta | idem | idem | idem |
| Reembolso | 7 dias | 7 dias | 7 dias | 7 dias |
| Vendas (ClickMax) | 0 | 1 paga (teste de Bruno) | 3 pagas (2 clientes reais + 1 teste de Bruno) | 0 |
| Entrega | `internal_membership` → portal novo `3ef7a340…` / turma `087479a3…` (1 entrega) | portal antigo `a8e2157a…` / turma `69345987…` **e** portal novo / turma `087479a3…` (2 entregas) | idem b (2 entregas) | idem b (2 entregas) |
| Acesso / liberação | 12 meses; liberação `DAYS_AFTER_PURCHASE` sem prazo (tudo liberado na compra) | idem | idem | idem |
| Página de vendas que usa | `/mini-mentoria` (51 views, 49 únicas) | `/inscricao-47` (196 / 172), `/parceiro-zion` (72 / 68), `/inscricao-dossie` (9 / 9) | `/inscricao` (183 / 133), `/inscricao-curta` (105 / 76); `/inscricao-97` é rascunho sem views | nenhuma |

[EV] para toda a tabela.

### Descrição completa de cada oferta (texto do ClickMax)

- **(a) e (d)** (idênticas): "Formação digital para estruturar um empreendimento turístico no seu terreno. Aulas gravadas, fichas e formulários interativos, e-books por pilar, planilhas de cálculo e kits (Kit do Investidor e kit de prompts, como modelos para você preencher). Metodologia Zion: Marco Zero e sete pilares. Acesso por 12 meses. Pagamento único. Sem acompanhamento individual e sem reunião. Parcerias e investimentos são possibilidades sujeitas à análise da Zion, não garantias. Reembolso em 7 dias."
- **(b) e (c)** (idênticas entre si): "Acesso individual à plataforma Zion Collection de estruturação de projetos de hospedagem. Inclui: Marco Zero; metodologia dos sete pilares (território, mercado, produto, modelo de negócio, masterplan, pré-viabilidade e capital); aulas interativas e vídeos; fichas guiadas e ferramentas; planilhas de orçamento e de viabilidade; construção progressiva do seu Dossiê de Desenvolvimento; e cadastro do seu terreno no banco de áreas da Zion. Acesso por 12 meses. Pagamento único, sem mensalidade. Material educativo: cadastro e análise não garantem investimento, financiamento nem parceria. A Zion avalia cada caso."

Observação [EV]: a descrição de (b) e (c) não diz "sem reunião"; a de (a) e (d) diz. O texto de (a) cita "kits" e "e-books", o de (b)/(c) não.

---

## 2. Turmas e conteúdo entregue

### 2.1 Quais turmas as 4 ofertas entregam [EV]

| Turma | Id | Portal | Conteúdo | Aulas | Membros | Entregue por |
|---|---|---|---|---|---|---|
| **NOVA** "Plataforma de estruturação (R$ 97)" (o nome ainda diz R$ 97) | `087479a3-9d6f-4e1f-a542-c47b347bf5ed` | Plataforma Zion Collection `3ef7a340…` (subdomínio `zion-plataforma`, publicado 24/11) | `79d3e792…` | 70 | 4 | a, b, c, d |
| **ANTIGA** "Zion Collection Club · Plataforma (R$ 97)" | `69345987-7679-41e5-8e66-27281afa6892` | Zion Collection `a8e2157a…` (subdomínio `zion-collection`) | **o mesmo `79d3e792…`** | 70 | 4 | b, c, d (não a) |

Nenhuma das 4 ofertas entrega outra turma. Existem outras turmas no portal antigo que **não** são entregues por estas ofertas: "Inscrição de terreno ou projeto (R$ 270)" `a6db275c…` (2 conteúdos, 91 aulas, 1 membro), 3 e-books de terreno (2 aulas cada), "Seu Airbnb Está Vazio?" (6 aulas) e "Calendário comercial" (2 aulas).

Detalhes de configuração (iguais nas duas turmas, pois o conteúdo é o mesmo) [EV]: acesso 12 meses (`accessDuration` 12, `month`); sem certificado (`issueCertificate` false); sem prévia grátis; comentários habilitados; sem data ou dias de liberação (liberação imediata); conteúdo `enabled` true, `availableForSale` false; `checkoutType` nulo.

Diferenças só de portal [EV]: nome do portal ("Zion Collection" × "Plataforma Zion Collection"), subdomínio, imagem de login. Tema escuro e cor `#C9B37E`, `firstAccessWithoutPass` true, suporte `[link de WhatsApp de suporte omitido]` e rodapé são iguais. Nenhum dos dois tem e-mail de suporte no portal.

### 2.2 Módulo a módulo e aula a aula (turma NOVA = turma ANTIGA) [EV]

Tipos no ClickMax: 26 `video`, 11 `document` (PDF/xlsx), 33 `external_link` (páginas interativas, fichas, formulários). **Todas as 70 aulas estão habilitadas** (nenhuma desabilitada). Mapeamento do tipo de material feito pelo auditor a partir do título e da extensão do link.

**M1 · Comece aqui · Onboarding (3)**
1. Bem-vindo à plataforma Zion Collection · vídeo (mp4)
2. Monte o seu dossiê inicial · formulário/página interativa (`/dossie/`)
3. Suporte · Tire suas dúvidas aqui · link para chat do ClickMax

**M2 · Marco Zero · A visão de toda a jornada (10)**
1. Comece aqui · Como usar o curso · PDF
2. Mapa de direcionamento · as tarefas e os próximos passos da Trilha inteira · página interativa
3. Aula interativa · Marco Zero · página interativa
4. Vídeo 1 · Bloco 1 · A visão, quem somos e o setor · vídeo (YouTube)
5. Vídeo 2 · Bloco 2 · As dores, a jornada e o seu diagnóstico · vídeo (YouTube)
6. Faça agora · O seu diagnóstico prévio · ficha interativa
7. E-book · Transforme Seu Terreno em Destino Turístico, Vol. 1 · PDF
8. Tutorial em vídeo · Como preencher a Ficha do Marco Zero · vídeo (mp4)
9. Kit de prompts do Dossiê · kit (página com prompts para ChatGPT/Claude)
10. Ficha do seu terreno: dados, fotos e documentos · formulário (Airtable)

**M3 · Pilar 1 · Território e destino (8)** · Aula interativa; Vídeo 3 (Bloco 1, o destino e a chegada); Vídeo 4 (Bloco 2, o chão, a área e os papéis); Faça agora · Ficha do Território (ficha); E-book Pilar 1 (PDF); Aprofundamento · E-book completo: Território e Localização (e-book em página); Aprofundamento · Aula de 40 slides (apresentação); Tutorial em vídeo da ficha (mp4).

**M4 · Pilar 2 · Mercado e demanda (8)** · mesma estrutura: Aula interativa; Vídeos 5 e 6 (comparáveis, diária e ocupação; curva do ano, quem paga e quantas cabem); Ficha do Mercado; E-book Pilar 2 (PDF); Aprofundamento e-book "Mercado e Demanda"; Aprofundamento 40 slides; Tutorial mp4.

**M5 · Pilar 3 · Produto e tipologias (8)** · Aula interativa; Vídeos 7 e 8 (nicho, para quem, momento; estadia, promessa, unidade); Ficha do Produto; E-book Pilar 3 (PDF); Aprofundamento e-book "Produto de Hospedagem e Diversificação"; Aprofundamento 40 slides; Tutorial mp4.

**M6 · Pilar 4 · Modelo de negócio (9)** · Aula interativa; Vídeos 9 e 10 (modelo de renda; modelo de venda); Extra · O mapa dos modelos (vídeo YouTube); Ficha do Modelo de Negócio; E-book Pilar 4 (PDF); Aprofundamento e-book "Modelos de Negócio e Monetização"; Aprofundamento 40 slides; Tutorial mp4.

**M7 · Pilar 5 · Masterplan faseado (8)** · Aula interativa; Vídeos 11 e 12 (masterplan, onde nunca; o que cabe, o que se vende e a fase um); Ficha do Masterplan faseado; E-book Pilar 5 (PDF); Aprofundamento e-book "Conceito, Posicionamento e Masterplan"; Aprofundamento 40 slides; Tutorial mp4.

**M8 · Pilar 6 · Pré-viabilidade (8)** · Aula interativa; Vídeos 13 e 14 (quanto custa o projeto inteiro; a conta, os três cenários e o tempo de volta); Ficha da Pré-viabilidade; E-book Pilar 6 (PDF); **Planilha 1 · Orçamento de Abertura (xlsx, versão EM BRANCO)**; **Planilha de pré-viabilidade, Estudo de Massas (xlsx, EM BRANCO)**; Tutorial mp4.

**M9 · Pilar 7 · Capital e Dossiê (8)** · Aula interativa; Vídeos 15 e 16 (de onde vem o capital; o Dossiê e a decisão); Ficha "O seu Dossiê de Desenvolvimento" (gera o PDF do dossiê); E-book Pilar 7 (PDF); **Kit do Investidor** (modelos: teaser, one-pager, pitch, masterplan de viabilidade, plano conceitual e marca); **Cadastre o seu terreno no banco de áreas da Zion** (formulário Airtable); Tutorial mp4.

Totais [EV]: 18 vídeos YouTube/mp4 de pilar e extras + tutoriais (26 aulas do tipo vídeo), 9 e-books/PDFs de pilar e Marco Zero, 2 planilhas, 8 fichas "Faça agora", 7 aulas interativas por pilar, 5 aprofundamentos em e-book e 5 em slides, 2 formulários Airtable, 1 kit de prompts, 1 kit do investidor.

### 2.3 Tabela "só na antiga / só na nova / nas duas" [EV]

| Item | Só na ANTIGA (`69345987`) | Só na NOVA (`087479a3`) | Nas duas |
|---|---|---|---|
| Módulos (9) e aulas (70), todas habilitadas | nenhum | nenhum | **todos** (mesmo conteúdo `79d3e792`) |
| Planilhas EM BRANCO, Kit do Investidor, kit de prompts, e-books, fichas, formulários Airtable, suporte por chat | nenhum | nenhum | todos |
| Portal / endereço | `zion-collection.clickmax.space`; portal compartilhado com outras turmas (R$ 270, e-books, Airbnb Vazio) | `zion-plataforma.clickmax.space`; portal só desta turma (1 turma, 1 conteúdo) | tema, suporte WhatsApp, 12 meses |
| Imagem de login | `assets/store/hero.webp` | `banner-portal.jpg` | demais imagens |
| Quem entrega | ofertas b, c, d | ofertas a, b, c, d | |
| Nome da turma | menciona "R$ 97" | menciona "R$ 97" | |
| Membros | 4 | 4 | |
| Produto ligado à turma | `072083e8` | `072083e8` e `cbbb5fb1` (Mini Mentoria) | |

Em resumo: **o conteúdo não difere; o que diferencia as turmas é o portal.**

---

## 3. Materiais, ferramentas e benefícios: o que está dentro e o que está fora das turmas

### 3.1 Dentro da turma (entregue por R$ 47 e por R$ 97) [EV]
8 fichas interativas (diagnóstico prévio, Território, Mercado, Produto, Modelo de Negócio, Masterplan faseado, Pré-viabilidade, Dossiê), 7 aulas interativas por pilar, 16 vídeos de pilar mais extra, 9 vídeos mp4 (boas-vindas e 8 tutoriais), e-books por pilar em PDF, aprofundamentos (e-book e 40 slides) dos pilares 1 a 5, 2 planilhas EM BRANCO, Kit do Investidor (modelos para preencher), Kit de prompts do Dossiê, Dossiê por pilar com PDF final (jsPDF), formulário do terreno (Airtable) e cadastro no banco de áreas (Airtable).

### 3.2 Fora de qualquer turma entregue por estas 4 ofertas [EV]
- **Os 11 simuladores bônus** ("Bônus · Ferramentas Zion Collection Club": Raio-X do Potencial Turístico; Comparador de Modelos de Hospedagem; Construtor de Projeto Turístico; Calculadora de Implantação Turística; Simulador de Viabilidade Econômica (ROI e payback); Simulador de Viabilidade Zion; Planejador de Implantação Progressiva; Mapa de Alternativas de Capital; Simulador de Sociedade e Parcerias; Zion Investor Ready; Criador de Pitch e Dossiê Turístico). Estão só no conteúdo `fa9a6c54…` da turma de R$ 270. As 11 aulas estão habilitadas lá, mas **nem R$ 47 nem R$ 97 as entregam**.
- Versões "EXEMPLO" das planilhas: existem no repositório, sem aula ligada (INVENTARIO, [EV] do arquivo; não reaberto agora).
- E-books complementares (Terreno ao Airbnb etc.): turmas próprias, outros produtos.

### 3.3 Benefícios prometidos × existência
| Benefício | Existe? | Evidência |
|---|---|---|
| Suporte | Sim, de forma limitada: link de chat do ClickMax (aula M1-3) e WhatsApp no portal e nas páginas. Sem SLA nem e-mail de suporte no portal | [EV] |
| Comunidade | **Não** na turma. Comentários nas aulas estão habilitados, mas não há comunidade/grupo ligado às ofertas | [EV] (comentários); [HIP] sobre ausência de grupo fora do ClickMax |
| Certificado | **Não** (`issueCertificate` false) | [EV] |
| Reunião / atendimento individual | **Não** entregue. R$ 47 (Mini Mentoria) diz expressamente que não inclui | [EV] |
| Cadastro de terreno no banco de áreas | Sim, é um formulário (Airtable) dentro da aula M9-7 e M2-10. Cadastro **não** é avaliação nem garantia | [EV]; processo de avaliação: INVENTARIO diz que não há fluxo definido [EV do arquivo] |
| Gerador de Dossiê | Existe como fichas por pilar que viram páginas e PDF final; não há ferramenta única com esse nome. Etapas de automação de dossiê "completo" do Airtable não implantadas (INVENTARIO) | [EV] aulas; [EV do arquivo] automações |
| Simuladores/calculadoras | Só planilhas e fichas em branco na turma; os simuladores estão fora (3.2) | [EV] |

---

## 4. Diferenças reais entre R$ 47 e R$ 97 (o que o comprador de R$ 97 recebe a mais ou a menos) [EV]

| Dimensão | Comprador R$ 47 (Mini Mentoria `0c71eeba`) | Comprador R$ 47 antiga / R$ 97 / intermediária |
|---|---|---|
| Conteúdo (módulos, aulas, planilhas, kits, fichas) | 70 aulas, 9 módulos | **idêntico** |
| Duração do acesso | 12 meses | idêntico |
| Liberação | imediata | idêntico |
| Suporte, comunidade, certificado, reunião | mesmos (suporte limitado; sem comunidade, certificado ou reunião) | idêntico |
| Simuladores bônus | não | **não** (também fora do R$ 97) |
| Portal de acesso | só o novo (`zion-plataforma`) | **dois**: antigo (`zion-collection`) e novo |
| Descrição da oferta | "sem acompanhamento individual e sem reunião" | sem essa frase; cita "cadastro do seu terreno no banco de áreas" |
| Nome do produto | "Mini Mentoria de Estruturação" | "Zion Collection Club \| Acesso à plataforma" |
| Promessa da página | contida: "possíveis parcerias e investimentos", "Não há acompanhamento individual nem reunião" | `/inscricao` (R$ 97) promete mais (ver seção 5) |
| Preço | R$ 47 | R$ 97 (diferença de R$ 50 sem entrega adicional) |

**Conclusão da seção:** hoje o comprador de R$ 97 não recebe nada a mais em conteúdo; recebe uma segunda porta de acesso ao mesmo conteúdo e uma página de venda com promessa maior (que a entrega não sustenta). O comprador de R$ 47 não recebe nada a menos em conteúdo.

---

## 5. O que cada página de vendas promete × o que a oferta entrega

Convenção: **OK** = há entrega; **SEM ENTREGA** = promessa sem nada que a sustente; **AMBÍGUO** = depende de interpretação. Texto lido nas páginas públicas em 25/11 [EV].

| Página | Oferta / preço | Visitas (únicas) | Promessas em risco |
|---|---|---|---|
| `/mini-mentoria` | a · R$ 47 | 51 (49) | Contida e coerente com a entrega. Pontos de atenção: **nome "Mentoria"** (SEM ENTREGA de mentoria, embora a página negue acompanhamento e reunião); "Dossiê pronto para apresentar a sócios, parceiros ou investidores" (OK como PDF gerado, mas não há validação); "possibilidade de a Zion avaliar uma conversa de parceria" (AMBÍGUO: não há processo ou critério público, INVENTARIO); "Suporte pelo WhatsApp" (OK, limitado) |
| `/inscricao-47` | b · R$ 47 | 196 (172) | **"Receba o suporte da nossa equipe e vamos agendar uma conversa. A nossa equipe entrará em contato com você."** (SEM ENTREGA de conversa/contato ativo); "Seja um parceiro Zion" (SEM ENTREGA); "Queremos te conhecer… nós avaliamos cada caso de forma personalizada" (AMBÍGUO; não há fluxo de avaliação ativo); "Envie o seu dossiê de apresentação à nossa equipe" (sem canal de envio na turma: só o formulário Airtable do terreno) |
| `/parceiro-zion` | b · R$ 47 | 72 (68) | **"Nós podemos ser o seu parceiro"**, "Você não sabe como encontrar um sócio?" (SEM ENTREGA de sócio ou rede); "depois da análise da Zion, existe a possibilidade de avançar para uma conversa de parceria" (AMBÍGUO); jornada "Apresente sua proposta à Zion" (sem canal); "Ferramenta de leitura do terreno" como captura de tela (AMBÍGUO: o quiz "Pilar 01 · Leitura do seu terreno" não está ligado à turma, INVENTARIO); FAQ diz "Não inclui reunião individual" (OK) |
| `/inscricao-dossie` | b · R$ 47 | 9 (9) | **"Suporte da nossa equipe: vamos agendar uma conversa. A nossa equipe entrará em contato com você"** (SEM ENTREGA); "Envie o seu dossiê à equipe" (sem canal); "A Zion está em plena expansão e quer te conhecer" |
| `/inscricao-curta` | c · R$ 97 | 105 (76) | **"tenha acesso a possibilidades de parceria e investimento"**; **"Anexe… e nós entraremos em contato com você"** (SEM ENTREGA de contato); "Seja um parceiro Zion" (SEM ENTREGA); sem FAQ que negue reunião |
| `/inscricao` | c · R$ 97 | 183 (133) | **"Isso abre a oportunidade de você ser nosso parceiro e receber investimentos na sua área"**; **"para conhecermos o potencial do seu terreno"**; "Você constrói. A Zion conhece e avalia" (AMBÍGUO: não há avaliação do potencial entregue); "Abra a possibilidade de ser um parceiro Zion e receber investimentos na sua área" e "A Zion está buscando novos destinos e novos parceiros" (SEM ENTREGA); perguntas de gancho "Qual seria o possível retorno? Quanto poderia faturar?" (parcial: a turma ensina a fazer a conta com premissas do aluno, sem retorno entregue); "Ferramenta de custo de implantação" como captura de tela (AMBÍGUO: a Calculadora de Implantação Turística está só no bônus de R$ 270; na turma há a Planilha 1 Orçamento de Abertura); FAQ afirma "Não inclui reunião individual" e "Não existe garantia de parceria" (OK, mitiga). Inclui bio do fundador com notas de hóspedes: não verificado. |

### Checklist de promessas sem entrega (dirigido) [EV nos textos; entrega pelo ClickMax/INVENTARIO]
| Promessa | Aparece em | Entrega? |
|---|---|---|
| Reunião / "agendar uma conversa" / "entrará em contato" | `/inscricao-47`, `/inscricao-dossie`, `/inscricao-curta` | **Não.** Nada na plataforma entrega reunião; o fluxo de compra R$ 47 está desligado e a Bela é instruída a não oferecer reunião (INVENTARIO) |
| Atendimento individual | nenhuma página promete; a Mini Mentoria nega expressamente | n/a |
| Capital / investimento recebido | `/inscricao` ("receber investimentos na sua área"), `/inscricao-curta` | **Não.** Só ensina a preparar; todas as FAQs ressalvam "não garante" |
| Parceria ("seja um parceiro Zion", "nós podemos ser o seu parceiro") | `/inscricao`, `/inscricao-curta`, `/inscricao-47`, `/parceiro-zion` | **Não** como entregável; só cadastro. Critério e fluxo de avaliação inexistentes (INVENTARIO) |
| Rede de investidores | nenhuma página usa essa expressão literal | n/a (mas "sócios, parceiros ou investidores" e "como encontrar um sócio" sugerem rede, sem entrega) |
| Simuladores / calculadoras fora da turma | `/inscricao` e `/parceiro-zion` mostram telas de ferramentas ("leitura do terreno", "custo de implantação") | Os simuladores existem **só** na turma de R$ 270; na turma entregue há fichas e planilhas. [HIP]: telas podem ser das fichas, a confirmar com Bruno |
| "Login e senha" | **nenhuma das 6 páginas usa essa expressão** (grep confirmado). As páginas dizem "o acesso chega no e-mail da compra". O portal usa primeiro acesso sem senha | OK |
| Avaliação do potencial do terreno | `/inscricao` | **Não** entregue (fichas organizam; não dão nota nem veredito, como a própria `/mini-mentoria` informa) |

---

## 6. Análise: manter dois produtos ou consolidar?

### 6.1 Fatos que pesam [EV]
- Conteúdo, duração e benefícios são idênticos; a diferença de R$ 50 não tem contrapartida entregue.
- Hoje coexistem 4 ofertas, 2 produtos, 2 portais, 2 turmas para 1 conteúdo, 6 páginas de venda ativas (3 oferecem R$ 47, 2 oferecem R$ 97, mais 1 rascunho de R$ 97).
- Base já compradora do R$ 97: 2 clientes reais (24/11), compra recente, dentro dos 7 dias de reembolso até 01/12 [HIP: contado a partir de 24/11, conferir a regra do gateway].
- Sem reembolso ou estorno registrado até agora. Sem venda real de R$ 47 em nenhuma oferta (o único R$ 47 pago é teste de Bruno): eficácia do funil R$ 47 não provada [EV].
- O fluxo de compra aprovada só escuta a oferta de R$ 97 e está desligado (INVENTARIO).

### 6.2 Cenário A · Manter R$ 47 e R$ 97 com diferenciação real

**O que ficaria em cada:**
- **R$ 47 (Mini Mentoria, renomeada):** exatamente a turma atual (70 aulas, fichas, planilhas em branco, kit, dossiê, cadastro de terreno), sem simuladores.
- **R$ 97:** a turma atual **mais** itens que já existem hoje mas não estão na turma: os 11 simuladores bônus, as planilhas versão EXEMPLO. Teria de ser montado como turma própria ou módulo extra.
- Sem reunião em nenhum dos dois, salvo decisão nova de Bruno e capacidade real da equipe [HIP].

**Prós:** preserva o que o comprador de R$ 97 já pagou (passa a ter, de fato, mais); degrau de preço defensável e explicável; aproveita material já pronto.
**Contras / riscos:**
- Exige criar e testar novo acesso e remontar páginas e anúncios; mexe em turma existente (precisa de "aprovado" de Bruno).
- Os simuladores prometem mais do que as regras de CLAUDE.md permitem dizer (sem retorno, sem "potencial"): é preciso conferir cada um antes de vendê-los. Não vi o conteúdo deles [limite].
- A diferença deixa a escolha mais complexa para quem vê a página; risco de dois preços para público frio. [HIP]
- Mantém 2 portais ou exige decidir qual vale para cada um.

### 6.3 Cenário B · Consolidar em R$ 47 (Mini Mentoria) e arquivar o R$ 97

**O que ficaria:** uma única oferta pública (`0c71eeba`) e uma única página (`/mini-mentoria`, a que já tem texto honesto); entrega só no portal novo. Ofertas `668391e7`, `c298aaed` e `74a3f8c6` arquivadas (sem apagar: duas têm vendas). Páginas antigas despublicadas ou redirecionadas. Os 2 clientes reais de R$ 97 **mantêm o acesso** (mesma turma). Remoção da entrega do portal antigo só no painel.

**Prós:**
- Coerência total entre preço, promessa e entrega; elimina a contradição "agendar conversa" × "sem reunião";
- Um único funil para medir (custo por venda), um único portal para suporte;
- Reduz o risco de reembolso por expectativa de parceria/investimento (as páginas de R$ 97 são as mais promissoras);
- Menos itens para manter; alinha-se à decisão de anúncios já ligados à Mini Mentoria (OFERTA.md do repositório).

**Contras / riscos:**
- **Sinalização de preço:** quem pagou R$ 97 pode descobrir que o mesmo conteúdo custa R$ 47. Mitigação a avaliar com Bruno: comunicar com transparência ou oferecer reembolso/ajuste dentro de 7 dias (envio de mensagem a leads exige "aprovado"). [HIP] sobre reação.
- Receita unitária menor (R$ 47 líquido do Pix ≈ R$ 44,51, conforme INVENTARIO, contra R$ 87,73 do R$ 97 pela comissão registrada nas vendas) [EV nos valores; a comparação de resultado é [HIP]].
- Arquivar oferta não é o mesmo que remover acesso: confirmar no ClickMax que arquivar `c298aaed` não corta o acesso dos 2 compradores (não testado; não afirmo) [HIP].
- Nome "Mentoria" precisa ser decidido (pode induzir a expectativa de acompanhamento).

### 6.4 Cenário C · Consolidar em R$ 97 com bônus / rampa

**O que ficaria:** uma oferta única a R$ 97, para a qual se transformariam os bônus reais (simuladores e planilhas exemplo) em módulo da turma; "rampa" = abrir com preço de entrada (por exemplo, R$ 47) e subir após marco definido, sem preço "de" falso nem urgência falsa.

**Prós:** respeita o preço pago pelos 2 compradores reais; maior receita por venda; um só produto.
**Contras / riscos:**
- O conteúdo entregue hoje não justifica R$ 97 sozinho: sem os bônus montados, repete-se o descompasso atual [EV].
- Os bônus ainda não estão na turma; exigem edição de turma, testes e conferência de cada simulador [limite: não vistos].
- "Rampa" é política de preço que precisa ser feita sem urgência ou escassez falsas (regra de CLAUDE.md); a conversão com R$ 97 em tráfego frio não foi medida: não há venda de anúncio nem para R$ 97 nem para R$ 47 [EV: só 2 compras reais de R$ 97, origem não confirmada].
- Maior chance de reembolso se a promessa de parceria/investimento nas páginas atuais permanecer.

### 6.5 Comparativo rápido
| Critério | A | B | C |
|---|---|---|---|
| Coerência promessa × entrega | alta se redigido de novo | **alta, já pronto** | média, depende dos bônus |
| Esforço e risco operacional | alto (2 entregas, turma nova) | **baixo** (arquivar, redirecionar, painel) | médio a alto |
| Respeito à base R$ 97 | alto | médio (precisa comunicação) | alto |
| Risco de reembolso | médio | **menor** | médio |
| Clareza para o visitante | média | **alta** | alta |
| Receita por venda | R$ 47 e R$ 97 | menor | maior |

### 6.6 Recomendação do auditor

**Cenário B, com salvaguardas** [julgamento do auditor, com base nas evidências acima; não é projeção de resultado].

Justificativa:
1. Hoje não há diferença real de entrega entre R$ 47 e R$ 97; manter dois preços para o mesmo conteúdo cria incoerência e risco de reclamação e reembolso, sem benefício que o comprador receba.
2. A página `/mini-mentoria` é a única cuja promessa está inteiramente dentro do que existe (nega reunião e acompanhamento; trata parceria como possibilidade). As demais prometem contato, parceria ou investimento que nada na plataforma sustenta.
3. O Cenário A ou C só se justifica se Bruno decidir montar de fato os bônus (11 simuladores, planilhas exemplo) e conferir o texto de cada um; isso é decisão comercial e trabalho adicional, não correção do que está no ar.

Salvaguardas a decidir com Bruno (nenhuma foi executada):
- Manter o acesso dos 2 clientes de R$ 97 e decidir como comunicar a diferença de preço (transparência; reembolso se pedirem; envio só com "aprovado").
- Antes de arquivar `c298aaed`, confirmar com a documentação do ClickMax que o acesso dos compradores é preservado.
- Despublicar ou redirecionar `/inscricao`, `/inscricao-curta`, `/inscricao-47`, `/parceiro-zion`, `/inscricao-dossie` para `/mini-mentoria`, ou ao menos remover as frases de contato, reunião e "receber investimentos".
- Arquivar a duplicata `74a3f8c6` (zero vendas e zero páginas).
- Remover a entrega do portal antigo nas ofertas que continuarem ativas e renomear as turmas (o nome ainda diz "R$ 97").
- Decidir o nome: "Mentoria" sem acompanhamento promete algo que não existe.
- Pendências técnicas do INVENTARIO para a oferta de R$ 47 (fluxo de compra aprovada, redirecionamento ao obrigado, textos da Bela com R$ 97, rastreamento) continuam abertas.

### 6.7 Limites desta auditoria
- Não abri o conteúdo das aulas, os vídeos, os simuladores, nem os formulários do Airtable.
- Não consultei fluxos, agentes, Meta ou Airtable agora (usei o INVENTARIO como fonte e marquei quando for dele).
- Não afirmo valor de mercado, retorno ou conversão futura. Visitas por página são contagens do ClickMax, sem relação com vendas por página.
- Não há atribuição por página para as 2 compras reais de R$ 97 (UTM vazio nas vendas), então não sei em qual página cada uma decidiu comprar.
