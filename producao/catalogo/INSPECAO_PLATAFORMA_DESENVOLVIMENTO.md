---
title: "Inspeção da plataforma de Desenvolvimento no ClickMax"
subtitle: "Somente leitura · Trilha 1, Plataforma de estruturação, Panorama, Biblioteca, formulários, agentes e prompts"
date: "27/11/2026"
---

# Como foi feito

- **ClickMax:** só ferramentas de leitura (`portals_list`, `classrooms_list`, `content_list`, `forms_list`, `forms_analytics`, `ai_agents_list`, `ai_agents_knowledge_list`, `products_get`). **Nada foi criado, alterado, publicado, ativado ou enviado.** Workspace `e87e8ba9…` (Bruno's Workspace).
- **Repositório:** conferimos cada link do site (`bchaerk-creator.github.io/zion-hotel-ai-developer/<x>`) contra `docs/<x>` e testamos os 176 endereços ao vivo (todos responderam 200). Lemos o código das fichas "Faça agora", do `/dossie/`, do `/agendar/` e do Kit de prompts.
- **Dados pessoais:** só contagens. Nenhum nome, e-mail, telefone ou resposta individual entrou neste relatório.
- **Não verificado (e por quê):**
  - vídeos do YouTube (17 aulas): o domínio é bloqueado neste ambiente, então não conferimos se estão públicos, a duração nem o conteúdo;
  - formulários do Airtable (5 aulas): domínio bloqueado;
  - servidor Lovable `zion-dossie-aulas.lovable.app` e endpoint `zionhotelgroup.com/api/public/dossie-landbank`: não chamamos (seria envio de dados);
  - conteúdo dos PDFs das bases de conhecimento da Zaya: o ClickMax não devolve o texto;
  - como o ClickMax conta como "concluída" uma aula de link externo;
  - duração de acesso por turma (12 meses) e a entrega exata por oferta: a leitura mostra o produto ligado à turma, não a regra de prazo.

---

# 1. Resumo em 6 linhas

1. **Funciona, mas não está "ok" para escalar.** Os 176 links do site existem no repositório e abrem; não achamos aula quebrada por link.
2. A **Trilha 1** (10 módulos, 83 aulas, 82 habilitadas) e a cópia **Plataforma de estruturação** (9 módulos, 70 aulas, todas habilitadas) seguem uma ordem lógica: Marco Zero → 7 pilares → Dossiê.
3. **Erros de estrutura:** posições repetidas em 2 módulos da Trilha 1, aula de masterclass com data vencida (5/11), Biblioteca dizendo "todos os volumes liberados" com 15 de 36 aulas desligadas.
4. **Risco de dado e de regra:** 7 fichas enviam nome, e-mail e respostas a um servidor Lovable; 5 aulas mandam documentos para o Airtable; e-books D06, F05 e F06 (jurídico, crédito, sócios) estão abertos sem revisão profissional nem aprovação de Bruno.
5. **Nenhum formulário do ClickMax está ligado a aula** (23 formulários, 13 ativos, 57 respostas): os "Faça agora" são páginas externas que salvam no aparelho, e não há critério de conclusão registrado na plataforma.
6. **O mesmo conteúdo é vendido em vários preços** (R$ 47, R$ 97, R$ 270, R$ 290) e os agentes de IA descrevem o Club de formas diferentes. Isso pede decisão de Bruno.

---

# 2. Inventário

## 2.1 Portais que levam conteúdo de Desenvolvimento

| Portal | Subdomínio | Estado | Turmas | Membros (contagem) |
|---|---|---|---|---|
| Zion · Jornada do Desenvolvimento `6d1b8c4d` | `mentoria-zion` | publicado | 11 (7 "Arquivo") | 14 |
| Zion Collection `a8e2157a` | `zion-collection` | publicado | 7 | 12 |
| Plataforma Zion Collection `3ef7a340` | `zion-plataforma` | publicado em 24/11 | 1 | 6 |
| Zion Land Bank `6d7ceb1c` | `zion-land-bank` | publicado | 1 | 7 |

## 2.2 Turmas que recebem os cursos-alvo

| Turma | Portal | Cursos | Membros | Produto ligado (oferta e estado) |
|---|---|---|---|---|
| Estruturação · Etapa de Viabilidade… `a490c3c8` | Jornada | Trilha 1 + Biblioteca | 4 | Trilha 1 (R$ 970, `incomplete`), Combo 3 trilhas (arquivada), Etapa de Desenvolvimento (R$ 290, `pending_corrections`) |
| Curso · Transforme seu terreno… `4834bc40` | Jornada | Trilha 1 + Biblioteca | 1 | Curso passo a passo (R$ 47, arquivada) |
| Arquivo · Turma Fundadores `2c33680d` | Jornada | Trilha 1 + Biblioteca | 1 | nenhum |
| Zion Land Bank · Candidatos `6d9cd29e` | Land Bank | Panorama + Trilha 1 | 7 | 5 produtos do Club e da Sessão (inclui "Inscrição no clube R$ 97") |
| Zion Collection · Inscrição (R$ 270) `a6db275c` | Zion Collection | Inscrição + Trilha 1 | 1 | 6 produtos (Sessão Zion 360°, Club, Inscrição) |
| Zion Collection Club · Plataforma (R$ 97) `69345987` | Zion Collection | Plataforma de estruturação | 6 | Club · Acesso à plataforma |
| Plataforma de estruturação (R$ 97) `087479a3` | Plataforma | Plataforma de estruturação | 6 | Club · Acesso à plataforma + Mini Mentoria de Estruturação |

O produto **Club · Acesso à plataforma** tem 3 ofertas aprovadas: R$ 97 (principal), "R$ 47" e "Mini Mentoria de Estruturação" (R$ 47). O produto separado **Mini Mentoria** `0c71eeba` está em `pending_corrections`.

## 2.3 Cursos

| Curso | Módulos | Aulas | Habilitadas | Tipos | Aulas sem capa |
|---|---|---|---|---|---|
| Trilha 1 · "Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso" `fa9a6c54` | 10 | 83 | 82 | 45 links, 26 vídeos (17 YouTube, 9 mp4), 12 documentos | 34 |
| Plataforma de estruturação Zion Collection `79d3e792` | 9 | 70 | 70 | 33 links, 26 vídeos, 11 documentos | 22 |
| Panorama do Desenvolvimento Hoteleiro · Marco Zero `03aa8ff9` | 2 | 12 | 8 | 6 links, 3 vídeos, 2 documentos, 1 texto | 6 |
| Biblioteca · Material de apoio (Método Zion 360°) `6ce56665` | 18 | 36 | 21 | 36 links | 36 |
| Inscrição do seu terreno ou projeto `16f37c16` (contexto: tem o Kit de prompts) | 3 | 8 | 8 | 4 links, 2 textos, 2 documentos | 8 |

- Todas as aulas têm descrição. Todos os módulos têm capa e descrição. Nenhum módulo vazio nos cursos-alvo.
- Liberação: tudo "dias após a compra" sem número de dias, ou seja, liberado na hora.
- Certificado: desligado na Trilha 1 e na Plataforma; ligado na Biblioteca.

## 2.4 Trilha 1 por módulo

| Módulo | Aulas | O que tem |
|---|---|---|
| M1 Comece aqui | 5 (1 desligada) | vídeo de boas-vindas "plataforma Zion Collection" (mp4, 8 min 36 s), dossiê inicial (`/dossie/`), agenda (desligada), chat de suporte ClickMax, e-book Glamping |
| M2 Marco Zero | 10 | Comece aqui (PDF), Mapa de direcionamento, aula interativa, 2 vídeos YouTube, Faça agora, e-book, tutorial (1 min 42 s), Kit de prompts, ficha do terreno (Airtable) |
| M3 a M9 Pilares 1 a 7 | 8 cada (Pilar 4: 9) | aula interativa, 2 vídeos YouTube (Pilar 4: +1 extra), Faça agora, e-book do pilar, aprofundamento D01–D05 (e-book + 40 slides; só Pilares 1–5), tutorial mp4 (3 min 26 s a 3 min 52 s). Pilar 6: 2 planilhas. Pilar 7: Kit do Investidor e cadastro no banco de áreas (Airtable) |
| M10 Bônus · Ferramentas Zion Collection Club | 11 | apps `zar-b01…b10` e `zar-a09` (40 telas cada) |

A **Plataforma** é a mesma sequência, sem o M10 Bônus, sem a aula de agenda e sem o e-book Glamping, e com as posições corrigidas.

---

# 3. Problemas encontrados

## 3.1 Quebra ou erro

| Id | Onde | Problema |
|---|---|---|
| E1 | Trilha 1 · M2 `da251ac7` | Duas aulas na posição 2: Mapa de direcionamento `4ae2e705` e Aula interativa `14c192e3`. A ordem exibida fica indefinida. |
| E2 | Trilha 1 · M9 `430dbc2f` | Duas aulas na posição 6: Kit do Investidor `1672d9d9` e Cadastre o seu terreno `2101c3c4`. |
| E3 | Panorama · M2 · aula de texto `b8d87e02` (habilitada) | "Masterclass ao vivo" com data fixa ("quinta-feira, 5 de novembro, às 20h") e Zoom. A data já passou. O texto manda falar "pelo chat de suporte", mas a aula de suporte desse curso (`2e2c325e`) está desligada. |
| E4 | Biblioteca `6ce56665` | A descrição diz "Todos os volumes já estão liberados", mas 15 de 36 aulas estão desligadas: D00 a D05 (12), Z00 (2) e a Aula aberta (1). |
| E5 | Biblioteca · Z01 | A aula "0 · Abertura" está na posição 3, depois do e-book e da aula. |
| E6 | Biblioteca · M18 `bdeaa540` (desligada) | Aponta para uma página de outro projeto (`projeto-de-bruno-25763216.clickmax.space/marco-zero`). Está desligada, então não afeta o aluno hoje. |
| E7 | Panorama · aulas `0328a4ad` e `f21bb4dc` (desligadas) | Apontam para rascunhos no `gamma.app`. Também desligadas. |

**O que está bem:** 0 links do site quebrados (176 de 176 existem em `docs/` e respondem 200), 0 aulas sem descrição, 0 módulos vazios.

## 3.2 Risco de regra ou de dado

| Id | Onde | Problema |
|---|---|---|
| R1 | Fichas "Faça agora" dos Pilares 1 a 7 (`docs/trilha1/aula1…aula3`, `pilar4…pilar7`) | A seção "mentor virtual" envia **nome, e-mail, respostas e cálculos** para `zion-dossie-aulas.lovable.app/api/feedback` quando o aluno toca no botão. A ficha diz "nada é enviado sem você pedir", mas não diz para onde vai. O servidor não foi validado (a ZAIOS também não foi testada com pessoas). O envio geral (`ZION_WEBHOOK_URL`) está vazio desde 25/11. |
| R2 | 5 aulas com Airtable: Trilha 1 `b086c4c3` e `2101c3c4`, Plataforma `e9274de1` e `6a3d7c71`, Inscrição `3918f9b0` | Pedem matrícula, escritura, CAR, fotos e vídeo num formulário de terceiro. O Airtable também aparece no Mapa de direcionamento e no Kit do Investidor. Não conferimos o formulário (domínio bloqueado). A descrição avisa o uso dos dados e diz que não há garantia, o que está certo. |
| R3 | `docs/dossie/` (aula "Monte o seu dossiê inicial", em 3 cursos) | Envia respostas e arquivos (matrícula, fotos, planta) para `www.zionhotelgroup.com/api/public/dossie-landbank`. Há caixa de consentimento obrigatória antes do envio. Não testamos o endpoint. |
| R4 | `docs/agendar/` (Panorama `000e4f90`, habilitada; Trilha 1 `2b6d424c`, desligada) | A página carrega o **pixel da Meta** (`fbq init 903918118859018`) dentro da área de membros. Não achamos aviso de rastreamento. |
| R5 | Biblioteca D06, F05 e F06 (habilitadas) | Jurídico/societário/Land Bank, crédito e garantias, sócios e fundos estão abertos ao aluno. Pela auditoria do ZIP 01, T10 e T13 estão "ausentes como núcleo", dependem de revisão jurídica e de crédito, e **nenhum e-book Z/D/F tem aprovação escrita de Bruno**. |
| R6 | Trilha 1 e Plataforma · "Aprofundamento" dos Pilares 1 a 5 | Apontam para `escola/d01…d05`, que estão **desligados na Biblioteca**. O mesmo e-book não aprovado fica aberto por um caminho e fechado por outro. |
| R7 | Trilha 1 · M1 `7e9c378b` e Inscrição `dc4ef9c9` | E-book Glamping liberado como bônus. Pela auditoria, T18 "só com adaptação", com números de mercado sem fonte e risco de conflito com a Glamping Store. |
| R8 | Ficha do Marco Zero (`docs/trilha1/marco-zero/`) | O PDF do diagnóstico termina com "A Bubble Zion e a condição exclusiva: www.zionhotelgroup.com/store". É oferta comercial dentro do material de aula. |
| R9 | Preços e entregas | O mesmo conteúdo chega por R$ 47 (2 ofertas aprovadas do Club), R$ 97 (Club), R$ 270 (Inscrição/Sessão), R$ 290 (Etapa de Desenvolvimento, `pending_corrections`) e R$ 970 (Trilha 1, `incomplete`). As turmas se chamam "(R$ 97)", mas as ofertas de R$ 47 entregam a mesma turma. Quem compra o Club cai em 2 turmas de 2 portais. A Trilha 1 completa, com os 11 bônus, vai para "Land Bank · Candidatos" (produtos de R$ 97). |
| R10 | Zaya `db450d9a` (ativa, sem canal) | A persona diz que a Zion "está desenvolvendo mais de 23 destinos turísticos". A base diz "mais de 20 anos no mercado internacional e 5 no Brasil" e que o Club inclui "mentoria com a equipe". Isso contradiz a Bela ativa (R$ 97, sem mentoria) e não tem fonte no repositório (regra "sem invenção"). |
| R11 | Bela `a8a076d4` (ativa, WhatsApp) | O suporte citado é `+55 48 98872-9883`, mas o `CLAUDE.md` e os portais usam `+55 48 6137-1061`. Os 7 pilares descritos batem com a Trilha 1. As regras de não promessa estão corretas. |
| R12 | Bela `adf143ae` (rascunho) | Texto antigo: adesão de R$ 270, sessão com Bruno e "11 ferramentas". Não está ativa, mas confunde se for publicada. |
| R13 | Vídeos tutoriais (9 mp4) e vídeo de boas-vindas | Narração sintética, sem licença registrada (pela auditoria do ZIP 01). Não reconferimos a voz aqui. |

## 3.3 Qualidade

| Id | Onde | Problema |
|---|---|---|
| Q1 | Nomes | O mesmo curso aparece como "Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso" (curso), "Trilha 1 · Desenvolvimento · … destino turístico de sucesso" (produto), "Transforme Seu Terreno em Destino Turístico" (e-book), "Jornada do Desenvolvimento" (portal, subdomínio `mentoria-zion`) e "plataforma Zion Collection" (vídeo de boas-vindas, que também abre a Trilha 1 no portal Jornada e no Land Bank). |
| Q2 | Trilha 1 · M10 | A descrição diz "Onze mini mentorias", e o nome traz "Zion Collection Club" num curso vendido em outros contextos. O Bônus 6 fala em "cabana ou Airbnb". A descrição do Marco Zero diz "jornada do curso", mas a Bela evita a palavra "curso". |
| Q3 | Capas | 34 de 83 aulas da Trilha 1 sem capa (tutoriais, aprofundamentos, bônus, Kit de prompts, Airtable), 22 de 70 na Plataforma e 36 de 36 na Biblioteca. A capa da Biblioteca vem de `raw.githubusercontent.com` (funciona, mas foge do padrão). |
| Q4 | Tutoriais prontos e não ligados | `docs/trilha1/videos/tutoriais/` tem tutoriais do Kit do Investidor (3 min 49 s), do Mapa de direcionamento (2 min 15 s) e das Planilhas 1 (3 min 55 s) e 2 (3 min 57 s), mas nenhuma aula aponta para eles. |
| Q5 | Duplicação entre cursos | Marco Zero (e-book e aula interativa) aparece em 4 cursos e o Kit de prompts em 3 (`04c0545a`, `83e4db3a`, `f2421cc7`), sempre com o mesmo link. Não quebra nada, mas multiplica a manutenção. |
| Q6 | Turmas de arquivo | São 7 turmas "Arquivo" no portal Jornada; 6 estão vazias e ligadas a produtos com ofertas arquivadas. Sem risco hoje, mas poluem o painel. |
| Q7 | Panorama | O suporte está desligado e a agenda ligada; no M1 os bônus de rascunho estão desligados. O curso é o "Marco Zero" do Land Bank, com vídeo de boas-vindas próprio (2 min 5 s). |

---

# 4. Formulários e prompts

## 4.1 Formulários e quizzes do ClickMax

- **Total:** 23 (12 formulários e 11 quizzes). **13 ativos**, 10 em rascunho. **57 respostas** no total.
- **Ligados a alguma aula: 0.** Nenhuma aula dos 5 cursos aponta para `api.clickmax.io/forms/...`.
- **Ligados ao Desenvolvimento** (pelo nome ou pelas perguntas):

| Id | Nome | Estado | Respostas | Observação |
|---|---|---|---|---|
| `6f58f46c` | Pilar 01 · Território — Leitura do seu terreno | ativo | 0 (0 visualizações) | É o único "Faça agora" nativo. Pede WhatsApp para dar o resultado, o que é desnecessário numa atividade de aula. Não está em nenhuma aula. |
| `bf175b14` | Club · Pré-diagnóstico da aula Marco Zero | ativo | 3 | Mistura aula e venda: Zion Score, "Bubble Zion", capital disponível, terreno como garantia, valor da área e "investir até R$ 5 mil". Usa "J3/J4", outra arquitetura de jornadas. |
| `68b6a1d2` | Fundação · Marco Zero — Diagnóstico de Partida | rascunho | 0 | Pergunta o capital disponível. |
| `9d72764c` | Aplicação · Turma Fundadores (Trilha 1) | rascunho | 0 | Preço de R$ 2.697 e garantia do terreno. |
| `91f1d150` | Land Bank · Diagnóstico da mentoria | rascunho | 0 | Pede endereço do terreno; texto só no feminino ("sozinha", "disposta"). |
| `7495df8b` | Club · Ficha de adesão (Jornada do Desenvolvimento) | ativo | 11 | Cadastro: nome, e-mail, WhatsApp e local. Proporcional. |
| `75ee0a3a` | Ficha do inscrito (pós-compra R$ 97) | ativo | 1 | Pede o valor estimado da área. |
| `aff270f4` | MM47 · Solicitação da Sessão de Diagnóstico | ativo | 0 | Pede o link do PDF do Dossiê; os consentimentos de marketing são opcionais e separados, o que está certo. |

- **Dados que pedem atenção:** capital disponível, terreno como garantia, valor da área, endereço. Servem para qualificar venda, não para aprender. Pela regra "não coletar dado desnecessário", não devem entrar em formulário de aula.

## 4.2 Fichas "Faça agora" (fora do ClickMax)

- São 8 páginas HTML (`docs/trilha1/marco-zero`, `aula1`, `aula2`, `aula3`, `pilar4`…`pilar7`). Calculam na hora, salvam no aparelho e geram o PDF da página do Dossiê (jsPDF).
- Os Pilares 1 a 7 têm o "mentor virtual" (ver R1).
- Os dados ficam no navegador: se o aluno trocar de aparelho, perde o que fez.

## 4.3 Prompts disponíveis ao aluno

- **Kit de prompts do Dossiê** (`docs/p/adbc67069af26ae0/kit-prompts-dossie/`, com `noindex` e coberto pelo `Disallow: /p/`), ligado em 3 aulas (`04c0545a` Trilha 1, `83e4db3a` Plataforma, `f2421cc7` Inscrição).
- **Nove comandos:** Marco Zero, Território, Mercado, Produto, Modelo de negócio, Masterplan, Pré-viabilidade, Capital e Dossiê, e Fechamento.
- **Pontos bons:**
  - bloco de regras fixo: usar só os arquivos anexados, escrever "A CONFIRMAR" quando faltar dado, não inventar números, não prometer, marcar o texto como "RASCUNHO PARA REVISÃO";
  - aviso de privacidade: cobrir CPF e endereço antes de anexar.
- **Falta:**
  - tutorial em vídeo do Kit;
  - um exemplo preenchido (dados fictícios);
  - um prompt por pilar dentro da própria aula do pilar (hoje fica só no Marco Zero).
- **Agentes de IA:** nenhum atende dentro da área de membros. A Bela (WhatsApp) é vendas e suporte; a Zaya está ativa, mas sem canal. As bases tratam de oferta e objeções, não da metodologia de Desenvolvimento. A única descrição de método nelas são os "7 pilares" e as "4 etapas", que batem com a Trilha 1.

---

# 5. Metodologia: aderência aos 7 pilares e ao padrão pedagógico

## 5.1 Qual lista de 7 pilares a plataforma usa

A Trilha 1 usa: **Território, Mercado, Produto, Modelo de negócio, Masterplan faseado, Pré-viabilidade, Capital e Dossiê**, em 4 etapas (ler o lugar, desenhar o produto, desenhar o terreno, fechar a conta).

É uma **quarta lista**, diferente das três mapeadas no ZIP 01:
- Manual: Território, Mercado, Produto, Estratégia, Capital e Implantação, Operação, Expansão;
- Trilha A: Território, Mercado, Produto, Estratégia, Investimento, Implantação, Lançamento;
- Programa Zion 360°: Zion Score, Dossiê, Viabilidade, Conceito, Master Plan, Estruturação, Investidores.

O quiz `bf175b14` ainda usa "J1–J7" (7 jornadas), e a aula aberta desligada se chama "As 7 jornadas". **Implantação/obra (pilar E) não existe na plataforma.**

## 5.2 Padrão pedagógico, pilar a pilar

Legenda: ✓ tem · parcial · ✗ falta · NV não verificado.

| Elemento do padrão | Marco Zero | P1 Território | P2 Mercado | P3 Produto | P4 Modelo | P5 Masterplan | P6 Pré-viab. | P7 Capital |
|---|---|---|---|---|---|---|---|---|
| Promessa "Aprenda o passo a passo" no módulo | ✗ (só no portal) | ✗ | ✗ | ✗ | parcial (na ficha) | parcial (na ficha) | parcial (na ficha) | parcial (na ficha) |
| Vídeo curto (2–3 min) | NV (YouTube); tutorial de 1 min 42 s ✓ | NV; tutorial de 3 min 36 s | NV; 3 min 38 s | NV; 3 min 39 s | NV; 3 min 26 s | NV; 3 min 38 s | NV; 3 min 44 s | NV; 3 min 52 s |
| Exercício | ✓ aula interativa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Formulário "Faça agora" | ✓ externo | ✓ externo | ✓ externo | ✓ externo | ✓ externo | ✓ externo | ✓ externo | ✓ externo |
| Formulário nativo ligado à aula | ✗ | ✗ (o quiz `6f58f46c` existe, solto) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Calculadora | parcial | ✓ na ficha | ✓ na ficha | ✓ na ficha | ✓ na ficha | ✓ na ficha | ✓ ficha + 2 planilhas | ✓ na ficha |
| Checklist | ✓ Mapa de direcionamento (geral) | parcial | parcial | parcial | parcial | parcial | ✗ na ficha | parcial |
| Entregável | ✓ página 0 do Dossiê | ✓ página 1 | ✓ página 2 | ✓ página 3 | ✓ página 4 | ✓ página 5 | ✓ página 6 | ✓ Dossiê + Kit do Investidor |
| Critério de conclusão observável | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Prompt de IA na aula | ✓ Kit (todos os pilares) | ✗ na aula | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Aprofundamento | ✓ e-book | ✓ D01 | ✓ D02 | ✓ D03 | ✓ D04 | ✓ D05 | ✗ (F01–F03 só na Biblioteca) | ✗ (F05–F06 só na Biblioteca) |

"Critério de conclusão" quer dizer uma frase do tipo "você terminou quando tem o PDF da página N com os campos X, Y e Z", registrada na plataforma. Hoje o PDF existe, mas a plataforma não pede nem registra a entrega.

## 5.3 O que falta, por tema (lacunas do ZIP 01 vistas na plataforma)

| Tema | Na plataforma | Falta |
|---|---|---|
| T10 Jurídico e societário | Só o D06 na Biblioteca, aberto e sem revisão | Módulo revisado por advogado; até lá, avaliar desligar ou marcar "em revisão" |
| T13 Crédito | Só o F05 na Biblioteca, aberto e sem revisão | Módulo com linhas reais, com fonte e data |
| T14 Incorporação | Ausente (só uma menção no Pilar 4, "modelo de venda") | Tudo, com revisão jurídica e de CVM |
| T11 Land Bank | Cadastro por Airtable no Pilar 7 e Panorama do Land Bank | Versão didática; contratos revisados |
| T15 Licenciamento | Pergunta solta nas fichas e no quiz `6f58f46c` | Checklist revisado por profissional, por município |
| T18 Glamping | E-book Glamping liberado como bônus | Revisão e retirada de números sem fonte |
| Pilar E Implantação e obra | Ausente | Módulo próprio depois do Pilar 7 |

---

# 6. Incrementos sugeridos (priorizados)

## 6.1 Rápidos e sem custo (edição no ClickMax, cada um exige o "aprovado" de Bruno, porque mexe no que já existe)

| # | Incremento | Resolve | Material que já existe |
|---|---|---|---|
| 1 | Reordenar M2 e M9 da Trilha 1 com a mesma ordem da Plataforma | E1, E2 | A ordem certa já está na Plataforma `79d3e792` |
| 2 | Atualizar ou desligar a masterclass com data vencida | E3 | — |
| 3 | Corrigir a descrição da Biblioteca e a posição da "0 · Abertura" | E4, E5 | — |
| 4 | Ligar os 4 tutoriais prontos (Kit do Investidor, Mapa, Planilhas 1 e 2) | Q4 | `docs/trilha1/videos/tutoriais/*.mp4` |
| 5 | Padronizar o telefone de suporte nos agentes (Bela) | R11 | `CLAUDE.md` §3 |
| 6 | Tirar a linha da Bubble/loja do PDF do Marco Zero | R8 | `docs/trilha1/marco-zero/index.html` (repositório; não exige mexer no ClickMax) |
| 7 | Avisar na ficha, antes do botão do mentor, quais dados vão e para onde | R1 | Fichas `docs/trilha1/*` (repositório) |
| 8 | Nome único do curso em portal, curso, produto e vídeo | Q1, Q2 | Decisão de nome (seção 7) |
| 9 | Capas das aulas que faltam | Q3 | `producao/utilitarios/build_entrega.py` e `render_capas.js` (molde de capas) |

## 6.2 Dependem de produção

| # | Incremento | Resolve | Material que já existe |
|---|---|---|---|
| 10 | Uma frase de critério de conclusão em cada aula "Faça agora", com um checklist de 3 itens | §5.2 | Mapa de direcionamento (já tem as tarefas por etapa) |
| 11 | Um prompt por pilar dentro da aula do pilar, com um exemplo de dados fictícios | §4.3 | Os 9 prompts do Kit |
| 12 | Formulário nativo "Entreguei a página N" ligado a cada pilar (só e-mail e o link do PDF), para registrar a conclusão | §5.2, persistência | O molde do `aff270f4` (MM47) já pede o link do PDF |
| 13 | Promessa "Aprenda o passo a passo para…" na descrição de cada módulo | §5.2 | As descrições atuais já trazem o entregável |
| 14 | Aprofundamento F01–F03 no Pilar 6 e F06 no Pilar 7, depois de aprovados | §5.2 | `docs/escola/f01…f06` |
| 15 | Módulo de Implantação e obra (pilar E) | §5.3 | Ementa E00–E06 do Método 360°; B06, B09, Ferramenta 05 |
| 16 | Trazer a ficha do terreno do Airtable para o ClickMax ou para a ZAIOS, com aviso de privacidade | R2 | `docs/dossie/` (já tem consentimento) |
| 17 | Vídeos gravados por Bruno ou com voz licenciada | R13 | Roteiros das aulas (`producao/`, ZIP 01) |

## 6.3 Dependem de Bruno ou de revisão profissional

| # | Incremento | Resolve | Material que já existe |
|---|---|---|---|
| 18 | Revisão jurídica do D06 e de crédito do F05/F06 (até lá, desligar ou marcar "em revisão") | R5 | D06, F05, F06, Produto 01, Kit de Captação |
| 19 | Decidir se D01–D05 ficam abertos (Trilha 1) ou fechados (Biblioteca) | R6 | — |
| 20 | Revisar o e-book Glamping (números e conflito com a Glamping Store) | R7 | E-book Glamping (61 p.) |
| 21 | Retirar ou comprovar "23 destinos" e "20 anos no mercado internacional" da Zaya | R10 | — |
| 22 | Decidir sobre o pixel da Meta na página `/agendar/` dentro da área de membros | R4 | — |
| 23 | Licença das vozes sintéticas | R13 | — |

---

# 7. O que só Bruno decide

1. **Lista oficial dos 7 pilares:** manter a da Trilha 1 (Território → Capital e Dossiê) ou adotar outra das três do ZIP 01. Onde entram Implantação e Operação.
2. **Nome único** do curso e do portal: "Trilha 1", "Jornada do Desenvolvimento", "Plataforma Zion Collection", "Mini Mentoria" ou outro. E se "mentoria" segue no subdomínio `mentoria-zion` e no módulo de bônus.
3. **Preço e acesso:** o mesmo conteúdo sai por R$ 47, R$ 97, R$ 270, R$ 290 e R$ 970. Quem fica com a Trilha 1 completa com os 11 bônus (hoje os candidatos do Land Bank têm, e a Plataforma de R$ 47/97 não). O que fazer com as turmas de arquivo.
4. **E-books Z/D/F:** aprovar, revisar ou desligar. Em especial D06 (jurídico), F05 (crédito) e F06 (sócios), que já estão abertos.
5. **Coleta de dados:** manter Airtable e Lovable como destino de documentos e respostas, ou trazer para o ClickMax/ZAIOS. Manter o pixel da Meta na página de agenda.
6. **Reunião ou não:** a Bela ativa diz "sem reunião", mas o Panorama do Land Bank ainda tem a aula de agenda ligada e a masterclass ao vivo. Qual é o formato atual para quem está no Land Bank.
7. **Afirmações sobre a Zion** usadas pela Zaya ("23 destinos", "20 anos internacional, 5 no Brasil"): comprovar ou retirar. E qual dos dois textos sobre o Club vale (com ou sem mentoria).
8. **Formulários de qualificação** que pedem capital, garantia e valor da área: manter só na venda e fora das aulas.
9. **Vídeos:** quem grava e com que voz.

*Relatório somente leitura. Nenhuma alteração foi feita no ClickMax. Nada foi enviado a ninguém.*

---

# 8. Correções aplicadas em 27/11 (com o "aprovado" de Bruno)

| # | O que foi feito | Onde |
|---|---|---|
| 1 | Ordem das aulas corrigida (sem posições repetidas) | Trilha 1 · Marco Zero `da251ac7` e Pilar 7 `430dbc2f`; conferido nos 10 módulos da Trilha 1 e nos 9 da Plataforma |
| 2 | Masterclass com data vencida desligada (não apagada) | Panorama · aula `b8d87e02` |
| 3 | Descrição da Biblioteca corrigida (sem "todos os volumes liberados", com aviso de material educativo) e "0 · Abertura" movida para o início do Z01 | Biblioteca `6ce56665`, módulo `0bcc016b` |
| 4 | 4 tutoriais ligados nos dois cursos, logo depois do material que explicam (Mapa de direcionamento, Planilha 1, Planilha 2, Kit do Investidor); os tutoriais das fichas dos Pilares 6 e 7 passaram para logo depois do "Faça agora" | Trilha 1 e Plataforma: aulas `0a86bd37`, `1dc113cf`, `ad87430b`, `9ea4b91d`, `a96ce642`, `852fb0a7`, `9d016a8e`, `0d6b773f` |
| 6 | Linha "A Bubble Zion e a condição exclusiva" retirada do PDF do diagnóstico | `docs/trilha1/marco-zero/index.html` |
| 7 | Aviso de para onde vão os dados do mentor virtual (servidor na Lovable) e de que a ficha funciona sem enviar | `docs/trilha1/aula1…aula6`, `pilar4…pilar7` |

**Não aplicado:**
- **5 · Telefone da Bela.** A Bela atende no próprio número da Zion Collection (+55 48 6137-1061), mas cita outro número de suporte (+55 48 98872-9883). Trocar exige reescrever à mão o texto inteiro do agente ativo (cerca de 9 mil caracteres), com risco de alterar outras regras. Fica para Bruno confirmar qual número é o de suporte humano; a troca é uma linha.
- **8 e 9** (nome do curso e capas): dependem de decisão e de produção.

**Observado ao aplicar:** a tela de resultado do Marco Zero ainda oferece "mentoria em grupo ou individual com o Bruno" e a Bubble da loja, o que contradiz a oferta atual (sem mentoria). Precisa de decisão de Bruno.
