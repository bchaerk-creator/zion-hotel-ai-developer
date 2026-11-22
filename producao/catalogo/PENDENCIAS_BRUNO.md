# O que só Bruno pode fazer

Atualizado pelas sessões de produção. Tudo o mais é feito automaticamente.

## Uma vez só
- [ ] Ligar o GitHub Pages (GitHub → Settings → Pages → branch `main`, pasta `/docs`). Sem isso as fotos das páginas e os links de download das entregas não abrem. (Não consigo conferir daqui: o acesso ao github.io é bloqueado neste ambiente.)
- [ ] Concluir a análise de vendedor no ClickMax (Carteira → `/sales/wallet`). Sem isso nenhum checkout vende.
  - **Atualização 08/11/2026:** o motivo de recusa da conta bancária não aparece mais; a conta de vendedor segue em análise pelo ClickMax.
  - Em 07/11/2026: o ClickMax registrou na conta bancária: "Comprovante bancário inválido. Faltou documento: Contrato Social ou Contrato MEI. Faltou o Cartão CNPJ (emitido no site da Receita Federal)." Envie esses documentos pela Carteira.

## Arquivos de entrega
Não dependem mais de Bruno: ficam em `docs/p/adbc67069af26ae0/<produto>/` e são ligados à oferta automaticamente (Ferramentas 01, 11, 13, 14, 17 e 29 já ligadas).

## Imagem do produto no checkout (opcional, 1 minuto por produto)
O ClickMax só aceita a imagem do produto se ela for enviada para o armazenamento dele, e o módulo de upload que eu usaria (posts sociais) está desligado nesta conta. As capas já estão prontas e em uso na página de vendas e na página de acesso. Para o checkout: Produtos → oferta → imagem do produto → subir o arquivo.
| Produto | Capa |
|---|---|
| Ferramenta 17 | `docs/p/adbc67069af26ae0/checklist-17/capa.jpg` |
| Ferramenta 11 | `docs/p/adbc67069af26ae0/kit-mensagens-11/capa.jpg` |
| Ferramenta 13 | `docs/p/adbc67069af26ae0/enxoval-13/capa.jpg` |
| Ferramenta 14 | `docs/p/adbc67069af26ae0/ocorrencias-14/capa.jpg` |
| Ferramenta 29 | `docs/p/adbc67069af26ae0/experiencias-29/capa.jpg` |
| Ferramenta 05 | `docs/p/adbc67069af26ae0/orcamento-05/capa.jpg` |
| Ferramenta 18 | `docs/p/adbc67069af26ae0/manutencao-18/capa.jpg` |
| Ferramenta 20 | `docs/p/adbc67069af26ae0/treinamento-20/capa.jpg` |
| Ferramenta 30 | `docs/p/adbc67069af26ae0/briefing-30/capa.jpg` |
| Ferramenta 15 | `docs/p/adbc67069af26ae0/fornecedores-15/capa.jpg` |
| Ferramenta 19 | `docs/p/adbc67069af26ae0/compras-19/capa.jpg` |
| Ferramenta 12 | `docs/p/adbc67069af26ae0/fotos-12/capa.jpg` |
| Ferramenta 22 | `docs/p/adbc67069af26ae0/campanhas-22/capa.jpg` |
| Ferramenta 23 | `docs/p/adbc67069af26ae0/roteiros-23/capa.jpg` |
| Ferramenta 16 | `docs/p/adbc67069af26ae0/parcerias-16/capa.jpg` |
| Ferramenta 28 | `docs/p/adbc67069af26ae0/capacidade-28/capa.jpg` |
| Ferramenta 10 | `docs/p/adbc67069af26ae0/financeiro-10/capa.jpg` |
| Ferramenta 24 | `docs/p/adbc67069af26ae0/assistente-24/capa.jpg` |
Se o módulo de posts sociais for ligado no ClickMax, eu passo a fazer isso sozinho.

## Ofertas enviadas para aprovação (10/11)
- 17, 11, 13, 14, 29, 18 e 20 estão em `pending` (análise do ClickMax). A 05 ficou de fora até a decisão sobre contingência e "para uma cabana".
- **Erro de sincronização com o gateway** nas ofertas criadas antes de 10/11 (17, 11, 13, 14, 29, 18): "Não autorizado. Token inválido ou ausente." A 20, criada hoje, sincronizou. Vale perguntar ao suporte do ClickMax se essas precisam ser sincronizadas de novo.
- Páginas de vendas ficam em rascunho até cada oferta ficar `active`; a rodada diária publica assim que aprovar.

