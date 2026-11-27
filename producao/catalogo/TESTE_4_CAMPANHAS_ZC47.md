# Teste de 4 campanhas · Plataforma Zion Collection (R$ 47)
Responsável: Bruno Chaerk. Elaborado em 27/11/2026. Rascunho: nada aqui liga anúncio. Campanhas nascem pausadas; ativar só com "aprovado" final de Bruno.

## Decisões de Bruno (27/11/2026)
- Teto: **R$ 20/dia por campanha, 5 dias** (4 campanhas = R$ 80/dia, **R$ 400 no total**). Pausar uma campanha que gastar R$ 100 sem nenhuma compra ou lead qualificado.
- Conta de anúncio: **Zion Collection 2** (`1271873041294684`, BRL). Página: `576944608845537`.
- Perguntas: **depois da compra**, como primeira tela da plataforma. Nas campanhas com formulário, as mesmas perguntas vão no formulário do Meta, antes da landing.

## As 4 campanhas
| # | Criativo | Formulário | Objetivo | Destino |
|---|---|---|---|---|
| 1 | V1 terreno (`zc47-card-1..7`) | Não | Vendas (ou Tráfego até confirmar o Purchase) | zionhotelgroup.com/inscricao |
| 2 | V2 pousada/Airbnb (`zc47v2-card-1..7`) | Não | idem | idem |
| 3 | V1 terreno | Sim (formulário do Meta, 15 perguntas) | Cadastros | formulário, depois a landing |
| 4 | V2 pousada/Airbnb | Sim | Cadastros | idem |

UTM: `zc47-terreno`, `zc47-pousada-airbnb`, `zc47-terreno-form`, `zc47-pousada-airbnb-form`.

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
