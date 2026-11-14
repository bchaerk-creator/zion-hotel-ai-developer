# 04 · O site da Zion: Lovable, GitHub Pages, ClickMax e Wix (13/11/2026)

Investigação somente leitura. Nada foi criado, editado, publicado nem enviado (Lovable, ClickMax, Wix, Windsor). O site institucional em `docs/` não foi alterado.

Fontes lidas: Lovable (lista de projetos, conhecimento, 300+ arquivos do projeto principal, histórico de edições), ClickMax (domínios de redirecionamento, projeto, páginas, agentes, webchat), `docs/` do repositório, páginas públicas da Wix, do GitHub Pages e do ClickMax. Os endereços `*.lovable.app` e `zionhotelgroup.com` são bloqueados pelo proxy deste ambiente (403): o estado ao vivo deles vem do diagnóstico que o próprio agente da Lovable gravou em `.lovable/plan.md` (13/11, 01:58 UTC), marcado como "não verificado por mim".

---

## RESUMO (10 linhas)

1. O site da Zion **sempre esteve na Lovable** e continua lá: projeto "Zion Hospitality Platform", criado em 30/07/2026, publicado, editado pela última vez em 13/11 às 01:58 UTC. Ninguém migrou o site para o ClickMax.
2. O que "mudou para ClickMax" é o **endereço**: em 12/11 (02:58 UTC) o domínio `zionhotelgroup.com` foi cadastrado no ClickMax (aba de domínios de links, status "connecting"). O DNS de `www.zionhotelgroup.com` hoje aponta para o ClickMax/Entri, que responde **404 para qualquer caminho, inclusive a Home** (diagnóstico da Lovable em 13/11). O site está intacto, mas o endereço oficial não o serve. Quem fez a conexão não consta nos registros que li.
3. O endereço `lovable.app` redireciona tudo para `www.zionhotelgroup.com`, então hoje nem ele abre o site. Correção mínima (precisa de "aprovado" e do acesso ao DNS): voltar `www` e a raiz para o IP da Lovable e tirar o domínio do ClickMax.
4. Hospedagem hoje: site principal na Lovable (com páginas "espelho" de GitHub Pages dentro dele), GitHub Pages para as landings de anúncio, ClickMax para infoprodutos e funil, **Wix** para o `www.zionbubbleglamping.com` (ao vivo, 200).
5. Não há agente de IA tipo concierge/chat público no site. Há agentes **internos**: Agente Território (só para membros, rota `/app`), redação do dossiê, leitura de região, Mapa do caso (IA em servidor) e um servidor MCP do Land Bank. O "agente dentro do site" que Bruno lembra provavelmente é o projeto **ZION Hospitality Compass** (junho, tem `/api/chat`, **não publicado**).
6. A Zaya (ClickMax, só WhatsApp +55 48 6137-1061) é o único concierge ativo. Não compete em tela, mas **se contradiz com o site**: a Zaya nunca fala de preço nem envia link de pagamento ou Calendly; o site mostra preços, links de pagamento do Asaas e o Calendly.
7. **Dois pixels do Meta** em jogo: `1378530017570073` (Lovable e também o site Wix) e `903918118859018` (nove páginas do GitHub Pages). As páginas do GitHub Pages servidas dentro do site recebem **os dois** pixels. Também há duas agendas (Calendly x ClickMax) e dois projetos de rastreio do ClickMax.
8. Contradições de oferta: o site mostra ao mesmo tempo Club sem preço (venda na reunião), adesão com ficha e pagamento (R$ 970 no Asaas), planos R$ 270/980/2.900 ainda publicados no ClickMax, Mentoria R$ 2.784 a R$ 9.504, Land Members R$ 270 e Diagnóstico R$ 47. Os infoprodutos do ClickMax (R$ 19, 27, 47) não aparecem no site.
9. Textos que violam as regras do CLAUDE.md: "vira renda", "ativo que gera receita e valoriza", "receita projetada e retorno esperado", "~R$ 400 mil por cabana por ano", "maior banco de áreas turísticas do Brasil" e números da Bubble (R$ 1.571, 43,46%, 6 anos) sem confirmação do Bruno (conflito 6 do mapa de sessões).
10. Recomendação: Lovable como vitrine institucional única (endereço oficial restaurado), ClickMax só para funil, pagamento e área de membros em subdomínio próprio, um pixel por finalidade, uma agenda, uma voz (Zaya) e uma oferta única na vitrine.

---

## 1. Mapa de hospedagem

### 1.1 Domínios e endereços

