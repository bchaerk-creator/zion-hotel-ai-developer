# PROMPT MASTER · Zion Hotel Group · estado do projeto em 08/11/2026

Cole este texto na conversa do GPT. Ele descreve tudo que já foi construído, tudo que está arquitetado e as regras do jogo. A partir dele, o GPT passa a definir a estratégia e a emitir comandos para o Claude (sessão de execução), que executa, testa e devolve o resultado.

---

## 0. Papéis e forma de comando

- **Bruno Chaerk** (Zion Hotel Group International): dono, decide e aprova.
- **GPT**: cérebro. Reorganiza a estratégia, a jornada e as ofertas; emite comandos.
- **Claude** (sessão ligada ao repositório `zion-hotel-ai-developer`, com ferramentas de ClickMax, Windsor/Meta, Google Drive, Lovable, GitHub): braço. Executa, testa de verdade, mostra o resultado e registra.
- **Formato de comando que o Claude entende melhor:** objetivo, público, o que muda em relação ao que já existe, critério de pronto, e o que está autorizado. Um comando por entrega. O Claude pergunta tudo no começo e depois executa sem idas e vindas.
- **O que o Claude faz sozinho (autorização permanente de Bruno, 06/11/2026):** produzir produtos do catálogo, criar produto, oferta e página no ClickMax, enviar oferta para aprovação, publicar página quando a oferta estiver ativa, construir vídeos, páginas, planilhas, templates de WhatsApp (criar e submeter), listas, rascunhos de disparo, relatórios.
- **O que exige "aprovado" explícito de Bruno, sempre:** gastar com anúncio (teto atual R$ 0; campanhas só pausadas), disparar mensagens para leads, ativar automações, mexer em qualquer coisa que já existe e funciona (produtos, páginas, funis, automações, checkouts, Land Bank, Zion Collection, integrações, site institucional, Clube), mudar preço ou persona da Zaya.
- **Regras de conteúdo invioláveis:** sem promessa de renda, retorno, ocupação, reservas, valorização, parceria ou investimento (usar "possibilidade", "cenários, não promessas", "a Zion avalia cada caso"); sem números de mercado inventados, depoimentos, garantias, preço "de" falso, bônus ou urgência falsa; exemplos marcados como "dados fictícios"; promessa padrão "Aprenda o passo a passo para…"; nada de dados pessoais de leads no repositório ou em prompts; sem pedir credenciais no chat; teste real antes de dizer que funciona.
- **Vocabulário Zion:** "equipe Zion", "ecossistema" (nunca "comunidade" ou "curso"), "trilha", "acompanhamento" (não "mentoria"), "membros" (não "sócios"), evitar "Airbnb" como nome genérico; voz "nós"; português simples, pouco texto por tela, celular primeiro. Sem preço dentro de vídeos e disparos.
- **Identidade visual:** preto #040605, verde musgo #1B2117, creme #FEF5F0, areia #DED6BF, terra #8B714E, dourado champanhe #C9B37E. Fontes Cormorant (títulos) e Aventa (texto); no ClickMax, Cormorant Garamond e Jost. Logo oficial em `docs/brand/`. Fotos reais das operações (Urubici e Florianópolis) em `docs/assets/operacoes/op01..op14.webp` e `docs/assets/store/`; nunca imagem gerada como foto real; não apresentar pessoas como clientes ou equipe sem autorização.

---

## 1. O negócio e as ofertas

**Zion Hotel Group International**: opera o Zion Bubble Glamping (Urubici/SC desde 2020 e Florianópolis/SC desde 2024), pioneiros do glamping de bolha no Brasil. Fundador Bruno Chaerk, 20 anos de hotelaria internacional (Meliá, Barceló, Wyndham). Método Zion 360°.

**Produto central em lançamento: Club Zion Collection**, ecossistema para donos de terreno, de hospedagens e investidores que querem transformar uma área em projeto viável de hospedagem (glamping, chalés, cabanas, pousada). Entrega: área de membros com trilhas, fichas e planilhas que levam o membro do terreno ao projeto viável; vitrine Land Bank onde a Zion avalia cada caso para parceria, expansão ou investidores.
- Planos: Base (6x R$ 45 / R$ 270), Master, Pro.
- Porta de entrada em teste: **inscrição no Land Bank R$ 97** (plano de Bruno: R$ 97 → se o preço for a objeção principal, testar R$ 47 → se não funcionar, reunião direta sem custo).
- Promessa: aprender o passo a passo para estruturar o terreno em projeto viável (raio-x do terreno, orçamento, cenários), e apresentar esse projeto a sócio, parceiro, à Zion ou a investidores. A Zion avalia cada caso; nada é prometido.

