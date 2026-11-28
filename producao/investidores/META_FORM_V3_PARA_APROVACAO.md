# Formulário Zion Investors v3 · pacote para aprovação (28/11/2026)
**Nada foi criado no Meta, nada foi vinculado a anúncio, nenhuma campanha foi ativada.** Conteúdo completo em `meta_form_spec.json`; prévia mobile (simulação) em `prints/meta-form-previa-mobile.jpg`; classificação em `classificacao.js` (24 testes, 0 falhas).

## 1. Qual formulário existe e o que o Meta permite
- Formulários Zion Investors na página Zion Glamping Collection (`576944608845537`): `1177931711576787` (ativo, sem anúncio) e `1143109468438825` (arquivado). Foram os que criei hoje; não há formulário "Zion Investors" anterior a esses.
- **Editar: não é permitido.** Pela API o Meta só deixa mudar o status (ativo/arquivado); o próprio Meta Ads Manager só oferece "Duplicar" em formulário já publicado ([Graphed](https://graphed.com/blog/how-to-edit-facebook-ad-form)). Plano: criar o **v3** a partir do `1177931711576787`, mantendo página, idioma, privacidade e botão final, e **arquivar** o `1177931711576787`. Não existe integração nativa a preservar (o ClickMax ainda não recebe este formulário).

## 2. Limites e políticas do Meta (o que consegui confirmar)
- **Número de perguntas:** fontes secundárias dizem 15 perguntas por formulário ([Relevant Audience](https://www.relevantaudience.com/facebook-ads/facebook-lead-ads-instant-forms-guide/)); não achei o número oficial. 12 perguntas + nome, telefone, e-mail, cidade, estado + a pergunta de autorização cabem na regra citada. **Limite de opções por pergunta não confirmado** (a pergunta 5 tem 9 opções, a 3 tem 8); o Meta devolve erro na criação se passar.
- **Informação financeira:** a política do Meta para serviços financeiros diz que anúncios não devem pedir informações financeiras como conta bancária, cartão ou roteamento ([Meta Transparency](https://transparency.meta.com/policies/ad-standards/restricted-goods-services/financial-services/)). Fonte secundária inclui renda e score de crédito na lista de proibidos. **Não encontrei texto oficial que permita ou proíba perguntar a faixa de capital que a pessoa pretende investir (perguntas 5 e 6).** Também **não confirmei** se a categoria especial "serviços financeiros" e a verificação de anunciante se aplicam a este anúncio no Brasil. Pergunta de capital em formulário público também é o ponto mais sensível para a CVM (oferta pública).
- **Recomendação (a sua própria regra de contingência):** tirar as perguntas **5 e 6** do formulário do Meta e coletá-las **só na qualificação privada** (conversa autorizada com a equipe/Bela). O formulário fica com 10 perguntas. A classificação A+/A/B passa a sair quando a qualificação privada preencher capital e disponibilidade (item 7 do seu comando); até lá o contato fica **PENDENTE**, nunca "curioso". Se preferir arriscar, o v3 completo com 12 perguntas também está pronto, com o risco de reprovação do formulário/anúncio.
- Fonte geral: [Meta, forms questions](https://developers.facebook.com/docs/marketing-api/guides/lead-ads/forms-questions).

## 3. Conferência dos argumentos da descrição
| Afirmação | Situação |
|---|---|
| mais de 266 mil seguidores | **Confirmado hoje:** @zionbubble tem 266.388 seguidores (Instagram, via Windsor). Número muda; revisar antes de veicular |
| mais de 23 destinos | Consta nos materiais e no site ("mais de 23"); o projeto Lovable mostra 29 no pipeline. "Mais de 23" é verdadeiro nos dois casos; precisa de documento interno que sustente |
| mais de 20 anos dos fundadores | Consta no site ("20+ anos de hotelaria internacional"); sem documento comprobatório no repositório |
| atuação desde 2020 | Consta nos materiais ("opera desde 2020") |
| "referência nacional no segmento de glamping" | Opinião de marca; sem prova no repositório. Risco de publicidade |
| "Estamos convidando você a conhecer possibilidades de investir capital…" | **Revisão jurídica** (CVM 86/88/160): convite explícito a investir antes do parecer |

## 4. Conflitos com decisões anteriores (preciso da sua escolha)
1. **Pergunta 10, opção 1 ("operações hoteleiras existentes")** e a 9 (sedes): você decidiu guardar as opções de Urubici e Florianópolis à parte. Recomendo **remover a opção 1** do formulário público (ficam: novos destinos, expansão, "todas as possibilidades").
2. **Pergunta 11 e classificação T** (proprietário de terreno → Zion Collection): o encaminhamento será **etiqueta + tarefa para humano**, sem mensagem automática da plataforma, para não misturar com a Bela de R$ 97. Recomendo manter assim.
3. **Faixas de capital** (R$ 150 mil, 300, 450…): o Master V2 dizia que R$ 150 mil é referência interna e que não se divulga mínimo. Exibi-las em formulário público pode ser lido como piso. Mais um motivo para o item 2.

## 5. Tela final, configuração e integração (como será criado)
- **Alta intenção** (revisão antes do envio), idioma pt_BR, página Zion Glamping Collection, política `zionhotelgroup.com/privacidade`, botão final **CONHEÇA NOSSO MODELO DE NEGÓCIO** → `https://www.zionhotelgroup.com/oportunidades` (texto exato do seu comando).
- Contato: nome, telefone (WhatsApp), e-mail, cidade, estado + pergunta de autorização de WhatsApp (Sim/Não; **o disparo só vale para "Sim"**). Sem CPF, sem comprovantes.
- **ClickMax** (rascunho, nada ativo): projeto/pipeline Zion Investors; campos ZI; tags `ZI_*` (a criar: `ZI_A_PLUS_ESTRATEGICO`, `ZI_A_QUALIFICADO`, `ZI_B_POTENCIAL`, `ZI_C_MATURACAO`, `ZI_D_INSTITUCIONAL`, `ZI_T_TERRENO`, `ZI_BUBBLE`, `ZI_PENDENTE`); fluxo `cd2fa28f…` com as 7 ações em paralelo (registrar + origem/campanha/conjunto/anúncio; classificar; Bela com consentimento; tarefa prioritária; landing na tela final; reclassificar quando houver novos dados; deduplicação por telefone). **Ainda falta montar os passos do fluxo e a ingestão do formulário do Meta**, que será própria (não usa a sincronização do Land Bank).
- Sem checkout, sem cobrança, sem aporte mínimo, sem promessa de rentabilidade.

## 6. Aprovações que preciso
(a) perguntas 5 e 6 fora do Meta (recomendado) ou dentro; (b) remover a opção "operações existentes" da pergunta 10 (recomendado); (c) criar o v3 e arquivar o `1177931711576787`; (d) texto de abertura aprovado pelo jurídico antes de anunciar.

## ATUALIZAÇÃO · decisões de Bruno e criação (28/11)
Decisões: (1) **12 perguntas no Meta**, incluindo capital e disponibilidade (5 e 6); (2) pergunta 10, opção 1 trocada por **"Operações da Zion."**; (3) terreno (T) = etiqueta + tarefa para uma pessoa, sem mensagem automática; (4) criar o v3 e arquivar o v2.
**Criado: formulário `2402615837235072`** ("ZION INVESTORS | v3 (28/11)"), página Zion Glamping Collection, alta intenção, 12 perguntas + autorização de WhatsApp + nome, telefone, e-mail, cidade, estado; texto de abertura, tela final e botão conforme o comando. O Meta aceitou os limites (12 perguntas e até 9 opções por pergunta) **na criação**; a **análise de política do anúncio** acontece depois, quando um anúncio usar o formulário, e pode reprovar as perguntas 5 e 6. Se reprovar, criar o v4 sem elas e coletar na qualificação privada.
**Arquivados:** `1177931711576787` (v2) e `1143109468438825` (v1). Nenhum anúncio usa nenhum dos três; nenhuma campanha foi ativada.
**Atenção:** a faixa "R$ 150 mil" aparece em formulário público e pode ser lida como piso; "referência nacional" e o convite explícito a investir capital seguem para o jurídico.
