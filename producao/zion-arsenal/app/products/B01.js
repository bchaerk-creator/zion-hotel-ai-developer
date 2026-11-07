/* ZAR-B01 · Como Atrair Investimentos para Minha Terra que Está Parada? · Zion Investor Ready */
(function(){
var F=ZA.fmt, esc=ZA.esc;
function tag(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';}
function arr(s,id){var x=s.v[id];return (!s.unknown(id)&&Array.isArray(x))?x:[];}
function has(a,v){return a.indexOf(v)>=0;}
/* escala 1–5 como radio (o tipo scale do motor esconde os inputs) */
function esc5(lo,hi){return [1,2,3,4,5].map(function(k){return {v:String(k),l:k+(k===1?' · '+lo:k===5?' · '+hi:'')};});}
function sc(s,id,def){var x=Number(s.t(id));return (s.t(id)!==''&&isFinite(x))?x:def;}

var DOCS=[
 {v:'matricula',l:'Matrícula atualizada do imóvel (certidão de inteiro teor recente)',who:'Cartório de Registro de Imóveis / advogado'},
 {v:'ccir',l:'CCIR e ITR em dia (rural) ou IPTU em dia (urbano)',who:'Contador / despachante'},
 {v:'car',l:'CAR · Cadastro Ambiental Rural (se for área rural)',who:'Engenheiro ambiental / agrônomo'},
 {v:'topo',l:'Levantamento topográfico ou georreferenciamento',who:'Engenheiro agrimensor'},
 {v:'zoneamento',l:'Consulta à prefeitura sobre uso do solo / zoneamento',who:'Arquiteto ou engenheiro'},
 {v:'onus',l:'Certidão de ônus reais e certidões de ações do proprietário',who:'Advogado'}];
var INFRA=[{v:'energia',l:'Energia elétrica chegando à área'},{v:'agua',l:'Água (poço, nascente outorgável ou rede)'},{v:'internet',l:'Sinal de celular ou internet'},{v:'construcao',l:'Alguma construção aproveitável (casa, galpão)'}];
var CARAC=[{v:'agua',l:'Rio, cachoeira ou nascente'},{v:'mata',l:'Mata nativa ou trilhas'},{v:'vista',l:'Vista panorâmica'},{v:'plano',l:'Área plana para implantar unidades'},{v:'lago',l:'Lago ou represa'}];
var GOV=[{v:'valor_terra',l:'Tenho uma referência de valor da terra feita por avaliador ou corretor'},{v:'saida',l:'Pensei em regras de saída (o que acontece se alguém quiser sair)'},{v:'decisao',l:'Sei como as decisões seriam tomadas entre as partes'},{v:'assessoria',l:'Já conversei com advogado ou contador sobre o formato'}];
var MAT=[{v:'fotos',l:'Fotos de qualidade (e, se possível, imagens aéreas)'},{v:'mapa',l:'Mapa de localização com distâncias e acessos'},{v:'masterplan',l:'Croqui ou estudo preliminar de implantação (masterplan)'},{v:'viabilidade',l:'Estudo preliminar de números (investimento, receita, custos)'},{v:'resumo',l:'Resumo executivo de 1 página'},{v:'pasta',l:'Pasta digital com documentos organizados'}];
var DIMS=[{k:'d1',n:'Documentação e segurança do ativo',w:20,who:'Advogado, cartório, contador'},{k:'d2',n:'Acesso e infraestrutura',w:15,who:'Engenheiro / concessionárias'},{k:'d3',n:'Potencial turístico',w:15,who:'Você (pesquisa de campo e de anúncios)'},{k:'d4',n:'Conceito do projeto',w:10,who:'Você, com apoio de arquiteto'},{k:'d5',n:'Números preliminares',w:15,who:'Você, com cotações e contador'},{k:'d6',n:'Modelo de parceria e governança',w:10,who:'Advogado e contador'},{k:'d7',n:'Material de apresentação',w:15,who:'Você'}];

function nivel(i){return i>=75?'Pronto para conversas preliminares':i>=50?'Em estruturação':i>=25?'Em fase inicial':'Ativo ainda não estruturado';}

ZA.register({
id:'B01', code:'ZAR-B01', collection:'Terrenos',
title:'Como Atrair Investimentos para Minha Terra que Está Parada?',
subtitle:'Preparar uma Oportunidade Turística para Investidores',
tool:'Zion Investor Ready',
deliverable:'Dossiê Preliminar de Oportunidade Turística para Investidores',
nameField:'nome', propertyField:'propriedade',
disclaimer:'O Zion Investor Ready mede a organização das informações do seu ativo; ele não avalia o imóvel, não garante captação de investimento, aprovação de licenças nem retorno. Números são estimativas preliminares feitas com os seus dados. Temas de documentação, ambientais, jurídicos e societários devem ser conduzidos com advogado, contador, engenheiro ou arquiteto habilitados.',

intro:[
 {kind:'mirror', title:'Você tem a terra. Mas sabe o que um investidor precisa enxergar antes de colocar dinheiro nela?',
  lead:'Você já imaginou cabanas ali, já mostrou fotos para conhecidos, talvez alguém tenha dito “isso daria um ótimo negócio”. Mas a conversa nunca passou disso.',
  body:'<div class="za-card"><p>Se você se reconhece em alguma destas situações, esta mini mentoria é para você:</p><ul><li>“Tenho uma área linda parada há anos e não sei por onde começar.”</li><li>“Já mostrei para uma pessoa com dinheiro, ela gostou, mas pediu ‘um projeto’ e eu não tinha.”</li><li>“Não sei se minha documentação está em condições de alguém entrar como sócio.”</li><li>“Não sei quanto custaria, quanto renderia nem o que eu ofereceria em troca.”</li></ul></div>'},
 {kind:'collapse', title:'Ter um terreno bonito não significa possuir uma oportunidade de investimento estruturada.',
  lead:'Investidor não compra paisagem: ele avalia risco, clareza e números. Uma área sem documentação organizada, sem conceito e sem contas preliminares é, para ele, uma incerteza.',
  body:'<div class="za-card"><p>Antes de colocar dinheiro, um investidor costuma fazer quatro perguntas:</p><ol><li><b>O ativo é seguro?</b> Documentação, situação legal, restrições.</li><li><b>Existe demanda?</b> Atrativos, acesso, público, mercado.</li><li><b>Qual é o projeto?</b> Conceito, modelo, quantidade de unidades.</li><li><b>Como entra e como sai?</b> Números preliminares e modelo de parceria.</li></ol><p>O Zion Investor Ready transforma essas perguntas em um <b>índice de prontidão por dimensão</b> e numa lista de <b>lacunas a resolver</b>. Ele não diz que você vai captar: mostra o que falta para uma conversa séria.</p></div>'},
 {kind:'start', title:'Vamos medir a prontidão da sua terra para investidores',
  lead:'Em 7 pilares você vai organizar o ativo, o potencial, o conceito, as contas, o modelo de parceria e o material de apresentação.',
  body:'<p>Tenha por perto, se possível: matrícula do imóvel, comprovantes de ITR/CCIR ou IPTU, fotos da área e qualquer orçamento que já tenha recebido. Se não souber algum dado, marque “não sei”: ele vira uma lacuna no seu dossiê.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Maria'},
   {id:'propriedade',label:'Nome da terra ou do projeto',type:'text',required:true,placeholder:'Ex.: Sítio Água Clara'},
   {id:'cidade',label:'Município e estado',type:'text',required:true,placeholder:'Ex.: Alto Paraíso (GO)'},
   {id:'area_ha',label:'Área total do terreno',type:'number',required:true,min:0.1,max:100000,step:'any',unit:'hectares',help:'1 hectare = 10.000 m². Use o valor da matrícula, se tiver.'},
   {id:'objetivo',label:'O que você busca hoje?',type:'radio',required:true,options:[{v:'socio_capital',l:'Encontrar um investidor ou sócio com capital'},{v:'desenvolver_junto',l:'Desenvolver junto com um parceiro que também opere'},{v:'arrendar',l:'Ceder o uso da área para um operador'},{v:'entender',l:'Entender se a terra tem condições de atrair alguém'}]}
  ]}
],

pillars:[
/* 1 */
{title:'Conheça seu ativo', screens:[
 {kind:'learn', title:'O primeiro filtro do investidor é a segurança do ativo',
  body:'<p>Antes de olhar a paisagem, quem investe quer saber se a terra pode receber um projeto sem surpresas: <b>de quem ela é</b>, <b>se há ônus ou disputas</b>, <b>o que a lei permite construir ali</b> e <b>se dá para chegar e operar</b> (acesso, energia, água).</p><p>Documentação incompleta não impede uma conversa, mas aumenta o risco percebido. E risco percebido maior costuma significar uma proposta pior para você, ou nenhuma proposta.</p><p>Neste pilar, você faz um inventário honesto. Ele não substitui a análise de um advogado ou de um engenheiro; serve para saber <b>o que levar até eles</b>.</p>',
  example:'Exemplo: duas áreas parecidas. A primeira tem matrícula atualizada, CAR e consulta de uso do solo. A segunda é posse de família ainda em inventário. Para o investidor, a primeira é um projeto; a segunda é, antes de tudo, um problema jurídico a resolver.'},
 {kind:'compare', title:'Como o investidor enxerga a sua documentação',
  cols:[{h:'Gera desconfiança',type:'bad',items:['“A escritura está com meu tio, mas a terra é nossa.”','Inventário não concluído ou herdeiros sem acordo','Não saber se há área de preservação no ponto onde se quer construir','ITR ou IPTU atrasados há anos','Estrada que fecha na época de chuva']},
        {h:'Gera confiança',type:'good',items:['Matrícula recente, em nome de quem vai negociar','Certidões negativas organizadas numa pasta','Consulta prévia à prefeitura sobre o que é permitido','Topografia que mostra onde é possível implantar','Acesso e energia descritos com clareza']}]},
 {kind:'form', title:'Inventário do ativo', intro:'Marque apenas o que você <b>tem em mãos hoje</b>. O que faltar vira lacuna no seu dossiê.',
  fields:[
   {id:'doc_status',label:'Situação da propriedade, pelo que você sabe',type:'radio',required:true,allowUnknown:true,options:[{v:'regular',l:'Matrícula em meu nome (ou da empresa/família que negocia), sem pendência conhecida'},{v:'parcial',l:'Há algo a resolver (inventário, escritura sem registro, divisão entre herdeiros)'},{v:'irregular',l:'Só tenho posse ou contrato particular, sem registro'}],help:'Esta pergunta não é um parecer: só registra o que você sabe. Quem confirma a situação é um advogado ou o cartório.'},
   {id:'doc_checks',label:'Documentos que você já tem',type:'checks',options:DOCS.map(function(d){return {v:d.v,l:d.l};})},
   {id:'acesso',label:'Como é o acesso até a área?',type:'radio',required:true,options:[{v:'asfalto',l:'Asfalto até a entrada'},{v:'terra_boa',l:'Estrada de terra boa o ano todo'},{v:'terra_ruim',l:'Estrada de terra difícil na chuva'},{v:'sem',l:'Sem acesso para carro comum'}]},
   {id:'infra',label:'Infraestrutura existente',type:'checks',options:INFRA}
  ]},
 {kind:'feedback', title:'O que o seu inventário revela',
  metrics:function(s,c){return [{label:'Documentação',value:F.num(c.d1,0)+'/100',tag:'calculado'},{label:'Acesso e infraestrutura',value:F.num(c.d2,0)+'/100',tag:'calculado'},{label:'Documentos em mãos',value:c.nDocs+' de 6',tag:'informado'}];},
  feedback:function(s,c){var o=[];var st=s.t('doc_status');
   if(s.unknown('doc_status')) o.push({lv:'bad',t:'Você não sabe a situação da propriedade. Esse é o primeiro ponto a esclarecer: peça uma certidão de inteiro teor da matrícula no cartório e leve a um advogado.'});
   else if(st==='irregular') o.push({lv:'bad',t:'Sem registro em seu nome, um investidor dificilmente formaliza qualquer acordo. A regularização é a primeira etapa, e o caminho certo só um advogado pode indicar.'});
   else if(st==='parcial') o.push({lv:'warn',t:'Há uma pendência na propriedade. Muitos projetos começam assim, mas o investidor vai querer saber <b>quanto tempo</b> e <b>quanto custa</b> resolver. Busque essa resposta com um advogado.'});
   else o.push({lv:'ok',t:'Propriedade sem pendência conhecida. Mantenha a matrícula atualizada (certidões recentes) para mostrar quando for pedido.'});
   if(c.nDocs<=2) o.push({lv:'warn',t:'Você tem '+c.nDocs+' dos 6 documentos de base. Faltam: '+c.docsFalta.map(function(d){return d.l.split(' (')[0];}).join('; ')+'.'});
   else o.push({lv:c.nDocs===6?'ok':'info',t:'Você tem '+c.nDocs+' dos 6 documentos de base.'+(c.nDocs<6?' Para completar: '+c.docsFalta.map(function(d){return d.l.split(' (')[0];}).join('; ')+'.':'')});
   if(s.t('acesso')==='terra_ruim'||s.t('acesso')==='sem') o.push({lv:'warn',t:'O acesso é um ponto fraco. Investidor e hóspede precisam chegar o ano todo. Levante quanto custaria melhorar a estrada ou se há plano público para isso.'});
   if(c.nInfra<2) o.push({lv:'warn',t:'Pouca infraestrutura no local: energia e água costumam estar entre os primeiros custos de implantação. Peça orientação às concessionárias e a um engenheiro.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Pedir a certidão de inteiro teor atualizada da matrícula no cartório'},{id:'a1_2',text:'Agendar uma conversa com advogado para entender a situação documental'},{id:'a1_3',text:'Montar uma pasta digital com todos os documentos do imóvel'}]}
]},
/* 2 */
{title:'Descubra o potencial', screens:[
 {kind:'learn', title:'Potencial turístico é a soma de atrativo, demanda e público',
  body:'<p>Uma cachoeira bonita é um atrativo. Mas o investidor quer saber se <b>pessoas já viajam para aquela região</b>, <b>quem são elas</b> e <b>o que a sua área oferece que as outras não oferecem</b>.</p><p>Três perguntas organizam o potencial:</p><ul><li><b>Atrativo:</b> o que há na sua terra que faz alguém querer passar a noite ali?</li><li><b>Demanda:</b> a região já recebe turistas? Há hospedagens com calendário ocupado?</li><li><b>Público:</b> para quem esse lugar é ideal (casais, famílias, quem busca descanso, aventura)?</li></ul><p>Uma forma simples de checar demanda, sem estatísticas externas: abra os anúncios de 5 hospedagens da região nas plataformas e veja os calendários dos próximos fins de semana.</p>',
  example:'Exemplo: uma área a 20 km de um destino que já lota nos feriados tem demanda comprovável. Outra, a 150 km de qualquer fluxo turístico, pode ter um atrativo incrível, mas precisa criar a própria demanda, o que é mais arriscado para quem investe.'},
 {kind:'compare', title:'Potencial descrito × potencial demonstrado',
  cols:[{h:'Descrito (fraco para investidor)',type:'bad',items:['“A vista é maravilhosa.”','“Todo mundo que vem aqui adora.”','“Turismo na região só cresce.” (sem fonte)','“Serve para qualquer público.”']},
        {h:'Demonstrado (forte)',type:'good',items:['Fotos e um mapa com os atrativos e distâncias','Lista de hospedagens próximas com diária e calendário observados','Público definido e o motivo de ele escolher sua área','Diferencial que concorrentes próximos não têm']}]},
 {kind:'form', title:'O potencial da sua área',
  fields:[
   {id:'atrativos',label:'Força dos atrativos dentro da sua área (1 a 5)',type:'radio',required:true,options:esc5('nenhum atrativo marcante','atrativo raro e muito forte')},
   {id:'caracteristicas',label:'Características presentes no terreno',type:'checks',options:CARAC},
   {id:'demanda',label:'Situação turística da região',type:'radio',required:true,allowUnknown:true,options:[{v:'consolidado',l:'Destino consolidado: já há muitas hospedagens e fluxo nos fins de semana'},{v:'emergente',l:'Destino emergente: há algum fluxo e poucas hospedagens'},{v:'sem_fluxo',l:'Sem fluxo turístico relevante hoje'}]},
   {id:'dist_cidade',label:'Distância até a cidade de apoio mais próxima (mercado, posto, saúde)',type:'number',required:true,allowUnknown:true,min:0,max:500,step:'any',unit:'km'},
   {id:'publico',label:'Público que você imagina como principal',type:'select',required:true,options:[{v:'casais',l:'Casais'},{v:'familias',l:'Famílias'},{v:'bemestar',l:'Quem busca descanso e bem-estar'},{v:'aventura',l:'Aventura e esportes na natureza'},{v:'grupos',l:'Grupos, retiros e eventos'},{v:'indefinido',l:'Ainda não sei'}]}
  ]},
 {kind:'feedback', title:'Leitura preliminar do potencial',
  metrics:function(s,c){return [{label:'Potencial turístico',value:F.num(c.d3,0)+'/100',tag:'calculado'},{label:'Características marcadas',value:String(c.nCar),tag:'informado'}];},
  feedback:function(s,c){var o=[];var d=s.t('demanda');
   if(s.unknown('demanda')) o.push({lv:'warn',t:'Você não sabe como está o turismo na região. Faça a pesquisa de 5 anúncios próximos (diária, avaliações, calendário). Sem isso, o potencial é só hipótese.'});
   else if(d==='consolidado') o.push({lv:'ok',t:'Destino consolidado: a demanda é mais fácil de demonstrar. Em compensação, a concorrência é maior, então o diferencial precisa ser claro.'});
   else if(d==='emergente') o.push({lv:'info',t:'Destino emergente: pode haver espaço para chegar antes, mas o investidor vai pedir sinais concretos de demanda. Registre o que observar nos calendários dos concorrentes.'});
   else o.push({lv:'warn',t:'Sem fluxo turístico, o projeto precisa criar a própria demanda (eventos, retiros, público de cidades próximas). Isso aumenta o risco percebido.'});
   if(sc(s,'atrativos',0)<=2) o.push({lv:'warn',t:'Você avaliou os atrativos como fracos. Nesse caso, o conceito (Pilar 3) precisa carregar o motivo da viagem: experiência, conforto, gastronomia.'});
   if(sc(s,'atrativos',0)>=4&&c.nCar>=3) o.push({lv:'ok',t:'Atrativos fortes e '+c.nCar+' características naturais: material excelente para fotos e para o mapa da oportunidade.'});
   var dc=s.n('dist_cidade'); if(dc!=null&&dc>40) o.push({lv:'info',t:'A cidade de apoio fica a '+F.num(dc,0)+' km. Isso pesa na operação (compras, manutenção, equipe). Leve isso para as contas do Pilar 4.'});
   if(s.t('publico')==='indefinido') o.push({lv:'warn',t:'Público ainda indefinido. No Pilar 3 você vai escolher um público principal: projeto “para todos” não convence investidor.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Pesquisar 5 hospedagens da região: diária, avaliações e calendário dos próximos fins de semana'},{id:'a2_2',text:'Fotografar os atrativos e marcar no mapa as distâncias até eles'},{id:'a2_3',text:'Escrever em uma frase por que o público escolhido viajaria até a sua área'}]}
]},
/* 3 */
{title:'Estruture o conceito', screens:[
 {kind:'learn', title:'Conceito é a resposta para “o que, exatamente, vai existir aqui?”',
  body:'<p>Investidor não investe em “um projeto de turismo”. Investe em algo concreto: <b>quantas unidades</b>, <b>de que tipo</b>, <b>para qual público</b>, <b>com qual diferencial</b>. Essa é a função do conceito.</p><p>Um conceito bom cabe em uma frase e cumpre três papéis: orienta o arquiteto, orienta as contas e orienta a apresentação.</p><div class="za-card"><b>Modelo de frase:</b> “[Tipo de hospedagem] para [público] que buscam [desejo principal], com [diferencial que só a sua área tem].”</div>',
  example:'Exemplo: “Quatro cabanas para casais que buscam silêncio e banho de cachoeira, a 15 minutos de um destino de ecoturismo conhecido.” Com essa frase, já dá para pedir um orçamento, estimar uma diária e montar uma apresentação.'},
 {kind:'compare', title:'Conceito vago × conceito estruturado',
  cols:[{h:'Vago',type:'bad',items:['“Um espaço de turismo e lazer.”','“Pode ser pousada, camping, eventos...”','Número de unidades indefinido','Diferencial igual ao de todos (“contato com a natureza”)']},
        {h:'Estruturado',type:'good',items:['Tipo de hospedagem escolhido','Quantidade de unidades na primeira etapa','Público principal definido','Diferencial concreto e verificável']}]},
 {kind:'form', title:'O conceito do seu projeto',
  fields:[
   {id:'modelo',label:'Tipo de hospedagem que você imagina',type:'radio',required:true,options:[{v:'cabanas',l:'Cabanas'},{v:'glamping',l:'Glamping (tendas, domos)'},{v:'chales',l:'Chalés'},{v:'pousada',l:'Pequena pousada'},{v:'misto',l:'Misto (mais de um tipo)'},{v:'indefinido',l:'Ainda não sei'}]},
   {id:'unidades',label:'Quantas unidades na primeira etapa?',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)',help:'Pense no começo do projeto, não na visão final.'},
   {id:'conceito',label:'Frase do conceito',type:'textarea',required:false,placeholder:'Ex.: Quatro cabanas para casais que buscam silêncio e banho de cachoeira…',help:'Use o modelo da tela anterior. Pelo menos uma frase completa.'},
   {id:'diferencial',label:'Seu principal diferencial',type:'text',required:false,placeholder:'Ex.: Cachoeira dentro da propriedade'}
  ]},
 {kind:'feedback', title:'Seu conceito, do ponto de vista do investidor',
  metrics:function(s,c){return [{label:'Conceito do projeto',value:F.num(c.d4,0)+'/100',tag:'calculado'},{label:'Unidades na 1ª etapa',value:F.num(s.n('unidades')),tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(s.t('modelo')==='indefinido') o.push({lv:'warn',t:'Tipo de hospedagem indefinido. Sem ele não há orçamento nem estimativa de receita. Se tiver dúvida entre modelos, compare custo, operação e adequação ao terreno antes de apresentar.'});
   if(c.concLen<30) o.push({lv:'warn',t:'A frase do conceito está ausente ou curta demais. Escreva uma frase completa com tipo, público, desejo e diferencial.'});
   else o.push({lv:'ok',t:'Seu conceito: “'+esc(s.t('conceito'))+'”. Leia em voz alta: se alguém de fora entende o que vai existir ali, a frase cumpre o papel.'});
   if(c.difLen<5) o.push({lv:'warn',t:'Diferencial não informado. Pergunte-se: o que existe na sua área que os concorrentes próximos não têm?'});
   if(s.t('publico')==='indefinido') o.push({lv:'warn',t:'Você ainda não definiu o público no Pilar 2. Conceito e público precisam conversar.'});
   var u=s.n('unidades',0); if(u>20) o.push({lv:'info',t:'Você prevê '+F.num(u)+' unidades já na primeira etapa. Projetos grandes exigem mais capital e mais licenças; uma primeira etapa menor costuma ser mais fácil de explicar e de validar.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Reescrever a frase do conceito até que uma pessoa de fora entenda o projeto'},{id:'a3_2',text:'Definir a quantidade de unidades da primeira etapa'},{id:'a3_3',text:'Conversar com um arquiteto sobre a implantação preliminar no terreno'}]}
]},
/* 4 */
{title:'Faça as contas', screens:[
 {kind:'learn', title:'Números preliminares: quanto custa, quanto pode gerar e quanto falta',
  body:'<p>Ninguém espera um estudo definitivo na primeira conversa. Mas o investidor espera que você saiba responder, ao menos de forma preliminar:</p><ul><li><b>Quanto custa implantar</b> a primeira etapa (e de onde veio esse número)?</li><li><b>Quanto pode gerar por ano</b>: unidades × 365 noites × ocupação × diária.</li><li><b>Quanto sobra</b> depois dos custos operacionais.</li><li><b>Quanto falta</b> de capital além do que você mesmo pode colocar.</li></ul><p>A ferramenta faz essas contas com os <b>seus</b> números. Ocupação, diária e custos devem vir da sua pesquisa (concorrentes, orçamentos), nunca de uma promessa. O resultado é uma estimativa, não uma previsão.</p>',
  example:'Exemplo ilustrativo: 4 cabanas × 365 noites × 40% de ocupação × R$ 450 = R$ 262.800 de receita bruta por ano. Se os custos operacionais forem 45% da receita, o resultado operacional estimado é R$ 144.540, antes de impostos sobre o lucro, financiamento e depreciação.'},
 {kind:'compare', title:'Números que afastam × números que aproximam',
  cols:[{h:'Afastam',type:'bad',items:['Ocupação de 80% o ano inteiro sem nenhuma referência','Investimento “de cabeça”, sem cotação','Ignorar custos de operação (limpeza, equipe, manutenção, comissões)','Prometer retorno em X meses']},
        {h:'Aproximam',type:'good',items:['Ocupação baseada no que você observou nos concorrentes','Cotações ou orçamentos, mesmo que preliminares','Custos operacionais estimados e explicados','Cenários (conservador, intermediário, otimista) em vez de promessa']}]},
 {kind:'form', title:'Seus números preliminares', intro:'Se não tiver algum número, marque “não sei”: ele vira lacuna, e o dossiê não inventa valores por você.',
  fields:[
   {id:'investimento',label:'Investimento estimado da primeira etapa',type:'money',required:true,allowUnknown:true,help:'Construção, infraestrutura, mobiliário, projetos e licenças.'},
   {id:'orc_origem',label:'De onde vem esse valor?',type:'radio',required:true,options:[{v:'cotacoes',l:'Cotações ou orçamentos de fornecedores'},{v:'estimativa',l:'Estimativa própria ou pesquisa de preços'},{v:'nenhum',l:'Ainda não tenho estimativa'}]},
   {id:'diaria',label:'Diária média que você considera realista',type:'money',required:true,allowUnknown:true,help:'Baseie-se em hospedagens parecidas na região.'},
   {id:'ocupacao',label:'Ocupação média anual que você considera realista',type:'percent',required:true,allowUnknown:true,max:100,help:'Planeje com prudência: média do ano, não da alta temporada.'},
   {id:'custo_op',label:'Custos operacionais como % da receita',type:'percent',required:true,allowUnknown:true,max:95,help:'Limpeza, equipe, energia, manutenção, comissões e impostos sobre a receita. Se tiver uma estimativa em reais, divida pela receita prevista.'},
   {id:'recursos',label:'Quanto você mesmo pode investir',type:'money',required:true,help:'Pode ser zero. É o que você colocaria além da terra.'}
  ]},
 {kind:'feedback', title:'O que as contas mostram',
  metrics:function(s,c){return [{label:'Receita bruta anual estimada',value:F.brl0(c.rec),tag:'estimativa'},{label:'Resultado operacional anual',value:F.brl0(c.res),tag:'estimativa'},{label:'Payback simples',value:c.payback==null?'—':F.num(c.payback,1)+' anos',tag:'estimativa'},{label:'Capital a buscar',value:F.brl0(c.gap),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.rec==null) o.push({lv:'warn',t:'Sem diária ou ocupação, não é possível estimar a receita. Pesquise ao menos 5 concorrentes para ter uma referência.'});
   if(c.res==null&&c.rec!=null) o.push({lv:'warn',t:'Sem a estimativa de custos operacionais, a receita aparece sozinha, e receita não é resultado. Monte uma lista de custos mensais esperados.'});
   if(s.unknown('investimento')||s.t('orc_origem')==='nenhum') o.push({lv:'bad',t:'Ainda não há estimativa de investimento. Peça orçamentos preliminares (unidade, infraestrutura, projetos): é a pergunta número um de quem investe.'});
   else if(s.t('orc_origem')==='estimativa') o.push({lv:'info',t:'Seu investimento é uma estimativa própria. Para o dossiê ganhar força, substitua por cotações, mesmo que preliminares.'});
   else o.push({lv:'ok',t:'Investimento baseado em cotações: isso dá credibilidade aos números.'});
   if(c.payback!=null&&c.payback<3) o.push({lv:'warn',t:'O payback simples estimado ficou em '+F.num(c.payback,1)+' anos. Resultado muito rápido costuma indicar premissas otimistas: revise ocupação, diária e custos antes de mostrar a alguém, e lembre que o cálculo não inclui período de obra, rampa de ocupação nem impostos sobre o lucro.'});
   if(c.payback!=null&&c.payback>12) o.push({lv:'warn',t:'Payback simples acima de 12 anos. Investidores tendem a pedir um projeto mais enxuto ou outro modelo de parceria.'});
   if(c.res!=null&&c.res<=0) o.push({lv:'bad',t:'Com essas premissas, a operação não gera resultado positivo. Revise o conceito ou os custos antes de buscar investidores.'});
   if(c.gap!=null) o.push({lv:'info',t:'Diferença entre o investimento e o que você pode colocar: '+F.brl0(c.gap)+'. É esse o valor que precisaria vir de parceiro, investidor ou de outras alternativas.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Pedir ao menos 2 orçamentos preliminares para a unidade de hospedagem'},{id:'a4_2',text:'Listar os custos mensais esperados da operação'},{id:'a4_3',text:'Montar os números em três cenários antes de apresentar'}]}
]},
/* 5 */
{title:'Escolha o modelo de parceria', screens:[
 {kind:'learn', title:'O investidor quer saber como entra, o que recebe e como sai',
  body:'<p>Existem várias formas de alguém participar de um projeto na sua terra. As mais comuns, de forma simplificada:</p><ul><li><b>Sociedade no projeto:</b> as partes criam ou usam uma empresa para o empreendimento; você pode entrar com a terra (ou o direito de uso) e o investidor com capital.</li><li><b>Arrendamento ou cessão de uso:</b> um operador usa a área por um prazo e paga por isso; você não opera.</li><li><b>Permuta:</b> você cede parte da área (ou dos direitos) em troca de construção ou de unidades prontas.</li><li><b>Aporte com participação nos resultados:</b> o investidor coloca capital e recebe uma parte do resultado por um período.</li></ul><p>Cada formato tem efeitos jurídicos, tributários e sucessórios diferentes. Aqui você escolhe a <b>direção</b>; o desenho do contrato é trabalho de advogado e contador.</p>',
  example:'Exemplo: um proprietário quer manter a terra na família e não quer operar. Arrendamento ou cessão de uso por prazo pode fazer mais sentido que sociedade. Outro quer participar da gestão e do crescimento: sociedade no projeto tende a ser mais coerente.'},
 {kind:'compare', title:'Proposta confusa × proposta clara',
  cols:[{h:'Confusa',type:'bad',items:['“Entra com o dinheiro e a gente vê depois como divide.”','Não dizer quem toma as decisões','Nenhuma regra para saída de uma das partes','Misturar a terra pessoal com o negócio sem orientação']},
        {h:'Clara',type:'good',items:['Formato de parceria escolhido como ponto de partida','Papel de cada parte definido (terra, capital, gestão)','Regras de decisão e de saída pensadas','Desenho validado com advogado e contador antes de assinar']}]},
 {kind:'form', title:'A direção da sua parceria',
  fields:[
   {id:'parceria',label:'Formato que você considera como ponto de partida',type:'radio',required:true,options:[{v:'sociedade',l:'Sociedade no projeto'},{v:'arrendamento',l:'Arrendamento ou cessão de uso'},{v:'permuta',l:'Permuta (área por construção ou unidades)'},{v:'aporte',l:'Aporte com participação nos resultados'},{v:'indefinido',l:'Ainda não sei'}]},
   {id:'papel',label:'O que você coloca no projeto',type:'radio',required:true,options:[{v:'terra',l:'Só a terra (ou o direito de uso)'},{v:'terra_gestao',l:'A terra e o meu trabalho na gestão'},{v:'terra_capital',l:'A terra e também algum capital'}]},
   {id:'governanca',label:'O que você já pensou ou fez',type:'checks',options:GOV}
  ]},
 {kind:'feedback', title:'Sua proposta de parceria',
  metrics:function(s,c){return [{label:'Modelo de parceria e governança',value:F.num(c.d6,0)+'/100',tag:'calculado'},{label:'Itens de governança',value:c.nGov+' de 4',tag:'informado'}];},
  feedback:function(s,c){var o=[];var p=s.t('parceria');
   if(p==='indefinido') o.push({lv:'warn',t:'Formato de parceria indefinido. Você não precisa ter a resposta final, mas deve chegar à conversa com uma proposta inicial.'});
   if(p==='arrendamento'&&s.t('papel')==='terra_gestao') o.push({lv:'warn',t:'No arrendamento quem opera é o arrendatário, mas você quer participar da gestão. Vale reavaliar: sociedade ou aporte com participação podem ser mais coerentes.'});
   if(p==='sociedade'&&s.t('objetivo')==='arrendar') o.push({lv:'info',t:'No início você disse que queria ceder o uso, e agora escolheu sociedade. Ambas são possíveis; só esteja seguro de que quer participar do risco do negócio.'});
   if(!has(c.gov,'valor_terra')) o.push({lv:'warn',t:'Sem uma referência de valor da terra, fica difícil discutir participação. Um avaliador ou corretor da região pode dar essa referência.'});
   if(!has(c.gov,'assessoria')) o.push({lv:'warn',t:'Antes de assinar qualquer documento, inclusive “cartas de intenção”, converse com um advogado e um contador sobre o formato.'});
   if(c.nGov===4) o.push({lv:'ok',t:'Você já pensou em valor da terra, decisões, saída e assessoria. Isso é raro e transmite seriedade.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Obter uma referência de valor da terra com avaliador ou corretor da região'},{id:'a5_2',text:'Escrever em uma página o que cada parte coloca e o que cada parte recebe'},{id:'a5_3',text:'Levar o formato escolhido para análise de advogado e contador'}]}
]},
/* 6 */
{title:'Prepare a oportunidade', screens:[
 {kind:'learn', title:'Oportunidade preparada é aquela que pode ser analisada sem você na sala',
  body:'<p>Um investidor interessado vai mostrar o projeto a alguém de confiança: um sócio, um contador, um familiar. O material precisa se explicar sozinho.</p><p>O conjunto mínimo de uma oportunidade preparada:</p><ol><li><b>Fotos</b> que mostram a área real (e imagens aéreas, se possível).</li><li><b>Mapa</b> com localização, acessos e distâncias.</li><li><b>Croqui de implantação</b>: onde ficariam as unidades.</li><li><b>Números preliminares</b> em cenários.</li><li><b>Resumo executivo</b> de 1 página.</li><li><b>Pasta de documentos</b> organizada.</li></ol>',
  example:'Exemplo: em vez de mandar 40 fotos por mensagem, você envia um resumo de 1 página com a frase do conceito, um mapa, 6 fotos escolhidas, o investimento estimado, os três cenários e o formato de parceria proposto. A conversa muda de nível.'},
 {kind:'compare', title:'Material improvisado × material preparado',
  cols:[{h:'Improvisado',type:'bad',items:['Fotos soltas no celular','Localização por “fica perto de…”','Números ditos em áudio','Documentos espalhados entre parentes']},
        {h:'Preparado',type:'good',items:['Seleção de fotos com legenda','Mapa com distâncias e acessos','Planilha ou resumo com premissas','Pasta digital com documentos e certidões']}]},
 {kind:'form', title:'Seu material de apresentação',
  fields:[
   {id:'materiais',label:'O que já está pronto',type:'checks',options:MAT},
   {id:'horas_semana',label:'Quantas horas por semana você pode dedicar a preparar a oportunidade?',type:'number',required:true,min:0,max:80,step:1,unit:'horas'}
  ]},
 {kind:'feedback', title:'Seu material, item por item',
  metrics:function(s,c){return [{label:'Materiais prontos',value:c.nMat+' de 6',tag:'informado'},{label:'Horas por semana',value:F.num(s.n('horas_semana')),tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(c.nMat===0) o.push({lv:'bad',t:'Nenhum material pronto ainda. Comece pelo resumo de 1 página: ele organiza todo o resto.'});
   else if(c.nMat<4) o.push({lv:'warn',t:'Você tem '+c.nMat+' de 6 materiais. Faltam: '+c.matFalta.map(function(m){return m.l.split(' (')[0];}).join('; ')+'.'});
   else o.push({lv:c.nMat===6?'ok':'info',t:'Você tem '+c.nMat+' de 6 materiais.'+(c.nMat<6?' Falta: '+c.matFalta.map(function(m){return m.l.split(' (')[0];}).join('; ')+'.':' Material completo para uma primeira análise.')});
   if(!has(c.mat,'viabilidade')&&c.rec!=null) o.push({lv:'info',t:'Você já tem números no Pilar 4: o relatório final desta mini mentoria pode servir de base para o seu estudo preliminar.'});
   var h=s.n('horas_semana',0); if(h<3) o.push({lv:'warn',t:'Com menos de 3 horas por semana, a preparação tende a se arrastar. Defina um horário fixo semanal para este projeto.'});
   else if(c.lac.length>0) o.push({lv:'info',t:'Com '+F.num(h)+' horas por semana e '+c.lac.length+' lacunas mapeadas, organize as lacunas em um roteiro semanal: o relatório final traz a ordem sugerida.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Escrever o resumo executivo de 1 página'},{id:'a6_2',text:'Selecionar 6 a 10 fotos com legenda e montar o mapa de localização'},{id:'a6_3',text:'Reservar um horário fixo por semana para preparar a oportunidade'}]}
]},
/* 7 */
{title:'Apresente ao mercado', screens:[
 {kind:'learn', title:'Apresentar é pedir algo claro para a pessoa certa',
  body:'<p>Antes de procurar alguém, você precisa conseguir dizer em uma frase: <b>quanto precisa</b>, <b>para quê</b> e <b>o que oferece em troca</b>. Sem isso, a conversa vira elogio à paisagem.</p><p>Depois, pense em <b>quem</b> procurar. Perfis diferentes avaliam coisas diferentes:</p><ul><li><b>Empresário local:</b> conhece a região, valoriza proximidade e confiança.</li><li><b>Quem já atua em turismo e hospedagem:</b> avalia operação, demanda e números com mais rigor.</li><li><b>Conhecidos e família:</b> conversa mais fácil, mas o risco de conflito pessoal é maior; formalize igual.</li></ul><p>Importante: oferecer participação em projeto para muitas pessoas, de forma pública, pode estar sujeito a regras específicas. Converse com um advogado antes de divulgar amplamente.</p>',
  example:'Exemplo de frase: “Busco um parceiro para implantar 4 cabanas na primeira etapa, com investimento estimado de R$ 600 mil. Entro com a área e a gestão; proponho sociedade no projeto, com participação a definir com base na avaliação da terra.”'},
 {kind:'compare', title:'Abordagem que queima × abordagem que abre portas',
  cols:[{h:'Queima a oportunidade',type:'bad',items:['Mandar a mesma mensagem para dezenas de pessoas','Apresentar sem números nem documentos','Pressionar por uma decisão rápida','Prometer rentabilidade']},
        {h:'Abre portas',type:'good',items:['Lista curta de perfis certos','Pedido claro em uma frase','Material que se explica sozinho','Convite para visitar a área, sem promessa de retorno']}]},
 {kind:'form', title:'Sua estratégia de apresentação',
  fields:[
   {id:'clareza',label:'Você consegue dizer, em uma frase, quanto precisa, para quê e o que oferece em troca?',type:'radio',required:true,options:[{v:'sim',l:'Sim'},{v:'parcial',l:'Em parte'},{v:'nao',l:'Ainda não'}]},
   {id:'perfil_inv',label:'Perfil de parceiro que você pretende procurar primeiro',type:'radio',required:true,options:[{v:'local',l:'Empresário ou investidor da região'},{v:'turismo',l:'Quem já atua em turismo e hospedagem'},{v:'conhecidos',l:'Conhecidos e família'},{v:'nao_sei',l:'Ainda não sei'}]},
   {id:'canais',label:'Como pretende chegar até essas pessoas',type:'checks',options:[{v:'indicacao',l:'Indicação de contatos de confiança'},{v:'associacoes',l:'Associações comerciais e de turismo da região'},{v:'eventos',l:'Eventos e feiras do setor'},{v:'visita',l:'Convite para visitar a área'}]},
   {id:'pitch_conf',label:'Sua segurança para apresentar o projeto hoje (1 a 5)',type:'radio',required:true,options:esc5('nenhuma','total')}
  ]},
 {kind:'feedback', title:'Seu índice Zion Investor Ready',
  metrics:function(s,c){return [{label:'Índice de prontidão',value:F.num(c.idx,0)+'/100',tag:'calculado'},{label:'Nível',value:c.nivel,tag:'calculado'},{label:'Lacunas a resolver',value:String(c.lac.length),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:c.idx>=75?'ok':c.idx>=50?'info':'warn',t:'Seu índice é <b>'+F.num(c.idx,0)+'/100</b> ('+c.nivel+'). A dimensão mais fraca é <b>'+c.pior.n+'</b> ('+F.num(c.pior.v,0)+'/100).'});
   if(c.bloqueio) o.push({lv:'bad',t:'Atenção: a situação documental é um bloqueio. Mesmo com índice alto nas outras dimensões, resolva a propriedade com um advogado antes de apresentar o projeto como oportunidade.'});
   if(s.t('clareza')!=='sim') o.push({lv:'warn',t:'Você ainda não tem o pedido em uma frase. Use o modelo do relatório final: quanto, para quê e o que oferece em troca.'});
   if(s.t('perfil_inv')==='nao_sei') o.push({lv:'warn',t:'Defina um perfil de parceiro antes de sair procurando. Uma lista curta de 5 nomes certos vale mais que 50 mensagens.'});
   if(s.t('perfil_inv')==='conhecidos') o.push({lv:'info',t:'Com conhecidos e família, formalize tudo da mesma forma que faria com desconhecidos. Isso protege a relação.'});
   if(sc(s,'pitch_conf',3)<=2&&c.idx>=50) o.push({lv:'info',t:'Seu projeto está mais organizado do que a sua segurança sugere. Ensaie a apresentação com o resumo de 1 página em mãos.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Escrever o pedido em uma frase: quanto, para quê e o que ofereço em troca'},{id:'a7_2',text:'Listar 5 pessoas ou empresas com o perfil de parceiro escolhido'},{id:'a7_3',text:'Resolver as lacunas críticas antes da primeira apresentação'}]}
]}
],

compute:function(s){
 var c={};
 // D1 documentação
 c.docs=arr(s,'doc_checks'); c.nDocs=DOCS.filter(function(d){return has(c.docs,d.v);}).length;
 c.docsFalta=DOCS.filter(function(d){return !has(c.docs,d.v);});
 var st=s.t('doc_status'); c.stPts=s.unknown('doc_status')?0:({regular:100,parcial:50,irregular:0}[st]||0);
 c.d1=0.5*c.stPts+0.5*(c.nDocs/6*100);
 c.bloqueio=s.unknown('doc_status')||st==='irregular';
 // D2 acesso e infraestrutura
 c.acPts={asfalto:100,terra_boa:70,terra_ruim:30,sem:0}[s.t('acesso')]||0;
 c.infra=arr(s,'infra'); c.nInfra=INFRA.filter(function(d){return has(c.infra,d.v);}).length;
 c.d2=0.5*c.acPts+0.5*(c.nInfra/4*100);
 // D3 potencial
 c.car=arr(s,'caracteristicas'); c.nCar=CARAC.filter(function(d){return has(c.car,d.v);}).length;
 var atr=sc(s,'atrativos',1); c.atrPts=(ZA.clamp(atr,1,5)-1)/4*100;
 c.demPts=s.unknown('demanda')?0:({consolidado:100,emergente:60,sem_fluxo:20}[s.t('demanda')]||0);
 c.d3=0.4*c.atrPts+0.4*c.demPts+0.2*(Math.min(c.nCar,4)/4*100);
 // D4 conceito
 c.concLen=s.t('conceito').trim().length; c.difLen=s.t('diferencial').trim().length;
 c.d4=25*(s.t('modelo')&&s.t('modelo')!=='indefinido'?1:0)+25*(s.t('publico')&&s.t('publico')!=='indefinido'?1:0)+25*(c.concLen>=30?1:0)+25*(c.difLen>=5?1:0);
 // D5 números
 var U=s.n('unidades',0), inv=s.n('investimento'), d=s.n('diaria'), oc=s.n('ocupacao'), co=s.n('custo_op');
 c.invKnown=inv!=null; c.origPts=c.invKnown?({cotacoes:100,estimativa:50,nenhum:0}[s.t('orc_origem')]||0):0;
 c.d5=0.4*c.origPts+20*(d!=null?1:0)+20*(oc!=null?1:0)+20*(co!=null?1:0);
 c.rec=(d!=null&&oc!=null&&U>0)?U*365*(oc/100)*d:null;
 c.res=(c.rec!=null&&co!=null)?c.rec*(1-co/100):null;
 c.payback=(c.invKnown&&c.res!=null&&c.res>0)?inv/c.res:null;
 c.gap=c.invKnown?Math.max(0,inv-s.n('recursos',0)):null;
 c.cen=[['Conservador',-15],['Intermediário',0],['Otimista',10]].map(function(x){
  if(d==null||oc==null||co==null||U<=0) return {nome:x[0],occ:null,rec:null,res:null,pb:null};
  var o2=ZA.clamp(oc+x[1],1,100), r=U*365*o2/100*d, re=r*(1-co/100);
  return {nome:x[0],occ:o2,rec:r,res:re,pb:(c.invKnown&&re>0)?inv/re:null};});
 // D6 parceria
 c.gov=arr(s,'governanca'); c.nGov=GOV.filter(function(d){return has(c.gov,d.v);}).length;
 c.d6=40*(s.t('parceria')&&s.t('parceria')!=='indefinido'?1:0)+15*c.nGov;
 // D7 apresentação
 c.mat=arr(s,'materiais'); c.nMat=MAT.filter(function(d){return has(c.mat,d.v);}).length;
 c.matFalta=MAT.filter(function(d){return !has(c.mat,d.v);});
 c.clarPts={sim:100,parcial:50,nao:0}[s.t('clareza')]||0;
 c.d7=0.6*(c.nMat/6*100)+0.4*c.clarPts;
 // índice
 c.idx=DIMS.reduce(function(t,x){return t+x.w*c[x.k];},0)/100;
 c.nivel=nivel(c.idx);
 c.dims=DIMS.map(function(x){return {k:x.k,n:x.n,w:x.w,v:c[x.k],contrib:x.w*c[x.k]/100,who:x.who};});
 c.pior=c.dims.slice().sort(function(a,b){return a.v-b.v;})[0];
 // lacunas
 var L=[]; function lac(dim,t,who,crit){L.push({dim:dim,t:t,who:who,crit:!!crit});}
 if(s.unknown('doc_status')) lac('d1','Confirmar a situação da propriedade (certidão de inteiro teor da matrícula)','Cartório e advogado',true);
 else if(st!=='regular') lac('d1','Resolver a pendência da propriedade ('+(st==='irregular'?'posse sem registro':'inventário, escritura ou divisão')+')','Advogado',true);
 c.docsFalta.forEach(function(x){lac('d1','Obter: '+x.l,x.who,x.v==='matricula'||x.v==='onus');});
 if(c.acPts<70) lac('d2','Levantar solução e custo para o acesso o ano todo','Engenheiro / prefeitura');
 INFRA.forEach(function(x){if(!has(c.infra,x.v)&&x.v!=='construcao') lac('d2','Verificar viabilidade e custo: '+x.l.toLowerCase(),'Concessionária / engenheiro'); else if(!has(c.infra,x.v)) lac('d2','Registrar que não há construção aproveitável (entra no orçamento)','Você');});
 if(s.unknown('demanda')||s.t('demanda')==='sem_fluxo') lac('d3','Demonstrar demanda: pesquisa de 5 hospedagens da região (diária, avaliações, calendário)','Você',true);
 if(atr<=2) lac('d3','Definir o motivo da viagem além dos atrativos (experiência, conforto, gastronomia)','Você');
 if(!s.t('modelo')||s.t('modelo')==='indefinido') lac('d4','Escolher o tipo de hospedagem','Você, com arquiteto',true);
 if(!s.t('publico')||s.t('publico')==='indefinido') lac('d4','Definir o público principal','Você');
 if(c.concLen<30) lac('d4','Escrever a frase do conceito','Você');
 if(c.difLen<5) lac('d4','Definir o diferencial principal','Você');
 if(!c.invKnown) lac('d5','Estimar o investimento da primeira etapa','Fornecedores / arquiteto',true);
 if(s.t('orc_origem')!=='cotacoes') lac('d5','Substituir estimativas por cotações de fornecedores','Fornecedores');
 if(d==null) lac('d5','Pesquisar a diária de referência em concorrentes','Você');
 if(oc==null) lac('d5','Definir uma ocupação prudente com base nos concorrentes','Você');
 if(co==null) lac('d5','Estimar os custos operacionais da hospedagem','Você, com contador');
 if(!s.t('parceria')||s.t('parceria')==='indefinido') lac('d6','Escolher o formato inicial de parceria','Você, com advogado',true);
 GOV.forEach(function(x){if(!has(c.gov,x.v)) lac('d6',{valor_terra:'Obter referência de valor da terra',saida:'Pensar regras de saída',decisao:'Definir como as decisões serão tomadas',assessoria:'Validar o formato com advogado e contador'}[x.v],x.v==='valor_terra'?'Avaliador / corretor':x.v==='assessoria'?'Advogado e contador':'Você, com advogado');});
 c.matFalta.forEach(function(x){lac('d7','Preparar: '+x.l,'Você');});
 if(s.t('clareza')!=='sim') lac('d7','Escrever o pedido em uma frase (quanto, para quê, o que oferece)','Você',true);
 c.lac=L; c.nLac=L.length; c.nCrit=L.filter(function(x){return x.crit;}).length;
 return c;
},

metrics:function(s,c){return [
 {label:'Índice Zion Investor Ready',value:F.num(c.idx,0)+'/100',tag:'calculado'},
 {label:'Nível de prontidão',value:c.nivel,tag:'calculado'},
 {label:'Dimensão mais fraca',value:c.pior.n,tag:'calculado'},
 {label:'Lacunas a resolver',value:c.nLac+' ('+c.nCrit+' críticas)',tag:'calculado'},
 {label:'Área',value:F.num(s.n('area_ha'),1)+' ha',tag:'informado'},
 {label:'Investimento estimado',value:F.brl0(s.n('investimento')),tag:s.t('orc_origem')==='cotacoes'?'informado':'estimativa'},
 {label:'Resultado operacional anual',value:F.brl0(c.res),tag:'estimativa'},
 {label:'Capital a buscar',value:F.brl0(c.gap),tag:'calculado'}
];},

priorities:function(s,c){var L=[];
 if(c.bloqueio) L.push({title:'Esclarecer a situação documental da propriedade com advogado',why:'Sem segurança do ativo, nenhuma outra dimensão sustenta a conversa com investidor.',score:10});
 else if(s.t('doc_status')==='parcial') L.push({title:'Definir com advogado o caminho e o prazo para resolver a pendência da propriedade',why:'O investidor vai perguntar quanto tempo e quanto custa resolver.',score:8});
 if(c.nDocs<4) L.push({title:'Completar a pasta de documentos de base ('+c.nDocs+' de 6)',why:'Faltam: '+c.docsFalta.map(function(d){return d.l.split(' (')[0];}).join('; ')+'.',score:7});
 if(!c.invKnown||s.t('orc_origem')==='nenhum') L.push({title:'Levantar o investimento da primeira etapa com orçamentos',why:'É a primeira pergunta de quem investe.',score:8});
 else if(s.t('orc_origem')==='estimativa') L.push({title:'Trocar a estimativa de investimento por cotações',why:'Números cotados dão credibilidade ao dossiê.',score:5});
 if(c.rec==null||c.res==null) L.push({title:'Completar diária, ocupação e custos para estimar o resultado',why:'Sem eles, não há como responder “quanto pode gerar”.',score:7});
 if(c.payback!=null&&c.payback<3) L.push({title:'Revisar premissas otimistas antes de apresentar',why:'Payback simples de '+F.num(c.payback,1)+' anos tende a gerar desconfiança.',score:6});
 if(s.t('demanda')==='sem_fluxo'||s.unknown('demanda')) L.push({title:'Demonstrar a demanda com pesquisa de concorrentes',why:'O potencial ainda é hipótese.',score:7});
 if(c.d4<75) L.push({title:'Fechar o conceito: tipo, público, frase e diferencial',why:'Conceito em '+F.num(c.d4,0)+'/100: sem ele não há orçamento nem apresentação.',score:6});
 if(c.acPts<70) L.push({title:'Levantar solução e custo para o acesso',why:'Acesso precário pesa na operação e no risco percebido.',score:5});
 if(s.t('parceria')==='indefinido') L.push({title:'Escolher o formato inicial de parceria',why:'O investidor precisa saber como entra e como sai.',score:6});
 if(!has(c.gov,'valor_terra')) L.push({title:'Obter referência de valor da terra',why:'Base para discutir participação ou contrapartida.',score:5});
 if(!has(c.gov,'assessoria')) L.push({title:'Validar o formato de parceria com advogado e contador',why:'Evita acordos informais que geram conflito depois.',score:4});
 if(c.nMat<4) L.push({title:'Montar o resumo executivo, o mapa e a seleção de fotos',why:c.nMat+' de 6 materiais prontos.',score:5});
 if(s.t('clareza')!=='sim') L.push({title:'Escrever o pedido em uma frase',why:'Quanto precisa, para quê e o que oferece em troca.',score:5});
 if(s.t('perfil_inv')==='nao_sei') L.push({title:'Definir o perfil de parceiro e listar 5 nomes',why:'Abordagem dirigida em vez de mensagens em massa.',score:3});
 if(c.idx>=75&&!c.bloqueio) L.push({title:'Agendar as primeiras conversas e visitas à área',why:'O dossiê está organizado o suficiente para conversas preliminares.',score:6});
 return L;},

report:function(s,c){
 var ficha=ZA.table(['Item','Informação'],[
  ['Terra / projeto',esc(s.t('propriedade'))],['Localização',esc(s.t('cidade'))],['Área',F.num(s.n('area_ha'),1)+' ha'],
  ['Situação da propriedade (declarada)',s.unknown('doc_status')?'não informada':esc({regular:'sem pendência conhecida',parcial:'há pendência a resolver',irregular:'posse sem registro'}[s.t('doc_status')]||'—')],
  ['Acesso',esc({asfalto:'asfalto até a entrada',terra_boa:'terra boa o ano todo',terra_ruim:'terra difícil na chuva',sem:'sem acesso para carro comum'}[s.t('acesso')]||'—')],
  ['Conceito',c.concLen?esc(s.t('conceito')):'<span class="za-small">a definir</span>'],
  ['Diferencial',c.difLen?esc(s.t('diferencial')):'<span class="za-small">a definir</span>'],
  ['Primeira etapa',F.num(s.n('unidades'))+' unidade(s) · '+esc({cabanas:'cabanas',glamping:'glamping',chales:'chalés',pousada:'pequena pousada',misto:'modelo misto',indefinido:'tipo a definir'}[s.t('modelo')]||'—')],
  ['Formato de parceria (ponto de partida)',esc({sociedade:'sociedade no projeto',arrendamento:'arrendamento ou cessão de uso',permuta:'permuta',aporte:'aporte com participação nos resultados',indefinido:'a definir'}[s.t('parceria')]||'—')]]);
 var zir=ZA.table(['Dimensão','Peso','Nota','Contribuição','Situação'],c.dims.map(function(x){return [x.n,x.w+'%',F.num(x.v,0)+'/100',F.num(x.contrib,1),x.v>=75?'pronta':x.v>=50?'em estruturação':'lacuna relevante'];}).concat([['<b>Índice Zion Investor Ready</b>','100%','','<b>'+F.num(c.idx,1)+'</b>','<b>'+esc(c.nivel)+'</b>']]),[1,2,3]);
 var lacT=c.lac.length?ZA.table(['Dimensão','Lacuna a resolver','Quem pode ajudar'],c.lac.slice().sort(function(a,b){return (b.crit-a.crit);}).map(function(x){var dn=DIMS.filter(function(d){return d.k===x.dim;})[0].n;return [esc(dn),(x.crit?'<b>crítica</b> · ':'')+esc(x.t),esc(x.who)];})):'<p>Nenhuma lacuna mapeada com os dados informados.</p>';
 var num=c.cen[0].rec==null?'<p class="za-missing">Faltam diária, ocupação ou custos operacionais para montar os cenários. Complete o Pilar 4.</p>':ZA.table(['Cenário','Ocupação','Receita bruta/ano','Resultado operacional/ano','Payback simples'],c.cen.map(function(x){return [x.nome,F.pct(x.occ,0),F.brl0(x.rec),F.brl0(x.res),x.pb==null?'—':F.num(x.pb,1)+' anos'];}),[1,2,3,4])+'<p class="za-small">Conservador = ocupação informada −15 p.p.; otimista = +10 p.p. Mesma diária e mesmo percentual de custos. Valores antes de impostos sobre o lucro, financiamento, depreciação, período de obra e rampa de ocupação. Cenários ilustrativos, não previsões.</p>';
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Unidades na 1ª etapa',F.num(s.n('unidades')),tag('informado')],
  ['Investimento da 1ª etapa',F.brl0(s.n('investimento')),s.unknown('investimento')?tag('hipotese','ausente'):tag(s.t('orc_origem')==='cotacoes'?'informado':'estimativa',s.t('orc_origem')==='cotacoes'?'cotações':'estimativa própria')],
  ['Diária média',F.brl0(s.n('diaria')),s.unknown('diaria')?tag('hipotese','ausente'):tag('estimativa','sua estimativa')],
  ['Ocupação média anual',F.pct(s.n('ocupacao'),0),s.unknown('ocupacao')?tag('hipotese','ausente'):tag('estimativa','sua estimativa')],
  ['Custos operacionais (% da receita)',F.pct(s.n('custo_op'),0),s.unknown('custo_op')?tag('hipotese','ausente'):tag('estimativa','sua estimativa')],
  ['Recursos próprios',F.brl0(s.n('recursos')),tag('informado')],
  ['Pesos das dimensões do índice','20/15/15/10/15/10/15',tag('recomendacao','metodologia Zion')],
  ['Pontuação de acesso','asfalto 100 · terra boa 70 · terra difícil 30 · sem acesso 0',tag('recomendacao','metodologia Zion')]],[1]);
 var modelos={sociedade:'sociedade no projeto',arrendamento:'arrendamento ou cessão de uso',permuta:'permuta',aporte:'aporte com participação nos resultados'};
 var frase='<div class="za-card"><b>Seu pedido em uma frase (rascunho para revisar):</b><p>“Busco '+({local:'um empresário ou investidor da região',turismo:'um parceiro que já atua em turismo e hospedagem',conhecidos:'um parceiro de confiança'}[s.t('perfil_inv')]||'um parceiro')+' para implantar '+F.num(s.n('unidades'))+' unidade(s) na primeira etapa de <b>'+esc(s.t('propriedade'))+'</b>, em '+esc(s.t('cidade'))+(c.invKnown?', com investimento estimado de '+F.brl0(s.n('investimento')):'')+'. '+({terra:'Entro com a área',terra_gestao:'Entro com a área e com a gestão',terra_capital:'Entro com a área e com parte do capital'}[s.t('papel')]||'Entro com a área')+(modelos[s.t('parceria')]?' e proponho, como ponto de partida, '+modelos[s.t('parceria')]+', com os termos a definir com assessoria jurídica e contábil':'')+'.”</p><p class="za-small">Não inclua promessas de rentabilidade. Apresente cenários e premissas.</p></div>';
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido por etapas</b><ol>'+
  '<li><b>Semanas 1 e 2 · segurança do ativo:</b> '+(top[0]?esc(top[0].title):'Atualizar as certidões do imóvel')+'.</li>'+
  '<li><b>Semanas 3 e 4 · números e conceito:</b> '+(top[1]?esc(top[1].title):'Revisar conceito e cenários')+'.</li>'+
  '<li><b>Semanas 5 e 6 · parceria:</b> '+(top[2]?esc(top[2].title):'Validar o formato de parceria com advogado e contador')+'.</li>'+
  '<li><b>Semanas 7 e 8 · material:</b> fechar resumo executivo, mapa, fotos e pasta de documentos; refazer o Zion Investor Ready e comparar o índice.</li>'+
  '<li><b>Depois disso:</b> '+(c.idx>=75&&!c.bloqueio?'conversas preliminares com uma lista curta de parceiros, sempre com assessoria antes de qualquer assinatura.':'só avance para conversas com investidores quando as lacunas críticas estiverem resolvidas.')+'</li></ol></div>';
 return {sections:[
  {title:'Ficha do ativo',html:ficha},
  {title:'Zion Investor Ready · prontidão por dimensão',html:zir+'<p class="za-small">Escala: 75+ pronto para conversas preliminares · 50–74 em estruturação · 25–49 fase inicial · abaixo de 25 ativo ainda não estruturado. O índice mede organização da informação, não o valor nem a viabilidade do imóvel.'+(c.bloqueio?' <b>Bloqueio documental identificado: resolva antes de apresentar.</b>':'')+'</p>'},
  {title:'Lacunas a resolver',html:'<p>'+c.nLac+' lacuna(s) mapeada(s), '+c.nCrit+' crítica(s). As críticas aparecem primeiro.</p>'+lacT},
  {title:'Números preliminares em cenários',html:num+(c.gap!=null?'<p>Capital a buscar além dos seus recursos: <b>'+F.brl0(c.gap)+'</b>.</p>':'')},
  {title:'Pedido ao mercado',html:frase},
  {title:'Premissas utilizadas',html:prem},
  {title:'O que este dossiê não é',html:'<p>Este é um dossiê <b>preliminar e orientativo</b>. Ele não é avaliação de imóvel, laudo, parecer jurídico, estudo de viabilidade definitivo nem oferta de investimento. Antes de qualquer acordo, consulte advogado, contador e, para a implantação, engenheiro ou arquiteto habilitados.</p>'}
 ],plan:plan};
}
});
})();
