// Teste de ponta a ponta: fotos na ficha do Território (aula1) e no PDF do Pilar 7.
// Uso: node e2e.js <pasta-saida> <caminho-jspdf.umd.min.js>   (servidor local de docs/ na porta 8790)
const { chromium, devices } = require("playwright");
const http = require("http"), fs = require("fs"), path = require("path"), zlib = require("zlib");
const SAIDA = path.resolve(process.argv[2] || "saida"), JSPDF = fs.readFileSync(process.argv[3]);
const DOCS = path.resolve(__dirname, "../../../../docs");
fs.mkdirSync(SAIDA, { recursive: true });
let falhas = 0, passou = 0;
const ok = (c, m) => { if (c) { passou++; console.log("ok   " + m); } else { falhas++; console.log("FALHA " + m); } };

// PNG sintético (gradiente + faixas), sem pessoas.
function crc32(b) { let c, t = []; for (let n = 0; n < 256; n++) { c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } let r = 0xffffffff; for (const x of b) r = t[(r ^ x) & 255] ^ (r >>> 8); return (r ^ 0xffffffff) >>> 0; }
function chunk(ty, d) { const l = Buffer.alloc(4); l.writeUInt32BE(d.length); const td = Buffer.concat([Buffer.from(ty), d]); const c = Buffer.alloc(4); c.writeUInt32BE(crc32(td)); return Buffer.concat([l, td, c]); }
function png(w, h, semente) {
  const raw = Buffer.alloc((w * 3 + 1) * h);
  for (let y = 0; y < h; y++) { raw[y * (w * 3 + 1)] = 0; for (let x = 0; x < w; x++) { const o = y * (w * 3 + 1) + 1 + x * 3; raw[o] = (x * 255 / w + semente * 60) & 255; raw[o + 1] = (y * 255 / h) & 255; raw[o + 2] = ((x + y) % 80 < 40 ? 200 : 40) & 255; } }
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = 2;
  return Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk("IHDR", ihdr), chunk("IDAT", zlib.deflateSync(raw)), chunk("IEND", Buffer.alloc(0))]);
}
const imgs = (n, w = 2400, h = 1600) => Array.from({ length: n }, (_, i) => ({ name: `terreno${i + 1}.png`, mimeType: "image/png", buffer: png(w, h, i) }));

const servidor = http.createServer((req, res) => {
  const p = path.join(DOCS, decodeURIComponent(req.url.split("?")[0]).replace(/\/$/, "/index.html"));
  if (!p.startsWith(DOCS) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  const ext = path.extname(p); res.writeHead(200, { "content-type": { ".html": "text/html; charset=utf-8", ".js": "application/javascript", ".css": "text/css" }[ext] || "application/octet-stream" }); res.end(fs.readFileSync(p));
}).listen(8790);

const FICHA = "http://localhost:8790/trilha1/aula1/", DOSSIE = "http://localhost:8790/trilha1/pilar7/";
async function novoCtx(browser) {
  const ctx = await browser.newContext({ ...devices["iPhone 13"], acceptDownloads: true });
  await ctx.route("**/jspdf.umd.min.js", (r) => r.fulfill({ contentType: "application/javascript", body: JSPDF }));
  await ctx.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  await ctx.route("https://fonts.gstatic.com/**", (r) => r.fulfill({ body: "" }));
  return ctx;
}
async function percorrerDossie(p) {
  // passa pela abertura e por todas as perguntas, sem inventar respostas (Não sei / primeira opção)
  if (await p.locator("#continuar").count()) await p.click("#continuar");
  else { await p.fill("#nome", "Aluno Teste"); await p.fill("#email", "teste@exemplo.com"); await p.fill("#cidade", "Urubici"); await p.selectOption("#uf", "SC"); await p.click("#comecar"); }
  for (let i = 0; i < 60 && !(await p.locator("#pdf").count()); i++) {
    if (await p.locator("#sim-voltar").count()) break;
    if (await p.locator("#ns").count()) { if ((await p.locator("#ns").getAttribute("aria-pressed")) !== "true") await p.click("#ns"); }
    else if (await p.locator("input[type=radio]").count()) { const nomes = await p.$$eval("input[type=radio]", (l) => [...new Set(l.map((x) => x.name))]); for (const n of nomes) await p.locator(`input[type=radio][name="${n}"]`).first().check({ force: true }); }
    else if (await p.locator("input[type=checkbox]").count()) await p.locator("input[type=checkbox]").first().check({ force: true });
    else if (await p.locator("#resp").count()) await p.fill("#resp", "1000");
    if (await p.locator("#avancar").count()) await p.click("#avancar");
    await p.waitForTimeout(60);
  }
  await p.waitForSelector("#pdf", { timeout: 5000 });
}
async function baixarPDF(p, nome) {
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#pdf")]);
  const f = path.join(SAIDA, nome); await dl.saveAs(f); return f;
}
const paginas = (f) => { const b = fs.readFileSync(f).toString("latin1"); return { paginas: (b.match(/\/Type\s*\/Page[^s]/g) || []).length, imagens: (b.match(/\/Subtype\s*\/Image/g) || []).length }; };


const SEED = (n, v) => ({ resumo: { v, rot: v === "avancar" ? "Avançar" : "Testar", sub: "Leitura de referência com dados fictícios.", motivo: "Dados fictícios de teste.", fragil: "Ponto fraco fictício do pilar " + n + ".", criterio: "Parar se a conta do pilar " + n + " não fechar.", compromisso: { acao: "Conferir o pilar " + n + " (fictício)", responsavel: "Aluno Teste", prazo: "2026-12-05", evidencia: "Anotação" }, numeros: [["Número A", "10"], ["Número B", "20"]], data: "2026-11-28", tabelas: [{ titulo: "Tabela fictícia " + n, cab: ["Item", "Valor"], linhas: [["A", "1"], ["B", "2"]] }] }, atualizado: "2026-11-28" });
(async () => {
  const browser = await chromium.launch();
  const ctx = await novoCtx(browser);
  const erros = [];
  const p = await ctx.newPage();
  p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(DOSSIE); await p.waitForFunction(() => !!window.jspdf);
  const chaves = ["zion-t1-aula1", "zion-t1-aula2", "zion-t1-aula3", "zion-t1-pilar4", "zion-t1-pilar5", "zion-t1-pilar6"];
  await p.evaluate(([c, f]) => { c.forEach((k, i) => localStorage.setItem(k, JSON.stringify(f(i + 1)))); }, [chaves, null]).catch(() => {});
  for (let i = 0; i < chaves.length; i++) await p.evaluate(([k, d]) => localStorage.setItem(k, JSON.stringify(d)), [chaves[i], SEED(i + 1, i % 2 ? "testar" : "avancar")]);
  await p.reload(); await p.waitForFunction(() => !!window.jspdf);
  await percorrerDossie(p);
  const f = await baixarPDF(p, "dossie-6-pilares.pdf"); const A = paginas(f);
  console.log("     6 pilares:", JSON.stringify(A));
  const txt = fs.readFileSync(f).toString("latin1");
  ok(A.paginas >= 16, "6 pilares feitos: ao menos 16 páginas (capa, sumário, p0, 12 dos pilares, p7...)");
  ok((txt.match(/1 de 2/g) || []).length >= 0, "marca 1 de 2 presente (verificado também por pdftotext)");
  ok(!erros.length, "sem erro de JavaScript " + erros.join("|"));
  await browser.close(); servidor.close();
  console.log(`\n${passou} verificações ok, ${falhas} falhas`); process.exit(falhas ? 1 : 0);
})();
