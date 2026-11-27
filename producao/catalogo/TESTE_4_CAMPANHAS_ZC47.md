# Teste de 4 campanhas · Plataforma Zion Collection (R$ 47)
Responsável: Bruno Chaerk. Elaborado em 27/11/2026. Rascunho: nada aqui liga anúncio. Campanhas nascem pausadas; ativar só com "aprovado" final de Bruno.

## Decisões de Bruno (27/11/2026)
- Teto: **R$ 20/dia por campanha, 5 dias** (4 campanhas = R$ 80/dia, **R$ 400 no total**). Pausar uma campanha que gastar R$ 100 sem nenhuma compra ou lead qualificado.
- Conta de anúncio: **Zion Collection 2** (`1271873041294684`, BRL). Página: `576944608845537`.
- Perguntas: **depois da compra**, como primeira tela da plataforma. Nas campanhas com formulário, as mesmas perguntas vão no formulário do Meta, antes da landing.

## As 4 campanhas (confirmado por Bruno em 27/11)
| # | Nome | Criativo | Entrada | Destino |
|---|---|---|---|---|
| 1 | ZC47 · Terreno · Direto | V1 terreno (`zc47-card-1..7`) | link direto | zionhotelgroup.com/inscricao (compra do acesso) |
| 2 | ZC47 · Pousada/Airbnb · Direto | V2 pousada/Airbnb (`zc47v2-card-1..7`) | link direto | idem |
| 3 | ZC47 · Terreno · Formulário | V1 terreno | formulário nativo do Meta **Land Bank** (já pronto) | tela final leva ao /inscricao |
| 4 | ZC47 · Pousada/Airbnb · Formulário | V2 pousada/Airbnb | formulário nativo do Meta **novo para pousada** (Bruno está fazendo) | tela final leva ao /inscricao |

Formulário nativo do terreno (campanha 3): **"Land Bank | Diagnóstico do terreno - Dono terreno"**, ID `1627911948376725` (página `576944608845537`; idioma cadastrado: English (US); 0 leads em 27/11). Formulário de pousada (campanha 4): **"Land Bank | Diagnóstico do terreno - Dono pousada"**, ID `1127602653227754` (lido de foto borrada: confirmar os dígitos antes de criar o anúncio; idioma English (US); 0 leads em 27/11).

UTM: `zc47-terreno`, `zc47-pousada-airbnb`, `zc47-terreno-form`, `zc47-pousada-airbnb-form`.
Rotina horária de leads (`trig_01Uydzp4XuTKYuk8TPvxTWFM`): **pausada por Bruno em 27/11**; reativar antes de contar com leads no ClickMax (e mapear o formulário novo de pousada, que a rotina ainda não conhece).

## Como medir (mesma fonte para as 4)
- Sem formulário: custo por compra paga (venda do ClickMax com UTM). Equilíbrio: **R$ 44,51 por venda** (líquido).
- Com formulário: custo por cadastro, % de cadastros "qualificados" (matrícula, área, quer parceria) e, depois, quantos compram.
- Comparação final: gasto ÷ vendas em cada braço, e gasto ÷ cadastro qualificado nos braços com formulário. Faturamento não é lucro.

## Questionário de 15 perguntas
1. Nome completo
2. WhatsApp
3. E-mail
4. Cidade e estado onde fica a área ou o negócio
5. Você é: dono de terreno / dono de pousada / anfitrião de Airbnb / outro
6. Tamanho da área (m² ou hectares)
7. A área tem matrícula? (sim / não / em regularização)
8. Infraestrutura (marque): água, energia, acesso por estrada asfaltada, internet, esgoto/fossa
9. O que há de atrativo perto da área? (resposta curta)
10. Já tem projeto ou ideia de empreendimento? (nenhum / ideia / projeto pronto / já opero)
11. Maior dificuldade hoje: falta de capital / falta de projeto / falta de conhecimento / falta de parceiro / outra
12. O que você deseja da Zion?
13. O que você espera dessa parceria?
14. Quer receber formação para se profissionalizar? (sim / não)
15. Gostaria de ser um parceiro Zion? (sim / talvez / só quero aprender)

Regras: sem pedir documento nem dado financeiro; o texto deve dizer que parceria depende de análise e não é garantida. Dados pessoais ficam no ClickMax, nunca no repositório.

