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
- **O cartão NÃO entra sozinho no funil.** O formulário não cria cartão; precisa de automação.
- Contato de teste criado: `Teste Adesão Club` (e-mail de teste do Bruno). Pode ser excluído.

## Pendente de "aprovado" de Bruno (automações)
1. Entrada: etiqueta da ficha → cartão na etapa 1.
2. Pagamento: tag `MÉTODO | COMPROU TRILHA 1` → etapa 3.
3. (Opcional) quem não paga em X horas → etapa 5.
Nenhuma mensagem é enviada por essas automações.

## Ainda não verificado
- Primeiro pagamento real pelo link de R$ 970 (webhook nunca recebeu um pagamento desse link).
- Parcelas do link no Asaas (slide antigo diz "até 10x"; Bruno diz 12x).
