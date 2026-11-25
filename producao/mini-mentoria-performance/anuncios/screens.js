// Capturas reais da plataforma (build atual) com perfil de EXEMPLO (dados fictícios). Uso: node anuncios/screens.js <saida> [jspdf]
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
const OUT = path.resolve(process.argv[2] || path.join(__dirname, 'telas')); const URL = 'file://' + path.resolve(__dirname, '../dist/index.html'); fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 760, height: 500 }, deviceScaleFactor: 1.5 }); await pg.goto(URL);
  await pg.fill('#nomePf', 'Exemplo (dados fictícios)'); await pg.click('#criaPf');
  await pg.evaluate(() => { const P = RX_APP.state().P; P.identificacao = { nome: 'Pousada Exemplo (dados fictícios)', tipo: 'Pousada' }; const o = ['2', '1', '0', '1', '2', 'unknown', '1', '0', '2', '1']; for (let m = 1; m <= 7; m++) for (let i = 1; i <= 10; i++) P.respostas['m' + m + 'q' + i] = o[(i + m) % 10];
    P.calculadoras.C4 = { disponiveis: '300', vendidas: '150', receita: '45000', fixos: [{ nome: 'Aluguel', valor: '6000' }, { nome: 'Equipe e sistemas', valor: '4000' }], limpeza: '80', insumos: '20', comissoes: '100', outrosVar: '0', noitesPorEstadia: '2', quedaOcupacaoPct: '20', quedaPrecoPct: '10', altaCustosPct: '10' }; });
  await pg.evaluate(() => RX_APP.ir('aula3')); await pg.waitForTimeout(300); await pg.evaluate(() => window.scrollTo(0, 440)); await pg.screenshot({ path: path.join(OUT, 'formulario.jpg'), type: 'jpeg', quality: 90 });
  await pg.evaluate(() => RX_APP.ir('aula4')); await pg.waitForTimeout(200); await pg.evaluate(() => document.querySelector('#calcRes').scrollIntoView()); await pg.evaluate(() => window.scrollBy(0, -60)); await pg.screenshot({ path: path.join(OUT, 'calculadora.jpg'), type: 'jpeg', quality: 90 });
  await pg.evaluate(() => RX_APP.ir('diag')); await pg.waitForTimeout(200); await pg.screenshot({ path: path.join(OUT, 'diagnostico.jpg'), type: 'jpeg', quality: 90 });
  await pg.evaluate(() => RX_APP.ir('plano')); await pg.waitForTimeout(200); await pg.evaluate(() => window.scrollBy(0, 360)); await pg.screenshot({ path: path.join(OUT, 'plano.jpg'), type: 'jpeg', quality: 90 });
  await b.close(); console.log('telas ok');
})();
