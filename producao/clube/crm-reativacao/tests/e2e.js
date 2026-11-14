// Teste de ponta a ponta com dados FICTÍCIOS. Uso: node tests/e2e.js [caminho do index.html]
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const os=require('os');
const page_=path.resolve(process.argv[2]||path.join(__dirname,'..','index.html'));
let falhas=0;const ok=(c,m)=>{console.log((c?'OK   ':'FALHA ')+m);if(!c)falhas++};
(async()=>{
 const b=await chromium.launch();const p=await b.newPage();
 await p.goto('file://'+page_);
 // funções puras
 const r=await p.evaluate(()=>{const c=window.__crm;return{
  f1:c.normFone('(48) 99999-0001'),f2:c.normFone('+55 48 99999-0002'),f3:c.normFone('048 3333-4444'),f4:c.normFone('123'),f5:c.normFone('5548999990003'),
  n:c.primeiroNome('MARIA da Silva'),
  csv:c.mapear(c.csvParse('Nome;Whatsapp;E-mail;Cidade\n"Silva, João";48 99999-0004;j@x.com;Gramado\n'))}});
 ok(r.f1==='5548999990001','normaliza celular com máscara');
 ok(r.f2==='5548999990002','normaliza +55');
 ok(r.f3==='554833334444','normaliza fixo com zero');
 ok(r.f4==='','rejeita número curto');
 ok(r.f5==='5548999990003','mantém já normalizado');
 ok(r.n==='Maria','primeiro nome capitalizado');
 ok(r.csv[0].nome==='Silva, João'&&r.csv[0].fone==='48 99999-0004','CSV com ; e aspas');
 // importar CSV pela interface
 const tmp=path.join(os.tmpdir(),'fict.csv');
 fs.writeFileSync(tmp,'Nome,Telefone,Email,Cidade,Estado,Origem,Tags\nAna Souza,(48) 98888-0001,ana@x.com,Urubici,SC,Meta,quente\nBeto Lima,48988880002,,Gramado,RS,Meta,\nAna Souza Dup,5548988880001,,,,,\nSem Fone,,s@x.com,,,,\n');
 await p.click('[data-tab=dados]');await p.setInputFiles('#arquivo',tmp);
 await p.waitForFunction(()=>document.querySelector('#resImport').textContent.length>0);
 const res=await p.textContent('#resImport');
 ok(/3 novos, 1 unidos/.test(res)&&/1 sem telefone/.test(res),'importação: '+res);
 // fila
 await p.click('[data-tab=fila]');
 ok((await p.textContent('.big')).includes('Ana Souza'),'primeiro da fila é a Ana');
 const msg=await p.inputValue('#msg');
 ok(msg.startsWith('Oi, Ana!')&&msg.includes('utm_campaign=reativacao-agenda')&&msg.includes('app.clickmax.io/book'),'mensagem de agendamento com link e UTM');
 let href=await p.getAttribute('#abrir','href');
 ok(href.startsWith('https://wa.me/5548988880001?text=')&&decodeURIComponent(href).includes('Oi, Ana!'),'link do WhatsApp com mensagem');
 await p.click('[data-of=bubble]');ok((await p.inputValue('#msg')).includes('store/comprar')&&(await p.inputValue('#msg')).includes('Bubble'),'oferta Bubble');
 await p.click('[data-of=clube]');ok((await p.inputValue('#msg')).includes('zion-collection')&&(await p.inputValue('#msg')).includes('Club'),'oferta Clube');
 // clicar abre o WhatsApp e marca contatado
 const [pop]=await Promise.all([p.context().waitForEvent('page',{timeout:5000}).catch(()=>null),p.click('#abrir')]);
 ok(!!pop,'abre nova aba do WhatsApp'); if(pop) await pop.close().catch(()=>{});
 await p.waitForFunction(()=>document.querySelector('.big')&&document.querySelector('.big').textContent.includes('Beto'));
 ok(true,'avança para o próximo (Beto)');
 const st=await p.evaluate(()=>window.__crm.leads.find(l=>l.nome==='Ana Souza'));
 ok(st.status==='contatado'&&st.oferta==='clube'&&st.ultimo,'Ana ficou como contatada, oferta clube');
 // persistência
 await p.reload();ok((await p.evaluate(()=>window.__crm.leads.length))===3,'dados persistem após recarregar');
 // exportação
 await p.click('[data-tab=dados]');const [dl]=await Promise.all([p.waitForEvent('download'),p.click('#exportar')]);
 const csv=fs.readFileSync(await dl.path(),'utf8');ok(csv.includes('contatado')&&csv.split('\n').length===4,'exporta CSV com status');
 await b.close();console.log(falhas?`\n${falhas} falha(s)`:'\nTudo certo');process.exit(falhas?1:0)})();
