# HANDOFF · Zion Collection · Campanha de vendas Low Ticket (Mini Mentoria de Estruturação, R$ 47)
Data: 25/11/2026 (madrugada). Preparado pelo Claude para o ChatGPT assumir estratégia de tráfego, estruturação da campanha, análise e escala.
Sem senhas, tokens ou chaves. Marcação: [CONFIRMADO] = lido/testado; [NÃO CONFIRMADO] = não foi possível verificar; [HIPÓTESE].

## 0. Regras do dono (Bruno Chaerk) que valem para quem assumir
- Gastar com anúncio, ligar campanha, disparar mensagem a leads, ativar automação e mexer no que já existe EXIGEM "aprovado" de Bruno. Criar campanhas sempre PAUSADAS.
- Sem invenção e sem promessa: nada de números de mercado inventados, depoimentos, resultado, "garantido", renda, investimento ou parceria prometidos. Parcerias e investimentos são "possibilidades, sujeitas à análise".
- Promessa-padrão: "Aprenda o passo a passo para estruturar um empreendimento turístico, preparar seu projeto para potenciais investidores e apresentar seu terreno à Zion."
- Fotos: só reais da Zion, sem pessoas; texto nunca em cima da foto (Bruno quer foto nítida).
- Gateway de pagamento das ofertas é a TICTO (não o Asaas).

## 1. Produto e preço
- Produto: Mini Mentoria de Estruturação (formação digital, SEM acompanhamento individual nem reunião). Slogan: "Transforme seu terreno em um destino turístico."
- Preço: R$ 47, pagamento único, Pix e cartão à vista (1x), sem boleto, sem recorrência, reembolso em 7 dias. Acesso por 12 meses.
- Conteúdo real (turma do portal): 9 módulos e 70 aulas e materiais (Onboarding, Marco Zero e 7 pilares: Território, Mercado, Produto, Modelo de Negócio, Masterplan, Pré-viabilidade, Capital e Dossiê); aulas gravadas em vídeo, fichas/formulários "Faça agora", e-books por pilar, 2 planilhas de cálculo (em branco), Kit do Investidor (modelos) e kit de prompts, Dossiê de Desenvolvimento (cada ficha vira uma página; PDF no final); cadastro opcional do terreno no banco de áreas da Zion (a Zion avalia cada caso). NÃO existe: calculadoras/simuladores na turma (ficam fora), acompanhamento, reunião, rede de investidores.

## 2. Landing page
- https://infoprodutos-zion.clickmax.space/mini-mentoria (página id be23f04a-fa2e-4fc6-91ee-51a9aeb915d1; no ar; foto real da bolha nítida no topo; seção "O que você recebe em cada etapa" (Dossiê 1 a 7); barra fixa de botão só no celular; checkout embutido no fim da página).
- Páginas antigas ainda no ar (não usar como destino principal): /inscricao-47 (R$ 47), /parceiro-zion (R$ 47), /inscricao-curta e /inscricao (R$ 97), /inscricao-dossie.

## 3. Checkout
- Não existe página de checkout separada confirmada: o checkout é um iframe embutido na landing (payments.clickmax.io/custom/<id da página>/yhyiqUB9OF). URL que leva direto ao quadro de pagamento: https://infoprodutos-zion.clickmax.space/mini-mentoria#pagar
- Hash do checkout da oferta: yhyiqUB9OF. Oferta id 0c71eeba-2654-432c-9701-0a31e6113a08 (aprovada, sem erro de sincronização do gateway).
- [NÃO CONFIRMADO] URL standalone do checkout (ex.: pay/...): não foi verificada por nenhuma ferramenta.

## 4. Página de confirmação da compra
- Existe /obrigado-plataforma (id d7166fc3-4f27-483b-8d9e-ca636c7facf0, publicada), MAS o checkout NÃO redireciona para ela (pendência de painel de Bruno). Os textos dela ainda citam R$ 97. Hoje a confirmação é o e-mail de acesso.

