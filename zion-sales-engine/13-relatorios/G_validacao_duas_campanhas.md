# G · Validação para as duas campanhas (SOMENTE LEITURA, 25/11/2026)
Nada foi alterado (Meta, ClickMax, repositório, sem commit). [E] = evidência lida; [H] = hipótese.

## 0. Limites (ler primeiro)
- [E] Windsor (conta 1271873041294684) devolve criativos só de anúncios com linha de dados na janela. Janela last_14d = 58 anúncios. `force_refresh` não existe no plano (ESSENTIAL).
- [E] **Faltam 4 dos 5 anúncios da Mini Mentoria** (120250559495520016, ...496680016, ...502270016, ...503550016): o Windsor só trouxe o 120250559499010016 (MM47-03, spend 0). Provável cache/anúncio sem dados. Texto deles está só no repositório (docs/ads/mm47/COPIES.md), não confirmado no Meta.
- [E] Campanhas de e-book jul–ago (120248288047820016, 120248825502440016, 120248888783830016): puxada ampla (jul–nov, ids, textos, creative_id) foi disparada como tarefa de fundo kf9zyalto. O resultado vai para a conversa principal e pode só chegar quando o usuário mandar nova mensagem. **Essas 3 campanhas NÃO estão classificadas aqui.**
- [E] Windsor não trouxe `video_id` (campo video_asset_video_id volta vazio/incompatível com os outros) nem links de carrossel por cartão. `link_url` vem nulo; o destino está em `call_to_action_url`. Em anúncios de formulário nativo e alguns carrosséis o destino vem `http://fb.me/` ou nulo (sem URL de site).
- **Conteúdo falado dos vídeos: NÃO verificado.** Sem modelo de transcrição local (faster-whisper instalado, mas sem modelo baixado; sem rede para baixar) e não achei roteiro/legenda do Vídeo 01/Vídeo 02 do Meta (id 1120695724114303) no repositório. Candidato: `docs/zion-collection/club/video/plataforma-v02.mp4` (8:36, vídeo da landing, [H] que seja a origem do Vídeo 02), sem roteiro. Roteiros achados: `producao/clube/video-2min/ROTEIRO.md` ("dor e troféu", sem preço, 71 s) e `ROTEIRO_PARCEIRO.md` (59 s, fala "reunião" e "Entre para o clube", sem preço). Artes dos carrosséis só lidas no repositório (docs/ads/mm47: card-01 e card-07 vistos).

## 1. Criativos por campanha: ad_id | creative_id | formato | conjunto | destino | preço no texto | promessas fora da entrega | classe
Destinos: /inscricao-47 = página R$ 47 (oferta 668391e7…, checkout z3a0AEkvRl); /inscricao = R$ 97 (oferta c298aaed…, checkout 1ApwIsdYSy); /parceiro-zion = R$ 47 (668391e7…); /mini-mentoria = R$ 47 (oferta 0c71eeba…, checkout yhyiqUB9OF).
Classes: 1 Pronto venda direta · 2 Aproveitável com copy nova · 3 Edição de vídeo/arte · 4 Incompatível com a oferta atual.