## Pendências técnicas (27/11)
- Públicos do campeão (lookalike 1%, abriu e enviou, vídeo novo, similar de formulário) não têm ID completo: usar interesses até Bruno passar os IDs. IDs de interesse achados na conta: Airbnb `6003252231836`, Lodging `6003285299359` (busca em espanhol, resultado fraco para "imóveis" e "empreendedorismo").
- Imagens dos 14 cartões precisam ir para a biblioteca da conta (a ação `create_ad_image` exige envio de arquivo pelo navegador de Bruno). Alternativa a testar: criativo de carrossel com as URLs públicas do GitHub Pages.
- Pixel: a landing tem o pixel `1378530017570073` e o checkout o `903918118859018`; o Purchase de R$ 47 ainda não foi visto no Meta. Até confirmar, os braços sem formulário começam por Tráfego (visualização da landing).
- Exclusão de compradores: falta a lista de clientes no Meta.
- Formulário pós-compra: precisa ser ligado ao acesso (mexe no que já existe), então só com "aprovado".

## Criado no Meta em 27/11/2026 (conta 1271873041294684, tudo PAUSADO, sem conjunto nem anúncio ainda)
- Campanha 1 · Terreno · Direto (OUTCOME_SALES): `120250606242900016`
- Campanha 4 · Pousada/Airbnb · Formulário (OUTCOME_LEADS): `120250606245620016`
- Campanhas 2 e 3: criação **negada pelo usuário** na sessão; não recriar sem novo pedido de Bruno.
- Configuração de público/pixel herdada dos conjuntos que já venderam: Brasil 25-65; interesse "Inversiones inmobiliarias" `6003446239080` + cargo "Empresário" `108611555829523`; pixel `903918118859018` (evento INITIATED_CHECKOUT nos conjuntos de venda; Land Bank/formulários usam só page_id `576944608845537`).

## ESTRATÉGIA CORRIGIDA (27/11/2026, autorização de Bruno / ChatGPT) · tudo PAUSADO
Conta Zion Collection 2 `1271873041294684`. Não usar interesses genéricos no lugar dos públicos personalizados. Não usar o público salvo amplo (`120240025249270016`).

### Campanhas (4, todas pausadas)
| # | Nome | ID | Objetivo |
|---|---|---|---|
| 1 | ZC47 · Terreno · Direto | `120250606242900016` | Vendas |
| 2 | ZC47 · Pousada/Airbnb · Direto | `120250606267250016` | Vendas |
| 3 | ZC47 · Terreno · Formulário | `120250606268260016` | Cadastros |
| 4 | ZC47 · Pousada/Airbnb · Formulário | `120250606245620016` | Cadastros |

### Conjuntos criados (pausados, orçamento PLACEHOLDER de R$ 6/dia: não é o orçamento final)
| Campanha | Conjunto | ID | Inclui | Exclui |
|---|---|---|---|---|
| 1 | A Quente | `120250606273670016` | Top Collection campeão `120250592796030016`, Collection campeão `120250592617440016`, Zion 90 `120250455830270016` | (compradores: lista inexistente) |
| 1 | B Remarketing | `120250606275220016` | Vídeo novo `120250592676910016`, vídeo antigo `120250455897500016`, Look a like formulário `120250593835770016`, similar personalizado `120250592781330016`, Instagram `120250592672940016` | os 3 do conjunto A |
| 1 | C Lookalike 1% | `120250606276400016` | `120250593921040016` | A e B |
| 3 | A Aquisição Lookalike 1% | `120250606282700016` | `120250593921040016` | Top Collection, Collection campeão, Zion 90 |
| 3 | B Recuperação (abriu formulário) | `120250606283690016` | Look a like formulário, similar personalizado | Top Collection, Collection campeão |
Campanhas 2 e 4: SEM conjunto ainda (falta público específico da persona pousada/Airbnb).

### Configuração técnica
- Expansão de audiência (Advantage+): desligada. Posicionamentos automáticos. Brasil, 25-65.
- Campanhas de vendas: otimização para Compra com o pixel `903918118859018`, conforme a ordem de Bruno. **Início de checkout NÃO foi herdado.** O Purchase ainda não está validado (ver pendências).
- Campanhas de formulário: cadastros (LEAD_GENERATION), página `576944608845537`.

