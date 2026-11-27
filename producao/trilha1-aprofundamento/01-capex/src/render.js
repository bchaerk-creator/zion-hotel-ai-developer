// Imprime um HTML em PDF A4 com o Chromium do Playwright e confere o resultado.
// Uso: node src/render.js <entrada.html> <saida.pdf> [--min N] [--max N]
// Dois modos:
//  · páginas fixas (section.pg, checklist): cada página tem de caber em 297 mm, sem o conteúdo passar da margem de baixo;
//  · texto corrido (e-book, como o do Pilar 6): nenhum elemento pode passar da largura útil, nenhuma caixa
//    indivisível pode ser mais alta que a área útil da página, e o total de páginas tem de ficar entre --min e --max.
// Falha (código 1) se uma fonte (Playfair Display, Inter) não carregar ou se qualquer conferência falhar.
const { chromium } = require("playwright"); const path = require("path"); const fs = require("fs");
const args = process.argv.slice(2); const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? +args[i + 1] : d; };
const [html, pdf] = args.filter((a, i) => !a.startsWith("--") && !(i > 0 && args[i - 1].startsWith("--"))).map((p) => path.resolve(p));
const MIN = opt("--min", 1), MAX = opt("--max", 999);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 650, height: 990 } });
  await p.goto("file://" + html);
  // páginas fixas têm 210 mm de largura (794 px); o texto corrido usa a largura útil do A4 (172 mm, 650 px)
  if (await p.$("section.pg")) await p.setViewportSize({ width: 794, height: 1123 });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
  const faltam = await p.evaluate(async () => { const t = ["400 20px 'Playfair Display'", "italic 400 20px 'Playfair Display'", "400 12px Inter", "700 12px Inter"]; for (const f of t) await document.fonts.load(f); return t.filter((f) => !document.fonts.check(f)); });
  if (faltam.length) throw new Error("fonte não carregou: " + faltam.join(", "));
  await p.emulateMedia({ media: "print" });
  let erro = 0;
  const fixas = await p.$$eval("section.pg", (s) => s.length);
  if (fixas) {
    const r = await p.evaluate(() => {
      const mm = 96 / 25.4; const out = [];
      document.querySelectorAll("section.pg").forEach((s, i) => {
        const top = s.getBoundingClientRect().top; const h = s.getBoundingClientRect().height;
        const pad = parseFloat(getComputedStyle(s).paddingBottom); let fundo = 0;
        s.querySelectorAll("*").forEach((e) => { const bb = e.getBoundingClientRect(); if (bb.height && getComputedStyle(e).position !== "absolute") fundo = Math.max(fundo, bb.bottom - top); });
        const lim = h - pad;
        out.push({ pagina: i + 1, alturaMm: +(h / mm).toFixed(1), conteudoMm: +(fundo / mm).toFixed(1), folgaMm: +((lim - fundo) / mm).toFixed(1) });
      });
      return out;
    });
    for (const x of r) { const ok = x.alturaMm <= 297.1 && x.folgaMm >= 0; if (!ok) erro++; console.log(`pág ${x.pagina}  altura ${x.alturaMm} mm  conteúdo até ${x.conteudoMm} mm  folga ${x.folgaMm} mm${ok ? "" : "  <<< TRANSBORDA"}`); }
  } else {
    // área útil do miolo: 297 − 18 − 17 = 262 mm de altura; 210 − 38 = 172 mm de largura
    const r = await p.evaluate(() => {
      const mm = 96 / 25.4, W = 172 * mm, Hu = 262 * mm, prob = []; const x0 = document.body.getBoundingClientRect().left;
      document.querySelectorAll("body *").forEach((e) => {
        const bb = e.getBoundingClientRect(); if (!bb.width) return;
        const cs = getComputedStyle(e); if (cs.position === "absolute") return;
        if (bb.right - x0 > W + 1) prob.push(`largura: <${e.tagName.toLowerCase()} class="${e.className}"> vai até ${((bb.right - x0) / mm).toFixed(1)} mm`);
        if (cs.breakInside === "avoid" && e.tagName !== "TR" && bb.height > Hu) prob.push(`caixa mais alta que a página (${(bb.height / mm).toFixed(0)} mm): ${e.className} "${e.textContent.slice(0, 50)}"`);
        if (!e.classList.contains("capa") && e.scrollWidth > e.clientWidth + 2 && cs.overflow !== "visible" && e.clientWidth) prob.push(`texto cortado: ${e.className}`);
      });
      return { largura: document.body.scrollWidth / mm, prob };
    });
    r.prob.slice(0, 30).forEach((x) => console.log("  <<<", x)); erro += r.prob.length;
  }
  await p.pdf({ path: pdf, format: "A4", printBackground: true, preferCSSPageSize: true });
  await b.close();
  const n = +require("child_process").execSync(`pdfinfo "${pdf}" | awk '/^Pages/{print $2}'`).toString().trim();
  const okN = n >= MIN && n <= MAX; if (!okN) erro++;
  console.log("pdf", pdf, n, "páginas", okN ? `(entre ${MIN} e ${MAX})` : `<<< fora de ${MIN} a ${MAX}`, erro ? `· ${erro} problema(s)` : "· tudo dentro da página");
  process.exit(erro ? 1 : 0);
})();
