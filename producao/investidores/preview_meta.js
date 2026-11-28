// Prévia mobile SIMULADA do formulário (não é a prévia oficial do Meta). Gera prints/meta-form-*.png a partir de meta_form_spec.json
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const S=JSON.parse(fs.readFileSync(path.join(__dirname,'meta_form_spec.json'),'utf8'));
const css=`*{box-sizing:border-box}body{margin:0;width:390px;min-height:760px;background:#f0f2f5;font:15px/1.4 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1c1e21}
.bar{background:#fff;padding:12px 16px;border-bottom:1px solid #dadde1;display:flex;justify-content:space-between;font-weight:600}
.pg{display:flex;gap:8px;align-items:center;padding:10px 16px;background:#fff;font-size:13px;color:#65676b}.av{width:28px;height:28px;border-radius:50%;background:#19291F}
.card{background:#fff;margin:10px;border-radius:10px;padding:16px}h1{font-size:20px;margin:0 0 4px}h2{font-size:17px;margin:0 0 12px;line-height:1.3}
.sub{color:#65676b;margin:0 0 12px}.p{margin:0 0 10px;font-size:14px}.o{border:1px solid #ccd0d5;border-radius:8px;padding:12px;margin-bottom:8px;font-size:14px}
.btn{background:#1877f2;color:#fff;border-radius:8px;text-align:center;padding:12px;font-weight:600;margin-top:8px}.bt2{background:#e4e6eb;color:#1c1e21}
.in{border:1px solid #ccd0d5;border-radius:8px;padding:12px;margin-bottom:8px;color:#8a8d91;background:#fff}.st{font-size:12px;color:#65676b}
.pill{display:inline-block;background:#fff3cd;border:1px solid #e0c36a;color:#7a5b00;border-radius:6px;padding:2px 8px;font-size:11px;margin-bottom:8px}`;
const wrap=(inner,step)=>`<style>${css}</style><div class="bar"><span>✕</span><span>${step}</span><span></span></div><div class="pg"><div class="av"></div>Zion Glamping Collection · Patrocinado</div>${inner}<div style="text-align:center;font-size:11px;color:#8a8d91;padding:8px">SIMULAÇÃO para aprovação · não é a prévia oficial do Meta</div>`;
const q=n=>S.perguntas.find(x=>x.n===n);const qcard=(x,pill)=>`<div class="card">${pill?`<div class="pill">${pill}</div>`:''}<h2>${x.label}</h2>${x.opcoes.map(o=>`<div class="o">${o[1]}</div>`).join('')}<div class="btn">Avançar</div></div>`;
const screens={
 '1-intro':wrap(`<div class="card"><h1>${S.intro.titulo}</h1><p class="sub"><b>${S.intro.subtitulo}</b></p>${S.intro.descricao.map(d=>`<p class="p">${d}</p>`).join('')}<div class="btn">Avançar</div></div>`,'Formulário'),
 '2-q1':wrap(qcard(q(1)),'Pergunta 1 de 12'),
 '3-q5':wrap(qcard(q(5),'Sujeita à política do Meta: pode ir para a qualificação privada'),'Pergunta 5 de 12'),
 '4-q10':wrap(qcard(q(10),'Opção 1 aguarda decisão (operações à parte)'),'Pergunta 10 de 12'),
 '5-contato':wrap(`<div class="card"><h2>Seus dados</h2>${S.contato.map(c=>`<div class="in">${c}</div>`).join('')}<div class="o">☐ Autorizo a Zion a entrar em contato comigo por WhatsApp.</div><p class="st">Ao enviar, você concorda com a <u>${S.privacidade.texto}</u> da Zion.</p><div class="btn">Avançar</div></div>`,'Dados de contato'),
 '6-revisao':wrap(`<div class="card"><h2>Revise suas respostas</h2><p class="st">Etapa de alta intenção: o Meta mostra um resumo e pede confirmação antes do envio.</p>${[1,2,7,12].map(n=>`<div class="o"><div class="st">${q(n).label}</div>${q(n).opcoes[0][1]}</div>`).join('')}<div class="btn">Enviar</div><div class="btn bt2">Voltar</div></div>`,'Revisar'),
 '7-final':wrap(`<div class="card" style="text-align:center"><h1>${S.final.titulo}</h1><p class="p">${S.final.descricao}</p><div class="btn">${S.final.botao}</div><p class="st">${S.final.url}</p></div>`,'Concluído')};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:760},deviceScaleFactor:1});
for(const [k,h] of Object.entries(screens)){await p.setContent(`<!doctype html><meta charset=utf-8>${h}`);await p.screenshot({path:path.join(__dirname,'prints',`meta-form-${k}.png`),fullPage:true})}
await b.close()})();
