# Auditoria 05 · Produto, curso e área de membros (ClickMax) e como vender a Jornada 1

Data: 13/11/2026 · Só leitura. Nada foi criado, alterado, ativado, arquivado, publicado ou apagado. Sem dados pessoais de alunos (só contagens).
Workspace: `e87e8ba9-37cf-4c54-9a97-3e4e1b01827a`. Fontes: ClickMax ao vivo em 13/11 (portais, turmas, conteúdos, produtos, ofertas, `sellers_status`, `analytics_total_sales`, `member_users_list`, `pages_list`) e o repositório (CLAUDE.md, MAPA, `docs/academy/`, `producao/catalogo/` com as auditorias de 12/11, `producao/jornada2/`, `producao/fabrica/`, `producao/mentoria-desenvolvimento-360/`, `producao/clube/`).

## RESUMO (10 linhas)

1. Há **3 áreas de membros** (portais) e **13 turmas**. A conta tem só **2 usuários-aluno no ClickMax**: o próprio Bruno (matriculado em 14 turmas) e 1 "Aluno Teste Trilha 1". **Nenhum comprador real está no ClickMax** (os contadores dos portais, 12/7/2, divergem disso: não verificado no painel).
2. A Jornada 1 vive no curso "Transforme Seu Terreno…" (`fa9a6c54`): **10 módulos, 63 aulas, todas ativas** (47 de Marco Zero e Pilares + 5 de Comece aqui + 11 de bônus). Não são 58 nem 43. Certificado desligado.
3. A Jornada 2 · Gestão (`f1d16209`) já tem **8 módulos x 4 aulas = 32, todas ativas**, ligada à turma "Jornada 2 · Gestão" (só Bruno). Os documentos antigos dizem "rascunho, desativado, 2 módulos": estão desatualizados.
4. **Nenhuma oferta de Jornada/Club/Land Bank está aprovada.** Trilha 1 (R$ 970, 12x): `incomplete` por `externalId` (gateway Ticto não criou a oferta). Inscrição Club + Land Bank (R$ 270): `incomplete` com erro de sincronização "Token inválido". R$ 97 do clube: arquivada. Kit R$ 97: `pending_corrections`.
5. Vendedor: `sellerStatus` **pending**, banco **approved**, KYC enviado em 06/11, sem motivo de recusa; `canSell` true. Em toda a história do ClickMax há **1 venda (R$ 97, R$ 97 de receita)**; a rota ClickMax nunca foi provada com compra real.
6. Hoje a Jornada se paga **pelo Asaas** (link `sd9u8uluy0urc2ye`, R$ 970): página sem preço → ficha ClickMax → Asaas → webhook (Lovable) aplica a tag e libera a turma `a490c3c8`. **Esse link nunca recebeu um pagamento real**; o acesso ponta a ponta não foi provado.
7. Recomendação: **UMA área de membros**, com turmas por degrau. Manter o portal `6d1b8c4d` (subdomínio `mentoria-zion`), porque a turma `a490c3c8` está ligada ao webhook do Asaas e à oferta; dar nome neutro de Academy. Turma não muda de portal: Land Bank e Zion Collection migram **criando turmas novas** no portal único, só depois de provar o acesso.
8. Como a base real de alunos no ClickMax é zero, **agora é a janela mais barata para consolidar**; depois da primeira venda, qualquer mudança passa a ter aluno pagante.
9. Venda da Jornada 1: manter o caminho Asaas (único montado) para a primeira venda, com teste de pagamento real, e preparar em paralelo a oferta ClickMax limpa (nova oferta, não consertar a velha). O que impede vender hoje: nenhum pagamento de teste, página/ofertas com preço e contagem de aulas conflitantes (R$ 270 x R$ 970; 43 x 63), Zaya ainda vende "R$ 270, 43 aulas".
10. Decisões do Bruno: preço (R$ 970 x R$ 270 x R$ 297), nome (Jornada do Desenvolvimento x Trilha 1 x Jornada 1), o que a compra inclui (reunião, masterclass, Land Bank, prazo), Asaas x ClickMax, nome neutro do portal único.