## 5. IDs ClickMax
- Workspace e87e8ba9-37cf-4c54-9a97-3e4e1b01827a; projeto Infoprodutos Zion 8d1152a4-4490-4666-bcb5-582b75c82660.
- Produto Mini Mentoria: cbbb5fb1-550f-4a8d-b269-5122c17b7780. Oferta: 0c71eeba-2654-432c-9701-0a31e6113a08. Entrega: portal 3ef7a340-0fcc-414a-8f3b-c9404c3b90f4, turma 087479a3-9d6f-4e1f-a542-c47b347bf5ed (só ela).
- Produtos/ofertas anteriores (referência): oferta R$ 47 668391e7-f4a8-4bd3-a212-deba406f8a7a (entrega duas turmas, inclui a antiga), oferta R$ 97 c298aaed-88ac-46dd-b6f3-f3c07ae08513, oferta intermediária 74a3f8c6-fc1d-4aa8-9ac9-7769a1c49aa5 (sem uso).
- Vendedor: canSell true; status geral do vendedor ainda "pending".

## 6. Pixel e dataset
- Pixel Meta: 903918118859018 [CONFIRMADO como o usado nos conjuntos de venda].
- Dataset vinculado: [NÃO CONFIRMADO] (nenhuma ferramenta mostra o dataset).
- As páginas do ClickMax NÃO têm o código do pixel no HTML; o pixel roda dentro do iframe de pagamento. O evento ViewContent está desligado nas páginas (pixelViewContent=false).

## 7. API de Conversões
- [NÃO CONFIRMADO]: não há ferramenta que mostre token, configuração ou histórico de envio. A documentação do ClickMax diz usar o mesmo eventID no pixel e na CAPI, mas isso não foi verificado na Meta. Verificar em Gerenciador de Eventos > Diagnóstico, Deduplicação e Qualidade de correspondência.

## 8. O Purchase dispara só após pagamento aprovado?
- NÃO CONFIRMADO, e há sinais de risco:
  - O código de checkout embutido no HTML chama fbq Purchase ao gerar Pix, boleto e cartão (não só na aprovação); isso contradiz a documentação do ClickMax ("compra aprovada"). Esse trecho está dormente na página-mãe; o que roda no iframe não pôde ser lido.
  - O InitiateCheckout dispara ao CARREGAR o checkout (sem clique): por isso initiate_checkout ≈ visualizações de página no Meta (89 LPV / 96 IC).
  - Em 24/11 houve 2 vendas reais (R$ 97, Pix) e o Meta registrou 0 compras em todas as campanhas.
  - Valor enviado pelo postMessage pode chegar dividido por 100 duas vezes (hipótese pelo código).
- Teste necessário (Bruno): Gerenciador de Eventos > Testar eventos; gerar Pix de teste e ver se Purchase chega antes do pagamento; conferir filtro de forma de pagamento do Purchase e token da CAPI no pixel.

## 9. Criativos (Google Drive)
- Os criativos da Mini Mentoria NÃO estão no Google Drive; estão no GitHub Pages (públicos): https://bchaerk-creator.github.io/zion-hotel-ai-developer/ads/mm47/<pasta>/card-0N.png (N=1 a 7; 1080x1350). Pastas: 01-capital, 02-destino, 03-participacao, 04-airbnb, 05-parceiro. Repositório: docs/ads/mm47/ e gerador producao/zion-collection/club-97/mini-mentoria/build_cards.js.
- Estrutura dos 7 cards: 1 desejo (frase da narrativa) · 2 dor · 3 "não precisa ter todo o capital; comece estruturando" · 4 a Zion como possível parceira (possibilidade) · 5 "O que você recebe" (9 módulos, 70 aulas e materiais, 12 meses; 6 tipos de entregável; capturas reais) · 6 jornada · 7 oferta R$ 47 + CTA "QUERO TRANSFORMAR MEU TERRENO".
- Carrosséis LT47 anteriores (pausados): docs/ads/lt47/. Campeão histórico: carrossel C do formulário R$ 270 (ad 120250522199990016).
- Se o ChatGPT precisar dos arquivos no Drive, é preciso copiar (não feito).

## 10. Copies, títulos e descrições (Mini Mentoria, 5 anúncios; botão "Saiba mais")
### Copies MM47 · Mini Mentoria de Estruturação (R$ 47 · pagamento único)

Slogan: Transforme seu terreno em um destino turístico.
Botão em todos: **Saiba mais**. Link: venda direta (site → checkout), com `utm_source=meta&utm_medium=paid&utm_campaign=mm47&utm_content=<id>`.
Nada publicado: só material para Bruno aprovar. Entregáveis citados limitam-se ao que existe na turma de R$ 47, conforme `producao/zion-collection/club-97/mini-mentoria/INVENTARIO.md` (sem simuladores, sem atendimento individual).

