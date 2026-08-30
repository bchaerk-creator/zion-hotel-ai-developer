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

## Camada de movimento (Motion)

As animações usam o [Motion](https://motion.dev) (antigo `framer-motion`), auto-hospedado
em `assets/js/` — sem CDN em runtime, sem build, sem npm.

| Arquivo | Papel |
|---|---|
| `assets/js/motion.dom.js` | Bundle UMD do Motion (`framer-motion/dom` v13.1.1, MIT, ~45 KB gzip). Expõe o global `Motion`. Não editar — é vendorizado. |
| `assets/js/zion-motion.js` | Camada da Zion: reveals com stagger, contadores, parallax do relevo no hero. |
| `assets/js/motion.LICENSE.md` | Licença MIT do Motion. |

### Aprimoramento progressivo

A base continua sendo CSS. O Motion só entra por cima:

1. No `<head>`, `window.ZION_MOTION` é `false` se o visitante pediu `prefers-reduced-motion`.
2. Se o Motion carregar, `zion-motion.js` assume os reveals e marca `window.ZION_MOTION_READY`.
3. Se não carregar (rede, bloqueio, erro), o `IntersectionObserver` de cada página assume
   300 ms após o `load`.

**O conteúdo nunca fica invisível**, mesmo sem JavaScript algum. Ao mexer nas animações,
mantenha essa garantia.

### Atualizar o Motion

```bash
npm pack framer-motion@latest
tar xzf framer-motion-*.tgz
cp package/dist/dom.js docs/assets/js/motion.dom.js
```

Depois teste as 5 páginas nos três caminhos: com Motion, com o script bloqueado e com
`prefers-reduced-motion: reduce`.
