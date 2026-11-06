# CLAUDE.md · Máquina de produtos Zion Hotel Academy

Regras fixas para toda sessão neste repositório. Responsável: Bruno Chaerk · Zion Hotel Group International.
O prompt de cada produto só precisa dizer o que muda: produto, público, dor, preço, formato e autorizações.

## 1. Regras inegociáveis
- **Autorização permanente de Bruno (06/11/2026), sem pedir "aprovado" a cada produto:**
  - produzir os produtos do catálogo, um por vez, e criar produto, oferta e página no ClickMax;
  - enviar a oferta para aprovação assim que `offers_get_incomplete_reason` voltar vazio;
  - publicar a página de vendas quando a oferta estiver **ativa** (aprovada), para ninguém cair num checkout que não vende;
  - usar nas copies que a sequência ou os scripts "partem da rotina usada nas unidades da Zion" (quando for verdade para o produto).
  - **Continua exigindo "aprovado" de Bruno:** gastar com anúncio (teto atual: R$ 0; campanhas só pausadas), disparar mensagens para leads, ativar automações, mexer em qualquer coisa que já existe.
  - Depois de cada publicação ou envio, registrar no `OFERTA.md` e no resumo da sessão.
- **Não mexa no que já existe:** produtos, páginas, funis, automações, checkouts, Land Bank, Zion Collection, integrações com Asaas, o site institucional (`docs/`) e o Clube. Crie tudo novo e separado.
- **Sem invenção:** nada de números de mercado, depoimentos, resultados, garantias, preço "de" falso, bônus ou urgência falsa. Exemplos sempre marcados como "dados fictícios".
- **Sem promessa** de reservas, ocupação, renda, investimento ou valorização. Use a promessa "Aprenda o passo a passo para ...". Diferencie o tempo para começar a usar do resultado externo.
- **Teste de verdade** antes de dizer que funciona, e mostre o resultado. Nunca diga que testou sem ter executado.
- **Dados pessoais e credenciais:** não peça senha nem credencial no chat e não colete dados desnecessários.

## 2. Identidade Zion
- **Cores:** preto `#040605`, verde musgo `#1B2117`, creme `#FEF5F0`, areia `#DED6BF`, terra `#8B714E`, dourado champanhe `#C9B37E`.
- **Fontes:** Cormorant (títulos) e Aventa (texto) em `docs/assets/fonts/`. No ClickMax, use Cormorant Garamond e Jost (Google Fonts).
- **Logo oficial:** `docs/brand/zion-logo-claro.png` (fundo escuro) e `zion-logo-escuro.png` (fundo claro). Não crie outro logo.
- **Fotos reais da Zion Bubble Glamping** (Urubici e Florianópolis): `docs/assets/operacoes/op01..op14.webp` e `docs/assets/store/`. Também ficam públicas em `https://bchaerk-creator.github.io/zion-hotel-ai-developer/<caminho a partir de docs/>`. Não apresente pessoas como clientes ou equipe da Zion sem autorização. Nunca use imagem gerada como foto real.
- **Texto:** português brasileiro simples, voz "nós", pouco texto por tela, botões claros. Pense primeiro no celular.