| Endereço | Onde está | Para que serve | Quem alimenta | Estado |
|---|---|---|---|---|
| `www.zionhotelgroup.com` (primário do projeto Lovable) | **DNS apontando para ClickMax/Entri** (`13.248.221.243`, `76.223.74.74`, `entri-domains.clickmax.space`); o esperado para a Lovable é `185.158.133.1` | Deveria ser o endereço oficial do site institucional | Lovable (conteúdo); ClickMax (DNS, desde 12/11) | **404 do ClickMax em todos os caminhos** (relato da Lovable em 13/11 01:58 UTC; não verificado por mim: bloqueio do proxy) |
| `zionhotelgroup.com` (raiz) | Lovable lista como sem registro A; ClickMax lista como domínio "connecting" (criado 12/11 02:58 UTC) | Raiz do mesmo site | idem | Quebrado |
| `www.zionhotel.com` | DNS `72.1.32.104`, TXT ausente (relato da Lovable) | Domínio extra do projeto Lovable | Lovable | Não configurado |
| `zion-hotel-group.lovable.app` | Lovable | Endereço técnico do site | Lovable | Redireciona (302) tudo para `www.zionhotelgroup.com`, logo cai no 404 |
| `id-preview--dd227afd-…lovable.app` | Lovable (prévia) | Prévia de edição, o que a Lovable tem de mais novo | Lovable | Prévia renderiza 200 (relato da Lovable) |
| `https://bchaerk-creator.github.io/zion-hotel-ai-developer/` | **GitHub Pages** (pasta `docs/` desta repositório) | Site institucional estático "Desenvolvemos Destinos", landings de anúncio (`zion-collection`, `parceiro-zion`, `land-members`, `raio-x`, `jornada-desenvolvimento`, `store`, `investidores`, `reuniao`…), entregáveis dos infoprodutos em `p/adbc67069af26ae0/` | Sessões do Claude Code (este repositório) | 200 (verificado, última atualização 13/11 00:46 GMT) |
| `infoprodutos-zion.clickmax.space` | **ClickMax** (projeto "Infoprodutos Zion", `domainCount` 0, 45 páginas, 2 funis, 1 formulário, 8 fluxos) | Páginas de venda dos infoprodutos, páginas "externas" que embrulham o GitHub Pages e o site, checkouts do ClickMax | Sessões do Claude Code via MCP | Raiz responde 404 (esperado: não há página na raiz); páginas existem em caminhos próprios |
| `api.clickmax.io/forms/…`, `api.clickmax.io/tr/…`, `app.clickmax.io/book/projeto-de-bruno-25763216/…` | ClickMax | Formulários de lead, rastreio das páginas, agenda da equipe | ClickMax (Zaya e fluxos) | Em uso pelo site e pelas landings |
| `www.zionbubbleglamping.com` (e raiz, com 301) | **Wix** (site "Zion Bubble Glamping | Hotel Bolha em Florianópolis & Urubici") | Site de reservas das duas operações | Wix (Bruno ou equipe) | 200 ao vivo (verificado). No ClickMax o domínio consta "disconnected" (atualizado 12/11 02:57 UTC, um minuto antes de `zionhotelgroup.com`) |
| `zaios.lovable.app` | Lovable (projeto "Zaios") | Plataforma ZAIOS para associados (login por link no e-mail) | Sessão ZAIOS | Fora do escopo; não verificado ao vivo (bloqueio do proxy) |

Observação sobre o ClickMax: o projeto Infoprodutos Zion tem `domainCount` 0 (nenhum domínio próprio ligado ao projeto). O cadastro de `zionhotelgroup.com` está na lista de **domínios de redirecionamento** do workspace (`redirect_domains_list`), que no ClickMax é pensada para links curtos. Ligar um domínio por esse caminho (Entri) reescreve o DNS do endereço, e é isso que tirou o site do ar no endereço oficial. É uma conclusão pelos registros (datas e DNS); não achei quem executou.

### 1.2 Projetos Lovable (workspace "ZION's Lovable", plano Pro, 21 projetos)

Resumo dos 21, do mais recente editado ao mais antigo (IDs abreviados; completos na Lovable).

| Projeto | ID | Publicado | Última edição | O que é |
|---|---|---|---|---|
| **Zion Hospitality Platform** | `dd227afd` | **Sim (público)** | 13/11/2026 | **O site da Zion** (institucional, Land Bank, Club, Jornada, Store, Academy/livros, Diagnóstico de Viabilidade, Hub). Único projeto que o próprio conhecimento do projeto chama de "único projeto vivo" |
| **Zaios** | `51fa7ea5` | Sim | 10/11 | Plataforma ZAIOS (associados, jornada Desenvolvimento e Operação, dossiê em PDF) |
| Zion Dossie Aulas | `9b225613` | Sim | 29/10 | App de exercícios das aulas ao vivo; endpoint de mentor virtual para ferramentas da Trilha 1 |
| Zion Landing Page | `e2f04e7b` | Não | 19/10 | Landing estática do diagnóstico de terreno |
| Zion Hospitality Ecosystem | `a4665945` | Não | 13/10 | Portais por público (proprietário, operador, desenvolvedor, investidor), seis verticais |
| Zion Ecossistema | `f35ca215` | Não | 09/10 | Versão anterior do hub de seis verticais |
| Zion Land Guide | `b2aa35c7` | Não | 06/10 | Landing de captação do Land Advisor |
| Zaios Pipeline | `21908e6b` | Não | 02/10 | Vazio (sem descrição) |
| Noite Mágica Landing | `733ccb39` | Não | 29/09 | Campanha da **Zion Bubble Glamping** (Urubici e Florianópolis), captura via Brevo e cupom |
| Zion Access Club | `c9cbfded` | Não | 02/09 | Clube privado de hospitalidade (conceito) |
| Airbnb Success Blueprint | `be1cc760` | **Sim** | 30/08 | Landing de e-book Airbnb (checkout Hotmart) |
| Remix of Airbnb Success Blueprint | `7c29b1bc` | **Sim** | 14/08 | Landing de e-book de glamping |
| Zion Map / Zion Score Map / Zion Compass | `43aa967d` / `57ea32e9` / `86ee59b6` | Não | 31/07 | Protótipos de diagnóstico de terreno com Supabase |
| Zion Structure | `ff90cece` | Não | 30/07 | Primeira versão do site institucional (design system e Home) |
| Glamping Ventures | `dc6af3fe` | Não | 30/07 | Landing de e-book |
| Zion Airbnb Guide | `53784b09` | Não | 28/07 | Landing de e-book Airbnb |
| Zion Glamping Club | `3540f1f2` | Não | 25/07 | Clube de noites compartilhadas (conceito antigo; descrição fala em renda potencial) |
| **ZION Hospitality Compass** | `b10a67ce` | Não | 22/06 | **Plataforma com chat de IA** (rotas `/api/chat` e `/chat/$threadId`, atrás de login) |
| Remix of Architect Portfolio Website Template | `059b19fa` | Não | 29/03 | Modelo sem uso |

