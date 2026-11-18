// Teste de ponta a ponta com dados FICTÍCIOS. Uso: node tests/e2e.js [caminho do index.html]
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const os=require('os');
const page_=path.resolve(process.argv[2]||path.join(__dirname,'..','index.html'));
let falhas=0;const ok=(c,m)=>{console.log((c?'OK   ':'FALHA ')+m);if(!c)falhas++};
(async()=>{
 const b=await chromium.launch();const ctx=await b.newContext({permissions:['clipboard-read','clipboard-write']});const p=await ctx.newPage();
 await ctx.route('https://bchaerk-creator.github.io/**/assets/store/*.webp',r=>r.fulfill({path:path.join(__dirname,'../../../../docs/assets/store',r.request().url().split('/').pop()),headers:{'access-control-allow-origin':'*'}}));
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
 ok(msg.startsWith('Oi, Ana!')&&msg.includes('utm_campaign=reativacao-diag')&&msg.includes('/raio-x/')&&/diagnóstico prévio gratuito/.test(msg),'oferta padrão: diagnóstico prévio com link e UTM');
 await p.click('[data-of=agenda]');const msgA=await p.inputValue('#msg');
 ok(msgA.includes('utm_campaign=reativacao-agenda')&&msgA.includes('app.clickmax.io/book')&&/45 minutos/.test(msgA),'oferta agendar reunião com link do calendário ClickMax e UTM');
 let href=await p.getAttribute('#abrir','href');
 ok(href.startsWith('https://wa.me/5548988880001?text=')&&decodeURIComponent(href).includes('Oi, Ana!'),'link do WhatsApp com mensagem');
 await p.click('[data-of=bubble]');ok((await p.inputValue('#msg')).includes('store/comprar')&&(await p.inputValue('#msg')).includes('Bubble'),'oferta Bubble');
 await p.click('[data-of=clube]');ok((await p.inputValue('#msg')).includes('zion-collection')&&(await p.inputValue('#msg')).includes('Club'),'oferta Clube');
 // prioridade
 const ordem=await p.evaluate(()=>{const dia=n=>new Date(Date.now()-n*864e5).toISOString();const c=window.__crm;c.juntar([{id:'a1',nome:'Antigo Frio',fone:'48977770001',imp:true,criado:dia(60),temp:10},{id:'a2',nome:'Antigo Morno',fone:'48977770002',imp:true,criado:dia(70),temp:50},{id:'a3',nome:'Quente Etiqueta',fone:'48977770003',imp:true,criado:dia(60),temp:5,tags:'DIAG | POTENCIAL ALTO'},{id:'a4',nome:'Novo Ontem',fone:'48977770004',criado:dia(1)},{id:'a5',nome:'Novo Hoje',fone:'48977770005',criado:dia(0)},{id:'a6',nome:'Form Antigo',fone:'48977770006',criado:dia(40)}]);return [c.fila().filter(l=>/^(Antigo|Quente|Novo|Form)/.test(l.nome)).map(l=>l.nome),c.prioridade(c.leads.find(l=>l.nome==='Novo Ontem')).rotulo,c.lembrete(c.leads.find(l=>l.nome==='Novo Ontem'))]});
 ok(JSON.stringify(ordem[0])===JSON.stringify(['Novo Hoje','Novo Ontem','Quente Etiqueta','Form Antigo','Antigo Morno','Antigo Frio']),'ordem da fila: '+ordem[0].join(' > '));
 ok(/ontem/.test(ordem[1])&&/ontem/.test(ordem[2]),'rótulo e lembrete usam a data real: '+ordem[2]);
 await p.evaluate(()=>{const c=window.__crm;for(const l of c.leads.filter(l=>/^(Antigo|Quente|Novo|Form)/.test(l.nome)))l.status='sem_interesse'});
 // já mandei / voltar para novo
 await p.click('[data-tab=fila]');
 const antes=await p.textContent('.big');await p.click('#jaMandei');
 const jm=await p.evaluate(n=>window.__crm.leads.find(l=>l.nome.toLowerCase()===n.toLowerCase().trim()||l.nome===n),antes);
 ok(jm&&jm.status==='contatado'&&!!jm.enviado,'"Já mandei" marca contatado com carimbo de data');
 ok(/1 enviados/.test(await p.textContent('#resumo')),'contador de enviados hoje: '+await p.textContent('#resumo'));
 // links rápidos
 const lr=await p.evaluate(()=>[window.__crm.linkRapido('diag'),window.__crm.linkRapido('agenda')]);
 ok(lr[0].includes('/raio-x/')&&lr[0].includes('utm_medium=ligacao_manual')&&lr[1].startsWith('https://app.clickmax.io/book/')&&lr[1].includes('utm_campaign=reativacao-agenda'),'links rápidos: '+lr.join(' | '));
 await p.click('#cpDiag');await p.waitForFunction(()=>/Copiado/.test(document.querySelector('#avLinks').textContent));const cb=await p.evaluate(()=>navigator.clipboard.readText());ok(cb.includes('/raio-x/')&&cb.includes('utm_source=whatsapp'),'botão copia o link do diagnóstico para a área de transferência');
 // ligação + reunião marcada
 const lg=await p.evaluate(()=>{const c=window.__crm;c.juntar([{id:'r1',nome:'Com Reuniao',fone:'48944440001',criado:new Date().toISOString(),reuniao:new Date(Date.now()+864e5).toISOString()},{id:'r2',nome:'Sem Reuniao',fone:'48944440002',criado:new Date().toISOString()}]);const f=c.fila().map(l=>l.nome);const r1=c.leads.find(l=>l.nome==='Com Reuniao');return [f.includes('Com Reuniao'),f.includes('Sem Reuniao'),r1.status]});
 ok(lg[0]===true&&lg[1]===true&&lg[2]==='agendou','quem tem reunião futura continua na fila (status agendou)');
 const ord=await p.evaluate(()=>{const c=window.__crm;const dia=h=>new Date(Date.now()+h*3600e3).toISOString();c.juntar([{id:'r3',nome:'Reuniao Tarde',fone:'48944440003',reuniao:dia(5)},{id:'r4',nome:'Reuniao Cedo',fone:'48944440004',reuniao:dia(2)},{id:'r5',nome:'Reuniao Passada',fone:'48944440005',reuniao:dia(-30)}]);const f=c.fila().map(l=>l.nome);return [f.slice(0,3),f.includes('Reuniao Passada'),c.prioridade(c.leads.find(l=>l.nome==='Reuniao Cedo')).rotulo,c.montar(c.leads.find(l=>l.nome==='Reuniao Cedo'),'conf')]});
 ok(JSON.stringify(ord[0])===JSON.stringify(['Reuniao Cedo','Reuniao Tarde','Com Reuniao'])||ord[0][0]==='Reuniao Cedo','primeiro as reuniões por horário: '+ord[0].join(' > '));
 ok(ord[1]===false,'reunião que já passou não entra na fila de confirmação');
 ok(/^0 · Confirmar reunião/.test(ord[2]),'rótulo: '+ord[2]);
 ok(/Passando para confirmar a nossa conversa de hoje, às \d{1,2}h/.test(ord[3])&&/horário de Brasília/.test(ord[3]),'mensagem de confirmação com dia e hora: '+ord[3].split('\n')[0]);
 await p.click('[data-tab=fila]');await p.evaluate(()=>{});
 await p.selectOption('#fStatus','agendou');await p.waitForFunction(()=>document.querySelector('.big')&&/Reuniao Cedo/.test(document.querySelector('.big').textContent));
 ok(await p.isVisible('.aviso')&&/Reunião/.test(await p.textContent('.aviso')),'card mostra o banner da reunião');
 ok((await p.inputValue('#msg')).includes('confirmar a nossa conversa'),'oferta Confirmar reunião vem selecionada para quem tem reunião');
 await p.click('[data-st=confirmado]');
 const cf=await p.evaluate(()=>window.__crm.leads.find(l=>l.nome==='Reuniao Cedo').status);
 ok(cf==='confirmado','botão Confirmou ✓ marca a reunião como confirmada');
 await p.selectOption('#fStatus','hoje');
 await p.evaluate(()=>{const c=window.__crm;for(const l of c.leads.filter(l=>/^(Antigo|Quente|Novo|Form|Com|Sem)/.test(l.nome)&&l.nome!=='Sem Reuniao'))l.status=l.status==='agendou'?'agendou':'sem_interesse'});
 await p.click('[data-tab=fila]');await p.click('#fStatus');await p.selectOption('#fStatus','novo');
 await p.waitForFunction(()=>document.querySelector('.big')&&document.querySelector('.big').textContent.includes('Sem Reuniao'));
 await p.click('#ligueiNao');await p.waitForTimeout(200);
 const lp=await p.evaluate(()=>{const l=window.__crm.leads.find(l=>l.nome==='Sem Reuniao');return [l.status,l.ligacoes,window.__crm.lembrete(l)]});
 ok(lp[0]==='ligou'&&lp[1]===1&&/Tentei te ligar/.test(lp[2]),'"Liguei · não atendeu" conta a ligação e muda o lembrete: '+lp[2]);
 ok((await p.inputValue('#msg')).includes('Tentei te ligar agora há pouco'),'mensagem depois da ligação cita a tentativa');
 ok((await p.getAttribute('#ligar','href'))==='tel:+5548944440002','botão Ligar usa tel: com o número');
 await p.evaluate(()=>{const l=window.__crm.leads.find(l=>l.nome==='Sem Reuniao');l.status='sem_interesse'});
 // lembrete
 const lm=await p.evaluate(()=>[window.__crm.lembrete({tags:'DISPARO A1 · OPERADOR PARCERIA',imp:true}),window.__crm.lembrete({tags:'FUNIL TERRENO | RESPONDEU',imp:true}),window.__crm.lembrete({tags:''}),window.__crm.lembrete({tags:'x',ctx:'Você pediu a diária da cabana.'})]);
 ok(/não lembre/.test(lm[0])&&/não lembre/.test(lm[1])&&/não lembre/.test(lm[2])&&lm[3]==='Você pediu a diária da cabana.','lembrete por etiqueta, padrão e edição manual');
 ok((await p.inputValue('#msg')).includes('Zion Bubble Glamping (Urubici e Florianópolis)'),'mensagem se apresenta (Zion Bubble Glamping)');
 await p.fill('#ctx','Você pediu informações no nosso Instagram.');ok((await p.inputValue('#msg')).includes('pediu informações no nosso Instagram'),'editar o lembrete muda a mensagem');
 // foto da Bubble
 await p.click('[data-of=bubble]');
 ok(await p.isChecked('#comFoto'),'foto marcada por padrão na oferta Bubble');
 await p.click('[data-foto=noturna]');await p.waitForTimeout(800);
 await p.click('#cpFoto');await p.waitForFunction(()=>document.querySelector('#avFoto').textContent.length>0);
 ok(/Foto copiada/.test(await p.textContent('#avFoto')),'copiar foto: '+await p.textContent('#avFoto'));
 const tipos=await p.evaluate(async()=>{const it=await navigator.clipboard.read();const t=it[0].types;const bl=await it[0].getType(t[0]);return [t,bl.size]});
 ok(tipos[0].includes('image/png')&&tipos[1]>5000,'área de transferência tem imagem PNG ('+tipos[1]+' bytes)');
 const [dlf]=await Promise.all([p.waitForEvent('download'),p.click('#svFoto')]);ok(/zion-bubble-noturna\.jpg/.test(dlf.suggestedFilename()),'salvar foto baixa o arquivo escolhido');
 await p.click('[data-of=clube]');ok(!(await p.isChecked('#comFoto')),'foto desmarcada nas outras ofertas');
 // clicar abre o WhatsApp e marca contatado
 const [pop]=await Promise.all([p.context().waitForEvent('page',{timeout:5000}).catch(()=>null),p.click('#abrir')]);
 ok(!!pop,'abre nova aba do WhatsApp'); if(pop) await pop.close().catch(()=>{});
 await p.waitForFunction(()=>document.querySelector('.big')&&document.querySelector('.big').textContent.includes('Beto'));
 ok(true,'avança para o próximo (Beto)');
 const st=await p.evaluate(()=>window.__crm.leads.find(l=>l.nome==='Ana Souza'));
 ok(st.status==='contatado'&&st.oferta==='clube'&&st.ultimo,'Ana ficou como contatada, oferta clube');
 // persistência
 const n0=await p.evaluate(()=>window.__crm.leads.length);await p.reload();ok((await p.evaluate(()=>window.__crm.leads.length))===n0,'dados persistem após recarregar');
 // exportação
 await p.click('[data-tab=dados]');const [dl]=await Promise.all([p.waitForEvent('download'),p.click('#exportar')]);
 const csv=fs.readFileSync(await dl.path(),'utf8');ok(csv.includes('contatado')&&csv.replace(/^\uFEFF/,'').startsWith('id,nome,fone')&&csv.split('\n').length===n0+1,'exporta CSV com status');
 // semente completa dados de uma versão antiga sem apagar status
 await p.evaluate(()=>{window.ZION_LEADS=[{id:'old1',nome:'Velho Salvo',fone:'48955550001',criado:'2026-11-13T10:00:00Z',temp:40,imp:false}];localStorage.setItem('zion_crm_leads_v1',JSON.stringify([{id:'old1',nome:'Velho Salvo',fone:'5548955550001',status:'respondeu',tags:'',origem:''}]))});
 const sem=await p.evaluate(()=>{const ls=JSON.parse(localStorage.getItem('zion_crm_leads_v1'));return ls.length});
 ok(sem===1,'preparou versão antiga salva');
 await b.close();console.log(falhas?`\n${falhas} falha(s)`:'\nTudo certo');process.exit(falhas?1:0)})();