---

## 1. Definições simples (a cadeia completa)

Pense num prédio de cursos. **Quem paga compra uma oferta; a oferta abre a porta de uma turma; a turma mostra cursos dentro de uma área de membros.**

| Termo | O que é, em uma frase | Exemplo real da conta |
|---|---|---|
| **Produto** | A "etiqueta" do que se vende (nome, tipo, categoria, projeto). Não tem preço. | "Zion Collection 06 · Seu Airbnb Está Vazio?" (`4b088fcf`), projeto Infoprodutos Zion |
| **Oferta** | O preço, as formas de pagamento, o checkout e **o que o comprador recebe (entrega)**. Um produto pode ter várias (ex.: bump). A entrega é presa à oferta, não ao produto. | Oferta R$ 47 (`75c27213`, checkout `QiaIwmZOFC`) e a oferta do bump R$ 19 (`ef27848a`). Entrega = `internal_membership` (portal Zion Collection + turma) |
| **Curso** (no ClickMax, "conteúdo") | O material: módulos e aulas. Vive na conta, não dentro do portal, e **pode ser reaproveitado em várias turmas**. | "Transforme Seu Terreno…" (`fa9a6c54`): 10 módulos, 63 aulas; está em 3 turmas |
| **Módulo / Aula** | Módulo é um capítulo do curso; aula pertence ao módulo (tipos: vídeo, link externo, documento, texto). | Módulo "Pilar 1 · Território e destino" (5 aulas) |
| **Turma** | O grupo de acesso dentro de **um** portal; define **quais cursos** o aluno vê. Não pode mudar de portal. | "Jornada do Desenvolvimento · Trilha 1" (`a490c3c8`) = curso Terreno + Biblioteca (99 aulas) |
| **Área de membros (portal)** | O "site" de login do aluno, com subdomínio e visual próprios. | "Zion · Jornada do Desenvolvimento" (subdomínio `mentoria-zion`) |
| **Aluno** (usuário-membro) | Pessoa com login; precisa estar no portal e na turma. Comprar não cria aluno sozinho: é a **entrega da oferta** (ou o webhook do Asaas) que cria/matricula. | "Aluno Teste Trilha 1" |

Regras que importam: (1) apagar/trocar a turma ligada à oferta quebra a entrega; (2) curso criado e não ligado a turma fica invisível; (3) "Arquivo · …" é só rótulo de Bruno, o ClickMax não tem arquivo: a turma continua ativa e os alunos dela continuam com acesso; (4) o Asaas não passa pela oferta do ClickMax: quem libera o acesso é o webhook do site (Lovable), que cita a **turma pelo id**.

---

## 2. Inventário das 3 áreas de membros (estado vivo em 13/11)

Alunos reais no ClickMax: `member_users_list` devolve **2** (1 conta do dono, 1 teste), ambos ativos. Os contadores `totalMemberUsers` dos portais (12, 7, 2) e das turmas não batem com isso (podem contar matrículas por turma ou registros removidos): **não verificado**, conferir no painel antes de qualquer mudança.

### 2.1 Portal "Zion · Jornada do Desenvolvimento" (`6d1b8c4d…`, subdomínio `mentoria-zion`, antes "Zion Hospitality Business", renomeado em 12/11)