Quatro projetos estão **publicados e públicos**: o site, a Zaios, o Zion Dossie Aulas e as duas landings de e-book (Airbnb Success Blueprint e o remix). As duas landings de e-book estão **no ar com URLs próprias e fora do controle do site principal**; vendem e-books pelo Hotmart. Conferir se ainda fazem parte da estratégia (não verificado o conteúdo delas).

**Qual é qual:**
- Site da Zion Bubble Glamping: **não está na Lovable**. Está na Wix. A Lovable só tem a campanha "Noite Mágica Landing" (não publicada).
- Land Bank, Zion Collection (Club), Academy e Método: **tudo dentro do projeto `dd227afd`** (rotas `/land-bank`, `/clube`, `/club`, `/hub`, `/academy`, `/metodo-zion`, `/jornada-desenvolvimento`, `/dossie-de-viabilidade`, `/raio-x`, `/inscreva`, `/oportunidades`, `/store`). Várias dessas rotas são "proxy": a Lovable busca a página no GitHub Pages e a serve no endereço oficial (clube, parceiro, land-members, raio-x, store, fundador, cases, investidores, método, reunião, sessão, dossiê, diagnóstico/agendar e resultado).
- ZAIOS: projeto próprio (`51fa7ea5`).

Histórico recente do projeto principal (últimas edições, todas por agente da Lovable): 06/11 menu e redirecionamentos do `/club`; 07/11 vídeo; 11/11 rotas `/clube`, `/parceiro`, `/diagnostico`, robots/sitemap/llms, SEO; 12/11 rota nova e item de menu; 13/11 link da Trilha 1 no Hub, "página nativa da Jornada" e o plano de diagnóstico do domínio.

---

## 2. O que o site diz hoje

Fonte: código do projeto Lovable `dd227afd` (arquivos citados) e, para as páginas espelhadas, `docs/` e o GitHub Pages. Estado ao vivo no endereço oficial: não verificado (domínio fora do ar, ver 1.1).

### 2.1 Menu e destinos (`src/lib/navegacao.ts`, `src/lib/links.ts`)

Menu: Home · Club Zion Collection (`/clube`) · Adesão (`/jornada-desenvolvimento`) · Land Bank (`/land-bank`) · Glamping Store (`/store`) · Sobre nós (`/sobre`) · Investidores (`/oportunidades`).

| Botão | Destino |
|---|---|
| Home: "Fazer inscrição no Club Zion Collection" | `/clube` (espelho de `docs/zion-collection/`; sem preço, leva à agenda da equipe no ClickMax) |
| Home: "Quero aderir ao Club" (faixa de adesão) | `/jornada-desenvolvimento` |
| `/jornada-desenvolvimento`: "Quero aderir ao Club" | Ficha ClickMax `api.clickmax.io/forms/dcSUhl5B…`; depois a ficha leva ao link do Asaas (R$ 970 segundo o repositório; a página **não mostra preço**) |
| Formulário do Club (`CLUB_FORM_URL`) | `api.clickmax.io/forms/IkNsg_hH…` |
| Diagnóstico `/diagnostico` | Formulário ClickMax `…/forms/COT5Zt5-…` (repassa só UTM, `fbclid`, `gclid`) |
| WhatsApp (todas as páginas) | `wa.me/554861371061` (a Zaya) |
| Agenda ("Conversar com a Zion" na Home, oferta do dossiê, `/sessao`, `/consultoria/obrigado`) | **Calendly** `calendly.com/contato-zionglampingcollection/1h` |
| Land Bank R$ 270 | Asaas `…/zrhq4rk88iyta3id` |
| Consultoria prévia R$ 490 | Asaas `…/r053uykadfxvn2wo` |
| Hub / Mentoria | Asaas (planos); planos sem link caem no WhatsApp com mensagem pronta |
| Livros do Método (vol. 1 a 7, glamping, território) | Hotmart `pay.hotmart.com/…` (Airbnb ainda em lista de espera) |
| Investidores | Botão "Em breve" (formulário vazio); página espelhada com cadastro de interesse |
| Entrar (membros) | Oculto (link vazio) |

