'use strict';
// Teste local com Playwright (Chromium) em servidor HTTP local. Sem rede externa.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { chromium } = require('playwright');

const js = fs.readFileSync(path.join(__dirname, 'persistir-utm.js'), 'utf8');
const html = `<!doctype html><html><head><meta charset="utf-8"><script>${js}</script></head><body>teste</body></html>`;

(async () => {
  const srv = http.createServer((q, r) => { r.writeHead(200, { 'content-type': 'text/html' }); r.end(html); });
  await new Promise((r) => srv.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${srv.address().port}/p`;
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  const search = async () => page.evaluate(() => Object.fromEntries(new URLSearchParams(location.search)));
  let results = [];
  const ok = (name) => { results.push(name); console.log('ok -', name); };

  // 1) primeiro toque: anuncio com UTMs completas
  await page.goto(`${base}?utm_source=meta&utm_medium=paid&utm_campaign=c1&utm_content=cr1&utm_term=111&sck=222&ad_id=111&campaign_id=222&adset_id=333&fbclid=ABC`);
  let s = await search();
  assert.equal(s.utm_campaign, 'c1'); assert.equal(s.fbclid, 'ABC');
  ok('primeira visita guarda e mantem a URL');

  // 2) volta por link de WhatsApp (canal), sem ids do anuncio
  await page.goto(`${base}?utm_source=whatsapp&utm_medium=bela&utm_campaign=fluxo1&src=whatsapp_bela#pagar`);
  s = await search();
  assert.equal(s.utm_source, 'whatsapp', 'canal do link atual nao e sobrescrito');
  assert.equal(s.src, 'whatsapp_bela');
  assert.equal(s.sck, '222', 'id da campanha devolvido');
  assert.equal(s.ad_id, '111'); assert.equal(s.adset_id, '333'); assert.equal(s.fbclid, 'ABC');
  assert.equal(await page.evaluate(() => location.hash), '#pagar', 'ancora preservada');
  ok('link de canal recebe ids do anuncio sem perder o canal nem a ancora');

  // 3) link sem nenhum parametro
  await page.goto(base);
  s = await search();
  assert.equal(s.utm_source, 'meta'); assert.equal(s.utm_content, 'cr1');
  ok('visita sem parametros recebe a origem guardada');

  // 4) expirado (31 dias) nao e usado
  await page.evaluate(() => { const o = JSON.parse(localStorage.getItem('zion_first_touch_v1')); o.t -= 31 * 864e5; localStorage.setItem('zion_first_touch_v1', JSON.stringify(o)); });
  await page.goto(base);
  s = await search();
  assert.deepEqual(s, {});
  ok('origem com mais de 30 dias nao e reaproveitada');

  // 5) nunca inventa: contexto novo, sem parametros
  const page2 = await (await browser.newContext()).newPage();
  await page2.goto(base);
  assert.deepEqual(await page2.evaluate(() => Object.fromEntries(new URLSearchParams(location.search))), {});
  ok('navegador sem historico nao ganha parametro nenhum');

  // 6) sem localStorage nao quebra
  const ctx3 = await browser.newContext();
  await ctx3.addInitScript(() => { Object.defineProperty(window, 'localStorage', { get() { throw new Error('bloqueado'); } }); });
  const page3 = await ctx3.newPage();
  const errors = []; page3.on('pageerror', (e) => errors.push(e));
  await page3.goto(`${base}?utm_source=meta`);
  assert.equal(errors.length, 0);
  assert.equal((await page3.evaluate(() => new URLSearchParams(location.search).get('utm_source'))), 'meta');
  ok('storage bloqueado: sem erro e URL intacta');

  await browser.close(); srv.close();
  console.log(`${results.length} testes passaram`);
})().catch((e) => { console.error('FALHOU', e); process.exit(1); });
