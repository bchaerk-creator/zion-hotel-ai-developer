# Checkout enxuto e página de agradecimento · Mini Mentoria (R$ 47)

Agente: ZION CONVERSION · 25/11/2026. **Só preparação: nada publicado, ligado ou alterado na oferta, no checkout ou no portal.** [E] evidência, [H] hipótese, [NC] não confirmado.

## 1. O que existe hoje (lido por `offers_get 0c71eeba…` em 25/11) [E]
Checkout nativo do ClickMax embutido na página (`<div data-cx-checkout>`), gateway Ticto, preço R$ 47 (`originalPrice` 4700), Pix ativo, cartão 1x, boleto desligado, sem recorrência, `requiredAddress` false, sem cupom (`showCoupon` false), sem contador (`showTimer` false), sem prova social (`socialProof` null), sem plugins (`checkoutPlugins` null), sem banners (`bannerDesktop/Mobile` null), `softDescriptor ZIONACADEMY`, suporte por telefone, reembolso 7 dias (`limitToRefund` 7), nome do produto "Mini Mentoria de Estruturação", descrição honesta (sem reunião, parceria = possibilidade). **Imagem do produto = placeholder do ClickMax** (`product-placeholder.png`): é o único ponto visual claramente pobre.

## 2. O que o ClickMax permite ajustar (docs `features/sales/checkout`) [E]
- **Configurações do checkout:** URL da **Página de obrigado**; **imagens** (produto 500×500 px, topo 1024×280 px, lateral 424×880 px; JPG/PNG até 2 MB); **Visualizar checkout** (prévia).
- **Edição da oferta → Recursos do checkout:** prova social (números reais), contador regressivo (1 a 60 min), botão de WhatsApp, chat, popup de desconto (exige cupom), avaliações (depoimentos escritos por você), vídeo no topo.
- **Limitação importante:** contador, WhatsApp, chat, popup, avaliações e vídeo "valem só para o checkout padrão, não para o checkout personalizado feito no editor de páginas" [E, docs]. Nosso checkout é o **embutido na página** [E, auditoria]; portanto estas opções provavelmente **não aparecem** nele [H, a confirmar no painel]. O que vale nele é o que está na página e nos dados da oferta.
- Prévia do checkout real: bloqueada no ambiente (`payments.clickmax.io`); **não vi o checkout renderizado**.

## 3. Configuração enxuta recomendada (Bruno ajusta no painel; nada foi aplicado)
| Item | Recomendação | Motivo | Fonte |
|---|---|---|---|
| Nome do produto e preço | manter: "Mini Mentoria de Estruturação", R$ 47 | preço explícito já vem da oferta | [E] |
| Pagamento | manter Pix + cartão 1x, sem boleto, sem recorrência | menos opções, menos abandono; Pix primeiro no celular (ClickMax já põe "Copiar código Pix" em primeiro) | [E] docs |
| Campos exigidos | manter só os do checkout padrão (nome, e-mail, telefone, CPF); `requiredAddress` false | produto digital; sem endereço | [E] oferta |
| **Imagem do produto** | trocar o placeholder por capa 500×500 px com a marca (cores #040605/#1B2117/#C9B37E; sem foto de pessoas; sem texto prometendo resultado) | checkout genérico passa menos confiança | [E] docs; arte: pedir ao CREATIVE |
| Banners topo/lateral | **não usar** (ou só logo discreto) | "banners em excesso" é anti-padrão do agente | spec CONVERSION |
| Contador / cupom / popup | **manter desligados** | sem urgência falsa; sem preço "de" | CLAUDE.md |
| Prova social (balões de compra) | **desligada** por ora | números reais e baixos podem prejudicar; reavaliar com volume | docs (mínimo configurável) |
| Avaliações | **não usar** | depoimentos só reais e documentados; não há | CLAUDE.md |
| Garantia | já aparece na página (7 dias) e na oferta; repetir a frase na descrição da oferta (já está) | CDC | [E] |
| Página de obrigado | **ligar à `/obrigado-mini-mentoria`** (seção 4) | hoje cai na página padrão do ClickMax | [E] docs |
| WhatsApp no checkout | opcional, só se aparecer a opção; número +55 48 6137-1061 | dúvida de pagamento | docs |

**Checkout "novo" do tipo página (checkout de página):** o ClickMax tem 15 modelos de página `checkout` (`pages_templates_list` type checkout; `pages_create` aceita `type: "checkout"` + `templateId` + `offerId`, que liga a oferta). **Não criei** nenhum: os modelos listados são de outros infoprodutos (pertencem a outro workspace de templates) e a página de venda já embute o checkout, então um segundo checkout em página daria uma duplicação sem ganho comprovado [H]. Se Bruno quiser testar "checkout em página própria" (mais enxuto: só produto, preço e pagamento), é possível criar um rascunho a partir de um template com `offerId 0c71eeba…`, sem publicar; precisa de decisão dele.

## 4. Página de agradecimento (rascunho criado)
- Rascunho `/obrigado-mini-mentoria`, id `1a0aed43-2f82-4b0a-826f-0424e2def674`, tipo `thankYou`, **não publicada, não ligada a nada**. Conteúdo: "Pagamento recebido. Bem-vindo."; como acessar (e-mail da compra; primeiro acesso sem criar senha [E: `firstAccessWithoutPass`]); botão "ENTRAR NA PLATAFORMA" (`zion-plataforma.clickmax.space`); por onde começar (Comece aqui → Marco Zero → sete pilares); suporte pelo WhatsApp; reembolso 7 dias; convite **opcional** ao cadastro do terreno (aula do Pilar 7, "a Zion avalia cada caso, não garante parceria nem investimento"). Sem R$ 97, sem reunião, sem promessa.
- **Diferença para `/obrigado-plataforma`:** a antiga tem um formulário (ficha pós-compra, ClickMax Forms) e diz "Seu acesso chega no e-mail da compra". A nova **não tem formulário**: a receita `thank-you` do importador proíbe captura. A ficha opcional continua sendo a aula/formulário dentro da plataforma (Pilar 7). Se Bruno quiser manter o formulário na página nova, adicioná-lo no editor visual.
- **Publicar antes de ligar:** a página precisa estar publicada para o redirecionamento funcionar (docs: "A página de obrigado não abre: confirme que a URL informada está publicada e acessível"). Publicar exige "aprovado" de Bruno.
- **Passo de painel para ligar o redirecionamento** (caminho conforme docs `features/sales/checkout` [E]): Produtos → Mini Mentoria de Estruturação → oferta → **Configurações do checkout** → campo **Página de obrigado** → colar `https://infoprodutos-zion.clickmax.space/obrigado-mini-mentoria` → salvar → **Visualizar checkout**. [NC: o rótulo exato do menu pode variar; a doc não mostra tela. A oferta lida por API não expõe esse campo, então não consegui conferir o valor atual; a auditoria anterior registra que hoje não redireciona.] Reversão: apagar o campo (volta à página padrão do ClickMax).
- Alternativa para checkout embutido na página: o funil. Se a venda for etapa de um funil, o gatilho `purchase_approved` leva à próxima etapa (página de obrigado) [E, docs funnel-diagnostics]; sem funil, vale o campo da oferta.

## 5. O que não foi possível ver
Checkout renderizado (Pix/cartão, campos reais, selos, velocidade no celular); se o redirecionamento do checkout **embutido** respeita o campo "Página de obrigado" [NC]; se o checkout embutido mostra a imagem do produto [NC]. Tudo isso entra no roteiro de teste de Bruno (`CHECKLIST_ENTREGA_E_RECUPERACAO_MM47.md`).