### 2.2 O que cada seção promete

- **Home (`src/routes/index.tsx`, `HomeInstitucional.tsx`)**: título "Transforme seu terreno em um destino turístico"; "Aprenda o passo a passo para estruturar um empreendimento de hospedagem de excelência e inscreva o seu terreno no ecossistema da Zion". Faixa "20+ anos de hotelaria internacional · Booking 9,6 · Airbnb Superhost 5/5 · Expedia 10". Marca "Zion Collection · o clube de vantagens do ecossistema Zion". Adesão ao Club (7 pilares, aulas interativas, 11 ferramentas de bônus). Mapa do site (Club, Land Bank, Store, Sobre, Investidores). Prova: "Priscila e Rodrigo, dos Chalés Magia do Campeche…" (sem autorização registrada, não verificado). FAQ e rodapé com aviso de que não há promessa de renda.
- **Jornada/Adesão (`jornada-desenvolvimento.tsx`)**: "Transforme o seu terreno em um projeto de hospedagem"; para dono de terreno, quem já hospeda, futuro desenvolvedor; 4 etapas e 7 pilares; aulas, fichas, 11 ferramentas de bônus, e-books; suporte "pela equipe Zaya"; foto real da Bubble com legenda correta; aviso educacional. Sem preço.
- **Club (`/clube`, espelho)**: sem preço; tudo leva à reunião de diagnóstico (decisão de 11/11: sem inscrição de R$ 97, clube vendido na reunião).
- **Land Bank / Diagnóstico de Viabilidade (`dossieOferta.ts`, `OfertaDossie.tsx`)**: Diagnóstico de Viabilidade **R$ 47** (dossiê em PDF e entrada no Banco de Áreas); "Zion Land Members + Radar" **R$ 270 (6x de R$ 45)** com "Leitura do Diagnóstico" de 45 min e kit com plano de ação.
- **Hub (`hubPlans.ts`)**: Mentoria em Grupo R$ 2.784 à vista (12x de R$ 302,09), com Acompanhamento R$ 4.704, Premium R$ 9.504, comparativo e botões ao Asaas ou WhatsApp.
- **Store (`/store`, espelho)**: Bubble Zion, implantação "em até 90 dias", garantias de fabricação, simulador de exemplo.
- **Livros (`checkouts.ts`)**: e-books por Hotmart.
- **Investidores (`/oportunidades`, espelho)**: cadastro de interesse com aviso de não ser oferta de investimento.
- **llms.txt**: afirma que a Zion "não promete renda, retorno, ocupação, crédito, sociedade nem investimento".

### 2.3 Comparação com a oferta vigente do funil

Oferta vigente conforme o repositório (11 e 12/11): Club vendido na **reunião de diagnóstico**, sem preço público; adesão à Jornada do Desenvolvimento por ficha → Asaas (R$ 970, ainda sem nenhum pagamento real recebido); inscrição de R$ 97 **descartada** em 11/11; infoprodutos de R$ 19 a R$ 47 no ClickMax.

| # | Contradição | Onde | Gravidade |
|---|---|---|---|
| C1 | **Duas portas para o mesmo Club**: "Club Zion Collection" (reunião, sem preço) e "Adesão" (ficha e pagamento direto). Mensagens e jornadas diferentes para o mesmo produto | menu, Home | Alta |
| C2 | **Preços antigos ainda publicados no ClickMax**: `/club` e `/club/planos` (Base 6x R$ 45 ou R$ 270, Master R$ 980, Pro R$ 2.900, "43 aulas"), publicados em 06/11, e checkouts de R$ 97 | `infoprodutos-zion.clickmax.space` | Alta |
| C3 | **Land Members R$ 270 e Diagnóstico R$ 47** no site contra a decisão de vender o Club na reunião | `dossieOferta.ts`, `/dossie`, `/consultoria/obrigado`, `/raio-x`, `/metodo` | Alta |
| C4 | **Mentoria R$ 2.784 a R$ 9.504** no Hub contra a "Mentoria de Desenvolvimento 360° premium e independente" em redesenho (aguarda Blueprint) | `/hub`, `hubPlans.ts` | Média |
| C5 | **Zaya x site**: a Zaya nunca informa preço, não envia link de pagamento nem Calendly; o site publica preços, links do Asaas e Calendly, e os botões de WhatsApp levam a ela. Quem clica "Quero entrar na Mentoria Premium" cai numa conversa em que a Zaya não pode falar de valor | `hubPlans.ts`, `HomeInstitucional.tsx`, `dossieOferta.ts` | Alta |
| C6 | **Duas agendas**: Calendly (site) e ClickMax `app.clickmax.io/book/…` (landings e Zaya) | site x GitHub Pages | Média |
| C7 | **Infoprodutos não aparecem no site**: nenhuma menção a Arsenal, ferramentas de R$ 19 ou Zion Collection 06 (R$ 47). Os e-books concorrentes do Hotmart (vol. 1 a 7) aparecem | `checkouts.ts` | Média |
| C8 | **"23 destinos" x "29 destinos"**: conhecimento do projeto e HomeSections dizem 29; Home, llms e FAQ dizem "mais de 23". Um trecho diz "entre Brasil e Europa" | `HomeSections.tsx`, `llms.txt`, `index.tsx` | Média |
| C9 | **Trilha 1: "43 aulas"** nas páginas antigas contra 58 no ClickMax (conflito 7 do mapa) | ClickMax `/club/planos` | Baixa |
| C10 | **Base do conteúdo**: a Home atual não usa `PortasHome`, `EscolaHome` e `RioEcossistemaHome` (exportados, uso fora da Home não verificado) nem `HomeSections` (legado mantido de propósito) | `HomeInstitucional.tsx` | Informativa |

