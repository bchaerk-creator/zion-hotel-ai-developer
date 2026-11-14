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
