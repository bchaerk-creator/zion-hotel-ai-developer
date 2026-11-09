# Mapa das sessões do Claude Code · Zion Hotel Group

Atualizado em 09/11/2026. Inventário feito só por leitura dos registros de cada sessão e do repositório.

**Regra para toda sessão nova:** antes de produzir qualquer coisa, procure aqui se o tema já existe. Ao terminar uma entrega, acrescente uma linha neste mapa (sessão, o que fez, onde está).

Este repositório é público. O mapa não traz dados de leads, números de campanha nem detalhes financeiros privados. IDs de ClickMax ficam no `CLAUDE.md` e nos `OFERTA.md`.

**Onde as coisas estão:**
- **`main`:** o que está em uso.
- **Branches `claude/*`:** trabalho de cada sessão, nem sempre levado para a `main`.
- **Sessões de agosto e setembro:** usaram o repositório pelo nome antigo `manus-github-test` (renomeado para `zion-hotel-ai-developer`, a confirmar). **Várias branches daquela época não existem mais no remoto.**

---

## 1. Fonte da verdade por tema

| Tema | Onde está a versão atual | Sessão dona |
|---|---|---|
| Regras do repositório, marca, ClickMax, moldes | `CLAUDE.md` (main) | — |
| **ZAIOS** (plataforma no Lovable, zaios.lovable.app) | `docs/zaios/` (decisões, premissas financeiras, roteiro de teste, passagem) | ZAIOS platform development |
| **Premissas financeiras** (fator, deduções 17%, quebra 1%, reserva 3%, múltiplo 6×, regra de decisão) | `docs/zaios/PREMISSAS_FINANCEIRAS_E_VERIFICACOES.md` | ZAIOS platform development |
| **Parecer de homologação matemática condicionada** (Comando 05D; para revisão do Bruno, nada homologado em definitivo) | `docs/academy/comando-05d/` | ZAIOS platform development |
| **Testes financeiros automatizados** (T1 a T12, Comando 05C; somente preparação, nada homologado) | `testes/financeiro/` (README, run.js, resultados) | ZAIOS platform development |
| **Metodologia financeira única** (dicionário v0.1, auditoria das fórmulas, plano de testes; ZAIOS como referência central, homologação pendente) | `docs/academy/comando-05b/` | ZAIOS platform development |
| **Arquitetura comercial** (decisão de 09/11: C · ecossistema integrado com ofertas independentes; matriz de ofertas, sobreposições, regras de acesso) | `docs/academy/comando-05a/ARQUITETURA_COMERCIAL.md` | ZAIOS platform development |
| **Academy · arquitetura, Tech Stack, plano comercial** | `docs/academy/` (Comando 01 e Comando 04) | ZAIOS platform development |
| **Fábrica educacional** (rotinas e agentes) | `producao/fabrica/FABRICA.md`, `ROTINAS.md`, `.claude/agents/` (9 agentes) | Marketing da Zion install |
| **Método Zion 360°** (52 unidades; 17 e-books Z, D, F) | `docs/escola/`, `escola/`, `producao/fila.json`, skill `zion-learning-design` | Zion Hospitality mentoria produção + produção autônoma |
| **Jornada 1 · Desenvolvimento** (Trilha 1, 58 aulas no ClickMax) | `docs/trilha1/` | várias (Clube) |
| **Jornada 2 · Gestão** (Marco Zero de Gestão e Módulo 2 Finanças prontos) | `producao/jornada2/`, `docs/trilha2/` | Marketing da Zion install |
| **Mentoria de Desenvolvimento Zion 360° (redesenho)** | `producao/mentoria-desenvolvimento-360/INVENTARIO.md`; aguarda o "Blueprint Mestre" | Marketing da Zion install |
| **Ferramentas de R$ 19** (01, 05, 11, 13, 14, 17, 18, 29) | `producao/utilitarios/`, `producao/low-ticket/`, `producao/catalogo/` | Zion infoprodutos catálogo |
| **Mini mentorias Zion Collection Club** (A01–A10, B01–B10, R$ 27) e criativos | `producao/zion-arsenal/` | Zion Arsenal infoprodutos |
| **26 produtos em rascunho no ClickMax** | `producao/CATALOGO_REVISAO.md` | Produtos Zion configuration |
| **Sync Meta → ClickMax** (de hora em hora) | `producao/clube/sync-meta-form/` | Marketing da Zion install |
| **Zaya** (SDR no ClickMax) | Cópia de referência na branch `claude/marketing-skills` | não alterar sem "aprovado" |
| **Land Bank** (jornada, diagnóstico, inscrição) | Branch `claude/land-bank-jornada`; `docs/landbank/` | várias |
| **Rotina diária de mídia e CRM** (Meta, Google, GA4, ClickMax) | Sessão "7 volumes e ebook Zion" (relatórios "Leitura") | 7 volumes e ebook Zion |
| **Reservas Zion Bubble** (Noite Mágica, Google Ads, pixel) | Branch `claude/noite-magica-assets` | Automação de reservas / Funil de reservas |
| **Linha de glamping** (Cocoon, Cabin 28, móveis, fornecedores) | Branch `claude/zion-cocoon-zenith-design-68cw2z`, `projects/zion-glamping-line/` | Zion Cocoon e Glamp Store |
| **Site institucional e Zion Capital** | `docs/` (main); branches `claude/web-bruno-*`, `claude/zion-capital-webpage-*` | Web para Bruno / Zion Capital |

