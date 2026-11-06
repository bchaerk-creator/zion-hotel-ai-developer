/* ZAR-A06 · Por Que Seus Hóspedes Não Dão 5 Estrelas? · Auditor Inteligente da Experiência */
(function(){
var F=ZA.fmt, esc=ZA.esc;
var ETAPAS=[['j_reserva','Reserva e decisão'],['j_prechegada','Pré-chegada'],['j_chegada','Chegada e check-in'],['j_acomodacao','Acomodação (limpeza e conforto)'],['j_estadia','Atendimento durante a estadia'],['j_saida','Saída e check-out'],['j_pos','Pós-estadia e avaliação']];
var PI_OPTS=[{v:'acesso',l:'Acesso e caminho sinalizados e iluminados (inclusive à noite)'},{v:'instrucoes',l:'Instruções de chegada enviadas antes, com foto ou vídeo'},{v:'entrada',l:'Entrada e área externa limpas e organizadas'},{v:'aroma',l:'Ambiente arejado, sem cheiro de mofo, fumaça ou produto forte'},{v:'temperatura',l:'Temperatura agradável na chegada (aquecido ou ventilado)'},{v:'boasvindas',l:'Gesto de boas-vindas (bilhete, mimo, recepção)'}];
var LIMP_OPTS=[{v:'checklist',l:'Checklist de limpeza escrito, por cômodo'},{v:'banheiro',l:'Inspeção final do banheiro (ralo, box, cabelos, espelho)'},{v:'enxoval',l:'Enxoval trocado, sem manchas e sem odor'},{v:'cozinha',l:'Cozinha, geladeira e utensílios conferidos'},{v:'pragas',l:'Controle periódico de insetos e pragas'},{v:'vistoria',l:'Vistoria final por outra pessoa ou com fotos'}];
var CONF_OPTS=[{v:'colchao',l:'Colchão firme, sem afundamento'},{v:'travesseiros',l:'Opções de travesseiro (alto/baixo)'},{v:'blackout',l:'Quarto escurece bem (cortina blackout)'},{v:'chuveiro',l:'Água quente com boa pressão'},{v:'silencio',l:'Pouco ruído (vizinhos, estrada, equipamentos)'},{v:'clima',l:'Aquecimento ou ventilação adequados ao clima'}];
var PERS_OPTS=[{v:'nome',l:'Chama o hóspede pelo nome'},{v:'ocasiao',l:'Pergunta o motivo da viagem'},{v:'dicas',l:'Envia dicas locais de acordo com o perfil'},{v:'surpresa',l:'Prepara um gesto para datas especiais'}];
var MSG_OPTS=[{v:'confirmacao',l:'Confirmação logo após a reserva'},{v:'prechegada',l:'Guia pré-chegada (2 a 3 dias antes)'},{v:'acesso',l:'Instruções de acesso no dia da chegada'},{v:'primeiro_dia',l:'Mensagem no dia seguinte à chegada (“está tudo bem?”)'},{v:'precheckout',l:'Orientações de check-out na véspera'},{v:'posestadia',l:'Agradecimento e pedido de avaliação após a saída'}];
var PB_OPTS=[{v:'contatos',l:'Lista de técnicos de confiança (encanador, eletricista, internet)'},{v:'pecas',l:'Peças de reposição à mão (lâmpadas, pilhas, resistência, fusíveis)'},{v:'alternativa',l:'Plano alternativo (aquecedor extra, roteador reserva, gás reserva)'},{v:'registro',l:'Registro escrito de cada ocorrência e da solução'}];
var NOTAS=[{v:'1',l:'1 · muito fraca'},{v:'2',l:'2 · fraca'},{v:'3',l:'3 · mediana'},{v:'4',l:'4 · boa'},{v:'5',l:'5 · excelente'}];
function nota(s,id){var x=Number(s.t(id));return (x>=1&&x<=5)?x:1;}
function lbl(opts,v){for(var i=0;i<opts.length;i++) if(opts[i].v===v) return opts[i].l; return v;}
function arr(s,id){return Array.isArray(s.v[id])?s.v[id]:[];}
function faltam(s,id,opts){var a=arr(s,id);return opts.filter(function(o){return a.indexOf(o.v)<0;});}
function classe(i){return i>=80?'sólida':i>=60?'boa, com lacunas':i>=40?'irregular':'crítica';}

ZA.register({
id:'A06', code:'ZAR-A06', collection:'Hospedagem',
title:'Por Que Seus Hóspedes Não Dão 5 Estrelas?',
subtitle:'Aprenda a Criar uma Experiência Memorável',
tool:'Auditor Inteligente da Experiência',
deliverable:'Plano de Qualidade e Experiência',
nameField:'nome', propertyField:'propriedade',
disclaimer:'O Índice de Experiência Zion é uma autoavaliação orientativa construída a partir das suas respostas; ele não reproduz o algoritmo de nenhuma plataforma. Avaliações dependem da percepção de cada hóspede: não há garantia de nota, avaliações positivas ou reservas.',

intro:[
 {kind:'mirror', title:'O que seu hóspede percebe que você ainda não percebeu?',
  lead:'Você caprichou na decoração, tirou fotos bonitas e cuida de tudo com carinho. Mesmo assim, aparecem 4 estrelas, comentários com “mas” e aquela avaliação que tira seu sono.',
  body:'<div class="za-card"><p>Talvez você se reconheça em alguma destas situações:</p><ul><li>“O hóspede elogiou a vista, mas reclamou do chuveiro.”</li><li>“Ninguém reclamou comigo durante a estadia, só na avaliação.”</li><li>“Eu sei que a limpeza é boa, mas sempre aparece um cabelo no box.”</li><li>“Não sei se o problema é a casa, o atendimento ou a chegada.”</li></ul></div>'},
 {kind:'collapse', title:'Uma hospedagem bonita não compensa uma experiência mal executada.',
  lead:'O hóspede não avalia a foto. Ele avalia cada momento: a mensagem que chegou (ou não), o caminho no escuro, o travesseiro, a resposta quando o Wi-Fi caiu.',
  body:'<div class="za-card"><p>A nota final é a soma de pequenos momentos. Um único ponto fraco, repetido em várias estadias, puxa a média para baixo mesmo quando o resto é ótimo.</p><p>Por isso, em vez de “melhorar tudo”, você vai <b>auditar a jornada etapa por etapa</b>, descobrir onde estão as falhas que se repetem e montar um plano de qualidade com padrões simples.</p></div>'},
 {kind:'start', title:'Vamos auditar a experiência da sua hospedagem',
  lead:'Em 7 pilares, você vai dar notas à jornada do hóspede, revisar primeira impressão, limpeza, atendimento, comunicação e problemas, e sair com um Plano de Qualidade.',
  body:'<p>Tenha à mão, se possível: suas últimas avaliações, as mensagens trocadas com hóspedes e o número de estadias dos últimos 6 meses. Se não tiver um dado, marque “não sei”: o relatório indica o que ficou como hipótese.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Ana'},
   {id:'propriedade',label:'Nome da hospedagem',type:'text',required:true,placeholder:'Ex.: Chalé Recanto da Serra'},
   {id:'tipo',label:'Tipo de hospedagem',type:'select',required:true,options:[{v:'airbnb',l:'Apartamento ou casa (Airbnb/temporada)'},{v:'cabana',l:'Cabana ou chalé'},{v:'glamping',l:'Glamping'},{v:'pousada',l:'Pequena pousada'},{v:'outro',l:'Outro'}]},
   {id:'destino',label:'Cidade / destino',type:'text',required:true,placeholder:'Ex.: Monte Verde (MG)'},
   {id:'unidades',label:'Quantas unidades você opera?',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)'},
   {id:'nota_media',label:'Nota média atual nas avaliações (escala de 0 a 5)',type:'number',required:true,min:0,max:5,step:0.01,allowUnknown:true,help:'Se você usa mais de uma plataforma, informe a da principal. Se a escala for 0 a 10, divida por 2.'}
  ]}
],

pillars:[
/* 1 */
{title:'Jornada do hóspede', screens:[
 {kind:'learn', title:'A experiência começa antes da chegada e termina depois da saída',
  body:'<p>O hóspede vive sua hospedagem em <b>7 etapas</b>: a decisão e a reserva, a espera até a viagem (pré-chegada), a chegada, a acomodação, o atendimento durante a estadia, a saída e o pós-estadia, quando ele escreve a avaliação.</p><p>Cada etapa gera uma lembrança. A avaliação costuma refletir <b>a etapa mais marcante</b>, boa ou ruim, e não a média de todas. Por isso, uma chegada confusa pode “apagar” uma estadia excelente.</p><p>Neste pilar você dá uma nota honesta, de 1 a 5, para cada etapa. A ferramenta transforma essas notas em um índice de 0 a 100 e mostra onde está o elo mais fraco.</p>',
  example:'Exemplo ilustrativo: notas 5, 5, 2, 5, 4, 4 e 3. A média é 4, mas a nota 2 na chegada é o ponto que tende a aparecer nas avaliações (“difícil de achar”, “chegamos no escuro”).'},
 {kind:'compare', title:'Olhar para a hospedagem × olhar para a jornada',
  cols:[{h:'Visão da hospedagem',type:'bad',items:['“A casa é linda, então a nota deveria ser 5”','Melhorias só em decoração e objetos','Só descobre problemas na avaliação','Trata cada reclamação como caso isolado']},
        {h:'Visão da jornada',type:'good',items:['Cada etapa tem um responsável e um padrão','Melhorias onde o hóspede sente o atrito','Pergunta durante a estadia, antes da avaliação','Procura falhas que se repetem']}]},
 {kind:'form', title:'Dê uma nota para cada etapa da jornada', intro:'Pense nas últimas estadias e nos comentários recebidos. Seja honesto: 1 = muito fraca, 5 = excelente.',
  fields:ETAPAS.map(function(e){return {id:e[0],label:e[1],type:'radio',required:true,options:NOTAS};})},
 {kind:'feedback', title:'O retrato da sua jornada',
  metrics:function(s,c){return [{label:'Média das etapas',value:F.num(c.jMedia,2)+' de 5',tag:'calculado'},{label:'Índice da jornada',value:F.num(c.D1,0)+' / 100',tag:'calculado'},{label:'Etapa mais fraca',value:c.jMin?c.jMin.nome:'—',tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.jMin&&c.jMin.nota<=2) o.push({lv:'bad',t:'A etapa <b>'+c.jMin.nome+'</b> recebeu nota '+c.jMin.nota+'. É o elo mais fraco da jornada e o primeiro candidato ao seu plano de qualidade.'});
   else if(c.jMin&&c.jMin.nota===3) o.push({lv:'warn',t:'Nenhuma etapa está crítica, mas <b>'+c.jMin.nome+'</b> ficou com nota 3. Etapas “medianas” costumam gerar avaliações de 4 estrelas.'});
   else if(c.jMin) o.push({lv:'ok',t:'Todas as etapas com nota 4 ou mais. O trabalho agora é manter o padrão e confirmar com os hóspedes se a sua percepção é a mesma deles.'});
   if(c.jFracas>=3) o.push({lv:'warn',t:'Você tem '+c.jFracas+' etapas com nota 3 ou menos. Não tente corrigir todas ao mesmo tempo: o OP3D no final vai indicar por onde começar.'});
   if(c.nota!=null&&c.jMedia>=4.5&&c.nota<4.6) o.push({lv:'info',t:'Sua autoavaliação ('+F.num(c.jMedia,1)+') está acima da nota que os hóspedes dão ('+F.num(c.nota,2)+'). Releia as avaliações com 4 estrelas ou menos: elas mostram o que você ainda não está vendo.'});
   if(c.nota==null) o.push({lv:'warn',t:'Sem a nota média atual, não dá para comparar sua percepção com a dos hóspedes. Consulte o painel da plataforma.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Reler as últimas 20 avaliações e anotar em qual etapa cada crítica aconteceu'},{id:'a1_2',text:'Fazer o percurso completo como se fosse um hóspede (da reserva à saída)'},{id:'a1_3',text:'Definir um responsável para cada etapa da jornada'}]}
]},
/* 2 */
{title:'Primeira impressão', screens:[
 {kind:'learn', title:'Os primeiros 10 minutos definem o humor da estadia',
  body:'<p>A primeira impressão acontece em sequência: <b>achar o lugar → entrar → sentir o ambiente</b>. Se o hóspede se perde no caminho, espera do lado de fora ou entra num ambiente frio e com cheiro de fechado, ele passa o resto da estadia procurando defeitos.</p><p>Quando a chegada é fácil e acolhedora, acontece o contrário: pequenos detalhes passam despercebidos. Os pontos de controle são simples: <b>acesso, instruções, entrada, cheiro, temperatura e boas-vindas</b>.</p>',
  example:'Exemplo ilustrativo: um chalé com estrada de terra sem placa. Um vídeo de 40 segundos mostrando o caminho a partir da última referência (posto, igreja, ponte) e uma luz acesa na entrada resolvem a maior parte das chegadas difíceis, a um custo baixo.'},
 {kind:'compare', title:'Chegada que gera tensão × chegada que acolhe',
  cols:[{h:'Gera tensão',type:'bad',items:['Endereço só pelo GPS, que erra o último trecho','Senha ou chave explicadas só por texto','Casa fechada há dias: cheiro de mofo e frio','Nenhum sinal de que alguém esperava o hóspede']},
        {h:'Acolhe',type:'good',items:['Vídeo ou fotos do caminho e ponto de referência','Instrução de acesso testada por alguém de fora','Casa arejada e na temperatura certa antes da chegada','Bilhete com o nome do hóspede e um mimo simples']}]},
 {kind:'form', title:'Como é a chegada hoje', intro:'Marque apenas o que acontece <b>em todas</b> as chegadas, não só às vezes.',
  fields:[
   {id:'pi_itens',label:'O que já está garantido na chegada',type:'checks',options:PI_OPTS},
   {id:'pi_espera',label:'Quanto tempo o hóspede costuma levar entre chegar ao portão e estar acomodado?',type:'number',required:true,min:0,max:180,step:1,unit:'minutos',allowUnknown:true,help:'Inclua tempo procurando a entrada, esperando alguém ou tentando abrir a fechadura.'}
  ]},
 {kind:'feedback', title:'Sua primeira impressão',
  metrics:function(s,c){return [{label:'Pontos garantidos',value:c.piN+' de 6',tag:'informado'},{label:'Índice de primeira impressão',value:F.num(c.D2,0)+' / 100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];var f=faltam(s,'pi_itens',PI_OPTS);
   if(c.piN<=2) o.push({lv:'bad',t:'Só '+c.piN+' dos 6 pontos de chegada estão garantidos. A primeira impressão está ficando por conta da sorte.'});
   else if(c.piN<6) o.push({lv:'warn',t:'Faltam '+f.length+' pontos para uma chegada sem atrito: '+f.map(function(x){return x.l.toLowerCase();}).join('; ')+'.'});
   else o.push({lv:'ok',t:'Todos os pontos de chegada estão garantidos. Mantenha-os no checklist para não depender da memória.'});
   if(arr(s,'pi_itens').indexOf('instrucoes')<0) o.push({lv:'warn',t:'Sem instruções de chegada com imagem, o GPS e a ansiedade do hóspede decidem a primeira impressão.'});
   var e=s.n('pi_espera');
   if(e!=null&&e>15) o.push({lv:'bad',t:'O hóspede leva cerca de '+F.num(e)+' minutos para se acomodar. Depois de horas de viagem, isso pesa. Procure onde está o atraso: caminho, chave ou espera.'});
   else if(e!=null&&e>5) o.push({lv:'info',t:'Cerca de '+F.num(e)+' minutos para se acomodar. Dá para reduzir com instruções mais claras e acesso testado.'});
   if(s.unknown('pi_espera')) o.push({lv:'info',t:'Você não sabe quanto tempo leva a chegada. Pergunte aos próximos hóspedes: “foi fácil chegar e entrar?”.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Gravar um vídeo curto do caminho e da entrada e enviar antes da chegada'},{id:'a2_2',text:'Pedir para alguém de fora testar as instruções de acesso sem ajuda'},{id:'a2_3',text:'Incluir no checklist: arejar, ajustar a temperatura e deixar a luz da entrada acesa'}]}
]},
/* 3 */
{title:'Limpeza e conforto', screens:[
 {kind:'learn', title:'Limpeza não é opinião: é processo e conferência',
  body:'<p>Limpeza é o tema que mais gera frustração porque o hóspede espera perfeição e qualquer falha é visível: um cabelo, uma mancha, uma panela engordurada. Quem limpa todo dia deixa de enxergar detalhes, por isso a limpeza precisa de <b>checklist escrito</b> e de <b>conferência final</b>.</p><p>Conforto é o segundo pilar da acomodação: <b>dormir bem</b> (colchão, travesseiro, escuro, silêncio, temperatura) e <b>tomar um bom banho</b>. São pontos que o hóspede não vê nas fotos, mas sente na primeira noite.</p>',
  example:'Exemplo ilustrativo: a pessoa da limpeza termina e envia 6 fotos padronizadas (cama, banheiro, ralo do box, pia da cozinha, geladeira aberta, sala). Em 2 minutos você confere à distância, sem precisar ir até a unidade.'},
 {kind:'compare', title:'Limpeza de memória × limpeza com padrão',
  cols:[{h:'De memória',type:'bad',items:['“Ela já sabe o que fazer”','Ninguém confere depois','Enxoval usado até rasgar','Colchão trocado só quando alguém reclama']},
        {h:'Com padrão',type:'good',items:['Checklist por cômodo, sempre igual','Fotos ou vistoria final antes de liberar a unidade','Enxoval com rodízio e descarte planejado','Itens de conforto revisados a cada temporada']}]},
 {kind:'form', title:'Seu padrão de limpeza e conforto', intro:'Marque o que já acontece <b>em toda troca de hóspede</b> ou está garantido na unidade.',
  fields:[
   {id:'lc_limpeza',label:'Limpeza',type:'checks',options:LIMP_OPTS},
   {id:'lc_conforto',label:'Conforto',type:'checks',options:CONF_OPTS}
  ]},
 {kind:'feedback', title:'Acomodação: o que está garantido',
  metrics:function(s,c){return [{label:'Itens de limpeza',value:c.limpN+' de 6',tag:'informado'},{label:'Itens de conforto',value:c.confN+' de 6',tag:'informado'},{label:'Índice de limpeza e conforto',value:F.num(c.D3,0)+' / 100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];var a=arr(s,'lc_limpeza');
   if(a.indexOf('checklist')<0) o.push({lv:'bad',t:'Não há checklist de limpeza escrito. Sem ele, a qualidade depende de quem limpa e do dia. É o primeiro padrão a criar.'});
   if(a.indexOf('vistoria')<0) o.push({lv:'warn',t:'Ninguém confere a unidade depois da limpeza. Uma vistoria rápida (ou fotos padronizadas) evita que pequenas falhas cheguem ao hóspede.'});
   var fc=faltam(s,'lc_conforto',CONF_OPTS);
   if(fc.length>=3) o.push({lv:'warn',t:'Faltam '+fc.length+' itens de conforto: '+fc.map(function(x){return x.l.toLowerCase();}).join('; ')+'. Comece pelo que afeta o sono e o banho.'});
   else if(fc.length) o.push({lv:'info',t:'Para fechar o conforto, faltam: '+fc.map(function(x){return x.l.toLowerCase();}).join('; ')+'.'});
   if(c.limpN>=5&&c.confN>=5) o.push({lv:'ok',t:'Acomodação bem padronizada. Mantenha a revisão a cada temporada.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Escrever o checklist de limpeza por cômodo e imprimir para a equipe'},{id:'a3_2',text:'Adotar fotos padronizadas ou vistoria final antes de liberar a unidade'},{id:'a3_3',text:'Testar colchão, travesseiros, chuveiro e escurecimento dormindo uma noite na unidade'}]}
]},
/* 4 */
{title:'Atendimento', screens:[
 {kind:'learn', title:'Atendimento é estar disponível e fazer o hóspede se sentir único',
  body:'<p>Bom atendimento tem duas partes. A primeira é <b>disponibilidade</b>: responder rápido e ter alguém acessível no horário em que o hóspede precisa (geralmente à noite e no fim de semana). A segunda é <b>personalização</b>: chamar pelo nome, saber o motivo da viagem e usar isso a favor dele.</p><p>O hóspede não espera um hotel cinco estrelas. Ele espera ser tratado como pessoa, e não como “a reserva de sexta”.</p>',
  example:'Exemplo ilustrativo: ao saber que o casal vem comemorar 10 anos de casamento, o anfitrião deixa um bilhete com os nomes e sugere o restaurante com vista. O custo é quase zero; a lembrança vai para a avaliação.'},
 {kind:'compare', title:'Atendimento reativo × atendimento atento',
  cols:[{h:'Reativo',type:'bad',items:['Responde quando dá','Fica inacessível à noite e no domingo','Mensagens iguais para todos','Só fala com o hóspede se ele chamar']},
        {h:'Atento',type:'good',items:['Tempo de resposta definido como padrão','Cobertura combinada para noites e folgas','Usa nome, ocasião e perfil do hóspede','Faz contato no momento certo, sem incomodar']}]},
 {kind:'form', title:'Como você atende hoje',
  fields:[
   {id:'at_resposta',label:'Tempo médio para responder uma mensagem durante a estadia',type:'number',required:true,min:0,max:1440,step:1,unit:'minutos',allowUnknown:true},
   {id:'at_cobertura',label:'Em que horários o hóspede consegue falar com alguém?',type:'radio',required:true,options:[{v:'24h',l:'A qualquer hora, inclusive emergências à noite'},{v:'estendido',l:'Das 7h às 22h, todos os dias'},{v:'comercial',l:'Só em horário comercial'},{v:'irregular',l:'Depende do dia, não há combinado'}]},
   {id:'at_pers',label:'O que você faz para personalizar o atendimento?',type:'checks',options:PERS_OPTS}
  ]},
 {kind:'feedback', title:'Seu atendimento',
  metrics:function(s,c){return [{label:'Pontuação de resposta',value:F.num(c.respScore,0)+' / 100',tag:s.unknown('at_resposta')?'hipotese':'calculado'},{label:'Pontuação de cobertura',value:F.num(c.cobScore,0)+' / 100',tag:'calculado'},{label:'Índice de atendimento',value:F.num(c.D4,0)+' / 100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];var r=s.n('at_resposta');
   if(r==null) o.push({lv:'warn',t:'Tempo de resposta desconhecido: usamos 50 pontos como hipótese. Anote, nas próximas duas semanas, quanto tempo você leva para responder.'});
   else if(r>240) o.push({lv:'bad',t:'Cerca de '+F.num(r)+' minutos para responder. Para quem está hospedado e com um problema, isso parece abandono.'});
   else if(r>60) o.push({lv:'warn',t:'Resposta em cerca de '+F.num(r)+' minutos. Durante a estadia, procure responder em até 1 hora, com uma mensagem curta de “recebi, já vejo”.'});
   else o.push({lv:'ok',t:'Resposta em até 1 hora: bom padrão de disponibilidade.'});
   if(s.t('at_cobertura')==='comercial'||s.t('at_cobertura')==='irregular') o.push({lv:'warn',t:'Fora do horário combinado, o hóspede fica sem ninguém. Problemas costumam acontecer à noite (chuveiro, energia, barulho). Defina pelo menos um contato para emergências.'});
   if(c.persN<=1) o.push({lv:'warn',t:'Pouca personalização. Perguntar o motivo da viagem na confirmação é o jeito mais simples de começar.'});
   else if(c.persN>=3) o.push({lv:'ok',t:'Você personaliza o atendimento em '+c.persN+' pontos. Isso costuma aparecer nas avaliações como “anfitrião atencioso”.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Definir um tempo máximo de resposta durante a estadia e cumpri-lo'},{id:'a4_2',text:'Combinar um contato de emergência para noites e folgas'},{id:'a4_3',text:'Perguntar o motivo da viagem em toda confirmação de reserva'}]}
]},
/* 5 */
{title:'Comunicação', screens:[
 {kind:'learn', title:'Comunicação boa evita a pergunta antes que ela aconteça',
  body:'<p>A maior parte das mensagens que o hóspede envia são <b>dúvidas que poderiam ter sido evitadas</b>: “qual a senha do Wi-Fi?”, “como liga o aquecedor?”, “a que horas é o check-out?”. Cada dúvida é um pequeno atrito.</p><p>A solução é uma <b>sequência de mensagens programadas</b> (confirmação, pré-chegada, acesso, primeiro dia, véspera da saída, pós-estadia) e um <b>manual da casa</b> com tudo o que o hóspede precisa saber. Assim você fala menos e o hóspede se sente mais bem cuidado.</p>',
  example:'Exemplo ilustrativo: a mensagem do dia seguinte à chegada (“Bom dia, Marina! Está tudo certo com a cabana? Se precisar de algo, é só me chamar.”) dá ao hóspede a chance de contar um problema enquanto ainda dá para resolver, e não só na avaliação.'},
 {kind:'compare', title:'Comunicação improvisada × comunicação planejada',
  cols:[{h:'Improvisada',type:'bad',items:['Informação espalhada em várias conversas','Regras da casa só no anúncio','Wi-Fi e equipamentos explicados na hora','Pedido de avaliação esquecido ou insistente']},
        {h:'Planejada',type:'good',items:['Sequência de mensagens com horário definido','Manual da casa impresso e digital','Instruções com foto dos equipamentos','Agradecimento sincero e um pedido de avaliação']}]},
 {kind:'form', title:'Suas mensagens e seu manual',
  fields:[
   {id:'co_msgs',label:'Quais mensagens você envia em toda reserva?',type:'checks',options:MSG_OPTS},
   {id:'co_manual',label:'Você tem um manual da casa?',type:'radio',required:true,options:[{v:'completo',l:'Sim, completo (Wi-Fi, regras, equipamentos, emergências, dicas)'},{v:'parcial',l:'Tenho algumas informações, mas incompletas'},{v:'nao',l:'Não tenho'}]}
  ]},
 {kind:'feedback', title:'Sua comunicação',
  metrics:function(s,c){return [{label:'Mensagens da sequência',value:c.msgN+' de 6',tag:'informado'},{label:'Índice de comunicação',value:F.num(c.D5,0)+' / 100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];var f=faltam(s,'co_msgs',MSG_OPTS);
   if(c.msgN<=2) o.push({lv:'bad',t:'Apenas '+c.msgN+' das 6 mensagens da sequência. O hóspede precisa perguntar para saber o básico.'});
   else if(f.length) o.push({lv:'warn',t:'Faltam na sua sequência: '+f.map(function(x){return x.l.toLowerCase();}).join('; ')+'.'});
   else o.push({lv:'ok',t:'Sequência completa de mensagens. Revise os textos a cada temporada.'});
   if(arr(s,'co_msgs').indexOf('primeiro_dia')<0) o.push({lv:'info',t:'A mensagem do primeiro dia é a que mais ajuda a resolver problemas antes da avaliação. Vale priorizá-la.'});
   if(s.t('co_manual')==='nao') o.push({lv:'warn',t:'Sem manual da casa, cada hóspede depende de você para usar a unidade. Comece com uma página: Wi-Fi, check-out, equipamentos e contatos.'});
   else if(s.t('co_manual')==='parcial') o.push({lv:'info',t:'Complete o manual com as dúvidas que mais chegam por mensagem: elas mostram o que está faltando.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Escrever e programar a sequência das 6 mensagens'},{id:'a5_2',text:'Montar ou completar o manual da casa (impresso e digital)'},{id:'a5_3',text:'Anotar as dúvidas repetidas dos hóspedes e incluí-las no manual'}]}
]},
/* 6 */
{title:'Tratamento de problemas', screens:[
 {kind:'learn', title:'Problema resolvido bem pode virar elogio',
  body:'<p>Toda hospedagem tem problemas: o chuveiro queima, a internet cai, o vizinho faz barulho. A avaliação ruim raramente vem do problema em si, e sim de <b>como ele foi tratado</b>: demora, desculpas vagas ou a sensação de que o anfitrião não se importou.</p><p>Dois hábitos mudam esse cenário: <b>registrar as reclamações por tema</b> (para ver o que se repete) e ter um <b>plano B</b> pronto (contatos, peças, alternativas). A ferramenta calcula sua taxa de reclamações a cada 100 estadias e mostra quais temas concentram o problema.</p>',
  example:'Exemplo ilustrativo: 6 reclamações em 40 estadias = 15 reclamações a cada 100 estadias. Se 3 delas forem sobre limpeza, metade do problema está em um único tema, e resolver esse tema tem mais efeito do que atacar todos.'},
 {kind:'compare', title:'Apagar incêndio × tratar a causa',
  cols:[{h:'Apagar incêndio',type:'bad',items:['Resolve na hora e esquece','Procura um técnico só quando quebra','Pede desculpas sem dar prazo','Cada reclamação é “azar”']},
        {h:'Tratar a causa',type:'good',items:['Registra tema, data e solução','Tem contatos e peças antes de precisar','Dá retorno com prazo e confirma a solução','Ataca primeiro o tema que mais se repete']}]},
 {kind:'form', title:'Suas reclamações e seu plano B', intro:'Considere os <b>últimos 6 meses</b>: avaliações, mensagens e conversas. Informe quantas vezes cada tema apareceu; deixe em branco os que não ocorreram.',
  fields:[
   {id:'pr_estadias',label:'Quantas estadias você teve nos últimos 6 meses?',type:'number',required:true,min:0,max:20000,step:1,unit:'estadias',allowUnknown:true},
   {id:'pr_reclam',label:'Reclamações por tema (número de ocorrências)',type:'list',required:false,preset:['Limpeza','Barulho','Wi-Fi / internet','Água quente / chuveiro','Chegada e acesso','Diferença em relação ao anúncio','Conforto da cama','Atendimento / demora na resposta'],namePlaceholder:'Tema',valuePlaceholder:'Ocorrências'},
   {id:'pr_solucao',label:'Quando surge um problema, em quanto tempo costuma ser resolvido?',type:'radio',required:true,options:[{v:'mesmo_dia',l:'No mesmo dia, com retorno ao hóspede'},{v:'dias',l:'Em 1 ou 2 dias'},{v:'sem_prazo',l:'Sem prazo definido, depende do técnico'}]},
   {id:'pr_planob',label:'O que você já tem pronto para emergências?',type:'checks',options:PB_OPTS}
  ]},
 {kind:'feedback', title:'Análise das suas reclamações',
  metrics:function(s,c){return [{label:'Reclamações registradas',value:F.num(c.recTotal),tag:'informado'},{label:'Reclamações a cada 100 estadias',value:c.taxaRecl==null?'—':F.num(c.taxaRecl,1),tag:'calculado'},{label:'Tema mais frequente',value:c.recTop?c.recTop.name:'—',tag:'calculado'},{label:'Índice de tratamento de problemas',value:F.num(c.D6,0)+' / 100',tag:c.taxaRecl==null?'estimativa':'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.recTotal===0) o.push({lv:'info',t:'Nenhuma reclamação registrada. Se for porque você não anota, comece agora: sem registro não há como ver padrões.'});
   if(c.recTop) o.push({lv:c.recTopPct>=40?'warn':'info',t:'<b>'+esc(c.recTop.name)+'</b> concentra '+F.pct(c.recTopPct,0)+' das reclamações ('+F.num(c.recTop.value)+' de '+F.num(c.recTotal)+'). '+(c.recTopPct>=40?'Um único tema responde por boa parte do problema: comece por ele.':'As reclamações estão distribuídas; priorize os 2 ou 3 primeiros temas.')});
   if(c.paretoTemas.length&&c.recTotal>0) o.push({lv:'info',t:'Os temas '+c.paretoTemas.map(function(x){return '<b>'+esc(x.name)+'</b>';}).join(', ')+' somam pelo menos 80% das ocorrências.'});
   if(c.taxaRecl==null) o.push({lv:'warn',t:'Sem o número de estadias, não é possível calcular a taxa de reclamações. Usamos 50 pontos como hipótese no índice.'});
   else if(c.taxaRecl>10) o.push({lv:'bad',t:'São '+F.num(c.taxaRecl,1)+' reclamações a cada 100 estadias. Isso indica falhas que se repetem, não casos isolados.'});
   else if(c.taxaRecl>3) o.push({lv:'warn',t:F.num(c.taxaRecl,1)+' reclamações a cada 100 estadias. Há espaço para reduzir atacando o tema principal.'});
   else if(c.recTotal>0) o.push({lv:'ok',t:'Taxa de reclamações baixa ('+F.num(c.taxaRecl,1)+' a cada 100 estadias).'});
   if(s.t('pr_solucao')==='sem_prazo') o.push({lv:'bad',t:'Problemas sem prazo de solução são o caminho mais curto para uma avaliação ruim. Monte a lista de técnicos e um plano B.'});
   if(c.pbN<2) o.push({lv:'warn',t:'Seu plano B está incompleto ('+c.pbN+' de 4 itens). Peças de reposição e contatos de técnicos resolvem a maioria das emergências comuns.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Criar um registro simples de ocorrências (data, tema, solução, prazo)'},{id:'a6_2',text:'Montar a lista de técnicos e o kit de peças de reposição'},{id:'a6_3',text:'Atacar a causa do tema de reclamação mais frequente neste mês'}]}
]},
/* 7 */
{title:'Plano de qualidade', screens:[
 {kind:'learn', title:'Qualidade é rotina: padrão, conferência e meta',
  body:'<p>O plano de qualidade junta tudo o que você viu em três peças:</p><ul><li><b>Padrões</b>: o checklist de chegada, limpeza, conforto e comunicação, sempre igual.</li><li><b>Conferência</b>: uma auditoria periódica, com alguém responsável, usando este mesmo índice.</li><li><b>Meta</b>: a nota que você quer alcançar e o prazo para revisar.</li></ul><p>A cada auditoria, refaça o Auditor e compare o índice. Se o índice sobe e a nota das plataformas não acompanha, volte às avaliações: talvez a falha esteja num ponto que você ainda não mediu.</p>',
  example:'Exemplo ilustrativo: auditoria quinzenal de 30 minutos, feita pela mesma pessoa, com o checklist impresso. Cada item “não conforme” vira uma tarefa com prazo na semana seguinte.'},
 {kind:'compare', title:'Plano de intenções × plano de qualidade',
  cols:[{h:'Intenções',type:'bad',items:['“Vou caprichar mais”','Sem responsável','Sem data para revisar','Mede só pela nota da plataforma']},
        {h:'Plano de qualidade',type:'good',items:['Padrões escritos por etapa da jornada','Um responsável pela auditoria','Frequência definida e registrada','Mede o índice interno e a nota externa']}]},
 {kind:'form', title:'Sua meta e sua rotina de qualidade',
  fields:[
   {id:'pq_meta',label:'Nota média que você quer alcançar (0 a 5)',type:'number',required:true,min:0,max:5,step:0.01},
   {id:'pq_auditoria',label:'Com que frequência você fará a auditoria da experiência?',type:'radio',required:true,options:[{v:'semanal',l:'Semanal'},{v:'quinzenal',l:'Quinzenal'},{v:'mensal',l:'Mensal'},{v:'nunca',l:'Ainda não consigo definir'}]},
   {id:'pq_responsavel',label:'Quem será o responsável pela auditoria?',type:'text',required:true,placeholder:'Ex.: eu mesma / Joana (governanta)'}
  ]},
 {kind:'feedback', title:'Seu Índice de Experiência Zion',
  metrics:function(s,c){return [{label:'Índice de Experiência Zion',value:F.num(c.iez,0)+' / 100',tag:'calculado'},{label:'Classificação',value:classe(c.iez),tag:'calculado'},{label:'Dimensão mais fraca',value:c.dimMin.nome,tag:'calculado'},{label:'Meta de nota',value:F.num(s.n('pq_meta'),2),tag:'informado'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:c.iez>=80?'ok':c.iez>=60?'info':c.iez>=40?'warn':'bad',t:'Seu índice é <b>'+F.num(c.iez,0)+'</b>, classificação <b>'+classe(c.iez)+'</b>. A dimensão com mais espaço de melhoria é <b>'+c.dimMin.nome+'</b> ('+F.num(c.dimMin.v,0)+' pontos).'});
   if(c.nota!=null&&s.n('pq_meta')!=null){var g=s.n('pq_meta')-c.nota;
     if(g>0) o.push({lv:'info',t:'Para sair de '+F.num(c.nota,2)+' e chegar a '+F.num(s.n('pq_meta'),2)+', as próximas avaliações precisam ficar acima da meta. Como a média acumula o histórico, a mudança é gradual: foque em consistência.'});
     else o.push({lv:'ok',t:'Sua nota atual já atinge a meta. O plano de qualidade serve para mantê-la.'});}
   if(s.t('pq_auditoria')==='nunca') o.push({lv:'warn',t:'Sem auditoria periódica, os padrões se perdem em poucas semanas. Comece com uma auditoria mensal.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Agendar a primeira auditoria da experiência no calendário'},{id:'a7_2',text:'Imprimir o Plano de Qualidade e combinar os padrões com a equipe'},{id:'a7_3',text:'Refazer o Auditor em 30 dias e comparar o índice'}]}
]}
],

compute:function(s){
 var c={};
 c.nota=s.n('nota_media'); c.U=s.n('unidades',1);
 c.jornada=ETAPAS.map(function(e){return {id:e[0],nome:e[1],nota:nota(s,e[0])};});
 var soma=0; c.jornada.forEach(function(x){soma+=x.nota;}); c.jMedia=soma/ETAPAS.length;
 c.jMin=c.jornada.slice().sort(function(a,b){return a.nota-b.nota;})[0]||null;
 c.jFracas=c.jornada.filter(function(x){return x.nota<=3;}).length;
 c.D1=(c.jMedia-1)/4*100;
 c.piN=arr(s,'pi_itens').length; c.D2=c.piN/6*100;
 c.limpN=arr(s,'lc_limpeza').length; c.confN=arr(s,'lc_conforto').length; c.D3=(c.limpN+c.confN)/12*100;
 var r=s.n('at_resposta'); c.respScore=r==null?50:(r<=15?100:r<=60?75:r<=240?50:20);
 c.cobScore={'24h':100,estendido:75,comercial:50,irregular:25}[s.t('at_cobertura')]||25;
 c.persN=arr(s,'at_pers').length;
 c.D4=(c.respScore+c.cobScore+c.persN/4*100)/3;
 c.msgN=arr(s,'co_msgs').length; c.manualScore={completo:100,parcial:50,nao:0}[s.t('co_manual')]||0;
 c.D5=c.msgN/6*100*0.7+c.manualScore*0.3;
 var rows=(s.v.pr_reclam||[]).filter(function(x){return x&&ZA.isNum(x.value)&&x.value>0&&String(x.name||'').trim();});
 rows=rows.slice().sort(function(a,b){return b.value-a.value;});
 c.recRows=rows; c.recTotal=ZA.listSum(rows); c.recTop=rows[0]||null;
 c.recTopPct=c.recTop&&c.recTotal>0?c.recTop.value/c.recTotal*100:0;
 var acc=0; c.paretoTemas=[]; for(var i=0;i<rows.length;i++){c.paretoTemas.push(rows[i]); acc+=rows[i].value; if(acc>=0.8*c.recTotal) break;}
 var est=s.n('pr_estadias'); c.estadias=est;
 c.taxaRecl=(est!=null&&est>0)?c.recTotal/est*100:null;
 c.rateScore=c.taxaRecl==null?50:ZA.clamp(100-5*c.taxaRecl,0,100);
 c.solScore={mesmo_dia:100,dias:60,sem_prazo:20}[s.t('pr_solucao')]||20;
 c.pbN=arr(s,'pr_planob').length;
 c.D6=0.5*c.rateScore+0.25*c.solScore+0.25*(c.pbN/4*100);
 c.dims=[{k:'D1',nome:'Jornada do hóspede',peso:20,v:c.D1},{k:'D2',nome:'Primeira impressão',peso:15,v:c.D2},{k:'D3',nome:'Limpeza e conforto',peso:20,v:c.D3},{k:'D4',nome:'Atendimento',peso:15,v:c.D4},{k:'D5',nome:'Comunicação',peso:15,v:c.D5},{k:'D6',nome:'Tratamento de problemas',peso:15,v:c.D6}];
 c.iez=0; c.dims.forEach(function(d){c.iez+=d.v*d.peso/100;});
 c.dimMin=c.dims.slice().sort(function(a,b){return a.v-b.v;})[0];
 return c;
},

metrics:function(s,c){return [
 {label:'Índice de Experiência Zion',value:F.num(c.iez,0)+' / 100',tag:'calculado'},
 {label:'Classificação',value:classe(c.iez),tag:'calculado'},
 {label:'Nota média atual',value:c.nota==null?'—':F.num(c.nota,2),tag:'informado'},
 {label:'Meta de nota',value:F.num(s.n('pq_meta'),2),tag:'informado'},
 {label:'Etapa mais fraca da jornada',value:c.jMin?c.jMin.nome+' ('+c.jMin.nota+')':'—',tag:'calculado'},
 {label:'Dimensão mais fraca',value:c.dimMin.nome,tag:'calculado'},
 {label:'Reclamações a cada 100 estadias',value:c.taxaRecl==null?'—':F.num(c.taxaRecl,1),tag:'calculado'},
 {label:'Principal tema de reclamação',value:c.recTop?c.recTop.name:'—',tag:'informado'}
];},

priorities:function(s,c){var L=[];
 if(c.jMin&&c.jMin.nota<=2) L.push({title:'Redesenhar a etapa “'+c.jMin.nome+'”',why:'É a etapa com a menor nota da jornada ('+c.jMin.nota+' de 5).',score:9});
 if(c.recTop&&c.recTopPct>=40) L.push({title:'Eliminar a causa das reclamações de '+c.recTop.name,why:'O tema concentra '+F.pct(c.recTopPct,0)+' das ocorrências registradas.',score:9});
 if(c.taxaRecl!=null&&c.taxaRecl>10) L.push({title:'Reduzir a taxa de reclamações (hoje '+F.num(c.taxaRecl,1)+' a cada 100 estadias)',why:'Falhas repetidas, não casos isolados.',score:8});
 if(arr(s,'lc_limpeza').indexOf('checklist')<0) L.push({title:'Criar o checklist de limpeza por cômodo',why:'Sem padrão escrito, a limpeza depende de quem faz e do dia.',score:8});
 if(arr(s,'lc_limpeza').indexOf('vistoria')<0) L.push({title:'Adotar vistoria final ou fotos padronizadas após a limpeza',why:'Pequenas falhas chegam ao hóspede sem conferência.',score:6});
 if(c.confN<=3) L.push({title:'Corrigir os itens de sono e banho que faltam',why:'Só '+c.confN+' de 6 itens de conforto garantidos.',score:7});
 if(c.piN<=3) L.push({title:'Padronizar a chegada (instruções com vídeo, casa arejada, boas-vindas)',why:'Só '+c.piN+' de 6 pontos de primeira impressão garantidos.',score:7});
 if(s.n('pi_espera')!=null&&s.n('pi_espera')>15) L.push({title:'Reduzir o tempo de chegada e acomodação',why:'Hoje leva cerca de '+F.num(s.n('pi_espera'))+' minutos.',score:6});
 if(s.n('at_resposta')!=null&&s.n('at_resposta')>60) L.push({title:'Responder em até 1 hora durante a estadia',why:'Tempo atual de cerca de '+F.num(s.n('at_resposta'))+' minutos.',score:6});
 if(['comercial','irregular'].indexOf(s.t('at_cobertura'))>=0) L.push({title:'Definir um contato de emergência fora do horário',why:'O hóspede fica sem apoio em parte do dia.',score:6});
 if(c.msgN<=3) L.push({title:'Programar a sequência de 6 mensagens',why:'Só '+c.msgN+' mensagens enviadas em toda reserva.',score:6});
 if(s.t('co_manual')!=='completo') L.push({title:'Completar o manual da casa',why:'Dúvidas básicas viram mensagens e atrito.',score:5});
 if(s.t('pr_solucao')==='sem_prazo') L.push({title:'Definir prazo de solução e montar a lista de técnicos',why:'Problemas sem prazo tendem a ir para a avaliação.',score:7});
 if(c.pbN<2) L.push({title:'Montar o kit de plano B (peças, contatos, alternativas)',why:'Só '+c.pbN+' de 4 itens prontos para emergências.',score:5});
 if(c.nota==null||s.unknown('pr_estadias')) L.push({title:'Levantar nota média e número de estadias dos últimos 6 meses',why:'Sem esses dados, parte do diagnóstico é hipótese.',score:5});
 if(s.t('pq_auditoria')==='nunca') L.push({title:'Agendar uma auditoria mensal da experiência',why:'Sem conferência periódica, os padrões se perdem.',score:4});
 if(c.persN<=1) L.push({title:'Perguntar o motivo da viagem e personalizar a recepção',why:'Personalização é barata e marca a estadia.',score:3});
 return L;},

report:function(s,c){
 var tg=function(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';};
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Unidades',F.num(c.U),tg('informado')],
  ['Nota média atual',c.nota==null?'—':F.num(c.nota,2),c.nota==null?tg('hipotese','não informado'):tg('informado')],
  ['Estadias nos últimos 6 meses',c.estadias==null?'—':F.num(c.estadias),c.estadias==null?tg('hipotese','não informado'):tg('informado')],
  ['Notas da jornada','autoavaliação de 1 a 5 por etapa',tg('informado')],
  ['Pesos do índice','Jornada 20% · Primeira impressão 15% · Limpeza e conforto 20% · Atendimento 15% · Comunicação 15% · Problemas 15%',tg('recomendacao','metodologia Zion')],
  ['Pontuação de resposta','até 15 min = 100 · até 60 = 75 · até 240 = 50 · acima = 20'+(s.unknown('at_resposta')?' (desconhecido: 50)':''),s.unknown('at_resposta')?tg('hipotese'):tg('recomendacao','metodologia Zion')],
  ['Taxa de reclamações','cada reclamação por 100 estadias reduz 5 pontos'+(c.taxaRecl==null?' (sem estadias: 50 pontos)':''),c.taxaRecl==null?tg('hipotese'):tg('recomendacao','metodologia Zion')]],[]);
 var dims=ZA.table(['Dimensão','Peso','Pontuação','Situação'],c.dims.map(function(d){return [d.nome,d.peso+'%',F.num(d.v,0)+' / 100',classe(d.v)];}).concat([['<b>Índice de Experiência Zion</b>','100%','<b>'+F.num(c.iez,0)+' / 100</b>','<b>'+classe(c.iez)+'</b>']]),[1,2]);
 var jor=ZA.table(['Etapa da jornada','Nota (1 a 5)','Leitura'],c.jornada.map(function(x){return [x.nome,String(x.nota),x.nota<=2?'crítica':x.nota===3?'mediana':'boa'];}),[1]);
 var rec=c.recRows.length?ZA.table(['Tema','Ocorrências','% do total','A cada 100 estadias'],c.recRows.map(function(x){return [esc(x.name),F.num(x.value),F.pct(x.value/c.recTotal*100,0),c.estadias?F.num(x.value/c.estadias*100,1):'—'];}),[1,2,3]):'<p class="za-small">Nenhuma reclamação registrada no período.</p>';
 var pads=[['Chegada',faltam(s,'pi_itens',PI_OPTS)],['Limpeza',faltam(s,'lc_limpeza',LIMP_OPTS)],['Conforto',faltam(s,'lc_conforto',CONF_OPTS)],['Personalização',faltam(s,'at_pers',PERS_OPTS)],['Mensagens',faltam(s,'co_msgs',MSG_OPTS)],['Plano B',faltam(s,'pr_planob',PB_OPTS)]];
 var padHtml=ZA.table(['Área','Padrões a implantar'],pads.map(function(p){return [p[0],p[1].length?p[1].map(function(x){return x.l;}).join('; '):'<span class="za-tag calculado">completo</span>'];}),[]);
 var rot='<div class="za-card"><p><b>Responsável pela auditoria:</b> '+esc(s.t('pq_responsavel'))+'<br><b>Frequência:</b> '+({semanal:'semanal',quinzenal:'quinzenal',mensal:'mensal',nunca:'a definir (sugestão: mensal)'}[s.t('pq_auditoria')]||'a definir')+'<br><b>Meta de nota:</b> '+F.num(s.n('pq_meta'),2)+(c.nota!=null?' (atual: '+F.num(c.nota,2)+')':'')+'</p><p class="za-small">Em cada auditoria: percorra a jornada como hóspede, confira os padrões da tabela acima, registre as não conformidades com prazo e refaça o índice.</p></div>';
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido de 30 dias</b><ol><li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Reler as avaliações e confirmar a etapa mais fraca')+'.</li><li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Escrever os checklists de chegada e limpeza')+'.</li><li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Programar a sequência de mensagens')+'.</li><li><b>Semana 4:</b> primeira auditoria da experiência com '+esc(s.t('pq_responsavel')||'o responsável')+'; refazer o Auditor e comparar o índice ('+F.num(c.iez,0)+' hoje).</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Índice de Experiência por dimensão',html:dims+'<p class="za-small">Faixas: 80 ou mais = sólida · 60 a 79 = boa, com lacunas · 40 a 59 = irregular · abaixo de 40 = crítica. Índice orientativo de autoavaliação.</p>'},
  {title:'Notas por etapa da jornada',html:jor},
  {title:'Análise das reclamações',html:rec+(c.paretoTemas.length&&c.recTotal>0?'<p class="za-small">Temas que somam pelo menos 80% das ocorrências: '+c.paretoTemas.map(function(x){return esc(x.name);}).join(', ')+'.</p>':'')},
  {title:'Padrões de qualidade a implantar',html:padHtml},
  {title:'Rotina de auditoria',html:rot}
 ],plan:plan};
}
});
})();
