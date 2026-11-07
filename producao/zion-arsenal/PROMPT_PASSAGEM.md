# Prompt de passagem · tudo o que já existe (Zion Collection Club · Hotel Business Academy)

Cole este texto na outra conversa. Ele descreve o que já foi construído e testado, onde está, os IDs reais e as regras. Reaproveite tudo; não recomece.

---

Você vai continuar um projeto da Zion Hotel Group International (responsável: Bruno Chaerk). Abaixo está tudo o que já foi construído e testado. Antes de criar qualquer coisa nova, verifique se já existe aqui e reaproveite.

## 1. Regras fixas (valem para tudo)
- Leia primeiro o `CLAUDE.md` do repositório `bchaerk-creator/zion-hotel-ai-developer`. Ele traz as regras inegociáveis, a identidade visual, os IDs do ClickMax e os moldes.
- **Pode fazer sem pedir:** criar produto, oferta e página no ClickMax; enviar oferta para aprovação quando `offers_get_incomplete_reason` voltar vazio; publicar página de vendas só quando a oferta estiver ativa.
- **Exige "aprovado" de Bruno:** gastar com anúncio (teto atual R$ 0, campanhas só pausadas), disparar mensagens para leads, ativar automações, mexer em qualquer coisa que já existe (produtos, páginas, funis, Land Bank, Zion Collection, Clube, site institucional).
- **Sem invenção:** nada de números de mercado, depoimentos, resultados, garantias ou urgência falsa. Exemplos sempre marcados como "dados fictícios".
- **Sem promessa** de reservas, renda, retorno ou captação. A promessa padrão é "Aprenda o passo a passo para…".
- **Teste de verdade** antes de dizer que funciona, e mostre o resultado.
- **Metodologias da marca:**
  - **ECROI:** Espelhamento → Colapso de crença → Reconhecimento → Orientação → Implementação.
  - **OP3D:** priorização em três níveis (20% → 4% → 0,8%), sempre apresentada como método, nunca como garantia.

## 2. Marca
- **Nome:** Zion Collection Club. **Slogan:** Hotel Business Academy. Definido por Bruno em 07/11/2026; substituiu "Zion Arsenal". Os códigos internos ZAR-A01… e as pastas `zar-xxx` continuam iguais.
- **Cores:** preto `#040605`, musgo `#1B2117`, creme `#FEF5F0`, areia `#DED6BF`, terra `#8B714E`, champanhe `#C9B37E`.
- **Fontes:** Cormorant (títulos) e Aventa (texto), em `docs/assets/fonts/`. No ClickMax, Cormorant Garamond e Jost.
- **Logo oficial:** `docs/brand/zion-logo-claro.png` (para fundo escuro) e `zion-logo-escuro.png` (para fundo claro).
- **Fotos reais (Zion Bubble Glamping):** `docs/assets/operacoes/op01..op14.webp` e `docs/assets/store/`. As fotos op01, op02, op13 e op14 têm pessoas. Use foto de hospedagem só onde se explica de onde vem o método, sempre com legenda.

## 3. As 20 mini mentorias interativas (produto pronto e no ar)
Cada uma tem 40 telas: abertura ECROI, 7 pilares (Aprenda, Compare, Preencha, Feedback, Aplique), consolidação e relatório. A ferramenta calcula na hora, salva o progresso no navegador, aplica OP3D e gera PDF. Testes: 20 de 20 produtos e 1.196 checks passando, com valores conferidos à mão.

- **Endereço:** `https://bchaerk-creator.github.io/zion-hotel-ai-developer/p/adbc67069af26ae0/zar-<id>/` (ex.: `zar-a02`).
- **Tutorial narrado** (~2 min, voz em português e cursor): `https://bchaerk-creator.github.io/zion-hotel-ai-developer/p/adbc67069af26ae0/tutoriais/zar-<id>-tutorial.mp4`.
- **Checkout ClickMax:** `https://payments.clickmax.io/<hash>`. Preço R$ 27, pagamento único, Pix e cartão à vista.

