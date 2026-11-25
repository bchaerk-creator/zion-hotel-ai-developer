# Arquitetura de públicos (quente × frio) · visão de dados

Autor: DATA · 25/11/2026 · **Nada foi criado, exportado nem enviado.** Aprovação específica de Bruno para qualquer público, exportação ou aplicação no Meta. Dados pessoais **nunca** no repositório.
Legenda: **[E]** evidência (lido/testado nesta sessão) · **[H]** hipótese · **[NC]** não confirmado.

## 1. Os públicos
| Público | Quem entra | Exclusões obrigatórias | Fonte dos dados |
|---|---|---|---|
| **Quente (venda)** | Leads da captação (`utm_campaign=captacao`, e-mail válido, **consentimento de publicidade**, ver §4), por coorte | **Compradores** da Mini Mentoria (e de qualquer oferta equivalente); quem pediu para sair; e-mail inválido | ClickMax: contatos com a etiqueta/UTM da captação **menos** `lastPurchaseDate` preenchida / `client=true` |
| **Frio (venda)** | Brasil amplo (segmentação do próprio Meta) | **Leads** da captação e **compradores**, quando tecnicamente possível | Listas de exclusão (leads e compradores) carregadas no Meta |
| **Captação** | Brasil amplo, interesses do tema | Compradores (sempre); leads recentes (opcional, para não pagar duas vezes pelo mesmo lead) | Lista de compradores |
Regra: o comprador **sai** de quente, de captação e de frio no mesmo dia em que compra (a lista de exclusão precisa ser atualizada; ver §5).

## 2. O que é exportável do ClickMax como lista [E: ferramentas lidas]
| Lista | Como (ferramenta) | Colunas úteis |
|---|---|---|
| Leads da captação por coorte | `leads_export_csv` com `filters` `createdAt` + `utmCampaign`/`utmContent`, ou `tagId` da coorte | `email`, `phone`, `createdAt`, `origin`, `tags` (o export **não** traz UTM [E]) |
| Compradores | `leads_export_csv` com `filters` `numberOfPurchases greaterThan 0` ou `client equals true` ou `transactionStatus equals paid`; ou `segmentId` de um segmento de compradores (`segments_create` em rascunho/`segments_preview_count` para contar sem baixar) | `email`, `phone`, `lastBuyDate`, `purchasedOfferNames` |
| Contagem sem baixar nada | `segments_preview_count`, `leads_search` com `perPage:1` (`meta.countItens`) | só número |
| Consentimento | filtros `lgpdApproved`, `emailConsentConfirmed`, `messagePreferencesAuthorized` (campos existem em `leads_search`) | hoje **`lgpdApproved=false` e `emailConsent` vazio** nos leads recentes [E]: ver §4 |
O arquivo gerado fica **fora do Git** (`~/zion-privado/publicos/`) e é apagado depois do upload.

## 3. Hash SHA-256: onde fazer
- O Meta aceita a lista **com hash SHA-256** (e-mail em minúsculas e sem espaços; telefone só dígitos com DDI 55) e também aceita texto puro, que **ele mesmo** faz o hash no envio [NC: confirmar no Gerenciador, documentação da Meta bloqueada nesta sessão].
- **Onde:** no **navegador/computador de Bruno** (ou na ferramenta do ChatGPT dele, sem enviar o arquivo a terceiros), **nunca no repositório** e nunca em ferramenta que guarde o arquivo. As regras de normalização são as mesmas do `capi-webhook/src/normalize.js` e de `conciliacao/lead_comprador.py` (minúsculas, sem espaços; **não** aplicar a regra do Gmail ao hash do público, só à conciliação opcional).
- O script do repositório **não** gera lista com hash de pessoas reais (não deve existir arquivo com PII nem com hash de PII no Git).

