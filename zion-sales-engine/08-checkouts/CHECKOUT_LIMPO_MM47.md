# Checkout limpo · Mini Mentoria de Estruturação Zion (R$ 47)

Agente: ZION CONVERSION · 25/11/2026 · ordem P0. **Nada foi alterado** (oferta, produto, turma, checkout e Ticto intactos). [E] lido por API, [H] hipótese, [NC] não confirmado. Entregáveis confirmados em `ENTREGAVEIS_VERIFICADOS.md`.

## 1. Como o checkout funciona hoje [E]
- Oferta `0c71eeba-2654-432c-9701-0a31e6113a08`, status `approved`, gateway Ticto, hash `yhyiqUB9OF`; é o checkout nativo do ClickMax **embutido** na página de vendas (`<div data-cx-checkout>`; iframe `payments.clickmax.io`, bloqueado neste ambiente: **não vi o checkout renderizado**).
- Nome da **oferta** e do **produto** (`cbbb5fb1…`): "Mini Mentoria de Estruturação". O nome "Zion Collection Club | Acesso à plataforma" apontado na auditoria pertence ao checkout da oferta antiga (`/inscricao-47`, R$ 97), não a esta oferta. Para a oferta de R$ 47 não há nome errado a corrigir; há só a falta do "Zion" para igualar anúncio e página.
- `checkoutTitle` null, `showDescription` true (a descrição aparece no checkout), `checkoutImageSource` "product", imagem do produto = `product-placeholder.png` (genérica), banners null, `requiredAddress` false, cupom e contador desligados, prova social null, plugins null, Pix + cartão 1x, boleto desligado, sem recorrência, reembolso 7 dias, `softDescriptor ZIONACADEMY`, suporte por telefone.
- O que a API (`offers_update`) permite alterar: `name`, `checkoutTitle` (até 120 caracteres), `description` (até 1000), `bannerDesktop/Mobile`, `checkoutImageSource`, `socialProof`, `checkoutPlugins`, `showTimer/Coupon`, `paymentConfig`, `limitToRefund`, `supportPhone`, `softDescriptor`, `requiredAddress`. A **imagem do produto** tem fluxo próprio (`offers_set_product_image`; só aceita imagem enviada ao armazenamento do ClickMax: Bruno sobe no painel). **Não há `products_update`**: renomear o produto só pelo painel (Produtos → editar).
- Recursos de plugin (WhatsApp, chat, vídeo, avaliações, popup, contador) valem só para o checkout padrão e provavelmente não aparecem no embutido [H, ver `CHECKOUT_E_AGRADECIMENTO_MM47.md`]. Nenhum deles é recomendado de qualquer forma.

## 2. Configuração alvo, campo a campo
| Campo | Hoje | Proposto | Motivo / impacto |
|---|---|---|---|
| `name` (oferta) | Mini Mentoria de Estruturação | **Mini Mentoria de Estruturação Zion** | igual ao anúncio e à página; é o "nome exato único" |
| Nome do produto (painel) | Mini Mentoria de Estruturação | **Mini Mentoria de Estruturação Zion** | sem API; o checkout pode mostrar o nome do produto ou da oferta [NC], por isso igualar os dois |
| `checkoutTitle` | null | **Mini Mentoria de Estruturação Zion** | título explícito no checkout |
| `description` | texto atual (sem reunião, parceria como possibilidade) | texto da seção 3 | resumo objetivo dos entregáveis com 9 módulos, 70 aulas e materiais; sem "Metodologia Zion" solta |
| `originalPrice` | 4700 | 4700 (manter) | R$47 |
| `paymentConfig` | pix ativo, cartão 1x, boleto off, sem recorrência | manter | Pix e cartão à vista; pagamento único |
| `limitToRefund` | 7 | 7 (manter) | garantia de 7 dias |
| `requiredAddress` | false | false | produto digital, sem endereço |
| `showTimer`, `showCoupon`, `socialProof`, `checkoutPlugins` | desligados/null | manter | sem cronômetro, sem urgência falsa, sem depoimento |
| `bannerDesktop/Mobile` | null | manter null | checkout limpo |
| Imagem do produto | placeholder | **capa 500×500** (`capa/capa-500.jpg`, ver seção 5) | confiança visual; Bruno sobe pelo painel |
| Campos obrigatórios | nome, e-mail, telefone e CPF do checkout padrão [H] | manter (exigidos pelo gateway/antifraude) | não há como reduzir por API [NC]; sem formulário de captação antes da compra |
| Página de obrigado | padrão do ClickMax | `https://infoprodutos-zion.clickmax.space/obrigado-mini-mentoria` (rascunho v2, precisa estar **publicada**) | ver seção 6 |
| Segurança / selo | do próprio ClickMax/Ticto | não configurável | o texto de segurança vem do checkout padrão [NC] |

