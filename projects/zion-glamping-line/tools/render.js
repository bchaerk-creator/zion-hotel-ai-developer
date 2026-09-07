#!/usr/bin/env node
/*
 render.js — renderiza os visualizadores 3D (HTML gerados por build_viewer.py) com Playwright/Chromium
 (WebGL por software, SwiftShader) e exporta os GLB.

 Uso:
   NODE_PATH=/opt/node22/lib/node_modules node render.js [--model cocoon|zenith] [--views a,b,c] [--no-glb] [--no-png] [--out <dir>] [--hash env=0]

 Saídas (padrão):
   ../cocoon/renders/cocoon_<vista>.png   ../cocoon/3d/zion-cocoon.glb
   ../zenith/renders/zenith_<vista>.png   ../zenith/3d/zion-zenith.glb
*/
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const HERE = __dirname;
const PROJECT = path.dirname(HERE);
const VIEWS = ['ext_front', 'ext_side', 'ext_rear', 'ext_aerial', 'int_living', 'int_bed', 'int_bath', 'night', 'structure', 'section'];
const MODELS = {
  cocoon: { html: path.join(PROJECT, 'cocoon', '3d', 'zion-cocoon-3d.html'), renders: path.join(PROJECT, 'cocoon', 'renders'), glb: path.join(PROJECT, 'cocoon', '3d', 'zion-cocoon.glb') },
  zenith: { html: path.join(PROJECT, 'zenith', '3d', 'zion-zenith-3d.html'), renders: path.join(PROJECT, 'zenith', 'renders'), glb: path.join(PROJECT, 'zenith', '3d', 'zion-zenith.glb') },
};

function arg(name, def) { const i = process.argv.indexOf(name); return i >= 0 ? process.argv[i + 1] : def; }
const onlyModel = arg('--model', null);
const onlyViews = arg('--views', null) ? arg('--views').split(',') : VIEWS;
const doGlb = !process.argv.includes('--no-glb');
const doPng = !process.argv.includes('--no-png');
const outOverride = arg('--out', null);
const extraHash = arg('--hash', '');   // p.ex. --hash env=0 (desliga o mapa de ambiente)
const WIDTH = 1920, HEIGHT = 1080, FRAMES = 4;

async function waitFrames(page, n, timeout = 240000) {
  const start = await page.evaluate(() => window.frameCount);
  await page.waitForFunction(s => window.frameCount >= s, start + n, { timeout, polling: 200 });
}

(async () => {
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium',
    headless: true,
    args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader', '--no-sandbox', '--disable-dev-shm-usage'],
  });
  const t0 = Date.now();
  try {
    for (const [model, cfg] of Object.entries(MODELS)) {
      if (onlyModel && onlyModel !== model) continue;
      if (!fs.existsSync(cfg.html)) { console.error('HTML não encontrado:', cfg.html, '(corra build_viewer.py primeiro)'); process.exitCode = 1; continue; }
      const rendersDir = outOverride || cfg.renders; fs.mkdirSync(rendersDir, { recursive: true });
      const ctx = await browser.newContext({ viewport: { width: WIDTH, height: HEIGHT }, deviceScaleFactor: 1 });
      const page = await ctx.newPage();
      page.setDefaultTimeout(300000);
      page.on('pageerror', e => console.error(`[${model}] erro na página:`, e.message));
      page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log(`[${model}] console.${m.type()}:`, m.text().slice(0, 300)); });
      console.log(`[${model}] a abrir ${path.relative(PROJECT, cfg.html)}`);
      await page.goto('file://' + cfg.html + '#view=ext_front' + (extraHash ? '&' + extraHash : ''), { waitUntil: 'load' });
      await page.waitForFunction(() => window.sceneReady === true, null, { timeout: 300000, polling: 250 });
      const gl = await page.evaluate(() => { const c = document.createElement('canvas'); const g = c.getContext('webgl'); const d = g && g.getExtension('WEBGL_debug_renderer_info'); return d ? g.getParameter(d.UNMASKED_RENDERER_WEBGL) : 'n/d'; });
      console.log(`[${model}] cena pronta (${((Date.now() - t0) / 1000).toFixed(1)} s) · WebGL: ${gl}`);

      if (doPng) {
        for (const view of onlyViews) {
          const ok = await page.evaluate(v => window.setView(v), view);
          if (!ok) { console.error(`[${model}] vista desconhecida: ${view}`); continue; }
          await waitFrames(page, FRAMES);
          const file = path.join(rendersDir, `${model}_${view}.png`);
          await page.screenshot({ path: file, type: 'png', fullPage: false });
          const size = fs.statSync(file).size;
          console.log(`[${model}] ${view.padEnd(11)} -> ${path.relative(PROJECT, file)}  ${(size / 1024).toFixed(0)} kB`);
          if (size < 60000) console.warn(`[${model}]   aviso: PNG muito pequeno (imagem vazia?)`);
        }
      }
      if (doGlb) {
        await page.evaluate(() => window.setView('ext_front'));
        const b64 = await page.evaluate(async () => {
          const buf = await window.exportGLB();
          const bytes = new Uint8Array(buf); let s = '';
          for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
          return btoa(s);
        });
        const glbPath = outOverride ? path.join(outOverride, path.basename(cfg.glb)) : cfg.glb;
        fs.mkdirSync(path.dirname(glbPath), { recursive: true });
        fs.writeFileSync(glbPath, Buffer.from(b64, 'base64'));
        console.log(`[${model}] GLB -> ${path.relative(PROJECT, glbPath)}  ${(fs.statSync(glbPath).size / 1024).toFixed(0)} kB`);
      }
      await ctx.close();
    }
  } finally {
    await browser.close();
  }
  console.log(`concluído em ${((Date.now() - t0) / 1000).toFixed(1)} s`);
})().catch(e => { console.error(e); process.exit(1); });
