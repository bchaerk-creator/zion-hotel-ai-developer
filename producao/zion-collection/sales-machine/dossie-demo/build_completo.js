const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://'+__dirname+'/exemplo-completo.html',{waitUntil:'load'});
  await p.evaluate(()=>document.fonts.ready);
  await p.pdf({path:__dirname+'/dist/Meu-Projeto-Exemplo-Completo.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});
  await b.close(); console.log('pdf ok');
})();
