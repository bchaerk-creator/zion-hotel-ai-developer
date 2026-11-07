// Gera promo/<ID>.json (8 cenas + narração) a partir de landings/<ID>.json + dados reais da ferramenta.
// Uso: node promo/gen.js A03 A04 ...
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), http = require('http');
const ROOT = path.join(__dirname, '..', 'app'); const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
const strip = s => String(s || '').replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();
// destaca em itálico dourado as 2 últimas palavras do título (antes da pontuação final)
const emph = t => { t = strip(t); const m = t.match(/^(.*?)([.?!]*)$/); const w = m[1].split(' '); const n = w.length > 4 ? 2 : 1; return w.slice(0, -n).join(' ') + ' *' + w.slice(-n).join(' ') + '*' + m[2]; };
const low = s => s.charAt(0).toLowerCase() + s.slice(1);
(async () => {
  const srv = await new Promise(r => { const s = http.createServer((q, res) => { let p = q.url.split('?')[0]; if (p.endsWith('/')) p += 'index.html'; const f = path.join(ROOT, p);
    if (!fs.existsSync(f)) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'content-type': MIME[path.extname(f)] }); fs.createReadStream(f).pipe(res); }).listen(0, () => r(s)); });
  const b = await chromium.launch();
  for (const id of process.argv.slice(2)) {
    const L = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'landings', id + '.json'), 'utf8'));
    const p = await b.newPage(); await p.goto(`http://127.0.0.1:${srv.address().port}/index.html?p=${id}`); await p.waitForSelector('#za-next');
    const m = await p.evaluate(() => ({ tool: ZA.cfg.tool, deliverable: ZA.cfg.deliverable, pillars: ZA.cfg.pillars.map(x => x.title) })); await p.close();
    const B = id[0] === 'B';
    const scenes = [
      { kicker: 'Zion Collection Club', title: emph(L.headline), text: strip(L.subheadline), shots: ['tela-form'],
        say: `${strip(L.headline)} ${strip(L.symptoms[0])}? ${strip(L.symptoms[1])}? Então este vídeo é para você.` },
      { kicker: 'O que quase ninguém percebe', title: emph(L.collapseTitle), text: strip(L.collapse).split('. ').slice(0, 2).join('. ').replace(/\.?$/, '.'),
        say: `${strip(L.collapseTitle)} ${strip(L.collapse).split('. ').slice(0, 2).join('. ').replace(/\.?$/, '.')}` },
      { kicker: 'O que você vai aprender', title: 'Sete pilares, *passo a passo*.', list: m.pillars.slice(0, 4),
        say: `Em sete pilares curtos, você aprende o passo a passo: ${m.pillars.slice(0, 3).map(low).join(', ')}, e ${low(m.pillars[3])}, até chegar ao seu plano.` },
      { kicker: 'A ferramenta', title: emph(m.tool) , text: 'Você preenche com os seus dados. A ferramenta calcula na hora e mostra o que eles revelam.', shots: ['tela-form', 'tela-feedback'],
        say: `Você preenche com os seus dados, e a ferramenta ${m.tool} calcula na hora e mostra, em cada pilar, o que os números revelam.` },
      { kicker: 'O que você sai sabendo', title: emph('O seu ' + (B ? 'projeto' : 'plano') + ', com os seus números.'), list: [m.deliverable + ' em PDF', 'Prioridades OP3D: do que mais pesa à ação essencial', 'Plano de ação para os próximos passos', 'Indicadores calculados com as suas respostas'], shots: ['tela-op3d'],
        say: `No final, você recebe em PDF: ${m.deliverable}, com as prioridades em três níveis e um plano de ação para os próximos passos.` },
      { kicker: 'E como funciona?', title: 'Responda. Calcule. *Decida.*', list: ['Quarenta telas curtas, no celular ou no computador', 'Feedback na hora, em cada pilar', 'Seu progresso fica salvo', 'Relatório personalizado para baixar'], shots: ['tela-relatorio'],
        say: 'Funciona no celular ou no computador. São quarenta telas curtas, com feedback na hora, progresso salvo e um relatório personalizado no final.' },
      { kicker: 'Quem está por trás', title: 'Feito por quem *opera hospedagem*.', text: 'Zion Collection Club · Hotel Business Academy, uma iniciativa do Zion Hotel Group International.', photo: 'op09', caption: 'Foto real · Zion Bubble Glamping',
        say: 'Este material é da Zion Collection Club, Hotel Business Academy, uma iniciativa do Zion Hotel Group International, que opera hospedagem de verdade.' },
      { kicker: 'Zion Collection Club', title: emph(L.finalHeadline), text: 'Aprenda o passo a passo. Utilize a ferramenta. Construa o seu resultado.', cta: true, fine: strip(L.disclaimer),
        say: 'Aprenda o passo a passo, utilize a ferramenta e construa o seu resultado. Pagamento único de vinte e sete reais.' }
    ];
    fs.writeFileSync(path.join(__dirname, id + '.json'), JSON.stringify({ id, tool: m.tool, cta: L.cta + ' · R$ 27', scenes }, null, 1));
    console.log(id, 'roteiro ok ·', m.tool);
  }
  await b.close(); srv.close();
})();