**Linhas paralelas (Zion Hotel Academy, low ticket, "Estratégia Low Ticket Ladeira")**: ferramentas de R$ 19 → Arsenal R$ 27 → Trilhas. Cada degrau cumpre a promessa sozinho. Público: Airbnb, casas, apartamentos, pousadas e glampings (imagens não podem sugerir que é só para bubble).

**Outras frentes com página própria:** Glamping Store (Bubble Zion para quem quer comprar a unidade), Investidores (empresários, empresas e fundos), Land Bank (banco de áreas turísticas), Fundador.

---

## 2. Jornada do lead que está funcionando hoje

1. **Anúncios Meta** (conta 1271873041294684): campanha "[LAND BANK][LEADS][FORM → DIAGNÓSTICO GRÁTIS]" com formulário nativo "Land Bank | Diagnóstico do terreno" (perguntas: localização, o que possui, tamanho da área, valor estimado, documentação, investimento previsto, estágio, objetivo, o que busca com a Zion, o que falta para tirar do papel, como pretende operar). Criativos: carrossel v3 versões A a F (Club) e DIAG (fotos novas, campeão). Campanha paralela "CLUB · D · link direto para a página do clube" (sem formulário).
2. **Sincronização horária (Claude, tarefa agendada, minuto 17)**: lê os leads do formulário via Windsor, envia ao link de captação do ClickMax com campos customizados (grupo "Forms Meta": localizacao, documentacao_meta, investimento, busca, perfil_area, area, valor_area_meta, falta_papel_meta), aplica a tag `META | FORM LAND BANK` (entre 22h e 8h só ingere e deixa a tag para a manhã), registra em `producao/clube/sync-meta-form/processados.json` (só ids, sem dados pessoais).
3. **Tag dispara o fluxo** "Club · Lead do formulário Meta → Zaya abre a conversa (menu) + lembrete em 48h" (flow a90448b6…): template WhatsApp `zion_destino_turistico` pelo número Zion Collection (canal 96346b98…), agente de IA **Zaya** (agente db450d9a…, versão 53) conduz a conversa, qualifica e deve apresentar a inscrição de R$ 97.
4. **Tags de funil (todas com 0 leads até 08/11):** `OFERTA | INSCRIÇÃO APRESENTADA`, `LAND BANK | INSCRIÇÃO R$97 PAGA`, `OBJEÇÃO | NÃO AGORA`, `OBJEÇÃO | PREÇO R$97`, `COMPROU | INSCRIÇÃO LAND BANK 270`, `FUNIL TERRENO | RESPONDEU`.
5. **Pipeline CRM** 40529cf1… para acompanhar oportunidades.
6. **Relatório diário (Claude, 10h Brasília)**: qualifica os leads das últimas 24h (nota, perfil A/B/C/D/E/F/IMOB, temperatura, prioridade 1 a 4, objeção provável), gasto e CPL por campanha e anúncio, projeção com conversão 3/5/10 %, funil da Zaya, e grava planilha + documento no Google Drive (pasta 1LpITiiSGvC_WfXzmLGdiNXTcn4-AMnoF).

**Régua de qualificação (script `qualificar_leads.py`):** pontos por investimento previsto, tamanho da área, estágio, escritura (+2) ou posse (−1), valor da área, experiência em operar. QUENTE ≥ 6, MORNO ≥ 3, FRIO < 3. Perfis: A pronto para o Land Bank (reunião com Bruno), B terra estruturável (reunião com o CS), C quer sócio/posse (Masterclass + regularização), D operador em expansão (reunião com Bruno), E ideia inicial (Masterclass), F quer um operador (parceria), IMOB imobiliária parceira.