### 2.4 Textos que violam as regras do CLAUDE.md

Regra: sem promessa de renda, reservas, ocupação, investimento ou valorização; sem números inventados ou não confirmados; sem superlativo autodeclarado.

| # | Texto | Onde | Regra violada |
|---|---|---|---|
| V1 | "Aquele pedaço parado **vira renda**. Sem parar a lida." | `HomeSections.tsx` linha 905 (legado) | Promessa de renda |
| V2 | "Viabilidade do ativo: produto, investimento, **receita projetada e retorno esperado**" | `HomeSections.tsx` linha 244 (legado) | Promessa de retorno |
| V3 | "Para quem tem um território e quer transformá-lo em um ativo que **gera receita e valoriza**"; "gera receita operacional e **valoriza como patrimônio**" | `docs/index.html` (GitHub Pages) | Renda e valorização |
| V4 | "Na Zion, a cabana chega perto de **R$ 400 mil por ano**"; "60% de ocupação"; "Faturamento por ano / Resultado operacional por ano" (exercício com R$ 1.571 e 60%) | `docs/store/index.html`, servido em `/store` | Resultado financeiro como atrativo de venda, mesmo com aviso |
| V5 | "R$ 1.571 de diária média, EBITDA 43,46%, 6 anos" | `HomeSections.tsx` (396, 397, 560, 981), `dossie-de-viabilidade.tsx` (296), `investidor.server.ts` (53), `dossieRedacao.server.ts` (31), `docs/index.html` | Números sem confirmação registrada do Bruno (conflito 6 do mapa). A regra de risco da própria Lovable os autoriza, mas o repositório manda não usar em material novo |
| V6 | "Estamos construindo **o maior banco de áreas turísticas do Brasil**" | `HomeInstitucional.tsx` linha 17, `InscrevaPage.tsx` linha 98 | Superlativo sem prova; também contra a regra 11 do conhecimento da Lovable ("sem superlativo autodeclarado") |
| V7 | "Radar do Land Bank, onde a Zion e **investidores olham os terrenos inscritos**" (templates e Club); "Faça parte do nosso pool de investidores" | Home (Investidores), templates da Zaya | Sugere acesso a investidor; as ressalvas existem mas o convite empurra a expectativa |
| V8 | "A Zion avalia **parcerias e apresentações a investidores**" | `docs/store/index.html` | Idem V7, com ressalva |
| V9 | "Booking 9,6 · Airbnb Superhost 5/5 · Expedia 10" | Home, `llms.txt` | Nota de plataforma sem fonte anexada (não verificado) |
| V10 | Depoimento/caso "Priscila e Rodrigo, Chalés Magia do Campeche" | `ProvaHome` | Pede autorização documentada (não verificado) |
| V11 | Descrição do projeto antigo Zion Glamping Club: "7 noites por ano… programa de aluguel para **potencialmente gerar receita**" | Lovable, projeto `3540f1f2` (não publicado) | Promessa de renda (fora do ar; só arquivar) |

Pontos **conformes**: todas as páginas atuais da Home e da Jornada trazem o aviso "Conteúdo educacional, não é promessa de renda, retorno, ocupação, crédito ou sociedade"; promessa de entrada é "Aprenda o passo a passo para…"; as instruções das IAs proíbem renda, retorno, valorização e zoneamento como fato; foto da Jornada tem legenda de operação real.

---

## 3. Agentes de IA dentro do site

### 3.1 O que existe de fato

