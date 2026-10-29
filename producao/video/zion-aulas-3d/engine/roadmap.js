// ---------- ROADMAP (mapa da trilha)
const RM_N=[['MARCO ZERO','Bloco 1'],['MARCO ZERO','Bloco 2'],['AULA 1','Território e destino'],['AULA 2','Mercado'],['AULA 3','Produto'],['AULA 4','Modelo de negócio'],['AULA 5','Masterplan'],['AULA 6','Estudo de massas']];
function roadmap(sc){const wrap=el('','','position:absolute;left:0;top:0;width:1920px;height:1080px',sc);
 const line=el('','<div class="f" style="position:absolute;left:0;top:0;height:100%;width:0;background:#E0BE5E"></div>','position:absolute;left:190px;top:400px;width:1540px;height:4px;background:rgba(217,207,188,.2)',wrap);
 const br=el('','<div style="font:600 18px IN;letter-spacing:4px;color:#E0BE5E;text-align:center">MARCO ZERO</div>','position:absolute;left:140px;top:300px;width:320px;border-top:2px solid rgba(224,190,94,.6);padding-top:10px;opacity:0',wrap);
 const br2=el('','<div style="font:600 18px IN;letter-spacing:4px;color:#D9CFBC;text-align:center">AS 6 AULAS DA TRILHA</div>','position:absolute;left:580px;top:300px;width:1200px;border-top:2px solid rgba(217,207,188,.35);padding-top:10px;opacity:0',wrap);
 const nodes=RM_N.map((n,i)=>el('',`<div class="o" style="width:60px;height:60px;border-radius:50%;margin:0 auto;border:3px solid rgba(224,190,94,.5);background:#16261C;display:flex;align-items:center;justify-content:center;font:800 26px IN;color:#E0BE5E;box-sizing:border-box">${i<2?i+1:i-1}</div><div style="font:600 17px IN;letter-spacing:3px;color:#E0BE5E;margin-top:16px">${n[0]}</div><div class="l" style="font:400 26px/1.2 PF;color:#F5F1E8;margin-top:6px">${n[1]}</div>`,`position:absolute;left:${190+i*220-100}px;top:372px;width:200px;text-align:center;opacity:0`,wrap));
 return {wrap,line,br,br2,nodes}}
function roadmapUp(R,t,t0,done,cur){fadeUp(R.br,t,t0+.2);fadeUp(R.br2,t,t0+.5);R.line.querySelector('.f').style.width=(100*eio(prog(t,t0,1.2))*(Math.max(cur,0)+.5)/8)+'%';
 R.nodes.forEach((e,i)=>{fadeUp(e,t,t0+.15+i*.1,.4,20);const o=e.querySelector('.o');const isD=done.includes(i),isC=i===cur;
  o.style.background=isD?'#E0BE5E':'#16261C';o.style.color=isD?'#16261C':'#E0BE5E';o.textContent=isD?'✓':(i<2?i+1:i-1);o.style.borderColor=isC?'#E0BE5E':'rgba(224,190,94,.5)';
  const k=isC?.5+.5*Math.sin(t*4):0;o.style.boxShadow=isC?`0 0 ${20+25*k}px rgba(224,190,94,.7)`:'none';e.style.transform+=isC?` scale(${1.08})`:'';e.querySelector('.l').style.color=isC?'#E0BE5E':(i>cur&&!isD?'rgba(245,241,232,.55)':'#F5F1E8')})}
function topicList(sc,items,top=600){return items.map(x=>el('chip lg',`<b></b>${x}`,'',sc))}
function topicUp(T,t,times,check,left=960,top=600,gap=92){T.forEach((c,i)=>{chipIn(c,t,times[i],left,top+i*gap);if(check&&check[i]){const b=c.querySelector('b');if(b)b.outerHTML='<span class="v">✓</span>'}})}
