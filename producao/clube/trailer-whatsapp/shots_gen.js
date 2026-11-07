const {chromium}=require("playwright");
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(let i=0;i<(+process.argv[3]||12);i++){await p.goto(`file://${__dirname}/${process.argv[2]}${process.argv[2].includes("?")?"&":"?"}s=${i}`);await p.evaluate(async()=>{await document.fonts.ready});await p.waitForTimeout(2600);await p.screenshot({path:`${__dirname}/shots/${process.argv[4]||"x"}${String(i).padStart(2,"0")}.png`});}
await b.close()})();
