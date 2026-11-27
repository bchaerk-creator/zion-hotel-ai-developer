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
