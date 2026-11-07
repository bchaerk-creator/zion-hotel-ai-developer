// Uso: node record.js <scenes.json> <outdir>  — grava uma cena por vez e escreve timings.json
const {chromium}=require("playwright"); const fs=require("fs"); const path=require("path");
const [,, specPath, outDir]=process.argv; const spec=JSON.parse(fs.readFileSync(specPath,"utf8"));
const CURSOR=`(()=>{if(window.__cur)return;const c=document.createElement("div");c.id="__cursor";c.style.cssText="position:fixed;z-index:2147483647;width:22px;height:22px;pointer-events:none;left:-50px;top:-50px;transform:translate(-2px,-2px)";c.innerHTML='<svg width="22" height="22" viewBox="0 0 24 24"><path d="M4 2l16 9-7 1.5L9 20z" fill="#16261C" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';document.body.appendChild(c);window.__cur=c;const h=document.createElement("style");h.textContent=".__hl{outline:4px solid #E0BE5E !important;outline-offset:3px;border-radius:6px;transition:outline-color .3s}";document.head.appendChild(h);})()`;
async function cursor(page){ await page.evaluate(CURSOR).catch(()=>{}); }
async function moveTo(page,x,y,steps=18){ const cur=page.__pos||{x:640,y:360}; for(let i=1;i<=steps;i++){const nx=cur.x+(x-cur.x)*i/steps, ny=cur.y+(y-cur.y)*i/steps; await page.mouse.move(nx,ny); await page.evaluate(([a,b])=>{if(window.__cur){window.__cur.style.left=a+"px";window.__cur.style.top=b+"px"}},[nx,ny]).catch(()=>{}); await page.waitForTimeout(14);} page.__pos={x,y}; }
async function center(page,sel){ const el=await page.$(sel); if(!el) return null; await el.scrollIntoViewIfNeeded(); await page.waitForTimeout(250); const b=await el.boundingBox(); if(!b) return null; return {x:b.x+Math.min(b.width/2,220), y:b.y+b.height/2}; }
async function hl(page,sel,on=true){ await page.evaluate(([s,o])=>{const e=document.querySelector(s); if(e) e.classList.toggle("__hl",o)},[sel,on]).catch(()=>{}); }
(async()=>{
  fs.mkdirSync(outDir,{recursive:true});
  const b=await chromium.launch(); const timings=[];
  const ctx=await b.newContext({viewport:{width:1280,height:720},recordVideo:{dir:outDir,size:{width:1280,height:720}},deviceScaleFactor:1});
  const page=await ctx.newPage(); page.__pos={x:640,y:360}; const T0=Date.now();
  for(let i=0;i<spec.scenes.length;i++){
    const sc=spec.scenes[i];
    if(sc.restore){ await page.goto(sc.restore.url); await page.evaluate(([k,v])=>localStorage.setItem(k,v),[sc.restore.key,sc.restore.value]); }
    const t0=Date.now();
    for(const a of sc.actions){
      try{
        if(a.goto){ await page.goto(a.goto,{waitUntil:"networkidle"}); await cursor(page); await page.waitForTimeout(a.wait||600); }
        else if(a.card){ const u=`file://${__dirname}/card.html?`+new URLSearchParams(a.card).toString(); await page.goto(u); await page.waitForTimeout(a.wait||400); }
        else if(a.wait!==undefined && Object.keys(a).length===1){ await page.waitForTimeout(a.wait); }
        else if(a.scroll!==undefined){ const n=Math.max(1,Math.round(Math.abs(a.scroll)/40)); for(let k=0;k<n;k++){ await page.mouse.wheel(0,a.scroll/n); await page.waitForTimeout(16);} await page.waitForTimeout(a.wait||400); }
        else if(a.show){ const p=await center(page,a.show); if(p){ await moveTo(page,p.x,p.y); } if(a.hl!==false) await hl(page,a.show,true); await page.waitForTimeout(a.wait||900); if(a.keep!==true) await hl(page,a.show,false); }
        else if(a.click){ const p=await center(page,a.click); if(p){ await moveTo(page,p.x,p.y); await page.waitForTimeout(150); await page.click(a.click); } await page.waitForTimeout(a.wait||700); }
        else if(a.type){ const p=await center(page,a.type); if(p){ await moveTo(page,p.x,p.y);} await page.click(a.type); await page.fill(a.type,""); await page.type(a.type,a.text,{delay:a.delay||28}); await page.waitForTimeout(a.wait||500); }
        else if(a.select){ const p=await center(page,a.select); if(p){ await moveTo(page,p.x,p.y);} await page.selectOption(a.select,a.value); await page.waitForTimeout(a.wait||500); }
        else if(a.eval){ await page.evaluate(a.eval); await page.waitForTimeout(a.wait||300); }
        else if(a.move){ await moveTo(page,a.move[0],a.move[1]); }
        else if(a.auto!==undefined){ // responde automaticamente N telas de uma ferramenta Faça agora
          const ANS=a.answers||[]; let ai=0;
          for(let k=0;k<a.auto;k++){
            const done=await page.$("#pdf"); if(done&&await done.isVisible()) break; // chegou à página de resultado
            const st=await page.evaluate(()=>{const v=e=>e.getBoundingClientRect().width>0;const ops=[...document.querySelectorAll("label.op")].filter(v);const ins=[...document.querySelectorAll("input:not([type=radio]):not([type=checkbox]),select,textarea")].filter(v).map(x=>({sel:x.tagName.toLowerCase()+"#"+x.id,type:x.type||"",ph:x.placeholder||""}));const radios=ops.length?0:[...document.querySelectorAll("input[type=radio],input[type=checkbox]")].filter(r=>r.parentElement&&r.parentElement.getBoundingClientRect().width>0).length;const q=document.querySelector(".pergunta,h1");return {ops:ops.length,ins,radios,q:q?q.textContent.trim():""}});
            if(st.ops>0){ // uma opção por grupo (name do radio), para telas com várias perguntas
              await page.evaluate((pk)=>{const g=new Map();for(const l of document.querySelectorAll("label.op")){if(l.getBoundingClientRect().width<=0)continue;const r=l.querySelector("input");const k=r?(r.name||r.id||"x"):"x";if(!g.has(k))g.set(k,[]);g.get(k).push(l)}document.querySelectorAll("label.op[data-autopick]").forEach(e=>e.removeAttribute("data-autopick"));for(const ls of g.values()){ls[Math.min(pk,ls.length-1)].setAttribute("data-autopick","1")}},a.pick||0);
              for(const l of await page.$$("label.op[data-autopick]")){ const bb=await l.boundingBox(); if(bb){await moveTo(page,bb.x+30,bb.y+bb.height/2,10);} await l.click().catch(()=>{}); await page.waitForTimeout(Math.min(a.pace||350,250)); }
              await page.waitForTimeout(a.pace||350); }
            else if(st.radios>0){ await page.evaluate(()=>{const groups=new Map();for(const r of document.querySelectorAll("input[type=radio],input[type=checkbox]")){if(!(r.parentElement&&r.parentElement.getBoundingClientRect().width>0))continue;const k=r.name?("n:"+r.name):(r.closest("fieldset")||r.parentElement.parentElement);if(!groups.has(k))groups.set(k,r)}for(const r of groups.values()){r.click()}}); await page.waitForTimeout(a.pace||350); }
            for(const inp of st.ins){ try{ if(inp.sel.startsWith("select")){await page.selectOption(inp.sel,{index:1})} else { let v=(a.values&&a.values[inp.sel])||null; if(!v&&ai<ANS.length&&!inp.sel.startsWith("input#c-")&&inp.type!=="date"){ v=String(ANS[ai++]); } if(!v){ const m=inp.ph.replace(/\./g,"").match(/\d+(?:,\d+)?/); v= inp.type==="number"?"10": inp.type==="email"?"ana@exemplo.com": inp.type==="date"?"2027-03-01": (m?m[0]:(/n[úu]mero|%|R\$|quant/i.test(inp.ph)?"4":"Exemplo de resposta: medido no calendário dos comparáveis")); } const el=await page.$(inp.sel); const bb=el?await el.boundingBox():null; if(bb){await moveTo(page,bb.x+40,bb.y+bb.height/2);} await page.fill(inp.sel,""); await page.type(inp.sel,v,{delay:a.delay||18}); } }catch(e){} }
            let moved=false; for(const sel of ["#avancar","#continuar","#vai","#proximo"]){ const el=await page.$(sel); if(el&&await el.isVisible()){ const bb=await el.boundingBox(); if(bb){await moveTo(page,bb.x+bb.width/2,bb.y+bb.height/2);} await el.click().catch(()=>{}); moved=true; break; } }
            await page.waitForTimeout(a.pace||350);
            const q2=await page.evaluate(()=>{const q=document.querySelector(".pergunta,h1");return q?q.textContent.trim():""});
            if(q2===st.q){ const ns=await page.$("#ns"); if(ns&&await ns.isVisible()){ await ns.click(); await page.waitForTimeout(250); for(const sel of ["#avancar","#continuar","#vai"]){const el=await page.$(sel); if(el&&await el.isVisible()){await el.click().catch(()=>{});break}} await page.waitForTimeout(a.pace||350);} }
            if(!moved) break;
          }
          await page.waitForTimeout(a.wait||600); }
        else if(a.fillStart){ for(const [id,v] of Object.entries(a.fillStart)){ const el=await page.$(id); if(el&&await el.isVisible()){ if(id==="#uf"){await page.selectOption(id,v)} else { const bb=await el.boundingBox(); if(bb){await moveTo(page,bb.x+40,bb.y+bb.height/2);} await page.fill(id,""); await page.type(id,v,{delay:28}); } } } await page.waitForTimeout(a.wait||400); }
        else if(a.text){ // localiza elemento por texto, rola até o centro e destaca (ou o ancestral `up`)
          const ok=await page.evaluate(([txt,sel,up])=>{const els=[...document.querySelectorAll(sel||"td,th,h1,h2,h3,p,li,b,label,span")];const e=els.find(x=>x.textContent.trim().toLowerCase().startsWith(txt.toLowerCase()));if(!e)return false;const t=up?(e.closest(up)||e):e;t.classList.add("__hl");window.__last=t;const r=t.getBoundingClientRect();window.scrollBy({top:r.top-260,behavior:"instant"});return true},[a.text,a.sel||null,a.up||null]);
          if(ok){ await page.waitForTimeout(250); const b=await page.evaluate(()=>{const r=window.__last.getBoundingClientRect();return {x:r.x+Math.min(r.width/2,200),y:r.y+r.height/2}}); await moveTo(page,b.x,b.y); }
          await page.waitForTimeout(a.wait||1200); if(a.keep!==true) await page.evaluate(()=>{if(window.__last)window.__last.classList.remove("__hl")}); }
      }catch(e){ console.error("ação falhou na cena",i,JSON.stringify(a).slice(0,120),e.message.split("\n")[0]); }
    }
    const spent=Date.now()-t0; const min=(sc.minMs||0); if(spent<min) await page.waitForTimeout(min-spent);
    const total=Date.now()-t0; timings.push({i,start_ms:t0-T0,ms:total}); console.log(`cena ${i}: ${(total/1000).toFixed(1)}s`);
  }
  const v=page.video(); await ctx.close(); const vp=await v.path(); await b.close();
  fs.writeFileSync(path.join(outDir,"timings.json"),JSON.stringify({video:vp,scenes:timings},null,1));
})();