| ID | Mini mentoria | Ferramenta | Oferta (hash do checkout) |
|---|---|---|---|
| A01 | Seu Airbnb Está Vazio? | Raio-X Inteligente de Reservas | `ySAkZG38VS` (oferta antiga; entrega ainda aponta para `arsenal-01`, troca só com aprovado) |
| A02 | Quanto Devo Cobrar pela Minha Diária? | Precificador Inteligente Zion | `3t5odnLVmc` |
| A03 | Sua Hospedagem Fatura, mas Dá Lucro? | Calculadora de Custos e Rentabilidade | `cUzIUJQ1ol` |
| A04 | Seu Anúncio Está Afastando Hóspedes? | Construtor Inteligente de Anúncios | `pm4gC73OBW` |
| A05 | Como Fazer Sua Hospedagem Valer Mais? | Construtor de Experiências e Valor | `HD8SZHwRQy` |
| A06 | Por Que Seus Hóspedes Não Dão 5 Estrelas? | Auditor Inteligente da Experiência | `2mnKe_GNte` |
| A07 | Você Está Perdendo Reservas no Atendimento? | Assistente de Conversão de Reservas | `ei3JNcZpzt` |
| A08 | Quanto Você Deixa de Ganhar com Cada Hóspede? | Calculadora de Receitas Extras | `nvG6nEEREG` |
| A09 | Vale a Pena Investir em uma Cabana ou Airbnb? | Simulador de Viabilidade Zion | `Dv_F82gBPs` |
| A10 | Sua Hospedagem Só Funciona com Você? | Organizador Operacional Zion | `zUjBfQ9hEl` |
| B01 | Como Atrair Investimentos para Minha Terra? | Zion Investor Ready | `jJf-ANO_iD` |
| B02 | Como Atrair um Sócio para Desenvolver Minha Terra? | Simulador de Sociedade e Parcerias | `gg1fqEpX6l` |
| B03 | Como Criar um Projeto de Hospedagem Mesmo Sem Dinheiro? | Construtor de Projeto Turístico | `hreVBmnEl7` |
| B04 | Tenho Terra, mas Não Tenho Dinheiro. E Agora? | Mapa de Alternativas de Capital | `UMLnQpZR2u` |
| B05 | Como Descobrir o Potencial Turístico da Minha Terra? | Raio-X do Potencial Turístico | `5bZM1XhAf8` |
| B06 | Como Saber Quanto Custa Construir uma Hospedagem? | Calculadora de Implantação Turística | `gwCKS07Azu` |
| B07 | Qual Hospedagem Construir no Meu Terreno? | Comparador de Modelos de Hospedagem | `Cd0sSzRXaU` |
| B08 | Como Calcular o Retorno de um Projeto Turístico? | Simulador de Viabilidade Econômica (ROI, payback, VPL, TIR) | `bGYBQgSYnC` |
| B09 | Como Começar um Projeto Turístico com Pouco Capital? | Planejador de Implantação Progressiva | `4ikeRL1ZDB` |
| B10 | Como Apresentar Minha Terra para Sócios e Investidores? | Criador de Pitch e Dossiê Turístico | `UfCzHr90AJ` |

Os IDs completos (produto, oferta, entregas) estão em `producao/zion-arsenal/control/clickmax.json`. As 19 ofertas novas entregam dois links: a ferramenta e o tutorial.

## 4. ClickMax (IDs reais)
- **Workspace:** `e87e8ba9-37cf-4c54-9a97-3e4e1b01827a`.
- **Projeto:** Infoprodutos Zion, `8d1152a4-4490-4666-bcb5-582b75c82660` (`infoprodutos-zion.clickmax.space`).
- **Vendedor:** em análise. Com isso, **nenhum checkout vende**. Motivo registrado: comprovante bancário inválido; faltam Contrato Social ou MEI e o Cartão CNPJ.
- **Páginas em rascunho:**
  - landing do A02, `/zar-a02` (página `a2683126-7cdd-48dd-8c4e-c8a9c8bcc74c`, checkout vinculado);
  - vitrine com as 20, `/zion-collection-club` (página `b4de9375-196b-4132-8911-e21a13194f4a`);
  - página técnica `/zar-teste-script` (`10432164-c02e-4f41-b527-44f3961295c9`), que pode ser apagada.
- **Limitação importante:** a importação de HTML pelo MCP do ClickMax **remove JavaScript**, como confirmado em teste. Por isso as ferramentas ficam no GitHub Pages e o ClickMax só vende e entrega o link.
- **Área de membros:** portal "Zion Hospitality Business", `6d1b8c4d-05b0-4bf8-b3ba-5e8e1d0b2b79`. As ferramentas também entram como bônus nas trilhas:
  - **Desenvolvimento:** módulo 9 do curso da Trilha 1 (`fa9a6c54-e40c-4ee0-99cc-ee6ec70e68fb`, módulo `48b713d7-b356-4749-975c-90e890f358f9`), com 11 aulas: B05, B07, B03, B06, B08, A09, B09, B04, B02, B01 e B10.
  - **Gestão:** curso `a28341aa-b5c6-4d52-88d5-d68d8a1a734d`, com A02, A03 e A08.
  - **Operação:** curso `2036a7b8-3f2c-4ce9-9c99-ff4398eb64e7`, com A06 e A10.
  - **Aceleração de Vendas:** curso `f3bf41a9-537e-4a47-b83f-da83b85642ed`, com A01, A04 e A07.
  - **Identidade e Branding:** curso `b449ff2d-126b-4e00-825f-3452eb310d68`, com A05 e A04.
  - Os 4 últimos cursos ainda **não estão em nenhuma turma**. Ligue cada um quando a trilha correspondente for criada.
  - Cada aula traz o link da ferramenta e o tutorial anexado.
