#!/usr/bin/env node
/*
 turntable.js — grava um vídeo (WebM) de órbita em torno do modelo 3D (visualizador gerado por build_viewer.py),
 com Playwright/Chromium (gravação nativa de vídeo do contexto; sem ffmpeg).

 Uso:
   NODE_PATH=/opt/node22/lib/node_modules node turntable.js [--model cocoon] [--seconds 14] [--out ../cocoon/renders/zion-casulo-orbita.webm]

 O vídeo parte da vista frontal, gira 360° em torno do centro da cabana com leve variação de altura da câmera,
 e termina na vista frontal 3/4. Resolução 1280 x 720. É uma animação técnica do modelo (não é um render fotorrealista).
*/
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const HERE = __dirname;
const PROJECT = path.dirname(HERE);
function arg(name, def) { const i = process.argv.indexOf(name); return i >= 0 ? process.argv[i + 1] : def; }
const model = arg('--model', 'cocoon');
const seconds = parseFloat(arg('--seconds', '14'));
const HTML = { cocoon: 'cocoon/3d/zion-cocoon-3d.html', zenith: 'zenith/3d/zion-zenith-3d.html', lodge: 'lodge/3d/zion-lodge-3d.html' }[model];
const NAME = { cocoon: 'zion-casulo', zenith: 'zion-safari', lodge: 'zion-lodge' }[model];
const out = path.resolve(HERE, arg('--out', `../${model}/renders/${NAME}-orbita.webm`));
const W = 1280, H = 720, FPS = 25;

(async () => {
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium', headless: true,
    args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader', '--no-sandbox', '--disable-dev-shm-usage'],
  });
  const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'zion-orbit-'));
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, recordVideo: { dir: tmp, size: { width: W, height: H } } });
  const page = await ctx.newPage();
  page.setDefaultTimeout(300000);
  await page.goto('file://' + path.join(PROJECT, HTML) + '#view=ext_front', { waitUntil: 'load' });
  await page.waitForFunction(() => window.sceneReady === true, null, { timeout: 300000, polling: 250 });
  await page.evaluate(() => { document.querySelectorAll('.brand, .bar, #hint, #load').forEach(e => { e.style.display = 'none'; }); });
  await page.evaluate(() => window.setView('ext_front'));
  // órbita: lê a posição inicial da câmera e roda em torno do alvo
  const frames = Math.round(seconds * FPS);
  const t0 = Date.now();
  for (let i = 0; i <= frames; i++) {
    const u = i / frames;
    await page.evaluate(({ u }) => {
      const c = window.camera, ct = window.controls;
      if (!c || !ct) return;
      if (!window.__orb) { const d = c.position.clone().sub(ct.target); window.__orb = { r: Math.hypot(d.x, d.z), y0: c.position.y, a0: Math.atan2(d.z, d.x), t: ct.target.clone() }; }
      const o = window.__orb; const a = o.a0 + u * Math.PI * 2; const r = o.r * (1 - 0.12 * Math.sin(u * Math.PI));
      c.position.set(o.t.x + r * Math.cos(a), o.y0 + 1.6 * Math.sin(u * Math.PI), o.t.z + r * Math.sin(a));
      c.lookAt(o.t); ct.update && ct.update();
    }, { u });
    await page.waitForTimeout(1000 / FPS);
  }
  await page.waitForTimeout(400);
  const video = page.video();
  await ctx.close();
  const file = await video.path();
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.copyFileSync(file, out);
  await browser.close();
  console.log(`vídeo -> ${path.relative(PROJECT, out)}  ${(fs.statSync(out).size / 1024).toFixed(0)} kB  (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
})().catch(e => { console.error(e); process.exit(1); });