## 3. Payload completo de `offers_update` (NÃO enviado; é substituição total)
Enviar todos os campos abaixo; um campo omitido pode voltar ao padrão [H]. Antes de enviar, reler `offers_get` e conferir que nada mudou.
```json
{
  "workspaceId": "e87e8ba9-37cf-4c54-9a97-3e4e1b01827a",
  "id": "0c71eeba-2654-432c-9701-0a31e6113a08",
  "name": "Mini Mentoria de Estruturação Zion",
  "checkoutTitle": "Mini Mentoria de Estruturação Zion",
  "description": "Formação digital autônoma para estruturar um empreendimento turístico no seu terreno: 9 módulos e 70 aulas e materiais (aulas gravadas, fichas interativas, e-books por pilar, 2 planilhas em branco, Kit do Investidor e kit de comandos para IA, como modelos) e o Dossiê em PDF. Acesso por 12 meses. Pagamento único de R$47, sem mensalidade. Pix ou cartão à vista. Reembolso em 7 dias. Sem reunião e sem atendimento individual. Parcerias e investimentos não são garantidos nem fazem parte da compra.",
  "type": "course",
  "productType": "internal",
  "productClass": "Curso",
  "productCategory": "Negócios e Carreira",
  "currency": "BRL",
  "originalPrice": 4700,
  "newPrice": null,
  "defaultInstallment": 1,
  "paymentConfig": {"pix": {"active": true}, "boleto": {"active": false}, "credit": {"active": true, "installments": 1}, "recurrence": null},
  "limitToRefund": 7,
  "supportPhone": "+55 48 6137-1061",
  "softDescriptor": "ZIONACADEMY",
  "requiredAddress": false,
  "showDescription": true,
  "showTimer": false,
  "timerMinutes": 10,
  "showCoupon": false,
  "highlightInstallment": false,
  "passPlatformFee": false,
  "allowAffiliateResale": true,
  "audience": "everyone",
  "requiredOffersMatch": "any",
  "checkoutImageSource": "product",
  "bannerDesktop": null,
  "bannerMobile": null,
  "socialProof": null,
  "checkoutPlugins": null,
  "country": "BR",
  "language": "pt",
  "offerSupportEmailId": null
}
```
Pontos de atenção: (a) a descrição acima tem 496 caracteres (limite 1000); (b) o e-mail de suporte que consta na oferta não está no esquema do `offers_update` e não foi copiado para o repositório; conferir no painel depois do envio que ele permaneceu; (c) a oferta está `approved`: alterar nome ou descrição pode exigir nova revisão do ClickMax [NC]; conferir `status` e `canSell` logo depois; (d) a oferta ainda não tem vendas (`hasTransaction` false), o que reduz o risco.

## 4. Antes e depois (checkout visto pelo comprador)
| | Antes | Depois (esperado, [NC] até Bruno ver) |
|---|---|---|
| Nome | Mini Mentoria de Estruturação | Mini Mentoria de Estruturação Zion |
| Imagem | placeholder do ClickMax | capa com tela real da plataforma e "R$47" |
| Descrição | boa, mas sem a contagem de módulos | 9 módulos, 70 aulas e materiais, 12 meses, R$47, Pix/cartão, 7 dias |
| Preço, pagamento | R$ 47, Pix e cartão 1x | igual |
| Distrações | nenhuma | nenhuma |