| Turma | id | Cursos ligados (aulas) | Oferta/produto ligado | Alunos (só contagem) |
|---|---|---|---|---|
| **Jornada do Desenvolvimento · Trilha 1** | `a490c3c8` | Terreno (63) + Biblioteca (36) = 99 | Trilha 1 R$ 970 (incompleta); Combo R$ 890 (arquivada) | Bruno + teste (a listagem da turma diz 3) |
| Jornada 2 · Gestão | `294be538` | Jornada 2 (32) + Bônus Gestão (3) = 35 | Trilha 2 R$ 297 e Combo (**arquivadas**) | 1 (Bruno) |
| Club Zion Collection · Kit de Captação | `8cd230af` | Kit Inicial · Como captar recursos (4) | Kit R$ 97 (`pending_corrections`) | 1 (Bruno) |
| Arquivo · Turma Fundadores (não vender) | `2c33680d` | Terreno + Biblioteca = 99 | nenhum | 1 |
| Arquivo · Turma A · Quero começar (padrão) | `3149fca9` | vazia | Mentoria Trilha A R$ 15.900 (arquivada) | 1 |
| Arquivo · Trilha 3 · Operação | `0da5717a` | vazia | Trilha 3 R$ 297 e Combo (arquivadas) | 1 |
| Arquivo · Aula Transforme seu terreno · R$ 47 | `92920c1c` | vazia | nenhum | 1 |
| Arquivo · Turma B · Quero crescer | `50304eb7` | vazia | nenhum | 1 |
| Arquivo · Zion Land Society · Membro | `af41e392` | vazia | nenhum | 1 |
| Arquivo · Fundação · Acesso Livre | `d5c94c5e` | vazia | nenhum | 1 |

Configuração: tema escuro, dourado `#C9A84C`, `firstAccessWithoutPass` **false** (os outros dois portais têm true), `footerDescription` ainda diz "Zion Hospitality Business · Academia de Negócios de Hospedagem", sem e-mail de suporte no portal (só `supportUrl` vazio).

**Cursos do portal:**

| Curso | id | Módulos | Aulas ativas / total | Observação |
|---|---|---|---|---|
| **Transforme Seu Terreno… (JORNADA 1)** | `fa9a6c54` | 10 | **63 / 63** | Tipos: 18 vídeo (YouTube), 33 link externo, 12 documento. Liberação "dias após a compra". Certificado off |
| Biblioteca · Material de apoio (e-books Z/D/F) | `6ce56665` | 18 | 36 / 36 | Só link/e-book; único com certificado ligado |
| **Jornada 2 · Gestão** | `f1d16209` | 8 | **32 / 32** | Cada módulo: vídeo, Faça agora, resumo PDF, planilha. `availableForSale=false` |
| Bônus Gestão / Operação / Identidade / Vendas | `a28341aa`, `2036a7b8`, `b449ff2d`, `f3bf41a9` | 1 cada | 3 / 2 / 2 / 3 | Só o de Gestão está em turma |
| Kit Inicial · Como captar recursos | `03378be0` | 1 | 4 / 4 | Turma do Kit |
| Arquivo · Trilhas 2, 3, 4 | `02363489`, `1d07adf7`, `1775d90d` | 7 cada | 0 | Esqueletos vazios, desabilitados; o de Operação é o único esqueleto de Operação |
| Arquivo · Aula gratuita de entrada | `17c64c44` | 3 | **6 ativas / 13** | Curso desabilitado e sem turma; 7 vídeos sem URL desativados |

**Jornada 1, módulo a módulo:** Comece aqui · Onboarding (5) · Marco Zero (7) · Pilar 1 Território (5) · Pilar 2 Mercado (5) · Pilar 3 Produto (5) · Pilar 4 Modelo de negócio (6) · Pilar 5 Masterplan faseado (5) · Pilar 6 Pré-viabilidade (7) · Pilar 7 Capital e Dossiê (7) · Bônus Ferramentas Zion Collection Club (11) = **63**. **Desativadas na Jornada 1: nenhuma.** O número "58" (documentos) era antes do módulo Comece aqui (12/11); o "43" da Zaya e das páginas é anterior. Já se sabia: só 8 de 17 vídeos têm duração cadastrada (auditoria de 12/11; não reconferi), sem prévia grátis.