- **Escada de preços:** ferramentas de R$ 19 → mini mentorias de R$ 27 → trilhas.

## 5. Meta Ads
- **Integração:** conector `facebook` do Windsor.ai, com escrita (create_campaign, create_adset, create_ad_image e create_ad_video).
- **Conta escolhida por Bruno:** Zion Collection 2, `1271873041294684`.
- **Situação:** nenhuma campanha do Zion Collection Club foi criada ainda. Sempre criar **pausada**; ativar só com "aprovado".
- **Padrão:** criativo 1080×1350, botão "Saiba mais", `utm_source=meta&utm_medium=paid&utm_campaign=<produto>&utm_content=<criativo>`.

## 6. Moldes e geradores prontos (reaproveite)
Todos ficam em `producao/zion-arsenal/` no repositório.
- **Motor das mini mentorias:**
  - `app/engine.js` e `app/engine.css`; cada produto é um arquivo em `app/products/<ID>.js`.
  - Guia de autoria em `docs/AUTHORING.md` e especificação dos 20 em `docs/PRODUCTS.md`.
  - Para criar uma nova, escreva `app/products/<ID>.js` e `tests/profiles/<ID>.json` e rode `node tests/run.js <ID>`. Pronto só com 100% dos checks.
- **Publicação:** `ZA_TOOLS=<pasta com terser e clean-css> node scripts/bundle.js <IDs>` gera um HTML único por ferramenta. Copie para `docs/p/adbc67069af26ae0/zar-<id>/index.html` e faça push no `main` (o GitHub Pages publica).
- **Landing de vendas ECROI (10 dobras):**
  - `scripts/landing.js` + `landings/<ID>.json`; importe com `pages_import_html_draft` e o `offerId`.
  - `scripts/vitrine.js` gera a vitrine.
  - O ClickMax pinta `<span>` de cinza: dê cor explícita. Marque os CTAs com `data-cx-cta`.
- **Tutorial narrado com cursor:**
  - `tutorial/gen.js` gera o roteiro a partir da ferramenta;
  - `tutorial/tts.py` cria a voz;
  - `tutorial/record.js` grava;
  - `tutorial/run_all.sh` grava em lote (3 em paralelo).
- **Voz em português (grátis, local):**
  - Piper, voz `pt_BR-faber-medium`. O modelo vem de `github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-pt_BR-faber-medium.tar.bz2`; o motor é instalado com `pip install piper-tts`.
  - O HuggingFace é bloqueado neste ambiente.
- **Vídeo de apresentação 9:16 no estilo do trailer do Club:**
  - `promo/shots.js <ID>` captura telas reais;
  - `promo/make.js <ID>` monta 8 cenas ECROI com narração.
  - Roteiro de exemplo: `promo/A02.json` (amostra de 1min21s aprovada para revisão).
- **Testes:** `tests/run.js` (Playwright) cobre estrutura, 3 perfis, validação, persistência, PDF e celular. `tests/demo.js` grava uma demo curta.
- **Hosts liberados no ambiente:** `infoprodutos-zion.clickmax.space`, `api.clickmax.io` e `bchaerk-creator.github.io`.

## 7. O que ainda falta (pendências reais)
1. Aprovação do vendedor no ClickMax (depende de Bruno enviar os documentos).
2. 18 landings de venda (A01 e A03 a B10), no padrão da landing do A02.
3. Vídeos de apresentação dos outros 19 produtos (depois de Bruno aprovar a amostra do A02) e inclusão do vídeo no topo de cada landing.
4. Trocar a entrega da oferta antiga do A01 para `zar-a01` + tutorial (precisa de aprovado).
5. Ligar os 4 cursos de bônus às turmas quando as trilhas Gestão, Operação, Aceleração de Vendas e Branding existirem.
6. Campanhas no Meta, pausadas, na conta Zion Collection 2.
7. E-books complementares, roteiros Gamma, capas e criativos: não produzidos.
8. Funis, CRM e automações: não configurados (ativar exige aprovado).

## 8. Como continuar
- Comece lendo `producao/zion-arsenal/RETOMADA.md` e `control/clickmax.json`.
- Antes de criar algo no ClickMax, confira se já existe, pelos IDs acima.
- Registre cada passo novo em `RETOMADA.md` e no `control/clickmax.json`.
