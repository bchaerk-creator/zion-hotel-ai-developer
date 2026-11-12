# Adesão ao Club Zion Collection · Jornada do Desenvolvimento (12/11/2026)

Fluxo: página → ficha de adesão (ClickMax) → pagamento no Asaas → webhook libera a área de membros.

| Peça | Onde | Id / endereço |
|---|---|---|
| Página de venda (sem preço) | GitHub Pages | `https://bchaerk-creator.github.io/zion-hotel-ai-developer/jornada-desenvolvimento/` |
| Ficha de adesão (ativa) | ClickMax, formulário | `7495df8b-489b-4395-91e1-404cbf90635f` · público `https://api.clickmax.io/forms/dcSUhl5BbcqmbFrhXY8oGHdF` |
| Depois da ficha | redireciona (3 s) | link do Asaas da Jornada `sd9u8uluy0urc2ye` |
| Etiqueta da ficha | ClickMax | `CLUBE \| ADESÃO · FICHA PREENCHIDA` `d200f176-6906-4a39-afd1-39bb3de1721d` |
| Funil novo | ClickMax, pipeline | `a7216b13-ead3-41ec-8029-c20d6cc5706a` · "Club Zion Collection · Adesão → Pagamento → Membro" |
| Etapas | 1 Preencheu a ficha `68fb945c-c559-499e-9f28-dd3f99ae7631` · 2 Foi ao pagamento `9d2f9dce-473d-4227-91a0-2abe0fd5cb1f` · 3 Pagou, acesso liberado `3508055e-18a7-4c55-bad7-c9a599928e04` · 4 Entrou na área `fbb583e8-18b5-4f9a-882d-d1adffbea8c7` · 5 Não pagou, retomar `f8d50a00-3c61-4eae-a6a3-6b4b90a52521` | |
| Liberação do acesso | webhook Asaas na Lovable | tag `MÉTODO \| COMPROU TRILHA 1` + turma `a490c3c8-17c5-478f-b017-3986bce21166` |

## Testado (12/11)
- Ficha abre (200), envio com contato de teste (resposta 201), contato criado com a etiqueta, redirecionamento para o link do Asaas (o Asaas é bloqueado neste ambiente: só se viu a navegação).
- Automação de entrada ativa (aprovada por Bruno em 12/11): segundo envio de teste criou o cartão "Teste Adesão Club 2" na etapa 1 do funil novo (origem: tag aplicada).
- Observação: o formulário mescla por e-mail e também reconhece o mesmo telefone. Um segundo envio com o mesmo telefone não atualizou o contato nem criou cartão.
- Contatos de teste criados: `Teste Adesão Club` e `Teste Adesão Club 2` (e-mails de teste). Podem ser excluídos.

## Automações ativas (aprovadas por Bruno em 12/11, só movem cartões, não enviam mensagem)
1. Entrada: tag `CLUBE | ADESÃO · FICHA PREENCHIDA` → cartão na etapa 1. managedFlow `a0a5dd32-461a-44d6-87c4-12406822309a`, flow `a473a722-d459-40d2-bdbb-5dffb754f00c`. Testada.
2. Passagem: tag `MÉTODO | COMPROU TRILHA 1` → etapa 3. managedFlow `174e6d57-f512-42ba-af7a-e29fdd0b5df7`, flow `4cf03b0c-4ea5-4b3b-b367-1ad3cc9790f9`. Filtro da tag conferido na estrutura do fluxo; **não testada com pagamento real** (aplicar a tag de compra dispararia também fluxos antigos de "Comprou Trilha 1").
3. Não criadas: etapa 2 (foi ao pagamento) e etapa 5 (não pagou); hoje são manuais.

## Ainda não verificado
- Primeiro pagamento real pelo link de R$ 970 (webhook nunca recebeu um pagamento desse link).
- Parcelas do link no Asaas (slide antigo diz "até 10x"; Bruno diz 12x).
- A etapa 4 (entrou na área) não tem automação; é manual.