**Entrega ponta a ponta (pagamento → acesso): NÃO provada.** Elos: oferta Trilha 1 incompleta (não vende no ClickMax); rota Asaas depende de webhook externo (Lovable) que cita a turma `a490c3c8`; o link `sd9u…` nunca recebeu pagamento; o único aluno criado (teste, 28/10) foi criado à mão. Não há comprador real do portal no ClickMax. Pós-compra "entrou na área" (etapa 4 do funil) é manual.

### 2.2 Portal "Zion Land Bank" (`6d7ceb1c…`, subdomínio `zion-land-bank`)

- 1 turma: **Zion Land Bank · Candidatos** (`6d9cd29e`, padrão): Panorama Marco Zero (12 aulas, 10 ativas; 2 e-books do Gamma desativados) + **a mesma Jornada 1 (63)** = 75 aulas. A turma mostra 7 alunos, mas a listagem de alunos só mostra o Bruno nela: não verificado.
- Ofertas ligadas: Inscrição Club + Land Bank R$ 270 (`incomplete`, erro de gateway) e Inscrição no clube R$ 97 (`archived`, **com 1 transação**, checkout `v_4pU5zNYj`, o usado pela landing de 11/11).
- Entrega ponta a ponta: **não funciona hoje no ClickMax** (oferta de R$ 270 sem gateway; R$ 97 arquivada). O que vende é o Asaas (link `zrhq…`, R$ 270, "Land Members + Radar") com webhook; **não verificado**.
- Observação: o Land Bank dá acesso à Jornada 1 inteira, então "Land Bank" e "Jornada 1" já se sobrepõem (ver seção 4).

### 2.3 Portal "Zion Collection" (`a8e2157a…`, subdomínio `zion-collection`)

- 2 turmas: Compradores · Seu Airbnb Está Vazio? (`75cf8dc3`, curso de 6 aulas) e Compradores · Calendário comercial de 30 dias (`ecdb5762`, 2 aulas). Todas as aulas ativas.
- Ofertas: ZC06 R$ 47 e bump R$ 19, **ambas `approved`**, entrega `internal_membership` para as turmas. É o único conjunto de oferta+turma que está completo em ClickMax.
- Entrega ponta a ponta: configurada e com ofertas aprovadas, **mas nenhuma compra real foi feita** (`hasTransaction` false nas duas): não verificado. Público diferente (Airbnb, casas, pousadas): é o produto de entrada da linha Collection.

---

## 3. Produtos e ofertas ligados à Jornada 1

Vendedor (`sellers_status`, 13/11): `sellerStatus` **pending**, `bankAccountStatus` **approved**, KYC enviado 06/11, `reason` vazio, gateway **ticto**, `canSell` true, `profileCompleted` true. Vendas na vida da conta: **1 produto vendido, R$ 97**, nenhuma venda externa registrada.

