# Consolidação da oferta canônica e preservação dos compradores de R$ 97

Agente: FUNNEL · 25/11/2026. **Plano apenas. Nada aqui foi executado.** Tudo abaixo que mexe em oferta, página ou acesso exige "aprovado" de Bruno.
Marcação: **[E]** evidência, **[H]** hipótese, **[NC]** não confirmado.

## 1. Situação [E]

| Oferta | Preço | Produto | Entrega | Páginas ligadas |
|---|---|---|---|---|
| `0c71eeba` Mini Mentoria (canônica) | R$ 47 | `cbbb5fb1` | só portal novo (turma `087479a3`) | `/mini-mentoria` |
| `668391e7` R$ 47 antiga | R$ 47 | `072083e8` | portal antigo **e** portal novo | `/inscricao-47`, `/parceiro-zion`, `/inscricao-dossie` |
| `c298aaed` R$ 97 | R$ 97 | `072083e8` | portal antigo **e** portal novo | `/inscricao`, `/inscricao-curta`, `/inscricao-97` (rascunho) |
| `74a3f8c6` duplicata | R$ 47 | `072083e8` | portal antigo e novo | nenhuma; sem vendas |

Os dois portais entregam o mesmo conteúdo (auditoria I). Os compradores reais de R$ 97 têm acesso pelas entregas da oferta `c298aaed` (turma nova e turma antiga). As páginas antigas prometem contato, parceria ou investimento que a plataforma não entrega.

## 2. O que NÃO fazer

1. **Não remover, desativar nem mover o acesso** de nenhum comprador (nem na turma nova, nem na antiga, nem no portal). Nada de `member_users_disable`, `member_users_remove_from_classroom` ou `portal_members_remove`.
2. Não apagar oferta, produto ou página com venda. Arquivar não é apagar, mas **ainda não está provado que arquivar preserva o acesso** [NC]. Só arquivar depois do teste da seção 4.
3. Não reembolsar nem alterar a venda de ninguém por iniciativa própria.
4. Não importar HTML sobre páginas publicadas (`/inscricao`, `/inscricao-47`, `/inscricao-curta`, `/parceiro-zion`, `/mini-mentoria`): atualiza a versão que está no ar.
5. Não mexer nas automações do Clube R$ 97 em rascunho, na Zaya, na Bela, no Land Bank nem no Club.
6. Não enviar a mensagem aos compradores sem "aprovado" (a seção 6 é só rascunho).

## 3. Plano passo a passo (cada passo com "aprovado")

**TRAVAS OBRIGATÓRIAS DE ACESSO (A07, auditoria da Fase 03). Valem para todos os passos abaixo e prevalecem sobre qualquer texto do plano:**
1. **Retrato antes/depois dos membros.** Antes de cada passo que toque oferta, página, entrega ou turma, registrar (fora do repositório) a lista de membros de **cada** turma dos dois portais (`member_users_list_by_classroom`) e, depois do passo, comparar. Qualquer diferença: reverter na hora e avisar Bruno. Sem retrato, o passo não começa.
2. **Confirmação escrita do ClickMax.** Antes de arquivar **qualquer** oferta que tenha compradores, obter por escrito do suporte do ClickMax que arquivar a oferta não revoga o acesso dos compradores. A documentação ou o teste com canário não substitui essa confirmação.
3. **Proibido mexer nas entregas de `c298aaed` e `668391e7`** (oferta dos compradores reais e a oferta de R$ 97 ligada à página de parceria) em qualquer hipótese: nem remover, nem trocar, nem renomear turma ligada a elas. Isto vale para os Passos 1, 6 e 7: os trechos desses passos que sugerem alterar essas entregas ficam **suspensos**.
4. **O canário fica fora dessas ofertas.** Compra de teste de Bruno **não** é feita em `c298aaed` nem em `668391e7`; o teste de "arquivar não corta acesso" usa uma oferta de teste isolada, criada só para isso, com um comprador de teste. O Passo 1 abaixo, que usa essas ofertas como canário, fica **substituído** por esta regra.
5. **Reembolso só a pedido do comprador** (a Opção B do e-mail da seção 6 informa, não cancela); nenhum acesso é removido por este plano.

