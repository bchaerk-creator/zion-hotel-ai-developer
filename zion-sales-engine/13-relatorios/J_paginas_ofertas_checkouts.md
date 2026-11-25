# Auditoria J · Páginas de venda, ofertas e checkouts (Infoprodutos Zion)

Somente leitura, 25/11/2026. Nada foi alterado, publicado, despublicado, arquivado ou apagado. Nenhum pedido criado, nenhum dado pessoal usado. Fontes: ClickMax MCP (pages_list, pages_get/checkouts_get, pages_tracking_status, products_list, offers_get, offers_get_incomplete_reason, portals_list, classrooms_list, funnels_list, flows_list, flows_structure_get, sellers_status) e Playwright (celular 390x844) nas páginas públicas. Marcação: **[E]** evidência medida, **[H]** hipótese. Reaproveito a auditoria B (páginas de inscrição) e a A (anúncios) já na pasta; o que vem delas está marcado.
Limites: o checkout em si (payments.clickmax.io) é bloqueado pelo proxy deste ambiente, então não foi aberto. "Visitas 7 dias" = `recentPageViews` do tracking (janela de 7 dias, não separa orgânico de pago). `analytics_sales_pages` não foi usado (o tracking por página já dá o dado). Contagem de redirecionamento pós-compra: o `offers_get` não expõe campo de redirecionamento.

## 0. Resumo executivo

- Projeto: 71 páginas (62 sales, 4 thankYou, 3 checkout, 1 quiz, 1 capture); **28 publicadas** (27 sales + 1 thankYou), 43 rascunhos. `pixelViewContent` = false nas 71 [E]. 64 produtos, 67 ofertas.
- Vendedor: `sellerStatus` pending, banco approved, `canSell` true, gateway ticto [E]. Gateway sincroniza ofertas aprovadas só se não tiver `providerSyncError`: 17 ofertas ainda com "Token inválido ou ausente" [E] (nenhuma delas está ligada a página publicada).
- Todas as 28 páginas publicadas: o hash do iframe do checkout bate com a oferta ligada à página (27 de 27 que têm iframe; as 3 páginas do Club antigo não têm iframe) [E].
- Os 3 achados mais graves: (1) página publicada /curso-terreno-destino-turistico (207 visitas em 7 dias, a mais visitada) liga a oferta **arquivada** de R$ 47; (2) página publicada /etapa-desenvolvimento (26 visitas) liga oferta de **R$ 290 em `pending_corrections`** (12x R$ 24,17 na página); (3) /club/planos publicada com **R$ 270 / R$ 980 / R$ 2.900** e link de pagamento Asaas, título "(Copy)".
- Ofertas de R$ 47 e R$ 97 que de fato recebem tráfego: 5 (seção 5), todas `approved`, sem erro de sincronização, gateway ticto. Nenhuma tem fluxo de pós-compra ativo; o fluxo do R$ 97 está em rascunho e nada existe para R$ 47.

## 1. Inventário de páginas (71)

Colunas: id (8 primeiros), nome, path, tipo, estado, offerId (8 primeiros), produto (8 primeiros), preço da oferta, hash do checkout, status da oferta (SYNCERR = erro de sincronização do gateway), visitas 7 dias, visitas totais acumuladas, oferta com transação (`hasTransaction`, pode incluir teste/pendente: [H] sobre natureza). Data de publicação = `lastPublishedAt`. Páginas rascunho respondem 404 no endereço público [E, amostra de 9].