| Produto (id) | Oferta (id) | Preço | Status | Erro de sincronização | Ligada a | Como se paga HOJE |
|---|---|---|---|---|---|---|
| **Trilha 1 · Desenvolvimento** (`046301c3`) | `6c3bf7b9` (hash `jgtQ3adVWs`) | **R$ 970**, Pix + cartão em até 12x | **incomplete** (`incompleteReason`: `externalId`) | `providerSyncError` vazio, mas **sem `externalId`** (a oferta não foi criada no gateway Ticto) | turma `a490c3c8` | **Asaas**, link `sd9u8uluy0urc2ye` (R$ 970; site fala "até 10x", Bruno fala 12x: conferir) |
| Inscrição no Club Zion Collection + Land Bank (`38722fcf`) | `c627c32e` | **R$ 270** à vista (1x) | incomplete (sem `incompleteReason`) | **"Não autorizado. Token inválido ou ausente."**, `gatewayName` nulo | turma Land Bank `6d9cd29e` | **Asaas**, link `zrhq4rk88iyta3id` (R$ 270, "6x R$ 45") |
| Zion Collection · Inscrição no clube R$ 97 (`1847aa9f`) | `72924971` | R$ 97 | **archived** | nenhum | Land Bank | Foi o único checkout ClickMax com venda (1) |
| Club · Kit de Captação + sessão (`c40895ad`) | `5b89a932` | R$ 97 | **pending_corrections** | nenhum | turma `8cd230af` | Página do kit fora do ar desde 11/11 (decisão de não ter preço); antigo link Asaas `1pbkdxksp3pw15xd` |
| Kit Inicial de Captação R$ 47 (`8ff3f7b3`) | `50fd0b0a` | R$ 47 | approved | nenhum | sem entrega de turma (entrega por link) | ClickMax (checkout `ylYvvUTnVq`), sem venda |
| Trilha 2 · Gestão (`9c499405`), Trilha 3 · Operação (`305a5b3a`), Combo 3 trilhas R$ 890 (`1e6dd03c`) | `7ed5967e`, `5ae65c46`, `cbf1d6d2` | R$ 297 / 297 / 890 | **archived** | "Token inválido" nas três | turmas Gestão, Operação, Terreno | Asaas `62zus3azyzd50jbw` (pacote R$ 890) segundo o Lovable; não vende em ClickMax |
| Mentoria Zion 360° · Trilha A (`50d6c664`) | `800ecfaf` | R$ 15.900 | archived | nenhum | turma Arquivo A | não vende |
| Club Master R$ 980, Club Pro R$ 2.900, "Trilha + Clube R$ 490" | **não existem como oferta no ClickMax** | — | — | — | — | Reunião/Asaas; Master e Pro sem link (não verificado no Asaas) |

Páginas de venda no ClickMax para a Trilha 1 e a Inscrição R$ 270: **nenhuma** (`pages_list` por `offerId` vazio). A página da Jornada é estática: `docs/jornada-desenvolvimento/` (GitHub Pages, **sem preço**), botão → ficha ClickMax `7495df8b` → redireciona em 3 s ao link Asaas `sd9u…`.

Descrição da oferta Trilha 1 ainda diz "Marco Zero e 6 aulas em 3 etapas… Mentoria Zion" (desatualizada) e o nome do produto ainda é "Trilha 1".

**O que impede vender agora:**
- **Rota ClickMax:** oferta sem `externalId` (gateway), vendedor `pending` (as ofertas de ferramentas aprovadas mostram que a aprovação da oferta ocorre, mas nenhuma compra real foi provada), sem página de venda, descrição/nome desatualizados, nada enviado para aprovação.
- **Rota Asaas (única montada):** primeiro pagamento real nunca ocorreu; preço real do link e parcelas não verificados (Asaas é bloqueado aqui); etapa 2 (foi ao pagamento) e 5 (não pagou) manuais; a entrada no funil depende da tag, que dispararia também fluxos antigos de "Comprou Trilha 1" (documentado em `FLUXO_ADESAO_CLUBE.md`).
- **Mensagens conflitantes:** Zaya e páginas antigas dizem R$ 270 e 43 aulas; `/hub` (Lovable) ainda mostra mentoria R$ 2.784 a R$ 12.375; página `docs/raio-x` rotula o link de R$ 270 como "R$ 97" (varredura de 12/11).
- **Pós-compra:** template de boas-vindas (`zion_clube_boas_vindas`) e o fluxo `575dd0b9` estão em rascunho/pendentes de aprovação da Meta.

---

## 4. RECOMENDAÇÃO

### 4.1 Quantas áreas de membros: UMA

Sua expectativa está certa. Razões: o Asaas/webhook, a oferta e as turmas exigem hoje ids de turma específicos; três portais obrigam o aluno a ter três logins para o mesmo ecossistema; o Land Bank já entrega a Jornada 1 inteira (mesmo curso ligado em 3 turmas); e **hoje não há aluno real no ClickMax**, então reorganizar custa quase nada. Depois da primeira venda cada mudança vira risco.

