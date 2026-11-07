/* ZAR-B07 · Qual Hospedagem Construir no Meu Terreno? · Comparador de Modelos de Hospedagem */
(function(){
var F=ZA.fmt, esc=ZA.esc;
var MODELS=[['cab','Cabana'],['gla','Glamping'],['cha','Chalé'],['pou','Pousada']];
var CRIT=[['t','Adequação ao terreno'],['p','Aderência ao público'],['a','Atratividade e diferenciação'],['i','Infraestrutura exigida'],['c','Custo × orçamento'],['o','Facilidade de operação']];
function nm(k){for(var i=0;i<MODELS.length;i++)if(MODELS[i][0]===k)return MODELS[i][1];return k;}
function opts15(lo,hi){return ['1','2','3','4','5'].map(function(v){return {v:v,l:v==='1'?'1 · '+lo:v==='5'?'5 · '+hi:v};});}
function scaleFields(pref,label,help){return MODELS.map(function(m){return {id:pref+'_'+m[0],label:m[1]+': '+label,type:'radio',required:true,options:opts15('muito ruim','excelente'),help:help||''};});}
function weightField(id,crit){return {id:id,label:'Peso que você dá a “'+crit+'” na sua decisão',type:'radio',required:true,options:opts15('pouco importante','decisivo')};}
function nv(s,id,def){var x=Number(s.t(id));return (isFinite(x)&&x>0)?x:def;}
function tag(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';}
function scoresMetrics(c,k){return MODELS.map(function(m){return {label:m[1],value:F.num(c.s[m[0]][k],1)+' / 5',tag:k==='c'?'calculado':'informado'};});}
ZA.register({
id:'B07', code:'ZAR-B07', collection:'Terrenos',
title:'Qual Hospedagem Construir no Meu Terreno?',
subtitle:'Cabana, Glamping, Chalé ou Pousada?',
tool:'Comparador de Modelos de Hospedagem',
deliverable:'Matriz Comparativa de Modelos',
nameField:'nome', propertyField:'propriedade',
disclaimer:'A matriz organiza as suas próprias avaliações e pesos: o resultado reflete as notas que você deu, não uma recomendação técnica definitiva. Antes de decidir, confirme com a prefeitura e o órgão ambiental o que é permitido no terreno, e consulte arquiteto ou engenheiro sobre a implantação. Nenhum modelo garante demanda, faturamento ou retorno.',

intro:[
 {kind:'mirror', title:'Você pode estar escolhendo o empreendimento errado para o seu terreno.',
  lead:'Você viu um glamping lindo nas redes, um amigo disse que pousada dá mais dinheiro, o fornecedor de cabanas garantiu que é o melhor negócio. Cada conversa puxa para um lado, e a decisão continua parada.',
  body:'<div class="za-card"><p>Talvez você esteja vivendo uma destas situações:</p><ul><li>“Gosto de glamping, mas não sei se combina com o meu terreno.”</li><li>“Não sei se o meu orçamento dá para uma pousada.”</li><li>“Tenho medo de escolher um modelo que eu não consiga operar.”</li><li>“Cada pessoa me indica uma coisa diferente.”</li></ul></div>'},
 {kind:'collapse', title:'O modelo mais bonito ou mais popular não é necessariamente o mais adequado para o seu terreno e o seu orçamento.',
  lead:'O modelo certo é o que equilibra o que o terreno permite, o que o seu público procura, o que você consegue construir e o que você consegue operar.',
  body:'<div class="za-card"><p>Neste percurso você vai comparar <b>quatro modelos</b> (cabana, glamping, chalé e pousada) em <b>seis critérios</b>:</p><ol><li>Adequação ao terreno</li><li>Aderência ao público</li><li>Atratividade e diferenciação</li><li>Infraestrutura exigida</li><li>Custo em relação ao orçamento</li><li>Facilidade de operação</li></ol><p>Você dá as notas e decide o <b>peso</b> de cada critério. A ferramenta monta a matriz ponderada e mostra qual modelo combina mais com as suas prioridades.</p></div>'},
 {kind:'start', title:'Vamos comparar os modelos com os seus critérios',
  lead:'Em 7 pilares, você avalia cada modelo, define o que mais importa para você e sai com uma matriz comparativa preenchida.',
  body:'<p>Não existe nota certa ou errada: use o que você sabe hoje. Onde tiver dúvida, dê a nota mais honesta possível e anote o que precisa confirmar. Se puder, tenha à mão fotos e informações do terreno e uma ideia do valor que pode investir.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Paulo'},
   {id:'propriedade',label:'Nome da propriedade ou do projeto',type:'text',required:true,placeholder:'Ex.: Sítio Águas Claras'},
   {id:'municipio',label:'Município / região',type:'text',required:true,placeholder:'Ex.: Chapada dos Guimarães (MT)'},
   {id:'area_ha',label:'Área aproximada do terreno',type:'number',required:true,min:0.01,max:100000,step:0.01,unit:'hectares'}
  ]}
],

pillars:[
/* 1 */
{title:'Características do terreno', screens:[
 {kind:'learn', title:'O terreno conversa com o modelo',
  body:'<p>Cada modelo de hospedagem tem exigências físicas diferentes. Pense em:</p><ul><li><b>Relevo:</b> terrenos inclinados podem favorecer estruturas elevadas ou leves; construções maiores tendem a exigir mais movimentação de terra.</li><li><b>Vegetação e áreas protegidas:</b> podem limitar onde e quanto se pode construir. Isso deve ser verificado com o órgão ambiental.</li><li><b>Clima:</b> frio intenso, calor ou chuva frequente mudam o conforto de tendas, cabanas e chalés.</li><li><b>Espaço e privacidade:</b> unidades espalhadas exigem mais área e caminhos; uma pousada concentra a estrutura.</li></ul><p>Nesta etapa, dê uma nota de 1 a 5 para o quanto cada modelo <b>se encaixa no seu terreno</b>.</p>',
  example:'Exemplo ilustrativo: num terreno com encosta e mata, um proprietário deu nota 5 para glamping (estruturas leves, pouca terraplanagem) e 2 para pousada (prédio maior, mais movimentação de terra). Ele registrou a dúvida sobre área protegida para confirmar com o órgão ambiental.'},
 {kind:'compare', title:'Olhar para o terreno × olhar só para a foto',
  cols:[{h:'Escolha pela foto',type:'bad',items:['“Vi um domo lindo, quero igual”','Ignorar o clima da região','Não saber se há área de preservação','Esquecer que unidades espalhadas exigem caminhos e redes']},
        {h:'Escolha pelo terreno',type:'good',items:['Caminhar o terreno e marcar áreas possíveis','Considerar relevo, sol, vento e chuva','Verificar restrições ambientais e de uso com quem tem competência','Pensar no deslocamento do hóspede e da equipe']}]},
 {kind:'form', title:'Como cada modelo se encaixa no seu terreno', intro:'Descreva o terreno e dê uma nota de adequação para cada modelo.',
  fields:[
   {id:'relevo',label:'Relevo predominante',type:'radio',required:true,options:[{v:'plano',l:'Plano'},{v:'ondulado',l:'Ondulado'},{v:'ingreme',l:'Íngreme / encosta'}]},
   {id:'clima',label:'Clima mais marcante',type:'radio',required:true,options:[{v:'frio',l:'Frio / serra'},{v:'quente',l:'Quente'},{v:'chuvoso',l:'Chuvoso / úmido'},{v:'ameno',l:'Ameno'}]},
   {id:'restricao_amb',label:'Há área de preservação, nascente ou mata a respeitar?',type:'radio',required:true,options:[{v:'sim',l:'Sim'},{v:'nao',l:'Não'},{v:'naosei',l:'Não sei'}]}
  ].concat(scaleFields('t','adequação ao terreno')).concat([weightField('peso_t','Adequação ao terreno')])},
 {kind:'feedback', title:'O que o seu terreno indica',
  metrics:function(s,c){return scoresMetrics(c,'t');},
  feedback:function(s,c){var o=[],b=c.melhorCrit.t;
   o.push({lv:'info',t:'Pela sua avaliação, o modelo que mais se encaixa no terreno é <b>'+b.map(nm).join(' / ')+'</b>.'});
   if(s.t('restricao_amb')==='sim') o.push({lv:'warn',t:'Há áreas a respeitar. Antes de definir o modelo, confirme com o órgão ambiental e um profissional habilitado onde e quanto é possível construir.'});
   if(s.t('restricao_amb')==='naosei') o.push({lv:'warn',t:'Você não sabe se há restrições ambientais. Isso pode mudar a nota de todos os modelos: verifique com o órgão ambiental do município ou estado.'});
   if(s.t('relevo')==='ingreme'&&c.s.pou.t>=4) o.push({lv:'warn',t:'Terreno íngreme e nota alta para pousada: confirme com engenheiro o custo de terraplanagem e fundação para uma construção maior.'});
   if(c.w.t>=4) o.push({lv:'info',t:'Você deu peso alto ao terreno ('+F.num(c.w.t)+'/5): ele vai pesar bastante na matriz final.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Caminhar o terreno e marcar no mapa as áreas possíveis para as unidades'},{id:'a1_2',text:'Consultar o órgão ambiental sobre áreas de preservação e restrições'},{id:'a1_3',text:'Registrar relevo, insolação e acesso com fotos para mostrar a um arquiteto'}]}
]},
/* 2 */
{title:'Público turístico', screens:[
 {kind:'learn', title:'Quem vem ao seu destino e o que essa pessoa procura',
  body:'<p>O mesmo destino recebe públicos diferentes: casais buscando romance e privacidade, famílias que precisam de espaço, grupos de amigos, aventureiros, pessoas em busca de descanso. Cada público tem afinidade maior com certos modelos:</p><ul><li>Privacidade e experiência diferente tendem a combinar com cabanas e glamping.</li><li>Famílias e estadias longas costumam pedir espaço e cozinha.</li><li>Quem quer serviço (café da manhã, recepção) pode preferir pousada.</li></ul><p>Essas são tendências gerais, não regras. O que vale é o que <b>você observa</b> no seu destino: quem se hospeda nos concorrentes, o que é elogiado nas avaliações, o que falta.</p>',
  example:'Exemplo ilustrativo: num destino onde os anúncios mais bem avaliados são para casais, um proprietário deu nota 5 para cabana e glamping no critério público e 3 para pousada.'},
 {kind:'compare', title:'Público imaginado × público observado',
  cols:[{h:'Imaginado',type:'bad',items:['“Todo mundo vai gostar”','Escolher o modelo pelo gosto pessoal','Não olhar quem já visita o destino']},
        {h:'Observado',type:'good',items:['Ler avaliações de hospedagens da região','Ver qual perfil de hóspede aparece nas fotos e comentários','Perguntar a guias, restaurantes e secretaria de turismo quem visita o destino']}]},
 {kind:'form', title:'Qual modelo conversa com o seu público',
  fields:[
   {id:'publico',label:'Público principal que você pretende atender',type:'radio',required:true,options:[{v:'casais',l:'Casais'},{v:'familias',l:'Famílias'},{v:'grupos',l:'Grupos de amigos'},{v:'aventura',l:'Aventura / ecoturismo'},{v:'corporativo',l:'Corporativo / eventos'}]},
   {id:'fonte_publico',label:'Como você conhece esse público?',type:'radio',required:true,options:[{v:'pesquisa',l:'Pesquisei avaliações e concorrentes'},{v:'conversa',l:'Conversei com quem trabalha no destino'},{v:'suposicao',l:'É minha suposição'}]}
  ].concat(scaleFields('p','aderência ao público')).concat([weightField('peso_p','Aderência ao público')])},
 {kind:'feedback', title:'Público e modelo',
  metrics:function(s,c){return scoresMetrics(c,'p');},
  feedback:function(s,c){var o=[];
   o.push({lv:'info',t:'Para o público escolhido, sua melhor nota foi para <b>'+c.melhorCrit.p.map(nm).join(' / ')+'</b>.'});
   if(s.t('fonte_publico')==='suposicao') o.push({lv:'warn',t:'O público é uma suposição. Antes de investir, leia avaliações de 5 a 10 hospedagens do destino e confirme quem realmente se hospeda ali.'});
   else o.push({lv:'ok',t:'Seu público tem alguma base de observação. Registre as fontes para usar na apresentação do projeto.'});
   if(s.t('publico')==='corporativo'&&c.s.pou.p<3) o.push({lv:'info',t:'Público corporativo costuma precisar de estrutura coletiva (salas, refeições). Confira se a nota da pousada reflete isso.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Ler avaliações de 10 hospedagens do destino e anotar o perfil dos hóspedes'},{id:'a2_2',text:'Conversar com 3 pessoas do trade local (guias, restaurantes, secretaria de turismo)'},{id:'a2_3',text:'Descrever em uma frase o hóspede ideal do projeto'}]}
]},
/* 3 */
{title:'Modelos disponíveis', screens:[
 {kind:'learn', title:'Conheça os quatro modelos antes de dar nota',
  body:'<ul><li><b>Cabana:</b> unidade independente, geralmente de madeira ou sistema construtivo industrializado, com privacidade e apelo de natureza.</li><li><b>Glamping:</b> estrutura leve (tenda, domo, bolha) com conforto de hotel. Costuma ter apelo visual forte; o conforto térmico e a durabilidade dependem muito do projeto e do clima.</li><li><b>Chalé:</b> unidade independente em alvenaria ou estrutura mista, normalmente mais robusta e com mais área.</li><li><b>Pousada:</b> várias acomodações numa estrutura com áreas comuns e, frequentemente, serviços como café da manhã e recepção.</li></ul><p>Neste pilar, a nota é sobre <b>atratividade e diferenciação</b>: quanto cada modelo, no seu destino, se destacaria diante do que já existe.</p>',
  example:'Exemplo ilustrativo: num destino com muitas pousadas tradicionais e nenhum glamping, um proprietário deu nota 5 para glamping em diferenciação e 2 para pousada. Num destino cheio de domos, a lógica poderia ser a inversa.'},
 {kind:'compare', title:'Diferenciação real × moda passageira',
  cols:[{h:'Moda',type:'bad',items:['Repetir o modelo que está em alta nas redes','Escolher pelo que o fornecedor vende','Não olhar o que os concorrentes já oferecem']},
        {h:'Diferenciação',type:'good',items:['Contar quantos concorrentes oferecem cada modelo','Combinar o modelo com um atrativo do terreno (vista, rio, mata)','Pensar se a proposta continua interessante daqui a alguns anos']}]},
 {kind:'form', title:'Atratividade de cada modelo no seu destino',
  fields:[
   {id:'conc_destino',label:'Qual modelo é mais comum entre os concorrentes do destino?',type:'radio',required:true,options:MODELS.map(function(m){return {v:m[0],l:m[1]};}).concat([{v:'naosei',l:'Não sei'}])}
  ].concat(scaleFields('a','atratividade e diferenciação')).concat([weightField('peso_a','Atratividade e diferenciação')])},
 {kind:'feedback', title:'Onde está a diferenciação',
  metrics:function(s,c){return scoresMetrics(c,'a');},
  feedback:function(s,c){var o=[],cd=s.t('conc_destino');
   o.push({lv:'info',t:'O modelo mais atrativo na sua avaliação é <b>'+c.melhorCrit.a.map(nm).join(' / ')+'</b>.'});
   if(cd==='naosei') o.push({lv:'warn',t:'Você não sabe qual modelo predomina no destino. Pesquise os anúncios da região: a diferenciação depende do que já existe.'});
   else if(c.s[cd]&&c.s[cd].a>=4) o.push({lv:'warn',t:'Você deu nota alta de diferenciação para <b>'+nm(cd)+'</b>, que é justamente o modelo mais comum no destino. Revise: o que faria o seu se destacar?'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Mapear os concorrentes do destino por modelo de hospedagem'},{id:'a3_2',text:'Listar o atrativo do terreno que cada modelo valorizaria'},{id:'a3_3',text:'Visitar ou se hospedar em pelo menos um exemplo do modelo favorito'}]}
]},
/* 4 */
{title:'Infraestrutura', screens:[
 {kind:'learn', title:'Cada modelo pede uma infraestrutura diferente',
  body:'<p>Todos os modelos precisam de acesso, água, energia e solução de esgoto. O que muda é o <b>quanto</b> e o <b>onde</b>:</p><ul><li>Unidades espalhadas (cabanas, chalés, glamping) exigem redes e caminhos até cada uma.</li><li>Uma pousada concentra redes, mas exige estrutura maior num ponto e, em geral, cozinha e áreas comuns.</li><li>Estruturas leves podem exigir menos fundação, mas precisam de banheiro, energia e conforto térmico resolvidos.</li></ul><p>Aqui a nota é: <b>quanto cada modelo cabe na infraestrutura que você tem ou consegue fazer</b>. 5 = exige pouco além do que existe; 1 = exige muita infraestrutura nova.</p>',
  example:'Exemplo ilustrativo: num terreno sem rede elétrica próxima, um proprietário deu nota 2 para pousada (cozinha, lavanderia e muitos quartos consomem bastante energia) e 3 para cabanas.'},
 {kind:'compare', title:'Infraestrutura esquecida × infraestrutura planejada',
  cols:[{h:'Esquecida',type:'bad',items:['Escolher o modelo e só depois pensar em água e esgoto','Supor que estruturas leves não precisam de infraestrutura','Não considerar caminhos até unidades distantes']},
        {h:'Planejada',type:'good',items:['Listar o que existe no terreno','Pedir a um profissional a estimativa de redes para cada modelo','Considerar a distância entre unidades e pontos de água e energia']}]},
 {kind:'form', title:'Infraestrutura que cada modelo exige',
  fields:[
   {id:'infra_tem',label:'O terreno já tem:',type:'checks',options:[{v:'acesso',l:'Acesso transitável'},{v:'energia',l:'Energia elétrica'},{v:'agua',l:'Água suficiente'},{v:'esgoto',l:'Solução de esgoto'},{v:'internet',l:'Internet / sinal'}]}
  ].concat(scaleFields('i','cabe na infraestrutura possível','5 = exige pouco além do que existe; 1 = exige muita infraestrutura nova.')).concat([weightField('peso_i','Infraestrutura exigida')])},
 {kind:'feedback', title:'Infraestrutura e modelo',
  metrics:function(s,c){return scoresMetrics(c,'i');},
  feedback:function(s,c){var o=[],t=s.v.infra_tem||[];
   o.push({lv:'info',t:'O modelo mais compatível com a infraestrutura possível é <b>'+c.melhorCrit.i.map(nm).join(' / ')+'</b>.'});
   if(t.length<=2) o.push({lv:'warn',t:'O terreno tem '+t.length+' de 5 itens básicos de infraestrutura. O custo de infraestrutura pode pesar mais do que a diferença entre modelos: veja o B06 para orçar esse bloco.'});
   else o.push({lv:'ok',t:'O terreno já tem '+t.length+' de 5 itens básicos. Isso amplia as opções de modelo.'});
   if(t.indexOf('esgoto')<0) o.push({lv:'warn',t:'Sem solução de esgoto definida. Consulte um profissional habilitado sobre a solução adequada ao terreno e ao número de hóspedes.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Pedir à concessionária a viabilidade de ligação de energia'},{id:'a4_2',text:'Consultar profissional sobre água e esgoto para cada modelo'},{id:'a4_3',text:'Desenhar um croqui com a posição das unidades e das redes'}]}
]},
/* 5 */
{title:'Custos', screens:[
 {kind:'learn', title:'Custo: a nota que vem das suas cotações',
  body:'<p>Neste critério, a nota não é sua: ela é <b>calculada</b> a partir do custo estimado de implantação de cada modelo (o projeto completo, com o número de unidades que você imagina) e do seu orçamento.</p><div class="za-card"><b>Nota de custo = 5 × (custo do modelo mais barato ÷ custo do modelo)</b>, limitada entre 1 e 5. Se o custo passar do orçamento disponível, a nota perde 1 ponto (mínimo 1). Se você não souber o custo de um modelo, ele recebe nota 3 como hipótese neutra.</div><p>Use valores de cotações ou estudos (o B06 ajuda a montar esse número). A ferramenta não fornece preços de mercado.</p>',
  example:'Exemplo ilustrativo: glamping R$ 250.000, cabanas R$ 400.000, orçamento R$ 450.000. Glamping recebe 5; cabanas recebem 5 × 250/400 = 3,1. Uma pousada de R$ 1.200.000 receberia 1,0 e, por passar do orçamento, ficaria no mínimo (1).'},
 {kind:'compare', title:'Comparar preço × comparar custo total',
  cols:[{h:'Preço solto',type:'bad',items:['Comparar o preço de uma tenda com o de um chalé','Ignorar infraestrutura e mobiliário','Comparar quantidades diferentes de unidades']},
        {h:'Custo total comparável',type:'good',items:['Projeto completo de cada modelo, com a mesma capacidade aproximada','Infraestrutura, mobiliário e projetos incluídos','Valores de cotações, com data']}]},
 {kind:'form', title:'Custo estimado de cada modelo', intro:'Informe o custo total estimado de implantação de cada modelo, com capacidade parecida.',
  fields:MODELS.map(function(m){return {id:'custo_'+m[0],label:'Custo total estimado: '+m[1],type:'money',required:true,min:1,allowUnknown:true};}).concat([
   {id:'orcamento',label:'Orçamento disponível para implantação',type:'money',required:true,min:1,allowUnknown:true},
   weightField('peso_c','Custo × orçamento')])},
 {kind:'feedback', title:'Notas de custo calculadas',
  metrics:function(s,c){return scoresMetrics(c,'c');},
  feedback:function(s,c){var o=[];
   if(c.semCusto.length) o.push({lv:'warn',t:'Sem custo para: '+c.semCusto.map(nm).join(', ')+'. Esses modelos receberam nota 3 (hipótese neutra). Busque estimativas para comparar de verdade.'});
   if(c.acimaOrc.length) o.push({lv:'bad',t:'Acima do orçamento: <b>'+c.acimaOrc.map(nm).join(', ')+'</b>. Esses modelos perderam 1 ponto. Para viabilizá-los seria preciso reduzir o projeto, implantar por etapas ou buscar parceria.'});
   if(!s.has('orcamento')) o.push({lv:'warn',t:'Orçamento não informado: não foi possível verificar quais modelos cabem no seu bolso.'});
   if(c.maisBarato) o.push({lv:'info',t:'Modelo de menor custo informado: <b>'+nm(c.maisBarato)+'</b> ('+F.brl(c.custo[c.maisBarato])+').'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Pedir cotações de implantação completa para os 2 modelos mais bem avaliados'},{id:'a5_2',text:'Comparar os custos com a mesma capacidade de hóspedes'},{id:'a5_3',text:'Definir o orçamento máximo que você aceita investir'}]}
]},
/* 6 */
{title:'Operação', screens:[
 {kind:'learn', title:'Construir é uma vez; operar é todo dia',
  body:'<p>Cada modelo tem uma rotina diferente:</p><ul><li><b>Unidades independentes</b> (cabana, chalé, glamping) podem funcionar com autoatendimento, mas exigem deslocamento para limpeza e manutenção.</li><li><b>Glamping</b> pode pedir manutenção mais frequente de lonas, estruturas e climatização, dependendo do material e do clima.</li><li><b>Pousada</b> geralmente exige equipe maior, recepção, café da manhã e gestão de serviços.</li></ul><p>A nota aqui é: <b>quão fácil seria para você operar esse modelo</b>, com o tempo, a equipe e a experiência que você tem.</p>',
  example:'Exemplo ilustrativo: um proprietário que mora longe e não quer equipe fixa deu nota 4 para cabanas (check-in autônomo) e 1 para pousada (exige equipe diária).'},
 {kind:'compare', title:'Operação ignorada × operação planejada',
  cols:[{h:'Ignorada',type:'bad',items:['Escolher o modelo sem pensar em quem vai limpar e atender','Supor que “depois contrata alguém”','Não considerar a distância entre sua casa e o terreno']},
        {h:'Planejada',type:'good',items:['Definir quem faz limpeza, manutenção e atendimento','Estimar a equipe mínima de cada modelo','Escolher um modelo compatível com seu tempo disponível']}]},
 {kind:'form', title:'Facilidade de operação',
  fields:[
   {id:'dedicacao',label:'Quanto tempo você poderá dedicar à operação?',type:'radio',required:true,options:[{v:'integral',l:'Tempo integral'},{v:'parcial',l:'Meio período'},{v:'pouco',l:'Pouco tempo (quero equipe ou gestão terceirizada)'}]},
   {id:'experiencia',label:'Você já trabalhou com hospedagem?',type:'radio',required:true,options:[{v:'sim',l:'Sim'},{v:'nao',l:'Não'}]}
  ].concat(scaleFields('o','facilidade de operação')).concat([weightField('peso_o','Facilidade de operação')])},
 {kind:'feedback', title:'Operação e modelo',
  metrics:function(s,c){return scoresMetrics(c,'o');},
  feedback:function(s,c){var o=[];
   o.push({lv:'info',t:'O modelo que você considera mais fácil de operar é <b>'+c.melhorCrit.o.map(nm).join(' / ')+'</b>.'});
   if(s.t('dedicacao')==='pouco'&&c.s.pou.o>=4) o.push({lv:'warn',t:'Você terá pouco tempo, mas deu nota alta de operação para pousada. Pousadas costumam exigir gestão diária: confira se a nota está realista.'});
   if(s.t('experiencia')==='nao') o.push({lv:'info',t:'Sem experiência em hospedagem, modelos com menos serviços tendem a ser mais simples para começar. Considere também se hospedar em empreendimentos parecidos para conhecer a rotina.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Escrever a rotina de um dia de operação do modelo favorito'},{id:'a6_2',text:'Estimar a equipe mínima e quem fará cada tarefa'},{id:'a6_3',text:'Conversar com um operador de hospedagem parecida sobre a rotina'}]}
]},
/* 7 */
{title:'Matriz de escolha', screens:[
 {kind:'learn', title:'Como a matriz ponderada decide',
  body:'<p>Cada modelo recebeu uma nota de 1 a 5 em seis critérios, e cada critério recebeu um peso de 1 a 5 dado por você. A nota final é a <b>média ponderada</b>:</p><div class="za-card"><b>Nota final = Σ (nota × peso) ÷ Σ pesos</b></div><p>A matriz também faz um <b>teste de sensibilidade</b>: recalcula com todos os pesos iguais. Se o vencedor muda, a decisão depende muito dos pesos e merece mais reflexão. E compara o resultado com o modelo que você prefere “de coração”: quando os dois coincidem, ótimo; quando divergem, vale entender por quê.</p><p>Modelos que você souber que não são permitidos no terreno podem ser excluídos.</p>',
  example:'Exemplo ilustrativo: pesos 5, 4, 3, 3, 4 e 2 (soma 21). Um modelo com notas 5, 5, 5, 3, 5 e 3 soma 95 pontos ponderados: 95 ÷ 21 = 4,52.'},
 {kind:'compare', title:'Decisão por impulso × decisão estruturada',
  cols:[{h:'Impulso',type:'bad',items:['Escolher pelo modelo da moda','Deixar um único critério decidir tudo','Ignorar o que não é permitido no terreno']},
        {h:'Estruturada',type:'good',items:['Notas e pesos registrados por escrito','Teste de sensibilidade dos pesos','Confirmação técnica e legal antes de investir']}]},
 {kind:'form', title:'Ajustes finais da matriz',
  fields:[
   {id:'preferido',label:'Qual modelo você escolheria “de coração”, antes desta análise?',type:'select',required:true,options:MODELS.map(function(m){return {v:m[0],l:m[1]};})},
   {id:'excluidos',label:'Algum modelo já está descartado por restrição legal, ambiental ou do terreno?',type:'checks',options:MODELS.map(function(m){return {v:m[0],l:m[1]};}),help:'Marque apenas se a restrição foi confirmada por quem tem competência.'}
  ]},
 {kind:'feedback', title:'O resultado da sua matriz',
  metrics:function(s,c){return c.ranking.map(function(r,i){return {label:(i+1)+'º '+nm(r.k),value:F.num(r.total,2)+' / 5',tag:'calculado'};});},
  feedback:function(s,c){var o=[];
   if(!c.vencedor){o.push({lv:'bad',t:'Todos os modelos foram excluídos. Revise as exclusões.'});return o;}
   o.push({lv:'ok',t:'Pela sua matriz, o modelo mais adequado é <b>'+nm(c.vencedor)+'</b>, com '+F.num(c.score[c.vencedor],2)+' de 5.'});
   if(c.vantagem!=null&&c.vantagem<0.25) o.push({lv:'warn',t:'A diferença para o 2º colocado ('+nm(c.ranking[1].k)+') é de apenas '+F.num(c.vantagem,2)+' ponto. Os dois são opções próximas: aprofunde custos e restrições antes de decidir.'});
   if(c.vencedorSemPeso!==c.vencedor) o.push({lv:'warn',t:'Com todos os pesos iguais, o vencedor seria <b>'+nm(c.vencedorSemPeso)+'</b>. A decisão depende bastante dos pesos que você escolheu: revise se eles refletem suas prioridades reais.'});
   else o.push({lv:'ok',t:'Teste de sensibilidade: com pesos iguais, o vencedor continua o mesmo.'});
   if(s.t('preferido')&&s.t('preferido')!==c.vencedor) o.push({lv:'info',t:'Seu modelo “de coração” é <b>'+nm(s.t('preferido'))+'</b>, mas a matriz indica <b>'+nm(c.vencedor)+'</b>. Veja no relatório em quais critérios ele perde.'});
   if(c.acimaOrc.indexOf(c.vencedor)>=0) o.push({lv:'bad',t:'O modelo vencedor está acima do orçamento informado. Avalie implantação por etapas ou parceria.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Validar o modelo vencedor com arquiteto ou engenheiro'},{id:'a7_2',text:'Confirmar com a prefeitura se o modelo é permitido no terreno'},{id:'a7_3',text:'Orçar em detalhe o modelo vencedor (use o B06)'}]}
]}
],

compute:function(s){
 var c={s:{},custo:{},score:{},scoreIgual:{}};
 MODELS.forEach(function(m){var k=m[0];c.s[k]={};
  ['t','p','a','i','o'].forEach(function(cr){c.s[k][cr]=ZA.clamp(nv(s,cr+'_'+k,3),1,5);});
  c.custo[k]=s.has('custo_'+k)&&s.n('custo_'+k)>0?s.n('custo_'+k):null;});
 var known=MODELS.map(function(m){return c.custo[m[0]];}).filter(function(x){return x!=null;});
 var minC=known.length?Math.min.apply(null,known):null;
 c.orc=s.has('orcamento')?s.n('orcamento'):null;
 c.semCusto=[]; c.acimaOrc=[]; c.maisBarato=null;
 MODELS.forEach(function(m){var k=m[0],v=c.custo[k];
  if(v==null){c.s[k].c=3;c.semCusto.push(k);return;}
  var sc=ZA.clamp(5*minC/v,1,5);
  if(c.orc!=null&&v>c.orc){sc=Math.max(1,sc-1);c.acimaOrc.push(k);}
  c.s[k].c=sc; if(v===minC&&!c.maisBarato) c.maisBarato=k;});
 c.w={}; var W=0;
 CRIT.forEach(function(cr){var w=ZA.clamp(nv(s,'peso_'+cr[0],3),1,5);c.w[cr[0]]=w;W+=w;}); c.W=W;
 var exc=s.v.excluidos||[]; c.excluidos=exc;
 MODELS.forEach(function(m){var k=m[0],t=0,u=0;
  CRIT.forEach(function(cr){t+=c.w[cr[0]]*c.s[k][cr[0]];u+=c.s[k][cr[0]];});
  c.score[k]=t/W; c.scoreIgual[k]=u/CRIT.length; c.score[k+'_pct']=c.score[k]/5*100;});
 var ativos=MODELS.map(function(m){return m[0];}).filter(function(k){return exc.indexOf(k)<0;});
 c.ranking=ativos.map(function(k){return {k:k,total:c.score[k]};}).sort(function(a,b){return b.total-a.total;});
 c.vencedor=c.ranking.length?c.ranking[0].k:null;
 c.vantagem=c.ranking.length>1?c.ranking[0].total-c.ranking[1].total:null;
 var r2=ativos.slice().sort(function(a,b){return c.scoreIgual[b]-c.scoreIgual[a];}); c.vencedorSemPeso=r2[0]||null;
 c.melhorCrit={};
 CRIT.forEach(function(cr){var mx=Math.max.apply(null,MODELS.map(function(m){return c.s[m[0]][cr[0]];}));c.melhorCrit[cr[0]]=MODELS.filter(function(m){return c.s[m[0]][cr[0]]===mx;}).map(function(m){return m[0];});});
 // critérios em que o vencedor perde para o preferido
 var pf=s.t('preferido'); c.preferido=pf||null;
 c.perdas=[]; if(c.vencedor&&pf&&pf!==c.vencedor){CRIT.forEach(function(cr){var d=c.s[c.vencedor][cr[0]]-c.s[pf][cr[0]]; if(d>0) c.perdas.push({crit:cr[1],dif:d,peso:c.w[cr[0]]});});}
 c.pesoMax=CRIT.slice().sort(function(a,b){return c.w[b[0]]-c.w[a[0]];})[0][1];
 c.vencScore=c.vencedor?c.score[c.vencedor]:null;
 return c;
},

metrics:function(s,c){var m=[
 {label:'Modelo indicado pela matriz',value:c.vencedor?nm(c.vencedor):'—',tag:'calculado'},
 {label:'Nota ponderada do vencedor',value:c.vencScore==null?'—':F.num(c.vencScore,2)+' / 5',tag:'calculado'},
 {label:'Vantagem sobre o 2º',value:c.vantagem==null?'—':F.num(c.vantagem,2)+' ponto',tag:'calculado'},
 {label:'Vencedor com pesos iguais',value:c.vencedorSemPeso?nm(c.vencedorSemPeso):'—',tag:'calculado'},
 {label:'Seu modelo “de coração”',value:c.preferido?nm(c.preferido):'—',tag:'informado'},
 {label:'Critério de maior peso',value:c.pesoMax,tag:'informado'},
 {label:'Orçamento disponível',value:c.orc==null?'—':F.brl(c.orc),tag:c.orc==null?'hipotese':'informado'}];
 return m;},

priorities:function(s,c){var L=[],v=c.vencedor;
 if(!v){L.push({title:'Rever os modelos excluídos',why:'Nenhum modelo restou na matriz.',score:10});return L;}
 if(c.acimaOrc.indexOf(v)>=0) L.push({title:'Ajustar o projeto de '+nm(v)+' ao orçamento ou planejar por etapas',why:'O modelo vencedor está acima do orçamento informado.',score:10});
 if(s.t('restricao_amb')!=='nao') L.push({title:'Confirmar restrições ambientais e de uso do solo com os órgãos competentes',why:'Restrições podem eliminar ou mudar modelos.',score:9});
 if(c.semCusto.indexOf(v)>=0) L.push({title:'Obter o custo de implantação de '+nm(v),why:'O vencedor recebeu nota de custo neutra por falta de dado.',score:9});
 if(c.vantagem!=null&&c.vantagem<0.25) L.push({title:'Aprofundar a comparação entre '+nm(v)+' e '+nm(c.ranking[1].k),why:'Diferença de apenas '+F.num(c.vantagem,2)+' ponto entre os dois.',score:8});
 if(c.vencedorSemPeso!==v) L.push({title:'Revisar os pesos dos critérios',why:'Com pesos iguais, o vencedor mudaria para '+nm(c.vencedorSemPeso)+'.',score:7});
 if(s.t('fonte_publico')==='suposicao') L.push({title:'Validar o público com avaliações e conversas no destino',why:'A nota de público está baseada em suposição.',score:7});
 if(c.orc==null) L.push({title:'Definir o orçamento máximo de implantação',why:'Sem ele, a nota de custo não considera o que cabe no bolso.',score:7});
 if(s.t('conc_destino')==='naosei') L.push({title:'Mapear os modelos oferecidos pelos concorrentes',why:'A nota de diferenciação depende do que já existe no destino.',score:6});
 if(c.preferido&&c.preferido!==v) L.push({title:'Entender por que '+nm(c.preferido)+' perde para '+nm(v),why:'Seu modelo preferido não foi o melhor na matriz.',score:5});
 if((s.v.infra_tem||[]).length<=2) L.push({title:'Orçar a infraestrutura básica do terreno',why:'Faltam vários itens básicos; o custo pode pesar mais que a escolha do modelo.',score:6});
 if(s.t('dedicacao')==='pouco') L.push({title:'Definir quem vai operar a hospedagem',why:'Você terá pouco tempo para a operação.',score:5});
 L.push({title:'Orçar em detalhe o modelo '+nm(v),why:'Próximo passo para transformar a escolha em projeto.',score:4});
 if(c.semCusto.length>1) L.push({title:'Completar os custos dos demais modelos',why:'Faltam custos para '+c.semCusto.map(nm).join(', ')+'.',score:3});
 return L;},

report:function(s,c){
 var inf=tag('informado'), cal=tag('calculado'), hip=tag('hipotese','hipótese');
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Área do terreno',F.num(s.n('area_ha'),2)+' ha',inf],
  ['Relevo / clima',esc(({plano:'Plano',ondulado:'Ondulado',ingreme:'Íngreme'})[s.t('relevo')]||'—')+' · '+esc(({frio:'frio',quente:'quente',chuvoso:'chuvoso',ameno:'ameno'})[s.t('clima')]||'—'),inf],
  ['Restrição ambiental',esc(({sim:'Sim',nao:'Não',naosei:'Não sabe'})[s.t('restricao_amb')]||'—'),s.t('restricao_amb')==='naosei'?hip:inf],
  ['Público principal',esc(({casais:'Casais',familias:'Famílias',grupos:'Grupos',aventura:'Aventura',corporativo:'Corporativo'})[s.t('publico')]||'—'),s.t('fonte_publico')==='suposicao'?hip:inf],
  ['Orçamento disponível',c.orc==null?'—':F.brl(c.orc),c.orc==null?hip:inf],
  ['Notas de custo','5 × menor custo ÷ custo do modelo (−1 se acima do orçamento)',cal],
  ['Modelos sem custo informado',c.semCusto.length?c.semCusto.map(nm).join(', ')+' (nota 3)':'nenhum',c.semCusto.length?hip:inf],
  ['Modelos excluídos',c.excluidos.length?c.excluidos.map(nm).join(', '):'nenhum',inf]],[]);
 var head=['Critério','Peso'].concat(MODELS.map(function(m){return m[1];}));
 var rows=CRIT.map(function(cr){return [cr[1]+(cr[0]==='c'?' '+cal:''),F.num(c.w[cr[0]])].concat(MODELS.map(function(m){return F.num(c.s[m[0]][cr[0]],1);}));});
 rows.push(['<b>Nota ponderada</b>','<b>Σ '+F.num(c.W)+'</b>'].concat(MODELS.map(function(m){var x=F.num(c.score[m[0]],2);return (m[0]===c.vencedor?'<b>'+x+' ★</b>':x)+(c.excluidos.indexOf(m[0])>=0?' (excluído)':'');})));
 rows.push(['Pesos iguais (sensibilidade)','—'].concat(MODELS.map(function(m){return F.num(c.scoreIgual[m[0]],2);})));
 var mat=ZA.table(head,rows,[1,2,3,4,5]);
 var custos=ZA.table(['Modelo','Custo estimado','Situação'],MODELS.map(function(m){var v=c.custo[m[0]];return [m[1],v==null?'—':F.brl(v),v==null?'sem dado (nota 3)':(c.acimaOrc.indexOf(m[0])>=0?'acima do orçamento':'dentro do orçamento'+(c.orc==null?' (não verificado)':''))];}),[1]);
 var rank=c.ranking.map(function(r,i){return '<li><b>'+nm(r.k)+'</b>: '+F.num(r.total,2)+' de 5 ('+F.pct(r.total/5*100,0)+')</li>';}).join('');
 var perdas=c.perdas.length?'<p>Em relação ao seu modelo preferido ('+esc(nm(c.preferido))+'), <b>'+esc(nm(c.vencedor))+'</b> tem nota maior em: '+c.perdas.map(function(p){return esc(p.crit)+' (+'+F.num(p.dif,1)+', peso '+p.peso+')';}).join('; ')+'.</p>':'';
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido de 30 dias</b><ol>'+
  '<li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Confirmar as restrições do terreno')+'.</li>'+
  '<li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Validar o público no destino')+'.</li>'+
  '<li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Orçar o modelo vencedor')+'.</li>'+
  '<li><b>Semana 4:</b> refazer a matriz com as informações confirmadas e levar o modelo escolhido para arquiteto ou engenheiro.</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Matriz comparativa ponderada',html:mat+'<p class="za-small">Notas de 1 a 5 dadas por você (exceto custo, calculado). Nota ponderada = Σ(nota × peso) ÷ Σ pesos.</p>'},
  {title:'Ranking',html:'<ol>'+rank+'</ol>'+(c.vencedorSemPeso!==c.vencedor?'<p class="za-missing">Sensibilidade: com pesos iguais, o vencedor seria '+esc(nm(c.vencedorSemPeso))+'. A escolha depende dos pesos.</p>':'<p class="za-small">Sensibilidade: com pesos iguais, o vencedor se mantém.</p>')+perdas},
  {title:'Custos considerados',html:custos}
 ],plan:plan};
}
});
})();
