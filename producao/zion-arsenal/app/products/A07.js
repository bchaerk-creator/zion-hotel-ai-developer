/* ZAR-A07 · Você Está Perdendo Reservas no Atendimento? · Assistente de Conversão de Reservas */
(function(){
var F=ZA.fmt, esc=ZA.esc;
var PERG=[{v:'datas',l:'Datas exatas e flexibilidade'},{v:'pessoas',l:'Quantas pessoas (adultos e crianças)'},{v:'ocasiao',l:'Motivo da viagem (descanso, comemoração, trabalho)'},{v:'criancas_pets',l:'Necessidades especiais (crianças pequenas, pet, acessibilidade)'},{v:'expectativa',l:'O que mais valorizam numa hospedagem'},{v:'origem',l:'De onde vêm e como vão chegar'}];
var PERG_TXT={datas:'As datas são fixas ou vocês têm alguma flexibilidade?',pessoas:'Quantas pessoas vêm, e tem alguma criança?',ocasiao:'É uma viagem de descanso ou estão comemorando alguma data especial?',criancas_pets:'Alguém do grupo precisa de algo específico (berço, pet, acessibilidade)?',expectativa:'O que não pode faltar para essa viagem ser perfeita para vocês?',origem:'Vocês vêm de onde? Assim já te mando a melhor rota.'};
var OBJ=[{v:'preco',l:'“Está caro” / “Tem desconto?”'},{v:'pensar',l:'“Vou pensar e te aviso”'},{v:'datas',l:'“Não tem nessa data?”'},{v:'distancia',l:'“É longe / o acesso é difícil?”'},{v:'pets',l:'“Aceita pet?” / regras da casa'},{v:'comparando',l:'“Estou vendo outras opções”'}];
var CANAIS=[{v:'whatsapp',l:'WhatsApp'},{v:'instagram',l:'Instagram (direct)'},{v:'airbnb',l:'Mensagens do Airbnb'},{v:'booking',l:'Mensagens do Booking'},{v:'telefone',l:'Telefone'},{v:'site',l:'Site ou e-mail'}];
var PUB={casais:'casais',familias:'famílias',amigos:'grupos de amigos',trabalho:'quem viaja a trabalho',pets:'quem viaja com pet'};
function arr(s,id){return Array.isArray(s.v[id])?s.v[id]:[];}
function msg(t){return '<div class="za-card" style="white-space:pre-line;font-size:15px">'+t+'</div>';}
function difs(s){return ['of_dif1','of_dif2','of_dif3'].map(function(k){return String(s.t(k)).trim();}).filter(Boolean);}
function nomeAt(s){return esc(s.t('at_nome')||'[seu nome]');}
function prop(s){return esc(s.t('propriedade')||'[sua hospedagem]');}

/* ---------- montagem dos scripts (sem IA: modelos preenchidos com os dados do cliente) ---------- */
function sPrimeira(s){
 var pub=s.t('ne_publico'), q;
 if(pub==='casais') q='É uma viagem a dois? Estão comemorando alguma data especial?';
 else if(pub==='familias') q='Quantos adultos e crianças vêm? Tem criança pequena?';
 else if(pub==='pets') q='Quantas pessoas vêm, e qual é o porte do pet?';
 else if(pub==='trabalho') q='Quantas pessoas vêm e vocês vão precisar de internet estável para trabalhar?';
 else q='Quantas pessoas vêm e qual é a ocasião da viagem?';
 return 'Olá, [nome do hóspede]! Aqui é '+nomeAt(s)+', da '+prop(s)+'. Que bom receber sua mensagem!\nConfirmei aqui: temos disponibilidade para [datas]. Para eu te passar o valor certinho e indicar a melhor opção, me conta: '+q;
}
function sQualif(s){
 var a=arr(s,'ne_perguntas'), use=a.length?a:['datas','pessoas','ocasiao'];
 return 'Perfeito! Só mais algumas perguntas rápidas para eu preparar sua proposta:\n'+use.map(function(k){return '• '+PERG_TXT[k];}).join('\n');
}
function sOferta(s,c){
 var d=difs(s), oc=String(s.t('ne_ocasiao')).trim(), pub=PUB[s.t('ne_publico')]||'nossos hóspedes';
 return 'Prontinho, [nome do hóspede]! Para [datas] ('+F.num(c.est,c.est%1?1:0)+' noites), [nº de pessoas] pessoas, o valor total fica em <b>R$ [valor total]</b>.\n'+
  '✔ Está incluído: '+esc(s.t('of_inclui')||'[o que está incluído]')+'.\n'+
  (d.length?'O que mais encanta '+pub+(oc?' que vêm para '+esc(oc):'')+':\n'+d.map(function(x){return '• '+esc(x);}).join('\n')+'\n':'')+
  'Para garantir as datas: '+esc(s.t('ob_condicao')||'[condição de pagamento]')+'.\n'+
  'Consigo segurar essas datas para você por '+F.num(s.n('fu_validade',24))+' horas. Quer que eu já reserve?';
}
function sObj(s,c,k){
 var d=difs(s), d1=d[0]?esc(d[0]):'[seu principal diferencial]', inc=esc(s.t('of_inclui')||'[o que está incluído]');
 var desc=s.n('ob_desconto',0), regra=String(s.t('ob_desc_regra')).trim();
 switch(k){
  case 'preco': return 'Entendo totalmente, [nome do hóspede]! Só para você comparar com tranquilidade: no valor já está incluído '+inc+', e você terá '+d1+'.'+(desc>0?'\nSe fizer sentido para vocês, consigo uma condição de até '+F.pct(desc,0)+(regra?' para '+esc(regra):'')+'.':'\nPrefiro manter o valor e garantir que nada fique faltando na experiência de vocês.')+'\nQuer que eu segure as datas enquanto você decide?';
  case 'pensar': return 'Claro, fique à vontade! Deixo as datas reservadas para você por '+F.num(s.n('fu_validade',24))+' horas, sem compromisso.\nFicou alguma dúvida que eu possa esclarecer agora? Às vezes um detalhe (horário, acesso, o que levar) faz diferença na decisão.';
  case 'datas': return 'Nessa data já estamos reservados, [nome do hóspede]. Tenho disponibilidade em [datas alternativas próximas]. Alguma delas funciona para vocês?\nSe preferir, aviso você caso a data original seja liberada.';
  case 'distancia': return 'Ótima pergunta! O acesso é [descrição honesta do caminho: tipo de estrada, tempo desde a cidade]. Eu envio um vídeo do trajeto antes da chegada para ninguém se perder.\nE vale a viagem: '+d1+'.';
  case 'pets': return 'Obrigado por perguntar antes! Nossa política é: [regra sobre pets e regras da casa, de forma clara]. Assim todo mundo aproveita com tranquilidade.';
  case 'comparando': return 'Faz todo sentido comparar! Para te ajudar: aqui você tem '+d1+(d[1]?' e '+esc(d[1]):'')+', e o valor já inclui '+inc+'.\nSe quiser, te mando mais fotos ou um vídeo do espaço para você decidir com calma.';
 }
 return '';
}
function sFollow1(s){return 'Oi, [nome do hóspede]! Passando para saber se ficou alguma dúvida sobre a '+prop(s)+' para [datas]. As datas seguem reservadas para você até [dia e horário]. Posso ajudar em algo?';}
function sFollow2(s){return 'Oi, [nome do hóspede]! Hoje às [horário] encerro a pré-reserva das suas datas. Se quiser, já deixo tudo garantido.\nSe os planos mudaram, sem problema: fico à disposição para uma próxima viagem. Um abraço, '+nomeAt(s)+'.';}
function sConfirma(s){return 'Reserva confirmada, [nome do hóspede]! Muito obrigado pela confiança.\nAlguns dias antes da chegada eu te envio o guia com o caminho, horários e tudo o que você precisa saber. Qualquer dúvida até lá, é só me chamar. '+nomeAt(s)+' · '+prop(s);}

ZA.register({
id:'A07', code:'ZAR-A07', collection:'Hospedagem',
title:'Você Está Perdendo Reservas no Atendimento?',
subtitle:'Aprenda a Transformar Consultas em Oportunidades',
tool:'Assistente de Conversão de Reservas',
deliverable:'Playbook de Atendimento e Reservas',
nameField:'nome', propertyField:'propriedade',
disclaimer:'Os scripts são modelos para adaptar ao seu jeito de falar; a receita “não capturada” é uma estimativa feita com os números que você informou, não uma previsão. Conversão depende de preço, datas, concorrência e do próprio hóspede: não há garantia de reservas ou faturamento.',

intro:[
 {kind:'mirror', title:'O cliente pergunta o preço e depois desaparece?',
  lead:'O celular apita, você responde na hora com o valor, e a conversa morre ali. No dia seguinte, outra consulta, a mesma história. Você fica pensando se o problema é o preço.',
  body:'<div class="za-card"><p>Veja se alguma destas frases é familiar:</p><ul><li>“Mando o valor e o cliente some.”</li><li>“Recebo muitas mensagens, mas poucas viram reserva.”</li><li>“Quando dizem ‘vou pensar’, eu não sei o que responder.”</li><li>“Tenho vergonha de chamar de novo para não parecer insistente.”</li></ul></div>'},
 {kind:'collapse', title:'Responder rápido não significa necessariamente vender bem.',
  lead:'Velocidade ajuda, mas uma resposta rápida que só informa o preço deixa o hóspede comparando números, e não experiências.',
  body:'<div class="za-card"><p>Uma consulta é uma conversa com etapas: <b>acolher → entender → apresentar → responder dúvidas → acompanhar</b>. Quando você pula etapas, o hóspede decide só pelo preço.</p><p>Neste percurso você vai medir sua taxa de conversão, estimar quanto deixa de reservar e sair com um <b>playbook de mensagens</b> montado com os dados da sua hospedagem.</p></div>'},
 {kind:'start', title:'Vamos montar o seu playbook de atendimento',
  lead:'Em 7 pilares, você vai mapear sua jornada comercial, ajustar cada etapa da conversa e sair com scripts prontos para copiar e adaptar.',
  body:'<p>Tenha à mão, se possível: o número de consultas e reservas do último mês (WhatsApp, Instagram, plataformas) e algumas conversas recentes. Se não tiver algum dado, marque “não sei”.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Ana'},
   {id:'propriedade',label:'Nome da hospedagem',type:'text',required:true,placeholder:'Ex.: Cabanas Vale Sereno'},
   {id:'tipo',label:'Tipo de hospedagem',type:'select',required:true,options:[{v:'airbnb',l:'Apartamento ou casa (Airbnb/temporada)'},{v:'cabana',l:'Cabana ou chalé'},{v:'glamping',l:'Glamping'},{v:'pousada',l:'Pequena pousada'},{v:'outro',l:'Outro'}]},
   {id:'destino',label:'Cidade / destino',type:'text',required:true,placeholder:'Ex.: Cunha (SP)'},
   {id:'unidades',label:'Quantas unidades você aluga?',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)'}
  ]}
],

pillars:[
/* 1 */
{title:'Jornada comercial', screens:[
 {kind:'learn', title:'Cada consulta é uma reserva em potencial',
  body:'<p>A <b>taxa de conversão</b> é o número de reservas dividido pelo número de consultas. Ela mostra quantas conversas viram hóspedes. Uma consulta é qualquer pedido de preço ou disponibilidade, por qualquer canal.</p><p>Com a conversão e o <b>valor médio de uma reserva</b> (diária média × estadia média), dá para estimar quanto cada ponto percentual de conversão representa em receita. É esse número que mostra se vale a pena investir tempo no atendimento.</p>',
  example:'Exemplo ilustrativo: 40 consultas e 6 reservas no mês = 15% de conversão. Se a reserva média vale R$ 700, cada ponto a mais de conversão (0,4 reserva) equivale a cerca de R$ 280 por mês.'},
 {kind:'compare', title:'Atender mensagens × gerir uma jornada comercial',
  cols:[{h:'Atender mensagens',type:'bad',items:['Não sabe quantas consultas recebe','Cada canal funciona de um jeito','Só conta as reservas, não as perdas','Culpa o preço por toda desistência']},
        {h:'Gerir a jornada',type:'good',items:['Conta consultas e reservas por mês','Usa o mesmo roteiro em todos os canais','Sabe em que etapa a conversa morre','Mede a conversão antes de mudar o preço']}]},
 {kind:'form', title:'Seus números de atendimento', intro:'Use o último mês completo ou uma média dos últimos 3 meses.',
  fields:[
   {id:'cv_consultas',label:'Consultas recebidas por mês (todos os canais)',type:'number',required:true,min:1,max:100000,step:1,unit:'consultas'},
   {id:'cv_reservas',label:'Reservas fechadas a partir dessas consultas',type:'number',required:true,min:0,max:100000,step:1,unit:'reservas',validate:function(v,s){var q=s.n('cv_consultas');return (q!=null&&v>q)?'As reservas não podem passar do número de consultas.':'';}},
   {id:'cv_canais',label:'Por onde as consultas chegam?',type:'checks',options:CANAIS},
   {id:'cv_diaria',label:'Diária média cobrada',type:'money',required:true,min:1},
   {id:'cv_estadia',label:'Estadia média',type:'number',required:true,min:1,max:60,step:0.1,unit:'noites',allowUnknown:true,help:'Se não souber, o cálculo usará 2 noites como hipótese.'}
  ]},
 {kind:'feedback', title:'Sua taxa de conversão',
  metrics:function(s,c){return [{label:'Taxa de conversão',value:c.conv==null?'—':F.pct(c.conv*100),tag:'calculado'},{label:'Consultas não convertidas/mês',value:F.num(c.perdidas),tag:'calculado'},{label:'Valor médio de uma reserva',value:F.brl(c.valorRes),tag:s.unknown('cv_estadia')?'estimativa':'calculado'},{label:'Cada +1 p.p. de conversão',value:F.brl(c.valorPP)+'/mês',tag:'estimativa'}];},
  feedback:function(s,c){var o=[];
   if(c.conv==null) o.push({lv:'warn',t:'Informe as consultas para calcular a conversão.'});
   else if(c.conv===0) o.push({lv:'bad',t:'Nenhuma consulta virou reserva no período. Antes de mexer no preço, vale revisar cada etapa da conversa.'});
   else o.push({lv:'info',t:'De cada 10 consultas, cerca de '+F.num(c.conv*10,1)+' viram reserva. As outras '+F.num(c.perdidas)+' consultas do mês são oportunidades para analisar.'});
   if(s.unknown('cv_estadia')) o.push({lv:'warn',t:'Estadia média desconhecida: usamos 2 noites como hipótese para o valor da reserva.'});
   if(arr(s,'cv_canais').length>=3) o.push({lv:'info',t:'Você atende por '+arr(s,'cv_canais').length+' canais. Um roteiro único evita que cada canal tenha um padrão diferente.'});
   if(!arr(s,'cv_canais').length) o.push({lv:'info',t:'Marque os canais por onde as consultas chegam para organizar o atendimento.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Contar consultas e reservas de todos os canais no fim de cada mês'},{id:'a1_2',text:'Identificar em que etapa as últimas 10 conversas perdidas pararam'},{id:'a1_3',text:'Usar o mesmo roteiro de atendimento em todos os canais'}]}
]},
/* 2 */
{title:'Atendimento inicial', screens:[
 {kind:'learn', title:'A primeira resposta decide se a conversa continua',
  body:'<p>Quem pergunta o preço quase sempre está consultando várias hospedagens ao mesmo tempo. A primeira resposta precisa fazer três coisas: <b>acolher</b> (cumprimentar pelo nome e se apresentar), <b>confirmar a disponibilidade</b> e <b>fazer uma pergunta</b> que mantenha a conversa viva.</p><p>Responder só com o número transforma você em mais uma opção na lista de preços. Responder com uma pergunta transforma a consulta em conversa.</p><p>O tempo também conta: quem responde primeiro tem mais chance de ser ouvido, desde que responda bem.</p>',
  example:'Exemplo ilustrativo: em vez de “R$ 450 a diária”, a resposta “Olá, Marina! Aqui é a Ana, da Cabana do Vale. Temos disponibilidade para o feriado! Para eu te passar o valor certinho: vocês vêm em quantas pessoas e é alguma comemoração?”.'},
 {kind:'compare', title:'Resposta-preço × resposta-conversa',
  cols:[{h:'Resposta-preço',type:'bad',items:['“R$ 450 a diária.”','Sem nome, sem apresentação','Nenhuma pergunta: a conversa acaba','Demora horas para responder à noite']},
        {h:'Resposta-conversa',type:'good',items:['Cumprimenta pelo nome e se apresenta','Confirma a disponibilidade das datas','Faz uma pergunta sobre o grupo ou a ocasião','Tem um tempo de resposta combinado']}]},
 {kind:'form', title:'Como você responde hoje',
  fields:[
   {id:'at_nome',label:'Como você assina as mensagens?',type:'text',required:true,placeholder:'Ex.: Ana'},
   {id:'at_tempo',label:'Tempo médio para a primeira resposta',type:'number',required:true,min:0,max:4320,step:1,unit:'minutos',allowUnknown:true},
   {id:'at_primeira',label:'O que costuma ter na sua primeira resposta?',type:'radio',required:true,options:[{v:'preco',l:'Só o preço'},{v:'preco_pergunta',l:'O preço e uma pergunta'},{v:'acolhe',l:'Cumprimento, disponibilidade e perguntas antes do preço'}]}
  ]},
 {kind:'feedback', title:'Sua primeira resposta, revisada',
  metrics:function(s,c){return [{label:'Pontuação de tempo',value:F.num(c.tempoScore,0)+' / 100',tag:s.unknown('at_tempo')?'hipotese':'calculado'},{label:'Pontuação da 1ª resposta',value:F.num(c.primeiraScore,0)+' / 100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];var t=s.n('at_tempo');
   if(t==null) o.push({lv:'warn',t:'Tempo de resposta desconhecido (50 pontos como hipótese). Anote o horário da consulta e da sua resposta durante uma semana.'});
   else if(t>120) o.push({lv:'bad',t:'Cerca de '+F.num(t)+' minutos para responder. Nesse intervalo, o hóspede provavelmente já recebeu outras propostas.'});
   else if(t>30) o.push({lv:'warn',t:'Resposta em cerca de '+F.num(t)+' minutos. Uma resposta curta de acolhimento, mesmo antes do preço, já segura a conversa.'});
   else o.push({lv:'ok',t:'Bom tempo de resposta. Agora o foco é a qualidade da mensagem.'});
   if(s.t('at_primeira')==='preco') o.push({lv:'bad',t:'Enviar só o preço deixa o hóspede comparando números. Use a mensagem abaixo como nova primeira resposta.'});
   else if(s.t('at_primeira')==='preco_pergunta') o.push({lv:'info',t:'Você já faz uma pergunta. Experimente perguntar <b>antes</b> do preço para montar uma proposta personalizada.'});
   else o.push({lv:'ok',t:'Sua primeira resposta já acolhe e qualifica. Use o modelo abaixo para padronizar.'});
   return o;},
  extra:function(s){return '<h2>Modelo de primeira resposta</h2>'+msg(sPrimeira(s))+'<p class="za-small">O texto completa automaticamente com seu nome e o nome da hospedagem. Os campos entre colchetes você preenche em cada conversa. A pergunta final se ajusta ao público que você escolher no Pilar 3.</p>';}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Salvar a nova primeira resposta como mensagem rápida no WhatsApp e nas plataformas'},{id:'a2_2',text:'Definir um tempo máximo para a primeira resposta, inclusive à noite'},{id:'a2_3',text:'Nunca enviar só o preço: sempre acolher e perguntar'}]}
]},
/* 3 */
{title:'Identificação de necessidades', screens:[
 {kind:'learn', title:'Perguntar antes de oferecer',
  body:'<p>Duas famílias podem pedir as mesmas datas e querer viagens completamente diferentes: uma procura sossego, a outra quer espaço para as crianças. Quando você pergunta, consegue <b>apresentar a hospedagem pelo ângulo que importa para aquela pessoa</b>.</p><p>As perguntas certas são poucas e naturais: datas, quem vem, a ocasião, necessidades especiais e o que não pode faltar. A resposta mais valiosa é a <b>ocasião</b>: ela dá o tom de toda a proposta.</p>',
  example:'Exemplo ilustrativo: o hóspede conta que vem pedir a namorada em casamento. A proposta passa a destacar o deck com vista para o pôr do sol, e o anfitrião oferece deixar flores no quarto. O preço é o mesmo; a percepção de valor, não.'},
 {kind:'compare', title:'Interrogatório × conversa',
  cols:[{h:'Interrogatório',type:'bad',items:['Formulário com 10 perguntas de uma vez','Perguntas que não mudam a proposta','Ignora o que o hóspede respondeu','Pede CPF antes de entender a viagem']},
        {h:'Conversa',type:'good',items:['2 ou 3 perguntas por mensagem','Cada pergunta muda algo na oferta','Usa a resposta na proposta seguinte','Dados de reserva só depois do “sim”']}]},
 {kind:'form', title:'O que você precisa descobrir',
  fields:[
   {id:'ne_perguntas',label:'O que você já pergunta (ou passará a perguntar) antes de enviar a proposta?',type:'checks',options:PERG},
   {id:'ne_publico',label:'Qual é o público mais comum da sua hospedagem?',type:'select',required:true,options:[{v:'casais',l:'Casais'},{v:'familias',l:'Famílias com crianças'},{v:'amigos',l:'Grupos de amigos'},{v:'trabalho',l:'Viagem a trabalho'},{v:'pets',l:'Pessoas com pet'}]},
   {id:'ne_ocasiao',label:'Qual é a ocasião mais comum das viagens?',type:'text',required:true,placeholder:'Ex.: descansar no fim de semana / aniversário de namoro'}
  ]},
 {kind:'feedback', title:'Suas perguntas de qualificação',
  metrics:function(s,c){return [{label:'Perguntas de qualificação',value:c.pergN+' de 6',tag:'informado'},{label:'Pontuação de qualificação',value:F.num(c.pergScore,0)+' / 100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];var a=arr(s,'ne_perguntas');
   if(c.pergN<=2) o.push({lv:'warn',t:'Você pergunta pouco antes de oferecer. Sem saber quem vem e por quê, a proposta fica genérica.'});
   else o.push({lv:'ok',t:'Boa base de qualificação ('+c.pergN+' perguntas). Distribua em 1 ou 2 mensagens para não parecer formulário.'});
   if(a.indexOf('ocasiao')<0) o.push({lv:'warn',t:'Você não pergunta a ocasião da viagem. É a pergunta que mais ajuda a personalizar a proposta.'});
   o.push({lv:'info',t:'Seu público principal são <b>'+(PUB[s.t('ne_publico')]||'—')+'</b>, e a ocasião mais comum é “'+esc(s.t('ne_ocasiao'))+'”. A proposta do Pilar 4 vai usar isso.'});
   return o;},
  extra:function(s){return '<h2>Modelo de mensagem de qualificação</h2>'+msg(sQualif(s));}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Perguntar a ocasião da viagem em toda consulta'},{id:'a3_2',text:'Anotar as respostas de cada hóspede para usar na proposta e na recepção'},{id:'a3_3',text:'Limitar a qualificação a no máximo 2 mensagens'}]}
]},
/* 4 */
{title:'Apresentação da oferta', screens:[
 {kind:'learn', title:'Proposta não é preço: é preço com motivo',
  body:'<p>Uma boa proposta tem cinco partes, nesta ordem:</p><ol><li><b>Resumo do pedido</b> (datas, noites, pessoas): mostra que você ouviu.</li><li><b>Valor total</b>, e não só a diária: evita surpresa com taxas.</li><li><b>O que está incluído</b>.</li><li><b>Até três diferenciais</b> ligados ao que o hóspede contou.</li><li><b>Próximo passo claro</b>: como reservar e até quando as datas ficam guardadas.</li></ol><p>Fotos ou um vídeo curto do espaço ajudam o hóspede a se imaginar ali.</p>',
  example:'Exemplo ilustrativo: “Para 12 a 14/07 (2 noites), 2 pessoas, o valor total é R$ 980, com café da manhã e lenha incluídos. Para o aniversário de vocês: banheira com vista e jantar a dois sob encomenda. Seguro as datas por 24 horas; quer que eu reserve?”'},
 {kind:'compare', title:'Proposta fria × proposta que vende',
  cols:[{h:'Fria',type:'bad',items:['Só a diária, sem total','Lista de 15 comodidades sem destaque','Nada sobre o que está incluído','Termina sem dizer como reservar']},
        {h:'Que vende',type:'good',items:['Valor total para as datas pedidas','Três diferenciais ligados ao pedido','Incluso explicado em uma linha','Fecha com prazo e convite para reservar']}]},
 {kind:'form', title:'Os elementos da sua proposta',
  fields:[
   {id:'of_dif1',label:'Diferencial nº 1 (o mais forte)',type:'text',required:true,placeholder:'Ex.: banheira de hidromassagem com vista para o vale'},
   {id:'of_dif2',label:'Diferencial nº 2',type:'text',placeholder:'Ex.: café da manhã colonial servido na cabana'},
   {id:'of_dif3',label:'Diferencial nº 3',type:'text',placeholder:'Ex.: trilha particular até a cachoeira'},
   {id:'of_inclui',label:'O que está incluído no valor',type:'text',required:true,placeholder:'Ex.: café da manhã, lenha para a lareira e roupa de cama'},
   {id:'of_formato',label:'Como você envia a proposta hoje?',type:'radio',required:true,options:[{v:'texto_preco',l:'Só o valor por texto'},{v:'texto_completo',l:'Texto com valor total, incluso e condições'},{v:'fotos',l:'Texto completo + fotos ou vídeo do espaço'}]}
  ]},
 {kind:'feedback', title:'Sua proposta montada',
  metrics:function(s,c){return [{label:'Diferenciais informados',value:c.difN+' de 3',tag:'informado'},{label:'Pontuação da proposta',value:F.num(c.ofertaScore,0)+' / 100',tag:'calculado'},{label:'Valor de referência da reserva',value:F.brl(c.valorRes),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.difN<3) o.push({lv:'warn',t:'Você informou '+c.difN+' diferencial(is). Três motivos concretos dão mais força à proposta.'});
   if(s.t('of_formato')==='texto_preco') o.push({lv:'bad',t:'Enviar só o valor é o formato que mais leva a comparação por preço. Use o modelo abaixo.'});
   else if(s.t('of_formato')==='texto_completo') o.push({lv:'info',t:'Proposta completa. Acrescentar 2 ou 3 fotos ou um vídeo curto ajuda o hóspede a se imaginar no lugar.'});
   else o.push({lv:'ok',t:'Formato completo, com imagem. Confira se o texto segue a ordem das cinco partes.'});
   o.push({lv:'info',t:'Na sua diária média e estadia média, uma reserva vale cerca de <b>'+F.brl(c.valorRes)+'</b>. Use o valor real das datas pedidas em cada proposta.'});
   return o;},
  extra:function(s,c){return '<h2>Modelo de proposta</h2>'+msg(sOferta(s,c))+'<p class="za-small">A ocasião e os diferenciais vêm das suas respostas. Ajuste o texto ao que cada hóspede contou.</p>';}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Enviar sempre o valor total das datas pedidas, não só a diária'},{id:'a4_2',text:'Montar um álbum com 5 fotos e um vídeo curto para anexar à proposta'},{id:'a4_3',text:'Terminar toda proposta com prazo e convite para reservar'}]}
]},
/* 5 */
{title:'Objeções', screens:[
 {kind:'learn', title:'Objeção é pergunta, não recusa',
  body:'<p>Quando o hóspede diz “está caro” ou “vou pensar”, ele normalmente está dizendo: <b>ainda não tenho certeza de que vale a pena</b>. A resposta certa não é baixar o preço na hora, e sim <b>esclarecer o valor</b> e facilitar a decisão.</p><p>Uma boa resposta a objeções segue três passos: <b>acolher</b> (“entendo”), <b>esclarecer</b> (o que está incluso, o diferencial, a condição) e <b>facilitar</b> (segurar as datas, enviar mais fotos, oferecer alternativa). O desconto, se existir, deve ter regra clara e limite que não fure seu preço mínimo.</p>',
  example:'Exemplo ilustrativo: com reserva média de R$ 700, conceder 10% de desconto custa R$ 70 por reserva. Se for oferecido a todos que pedem, o desconto deixa de ser exceção e vira o novo preço.'},
 {kind:'compare', title:'Ceder × conduzir',
  cols:[{h:'Ceder',type:'bad',items:['Baixa o preço no primeiro “está caro”','Responde “ok, fico no aguardo” ao “vou pensar”','Discute com o hóspede','Promete o que não pode cumprir']},
        {h:'Conduzir',type:'good',items:['Lembra o que está incluído e o diferencial','Segura as datas por um prazo e oferece ajuda','Responde com calma e informação','Desconto só com regra e limite definidos']}]},
 {kind:'form', title:'As objeções que você ouve',
  fields:[
   {id:'ob_lista',label:'Quais objeções aparecem com mais frequência?',type:'checks',options:OBJ},
   {id:'ob_condicao',label:'Condição de pagamento para reservar',type:'text',required:true,placeholder:'Ex.: 50% via Pix para reservar e 50% na chegada'},
   {id:'ob_desconto',label:'Desconto máximo que você aceita conceder',type:'percent',required:true,max:30,help:'Coloque 0 se você não trabalha com desconto.'},
   {id:'ob_desc_regra',label:'Em que condição o desconto vale?',type:'text',placeholder:'Ex.: estadias de 3 noites ou mais, de domingo a quinta'}
  ]},
 {kind:'feedback', title:'Suas respostas a objeções',
  metrics:function(s,c){return [{label:'Objeções mapeadas',value:String(c.objN),tag:'informado'},{label:'Custo do desconto máximo por reserva',value:F.brl(c.descValor),tag:'calculado'}];},
  feedback:function(s,c){var o=[];var d=s.n('ob_desconto',0);
   if(d>0&&!String(s.t('ob_desc_regra')).trim()) o.push({lv:'warn',t:'Você aceita até '+F.pct(d,0)+' de desconto, mas sem regra definida. Sem regra, o desconto vira padrão. Defina para quais datas ou estadias ele vale.'});
   if(d>0) o.push({lv:'info',t:'Cada reserva com o desconto máximo deixa de faturar cerca de '+F.brl(c.descValor)+'. Use-o como ferramenta para ocupar datas fracas, não como resposta automática.'});
   if(d>=20) o.push({lv:'warn',t:'Desconto de '+F.pct(d,0)+' é alto. Confira se o valor final ainda cobre seus custos (o produto A02 calcula sua diária mínima).'});
   if(!c.objN) o.push({lv:'info',t:'Marque as objeções que você ouve para receber as respostas prontas.'});
   else o.push({lv:'ok',t:'Respostas montadas para '+c.objN+' objeção(ões). Elas estão abaixo e no seu playbook final.'});
   return o;},
  extra:function(s,c){var a=arr(s,'ob_lista');if(!a.length)return '';return '<h2>Respostas prontas</h2>'+a.map(function(k){return '<p><b>'+esc(OBJ.filter(function(x){return x.v===k;})[0].l)+'</b></p>'+msg(sObj(s,c,k));}).join('');}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Salvar as respostas a objeções como mensagens rápidas'},{id:'a5_2',text:'Definir por escrito a regra e o limite de desconto'},{id:'a5_3',text:'Responder “vou pensar” sempre com prazo e oferta de ajuda'}]}
]},
/* 6 */
{title:'Acompanhamento', screens:[
 {kind:'learn', title:'O silêncio do hóspede não é um “não”',
  body:'<p>Muitas consultas morrem por esquecimento, não por desinteresse: o hóspede se distraiu, esperou falar com o parceiro ou deixou para depois. Um <b>acompanhamento (follow-up)</b> educado relembra a proposta e mostra atenção.</p><p>O roteiro recomendado tem dois contatos: o <b>primeiro</b>, algumas horas depois da proposta, perguntando se ficou alguma dúvida; o <b>segundo</b>, perto do fim do prazo em que as datas ficam guardadas, avisando com honestidade que a pré-reserva vai expirar. Sem pressão inventada: nada de “últimas vagas” se não for verdade.</p>',
  example:'Exemplo ilustrativo: proposta enviada às 10h, primeiro acompanhamento às 18h (“ficou alguma dúvida?”), segundo no dia seguinte às 9h (“hoje às 10h encerro a pré-reserva”). Depois disso, a conversa é encerrada com gentileza.'},
 {kind:'compare', title:'Insistir × acompanhar',
  cols:[{h:'Insistir',type:'bad',items:['Mensagem todo dia até o hóspede responder','Urgência falsa (“só resta uma vaga”)','Tom de cobrança','Nenhum prazo para encerrar']},
        {h:'Acompanhar',type:'good',items:['Dois contatos com intervalo definido','Prazo real de pré-reserva','Tom de ajuda (“ficou alguma dúvida?”)','Encerramento gentil, porta aberta']}]},
 {kind:'form', title:'Seu roteiro de acompanhamento',
  fields:[
   {id:'fu_pratica',label:'Você faz acompanhamento hoje?',type:'radio',required:true,options:[{v:'nunca',l:'Nunca: espero o hóspede responder'},{v:'as_vezes',l:'Às vezes, quando lembro'},{v:'sempre',l:'Sempre, com um roteiro'}]},
   {id:'fu_horas',label:'Quantas horas depois da proposta, sem resposta, você fará o primeiro acompanhamento?',type:'number',required:true,min:1,max:168,step:1,unit:'horas'},
   {id:'fu_validade',label:'Por quantas horas você segura as datas da proposta?',type:'number',required:true,min:1,max:168,step:1,unit:'horas'}
  ]},
 {kind:'feedback', title:'Seu roteiro de acompanhamento',
  metrics:function(s,c){return [{label:'1º acompanhamento',value:F.num(s.n('fu_horas'))+' h após a proposta',tag:'informado'},{label:'Validade da pré-reserva',value:F.num(s.n('fu_validade'))+' h',tag:'informado'},{label:'Pontuação de acompanhamento',value:F.num(c.fuScore,0)+' / 100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];var h=s.n('fu_horas',0),v=s.n('fu_validade',0);
   if(s.t('fu_pratica')==='nunca') o.push({lv:'bad',t:'Sem acompanhamento, as '+F.num(c.perdidas)+' consultas não convertidas do mês ficam sem uma segunda chance.'});
   else if(s.t('fu_pratica')==='as_vezes') o.push({lv:'warn',t:'Acompanhamento ocasional depende da memória. Com o roteiro abaixo, ele vira rotina.'});
   else o.push({lv:'ok',t:'Você já acompanha as propostas. Padronize os textos com os modelos abaixo.'});
   if(h>=v) o.push({lv:'warn',t:'O primeiro acompanhamento ('+F.num(h)+' h) acontece depois ou junto do fim da pré-reserva ('+F.num(v)+' h). Faça o contato antes do prazo expirar.'});
   if(h>24) o.push({lv:'info',t:'Esperar mais de 24 horas para o primeiro contato é longo: o hóspede pode já ter decidido.'});
   return o;},
  extra:function(s){return '<h2>Acompanhamento 1 · '+F.num(s.n('fu_horas'))+' h após a proposta</h2>'+msg(sFollow1(s))+'<h2>Acompanhamento 2 · antes do fim da pré-reserva</h2>'+msg(sFollow2(s));}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Marcar no celular um lembrete para cada proposta enviada'},{id:'a6_2',text:'Usar os dois acompanhamentos em todas as propostas sem resposta'},{id:'a6_3',text:'Nunca usar urgência falsa: prazo de pré-reserva real e informado'}]}
]},
/* 7 */
{title:'Indicadores e melhoria', screens:[
 {kind:'learn', title:'O que não é registrado não melhora',
  body:'<p>Três números bastam para acompanhar o atendimento todo mês: <b>consultas</b>, <b>reservas</b> e <b>taxa de conversão</b>. Se der, anote também o <b>motivo das perdas</b> (preço, datas, sem resposta, escolheu outro).</p><p>Com uma meta de conversão, a ferramenta estima quanto de receita a melhoria representaria. É uma estimativa para orientar o esforço, e não uma promessa: a conversão também depende de preço, datas e concorrência.</p>',
  example:'Exemplo ilustrativo: 40 consultas por mês, conversão de 15% para 25% = 4 reservas a mais. Com reserva média de R$ 700, isso equivale a cerca de R$ 2.800 por mês, se as demais condições se mantiverem.'},
 {kind:'compare', title:'Sensação × indicador',
  cols:[{h:'Sensação',type:'bad',items:['“Esse mês foi fraco”','Não sabe por que perdeu','Muda o preço por impulso','Compara com o vizinho']},
        {h:'Indicador',type:'good',items:['Consultas, reservas e conversão do mês','Motivo de cada perda anotado','Muda uma coisa por vez e mede','Compara com o próprio mês anterior']}]},
 {kind:'form', title:'Sua meta e seu controle',
  fields:[
   {id:'in_meta',label:'Meta de conversão consulta → reserva',type:'percent',required:true,min:1,max:100,help:'Defina uma meta próxima da sua realidade e revise depois de 3 meses.'},
   {id:'in_registro',label:'Onde você vai registrar os números?',type:'radio',required:true,options:[{v:'planilha',l:'Planilha ou aplicativo'},{v:'caderno',l:'Caderno'},{v:'nao',l:'Ainda não sei'}]},
   {id:'in_revisao',label:'Com que frequência você vai revisar?',type:'radio',required:true,options:[{v:'semanal',l:'Semanal'},{v:'quinzenal',l:'Quinzenal'},{v:'mensal',l:'Mensal'}]}
  ]},
 {kind:'feedback', title:'O que a meta representa',
  metrics:function(s,c){return [{label:'Conversão atual',value:c.conv==null?'—':F.pct(c.conv*100),tag:'calculado'},{label:'Meta',value:F.pct(c.meta*100,0),tag:'informado'},{label:'Reservas/mês na meta',value:F.num(c.resMeta,1),tag:'estimativa'},{label:'Receita não capturada/mês',value:F.brl(c.ganhoMeta),tag:'estimativa'}];},
  feedback:function(s,c){var o=[];
   if(c.conv!=null&&c.meta<=c.conv) o.push({lv:'ok',t:'Sua conversão atual já atinge a meta. Use o playbook para manter o padrão e teste uma meta um pouco maior daqui a 3 meses.'});
   else o.push({lv:'info',t:'Chegar a '+F.pct(c.meta*100,0)+' de conversão com o mesmo volume de consultas representaria cerca de <b>'+F.num(c.resMeta-c.res,1)+' reservas a mais</b> e <b>'+F.brl(c.ganhoMeta)+'</b> por mês ('+F.brl(c.ganhoMetaAno)+' por ano). Estimativa, não garantia.'});
   if(c.conv!=null&&c.meta-c.conv>0.2) o.push({lv:'warn',t:'A meta está mais de 20 pontos acima da conversão atual. Considere uma meta intermediária para os próximos 3 meses.'});
   if(s.t('in_registro')==='nao') o.push({lv:'warn',t:'Sem um lugar para registrar, a meta não pode ser acompanhada. Uma planilha simples com 3 colunas já resolve.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Criar a planilha de consultas, reservas, conversão e motivo das perdas'},{id:'a7_2',text:'Revisar os números na frequência definida e ajustar um script por vez'},{id:'a7_3',text:'Refazer o Assistente em 30 dias com os números reais'}]}
]}
],

compute:function(s){
 var c={};
 c.cons=s.n('cv_consultas',0); c.res=s.n('cv_reservas',0);
 c.conv=c.cons>0?c.res/c.cons:null;
 c.diaria=s.n('cv_diaria',0); c.est=s.n('cv_estadia',2)||2;
 c.valorRes=c.diaria*c.est;
 c.perdidas=Math.max(0,c.cons-c.res);
 c.receitaAtual=c.res*c.valorRes;
 c.meta=s.n('in_meta',0)/100;
 c.resMeta=c.cons*c.meta;
 c.ganhoMeta=Math.max(0,c.resMeta-c.res)*c.valorRes; c.ganhoMetaAno=c.ganhoMeta*12;
 c.valorPP=c.cons*0.01*c.valorRes;
 c.descValor=c.valorRes*s.n('ob_desconto',0)/100;
 var t=s.n('at_tempo'); c.tempoScore=t==null?50:(t<=5?100:t<=30?75:t<=120?50:20);
 c.primeiraScore={acolhe:100,preco_pergunta:60,preco:20}[s.t('at_primeira')]||20;
 c.pergN=arr(s,'ne_perguntas').length; c.pergScore=c.pergN/6*100;
 c.difN=difs(s).length;
 c.ofertaScore=0.6*({fotos:100,texto_completo:75,texto_preco:25}[s.t('of_formato')]||25)+0.4*(c.difN/3*100);
 c.objN=arr(s,'ob_lista').length;
 c.fuScore={sempre:100,as_vezes:50,nunca:0}[s.t('fu_pratica')]||0;
 c.regScore={planilha:100,caderno:60,nao:0}[s.t('in_registro')]||0;
 c.etapas=[{nome:'Tempo de resposta',v:c.tempoScore},{nome:'Primeira resposta',v:c.primeiraScore},{nome:'Qualificação',v:c.pergScore},{nome:'Proposta',v:c.ofertaScore},{nome:'Acompanhamento',v:c.fuScore},{nome:'Registro e indicadores',v:c.regScore}];
 c.prontidao=0; c.etapas.forEach(function(e){c.prontidao+=e.v/6;});
 c.etapaMin=c.etapas.slice().sort(function(a,b){return a.v-b.v;})[0];
 // simulação de conversão
 var self=c; c.sim=[['Atual',c.conv==null?0:c.conv],['Atual + 5 p.p.',Math.min(1,(c.conv||0)+0.05)],['Meta',c.meta]].map(function(x){var r=self.cons*x[1];return {nome:x[0],conv:x[1],res:r,receita:r*self.valorRes};});
 return c;
},

metrics:function(s,c){return [
 {label:'Taxa de conversão',value:c.conv==null?'—':F.pct(c.conv*100),tag:'calculado'},
 {label:'Consultas/mês',value:F.num(c.cons),tag:'informado'},
 {label:'Reservas/mês',value:F.num(c.res),tag:'informado'},
 {label:'Valor médio de uma reserva',value:F.brl(c.valorRes),tag:s.unknown('cv_estadia')?'estimativa':'calculado'},
 {label:'Meta de conversão',value:F.pct(c.meta*100,0),tag:'informado'},
 {label:'Receita não capturada/mês (até a meta)',value:F.brl(c.ganhoMeta),tag:'estimativa'},
 {label:'Índice de prontidão comercial',value:F.num(c.prontidao,0)+' / 100',tag:'calculado'},
 {label:'Etapa mais fraca do atendimento',value:c.etapaMin.nome,tag:'calculado'}
];},

priorities:function(s,c){var L=[];
 if(s.t('at_primeira')==='preco') L.push({title:'Trocar a resposta-preço pela resposta-conversa',why:'Hoje a primeira mensagem leva o hóspede a comparar só preço.',score:9});
 if(s.t('fu_pratica')==='nunca') L.push({title:'Implantar os dois acompanhamentos em toda proposta sem resposta',why:F.num(c.perdidas)+' consultas por mês não recebem uma segunda chance.',score:9});
 else if(s.t('fu_pratica')==='as_vezes') L.push({title:'Transformar o acompanhamento em rotina com lembretes',why:'Hoje depende da memória.',score:6});
 if(s.n('at_tempo')!=null&&s.n('at_tempo')>120) L.push({title:'Reduzir o tempo da primeira resposta',why:'Hoje cerca de '+F.num(s.n('at_tempo'))+' minutos.',score:8});
 else if(s.n('at_tempo')!=null&&s.n('at_tempo')>30) L.push({title:'Responder em até 30 minutos com uma mensagem de acolhimento',why:'Tempo atual de cerca de '+F.num(s.n('at_tempo'))+' minutos.',score:5});
 if(s.unknown('at_tempo')) L.push({title:'Medir o tempo de resposta durante uma semana',why:'Dado desconhecido; o índice usa hipótese.',score:4});
 if(c.pergN<=2) L.push({title:'Fazer as perguntas de qualificação antes da proposta',why:'Só '+c.pergN+' perguntas hoje; a proposta fica genérica.',score:7});
 if(arr(s,'ne_perguntas').indexOf('ocasiao')<0) L.push({title:'Perguntar a ocasião da viagem em toda consulta',why:'É o dado que mais personaliza a proposta.',score:6});
 if(s.t('of_formato')==='texto_preco') L.push({title:'Enviar a proposta completa (total, incluso, diferenciais e prazo)',why:'Hoje só o valor é enviado.',score:8});
 else if(s.t('of_formato')==='texto_completo') L.push({title:'Anexar fotos ou vídeo curto à proposta',why:'Ajuda o hóspede a se imaginar no lugar.',score:3});
 if(c.difN<3) L.push({title:'Definir três diferenciais concretos para a proposta',why:'Só '+c.difN+' informado(s).',score:5});
 if(s.n('ob_desconto',0)>0&&!String(s.t('ob_desc_regra')).trim()) L.push({title:'Criar regra e limite para o desconto',why:'Sem regra, o desconto vira o novo preço.',score:6});
 if(c.objN>=3) L.push({title:'Salvar as respostas às objeções como mensagens rápidas',why:c.objN+' objeções frequentes mapeadas.',score:5});
 if(s.t('in_registro')==='nao') L.push({title:'Registrar consultas, reservas e motivos de perda todo mês',why:'Sem registro não há como medir a melhoria.',score:7});
 if(c.conv!=null&&c.meta>c.conv&&c.ganhoMeta>0) L.push({title:'Perseguir a meta de '+F.pct(c.meta*100,0)+' de conversão',why:'Estimativa de '+F.brl(c.ganhoMeta)+' por mês não capturados hoje.',score:c.conv<0.1?8:6});
 if(s.n('fu_horas',0)>=s.n('fu_validade',0)) L.push({title:'Fazer o 1º acompanhamento antes de a pré-reserva expirar',why:'O prazo atual de contato é igual ou maior que a validade.',score:5});
 return L;},

report:function(s,c){
 var tg=function(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';};
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Consultas por mês',F.num(c.cons),tg('informado')],
  ['Reservas por mês',F.num(c.res),tg('informado')],
  ['Diária média',F.brl(c.diaria),tg('informado')],
  ['Estadia média',F.num(c.est,1)+' noites',s.unknown('cv_estadia')?tg('hipotese'):tg('informado')],
  ['Valor médio de uma reserva',F.brl(c.valorRes),tg('calculado')],
  ['Meta de conversão',F.pct(c.meta*100,0),tg('informado')],
  ['Receita não capturada','(reservas na meta − reservas atuais) × valor médio da reserva; mantidos consultas e preço',tg('estimativa')],
  ['Tempo de resposta usado no índice',s.unknown('at_tempo')?'desconhecido (50 pontos)':F.num(s.n('at_tempo'))+' min',s.unknown('at_tempo')?tg('hipotese'):tg('informado')]],[]);
 var sim=ZA.table(['Situação','Conversão','Reservas/mês','Receita/mês das reservas'],c.sim.map(function(x){return [x.nome,F.pct(x.conv*100),F.num(x.res,1),F.brl(x.receita)];}),[1,2,3]);
 var etp=ZA.table(['Etapa do atendimento','Pontuação'],c.etapas.map(function(e){return [e.nome,F.num(e.v,0)+' / 100'];}).concat([['<b>Índice de prontidão comercial</b>','<b>'+F.num(c.prontidao,0)+' / 100</b>']]),[1]);
 var objs=arr(s,'ob_lista');
 var book='<h3>1. Primeira resposta</h3>'+msg(sPrimeira(s))+'<h3>2. Qualificação</h3>'+msg(sQualif(s))+'<h3>3. Proposta</h3>'+msg(sOferta(s,c))+
  '<h3>4. Respostas a objeções</h3>'+(objs.length?objs.map(function(k){return '<p><b>'+esc(OBJ.filter(function(x){return x.v===k;})[0].l)+'</b></p>'+msg(sObj(s,c,k));}).join(''):'<p class="za-small">Nenhuma objeção marcada. Modelo para “vou pensar”:</p>'+msg(sObj(s,c,'pensar')))+
  '<h3>5. Acompanhamento 1 ('+F.num(s.n('fu_horas'))+' h após a proposta)</h3>'+msg(sFollow1(s))+'<h3>6. Acompanhamento 2 (antes de '+F.num(s.n('fu_validade'))+' h)</h3>'+msg(sFollow2(s))+'<h3>7. Confirmação da reserva</h3>'+msg(sConfirma(s))+
  '<p class="za-small">Campos entre colchetes são preenchidos em cada conversa. Adapte o tom ao seu jeito de falar e mantenha as informações sempre verdadeiras.</p>';
 var ctrl='<div class="za-card"><p><b>Registro:</b> '+({planilha:'planilha ou aplicativo',caderno:'caderno',nao:'a definir (sugestão: planilha)'}[s.t('in_registro')]||'a definir')+' · <b>Revisão:</b> '+({semanal:'semanal',quinzenal:'quinzenal',mensal:'mensal'}[s.t('in_revisao')]||'—')+'</p><p>Colunas sugeridas: data · canal · datas pedidas · nº de pessoas · ocasião · proposta enviada (s/n) · acompanhamentos · resultado · motivo da perda.</p></div>';
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido de 30 dias</b><ol><li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Salvar os scripts como mensagens rápidas')+'; começar o registro de consultas e reservas.</li><li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Aplicar a proposta completa em todas as consultas')+'.</li><li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Aplicar os dois acompanhamentos')+'.</li><li><b>Semana 4:</b> calcular a conversão do mês, comparar com '+(c.conv==null?'o ponto de partida':F.pct(c.conv*100))+' e ajustar um script por vez.</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Simulação de conversão',html:sim+'<p class="za-small">Mantidos o volume de consultas e o valor médio da reserva. Simulação ilustrativa, não previsão.</p>'},
  {title:'Diagnóstico por etapa do atendimento',html:etp},
  {title:'Playbook de mensagens',html:book},
  {title:'Controle mensal',html:ctrl}
 ],plan:plan};
}
});
})();