## ZC2-MM47-01-CAPITAL
**Texto primário**
Tenho terreno, mas não tenho capital.

Você não precisa ter todo o capital para começar. Comece estruturando, não construindo.

Sem projeto, orçamento e estudo de viabilidade, fica mais difícil conversar sobre capital. Na Mini Mentoria de Estruturação você aprende o passo a passo para estruturar um empreendimento turístico: potencial territorial, inteligência de mercado, conceito do empreendimento, estruturação do projeto, viabilidade financeira, preparação para potenciais investidores e possibilidade de parceria com a Zion.

O que você recebe: 9 módulos e 70 aulas e materiais, com 12 meses de acesso. Aulas gravadas, fichas e formulários interativos, e-books, planilhas de cálculo, kits e modelos (Kit do Investidor e kit de prompts) e o Dossiê de Desenvolvimento.

A Zion está em expansão e quer te conhecer. Ao estruturar o seu projeto na mentoria, você pode cadastrar o seu terreno no banco de áreas da Zion (é opcional, e o seu projeto só é apresentado com a sua autorização). Se fizer sentido, podemos conversar sobre parceria e, a critério da Zion, apresentar você a investidores e à nossa rede.

O caminho: inscreva-se, receba o acesso, aprenda, estruture, gere seu Dossiê e apresente à Zion.

Cada projeto passa por análise da Zion. Parcerias, investimentos e conexões são possibilidades, não garantias. R$ 47, pagamento único, Pix ou cartão à vista, com reembolso em 7 dias.

**Headline:** Estruture antes de buscar capital (33)
**Descrição:** Mini Mentoria de Estruturação · R$ 47

## ZC2-MM47-02-DESTINO
**Texto primário**
Transforme seu terreno em um destino turístico.

Um terreno bonito ainda não é um destino. Antes, ele precisa de conceito e de projeto.

Na Mini Mentoria de Estruturação você aprende o passo a passo para estruturar um empreendimento turístico: potencial territorial, inteligência de mercado, conceito do empreendimento, estruturação do projeto, viabilidade financeira, preparação para potenciais investidores e possibilidade de parceria com a Zion.

O que você recebe: 9 módulos e 70 aulas e materiais, com 12 meses de acesso. Aulas gravadas, fichas e formulários interativos, e-books, planilhas de cálculo, kits e modelos (Kit do Investidor e kit de prompts) e o Dossiê de Desenvolvimento.

A Zion está em expansão e quer te conhecer. Ao estruturar o seu projeto na mentoria, você pode cadastrar o seu terreno no banco de áreas da Zion (é opcional, e o seu projeto só é apresentado com a sua autorização). Se fizer sentido, podemos conversar sobre parceria e, a critério da Zion, apresentar você a investidores e à nossa rede.

O caminho: inscreva-se, receba o acesso, aprenda, estruture, gere seu Dossiê e apresente à Zion.

Cada projeto passa por análise da Zion. Parcerias, investimentos e conexões são possibilidades, não garantias. R$ 47, pagamento único, Pix ou cartão à vista, com reembolso em 7 dias.

**Headline:** Do terreno ao destino turístico (31)
**Descrição:** Mini Mentoria de Estruturação · R$ 47

## ZC2-MM47-03-PARTICIPACAO
**Texto primário**
Sua terra pode ser sua participação.

Em uma parceria, a terra pode ser a participação do proprietário. O formato depende da análise da Zion, que está em expansão e avalia cada projeto.

Para chegar a essa conversa, o terreno precisa virar projeto. Na Mini Mentoria de Estruturação você aprende o passo a passo para estruturar um empreendimento turístico: potencial territorial, inteligência de mercado, conceito do empreendimento, estruturação do projeto, viabilidade financeira, preparação para potenciais investidores e possibilidade de parceria com a Zion.

O que você recebe: 9 módulos e 70 aulas e materiais, com 12 meses de acesso. Aulas gravadas, fichas e formulários interativos, e-books, planilhas de cálculo, kits e modelos (Kit do Investidor e kit de prompts) e o Dossiê de Desenvolvimento.

A Zion está em expansão e quer te conhecer. Ao estruturar o seu projeto na mentoria, você pode cadastrar o seu terreno no banco de áreas da Zion (é opcional, e o seu projeto só é apresentado com a sua autorização). Se fizer sentido, podemos conversar sobre parceria e, a critério da Zion, apresentar você a investidores e à nossa rede.

