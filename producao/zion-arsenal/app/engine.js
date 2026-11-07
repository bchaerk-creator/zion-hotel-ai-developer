/* Zion Collection Club — motor interativo reutilizável (v1)
 * Um único motor; cada mini mentoria é um arquivo products/<ID>.js que chama ZA.register({...}).
 * Estrutura obrigatória: 3 telas de abertura + 7 pilares × 5 momentos + consolidação + relatório = 40 telas.
 * Sem dependências externas. Estado salvo no navegador (localStorage) a cada alteração.
 */
(function(){
'use strict';
var ZA = window.ZA = window.ZA || {};
var MOMENTS = {learn:'Aprenda', compare:'Compare', form:'Preencha', feedback:'Feedback', apply:'Aplique'};
var ORDER = ['learn','compare','form','feedback','apply'];

/* ---------- utilidades ---------- */
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function isNum(x){return typeof x==='number'&&isFinite(x);}
var fmt = {
  brl:function(v,dec){if(!isNum(v))return '—';return v.toLocaleString('pt-BR',{style:'currency',currency:'BRL',minimumFractionDigits:dec==null?2:dec,maximumFractionDigits:dec==null?2:dec});},
  brl0:function(v){return fmt.brl(v,0);},
  pct:function(v,dec){if(!isNum(v))return '—';return v.toLocaleString('pt-BR',{minimumFractionDigits:dec==null?1:dec,maximumFractionDigits:dec==null?1:dec})+'%';},
  num:function(v,dec){if(!isNum(v))return '—';return v.toLocaleString('pt-BR',{minimumFractionDigits:dec||0,maximumFractionDigits:dec==null?0:dec});},
  meses:function(v){if(!isNum(v))return '—';if(v>600)return 'mais de 50 anos';var a=Math.floor(v/12),m=Math.round(v%12);if(m===12){a++;m=0;}return (a?a+(a>1?' anos':' ano'):'')+(a&&m?' e ':'')+(m?m+(m>1?' meses':' mês'):'')||'0 mês';}
};
function sum(arr){var t=0;(arr||[]).forEach(function(x){if(isNum(x))t+=x;});return t;}
function listSum(rows){return sum((rows||[]).map(function(r){return r&&isNum(r.value)?r.value:0;}));}
ZA.esc=esc; ZA.fmt=fmt; ZA.sum=sum; ZA.listSum=listSum; ZA.isNum=isNum;
ZA.clamp=function(v,a,b){return Math.max(a,Math.min(b,v));};
ZA.safeDiv=function(a,b){return (isNum(a)&&isNum(b)&&b!==0)?a/b:null;};

/* ---------- registro e montagem das telas ---------- */
ZA.register = function(cfg){ ZA.cfg = cfg; ZA.screens = build(cfg); if(ZA._onRegister) ZA._onRegister(cfg); };
function build(cfg){
  var s=[];
  (cfg.intro||[]).forEach(function(sc,i){s.push(Object.assign({pillar:0,idx:'I'+(i+1)},sc));});
  (cfg.pillars||[]).forEach(function(p,pi){
    (p.screens||[]).forEach(function(sc,si){
      s.push(Object.assign({pillar:pi+1,pillarTitle:p.title,moment:sc.kind,idx:'P'+(pi+1)+'.'+(si+1)},sc));
    });
  });
  s.push({kind:'consolidation',pillar:8,title:cfg.consolidationTitle||'Consolidação dos seus resultados',idx:'C'});
  s.push({kind:'report',pillar:9,title:cfg.reportTitle||cfg.deliverable,idx:'R'});
  return s;
}
ZA.validateConfig = function(cfg){
  var errs=[]; var sc=build(cfg);
  if((cfg.intro||[]).length!==3) errs.push('intro deve ter 3 telas');
  if((cfg.pillars||[]).length!==7) errs.push('deve haver 7 pilares');
  (cfg.pillars||[]).forEach(function(p,i){
    var kinds=(p.screens||[]).map(function(x){return x.kind;});
    if(kinds.join()!==ORDER.join()) errs.push('pilar '+(i+1)+' deve seguir learn,compare,form,feedback,apply (tem '+kinds.join()+')');
    var f=(p.screens||[])[2]; if(f&&!(f.fields&&f.fields.length)) errs.push('pilar '+(i+1)+' sem campos no exercício');
  });
  if(sc.length!==40) errs.push('total de telas = '+sc.length+' (esperado 40)');
  ['compute','priorities','report'].forEach(function(k){ if(typeof cfg[k]!=='function') errs.push('falta função '+k); });
  var ids={}; allFields(cfg).forEach(function(f){ if(ids[f.id]) errs.push('campo duplicado '+f.id); ids[f.id]=1; });
  return errs;
};
function allFields(cfg){var out=[];build(cfg).forEach(function(s){(s.fields||[]).forEach(function(f){out.push(f);});});return out;}
ZA.allFields=function(){return allFields(ZA.cfg);};

/* ---------- estado ---------- */
var st, KEY;
function blank(){return {v:{},u:{},checks:{},notes:{},pos:0,max:0,updated:null,started:new Date().toISOString()};}
function load(){try{var raw=localStorage.getItem(KEY);if(raw){var o=JSON.parse(raw);return Object.assign(blank(),o);}}catch(e){}return blank();}
var saveT;
function save(){st.updated=new Date().toISOString();try{localStorage.setItem(KEY,JSON.stringify(st));}catch(e){}
  var el=document.getElementById('za-saved'); if(el){el.textContent='Salvo automaticamente · '+new Date().toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'});}}
function saveSoon(){clearTimeout(saveT);saveT=setTimeout(save,250);}
ZA.state=function(){return st;};

/* valores acessíveis às fórmulas: s.v[id], com s.has(id) e s.n(id, padrao) */
function ctx(){
  var c={v:st.v,u:st.u,checks:st.checks,notes:st.notes};
  c.has=function(id){var x=st.v[id];if(st.u[id])return false;if(Array.isArray(x))return x.length>0;return x!==undefined&&x!==null&&x!=='';};
  c.n=function(id,def){var x=st.v[id];return (!st.u[id]&&isNum(x))?x:(def===undefined?null:def);};
  c.t=function(id,def){var x=st.v[id];return (!st.u[id]&&x!=null&&x!=='')?x:(def||'');};
  c.unknown=function(id){return !!st.u[id];};
  c.checked=function(id){return !!st.checks[id];};
  return c;
}
function calc(){var c=ctx();var r={};try{r=ZA.cfg.compute(c)||{};}catch(e){console.error('compute',e);r={_error:String(e)};}return {s:c,c:r};}
ZA.calc=calc;

/* ---------- campos ---------- */
function fieldHTML(f){
  var v=st.v[f.id], unk=!!st.u[f.id], id='f_'+f.id, h='';
  h+='<div class="za-field" data-f="'+esc(f.id)+'"><label class="za-l" for="'+id+'">'+esc(f.label)+(f.required?' *':'')+'</label>';
  var dis=unk?' disabled':'';
  switch(f.type){
    case 'number': case 'money': case 'percent':
      var unit=f.unit||(f.type==='money'?'R$':f.type==='percent'?'%':'');
      h+='<div class="za-inwrap">'+(f.type==='money'?'<span class="za-unit">R$</span>':'')+
         '<input class="za-in" id="'+id+'" type="number" inputmode="decimal" step="'+(f.step||'any')+'"'+
         (f.min!=null?' min="'+f.min+'"':'')+(f.max!=null?' max="'+f.max+'"':'')+
         ' value="'+(isNum(v)?v:'')+'" placeholder="'+esc(f.placeholder||'')+'"'+dis+'>'+
         (f.type!=='money'&&unit?'<span class="za-unit">'+esc(unit)+'</span>':'')+'</div>';
      break;
    case 'text': h+='<input class="za-in" id="'+id+'" type="text" maxlength="'+(f.max||160)+'" value="'+esc(v||'')+'" placeholder="'+esc(f.placeholder||'')+'"'+dis+'>'; break;
    case 'textarea': h+='<textarea class="za-in" id="'+id+'" rows="'+(f.rows||4)+'" maxlength="'+(f.max||2000)+'" placeholder="'+esc(f.placeholder||'')+'"'+dis+'>'+esc(v||'')+'</textarea>'; break;
    case 'select':
      h+='<select class="za-in" id="'+id+'"'+dis+'><option value="">Selecione…</option>'+(f.options||[]).map(function(o){return '<option value="'+esc(o.v)+'"'+(v===o.v?' selected':'')+'>'+esc(o.l)+'</option>';}).join('')+'</select>'; break;
    case 'radio':
      h+='<div class="za-opts">'+(f.options||[]).map(function(o,i){return '<label class="za-opt"><input type="radio" name="'+id+'" value="'+esc(o.v)+'"'+(v===o.v?' checked':'')+dis+'><span>'+esc(o.l)+(o.d?'<br><span class="za-small">'+esc(o.d)+'</span>':'')+'</span></label>';}).join('')+'</div>'; break;
    case 'checks':
      var arr=Array.isArray(v)?v:[];
      h+='<div class="za-opts">'+(f.options||[]).map(function(o){return '<label class="za-opt"><input type="checkbox" value="'+esc(o.v)+'"'+(arr.indexOf(o.v)>=0?' checked':'')+'><span>'+esc(o.l)+'</span></label>';}).join('')+'</div>'; break;
    case 'scale':
      var lo=f.min||1, hi=f.max||5; h+='<div class="za-scale">';
      for(var k=lo;k<=hi;k++) h+='<label><input type="radio" name="'+id+'" value="'+k+'"'+(v===k?' checked':'')+dis+'><span>'+k+'</span></label>';
      h+='</div>'+(f.ends?'<div class="za-help">'+esc(f.ends[0])+' ← → '+esc(f.ends[1])+'</div>':''); break;
    case 'list':
      var rows=Array.isArray(v)?v:(f.preset?f.preset.map(function(n){return {name:n,value:null};}):[]);
      if(!Array.isArray(v)){st.v[f.id]=rows;}
      h+='<div class="za-list" id="'+id+'">'+rows.map(function(r,i){return listRow(f,r,i);}).join('')+'</div>'+
         '<button type="button" class="za-list-add" data-add="'+esc(f.id)+'">+ adicionar item</button>';
      break;
  }
  if(f.help) h+='<div class="za-help">'+f.help+'</div>';
  if(f.allowUnknown) h+='<label class="za-unk"><input type="checkbox" data-unk="'+esc(f.id)+'"'+(unk?' checked':'')+'> Não sei / não tenho esse dado agora</label>';
  h+='<div class="za-err"></div></div>';
  return h;
}
function listRow(f,r,i){
  return '<div class="za-list-row" data-i="'+i+'"><input class="za-in" type="text" maxlength="80" data-lk="name" value="'+esc(r.name||'')+'" placeholder="'+esc(f.namePlaceholder||'Item')+'">'+
    '<input class="za-in" type="number" inputmode="decimal" step="any" min="0" data-lk="value" value="'+(isNum(r.value)?r.value:'')+'" placeholder="'+esc(f.valuePlaceholder||'R$')+'">'+
    '<button type="button" class="za-list-del" title="Remover" data-del="'+i+'">×</button></div>';
}
function readNumber(raw){ if(raw===''||raw==null) return null; var n=Number(String(raw).replace(',','.')); return isFinite(n)?n:NaN; }
function validateField(f){
  if(st.u[f.id]) return '';
  var v=st.v[f.id];
  var empty=(v===undefined||v===null||v===''||(Array.isArray(v)&&v.length===0));
  if(f.type==='list'){ var rows=v||[]; var bad=rows.some(function(r){return r.value!=null&&(!isNum(r.value)||r.value<0);});
    if(bad) return 'Use apenas valores positivos.'; if(f.required&&listSum(rows)<=0) return 'Informe ao menos um valor.'; return ''; }
  if(empty) return f.required?(f.allowUnknown?'Preencha ou marque “Não sei”.':'Campo obrigatório.'):'';
  if(f.type==='number'||f.type==='money'||f.type==='percent'){
    if(!isNum(v)) return 'Digite um número válido.';
    var min=f.min!=null?f.min:0, max=f.max!=null?f.max:(f.type==='percent'?100:null);
    if(v<min) return min===0?'O valor não pode ser negativo.':'Valor mínimo: '+min+'.';
    if(max!=null&&v>max) return f.type==='percent'?'O percentual deve ficar entre 0 e 100.':'Valor máximo: '+max+'.';
  }
  if(f.validate){ var m=f.validate(v,ctx()); if(m) return m; }
  return '';
}
function showErrors(sc){
  var ok=true;
  (sc.fields||[]).forEach(function(f){
    var el=document.querySelector('[data-f="'+f.id+'"]'); if(!el) return;
    var m=validateField(f); el.classList.toggle('invalid',!!m); el.querySelector('.za-err').textContent=m; if(m) ok=false;
  });
  return ok;
}
function screenValid(sc){ return (sc.fields||[]).every(function(f){return !validateField(f);}); }

function bindFields(sc){
  (sc.fields||[]).forEach(function(f){
    var wrap=document.querySelector('[data-f="'+f.id+'"]'); if(!wrap) return;
    var upd=function(){ saveSoon(); var m=validateField(f); if(!m){wrap.classList.remove('invalid');} };
    if(f.type==='list'){
      wrap.addEventListener('input',function(e){var row=e.target.closest('.za-list-row');if(!row)return;var i=+row.dataset.i,k=e.target.dataset.lk;
        st.v[f.id][i][k]=k==='value'?readNumber(e.target.value):e.target.value; upd();});
      wrap.addEventListener('click',function(e){
        if(e.target.dataset.del!=null){st.v[f.id].splice(+e.target.dataset.del,1);rerenderList(f);upd();}
        if(e.target.dataset.add!=null){st.v[f.id].push({name:'',value:null});rerenderList(f);upd();}
      });
    } else if(f.type==='checks'){
      wrap.addEventListener('change',function(){st.v[f.id]=[].slice.call(wrap.querySelectorAll('input[type=checkbox]:not([data-unk]):checked')).map(function(x){return x.value;});upd();});
    } else if(f.type==='radio'||f.type==='scale'){
      wrap.addEventListener('change',function(e){if(e.target.dataset.unk!=null)return;st.v[f.id]=f.type==='scale'?Number(e.target.value):e.target.value;upd();});
    } else {
      var inp=wrap.querySelector('#f_'+f.id);
      inp.addEventListener('input',function(){st.v[f.id]=(f.type==='number'||f.type==='money'||f.type==='percent')?readNumber(inp.value):inp.value;upd();});
      inp.addEventListener('blur',function(){var m=validateField(f);wrap.classList.toggle('invalid',!!m);wrap.querySelector('.za-err').textContent=m;});
    }
    var u=wrap.querySelector('[data-unk]');
    if(u) u.addEventListener('change',function(){ if(u.checked){st.u[f.id]=true;} else {delete st.u[f.id];} saveSoon(); render(); });
  });
}
function rerenderList(f){var el=document.getElementById('f_'+f.id);el.innerHTML=st.v[f.id].map(function(r,i){return listRow(f,r,i);}).join('');}

/* ---------- OP3D ---------- */
ZA.op3d = function(items){
  var list=(items||[]).filter(function(x){return x&&x.score>0;}).sort(function(a,b){return b.score-a.score;});
  var N=list.length; if(!N) return {all:[],l1:[],l2:[],l3:[]};
  var n1=Math.min(N,Math.max(3,Math.ceil(N*0.2)));
  var n2=Math.min(n1,Math.max(1,Math.ceil(n1*0.2)));
  if(n1>=3&&n2<2) n2=2; if(n2>n1) n2=n1;
  return {all:list,l1:list.slice(0,n1),l2:list.slice(0,n2),l3:list.slice(0,1)};
};
function op3dHTML(o){
  if(!o.all.length) return '<p class="za-small">Ainda não há dados suficientes para priorizar. Volte aos exercícios e complete as informações.</p>';
  function li(x){return '<li><b>'+esc(x.title)+'</b>'+(x.why?'<br><span style="opacity:.85">'+esc(x.why)+'</span>':'')+'</li>';}
  return '<div class="za-op3d">'+
   '<div class="za-lvl l1"><h4>Nível 1 · os 20% que mais pesam</h4><ol>'+o.l1.map(li).join('')+'</ol></div>'+
   '<div class="za-lvl l2"><h4>Nível 2 · os 4% decisivos</h4><ol>'+o.l2.map(li).join('')+'</ol></div>'+
   '<div class="za-lvl l3"><h4>Nível 3 · os 0,8% · sua ação essencial agora</h4><ol>'+o.l3.map(li).join('')+'</ol></div></div>'+
   '<p class="za-small">OP3D é um método de priorização em três níveis (Pareto aplicado sobre Pareto). Os percentuais orientam o foco; não são garantia matemática de resultado.</p>';
}
ZA.op3dHTML=op3dHTML;

/* ---------- blocos de exibição ---------- */
function metricsHTML(ms){
  return '<div class="za-metrics">'+(ms||[]).map(function(m){return '<div class="za-metric"><div class="k">'+esc(m.label)+'</div><div class="v">'+esc(m.value)+'</div>'+(m.tag?'<span class="za-tag '+esc(m.tag)+'">'+esc(tagName(m.tag))+'</span>':'')+(m.note?'<div class="za-small">'+esc(m.note)+'</div>':'')+'</div>';}).join('')+'</div>';
}
function tagName(t){return {informado:'informado por você',calculado:'calculado',estimativa:'estimativa',hipotese:'hipótese',recomendacao:'recomendação',externo:'referência externa'}[t]||t;}
ZA.metricsHTML=metricsHTML;
function fbHTML(items){return '<ul class="za-fb">'+(items||[]).map(function(x){return '<li class="'+esc(x.lv||'info')+'">'+x.t+'</li>';}).join('')+'</ul>';}
ZA.fbHTML=fbHTML;
ZA.table=function(head,rows,numCols){numCols=numCols||[];return '<div class="za-tscroll"><table class="za-t"><thead><tr>'+head.map(function(h){return '<th>'+esc(h)+'</th>';}).join('')+'</tr></thead><tbody>'+
  rows.map(function(r){return '<tr>'+r.map(function(c,i){return '<td'+(numCols.indexOf(i)>=0?' class="n"':'')+'>'+c+'</td>';}).join('')+'</tr>';}).join('')+'</tbody></table></div>';};

function missingList(){
  var out=[]; allFields(ZA.cfg).forEach(function(f){ if(st.u[f.id]) out.push(f.label); });
  return out;
}
function selectedActions(){
  var out=[]; ZA.screens.forEach(function(sc){ if(sc.kind==='apply'){ (sc.actions||[]).forEach(function(a){ if(st.checks[a.id]) out.push({pillar:sc.pillar,pillarTitle:sc.pillarTitle,text:a.text,id:a.id}); }); if(st.notes['n_'+sc.idx]) out.push({pillar:sc.pillar,pillarTitle:sc.pillarTitle,text:st.notes['n_'+sc.idx],own:true}); } });
  return out;
}
ZA.selectedActions=function(){return selectedActions();};
function allFeedback(r){
  var out=[]; ZA.screens.forEach(function(sc){ if(sc.kind==='feedback'&&sc.feedback){ try{ (sc.feedback(r.s,r.c)||[]).forEach(function(x){ out.push(Object.assign({pillar:sc.pillar,pillarTitle:sc.pillarTitle},x)); }); }catch(e){console.error(e);} } });
  return out;
}

/* ---------- renderização ---------- */
var root;
function render(){
  var sc=ZA.screens[st.pos], r=calc(), cfg=ZA.cfg, h='';
  var n=ZA.screens.length;
  document.querySelector('.za-prog-bar i').style.width=Math.round((st.pos+1)/n*100)+'%';
  document.querySelector('.za-prog-txt').textContent='Tela '+(st.pos+1)+' de '+n+(sc.pillar>=1&&sc.pillar<=7?' · Pilar '+sc.pillar+' de 7':'');
  h+='<div class="za-print-head"><b>ZION COLLECTION CLUB · HOTEL BUSINESS ACADEMY</b><br>'+esc(cfg.code)+' · '+esc(cfg.title)+'</div>';
  if(sc.pillar>=1&&sc.pillar<=7) h+='<div class="za-pillar-tag">Pilar '+sc.pillar+' · '+esc(sc.pillarTitle)+'<span class="za-moment">'+MOMENTS[sc.kind]+'</span></div>';
  switch(sc.kind){
    case 'mirror': case 'collapse':
      h+='<div class="za-hero"><div class="za-pillar-tag" style="color:var(--champ)">'+(sc.kind==='mirror'?'Espelhamento':'Colapso de crença')+'</div><h1 class="za-h">'+sc.title+'</h1><p class="za-lead">'+(sc.lead||'')+'</p></div>'+(sc.body||''); break;
    case 'start':
      h+='<div class="za-hero"><div class="za-pillar-tag" style="color:var(--champ)">'+esc(cfg.tool)+'</div><h1 class="za-h">'+sc.title+'</h1><p class="za-lead">'+(sc.lead||'')+'</p></div>'+(sc.body||'')+
         '<div class="za-card">'+(sc.fields||[]).map(fieldHTML).join('')+'</div>'; break;
    case 'learn':
      h+='<h1 class="za-h">'+sc.title+'</h1>'+(sc.body||'')+(sc.example?'<div class="za-example"><b>Exemplo</b>'+sc.example+'</div>':''); break;
    case 'compare':
      h+='<h1 class="za-h">'+sc.title+'</h1>'+(sc.intro?'<p>'+sc.intro+'</p>':'')+'<div class="za-compare">'+(sc.cols||[]).map(function(c){return '<div class="za-col '+(c.type||'')+'"><h4>'+esc(c.h)+'</h4><ul>'+c.items.map(function(i){return '<li>'+i+'</li>';}).join('')+'</ul></div>';}).join('')+'</div>'+(sc.after||''); break;
    case 'form':
      h+='<h1 class="za-h">'+sc.title+'</h1><div class="za-pillar-tag">Exercício '+sc.pillar+' de 7</div>'+(sc.intro?'<p>'+sc.intro+'</p>':'')+'<div class="za-card">'+(sc.fields||[]).map(fieldHTML).join('')+'</div>'; break;
    case 'feedback':
      h+='<h1 class="za-h">'+sc.title+'</h1>'+(sc.intro?'<p>'+sc.intro+'</p>':'');
      try{ if(sc.metrics) h+=metricsHTML(sc.metrics(r.s,r.c)); h+=fbHTML(sc.feedback?sc.feedback(r.s,r.c):[]); if(sc.extra) h+=sc.extra(r.s,r.c); }catch(e){ h+='<p class="za-missing">Não foi possível calcular com os dados atuais. Revise o exercício anterior.</p>'; console.error(e); }
      break;
    case 'apply':
      h+='<h1 class="za-h">'+sc.title+'</h1>'+(sc.intro?'<p>'+sc.intro+'</p>':'')+'<div class="za-card za-actions"><div class="za-small" style="margin-bottom:8px">Marque o que você vai aplicar. As ações marcadas entram no seu plano final.</div><div class="za-opts">'+
        (sc.actions||[]).map(function(a){return '<label class="za-opt"><input type="checkbox" data-act="'+esc(a.id)+'"'+(st.checks[a.id]?' checked':'')+'><span>'+a.text+'</span></label>';}).join('')+
        '</div><div class="za-field"><label class="za-l" for="note">Minha ação própria (opcional)</label><textarea class="za-in" id="note" rows="2" maxlength="300" data-note="n_'+sc.idx+'">'+esc(st.notes['n_'+sc.idx]||'')+'</textarea></div></div>'; break;
    case 'consolidation':
      h+='<h1 class="za-h">'+esc(sc.title)+'</h1><p>Este é o retrato do que você informou e do que foi calculado. Confira antes de gerar o relatório: se algo estiver errado, volte ao exercício pelo menu “Telas”.</p>';
      try{ h+=metricsHTML(cfg.metrics?cfg.metrics(r.s,r.c):[]); }catch(e){console.error(e);}
      var fb=allFeedback(r).filter(function(x){return x.lv==='bad'||x.lv==='warn';});
      h+='<h2>Pontos de atenção encontrados</h2>'+(fb.length?fbHTML(fb):'<p class="za-small">Nenhum ponto crítico identificado com os dados informados.</p>');
      h+='<h2>Prioridades OP3D</h2>'+op3dHTML(ZA.op3d(cfg.priorities(r.s,r.c)));
      var miss=missingList(); if(miss.length) h+='<h2>Dados que faltam</h2><div class="za-missing">Você marcou “não sei” em: '+miss.map(esc).join('; ')+'. Os resultados que dependem desses dados são parciais e devem ser tratados como hipóteses.</div>';
      break;
    case 'report':
      h+=reportHTML(r); break;
  }
  if(sc.kind!=='report') h+='';
  root.innerHTML=h;
  bindFields(sc);
  root.querySelectorAll('[data-act]').forEach(function(cb){cb.addEventListener('change',function(){if(cb.checked)st.checks[cb.dataset.act]=true;else delete st.checks[cb.dataset.act];saveSoon();});});
  root.querySelectorAll('[data-note]').forEach(function(t){t.addEventListener('input',function(){st.notes[t.dataset.note]=t.value;saveSoon();});});
  root.querySelectorAll('[data-go]').forEach(function(b){b.addEventListener('click',function(){go(+b.dataset.go);});});
  var pr=document.getElementById('za-print'); if(pr) pr.addEventListener('click',function(){ window.print(); });
  var ex=document.getElementById('za-export'); if(ex) ex.addEventListener('click',exportJSON);
  document.getElementById('za-prev').disabled=st.pos===0;
  var nx=document.getElementById('za-next');
  nx.textContent=st.pos===n-2?'Gerar relatório':(st.pos===n-1?'Concluído':'Continuar');
  nx.disabled=st.pos===n-1;
  renderIndex();
  window.scrollTo(0,0);
  document.title=cfg.code+' · '+(sc.idx)+' · Zion Collection Club';
}
function reportHTML(r){
  var cfg=ZA.cfg, s=r.s, c=r.c, rep={};
  try{ rep=cfg.report(s,c)||{}; }catch(e){ console.error(e); rep={sections:[{title:'Erro',html:'<p>Não foi possível montar o relatório com os dados atuais.</p>'}]}; }
  var who=esc(s.t(cfg.nameField||'nome','')), what=esc(s.t(cfg.propertyField||'propriedade',''));
  var h='<div class="za-hero"><div class="za-pillar-tag" style="color:var(--champ)">'+esc(cfg.code)+' · Relatório personalizado</div><h1 class="za-h">'+esc(cfg.deliverable)+'</h1><p class="za-lead">'+(what?what+' · ':'')+(who?'Preparado para '+who+' · ':'')+new Date().toLocaleDateString('pt-BR')+'</p></div>';
  h+='<div class="za-tools za-noprint"><button class="za-btn gold" id="za-print">Baixar PDF</button><button class="za-btn ghost" id="za-export">Exportar dados (JSON)</button></div>';
  h+='<p class="za-small za-noprint">Em “Baixar PDF”, escolha <b>Salvar como PDF</b> na janela de impressão.</p>';
  h+='<h2>Indicadores</h2>'+metricsHTML(cfg.metrics?cfg.metrics(s,c):[]);
  (rep.sections||[]).forEach(function(x){ h+='<h2>'+esc(x.title)+'</h2>'+x.html; });
  h+='<h2>Prioridades OP3D</h2>'+op3dHTML(ZA.op3d(cfg.priorities(s,c)));
  var acts=selectedActions();
  h+='<h2>Seu plano de ação</h2>';
  if(rep.plan) h+=rep.plan;
  h+=acts.length?ZA.table(['Pilar','Ação escolhida por você'],acts.map(function(a){return [esc(a.pillar+'. '+a.pillarTitle),esc(a.text.replace(/<[^>]+>/g,''))+(a.own?' <span class="za-tag informado">sua ação</span>':'')];})):'<p class="za-small">Você ainda não marcou ações nas telas “Aplique”. Volte a elas para montar seu plano.</p>';
  var fb=allFeedback(r).filter(function(x){return x.lv==='bad'||x.lv==='warn';});
  if(fb.length) h+='<h2>Pontos de atenção</h2>'+fbHTML(fb);
  var miss=missingList(); if(miss.length) h+='<h2>Dados ausentes</h2><div class="za-missing">Itens marcados como “não sei”: '+miss.map(esc).join('; ')+'. Conclusões que dependem deles são hipóteses, não diagnóstico.</div>';
  h+='<div class="za-disclaimer"><b>Como ler este relatório.</b> “Informado” = dado que você digitou. “Calculado” = resultado de fórmula sobre seus dados. “Estimativa” e “hipótese” = premissas que precisam ser confirmadas. “Recomendação” = orientação da metodologia Zion. '+(cfg.disclaimer||'Este material é educacional e orientativo. Não constitui garantia de resultado, reservas, faturamento, lucro ou retorno.')+'<br>Zion Collection Club · Hotel Business Academy · Metodologias ECROI e OP3D.</div>';
  return h;
}
function renderIndex(){
  var el=document.getElementById('za-idx'), h='', last=-1;
  var names={0:'Abertura',8:'Consolidação',9:'Relatório'};
  ZA.screens.forEach(function(sc,i){
    if(sc.pillar!==last){ h+='<div class="za-idx-p">'+(sc.pillar>=1&&sc.pillar<=7?'Pilar '+sc.pillar+' · '+esc(sc.pillarTitle):names[sc.pillar])+'</div>'; last=sc.pillar; }
    var lbl=(sc.kind in MOMENTS?MOMENTS[sc.kind]+' · ':'')+String(sc.title).replace(/<[^>]+>/g,'');
    h+='<a href="#" data-goidx="'+i+'" class="'+(i===st.pos?'cur':'')+(i>st.max?' locked':'')+'">'+(i<st.max?'<span class="d">✓</span>':'')+esc(lbl.slice(0,70))+'</a>';
  });
  el.innerHTML=h;
  el.querySelectorAll('[data-goidx]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();go(+a.dataset.goidx);toggleDrawer(false);});});
}
function go(i){ if(i<0||i>=ZA.screens.length) return; st.pos=i; if(i>st.max) st.max=i; save(); render(); }
function next(){
  var sc=ZA.screens[st.pos];
  if(!showErrors(sc)) { var first=document.querySelector('.za-field.invalid'); if(first) first.scrollIntoView({behavior:'smooth',block:'center'}); return; }
  go(st.pos+1);
}
ZA.go=go; ZA.next=next; ZA.screenValid=function(i){return screenValid(ZA.screens[i]);};
function toggleDrawer(on){document.getElementById('za-drawer').classList.toggle('open',on);}
function exportJSON(){
  var blob=new Blob([JSON.stringify({produto:ZA.cfg.code,versao:1,exportado:new Date().toISOString(),dados:st},null,2)],{type:'application/json'});
  var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=ZA.cfg.code+'-meus-dados.json';document.body.appendChild(a);a.click();a.remove();
}
function importJSON(file){
  var fr=new FileReader(); fr.onload=function(){ try{ var o=JSON.parse(fr.result); if(o.produto!==ZA.cfg.code) throw new Error('arquivo de outro produto'); st=Object.assign(blank(),o.dados); save(); render(); alert('Dados importados.'); }catch(e){ alert('Não foi possível importar: '+e.message); } }; fr.readAsText(file);
}

/* ---------- inicialização ---------- */
ZA.boot = function(mount){
  var cfg=ZA.cfg; KEY='za:v1:'+cfg.code; st=load();
  if(st.pos>=ZA.screens.length) st.pos=0;
  mount.innerHTML=
   '<header class="za-top"><div class="za-brand">ZION <b>COLLECTION CLUB</b></div><div class="za-prog"><div class="za-prog-bar"><i></i></div><div class="za-prog-txt"></div></div><button class="za-menu-btn" id="za-menu">Telas</button></header>'+
   '<main class="za-wrap" id="za-root"></main>'+
   '<nav class="za-nav"><div class="za-nav-in"><button class="za-btn ghost" id="za-prev">Voltar</button><span class="za-saved" id="za-saved"></span><button class="za-btn" id="za-next">Continuar</button></div></nav>'+
   '<div class="za-drawer" id="za-drawer"><div class="za-drawer-in"><div style="display:flex;justify-content:space-between;align-items:center"><b>'+esc(cfg.code)+'</b><button class="za-menu-btn" style="color:var(--texto);border-color:#ccc" id="za-close">Fechar</button></div>'+
   '<div class="za-small" style="margin:6px 0 10px">'+esc(cfg.title)+'</div><div class="za-idx" id="za-idx"></div>'+
   '<div class="za-tools"><button class="za-btn ghost" id="za-exp2">Exportar dados</button><label class="za-btn ghost" style="display:inline-block">Importar dados<input type="file" accept="application/json" id="za-imp" style="display:none"></label><button class="za-btn ghost" id="za-reset">Recomeçar do zero</button></div>'+
   '<p class="za-small">Seus dados ficam salvos neste navegador. Para continuar em outro aparelho, exporte e importe o arquivo.</p></div></div>';
  root=document.getElementById('za-root');
  document.getElementById('za-prev').addEventListener('click',function(){go(st.pos-1);});
  document.getElementById('za-next').addEventListener('click',next);
  document.getElementById('za-menu').addEventListener('click',function(){toggleDrawer(true);});
  document.getElementById('za-close').addEventListener('click',function(){toggleDrawer(false);});
  document.getElementById('za-drawer').addEventListener('click',function(e){if(e.target.id==='za-drawer')toggleDrawer(false);});
  document.getElementById('za-exp2').addEventListener('click',exportJSON);
  document.getElementById('za-imp').addEventListener('change',function(e){if(e.target.files[0])importJSON(e.target.files[0]);});
  document.getElementById('za-reset').addEventListener('click',function(){ if(confirm('Apagar todas as respostas deste produto neste navegador?')){ st=blank(); save(); toggleDrawer(false); render(); } });
  if(st.updated){ var el=document.getElementById('za-saved'); el.textContent='Progresso recuperado · continue de onde parou'; }
  render();
};
})();