### 1.1 VENDAS PLATAFORMA R$97 (120250538576770016), status 25/11: Vídeo 01/02/remarketing ACTIVE; carrosséis PAUSED
Importante [E]: a campanha se chama "R$97" mas **os 5 vídeos apontam para /inscricao-47, que cobra R$ 47**. Só os carrosséis apontam para /inscricao (R$ 97). O texto dos vídeos diz "taxa de R$ 47".
| ad_id | creative_id | Nome / formato / conjunto | Destino (UTM utm_campaign / utm_content) | Texto primário (resumo; completo no Windsor) | Título | CTA |
|---|---|---|---|---|---|---|
| 120250538593890016 | 1550506153791834 | Vídeo 01 narrativa · vídeo · interesses campeão | /inscricao-47 → R$ 47 · plataforma47_vendas / video01 | "Você tem um terreno em destino turístico, mas não tem capital? Existe um caminho para você. A Zion está em plena expansão e quer te conhecer. Apresente-nos o seu terreno, projeto ou ideia, e nós avaliamos cada caso de forma personalizada. Para isso, inscreva-se na nossa plataforma (taxa de R$ 47), estruture a sua ideia com os formulários e PDFs e nos apresente. Receba o suporte da nossa equipe e vamos agendar uma conversa. A nossa equipe entrará em contato com você. Parcerias e investimentos são possibilidades, não garantias." | Queremos conhecer o seu terreno | Saiba mais |
| 120250554660270016 | 1690587456078920 | Vídeo 02 longa · vídeo · interesses | /inscricao-47 → R$ 47 · plataforma47_vendas / video02_longa | mesmo texto acima | Inscreva o seu terreno na Zion Collection. | Saiba mais |
| 120250554662510016 | 2151933725406637 | Vídeo 02 curta · vídeo · interesses | /inscricao-47#pagar → R$ 47 · video02_curta | mesmo texto | idem | Saiba mais |
| 120250555107730016 | 1137580725675043 | Vídeo 01 remarketing · vídeo · remarketing IG365+vídeo+form 90d | /inscricao-47 → R$ 47 · video01_remarketing | mesmo texto | Queremos conhecer o seu terreno | Saiba mais |
| 120250555108170016 | 2474773346265039 | Vídeo 02 remarketing curta · vídeo · remarketing | /inscricao-47#pagar → R$ 47 · video02_curta_remarketing | mesmo texto | Inscreva o seu terreno na Zion Collection. | Saiba mais |
| 120250539569620016 | 1044622645286567 | Carrossel 10 A com preço · carrossel · interesses | /inscricao → R$ 97 · plataforma97_vendas / carrossel10_a_preco | "Faça a sua inscrição. Queremos te conhecer. Seja um parceiro Zion. Tem um terreno em destino turístico e não tem capital, ou não sabe por onde começar? A nossa plataforma é a sua ferramenta: você assiste aos nossos vídeos, preenche os formulários e constrói o seu Dossiê de Desenvolvimento, com a sua ideia, a infraestrutura que já existe, o orçamento e a pré-viabilidade. Você constrói. A Zion conhece e avalia cada ideia, cada região e cada terreno." | Queremos conhecer o seu terreno | Saiba mais |
| 120250539585710016 | 1417353493503684 | Carrossel 10 B sem preço · carrossel | /inscricao → R$ 97 · carrossel10_b_sempreco | mesmo texto | idem | Saiba mais |
Descrição (campo description) não retornada pelo Windsor nestes anúncios [não verificado]. Imagem do carrossel 10: image_url única (cartão 1) no Windsor; demais cartões não lidos.
Classificação:
- Vídeos 01/02 (5 anúncios): **2** (texto). Promessas fora da entrega [E]: "vamos agendar uma conversa", "nossa equipe entrará em contato", "receba o suporte da nossa equipe", "taxa de R$ 47", "Zion quer te conhecer", "Parcerias e investimentos". A oferta 0c71eeba diz "sem acompanhamento individual e sem reunião". Preço do texto (R$ 47) bate com /inscricao-47 mas não com o nome "R$97". Conteúdo falado do vídeo não verificado: se o vídeo falar reunião/preço/parceria, vira **3**.
- Carrossel 10 A/B: **2** (A pode virar 3 se a arte mostrar R$ 97 e o destino for R$ 47). Texto sem preço, sem reunião, mas "Seja um parceiro Zion", "Queremos te conhecer", "A Zion conhece e avalia" sugerem parceria; destino /inscricao tem trechos de retorno/investidor (ver B_paginas_checkout.md).

### 1.2 Formulário R$ 47 (120250557420830016), ACTIVE, conjunto "ZC2 | FORM 47 DIRETO | BRASIL 25-65", objetivo lead nativo (sem URL de site)
| 120250557461740016 | 2640402549807923 | VIDEO 02 | FORM 47 · vídeo | utm form47direto/video02 | texto igual ao Vídeo 02 vendas ("taxa de R$ 47", "vamos agendar uma conversa", "equipe entrará em contato") | título "Inscreva o seu terreno na Zion Collection." | **4** para venda direta (é de formulário, e promete conversa) |
| 120250557534120016 | 1143005531761496 | CARROSSEL C | FORM 47 | 9 CARTÕES · carrossel | destino `http://fb.me/` (formulário); utm form47direto/carrosselC9 | mesmo texto | título "Zion Glamping Collection" | **4** para venda direta; **2** se reaproveitar a arte/copy |
Arte: cards em docs/ads/form47 (carrossel-c-card-*); preço na arte não lido.