O caminho: inscreva-se, receba o acesso, aprenda, estruture, gere seu Dossiê e apresente à Zion.

Cada projeto passa por análise da Zion. Parcerias, investimentos e conexões são possibilidades, não garantias. R$ 47, pagamento único, Pix ou cartão à vista, com reembolso em 7 dias.

**Headline:** Sua terra pode entrar no projeto (32)
**Descrição:** Mini Mentoria de Estruturação · R$ 47

## ZC2-MM47-04-AIRBNB
**Texto primário**
Quero construir um Airbnb, mas não sei por onde começar.

Antes de construir, é preciso saber o que construir, onde, para quem e se o projeto fecha as contas. Comece estruturando, não construindo.

Na Mini Mentoria de Estruturação você aprende o passo a passo para estruturar um empreendimento turístico: potencial territorial, inteligência de mercado, conceito do empreendimento, estruturação do projeto, viabilidade financeira, preparação para potenciais investidores e possibilidade de parceria com a Zion.

O que você recebe: 9 módulos e 70 aulas e materiais, com 12 meses de acesso. Aulas gravadas, fichas e formulários interativos, e-books, planilhas de cálculo, kits e modelos (Kit do Investidor e kit de prompts) e o Dossiê de Desenvolvimento.

A Zion está em expansão e quer te conhecer. Ao estruturar o seu projeto na mentoria, você pode cadastrar o seu terreno no banco de áreas da Zion (é opcional, e o seu projeto só é apresentado com a sua autorização). Se fizer sentido, podemos conversar sobre parceria e, a critério da Zion, apresentar você a investidores e à nossa rede.

O caminho: inscreva-se, receba o acesso, aprenda, estruture, gere seu Dossiê e apresente à Zion.

Cada projeto passa por análise da Zion. Parcerias, investimentos e conexões são possibilidades, não garantias. R$ 47, pagamento único, Pix ou cartão à vista, com reembolso em 7 dias.

**Headline:** Por onde começar seu Airbnb (27)
**Descrição:** Mini Mentoria de Estruturação · R$ 47

## ZC2-MM47-05-PARCEIRO
**Texto primário**
Seja um potencial parceiro Zion.

A Zion está em expansão e avalia cada projeto. Antes de qualquer conversa, o seu terreno precisa virar um projeto que dê para apresentar.

Na Mini Mentoria de Estruturação você aprende o passo a passo para estruturar um empreendimento turístico: potencial territorial, inteligência de mercado, conceito do empreendimento, estruturação do projeto, viabilidade financeira, preparação para potenciais investidores e possibilidade de parceria com a Zion.

O que você recebe: 9 módulos e 70 aulas e materiais, com 12 meses de acesso. Aulas gravadas, fichas e formulários interativos, e-books, planilhas de cálculo, kits e modelos (Kit do Investidor e kit de prompts) e o Dossiê de Desenvolvimento.

A Zion está em expansão e quer te conhecer. Ao estruturar o seu projeto na mentoria, você pode cadastrar o seu terreno no banco de áreas da Zion (é opcional, e o seu projeto só é apresentado com a sua autorização). Se fizer sentido, podemos conversar sobre parceria e, a critério da Zion, apresentar você a investidores e à nossa rede.

O caminho: inscreva-se, receba o acesso, aprenda, estruture, gere seu Dossiê e apresente à Zion.

Cada projeto passa por análise da Zion. Parcerias, investimentos e conexões são possibilidades, não garantias. R$ 47, pagamento único, Pix ou cartão à vista, com reembolso em 7 dias.

**Headline:** Seja um potencial parceiro Zion (31)
**Descrição:** Mini Mentoria de Estruturação · R$ 47


