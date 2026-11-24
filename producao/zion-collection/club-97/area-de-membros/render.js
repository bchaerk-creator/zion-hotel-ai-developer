// Gera o banner do portal, a capa do curso e as capas dos 10 módulos da área de membros Zion Collection.
// Uso: node producao/zion-collection/club-97/area-de-membros/render.js
const { chromium } = require('playwright'); const path = require('path');
const out = path.join(__dirname, '../../../../docs/zion-collection/club/membros');
const LINHA = 'Plataforma de estruturação de projetos de hospedagem';
// Nomes reais dos módulos no ClickMax (curso fa9a6c54…), em 24/11/2026.
const modulos = [ // [arquivo, linha de cima, título, linha de baixo, algarismo]
  ['01', 'Início', 'Comece aqui', 'Onboarding', ''],
  ['02', 'Visão geral', 'Marco Zero', 'A visão de toda a jornada', '0'],
  ['03', 'Pilar 1', 'Território e destino', '', '1'],
  ['04', 'Pilar 2', 'Mercado e demanda', '', '2'],
  ['05', 'Pilar 3', 'Produto e tipologias', '', '3'],
  ['06', 'Pilar 4', 'Modelo de negócio', '', '4'],
  ['07', 'Pilar 5', 'Masterplan faseado', '', '5'],
  ['08', 'Pilar 6', 'Pré-viabilidade', '', '6'],
  ['09', 'Pilar 7', 'Capital e Dossiê', '', '7'],
  ['10', 'Bônus', 'Ferramentas', 'Zion Collection Club', '+'],
];
const jobs = [
  // banner: texto todo na faixa central, para sobreviver ao corte largo (desktop) e ao corte estreito (celular)
  ['banner-portal.jpg', 1920, 1080, { tipo: 'banner', u: 8.6, foto: 'operacoes/op09.webp', titulo: 'Zion Collection', linha: LINHA }],
  ['banner-portal-1920x480.jpg', 1920, 480, { tipo: 'banner', u: 6.6, foto: 'operacoes/op09.webp', titulo: 'Zion Collection', linha: LINHA }],
  ['banner-portal-celular.jpg', 1080, 600, { tipo: 'banner', u: 8.4, foto: 'operacoes/op09.webp', titulo: 'Zion Collection', linha: LINHA, moldura: 1 }],
  ['curso-h.jpg', 1920, 1080, { tipo: 'capa', u: 10.8, foto: 'operacoes/op08.webp', sobre: 'Zion Collection · Curso', titulo: 'Transforme o seu terreno em um <em>projeto de hospedagem</em>' }],
  ['curso-v.jpg', 1080, 1620, { tipo: 'capa', v: 1, u: 10.8, foto: 'operacoes/op08.webp', sobre: 'Zion Collection · Curso', titulo: 'Transforme o seu terreno em um <em>projeto de hospedagem</em>' }],
];
for (const [n, sobre, titulo, linha, num] of modulos) {
  jobs.push([`modulo-${n}-h.jpg`, 1280, 720, { tipo: 'capa', mod: 1, u: 7.2, sobre, titulo, linha, num }]);
  jobs.push([`modulo-${n}-v.jpg`, 720, 1080, { tipo: 'capa', mod: 1, v: 1, u: 7.2, sobre, titulo, linha, num }]);
}
(async () => { const b = await chromium.launch();
  for (const [jpg, w, h, d] of jobs) { const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto('file://' + path.join(__dirname, 'modelo.html') + '#' + encodeURIComponent(JSON.stringify(d)));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
    const falhas = await p.evaluate(() => [...document.images].filter(i => !i.naturalWidth).length + [...document.fonts].filter(f => f.status === 'error').length);
    if (falhas) throw new Error(jpg + ': imagem ou fonte não carregou');
    await p.screenshot({ path: path.join(out, jpg), type: 'jpeg', quality: 88 }); console.log('ok', jpg); await p.close(); }
  await b.close(); })();