**Manter:** o portal `6d1b8c4d` (subdomínio `mentoria-zion`). É o que já tem a turma ligada ao webhook do Asaas (`a490c3c8`), a Jornada 1, a Jornada 2, os bônus e a capa nova. Só **renomear para um nome neutro de Academy** (proposta, decisão do Bruno; hoje diz "Jornada do Desenvolvimento", que não serve quando a Jornada 2 entrar). Subdomínio não precisa mudar.

**Turma = degrau de acesso** (nomes como proposta):

| Turma (no portal único) | Cursos | Quem entra |
|---|---|---|
| Jornada 1 · Desenvolvimento (a `a490c3c8`, já existente) | Terreno (63) + Biblioteca (36), depois bônus | compra da Jornada 1 |
| Jornada 2 · Gestão (a `294be538`, já existente) | Jornada 2 (32) + Bônus Gestão | compra da Jornada 2 |
| Jornada 3 · Operação (a criar quando houver conteúdo) | Operação (hoje só o esqueleto) | idem |
| Club (Base) | Jornada 1 + o que o Club prometer (masterclass, Land Bank) | adesão ao Club |
| Land Bank · Candidatos | Panorama + Jornada 1 | inscrição (ver abaixo) |
| Zion Collection · Compradores ZC06 e Calendário | ZC06, Calendário | compra R$ 47/R$ 19 |
| Kit de Captação | Kit | compra do kit (se voltar) |
| Revisão (Bruno) | qualquer curso | só Bruno e testes |

**O que fazer com as outras áreas (nada de apagar; sem alunos reais a migrar, mas só com "aprovado"):**
- **Land Bank** e **Zion Collection**: como a turma não muda de portal, a migração é **criar turma nova no portal único**, ligar os mesmos cursos, **adicionar** a entrega às ofertas (`offers_add_membership_delivery` acrescenta, não substitui), testar com compra real e só então desativar o portal antigo. Land Bank antes precisa de mapa dos fluxos/webhooks que citam `6d9cd29e` (não verificado). Zion Collection pode ficar por último, pois é o único conjunto de oferta aprovada.
- **6 turmas "Arquivo" vazias + Fundadores**: manter sem tocar até conferir no painel os "alunos" que os contadores mostram; depois desabilitar. "Fundadores" é o mesmo curso do Terreno por um segundo canal.
- **Cursos "Arquivo · Trilha 2/3/4"** e **Aula gratuita**: ficam como estão (esqueletos). Operação aproveita o esqueleto de Trilha 3 só como referência, conforme `producao/jornada2/AUDITORIA.md`.
- **Ofertas arquivadas** (Trilha 2, 3, Combo, Mentoria A, R$ 97): não excluir; apontam para turmas com membro (Bruno).

### 4.2 Como organizar a Jornada 1 como primeira trilha

Estrutura alvo (curso único, "Jornada 1 · Desenvolvimento"; **renomear o curso é decisão do Bruno**, o id não muda):

1. **Comece aqui** (5): boas-vindas, dossiê inicial, agendar reunião, suporte, e-book Glamping. Corrigir: a aula "Masterclass" do Panorama já passou (não foi copiada) e a duração do vídeo de boas-vindas ficou 0.
2. **Marco Zero** (7).
3. **Pilares 1 a 7** (5, 5, 5, 6, 5, 7, 7) com, em cada pilar: aula interativa, vídeos, "Faça agora", e-book.
4. **Bônus** (11 ferramentas Zion Collection Club): fica dentro da jornada, no fim.
5. **Material de apoio**: a Biblioteca (36) continua como curso à parte na mesma turma, não misturada nos módulos.
6. **Certificado**: ligar (hoje só a Biblioteca tem). Cadastrar duração dos 9 vídeos sem duração e, se Bruno quiser, uma aula de prévia grátis.
7. Para as outras jornadas entrarem **na mesma área**: cada jornada é um curso próprio e uma turma própria; bônus de ferramentas (Gestão, Operação, Identidade, Vendas) viram o último módulo da jornada correspondente (hoje são cursos soltos, 3 sem turma); o curso de Gestão já está pronto, o de Operação ainda não existe.
8. Padrão de nomes: "Jornada N · Nome" para curso e turma; "Arquivo" só em o que for descartado.