## Ofertas aprovadas (11/11)
- 17, 11, 13, 14, 29, 18 e 20 aprovadas pelo ClickMax (`canSell` true). A conta de vendedor segue `pending`.
- **Publicada:** só a página da 20 (`https://infoprodutos-zion.clickmax.space/treinamento-primeiro-turno`), que não tem erro de sincronização.
- **Seguradas em rascunho:** 17, 11, 13, 14, 29 e 18, porque ainda mostram "Não autorizado. Token inválido ou ausente." no gateway. Publicar nelas pode levar alguém a um checkout que não cobra. **Bruno:** perguntar ao suporte do ClickMax como ressincronizar.
- 30 enviada para aprovação em 11/11, sem erro de sincronização.

## Rodada de 12/11
- 30 aprovada, sem erro de sincronização: página publicada e conferida no ar (`https://infoprodutos-zion.clickmax.space/briefing-experiencia`).
- 17, 11, 13, 14, 29 e 18 continuam com "Token inválido ou ausente": páginas seguem seguradas. 05 segue fora (decisão de Bruno).
- 15 criada e enviada para aprovação.

## Rodada de 13/11
- 15 aprovada, sem erro de sincronização: página publicada e conferida no ar (`https://infoprodutos-zion.clickmax.space/comparador-fornecedores`).
- 13, 14, 29 e 18 conferidas hoje: aprovadas, mas ainda com "Token inválido ou ausente"; 17 e 11 tinham o mesmo erro na conferência de 12/11. Páginas seguem seguradas.
- 19 criada e enviada para aprovação.

## Rodada de 14/11
- 19 aprovada, sem erro de sincronização: página publicada e conferida no ar (`https://infoprodutos-zion.clickmax.space/controle-compras`).
- 17 e 11 conferidas hoje: ainda com "Token inválido ou ausente" (13, 14, 29 e 18 tinham o mesmo erro em 13/11). Páginas seguem seguradas.
- 12 criada e enviada para aprovação. Próximos da fila: E05 e E06 precisam dos PDFs A01 a A10 (item 5 de "Uma vez só"); sem eles, a rodada segue com as ferramentas 22, 23, 16, 28.


## Rodada de 15/11
- 12 aprovada, sem erro de sincronização: página publicada e conferida no ar (`https://infoprodutos-zion.clickmax.space/fotos-comodidades`).
- 29 conferida hoje: ainda com "Token inválido ou ausente" (17, 11, 13, 14 e 18 com o mesmo erro nas conferências de 13 e 14/11). Páginas seguem seguradas.
- 22 criada e enviada para aprovação.

## Rodada de 22/11
- Só conferência: 18 ainda com "Token inválido ou ausente"; vendedor ainda `pending` (`canSell` true, conta bancária aprovada). Nenhuma oferta nova a enviar ou publicar.
- Nenhum produto novo: continua sem decisão sobre 01, 21, 25, 26, 27, E08 ou os PDFs A01–A10.

## Rodada de 21/11
- 24 aprovada, sem erro de sincronização: página publicada e conferida no ar (`https://infoprodutos-zion.clickmax.space/assistente-atendimento`). Todas as ofertas criadas desde 11/11 estão aprovadas e com página no ar.
- 29 conferida hoje: ainda com "Token inválido ou ausente". As páginas de 17, 11, 13, 14, 29 e 18 seguem seguradas. Vendedor ainda `pending`.
- Nenhum produto novo: a fila sem decisão pendente acabou em 20/11 e não houve decisão registrada sobre 01, 21, 25, 26, 27, E08 ou os PDFs A01–A10. A rodada diária segue só conferindo ofertas até uma dessas decisões.

## Rodada de 20/11
- 10 aprovada, sem erro de sincronização: página publicada e conferida no ar (`https://infoprodutos-zion.clickmax.space/fechamento-mensal`).
- 14 conferida hoje: ainda com "Token inválido ou ausente". As páginas de 17, 11, 13, 14, 29 e 18 seguem seguradas. Vendedor ainda `pending`.
- 24 (Assistente de IA para Atendimento) criada e enviada para aprovação; página em rascunho em `/assistente-atendimento`. Instrução do exemplo testada com um modelo de IA: 12 de 12.
- **A fila de ferramentas sem decisão pendente acabou.** Só resta a 09, que repetiria quase tudo da Ferramenta 01. Para a rodada diária continuar, preciso de uma decisão sobre:
  - 01, 21, 25, 26 e 27 (sobreposições);
  - E08 (Jornada 2);
  - os PDFs A01–A10 (E05/E06);
  - ou uma nova lista de produtos.
  Até lá, as próximas rodadas só fazem o passo 1 (conferir ofertas e publicar páginas aprovadas) e avisam.

