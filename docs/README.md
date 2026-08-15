# Site · Zion Hotel Group International

Site institucional do grupo + página do founder, construídos com a identidade visual oficial Zion e estrutura de copy ECROI. Arquivos autocontidos (CSS + fonte Aventa variável embutida em base64), sem dependências externas e sem build.

## Páginas

### `index.html` — Zion Hotel Group International
Site institucional acoplando as **três modalidades** do grupo:

1. **Zion Hotel Development** — desenvolvimento imobiliário turístico (diagnóstico, viabilidade, produto, estrutura, captação)
2. **Zion Hotel Management** — operação, performance, padrão e governança
3. **Zion Collection** — a bandeira, com as 5 coleções: Bubble, Mountain, Beach, Wellness e Signature

Mais o **ecossistema** completo: Zion Bubble Glamping, Zion Advisory, Zion Hospitality Academy, Zion Capital, Zion Exchange, Zion Design Studio e Zion Glamp Store. Inclui método Pirâmide Invertida©, projetos, seção do founder e CTA de Diagnóstico Territorial.

### `development.html` · `management.html` · `collection.html` — modalidades
Páginas internas dedicadas, uma por modalidade, no mesmo padrão visual: hero próprio, "para quem é", processo/pilares detalhados, entregas em grade e CTA segmentado. Interligadas pela navegação e pelos botões "Explorar a Modalidade" da home.

### `capital.html` — Zion Capital (investidores institucionais)
Página da **rodada Fase 1 da Zion Collection**, construída sobre os dados do *Zion Collection Investment Teaser 2026*: hero, números da plataforma, track record de Urubici e Florianópolis, **esteira de destinos** filtrável, as três fases, o aporte (US$ 21,6 mi em duas tranches), o retorno (preferência de 20% a.a., IRR 38,0%, MOIC 1,62x), a cascata de distribuição, a tabela de reciclagem por ondas, estrutura societária, Land Partnership Model, taxas da plataforma, sete riscos com mitigadores, FAQ, o funil NDA→Closing e aviso legal.

A esteira é renderizada a partir do array `DESTINOS`, no `<script>` ao final do arquivo — **é o único lugar a editar** para incluir, remover ou atualizar um destino:

```js
{
  nome:'Gramado', local:'Serra Gaúcha · RS',
  estagio:'onda1',              // operacao | onda1 | selecionado
  etiqueta:'Onda 1 · Tranche A',
  tese:'...',                   // 2 a 3 linhas
  specs:[['Unidades','12 Bubble Suites'],['CAPEX do destino','≈ R$ 4,9 mi'],
         ['Fase','01 · Asset Light'],['Implantação','6 meses']],
  nota:'Liberação no closing',
  cta:'Acessar data room', href:'#convite'
}
```

Os filtros no topo da seção leem o campo `estagio`; `specs` aceita 2 ou 4 pares `[rótulo, valor]`. Todos os números da página vêm do teaser — ao atualizar o teaser, atualize também esta página.

### `bruno.html` — Bruno Chaerk (founder)
Página pessoal one-page: espelhamento, colapso de crença, método, resultados, ecossistema e educação. Interligada ao site do grupo pela navegação.

## Identidade

Direção de arte com referências de luxo de Aman Resorts e Six Senses, mantendo o DNA Zion:

- Paleta oficial: `#040605` preto, `#FEF5F0` creme, `#DED6BF` areia, `#8B714E` terra, `#1B2117` verde musgo
- Display serifada Cormorant Garamond light (com itálico verdadeiro, subsetada e embutida) para títulos em caixa baixa, no código visual Aman
- Aventa (variável, embutida) para labels em CAPS espaçadas, corpo e navegação
- Heros centrados e contemplativos, CTAs silenciosos de borda fina, fade-in suave ao rolar
- Bandas territoriais: curvas de nível SVG em areia sobre preto como camada imersiva (slots prontos para receber fotografia editorial real)
- Palavras com linha conectora, zero gradientes, espaço negativo generoso


## Conversão e medição (HubSpot)

- Formulário "Diagnóstico Estratégico Zion" (portal 51284703) embutido na seção de contato da home
- CTA alternativo de agendamento: meetings.hubspot.com/bruno-chaerk
- Tracking code HubSpot em todas as páginas (analytics + associação de leads)

## Performance e SEO

- Fontes WOFF2 subsetadas e externalizadas em `assets/fonts/` (~25 KB cada, cache entre páginas); HTML de 14 a 44 KB
- Favicon, canonical, og:image (`assets/og.jpg`), sitemap.xml, robots.txt e JSON-LD Organization

## Deploy

Qualquer host estático:

- **GitHub Pages**: Settings → Pages → Deploy from branch → pasta `/docs`
- **Vercel / Netlify**: apontar para a pasta `docs/`
- **Teste local**: abrir `docs/index.html` no navegador

## Personalização

- CTAs apontam para o Instagram `@brunochaerkofc`. Para trocar por WhatsApp ou formulário (GoHighLevel), buscar por `instagram.com/brunochaerkofc` nos HTMLs.
- Fotografias editoriais podem ser adicionadas como camadas com overlay escuro, conforme brand guideline.