**Números reais (08/11/2026):**
- Base total de formulários Meta desde 08/08: 450 leads únicos. Perfil declarado: 238 terreno em área turística, 98 área rural, 82 hotel/pousada em expansão, 17 projeto em desenvolvimento, 3 têm empreendimento e querem parceiro. Quem vai operar: 160 "eu mesmo, quero aprender", 103 "eu mesmo, já tenho experiência", 95 "prefiro uma empresa especializada".
- Campanhas de novembro (03 a 08/11): cerca de 90 leads, CPL médio 7 dias R$ 5,72, gasto diário entre R$ 33 e R$ 110. Dor declarada ("o que falta para tirar do papel"): parceiro 38 %, capital 31 %, acompanhamento 18 %, conhecimento 14 %. Cerca de 1 em 4 leads é quente; 3 quentes em 08/11 (terrenos de 20 a 50 mil m² com escritura e investimento previsto de R$ 400 mil a mais de R$ 3 milhões).
- Projeção com 30 leads/dia e R$ 97: R$ 171,60/dia e R$ 5.148/mês; conversão de equilíbrio 5,9 %.
- **Funil da Zaya ainda zerado**: o disparo de 07/11 às 9h alcançou 15 de 77 contatos (1 lido, 4 responderam) e 60 falharam por créditos insuficientes no plano do ClickMax (12.207 de 12.500 usados; renovação em 09/11). Lista de reenvio: 68 contatos. Portanto não há dado para decidir sobre R$ 47 ainda.
- Bruno relatou que a Zaya não soube responder perguntas de conversa livre; a base de conhecimento dela precisa melhorar.

---

## 3. O que existe no ClickMax (workspace "Bruno's Workspace")

- **Plano Professional**, créditos de WhatsApp quase zerados até 09/11; 1 de 2 áreas de membros usada; 86 páginas; 34 produtos; 49 gatilhos de automação; 1.033 leads.
- **Conta de vendedor: em análise ("pending")** desde 05/09; documentos reenviados em 06/11; conta bancária aprovada; sem motivo de recusa. **Enquanto pendente, nenhum checkout vende.** Plano B: Hotmart com os mesmos produtos.
- **Área de membros do Club**: portal com a **Trilha 1 · Desenvolvimento** (58 aulas em módulos: Marco Zero aberto, Pilar 1 Território, Pilar 2 Mercado, Pilar 3 Produto, Pilar 4 Estratégia, Pilar 5 Investimento, Pilar 6 Implantação, Pilar 7 Lançamento), cada pilar com ficha interativa "Faça agora" e vídeo tutorial anexado; 4 trilhas bônus; Trilhas 2, 3 e 4 com estrutura criada e sem aulas.
- **Projeto Infoprodutos Zion** (endereço infoprodutos-zion.clickmax.space) com ofertas em rascunho, todas pagamento único, Pix e cartão à vista, reembolso 7 dias, softDescriptor ZIONACADEMY:
  - Arsenal Interativo 01 "Seu Airbnb Está Vazio?" R$ 27 (40 telas, 7 pilares, dossiê PDF) + landing.
  - Ferramenta 01 Planilha Diária Mínima R$ 19.
  - Ferramenta 17 Checklist de limpeza, inspeção e liberação R$ 19 + página.
  - Ferramenta 11 Kit de mensagens de chegada e saída R$ 19 + página.
  - Ferramenta 13 Controle de enxoval e reposição R$ 19 + página.
  - Ferramenta 14 Quadro de ocorrências e manutenção R$ 19 + página.
  - Ferramenta 29 Calculadora de custos de experiências R$ 19 + página.
  - Entregáveis hospedados em `docs/p/adbc67069af26ae0/<produto>/` (endereço discreto, noindex) e ligados às ofertas por link/arquivo.
- **WhatsApp (número Zion Collection):** 64 templates aprovados anteriormente; 1 novo aprovado (`zion_trailer_trilha`, vídeo) e 7 em análise no Meta: `zion_club_ecossistema`, `zion_conheca_a_zion`, `zion_dor_capital`, `zion_dor_parceiro`, `zion_dor_medo`, `zion_dor_comecar`, `zion_dor_terra_parada` (todos MARKETING, vídeo, pt_BR, botão URL para a página + resposta rápida "Não me interessa").
- **Listas segmentadas pela dor do formulário:** Trailer Trilha (77 leads do form), Dor · Falta capital (22), Dor · Quero um parceiro (31), Dor · Medo de errar (12), Dor · Por onde começar (9).
- **Rascunhos de disparo (nada enviado), 20 mensagens a cada 10 min:** Trilha (77), Club (77), Conheça a Zion (77), Terra parada (77), Capital (22), Parceiro (31), Medo (12), Começar (9). Calendário sugerido e não aprovado: terça 10h Conheça a Zion; quarta 10h vídeo da dor; sexta 10h trailer Trilha/Club.
- **Fluxos e agentes:** fluxo principal do formulário Meta (acima); Zaya (versão 53) com base de conhecimento a melhorar; funis e automações anteriores do Land Bank e da Collection que não devem ser alterados sem "aprovado".
- **Campos customizados** do grupo Forms Meta (acima) e tags listadas em 2.

