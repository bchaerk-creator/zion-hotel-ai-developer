#!/usr/bin/env node
// Grava um vídeo HTML (com window.seek e window.DURACAO) em MP4, quadro a quadro.
// Uso:
//   node producao/video/motion/render.js <pasta-do-video> [--formato 9x16|16x9] [--fps 30] [--quadros 0,5,10]
// --quadros gera só PNGs desses instantes (folha de contato para revisar antes de gravar tudo).
// Precisa de: playwright (npm i -g playwright, ou NODE_PATH apontando para ele) e ffmpeg no PATH.
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

let chromium;
try { ({ chromium } = require('playwright')); } catch {
  try { ({ chromium } = require(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'))); } catch {
    console.error('Playwright não encontrado. Rode: npm i -g playwright'); process.exit(1);
  }
}

const args = process.argv.slice(2);
const opt = (nome, padrao) => { const i = args.indexOf('--' + nome); return i >= 0 ? args[i + 1] : padrao; };
const pasta = path.resolve(args.find(a => !a.startsWith('--') && !args[args.indexOf(a) - 1]?.startsWith('--')) || '.');
const formato = opt('formato', '9x16');
const fps = parseInt(opt('fps', '30'), 10);
const quadros = opt('quadros', null);
const [W, H] = formato === '16x9' ? [1920, 1080] : [1080, 1920];
const saida = path.join(pasta, 'saida');
fs.mkdirSync(saida, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(pasta, 'index.html') + `?formato=${formato}&render=1`);
  await page.evaluate(() => window.pronto);
  const duracao = await page.evaluate(() => window.DURACAO);
  const quadro = async t => {
    const url = await page.evaluate(t => { window.seek(t); return document.querySelector('canvas').toDataURL('image/png'); }, t);
    return Buffer.from(url.split(',')[1], 'base64');
  };

  if (quadros) {
    for (const t of quadros.split(',').map(Number)) {
      const arq = path.join(saida, `quadro-${formato}-${String(t).replace('.', '_')}s.png`);
      fs.writeFileSync(arq, await quadro(t));
      console.log(arq);
    }
    await browser.close();
    return;
  }

  const arq = path.join(saida, `${path.basename(pasta)}-${formato}.mp4`);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'slow', '-movflags', '+faststart', arq],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const total = Math.round(duracao * fps);
  for (let i = 0; i < total; i++) {
    const buf = await quadro(i / fps);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % fps === 0) process.stdout.write(`\r${formato}: ${Math.round(i / fps)}s / ${duracao}s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log(`\n${arq}`);
})();
