/* ZAR-A04 · Seu Anúncio Está Afastando Hóspedes? · Construtor Inteligente de Anúncios */
(function(){
var F=ZA.fmt, esc=ZA.esc;
var TGL={hipotese:'hipótese',recomendacao:'recomendação'};
function tg(t,l){return '<span class="za-tag '+t+'">'+(l||TGL[t]||t)+'</span>';}
var LIM=50; /* limite orientativo de caracteres do título; confira o da sua plataforma */
var GENERICOS=['lindo','linda','lindos','lindas','aconchegante','aconchegantes','maravilhoso','maravilhosa','ótimo','ótima','incrível','incrivel','perfeito','perfeita','top','charmoso','charmosa','agradável','bonito','bonita'];
var DIFS=[
 {v:'vista',l:'Vista (montanha, mar, vale, lago)',c:'vista panorâmica',b:'Vista aberta para contemplar a paisagem do amanhecer ao pôr do sol.'},
 {v:'ofuro',l:'Ofurô, banheira ou hidromassagem',c:'ofurô',b:'Ofurô para relaxar no fim do dia, depois dos passeios.'},
 {v:'lareira',l:'Lareira ou fogão a lenha',c:'lareira',b:'Lareira para as noites frias, com lenha à disposição.'},
 {v:'piscina',l:'Piscina',c:'piscina',b:'Piscina para aproveitar os dias de sol sem sair da hospedagem.'},
 {v:'natureza',l:'Trilhas, mata ou cachoeira no local',c:'trilha e natureza',b:'Trilhas e natureza a poucos passos, para quem quer desacelerar.'},
 {v:'cafe',l:'Café da manhã incluso',c:'café da manhã',b:'Café da manhã incluso, para começar o dia sem preocupação.'},
 {v:'pet',l:'Aceita pets',c:'pet friendly',b:'Seu pet é bem-vindo: ninguém da família precisa ficar para trás.'},
 {v:'homeoffice',l:'Internet rápida e espaço para trabalhar',c:'Wi-Fi rápido',b:'Internet rápida e uma mesa confortável para trabalhar.'},
 {v:'centro',l:'Localização central (a pé do centro ou da praia)',c:'localização central',b:'Localização central: dá para fazer muita coisa a pé.'},
 {v:'cozinha',l:'Cozinha completa',c:'cozinha completa',b:'Cozinha completa para preparar as refeições do seu jeito.'},
 {v:'estacionamento',l:'Estacionamento no local',c:'estacionamento',b:'Estacionamento no local, sem preocupação com o carro.'},
 {v:'experiencias',l:'Experiências (passeios, jantar, kits especiais)',c:'experiências locais',b:'Experiências locais que podem ser combinadas com antecedência.'}];
function dif(v){for(var i=0;i<DIFS.length;i++) if(DIFS[i].v===v) return DIFS[i]; return null;}
var PUB_T={casais:'Para casais',familias:'Para famílias',amigos:'Para grupos de amigos',remoto:'Para trabalho remoto',pet:'Para você e seu pet',aventura:'Para aventureiros'};
var PUB_D={casais:'casais',familias:'famílias',amigos:'grupos de amigos',remoto:'quem trabalha remoto',pet:'quem viaja com pet',aventura:'quem gosta de aventura'};
var OCAS_T={romantico:'Refúgio a dois',familia:'Férias em família',descanso:'Descanso e silêncio',remoto:'Trabalho e natureza',aventura:'Base para aventura',feriado:'Feriado especial'};
var OCAS_D={romantico:'para um fim de semana a dois',familia:'para férias em família',descanso:'para descansar e desligar da rotina',remoto:'para trabalhar com tranquilidade fora de casa',aventura:'para quem vem explorar a região',feriado:'para aproveitar feriados e datas especiais'};
var COMOD={wifi:'Wi-Fi',roupa:'roupa de cama e banho',estacionamento:'estacionamento',ar:'ar-condicionado ou aquecedor',tv:'TV',churrasqueira:'churrasqueira',maquina:'máquina de lavar',berco:'berço'};
var CHAMADA={datas:'Escolha suas datas e reserve o seu refúgio.',duvidas:'Ficou alguma dúvida? Mande uma mensagem: respondemos rápido.',feriados:'Planejando um feriado? Consulte a disponibilidade com antecedência.'};
var FOTOS=[
 {k:'capa_dif',l:'Capa: o principal diferencial em destaque'},{k:'externa',l:'Vista ou área externa'},{k:'quarto',l:'Quarto e cama arrumada'},{k:'estar',l:'Sala ou espaço de estar'},
 {k:'banheiro',l:'Banheiro'},{k:'cozinha',l:'Cozinha ou copa'},{k:'difs_uso',l:'Outros diferenciais em uso'},{k:'detalhes',l:'Detalhes e decoração'},
 {k:'cafe',l:'Café, amenities e kit de boas-vindas'},{k:'entorno',l:'Entorno e atrativos próximos'},{k:'noite',l:'À noite, com iluminação'},{k:'fachada',l:'Fachada e chegada'}];
function genericos(t){return String(t||'').toLowerCase().split(/[^a-zà-úç]+/).filter(function(w){return GENERICOS.indexOf(w)>=0;}).length;}
function cap(t){t=String(t||'').trim();return t?t.charAt(0).toUpperCase()+t.slice(1):'';}
function semPonto(t){return String(t||'').trim().replace(/[.!\s]+$/,'');}
function juntar(a){return a.length<2?a.join(''):a.slice(0,-1).join(', ')+' e '+a[a.length-1];}

ZA.register({
id:'A04', code:'ZAR-A04', collection:'Hospedagem',
title:'Seu Anúncio Está Afastando Hóspedes?',
subtitle:'Transforme Sua Hospedagem em uma Oferta de Desejo',
tool:'Construtor Inteligente de Anúncios',
deliverable:'Anúncio Revisado e Plano Visual',
nameField:'nome', propertyField:'propriedade',
disclaimer:'Título e descrição são montados a partir de modelos preenchidos com as suas respostas: revise, ajuste ao seu estilo e confira as regras e limites de caracteres da sua plataforma. As pontuações medem a completude do anúncio por critérios da metodologia Zion e não preveem reservas nem faturamento.',

intro:[
 {kind:'mirror', title:'O hóspede vê seu anúncio, mas escolhe outro?',
  lead:'Você sabe que a sua hospedagem é boa. Quem vem, elogia. Mas, na tela do celular, entre dezenas de opções, ela parece só mais uma.',
  body:'<div class="za-card"><p>Algumas situações comuns:</p><ul><li>“Meu título diz ‘lindo chalé aconchegante’, igual a todos.”</li><li>“A foto de capa é a fachada, porque foi a primeira que tirei.”</li><li>“Escrevi a descrição listando os móveis.”</li><li>“O ofurô, que é o que eu tenho de melhor, aparece lá no fim.”</li></ul></div>'},
 {kind:'collapse', title:'Uma hospedagem bonita não é suficiente se o anúncio não transmite seus diferenciais.',
  lead:'O hóspede não visita o lugar antes de reservar. Ele decide pela capa, pelo título e pelas primeiras linhas. Se o seu melhor não está ali, para ele não existe.',
  body:'<div class="za-card"><p>Um anúncio que desperta desejo responde a três perguntas, nesta ordem:</p><ol><li><b>É para mim?</b> (público e ocasião)</li><li><b>Por que este e não outro?</b> (diferenciais e posicionamento)</li><li><b>Posso confiar?</b> (fotos completas, informações claras, avaliações)</li></ol><p>Neste percurso, o Construtor vai pontuar o seu anúncio atual e montar, com as suas respostas, um título, uma descrição e um roteiro de fotos novos.</p></div>'},
 {kind:'start', title:'Vamos reconstruir o seu anúncio',
  lead:'Em 7 pilares você vai diagnosticar o anúncio, definir público e posicionamento e sair com título, descrição e plano de fotos prontos para revisar.',
  body:'<p>Deixe o seu anúncio aberto em outra aba: você vai copiar o título atual e contar as fotos. Nenhum texto é enviado para fora deste navegador: tudo é montado aqui, a partir de modelos.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Fernanda'},
   {id:'propriedade',label:'Nome da hospedagem',type:'text',required:true,placeholder:'Ex.: Chalé Mirante'},
   {id:'tipo',label:'Tipo de hospedagem',type:'select',required:true,options:[{v:'airbnb',l:'Apartamento ou casa (Airbnb/temporada)'},{v:'cabana',l:'Cabana ou chalé'},{v:'glamping',l:'Glamping'},{v:'pousada',l:'Pequena pousada'},{v:'outro',l:'Outro'}]},
   {id:'destino',label:'Cidade / destino',type:'text',required:true,placeholder:'Ex.: Urubici (SC)'},
   {id:'unidades',label:'Quantas unidades você anuncia?',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)'}
  ]}
],

pillars:[
/* 1 */
{title:'Diagnóstico do anúncio', screens:[
 {kind:'learn', title:'Pontue o anúncio como um hóspede apressado',
  body:'<p>O hóspede rola a lista e para em poucos anúncios. Nessa parada rápida, ele olha a capa, lê o título e talvez as primeiras linhas. O diagnóstico do Construtor usa critérios simples, que você consegue checar sozinho:</p><ul><li>O <b>título</b> cita fatos (ofurô, vista, café incluso) em vez de adjetivos (“lindo”, “aconchegante”)?</li><li>O título é <b>curto</b> o bastante para não ser cortado? (usamos '+LIM+' caracteres como referência orientativa)</li><li>A <b>capa</b> mostra o principal diferencial?</li><li>Há fotos suficientes para “visitar” cada ambiente?</li><li>A descrição começa pela experiência e informa regras e acesso com clareza?</li></ul>',
  example:'Exemplo: “Lindo chalé aconchegante na serra” tem 33 caracteres e dois adjetivos genéricos, mas nenhum fato. “Refúgio a dois em chalé com ofurô · Urubici” tem 43 caracteres e diz para quem é, o que tem e onde fica.'},
 {kind:'compare', title:'Adjetivo × fato',
  cols:[{h:'Adjetivos (todo mundo usa)',type:'bad',items:['Lindo','Aconchegante','Maravilhoso','Incrível','Charmoso']},
        {h:'Fatos (só você tem)',type:'good',items:['Ofurô aquecido no deck','Vista para o vale','Lareira e lenha inclusa','A 300 m da praia','Café da manhã caseiro']}]},
 {kind:'form', title:'Seu anúncio hoje',
  fields:[
   {id:'titulo_atual',label:'Copie aqui o título atual do anúncio',type:'text',required:true,max:120},
   {id:'n_fotos',label:'Quantas fotos o anúncio tem?',type:'number',required:true,min:0,max:200,step:1,unit:'fotos',allowUnknown:true},
   {id:'anuncio_tem',label:'Marque o que o seu anúncio já tem',type:'checks',options:[{v:'tit_dif',l:'Título cita um diferencial concreto'},{v:'tit_pub',l:'Título indica para quem é ou a ocasião'},{v:'capa_dif',l:'Foto de capa mostra o principal diferencial'},{v:'luz',l:'Fotos com boa luz natural e horizonte reto'},{v:'desc_exp',l:'Descrição começa pela experiência, não pelas regras'},{v:'desc_info',l:'Descrição informa acesso, check-in e regras com clareza'},{v:'comod',l:'Lista de comodidades completa na plataforma'},{v:'resp_aval',l:'Avaliações recentes respondidas'}]}
  ]},
 {kind:'feedback', title:'Pontuação do anúncio atual',
  metrics:function(s,c){return [{label:'Pontuação atual',value:F.num(c.scoreAtual,0)+'/100',tag:'calculado'},{label:'Caracteres do título',value:String(c.tituloLen),tag:'calculado'},{label:'Adjetivos genéricos no título',value:String(c.nGenericos),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.scoreAtual<50) o.push({lv:'bad',t:'Pontuação de '+F.num(c.scoreAtual,0)+'/100. O anúncio deixa de mostrar boa parte do que faz alguém escolher você. A boa notícia: quase tudo se corrige com texto e ordem de fotos.'});
   else if(c.scoreAtual<75) o.push({lv:'warn',t:'Pontuação de '+F.num(c.scoreAtual,0)+'/100. Há uma base, mas faltam elementos que ajudam o hóspede a decidir.'});
   else o.push({lv:'ok',t:'Pontuação de '+F.num(c.scoreAtual,0)+'/100. O anúncio está completo; o ganho virá de posicionamento e de um título mais preciso.'});
   if(c.nGenericos>0) o.push({lv:'warn',t:'Seu título tem '+c.nGenericos+' adjetivo(s) genérico(s). Troque cada um por um fato que só a sua hospedagem tem.'});
   if(c.tituloLen>LIM) o.push({lv:'warn',t:'O título tem '+c.tituloLen+' caracteres. Títulos longos podem ser cortados na lista de busca; confira o limite da sua plataforma.'});
   if(s.unknown('n_fotos')) o.push({lv:'warn',t:'Número de fotos desconhecido: esse critério ficou com zero. Conte as fotos antes de publicar a nova versão.'});
   else if(s.n('n_fotos',0)<10) o.push({lv:'warn',t:'Só '+F.num(s.n('n_fotos',0))+' fotos. O roteiro do Pilar 5 vai mostrar o que falta.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Salvar uma cópia do anúncio atual (título, descrição e ordem das fotos) antes de mudar'},{id:'a1_2',text:'Anotar visualizações e consultas do mês para comparar depois'},{id:'a1_3',text:'Pedir a duas pessoas de fora que digam, em 5 segundos, o que entenderam do anúncio'}]}
]},
/* 2 */
{title:'Público ideal', screens:[
 {kind:'learn', title:'O anúncio fala com uma pessoa, numa ocasião',
  body:'<p>Mesmo quando recebe públicos variados, o anúncio vende melhor quando escolhe <b>um público principal</b> e <b>uma ocasião</b>: o casal em fim de semana romântico, a família nas férias, quem trabalha remoto e quer natureza por perto.</p><p>Também ajuda saber o <b>desejo principal</b> desse público, aquilo que ele procura acima de tudo: privacidade, espaço para as crianças, silêncio, internet que não cai. Esse desejo vai aparecer no título e no segundo parágrafo da descrição.</p>',
  example:'Exemplo: público “casais”, ocasião “refúgio a dois”, desejo “privacidade e silêncio”. A descrição dirá: “Pensada para casais, para um fim de semana a dois. Aqui você encontra privacidade e silêncio.”'},
 {kind:'compare', title:'Para todos × para alguém',
  cols:[{h:'Para todos',type:'bad',items:['“Ideal para casais, famílias e amigos”','Fotos sem contexto de uso','Descrição sem ocasião']},
        {h:'Para alguém',type:'good',items:['“Refúgio a dois com ofurô”','Fotos mostrando o momento desejado','Descrição que conversa com a viagem do hóspede']}]},
 {kind:'form', title:'Seu público e a ocasião',
  fields:[
   {id:'publico',label:'Público principal',type:'radio',required:true,options:[{v:'casais',l:'Casais'},{v:'familias',l:'Famílias'},{v:'amigos',l:'Grupos de amigos'},{v:'remoto',l:'Quem trabalha remoto'},{v:'pet',l:'Quem viaja com pet'},{v:'aventura',l:'Viajantes de aventura'}]},
   {id:'ocasiao',label:'Ocasião principal da viagem',type:'radio',required:true,options:[{v:'romantico',l:'Refúgio a dois'},{v:'familia',l:'Férias em família'},{v:'descanso',l:'Descanso e desconexão'},{v:'remoto',l:'Trabalho remoto com natureza'},{v:'aventura',l:'Aventura e esportes'},{v:'feriado',l:'Feriados e datas especiais'}]},
   {id:'desejo',label:'O que esse público mais deseja encontrar?',type:'text',required:true,allowUnknown:true,max:80,placeholder:'Ex.: privacidade e silêncio'}
  ]},
 {kind:'feedback', title:'Coerência entre público e ocasião',
  metrics:function(s,c){return [{label:'Público',value:PUB_D[s.t('publico')]||'—',tag:'informado'},{label:'Ocasião',value:OCAS_T[s.t('ocasiao')]||'—',tag:'informado'}];},
  feedback:function(s,c){var o=[],p=s.t('publico'),oc=s.t('ocasiao');
   var par={casais:['romantico','descanso','feriado'],familias:['familia','feriado','descanso'],amigos:['feriado','aventura','descanso'],remoto:['remoto','descanso'],pet:['descanso','aventura','feriado','familia'],aventura:['aventura','descanso']};
   if(par[p]&&par[p].indexOf(oc)<0) o.push({lv:'warn',t:'Público e ocasião parecem pouco combinados ('+esc(PUB_D[p])+' × '+esc(OCAS_T[oc]||'')+'). Confira se a ocasião escolhida é mesmo a de quem mais reserva.'});
   else o.push({lv:'ok',t:'Público e ocasião combinam: o anúncio pode falar de forma direta com '+esc(PUB_D[p]||'o seu hóspede')+'.'});
   if(!s.t('desejo')) o.push({lv:'warn',t:'Desejo principal não informado: a descrição será montada sem essa frase. Pergunte aos próximos hóspedes o que os fez escolher você.'});
   else o.push({lv:'info',t:'O desejo “'+esc(s.t('desejo'))+'” vai entrar na descrição. Garanta que as fotos mostrem isso.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Ler as últimas avaliações e anotar as palavras que os hóspedes usam'},{id:'a2_2',text:'Perguntar aos próximos hóspedes por que escolheram a hospedagem'},{id:'a2_3',text:'Escolher uma foto que mostre o desejo principal do público'}]}
]},
/* 3 */
{title:'Posicionamento', screens:[
 {kind:'learn', title:'Posicionamento é a promessa que o preço precisa sustentar',
  body:'<p>Posicionamento é o lugar que a sua hospedagem ocupa na cabeça do hóspede em comparação com as outras. Três caminhos comuns:</p><ul><li><b>Econômico</b>: o melhor custo-benefício da região, com o essencial bem-feito;</li><li><b>Conforto</b>: estrutura completa e tranquilidade, sem surpresas;</li><li><b>Experiência</b>: um momento memorável, que justifica pagar mais.</li></ul><p>O <b>estilo</b> (rústico, moderno, natureza, praia, histórico) dá o tom das fotos e do texto. A <b>promessa</b> é uma frase que resume a experiência — ela abre a descrição.</p>',
  example:'Exemplo: posicionamento “experiência”, estilo “rústico”, promessa “Acordar com o mar de nuvens e terminar o dia no ofurô”. Tudo no anúncio precisa confirmar essa frase.'},
 {kind:'compare', title:'Promessa vaga × promessa concreta',
  cols:[{h:'Vaga',type:'bad',items:['“Um lugar incrível para relaxar”','“Venha conhecer nosso cantinho”','“Tudo o que você precisa”']},
        {h:'Concreta',type:'good',items:['“Acordar com o mar de nuvens e terminar o dia no ofurô”','“Dias de praia e piscina sem precisar pegar o carro”','“Trabalhar de frente para a mata, com internet estável”']}]},
 {kind:'form', title:'Seu posicionamento',
  fields:[
   {id:'posic',label:'Posicionamento',type:'radio',required:true,options:[{v:'economico',l:'Econômico',d:'Custo-benefício e o essencial bem-feito'},{v:'conforto',l:'Conforto',d:'Estrutura completa e tranquilidade'},{v:'experiencia',l:'Experiência',d:'Um momento memorável'}]},
   {id:'estilo',label:'Estilo da hospedagem',type:'radio',required:true,options:[{v:'rustico',l:'Rústico'},{v:'moderno',l:'Moderno'},{v:'natureza',l:'Imerso na natureza'},{v:'praia',l:'Praia'},{v:'historico',l:'Histórico / charme de época'}]},
   {id:'promessa',label:'Sua promessa em uma frase',type:'text',required:true,max:140,placeholder:'Ex.: Acordar com o mar de nuvens e terminar o dia no ofurô'}
  ]},
 {kind:'feedback', title:'Sua promessa',
  metrics:function(s,c){return [{label:'Caracteres da promessa',value:String(s.t('promessa').length),tag:'calculado'},{label:'Adjetivos genéricos na promessa',value:String(genericos(s.t('promessa'))),tag:'calculado'}];},
  feedback:function(s,c){var o=[],g=genericos(s.t('promessa'));
   o.push({lv:'info',t:'Sua promessa: “'+esc(s.t('promessa'))+'”. Ela vai abrir a descrição.'});
   if(g>0) o.push({lv:'warn',t:'A promessa tem '+g+' adjetivo(s) genérico(s). Descreva o que a pessoa vai fazer, ver ou sentir.'});
   if(s.t('promessa').length<25) o.push({lv:'warn',t:'Promessa muito curta. Inclua uma ação concreta (acordar, mergulhar, trabalhar, acender a lareira).'});
   if(s.t('posic')==='experiencia') o.push({lv:'info',t:'Posicionamento de experiência exige fotos de momentos (ofurô aceso, mesa posta, lareira ao anoitecer), não só de ambientes.'});
   if(s.t('posic')==='economico') o.push({lv:'info',t:'No posicionamento econômico, clareza e honestidade vendem: diga exatamente o que está incluído e o que não está.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Escrever a promessa num papel e conferir se cada foto a confirma'},{id:'a3_2',text:'Eliminar do anúncio o que contradiz o posicionamento'},{id:'a3_3',text:'Alinhar o tom das respostas às consultas ao estilo escolhido'}]}
]},
/* 4 */
{title:'Título comercial', screens:[
 {kind:'learn', title:'Três modelos de título que funcionam',
  body:'<p>O Construtor monta três versões de título com as suas respostas:</p><ul><li><b>Modelo A · Diferencial + tipo + local</b>: “Chalé com ofurô e vista panorâmica · Urubici”.</li><li><b>Modelo B · Ocasião + diferencial</b>: “Refúgio a dois em chalé com ofurô · Urubici”.</li><li><b>Modelo C · Público + diferencial</b>: “Para casais: chalé com ofurô · Urubici”.</li></ul><p>Se a versão escolhida passar de '+LIM+' caracteres (referência orientativa), o Construtor gera uma versão compacta, retirando primeiro o segundo diferencial e depois a localização.</p>',
  example:'Exemplo: “Casa com piscina e localização central · Praia Grande, Ubatuba” tem 62 caracteres. A versão compacta fica “Casa com piscina · Praia Grande, Ubatuba”, com 40.'},
 {kind:'compare', title:'O que entra e o que sai do título',
  cols:[{h:'Sai',type:'bad',items:['Adjetivos genéricos','Nome da hospedagem (já aparece no anúncio)','Letras maiúsculas e excesso de emojis','Informações que mudam (preço, promoção)']},
        {h:'Entra',type:'good',items:['O principal diferencial','Tipo de hospedagem','Ocasião ou público','Referência de localização']}]},
 {kind:'form', title:'Ingredientes do novo título',
  fields:[
   {id:'tipo_nome',label:'Como você chama a hospedagem no título?',type:'text',required:true,max:30,placeholder:'Ex.: Chalé, Cabana, Casa, Apartamento'},
   {id:'dif_principal',label:'Seu principal diferencial',type:'select',required:true,options:DIFS.map(function(d){return {v:d.v,l:d.l};})},
   {id:'difs_extra',label:'Outros diferenciais que você tem',type:'checks',options:DIFS.map(function(d){return {v:d.v,l:d.l};})},
   {id:'local_ref',label:'Referência de localização para o título',type:'text',required:true,max:40,placeholder:'Ex.: Urubici ou Praia Grande, Ubatuba'},
   {id:'modelo_titulo',label:'Qual modelo você prefere usar?',type:'radio',required:true,options:[{v:'A',l:'A · Diferencial + tipo + local'},{v:'B',l:'B · Ocasião + diferencial'},{v:'C',l:'C · Público + diferencial'}]}
  ]},
 {kind:'feedback', title:'Seus títulos',
  metrics:function(s,c){return [{label:'Título escolhido',value:c.tituloFinal,tag:'recomendacao'},{label:'Caracteres',value:String(c.tituloFinalLen),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   ['A','B','C'].forEach(function(k){var t=c.titulos[k];o.push({lv:k===c.modelo?'ok':'info',t:'Modelo '+k+(k===c.modelo?' (escolhido)':'')+': <b>'+esc(t)+'</b> · '+t.length+' caracteres'+(t.length>LIM?' (longo)':'')});});
   if(c.compactado) o.push({lv:'warn',t:'O modelo escolhido passou de '+LIM+' caracteres. Versão compacta sugerida: <b>'+esc(c.tituloFinal)+'</b> ('+c.tituloFinalLen+' caracteres).'});
   if(c.d2==null) o.push({lv:'info',t:'Você marcou apenas um diferencial. Se tiver outro, ele pode entrar no modelo A e na descrição.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Publicar o novo título e anotar a data da mudança'},{id:'a4_2',text:'Testar outro modelo de título depois de 30 dias, se o primeiro não trouxer mais consultas'},{id:'a4_3',text:'Usar o mesmo diferencial principal na foto de capa'}]}
]},
/* 5 */
{title:'Fotografias e apresentação', screens:[
 {kind:'learn', title:'As fotos contam a estadia, na ordem certa',
  body:'<p>As fotos são uma visita guiada. A ordem importa mais do que a quantidade:</p><ol><li><b>Capa</b>: o principal diferencial, no melhor horário de luz;</li><li>A <b>vista</b> ou a área externa;</li><li>Os <b>ambientes</b> na ordem em que o hóspede vai usá-los (quarto, estar, banheiro, cozinha);</li><li>Os <b>outros diferenciais</b> em uso (lareira acesa, mesa posta);</li><li><b>Detalhes</b>, amenities e o <b>entorno</b>;</li><li>Por último, <b>fachada e chegada</b>, que ajudam a encontrar o lugar.</li></ol><p>Dicas práticas, mesmo com celular: luz natural, câmera na altura do peito, horizonte reto, cama arrumada, objetos pessoais fora do quadro.</p>',
  example:'Exemplo: em vez de abrir com a fachada vista da estrada, abra com o ofurô aceso ao entardecer, depois a vista do deck, depois a cama com a janela para o vale.'},
 {kind:'compare', title:'Foto que afasta × foto que atrai',
  cols:[{h:'Afasta',type:'bad',items:['Ambiente escuro, com luz amarela fraca','Foto torta ou cortando a cama','Banheiro com toalhas jogadas','Dez fotos do mesmo ângulo']},
        {h:'Atrai',type:'good',items:['Janelas abertas e luz do dia','Horizonte reto e ambiente inteiro','Toalhas dobradas e amenities à vista','Cada foto mostra algo novo']}]},
 {kind:'form', title:'Quais fotos você já tem',
  fields:[
   {id:'fotos_tem',label:'Marque as fotos de boa qualidade que você já tem',type:'checks',options:FOTOS.map(function(f){return {v:f.k,l:f.l};})},
   {id:'luz',label:'Em que horário a luz fica mais bonita na sua hospedagem?',type:'radio',required:true,options:[{v:'manha',l:'Manhã'},{v:'tarde',l:'Fim de tarde'},{v:'naosei',l:'Ainda não observei'}]},
   {id:'quem_fotografa',label:'Quem vai fazer as fotos que faltam?',type:'radio',required:true,options:[{v:'eu',l:'Eu, com celular'},{v:'prof',l:'Fotógrafo profissional'},{v:'indef',l:'Ainda não sei'}]}
  ]},
 {kind:'feedback', title:'Seu roteiro de fotos',
  metrics:function(s,c){return [{label:'Cobertura do roteiro',value:F.pct(c.fotosCobertura*100,0),tag:'calculado'},{label:'Fotos a produzir',value:String(c.fotosFaltam.length),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.fotosFaltam.length) o.push({lv:c.fotosCobertura<0.5?'warn':'info',t:'Fotos a produzir: '+c.fotosFaltam.map(function(f){return '<b>'+esc(f)+'</b>';}).join(', ')+'.'});
   else o.push({lv:'ok',t:'Você já tem todas as fotos do roteiro. Agora, só falta colocá-las na ordem sugerida.'});
   if(c.fotosTemK.indexOf('capa_dif')<0) o.push({lv:'bad',t:'Falta a foto mais importante: a capa com '+esc(c.d1?c.d1.c:'o principal diferencial')+'. Ela é a prioridade número 1 da sessão de fotos.'});
   if(s.t('luz')==='naosei') o.push({lv:'warn',t:'Observe a luz em dois horários (manhã e fim de tarde) antes de fotografar a capa.'});
   else o.push({lv:'info',t:'Fotografe a capa e a área externa '+(s.t('luz')==='manha'?'pela manhã':'no fim de tarde')+', quando a luz é melhor na sua hospedagem.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Reordenar as fotos atuais seguindo o roteiro, ainda hoje'},{id:'a5_2',text:'Agendar a sessão de fotos que faltam no melhor horário de luz'},{id:'a5_3',text:'Arrumar cada ambiente com um checklist antes de fotografar'}]}
]},
/* 6 */
{title:'Descrição e benefícios', screens:[
 {kind:'learn', title:'Descrição em blocos: da experiência às informações práticas',
  body:'<p>A maioria das pessoas lê só o começo da descrição. Por isso, o Construtor monta o texto em blocos, do mais desejado ao mais prático:</p><ol><li><b>Promessa</b> (a frase do Pilar 3);</li><li><b>Para quem é</b> (público, ocasião e desejo);</li><li><b>Diferenciais como benefícios</b>: não “tem ofurô”, mas “ofurô para relaxar no fim do dia”;</li><li><b>O espaço</b>: capacidade, quartos e comodidades;</li><li><b>Localização e acesso</b>, com honestidade sobre estrada de terra, se houver;</li><li><b>Check-in</b> e chamada final.</li></ol>',
  example:'Exemplo de diferencial transformado em benefício: “Lareira” vira “Lareira para as noites frias, com lenha à disposição.” “Aceita pets” vira “Seu pet é bem-vindo: ninguém da família precisa ficar para trás.”'},
 {kind:'compare', title:'Lista de itens × benefícios',
  cols:[{h:'Lista de itens',type:'bad',items:['“1 cama de casal, 1 sofá, TV, micro-ondas”','Regras no primeiro parágrafo','Esconder que o acesso é de terra']},
        {h:'Benefícios',type:'good',items:['“Cozinha completa para preparar as refeições do seu jeito”','Regras no fim, de forma clara','Acesso explicado com honestidade e orientações']}]},
 {kind:'form', title:'Informações para a descrição',
  fields:[
   {id:'capacidade',label:'Capacidade máxima de hóspedes',type:'number',required:true,min:1,max:60,step:1,unit:'hóspedes'},
   {id:'quartos',label:'Número de quartos',type:'number',required:true,min:0,max:30,step:1,unit:'quartos',help:'Use 0 para estúdio ou ambiente integrado.'},
   {id:'comodidades',label:'Comodidades',type:'checks',options:Object.keys(COMOD).map(function(k){return {v:k,l:COMOD[k].charAt(0).toUpperCase()+COMOD[k].slice(1)};})},
   {id:'acesso',label:'Como é o acesso?',type:'radio',required:true,options:[{v:'asfalto',l:'Asfalto até a porta'},{v:'terra_boa',l:'Trecho de terra em boas condições'},{v:'terra_dificil',l:'Trecho de terra que exige atenção na chuva'}]},
   {id:'distancia_km',label:'Distância até o centro da cidade',type:'number',required:true,min:0,max:500,step:0.1,unit:'km',allowUnknown:true},
   {id:'checkin',label:'Como é o check-in?',type:'radio',required:true,options:[{v:'autonomo',l:'Autônomo (senha, cofre de chaves)'},{v:'presencial',l:'Presencial'}]}
  ]},
 {kind:'feedback', title:'Sua descrição montada',
  metrics:function(s,c){return [{label:'Blocos da descrição',value:String(c.descParas.length),tag:'calculado'},{label:'Caracteres',value:F.num(c.descChars),tag:'calculado'},{label:'Benefícios incluídos',value:String(c.nDifs),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:'info',t:'Prévia do início: “'+c.descParas[0]+'” A descrição completa está no relatório.'});
   if(c.nComod<3) o.push({lv:'warn',t:'Poucas comodidades marcadas ('+c.nComod+'). Hóspedes filtram por elas: confira se não esqueceu Wi-Fi, roupa de cama ou estacionamento.'});
   if(s.t('acesso')==='terra_dificil') o.push({lv:'info',t:'Acesso que exige atenção foi descrito com honestidade e com a promessa de enviar orientações. Isso evita avaliação negativa por surpresa.'});
   if(s.unknown('distancia_km')) o.push({lv:'warn',t:'Distância até o centro desconhecida: a descrição não cita a distância. Meça no mapa, é uma das perguntas mais comuns.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Revisar a descrição montada e ajustar ao seu jeito de falar'},{id:'a6_2',text:'Atualizar a lista de comodidades na plataforma'},{id:'a6_3',text:'Preparar uma mensagem com orientações de acesso para enviar antes da chegada'}]}
]},
/* 7 */
{title:'Anúncio revisado', screens:[
 {kind:'learn', title:'Juntar, revisar e publicar',
  body:'<p>Com título, descrição e roteiro de fotos prontos, falta decidir o <b>tom</b> e a <b>chamada final</b>, e marcar um prazo para as fotos que faltam.</p><ul><li><b>Tom acolhedor</b>: abre com “Que bom ter você por aqui.”;</li><li><b>Tom sofisticado</b>: abre com o nome da hospedagem e a promessa, sem exclamações;</li><li><b>Tom aventureiro</b>: abre com a promessa e apresenta a hospedagem como ponto de partida.</li></ul><p>A pontuação final mede a <b>completude</b> do anúncio revisado pelos mesmos critérios Zion. Ela mostra o quanto o anúncio ficou mais claro; não é uma previsão de reservas.</p>',
  example:'Exemplo: anúncio atual com 40/100 e anúncio revisado com 85/100. O ganho vem de título com fato e ocasião, três diferenciais descritos como benefícios e metade do roteiro de fotos já coberto.'},
 {kind:'compare', title:'Publicar tudo de uma vez × publicar e medir',
  cols:[{h:'Tudo de uma vez',type:'bad',items:['Trocar título, fotos, preço e regras no mesmo dia','Não guardar a versão anterior','Não saber o que funcionou']},
        {h:'Publicar e medir',type:'good',items:['Título e descrição primeiro, depois as fotos','Versão anterior salva','Comparar visualizações e consultas a cada 2 semanas']}]},
 {kind:'form', title:'Acabamento do anúncio',
  fields:[
   {id:'tom',label:'Tom do texto',type:'radio',required:true,options:[{v:'acolhedor',l:'Acolhedor'},{v:'sofisticado',l:'Sofisticado'},{v:'aventureiro',l:'Aventureiro'}]},
   {id:'chamada',label:'Chamada final',type:'radio',required:true,options:Object.keys(CHAMADA).map(function(k){return {v:k,l:CHAMADA[k]};})},
   {id:'prazo_fotos',label:'Em quantos dias você consegue produzir as fotos que faltam?',type:'number',required:true,min:0,max:90,step:1,unit:'dias'}
  ]},
 {kind:'feedback', title:'Antes e depois',
  metrics:function(s,c){return [{label:'Pontuação atual',value:F.num(c.scoreAtual,0)+'/100',tag:'calculado'},{label:'Pontuação do anúncio revisado',value:F.num(c.scoreNovo,0)+'/100',tag:'calculado'},{label:'Ganho de completude',value:(c.ganho>=0?'+':'')+F.num(c.ganho,0)+' pontos',tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:'info',t:'Título final: <b>'+esc(c.tituloFinal)+'</b>.'});
   if(c.ganho>0) o.push({lv:'ok',t:'O anúncio revisado ganha '+F.num(c.ganho,0)+' pontos de completude. Publique e acompanhe visualizações e consultas nas próximas semanas.'});
   else o.push({lv:'warn',t:'O anúncio revisado não supera o atual em completude. Reveja diferenciais, comodidades e fotos antes de publicar.'});
   if(c.fotosFaltam.length&&s.n('prazo_fotos',0)>30) o.push({lv:'warn',t:'Prazo de '+F.num(s.n('prazo_fotos'))+' dias para as fotos. Enquanto isso, reordene as fotos atuais seguindo o roteiro.'});
   if(c.fotosFaltam.length&&s.n('prazo_fotos',0)===0) o.push({lv:'info',t:'Prazo zero: comece hoje pela foto de capa.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Publicar título e descrição revisados nesta semana'},{id:'a7_2',text:'Produzir as fotos que faltam dentro do prazo definido'},{id:'a7_3',text:'Comparar visualizações e consultas depois de 30 dias'}]}
]}
],

compute:function(s){
 var c={};
 // diagnóstico atual
 var ta=s.t('titulo_atual'); c.tituloLen=ta.length; c.nGenericos=genericos(ta);
 c.nTem=(s.v.anuncio_tem||[]).length;
 var nf=s.has('n_fotos')?s.n('n_fotos',0):null;
 c.ptFotos=nf==null?0:nf>=20?10:nf>=10?5:0;
 c.scoreAtual=c.nTem*10+c.ptFotos+(c.tituloLen>=20&&c.tituloLen<=LIM?5:0)+(c.nGenericos===0?5:0);
 // títulos
 var tipo=s.t('tipo_nome','Hospedagem').trim()||'Hospedagem', loc=s.t('local_ref').trim();
 c.d1=dif(s.t('dif_principal'));
 var extras=DIFS.filter(function(d){return (s.v.difs_extra||[]).indexOf(d.v)>=0&&(!c.d1||d.v!==c.d1.v);});
 c.d2=extras.length?extras[0].c:null;
 c.nDifs=(c.d1?1:0)+extras.length;
 var d1=c.d1?c.d1.c:'boa estrutura';
 function mk(k,comD2,comLoc){var base;
   if(k==='A') base=cap(tipo)+' com '+d1+(comD2&&c.d2?' e '+c.d2:'');
   else if(k==='B') base=(OCAS_T[s.t('ocasiao')]||'Seu refúgio')+' em '+tipo.toLowerCase()+' com '+d1;
   else base=(PUB_T[s.t('publico')]||'Para você')+': '+tipo.toLowerCase()+' com '+d1;
   return base+(comLoc&&loc?' · '+loc:'');}
 c.titulos={A:mk('A',true,true),B:mk('B',true,true),C:mk('C',true,true)};
 c.modelo=s.t('modelo_titulo','A'); c.titulo=c.titulos[c.modelo];
 var t=c.titulo; c.compactado=false;
 if(t.length>LIM){t=mk(c.modelo,false,true);c.compactado=true;}
 if(t.length>LIM){t=mk(c.modelo,false,false);}
 c.tituloFinal=t; c.tituloFinalLen=t.length;
 // fotos
 c.fotosTemK=s.v.fotos_tem||[];
 c.roteiro=FOTOS.map(function(f,i){var l=f.l;
   if(f.k==='capa_dif') l='Capa: '+d1+' em destaque';
   if(f.k==='difs_uso') l=extras.length?'Diferenciais em uso: '+juntar(extras.map(function(d){return d.c;})):'Outros detalhes da experiência em uso';
   if(f.k==='entorno'&&loc) l='Entorno e atrativos: '+loc;
   return {n:i+1,k:f.k,l:l,tem:c.fotosTemK.indexOf(f.k)>=0};});
 c.fotosFaltam=c.roteiro.filter(function(r){return !r.tem;}).map(function(r){return r.l;});
 c.fotosCobertura=(FOTOS.length-c.fotosFaltam.length)/FOTOS.length;
 // descrição
 var prop=esc(s.t('propriedade')), prom=esc(semPonto(s.t('promessa'))), tom=s.t('tom','acolhedor');
 var P=[];
 if(tom==='sofisticado') P.push(prop+'. '+prom+'.');
 else if(tom==='aventureiro') P.push(prom+'. '+prop+' é o seu ponto de partida.');
 else P.push('Que bom ter você por aqui. '+prop+': '+prom.charAt(0).toLowerCase()+prom.slice(1)+'.');
 P.push('Pensada para '+(PUB_D[s.t('publico')]||'você')+(OCAS_D[s.t('ocasiao')]?', '+OCAS_D[s.t('ocasiao')]:'')+'.'+(s.t('desejo')?' Aqui você encontra '+esc(semPonto(s.t('desejo')))+'.':''));
 var bens=(c.d1?[c.d1]:[]).concat(extras).slice(0,5).map(function(d){return d.b;});
 if(bens.length) P.push('O que torna a estadia especial: '+bens.join(' '));
 var capN=s.n('capacidade',1), q=s.n('quartos',0);
 var com=(s.v.comodidades||[]).map(function(k){return COMOD[k];}).filter(Boolean); c.nComod=com.length;
 P.push('O espaço acomoda até '+F.num(capN)+(capN>1?' hóspedes':' hóspede')+(q>0?', com '+F.num(q)+(q>1?' quartos':' quarto'):', em ambiente integrado')+'.'+(com.length?' Comodidades: '+juntar(com)+'.':''));
 var dist=s.has('distancia_km')?s.n('distancia_km'):null;
 var ac={asfalto:'O acesso é todo por via asfaltada.',terra_boa:'O último trecho é de estrada de terra em boas condições.',terra_dificil:'O acesso tem um trecho de terra que pede atenção em dias de chuva; enviamos as orientações antes da chegada.'}[s.t('acesso')]||'';
 P.push('Localização: '+(loc?esc(loc):esc(s.t('destino')))+(dist!=null?', a cerca de '+F.num(dist,dist%1?1:0)+' km do centro':'')+'. '+ac);
 P.push(s.t('checkin')==='presencial'?'Recebemos você pessoalmente na chegada.':'Check-in autônomo, com instruções enviadas antes da chegada.');
 P.push(CHAMADA[s.t('chamada')]||CHAMADA.datas);
 c.descParas=P; c.descChars=P.join('\n\n').replace(/&[a-z#0-9]+;/gi,'x').length;
 // pontuação do anúncio revisado (completude)
 c.ptTitulo=(c.tituloFinalLen<=LIM&&genericos(c.tituloFinal)===0)?20:10;
 c.ptDifs=Math.min(c.nDifs,3)/3*20;
 c.ptFotosNovo=c.fotosCobertura*30;
 c.ptDesc=(capN>0?10:0)+(c.nComod>=3?10:0)+(s.t('promessa')?10:0);
 c.scoreNovo=c.ptTitulo+c.ptDifs+c.ptFotosNovo+c.ptDesc;
 c.ganho=c.scoreNovo-c.scoreAtual;
 return c;
},

metrics:function(s,c){return [
 {label:'Pontuação do anúncio atual',value:F.num(c.scoreAtual,0)+'/100',tag:'calculado'},
 {label:'Pontuação do anúncio revisado',value:F.num(c.scoreNovo,0)+'/100',tag:'calculado'},
 {label:'Título sugerido',value:c.tituloFinal,tag:'recomendacao'},
 {label:'Caracteres do título',value:String(c.tituloFinalLen),tag:'calculado'},
 {label:'Diferenciais no anúncio',value:String(c.nDifs),tag:'informado'},
 {label:'Cobertura do roteiro de fotos',value:F.pct(c.fotosCobertura*100,0),tag:'calculado'},
 {label:'Fotos a produzir',value:String(c.fotosFaltam.length),tag:'calculado'}
];},

priorities:function(s,c){var L=[];
 if(c.fotosTemK.indexOf('capa_dif')<0) L.push({title:'Produzir a foto de capa com '+(c.d1?c.d1.c:'o principal diferencial'),why:'É o primeiro elemento que o hóspede vê na busca.',score:10});
 else L.push({title:'Colocar a foto do principal diferencial como capa',why:'Você já tem a foto; falta usá-la no lugar certo.',score:8});
 L.push({title:'Publicar o novo título: '+c.tituloFinal,why:c.nGenericos>0?'O título atual tem '+c.nGenericos+' adjetivo(s) genérico(s) e nenhum fato.':'Título com diferencial, '+(c.modelo==='A'?'tipo':c.modelo==='B'?'ocasião':'público')+' e localização.',score:c.nGenericos>0||(s.v.anuncio_tem||[]).indexOf('tit_dif')<0?9:7});
 if((s.v.anuncio_tem||[]).indexOf('desc_exp')<0) L.push({title:'Substituir a descrição pela versão montada em blocos',why:'A descrição atual não começa pela experiência.',score:8});
 else L.push({title:'Revisar a descrição com a estrutura em blocos',why:'Garante que benefícios e informações práticas estejam completos.',score:5});
 if(c.fotosCobertura<0.75) L.push({title:'Produzir as '+c.fotosFaltam.length+' fotos que faltam no roteiro',why:'Cobertura de '+F.pct(c.fotosCobertura*100,0)+' dos ambientes e momentos.',score:7});
 L.push({title:'Reordenar as fotos atuais seguindo o roteiro',why:'Custa zero e muda a primeira impressão.',score:6});
 if(c.nDifs<3) L.push({title:'Identificar ou criar mais um diferencial concreto',why:'Só '+c.nDifs+' diferencial(is) marcado(s).',score:6});
 if(c.nComod<3) L.push({title:'Completar a lista de comodidades na plataforma',why:'Hóspedes filtram a busca por comodidades.',score:6});
 if((s.v.anuncio_tem||[]).indexOf('desc_info')<0) L.push({title:'Deixar claros acesso, check-in e regras',why:'Informação ausente gera dúvidas e desistências.',score:6});
 if((s.v.anuncio_tem||[]).indexOf('resp_aval')<0) L.push({title:'Responder as avaliações recentes',why:'Respostas mostram cuidado a quem ainda vai reservar.',score:4});
 if(s.unknown('n_fotos')||s.n('n_fotos',0)<10) L.push({title:'Conferir e ampliar o número de fotos',why:s.unknown('n_fotos')?'Número de fotos desconhecido.':'Só '+F.num(s.n('n_fotos',0))+' fotos.',score:5});
 if(s.t('luz')==='naosei') L.push({title:'Observar a luz em dois horários antes da sessão de fotos',why:'A capa depende do melhor horário de luz.',score:4});
 if(!s.t('desejo')) L.push({title:'Descobrir o desejo principal do público com os próximos hóspedes',why:'A descrição ficou sem essa frase.',score:4});
 if(s.unknown('distancia_km')) L.push({title:'Medir a distância até o centro e incluir na descrição',why:'É uma dúvida frequente dos hóspedes.',score:3});
 return L;},

report:function(s,c){
 var prem=ZA.table(['Elemento','Valor','Origem'],[
  ['Título atual',esc(s.t('titulo_atual'))+' ('+c.tituloLen+' caracteres)',tg('informado')],
  ['Fotos no anúncio atual',s.has('n_fotos')?F.num(s.n('n_fotos')):'—',s.has('n_fotos')?tg('informado'):tg('hipotese','sem dado')],
  ['Público e ocasião',esc((PUB_D[s.t('publico')]||'—')+' · '+(OCAS_T[s.t('ocasiao')]||'—')),tg('informado')],
  ['Posicionamento e estilo',esc(({economico:'Econômico',conforto:'Conforto',experiencia:'Experiência'}[s.t('posic')]||'—')+' · '+({rustico:'rústico',moderno:'moderno',natureza:'imerso na natureza',praia:'praia',historico:'histórico'}[s.t('estilo')]||'—')),tg('informado')],
  ['Principal diferencial',esc(c.d1?c.d1.c:'—'),tg('informado')],
  ['Limite de caracteres do título',String(LIM),tg('estimativa','referência orientativa')],
  ['Textos','montados por modelos com as suas respostas',tg('recomendacao')]],[]);
 var tit='<div class="za-card"><p><b>Título recomendado</b> ('+c.tituloFinalLen+' caracteres):</p><p style="font-size:20px"><b>'+esc(c.tituloFinal)+'</b></p></div>'+
  ZA.table(['Modelo','Título','Caracteres'],['A','B','C'].map(function(k){return [k+(k===c.modelo?' (escolhido)':''),esc(c.titulos[k]),String(c.titulos[k].length)];}),[2]);
 var desc='<div class="za-card">'+c.descParas.map(function(p){return '<p>'+p+'</p>';}).join('')+'</div><p class="za-small">'+F.num(c.descChars)+' caracteres. Texto montado por modelo: revise palavras, confirme que tudo é verdadeiro e ajuste ao seu jeito de falar.</p>';
 var fotos=ZA.table(['Ordem','Foto','Situação'],c.roteiro.map(function(r){return [String(r.n),esc(r.l),r.tem?tg('informado','já tenho'):tg('recomendacao','a produzir')];}),[]);
 var luz={manha:'pela manhã',tarde:'no fim de tarde',naosei:'no horário de melhor luz (observe antes)'}[s.t('luz')]||'';
 var notas=ZA.table(['Critério','Atual','Revisado'],[
  ['Itens do checklist do anúncio (até 80)',F.num(c.nTem*10),'—'],['Fotos (até 10) / roteiro (até 30)',F.num(c.ptFotos),F.num(c.ptFotosNovo,1)],
  ['Título (até 10 / até 20)',F.num(c.scoreAtual-c.nTem*10-c.ptFotos),F.num(c.ptTitulo)],['Diferenciais (até 20)','—',F.num(c.ptDifs,1)],['Descrição (até 30)','—',F.num(c.ptDesc)],
  ['<b>Total</b>','<b>'+F.num(c.scoreAtual,0)+'</b>','<b>'+F.num(c.scoreNovo,0)+'</b>']],[1,2]);
 var top=ZA.op3d(this.priorities(s,c)).l1, pz=s.n('prazo_fotos',0);
 var plan='<div class="za-card"><b>Roteiro de 30 dias</b><ol>'+
  '<li><b>Semana 1:</b> salvar a versão atual do anúncio e anotar visualizações e consultas. '+(top[0]?'Prioridade: '+esc(top[0].title)+'.':'')+'</li>'+
  '<li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Reordenar as fotos seguindo o roteiro')+'; fotografar '+luz+'.</li>'+
  '<li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Completar comodidades e informações práticas')+(c.fotosFaltam.length?' · prazo que você definiu para as fotos: '+F.num(pz)+' dias':'')+'.</li>'+
  '<li><b>Semana 4:</b> comparar visualizações e consultas com a semana 1. Se não houver mudança, testar outro modelo de título.</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Título revisado',html:tit},
  {title:'Descrição revisada',html:desc},
  {title:'Plano visual: roteiro de fotos em ordem',html:fotos+'<p class="za-small">Fotografe capa e área externa '+luz+'. Luz natural, horizonte reto, ambiente arrumado e objetos pessoais fora do quadro.</p>'},
  {title:'Pontuação antes e depois',html:notas+'<p class="za-small">Pontuação de completude pelos critérios da metodologia Zion. Mede clareza e completude, não prevê reservas.</p>'}
 ],plan:plan};
}
});
})();
