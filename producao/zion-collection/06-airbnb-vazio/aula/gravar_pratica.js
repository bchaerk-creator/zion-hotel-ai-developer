// Grava a videoaula prática usando a ferramenta real (dist da ferramenta) e escreve as legendas sincronizadas.
// Uso: node aula/gravar_pratica.js <jspdf.umd.min.js>   → aula/dist/pratica_raw.webm + aula/dist/videoaula_pratica.srt
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const JSPDF = fs.readFileSync(process.argv[2], 'utf8'); const D = path.resolve(__dirname, 'dist');
const PR = JSON.parse(execFileSync('python3', ['-I', '-c', `import sys,json;sys.path.insert(0,${JSON.stringify(__dirname)});from roteiro import PRATICA;print(json.dumps(PRATICA))`]).toString());
const dur = f => f.split(/\s+/).length / 2.2 + 1.5;
const tc = s => { const ms = Math.round(s * 1000), h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, se = Math.floor(ms / 1000) % 60; return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(se).padStart(2, '0')},${String(ms % 1000).padStart(3, '0')}`; };
function quebrar(f) { const o = []; let c = []; for (const w of f.split(/\s+/)) { c.push(w); if (c.length >= 12 || (c.length >= 6 && /[.:?!]$/.test(w))) { o.push(c.join(' ')); c = []; } } if (c.length) o.push(c.join(' ')); return o; }
(async () => {
  const b = await chromium.launch({ args: ['--lang=pt-BR'], env: { ...process.env, LANG: 'pt_BR.UTF-8', LANGUAGE: 'pt_BR' } });
  const ctx = await b.newContext({ locale: 'pt-BR', timezoneId: 'America/Sao_Paulo', viewport: { width: 1920, height: 1080 }, recordVideo: { dir: D, size: { width: 1920, height: 1080 } } });
  await ctx.route('**/jspdf.umd.min.js', r => r.fulfill({ contentType: 'application/javascript', body: JSPDF }));
  const p = await ctx.newPage(); const t0 = Date.now(); const now = () => (Date.now() - t0) / 1000;
  await p.goto('file://' + path.resolve(__dirname, '../ferramenta/dist/diagnostico-zion-de-oferta.html'));
  await p.addStyleTag({ content: 'body{zoom:1.45} html{scroll-behavior:smooth}' });
  await p.evaluate(() => localStorage.clear());
  const marcas = []; const espera = ms => p.waitForTimeout(ms);
  const rolar = async (sel) => { await p.locator(sel).first().evaluate(e => e.scrollIntoView({ behavior: 'smooth', block: 'center' })); await espera(900); };
  const acoes = {
    abrir: async () => { await espera(800); },
    perfil: async () => { await p.click('#p_nome'); await p.type('#p_nome', 'Minha hospedagem', { delay: 70 }); await p.type('#p_periodo', 'últimos 90 dias', { delay: 70 }); },
    exemplo: async () => { await rolar('#btnExemplo'); await espera(500); await p.click('#btnExemplo'); },
    notas1: async () => { await rolar('#c_fotos'); await espera(1500); await rolar('#c_titulo'); await espera(2500); await rolar('#c_preco'); },
    notas2: async () => { await rolar('#c_diferenciais'); await espera(2000); await rolar('#c_atendimento'); await espera(2500); await rolar('#c_conforto'); },
    resultado: async () => { await rolar('#btnCalcular'); await p.click('#btnCalcular'); await espera(3000); await rolar('.barra'); },
    foco: async () => { await rolar('.foco'); },
    plano: async () => { await rolar('#btnPlano'); await p.click('#btnPlano'); await espera(1200);
      for (let i = 0; i < 3; i++) { await rolar(`[data-pl="${i}"][data-k="responsavel"]`); await p.type(`[data-pl="${i}"][data-k="responsavel"]`, 'Ana', { delay: 90 }); await p.fill(`[data-pl="${i}"][data-k="prazo"]`, `2026-12-${String(i * 7 + 1).padStart(2, '0')}`); } },
    exportar: async () => { await rolar('#btnPDF'); await p.click('#btnPDF'); await espera(1200); await p.click('#btnCSV'); },
    fechar: async () => { await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'smooth' })); },
  };
  for (const [id, tit, fala] of PR) {
    const ini = now(); await acoes[id](); const resto = dur(fala) - (now() - ini); if (resto > 0) await espera(resto * 1000);
    marcas.push([ini, now() - ini, fala]);
  }
  await espera(1000); const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), path.join(D, 'pratica_raw.webm'));
  const L = []; let n = 1;
  for (const [ini, d, fala] of marcas) { const ps = quebrar(fala), tot = ps.reduce((a, x) => a + x.split(' ').length, 0); let t = ini + 0.3; const u = d - 0.6;
    for (const x of ps) { const dd = u * x.split(' ').length / tot; L.push(n++, `${tc(t)} --> ${tc(t + dd - 0.05)}`, x, ''); t += dd; } }
  fs.writeFileSync(path.join(D, 'videoaula_pratica.srt'), L.join('\n'));
  console.log('gravado', now().toFixed(1), 's'); await b.close();
})();