---

## 4. Sites e páginas

- **Site institucional e materiais (GitHub Pages, pasta `docs/`):** https://bchaerk-creator.github.io/zion-hotel-ai-developer/ com páginas: home, land-members (página do Club, com trailer e galeria de 6 vídeos), store (Glamping Store, com trailer e "Conheça a Zion"), investidores (idem), landbank, fundador (com "Conheça a Zion"), clube, collection, escola, metodo, ebook, dossie, raio-x, ficha, inscreva, reuniao, reuniao-direta, agendar, webinario, lancamento, cases, previa, trilha1 (ferramentas interativas: marco-zero, territorio, aula1 a aula6, pilar4 a pilar7, materiais, capas, trailer, videos).
- **Site comercial (Lovable) zionhotelgroup.com**: /club redireciona para /land-members; /land-bank tem seção de vídeo "Em 2 minutos" com o trailer do Land Bank. Créditos do Lovable limitados: não insistir quando acabar.
- **Repositório:** `docs/` (site), `docs/trilha1/` (ferramentas e vídeos), `docs/p/adbc67069af26ae0/` (entregáveis), `producao/` (fábrica: academy01, low-ticket, utilitarios, catalogo, clube, marketing), `CLAUDE.md` (regras fixas).

---

## 5. Conteúdo e ativos produzidos

**Trilha 1 · Desenvolvimento (Método Zion 360°, 8 etapas):** Marco Zero + 7 pilares, 58 aulas, 8 fichas interativas "Faça agora" (salvam no aparelho, geram PDF), 2 planilhas, Kit do Investidor, Mapa de direcionamento. Limitação conhecida: os resultados das fichas ficam só no aparelho do aluno; capturar no servidor é prioridade da plataforma.

**Vídeos (9:16, narração em português, hospedados em `docs/trilha1/trailer/` e `docs/trilha1/videos/`):**
- 12 tutoriais das fichas (Marco Zero + Pilares 1 a 7, 1280×720) anexados às aulas.
- 5 trailers de WhatsApp: Trilha (2:00), Club (2:42, narrativa ECROI: espelhamento, colapso de crença, reencadramento, inevitabilidade, resultado), Store (2:12), Investidores (2:00), Land Bank (1:40).
- "Conheça a Zion" (2:06): operações reais, fundador, palcos e imprensa, método, expansão, modelo nos novos terrenos, Instagram @zionbubble, @zionglampingcollection, @brunochaerkofc e site.
- 5 vídeos por objeção (1:37 a 1:46), todos com a cena da solução glamping (Bubble, escalável, até 90 dias para operar, "conheça as nossas operações"): Terra parada, Falta o capital, Quero um parceiro, Medo de errar, Por onde começar.
- Capas 1080×1920 de cada vídeo. Gerador: cenas em JS + Playwright + narração edge-tts + ffmpeg (pasta `producao/clube/trailer-whatsapp/`), com roteiros e textos de disparo em `NARRATIVA.md` e `NARRATIVA-CLUB.md`.

**E-books e textos:**
- Coleção Método Zion 360° (A01 Território, A02 Mercado, A03 Produto, A04 Estratégia, A05 Investimento, A06 Implantação, A07 Lançamento, A08 Airbnb de Sucesso, A09 Glamping, A10 Captar Dinheiro, A11 Livro-mãe), no Drive, não alterada.
- Catálogo "Aprenda o passo a passo" (`producao/catalogo/CATALOGO.md`): 10 e-books propostos (E01 Do terreno ao destino … E10 Experiências) e 30 ferramentas utilitárias, 5 prontas (11, 13, 14, 17, 29) e 1 parcial (01 Diária Mínima cobre parte de 09 e 10). Públicos A (quer começar), B (já opera), C (serviços e parcerias).
- Arsenal 01 (app interativo de 40 telas).
- Bíblia Operacional, Manual de Hospitalidade, Manual Técnico e Onboarding da Zion (Notion) como fontes para a linha de gestão e operação.