## 4. LGPD e consentimento (bloqueio antes de usar a base)
1. **Textos separados** e **opcionais**: (a) consentimento para comunicação comercial (e-mail/WhatsApp); (b) consentimento para **personalização de publicidade** (uso do e-mail/telefone em listas de anúncio). **O cadastro não pode depender** de nenhum dos dois.
2. **Estado hoje [E]:** contatos recentes da captação chegam com `lgpdApproved=false`, sem `emailConsent` e com todos os canais de mensagem **ligados por padrão**. Não há registro de consentimento de publicidade. **Enquanto não houver base legal definida por Zion/jurídico [NC], não suba a base de leads como público personalizado nem exclua/inclua por lista** sem ela.
3. **Exclusão de compradores é de baixo risco** (proteger quem já comprou) e normalmente cabe em interesse legítimo/execução do contrato [NC, orientação jurídica de Zion]: pode ser o **primeiro** público a subir.
4. Política de privacidade atualizada para mensuração e públicos [NC].

## 5. O que o Windsor/Meta permite aplicar
- **Criação/edição de público personalizado: NÃO há ação no Windsor.** `list_actions` do conector `facebook` (lido em 25/11/2026) lista campanha, conjunto e anúncio (criar, ativar, pausar, orçamento, arquivar, excluir), formulário de cadastro, imagem/vídeo, e busca de segmentação/locais. **Nenhuma** ação de público personalizado, lista de clientes ou lookalike [E].
- **Aplicar público a um conjunto** (incluir/excluir) só é possível **depois** que o público existir: `update_adset`/`create_adset` aceitam o objeto `targeting`; o Meta lê `custom_audiences` e `excluded_custom_audiences` dentro dele [H, estrutura da Graph API; não testado, **[NC]**]. Como o parâmetro substitui o `targeting` inteiro, **leia o conjunto antes** e reenvie tudo; qualquer escrita no Meta é "aprovado" de Bruno.
- **Criar, subir e excluir públicos = no Gerenciador de Anúncios, por Bruno.** Passo a passo (**[NC]**: menus conferidos de memória; documentação oficial da Meta não pôde ser aberta nesta sessão, mande print se o nome for outro):
  1. Gerenciador de Anúncios › conta certa › **Públicos** › **Criar público** › **Público personalizado** › **Lista de clientes**.
  2. Escolher o arquivo (CSV com `email`, `phone`; ou já com hash) e mapear as colunas; aceitar o aviso de consentimento da Meta (**só se a base legal do §4 estiver resolvida**).
  3. Nome padrão: `EXCL | compradores MM47 | AAAA-MM-DD` · `QUENTE | leads captacao | coorte AAAA-MM-DD`.
  4. No conjunto de anúncios › **Público** › **Excluir** › escolher `EXCL | compradores…` (e `leads` no frio).
  5. Aguardar o processamento (o Meta mostra o tamanho e a taxa de correspondência; lista pequena pode não servir para entrega) [NC].
- Atualização: listas são **estáticas**; precisam ser **reenviadas** quando houver compra nova (rotina semanal, ou diária com compra). Alternativa sem lista: público a partir do **pixel/CAPI** (quem comprou) e de **formulário de cadastro** do Meta (quem abriu/enviou) [NC se disponível na conta], que se atualizam sozinhos.

## 6. O que fica pendente de aprovação (impacto e reversão)
| Ação | Quem | Reversão |
|---|---|---|
| Exportar lista de compradores/leads (arquivo fora do Git) | Bruno (ou ChatGPT dele) | Apagar o arquivo |
| Criar público de exclusão de compradores | Bruno, Gerenciador | Excluir o público |
| Subir público de leads (quente) | Bruno, **só após §4** | Excluir o público |
| Aplicar exclusões nos conjuntos (via painel ou `update_adset`) | Bruno/ChatGPT, "aprovado" | Remover a exclusão |
| Etiquetas de coorte no CRM | Bruno ("aprovado") | `tags_remove_from_leads` |