---

## 2. Sessões e o que cada uma produziu

### Em uso agora (novembro)

| Sessão | O que fez | Onde | O que espera do Bruno |
|---|---|---|---|
| **ZAIOS platform development** | ZAIOS no Lovable (jornadas Desenvolvimento e Operação, 396 testes, Dossiê); premissas financeiras; Comando 01 (fábrica) e Comando 04 (reestruturação, Tech Stack, pesquisa jurídica) | `docs/zaios/`, `docs/academy/` | Teste fechado da ZAIOS; decisão comercial (Club x Academy); primeiro experimento |
| **Marketing da Zion install** | Sync Meta → ClickMax; Fábrica Educacional (9 agentes); Jornada 2 · Gestão (Marco Zero e Módulo 2 Finanças, testados, rascunhos desativados no ClickMax); inventário da Mentoria de Desenvolvimento | `producao/jornada2/`, `docs/trilha2/`, `producao/fabrica/`, `producao/mentoria-desenvolvimento-360/` | "Blueprint Mestre"; "aprovado" para a turma de revisão do Módulo 2 |
| **Zion infoprodutos catálogo** | Rodada diária de ferramentas de R$ 19; última: Ferramenta 18 Planner de Manutenção Preventiva (31 testes, 09/11); antes: 05 Orçamento da Cabana | `producao/utilitarios/18-manutencao-preventiva/`, entregas em `docs/p/…/manutencao-18/` | Conta de vendedor ClickMax; decidir 01 e 21 (sobreposição com B05/B10/Land Bank e A07); próxima: 20 Kit de treinamento do primeiro turno |
| **Zion Arsenal infoprodutos** | 20 mini mentorias (no ar no GitHub Pages, 1.196 testes), 19 ofertas e landings em rascunho no ClickMax, tutoriais e vídeos de apresentação, bônus nas 5 trilhas, 190 criativos Meta 4:5 com copies e UTMs. 09/11: classificação e **matriz final da linha B** (diretriz comercial do Bruno, alinhada com a sessão de arquitetura da Academy e o Comando 05A): B03, B05, B06, B07 e B09 candidatos à venda individual; B01, B02, B04, B08 e B10 sem campanha individual, propostos como ferramenta interna ou benefício; comparação B06 x Ferramenta 05; novos nomes para B01, B08 e B10. Só planejamento, nada alterado. Nenhuma campanha criada | `producao/zion-arsenal/` (`MATRIZ_FINAL_LINHA_B.md`, `CLASSIFICACAO_LINHA_B.md`, criativos em `criativos/`, retomada em `RETOMADA.md`) | "Aprovado" na matriz da linha B (destinos, B06 x Ferramenta 05, novos nomes); vendedor aprovado; "ok" para campanhas pausadas da linha A; troca da oferta do A01 |
| **Produtos Zion configuration** | 26 produtos em rascunho no ClickMax; campanha Arsenal 01 pausada | `producao/CATALOGO_REVISAO.md` | Documentos do vendedor ClickMax |
| **7 volumes e ebook Zion** (hub de mídia) | Coleção de e-books e, desde outubro, rotina diária de mídia e CRM | Branch `claude/zion-volumes-ebook-creation-*` (não está no remoto); artifacts | Número de disparo; teto de anúncios; pagamento de contas de anúncio; pixel |
| **Automação de reservas Zion** | Noite Mágica: landing e formulário no ClickMax, pixel próprio, campanha de teste **pausada** | Branch `claude/noite-magica-assets` | Ok para ativar; faturamento do canal site |
| **Zion Cocoon e Glamp Store** | Projetos da linha de glamping e Cabin 28 | `projects/zion-glamping-line/` (branch própria) | Escolher opção A ou B; engenheiro; cotações |

