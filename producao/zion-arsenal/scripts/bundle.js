// Empacota uma mini mentoria em um único HTML (CSS + motor + produto embutidos) → out/bundle/<ID>.html
// Caminho de hospedagem não-adivinhável guardado em control/paths.json (gerado uma vez; idempotente).
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const T=process.env.ZA_TOOLS;const {minify}=require(T+'/node_modules/terser');const CleanCSS=require(T+'/node_modules/clean-css');
const P='control/paths.json';const paths=fs.existsSync(P)?JSON.parse(fs.readFileSync(P,'utf8')):{};
const css=fs.readFileSync('app/engine.css','utf8'),eng=fs.readFileSync('app/engine.js','utf8');
fs.mkdirSync('out/bundle',{recursive:true});
(async()=>{
const mcss=new CleanCSS({}).minify(css).styles;const meng=(await minify(eng,{compress:true,mangle:true})).code;
for(const id of process.argv.slice(2)){
  if(!paths[id]) paths[id]='/f/'+id.toLowerCase()+'-'+crypto.randomBytes(6).toString('hex');
  const prod=(await minify(fs.readFileSync(`app/products/${id}.js`,'utf8'),{compress:true,mangle:true})).code;
  const safe=s=>s.replace(/<\/script/gi,'<\\/script');
  const html=`<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>${id} · Zion Collection Club · Hotel Business Academy</title><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Jost:wght@400;500;600&display=swap" rel="stylesheet"><style>${mcss}</style></head><body><div id="za-app"><main class="za-wrap"><p>Carregando sua mini mentoria…</p></main></div><script>${safe(meng)}</script><script>ZA._onRegister=function(){ZA.boot(document.getElementById('za-app'));};</script><script>${safe(prod)}</script></body></html>`;
  fs.writeFileSync(`out/bundle/${id}.html`,html);console.log(id,paths[id],html.length,'bytes');
}
fs.writeFileSync(P,JSON.stringify(paths,null,1));
})();