| Agente / uso de IA | Onde | O que faz | Quem acessa | Ativo? |
|---|---|---|---|---|
| **Agente Território Zion** | `src/lib/hubApp.functions.ts`, rota `/app` (botão "Conversar com o agente sobre este diagnóstico") | Lê o diagnóstico do membro e conversa; regras: sem promessa, sem "viável/inviável", sem inventar leis, termina com frase fixa. Modelo via gateway da Lovable (`openai/gpt-6-astra`) | **Só membros** (`is_hub_member`, login) | Código ativo; depende de a compra liberar o membro. Uso real não verificado |
| Redação do dossiê | `dossieRedacao.server.ts` (gemini-2.5-flash) e `dossieRedacao.validador.ts` | Escreve o texto do Diagnóstico de Viabilidade a partir de números calculados em tabelas; validador reprova promessa e número inventado; passa por revisão | Cliente que pagou o R$ 47; equipe | Ativo no fluxo do dossiê |
| Leitura do território / região / Mapa do caso | `territorio.server.ts`, `regiao.server.ts`, `mapaCaso.server.ts` | Texto e pesquisa qualitativa; "nunca prometa renda…" nas instruções; Mapa do caso grava link no ClickMax | Servidor (pós-pagamento) | Ativo no webhook |
| **Servidor MCP do Land Bank** | `src/lib/mcp`, rotas `/mcp` e `/.mcp/*` | Ferramentas para listar e ler diagnósticos de terreno (contêm dados pessoais de proprietários) | Clientes MCP com login OAuth | Ativo; fonte de risco de privacidade se uma sessão tiver acesso (não verificado quem tem) |
| Marco Zero "agente" | `src/lib/marcoZero/agente.ts`, rotas `/academy/marco-zero-desenvolvimento/agente` | Demonstração **sem IA**, determinística, dados não guardados | Público | Ativo, não é IA |
| ClickMax livechat | `docs/raio-x/index.html` carrega `api.clickmax.io/sdk/livechat.js` (GitHub Pages) | Chat/webchat do ClickMax na página do diagnóstico | Público | Existe um canal webchat "Suporte · Clube Zion Land" **ativo** (10 etapas, pré-chat). Se está ligado ao agente de IA: não (o único agente é a Zaya, canal WhatsApp) |
| **ZION Hospitality Compass** | Projeto Lovable `b10a67ce`, rotas `/api/chat` e `/chat/$threadId` | Plataforma de orientação com chat de IA, atrás de login | Ninguém (não publicado) | **Inativo**. É o candidato mais provável a ser o "agente de IA dentro do site" que Bruno lembra. Conteúdo do conhecimento vazio; não li as regras de conversa do código |

**Não existe** concierge, widget de chat ou assistente de IA aberto ao visitante no site principal. Busca por "chat", "concierge" e "gemini" no código: só o chat do `/app` e o gateway de IA no servidor.

### 3.2 Conhecimento do projeto Lovable

O conhecimento (`get_project_knowledge`) define o site como "único projeto vivo", tom sóbrio e **regras de risco**: IA nunca origina números; zoneamento só como "verificar com a prefeitura"; "checklist documental" em vez de "análise documental" no produto de R$ 97 (o preço atual do dossiê é R$ 47: texto desatualizado); dossiê com revisão humana (o `AGENTS.md` já diz "imediato com revisão posterior": regra trocada sem atualizar o conhecimento); "nenhum número inventado" com a lista de números autorizados (inclui os da Bubble). Duas portas separadas (terrenista e investidor).

### 3.3 Competem com a Zaya?

- **Em canal, não.** A Zaya vive no WhatsApp (+55 48 6137-1061) e é o único agente de IA do ClickMax (ativo, versão 56, 79 conversas, 24 escaladas, objetivo único: agendar reunião de diagnóstico, sem falar de preço). O site não tem chat que dispute o visitante.
- **Em mensagem, sim.** Quatro conflitos: (a) preço (site mostra, Zaya não pode falar); (b) pagamento (site vende por Asaas, Zaya "nunca envia link de pagamento" e escala quem já comprou); (c) agenda (site usa Calendly, Zaya só envia o link do ClickMax e "nunca envie link do Calendly"); (d) o número de WhatsApp aparece como "atendido pela Zaya, SDR com IA" no código e como "equipe Zion" nas páginas.
- **Duas fontes de "voz da Zion"**: o Agente Território (membros) e a Zaya (leads) têm regras próprias de tom (a Zaya: "máximo 2 frases, sem listas"; o Território: "frases curtas, sem travessão") e não compartilham memória.

---

## 4. Conexão com ClickMax e com o Meta

### 4.1 Como o site se liga ao ClickMax

| Ligação | Como | Onde |
|---|---|---|
| Formulários | Botões abrem formulários hospedados no ClickMax (`api.clickmax.io/forms/…`): Club, Jornada/adesão, diagnóstico, parceiro | `links.ts`, `jornada-desenvolvimento.tsx`, `diagnosticoTracking.ts`, `docs/parceiro-zion` |
| UTM | Só o `/diagnostico` repassa `utm_*`, `fbclid`, `gclid` aos formulários. Nos demais botões não verificado | `diagnosticoTracking.ts` |
| Rastreio do ClickMax | Script `api.clickmax.io/sdk/script.js` e imagem `…/tr/<projeto>?ty=page_view` nas landings do GitHub Pages (17 páginas com `tr/projeto-de-bruno-25763216`, 3 com `tr/infoprodutos-zion`) e no `/diagnostico` da Lovable (`tr/projeto-de-bruno-25763216`) | `docs/`, `DiagnosticoPage.tsx` |
| Páginas "externas" no ClickMax | Páginas do tipo externo embrulham `www.zionhotelgroup.com/clube`, `/parceiro` e o GitHub Pages dentro do ClickMax (para medir e ligar ao funil). **Dependem do endereço oficial**, hoje fora do ar | ClickMax: "Clube · Landing (zionhotelgroup.com/clube)", "Parceiro · Landing (…/parceiro)" |
| Captura de lead pelo servidor | Raio-X, dossiê e Mapa do caso gravam contato e campo no ClickMax pelo "link de captura" oficial (`api.clickmax.io/ingest/{id}`); segredo `CLICKMAX_CAPTURE_LINK_URL` (e `CLICKMAX_DOSSIE_CAPTURE_URL` ainda pendente por decisão do fundador) | `clickmaxCaptura.server.ts`, `clickmaxDossie.server.ts`, `mapaCasoClickmax.server.ts` |
| Pagamento → acesso | Webhook do Asaas na Lovable (`/api/public/asaas-webhook`) aplica tag e turma no ClickMax e libera o Hub; chave `CLICKMAX_API_KEY` **estava "pendente"** nos segredos (`roadmap.md`): a liberação real de acesso nunca foi validada. Primeiro pagamento real da Jornada de R$ 970: nunca recebido (repositório, 12/11) | `asaasHubWebhook.server.ts`, `FLUXO_ADESAO_CLUBE.md` |
| `domainCount` | `0` no projeto Infoprodutos Zion. O domínio `zionhotelgroup.com` está só na lista de redirecionamento do workspace, "connecting" | ClickMax |

