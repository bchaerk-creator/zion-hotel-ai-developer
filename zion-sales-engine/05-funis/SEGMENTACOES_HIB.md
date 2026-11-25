# Segmentações do funil híbrido · ClickMax (prefixo `[HIB]`)

Agente: FUNNEL · 25/11/2026. Workspace `e87e8ba9-37cf-4c54-9a97-3e4e1b01827a`. Segmentos são **só filtros**: não enviam nada, não ativam automação, não aplicam etiqueta. Contagens agregadas lidas em 25/11 pelo ClickMax (`segments_list`), sem nomes. Base total de contatos: 2.912.
Marcação: **[E]** evidência, **[NC]** não confirmado.

## 1. Segmentos criados (14)

| # | Nome | Id do segmento | Filtro (resumo) | Contagem |
|---|---|---|---|---|
| 01 | `[HIB] 01 Origem · Meta (anúncio ou formulário)` | `d8a3cd82-4be9-452b-9956-fdf0fa139961` | `utm_source` em meta, facebook, fb, ig **ou** `utm_medium` em formulario_meta, lead_ads | 250 |
| 02 | `[HIB] 02 Campanha · Form inscrição (22/11)` | `81efc169-13a6-465c-a229-3c6b87603882` | `utm_campaign` = campanha de captação "FORM INSCRIÇÃO → LANDING → R$ 270 [22/11]" | 83 |
| 03 | `[HIB] 03 Criativo · Carrossel C` | `cf348be7-0b1d-48d4-9d23-2c39da1b3511` | `utm_content` = "ZC2 \| INSCRICAO 270 \| CARROSSEL C \| CAMPEAO NARRATIVA NOVA" | 41 |
| 04 | `[HIB] 04 Criativo · Vídeo 02 Dono de Terreno` | `634b33ef-63fa-4546-ae6b-a5248190ed1e` | `utm_content` = "ZC2 \| ... \| VIDEO 02 \| DONO TERRENO" **ou** "VIDEO 02 \| FORM 47" | 24 |
| 05 | `[HIB] 05 Criativo · Vídeo 01 Terreno e Capital` | `3d7c1c5a-fd87-478a-8e56-5c27f4e3ff17` | `utm_content` = "ZC2 \| ... \| VIDEO 01 \| TERRENO CAPITAL" | 15 |
| 06 | `[HIB] 06 Coorte · entrada desde 23/11/2026` | `bcbcd0d4-828e-48a4-a246-bf91993dbbba` | `createdAt` ≥ 23/11/2026 (hora de Brasília) | 75 |
| 07 | `[HIB] 07 Interesse · lead do formulário de inscrição` | `2fbccb87-7cce-4794-a601-133503c5ee84` | etiqueta `INSCRIÇÃO 270 \| LEAD DO FORMULÁRIO` (`d3053721…`) | 80 |
| 08 | `[HIB] 08 Visita (proxy · status visitou)` | `2e9cee74-ea6d-4b78-adcf-1e0af7900958` | status do contato = `visited` | 0 |
| 09 | `[HIB] 09 Checkout (proxy · carrinho aberto ou abandonado)` | `21c1de16-8f69-41f7-9c37-0ca6f325215f` | status = `in_cart` **ou** `abandoned_cart` | 0 |
| 10 | `[HIB] 10 Pagamento pendente (Pix gerado, não pago)` | `cb9705f8-3a91-4e39-9573-14a263761a49` | oferta `0c71eeba…` **e** transação `pending` | 0 |
| 11 | `[HIB] 11 Compra aprovada · Mini Mentoria R$47` | `e7d774d5-ef18-4185-9fe9-c733a7b5855e` | oferta `0c71eeba…` **e** transação `paid` | 0 |
| 12 | `[HIB] 12 Reembolso (proxy · cancelada na oferta MM47)` | `8050cb11-df8e-4f76-acf0-4196e139a90a` | oferta `0c71eeba…` **e** transação `canceled` | 0 |
| 13 | `[HIB] 13 EXCLUSÃO · compradores da plataforma` | `147d145f-5bfd-4ec0-969c-f480a6342140` | **ou**: membro da turma `087479a3…`; etiqueta `MM47 \| COMPROU` (`0366905f…`); (oferta `0c71eeba…` e paga); (produto com "Acesso à plataforma" no nome e pago) | menos de 5 (quem já comprou a plataforma, por qualquer oferta) |
| 14 | `[HIB] 14 Quente elegível (lead de inscrição sem comprador)` | `365adb44-0e20-49ce-a92d-ab7159776c58` | etiqueta do 07 **e não** (turma, etiqueta COMPROU, oferta MM47 paga) | 80 |

