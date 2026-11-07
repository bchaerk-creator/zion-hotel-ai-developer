// Gera o roteiro narrado tutorial/<ID>.json a partir da própria ferramenta (telas, campos, nomes) + perfil 1 de testes.
// Uso: node tutorial/gen.js A01 A03 ...
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http');
const ROOT = path.join(__dirname, '..', 'app');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
const strip = s => String(s || '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
const lower1 = s => s.charAt(0).toLowerCase() + s.slice(1);
(async () => {
  const srv = await new Promise(r => { const s = http.createServer((q, res) => { let p = q.url.split('?')[0]; if (p.endsWith('/')) p += 'index.html'; const f = path.join(ROOT, p);
    if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res); }).listen(0, () => r(s)); });
  const b = await chromium.launch();
  for (const id of process.argv.slice(2)) {
    const page = await b.newPage(); await page.goto(`http://127.0.0.1:${srv.address().port}/index.html?p=${id}`); await page.waitForSelector('#za-next');
    const m = await page.evaluate(() => ({ tool: ZA.cfg.tool, deliverable: ZA.cfg.deliverable, title: ZA.cfg.title,
      screens: ZA.screens.map(s => ({ kind: s.kind, title: s.title, pillar: s.pillar, pillarTitle: s.pillarTitle, fields: (s.fields || []).map(f => ({ id: f.id, type: f.type, allowUnknown: !!f.allowUnknown, label: f.label })), actions: (s.actions || []).map(a => a.id) })) }));
    await page.close();
    const prof = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'tests', 'profiles', id + '.json'), 'utf8')).profiles[0];
    const V = prof.values;
    const fillOps = (fields, unkOne) => { const ops = []; let unkDone = false;
      for (const f of fields) {
        if (unkOne && !unkDone && f.allowUnknown) { ops.push(['unk', f.id]); unkDone = true; continue; }
        if (V[f.id] === undefined) continue; ops.push(['fill', f.id, V[f.id]]);
      } return { ops, unkDone }; };
    const S = m.screens, start = 2, p1form = 5;
    // tela-vitrine: exercício (fora do pilar 1) com mais campos digitáveis e, de preferência, com "não sei"
    let best = -1, show = 15;
    S.forEach((s, i) => { if (s.kind !== 'form' || s.pillar < 2) return; const n = s.fields.filter(f => ['number', 'money', 'percent', 'text'].includes(f.type)).length + (s.fields.some(f => f.allowUnknown) ? 3 : 0); if (n > best) { best = n; show = i; } });
    const sh = S[show]; const shFill = fillOps(sh.fields, true);
    const p1 = fillOps(S[p1form].fields, false).ops;
    const segs = [
      { id: 's01', say: `Olá! Neste tutorial você vai ver, na prática, como usar a ferramenta ${m.tool}. No final, você recebe em PDF: ${m.deliverable}.`, do: [['move', '.za-hero h1']] },
      { id: 's02', say: 'No topo fica a barra de progresso. São quarenta telas, organizadas em sete pilares. Tudo o que você responde fica salvo automaticamente neste navegador.', do: [['move', '.za-prog']] },
      { id: 's03', say: 'O botão Telas abre o índice. Por ele, você volta a qualquer etapa já visitada para revisar ou corrigir uma resposta.', do: [['click', '#za-menu'], ['wait', 2500], ['click', '#za-close']] },
      { id: 's04', say: 'As primeiras telas mostram o problema e a ideia central do método. Leia com calma e clique em Continuar.', do: [['wait', 1500], ['click', '#za-next'], ['wait', 2500], ['click', '#za-next']] },
      { id: 's05', say: 'Nesta tela você faz a sua apresentação. Preencha os dados pedidos, sempre com a sua realidade.', do: fillOps(S[start].fields, false).ops },
      { id: 's06', say: 'Clique em Continuar. Se algum campo obrigatório ficar vazio, a ferramenta avisa antes de avançar.', do: [['click', '#za-next']] },
      { id: 's07', say: `Cada pilar tem cinco momentos. O primeiro é Aprenda: uma explicação curta, com um exemplo. Aqui, o primeiro pilar é: ${strip(S[3].pillarTitle)}.`, do: [['scroll', 300], ['wait', 1200], ['move', '.za-example'], ['wait', 800], ['click', '#za-next']] },
      { id: 's08', say: 'Depois vem Compare: duas formas de fazer, lado a lado, para você enxergar a diferença.', do: [['move', '.za-col'], ['wait', 1500], ['click', '#za-next']] },
      { id: 's09', say: 'Em seguida, Preencha. É o exercício do pilar, sempre com os seus números e as suas respostas.', do: p1 },
      { id: 's10', say: 'No momento Feedback, a ferramenta lê as suas respostas e mostra o que elas revelam.', do: [['click', '#za-next'], ['wait', 900], ['move', '.za-fb li']] },
      { id: 's11', say: 'E em Aplique, você marca as ações que vai colocar em prática. Elas entram no seu plano final.', do: [['click', '#za-next'], ['wait', 900], ...S[7].actions.slice(0, 2).map(a => ['check', `[data-act=${a}]`])] },
      { id: 's12', say: `Vamos adiantar até o pilar ${sh.pillar}: ${strip(sh.pillarTitle)}.`, do: [['prefill', show]] },
      { id: 's13', say: shFill.unkDone ? 'Se você não tiver algum dado, marque Não sei. A ferramenta continua e avisa no relatório que aquele ponto é uma hipótese, não um diagnóstico.' : 'Preencha cada campo com calma. Se tiver dúvida, a ajuda abaixo de cada campo explica o que informar.', do: shFill.ops },
      { id: 's14', say: 'Veja o feedback deste pilar: os números são calculados na hora, a partir do que você informou.', do: [['click', '#za-next'], ['wait', 900], ['move', '.za-fb li']] },
      { id: 's15', say: 'Agora, a consolidação. Aqui aparecem os indicadores, os pontos de atenção e as prioridades OP3D: do que mais pesa até a sua ação essencial agora.', do: [['prefill', 38], ['wait', 1500], ['scroll', 500], ['wait', 1200], ['scroll', 700], ['wait', 1200], ['scroll', 700]] },
      { id: 's16', say: 'Por fim, o relatório personalizado. Clique em Baixar PDF e escolha Salvar como PDF. Você também pode exportar os seus dados para continuar em outro aparelho.', do: [['go', 39], ['wait', 1000], ['move', '#za-print'], ['wait', 1800], ['move', '#za-export'], ['wait', 1500], ['scroll', 600], ['wait', 1000], ['scroll', 700]] },
      { id: 's17', say: 'Pronto. Agora é com você: preencha com a sua situação real e use o relatório para decidir os próximos passos. Aprenda o passo a passo, utilize as ferramentas e construa o seu resultado.', do: [['scroll', -4000], ['move', '.za-hero h1']] }
    ];
    fs.writeFileSync(path.join(__dirname, id + '.json'), JSON.stringify({ product: id, title: 'Tutorial · ' + m.tool, segments: segs }, null, 1));
    console.log(id, 'roteiro ok · vitrine na tela', show + 1, '· não sei:', shFill.unkDone);
  }
  await b.close(); srv.close();
})();