## 5. Capa do produto (500×500)
Arquivos: `capa/capa.html` (molde), `capa/render.js`, `capa/capa-1080.jpg` e `capa/capa-500.jpg`. Fundo musgo `#1B2117`, logo oficial claro, tela real da plataforma (aula do Marco Zero), texto "Mini Mentoria de Estruturação Zion · R$47 · pagamento único · 12 meses de acesso" e a linha "Para Airbnb, casas, apartamentos, pousadas e glampings". Sem pessoas e sem foto de hospedagem de destaque (a única imagem de hospedagem é o fundo da própria tela real). Revisada visualmente em 25/11. Regerar: `NODE_PATH=$(npm root -g) node zion-sales-engine/08-checkouts/capa/render.js` e reduzir para 500×500.
**Como aplicar (Bruno):** painel → Produtos → Mini Mentoria → oferta → Imagem do produto → enviar `capa-500.jpg` (JPG até 2 MB). `offers_set_product_image` só aceita uma URL do armazenamento do ClickMax; depois do upload no painel posso conferir por `offers_get` (`thumbnail`).

## 6. Obrigado, entrega e eventos (ligações do checkout)
1. Publicar `/obrigado-mini-mentoria` (depois da revisão v2 abaixo; exige "aprovado").
2. Painel → oferta → Configurações do checkout → **Página de obrigado** → colar a URL acima [rótulo exato NC].
3. Reversão: apagar o campo (volta à página padrão).

## 7. Reversão do `offers_update`
Reenviar o mesmo payload com `name` "Mini Mentoria de Estruturação", `checkoutTitle` null e a `description` anterior (guardada na seção 1 por `offers_get` de 25/11: "Formação digital para estruturar um empreendimento turístico no seu terreno. Aulas gravadas, fichas e formulários interativos, e-books por pilar, planilhas de cálculo e kits (Kit do Investidor e kit de prompts, como modelos para você preencher). Metodologia Zion: Marco Zero e sete pilares. Acesso por 12 meses. Pagamento único. Sem acompanhamento individual e sem reunião. Parcerias e investimentos são possibilidades sujeitas à análise da Zion, não garantias. Reembolso em 7 dias."). Os acessos de compradores não dependem do nome da oferta.

## 8. Roteiro de validação no celular (Bruno)
Use o celular com 4G, janela anônima, **sem pagar** (a menos que escolha testar o Pix, ver item 7).
1. Abra a página rascunho (A ou B v2) pelo painel → "Visualizar". Confira: preço, 12 meses, 9 módulos, 70 aulas e materiais, Pix e cartão, garantia 7 dias aparecem **antes** do botão de pagar.
2. Toque no botão do topo (A): deve **rolar** até a demonstração, nunca abrir pagamento. Na B, não há botão no topo.
3. Role até a oferta e toque em "QUERO ACESSAR A PLATAFORMA POR R$47": deve descer até o checkout.
4. No checkout: nome do produto = "Mini Mentoria de Estruturação Zion"; valor R$ 47; sem cronômetro, sem endereço, sem campo estranho; imagem da capa; descrição legível; botão de finalizar visível sem esforço; Pix e cartão só à vista.
5. Anote: quantos campos pede, se o teclado cobre o botão, se a página rola sem travar.
6. Confira se aparece alguma palavra "inscrição", "cadastro", "reunião" ou "Club" em qualquer ponto. Se aparecer, fotografe.
7. (Teste de ponta a ponta, exige "aprovado" e uma compra real de R$ 47 com reembolso depois) Pagar por Pix; conferir: pagamento aprovado → página de obrigado → e-mail de acesso [NC] → login no portal → módulo Comece aqui. Qualquer etapa que falhar, registrar o horário.
