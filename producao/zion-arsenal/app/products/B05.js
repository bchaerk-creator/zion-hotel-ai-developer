/* ZAR-B05 · Como Descobrir o Potencial Turístico da Minha Terra? · Raio-X do Potencial Turístico */
(function(){
var F=ZA.fmt, esc=ZA.esc;
function tag(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';}
function arr(s,id){var x=s.v[id];return (!s.unknown(id)&&Array.isArray(x))?x:[];}
function has(a,v){return a.indexOf(v)>=0;}
function esc5(lo,hi){return [1,2,3,4,5].map(function(k){return {v:String(k),l:k+(k===1?' · '+lo:k===5?' · '+hi:'')};});}
function sc(s,id,def){var x=Number(s.t(id));return (s.t(id)!==''&&isFinite(x))?x:def;}

var DIM=[{k:'loc',n:'Localização',w:15},{k:'atr',n:'Atrativos',w:25},{k:'ace',n:'Acesso',w:15},{k:'inf',n:'Infraestrutura',w:15},{k:'mer',n:'Mercado e demanda',w:20},{k:'res',n:'Restrições e pendências',w:10}];
var ATR=[{id:'at_paisagem',n:'Paisagem e vista'},{id:'at_agua',n:'Água (rio, cachoeira, lago)'},{id:'at_mata',n:'Mata, fauna e trilhas'},{id:'at_cultural',n:'Cultura, história ou produção rural'},{id:'at_exclusividade',n:'Exclusividade na região'}];
var INFRA=[{v:'energia',l:'Energia elétrica na área'},{v:'agua',l:'Água em quantidade (poço, nascente, rede)'},{v:'sinal',l:'Sinal de celular ou internet'},{v:'saneamento',l:'Solução de esgoto definida ou possível'},{v:'construcao',l:'Construção aproveitável'},{v:'plano',l:'Área plana para implantar unidades'}];
var RESTR=[{v:'app',l:'Área de preservação (margem de rio, nascente, encosta, topo de morro)',crit:false},{v:'reserva_legal',l:'Reserva legal ainda não definida ou não averbada',crit:false},{v:'uc',l:'Unidade de conservação no entorno',crit:false},{v:'doc',l:'Pendência documental (inventário, escritura, divisão)',crit:true},{v:'servidao',l:'Servidão (linha de transmissão, duto, passagem)',crit:false},{v:'risco',l:'Área sujeita a alagamento ou deslizamento',crit:true},{v:'vizinhanca',l:'Conflito de posse ou de vizinhança',crit:true}];
var CONS=[{v:'prefeitura',l:'Prefeitura (uso do solo, zoneamento)'},{v:'ambiental',l:'Órgão ambiental'},{v:'cartorio',l:'Cartório de Registro de Imóveis'},{v:'profissional',l:'Profissional habilitado (engenheiro, arquiteto ou advogado)'}];
var PESOS=[{id:'peso_loc',k:'loc'},{id:'peso_atr',k:'atr'},{id:'peso_ace',k:'ace'},{id:'peso_inf',k:'inf'},{id:'peso_mer',k:'mer'},{id:'peso_res',k:'res'}];
function classe(i){return i>=70?'Potencial alto (preliminar)':i>=50?'Potencial moderado':i>=30?'Potencial limitado':'Baixo potencial com os dados atuais';}

ZA.register({
id:'B05', code:'ZAR-B05', collection:'Terrenos',
title:'Como Descobrir o Potencial Turístico da Minha Terra?',
subtitle:'Avaliar as Possibilidades da Sua Propriedade',
tool:'Raio-X do Potencial Turístico',
deliverable:'Diagnóstico Orientativo do Potencial Turístico',
nameField:'nome', propertyField:'propriedade',
disclaimer:'O Raio-X é um diagnóstico orientativo baseado nas suas respostas e em uma ponderação da metodologia Zion. Ele não substitui estudo de mercado, laudo técnico, consulta ambiental ou parecer jurídico, e não garante demanda, aprovação de licenças nem retorno. Restrições ambientais, documentais e de uso do solo só podem ser confirmadas pelos órgãos competentes e por profissional habilitado (engenheiro, arquiteto ou advogado).',

intro:[
 {kind:'mirror', title:'Sua terra tem natureza e uma vista bonita. Mas isso é suficiente para um negócio?',
  lead:'Todo mundo que visita diz que daria uma pousada linda. Você também acha. Mas, quando pensa em investir, bate a dúvida: será que alguém viajaria até aqui e pagaria para ficar?',
  body:'<div class="za-card"><p>Talvez você se reconheça:</p><ul><li>“A vista é incrível, mas fica longe de tudo.”</li><li>“Tem cachoeira, mas a estrada é ruim na chuva.”</li><li>“Não sei se a região recebe turistas.”</li><li>“Não sei se posso construir perto do rio.”</li></ul></div>'},
 {kind:'collapse', title:'Beleza natural não é a mesma coisa que viabilidade turística.',
  lead:'Potencial turístico é a combinação de vários fatores: onde a terra está, o que ela oferece, como se chega, o que já existe, se há demanda e o que pode impedir o projeto.',
  body:'<div class="za-card"><p>O Raio-X avalia seis dimensões, cada uma de 0 a 100:</p><ol>'+DIM.map(function(d){return '<li><b>'+d.n+'</b> · peso '+d.w+'%</li>';}).join('')+'</ol><p>O índice final é a média ponderada. Uma dimensão muito fraca pode limitar o projeto mesmo com índice bom, e o diagnóstico mostra isso. No último pilar, você também testa o índice com <b>os seus próprios pesos</b>.</p></div>'},
 {kind:'start', title:'Vamos fazer o Raio-X do potencial da sua terra',
  lead:'Em 7 pilares, você avalia cada dimensão e sai com um diagnóstico orientativo e uma lista do que confirmar.',
  body:'<p>Se não souber um dado, marque “não sei”: ele reduz a confiança do diagnóstico e vira tarefa no seu plano.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Marta'},
   {id:'propriedade',label:'Nome da terra',type:'text',required:true,placeholder:'Ex.: Sítio Vale Verde'},
   {id:'cidade',label:'Município e estado',type:'text',required:true,placeholder:'Ex.: Itaipava (RJ)'},
   {id:'area_ha',label:'Área total',type:'number',required:true,min:0.05,max:100000,step:'any',unit:'hectares'},
   {id:'finalidade',label:'O que você imagina para a terra?',type:'radio',required:true,options:[{v:'hospedagem',l:'Hospedagem (cabanas, chalés, glamping, pousada)'},{v:'dayuse',l:'Day use e lazer'},{v:'eventos',l:'Eventos e retiros'},{v:'nao_sei',l:'Ainda não sei'}]}
  ]}
],

pillars:[
/* 1 */
{title:'Localização', screens:[
 {kind:'learn', title:'Localização: a que distância está o seu hóspede?',
  body:'<p>Para hospedagem de lazer, a localização é medida em <b>tempo de viagem</b> desde os centros de onde vêm os turistas (os “centros emissores”), não em quilômetros. Também pesam:</p><ul><li><b>O destino:</b> a região já é conhecida? Está surgindo? Ainda não recebe turistas?</li><li><b>A cidade de apoio:</b> mercado, posto, farmácia e mão de obra a uma distância razoável.</li></ul><div class="za-card"><b>Pontuação (metodologia Zion):</b> tempo ao centro emissor ≤2h 100 · ≤4h 70 · ≤6h 40 · mais 20. Destino consolidado 100 · emergente 65 · sem fluxo 25. Cidade de apoio ≤15 km 100 · ≤40 km 70 · mais 40. A nota é a média dos três.</div>',
  example:'Exemplo: 3 h do centro emissor (70), destino emergente (65) e cidade de apoio a 20 km (70): localização = (70 + 65 + 70) ÷ 3 = 68/100.'},
 {kind:'compare', title:'Longe × fora de mão',
  cols:[{h:'Longe, mas viável',items:['Destino conhecido que já atrai viagens longas','Hospedagem que é o próprio motivo da viagem','Estadias mais longas compensam o deslocamento']},
        {h:'Fora de mão',type:'bad',items:['Longe dos centros e fora de qualquer rota turística','Cidade de apoio distante (custo de operação alto)','Hóspede de fim de semana não aceita o tempo de viagem']}]},
 {kind:'form', title:'Onde fica a sua terra',
  fields:[
   {id:'tempo_emissor',label:'Tempo de viagem até o principal centro de onde viriam os turistas',type:'number',required:true,allowUnknown:true,min:0,max:48,step:'any',unit:'horas',help:'Ex.: capital ou cidade grande mais próxima. Use um aplicativo de mapas.'},
   {id:'destino',label:'Situação turística da região',type:'radio',required:true,options:[{v:'consolidado',l:'Destino consolidado (já muito procurado)'},{v:'emergente',l:'Destino emergente (algum fluxo, crescendo)'},{v:'sem',l:'Sem fluxo turístico relevante'}]},
   {id:'dist_apoio',label:'Distância até a cidade de apoio',type:'number',required:true,allowUnknown:true,min:0,max:500,step:'any',unit:'km'}
  ]},
 {kind:'feedback', title:'Leitura da localização',
  metrics:function(s,c){return [{label:'Localização',value:F.num(c.s.loc,0)+'/100',tag:'calculado'},{label:'Tempo ao centro emissor',value:s.unknown('tempo_emissor')?'—':F.num(s.n('tempo_emissor'),1)+' h',tag:'informado'}];},
  feedback:function(s,c){var o=[];var t=s.n('tempo_emissor');
   if(s.unknown('tempo_emissor')) o.push({lv:'warn',t:'Tempo até o centro emissor desconhecido: a localização foi pontuada sem ele. Meça no mapa: é um dos dados mais importantes do Raio-X.'});
   else if(t<=2) o.push({lv:'ok',t:'A até 2 horas de um centro emissor: perfil favorável a fins de semana e escapadas.'});
   else if(t>4) o.push({lv:'warn',t:'Mais de 4 horas de viagem: para fins de semana isso pesa. O projeto precisará de estadias mais longas ou de ser o próprio motivo da viagem.'});
   if(s.t('destino')==='sem') o.push({lv:'warn',t:'Região sem fluxo turístico: a demanda terá de ser criada. Isso não impede o projeto, mas aumenta o esforço comercial.'});
   if(s.unknown('dist_apoio')) o.push({lv:'warn',t:'Distância até a cidade de apoio desconhecida. Ela influencia custos de compras, manutenção e equipe.'});
   else if(s.n('dist_apoio')>40) o.push({lv:'info',t:'Cidade de apoio a mais de 40 km: considere no custo operacional as idas para compras, lavanderia e manutenção.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Medir no mapa o tempo de viagem a partir de 3 cidades de origem possíveis'},{id:'a1_2',text:'Listar os serviços disponíveis na cidade de apoio'},{id:'a1_3',text:'Verificar se a região aparece em roteiros turísticos ou guias locais'}]}
]},
/* 2 */
{title:'Atrativos', screens:[
 {kind:'learn', title:'Atrativos: o que faz alguém escolher a sua terra',
  body:'<p>Atrativo é aquilo que gera desejo de estar ali. O Raio-X avalia cinco tipos, de 1 a 5:</p><ul>'+ATR.map(function(a){return '<li><b>'+a.n+'</b></li>';}).join('')+'</ul><p>O último, <b>exclusividade</b>, é decisivo: um rio bonito numa região cheia de rios bonitos atrai menos do que um mirante único. Seja honesto e compare com outras propriedades da região.</p><div class="za-card"><b>Nota de atrativos = (média das cinco notas − 1) ÷ 4 × 100</b></div>',
  example:'Exemplo: notas 4, 5, 4, 2 e 3 têm média 3,6. Atrativos = (3,6 − 1) ÷ 4 × 100 = 65/100.'},
 {kind:'compare', title:'Atrativo de cartão-postal × atrativo de hospedagem',
  cols:[{h:'Só cartão-postal',items:['Bonito para uma foto rápida','Visitado em poucos minutos','Sem relação com a estadia']},
        {h:'Atrativo de hospedagem',type:'good',items:['Faz parte da experiência de ficar (banho de rio, nascer do sol, trilha)','Pode ser vivido várias vezes na estadia','Difícil de encontrar em outras propriedades']}]},
 {kind:'form', title:'Avalie os atrativos (1 a 5)', intro:'Compare com outras propriedades da região, não com fotos da internet.',
  fields:ATR.map(function(a){return {id:a.id,label:a.n,type:'radio',required:true,options:esc5('inexistente ou comum','forte e raro')};})},
 {kind:'feedback', title:'Força dos atrativos',
  metrics:function(s,c){return [{label:'Atrativos',value:F.num(c.s.atr,0)+'/100',tag:'calculado'},{label:'Atrativo mais forte',value:c.atrTop.n,tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:'info',t:'Seu atrativo mais forte é <b>'+c.atrTop.n+'</b> ('+c.atrTop.v+'/5). Ele deve estar no centro do conceito e das fotos.'});
   var ex=sc(s,'at_exclusividade',1); if(ex<=2) o.push({lv:'warn',t:'Exclusividade baixa: o que a sua terra oferece também existe em outras da região. A diferenciação terá de vir da experiência, do conforto ou do serviço.'});
   else if(ex>=4) o.push({lv:'ok',t:'Exclusividade alta: há algo raro na sua terra. Documente com boas fotos e confirme com visitantes de fora.'});
   if(c.s.atr<35) o.push({lv:'warn',t:'Atrativos fracos ('+F.num(c.s.atr,0)+'/100). Projetos assim dependem mais de localização e de conceito.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Pedir a 3 pessoas de fora da região que avaliem os atrativos'},{id:'a2_2',text:'Fotografar o atrativo principal em diferentes horários e estações'},{id:'a2_3',text:'Comparar com os atrativos de 3 hospedagens da região'}]}
]},
/* 3 */
{title:'Acesso', screens:[
 {kind:'learn', title:'Acesso: o hóspede precisa chegar, e o fornecedor também',
  body:'<p>Uma estrada ruim afeta tudo: avaliações, cancelamentos em dias de chuva, custo de obra (o caminhão também precisa chegar) e manutenção. O Raio-X combina três fatores:</p><div class="za-card"><b>Acesso = 50% tipo de via + 25% acesso em dia de chuva + 25% trecho de terra</b><br>Via: asfalto 100 · terra boa 70 · terra ruim 35 · sem acesso para carro comum 10. Chuva: sempre 100 · às vezes 50 · não 0. Trecho de terra: 0 km 100 · até 5 km 75 · até 15 km 50 · mais 25.</div>',
  example:'Exemplo: estrada de terra boa (70), às vezes complicada na chuva (50), com 8 km de terra (50): acesso = 35 + 12,5 + 12,5 = 60/100.'},
 {kind:'compare', title:'Acesso que afasta × acesso que funciona',
  cols:[{h:'Afasta',type:'bad',items:['Só chega de 4×4 em época de chuva','Sem sinalização, o GPS se perde','Hóspede descobre a estrada só na chegada']},
        {h:'Funciona',type:'good',items:['Trafegável o ano todo com carro comum','Indicação clara do caminho','Estrada descrita com honestidade no anúncio']}]},
 {kind:'form', title:'Como se chega até a sua terra',
  fields:[
   {id:'via',label:'Tipo de via até a entrada',type:'radio',required:true,options:[{v:'asfalto',l:'Asfalto até a entrada'},{v:'terra_boa',l:'Terra em bom estado'},{v:'terra_ruim',l:'Terra em mau estado'},{v:'sem',l:'Sem acesso para carro comum'}]},
   {id:'km_terra',label:'Trecho de estrada de terra até a área',type:'number',required:true,min:0,max:300,step:'any',unit:'km'},
   {id:'chuva',label:'Carro comum chega em dias de chuva?',type:'radio',required:true,options:[{v:'sim',l:'Sim, sempre'},{v:'as_vezes',l:'Às vezes'},{v:'nao',l:'Não'}]}
  ]},
 {kind:'feedback', title:'Leitura do acesso',
  metrics:function(s,c){return [{label:'Acesso',value:F.num(c.s.ace,0)+'/100',tag:'calculado'},{label:'Trecho de terra',value:F.num(s.n('km_terra'),1)+' km',tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(s.t('chuva')==='nao') o.push({lv:'bad',t:'Sem acesso em dias de chuva, a hospedagem fica sujeita a cancelamentos e avaliações ruins. Melhorar a estrada pode ser pré-requisito do projeto.'});
   else if(s.t('chuva')==='as_vezes') o.push({lv:'warn',t:'Acesso incerto na chuva. Levante com a prefeitura ou com vizinhos se há manutenção prevista, e quanto custaria melhorar os pontos críticos.'});
   if(s.t('via')==='sem') o.push({lv:'bad',t:'Sem acesso para carro comum, a obra e a operação ficam muito mais caras. Avalie isso antes de qualquer outra coisa.'});
   if(s.n('km_terra',0)>15) o.push({lv:'warn',t:'Mais de 15 km de terra pesam no tempo de viagem e na percepção do hóspede.'});
   if(c.s.ace>=75) o.push({lv:'ok',t:'Acesso favorável. Descreva-o com clareza no material de apresentação.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Percorrer o acesso em dia de chuva e anotar os pontos críticos'},{id:'a3_2',text:'Consultar a prefeitura sobre manutenção da estrada'},{id:'a3_3',text:'Verificar se caminhões de obra conseguem chegar à área'}]}
]},
/* 4 */
{title:'Infraestrutura', screens:[
 {kind:'learn', title:'Infraestrutura: o que já existe e o que precisa ser levado',
  body:'<p>Energia, água, sinal, esgoto e uma área plana para implantar: cada item que falta vira custo e prazo. Em áreas rurais, levar energia ou perfurar um poço pode ser uma parte relevante do investimento, e depende de autorização ou de projeto técnico.</p><div class="za-card"><b>Infraestrutura = itens presentes ÷ 6 × 100</b></div><p>Água e esgoto exigem atenção especial: captação de água e solução de esgoto costumam depender de outorga ou licença. Quem orienta é um engenheiro e o órgão ambiental.</p>',
  example:'Exemplo: energia, água, sinal e área plana presentes (4 de 6): infraestrutura = 67/100. Falta definir esgoto e não há construção aproveitável.'},
 {kind:'compare', title:'Infra que se resolve × infra que pode inviabilizar',
  cols:[{h:'Costuma se resolver com projeto',items:['Sinal de celular (antena, internet via satélite)','Energia a poucos metros da rede','Esgoto com solução individual aprovada']},
        {h:'Pode inviabilizar ou encarecer muito',type:'bad',items:['Rede de energia muito distante','Falta de água em quantidade suficiente','Área sem nenhum ponto plano ou estável']}]},
 {kind:'form', title:'O que existe na sua terra',
  fields:[
   {id:'infra',label:'Infraestrutura presente',type:'checks',options:INFRA},
   {id:'dist_rede',label:'Distância até a rede de energia mais próxima',type:'number',required:true,allowUnknown:true,min:0,max:200,step:'any',unit:'km',help:'Zero se já há energia na área.'}
  ]},
 {kind:'feedback', title:'Leitura da infraestrutura',
  metrics:function(s,c){return [{label:'Infraestrutura',value:F.num(c.s.inf,0)+'/100',tag:'calculado'},{label:'Itens presentes',value:c.nInf+' de 6',tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(c.infFalta.length) o.push({lv:c.nInf<=2?'warn':'info',t:'Itens a resolver: '+c.infFalta.map(function(x){return x.l.toLowerCase();}).join('; ')+'.'});
   else o.push({lv:'ok',t:'Todos os itens de infraestrutura presentes.'});
   if(!has(c.inf,'agua')) o.push({lv:'warn',t:'Sem água garantida em quantidade, não há hospedagem. Verifique com engenheiro a viabilidade de poço ou captação e a necessidade de outorga.'});
   if(!has(c.inf,'energia')){ if(s.unknown('dist_rede')) o.push({lv:'warn',t:'Sem energia na área e sem saber a distância da rede. Consulte a concessionária: esse custo pode ser decisivo.'});
     else if(s.n('dist_rede',0)>1) o.push({lv:'warn',t:'Rede de energia a '+F.num(s.n('dist_rede'),1)+' km. Peça à concessionária uma estimativa de custo e prazo de ligação.'});}
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Consultar a concessionária sobre ligação de energia'},{id:'a4_2',text:'Conversar com engenheiro sobre água e esgoto'},{id:'a4_3',text:'Marcar no mapa as áreas planas e estáveis'}]}
]},
/* 5 */
{title:'Mercado e demanda', screens:[
 {kind:'learn', title:'Demanda: existe gente procurando o que você quer oferecer?',
  body:'<p>Sem pesquisa, demanda é opinião. A forma mais simples de buscar evidência, sem depender de estatísticas: escolher <b>5 hospedagens parecidas na região</b> e observar nas plataformas a diária, as avaliações e o calendário dos próximos fins de semana e feriados.</p><div class="za-card"><b>Mercado = 40% evidência de demanda + 30% sazonalidade + 30% referência de diária</b><br>Evidência: pesquisa feita 100 · percepção 50 · nenhuma 0. Sazonalidade: procura o ano todo 100 · temporadas e feriados 60 · só uma estação curta 25. Diária de referência pesquisada: 100; desconhecida: 0.</div>',
  example:'Exemplo: percepção de que há procura (50), demanda concentrada em temporadas (60) e diária de referência pesquisada: mercado = 20 + 18 + 30 = 68/100.'},
 {kind:'compare', title:'Opinião × evidência',
  cols:[{h:'Opinião',type:'bad',items:['“Todo fim de semana tem gente aqui.”','“Ouvi dizer que as pousadas lotam.”','“Turismo na região só cresce.”']},
        {h:'Evidência',type:'good',items:['Calendários de 5 concorrentes observados','Diárias e avaliações anotadas numa planilha','Datas de maior procura identificadas']}]},
 {kind:'form', title:'O que você sabe sobre a demanda',
  fields:[
   {id:'evidencia',label:'Que evidência de demanda você tem?',type:'radio',required:true,options:[{v:'pesquisa',l:'Pesquisei concorrentes (diária, avaliações, calendário)'},{v:'percepcao',l:'Percepção minha ou de conhecidos'},{v:'nao',l:'Nenhuma ainda'}]},
   {id:'sazonalidade',label:'Como é a procura turística na região ao longo do ano?',type:'radio',required:true,options:[{v:'ano',l:'Distribuída ao longo do ano'},{v:'temporadas',l:'Concentrada em temporadas e feriados'},{v:'curta',l:'Só numa estação curta'}]},
   {id:'concorrentes',label:'Hospedagens parecidas na região',type:'radio',required:true,options:[{v:'nenhuma',l:'Não conheço nenhuma'},{v:'poucas',l:'Poucas'},{v:'muitas',l:'Muitas'}]},
   {id:'diaria_ref',label:'Diária média de referência de hospedagens parecidas',type:'money',required:true,allowUnknown:true}
  ]},
 {kind:'feedback', title:'Leitura do mercado',
  metrics:function(s,c){return [{label:'Mercado e demanda',value:F.num(c.s.mer,0)+'/100',tag:'calculado'},{label:'Diária de referência',value:F.brl0(s.n('diaria_ref')),tag:'informado'}];},
  feedback:function(s,c){var o=[];var ev=s.t('evidencia');
   if(ev==='nao') o.push({lv:'warn',t:'Sem evidência de demanda, o mercado é a dimensão mais incerta do Raio-X. A pesquisa de 5 concorrentes leva poucas horas e muda a qualidade do diagnóstico.'});
   else if(ev==='percepcao') o.push({lv:'info',t:'Percepção é um começo. Transforme em evidência registrando diária, avaliações e calendário de 5 concorrentes.'});
   else o.push({lv:'ok',t:'Você já pesquisou concorrentes: o diagnóstico de mercado tem base concreta.'});
   if(s.t('concorrentes')==='nenhuma') o.push({lv:'info',t:'Nenhuma hospedagem parecida conhecida: pode ser oportunidade ou sinal de pouca demanda. Só a pesquisa distingue uma coisa da outra.'});
   if(s.t('concorrentes')==='muitas') o.push({lv:'info',t:'Muitos concorrentes indicam demanda existente, e também exigem diferencial claro.'});
   if(s.t('sazonalidade')==='curta') o.push({lv:'warn',t:'Procura concentrada numa estação curta: o projeto precisa se pagar com poucos meses fortes. Pense em públicos para a baixa temporada (eventos, retiros, trabalho remoto).'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Montar uma planilha com 5 concorrentes: diária, nota, avaliações e calendário'},{id:'a5_2',text:'Identificar os meses e datas de maior e menor procura'},{id:'a5_3',text:'Ler as avaliações negativas dos concorrentes para encontrar oportunidades'}]}
]},
/* 6 */
{title:'Restrições e pendências', screens:[
 {kind:'learn', title:'Restrições: o que pode limitar ou impedir o projeto',
  body:'<p>Muitas terras com potencial têm limitações que só aparecem tarde: faixas de preservação ao longo de rios e nascentes, reserva legal, unidades de conservação próximas, servidões, áreas de risco, pendências na documentação ou conflitos de posse.</p><p>Este pilar <b>não</b> verifica nada disso por você: ele registra o que você <b>já sabe</b> e quais <b>consultas já fez</b>. Só os órgãos competentes e profissionais habilitados confirmam restrições.</p><div class="za-card"><b>Restrições = (100 − 15 × restrições conhecidas) × (60% + 10% × consultas feitas)</b><br>Sem consultas, a nota fica limitada a 60: “não conheço restrições” não é o mesmo que “não há restrições”.</div>',
  example:'Exemplo: uma restrição conhecida (faixa de preservação do rio) e uma consulta feita (prefeitura): (100 − 15) × 70% = 59,5/100.'},
 {kind:'compare', title:'Descobrir antes × descobrir depois',
  cols:[{h:'Depois (caro)',type:'bad',items:['Obra embargada perto do rio','Investidor desiste ao ver a matrícula','Licença negada por estar em área de proteção']},
        {h:'Antes (barato)',type:'good',items:['Consulta prévia à prefeitura e ao órgão ambiental','Certidões do imóvel atualizadas','Implantação planejada fora das áreas restritas']}]},
 {kind:'form', title:'O que você já sabe e o que já consultou',
  fields:[
   {id:'restricoes',label:'Restrições ou pendências que você já sabe que existem',type:'checks',options:RESTR.map(function(r){return {v:r.v,l:r.l};})},
   {id:'consultas',label:'Consultas que você já fez',type:'checks',options:CONS}
  ]},
 {kind:'feedback', title:'Leitura das restrições',
  metrics:function(s,c){return [{label:'Restrições e pendências',value:F.num(c.s.res,0)+'/100',tag:'calculado'},{label:'Restrições conhecidas',value:String(c.nR),tag:'informado'},{label:'Consultas feitas',value:c.nC+' de 4',tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(c.crit.length) o.push({lv:'bad',t:'Pontos críticos: '+c.crit.map(function(r){return r.l.toLowerCase();}).join('; ')+'. Eles podem impedir ou adiar o projeto. Busque orientação de advogado ou engenheiro antes de investir.'});
   if(c.nR===0&&c.nC===0) o.push({lv:'warn',t:'Nenhuma restrição conhecida, mas nenhuma consulta feita. Isso é falta de informação, não ausência de restrição.'});
   if(c.nR>0&&!c.crit.length) o.push({lv:'info',t:c.nR+' restrição(ões) conhecida(s). Em geral, elas definem <b>onde</b> e <b>como</b> construir. Um levantamento técnico mostra a área efetivamente utilizável.'});
   if(!has(c.cons,'ambiental')&&(has(c.restr,'app')||has(c.restr,'uc')||has(c.restr,'reserva_legal'))) o.push({lv:'warn',t:'Há restrição ambiental conhecida e nenhuma consulta ao órgão ambiental. Esse é o próximo passo.'});
   if(c.nC===4) o.push({lv:'ok',t:'Você consultou prefeitura, órgão ambiental, cartório e profissional habilitado. Base sólida para seguir.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Pedir consulta prévia de uso do solo na prefeitura'},{id:'a6_2',text:'Atualizar as certidões do imóvel no cartório'},{id:'a6_3',text:'Levar as restrições conhecidas a um engenheiro ou advogado'}]}
]},
/* 7 */
{title:'Diagnóstico preliminar', screens:[
 {kind:'learn', title:'Do Raio-X ao diagnóstico: índice, gargalo e confiança',
  body:'<p>O diagnóstico combina as seis dimensões em três leituras:</p><ul><li><b>Índice Zion</b> (pesos fixos: atrativos 25%, mercado 20%, localização, acesso e infraestrutura 15% cada, restrições 10%).</li><li><b>Índice com os seus pesos:</b> você diz o que importa mais para o seu projeto, de 1 a 5, e o Raio-X recalcula.</li><li><b>Gargalo:</b> a dimensão mais fraca, que pode limitar o projeto mesmo com índice bom.</li></ul><p>Há ainda a <b>confiança</b> do diagnóstico: a parte dos dados-chave que você informou (tempo ao centro emissor, cidade de apoio, distância da rede de energia e diária de referência).</p><div class="za-card">Faixas orientativas: 70+ potencial alto (preliminar) · 50 a 69 moderado · 30 a 49 limitado · abaixo de 30 baixo com os dados atuais.</div>',
  example:'Exemplo: índice Zion de 65 (moderado) com gargalo em restrições (59). Se o projeto for de retiros, o proprietário pode dar peso 5 a atrativos e 2 a localização e ver o índice mudar.'},
 {kind:'compare', title:'Diagnóstico útil × diagnóstico perigoso',
  cols:[{h:'Perigoso',type:'bad',items:['Tratar o índice como garantia de sucesso','Ignorar o gargalo porque a média é boa','Decidir com dados que você marcou como “não sei”']},
        {h:'Útil',type:'good',items:['Usar o índice para comparar e priorizar','Atacar primeiro o gargalo','Confirmar os dados ausentes antes de investir']}]},
 {kind:'form', title:'O que mais importa para o seu projeto (1 a 5)', intro:'Dê peso maior ao que for decisivo para o tipo de projeto que você imagina.',
  fields:[
   {id:'peso_loc',label:'Localização',type:'radio',required:true,options:esc5('pouco importante','decisivo')},
   {id:'peso_atr',label:'Atrativos',type:'radio',required:true,options:esc5('pouco importante','decisivo')},
   {id:'peso_ace',label:'Acesso',type:'radio',required:true,options:esc5('pouco importante','decisivo')},
   {id:'peso_inf',label:'Infraestrutura',type:'radio',required:true,options:esc5('pouco importante','decisivo')},
   {id:'peso_mer',label:'Mercado e demanda',type:'radio',required:true,options:esc5('pouco importante','decisivo')},
   {id:'peso_res',label:'Restrições e pendências',type:'radio',required:true,options:esc5('pouco importante','decisivo')}
  ]},
 {kind:'feedback', title:'Seu diagnóstico preliminar',
  metrics:function(s,c){return [{label:'Índice Zion',value:F.num(c.idx,0)+'/100',tag:'calculado'},{label:'Índice com seus pesos',value:F.num(c.idxCli,0)+'/100',tag:'calculado'},{label:'Gargalo',value:c.garg.n,tag:'calculado'},{label:'Confiança dos dados',value:F.pct(c.conf*100,0),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:c.idx>=70?'ok':c.idx>=50?'info':'warn',t:'Classificação: <b>'+c.classe+'</b>. Índice Zion '+F.num(c.idx,0)+'/100; com os seus pesos, '+F.num(c.idxCli,0)+'/100.'});
   if(Math.abs(c.idx-c.idxCli)>=10) o.push({lv:'info',t:'Os seus pesos mudam o índice em '+F.num(Math.abs(c.idx-c.idxCli),0)+' pontos. Confirme se as prioridades que você deu fazem sentido para o público e o modelo pretendidos.'});
   o.push({lv:c.garg.v<40?'bad':'warn',t:'Gargalo: <b>'+c.garg.n+'</b> ('+F.num(c.garg.v,0)+'/100). É por ele que o plano começa.'});
   if(c.crit.length) o.push({lv:'bad',t:'Há '+c.crit.length+' ponto(s) crítico(s) de restrição. Independentemente do índice, resolva-os com profissional habilitado antes de investir.'});
   if(c.conf<0.75) o.push({lv:'warn',t:'Confiança de '+F.pct(c.conf*100,0)+': parte dos dados-chave está ausente. O diagnóstico é mais hipótese do que leitura.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Atacar o gargalo identificado nas próximas 2 semanas'},{id:'a7_2',text:'Completar os dados marcados como “não sei”'},{id:'a7_3',text:'Refazer o Raio-X depois das consultas e comparar o índice'}]}
]}
],

compute:function(s){
 var c={s:{}};
 // localização
 var t=s.n('tempo_emissor'), da=s.n('dist_apoio');
 c.pTempo=t==null?0:t<=2?100:t<=4?70:t<=6?40:20;
 c.pDest={consolidado:100,emergente:65,sem:25}[s.t('destino')]||0;
 c.pApoio=da==null?0:da<=15?100:da<=40?70:40;
 c.s.loc=(c.pTempo+c.pDest+c.pApoio)/3;
 // atrativos
 var notas=ATR.map(function(a){return {n:a.n,v:sc(s,a.id,1)};});
 c.atrMedia=notas.reduce(function(x,a){return x+a.v;},0)/notas.length;
 c.s.atr=(c.atrMedia-1)/4*100;
 c.atrTop=notas.slice().sort(function(a,b){return b.v-a.v;})[0];
 // acesso
 var kt=s.n('km_terra',0);
 c.s.ace=0.5*({asfalto:100,terra_boa:70,terra_ruim:35,sem:10}[s.t('via')]||0)+0.25*({sim:100,as_vezes:50,nao:0}[s.t('chuva')]||0)+0.25*(kt===0?100:kt<=5?75:kt<=15?50:25);
 // infraestrutura
 c.inf=arr(s,'infra'); c.nInf=INFRA.filter(function(x){return has(c.inf,x.v);}).length; c.infFalta=INFRA.filter(function(x){return !has(c.inf,x.v);});
 c.s.inf=c.nInf/6*100;
 // mercado
 c.s.mer=0.4*({pesquisa:100,percepcao:50,nao:0}[s.t('evidencia')]||0)+0.3*({ano:100,temporadas:60,curta:25}[s.t('sazonalidade')]||0)+0.3*(s.n('diaria_ref')!=null?100:0);
 // restrições
 c.restr=arr(s,'restricoes'); c.cons=arr(s,'consultas');
 c.nR=RESTR.filter(function(r){return has(c.restr,r.v);}).length; c.nC=CONS.filter(function(r){return has(c.cons,r.v);}).length;
 c.crit=RESTR.filter(function(r){return r.crit&&has(c.restr,r.v);});
 c.s.res=ZA.clamp(100-15*c.nR,0,100)*(0.6+0.1*c.nC);
 // índices
 c.idx=DIM.reduce(function(x,d){return x+d.w*c.s[d.k];},0)/100;
 var pw=PESOS.map(function(p){return {k:p.k,p:sc(s,p.id,3)};}), sp=pw.reduce(function(x,p){return x+p.p;},0);
 c.idxCli=sp?pw.reduce(function(x,p){return x+p.p*c.s[p.k];},0)/sp:c.idx;
 c.pesosCli=pw;
 c.classe=classe(c.idx);
 c.dims=DIM.map(function(d){return {k:d.k,n:d.n,w:d.w,v:c.s[d.k]};});
 c.garg=c.dims.slice().sort(function(a,b){return a.v-b.v;})[0];
 var keys=['tempo_emissor','dist_apoio','dist_rede','diaria_ref']; c.conf=keys.filter(function(k){return !s.unknown(k)&&s.n(k)!=null;}).length/keys.length;
 return c;
},

metrics:function(s,c){return [
 {label:'Índice Zion de potencial',value:F.num(c.idx,0)+'/100',tag:'calculado'},
 {label:'Classificação',value:c.classe,tag:'calculado'},
 {label:'Índice com seus pesos',value:F.num(c.idxCli,0)+'/100',tag:'calculado'},
 {label:'Gargalo',value:c.garg.n+' ('+F.num(c.garg.v,0)+')',tag:'calculado'},
 {label:'Dimensão mais forte',value:c.dims.slice().sort(function(a,b){return b.v-a.v;})[0].n,tag:'calculado'},
 {label:'Pontos críticos de restrição',value:String(c.crit.length),tag:'informado'},
 {label:'Confiança dos dados',value:F.pct(c.conf*100,0),tag:'calculado'},
 {label:'Diária de referência',value:F.brl0(s.n('diaria_ref')),tag:'informado'}
];},

priorities:function(s,c){var L=[];
 c.crit.forEach(function(r){L.push({title:'Resolver com profissional habilitado: '+r.l.toLowerCase(),why:'Ponto crítico que pode impedir ou adiar o projeto.',score:r.v==='risco'?10:9});});
 if(c.nC===0) L.push({title:'Fazer a consulta prévia de uso do solo na prefeitura',why:'Sem consultas, restrições são desconhecidas.',score:8});
 if(!has(c.cons,'ambiental')&&(has(c.restr,'app')||has(c.restr,'uc')||has(c.restr,'reserva_legal'))) L.push({title:'Consultar o órgão ambiental sobre as restrições conhecidas',why:'Define onde e como é possível construir.',score:8});
 if(s.t('evidencia')!=='pesquisa') L.push({title:'Pesquisar 5 concorrentes: diária, avaliações e calendário',why:'Transforma opinião sobre demanda em evidência.',score:s.t('evidencia')==='nao'?8:6});
 if(s.unknown('tempo_emissor')) L.push({title:'Medir o tempo de viagem até os centros emissores',why:'Dado-chave da localização.',score:6});
 if(s.unknown('diaria_ref')) L.push({title:'Levantar a diária de referência da região',why:'Necessária para qualquer conta futura.',score:5});
 if(s.t('chuva')==='nao'||s.t('via')==='sem') L.push({title:'Levantar solução e custo para o acesso o ano todo',why:'Acesso precário pode inviabilizar a operação.',score:8});
 else if(c.s.ace<50) L.push({title:'Planejar melhorias no acesso',why:'Acesso em '+F.num(c.s.ace,0)+'/100.',score:5});
 if(!has(c.inf,'agua')) L.push({title:'Verificar com engenheiro a viabilidade de água em quantidade',why:'Sem água não há hospedagem.',score:8});
 if(!has(c.inf,'energia')) L.push({title:'Consultar a concessionária sobre custo e prazo de energia',why:'Pode ser parte relevante do investimento.',score:6});
 if(sc(s,'at_exclusividade',1)<=2) L.push({title:'Definir um diferencial de experiência, já que os atrativos são comuns na região',why:'Exclusividade baixa.',score:4});
 if(c.garg&&c.garg.v<50) L.push({title:'Concentrar esforço no gargalo: '+c.garg.n.toLowerCase(),why:'Dimensão mais fraca ('+F.num(c.garg.v,0)+'/100).',score:7});
 if(c.idx>=70&&!c.crit.length) L.push({title:'Seguir para a escolha do modelo e o orçamento preliminar',why:'Potencial alto (preliminar) sem pontos críticos conhecidos.',score:6});
 return L;},

report:function(s,c){
 var dims=ZA.table(['Dimensão','Nota','Peso Zion','Seu peso','Leitura'],c.dims.map(function(d){var p=c.pesosCli.filter(function(x){return x.k===d.k;})[0].p;return [d.n,F.num(d.v,0)+'/100',d.w+'%',p+' de 5',d.v>=70?'favorável':d.v>=50?'atenção':'gargalo potencial'];}).concat([['<b>Índice Zion</b>','<b>'+F.num(c.idx,1)+'/100</b>','100%','','<b>'+esc(c.classe)+'</b>'],['<b>Índice com seus pesos</b>','<b>'+F.num(c.idxCli,1)+'/100</b>','','','']]),[1,2,3]);
 var atr=ZA.table(['Atrativo','Nota'],ATR.map(function(a){return [a.n,sc(s,a.id,1)+' de 5'];}),[1]);
 var rest=(c.nR?ZA.table(['Restrição conhecida','Gravidade'],RESTR.filter(function(r){return has(c.restr,r.v);}).map(function(r){return [esc(r.l),r.crit?'<b>crítica</b>':'define onde e como construir'];})):'<p>Nenhuma restrição conhecida informada.</p>')+'<p>Consultas feitas: '+(c.nC?c.cons.map(function(v){return esc((CONS.filter(function(x){return x.v===v;})[0]||{l:v}).l);}).join('; '):'nenhuma')+'.</p><p class="za-small">Esta lista registra o que você sabe; não é verificação. Confirme com prefeitura, órgão ambiental, cartório e profissional habilitado.</p>';
 var conf=ZA.table(['O que confirmar','Situação'],[
  ['Tempo até o centro emissor',s.unknown('tempo_emissor')?'<b>ausente</b>':'informado'],['Distância da cidade de apoio',s.unknown('dist_apoio')?'<b>ausente</b>':'informado'],
  ['Distância da rede de energia',s.unknown('dist_rede')?'<b>ausente</b>':'informado'],['Diária de referência',s.unknown('diaria_ref')?'<b>ausente</b>':'informado'],
  ['Evidência de demanda',{pesquisa:'pesquisa feita',percepcao:'<b>só percepção</b>',nao:'<b>nenhuma</b>'}[s.t('evidencia')]||'—'],
  ['Consultas a órgãos e profissionais',c.nC+' de 4']]);
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Pesos Zion das dimensões','localização 15 · atrativos 25 · acesso 15 · infraestrutura 15 · mercado 20 · restrições 10',tag('recomendacao','metodologia Zion')],
  ['Seus pesos',c.pesosCli.map(function(p){return p.p;}).join(' · '),tag('informado')],
  ['Faixas de tempo, distância e via','conforme explicado em cada pilar',tag('recomendacao','metodologia Zion')],
  ['Fator de consultas em restrições','60% + 10% por consulta feita',tag('recomendacao','metodologia Zion')],
  ['Diária de referência',F.brl0(s.n('diaria_ref')),s.unknown('diaria_ref')?tag('hipotese','ausente'):tag('informado','sua pesquisa')],
  ['Área total',F.num(s.n('area_ha'),2)+' ha',tag('informado')]],[1]);
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido de 30 dias</b><ol><li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Revisar os dados do Raio-X')+'.</li><li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Pesquisar concorrentes')+'.</li><li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Consultar a prefeitura')+'.</li><li><b>Semana 4:</b> completar os dados ausentes, refazer o Raio-X e decidir: seguir para conceito e orçamento, resolver os gargalos primeiro ou repensar a finalidade da terra.</li></ol></div>';
 return {sections:[
  {title:'Raio-X por dimensão',html:dims+'<p class="za-small">Faixas orientativas: 70+ potencial alto (preliminar) · 50–69 moderado · 30–49 limitado · abaixo de 30 baixo com os dados atuais. Gargalo: <b>'+esc(c.garg.n)+'</b>.</p>'},
  {title:'Atrativos avaliados',html:atr},
  {title:'Restrições e pendências',html:rest},
  {title:'Confiança do diagnóstico',html:'<p>Confiança dos dados-chave: <b>'+F.pct(c.conf*100,0)+'</b>.</p>'+conf},
  {title:'Premissas utilizadas',html:prem}
 ],plan:plan};
}
});
})();