### Anteriores (agosto a outubro)

| Sessão | O que fez | Onde |
|---|---|---|
| Zion Hospitality mentoria produção | Ciclo 1 da escola, Z00 (e-book + 40 slides), skill e 3 agentes, curso no ClickMax | `escola/ciclo-01/`, `docs/escola/z00/` |
| Pilares 02–04, Pilares 05–07, Master Educational Roadmap, Mentoria decks | Estrutura antiga de 7 pilares (60 slides por pilar, e-books, exercícios) | Repositório `manus-github-test`, branches `claude/pilares-*`, `claude/zion-academy`, `claude/mentoria-decks-pilares` |
| Entregáveis da mentoria, ClickMax estrutura da mentoria | Interrompidas, sem entrega | — |
| Funil de reservas Zion | Google Ads ativo (Marca e Floripa), cadência de reativação em rascunho | Branch não está no remoto |
| Estratégia GitHub e Meta | Funil do Land Bank no Lovable + Supabase + HubSpot; regras (a IA nunca origina número financeiro; terrenista e investidor em funis separados) | `docs/land-bank/` (branch não está no remoto) |
| Feedback e mapa do site | Esteira do dossiê (Asaas, Hotmart, Brevo) | Branch não está no remoto |
| ZAIOS CRM Zion Hotel Group | **Outro projeto Lovable "ZAIOS CRM"** (kanban, WhatsApp, copiloto), separado da ZAIOS atual | Lovable (workspace ZION's Lovable) |
| Organizar Land Bank | CRM em Python com Land Bank | `src/crm/` (branch `claude/land-bank-organization-*`) |
| Skill no domgifrhub | Score de 60 destinos do Sul, Lead Score 0–100 | `src/prospects/` (branch própria) |
| Extração HubSpot → ClickMax | Consolidação de leads antigos, fila de ligações | ClickMax (listas e pipeline) |
| Artifact 307781bf | Diagnóstico do WhatsApp no ClickMax (erro da conta WABA na época) | — |
| Zion investor experience, Zion Capital página, Web para Bruno, Site no Figma | Site institucional, edição para investidores, plugin de Figma | Branches `claude/zion-investor-platform-*`, `claude/zion-capital-webpage-*`, `claude/web-bruno-*`, `claude/figma-site-design-*` |
| Modelo de financiamento, Black Finance | Escada de capital e crédito privado (submarca) | Repositório `manus-github-test` |
| Plano de negócio Zion e Ecogrupo | Plano com Ecogrupo e tokenização a partir do banco de áreas | Branch `claude/zion-ecogropo-business-plan-*` |
| Zion editorial carrossel | Sistema de carrossel editorial, edição 01 | Branch `claude/zion-editorial-carrossel-*` |
| Zion cinematographic video editing, Reel, Edição de vídeos | Edição de vídeo (só ambiente local) | — |
| Túnel, Capota da Bubble, Prompts FLO | Projetos de estrutura e prompts | Branches próprias |
| Indique e Ganhe | Afiliado ClickMax no Instagram pessoal; **fora da marca Zion** | Artifact |

Fora do escopo Zion e não mapeadas: rescisão trabalhista, contrato de zeladoria, vídeos Opus, instalação de plugin.

---

## 3. Sobreposições e conflitos a resolver

**Decisão de 09/11/2026 (Bruno):** arquitetura comercial C. Academy é a marca educacional; Club é assinatura com benefícios por plano; ferramentas e mini mentorias são vendidas individualmente; a Mentoria de Desenvolvimento Zion 360° é premium e independente (não entra em plano do Club); ZAIOS é plataforma compartilhada com permissões por produto. Detalhes e pendências em `docs/academy/comando-05a/ARQUITETURA_COMERCIAL.md`. O conflito 8 abaixo passa a ser tratado lá. **Linha B:** diretriz comercial do Bruno (09/11) repassada à sessão Zion Arsenal, que prepara a matriz final; detalhes na seção 4 do mesmo documento.

**Comando 05B (Bruno, 09/11/2026), decisões:** (1) arquitetura C preservada; (2) linha B: venda individual B03, B06, B07, B09; uso interno ou benefício B01, B02, B04, B05, B08, B10, sem campanhas novas e sem retirar acessos; (3) B06 = orçamento do empreendimento completo e F05 = orçamento de uma cabana (R$ 19 a validar), sem duplicar promessa; (4) nomes aprovados: B01 "Sua Terra Está Pronta para Ser Apresentada?", B08 "Simule os Cenários do Seu Projeto Turístico: Custos, Receitas e Prazos", B10 "Como Apresentar o Projeto da Sua Terra com Clareza?" (só para revisão futura); (5) ZAIOS como referência financeira central, sem homologação automática. Auditoria em `docs/academy/comando-05b/`. **Seis decisões metodológicas aprovadas (09/11):** D1 (retorno anual x acumulado), D2-C (reserva de reposição 4% da receita bruta realizada, 3–6%, separada da emergência), D3-A (quebra 1% como custo variável, medido primeiro), D4 (pró-labore x distribuição x caixa), D7-C (saída por 3 métodos, com cenário sem venda), D11-A (Régua Única de 5 critérios, sinal parcial). Dicionário v0.4 em `docs/academy/comando-05b/DICIONARIO_FINANCEIRO.md`; nada implementado.

**Duas frentes em paralelo (Bruno, 09/11/2026), só planejamento:**
1. **Arquitetura comercial.** Zion Arsenal classifica e posiciona a linha B. Produtos Zion configuration fornece os dados, sem mexer nos 26 rascunhos. ZAIOS platform development consolida, verifica sobreposições e prepara as decisões.
2. **Produção pedagógica da Mentoria de Desenvolvimento.** Marketing da Zion install compara o Blueprint aprovado com a Trilha 1: aproveitar, atualizar ou produzir do zero, sem alterar as 58 aulas nem os acessos. Já monta o inventário da Trilha 1; a comparação começa quando o Blueprint chegar.


| # | Conflito | Sessões | Proposta |
|---|---|---|---|
| 1 | **Jornada 2 · Gestão em dois desenhos:** 8 módulos já em produção (Marco Zero e Finanças prontos) x 6 módulos com o Acelerador de Vendas no centro (proposta do Comando 04) | Marketing da Zion install × ZAIOS | Manter o que já está produzido. Encaixar o Acelerador de Vendas (WhatsApp, CRM, venda direta) no módulo "Marketing e vendas" do plano de 8 módulos. Bruno decide |
| 2 | **Reserva:** 3% na ZAIOS x 4% no Módulo 2 de Gestão | idem | Usar a decisão registrada (3%, editável) ou o Bruno muda nos dois lugares |
| 3 | **Agentes duplicados:** a fábrica tem 9 agentes; o Comando 01 propôs só 2 novos | idem | Valem os 9 da fábrica (já estão na main) |
| 4 | **Três "ZAIOS":** ZAIOS atual (zaios.lovable.app), o projeto "ZAIOS CRM" (outubro) e os CRMs em Python (`src/crm`, `src/prospects`) | várias | Confirmar qual é a ZAIOS oficial; os outros viram referência ou são arquivados |
| 5 | **Zion Score** aparece no diagnóstico antigo (/28), no `src/` e em templates; a decisão atual é Zion Score fora da ZAIOS | várias | Não reutilizar o Zion Score sem nova decisão |
| 6 | **Números da Bubble** (diária R$ 1.571 ou R$ 1.568, EBITDA 43,46%, 6 anos) usados em site, carrossel e materiais **sem confirmação registrada do Bruno** | várias | Bruno confirma os números canônicos; até lá, não usar em material novo |
| 7 | **Trilha 1: 43 ou 58 aulas** (Zaya e páginas dizem 43; o ClickMax tem 58 ativas) | Zaya × ClickMax | Bruno decide o número oficial; a Zaya só muda com "aprovado" |
| 8 | **Ofertas que se repetem:** Club Base R$ 270 = Trilha de Desenvolvimento; Club Pro R$ 2.900 = acompanhamento; "Zion Start R$ 970" perto do Club Master R$ 980; linha B do Arsenal perto do Land Bank | várias | Decisão comercial única (Comando 04, opção 1 recomendada) |
| 9 | **Estrutura antiga de 7 pilares** (repositório antigo) x Método 360° de 52 unidades x Jornada 1 atual | educacionais | A Jornada 1 atual e o Método 360° valem; o material antigo é só fonte |
| 10 | **Branches perdidas:** várias branches de agosto e setembro não existem mais no remoto | antigas | Recuperar só se alguém precisar; os artifacts continuam no claude.ai |

---

## 4. Como manter este mapa vivo

1. Toda sessão começa lendo `CLAUDE.md`, este mapa e a "fonte da verdade" do tema.
2. Ao terminar, acrescenta ou atualiza a sua linha e registra decisões no documento do tema (ex.: `docs/zaios/DECISOES.md`).
3. Mensagens entre sessões servem para avisar; o que vale está no repositório.