Gateways de pagamento diferentes: o site vende pelo **Asaas** (webhook na Lovable) e pelo **Hotmart**; o ClickMax vende pelo **checkout próprio** (pendente de aprovação do vendedor). São três fontes de "compra" que não conversam entre si.

### 4.2 Pixels do Meta encontrados

| ID do pixel | Onde aparece | Observação |
|---|---|---|
| **1378530017570073** | Site Lovable (`MetaPixel.tsx`, injeção em páginas espelhadas em `paginaEstatica.server.ts`, noscript) **e** site Wix `www.zionbubbleglamping.com` | O mesmo pixel nos dois sites: audiência de hóspedes da Bubble misturada com Academy, Land Bank e Club. Se foi proposital: não verificado |
| **903918118859018** | Nove páginas do GitHub Pages (`zion-collection`, `parceiro-zion`, `land-members`, `raio-x`, etc.) | Pixel das landings de anúncio |
| Rastreio ClickMax (`tr/projeto-de-bruno-25763216` e `tr/infoprodutos-zion`) | Landings e diagnóstico | Não é pixel do Meta, mas é uma segunda fonte de atribuição de lead |

Eventos disparados pelo site (Lovable): `PageView`, `ViewContent` (livros), `Lead` e `InitiateCheckout` (cliques em `pay.hotmart.com`), `Lead` (zion-score), `Contact` (WhatsApp). O código **não** dispara evento ao clicar nos links do Asaas ou do ClickMax, e as vendas pelo Asaas não têm evento `Purchase` no navegador. Contas de anúncio: o repositório cita a conta `1271873041294684` para o Club (diferente das quatro do CLAUDE.md); qual pixel pertence a qual conta: não verificado (não consultei o Windsor).

### 4.3 Risco de dois pixels e duas fontes de lead

**Sim, há risco real:**
1. **Pixel duplo nas páginas espelhadas.** `paginaEstatica.server.ts` injeta o pixel `1378530017570073` quando o HTML de origem **não contém** esse ID. Todas as landings espelhadas do GitHub Pages (clube, parceiro, land-members, raio-x) já têm o `903918118859018`, então carregam **os dois pixels**, cada um contando `PageView`. Se o anúncio otimiza num pixel e o outro conta visitas, os números não fecham.
2. **Pixel compartilhado entre dois negócios** (Wix da Bubble e site Zion).
3. **Duas agendas** (Calendly e ClickMax): agendamentos separados, e a Zaya só enxerga o do ClickMax.
4. **Duas fontes de lead com chaves diferentes**: Supabase (leads, diagnósticos e Raio-X), ClickMax (formulários e captura), HubSpot (código presente, desligado por padrão), Brevo (campanha da Bubble, não publicada). O mesmo lead pode existir em 2 ou 3 bases.
5. **Dois projetos de rastreio do ClickMax** (`projeto-de-bruno-25763216` e `infoprodutos-zion`).
6. **Duas áreas de membros** liberadas por caminhos diferentes (webhook na Lovable versus entrega nativa do ClickMax).

---

## 5. Recomendação (não executada)

### 5.1 Fonte da verdade

- **Lovable (`dd227afd`) = vitrine institucional única**: "o que somos, o que temos, o que oferecemos". Endereço oficial `www.zionhotelgroup.com`. É o único lugar onde o texto da oferta é escrito.
- **ClickMax = só funil, pagamento e área de membros** (formulário, agenda, Zaya, checkouts, entrega). Páginas de venda de infoprodutos vivem em `infoprodutos-zion.clickmax.space` ou em um subdomínio como `go.zionhotelgroup.com`, **nunca** no domínio raiz do site.
- **GitHub Pages = depósito de entregáveis e landings de anúncio**, sem aparecer como "o site". As páginas espelhadas na Lovable devem virar páginas nativas (a Jornada já foi convertida em 13/11) ou passar a ter um único pixel.
- **Wix** continua só para reservas das Bubbles.
- **Zaya** continua sendo a única voz de IA com o lead; o Agente Território fica restrito a membros.

### 5.2 O que o site precisa para mostrar "o que somos, o que temos, o que oferecemos" com a oferta única

