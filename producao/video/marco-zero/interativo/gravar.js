// Grava index.html (window.seek) em quadros PNG, 30 fps, para o ffmpeg montar o MP4.
const path = require('path'), fs = require('fs');
const { chromium } = require(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'));
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.join(__dirname, 'index.html') + '?render=1'); await p.evaluate(() => window.pronto);
  fs.mkdirSync(path.join(__dirname, 'quadros'), { recursive: true });
  const d = await p.evaluate(() => window.DURACAO), tempos = process.argv.slice(2).map(Number);
  const lista = tempos.length ? tempos : [...Array(d * 30).keys()].map(i => i / 30);
  for (const [i, t] of lista.entries()) {
    await p.evaluate(t => window.seek(t), t);
    await p.locator('#palco').screenshot({ path: path.join(__dirname, 'quadros', tempos.length ? `t${t}.png` : `${String(i).padStart(4, '0')}.png`) });
  }
  await b.close();
})();