### Validação do pixel (Windsor, últimos 14 dias)
- Compra: 0 em todas as campanhas (inconclusivo: as vendas reais não vieram de clique em anúncio).
- Início de checkout: 149 para 139 visitas à página na campanha R$ 97, passando de 100%: o evento dispara ao carregar a página (contaminado).
- Ver conteúdo: 0 em todas.

### Pendências técnicas (não resolvidas)
1. **Anúncios não criados:** os 14 cartões ainda precisam ser carregados na biblioteca do Meta (upload pelo navegador de Bruno); depois recupero os `image_hash` e monto os carrosséis na ordem 1 a 7.
2. **Vídeos:** o ZIP dos vídeos novos nunca chegou a esta sessão.
3. **Regras dos públicos não validadas:** a API devolve só contagem; é preciso conferir no Gerenciador origem, retenção e se "Look a like formulário" e "Público similar personalizado" são mesmo "abriu sem enviar".
4. **Falta público de quem enviou formulário** (para excluir na aquisição) e **lista de compradores** (exclusão).
5. **Campanhas 2 e 4:** proposta de públicos da persona pousada/Airbnb: criar públicos a partir de quem viu o vídeo/página da versão V2, de quem abrir ou enviar o formulário `1127602653227754` e, com volume, um Lookalike deles. Conteúdo do formulário de pousada não validado por API.
6. **Pixel/Purchase:** confirmar no Gerenciador de Eventos qual pixel (`903918118859018` ou `1378530017570073`) recebe a compra confirmada e se há CAPI/deduplicação com ClickMax/Asaas. Nenhuma integração foi alterada.
7. **Orçamento:** proposta consolidada abaixo, aguardando aprovação; conjuntos têm só placeholder.
8. **UTMs do comando oficial** (`utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign={{campaign.id}}&utm_content={{ad.id}}&utm_term={{adset.id}}&utm_placement={{placement}}`): serão aplicadas nos anúncios; verificar depois que chegam ao ClickMax.

### Orçamento: proposta para aprovação (nada aplicado)
Teto global já aprovado por Bruno: R$ 400 (5 dias). Sugestão de divisão diária de R$ 80: venda direta (campanhas 1 e 2) 50%, remarketing 35%, lookalike 15%, formulários dentro do mesmo teto. Detalhar por conjunto só depois do tamanho real das audiências (todas as personalizadas são menores que 1.000 pessoas, exceto vídeo novo ~2.500, vídeo antigo ~1.900 e Instagram/365 ~45 mil): públicos tão pequenos não absorvem R$ 20/dia sem frequência alta.

### Anúncios criados (27/11/2026, todos PAUSADOS) · carrossel V1 terreno, 7 cartões, imagens por URL pública do GitHub
| Campanha / conjunto | Anúncio | ID |
|---|---|---|
| 1 / A Quente | ZC2 \| VENDAS \| V1 \| TERRENO \| CARROSSEL CAMPEÃO \| QUENTE | `120250606465070016` |
| 1 / B Remarketing | ... \| REMARKETING | `120250606476200016` |
| 1 / C Lookalike 1% | ... \| LOOKALIKE 1% | `120250606476980016` |
| 3 / A Aquisição Lookalike | ZC2 \| CADASTROS \| ... \| FORM LAND BANK (formulário `1627911948376725`) | `120250606477690016` |
- Imagens: o Meta busca as imagens pelo endereço público (`picture`); **image_hash e prévia NÃO foram recuperados** (o Windsor não lê o criativo): conferir a prévia no Gerenciador. Ordem enviada: cartões 1 a 7.
- Destino das campanhas de venda: `https://www.zionhotelgroup.com/inscricao` com `utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign={{campaign.id}}&utm_content={{ad.id}}&utm_term={{adset.id}}&utm_placement={{placement}}`; CTA "Saiba mais".
- Ainda sem anúncio: campanha 3 / B Recuperação; campanhas 2 e 4 (sem conjunto); versão V2 pousada/Airbnb (falta público); vídeos.