1. Uma frase de abertura: o que a Zion é (grupo que desenvolve, gere e opera hospedagens; duas Bubbles em operação).
2. Uma trilha de três blocos: **Aprender** (Club Zion Collection e Jornada), **Estruturar** (Land Bank/diagnóstico), **Equipar** (Glamping Store). Hoje o menu mistura sete itens e dois deles levam ao mesmo Club.
3. Uma só porta para o Club, com um só fluxo (reunião de diagnóstico **ou** ficha e pagamento; a decisão é do Bruno). A Home e a Jornada passam a falar a mesma coisa.
4. Mostrar, ou não, os infoprodutos (Arsenal, ferramentas, Zion Collection 06) numa seção "Ferramentas" com link para o ClickMax. Hoje o site não os conhece.
5. Preços só onde a Zaya e o texto concordarem. Se o Club é vendido na reunião, o site não mostra preço do Club, do Land Members nem da Mentoria.
6. Provas só com autorização e fonte (notas das plataformas, caso Campeche, números da Bubble).

### 5.3 Mudanças sugeridas (nenhuma foi feita)

**Urgente, precisa de "aprovado" e de quem tem acesso ao DNS:**
- U1. No provedor de DNS: `www.zionhotelgroup.com` e `zionhotelgroup.com` com A `185.158.133.1` (sem os registros do ClickMax/Entri); "Check again" em Domínios da Lovable. Paliativo imediato: "Unset as primary" do `www.zionhotelgroup.com` na Lovable para o `lovable.app` voltar a servir o site (do plano da própria Lovable).
- U2. No ClickMax: remover `zionhotelgroup.com` da lista de domínios de redirecionamento (status "connecting"). Se for preciso um domínio para links curtos ou páginas, usar um **subdomínio** (`go.` ou `pay.`).
- U3. Confirmar quem conectou o domínio em 12/11 e se `www.zionbubbleglamping.com` também foi mexido (disconnected às 02:57 UTC), para não tirar a Wix do ar.

**Oferta e texto (todas mexem no que existe: "aprovado"):**
- O1. Escolher uma só porta para o Club e redirecionar `/jornada-desenvolvimento` e `/clube` para a mesma mensagem.
- O2. Despublicar no ClickMax as páginas `/club` e `/club/planos` e os checkouts de R$ 97, ou redirecioná-los.
- O3. Tirar da vitrine preços de Land Members (R$ 270), Diagnóstico (R$ 47) e Mentoria, ou alinhar a Zaya a eles.
- O4. Corrigir V1 a V8 e V11; remover "o maior banco de áreas turísticas do Brasil"; padronizar "mais de 23 destinos" ou "29" após confirmação do Bruno.
- O5. Pedir ao Bruno a confirmação dos números da Bubble, das notas de plataforma e a autorização do caso Campeche antes de qualquer reuso.
- O6. Atualizar o conhecimento do projeto Lovable (preço do dossiê R$ 47, regime de revisão, nova oferta).

**Rastreio e leads:**
- T1. Decidir pixel por finalidade (por exemplo, `903918118859018` para Academy, Club e Land Bank; `1378530017570073` só para a Bubble) e **trocar a regra de injeção** para nunca somar pixel a uma página que já tem outro.
- T2. Escolher uma agenda (ClickMax, a que a Zaya usa) e trocar os links do Calendly.
- T3. Unificar o projeto de rastreio do ClickMax (`projeto-de-bruno-25763216` ou `infoprodutos-zion`).
- T4. Definir qual base é a oficial de lead (ClickMax) e manter o Supabase só como cópia técnica.
- T5. Disparar `Purchase` e `Lead` no retorno do pagamento (hoje não há) e repassar UTM em todos os botões.
- T6. Validar o webhook do Asaas com um pagamento real (a chave do ClickMax estava "pendente").

**Agentes:**
- A1. Documentar uma regra: Zaya conversa com lead; Agente Território só com membro. Alinhar tom e limites.
- A2. Revisar quem tem acesso ao servidor MCP do Land Bank (dados pessoais).
- A3. Arquivar os projetos Lovable sem uso (Compass, Ecosystem, Ecossistema, Structure, Landing antigas) e decidir sobre as duas landings de e-book publicadas (`be1cc760`, `7c29b1bc`).

---

## 6. Não verificado

- Estado ao vivo de `www.zionhotelgroup.com`, `lovable.app` e `zaios.lovable.app` (proxy bloqueia; vale o relato da Lovable em `.lovable/plan.md`).
- Quem cadastrou `zionhotelgroup.com` no ClickMax e como (Entri, DNS manual).
- Publicação atual do projeto Lovable (última versão no ar): a Lovable informou que não conseguiu ler.
- Conteúdo do site Wix além da página inicial; ID do GA4 de `www.zionbubbleglamping.com` (só o pixel apareceu no HTML); configuração de domínio na Wix.
- Qual pixel pertence a qual conta de anúncio; eventos recebidos no Meta.
- Conteúdo das landings de e-book publicadas e do Compass (regras do chat).
- UTM nos botões além do `/diagnostico`.
- Uso real do Agente Território e do servidor MCP.
- Estado dos campos `HUBSPOT_ATIVO` e dos segredos (Lovable não mostra valores).
- Notas Booking/Airbnb/Expedia e autorização do caso Campeche.