## Rodada de 19/11
- 28 aprovada, sem erro de sincronização: página publicada e conferida no ar (`https://infoprodutos-zion.clickmax.space/capacidade-atendimento`).
- 13 conferida hoje: ainda com "Token inválido ou ausente". As páginas de 17, 11, 13, 14, 29 e 18 seguem seguradas. Vendedor ainda `pending`.
- 10 (Fechamento Mensal por Imóvel) criada e enviada para aprovação; página em rascunho em `/fechamento-mensal`.
- **Decidir: ferramentas 25, 26 e 27 (projeto).** Antes de produzir, encontrei sobreposição com o que já existe:
  - 25 (premissas) com as abas Premissas e Viabilidade das planilhas do Clube, a ZAIOS F01–F03 e a Linha B (B08);
  - 26 (reuniões de projeto) com o Kit de Captação;
  - 27 (apresentação) com o kit do investidor (one-pager e apresentação).
  Seguir com promessa diferente, virar material do Clube ou sair do catálogo? Até a decisão, a rodada diária segue com o que sobra do público B: 09 (o que falta na Ferramenta 01) e 24 (assistente de IA).

## Rodada de 18/11
- 16 aprovada, sem erro de sincronização: página publicada e conferida no ar (`https://infoprodutos-zion.clickmax.space/kit-parcerias`).
- 29 conferida hoje: ainda com "Token inválido ou ausente". As páginas de 17, 11, 13, 14, 29 e 18 seguem seguradas.
- Vendedor ainda `pending` (`canSell` true, conta bancária aprovada).
- 28 (Planner de Capacidade e Atendimento) criada e enviada para aprovação; página em rascunho em `/capacidade-atendimento`.
- Fila "A fazer" que resta: 24 (assistente de IA), 25, 26 e 27. A 27 é Gamma e a 24 é instrução de IA: formatos diferentes do molde de planilha.

## Rodada de 17/11
- 23 aprovada, sem erro de sincronização: página publicada e conferida no ar (`https://infoprodutos-zion.clickmax.space/roteiros-conteudo`).
- 14 conferida hoje: ainda com "Token inválido ou ausente". As páginas de 17, 11, 13, 14, 29 e 18 seguem seguradas.
- 16 (Kit Operacional de Parcerias) criada e enviada para aprovação; página em rascunho em `/kit-parcerias`.

## Rodada de 16/11
- 22 aprovada, sem erro de sincronização: página publicada e conferida no ar (`https://infoprodutos-zion.clickmax.space/campanhas-baixa-procura`).
- 18 conferida hoje: ainda com "Token inválido ou ausente" (17, 11, 13, 14 e 29 com o mesmo erro nas conferências de 13 a 15/11). Páginas seguem seguradas.
- 23 criada e enviada para aprovação.
- Em 15/11 o painel do ClickMax mostrava 0 visitas nas páginas das ferramentas e nenhuma venda delas (a única venda de novembro no projeto foi a entrada do Clube, R$ 97): falta tráfego, que depende de Bruno (orçamento e conta de anúncio, ou envio para a base).
## Decidir (09/11)
- **Ferramentas 01 e 21 do catálogo:** com as promessas sem duplicação (Comando 05A/05B), a 01 (ficha de apresentação do terreno) se sobrepõe a B05, B10 e ao Dossiê do Land Bank, e a 21 (mensagens de reservas) à A07. Seguir, mudar a promessa ou tirar do catálogo? Até a decisão, a rodada diária segue com 20, 15, 19.
- **E-book E08 (Gestão e operação):** sobrepõe-se à Jornada 2 (Gestão) da Fábrica Educacional. Seguir como e-book separado, virar material da Jornada 2 ou sair do catálogo? A rodada diária pulou o E08 em 11/11.
- **Ferramenta 05:** contingência no lugar de "reserva" e percentual inicial (dicionário financeiro D6), e a frase "para uma cabana" separando da B06. Só com "aprovado".

## Zion Collection 06 · Seu Airbnb Está Vazio? (11/11)
Detalhes em `producao/zion-collection/06-airbnb-vazio/OFERTA.md`, seção 8.
- **Sobreposição com o Arsenal 01** (mesmo título, R$ 27): A) o 06 vira a oferta do tema e o Arsenal 01 sai de venda ou vira bônus; B) manter os dois com nomes diferentes.
- Aprovar o produto completo (padrão para os outros 19) ou pedir ajustes.
- Gravar a narração das aulas (`aula/TELEPROMPTER.md`), por Bruno ou locutor com voz licenciada.
- "Aprovado" para: merge na `main` (entrega no ar), enviar as 2 ofertas para aprovação do ClickMax, publicar a landing quando estiverem ativas.
- Pixel do Meta / API de conversões para infoprodutos.

## Quando quiser
- Teto de verba para anúncios (hoje R$ 0; campanhas só pausadas).