| id | nome | path | tipo | estado | offerId | produto | preço | hash | status oferta | vis. 7d | vis. total | oferta c/ transação |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8060255e | Mini Mentoria de Performance Hoteleira | /mini-mentoria-performance | sales | rascunho | ca1d914c | d8a2348e | R$ 47 | S8De0erMoM | approved | 0 | 0 | não |
| be23f04a | Zion Collection · Inscrição (Cadastro de Projetos) (Copy) (Cop | /mini-mentoria | sales | publicada 2026-11-25 | 0c71eeba | cbbb5fb1 | R$ 47 | yhyiqUB9OF | approved | 51 | 51 | não |
| 066b2cb9 | Zion Collection · Inscrição (Cadastro de Projetos) (Copy) (Cop | /parceiro-zion | sales | publicada 2026-11-25 | 668391e7 | 072083e8 | R$ 47 | z3a0AEkvRl | approved | 72 | 72 | não |
| 828beb3b | Zion Collection · Inscrição (Cadastro de Projetos) (Copy) (Cop | /inscricao-dossie | sales | publicada 2026-11-24 | 668391e7 | 072083e8 | R$ 47 | z3a0AEkvRl | approved | 9 | 9 | não |
| fb1e89b9 | Zion Collection · Inscrição (Cadastro de Projetos) (Copy) (Cop | /inscricao-47 | sales | publicada 2026-11-25 | 668391e7 | 072083e8 | R$ 47 | z3a0AEkvRl | approved | 196 | 196 | não |
| d7166fc3 | Zion Collection · Obrigado Plataforma | /obrigado-plataforma | thankYou | publicada 2026-11-24 | null | - | - | - | - | 2 | 2 | - |
| 1597b2cc | Zion Collection · Inscrição (Cadastro de Projetos) (Copy) | /inscricao-curta | sales | publicada 2026-11-25 | c298aaed | 072083e8 | R$ 97 | 1ApwIsdYSy | approved | 105 | 105 | não |
| d6b63999 | Zion Collection Club · Acesso à plataforma (R$ 97) · rascunho | /inscricao-97 | sales | rascunho | c298aaed | 072083e8 | R$ 97 | 1ApwIsdYSy | approved | 0 | 0 | não |
| 77c286e6 | Zion Collection · Inscrição (Cadastro de Projetos) | /inscricao | sales | publicada 2026-11-24 | c298aaed | 072083e8 | R$ 97 | 1ApwIsdYSy | approved | 183 | 183 | não |
| 3bf6dd22 | Sessão Zion 360° · Expansão Brasil | /sessao-zion-360 | sales | rascunho | f16e61ac | 4ca336d4 | R$ 270 | 5q1Ndy1cIS | archived | 13 | 13 | não |
| de068af2 | Você tem terra. Falta capital? · Zion Hotel Academy (página B) | /terra-capital-b | sales | publicada 2026-11-21 | 338c9ed8 | ff15b3c0 | R$ 67 | k5ETStF7A7 | approved | 4 | 4 | não |
| bd7bf43d | Você tem terra. Falta capital? · Zion Hotel Academy | /terra-capital-a | sales | publicada 2026-11-21 | 1eb339a6 | ff15b3c0 | R$ 47 | Yqp_fxiRJl | approved | 12 | 12 | não |
| 6fa73e75 | Curso · Transforme seu terreno em um destino turístico | /curso-terreno-destino-turistico | sales | publicada 2026-11-21 | c91f1ff2 | 28021a97 | R$ 47 | IUVjj5Y-KR | archived | 207 | 207 | não |
| abfff20b | Ferramenta 24 · Assistente de IA para Atendimento | /assistente-atendimento | sales | publicada 2026-11-21 | 8ea1c87b | 1dfce039 | R$ 19 | VSiwxpwGew | approved | 0 | 0 | não |
| e3cdda59 | Etapa de Desenvolvimento · Checkout | /etapa-desenvolvimento | sales | publicada 2026-11-20 | 095e1914 | 53691d5e | R$ 290 | ftzIEt5sY_ | pending_corrections | 26 | 26 | não |
| e150beeb | Ferramenta 10 · Fechamento Mensal por Imóvel | /fechamento-mensal | sales | publicada 2026-11-20 | 2e335c78 | 2446ba99 | R$ 19 | 2BpmmqQLeG | approved | 0 | 0 | não |
| 4a1b7c4c | Ferramenta 28 · Planner de Capacidade e Atendimento | /capacidade-atendimento | sales | publicada 2026-11-19 | 2f851e16 | 0cf14c74 | R$ 19 | rcTdhslLRC | approved | 0 | 0 | não |
| 6abeac69 | Venda · Qual Cabana para o Meu Terreno? — E-book + Kit | /ebook-qual-cabana | sales | publicada 2026-11-19 | add69459 | 1a47cf61 | R$ 13 | vQ-m3t67Ex | approved | 1 | 1 | não |
| 1dda728d | Venda · Do Terreno ao Airbnb — E-book + Kit | /ebook-do-terreno-ao-airbnb | sales | publicada 2026-11-19 | 0afcefb4 | 92b71e84 | R$ 13 | wo5MSoDCzY | approved | 2 | 2 | não |
| d81d772f | Venda · Terreno Parado, Projeto com Sócio — E-book + Kit | /ebook-terreno-parado-socio | sales | publicada 2026-11-19 | 3852a88a | 5ca4d2e4 | R$ 13 | 9QWCrhlLZl | approved | 3 | 3 | não |
| ba973c0c | Ferramenta 16 · Kit Operacional de Parcerias | /kit-parcerias | sales | publicada 2026-11-18 | eca8f010 | f106fa17 | R$ 19 | pAGdV-2yw1 | approved | 0 | 0 | não |
| cc7b6b14 | Ferramenta 23 · Kit de Roteiros de Conteúdo e Vídeos | /roteiros-conteudo | sales | publicada 2026-11-17 | b0f2a1e3 | 74ea712d | R$ 19 | ujYWp_XYpj | approved | 0 | 0 | não |
| b964111c | Kit Primeira Cabana · R$ 47 | /kit-primeira-cabana | sales | rascunho | 1a6a5acb | a84cf626 | R$ 47 | -5ovThQv35 | approved | 0 | 0 | não |
| e23ecfe2 | Ferramenta 22 · Planner de Campanhas para Períodos de Baixa Pr | /campanhas-baixa-procura | sales | publicada 2026-11-16 | b34854f5 | e9a5c19f | R$ 19 | DVd1Z5pOef | approved | 0 | 0 | não |
| ee0a4b0e | Ferramenta 12 · Checklist de Fotos e Comodidades do Anúncio | /fotos-comodidades | sales | publicada 2026-11-15 | 1651f122 | d2c18a5d | R$ 19 | BduC1TgySd | approved | 0 | 0 | não |
| 3182a2d0 | Ferramenta 19 · Controle de Compras e Consumo Interno | /controle-compras | sales | publicada 2026-11-14 | 6c4de218 | be520313 | R$ 19 | Ni8Incw1xB | approved | 0 | 0 | não |
| ac3388c6 | Ferramenta 15 · Comparador de Fornecedores | /comparador-fornecedores | sales | publicada 2026-11-13 | 8b5e30b2 | ee019a14 | R$ 19 | CDr4NA5HC6 | approved | 0 | 0 | não |
| 14ab1a6a | Zion Collection 06 · Seu Airbnb Está Vazio? · R$ 47 (rascunho) | /seu-airbnb-esta-vazio | sales | rascunho | 75c27213 | 4b088fcf | R$ 47 | QiaIwmZOFC | approved | 0 | 0 | não |
| 7531d1b2 | Ferramenta 30 · Gerador de Briefing de Experiência | /briefing-experiencia | sales | publicada 2026-11-12 | f28b840b | ba7395b4 | R$ 19 | IO3t7_0ZHV | approved | 0 | 0 | não |
| 5e0d2e63 | Parceiro · Entrada no clube · Checkout R$ 97 | /crfXyfBMfqiQ9mvNWa54k | checkout | rascunho | null | - | - | - | - | 0 | 0 | - |
| c03eb47f | Agenda da equipe Zion (reunião) | /rU9XGY3jRuxsyehcH0RzJ | thankYou | rascunho | null | - | - | - | - | 0 | 0 | - |
| 77de73d2 | Parceiro · Formulário de situação (6 perguntas) | /Iadmm6dd3r8ojUdrHbMdt | quiz | rascunho | null | - | - | - | - | 0 | 0 | - |
| 9d1aee54 | Parceiro · Landing (zionhotelgroup.com/parceiro) | /x8uT9tGPfgYIUTjq8PcDP | capture | rascunho | null | - | - | - | - | 0 | 257 | - |
| 275fe570 | Clube · Alinhamento + agenda (página de agendamento) | /d66jfBtHc-KO0CZgYOW2b | thankYou | rascunho | null | - | - | - | - | 0 | 0 | - |
| ac57f756 | Clube · Checkout R$ 97 (ClickMax) | /SFOhLK0UqN9tD8TV3DkqR | checkout | rascunho | null | - | - | - | - | 0 | 0 | - |
| ce137aea | Clube · Landing (zionhotelgroup.com/clube) | /SRrKJg03ivD0DbbBxQGel | sales | rascunho | null | - | - | - | - | 29 | 132 | - |
| c3670c67 | Ferramenta 20 · Kit de Treinamento do Primeiro Turno | /treinamento-primeiro-turno | sales | publicada 2026-11-11 | e1cda5e6 | fcb2b52e | R$ 19 | AzLhCjcBtK | approved | 2 | 2 | não |
| 5c8911fb | Ferramenta 18 · Planner de Manutenção Preventiva | /manutencao-preventiva | sales | rascunho | a7beacee | ec984b9b | R$ 19 | 9EgkyYXxs_ | approved+SYNCERR | 0 | 0 | não |
| 618d5a9b | Ferramenta 05 · Orçamento da Cabana | /orcamento-cabana | sales | rascunho | a09778db | 49a1249e | R$ 19 | aQxGaFEShH | approved | 0 | 0 | não |
| 9aadd649 | Ferramenta 29 · Custos de Experiências | /custos-experiencias | sales | rascunho | a52ce33e | 8ac4c7b3 | R$ 19 | zMFmcFiYq_ | approved+SYNCERR | 0 | 0 | não |
| e78dfdca | Ferramenta 01 · Planilha Diária Mínima · Venda R$ 19 | /diaria-minima | sales | rascunho | 974727ce | 23d17f13 | R$ 19 | -e5nx6Wvi9 | incomplete+SYNCERR | 0 | 0 | não |
| 493d6f48 | B10 · Como Apresentar Minha Terra para Sócios e Investidores?  | /zar-b10 | sales | rascunho | c99834fe | 800ce650 | R$ 27 | UfCzHr90AJ | incomplete+SYNCERR | 0 | 0 | não |
| 9925d5ea | B09 · Como Começar um Projeto Turístico com Pouco Capital? · V | /zar-b09 | sales | rascunho | ad75e119 | 05ff0185 | R$ 27 | 4ikeRL1ZDB | approved | 0 | 0 | não |
| 7aaea445 | A08 · Quanto Você Deixa de Ganhar com Cada Hóspede? · Venda R$ | /zar-a08 | sales | rascunho | c377b2bc | dfd5a6bb | R$ 27 | nvG6nEEREG | approved | 0 | 0 | não |
| ffbafeaa | B08 · Como Calcular o Retorno de um Projeto Turístico? · Venda | /zar-b08 | sales | rascunho | bb48dcf4 | 036cc375 | R$ 27 | bGYBQgSYnC | incomplete+SYNCERR | 0 | 0 | não |
| 155cf61d | B04 · Tenho Terra, mas Não Tenho Dinheiro. E Agora? · Venda R$ | /zar-b04 | sales | rascunho | c2d62b6e | 693d5535 | R$ 27 | UMLnQpZR2u | incomplete+SYNCERR | 0 | 0 | não |
| 10010ff8 | A07 · Você Está Perdendo Reservas no Atendimento? · Venda R$ 2 | /zar-a07 | sales | rascunho | a45f642c | 1b13e6af | R$ 27 | ei3JNcZpzt | approved | 0 | 0 | não |
| 349fc9c1 | B07 · Qual Hospedagem Construir no Meu Terreno? · Venda R$ 27 | /zar-b07 | sales | rascunho | 36e4354d | 5062c10b | R$ 27 | Cd0sSzRXaU | approved | 0 | 0 | não |
| 94561896 | B03 · Como Criar um Projeto de Hospedagem Mesmo Sem Dinheiro?  | /zar-b03 | sales | rascunho | 7fb9cb7d | 30784e11 | R$ 27 | hreVBmnEl7 | approved | 0 | 0 | não |
| d0f8ceac | A06 · Por Que Seus Hóspedes Não Dão 5 Estrelas? · Venda R$ 27 | /zar-a06 | sales | rascunho | 49e9edff | 29248a7f | R$ 27 | 2mnKe_GNte | approved | 0 | 0 | não |
| 158bb5a5 | B06 · Como Saber Quanto Custa Construir uma Hospedagem? · Vend | /zar-b06 | sales | rascunho | b1894587 | c6f0dcc3 | R$ 27 | gwCKS07Azu | incomplete+SYNCERR | 0 | 0 | não |
| d577ebe1 | B02 · Como Atrair um Sócio para Desenvolver Minha Terra? · Ven | /zar-b02 | sales | rascunho | a6dace7c | 878c421d | R$ 27 | gg1fqEpX6l | incomplete+SYNCERR | 0 | 0 | não |
| b979b34a | A05 · Como Fazer Sua Hospedagem Valer Mais? · Venda R$ 27 | /zar-a05 | sales | rascunho | 7693376d | d0be6330 | R$ 27 | HD8SZHwRQy | approved | 0 | 0 | não |
| 4d32714f | A04 · Seu Anúncio Está Afastando Hóspedes? · Venda R$ 27 | /zar-a04 | sales | rascunho | e1a97579 | 1226161b | R$ 27 | pm4gC73OBW | approved | 0 | 0 | não |
| f02554ad | B05 · Como Descobrir o Potencial Turístico da Minha Terra? · V | /zar-b05 | sales | rascunho | 8089d5f6 | 400fee7a | R$ 27 | 5bZM1XhAf8 | incomplete+SYNCERR | 0 | 0 | não |
| a91f9964 | B01 · Como Atrair Investimentos para Minha Terra que Está Para | /zar-b01 | sales | rascunho | fb92b3d5 | 60f20d8f | R$ 27 | jJf-ANO_iD | incomplete+SYNCERR | 0 | 0 | não |
| 26aefd11 | A03 · Sua Hospedagem Fatura, mas Dá Lucro? · Venda R$ 27 | /zar-a03 | sales | rascunho | ca0852f1 | 5d37cec4 | R$ 27 | cUzIUJQ1ol | approved | 0 | 0 | não |
| 214ef113 | A10 · Sua Hospedagem Só Funciona com Você? · Venda R$ 27 | /zar-a10 | sales | rascunho | 6f2dfac2 | 3f642634 | R$ 27 | zUjBfQ9hEl | approved | 0 | 0 | não |
| c6a56cf3 | A09 · Vale a Pena Investir em uma Cabana ou Airbnb? · Venda R$ | /zar-a09 | sales | rascunho | fa8a9a32 | bc04f0d0 | R$ 27 | Dv_F82gBPs | incomplete+SYNCERR | 0 | 0 | não |
| feb343db | Ferramenta 14 · Quadro de Ocorrências | /quadro-ocorrencias | sales | rascunho | 74460a23 | 24e847f2 | R$ 19 | sdDDSurhAZ | approved+SYNCERR | 0 | 0 | não |
| 644d73f3 | Club Zion Collection · Planos | /club/planos | sales | publicada 2026-11-06 | null | - | - | - | - | 0 | 0 | - |
| 4791b65b | Club Zion Collection | /club | sales | publicada 2026-11-06 | null | - | - | - | - | 0 | 0 | - |
| 925b7055 | Club Zion Collection · Planos e checkout (Base, Master, Pro) | /sd4HXeHfLsF82452FkzXl | checkout | rascunho | null | - | - | - | - | 0 | 0 | - |
| 6e9ce423 | Club Zion Collection · Home (entrada do Meta) | /kuTFCUfFFF3crBFS0vcEn | sales | rascunho | null | - | - | - | - | 0 | 0 | - |
| d816d6db | Ferramenta 13 · Controle de Enxoval | /controle-enxoval | sales | rascunho | b667369e | 59742f6f | R$ 19 | aIN6h2A0bT | approved+SYNCERR | 0 | 0 | não |
| b4de9375 | Vitrine · Zion Collection Club · Hotel Business Academy (20 mi | /zion-collection-club | sales | publicada 2026-11-07 | null | - | - | - | - | 0 | 1 | - |
| a2683126 | ZAR-A02 · Quanto Devo Cobrar pela Minha Diária? · Venda R$ 27 | /zar-a02 | sales | rascunho | f44d1d87 | 59aafa84 | R$ 27 | 3t5odnLVmc | approved | 0 | 0 | não |
| 10432164 | ZAR · TESTE técnico de script (não publicar) | /zar-teste-script | thankYou | rascunho | null | - | - | - | - | 0 | 0 | - |
| 545010c0 | Ferramenta 11 · Kit de Mensagens | /kit-mensagens | sales | rascunho | fad5df5a | 99a12f38 | R$ 19 | X4mTsfhUtb | approved+SYNCERR | 0 | 0 | não |
| 023476bb | Ferramenta 17 · Checklist de Limpeza | /checklist-limpeza | sales | rascunho | 08ad22e8 | 9545b75a | R$ 19 | uB0Db7Gpg4 | approved+SYNCERR | 0 | 0 | não |
| 82e1bb5f | Academy 01 · Seu Airbnb Está Vazio? · Venda R$ 27 | /academy-01 | sales | rascunho | 1ff56fea | 5b4bf1f6 | R$ 27 | ySAkZG38VS | incomplete+SYNCERR | 0 | 0 | não |

## 2. Achados (ordenados por gravidade)

### P0 / P1

**J-01 · P0 · Página publicada com tráfego liga oferta ARQUIVADA** [E]
- /curso-terreno-destino-turistico (id 6fa73e75): publicada 21/11, 207 visitas em 7 dias, última visita 23/11; iframe `payments.clickmax.io/custom/6fa73e75…/IUVjj5Y-KR`; oferta c91f1ff2 "Transforme seu terreno em um destino turístico · Curso passo a passo" R$ 47 com `status: archived`. A página exibe "R$ 47 · pagamento único · Pix ou cartão".
- [H] checkout de oferta arquivada não vende (não testado, checkout bloqueado aqui): quem chegar nessa página (campanhas pausadas antigas, links salvos) não consegue pagar.
- Correção proposta: decidir com Bruno se a oferta volta (desarquivar) ou se a página é despublicada/redirecionada para /inscricao-47 ou /parceiro-zion. Esforço: baixo (15 min).

**J-02 · P0 · Página publicada liga oferta de R$ 290 não aprovada** [E]
- /etapa-desenvolvimento (id e3cdda59): publicada 20/11, 26 visitas, última 24/11; oferta 095e1914 R$ 290 (`originalPrice 29000`), `status: pending_corrections`, `incompleteReason` vazio; página mostra "12x de R$ 24,17" e "Entrar e começar o passo a passo". Entrega: classroom a490c3c8 do portal "Zion · Jornada do Desenvolvimento" (turma antiga "Estruturação · Etapa de Viabilidade…", 4 membros, 119 aulas).
- Esta linha de preço (R$ 290) é obsoleta pela regra do projeto (R$ 47/R$ 97 atuais). Sem Pix/cartão confirmado por mim [H].
- Correção: despublicar a página (ou trocar a oferta) e arquivar a oferta depois de decidir; proposta abaixo. Esforço: baixo.

**J-03 · P1 · /club/planos e /club publicadas com preços e checkout antigos** [E]
- /club/planos (id 644d73f3, publicada 06/11, `<title>` "Club Zion Collection · Planos (Copy)"): R$ 45/mês ou R$ 270 à vista, R$ 81,67 ou R$ 980, R$ 241,67 ou R$ 2.900; links para `asaas.com/000/c/zrhq4rk88iyta3id`; offerId null. /club (id 4791b65b, título "(Copy)"): "R$ 45 … R$ 81,67 … R$ 241,67", H1 "entre para o clube". Texto "possibilidade de parceria e de investimentos" (promessa sensível). 0 visitas em 7 dias, última visita nunca registrada.
- Atenção: o CLAUDE.md manda não mexer no Clube/Asaas; é só relatório. Correção proposta: Bruno decide (manter, despublicar). Esforço: baixo.

**J-04 · P1 · Vitrine publicada linka 20 páginas não publicadas (404)** [E]
- /zion-collection-club (id b4de9375, publicada 07/11, 1 visita total): R$ 27 em cada cartão e 20 links (`/academy-01`, `/zar-a02`…`/zar-b10`). As páginas destino estão em rascunho e respondem 404 (testei /academy-01 e /zar-a02). Ofertas R$ 27 existem (algumas `incomplete`/SYNCERR). 
- Correção: despublicar a vitrine ou publicar o que for vender. Esforço: baixo.

**J-05 · P1 · Entrega duplicada em dois portais, turmas chamadas "(R$ 97)" para compradores de R$ 47** [E]
- Ofertas R$ 97 (c298aaed) e R$ 47 (668391e7) e a oferta órfã 74a3f8c6 entregam em DUAS turmas com o mesmo conteúdo (content 79d3e792, 70 aulas): portal Zion Collection (a8e2157a) turma 69345987 "Zion Collection Club · Plataforma (R$ 97)" e portal Plataforma Zion Collection (3ef7a340) turma 087479a3 "Plataforma de estruturação (R$ 97)". Cada comprador ganha duas contas/acessos e vê "(R$ 97)" no nome da turma se o nome aparecer [H sobre visibilidade]. A /obrigado-plataforma aponta só para zion-plataforma.
- Preço diferente (R$ 47 x R$ 97) com entrega idêntica [E]: um clone de oferta, não um produto diferente.
- Correção: escolher um portal canônico, remover o segundo deliverable das ofertas novas, renomear a turma sem preço (a mudança de nome de turma não afeta quem já comprou). Esforço: médio (portal + testar com compra real/convite).

**J-06 · P1 · Sem pós-compra ativo para as ofertas que vendem hoje** [E]
- Fluxo "Clube R$ 97 (plataforma) · Compra aprovada → acesso, ficha e equipe" (fcc14b4d) está em **rascunho**, filtrado só para offerId c298aaed (R$ 97); tem grantClassroomAccess, tag, oportunidade e mensagem. Nenhum fluxo cobre a oferta R$ 47 (668391e7), Mini Mentoria (0c71eeba) nem Kit/terra-capital. Fluxos de pagamento ativos apontam para ofertas **arquivadas**: "Inscrição 270 · Pagamento confirmado" (offerId 3a86e24c, arquivada), "Inscrição de Terreno ou Projeto · Pós-compra" (mesma), "Consultoria Zion 360 · Pós-compra" (offer f16e61ac, arquivada, 1 execução).
- O acesso à área de membros vem do `deliverable` da oferta (automático, [E] existe); o que falta é aviso/e-mail de acesso e tag de comprador personalizados [H: o e-mail padrão de acesso do ClickMax não foi verificado].
- Correção: ativar (com aprovação de Bruno) um fluxo único de pós-compra para as ofertas vigentes; desligar os fluxos de R$ 270. Esforço: médio. Nada foi ativado por mim.

### P2

**J-07 · P2 · Páginas /inscricao-* clonadas: 6 páginas para 3 ofertas** [E, auditoria B]
- Páginas (nomes com "(Copy)" até 5 vezes e `<title>` idêntico "Zion Collection · Inscrição (Cadastro de Projetos) (Copy)…"): /inscricao (R$ 97, 183 visitas), /inscricao-curta (R$ 97, 105), /inscricao-47 (R$ 47, 196), /parceiro-zion (R$ 47, 72), /inscricao-dossie (R$ 47, 9), /mini-mentoria (oferta própria R$ 47, 51). /inscricao-97 é rascunho duplicado de /inscricao-curta (mesma oferta c298aaed).
- Mesmas ofertas duplicam o texto "R$ 47/97" só no preço; /inscricao-47 e /inscricao-dossie quase idênticas (texto e oferta).
- Correção: consolidar (seção 6). Esforço: médio (manter 2, redirecionar anúncios, despublicar o resto).

**J-08 · P2 · Campanha nomeada "R$ 97" vende R$ 47** [E, auditoria A]
- Anúncios ativos (3 campanhas, 12 anúncios, R$ 96,55 gasto em 24/11, 0 compras) apontam para /inscricao-47 e /parceiro-zion (R$ 47); /inscricao e /inscricao-curta (R$ 97) seguem no ar sem anúncio ativo, mas com visitas em 7 dias (183 e 105) [E] vindas de campanhas pausadas/links [H].

**J-09 · P2 · Oferta órfã duplicada** [E]
- Oferta 74a3f8c6 "Mini Mentoria de Estruturação" (R$ 47, hash `lbpKjFcTMy`, `isMain: false`) está dentro do produto "Zion Collection Club | Acesso à plataforma" (072083e8), nenhuma página a usa, entrega nas duas turmas do Club; cópia da 0c71eeba (produto cbbb5fb1) que entrega só na 087479a3. Checkout público existe e vende [H].

**J-10 · P2 · Oferta aprovada com portal de entrega NÃO publicado** [E]
- Mini Mentoria de Performance Hoteleira: oferta ca1d914c R$ 47 `approved` (hash `S8De0erMoM`); página /mini-mentoria-performance em rascunho (não vende), mas o portal 41353f3c ("zion-raio-x-hospedagem") está com `publishedAt: null` e 0 membros. Risco se a oferta for usada antes de publicar o portal (comprador sem acesso). Também o checkout público da oferta já abre direto em payments.clickmax.io/S8De0erMoM [H].

**J-11 · P2 · Páginas publicadas sem preço escrito no texto** [E]
- /terra-capital-a e /terra-capital-b (R$ 47 e R$ 67 no iframe; no texto só R$ 220/30/50/200 mil de "dados fictícios"): as duas páginas têm texto idêntico (5.424 caracteres); preço só aparece dentro do checkout (hash correto: Yqp_fxiRJl R$ 47, k5ETStF7A7 R$ 67). A oferta A tem transação (`hasTransaction` true). 12 e 4 visitas, última em 21/11; portal "Zion Hotel Academy" publicado, 1 turma, 23 aulas.
- /inscricao-47 (R$ 47 em 1 selo) e /inscricao-curta (R$ 97 só no selo): ver auditoria B.

**J-12 · P2 · Ofertas aprovadas com `providerSyncError` (gateway)** [E]
- 17 ofertas com "Não autorizado. Token inválido ou ausente.": Ferramentas 01, 11, 13, 14, 17, 18, 29 (tool R$ 19), Arsenal R$ 27 (ySAkZG38VS, `incomplete`), Club Land Bank R$ 270 (36zciytFiY, `incomplete`), 8 ofertas ZAR R$ 27 (A09, B01..B08, B10 `incomplete`). Coerente com CLAUDE.md. 
- As 6 ofertas `approved` com erro (Ferramentas 11, 13, 14, 17, 18, 29) têm página em rascunho, então hoje ninguém cai nelas; /kit-parcerias etc. (publicadas) não têm erro. Se Bruno publicar as de erro, o checkout pode falhar [H].
- Correção: reenviar sincronização/abrir chamado ClickMax (fora do escopo). Esforço: depende do suporte.

**J-13 · P2 · Títulos/metadados** [E]
- `title` nulo em 69 de 71 páginas (a aba usa o nome interno); nomes com "(Copy)": 5 páginas (nome) + 2 (`<title>` /club, /club/planos). `description` nula, `favIcon` nula nas páginas amostradas; `pixelViewContent` false nas 71. Em /terra-capital-a/b o `title` está preenchido e igual nas duas.
- Correção: preencher `title`/`description` por página e decidir pixel (outra auditoria, C). Esforço: baixo.

### P3

**J-14 · P3 · Obsoletas no inventário** [E] Ofertas arquivadas (9): R$ 97 Land Bank (v_4pU5zNYj), R$ 270 (Club, Sessão 360 x3, Inscrição Terreno/Projeto), curso R$ 47 (IUVjj5Y-KR). Ofertas `pending_corrections`: Club Kit Captação R$ 97 (c40895ad) e Etapa de Desenvolvimento R$ 290. Linhas antigas: Mentoria Zion 360 (portal mentoria-zion, 11 turmas, 8 "Arquivo ·"), Land Bank (portal 6d7ceb1c, 7 membros), Club 97 antigo.

**J-15 · P3 · Páginas externas do funil Parceiros/Club (rascunho, publicado como funil)** [E] Funis "Parceiros Club" e "Club Collection" `published` com nós em `draft` e `needsRearrange`; páginas externas (`editorVersion external`) com `lastPageViewAt` de 17/11 (capture, 257 visitas totais) e 23/11 (Clube landing, 29 visitas em 7 dias, página `ce137aea` em rascunho mas com tráfego: o tráfego vai ao site externo zionhotelgroup.com via script, não ao ClickMax [H]).

**J-16 · P3 · Mini Mentoria (página) é a mais clara; /inscricao-curta e /inscricao-dossie são fracas** [E, auditoria B]. Promessa de capital/parceria em frases ("receber investimentos na sua área", "tenha acesso a possibilidades de parceria e investimento") em /inscricao e /inscricao-curta; /etapa-desenvolvimento "ver a possibilidade de investimentos e parcerias com a Zion" (contrapeso: "não há garantia"). Fora do escopo desta auditoria; só registro.

## 3. Duplicações e clones

| Grupo | Páginas | Oferta | Observação |
|---|---|---|---|
| Inscrição R$ 97 | /inscricao (77c286e6), /inscricao-curta (1597b2cc), /inscricao-97 rascunho (d6b63999) | c298aaed (1ApwIsdYSy) | texto quase igual, mesma oferta; `/inscricao-97` é cópia em rascunho [E] |
| Inscrição R$ 47 | /inscricao-47 (fb1e89b9), /inscricao-dossie (828beb3b), /parceiro-zion (066b2cb9) | 668391e7 (z3a0AEkvRl) | três páginas, mesma oferta; /inscricao-dossie quase sem tráfego (9) |
| Mini Mentoria | /mini-mentoria (be23f04a) → 0c71eeba; oferta clone 74a3f8c6 no produto do Club | duplicata de oferta | J-09 |
| Terra/capital A × B | bd7bf43d, de068af2 | R$ 47 × R$ 67 | desenho de teste A/B, texto idêntico [E], OK por intenção |
| Cursos antigos | /curso-terreno-destino-turistico + /etapa-desenvolvimento | R$ 47 (arquivada) e R$ 290 | mesma turma de 119 aulas em 3 turmas (a490c3c8, 4834bc40, 2c33680d) [E] |
| Club antigo | /club, /club/planos, 6e9ce423, 925b7055 | offerId null | "(Copy)" nos títulos |

## 4. Entrega automática por oferta (ofertas ligadas a páginas ou com tráfego)

| Oferta (hash) | Entrega | Situação |
|---|---|---|
| R$ 97 c298aaed (1ApwIsdYSy) | 2 turmas: 3ef7a340/087479a3 e a8e2157a/69345987 | OK mas duplicada (J-05); fluxo de pós-compra em rascunho (J-06) |
| R$ 47 668391e7 (z3a0AEkvRl) | as mesmas 2 turmas | idem; sem fluxo |
| Mini Mentoria 0c71eeba (yhyiqUB9OF) | 087479a3 (portal 3ef7a340 publicado) | OK; sem fluxo |
| Mini Mentoria Perf. ca1d914c (S8De0erMoM) | 15186b3f (portal 41353f3c, **não publicado**) | J-10 |
| terra-capital A 1eb339a6 / B 338c9ed8 | turma c050fbc6 (portal Zion Hotel Academy, publicado) | OK [E]; 1 membro |
| Curso 47 c91f1ff2 (arquivada) | 4834bc40 (portal mentoria-zion) | oferta arquivada |
| Etapa 290 095e1914 | a490c3c8 (portal mentoria-zion, 4 membros) | oferta pending |
| Ferramentas R$ 19 (publicadas 10, 12, 15, 16, 19, 20, 22, 23, 24, 28, 30) | link + arquivo (sem membership) | OK [E] `deliverableCategories` link,file; entrega 1 arquivo por oferta [H] não abri |
| E-books R$ 13 (3 páginas) e combos R$ 19 | membership nas turmas "E-book · …" do portal Zion Collection | OK; combos compartilham turmas dos e-books (esperado) |
| Arsenal R$ 27 ySAkZG38VS | só link, SYNCERR | página rascunho |
| Land Bank/Club R$ 97, R$ 270 | turmas do portal Land Bank / Collection | arquivadas |

Nenhuma oferta aprovada com `deliverables` vazio entre as ligadas a páginas [E]. Produtos sem portal: ferramentas (esperado: entrega por arquivo), Arsenal (link). Sem e-mail de acesso verificado [H]: não existe fluxo ativo de e-mail para as ofertas vigentes; confiar no e-mail padrão do ClickMax não foi comprovado.

## 5. Ofertas de R$ 47 / R$ 97 que de fato recebem tráfego

| Oferta | Preço | Páginas que levam a ela (vis. 7d) | Estado do checkout |
|---|---|---|---|
| 668391e7 (z3a0AEkvRl) | R$ 47 | /inscricao-47 (196), /parceiro-zion (72), /inscricao-dossie (9) = 277; **campanhas ativas** (auditoria A) | `approved`, `providerSyncError` {}, gateway ticto, Pix + cartão 1x, boleto off, reembolso 7 dias, `hasTransaction` true |
| c298aaed (1ApwIsdYSy) | R$ 97 | /inscricao (183), /inscricao-curta (105) = 288 (campanhas pausadas, sem anúncio ativo [E, A]) | idem, `hasTransaction` true |
| 0c71eeba (yhyiqUB9OF) | R$ 47 | /mini-mentoria (51); nenhum anúncio ativo aponta [E, A] | `approved`, sem erro |
| 1eb339a6 (Yqp_fxiRJl) / 338c9ed8 (k5ETStF7A7) | R$ 47 / R$ 67 | /terra-capital-a (12), -b (4), última visita 21/11 | `approved`, sem erro; A com transação |
| c91f1ff2 (IUVjj5Y-KR) | R$ 47 | /curso-terreno-destino-turistico (207) | **archived** (J-01) |
| 095e1914 (ftzIEt5sY_) | R$ 290 | /etapa-desenvolvimento (26) | **pending_corrections** (J-02) |

`checkout aprovada` aqui significa `status: approved` na oferta; o checkout real (carregamento, campos, preço final, redirecionamento) não foi verificado, ver auditoria B seção 7.

## 6. Páginas de obrigado (thankYou) e redirecionamento

- 4 páginas thankYou: `/obrigado-plataforma` (d7166fc3, publicada 24/11, 2 visitas, link para zion-plataforma.clickmax.space e um formulário), `/rU9XGY3jRuxsyehcH0RzJ` (agenda da equipe, externa, rascunho), `/d66jfBtHc-KO0CZgYOW2b` (Clube alinhamento + agenda, externa, rascunho), `/zar-teste-script` (teste técnico, rascunho, "não publicar").
- [E] nenhuma tem `linkedFunnels`, exceto as externas do funil Parceiros/Club (1). [H] nenhum checkout atual redireciona para /obrigado-plataforma: `offers_get` não traz campo de redirecionamento e a página não está ligada a funil. As 2 visitas em 24/11 parecem teste interno [H].
- Correção: se Bruno quer pós-compra, ligar a oferta (R$ 97/R$ 47) à página e mostrar o login; hoje a página diz "Pagamento recebido" e leva só a um portal. Esforço: baixo/médio.

## 7. Tags, pixels e metadados por página

- `pixelViewContent`: false em 71/71 [E]. Eventos de tracking disponíveis: page_viewed, scroll, time_on_page, exit_intent (todas as v3). Checkout events no `triggerMap` de cada sales. Outra auditoria (C) cobre pixel/CAPI.
- `title`: nulo em 69/71 (usa o nome interno). Títulos com "(Copy)": ver J-13. `description`: nula nas amostradas (/club, /inscricao-47 etc.).
- `externalConfig`: 7 páginas externas (Land Bank/Clube/Parceiros) com tracking via script; tracking 0 nos 7 dias, exceto /clube landing (29).
- CTAs: todas as 27 páginas de venda publicadas usam `#pagar` ou `#oferta` internos [E, scan de hrefs em amostra de 22 + B]; âncora presente. /curso-terreno e /etapa-desenvolvimento têm links externos (zionhotelgroup.com, Instagram) além do CTA. Nenhum CTA aponta para outra oferta [E]. Nenhuma página publicada com offerId nulo, exceto o Club antigo (3 páginas, sem iframe) e a vitrine [E].
- UTMs: preservadas até o iframe nas 6 páginas de inscrição [E, B].

## 8. Proposta de decisão por página e oferta (PROPOSTA PARA APROVAÇÃO DE BRUNO; nada foi executado)

Páginas publicadas
| Página | Proposta |
|---|---|
| /inscricao-47 (R$ 47, anúncios ativos) | **Manter** (destino principal), ajustar texto/título depois |
| /parceiro-zion (R$ 47, anúncios ativos) | **Manter** (mais completa) |
| /inscricao-dossie (R$ 47, 9 visitas) | **Despublicar** (consolidar em /inscricao-47) |
| /mini-mentoria (R$ 47, 51 visitas, oferta própria) | **Manter** (é a mais clara) ou consolidar com /parceiro-zion, Bruno decide |
| /inscricao (R$ 97) e /inscricao-curta (R$ 97) | **Consolidar** em uma só (manter /inscricao, mais completa) e **despublicar** a outra; ou despublicar as duas se R$ 97 não vai mais ao ar |
| /terra-capital-a e -b | **Manter** se o teste A/B continua; senão consolidar |
| /curso-terreno-destino-turistico | **Despublicar** (oferta arquivada) ou desarquivar a oferta; decidir |
| /etapa-desenvolvimento (R$ 290) | **Despublicar** |
| /club/planos, /club (Copy, R$ 270/980/2.900) | **Despublicar** (decisão de Bruno sobre o Clube) |
| /zion-collection-club (vitrine, 20 links mortos) | **Despublicar** |
| /obrigado-plataforma | **Manter**, ligar ao checkout se Bruno aprovar |
| Ferramentas R$ 19 publicadas (10, 12, 15, 16, 19, 20, 22, 23, 24, 28, 30) e e-books R$ 13 (3) | **Manter** (0 a 3 visitas, sem problema técnico) |
Rascunhos: manter ZAR/ferramentas 01, 05, 11, 13, 14, 17, 18, 29 até o erro de sincronização ser resolvido; **arquivar** os rascunhos duplicados /inscricao-97, /zar-teste-script, /sessao-zion-360 (oferta arquivada), /mini-mentoria-performance (manter só se publicar o portal).
Ofertas
| Oferta | Proposta |
|---|---|
| 668391e7 R$ 47, c298aaed R$ 97, 0c71eeba R$ 47, 1eb339a6/338c9ed8 | **Manter** |
| 74a3f8c6 (Mini Mentoria órfã) | **Arquivar** (ou apagar), depois de confirmar que ninguém comprou |
| c91f1ff2 (curso R$ 47 arquivada) | **Manter arquivada**; se página sai, nada mais a fazer |
| 095e1914 (R$ 290), c40895ad (R$ 97 kit), 36zciytFiY | **Arquivar** |
| ofertas ZAR R$ 27 sem página | **Manter** (aprovadas sem venda) ou arquivar as `incomplete` |
| Fluxos "Inscrição 270 · …", "Consultoria 360 · …" | **Arquivar/pausar** (R$ 270 obsoletos) |
Pendências de entrega: ativar fluxo único de pós-compra para as ofertas vigentes; escolher portal canônico; publicar portal 41353f3c antes de vender a Mini Mentoria de Performance.

Esforço total aproximado: consolidar páginas e ofertas 1 a 2 horas; ajustar entrega em dois portais 1 a 2 horas mais um teste de compra real (precisa de Bruno).

## 9. O que não foi verificado

Checkout (carregamento, campos, preço final); e-mail de acesso e login; conteúdo interno das turmas (só metadados); `hasTransaction` não distingue teste, pendente ou paga; campanhas ativas apenas conforme auditoria A; tráfego por origem (pago/orgânico) por página; redirecionamento pós-compra (sem campo na API).