### 4.3 Como vender a Jornada 1

**Princípio (decisão de Bruno em 11/11 e 12/11):** sem preço no anúncio nem na página; tudo leva à ficha/reunião; a página sem preço já existe.

| Peça | Hoje | Recomendação |
|---|---|---|
| **Página** | `docs/jornada-desenvolvimento/` (sem preço), ficha ClickMax `7495df8b` | Manter. Quando houver oferta ClickMax, criar página no ClickMax (padrão de `pages_generation_context_get` → `pages_validate_html` → `pages_import_html_draft` com `offerId`) como rascunho |
| **Oferta** | R$ 970 incompleta (`externalId`); R$ 270 com erro | **Criar uma oferta nova e limpa** no produto da Jornada (como foi feito com a Ferramenta 20, que nasceu com gateway e sem erro) em vez de consertar a antiga. Padrão: pagamento único, Pix e cartão, sem boleto, `ZIONACADEMY`, `+55 48 6137-1061`, reembolso 7 dias. Texto novo (63 aulas; sem "6 aulas em 3 etapas", sem "mentoria") |
| **Checkout** | Asaas (único testado) | Etapa 1: seguir no Asaas, fazer **1 pagamento real de teste** e confirmar tag + turma + e-mail de acesso. Etapa 2: ClickMax quando vendedor aprovado e oferta enviada para aprovação (só com `offers_get_incomplete_reason` vazio) |
| **Entrega** | Webhook Asaas → tag `MÉTODO \| COMPROU TRILHA 1` + turma `a490c3c8`; na oferta ClickMax: `internal_membership` (portal + turma) | Na oferta nova, `offers_add_membership_delivery` com portal `6d1b8c4d` e turma `a490c3c8` (mesmos ids do webhook, nada muda para quem já usa) |
| **Pós-compra** | Fluxo `575dd0b9` (rascunho), boas-vindas pendente na Meta, funil de adesão com etapas 2, 4 e 5 manuais | Ligar (com "aprovado"): tag de compra → cartão etapa 3 → boas-vindas → e-mail de acesso do portal → **primeira aula "Comece aqui"** → agendar reunião |
| **Fluxos** | `c5092264` (carrinho), `11e8b263` (Pix pendente), `5a8e7d04`/`de4a391a` (formulário sem compra) | Os de **Pix/carrinho** só disparam em checkout ClickMax (inferência): não cobrem pagamento Asaas. Para o Asaas, a recuperação é o funil "Preencheu a ficha / Foi ao pagamento / Não pagou" (manual) |
| **Zaya** | Diz "R$ 270, 43 aulas" | Alinhar texto (só com "aprovado") antes de anunciar |

**O que depende de decisão do Bruno:** (1) **preço**: R$ 970 (link Asaas, oferta ClickMax) x R$ 270 (Club Base, Zaya, páginas antigas) x R$ 297 (Trilha 1 antiga) x "R$ 270 por jornada" (comando); (2) **nome** do produto: Jornada do Desenvolvimento, Trilha 1 ou Jornada 1; (3) **o que inclui**: reunião de diagnóstico, masterclass, Land Bank, Club, prazo de acesso (12 meses ou vitalício; a liberação hoje é "dias após a compra"); (4) **Asaas x ClickMax** como checkout principal; (5) **nome neutro do portal único**; (6) número oficial de aulas (63); (7) Land Bank continua produto/inscrição separada ou vira benefício; (8) certificado sim/não.

---

## 5. Riscos antes de mexer e ordem segura