### Atualização 27/11 (noite) · persona pousada/Airbnb, tudo PAUSADO
- Conjunto criado: **C2 Pousada Direto · A Quente** `120250606574100016` (campanha 2). Inclui Público Instagram `120250592672940016` e Zion Collection 365 `120250455931010016`; exclui Top Collection, Collection campeão, Zion 90 e Instagram não, só os de terreno de maior intenção. Orçamento placeholder R$ 6/dia. **ATENÇÃO: são públicos gerais da conta (incluem donos de terreno), não de pousada/Airbnb. Usei como ponte porque o comando proíbe público aberto, mas é decisão que depende da aprovação de Bruno/ChatGPT; se não aprovado, arquivar este conjunto.**
- Anúncio criado: `120250606583090016` (carrossel V2 pousada/Airbnb, cartões `zc47v2-card-1..7`). Corrigido o link do cartão 7, que saiu com `utm_content=x` fixo; criativo novo `4283918998407261`.
- Anúncio criado: `120250606583390016` (campanha 3 · B Recuperação · formulário Land Bank `1627911948376725`).
- Campanha 4 (pousada/Airbnb formulário): continua SEM conjunto e SEM anúncio. Uma tentativa de conjunto com interesses Airbnb/Lodging não rodou e **não foi refeita**, por violar a regra de não usar interesses genéricos sem aprovação. Formulário `1127602653227754` (conteúdo não validado por API).
- Pixel das campanhas de venda: `903918118859018` (o do ClickMax, usado nos conjuntos que venderam); `1378530017570073` é o do site. Evento configurado: Compra, pendente de validação.
- Orçamento: R$ 6/dia por CONJUNTO é só placeholder, não é aprovação.

## FASE 01 · CARROSSÉIS E FORMULÁRIOS (27/11/2026, noite) · tudo PAUSADO
Escopo: só campanhas com formulário (3 e 4). Vendas diretas e vídeos fora desta etapa. Investimento proposto da fase: R$ 40/dia (os outros R$ 40/dia ficam para vídeos). Rotina de leads continua pausada.

### Campanha 3 · Terreno (`120250606268260016`), formulário `1627911948376725` (Land Bank | Diagnóstico do terreno - Dono terreno)
| Conjunto | ID | Público | Exclui | Orçamento |
|---|---|---|---|---|
| A Aquisição Lookalike 1% | `120250606282700016` | Lookalike `120250593921040016` | Top Collection, Collection campeão, Zion 90 | proposto R$ 20/dia; **no Meta ainda R$ 6** (aumento pendente de aprovação) |
| B Recuperação (abriu sem enviar) | `120250606283690016` | Look a like formulário `120250593835770016`, similar personalizado `120250592781330016` | Top Collection, Collection campeão | proposto R$ 10/dia; **no Meta ainda R$ 6** |
Anúncios (carrossel V1, cartões 1 a 7 na ordem): A `120250606477690016`; B `120250606583390016`.

### Campanha 4 · Pousada/Airbnb (`120250606245620016`), formulário `1127602653227754` (Land Bank | Diagnóstico do terreno - Dono pousada)
- Conjunto de teste: `120250606978700016` · Brasil 25-65 · orçamento proposto R$ 10/dia; **no Meta R$ 10/dia** (criado já com esse valor, pausado).
- Público: (Bed and breakfast `6003196503578` OU VRBO `6003646743113` OU Alquiler vacacional `6003175542014` OU Airbnb `6003252231836` OU Hospitality management studies `6003359052437`) **E** (cargo Empresário `108611555829523` OU Entrepreneurship `105587479474873`). Exclui Top Collection, Collection campeão e Zion 90.
- Tamanhos globais estimados pelo Meta (não só Brasil): B&B 18-21 mi; VRBO 2,6-3,0 mi; Alquiler vacacional 128-151 mi; Airbnb 406-478 mi; Hospitality management studies 34-40 mi; Entrepreneurship (cargo) 570-670 mil. Nenhum interesse identifica "dono de pousada" com precisão: o corte por cargo reduz o público a quem se declara empresário/empreendedor. Interesses de maior pertinência: B&B e VRBO. Pouco pertinentes (não usados): Lodging, Sector hotelero, Hoteles (consumidores amplos); "Hospitality industry" como empregador (10 mil, funcionários, não donos); formação "Hotel and Restaurant Management" (111 mil, estudantes).
- Anúncio: `120250606981070016` (carrossel V2, 7 cartões na ordem 1 a 7; formulário `1127602653227754`).

