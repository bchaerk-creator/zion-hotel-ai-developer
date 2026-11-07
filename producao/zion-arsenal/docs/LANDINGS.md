# Como fazer a landing de venda de uma mini mentoria (padrão Zion Collection Club)

Referência pronta e aprovada: `landings/A02.json` → `node scripts/landing.js A02` → `out/landings/A02.html` (importada no ClickMax como rascunho em `/zar-a02`).

## 1. Copy (`landings/<ID>.json`)
Copie a estrutura de `landings/A02.json` e preencha **todos** os campos para o seu produto. Use como fonte:
- `docs/PRODUCTS.md` (dor, gancho, espelhamento, colapso, ferramenta, 7 pilares, entrega);
- `app/products/<ID>.js` (títulos reais dos 7 pilares, entrega, disclaimer do produto).

Campos:
- `code` (ex.: "ZAR-A03"), `title`, `tool`, `seoTitle` ("<título> · Zion Collection Club"), `seoDescription` (≤ 155 caracteres);
- `headline` (o gancho, em forma de pergunta) e `subheadline` (o que ele descobre ou monta, com a ferramenta);
- `cta`: um rótulo curto e o **mesmo** em todos os botões (ex.: "Quero meu diagnóstico");
- `collapseTitle` e `collapse` (o colapso de crença do PRODUCTS.md);
- `symptoms`: 5 situações reais em que o público se reconhece;
- `solutionTitle`, `solution`, `pillars`: 7 pares [título real do pilar, frase curta];
- `demoTitle`, `demoSteps` (4 passos), `demoInputs` (4 a 5 linhas [rótulo, valor]), `demoResult` (HTML com 2 a 3 linhas `<div class='row' style='border:0'><span>…</span><b>…</b></div>` e um `<p style='margin:8px 0 0;font-size:14px'>…</p>` interpretando o exemplo);
- `implementation`, `deliverables` (5 itens: mini mentoria 40 telas/7 pilares/7 exercícios; a ferramenta e o que ela calcula; o relatório em PDF pelo nome real; e-book complementar; acesso no celular ou computador com salvamento automático);
- `faq`: 6 pares; inclua "Tem acompanhamento?" (não), "Garante resultado?" (não, explicando) e "Como recebo o acesso?" ("Após a aprovação do pagamento, você recebe por e-mail o link de acesso à sua mini mentoria e o tutorial em vídeo.");
- `finalHeadline`, `disclaimer` (específico: B01 "Não garante captação de investimento", B08 "Não garante retorno" etc.).

## 2. Números da demonstração: SEMPRE da ferramenta real
Não invente nem calcule de cabeça. Abra a ferramenta com o perfil 1 de `tests/profiles/<ID>.json` e leia os resultados:
```js
// node -e com playwright: abrir app/index.html?p=<ID> (sirva a pasta app via http), preencher ZA.state().v com profile.values e ler ZA.calc().c e ZA.cfg.metrics(...)
```
Use esses valores (entradas do perfil e resultados) em `demoInputs` e `demoResult`. A landing já diz "Números fictícios, apenas para demonstrar o funcionamento".

## 3. Regras de conteúdo (obrigatórias)
- Português do Brasil, frases curtas, voz próxima. Sem jargão.
- **Proibido:** prometer reservas, faturamento, lucro, retorno, captação de investidores, aprovação de licença; inventar estatística, depoimento ou "resultado de aluno"; preço "de" falso; urgência ou bônus falsos.
- Use "Aprenda o passo a passo para…". O produto é educacional e de autoaplicação: sem mentoria, consultoria ou acompanhamento.
- Coleção B (terrenos): temas jurídicos, ambientais e societários → "consulte profissional habilitado".
- Público: os produtos servem para Airbnb, casas, apartamentos, pousadas e glampings (A). Não restrinja a bubble/glamping.

## 4. Gerar e conferir
- `node scripts/landing.js <ID>` → `out/landings/<ID>.html`.
- Screenshot no celular (iPhone 13) e no desktop; confira que não há rolagem horizontal (`scrollWidth > innerWidth` deve ser falso), que nada ficou cortado e que não aparece "undefined".

## 5. Importar no ClickMax (rascunho)
- Workspace `e87e8ba9-37cf-4c54-9a97-3e4e1b01827a`, projeto `8d1152a4-4490-4666-bcb5-582b75c82660`.
- `mcp__clickmax__pages_import_html_draft` com:
  - `manifest: {"recipeId":"sales"}`;
  - `offerId`: o da oferta do produto em `control/clickmax.json` (`products.<ID>.offerId`);
  - `placement: {projectId, name: "<ID> · <título> · Venda R$ 27", type: "sales", path: "/zar-<id em minúsculas>"}`;
  - `html`: o conteúdo **exato** de `out/landings/<ID>.html`.
- Avisos de paleta (`brand: #... is not in the workspace palette`) são esperados; ignore. Erros (`REQUIRED_...`) precisam ser corrigidos.
- **Nunca** publique a página, nunca edite páginas existentes e nunca use outro path. Se o path já existir, pare e relate.
- Guarde o `pageId` retornado.