### Riscos
1. **Webhook do Asaas (Lovable) cita a turma `a490c3c8` e as tags por id.** Excluir, recriar ou "trocar de portal" essa turma quebra o acesso do próximo pagante sem aviso. Renomear não quebra.
2. **Base real no ClickMax é zero, mas há compradores por fora** (Asaas, modelos antigos R$ 97 e R$ 270, poucos por tag). A lista deles precisa vir do Bruno: não se sabe se têm login. Antes de desabilitar turma/portal: conferir no painel os contadores 12/7/2.
3. **Turma não muda de portal.** Consolidar portais significa turmas novas + religar entregas das ofertas (as entregas somam, nunca substituem) + re-matricular + reenviar link de acesso. Quem tiver acesso hoje precisa continuar tendo.
4. **Ofertas arquivadas ainda apontam para turmas** (Trilha 2/Combo → Gestão, Operação, Terreno). Não vendem, mas o acesso existente continua; não apagar turma/curso ligado.
5. **Mesmo curso em 3 turmas** (Terreno em Jornada 1, Fundadores, Land Bank): editar o curso altera os três. Bom para correção única, perigoso para experimento.
6. **Alterar oferta aprovada ou com transação** reabre aprovação (`pending_corrections`; já aconteceu com o kit R$ 97 ao trocar preço). A oferta R$ 97 arquivada tem 1 transação: não excluir.
7. **Fluxos antigos de "Comprou Trilha 1"** (boas-vindas) disparam junto com a tag nova; testar com contato de teste antes de anunciar.
8. **Gateway:** ofertas criadas antes de 10/11 têm erro de sincronização ("Token inválido"); consertar a velha pode não resolver, criar nova resolveu para a 20. Ticto é o gateway; o `sellerStatus` ainda é pending.
9. **Zaya e páginas** vendem preço/aulas antigos: risco de promessa diferente da entrega (CDC).
10. **Aulas externas** (YouTube, Gamma, Airtable, wa.me) não foram checadas pelo proxy (auditoria de 12/11): não verificado se todas abrem para o aluno.

### Ordem segura (cada passo com "aprovado" do Bruno quando mexe no que existe)
0. Conferir no painel quem são os alunos reais (contadores 12/7/2) e obter do Bruno a lista de pagantes do Asaas.
1. Decidir preço, nome, o que inclui e Asaas x ClickMax (seção 4.3).
2. **Teste de pagamento real de baixo valor** pelo Asaas com e-mail de teste: confirmar tag, turma `a490c3c8`, e-mail de acesso, login no portal e abertura da 1ª aula. Só aí anunciar.
3. Corrigir textos sem mexer em estrutura: descrição da oferta, nome do produto/curso, rodapé do portal, Zaya (com "aprovado"), preços divergentes das páginas.
4. Nome neutro do portal (renomear não muda ids); ligar certificado; cadastrar durações.
5. Criar a oferta nova da Jornada 1 (com gateway), ligar a entrega à turma `a490c3c8`, enviar para aprovação (com `offers_get_incomplete_reason` vazio), página ClickMax em rascunho, publicar só com oferta ativa.
6. Ligar pós-compra (tag → etapa 3 → boas-vindas → acesso), com os templates aprovados pela Meta.
7. Só então consolidar: criar turma Land Bank e turma Zion Collection no portal único, religar entregas, testar com compra real, desabilitar portais antigos (nunca excluir).
8. Por último: desabilitar turmas "Arquivo" vazias e Fundadores, depois de confirmar alunos.

## Limites do levantamento
- Asaas, Lovable (webhook) e Hotmart não são acessíveis aqui: preço real dos links, parcelas e o webhook são **não verificados**.
- `portal_members_list` voltou erro 500 do ClickMax; contagens de alunos vêm de `member_users_list` e dos contadores das turmas (que divergem entre si).
- Não verifiquei nesta sessão: durações dos vídeos (só o dado de 12/11), URLs de aulas, texto exato da Zaya, fluxos que citam as turmas.
- Nenhuma ferramenta de escrita foi chamada.