**Passo 0 · Congelar o que sobe de risco (sem mudar nada em produção).**
Confirmar com TRAFFIC que nenhum anúncio ativo aponta para `/inscricao`, `/inscricao-curta`, `/inscricao-47`, `/parceiro-zion` ou `/inscricao-dossie`. Hoje a regra é campanhas pausadas e teto R$ 0 [E, CLAUDE.md], então o risco de tráfego pago nas páginas antigas é baixo [H]; confirmar de qualquer forma.

**Passo 1 · Provar que arquivar não corta acesso (teste com a compra do próprio Bruno).**
Existem compras de teste do próprio Bruno em `668391e7` e `c298aaed` [E, auditoria]. Usar essa conta como "canário":
1. Anotar o estado do acesso do canário (portal novo e antigo) por `member_users_get_by_lead`.
2. Com "aprovado", arquivar a oferta de teste mais isolada: a duplicata `74a3f8c6` (zero vendas, zero páginas) não serve de canário, porque não tem comprador. Então arquivar `668391e7` **apenas depois** de o canário confirmar a regra pela documentação do ClickMax (`docs_search`: arquivar oferta e acesso de membros) ou por pergunta ao suporte.
3. Reler o acesso do canário. Se continuar igual, a regra está provada. Se mudar, **reverter na hora** (`offers_unarchive`) e reconceder o acesso do canário.

**Passo 2 · Duplicata `74a3f8c6`.** Arquivar (sem apagar). Zero vendas, zero páginas [E]. Reversão: `offers_unarchive`.

**Passo 3 · Páginas antigas.** Duas opções, da mais segura para a mais forte:
- (a) Trocar só o destino do botão e tirar as frases de contato/investimento. Exige reimportar página publicada: precisa de "aprovado" e de cópia prévia (`pages_clone`) para reversão.
- (b) Despublicar (`pages_unpublish`) e deixar o endereço sem página. **Quebra o link** de quem ainda o tiver (anúncio antigo, WhatsApp antigo, e-mail). Só depois de 7 dias com o Passo 4 funcionando.
Preferência [H]: (a) para `/inscricao`, `/inscricao-curta`, `/inscricao-47` e `/inscricao-dossie`; resolver `/parceiro-zion` à parte (ver passo 5).

**Passo 4 · Redirecionar o tráfego sem quebrar nada.**
1. Ordem: primeiro garantir que `/mini-mentoria` vende (teste de compra e entrega, fluxos de rascunho aprovados); só depois mover o tráfego.
2. Anúncios: trocar a URL de destino no Meta, **pelo TRAFFIC e com "aprovado"**, para `/mini-mentoria` com UTM (`utm_source=meta&utm_medium=paid&utm_campaign=mm47&utm_content=<criativo>` (padrão único `09-tracking/PADRAO_UTM.md`: nas Tags de URL, com `utm_term`, `sck` e ids; destino sem parâmetros)). Criar anúncio novo em vez de editar o antigo preserva o histórico de aprendizado [H].
3. Links já distribuídos (bio, mensagens da Bela/Zaya): listar com o DATA e trocar um a um. Textos da Bela/Zaya com "R$ 97" **não são alterados por este agente**: apenas informar o responsável.
4. Link curto de transição: `redirect_links_create` (domínio de redirecionamento do ClickMax) para um endereço novo e estável que aponte para `/mini-mentoria`, para os próximos materiais usarem. Os endereços antigos continuam como estão até o passo 3.
5. Medir 7 dias: visitas em `/mini-mentoria`, visitas residuais nas páginas antigas. Só despublicar as antigas quando a visita residual for desprezível.

**Passo 5 · `/parceiro-zion`.** O nome mistura venda direta com captação. Reapontar a oferta da página (hoje `668391e7`) não é suficiente: a página fala de parceiro. Proposta: tratá-la como página da captação, **fora** deste funil; decisão de Bruno (despublicar, redirecionar ou levar ao time de captação).

**Passo 6 · Ofertas `668391e7` e `c298aaed`.** Arquivar só depois dos passos 1 a 4 e da comunicação aos compradores. Depois de arquivar, conferir de novo o acesso de **todos** os compradores (2 reais e testes).

**Passo 7 · Entrega duplicada.** Remover a entrega do portal antigo nas ofertas que continuarem ativas e renomear turmas que dizem "R$ 97": só pelo painel e só com "aprovado". Para as ofertas arquivadas, **não mexer** nas entregas.