## 3. ClickMax (ids reais)
- Workspace: `e87e8ba9-37cf-4c54-9a97-3e4e1b01827a` (Bruno's Workspace).
- Projeto para todos os infoprodutos: **Infoprodutos Zion** `8d1152a4-4490-4666-bcb5-582b75c82660`, endereço `infoprodutos-zion.clickmax.space`.
- Padrão de oferta:
  - pagamento único, Pix e cartão à vista, sem boleto e sem recorrência;
  - `softDescriptor` `ZIONACADEMY`;
  - `supportPhone` `+55 48 6137-1061`;
  - e-mail de suporte da conta;
  - reembolso em 7 dias, como prevê o Código de Defesa do Consumidor.
- Carregue a skill do ClickMax antes de usar as ferramentas, e confira a conta de vendedor com `sellers_status`.
  - Status em nov/2026: em análise; conta bancária aprovada.
  - Com o vendedor pendente, nenhum checkout vende.
- Página de vendas: `pages_generation_context_get` → `pages_validate_html` → `pages_import_html_draft`, com o `offerId`.
  - Marque `data-cx-section` (hero, problem, solution, offer, cta, faq, social-proof), `data-cx-cta` nos botões e `<div data-cx-checkout></div>`.
  - O ClickMax pinta todo `<span>` de cinza: dê cor explícita aos spans da página.
- Entrega:
  - **área de membros**: `portals_*`, `classroom_*`, `content_*`, `lesson_*` e `offers_add_membership_delivery`;
  - **link**: `offers_add_link_delivery`;
  - **arquivo**: `offers_add_file_delivery` com URL pública, ou Bruno sobe em Produtos → oferta → "Cadastrar E-Books, PDFs ou Arquivos Digitais".
- Uma tag isolada não comprova pagamento nem entrega: verifique o caminho completo, do pagamento confirmado até o acesso.
- A aprovação da oferta é feita por uma pessoa do ClickMax: envie para aprovação só depois que `offers_get_incomplete_reason` voltar vazio.
- Plano B: Hotmart, com o mesmo produto.

## 4. Produtos já existentes neste repositório
| Produto | Pasta | ClickMax |
|---|---|---|
| Arsenal Interativo 01 · Seu Airbnb Está Vazio? (40 telas, 7 pilares, dossiê em PDF) | `producao/academy01/arsenal/` | Oferta `1ff56fea-8d49-4018-b0cd-e64e408eddf3` (R$ 27, checkout `ySAkZG38VS`) |
| Landing do Arsenal 01 | `producao/academy01/landing/` | Página `82e1bb5f-9f91-4dc7-9a3d-c6635dbee0e6` (rascunho, `/academy-01`) |
| Ferramenta 01 · Planilha Diária Mínima | `producao/low-ticket/01-diaria-minima/` | Oferta `974727ce-d051-4c86-99b6-c3b04fdf9d8e` (R$ 19, checkout `-e5nx6Wvi9`) |
| Ferramenta 17 · Checklist de Limpeza, Inspeção e Liberação | `producao/utilitarios/17-checklist-limpeza/` | Oferta `08ad22e8-9f9a-4244-856f-1bca05234924` (R$ 19, checkout `uB0Db7Gpg4`), página `023476bb-0ea7-41b2-ba99-73c62a5aa94c` (rascunho, `/checklist-limpeza`) |
| Ferramenta 11 · Kit de Mensagens de Chegada e Saída | `producao/utilitarios/11-mensagens-chegada-saida/` | Oferta `fad5df5a-49fa-442e-aed7-c08cf2f6f92f` (R$ 19, checkout `X4mTsfhUtb`), página `545010c0-a48c-4555-9b73-d501dac3c6a7` (rascunho, `/kit-mensagens`) |
| Catálogo de 10 e-books e 30 ferramentas | `producao/catalogo/CATALOGO.md` | Ordem de produção e pendências |
| Mapa de 30 oportunidades e priorização | `producao/low-ticket/MAPA_OPORTUNIDADES.md` | Fila dos próximos produtos |

Escada de preços (Estratégia Low Ticket Ladeira): ferramentas de R$ 19 → Arsenal R$ 27 → Trilhas. Cada degrau entrega a sua promessa sozinho.

## 5. Como construir (moldes já testados: reaproveite, não recomece)
- **Planilha:** gere com `openpyxl` como em `producao/low-ticket/01-diaria-minima/build_planilha.py`.
  - Sempre duas versões: em branco e com exemplo.
  - Inclua a aba "Comece aqui" e use amarelo para o que o comprador preenche e verde para o que é calculado.
  - Teste recalculando no LibreOffice (`soffice --headless --convert-to xlsx`) e compare com uma conta independente (`test_planilha.py`).
- **App interativo:** use o molde de `producao/academy01/arsenal/`:
  - telas, salvamento local, feedback em 5 partes (resultado, significado, atenção, o que fazer, como verificar) e PDF com jsPDF via cdnjs;
  - lógica em `src/logic*.js`, testada com Node;
  - teste de ponta a ponta com Playwright, servindo o jsPDF do pacote npm, porque o cdnjs é bloqueado aqui.
- **Landing page:** use o molde de `producao/academy01/landing/` (sete bandas, fotos reais por URL pública).
- **Testes de navegador:** o Playwright já vem instalado (`require('playwright')`).
- **Ferramenta utilitária (planilha + guia + PDF + página):** use os moldes `producao/utilitarios/17-checklist-limpeza/` e `producao/utilitarios/11-mensagens-chegada-saida/` (build_planilha, test_planilha contra regra independente, build_docs + render.js, empacotar.sh, landing/build_landing.py). Fotos sem pessoas: op04, op05, op07, op08, op09, op10, op11, op12 (op01, op02, op13 e op14 têm pessoas).
- **Página no ClickMax:** sem imagens embutidas em base64 (não cabem na chamada); demonstração em HTML puro.
- **Entrega:** o ZIP fica em `dist/` (fora do git, repositório público). Bruno sobe os ZIPs pendentes de uma vez; a lista fica em `producao/catalogo/PENDENCIAS_BRUNO.md`.
- **Arquivos isolados por produto:** `producao/<linha>/<nn-nome>/` com `src/`, `dist/`, `tests/` e `OFERTA.md` (público, promessa, entregáveis, copy, perguntas frequentes, 3 anúncios, preço, custos e indicadores).

## 6. Anúncios no Meta
- **Formato:** cada criativo 1080×1350 é um anúncio. Todos levam à mesma landing, com `utm_source=meta&utm_medium=paid&utm_campaign=<produto>&utm_content=<criativo>`.
- **Botão:** no Meta o botão é de uma lista fixa; use "Saiba mais". A chamada personalizada vai na arte e na primeira linha do texto.
- **Criação de campanha:** só pelo conector da conta de anúncios (ex.: Windsor.ai), se estiver conectado. Crie sempre **pausada**, dentro do orçamento máximo do prompt, e ative só com "aprovado".
- **Medição:** compare o custo por venda com o preço menos taxas e impostos. Faturamento não é lucro.

## 7. Economia de créditos
- Uma sessão por produto. Faça as perguntas necessárias de uma vez no começo e depois execute sem idas e vindas.
- Reaproveite os moldes acima. Faça uma revisão visual, uma rodada de ajustes e entregue.
- No final, entregue: links dos rascunhos, arquivos, resultado dos testes, pendências e o que depende de Bruno.
