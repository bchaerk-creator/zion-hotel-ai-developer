/* ZAR-A01 · Seu Airbnb Está Vazio? · Raio-X Inteligente de Reservas */
(function(){
var F=ZA.fmt, esc=ZA.esc;
function ESC5(lo,hi){return [1,2,3,4,5].map(function(k){return {v:String(k),l:k+(k===1?' · '+lo:k===5?' · '+hi:'')};});}
function sn(s,id,d){var x=Number(s.t(id));return s.t(id)!==''&&isFinite(x)?x:d;}
var TGL={hipotese:'hipótese',recomendacao:'recomendação'};
function tg(t,l){return '<span class="za-tag '+t+'">'+(l||TGL[t]||t)+'</span>';}
var DIFS=[{v:'vista',l:'Vista (montanha, mar, vale, lago)'},{v:'ofuro',l:'Ofurô, banheira ou hidromassagem'},{v:'lareira',l:'Lareira ou fogão a lenha'},{v:'piscina',l:'Piscina'},{v:'natureza',l:'Trilhas, mata ou cachoeira no local'},{v:'cafe',l:'Café da manhã incluso'},{v:'pet',l:'Aceita pets'},{v:'homeoffice',l:'Internet rápida e espaço para trabalhar'},{v:'centro',l:'Localização a pé do centro ou da praia'},{v:'cozinha',l:'Cozinha completa'},{v:'estacionamento',l:'Estacionamento no local'},{v:'experiencias',l:'Experiências (passeios, jantar, kits especiais)'}];
var PUB={casais:'casais',familias:'famílias com crianças',amigos:'grupos de amigos',remoto:'quem trabalha remoto',pet:'tutores de pets',aventura:'viajantes de aventura e natureza',indefinido:'público ainda não definido'};
var DIM_ACAO={publico:'Definir o público prioritário e reescrever o anúncio falando com ele',diferenciais:'Colocar os 3 principais diferenciais no título e nas 5 primeiras fotos',anuncio:'Refazer fotos, título e descrição do anúncio com foco em benefícios',preco:'Revisar a diária comparando com concorrentes e com os seus custos',experiencia:'Atacar as reclamações recorrentes e acelerar o tempo de resposta'};

ZA.register({
id:'A01', code:'ZAR-A01', collection:'Hospedagem',
title:'Seu Airbnb Está Vazio?',
subtitle:'O Problema Pode Estar na Sua Oferta',
tool:'Raio-X Inteligente de Reservas',
deliverable:'Dossiê de Melhoria da Hospedagem',
nameField:'nome', propertyField:'propriedade',
disclaimer:'O Raio-X é um diagnóstico orientativo: as pontuações seguem critérios da metodologia Zion e as conclusões sem dados completos são hipóteses a confirmar. Não há garantia de reservas, ocupação ou faturamento.',

intro:[
 {kind:'mirror', title:'Seu Airbnb está anunciado, mas ninguém reserva?',
  lead:'Você investiu na hospedagem, publicou o anúncio, baixou os preços e mesmo assim continua esperando as reservas chegarem?',
  body:'<div class="za-card"><p>Talvez você se reconheça em alguma destas situações:</p><ul><li>“Abro o calendário e vejo semanas inteiras em branco.”</li><li>“Já baixei a diária duas vezes e nada mudou.”</li><li>“As pessoas olham, às vezes perguntam, mas não fecham.”</li><li>“Não sei se o problema é o preço, as fotos, a época ou eu.”</li></ul></div>'},
 {kind:'collapse', title:'Nem sempre o problema é a diária ou a falta de turistas.',
  lead:'Sua oferta pode estar deixando de mostrar os motivos certos para o hóspede reservar.',
  body:'<div class="za-card"><p>Uma reserva acontece depois de uma sequência de pequenas decisões do hóspede:</p><ol><li><b>Ver</b> o anúncio na busca (exposição);</li><li><b>Clicar e se interessar</b> (foto, título, preço na lista);</li><li><b>Confiar e decidir</b> (descrição, avaliações, regras, atendimento).</li></ol><p>Baixar o preço mexe só em parte da primeira etapa. Se o problema está em outra, o desconto custa caro e não resolve. O Raio-X vai mostrar <b>onde</b> o hóspede está desistindo — e, quando faltar dado, vai dizer claramente que se trata de uma hipótese.</p></div>'},
 {kind:'start', title:'Vamos fazer o Raio-X da sua hospedagem',
  lead:'Em 7 pilares você vai medir sua ocupação, avaliar público, diferenciais, anúncio, preço e experiência, e sair com um plano de melhoria de 30 dias.',
  body:'<p>Se tiver acesso, deixe aberto o painel da sua plataforma (visualizações, consultas, reservas, avaliações). Se não tiver algum dado, marque “não sei”: o dossiê vai separar o que é constatação do que é hipótese.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Marina'},
   {id:'propriedade',label:'Nome da hospedagem',type:'text',required:true,placeholder:'Ex.: Chalé Recanto da Serra'},
   {id:'tipo',label:'Tipo de hospedagem',type:'select',required:true,options:[{v:'airbnb',l:'Apartamento ou casa (Airbnb/temporada)'},{v:'cabana',l:'Cabana ou chalé'},{v:'glamping',l:'Glamping'},{v:'pousada',l:'Pequena pousada'},{v:'outro',l:'Outro'}]},
   {id:'destino',label:'Cidade / destino',type:'text',required:true,placeholder:'Ex.: São Bento do Sapucaí (SP)'},
   {id:'unidades',label:'Quantas unidades você aluga?',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)'}
  ]}
],

pillars:[
/* 1 */
{title:'Raio-X da hospedagem', screens:[
 {kind:'learn', title:'Antes de mudar qualquer coisa, meça',
  body:'<p>“Está vazio” é uma sensação. Para diagnosticar, você precisa de quatro números do último mês:</p><ul><li><b>Noites disponíveis</b>: noites que estavam abertas para venda (todas as unidades somadas).</li><li><b>Noites vendidas</b>: noites efetivamente ocupadas por hóspedes pagantes.</li><li><b>Diária média</b>: quanto você recebeu, em média, por noite vendida.</li><li><b>Reservas</b>: quantas estadias diferentes aconteceram.</li></ul><p>Com eles calculamos a <b>ocupação</b> (vendidas ÷ disponíveis), a <b>receita por noite disponível</b> (receita ÷ noites disponíveis) e a <b>estadia média</b> (noites vendidas ÷ reservas). A receita por noite disponível junta preço e ocupação num número só: é ela que mostra se baixar a diária está realmente ajudando.</p>',
  example:'Exemplo ilustrativo: 30 noites disponíveis, 9 vendidas a R$ 250. Ocupação de 30%, receita de R$ 2.250 e receita por noite disponível de R$ 75. Se baixar para R$ 200 e vender 11 noites, a receita por noite disponível vai a R$ 73,33: vendeu mais noites, mas ganhou menos por noite aberta.'},
 {kind:'compare', title:'Achismo × diagnóstico',
  cols:[{h:'Achismo',type:'bad',items:['“O mês foi fraco” sem saber quantas noites foram vendidas','Comparar com o mês de alta temporada','Olhar só o faturamento total','Concluir que o problema é preço sem olhar o resto']},
        {h:'Diagnóstico',type:'good',items:['Ocupação calculada com noites disponíveis reais','Comparar o mesmo mês ou meses parecidos','Acompanhar receita por noite disponível','Testar uma hipótese por vez e medir']}]},
 {kind:'form', title:'Os números do seu último mês', intro:'Use o último mês completo. Some todas as unidades.',
  fields:[
   {id:'noites_disp',label:'Noites disponíveis no mês (todas as unidades)',type:'number',required:true,min:1,max:6200,step:1,unit:'noites',help:'Ex.: 1 unidade aberta o mês todo = 30. Desconte bloqueios de uso próprio ou manutenção.'},
   {id:'noites_vend',label:'Noites vendidas no mês',type:'number',required:true,min:0,max:6200,step:1,unit:'noites',validate:function(v,s){var d=s.n('noites_disp');return (ZA.isNum(d)&&v>d)?'Noites vendidas não podem passar das disponíveis.':'';}},
   {id:'diaria_media',label:'Diária média recebida',type:'money',required:true,min:1,help:'Receita de hospedagem do mês ÷ noites vendidas. Se não vendeu, use a diária anunciada.'},
   {id:'reservas_mes',label:'Número de reservas no mês',type:'number',required:true,min:0,step:1,allowUnknown:true,help:'Cada estadia conta como uma reserva, independentemente do número de noites.'}
  ]},
 {kind:'feedback', title:'O retrato do seu mês',
  metrics:function(s,c){return [{label:'Ocupação',value:F.pct(c.ocup*100),tag:'calculado'},{label:'Receita do mês',value:F.brl(c.receita),tag:'calculado'},{label:'Receita por noite disponível',value:F.brl(c.revpan),tag:'calculado'},{label:'Estadia média',value:c.estadia==null?'sem dado':F.num(c.estadia,1)+' noites',tag:c.estadia==null?'hipotese':'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.vend===0) o.push({lv:'bad',t:'Nenhuma noite vendida no mês. Vamos verificar cada etapa da oferta para descobrir onde o hóspede está parando.'});
   else if(c.ocup<0.3) o.push({lv:'warn',t:'Ocupação de '+F.pct(c.ocup*100)+': '+F.num(c.vazias)+' noites ficaram vazias. O Raio-X vai procurar o motivo nas próximas etapas.'});
   else o.push({lv:'info',t:'Ocupação de '+F.pct(c.ocup*100)+', com '+F.num(c.vazias)+' noites vazias no mês. Compare com o mesmo mês do ano anterior, se tiver.'});
   if(c.reservas==null) o.push({lv:'warn',t:'Sem o número de reservas, não sabemos a estadia média nem a conversão de consultas. Isso vira <b>hipótese</b> no dossiê.'});
   else if(c.estadia!=null&&c.estadia<1.5) o.push({lv:'info',t:'Estadias curtas (média de '+F.num(c.estadia,1)+' noites) multiplicam limpezas e deixam “buracos” no calendário. Vale olhar a estadia mínima.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Registrar todo mês: noites disponíveis, vendidas, diária média e reservas'},{id:'a1_2',text:'Comparar meses equivalentes (não alta com baixa temporada)'},{id:'a1_3',text:'Acompanhar a receita por noite disponível antes de dar qualquer desconto'}]}
]},
/* 2 */
{title:'Público prioritário', screens:[
 {kind:'learn', title:'Quem tenta agradar todo mundo não convence ninguém',
  body:'<p>Na busca, o hóspede passa poucos segundos em cada anúncio. Ele reserva quando sente que <b>aquele lugar foi pensado para a viagem dele</b>. Um casal em lua de mel, uma família com crianças pequenas e um grupo de amigos procuram coisas diferentes: privacidade, segurança, espaço para todos.</p><p>Escolher um <b>público prioritário</b> não proíbe os outros. Ele define o que vai na primeira foto, no título e no primeiro parágrafo.</p>',
  example:'Exemplo: um chalé com ofurô e uma cama de casal anunciado como “Chalé para até 4 pessoas” disputa com casas maiores. Anunciado como refúgio a dois, ele passa a ser o melhor da busca para um público específico.'},
 {kind:'compare', title:'Anúncio genérico × anúncio com público',
  cols:[{h:'Genérico',type:'bad',items:['“Ótimo para casais, famílias e amigos”','Primeira foto: fachada de longe','Descrição lista móveis','Fotos sem pessoas ou sem uso do espaço']},
        {h:'Com público',type:'good',items:['“Refúgio para casais com ofurô e vista”','Primeira foto: o momento que o público deseja','Descrição fala da viagem dele','Fotos mostram o espaço sendo vivido']}]},
 {kind:'form', title:'Para quem é a sua hospedagem',
  fields:[
   {id:'publico',label:'Qual público reserva mais (ou combina mais) com a sua hospedagem?',type:'radio',required:true,options:[{v:'casais',l:'Casais'},{v:'familias',l:'Famílias com crianças'},{v:'amigos',l:'Grupos de amigos'},{v:'remoto',l:'Quem trabalha remoto'},{v:'pet',l:'Tutores de pets'},{v:'aventura',l:'Viajantes de aventura e natureza'},{v:'indefinido',l:'Ainda não sei'}]},
   {id:'publico_fala',label:'O seu anúncio fala claramente com esse público? (1 a 5)',type:'radio',required:true,options:ESC5('não fala','fala muito bem')},
   {id:'publico_fotos',label:'As fotos mostram o espaço sendo usado do jeito que esse público usaria?',type:'radio',required:true,options:[{v:'sim',l:'Sim'},{v:'parcial',l:'Algumas fotos'},{v:'nao',l:'Não'}]}
  ]},
 {kind:'feedback', title:'Clareza de público',
  metrics:function(s,c){return [{label:'Pontuação de público',value:F.num(c.sPub,0)+'/100',tag:'calculado'},{label:'Público prioritário',value:PUB[s.t('publico')]||'—',tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(s.t('publico')==='indefinido') o.push({lv:'bad',t:'Sem público definido, o anúncio tende a ficar genérico. Olhe suas últimas 10 reservas: quem veio e por quê? Esse é o ponto de partida.'});
   if(c.sPub<50) o.push({lv:'warn',t:'Pontuação de '+F.num(c.sPub,0)+'/100. O hóspede provavelmente não se reconhece no anúncio. Primeira foto, título e primeiro parágrafo precisam falar com '+esc(PUB[s.t('publico')]||'o seu público')+'.'});
   else if(c.sPub<75) o.push({lv:'info',t:'Pontuação de '+F.num(c.sPub,0)+'/100. Há uma direção, mas ela ainda não aparece com força em todas as fotos e textos.'});
   else o.push({lv:'ok',t:'Público claro ('+F.num(c.sPub,0)+'/100). Mantenha essa coerência em todas as fotos e respostas.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Analisar as últimas 10 reservas e anotar quem veio e o motivo da viagem'},{id:'a2_2',text:'Escolher uma foto de capa que mostre o momento desejado pelo público prioritário'},{id:'a2_3',text:'Reescrever o primeiro parágrafo do anúncio falando com esse público'}]}
]},
/* 3 */
{title:'Diferenciais e proposta de valor', screens:[
 {kind:'learn', title:'Diferencial escondido não vende',
  body:'<p>Diferencial é aquilo que faz o hóspede escolher você <b>em vez</b> do anúncio ao lado: uma vista, um ofurô, a lareira, aceitar pets, café da manhã caseiro. Ter o diferencial não basta: ele precisa aparecer <b>onde o hóspede decide</b>, ou seja, na foto de capa, nas primeiras fotos e no título.</p><p>A <b>proposta de valor</b> junta público e diferencial numa frase: “para quem quer X, oferecemos Y”.</p>',
  example:'Exemplo: “Para casais que querem desligar da cidade, um chalé com ofurô aquecido e vista para o vale, a 10 minutos do centro.” O ofurô aparece na 1ª foto e no título.'},
 {kind:'compare', title:'Diferencial invisível × diferencial evidente',
  cols:[{h:'Invisível',type:'bad',items:['Ofurô aparece só na 18ª foto','Vista citada no fim da descrição','“Aceitamos pets” escondido nas regras','Café da manhã sem foto']},
        {h:'Evidente',type:'good',items:['Ofurô aceso ao entardecer na foto de capa','Título com “vista para o vale”','Foto do pet no deck e menção no título','Foto da mesa posta logo no início']}]},
 {kind:'form', title:'Seus diferenciais',
  fields:[
   {id:'difs',label:'Quais destes diferenciais você realmente tem?',type:'checks',options:DIFS},
   {id:'difs_destaque',label:'Seus 3 principais diferenciais aparecem no título ou nas 5 primeiras fotos?',type:'radio',required:true,options:[{v:'todos',l:'Sim, todos'},{v:'alguns',l:'Alguns'},{v:'nenhum',l:'Nenhum'}]},
   {id:'dif_unico',label:'Existe algo que só a sua hospedagem tem na região? (opcional)',type:'text',required:false,placeholder:'Ex.: nascer do sol sobre o mar de nuvens'}
  ]},
 {kind:'feedback', title:'Força dos seus diferenciais',
  metrics:function(s,c){return [{label:'Pontuação de diferenciais',value:F.num(c.sDif,0)+'/100',tag:'calculado'},{label:'Diferenciais marcados',value:String(c.nDifs),tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(c.nDifs===0) o.push({lv:'bad',t:'Nenhum diferencial marcado. Antes de baixar o preço, descubra o que há de único: um detalhe do lugar, um serviço, um cuidado. Sem isso, a única comparação possível é o preço.'});
   else if(c.nDifs<3) o.push({lv:'warn',t:'Poucos diferenciais ('+c.nDifs+'). Veja se há algo que você já oferece e não comunica.'});
   if(s.t('difs_destaque')==='nenhum'&&c.nDifs>0) o.push({lv:'bad',t:'Você tem diferenciais, mas eles não aparecem no título nem nas primeiras fotos. É uma das correções mais rápidas e baratas do seu plano.'});
   else if(s.t('difs_destaque')==='alguns') o.push({lv:'warn',t:'Só parte dos diferenciais aparece onde o hóspede decide. Reordene as fotos.'});
   else if(s.t('difs_destaque')==='todos') o.push({lv:'ok',t:'Seus diferenciais estão onde o hóspede decide.'});
   if(s.t('dif_unico')) o.push({lv:'info',t:'Seu diferencial único (“'+esc(s.t('dif_unico'))+'”) merece uma foto própria e uma menção no título.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Escrever a proposta de valor em uma frase (público + diferencial)'},{id:'a3_2',text:'Colocar os 3 principais diferenciais nas 5 primeiras fotos'},{id:'a3_3',text:'Criar ou melhorar um diferencial simples que hoje falta (ex.: kit de boas-vindas)'}]}
]},
/* 4 */
{title:'Anúncio que desperta desejo', screens:[
 {kind:'learn', title:'O funil do anúncio: ver, consultar, reservar',
  body:'<p>Muitas plataformas mostram no painel do anfitrião quantas pessoas <b>viram</b> o anúncio, quantas <b>consultaram</b> ou começaram uma reserva e quantas <b>reservaram</b>. Esse é o funil da sua hospedagem:</p><div class="za-card"><b>Visualizações → Consultas → Reservas</b></div><ul><li>Poucas visualizações: problema de <b>exposição</b> (calendário, preço na lista, posição na busca).</li><li>Muitas visualizações e poucas consultas: o <b>anúncio</b> não desperta desejo (foto de capa, título, preço exibido).</li><li>Muitas consultas e poucas reservas: o problema está na <b>decisão</b> (atendimento, regras, confiança).</li></ul><p>Sem esses números, o Raio-X usa a pontuação do anúncio como hipótese.</p>',
  example:'Exemplo ilustrativo: 600 visualizações, 12 consultas e 3 reservas. De cada 50 pessoas que viram, 1 consultou; de cada 4 que consultaram, 1 reservou. As duas passagens podem ser investigadas.'},
 {kind:'compare', title:'O que pesa no clique',
  cols:[{h:'Afasta',type:'bad',items:['Foto de capa escura ou torta','Título com “lindo”, “aconchegante” e nada concreto','Poucas fotos ou fotos repetidas','Descrição que começa pelas regras']},
        {h:'Atrai',type:'good',items:['Capa clara mostrando o principal diferencial','Título com diferencial e ocasião','20 a 30 fotos em ordem de importância (orientativo)','Descrição que começa pela experiência']}]},
 {kind:'form', title:'Seu anúncio e o seu funil', intro:'Se não tiver os números do funil, marque “não sei”.',
  fields:[
   {id:'visualizacoes',label:'Visualizações do anúncio no mês',type:'number',required:true,min:0,step:1,allowUnknown:true},
   {id:'consultas',label:'Consultas ou pedidos de reserva no mês',type:'number',required:true,min:0,step:1,allowUnknown:true},
   {id:'n_fotos',label:'Quantas fotos o anúncio tem?',type:'number',required:true,min:0,max:200,step:1,unit:'fotos'},
   {id:'fotos_qual',label:'Qualidade das fotos: luz, enquadramento, nitidez (1 a 5)',type:'radio',required:true,options:ESC5('fracas','profissionais')},
   {id:'titulo_benef',label:'O título cita um diferencial ou benefício concreto?',type:'radio',required:true,options:[{v:'sim',l:'Sim'},{v:'nao',l:'Não'}]},
   {id:'desc_benef',label:'A descrição começa pela experiência e pelos benefícios?',type:'radio',required:true,options:[{v:'sim',l:'Sim'},{v:'parcial',l:'Mais ou menos'},{v:'nao',l:'Não, começa por regras ou lista de itens'}]}
  ]},
 {kind:'feedback', title:'Onde o hóspede para',
  metrics:function(s,c){return [{label:'Pontuação do anúncio',value:F.num(c.sAnun,0)+'/100',tag:'calculado'},{label:'Visualização → consulta',value:c.txConsulta==null?'sem dado':F.pct(c.txConsulta*100,1),tag:c.txConsulta==null?'hipotese':'calculado'},{label:'Consulta → reserva',value:c.txReserva==null?'sem dado':F.pct(c.txReserva*100,1),tag:c.txReserva==null?'hipotese':'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.hipFunil==='consulta_reserva') o.push({lv:'warn',t:'Menos de 1 em cada 3 consultas vira reserva (parâmetro orientativo da metodologia). <b>Constatação:</b> o hóspede se interessa, mas desiste na conversa. Revise tempo de resposta, clareza de regras e como você apresenta o valor.'});
   else if(c.hipFunil==='visita_consulta') o.push({lv:'warn',t:'<b>Hipótese:</b> o anúncio (pontuação '+F.num(c.sAnun,0)+'/100) pode estar perdendo o hóspede no clique. Capa, título e primeiras fotos são o primeiro alvo.'});
   else if(c.hipFunil==='visibilidade') o.push({lv:'info',t:'O anúncio está bem avaliado e as consultas convertem. <b>Hipótese:</b> o gargalo pode ser exposição (calendário aberto, preço na lista, estadia mínima). Teste um ajuste por vez.'});
   else o.push({lv:'warn',t:'Sem os números do funil, não dá para afirmar em que etapa o hóspede desiste. Tratamos a pontuação do anúncio ('+F.num(c.sAnun,0)+'/100) como <b>hipótese</b>. Procure esses dados no painel da plataforma.'});
   if(s.n('n_fotos',0)<15) o.push({lv:'warn',t:'Só '+F.num(s.n('n_fotos',0))+' fotos. O hóspede não consegue “visitar” o lugar. Mostre cada ambiente, os diferenciais e o entorno.'});
   if(sn(s,'fotos_qual',3)<=2) o.push({lv:'bad',t:'Fotos avaliadas como fracas. Luz natural, horizonte reto e ambientes arrumados mudam muito a primeira impressão, mesmo com celular.'});
   if(s.t('titulo_benef')==='nao') o.push({lv:'warn',t:'O título não cita nenhum diferencial. Troque adjetivos por fatos: “com ofurô e vista para o vale”.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Anotar todo mês visualizações, consultas e reservas do painel'},{id:'a4_2',text:'Trocar a foto de capa por uma que mostre o principal diferencial'},{id:'a4_3',text:'Reescrever o título com diferencial + ocasião'}]}
]},
/* 5 */
{title:'Preço e rentabilidade', screens:[
 {kind:'learn', title:'Preço é uma comparação, não só um número',
  body:'<p>O hóspede compara sua diária com os anúncios parecidos que aparecem ao lado. Se o seu preço está bem acima <b>sem diferenciais visíveis</b>, ele escolhe outro. Se está bem abaixo, pode desconfiar ou você pode estar deixando dinheiro na mesa.</p><p>Ao mesmo tempo, o preço precisa pagar a conta: comissão, custos de cada estadia e custos fixos do mês. Baixar a diária para encher o calendário só faz sentido se a conta continuar fechando.</p>',
  example:'Exemplo ilustrativo: diária de R$ 250 contra R$ 280 dos concorrentes (11% abaixo). Com 9 noites, 3 reservas, comissão de 15%, R$ 120 de custo por estadia e R$ 1.800 de custo fixo, o mês fecha em 2.250 × 0,85 − 360 − 1.800 = <b>−R$ 247,50</b>. Preço baixo e mês negativo: o problema não se resolve só com desconto.'},
 {kind:'compare', title:'Duas formas de usar o preço',
  cols:[{h:'Preço como muleta',type:'bad',items:['Desconto sempre que o calendário esvazia','Sem saber quanto custa cada estadia','Competir com o anúncio mais barato','Resultado do mês desconhecido']},
        {h:'Preço como estratégia',type:'good',items:['Comparar com 3 a 5 anúncios realmente parecidos','Saber o resultado do mês','Desconto com motivo e prazo','Justificar preço maior com diferenciais visíveis']}]},
 {kind:'form', title:'Seu preço e seus custos', intro:'Se não souber custos ou concorrência, marque “não sei” — o dossiê indicará como hipótese.',
  fields:[
   {id:'preco_conc',label:'Diária média de 3 a 5 concorrentes parecidos',type:'money',required:true,allowUnknown:true,help:'Mesma região, capacidade e padrão, nas mesmas datas.'},
   {id:'comissao',label:'Comissão média da plataforma',type:'percent',required:true,max:40},
   {id:'custo_fixo',label:'Custos fixos da hospedagem no mês',type:'money',required:true,allowUnknown:true,help:'Financiamento ou aluguel, condomínio, internet, contas fixas, contador, manutenção.'},
   {id:'custo_estadia',label:'Custo por estadia (limpeza, lavanderia, amenities)',type:'money',required:true,allowUnknown:true}
  ]},
 {kind:'feedback', title:'Seu preço em perspectiva',
  metrics:function(s,c){return [{label:'Diferença para concorrentes',value:c.gap==null?'sem dado':(c.gap>=0?'+':'')+F.pct(c.gap*100,1),tag:c.gap==null?'hipotese':'calculado'},{label:'Resultado estimado do mês',value:c.resultado==null?'sem dado':F.brl(c.resultado),tag:c.resultado==null?'hipotese':'estimativa'},{label:'Pontuação de preço',value:c.sPreco==null?'sem dado':F.num(c.sPreco,0)+'/100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.gap==null) o.push({lv:'warn',t:'Sem a diária dos concorrentes, não dá para saber se o preço afasta o hóspede. <b>Hipótese a verificar</b>: pesquise 3 a 5 anúncios parecidos nas mesmas datas.'});
   else if(c.gap>0.15) o.push({lv:'warn',t:'Sua diária está '+F.pct(c.gap*100,0)+' acima dos concorrentes. Isso só funciona se os diferenciais estiverem muito evidentes (pontuação de diferenciais: '+F.num(c.sDif,0)+'/100).'});
   else if(c.gap<-0.15) o.push({lv:'warn',t:'Sua diária está '+F.pct(-c.gap*100,0)+' abaixo dos concorrentes e mesmo assim o calendário não enche. Isso sugere que o problema <b>não é preço</b>: olhe anúncio, público e diferenciais.'});
   else o.push({lv:'info',t:'Sua diária está próxima da concorrência ('+(c.gap>=0?'+':'')+F.pct(c.gap*100,0)+'). O preço dificilmente é o único motivo do calendário vazio.'});
   if(c.resultado==null) o.push({lv:'warn',t:'Sem custos fixos e custo por estadia, o resultado do mês fica desconhecido. Baixar preço sem esse número é arriscado.'});
   else if(c.resultado<0) o.push({lv:'bad',t:'Estimativa: o mês fecha em '+F.brl(c.resultado)+'. Antes de novos descontos, calcule sua diária mínima (veja a mini mentoria A02).'});
   else o.push({lv:'ok',t:'Estimativa: o mês fecha positivo em '+F.brl(c.resultado)+'.'});
   if(c.reservas==null&&c.resultado!=null) o.push({lv:'info',t:'Como o número de reservas não foi informado, o resultado usa a hipótese de estadia média de 2 noites.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Pesquisar 5 concorrentes parecidos nas mesmas datas e anotar as diárias'},{id:'a5_2',text:'Calcular o resultado do mês antes de qualquer novo desconto'},{id:'a5_3',text:'Dar desconto só com motivo e prazo (ex.: semana específica)'}]}
]},
/* 6 */
{title:'Experiência do hóspede', screens:[
 {kind:'learn', title:'Avaliações e resposta: a confiança que fecha a reserva',
  body:'<p>Quem não conhece o lugar decide pelo que outros hóspedes contaram. A <b>nota</b>, a <b>quantidade de avaliações</b> e o que aparece nos comentários pesam na decisão, e reclamações repetidas (limpeza, barulho, internet) afastam novos hóspedes mesmo com nota alta.</p><p>O <b>tempo de resposta</b> também conta: quem pergunta costuma consultar outros anúncios ao mesmo tempo. Quem responde primeiro e com clareza tem vantagem.</p>',
  example:'Exemplo: dois anúncios com nota 4,8. Um tem 3 avaliações e o outro tem 60. Para o hóspede, o segundo parece mais seguro, porque a nota foi confirmada por muito mais gente.'},
 {kind:'compare', title:'Reclamação ignorada × reclamação resolvida',
  cols:[{h:'Ignorada',type:'bad',items:['Responder avaliação negativa na defensiva','Repetir o mesmo problema em várias estadias','Demorar horas para responder consultas','Não pedir avaliação ao fim da estadia']},
        {h:'Resolvida',type:'good',items:['Agradecer e dizer o que foi corrigido','Checklist para o problema não voltar','Respostas prontas para as perguntas frequentes','Mensagem de despedida pedindo avaliação']}]},
 {kind:'form', title:'Sua reputação hoje',
  fields:[
   {id:'nota',label:'Nota média das avaliações (0 a 5)',type:'number',required:true,min:0,max:5,step:0.01,allowUnknown:true},
   {id:'n_avaliacoes',label:'Quantidade de avaliações',type:'number',required:true,min:0,step:1,allowUnknown:true},
   {id:'tempo_resp',label:'Em quanto tempo você costuma responder uma consulta?',type:'radio',required:true,options:[{v:'1h',l:'Em até 1 hora'},{v:'6h',l:'Em até 6 horas'},{v:'24h',l:'Em até 24 horas'},{v:'mais',l:'Mais de 24 horas'}]},
   {id:'reclamacoes',label:'Quais reclamações já apareceram mais de uma vez?',type:'checks',options:[{v:'limpeza',l:'Limpeza'},{v:'barulho',l:'Barulho'},{v:'wifi',l:'Internet'},{v:'checkin',l:'Check-in ou acesso difícil'},{v:'conforto',l:'Cama, chuveiro ou conforto'},{v:'fotos',l:'Lugar diferente das fotos'},{v:'nenhuma',l:'Nenhuma reclamação recorrente'}]}
  ]},
 {kind:'feedback', title:'Sua experiência na visão do hóspede',
  metrics:function(s,c){return [{label:'Pontuação de experiência',value:F.num(c.sExp,0)+'/100',tag:c.nota==null?'hipotese':'calculado'},{label:'Nota média',value:c.nota==null?'sem dado':F.num(c.nota,2),tag:c.nota==null?'hipotese':'informado'},{label:'Reclamações recorrentes',value:String(c.nRecl),tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(c.nota==null) o.push({lv:'warn',t:'Sem a nota média, a pontuação de experiência considera só tempo de resposta e reclamações. É uma <b>hipótese parcial</b>.'});
   else if(c.nota<4.5) o.push({lv:'bad',t:'Nota de '+F.num(c.nota,2)+'. Leia as últimas avaliações e encontre o motivo que se repete: ele é prioridade antes de investir em divulgação.'});
   else o.push({lv:'ok',t:'Nota de '+F.num(c.nota,2)+'. Use trechos de avaliações positivas como argumento nas respostas às consultas.'});
   var na=s.n('n_avaliacoes'); if(ZA.isNum(na)&&na<5) o.push({lv:'warn',t:'Apenas '+F.num(na)+' avaliações. Peça avaliação na mensagem de despedida de cada estadia.'});
   if(c.nRecl>0) o.push({lv:'warn',t:'Reclamações recorrentes: <b>'+c.reclNomes.join(', ')+'</b>. Cada uma precisa de uma correção concreta e de uma resposta pública mostrando o que mudou.'});
   if(['24h','mais'].indexOf(s.t('tempo_resp'))>=0) o.push({lv:'warn',t:'Responder em mais de algumas horas dá tempo para o hóspede fechar com outro anúncio. Prepare respostas prontas e ative notificações.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Criar um checklist para a reclamação mais frequente'},{id:'a6_2',text:'Preparar 5 respostas prontas para as perguntas mais comuns'},{id:'a6_3',text:'Enviar mensagem de despedida pedindo avaliação em toda estadia'}]}
]},
/* 7 */
{title:'Plano de melhoria de 30 dias', screens:[
 {kind:'learn', title:'Uma correção por vez, medindo o efeito',
  body:'<p>O Raio-X juntou cinco dimensões: <b>público, diferenciais, anúncio, preço e experiência</b>. A de menor pontuação é o seu gargalo provável. Mudar tudo ao mesmo tempo impede saber o que funcionou.</p><p>O plano de 30 dias segue três regras: <b>(1)</b> começar pelo gargalo; <b>(2)</b> caber no tempo e no orçamento que você tem; <b>(3)</b> medir ocupação e funil antes e depois.</p>',
  example:'Exemplo: se o gargalo é o anúncio, a semana 1 é refazer a capa e o título; a semana 2, reordenar as fotos; e as semanas 3 e 4 servem para comparar visualizações e consultas com o mês anterior.'},
 {kind:'compare', title:'Plano que trava × plano que anda',
  cols:[{h:'Trava',type:'bad',items:['Lista de 20 melhorias sem ordem','Começar pela reforma mais cara','Mudar preço, fotos e título no mesmo dia','Não anotar os números de antes']},
        {h:'Anda',type:'good',items:['3 prioridades por ordem de impacto','Começar pelo que é barato e rápido','Uma mudança principal por semana','Comparar com os números do Pilar 1']}]},
 {kind:'form', title:'Sua meta e seus recursos',
  fields:[
   {id:'meta_ocup',label:'Ocupação que você quer alcançar como meta',type:'percent',required:true,min:1,max:100,help:'Uma meta, não uma previsão. Comece por algo próximo da realidade.'},
   {id:'horas_sem',label:'Horas por semana disponíveis para as melhorias',type:'number',required:true,min:0,max:80,step:1,unit:'h/semana'},
   {id:'orcamento',label:'Orçamento disponível para melhorias neste mês',type:'money',required:true,help:'Pode ser zero: várias melhorias não custam nada.'},
   {id:'foco',label:'O que é mais importante para você agora?',type:'radio',required:true,options:[{v:'noites',l:'Vender mais noites'},{v:'diaria',l:'Conseguir cobrar uma diária melhor'},{v:'avaliacoes',l:'Melhorar avaliações e reputação'}]}
  ]},
 {kind:'feedback', title:'Seu Raio-X consolidado',
  metrics:function(s,c){return [{label:'Índice Raio-X',value:F.num(c.indice,0)+'/100',tag:'calculado'},{label:'Gargalo provável',value:c.gargalo?c.gargalo.nome:'—',tag:c.confianca<50?'hipotese':'calculado'},{label:'Confiança do diagnóstico',value:F.pct(c.confianca,0),tag:'calculado'},{label:'Noites a mais para a meta',value:F.num(c.noitesMeta,1),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.gargalo) o.push({lv:c.gargalo.v<50?'bad':'warn',t:'Dimensão com menor pontuação: <b>'+c.gargalo.nome+'</b> ('+F.num(c.gargalo.v,0)+'/100). '+(c.confianca<50?'Como faltam muitos dados, trate como <b>hipótese</b> inicial.':'Ela é o ponto de partida do plano.')});
   if(c.ganhoMeta>0) o.push({lv:'info',t:'Para chegar a '+F.pct(s.n('meta_ocup'),0)+' de ocupação seriam cerca de '+F.num(c.noitesMeta,1)+' noites a mais por mês. Na diária atual, isso equivale a '+F.brl(c.ganhoMeta)+' de receita a mais — uma referência da meta, não uma previsão.'});
   else o.push({lv:'ok',t:'Sua ocupação atual já alcança a meta informada. O foco pode ser diária e experiência.'});
   if(s.n('horas_sem',0)<2) o.push({lv:'warn',t:'Com menos de 2 horas por semana, escolha só a ação essencial (Nível 3 do OP3D) e conclua antes de seguir.'});
   if(s.n('orcamento',0)===0) o.push({lv:'info',t:'Orçamento zero: priorize título, ordem das fotos, descrição, respostas prontas e pedido de avaliação. Nada disso custa dinheiro.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Executar uma prioridade por semana, na ordem do OP3D'},{id:'a7_2',text:'Anotar os números de hoje para comparar em 30 dias'},{id:'a7_3',text:'Refazer o Raio-X daqui a 30 dias com os números novos'}]}
]}
],

compute:function(s){
 var c={};
 c.disp=s.n('noites_disp',0); c.vend=Math.min(s.n('noites_vend',0),c.disp); c.p=s.n('diaria_media',0);
 c.ocup=c.disp>0?c.vend/c.disp:0; c.receita=c.vend*c.p; c.revpan=c.disp>0?c.receita/c.disp:0; c.vazias=c.disp-c.vend;
 c.reservas=s.has('reservas_mes')?s.n('reservas_mes'):null;
 c.estadia=(c.reservas!=null&&c.reservas>0)?c.vend/c.reservas:null;
 c.views=s.has('visualizacoes')?s.n('visualizacoes'):null; c.cons=s.has('consultas')?s.n('consultas'):null;
 c.txConsulta=(c.views!=null&&c.views>0&&c.cons!=null)?c.cons/c.views:null;
 c.txReserva=(c.cons!=null&&c.cons>0&&c.reservas!=null)?c.reservas/c.cons:null;
 c.txViewRes=(c.views!=null&&c.views>0&&c.reservas!=null)?c.reservas/c.views:null;
 // dimensões
 c.sPub=(sn(s,'publico_fala',1)-1)/4*60+({sim:40,parcial:20,nao:0}[s.t('publico_fotos')]||0);
 if(s.t('publico')==='indefinido') c.sPub=Math.min(c.sPub,30);
 c.nDifs=(s.v.difs||[]).length;
 c.sDif=Math.min(c.nDifs,5)*10+({todos:50,alguns:25,nenhum:0}[s.t('difs_destaque')]||0);
 c.sAnun=Math.min(s.n('n_fotos',0),25)/25*30+(sn(s,'fotos_qual',1)-1)/4*30+(s.t('titulo_benef')==='sim'?20:0)+({sim:20,parcial:10,nao:0}[s.t('desc_benef')]||0);
 c.conc=s.has('preco_conc')&&s.n('preco_conc')>0?s.n('preco_conc'):null;
 c.gap=c.conc!=null?c.p/c.conc-1:null;
 c.com=s.n('comissao',0)/100;
 c.cf=s.has('custo_fixo')?s.n('custo_fixo'):null; c.ce=s.has('custo_estadia')?s.n('custo_estadia'):null;
 c.resEst=c.reservas!=null?c.reservas:c.vend/2;
 c.resultado=(c.cf!=null&&c.ce!=null)?c.receita*(1-c.com)-c.ce*c.resEst-c.cf:null;
 var base=c.gap==null?null:ZA.clamp(100-Math.abs(c.gap)*200,0,100);
 if(base==null&&c.resultado!=null) base=c.resultado>=0?70:30;
 else if(base!=null&&c.resultado!=null&&c.resultado<0) base=Math.max(0,base-30);
 c.sPreco=base;
 c.nota=s.has('nota')?s.n('nota'):null;
 var recl=(s.v.reclamacoes||[]).filter(function(x){return x!=='nenhuma';});
 var nomes={limpeza:'limpeza',barulho:'barulho',wifi:'internet',checkin:'check-in/acesso',conforto:'conforto',fotos:'diferença em relação às fotos'};
 c.nRecl=recl.length; c.reclNomes=recl.map(function(x){return nomes[x]||x;});
 var resp={'1h':25,'6h':15,'24h':5,'mais':0}[s.t('tempo_resp')]||0, rp=Math.max(0,15-5*c.nRecl);
 c.sExp=c.nota==null?(resp+rp)/40*100:ZA.clamp((c.nota-4)*60,0,60)+resp+rp;
 c.dims=[{k:'publico',nome:'Público prioritário',v:c.sPub},{k:'diferenciais',nome:'Diferenciais',v:c.sDif},{k:'anuncio',nome:'Anúncio',v:c.sAnun},{k:'preco',nome:'Preço e rentabilidade',v:c.sPreco},{k:'experiencia',nome:'Experiência do hóspede',v:c.sExp}];
 var val=c.dims.filter(function(d){return d.v!=null;});
 c.indice=val.length?ZA.sum(val.map(function(d){return d.v;}))/val.length:0;
 c.gargalo=val.length?val.reduce(function(a,b){return b.v<a.v?b:a;}):null;
 c.gargaloK=c.gargalo?c.gargalo.k:'';
 var chave=['reservas_mes','visualizacoes','consultas','preco_conc','custo_fixo','custo_estadia','nota','n_avaliacoes'];
 c.confianca=chave.filter(function(k){return s.has(k);}).length/chave.length*100;
 // hipótese de funil
 if(c.views==null&&c.cons==null) c.hipFunil='sem_dados';
 else if(c.txReserva!=null&&c.txReserva<1/3) c.hipFunil='consulta_reserva';
 else if(c.sAnun<60) c.hipFunil='visita_consulta';
 else c.hipFunil='visibilidade';
 var meta=s.n('meta_ocup',0)/100;
 c.noitesMeta=Math.max(0,meta*c.disp-c.vend); c.ganhoMeta=c.noitesMeta*c.p;
 return c;
},

metrics:function(s,c){return [
 {label:'Ocupação do mês',value:F.pct(c.ocup*100),tag:'calculado'},
 {label:'Receita do mês',value:F.brl(c.receita),tag:'calculado'},
 {label:'Receita por noite disponível',value:F.brl(c.revpan),tag:'calculado'},
 {label:'Índice Raio-X',value:F.num(c.indice,0)+'/100',tag:'calculado'},
 {label:'Gargalo provável',value:c.gargalo?c.gargalo.nome:'—',tag:c.confianca<50?'hipotese':'calculado'},
 {label:'Confiança do diagnóstico',value:F.pct(c.confianca,0),tag:'calculado'},
 {label:'Consulta → reserva',value:c.txReserva==null?'sem dado':F.pct(c.txReserva*100,1),tag:c.txReserva==null?'hipotese':'calculado'},
 {label:'Resultado estimado do mês',value:c.resultado==null?'sem dado':F.brl(c.resultado),tag:c.resultado==null?'hipotese':'estimativa'}
];},

priorities:function(s,c){var L=[];
 if(c.gargalo) L.push({title:DIM_ACAO[c.gargalo.k],why:'É a dimensão com menor pontuação no Raio-X ('+F.num(c.gargalo.v,0)+'/100)'+(c.confianca<50?'; hipótese, pois faltam dados.':'.'),score:9});
 if(c.hipFunil==='consulta_reserva') L.push({title:'Revisar o atendimento das consultas: rapidez, clareza e apresentação do valor',why:'Só '+F.pct(c.txReserva*100,0)+' das consultas viram reserva.',score:9});
 if(c.hipFunil==='sem_dados'||c.confianca<50) L.push({title:'Levantar no painel da plataforma visualizações, consultas e reservas do mês',why:'Sem esses dados, o diagnóstico continua sendo hipótese.',score:8});
 if(c.sAnun<60&&c.gargaloK!=='anuncio') L.push({title:'Refazer a foto de capa e o título do anúncio',why:'Pontuação do anúncio: '+F.num(c.sAnun,0)+'/100.',score:7});
 if(s.t('difs_destaque')!=='todos'&&c.nDifs>0&&c.gargaloK!=='diferenciais') L.push({title:'Levar os diferenciais para o título e as 5 primeiras fotos',why:'Hoje eles não aparecem onde o hóspede decide.',score:7});
 if(c.nDifs===0) L.push({title:'Criar e comunicar ao menos um diferencial concreto',why:'Sem diferencial, o hóspede compara apenas preço.',score:7});
 if(s.t('publico')==='indefinido'&&c.gargaloK!=='publico') L.push({title:'Analisar as últimas reservas e escolher o público prioritário',why:'Sem público definido, o anúncio fica genérico.',score:8});
 if(c.resultado!=null&&c.resultado<0) L.push({title:'Calcular a diária mínima antes de novos descontos',why:'O mês estimado fecha em '+F.brl(c.resultado)+'.',score:8});
 if(c.gap!=null&&c.gap>0.15) L.push({title:'Justificar a diária acima do mercado com diferenciais visíveis ou ajustar o preço',why:'Diária '+F.pct(c.gap*100,0)+' acima dos concorrentes.',score:6});
 if(c.gap!=null&&c.gap<-0.15) L.push({title:'Parar de baixar o preço e corrigir a oferta',why:'Diária '+F.pct(-c.gap*100,0)+' abaixo do mercado e o calendário continua vazio.',score:6});
 if(c.gap==null) L.push({title:'Pesquisar 5 concorrentes parecidos nas mesmas datas',why:'Falta referência de preço.',score:5});
 if(c.nRecl>0) L.push({title:'Eliminar a reclamação recorrente: '+c.reclNomes[0],why:'Reclamações repetidas afastam novos hóspedes.',score:c.nota!=null&&c.nota<4.5?8:6});
 if(['24h','mais'].indexOf(s.t('tempo_resp'))>=0) L.push({title:'Responder consultas em até 1 hora com respostas prontas',why:'Resposta lenta abre espaço para o concorrente.',score:6});
 if(!s.has('n_avaliacoes')||s.n('n_avaliacoes',0)<5) L.push({title:'Pedir avaliação ao fim de cada estadia',why:'Poucas avaliações (ou número desconhecido) reduzem a confiança de quem ainda não conhece o lugar.',score:5});
 if(s.n('n_fotos',0)<15) L.push({title:'Produzir fotos de todos os ambientes, diferenciais e entorno',why:'O anúncio tem só '+F.num(s.n('n_fotos',0))+' fotos.',score:5});
 if(c.hipFunil==='visibilidade') L.push({title:'Testar um ajuste de exposição por vez (calendário, estadia mínima, preço na lista)',why:'Anúncio e conversão estão bons; a hipótese é pouca exposição.',score:6});
 return L;},

report:function(s,c){
 function org(id,lbl){return s.has(id)?tg('informado'):tg('hipotese','sem dado');}
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Noites disponíveis no mês',F.num(c.disp),tg('informado')],
  ['Noites vendidas no mês',F.num(c.vend),tg('informado')],
  ['Diária média',F.brl(c.p),tg('informado')],
  ['Reservas no mês',c.reservas==null?'—':F.num(c.reservas),org('reservas_mes')],
  ['Visualizações / consultas',(c.views==null?'—':F.num(c.views))+' / '+(c.cons==null?'—':F.num(c.cons)),(c.views!=null&&c.cons!=null)?tg('informado'):tg('hipotese','incompleto')],
  ['Diária dos concorrentes',c.conc==null?'—':F.brl(c.conc),org('preco_conc')],
  ['Custos fixos / custo por estadia',(c.cf==null?'—':F.brl(c.cf))+' / '+(c.ce==null?'—':F.brl(c.ce)),(c.cf!=null&&c.ce!=null)?tg('informado'):tg('hipotese','incompleto')],
  ['Reservas usadas no resultado',F.num(c.resEst,1),c.reservas==null?tg('hipotese','hipótese: estadia de 2 noites'):tg('informado')],
  ['Nota média',c.nota==null?'—':F.num(c.nota,2),org('nota')],
  ['Ocupação-meta',F.pct(s.n('meta_ocup'),0),tg('informado')]],[1]);
 var dimRows=c.dims.map(function(d){var leit=d.v==null?'sem dados para pontuar':d.v<50?'crítico':d.v<75?'pode melhorar':'bom';
   return [esc(d.nome),d.v==null?'—':F.num(d.v,0)+'/100',leit+(c.gargalo&&d.k===c.gargalo.k?' · <b>gargalo provável</b>':'')];});
 var dimT=ZA.table(['Dimensão','Pontuação','Leitura'],dimRows,[1]);
 var fun=ZA.table(['Etapa','Número','Passagem'],[
  ['Visualizações',c.views==null?'sem dado':F.num(c.views),'—'],
  ['Consultas',c.cons==null?'sem dado':F.num(c.cons),c.txConsulta==null?'sem dado':F.pct(c.txConsulta*100,1)+' das visualizações'],
  ['Reservas',c.reservas==null?'sem dado':F.num(c.reservas),c.txReserva==null?'sem dado':F.pct(c.txReserva*100,1)+' das consultas']],[1]);
 var HF={consulta_reserva:'<b>Constatação (dados informados):</b> o hóspede consulta, mas não fecha. O ponto de perda está na conversa: tempo de resposta, regras, confiança e apresentação do valor.',
   visita_consulta:'<b>Hipótese:</b> as consultas convertem, mas a pontuação do anúncio sugere que o hóspede desiste antes de consultar (capa, título, primeiras fotos).',
   visibilidade:'<b>Hipótese:</b> anúncio e conversão estão bem; a limitação pode estar na exposição (calendário fechado, estadia mínima alta, preço exibido na lista).',
   sem_dados:'<b>Hipótese:</b> sem os números do funil, não é possível afirmar em que etapa o hóspede desiste. As conclusões vêm das pontuações das dimensões e precisam ser confirmadas com os dados do painel.'};
 var leitura=[];
 leitura.push('<li>'+tg('calculado','constatação')+' Ocupação de '+F.pct(c.ocup*100)+' com '+F.num(c.vazias)+' noites vazias e receita por noite disponível de '+F.brl(c.revpan)+'.</li>');
 if(c.gap!=null) leitura.push('<li>'+tg('calculado','constatação')+' Diária '+(c.gap>=0?F.pct(c.gap*100,0)+' acima':F.pct(-c.gap*100,0)+' abaixo')+' da média informada dos concorrentes.</li>');
 else leitura.push('<li>'+tg('hipotese')+' O preço pode ou não estar afastando hóspedes: falta a referência dos concorrentes.</li>');
 if(c.resultado!=null) leitura.push('<li>'+tg('estimativa')+' Resultado estimado do mês: '+F.brl(c.resultado)+(c.reservas==null?' (com hipótese de estadia média de 2 noites)':'')+'.</li>');
 else leitura.push('<li>'+tg('hipotese')+' Não sabemos se o mês fecha positivo: faltam custos.</li>');
 if(c.nota==null) leitura.push('<li>'+tg('hipotese')+' A experiência foi pontuada sem a nota média; a leitura é parcial.</li>');
 var como='<p class="za-small">Como a pontuação é calculada (critérios da metodologia Zion, orientativos): <b>Público</b> = clareza do anúncio (até 60) + fotos com uso do espaço (até 40). <b>Diferenciais</b> = 10 por diferencial, até 5 (até 50) + destaque no título/fotos (até 50). <b>Anúncio</b> = quantidade de fotos até 25 (até 30) + qualidade (até 30) + título com benefício (20) + descrição por benefícios (até 20). <b>Preço</b> = 100 menos 2 pontos por ponto percentual de distância dos concorrentes, com −30 se o mês estimado fecha negativo. <b>Experiência</b> = nota acima de 4 (até 60) + tempo de resposta (até 25) + ausência de reclamações recorrentes (até 15). Dimensões sem dado ficam fora do índice.</p>';
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var hs=s.n('horas_sem',0), orc=s.n('orcamento',0);
 var plan='<div class="za-card"><b>Roteiro de 30 dias</b> · '+F.num(hs)+' h/semana · orçamento de '+F.brl(orc)+'<ol>'+
  '<li><b>Semana 1:</b> anotar os números de hoje (ocupação '+F.pct(c.ocup*100)+', funil e nota) e '+(top[0]?esc(top[0].title).toLowerCase():'confirmar os dados informados')+'.</li>'+
  '<li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Revisar título e foto de capa')+'.</li>'+
  '<li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Preparar respostas prontas e pedido de avaliação')+'.</li>'+
  '<li><b>Semana 4:</b> comparar ocupação, visualizações, consultas e reservas com a semana 1; refazer o Raio-X e decidir a próxima prioridade.</li></ol>'+
  (orc===0?'<p class="za-small">Com orçamento zero, priorize mudanças de texto, ordem de fotos e atendimento.</p>':'')+'</div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Raio-X por dimensão',html:dimT+'<p>Índice Raio-X: <b>'+F.num(c.indice,0)+'/100</b> · confiança do diagnóstico: <b>'+F.pct(c.confianca,0)+'</b> dos dados-chave informados.</p>'+como},
  {title:'Funil de reservas',html:fun+'<p>'+HF[c.hipFunil]+'</p>'},
  {title:'Constatações e hipóteses',html:'<ul>'+leitura.join('')+'</ul><p class="za-small">“Constatação” vem de dados que você informou. “Hipótese” indica que faltam dados: confirme antes de tomar decisões grandes.</p>'}
 ],plan:plan};
}
});
})();