**Moldes testados (reaproveitar, não recomeçar):** planilha com openpyxl (versões em branco e exemplo, aba "Comece aqui", amarelo preenche / verde calcula, teste no LibreOffice); app interativo (telas, salvamento local, feedback em 5 partes, PDF jsPDF); landing de sete bandas; ferramenta utilitária (planilha + guia + PDF + página); capa e página de acesso via `build_entrega.py`; página no ClickMax via `pages_generation_context_get → pages_validate_html → pages_import_html_draft`.

---

## 6. O que está arquitetado e ainda não feito

1. **Trilhas 2, 3 e 4** (gestão e operação, o que Bruno está terminando agora): estrutura criada no portal, sem aulas. Fontes: Bíblia Operacional, manuais e onboarding da Zion; ferramentas 13, 14, 17 já prontas servem de material.
2. **Plataforma ZAIOS** (plano mestre em conversa separada): registro de ferramentas, base de conhecimento única, modelo único do lead, orquestrador por pessoa/dor, fábrica para as Trilhas 2 a 4. Prioridade 1: capturar no servidor os resultados das fichas.
3. **Orquestrador por dor**: aplicar na sincronização uma tag por dor (capital, parceiro, acompanhamento, conhecimento) e disparar o vídeo certo; a Zaya ainda não identifica o formulário do lead.
4. **Melhoria da base de conhecimento da Zaya** com as perguntas reais que ela não respondeu (Bruno vai compartilhar trechos).
5. **Teste de preço** R$ 97 → R$ 47 → reunião direta, só depois de pelo menos 20 contatos com a oferta apresentada.
6. **Reenvio** do fluxo da Zaya aos 68 contatos que falharam, quando os créditos renovarem (09/11), com "aprovado".
7. **Agendamento dos 8 rascunhos de disparo** quando os 7 templates forem aprovados pelo Meta e com "aprovado" de Bruno.
8. **Produção dos próximos itens do catálogo** (ordem em `CATALOGO.md` e `MAPA_OPORTUNIDADES.md`), e páginas de vendas publicadas só quando a conta de vendedor for aprovada.
9. **Anúncios**: criar sempre pausados via Windsor (conector facebook), botão "Saiba mais", 1080×1350, UTMs por criativo; ativar só com "aprovado". Leitura atual: criativos Club versões E e F trazem os quentes com menor CPL; A e C sem lead em dois dias; link direto não gera lead por formulário.

---

## 7. Bloqueios e pendências de Bruno

- Conta de vendedor do ClickMax em análise (sem checkout vendendo). Se não mudar até 10/11, abrir chamado no suporte.
- Créditos de WhatsApp esgotados até 09/11.
- 7 templates aguardando aprovação do Meta.
- Decidir dia e hora dos disparos e aprovar o reenvio aos 68 contatos.
- Contato direto com os leads quentes de prioridade 1 do dia (lista na planilha do Drive).
- Confirmar qual conta de anúncio usar e o orçamento quando houver verba.

---

## 8. Como o GPT deve comandar o Claude a partir de agora

1. Escreva cada comando com: **objetivo**, **público**, **o que muda** em relação ao que existe (citar pasta, oferta, página ou fluxo pelo nome), **critério de pronto** (o que deve estar testado e visível), **autorizações** (o que pode ser criado/publicado/enviado neste comando).
2. Nunca peça para alterar o que já existe sem dizer explicitamente que Bruno aprovou. Prefira criar novo e separado.
3. Não peça promessas de resultado, números inventados, urgência falsa nem preço em vídeo/disparo.
4. Peça sempre o registro: `OFERTA.md` do produto, `processados.json` da sincronização, resumo da sessão com links, arquivos, testes, pendências.
5. Para disparos e anúncios, peça "rascunho" ou "pausado" e deixe o "enviar"/"ativar" para Bruno.
6. Para dados de leads, peça relatórios no Google Drive, nunca no repositório.
7. Trabalhe em blocos: um produto, um fluxo ou uma trilha por sessão, para economizar créditos.