## 11. Público-alvo e proposta comercial
- Persona: dono de terreno em destino turístico no Brasil, sem capital suficiente e sem saber por onde começar a estruturar um empreendimento (glamping/pousada/cabanas/Airbnb), 25 a 65 anos.
- Proposta: formação digital de R$ 47 que leva o proprietário a montar seu Dossiê de Desenvolvimento, passo a passo, por 7 pilares; cadastro opcional do terreno no banco de áreas da Zion; a Zion está em expansão e avalia cada caso (parceria/investimento = possibilidade, nunca garantia).
- Segmentação da campanha atual: Brasil, 25–65, interesses/comportamentos copiados da LT47 (interesse "Inversiones inmobiliarias", comportamentos "Frequent international travelers" e "Recently Detected Iphone 14 Devices", cargo "Empresário"); posicionamentos manuais sem Audience Network (FB feed/stories/reels; IG feed/stories/reels/explore); Advantage+ audience desligado.
- Públicos existentes na conta: "Público Zion 90" 120250455830270016, "Público video" 120250455897500016, "Zion collection 365" 120250455931010016 (usados no remarketing); lista própria "Base_Zion_Meta_Email_Telefone_Nome.csv" (única fonte de venda de e-book em 31/07/2026, por Purchase, ROAS 0,24). Sugestão da auditoria: testar a base própria (público quente) com preço no texto.

## 12. Conta de anúncios recomendada
- Zion Collection 2: ID 1271873041294684. Página do Facebook 576944608845537. Instagram: o ligado à página. Pixel 903918118859018. Conta de leads (facebook_leads): 576944608845537. Outras contas: Zion Bubble 1767208367384473, Bruno Ch, BRUNO 01.
- Campanhas na conta (estado em 25/11 ~01h BRT): 
  - Mini Mentoria 120250559484620016 "[ZC2][TRAFEGO][MINI MENTORIA 47][DESENVOLVIMENTO]" LIGADA, objetivo Tráfego, otimiza LANDING_PAGE_VIEWS, conjunto 120250559488770016 R$ 30/dia (Brasil 25–65), anúncios 01 CAPITAL 120250559495520016, 02 DESTINO ...496680016, 03 PARTICIPACAO ...499010016, 04 AIRBNB ...502270016, 05 PARCEIRO ...503550016. [Estado lido de volta: NÃO CONFIRMADO; cache do Windsor.] Aprovada por Bruno para ligar em 25/11.
  - LT47 120250557994600016: PAUSADA em 25/11 (otimizava ViewContent, que não dispara).
  - Venda direta 120250538576770016 (rótulo "R$ 97", destino /inscricao-47 = R$ 47): LIGADA, otimiza INITIATED_CHECKOUT, R$ 50/dia (30+20), Audience Network consome a maior parte do gasto.
  - Formulário R$ 47 120250557420830016: LIGADA, R$ 30/dia, lead nativo, 1 lead até agora.
  - Captação R$ 270 120250521777310016: PAUSADA (CPL ~R$ 2,47; mensagens da Bela/Zaya/abertura incoerentes).
- Orçamento diário ligado: ~R$ 110 (Mini Mentoria 30 + venda direta 50 + formulário 30).

## 13. Status dos testes
- Pagamento: a compra de teste de Bruno em R$ 47 (Pix, 24/11 19:12Z, oferta 668391e7) foi paga. Bruno informou em 25/11 que "o pagamento está funcionando". Para a oferta da Mini Mentoria (0c71eeba) NÃO há venda registrada ainda: pagamento Pix/cartão desta oferta [NÃO CONFIRMADO]; cartão sem nenhuma transação registrada em lugar nenhum. O ambiente do Claude bloqueia payments.clickmax.io (403), então o quadro de pagamento nunca foi visto pelo Claude.
- Rastreamento: NÃO validado (ver 6, 7, 8). Meta mostra 0 compras mesmo com 2 vendas reais de R$ 97 em 24/11.
- Entrega automática: comprovada com as 2 vendas reais de R$ 97 (acesso criado em 1–2 min na turma). Para a oferta nova (produto separado) não está provada de ponta a ponta; a entrega configurada é só a turma 087479a3. Nenhum fluxo de pós-compra (e-mail/tag/card/tarefa) está ligado para R$ 47/Mini Mentoria (fluxo fcc14b4d só cobre a oferta R$ 97 e está em rascunho).