## 4. Riscos

| Risco | Impacto | Como reduzir |
|---|---|---|
| Arquivar oferta cortar o acesso de comprador [NC] | Comprador pagante sem acesso | Passo 1 (canário); nunca arquivar `c298aaed` antes |
| Comprador de R$ 97 sentir que pagou mais pelo mesmo conteúdo | Reclamação, pedido de reembolso | Comunicar com honestidade (seção 6); decidir antes a política (decisão de Bruno) |
| Link antigo cair numa página despublicada | Venda perdida | Preferir editar a despublicar; manter 7 dias |
| Anúncio apontando para página antiga | Tráfego pago em promessa antiga | Passo 0 |
| `/mini-mentoria` com o texto do botão sem preço | Fricção e regra violada | Trocar texto do botão (aprovado) |
| Rastreamento: compra sem UTM | Meta sem compra atribuída | TRACKING; prazo de reenvio ao Meta = pagamento + 7 dias |
| Duplicar fluxos para a mesma compra | E-mail duplo | Fluxos novos têm escopo de oferta; fluxos antigos estão presos a outras ofertas [E] |

## 5. Reversão

| Ação | Como desfazer |
|---|---|
| Arquivar oferta | `offers_unarchive` (e reler acesso) |
| Despublicar página | `pages_publish` da versão anterior (conferir `lastPublishedAt`) |
| Editar página publicada | Reimportar a cópia feita antes (`pages_clone` do estado atual) |
| Trocar URL de anúncio | Voltar a URL anterior ou reativar o anúncio original (guardar o id) |
| Redirect link | `redirect_links_delete` |
| Acesso removido por engano | `member_users_enable` e conceder de novo na turma |

## 6. Rascunho de comunicação aos compradores reais de R$ 97 (NÃO ENVIAR)

Quem envia: Bruno, em nome da Zion, só depois de "aprovado". Canal: e-mail. Sem WhatsApp (modelos não submetidos). Sem nome nem e-mail no repositório: personalizar na hora.

**Antes de enviar, Bruno decide (uma das opções, ou outra):**
- **A. Só informar** e confirmar que o acesso continua.
- **B. Informar e oferecer o reembolso integral** a quem pedir, dentro do prazo legal de 7 dias (as compras são recentes [E, fatos-chave]; o prazo é a data de cada compra + 7 dias, conferir a data exata no ClickMax).
- **C. Informar e devolver a diferença de preço.** Exige conferir se o ClickMax permite reembolso parcial [NC]; é decisão financeira de Bruno.

**Assunto:** Uma informação sobre o seu acesso à plataforma Zion

> Olá, [nome].
>
> Você comprou o acesso à plataforma Zion Collection por R$ 97. Queremos ser claros com você: depois da sua compra, passamos a oferecer o mesmo conteúdo da plataforma por R$ 47, com o nome Mini Mentoria de Estruturação.
>
> O que muda para você: nada no acesso. Você continua com o seu acesso à plataforma, com todas as aulas, fichas e materiais, pelo período combinado. Não vamos remover nem alterar o seu acesso.
>
> Também queremos corrigir uma impressão que as páginas anteriores podiam passar. O que você comprou é um curso gravado, com fichas, e-books, planilhas em branco e modelos para preencher. Ele não inclui reunião nem acompanhamento individual. Parcerias e investimentos, quando existem, são possibilidades sujeitas à análise da Zion, e não fazem parte do produto.
>
> [OPÇÃO B: Se, com essas informações, você preferir não continuar, você pode pedir o reembolso integral até [data], respondendo este e-mail.]
> [OPÇÃO C: Vamos devolver a diferença de R$ 50 para você. Basta responder este e-mail confirmando.]
>
> Se tiver qualquer dúvida, responda este e-mail ou fale com a gente no WhatsApp +55 48 6137-1061.
>
> Um abraço,
> Bruno Chaerk
> Zion Hotel Group International

Notas para quem revisar:
- Não promete resultado, parceria nem investimento.
- A opção C só entra se o reembolso parcial for possível e aprovado por Bruno.
- Se a ficha de `/obrigado-plataforma` foi preenchida por eles, **não** escrever que "a Zion vai avaliar o terreno": a avaliação é opcional e sem garantia [E, fatos-chave].
- Enviar de um endereço com resposta monitorada.