### 1.3 LT47 (120250557994600016), PAUSADA, conjunto "ZC2 | LT47 | BRASIL 25-65 | ADVANTAGE"; 1 imagem por anúncio
Todos: destino /parceiro-zion (R$ 47, oferta 668391e7…), UTM lt47 + utm_term={{ad.id}}. Texto cita "O acesso custa R$ 47, pagamento único", "Pix ou cartão à vista, reembolso em 7 dias", "Plataforma de Estruturação Zion Collection" (nome ≠ "Mini Mentoria"), entregáveis "formação em vídeos e aulas, ferramentas e formulários, Dossiê de Desenvolvimento" (batem com a turma de 9 módulos/70 aulas). Título "Zion Glamping Collection". CTA Saiba mais. Descrição não retornada.
| ad_id | creative_id | Nome | Promessas fora da entrega | Classe |
|---|---|---|---|---|
| 120250558004500016 | 4481706062097990 | 01 PARCEIRO ("Nós podemos ser o seu parceiro") | "parceiro", "Antes de qualquer conversa", "apresente o seu projeto à Zion" (leve) | **1** (trocar "Plataforma de Estruturação" por "Mini Mentoria" se a oferta for esta) |
| 120250558012060016 | 1704992391203624 | 02 CAPITAL | "conversar sobre capital", "apresenta o projeto à Zion" | **1** (com ressalva) |
| 120250558029670016 | 1726599222390803 | 03 TERRA ("sua terra seria a sua participação") | participação/parceria, "chegar a essa conversa" | **2** |
| 120250558039370016 | 1143295985331615 | 04 EXPANSÃO ("Nosso próximo empreendimento pode nascer no seu terreno") | sugere que a Zion fará o empreendimento no terreno do comprador | **2** |
| 120250558040250016 | 972968655597476 | 05 INVESTIDOR ("encontrar um investidor") | "pode conectá-lo a investidores" (captação) | **2** (ou 4 pela promessa de investidor) |
Preço na arte: não lido (cards em docs/ads/lt47/*). [H] segue o texto (R$ 47).

### 1.4 Mini Mentoria (120250559484620016), ACTIVE, conjunto "ZC2 | MM47 | BRASIL 25-65"
Único retornado: 120250559499010016 · creative_id 4254761594656807 · ZC2-MM47-03-PARTICIPACAO · imagem · destino /mini-mentoria → R$ 47, oferta 0c71eeba… · UTM mm47 + utm_term={{ad.id}} · título "Zion Glamping Collection" · CTA Saiba mais.
Texto [E]: "Sua terra pode ser sua participação. ... Mini Mentoria de Estruturação ... 9 módulos e 70 aulas ... 12 meses de acesso ... Aulas gravadas, fichas e formulários interativos, e-books, planilhas de cálculo, kits e modelos (Kit do Investidor e kit de prompts) e o Dossiê... você pode cadastrar o seu terreno no banco de áreas da Zion (é opcional...). Se fizer sentido, podemos conversar sobre parceria e, a critério da Zion, apresentar você a investidores... R$ 47, pagamento único, Pix ou cartão à vista, com reembolso em 7 dias." Arte [E, lida no repositório]: card 1 "Sua terra pode ser sua participação"; card 7 "R$ 47 pagamento único, Pix ou cartão à vista, reembolso em 7 dias" com aviso de que não garante parceria/investimento.
Classe: **1** (entregáveis e preço batem; ressalva: "participação", "podemos conversar sobre parceria", "apresentar a investidores" são promessas condicionais; a oferta diz "sem reunião").
Os outros 4 (01 capital, 02 destino, 04 airbnb, 05 parceiro): texto em docs/ads/mm47/COPIES.md (mesmo corpo, R$ 47, mesmos entregáveis, mesma frase de parceria/investidores) → [H] classe 1/2 igual ao 03; **ids/creative_ids não obtidos**; 04 AIRBNB fala em Airbnb ("Quero construir um Airbnb") e destoa do público de terreno.

### 1.5 Captação R$ 270 (120250521777310016), todos pausados, destino formulário → landing R$ 270
Texto de todos cita **R$ 270** e **"sessão estratégica individual de 45 minutos com Bruno Chaerk"** (V02, V03, V04, V05, Carrossel C) ou "sessão individual de 45 minutos" (V01, V06, carrosséis A/B); "possibilidade de parcerias e investimentos". CTA Saiba mais/Cadastre-se. Classe **4** (preço e sessão individual não existem na oferta atual).
| ad_id | creative_id | Nome |
|---|---|---|
| 120250521979600016 | 2305015426733583 | Vídeo 01 TERRENO CAPITAL (campeão) |
| 120250521991370016 | 1171238248662600 | Vídeo 02 DONO TERRENO (campeão) |
| 120250522199990016 | 1485278267092837 | Carrossel C CAMPEÃO NARRATIVA NOVA (campeão, spend 118,75) |
| 120250521979940016 | 1424898489628165 | Vídeo 03 CONSULTORIA |
| 120250521991530016 | 1197984949588370 | Vídeo 04 COLLECTION |
| 120250521991690016 | 1635313738396058 | Vídeo 05 BUBBLE BLACK FRIDAY |
| 120250521980350016 | 1169597255583245 | Vídeo 06 HISTÓRICO |
| 120250521997630016 | 4728683210712261 | Carrossel A TERRENOS |
| 120250521997960016 | 948338695026535 | Carrossel B FOTOS NOVAS |
Ressalva: **a arte/vídeo dos campeões pode ser aproveitável** (classe 3, edição) se tirarem o R$ 270 e a sessão; o texto do anúncio (hook "terreno sem capital") é o mesmo tema. Arte lida? Não (cards em docs/ads/inscricao-270/campeao-narrativa); [H] a arte cita R$ 270 e sessão.

### 1.6 Outras campanhas pausadas (só inventário; texto completo não capturado, exceto onde indicado)
Todas **4** (formulário/reunião/Land Bank/venda de imóvel/clube R$ 97 antigo), por nome de campanha e destino; nenhuma foi lida arte a arte.
- Land Bank / Diagnóstico → Reunião [03/11], [11/11], [16/11], [18/11]: 120250176147330016 (2030502600970565, vídeo investidores; texto: "método de chalés de experiência e glamping cresce no mundo inteiro" = afirmação de mercado), 120250176153150016 (2336647193766039), 120250176168560016 (1011516751308260), 120250257031200016 (2084274299408370, "sócio e investimentos"), 120250348354880016 (1175599825031024), 120250348626400016 (2797484337313459), 120250422519450016 (1716061383553751), 120250422539560016 (1758787151889334), 120250422623800016 (1844410409937278), 120250456019330016 (2336647193766039), 120250456019840016 (2084274299408370). Prometem diagnóstico/reunião/Land Bank.
- CLUB D 06/11: 120250257022920016 (4768497913377955), carrossel "link direto", "Aprenda e entre para a área de membros do Club Zion Collection" → pode ser **2** (tema aprender), não verificado preço.
- CLUB Clube R$ 97 10/11 (landing nova): 120250331969970016 carrossel (1151299221193175), 120250331971600016 vídeo 2 min "dor e troféu" (39730895483221254; roteiro sem preço) → **3/2** candidatos (o vídeo não fala preço pelo roteiro, mas o texto/landing eram do clube antigo); conteúdo do vídeo final não verificado.
- PARCEIRO ZION 11/11: 120250333274220016 (1672519380913829), 120250333404560016 (1797580271323187), 120250333765310016 (29098431786431901), 120250333775750016 (984608330862362): "Seja um parceiro Zion... você entra com área e infraestrutura, a Zion entra com cabana" → **4** (parceria operacional ≠ plataforma de ensino; vídeo fala reunião).
- Curso Terreno R$ 47 [20/11]: 120250502769000016 e 120250502771910016 (creative 3324408417751938, mesma peça duplicada), 120250502771670016 (1851690215857684). Texto: "Aprenda o passo a passo... território, estudo de mercado e orçamento. Curso online, Pix ou cartão, reembolso em 7 dias." (sem preço no texto, sem reunião; "Antes de falar com um investidor, saiba quanto custa o seu projeto"). [E] texto limpo. **Aproveitável (2)**: entrega de hoje cobre território/mercado/orçamento; destino antigo (landing do curso de terreno) a trocar; arte não lida (docs/ads/curso-terreno-v2).
- URUBICI/FLORIPA (venda de imóvel, formulário), 17/11: 120250439106060016, ...107100016, ...108510016, ...109870016, ...445411680016, ...445414960016, ...445416360016, ...445420120016 (Urubici); 120250439967500016, ...968170016, ...969400016, ...970760016, ...973610016 (Floripa). **4** (outro produto).
- creative_ids Urubici/Floripa: 1770231867376522, 1908696983294716, 1704293507882765, 1194381416568464, 30462325630024297, 1766473867753013, 4586740044942345, 1016791244036232; 4105168749787557, 1105063859196222, 1251166870914922, 1110488588472969, 1136033082588361.

## 2. Resumo de classes (para reutilizar)
- **1 Pronto:** 4254761594656807 (MM47-03, ad 120250559499010016); [com ressalva de frases de parceria] 4481706062097990 (LT47-01), 1704992391203624 (LT47-02).
- **2 Aproveitável (copy):** 1550506153791834, 1690587456078920, 2151933725406637, 1137580725675043, 2474773346265039 (vídeos vendas; tirar "taxa", "agendar conversa", "entrará em contato", "suporte da equipe"); 1044622645286567, 1417353493503684 (carrosséis 10 A/B); 1726599222390803, 1143295985331615, 972968655597476 (LT47-03/04/05; tirar participação/empreendimento/investidor); 3324408417751938, 1851690215857684 (Curso Terreno); 2640402549807923, 1143005531761496 (Form 47, só se trocar a copy e o destino).
- **3 Edição de vídeo/arte:** nenhum confirmado por leitura do conteúdo; candidatos [H]: campeões R$ 270 (2305015426733583, 1171238248662600, 1485278267092837) e vídeos do clube 39730895483221254 (2 min).
- **4 Incompatível:** demais (R$ 270 sessão com Bruno; formulários/reunião/Land Bank; Parceiro; Urubici/Floripa).
- Duplicidade: creative_id 3324408417751938 (2 anúncios), 2336647193766039 e 2084274299408370 (cada um em 2 anúncios).

## 3. Item B mínimo (ClickMax) [E]
- 0c71eeba… "Mini Mentoria de Estruturação" (produto cbbb5fb1…): R$ 47, approved, ticto, Pix+cartão, boleto off, 7 dias. Descrição: "Sem acompanhamento individual e sem reunião... Acesso 12 meses". Entrega: **só turma 087479a3…** (portal 3ef7a340…).
- c298aaed… "Zion Collection Club | Acesso à plataforma" (produto 072083e8…): R$ 97, approved, entrega **as duas turmas** (087479a3… e 69345987…). Descrição: "cadastro do seu terreno no banco de áreas", "Acesso por 12 meses".
- 668391e7… mesma descrição e produto, R$ 47 ("(R$ 47)"), entrega as duas turmas; não é a principal (isMain false).
- 74a3f8c6… nome "Mini Mentoria de Estruturação", **produto 072083e8… (Club)**, R$ 47, approved, descrição da Mini Mentoria, entrega as duas turmas. [H] é a oferta secundária criada para a Mini Mentoria dentro do produto Club. Vendas: não consultei (leitura de vendas fora do escopo mínimo).
- Turma antiga 69345987… ("Zion Collection Club · Plataforma (R$ 97)", portal a8e2157a…) e turma nova 087479a3… ("Plataforma de estruturação (R$ 97)", portal 3ef7a340…): **ambas 9 módulos e 70 aulas, mesmos nomes, mesmos ids de aula, mesmo conteúdo (id 79d3e792…)**: 3+10+8+8+8+9+8+8+8 aulas (11 documentos, 33 links externos, 26 vídeos). Conclusão [E]: R$ 97 e Mini Mentoria R$ 47 entregam o **mesmo conteúdo**; o R$ 97 só entrega o acesso duplicado (nos dois portais). Diferença só no texto da descrição (R$ 97 cita banco de áreas; Mini Mentoria diz sem reunião).
- Páginas (todas v3, publicadas, 25/11): /inscricao-curta (1597b2cc…, R$97 c298aaed…, checkout 1ApwIsdYSy, 105 views), /inscricao (77c286e6…, R$97 c298aaed…, 1ApwIsdYSy, 183), /inscricao-47 (fb1e89b9…, 668391e7…, z3a0AEkvRl, 196), /parceiro-zion (066b2cb9…, 668391e7…, z3a0AEkvRl, 72), /mini-mentoria (be23f04a…, 0c71eeba…, yhyiqUB9OF, 51). Conteúdo (preço no topo, FAQ, prints, bloco de entregáveis): ver B_paginas_checkout.md (inalterado como base; as páginas não foram republicadas depois, exceto /mini-mentoria 25/11 03:51 e /parceiro-zion 01:35). Há também rascunho /mini-mentoria-performance (oferta ca1d914c…, não publicado) e /inscricao-dossie.

## 4. Pixel/CAPI desde C_pixel_capi.md [E]
- pages_tracking_status (7 dias): /inscricao 183 views (último 25/11 02:03Z), /inscricao-curta 105, /inscricao-47 196, /parceiro-zion 72, /mini-mentoria 51; todas com page views recentes.
- `pixelViewContent`: **false nas 5 páginas** (leitura de pages_list agora) → ViewContent continua sem ser disparado pela página. Sem mudança.
- Repositório: nenhum commit com pixel/CAPI/InitiateCheckout/ViewContent desde 24/11. Últimos commits são de Mini Mentoria (landing/barra/hero).
- Não há evidência de que Pixel/CAPI/token tenham sido corrigidos; configuração de pixel e token não é visível por MCP. Teste de navegador/Gerenciador de Eventos continua pendente (seção 8 de C).
