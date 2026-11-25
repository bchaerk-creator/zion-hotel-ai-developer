// Teste local (Playwright) das variantes v3: SHOTS=<pasta> NODE_PATH=$(npm root -g) node teste_local_v3.js
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const PROIBIDOS = [/inscri[çc][ãa]o/i, /cadastr/i, /taxa/i, /\b70 aulas/i, /\b26\b/, /10 fichas/i, /6 modelos/i, /Sess[ãa]o de onboarding(?! e estrat)/i, /equipe entrar/i, /receber investimento/i, /s[óo]cio/i, /faturamento/i,
  /consultoria/i, /taxa de inscri/i, /s[óo]cio garantido/i, /garantimos/i, /R\$ ?97/, /R\$ ?270/, /rede de investidores/i, /simulador/i, /calculadora/i, /mapa\.jpg/i, /agendar/i, /land ?bank/i, /land members/i, /(?<!nem )boleto/i];
const CTA = 'QUERO ACESSAR A PLATAFORMA POR R$47';
(async () => {
  const b = await chromium.launch(); let falhas = 0;
  for (const v of ['a', 'b']) {
    const arq = path.join(__dirname, `variante-${v}-v3`, 'index.html');
    const html = fs.readFileSync(arq, 'utf8').replace(/<style>[\s\S]*?<\/style>/, '');
    const texto = html.replace(/<[^>]+>/g, ' ').replace('Tem reunião ou atendimento individual?', 'Tem reunião?');
    for (const re of PROIBIDOS) if (re.test(html)) { console.log(v, 'PROIBIDO:', re); falhas++; }
    // parceiro/parceria só como "potenciais parceiros" ou negação de garantia
    for (const m of texto.matchAll(/.{0,30}parcei?r[oa]s?.{0,12}/gi)) if (!/potenciais parceiros|buscar parceiros|garante parceria|garantia de parceria|garantido/i.test(m[0])) { console.log(v, 'PARCERIA fora de contexto:', m[0]); falhas++; }
    for (const m of texto.matchAll(/.{0,90}(reuni[aã]o|atendimento individual).{0,110}/gi)) if (!/(Tem reunião\?|solicitar uma reunião gratuita|reunião gratuita|não há atendimento individual contínuo|Não há atendimento individual contínuo)/i.test(m[0])) { console.log(v, 'REUNIAO fora das frases da regra:', m[0]); falhas++; }
    if (!/Formação paga · Mini Mentoria Zion · R\$47/.test(html)) { console.log(v, 'FALTA FAIXA'); falhas++; }
    if (!/Sessão de Diagnóstico Estratégico/.test(html) || !/sujeita à análise e à agenda/.test(html) || !/não são garantidos/.test(html)) { console.log(v, 'FALTA SESSAO/NOTA'); falhas++; }
    if (!/Depois da mentoria: solicite/.test(html)) { console.log(v, 'FALTA ETAPA I'); falhas++; }
    for (const [nome, w, h] of [['mobile', 390, 844], ['desktop', 1366, 800]]) {
      const p = await b.newPage({ viewport: { width: w, height: h } });
      const erros = []; p.on('pageerror', e => erros.push(String(e)));
      await p.goto('file://' + arq, { waitUntil: 'domcontentloaded' }); await p.waitForTimeout(700);
      const r = await p.evaluate((CTA) => {
        const all = [...document.querySelectorAll('[data-cx-cta]')];
        const pagar = all.filter(a => a.getAttribute('href') === '#pagar');
        const anchors = all.filter(a => a.getAttribute('href') !== '#pagar');
        const oferta = document.querySelector('#oferta');
        const pos = el => el.compareDocumentPosition(oferta); // 2 = oferta antes do el
        const antesDaOferta = all.filter(a => (oferta.compareDocumentPosition(a) & 4) === 0 && a !== oferta); // a vem antes de oferta
        const precoNode = [...document.querySelectorAll('.preco')][0];
        const primeiroPagar = pagar[0];
        const precoAntes = !!precoNode && !!(precoNode.compareDocumentPosition(primeiroPagar) & 4);
        const secs = [...document.querySelectorAll('[data-cx-section]')].map(s => s.dataset.cxSection);
        return {
          overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
          checkout: document.querySelectorAll('[data-cx-checkout]').length,
          spans: document.querySelectorAll('span').length, scripts: document.querySelectorAll('script').length,
          secoes: [...new Set(secs)].join(','),
          ctasPagar: pagar.length, pagarSemPreco: pagar.filter(a => a.textContent.trim() !== CTA).length,
          ancorasQuebradas: anchors.filter(a => !document.querySelector(a.getAttribute('href'))).length,
          ancoras: anchors.length,
          pagarAntesDaOferta: pagar.filter(a => antesDaOferta.includes(a)).length,
          ctaNoHero: document.querySelector('#hero').querySelectorAll('[data-cx-cta]').length,
          precoAntesDoPrimeiroPagar: precoAntes,
          ordemPrecoOferta: !!oferta.querySelector('.preco'),
          h1: document.querySelector('h1').innerText,
        };
      }, CTA);
      const esperaHero = v === 'a' ? 1 : 0;
      const bad = r.overflow || r.checkout !== 1 || r.spans || r.scripts || r.pagarSemPreco || r.ancorasQuebradas || r.pagarAntesDaOferta || !r.precoAntesDoPrimeiroPagar || !r.ordemPrecoOferta || r.ctaNoHero !== esperaHero || erros.length || !r.ctasPagar;
      if (bad) falhas++;
      console.log(v.toUpperCase(), nome, JSON.stringify(r), 'erros:', erros.length, bad ? 'FALHA' : 'ok');
      await p.screenshot({ path: path.join(process.env.SHOTS || __dirname, `v3-${v}-${nome}.png`), fullPage: nome === 'mobile' });
    }
  }
  await b.close(); console.log(falhas ? 'FALHAS: ' + falhas : 'TUDO OK'); process.exit(falhas ? 1 : 0);
})();
