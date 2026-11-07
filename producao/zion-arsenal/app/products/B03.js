/* ZAR-B03 · Como Criar um Projeto de Hospedagem Mesmo Sem Dinheiro? · Construtor de Projeto Turístico */
(function(){
var F=ZA.fmt, esc=ZA.esc;
function tag(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';}
function arr(s,id){var x=s.v[id];return (!s.unknown(id)&&Array.isArray(x))?x:[];}
function has(a,v){return a.indexOf(v)>=0;}
function rows(s,id){return arr(s,id).filter(function(r){return r&&ZA.isNum(r.value)&&r.value>0;});}

/* atributos do terreno → pontos por vocação */
var VOC=[{k:'natureza',n:'Natureza e aventura',desejo:'aventura e contato direto com a natureza'},{k:'bemestar',n:'Descanso e bem-estar',desejo:'descanso, silêncio e recuperação'},{k:'romantico',n:'Romântico (casais)',desejo:'momentos a dois em um cenário especial'},{k:'rural',n:'Rural e agroturismo',desejo:'a vida no campo, a produção e a comida de origem'},{k:'familia',n:'Família e lazer',desejo:'lazer ao ar livre com as crianças'}];
var ATR=[
 {v:'agua',l:'Rio, cachoeira, lago ou nascente',p:{natureza:2,bemestar:1,familia:1}},
 {v:'mata',l:'Mata nativa e trilhas',p:{natureza:2,bemestar:1}},
 {v:'vista',l:'Vista panorâmica (serra, vale, mar)',p:{romantico:2,bemestar:1}},
 {v:'silencio',l:'Isolamento e silêncio',p:{bemestar:2,romantico:1}},
 {v:'producao',l:'Produção rural (pomar, horta, animais, café, vinho, queijo)',p:{rural:2,familia:1}},
 {v:'plano',l:'Área plana ampla para lazer',p:{familia:2,rural:1}},
 {v:'relevo',l:'Relevo para aventura (morros, pedras, mirantes)',p:{natureza:2}},
 {v:'historia',l:'Casarão, história ou cultura local',p:{rural:1,romantico:1}},
 {v:'clima',l:'Clima de serra (frio, neblina, lareira)',p:{romantico:2,bemestar:1}}];
var VMAX={}; VOC.forEach(function(x){VMAX[x.k]=ATR.reduce(function(t,a){return t+(a.p[x.k]||0);},0);});
var PUB={casais:{l:'casais',voc:'romantico'},familias:{l:'famílias com crianças',voc:'familia'},aventureiros:{l:'quem pratica esportes e aventura',voc:'natureza'},descanso:{l:'quem busca descanso e bem-estar',voc:'bemestar'},rural:{l:'quem quer viver a experiência do campo',voc:'rural'}};
var MODS={cabanas:{l:'cabanas',cx:2,fit:{plano:2,ondulado:2,acidentado:2,misto:2}},glamping:{l:'unidades de glamping',cx:1,fit:{plano:2,ondulado:2,acidentado:1,misto:2}},chales:{l:'chalés',cx:2,fit:{plano:2,ondulado:2,acidentado:1,misto:2}},casa:{l:'casa de campo inteira',cx:1,fit:{plano:2,ondulado:1,acidentado:0,misto:1}},pousada:{l:'pequena pousada',cx:3,fit:{plano:2,ondulado:1,acidentado:0,misto:1}}};
var PREP=[{v:'fotos',l:'Fotos e vídeos atuais do terreno'},{v:'croqui',l:'Desenho ou croqui de onde ficariam as unidades'},{v:'fornecedores',l:'Lista de fornecedores ou construtores para pedir orçamento'},{v:'profissional',l:'Conversa inicial com arquiteto ou engenheiro'}];
var DIMN=['Terreno','Vocação','Público','Conceito','Modelo','Investimento','Preparação'];

ZA.register({
id:'B03', code:'ZAR-B03', collection:'Terrenos',
title:'Como Criar um Projeto de Hospedagem Mesmo Sem Dinheiro?',
subtitle:'Começar pelo Conhecimento e pelo Planejamento',
tool:'Construtor de Projeto Turístico',
deliverable:'Projeto Conceitual de Hospedagem',
nameField:'nome', propertyField:'propriedade',
disclaimer:'O Projeto Conceitual é um documento de planejamento preliminar. Vocação, público e investimento são leituras orientativas feitas com as suas respostas e os seus valores; não substituem projeto arquitetônico, estudo de viabilidade, consultas legais e ambientais nem garantem demanda, aprovação de licenças ou retorno. Para implantar, procure arquiteto ou engenheiro habilitado e, em temas documentais, um advogado.',

intro:[
 {kind:'mirror', title:'Você não precisa começar comprando uma cabana. Precisa começar com um plano.',
  lead:'Você olha para a sua terra e imagina hóspedes, fogueira, café da manhã. Mas, quando pensa em dinheiro, a ideia volta para a gaveta.',
  body:'<div class="za-card"><p>Talvez você pense assim:</p><ul><li>“Só vou pensar nisso quando tiver dinheiro para construir.”</li><li>“Não sei nem que tipo de hospedagem faria sentido aqui.”</li><li>“Já vi cabanas lindas na internet, mas não sei se servem para o meu terreno.”</li><li>“Não sei quanto custaria, então nem começo.”</li></ul></div>'},
 {kind:'collapse', title:'Nem sempre a primeira etapa de um projeto turístico é construir. Muitas vezes é organizar a oportunidade.',
  lead:'Quem constrói sem plano costuma gastar duas vezes: uma para fazer, outra para corrigir. O plano custa pouco e define tudo o que vem depois.',
  body:'<div class="za-card"><p>Um projeto conceitual responde, antes de qualquer obra:</p><ol><li><b>O que a terra oferece?</b> Atributos e limitações.</li><li><b>Qual é a vocação?</b> Que tipo de experiência ela favorece.</li><li><b>Para quem?</b> O público com mais afinidade.</li><li><b>O quê, exatamente?</b> Conceito, modelo e quantidade de unidades.</li><li><b>Quanto custaria começar?</b> Uma primeira etapa possível.</li></ol><p>Tudo isso se faz com tempo, observação e pesquisa, e é o que dá base para buscar recursos depois.</p></div>'},
 {kind:'start', title:'Vamos construir o projeto conceitual da sua hospedagem',
  lead:'Em 7 pilares, o Construtor lê a vocação da sua terra, cruza com o público, monta o conceito e estima uma primeira etapa.',
  body:'<p>Não é preciso ter orçamentos agora: onde faltar um dado, marque “não sei” e ele vira tarefa no seu plano.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Rosa'},
   {id:'propriedade',label:'Nome da terra ou do projeto',type:'text',required:true,placeholder:'Ex.: Sítio Recanto do Rio'},
   {id:'cidade',label:'Município e estado',type:'text',required:true,placeholder:'Ex.: São Bento do Sapucaí (SP)'},
   {id:'area_ha',label:'Área total',type:'number',required:true,min:0.05,max:100000,step:'any',unit:'hectares'},
   {id:'recursos_hoje',label:'Como estão seus recursos hoje?',type:'radio',required:true,options:[{v:'zero',l:'Não tenho dinheiro para investir agora'},{v:'pouco',l:'Tenho pouco, suficiente para planejar'},{v:'algum',l:'Tenho algum recurso para começar uma etapa'}]}
  ]}
],

pillars:[
/* 1 */
{title:'Conhecendo o terreno', screens:[
 {kind:'learn', title:'O projeto começa caminhando pela sua terra com outros olhos',
  body:'<p>Antes de imaginar construções, faça um <b>inventário</b>: o que a terra tem que pode encantar um hóspede, e o que limita a implantação.</p><ul><li><b>Atributos:</b> água, mata, vista, silêncio, produção, clima, história.</li><li><b>Relevo:</b> plano, ondulado ou acidentado. Ele influencia o tipo de unidade e o custo da obra.</li><li><b>Área útil:</b> a parte que dá para ocupar, descontando encostas fortes, margens de rio e outras áreas protegidas. Só um engenheiro ou o órgão ambiental confirmam o que pode ser ocupado.</li><li><b>Infraestrutura:</b> energia, água e sinal de celular.</li></ul>',
  example:'Exemplo: um sítio de 8 hectares com rio, mata e serra parece amplo. Mas se a maior parte for encosta e faixa de proteção do rio, a área útil pode ser de 20% a 30%. Isso muda a quantidade e a posição das unidades.'},
 {kind:'compare', title:'Olhar de dono × olhar de projeto',
  cols:[{h:'Olhar de dono',type:'bad',items:['“Aqui é tudo bonito.”','“Dá para construir em qualquer lugar.”','“Água a gente dá um jeito.”']},
        {h:'Olhar de projeto',type:'good',items:['Quais atributos são raros e quais são comuns na região','Onde é plano, onde é encosta, onde é protegido','Quanto custa levar energia e água até cada ponto']}]},
 {kind:'form', title:'Inventário do terreno',
  fields:[
   {id:'atributos',label:'Atributos presentes',type:'checks',options:ATR.map(function(a){return {v:a.v,l:a.l};})},
   {id:'topografia',label:'Relevo predominante',type:'radio',required:true,options:[{v:'plano',l:'Plano'},{v:'ondulado',l:'Ondulado (suave)'},{v:'acidentado',l:'Acidentado (encostas fortes)'},{v:'misto',l:'Misto'}]},
   {id:'area_util',label:'Parte do terreno que você acredita ser ocupável',type:'percent',required:true,allowUnknown:true,help:'Estimativa sua. A confirmação depende de levantamento técnico.'},
   {id:'infra',label:'Infraestrutura existente',type:'checks',options:[{v:'energia',l:'Energia elétrica'},{v:'agua',l:'Água'},{v:'sinal',l:'Sinal de celular ou internet'}]}
  ]},
 {kind:'feedback', title:'O retrato do seu terreno',
  metrics:function(s,c){return [{label:'Atributos marcados',value:String(c.nAtr),tag:'informado'},{label:'Área ocupável estimada',value:c.areaUtilHa==null?'—':F.num(c.areaUtilHa,1)+' ha',tag:'estimativa'},{label:'Maturidade · terreno',value:F.num(c.m[0],0)+'/100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.nAtr===0) o.push({lv:'warn',t:'Nenhum atributo marcado. Caminhe pela área com um caderno e fotografe tudo o que um visitante acharia especial.'});
   else if(c.nAtr>=4) o.push({lv:'ok',t:c.nAtr+' atributos marcados: há matéria-prima para mais de um conceito. O Pilar 2 mostra qual vocação eles favorecem.'});
   else o.push({lv:'info',t:c.nAtr+' atributo(s) marcado(s). Com poucos atributos, o conceito e a experiência terão peso maior.'});
   if(s.t('topografia')==='acidentado') o.push({lv:'warn',t:'Relevo acidentado: obras em encosta exigem projeto técnico e tendem a custar mais. Modelos leves (glamping, cabanas elevadas) costumam se adaptar melhor.'});
   if(s.unknown('area_util')) o.push({lv:'warn',t:'Você não sabe quanto da área é ocupável. Um levantamento topográfico e uma conversa com engenheiro respondem isso, e são investimentos de planejamento, bem menores que a obra.'});
   else if(s.n('area_util',0)<20) o.push({lv:'info',t:'Área ocupável pequena ('+F.pct(s.n('area_util'),0)+'). Projetos compactos, com poucas unidades bem posicionadas, tendem a combinar melhor.'});
   if(c.nInfra<2) o.push({lv:'warn',t:'Pouca infraestrutura existente. Energia e água entram no investimento do Pilar 6.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Caminhar pelo terreno e fotografar todos os atributos'},{id:'a1_2',text:'Marcar num mapa ou imagem de satélite as áreas planas, encostas e cursos d’água'},{id:'a1_3',text:'Perguntar a um engenheiro quanto custaria um levantamento topográfico'}]}
]},
/* 2 */
{title:'Vocação turística', screens:[
 {kind:'learn', title:'Vocação é o tipo de experiência que a terra favorece naturalmente',
  body:'<p>Cada atributo do terreno “puxa” para um tipo de experiência. Água e mata puxam para natureza; silêncio e serra, para descanso e romance; produção rural, para agroturismo. O Construtor soma esses pontos e mostra a força de cada <b>vocação</b> de 0 a 100.</p><div class="za-card"><b>Como é calculado:</b> cada atributo dá 1 ou 2 pontos para certas vocações. A nota de cada vocação é a soma obtida ÷ a soma máxima possível para ela × 100.</div><p>A vocação mais forte não é obrigatória, mas ir contra ela costuma exigir mais investimento para criar a experiência.</p>',
  example:'Exemplo: rio + mata + silêncio + clima de serra somam 5 dos 6 pontos possíveis em “Descanso e bem-estar” (83/100) e 4 de 6 em “Natureza e aventura” (67/100).'},
 {kind:'compare', title:'Vocação forçada × vocação natural',
  cols:[{h:'Forçada',type:'bad',items:['Parque aquático numa área sem água','Hospedagem romântica ao lado de uma rodovia','Agroturismo sem nenhuma produção']},
        {h:'Natural',type:'good',items:['Retiro de descanso numa área silenciosa de serra','Cabanas de casal com vista e clima frio','Hospedagem rural num sítio produtivo']}]},
 {kind:'form', title:'O que você gostaria de oferecer',
  fields:[
   {id:'interesse',label:'Que tipo de experiência você mais gostaria de oferecer?',type:'radio',required:true,options:VOC.map(function(v){return {v:v.k,l:v.n};})},
   {id:'experiencias',label:'Experiências possíveis na sua área',type:'checks',options:[{v:'trilha',l:'Trilhas e caminhadas'},{v:'banho',l:'Banho de rio ou cachoeira'},{v:'estrelas',l:'Observação de estrelas'},{v:'colheita',l:'Colheita, horta ou lida com animais'},{v:'cafe',l:'Café da manhã com produtos locais'},{v:'fogueira',l:'Fogueira e noites ao ar livre'},{v:'relax',l:'Ofurô, banheira ou espaço de relaxamento'}]},
   {id:'destino_prox',label:'Sua área fica perto de um destino turístico conhecido?',type:'radio',required:true,options:[{v:'sim',l:'Sim, a menos de 30 minutos'},{v:'medio',l:'Entre 30 minutos e 1h30'},{v:'nao',l:'Não, mais longe que isso'}]}
  ]},
 {kind:'feedback', title:'A vocação da sua terra',
  metrics:function(s,c){return c.vocRank.slice(0,3).map(function(v){return {label:v.n,value:F.num(v.score,0)+'/100',tag:'calculado'};});},
  feedback:function(s,c){var o=[];var top=c.vocRank[0];
   if(c.nAtr===0) o.push({lv:'warn',t:'Sem atributos marcados no Pilar 1, não há como ler a vocação. Volte ao inventário.'});
   else o.push({lv:'info',t:'A vocação mais forte da sua terra é <b>'+top.n+'</b> ('+F.num(top.score,0)+'/100).'});
   if(c.nAtr>0){ if(c.intRank===1) o.push({lv:'ok',t:'O que você quer oferecer coincide com a vocação mais forte. Isso reduz o esforço para criar a experiência.'});
     else if(c.intScore>=50) o.push({lv:'info',t:'Sua preferência ('+c.intNome+', '+F.num(c.intScore,0)+'/100) é a '+c.intRank+'ª vocação da terra. Pode funcionar, combinando com a mais forte.'});
     else o.push({lv:'warn',t:'Sua preferência ('+c.intNome+') tem só '+F.num(c.intScore,0)+'/100 de afinidade com o terreno. Ir por esse caminho exige criar a experiência do zero.'});}
   var ne=arr(s,'experiencias').length; if(ne<2) o.push({lv:'warn',t:'Poucas experiências possíveis marcadas. Experiências são o que transforma uma diária em uma estadia lembrada.'});
   else o.push({lv:'ok',t:ne+' experiências possíveis: elas entram no conceito do Pilar 4.'});
   if(s.t('destino_prox')==='nao') o.push({lv:'info',t:'Longe de destinos conhecidos, o projeto precisa ser o próprio motivo da viagem. Vocação e conceito ficam ainda mais importantes.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Visitar ou pesquisar 3 hospedagens da região com a mesma vocação'},{id:'a2_2',text:'Testar as experiências possíveis com amigos ou familiares'},{id:'a2_3',text:'Escolher a vocação principal do projeto'}]}
]},
/* 3 */
{title:'Público', screens:[
 {kind:'learn', title:'O público certo é o que já deseja aquilo que a sua terra oferece',
  body:'<p>Cada vocação tem um público com afinidade natural: descanso combina com quem busca bem-estar; serra e silêncio, com casais; produção rural e área plana, com famílias. O Construtor mede a <b>afinidade</b> entre o público escolhido e a vocação do terreno.</p><p>Três perguntas ajudam a definir o público:</p><ul><li>Quem viajaria até aqui e de onde vem?</li><li>Quanto tempo de viagem essa pessoa aceita para um fim de semana?</li><li>Quantos dias ela ficaria?</li></ul>',
  example:'Exemplo: um terreno com vocação “romântico” 100/100 e público “casais” tem afinidade máxima. Se o público escolhido for “famílias com crianças” e a vocação família for 25/100, o projeto vai precisar criar estrutura de lazer que a terra não oferece naturalmente.'},
 {kind:'compare', title:'Público genérico × público definido',
  cols:[{h:'Genérico',type:'bad',items:['“Para todo mundo que gosta de natureza.”','Sem saber de onde vem o hóspede','Sem saber quantos dias ele fica']},
        {h:'Definido',type:'good',items:['“Casais de cidades a até 3 horas, para fins de semana.”','Origem e tempo de viagem conhecidos','Estadia típica estimada']}]},
 {kind:'form', title:'Seu público principal',
  fields:[
   {id:'publico',label:'Público principal',type:'radio',required:true,options:Object.keys(PUB).map(function(k){return {v:k,l:PUB[k].l.charAt(0).toUpperCase()+PUB[k].l.slice(1)};})},
   {id:'origem_publico',label:'De onde viria esse público (cidade ou região)',type:'text',required:true,placeholder:'Ex.: São Paulo e Campinas'},
   {id:'tempo_viagem',label:'Tempo de viagem desde essa origem',type:'number',required:true,allowUnknown:true,min:0,max:48,step:'any',unit:'horas'},
   {id:'permanencia',label:'Estadia típica que você imagina',type:'radio',required:true,options:[{v:'fds',l:'Fins de semana (2 noites)'},{v:'feriado',l:'Feriados e férias (3 a 5 noites)'},{v:'semana',l:'Semana ou mais'}]}
  ]},
 {kind:'feedback', title:'Afinidade entre público e terreno',
  metrics:function(s,c){return [{label:'Afinidade público × vocação',value:F.num(c.pubFit,0)+'/100',tag:'calculado'},{label:'Maturidade · público',value:F.num(c.m[2],0)+'/100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.pubFit>=75) o.push({lv:'ok',t:'Alta afinidade: o público escolhido busca exatamente o que a sua terra oferece.'});
   else if(c.pubFit>=50) o.push({lv:'info',t:'Afinidade média ('+F.num(c.pubFit,0)+'/100). Reforce no conceito as experiências que esse público procura.'});
   else o.push({lv:'warn',t:'Afinidade baixa ('+F.num(c.pubFit,0)+'/100) entre o público e os atributos do terreno. Considere o público de maior afinidade: '+esc(c.pubSug)+'.'});
   var t=s.n('tempo_viagem'); if(s.unknown('tempo_viagem')) o.push({lv:'warn',t:'Você não sabe o tempo de viagem do público. Calcule pelo mapa: ele define se o projeto é de fim de semana ou de férias.'});
   else if(t>4&&s.t('permanencia')==='fds') o.push({lv:'warn',t:'Mais de 4 horas de viagem para estadias de fim de semana tende a afastar o hóspede. Reveja a origem do público ou a estadia típica.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Conversar com 5 pessoas do público escolhido sobre o que buscam numa viagem'},{id:'a3_2',text:'Medir no mapa o tempo de viagem das principais cidades de origem'},{id:'a3_3',text:'Ler avaliações de hóspedes em hospedagens parecidas para entender o que valorizam'}]}
]},
/* 4 */
{title:'Conceito', screens:[
 {kind:'learn', title:'Conceito é a promessa da hospedagem em poucas palavras',
  body:'<p>O conceito une vocação, público e experiência numa ideia que guia todas as decisões: arquitetura, decoração, preço, fotos e comunicação.</p><p>Um conceito completo tem:</p><ul><li><b>Nome provisório</b> (pode mudar depois).</li><li><b>Promessa:</b> o que o hóspede vai sentir ou viver.</li><li><b>Três palavras</b> que descrevem a atmosfera.</li><li><b>Experiência principal:</b> a cena que o hóspede vai fotografar e contar.</li></ul><p>O Construtor monta, com as suas respostas, uma <b>frase-conceito</b> que você pode refinar.</p>',
  example:'Exemplo: “Refúgio Serra Fria · cabanas para quem busca descanso e silêncio, com banho de rio ao amanhecer. Atmosfera: silêncio, rio, aconchego.”'},
 {kind:'compare', title:'Conceito decorativo × conceito que orienta',
  cols:[{h:'Decorativo',type:'bad',items:['“Um lugar mágico.”','Palavras que servem para qualquer hospedagem','Sem experiência concreta']},
        {h:'Orienta decisões',type:'good',items:['Diz para quem é e o que se vive ali','Ajuda a escolher materiais, cores e serviços','Tem uma experiência que só existe nesse lugar']}]},
 {kind:'form', title:'Monte seu conceito',
  fields:[
   {id:'nome_conceito',label:'Nome provisório do projeto',type:'text',required:true,placeholder:'Ex.: Refúgio Serra Fria'},
   {id:'promessa',label:'Promessa ao hóspede',type:'textarea',required:false,placeholder:'Ex.: Dias de silêncio, banho de rio e café da manhã da roça'},
   {id:'palavras',label:'Três palavras da atmosfera',type:'text',required:false,placeholder:'Ex.: silêncio, rio, aconchego'},
   {id:'experiencia_principal',label:'Experiência principal (a cena que o hóspede vai contar)',type:'text',required:true,placeholder:'Ex.: banho de rio ao amanhecer'}
  ]},
 {kind:'feedback', title:'Sua frase-conceito',
  metrics:function(s,c){return [{label:'Conceito completo',value:F.num(c.m[3],0)+'/100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:'info',t:'Frase-conceito montada: <b>'+c.frase+'</b>'});
   if(s.t('promessa').trim().length<30) o.push({lv:'warn',t:'A promessa está ausente ou curta. Escreva o que o hóspede vai sentir, em uma frase completa.'});
   if(!s.t('palavras').trim()) o.push({lv:'warn',t:'Defina as três palavras da atmosfera: elas orientam arquitetura, decoração e fotos.'});
   if(s.t('experiencia_principal').trim().length<5) o.push({lv:'warn',t:'A experiência principal precisa ser concreta: uma cena, não um adjetivo.'});
   if(c.m[3]===100) o.push({lv:'ok',t:'Conceito completo. Teste a frase com pessoas do público escolhido e veja se elas querem saber mais.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Ler a frase-conceito para 5 pessoas do público e anotar as reações'},{id:'a4_2',text:'Montar um painel de referências (fotos, materiais, cores) coerente com as 3 palavras'},{id:'a4_3',text:'Ajustar o nome provisório depois dos testes'}]}
]},
/* 5 */
{title:'Modelo de hospedagem', screens:[
 {kind:'learn', title:'O modelo certo é o que cabe no terreno, no conceito e no bolso',
  body:'<p>Cabanas, glamping, chalés, casa inteira e pousada têm custos, operação e adaptação ao relevo diferentes. O Construtor avalia duas coisas:</p><ul><li><b>Adequação ao relevo</b> (0 a 100): alguns modelos se adaptam bem a encostas; outros precisam de área plana.</li><li><b>Complexidade de implantação</b> (1 a 3): quanto de obra, licenças e equipe o modelo costuma exigir.</li></ul><p>Pense também em <b>etapas</b>: começar com poucas unidades e crescer com a receita é uma forma de começar com menos dinheiro.</p>',
  example:'Exemplo: em terreno acidentado, uma pousada (prédio maior, área plana) tem adequação baixa; cabanas elevadas ou glamping se adaptam melhor e permitem começar com 2 unidades.'},
 {kind:'compare', title:'Começar grande × começar por etapas',
  cols:[{h:'Tudo de uma vez',type:'bad',items:['Exige todo o capital antes da primeira diária','Erros de projeto se repetem em todas as unidades','Risco concentrado']},
        {h:'Por etapas',type:'good',items:['Primeira etapa menor e validável','Aprendizado aplicado às próximas unidades','A receita da etapa 1 pode ajudar a etapa 2']}]},
 {kind:'form', title:'Seu modelo e suas etapas',
  fields:[
   {id:'modelo',label:'Modelo de hospedagem',type:'radio',required:true,options:Object.keys(MODS).map(function(k){return {v:k,l:MODS[k].l.charAt(0).toUpperCase()+MODS[k].l.slice(1)};})},
   {id:'unidades_total',label:'Unidades na visão completa do projeto',type:'number',required:true,min:1,max:200,step:1,unit:'unidades'},
   {id:'unidades_f1',label:'Unidades na primeira etapa',type:'number',required:true,min:1,max:200,step:1,unit:'unidades',validate:function(v,s){var t=s.n('unidades_total');return (t!=null&&v>t)?'A primeira etapa não pode ter mais unidades que o total.':'';}},
   {id:'capacidade',label:'Hóspedes por unidade',type:'number',required:true,min:1,max:30,step:1,unit:'pessoas'}
  ]},
 {kind:'feedback', title:'Adequação do modelo',
  metrics:function(s,c){return [{label:'Adequação ao relevo',value:F.num(c.fit,0)+'/100',tag:'calculado'},{label:'Complexidade',value:c.cx+' de 3',tag:'recomendacao'},{label:'Leitos na 1ª etapa',value:F.num(c.leitosF1),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.fit<50) o.push({lv:'warn',t:'O modelo escolhido tem baixa adequação ao relevo informado. Converse com um arquiteto antes de seguir: pode ser preciso mudar o modelo ou a área de implantação.'});
   else if(c.fit<100) o.push({lv:'info',t:'Adequação média ao relevo. É viável, mas a escolha do local exato das unidades fará diferença no custo.'});
   else o.push({lv:'ok',t:'O modelo se adapta bem ao relevo informado.'});
   if(c.cx===3) o.push({lv:'info',t:'Pousada é o modelo de maior complexidade (obra, equipe, licenças). Para começar com pouco capital, avalie uma primeira etapa com unidades independentes.'});
   var f1=s.n('unidades_f1',0), t=s.n('unidades_total',0);
   if(f1===t&&t>3) o.push({lv:'warn',t:'A primeira etapa já é o projeto inteiro ('+F.num(t)+' unidades). Dividir em etapas reduz o capital inicial necessário.'});
   else if(f1<t) o.push({lv:'ok',t:'Primeira etapa com '+F.num(f1)+' de '+F.num(t)+' unidades: '+F.pct(f1/t*100,0)+' do projeto. Bom caminho para começar menor.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Visitar ou pesquisar 2 hospedagens do modelo escolhido'},{id:'a5_2',text:'Definir o local aproximado das unidades da primeira etapa'},{id:'a5_3',text:'Confirmar com arquiteto se o modelo combina com o relevo'}]}
]},
/* 6 */
{title:'Investimento preliminar', screens:[
 {kind:'learn', title:'Quanto custaria começar, e o que dá para fazer antes da obra',
  body:'<p>O investimento de uma hospedagem tem três blocos: <b>unidades</b> (construção ou estrutura + mobiliário), <b>infraestrutura</b> (energia, água, saneamento, acesso interno) e <b>projetos</b> (topografia, arquitetura, consultas e licenças). Sobre o total, aplica-se uma <b>reserva de contingência</b> para imprevistos.</p><div class="za-card"><b>Etapa 1 = [unidades da etapa 1 × (custo da unidade + mobiliário) + infraestrutura + projetos] × (1 + contingência)</b></div><p>O bloco de <b>projetos</b> é o que mais combina com quem tem pouco dinheiro: ele vem antes da obra, custa uma fração do total e transforma a ideia em algo que pode ser orçado, aprovado e apresentado.</p><p class="za-small">Use valores de cotações ou pesquisas suas. O Construtor não usa preços de mercado.</p>',
  example:'Exemplo ilustrativo: 2 cabanas × (R$ 120 mil + R$ 15 mil) + R$ 55 mil de infraestrutura + R$ 25 mil de projetos = R$ 350 mil; com 10% de contingência, R$ 385 mil. Os R$ 25 mil de projetos podem ser feitos antes, em partes.'},
 {kind:'compare', title:'Orçamento de cabeça × orçamento por blocos',
  cols:[{h:'De cabeça',type:'bad',items:['“Uma cabana custa uns 100 mil.”','Esquece energia, água e esgoto','Sem projetos nem licenças','Sem reserva para imprevistos']},
        {h:'Por blocos',type:'good',items:['Unidade + mobiliário cotados','Infraestrutura listada item a item','Projetos e consultas como primeira etapa','Contingência explícita']}]},
 {kind:'form', title:'Seu investimento preliminar',
  fields:[
   {id:'custo_unidade',label:'Custo de construção de uma unidade',type:'money',required:true,allowUnknown:true,help:'De uma cotação ou pesquisa com fornecedores.'},
   {id:'mobiliario',label:'Mobiliário e enxoval por unidade',type:'money',required:true,allowUnknown:true},
   {id:'infra_lista',label:'Infraestrutura (valores totais)',type:'list',required:false,preset:['Energia','Água / poço','Saneamento','Acesso interno'],namePlaceholder:'Item',valuePlaceholder:'R$'},
   {id:'projetos',label:'Projetos e consultas (valores totais)',type:'list',required:false,preset:['Levantamento topográfico','Projeto arquitetônico','Consultas e licenças'],namePlaceholder:'Item',valuePlaceholder:'R$'},
   {id:'contingencia',label:'Reserva de contingência',type:'percent',required:true,max:50,help:'Percentual sobre o total para imprevistos. Escolha conforme o grau de incerteza dos seus números.'},
   {id:'recursos',label:'Recursos que você tem para o projeto hoje',type:'money',required:true,help:'Pode ser zero.'}
  ]},
 {kind:'feedback', title:'Sua primeira etapa em números',
  metrics:function(s,c){return [{label:'Etapa 1 com contingência',value:F.brl0(c.invF1),tag:'estimativa'},{label:'Projeto completo',value:F.brl0(c.invTotal),tag:'estimativa'},{label:'Projetos e consultas',value:F.brl0(c.plan),tag:'informado'},{label:'Falta para a etapa 1',value:F.brl0(c.gapF1),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.invF1==null) o.push({lv:'warn',t:'Sem custo da unidade ou do mobiliário, não dá para estimar a etapa 1. Peça 2 orçamentos a fornecedores do modelo escolhido.'});
   if(c.nInfraL===0) o.push({lv:'warn',t:'Nenhum item de infraestrutura informado. Energia, água e saneamento quase sempre fazem parte do investimento.'});
   if(c.plan<=0) o.push({lv:'warn',t:'Nenhum valor de projetos e consultas. Essa é a etapa que você pode começar antes da obra: pergunte preços de topografia e de projeto.'});
   else if(c.cobPlan!=null&&c.cobPlan>=1) o.push({lv:'ok',t:'Seus recursos atuais ('+F.brl0(s.n('recursos'))+') cobrem a etapa de projetos e consultas ('+F.brl0(c.plan)+'). Você pode começar a planejar agora.'});
   else if(c.cobPlan!=null) o.push({lv:'info',t:'Seus recursos cobrem '+F.pct(c.cobPlan*100,0)+' da etapa de projetos. Divida-a: topografia primeiro, depois arquitetura.'});
   if(s.n('contingencia',0)<5) o.push({lv:'warn',t:'Contingência abaixo de 5%. Imprevistos em obra rural são comuns; uma reserva baixa transforma qualquer surpresa em problema.'});
   if(c.gapF1!=null&&c.gapF1>0) o.push({lv:'info',t:'Para a etapa 1 faltariam '+F.brl0(c.gapF1)+'. O plano conceitual é exatamente o material para conversar sobre parceria, financiamento ou implantação progressiva.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Pedir 2 orçamentos da unidade e do mobiliário'},{id:'a6_2',text:'Consultar a concessionária sobre o custo de levar energia'},{id:'a6_3',text:'Começar pela etapa de projetos: topografia e consulta de uso do solo'}]}
]},
/* 7 */
{title:'Projeto conceitual', screens:[
 {kind:'learn', title:'O projeto conceitual é a sua ferramenta para buscar recursos',
  body:'<p>Com terreno, vocação, público, conceito, modelo e investimento organizados, você tem um <b>Projeto Conceitual</b>. Ele não é projeto arquitetônico nem estudo de viabilidade, mas permite:</p><ul><li>pedir orçamentos precisos;</li><li>conversar com arquiteto e engenheiro sabendo o que quer;</li><li>apresentar a ideia a possíveis parceiros;</li><li>decidir a próxima etapa com segurança.</li></ul><p>O Construtor calcula a <b>maturidade do projeto</b> (0 a 100) como a média de sete dimensões: terreno, vocação, público, conceito, modelo, investimento e preparação.</p>',
  example:'Exemplo: um projeto com conceito e modelo completos, mas sem orçamento e sem fotos, tem maturidade média. A próxima ação é clara: orçar e documentar, não “esperar o dinheiro”.'},
 {kind:'compare', title:'Ideia guardada × projeto em andamento',
  cols:[{h:'Ideia guardada',type:'bad',items:['Só na cabeça do dono','Esperando o dinheiro aparecer','Sem prazo']},
        {h:'Projeto em andamento',type:'good',items:['Documento com conceito, modelo e números','Próximo passo definido','Prazo e horas por semana reservados']}]},
 {kind:'form', title:'Preparação e próximo passo',
  fields:[
   {id:'preparo',label:'O que você já tem',type:'checks',options:PREP},
   {id:'prazo_meses',label:'Em quantos meses quer concluir o projeto conceitual com orçamentos?',type:'number',required:true,min:1,max:36,step:1,unit:'meses'},
   {id:'proximo_passo',label:'Qual será seu próximo passo?',type:'radio',required:true,options:[{v:'orcamentos',l:'Pedir orçamentos'},{v:'topografia',l:'Contratar topografia / consulta técnica'},{v:'arquiteto',l:'Conversar com arquiteto'},{v:'parceiro',l:'Apresentar a ideia a um possível parceiro'},{v:'pesquisa',l:'Pesquisar mais o público e a concorrência'}]}
  ]},
 {kind:'feedback', title:'A maturidade do seu projeto',
  metrics:function(s,c){return [{label:'Maturidade do projeto',value:F.num(c.idx,0)+'/100',tag:'calculado'},{label:'Dimensão mais fraca',value:c.pior.n,tag:'calculado'},{label:'Vocação principal',value:c.vocRank[0].n,tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:c.idx>=75?'ok':c.idx>=50?'info':'warn',t:'Maturidade de <b>'+F.num(c.idx,0)+'/100</b>. Dimensão mais fraca: <b>'+c.pior.n+'</b> ('+F.num(c.pior.v,0)+'/100).'});
   if(s.t('proximo_passo')==='parceiro'&&c.idx<60) o.push({lv:'warn',t:'Você quer apresentar a um parceiro, mas o projeto ainda está com maturidade baixa. Fortaleça primeiro a dimensão mais fraca.'});
   if(s.t('proximo_passo')==='orcamentos'&&c.invF1!=null) o.push({lv:'info',t:'Você já tem uma estimativa; os orçamentos vão confirmá-la ou corrigi-la.'});
   if(!has(arr(s,'preparo'),'profissional')) o.push({lv:'info',t:'Uma conversa inicial com arquiteto ou engenheiro costuma evitar escolhas caras. Leve este relatório.'});
   if(s.n('prazo_meses',0)>12) o.push({lv:'warn',t:'Prazo de mais de 12 meses para o projeto conceitual. Divida em metas mensais para não perder o ritmo.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Imprimir o Projeto Conceitual e levá-lo à primeira conversa técnica'},{id:'a7_2',text:'Executar o próximo passo escolhido nos próximos 15 dias'},{id:'a7_3',text:'Refazer o Construtor depois dos orçamentos e comparar a maturidade'}]}
]}
],

compute:function(s){
 var c={};
 c.atr=arr(s,'atributos'); c.nAtr=ATR.filter(function(a){return has(c.atr,a.v);}).length;
 c.voc={}; VOC.forEach(function(v){var p=ATR.reduce(function(t,a){return t+(has(c.atr,a.v)?(a.p[v.k]||0):0);},0); c.voc[v.k]=VMAX[v.k]?p/VMAX[v.k]*100:0;});
 c.vocRank=VOC.map(function(v,i){return {k:v.k,n:v.n,desejo:v.desejo,score:c.voc[v.k],i:i};}).sort(function(a,b){return (b.score-a.score)||(a.i-b.i);});
 var it=s.t('interesse'); c.intRank=1+c.vocRank.map(function(v){return v.k;}).indexOf(it); c.intScore=c.voc[it]||0;
 c.intNome=(VOC.filter(function(v){return v.k===it;})[0]||{n:'—'}).n;
 c.nInfra=arr(s,'infra').length;
 var au=s.n('area_util'); c.areaUtilHa=au!=null?s.n('area_ha',0)*au/100:null;
 // público
 var pb=PUB[s.t('publico')]; c.pubFit=pb?c.voc[pb.voc]:0;
 var best=Object.keys(PUB).map(function(k){return {l:PUB[k].l,v:c.voc[PUB[k].voc]};}).sort(function(a,b){return b.v-a.v;})[0]; c.pubSug=best.l;
 // conceito
 var nome=s.t('nome_conceito').trim(), prom=s.t('promessa').trim(), pal=s.t('palavras').trim(), exp=s.t('experiencia_principal').trim();
 var md=MODS[s.t('modelo')], top=c.vocRank[0];
 c.frase=esc(nome||'Projeto')+' · '+esc(md?md.l:'hospedagem')+' para '+esc(pb?pb.l:'o público escolhido')+' em busca de '+esc(c.nAtr?top.desejo:'uma experiência a definir')+', em '+esc(s.t('cidade'))+'. Experiência principal: '+(exp?esc(exp):'a definir')+'.'+(pal?' Atmosfera: '+esc(pal)+'.':'');
 // modelo
 c.fit=md?(md.fit[s.t('topografia')]||0)/2*100:0; c.cx=md?md.cx:0;
 c.leitosF1=s.n('unidades_f1',0)*s.n('capacidade',0);
 // investimento
 var cu=s.n('custo_unidade'), mob=s.n('mobiliario'), ct=s.n('contingencia',0)/100;
 c.infraL=rows(s,'infra_lista'); c.nInfraL=c.infraL.length; c.infraSum=ZA.listSum(c.infraL);
 c.projL=rows(s,'projetos'); c.plan=ZA.listSum(c.projL);
 c.custoUnit=(cu!=null&&mob!=null)?cu+mob:null;
 c.invF1=c.custoUnit!=null?(s.n('unidades_f1',0)*c.custoUnit+c.infraSum+c.plan)*(1+ct):null;
 c.invTotal=c.custoUnit!=null?(s.n('unidades_total',0)*c.custoUnit+c.infraSum+c.plan)*(1+ct):null;
 c.gapF1=c.invF1!=null?Math.max(0,c.invF1-s.n('recursos',0)):null;
 c.cobPlan=c.plan>0?s.n('recursos',0)/c.plan:null;
 // maturidade
 var m=[];
 m[0]=50*Math.min(c.nAtr,4)/4+25*(au!=null?1:0)+25*Math.min(c.nInfra,3)/3;
 m[1]=c.nAtr?top.score:0;
 m[2]=0.7*c.pubFit+30*(s.n('tempo_viagem')!=null?1:0);
 m[3]=25*(nome?1:0)+25*(prom.length>=30?1:0)+25*(pal?1:0)+25*(exp.length>=5?1:0);
 m[4]=c.fit;
 m[5]=40*(c.custoUnit!=null?1:0)+20*(c.nInfraL>0?1:0)+20*(c.plan>0?1:0)+20*(ct>0?1:0);
 c.nPrep=PREP.filter(function(p){return has(arr(s,'preparo'),p.v);}).length;
 m[6]=25*c.nPrep;
 c.m=m; c.idx=m.reduce(function(t,x){return t+x;},0)/7;
 c.dims=DIMN.map(function(n,i){return {n:n,v:m[i]};});
 c.pior=c.dims.slice().sort(function(a,b){return a.v-b.v;})[0];
 return c;
},

metrics:function(s,c){return [
 {label:'Maturidade do projeto',value:F.num(c.idx,0)+'/100',tag:'calculado'},
 {label:'Vocação principal',value:c.nAtr?c.vocRank[0].n:'—',tag:'calculado'},
 {label:'Afinidade público × vocação',value:F.num(c.pubFit,0)+'/100',tag:'calculado'},
 {label:'Adequação do modelo ao relevo',value:F.num(c.fit,0)+'/100',tag:'calculado'},
 {label:'Unidades (etapa 1 / total)',value:F.num(s.n('unidades_f1'))+' / '+F.num(s.n('unidades_total')),tag:'informado'},
 {label:'Investimento etapa 1',value:F.brl0(c.invF1),tag:'estimativa'},
 {label:'Projetos e consultas',value:F.brl0(c.plan),tag:'informado'},
 {label:'Dimensão mais fraca',value:c.pior.n,tag:'calculado'}
];},

priorities:function(s,c){var L=[];
 if(c.nAtr<2) L.push({title:'Fazer o inventário de atributos do terreno',why:'Sem ele não há leitura de vocação.',score:8});
 if(s.unknown('area_util')) L.push({title:'Descobrir a área ocupável com levantamento técnico',why:'Define quantas unidades cabem e onde.',score:7});
 if(c.nAtr>=2&&c.intScore<50) L.push({title:'Reconsiderar a experiência desejada à luz da vocação do terreno',why:'Sua preferência tem '+F.num(c.intScore,0)+'/100 de afinidade.',score:6});
 if(c.pubFit<50) L.push({title:'Rever o público principal (sugestão: '+c.pubSug+')',why:'Afinidade público × terreno de '+F.num(c.pubFit,0)+'/100.',score:7});
 if(s.unknown('tempo_viagem')) L.push({title:'Medir o tempo de viagem do público até a área',why:'Define se o projeto é de fim de semana ou de férias.',score:4});
 if(c.m[3]<75) L.push({title:'Completar o conceito: promessa, três palavras e experiência',why:'Conceito em '+F.num(c.m[3],0)+'/100.',score:6});
 if(c.fit<50) L.push({title:'Validar o modelo com arquiteto (baixa adequação ao relevo)',why:'O modelo pode exigir obra cara ou ser inviável no local.',score:8});
 if(s.n('unidades_f1',0)===s.n('unidades_total',0)&&s.n('unidades_total',0)>3) L.push({title:'Dividir o projeto em etapas',why:'Reduz o capital necessário para começar.',score:6});
 if(c.custoUnit==null) L.push({title:'Pedir orçamentos da unidade e do mobiliário',why:'Sem eles, não há investimento estimado.',score:7});
 if(c.nInfraL===0) L.push({title:'Levantar custos de energia, água e saneamento',why:'Infraestrutura costuma ser parte relevante do investimento.',score:5});
 if(c.plan<=0) L.push({title:'Orçar a etapa de projetos e consultas',why:'É a etapa que você pode iniciar com pouco dinheiro.',score:6});
 else if(c.cobPlan!=null&&c.cobPlan>=1) L.push({title:'Contratar a etapa de projetos e consultas',why:'Seus recursos atuais já cobrem essa etapa.',score:7});
 if(c.nPrep<2) L.push({title:'Fotografar o terreno e desenhar o croqui das unidades',why:'Material básico para orçar e apresentar.',score:4});
 if(!has(arr(s,'preparo'),'profissional')) L.push({title:'Marcar conversa inicial com arquiteto ou engenheiro',why:'Evita escolhas caras e confirma o que pode ser construído.',score:5});
 return L;},

report:function(s,c){
 var voc=ZA.table(['Vocação','Afinidade'],c.vocRank.map(function(v){return [v.n,F.num(v.score,0)+'/100'];}),[1]);
 var conc='<div class="za-card"><p><b>'+c.frase+'</b></p>'+(s.t('promessa')?'<p>Promessa: '+esc(s.t('promessa'))+'</p>':'')+'<p>Público: '+esc((PUB[s.t('publico')]||{l:'a definir'}).l)+', vindo de '+esc(s.t('origem_publico'))+(s.n('tempo_viagem')!=null?' ('+F.num(s.n('tempo_viagem'),1)+' h de viagem)':'')+'. Estadia típica: '+esc({fds:'fins de semana',feriado:'feriados e férias',semana:'semana ou mais'}[s.t('permanencia')]||'—')+'.</p><p>Experiências possíveis: '+(arr(s,'experiencias').length?esc(arr(s,'experiencias').map(function(x){return {trilha:'trilhas',banho:'banho de rio ou cachoeira',estrelas:'observação de estrelas',colheita:'colheita e lida rural',cafe:'café da manhã com produtos locais',fogueira:'fogueira',relax:'espaço de relaxamento'}[x];}).join(', ')):'a definir')+'.</p></div>';
 var mod=ZA.table(['Item','Valor'],[['Modelo',esc((MODS[s.t('modelo')]||{l:'—'}).l)],['Relevo',esc({plano:'plano',ondulado:'ondulado',acidentado:'acidentado',misto:'misto'}[s.t('topografia')]||'—')],['Adequação ao relevo',F.num(c.fit,0)+'/100'],['Complexidade de implantação',c.cx+' de 3'],['Unidades etapa 1 / total',F.num(s.n('unidades_f1'))+' / '+F.num(s.n('unidades_total'))],['Leitos na etapa 1',F.num(c.leitosF1)]],[1]);
 var inv=c.custoUnit==null?'<p class="za-missing">Custo da unidade ou do mobiliário não informado: o investimento das etapas ainda não pode ser estimado. A etapa de projetos soma '+F.brl0(c.plan)+'.</p>':ZA.table(['Bloco','Etapa 1','Projeto completo'],[
  ['Unidades × (construção + mobiliário)',F.brl0(s.n('unidades_f1',0)*c.custoUnit),F.brl0(s.n('unidades_total',0)*c.custoUnit)],
  ['Infraestrutura',F.brl0(c.infraSum),F.brl0(c.infraSum)],['Projetos e consultas',F.brl0(c.plan),F.brl0(c.plan)],
  ['Contingência ('+F.pct(s.n('contingencia',0),0)+')',F.brl0(c.invF1-c.invF1/(1+s.n('contingencia',0)/100)),F.brl0(c.invTotal-c.invTotal/(1+s.n('contingencia',0)/100))],
  ['<b>Total</b>','<b>'+F.brl0(c.invF1)+'</b>','<b>'+F.brl0(c.invTotal)+'</b>']],[1,2])+'<p class="za-small">Infraestrutura e projetos foram considerados uma única vez, na etapa 1. Na prática, a expansão pode exigir infraestrutura adicional.</p>';
 var mat=ZA.table(['Dimensão','Maturidade'],c.dims.map(function(d){return [d.n,F.num(d.v,0)+'/100'];}).concat([['<b>Maturidade do projeto</b>','<b>'+F.num(c.idx,1)+'/100</b>']]),[1]);
 var semDinheiro='<ul><li>Inventário do terreno com fotos e mapa (custo: seu tempo).</li><li>Pesquisa de concorrentes e conversas com o público (custo: seu tempo).</li><li>Conceito testado com pessoas reais.</li><li>Orçamentos de fornecedores (geralmente sem custo).</li><li>Etapa de projetos e consultas: '+F.brl0(c.plan)+(c.cobPlan!=null?' · seus recursos cobrem '+F.pct(Math.min(1,c.cobPlan)*100,0)+' dela':'')+'.</li></ul>';
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Área total',F.num(s.n('area_ha'),2)+' ha',tag('informado')],
  ['Área ocupável',s.unknown('area_util')?'—':F.pct(s.n('area_util'),0),s.unknown('area_util')?tag('hipotese','ausente'):tag('estimativa','sua estimativa')],
  ['Custo por unidade',F.brl0(s.n('custo_unidade')),s.unknown('custo_unidade')?tag('hipotese','ausente'):tag('informado')],
  ['Mobiliário por unidade',F.brl0(s.n('mobiliario')),s.unknown('mobiliario')?tag('hipotese','ausente'):tag('informado')],
  ['Contingência',F.pct(s.n('contingencia',0),0),tag('informado')],
  ['Pontos de atributo por vocação','tabela Zion (1 ou 2 pontos por atributo)',tag('recomendacao','metodologia Zion')],
  ['Adequação modelo × relevo','tabela Zion (0, 50 ou 100)',tag('recomendacao','metodologia Zion')],
  ['Maturidade','média simples das 7 dimensões',tag('recomendacao','metodologia Zion')]],[1]);
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var pp={orcamentos:'pedir orçamentos',topografia:'contratar topografia / consulta técnica',arquiteto:'conversar com arquiteto',parceiro:'apresentar a ideia a um possível parceiro',pesquisa:'pesquisar público e concorrência'}[s.t('proximo_passo')]||'definir o próximo passo';
 var plan='<div class="za-card"><b>Roteiro do projeto conceitual ('+F.num(s.n('prazo_meses'))+' meses)</b><ol><li><b>Primeiras 2 semanas:</b> '+esc(pp)+'.</li><li><b>Primeiro mês:</b> '+(top[0]?esc(top[0].title):'Completar o inventário do terreno')+'.</li><li><b>Segundo mês:</b> '+(top[1]?esc(top[1].title):'Fechar o conceito')+'.</li><li><b>Terceiro mês:</b> '+(top[2]?esc(top[2].title):'Orçar a etapa 1')+'.</li><li><b>Ao final do prazo:</b> refazer o Construtor com os orçamentos e decidir o caminho de recursos (próprios, parceria ou etapas).</li></ol></div>';
 return {sections:[
  {title:'Vocação turística do terreno',html:voc+'<p class="za-small">Leitura orientativa a partir dos atributos que você marcou. Não substitui pesquisa de demanda.</p>'},
  {title:'Conceito',html:conc},
  {title:'Modelo de hospedagem',html:mod},
  {title:'Investimento preliminar',html:inv},
  {title:'O que dá para fazer antes de ter o dinheiro da obra',html:semDinheiro},
  {title:'Maturidade do projeto por dimensão',html:mat},
  {title:'Premissas utilizadas',html:prem}
 ],plan:plan};
}
});
})();