Leitura: o 14 = 80 e o 07 = 80 mostram que **nenhum** lead de inscrição é comprador da plataforma hoje [E]. O 11 = 0 confirma 0 compras da oferta R$ 47 [E, coerente com `FUNIL_CANONICO.md`]. Os segmentos recarregam sozinhos (atualização do ClickMax).

## 2. Uso de cada segmento

- **Exclusão de compradores:** `[HIB] 13`. Em qualquer fluxo de recuperação ou remarketing, o público é `[HIB] 14` ou outro **menos** o 13. No Meta, subir o 13 como público de exclusão.
- **Coortes:** o 06 é a coorte de 23/11 em diante. Para comparar leads com o mesmo tempo de maturação, duplicar o segmento por semana (`createdAt` entre duas datas; o filtro aceita ≥ e ≤) e medir conversão em 7 e 14 dias.
- **Criativo:** o ClickMax grava o `utm_content` do anúncio no lead; os 03 a 05 medem lead por criativo. Para os criativos novos do pacote P0, criar um segmento por `utm_content` novo (nome do criativo igual ao do anúncio).
- **Tipo de caminho:** quente = 07/14; frio = compra sem a etiqueta de captação e com UTM de venda direta (segmento a criar quando houver a UTM definitiva do frio, [NC]).

## 3. O que não dá para filtrar com o dado atual (e o que falta)

| Necessidade | Situação | Campo ou evento que faltaria |
|---|---|---|
| **Visita à landing/oferta por lead** | Só o status `visited` (0 contatos). O ClickMax tem o filtro `pageId` (lead que passou por uma página) e o passo "página visitada" nos fluxos, mas o lead só é identificado depois de preencher algo; visitante anônimo não é lead | Evento "visualização da oferta" e "clique com preço" gravados no lead (via `visitors_*` com identificação por e-mail/UTM, ou evento de página enviado ao CRM). Tarefa do TRACKING |
| **Checkout efetivo por lead** | O `initiate_checkout` dispara no carregamento do iframe [E], então "abriu o checkout" não prova intenção. O proxy (`in_cart`/`abandoned_cart`) é 0 hoje | Evento "início efetivo de checkout" (campo preenchido ou Pix gerado). Já existe o gatilho `checkout.pix.generated.v1` nos fluxos |
| **Pix gerado** | Hoje só `pending` (transação criada, não paga) | Distinguir "Pix gerado" de "pendente" depende do evento `checkout.pix.generated.v1`; um fluxo poderia aplicar uma etiqueta (não criado, exige ativação) |
| **Reembolso** | O ClickMax só tem os status `paid`, `pending`, `failed`, `canceled`; o 12 usa `canceled` como proxy | Status ou etiqueta de reembolso real. Quem reembolsa (Ticto/ClickMax) deve gerar evento; [NC] qual evento o checkout emite. Proposta: etiqueta manual `MM47 \| REEMBOLSO` aplicada junto com o estorno |
| **Consentimento de publicidade** | Não existe campo | Campo personalizado "consentimento de anúncios" gravado pelo formulário |
| **Interesse** | Só a etiqueta de entrada | Campo de qualificação (ex.: "tem terreno?") **opcional**, sem condicionar o cadastro |
| **Criativo e campanha dos leads antigos** | Dependem da UTM; lead sem UTM = "não atribuído" | Nenhuma ação retroativa, para não inventar atribuição |

## 4. Como remover (reversão)

Cada segmento sai com `segments_delete` (id da tabela, `workspaceId` acima). Efeito: apaga o segmento e a lista sincronizada dele; **não** altera contatos, etiquetas ou fluxos. Nada usa os segmentos ainda (nenhum fluxo, disparo ou público aponta para eles). Ordem sugerida se quiser limpar tudo: 14, 13, 12, 11, 10, 09, 08, 07, 06, 05, 04, 03, 02, 01.

Etiqueta criada: `HIB | EDUCAÇÃO · INÍCIO` `aaf465a6-15f9-4813-bff5-1ff037e866bb` (sem uso; gatilho do fluxo de educação). Remoção: `tags_delete`.