## 14. UTMs e webhooks
- UTM padrão dos anúncios da Mini Mentoria (url_tags): utm_source=meta&utm_medium=paid&utm_campaign=mm47&utm_content=<ZC2-MM47-01-CAPITAL | 02-DESTINO | 03-PARTICIPACAO | 04-AIRBNB | 05-PARCEIRO>&utm_term={{ad.id}}&sck={{campaign.id}}&ad_id={{ad.id}}&campaign_id={{campaign.id}}. A página repassa os parâmetros ao iframe do checkout [CONFIRMADO em teste]. A venda guarda utmSource/Medium/Campaign/Content/Term, src e sck; NÃO guarda ad_id/campaign_id (por isso utm_term e sck carregam os ids).
- PROBLEMA: as 2 vendas reais de 24/11 vieram com todos os campos UTM nulos; não se sabe se a causa é a URL dos anúncios sem UTM ou a Ticto não devolver. A gravação de UTM numa venda real ainda NÃO foi provada.
- Webhooks: nenhum webhook de Meta/Asaas configurado para estas ofertas (gateway Ticto; Asaas só em um fluxo rascunho sem execuções). Existe webhook das fichas do curso (ZION_WEBHOOK_URL) para o Airtable (automação "Página do Dossiê chegou do curso", implantada, não testada). Hotmart: integração NÃO conectada no ClickMax.

## Pendências técnicas (ordem de importância)
1. Provar que o Purchase só dispara com pagamento aprovado e que chega ao Meta (Testar eventos; Pix de teste; token da CAPI; deduplicação; dataset).
2. Decidir o evento de otimização: hoje Tráfego/LPV (Mini Mentoria) e INITIATED_CHECKOUT (venda direta), nenhum otimiza Purchase; ViewContent desligado nas páginas.
3. Garantir UTM gravada na venda real (comprovar com uma venda).
4. Extrato da Ticto (22–25/11): Pix expirado, recusas, abandono, códigos de pedido, UTMs recebidas; taxa de cartão (sem dado; Pix R$ 47 paga R$ 2,49, líquido R$ 44,51).
5. Configurar no painel o redirecionamento do checkout para /obrigado-plataforma (e corrigir os textos R$ 97 dela) e remover o portal antigo da oferta R$ 47 antiga.
6. Pós-compra todo em rascunho: e-mail, tag, card e tarefa; WhatsApp pós-compra (clube_pos_compra) não existe.
7. Bela (agente ativo) proíbe oferecer o produto de R$ 47 e fala em R$ 97; Zaya oferece reunião grátis; abertura antiga citou R$ 270: mensagens incoerentes com a oferta.
8. Tráfego de servidor (~40% das visitas de 24/11, sessão ≤3 s, IPs da infraestrutura da Meta e de nuvem): filtrar na análise; Audience Network com CPM de R$ 240–268 na venda direta.
9. Conta de vendedor ClickMax ainda "pending".
10. Formulários antigos da conta citam "R$ 350 mil de faturamento por bubble" e rentabilidade de 30–35% a.a. [HIPÓTESE de estar em anúncio ativo]: promessas proibidas.
11. Barra fixa do botão: o ClickMax removeu o padding de segurança do iPhone (pode ficar rente à barra de gestos).

## Métricas de referência (24/11, Windsor, cache pode atrasar; dia parcial)
- Gasto da conta ~R$ 152 (R$ 59,9 da captação R$ 270 antes de pausar). 2 vendas reais de R$ 97; 0 de R$ 47; 0 compras no Meta.
- Funil ClickMax 24/11: 321 visitantes (183 BR + 140 tráfego de servidor "US") → 4 Pix gerados → 4 pagos (2 reais + 2 testes de Bruno). Conversão visita→Pix: 0,62% sem testes (2/321); 1,09% só BR.
- Venda direta (R$ 69,98): 125 cliques, 89 LPV, 96 IC, 0 compras. Melhores criativos: Vídeo 02 curta (CTR ~21%) e longa (~19%).
- LT47 (R$ 16,98): 34 cliques, 24 LPV, 24 IC; melhor CTR 04-EXPANSAO.
- Líquido por venda: R$ 47 → R$ 44,51; R$ 97 → R$ 87,73. CPA máximo antes de imposto: R$ 44,51 e R$ 87,73. CAC real incomprovável sem UTM (cenários R$ 35–R$ 105).
- Relatório completo da auditoria (13 seções): arquivo RELATORIO_FINAL.md entregue a Bruno (anexar na conversa).
- Campanha de e-book que vendeu (Meta): "[360][ebook][ofertadireta][vendas][site][16/07]" (id 120248288047820016): Vendas, otimiza PURCHASE, base própria, R$ 15/dia, 2 compras de pixel em 31/07/2026, gasto R$ 347,51, ROAS ~0,24.