### Limitações encontradas (não contornadas)
1. **Públicos de quem abriu/enviou formulário:** o Windsor não tem ação para criar públicos de formulário (só site e Lookalike). Criar no Gerenciador (Públicos > Criar > Público personalizado > Formulário instantâneo): "abriu" e "enviou", um para o `1627911948376725` e outro para o `1127602653227754`. Sem eles, **não há exclusão de quem já enviou** nos conjuntos de aquisição.
2. **UTMs nos anúncios de formulário:** o link vai no próprio formulário (tela final) e é fixo (`utm_campaign=zc47-terreno-form` / `zc47-pousada-airbnb-form`); não aceita `{{ad.id}}`. Atribuição por anúncio só pela origem do lead no Meta.
3. **Formulários e prévias:** o conteúdo, a tela final e o idioma (English US) não são legíveis por API; as imagens foram buscadas por URL pública (sem `image_hash`) e a prévia dos anúncios não foi conferida.
4. **Landing/pixel:** a landing `/inscricao` não foi aberta em produção; nenhum pixel ou integração foi alterado.
5. **Orçamento:** aumentos para R$ 20 e R$ 10 na campanha 3 exigem aprovação via token do Windsor; não confirmados.

## FINALIZAÇÃO DA FASE 01 · configuração proposta para aprovação (27/11/2026) · NADA APLICADO, NADA ATIVADO
Ativar exclusivamente as campanhas de formulário (3 e 4). Campanhas de venda direta (1 e 2) e vídeos fora desta etapa.

| Conjunto | ID | R$/dia proposto | Hoje no Meta |
|---|---|---|---|
| C3 A Terreno · Lookalike 1% | `120250606282700016` | 20 | 6 (pendente de aprovação) |
| C3 B Terreno · Remarketing | `120250606283690016` | 10 | 6 (pendente de aprovação) |
| C4 Pousada/Airbnb · teste | `120250606978700016` | 10 | 10 |
Total R$ 40/dia. Limite efetivo de 5 dias (proposto): teto de gasto da campanha 3 = R$ 150 (R$ 30 × 5) e da campanha 4 = R$ 50 (R$ 10 × 5), ou seja R$ 200 na fase; `spend_cap` ainda NÃO aplicado (Windsor exige aprovação). Alternativa: data final do conjunto no momento da ativação.
Orçamento global: R$ 40/dia da fase + R$ 30/dia da campanha de vídeos (a campanha `ZC47 | Frio | Fase 1` aparece ativa) = R$ 70/dia, dentro de R$ 80/dia (R$ 400 em 5 dias).
Rastreio de origem: o Windsor (`facebook_leads`) devolve campaign_id, adset_id, adset_name, ad_name, form_id e form_name por lead; não devolve ad_id.
Pendências antes de ligar (dependem de Bruno no Meta): validar os dois formulários em português, a tela de agradecimento e o link para `/inscricao`; criar os públicos de quem abriu e enviou cada formulário (e depois aplicar as exclusões); conferir a prévia dos três anúncios e dos sete cartões de cada um.

### Ajuste de copy (27/11, pedido de Bruno) · só o texto principal dos 3 anúncios de formulário; cartões e narrativa dos cartões intactos; tudo PAUSADO
Frase acrescentada: "Por meio da nossa plataforma, você poderá apresentar o seu terreno, o seu projeto ou a sua visão à equipe Zion, de forma estruturada. Isso abre a possibilidade de parcerias e investimentos no seu terreno ou empreendimento*." (pousada: "o seu negócio, o seu terreno de expansão ou a sua visão"). Nota: "*Contato, parceria e investimento sujeitos à análise e à agenda. Não são garantidos."
Novos criativos (o Meta não edita criativo, cria um novo): C3-A `1417382006855324` (anúncio `120250606477690016`), C3-B `1833781987860428` (anúncio `120250606583390016`), C4 `1507212061318804` (anúncio `120250606981070016`).
Redação de Bruno "você tem acesso à equipe Zion" foi escrita como "poderá apresentar à equipe Zion" + asterisco, para não soar como garantia de reunião.

