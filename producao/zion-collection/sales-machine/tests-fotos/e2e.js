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

(async () => {
  const browser = await chromium.launch();
  const ctx = await novoCtx(browser);
  const reqs = [], erros = [];
  ctx.on("request", (r) => { if (!r.url().startsWith("http://localhost:8790")) reqs.push({ url: r.url(), post: r.postDataBuffer() ? r.postDataBuffer().length : 0, m: r.method() }); });
  const p = await ctx.newPage();
  p.on("pageerror", (e) => erros.push(String(e))); p.on("console", (m) => { if (m.type() === "error" && !/Failed to load resource/.test(m.text())) erros.push(m.text()); });

  // ---------- 1) PDF sem foto: sem página extra ----------
  await p.goto(DOSSIE); await p.waitForFunction(() => !!window.jspdf);
  await percorrerDossie(p);
  const semFoto = await baixarPDF(p, "dossie-sem-foto.pdf"); const A = paginas(semFoto);
  ok(!(await p.evaluate(() => window.ZionFotos.ler().length)), "sem foto: nada salvo");
  console.log("     sem foto:", JSON.stringify(A));
  ok(A.imagens === 0, "sem foto: PDF sem imagens");
  ok(!/Fotografias da propriedade/.test(fs.readFileSync(semFoto).toString("latin1")), "sem foto: não aparece página de fotos");

  // ---------- 2) ficha: anexar 2 fotos ----------
  await p.goto(FICHA); await p.waitForSelector("#fotos-zion");
  ok(await p.locator("#fotos-zion").isVisible(), "ficha do Território mostra o bloco Fotos da propriedade");
  await p.setInputFiles("#fotos-arq", imgs(2));
  await p.waitForFunction(() => document.querySelectorAll("#fotos-grade figure").length === 2);
  ok(true, "2 fotos anexadas e exibidas");
  await p.locator("#fotos-grade input[type=text]").first().fill("Entrada do terreno"); await p.locator("#fotos-grade input[type=text]").first().blur();
  await p.screenshot({ path: path.join(SAIDA, "ficha-2-fotos.png"), fullPage: true });
  const med = await p.evaluate(() => window.ZionFotos.ler().map((f) => ({ w: f.w, h: f.h, len: f.dataUrl.length, jpeg: f.dataUrl.startsWith("data:image/jpeg"), leg: f.legenda })));
  console.log("     salvas:", JSON.stringify(med));
  ok(med.length === 2 && med.every((m) => Math.max(m.w, m.h) === 1200 && m.jpeg), "fotos reduzidas a 1200 px no lado maior, em JPEG");
  ok(med[0].leg === "Entrada do terreno", "legenda salva");
  ok(!(await p.evaluate(() => /Exif/.test(atob(window.ZionFotos.ler()[0].dataUrl.split(",")[1]).slice(0, 4000)))), "sem EXIF no resultado");

  // ---------- 3) persistência ----------
  await p.reload(); await p.waitForSelector("#fotos-grade figure");
  ok((await p.locator("#fotos-grade figure").count()) === 2, "após recarregar, as 2 fotos continuam");
  ok((await p.locator("#fotos-grade input[type=text]").first().inputValue()) === "Entrada do terreno", "após recarregar, a legenda continua");

  // ---------- 4) arquivo inválido e acima de 5 MB ----------
  await p.setInputFiles("#fotos-arq", [{ name: "doc.pdf", mimeType: "application/pdf", buffer: Buffer.from("%PDF-1.4 x") }]);
  await p.waitForTimeout(200);
  let m = await p.textContent("#fotos-msg"); ok(/JPG, PNG ou WEBP/.test(m), "arquivo inválido: mensagem clara (" + m + ")");
  await p.setInputFiles("#fotos-arq", [{ name: "grande.png", mimeType: "image/png", buffer: Buffer.alloc(5 * 1024 * 1024 + 10, 1) }]);
  await p.waitForTimeout(200);
  m = await p.textContent("#fotos-msg"); ok(/mais de 5 MB/.test(m), "acima de 5 MB: mensagem clara (" + m + ")");
  await p.setInputFiles("#fotos-arq", [{ name: "quebrada.png", mimeType: "image/png", buffer: Buffer.from("isto nao e imagem") }]);
  await p.waitForTimeout(400);
  m = await p.textContent("#fotos-msg"); ok(/Não foi possível ler/.test(m), "imagem corrompida: mensagem clara (" + m + ")");
  ok((await p.locator("#fotos-grade figure").count()) === 2, "inválidos não entram na lista");

  // ---------- 5) limite de 6 ----------
  await p.setInputFiles("#fotos-arq", imgs(5, 1600, 1200));
  await p.waitForFunction(() => document.querySelectorAll("#fotos-grade figure").length === 6);
  m = await p.textContent("#fotos-msg");
  ok((await p.locator("#fotos-grade figure").count()) === 6, "limite: 6 fotos");
  ok(/limite/.test(m), "limite: mensagem clara (" + m + ")");
  ok(await p.locator("#fotos-btn").isDisabled(), "limite: botão de escolher desativado");
  await p.screenshot({ path: path.join(SAIDA, "ficha-6-fotos.png"), fullPage: true });
  ok(await p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), "ficha sem rolagem horizontal (iPhone 13)");

  // ---------- 6) PDF com 6 fotos ----------
  await p.goto(DOSSIE); await p.waitForFunction(() => !!window.jspdf);
  await percorrerDossie(p);
  const com6 = await baixarPDF(p, "dossie-6-fotos.pdf"); const B = paginas(com6);
  console.log("     com 6 fotos:", JSON.stringify(B));
  ok(B.paginas === A.paginas + 1, `com fotos: uma página a mais (${A.paginas} -> ${B.paginas})`);
  ok(B.imagens === 6, `com fotos: 6 imagens no PDF (${B.imagens})`);

  // ---------- 7) remover e PDF com 2 fotos, conferido em imagem ----------
  await p.goto(FICHA); await p.waitForSelector("#fotos-grade figure");
  for (let i = 0; i < 4; i++) await p.locator("#fotos-grade .rm").last().click();
  ok((await p.locator("#fotos-grade figure").count()) === 2 && !(await p.locator("#fotos-btn").isDisabled()), "remover foto funciona e libera o botão");
  await p.reload(); ok((await p.locator("#fotos-grade figure").count()) === 2, "remoção persiste após recarregar");
  await p.goto(DOSSIE); await p.waitForFunction(() => !!window.jspdf);
  await percorrerDossie(p);
  const com2 = await baixarPDF(p, "dossie-2-fotos.pdf"); const C = paginas(com2);
  console.log("     com 2 fotos:", JSON.stringify(C));
  ok(C.paginas === A.paginas + 1 && C.imagens === 2, "com 2 fotos: uma página a mais e 2 imagens");
  const { execSync } = require("child_process");
  const idx = A.paginas; // a página de fotos vem depois das páginas 0 a 6 (antes da 7): conferimos por texto
  let achou = -1;
  for (let k = 1; k <= C.paginas; k++) { const t = execSync(`pdftotext -f ${k} -l ${k} "${com2}" -`).toString(); if (/Fotografias da propriedade/.test(t) && /sem verifica/.test(t)) { achou = k; break; } }
  ok(achou > 0, "página 'Fotografias da propriedade' com aviso de fotos sem verificação (página " + achou + ")");
  const tp = execSync(`pdftotext -f ${achou} -l ${achou} "${com2}" -`).toString(); ok(/Entrada do terreno/.test(tp), "legenda aparece abaixo da foto no PDF");
  const prox = execSync(`pdftotext -f ${achou + 1} -l ${achou + 1} "${com2}" -`).toString(); ok(/P.GINA 7|CAPITAL E DECIS/i.test(prox), "a página seguinte é a página 7");
  execSync(`pdftoppm -f ${achou} -l ${achou} -r 60 -png "${com2}" "${path.join(SAIDA, "pdf-pagina-fotos")}"`);
  const png1 = fs.readdirSync(SAIDA).find((f) => f.startsWith("pdf-pagina-fotos")); ok(!!png1, "página de fotos convertida em imagem: " + png1);

  // ---------- 8) rede e erros ----------
  const permitidas = (u) => /^https:\/\/(fonts\.googleapis\.com|fonts\.gstatic\.com|cdnjs\.cloudflare\.com\/ajax\/libs\/jspdf\/2\.5\.1\/)/.test(u); // recursos próprios da página (fontes e jsPDF), interceptados e servidos localmente
  const outras = reqs.filter((r) => !permitidas(r.url));
  ok(outras.length === 0, "nenhuma requisição a outro endereço além das fontes e do jsPDF da própria página (" + outras.map((r) => r.m + " " + r.url).join(", ") + ")");
  ok(reqs.every((r) => r.m === "GET" && !/base64|data:image/.test(r.url)), "todas as requisições externas são GET sem dados de foto");
  ok(!reqs.some((r) => r.post > 0), "nenhum corpo enviado (POST) a lugar nenhum");
  ok(erros.length === 0, "sem erro de JavaScript" + (erros.length ? ": " + erros.join(" | ") : ""));
  await browser.close(); servidor.close();
  console.log(`\n${passou} verificações ok, ${falhas} falhas`); process.exit(falhas ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
