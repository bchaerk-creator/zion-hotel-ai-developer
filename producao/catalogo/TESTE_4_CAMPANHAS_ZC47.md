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