### Regra de Bruno (27/11): o carrossel de pousada/Airbnb sempre abre com o cartão da bolha
O primeiro cartão do anúncio de pousada `120250606981070016` passou a ser o MESMO cartão 1 do carrossel de terrenos (`zc47-card-1.png`, bolha). Novo criativo `1795962314851759`. O cartão persona antigo ("Dono de pousada ou Airbnb: pensando em diferenciação...") ficou fora do anúncio e guardado em `docs/ads/zc47-carrossel/zc47v2-card-1-original-persona.png`; `zc47v2-card-1.png` agora é igual ao `zc47-card-1.png`. Carrossel segue com 7 cartões (bolha + V2 cartões 2 a 7). Ponto de atenção: o texto do cartão da bolha fala de "terreno" e "capital"; o título do cartão no Meta continua "Dono de pousada ou Airbnb". Tudo PAUSADO.

## ATIVAÇÃO · 27/11/2026 (aprovação expressa de Bruno: "Pode ligar, está aprovado")
Ligados (campanha, conjunto e anúncio): campanhas 3 `120250606268260016` e 4 `120250606245620016`; conjuntos `120250606282700016` (R$ 20/dia), `120250606283690016` (R$ 10/dia), `120250606978700016` (R$ 10/dia); anúncios `120250606477690016`, `120250606583390016`, `120250606981070016`.
Orçamento total R$ 40/dia. **Limite efetivo:** o teto de gasto por campanha (`spend_cap`) de R$ 150 e R$ 50 foi RECUSADO pelo Meta (mínimo R$ 300). Alternativa aplicada: data final dos 3 conjuntos em 02/12/2026 20h (Brasília). Gasto máximo previsto na fase: cerca de R$ 200.
Continuam PAUSADAS: campanhas 1 e 2 (venda direta) e seus conjuntos e anúncios. Não alterado: Bela, ClickMax, automações, `ZC47 | Frio | Fase 1`. Rotina de leads: pausada (reativar para os leads entrarem no ClickMax).
Pendências de conferência manual: prévia dos 3 anúncios; formulários em português e telas de agradecimento; links para /inscricao; públicos de quem abriu/enviou para exclusão.

## Estado em 27/11 (noite) · campanhas 3 e 4 PAUSADAS por Bruno até a aprovação visual definitiva
- Cartão 1 de pousada/Airbnb final (`zc47v2-card-1-final.png`, no ar no Pages e idêntico ao arquivo local) aplicado ao anúncio `120250606981070016`: Meta confirmou novo criativo `1510524187592289` (cópia do `1795962314851759` com o cartão 1 trocado). `image_hash` e miniatura NÃO legíveis pelo Windsor (anúncio sem entrega devolve 0 linhas): conferir a prévia no Gerenciador.
- Causa do atraso do Pages: publicações canceladas por commits da outra sessão (vídeos); cada push novo cancela a publicação em andamento.
- Orçamento vitalício **inviável nos conjuntos já criados**: o Meta recusa trocar orçamento diário por vitalício em conjunto existente ("o orçamento atual é periódico"). Só seria possível criando conjuntos novos, o que Bruno proibiu. Mantido o orçamento diário R$ 20, R$ 10 e R$ 10, data final 02/12/2026 20h.
- Gasto já realizado nas campanhas 3 e 4: R$ 0.

## LIBERAÇÃO DEFINITIVA · 27/11/2026 (aprovação expressa de Bruno: "Aprovado.") · para acompanhamento do ChatGPT
Ativadas as campanhas 3 `120250606268260016` e 4 `120250606245620016` (com confirmação do Windsor). Conjuntos e anúncios já estavam ativos dentro delas.
| Item | ID | Orçamento aplicado | Encerra |
|---|---|---|---|
| C3 A Terreno Lookalike 1% | conjunto `120250606282700016` · anúncio `120250606477690016` | R$ 20/dia | 02/12/2026 17h (Brasília) |
| C3 B Terreno remarketing | conjunto `120250606283690016` · anúncio `120250606583390016` | R$ 10/dia | idem |
| C4 Pousada/Airbnb | conjunto `120250606978700016` · anúncio `120250606981070016` (criativo `1510524187592289`) | R$ 10/dia | idem |
Total R$ 40/dia · máximo pretendido R$ 200. Orçamento vitalício inviável (Meta recusa trocar diário por vitalício em conjunto existente); teto por campanha recusado (mínimo R$ 300). Controle do teto: data final de 5 dias a partir da ativação. Gasto antes da ativação: R$ 0.
Intocados: campanhas 1 e 2 (pausadas), campanha de vídeos `ZC47 | Frio | Fase 1`, Bela, ClickMax, automações. Rotina de leads: pausada (leads só no Meta até reativar).
