/* ZAR-B10 · Como Apresentar Minha Terra para Sócios e Investidores? · Criador de Pitch e Dossiê Turístico */
(function(){
var F=ZA.fmt, esc=ZA.esc;
var SEC=[['ativo','O ativo'],['destino','O destino'],['mercado','O mercado'],['conceito','O conceito'],['invest','O investimento'],['parceria','O modelo de parceria'],['apres','A apresentação']];
var EXP=[{v:'trilhas',l:'Trilhas e natureza'},{v:'gastronomia',l:'Gastronomia local'},{v:'bemestar',l:'Bem-estar (ofurô, spa, yoga)'},{v:'aventura',l:'Aventura (rapel, cachoeiras, bike)'},{v:'rural',l:'Vivência rural'},{v:'eventos',l:'Pequenos eventos'}];
var MAT=[{v:'fotos',l:'Fotos de qualidade do terreno'},{v:'video',l:'Vídeo ou imagens aéreas'},{v:'mapa',l:'Mapa de localização e acesso'},{v:'estudo',l:'Estudo econômico preliminar (ex.: B08)'},{v:'documentos',l:'Documentos do imóvel'},{v:'projeto',l:'Projeto ou estudo arquitetônico'}];
function tag(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';}
function len(s,id){return String(s.t(id)||'').trim().length;}
function txt(s,id,f){var t=String(s.t(id)||'').trim();return t?esc(t):'<i>'+(f||'a preencher')+'</i>';}
function lbl(list,v){for(var i=0;i<list.length;i++)if(list[i].v===v)return list[i].l;return v;}
function status(p){return p>=70?'pronto':p>=40?'ajustar':'lacuna';}
function stTag(p){var st=status(p);return st==='pronto'?tag('calculado','pronto'):st==='ajustar'?tag('estimativa','ajustar'):tag('hipotese','lacuna');}
var MOD={cabana:'Cabanas',glamping:'Glamping',chale:'Chalés',pousada:'Pousada',misto:'Misto',outro:'Outro'};
var PARC={sociedade:'Sociedade no empreendimento',arrendamento:'Arrendamento da área',permuta:'Permuta (terra por unidades ou participação)',investidor:'Investidor financeiro com retorno combinado',indefinido:'Ainda não definido'};
var DOC={escritura:'Escritura registrada em nome do proprietário',regularizacao:'Em regularização',posse:'Posse sem escritura',naosei:'Situação não verificada'};
ZA.register({
id:'B10', code:'ZAR-B10', collection:'Terrenos',
title:'Como Apresentar Minha Terra para Sócios e Investidores?',
subtitle:'Transforme Sua Propriedade em uma Proposta Estruturada',
tool:'Criador de Pitch e Dossiê Turístico',
deliverable:'Pitch e Dossiê Preliminar do Projeto',
nameField:'nome', propertyField:'propriedade',
disclaimer:'O pitch e o dossiê são materiais preliminares montados com as informações que você forneceu; o índice de prontidão mede a completude dessas informações, não a qualidade do negócio. Este material não garante interesse, captação de investimento, fechamento de parceria nem retorno. Números financeiros são estimativas a confirmar. Antes de negociar, valide documentação, licenças e a estrutura da parceria com advogado, contador e demais profissionais habilitados.',

intro:[
 {kind:'mirror', title:'Pare de apresentar apenas fotos da sua terra. Aprenda a apresentar uma oportunidade.',
  lead:'Você mostra o terreno com orgulho: a vista, a cachoeira, o pôr do sol. A pessoa elogia, diz que é lindo… e a conversa termina aí.',
  body:'<div class="za-card"><p>Talvez isso já tenha acontecido com você:</p><ul><li>“Mandei fotos para um possível sócio e ele nunca respondeu.”</li><li>“Me perguntaram quanto custa e quanto rende e eu não soube responder.”</li><li>“Não sei o que colocar numa apresentação.”</li><li>“Tenho medo de parecer amador diante de um investidor.”</li></ul></div>'},
 {kind:'collapse', title:'Uma apresentação visualmente bonita, sem informações suficientes, não substitui um projeto preliminarmente estruturado.',
  lead:'Quem avalia uma parceria quer entender, em poucos minutos: o que é o ativo, por que o destino atrai pessoas, quem é o público, qual é o conceito, quanto custa, como o dinheiro volta e qual é o papel de cada parte.',
  body:'<div class="za-card"><p>Neste percurso você vai organizar sete blocos de informação, que viram:</p><ol><li>um <b>roteiro de pitch slide a slide</b>, montado com as suas respostas;</li><li>um <b>dossiê preliminar</b> com os dados do projeto;</li><li>um <b>índice de prontidão</b> que mostra quais blocos estão completos e quais têm lacunas.</li></ol><p>A ferramenta não inventa números nem promete retorno: ela organiza o que você sabe e aponta o que falta.</p></div>'},
 {kind:'start', title:'Vamos montar o seu pitch e o seu dossiê',
  lead:'Em 7 pilares, você responde sobre o ativo, o destino, o mercado, o conceito, o investimento, a parceria e a apresentação.',
  body:'<p>Se já fez outras mini mentorias da Coleção B (potencial turístico, orçamento, estudo econômico), tenha os resultados à mão. Onde não tiver um dado, marque “não sei”: o relatório mostrará a lacuna.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Helena'},
   {id:'propriedade',label:'Nome do projeto ou da propriedade',type:'text',required:true,placeholder:'Ex.: Reserva Vale do Sol'},
   {id:'municipio',label:'Município / estado',type:'text',required:true,placeholder:'Ex.: Urubici (SC)'},
   {id:'contato',label:'Contato para o último slide (e-mail ou telefone)',type:'text',required:false,placeholder:'Opcional'}
  ]}
],

pillars:[
/* 1 */
{title:'O ativo', screens:[
 {kind:'learn', title:'O ativo: o que exatamente está sendo oferecido',
  body:'<p>O primeiro bloco descreve a terra de forma objetiva: área, localização precisa, situação documental e características que a diferenciam (água, vista, mata, relevo, vizinhança). Quem avalia uma parceria quer saber <b>o que é</b> e <b>se está regular</b> antes de se interessar pelo resto.</p><p>A situação documental pesa muito: um terreno com escritura registrada transmite mais segurança do que uma posse ou uma regularização em andamento. Seja transparente: esconder uma pendência costuma destruir a confiança quando ela aparece. A análise documental deve ser feita por advogado ou no cartório.</p>',
  example:'Exemplo ilustrativo de descrição: “Área de 12 hectares a 12 km do centro, com nascente, trecho de mata nativa e mirante natural voltado para o vale. Escritura registrada.”'},
 {kind:'compare', title:'Descrição emocional × descrição de ativo',
  cols:[{h:'Emocional',type:'bad',items:['“Um paraíso escondido”','Sem área nem localização','Documentação omitida','Só fotos']},
        {h:'De ativo',type:'good',items:['Área em hectares ou m²','Distância do centro e via de acesso','Situação documental declarada','Diferenciais físicos concretos']}]},
 {kind:'form', title:'Descreva o seu ativo',
  fields:[
   {id:'area_ha',label:'Área total',type:'number',required:true,min:0.01,max:100000,step:0.01,unit:'hectares'},
   {id:'localizacao',label:'Localização (distância e referência)',type:'text',required:true,placeholder:'Ex.: 12 km do centro de Urubici, pela SC-370'},
   {id:'documentacao',label:'Situação documental',type:'radio',required:true,options:[{v:'escritura',l:'Escritura registrada em meu nome'},{v:'regularizacao',l:'Em regularização'},{v:'posse',l:'Posse sem escritura'},{v:'naosei',l:'Não sei / não verifiquei'}]},
   {id:'ativo_dif',label:'Diferenciais físicos do terreno',type:'textarea',required:true,placeholder:'Água, vista, mata, relevo, vizinhança, acesso…'}
  ]},
 {kind:'feedback', title:'Prontidão do bloco “O ativo”',
  metrics:function(s,c){return [{label:'Prontidão do bloco',value:F.num(c.sec.ativo)+'/100',tag:'calculado'},{label:'Área',value:F.num(s.n('area_ha'),2)+' ha',tag:'informado'}];},
  feedback:function(s,c){var o=[],d=s.t('documentacao');
   if(d==='escritura') o.push({lv:'ok',t:'Escritura registrada: um dos pontos que mais transmitem segurança. Tenha a matrícula atualizada para o dossiê.'});
   if(d==='regularizacao') o.push({lv:'warn',t:'Documentação em regularização. Informe isso com clareza e mostre em que etapa está, com apoio de advogado.'});
   if(d==='posse') o.push({lv:'bad',t:'Posse sem escritura limita parcerias e financiamentos. Procure um advogado para avaliar os caminhos de regularização antes de apresentar o projeto.'});
   if(d==='naosei') o.push({lv:'bad',t:'Situação documental não verificada. Peça a matrícula atualizada no cartório e consulte um advogado: esta é uma das primeiras perguntas de qualquer parceiro.'});
   if(len(s,'ativo_dif')<40) o.push({lv:'warn',t:'Os diferenciais estão descritos de forma muito curta. Liste características concretas: água, vista, mata, relevo, acesso.'});
   if(len(s,'localizacao')<10) o.push({lv:'warn',t:'Localização pouco precisa. Informe distância do centro e via de acesso.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Pedir a matrícula atualizada do imóvel no cartório'},{id:'a1_2',text:'Consultar um advogado sobre a situação documental'},{id:'a1_3',text:'Escrever a descrição objetiva do ativo em 3 linhas'}]}
]},
/* 2 */
{title:'O destino', screens:[
 {kind:'learn', title:'O destino: por que alguém viajaria até lá',
  body:'<p>Um terreno bonito num destino sem visitantes é um desafio muito maior do que um terreno comum num destino procurado. Este bloco responde: <b>o que atrai pessoas para a região</b>, <b>como se chega</b> e <b>de onde vêm as informações</b>.</p><p>Use fontes verificáveis sempre que possível: secretaria de turismo do município, órgãos oficiais de turismo do estado, dados públicos. Se a informação for sua (observação, conversas), apresente-a como tal. Nunca use números de fluxo turístico sem fonte.</p>',
  example:'Exemplo ilustrativo: “Destino de serra com cânions e cachoeiras, a 2h30 da capital. Acesso por rodovia asfaltada até a cidade e 6 km de estrada de terra em bom estado.”'},
 {kind:'compare', title:'Destino sem fonte × destino com fonte',
  cols:[{h:'Sem fonte',type:'bad',items:['“A região recebe milhares de turistas”','“Está bombando”','Acesso descrito como “fácil”']},
        {h:'Com fonte',type:'good',items:['Atrativos listados e localizados','Distâncias e tipo de estrada','Dados oficiais citados com a fonte','Observações próprias identificadas como tal']}]},
 {kind:'form', title:'Descreva o destino',
  fields:[
   {id:'atrativos',label:'Principais atrativos da região',type:'textarea',required:true,placeholder:'Cachoeiras, parques, gastronomia, eventos, clima…'},
   {id:'dist_cidade',label:'Distância até a cidade mais próxima com serviços',type:'number',required:true,min:0,max:1000,step:0.1,unit:'km',allowUnknown:true},
   {id:'acesso',label:'Acesso até o terreno',type:'radio',required:true,options:[{v:'asfalto',l:'Asfalto até a porteira'},{v:'terra_boa',l:'Estrada de terra em bom estado'},{v:'terra_ruim',l:'Estrada de terra precária'}]},
   {id:'fonte_destino',label:'Você tem informações de fontes oficiais sobre o turismo no destino?',type:'radio',required:true,options:[{v:'oficial',l:'Sim, de órgãos oficiais de turismo'},{v:'propria',l:'Tenho observações e pesquisa própria'},{v:'nenhuma',l:'Não tenho informações'}]}
  ]},
 {kind:'feedback', title:'Prontidão do bloco “O destino”',
  metrics:function(s,c){return [{label:'Prontidão do bloco',value:F.num(c.sec.destino)+'/100',tag:'calculado'},{label:'Distância da cidade',value:s.has('dist_cidade')?F.num(s.n('dist_cidade'),1)+' km':'—',tag:'informado'}];},
  feedback:function(s,c){var o=[],f=s.t('fonte_destino');
   if(f==='oficial') o.push({lv:'ok',t:'Você tem dados oficiais. Cite sempre a fonte e o ano no dossiê.'});
   if(f==='propria') o.push({lv:'info',t:'Informações próprias são válidas, desde que apresentadas como observação. Procure a secretaria de turismo do município para complementar.'});
   if(f==='nenhuma') o.push({lv:'bad',t:'Sem informações sobre o turismo no destino, o investidor não consegue avaliar a demanda. Comece pela secretaria de turismo do município.'});
   if(s.t('acesso')==='terra_ruim') o.push({lv:'warn',t:'Acesso precário é uma objeção previsível. Apresente-o com transparência e, se houver, o plano e o custo para melhorá-lo.'});
   if(s.unknown('dist_cidade')) o.push({lv:'warn',t:'Distância até a cidade não informada. Meça no mapa: é uma informação básica de qualquer dossiê.'});
   if(len(s,'atrativos')<40) o.push({lv:'warn',t:'Atrativos descritos de forma muito curta. Liste nomes, distâncias e o que cada um oferece.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Procurar a secretaria de turismo do município e pedir dados disponíveis'},{id:'a2_2',text:'Montar a lista de atrativos com distâncias até o terreno'},{id:'a2_3',text:'Registrar o acesso com fotos e quilometragem'}]}
]},
/* 3 */
{title:'O mercado', screens:[
 {kind:'learn', title:'O mercado: quem compra e quanto se cobra',
  body:'<p>Este bloco mostra que existe gente disposta a pagar por hospedagem no destino. Ele reúne:</p><ul><li><b>Público:</b> quem visita o destino e quem você quer atender.</li><li><b>Concorrência:</b> quantas hospedagens comparáveis existem.</li><li><b>Referências de preço e ocupação:</b> diárias praticadas por concorrentes parecidos e, se você tiver fonte, uma referência de ocupação.</li></ul><p>A pesquisa de concorrentes é a fonte mais acessível: anúncios em plataformas mostram preços e avaliações. Ocupação é mais difícil de obter: só use um número se souber de onde ele veio.</p>',
  example:'Exemplo ilustrativo: “Pesquisamos 8 hospedagens comparáveis num raio de 15 km. Diária média de R$ 450 em fins de semana fora de feriado. Avaliações elogiam silêncio e vista.”'},
 {kind:'compare', title:'Mercado imaginado × mercado pesquisado',
  cols:[{h:'Imaginado',type:'bad',items:['“Todo mundo quer se hospedar na natureza”','Diária escolhida pelo desejo','Ocupação de sonho, sem fonte']},
        {h:'Pesquisado',type:'good',items:['Público descrito com base em observação','Concorrentes comparáveis contados e listados','Diária de referência de anúncios reais','Ocupação apenas com fonte declarada']}]},
 {kind:'form', title:'Descreva o mercado',
  fields:[
   {id:'publico',label:'Público que você quer atender e por quê',type:'textarea',required:true,placeholder:'Ex.: casais de 30 a 50 anos da capital, que buscam descanso em fins de semana…'},
   {id:'n_conc',label:'Hospedagens comparáveis pesquisadas',type:'number',required:true,min:0,max:500,step:1,unit:'hospedagens',allowUnknown:true},
   {id:'diaria_ref',label:'Diária média de referência dos concorrentes pesquisados',type:'money',required:true,allowUnknown:true},
   {id:'ocup_ref',label:'Ocupação de referência (somente se tiver fonte)',type:'percent',required:true,allowUnknown:true}
  ]},
 {kind:'feedback', title:'Prontidão do bloco “O mercado”',
  metrics:function(s,c){return [{label:'Prontidão do bloco',value:F.num(c.sec.mercado)+'/100',tag:'calculado'},{label:'Receita bruta potencial (referência)',value:c.recPot==null?'—':F.brl(c.recPot),tag:'estimativa'}];},
  feedback:function(s,c){var o=[];
   if(s.unknown('n_conc')||s.n('n_conc',0)===0) o.push({lv:'warn',t:'Nenhum concorrente pesquisado. Analise pelo menos 5 hospedagens comparáveis: preço, avaliações e o que oferecem.'});
   else if(s.n('n_conc')<5) o.push({lv:'warn',t:'Você pesquisou '+F.num(s.n('n_conc'))+' concorrente(s). Amplie para pelo menos 5 para ter uma referência mais sólida.'});
   else o.push({lv:'ok',t:F.num(s.n('n_conc'))+' concorrentes pesquisados: boa base de referência.'});
   if(s.unknown('diaria_ref')) o.push({lv:'warn',t:'Sem diária de referência, o investidor não consegue avaliar a receita. Pesquise anúncios comparáveis.'});
   if(s.unknown('ocup_ref')) o.push({lv:'info',t:'Ocupação de referência não informada. Melhor deixar em branco do que usar um número sem fonte; deixe claro no dossiê que esse dado será levantado.'});
   if(c.recPot!=null) o.push({lv:'info',t:'Com a diária e a ocupação de referência, a receita bruta potencial de hospedagem seria de '+F.brl(c.recPot)+' por ano (estimativa, antes de custos), considerando as unidades do Pilar 4.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Montar uma tabela com 5 a 10 concorrentes: preço, avaliação, diferenciais'},{id:'a3_2',text:'Ler avaliações para entender o que o público valoriza'},{id:'a3_3',text:'Registrar a fonte de cada número usado no dossiê'}]}
]},
/* 4 */
{title:'O conceito', screens:[
 {kind:'learn', title:'O conceito: a ideia do projeto em uma frase',
  body:'<p>O conceito traduz terra, destino e mercado numa proposta clara: <b>que tipo de hospedagem, para quem, com qual experiência</b>. Ele deve caber numa frase e ser coerente com o público do Pilar 3.</p><p>Inclua o modelo (cabanas, glamping, chalés, pousada), a quantidade de unidades prevista e as experiências que tornam o projeto diferente. Experiências ligadas ao próprio terreno e ao destino são as mais convincentes.</p>',
  example:'Exemplo ilustrativo: “Quatro cabanas na mata para casais que buscam silêncio, com trilha até a nascente, café colonial de produtores locais e ofurô privativo.”'},
 {kind:'compare', title:'Conceito genérico × conceito claro',
  cols:[{h:'Genérico',type:'bad',items:['“Um lugar para relaxar na natureza”','Modelo indefinido','Experiências que qualquer um oferece']},
        {h:'Claro',type:'good',items:['Modelo e quantidade de unidades','Público definido','Experiências ligadas ao terreno e ao destino']}]},
 {kind:'form', title:'Defina o conceito',
  fields:[
   {id:'conceito',label:'O conceito do projeto em uma frase',type:'text',required:true,max:200,placeholder:'Ex.: Cabanas na mata para casais em busca de silêncio'},
   {id:'modelo',label:'Modelo de hospedagem',type:'select',required:true,options:[{v:'cabana',l:'Cabanas'},{v:'glamping',l:'Glamping'},{v:'chale',l:'Chalés'},{v:'pousada',l:'Pousada'},{v:'misto',l:'Misto'},{v:'outro',l:'Outro'}]},
   {id:'unidades',label:'Unidades previstas',type:'number',required:true,min:1,max:300,step:1,unit:'unidade(s)'},
   {id:'experiencias',label:'Experiências que farão parte da proposta',type:'checks',options:EXP}
  ]},
 {kind:'feedback', title:'Prontidão do bloco “O conceito”',
  metrics:function(s,c){return [{label:'Prontidão do bloco',value:F.num(c.sec.conceito)+'/100',tag:'calculado'},{label:'Experiências',value:F.num(c.nExp),tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(len(s,'conceito')<20) o.push({lv:'warn',t:'O conceito está curto demais para comunicar a proposta. Inclua modelo, público e experiência numa frase.'});
   else o.push({lv:'ok',t:'Conceito: “'+esc(s.t('conceito'))+'”.'});
   if(c.nExp===0) o.push({lv:'warn',t:'Nenhuma experiência definida. Experiências ligadas ao terreno ajudam a diferenciar o projeto.'});
   if(c.nExp>4) o.push({lv:'info',t:'Muitas experiências ao mesmo tempo podem dispersar o conceito. Destaque as 2 ou 3 mais fortes no pitch.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Testar a frase do conceito com 3 pessoas do público-alvo'},{id:'a4_2',text:'Escolher as 2 ou 3 experiências mais fortes para o pitch'},{id:'a4_3',text:'Fazer um croqui simples da implantação das unidades'}]}
]},
/* 5 */
{title:'O investimento', screens:[
 {kind:'learn', title:'O investimento: quanto custa e como o dinheiro volta',
  body:'<p>Este é o bloco que o investidor procura primeiro e que mais costuma faltar. Ele precisa trazer, com a origem de cada número:</p><ul><li><b>Investimento estimado</b> para implantar o conceito (de preferência baseado em cotações, como no B06).</li><li><b>Receita anual estimada</b> quando o empreendimento estiver operando.</li><li><b>Payback estimado</b> (em quantos anos o investimento seria recuperado), vindo de um estudo como o B08.</li></ul><p>São estimativas, e devem ser apresentadas assim. Números sem base, ou apresentados como garantidos, são um dos principais motivos de perda de credibilidade.</p>',
  example:'Exemplo ilustrativo: “Investimento estimado de R$ 800.000 com base em cotações. Estudo preliminar indica receita de R$ 520.000 por ano a partir do terceiro ano e payback estimado de 7 anos no cenário intermediário.”'},
 {kind:'compare', title:'Números de vendedor × números de dossiê',
  cols:[{h:'De vendedor',type:'bad',items:['“Retorno garantido em 3 anos”','Investimento “de cabeça”','Só o melhor cenário']},
        {h:'De dossiê',type:'good',items:['Investimento com base em cotações','Receita e payback como estimativas','Três cenários e premissas declaradas']}]},
 {kind:'form', title:'Os números do projeto',
  fields:[
   {id:'invest',label:'Investimento total estimado',type:'money',required:true,min:1,allowUnknown:true},
   {id:'base_invest',label:'Base desse valor',type:'radio',required:true,options:[{v:'cotacoes',l:'Cotações e orçamento por itens'},{v:'estimativa',l:'Estimativa própria'},{v:'nao',l:'Ainda não tenho base'}]},
   {id:'receita_est',label:'Receita anual estimada (operação estabilizada)',type:'money',required:true,allowUnknown:true},
   {id:'payback_est',label:'Payback estimado (de um estudo econômico)',type:'number',required:true,min:0.1,max:50,step:0.1,unit:'anos',allowUnknown:true}
  ]},
 {kind:'feedback', title:'Prontidão do bloco “O investimento”',
  metrics:function(s,c){return [{label:'Prontidão do bloco',value:F.num(c.sec.invest)+'/100',tag:'calculado'},{label:'Investimento por unidade',value:c.investUnid==null?'—':F.brl(c.investUnid),tag:'calculado'},{label:'Receita anual ÷ investimento',value:c.giroInv==null?'—':F.pct(c.giroInv*100,0),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(s.unknown('invest')) o.push({lv:'bad',t:'Sem investimento estimado, o pitch não responde à primeira pergunta do investidor. Monte um orçamento (o B06 ajuda).'});
   if(s.t('base_invest')==='nao') o.push({lv:'warn',t:'O investimento ainda não tem base. Antes de apresentar, consiga ao menos cotações dos itens principais.'});
   if(s.unknown('receita_est')||s.unknown('payback_est')) o.push({lv:'warn',t:'Receita e/ou payback não informados. Um estudo econômico preliminar (como o B08) dá esses números com premissas explícitas.'});
   if(c.recIncoerente) o.push({lv:'warn',t:'A receita anual estimada ('+F.brl(s.n('receita_est'))+') está mais de 20% acima da receita bruta potencial calculada com a sua própria diária e ocupação de referência ('+F.brl(c.recPot)+'). Revise as premissas ou explique a diferença (por exemplo, receitas extras).'});
   if(c.giroInv!=null) o.push({lv:'info',t:'A receita anual estimada equivale a '+F.pct(c.giroInv*100,0)+' do investimento. Lembre: receita não é lucro; o dossiê deve mostrar também custos e resultado.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Montar o orçamento de implantação com cotações'},{id:'a5_2',text:'Fazer um estudo econômico com três cenários'},{id:'a5_3',text:'Revisar a linguagem: estimativa, nunca garantia'}]}
]},
/* 6 */
{title:'O modelo de parceria', screens:[
 {kind:'learn', title:'O modelo de parceria: quem entra com o quê',
  body:'<p>Investidores e sócios querem saber <b>o que você está propondo</b>. Alguns formatos comuns de conversa:</p><ul><li><b>Sociedade:</b> terra e capital viram participações num empreendimento.</li><li><b>Arrendamento:</b> o parceiro usa a área por um prazo e paga ao proprietário.</li><li><b>Permuta:</b> a terra é trocada por unidades ou participação no resultado.</li><li><b>Investidor financeiro:</b> aporta capital com uma forma de remuneração combinada.</li></ul><p>Defina o que você <b>busca</b> (valor de aporte, operação, conhecimento) e o que <b>oferece</b> em troca. A forma jurídica, tributária e contratual deve ser estruturada com advogado e contador: este material não substitui essa orientação.</p>',
  example:'Exemplo ilustrativo: “Buscamos sócio com aporte de R$ 400.000 para a implantação. O proprietário entra com a terra e a gestão local. Participação e responsabilidades a definir em acordo, com assessoria jurídica.”'},
 {kind:'compare', title:'Pedido vago × proposta clara',
  cols:[{h:'Vago',type:'bad',items:['“Procuro alguém para investir”','Sem valor de aporte','Sem dizer o que o parceiro recebe','Contrato “de boca”']},
        {h:'Clara',type:'good',items:['Formato de parceria indicado','Valor de aporte buscado','Contrapartidas e papéis descritos','Estrutura validada com advogado e contador']}]},
 {kind:'form', title:'Sua proposta de parceria',
  fields:[
   {id:'modelo_parc',label:'Formato de parceria que você pretende propor',type:'radio',required:true,options:Object.keys(PARC).map(function(k){return {v:k,l:PARC[k]};})},
   {id:'aporte',label:'Valor de aporte buscado',type:'money',required:true,allowUnknown:true},
   {id:'contrapartida',label:'O que você oferece e o que espera do parceiro',type:'textarea',required:true,placeholder:'Ex.: entro com a terra e a gestão local; busco capital para a implantação e experiência em hospitalidade…'},
   {id:'consultou',label:'Você já consultou profissionais sobre a estrutura da parceria?',type:'radio',required:true,options:[{v:'ambos',l:'Advogado e contador'},{v:'advogado',l:'Somente advogado'},{v:'contador',l:'Somente contador'},{v:'nao',l:'Ainda não'}]}
  ]},
 {kind:'feedback', title:'Prontidão do bloco “O modelo de parceria”',
  metrics:function(s,c){return [{label:'Prontidão do bloco',value:F.num(c.sec.parceria)+'/100',tag:'calculado'},{label:'Aporte ÷ investimento',value:c.aportePct==null?'—':F.pct(c.aportePct*100,0),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(s.t('modelo_parc')==='indefinido') o.push({lv:'warn',t:'Formato de parceria indefinido. Você pode apresentar opções, mas o interlocutor precisa saber o que está sendo proposto.'});
   if(s.t('consultou')==='nao') o.push({lv:'warn',t:'Antes de formalizar qualquer acordo, consulte advogado e contador sobre a estrutura da parceria.'});
   if(c.aportePct!=null&&c.aportePct>1) o.push({lv:'warn',t:'O aporte buscado é maior que o investimento estimado. Explique a diferença (capital de giro, reservas) ou revise os números.'});
   if(c.aportePct!=null&&c.aportePct<=1) o.push({lv:'info',t:'O aporte buscado cobre '+F.pct(c.aportePct*100,0)+' do investimento estimado. Mostre de onde virá o restante.'});
   if(len(s,'contrapartida')<40) o.push({lv:'warn',t:'Contrapartidas pouco detalhadas. Descreva o que cada parte entrega e espera.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Agendar conversa com advogado sobre o formato de parceria'},{id:'a6_2',text:'Conversar com um contador sobre a estrutura tributária'},{id:'a6_3',text:'Escrever os papéis e responsabilidades de cada parte'}]}
]},
/* 7 */
{title:'A apresentação', screens:[
 {kind:'learn', title:'A apresentação: o roteiro em 10 slides',
  body:'<p>O Criador monta um roteiro de pitch em 10 slides a partir das suas respostas:</p><ol><li>Capa e conceito</li><li>A oportunidade</li><li>O ativo</li><li>O destino e o acesso</li><li>Mercado e público</li><li>Conceito e experiências</li><li>Investimento e números preliminares</li><li>Modelo de parceria</li><li>Pontos de atenção e próximos passos</li><li>Contato</li></ol><p>Ajuste o roteiro ao interlocutor: um sócio-operador quer entender a operação; um investidor financeiro, os números e a segurança; familiares e amigos, a clareza e o risco. Leve materiais de apoio: fotos, mapa, estudo, documentos.</p>',
  example:'Exemplo ilustrativo: para uma reunião de 15 minutos, cerca de 1 minuto por slide e 5 minutos para perguntas.'},
 {kind:'compare', title:'Apresentação que encanta × apresentação que convence',
  cols:[{h:'Só encanta',type:'bad',items:['Muitas fotos, poucos dados','Sem pedido claro no final','Pendências escondidas']},
        {h:'Convence',type:'good',items:['Fotos com dados objetivos','Pedido e próximos passos claros','Pontos de atenção apresentados com plano']}]},
 {kind:'form', title:'Como será a sua apresentação',
  fields:[
   {id:'publico_pitch',label:'Para quem você vai apresentar primeiro?',type:'radio',required:true,options:[{v:'anjo',l:'Investidor pessoa física'},{v:'socio_operador',l:'Sócio-operador (alguém do ramo de hospedagem)'},{v:'fundo',l:'Empresa ou fundo de investimento'},{v:'familia',l:'Familiares e amigos'}]},
   {id:'formato',label:'Formato',type:'radio',required:true,options:[{v:'presencial',l:'Reunião presencial (com visita ao terreno)'},{v:'online',l:'Reunião online'},{v:'documento',l:'Documento enviado por mensagem ou e-mail'}]},
   {id:'tempo',label:'Tempo disponível para a apresentação',type:'number',required:true,min:1,max:120,step:1,unit:'minutos'},
   {id:'materiais',label:'Materiais de apoio que você já tem',type:'checks',options:MAT}
  ]},
 {kind:'feedback', title:'Seu índice de prontidão',
  metrics:function(s,c){return [{label:'Índice de prontidão',value:F.num(c.indice,0)+'/100',tag:'calculado'},{label:'Classificação',value:c.classe,tag:'calculado'},{label:'Blocos com lacuna',value:F.num(c.nLacunas),tag:'calculado'}];},
  feedback:function(s,c){var o=[],p=s.t('publico_pitch'),t=s.n('tempo',0);
   if(c.indice>=80) o.push({lv:'ok',t:'Seu material está bem estruturado ('+F.num(c.indice,0)+'/100). Revise as lacunas restantes antes da reunião.'});
   else if(c.indice>=60) o.push({lv:'warn',t:'Seu material está em estruturação ('+F.num(c.indice,0)+'/100). Complete os blocos marcados como “ajustar” ou “lacuna”.'});
   else o.push({lv:'bad',t:'O material ainda é inicial ('+F.num(c.indice,0)+'/100). Antes de apresentar, resolva as lacunas principais: o risco é perder credibilidade numa primeira conversa.'});
   if(c.piorSec) o.push({lv:'info',t:'Bloco mais fraco: <b>'+c.piorSec[1]+'</b> ('+F.num(c.sec[c.piorSec[0]])+'/100).'});
   if((p==='anjo'||p==='fundo')&&c.sec.invest<70) o.push({lv:'bad',t:'Você vai falar com investidor, mas o bloco de investimento está incompleto. Esse é o bloco que ele mais vai perguntar.'});
   if(p==='socio_operador'&&c.sec.mercado<70) o.push({lv:'warn',t:'Um sócio-operador vai querer entender o mercado. Reforce o bloco de mercado.'});
   if(t<5) o.push({lv:'warn',t:'Menos de 5 minutos é pouco para 10 slides. Prepare uma versão curta com capa, oportunidade, números e pedido.'});
   if(t>30) o.push({lv:'info',t:'Mais de 30 minutos: reserve metade do tempo para perguntas e, se possível, para a visita ao terreno.'});
   if((s.v.materiais||[]).indexOf('documentos')<0) o.push({lv:'warn',t:'Documentos do imóvel não estão entre os materiais. Eles costumam ser pedidos logo após a primeira conversa.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Montar os 10 slides a partir do roteiro do relatório'},{id:'a7_2',text:'Ensaiar a apresentação no tempo disponível'},{id:'a7_3',text:'Preparar uma pasta com documentos, mapa e estudo para enviar depois da reunião'}]}
]}
],

compute:function(s){
 var c={sec:{}};
 var doc={escritura:40,regularizacao:20,posse:10,naosei:0}[s.t('documentacao')]||0;
 c.sec.ativo=(s.n('area_ha',0)>0?20:0)+(len(s,'localizacao')>=10?20:len(s,'localizacao')>0?10:0)+doc+(len(s,'ativo_dif')>=40?20:len(s,'ativo_dif')>0?10:0);
 c.sec.destino=(len(s,'atrativos')>=40?30:len(s,'atrativos')>0?15:0)+(s.has('dist_cidade')?20:0)+({asfalto:20,terra_boa:15,terra_ruim:5}[s.t('acesso')]||0)+({oficial:30,propria:20,nenhuma:0}[s.t('fonte_destino')]||0);
 c.sec.mercado=(len(s,'publico')>=40?30:len(s,'publico')>0?15:0)+(s.has('n_conc')&&s.n('n_conc')>=1?20:0)+(s.has('diaria_ref')?25:0)+(s.has('ocup_ref')?25:0);
 c.nExp=(s.v.experiencias||[]).length;
 c.sec.conceito=(len(s,'conceito')>=20?30:len(s,'conceito')>0?15:0)+(s.t('modelo')?20:0)+(s.n('unidades',0)>0?20:0)+(c.nExp>=2?30:c.nExp===1?15:0);
 c.sec.invest=(s.has('invest')?30:0)+({cotacoes:30,estimativa:15,nao:0}[s.t('base_invest')]||0)+(s.has('receita_est')?20:0)+(s.has('payback_est')?20:0);
 c.sec.parceria=(s.t('modelo_parc')&&s.t('modelo_parc')!=='indefinido'?30:0)+(s.has('aporte')?20:0)+(len(s,'contrapartida')>=40?30:len(s,'contrapartida')>0?15:0)+({ambos:20,advogado:15,contador:15,nao:0}[s.t('consultou')]||0);
 var t=s.n('tempo',0); c.nMat=(s.v.materiais||[]).length;
 c.sec.apres=(s.t('publico_pitch')?20:0)+(s.t('formato')?10:0)+(t>=5&&t<=30?10:0)+Math.min(60,c.nMat*10);
 var tot=0; SEC.forEach(function(x){tot+=c.sec[x[0]];}); c.indice=tot/SEC.length;
 c.classe=c.indice>=80?'Estruturado':c.indice>=60?'Em estruturação':'Inicial';
 c.nLacunas=SEC.filter(function(x){return c.sec[x[0]]<40;}).length;
 c.piorSec=SEC.slice().sort(function(a,b){return c.sec[a[0]]-c.sec[b[0]];})[0];
 var U=s.n('unidades',0);
 c.recPot=(U>0&&s.has('diaria_ref')&&s.has('ocup_ref'))?U*365*s.n('ocup_ref')/100*s.n('diaria_ref'):null;
 c.investUnid=(s.has('invest')&&U>0)?s.n('invest')/U:null;
 c.giroInv=(s.has('invest')&&s.has('receita_est'))?s.n('receita_est')/s.n('invest'):null;
 c.aportePct=(s.has('invest')&&s.has('aporte'))?s.n('aporte')/s.n('invest'):null;
 c.recIncoerente=(c.recPot!=null&&s.has('receita_est')&&s.n('receita_est')>c.recPot*1.2);
 // lacunas concretas
 var L=[];
 if(['posse','naosei'].indexOf(s.t('documentacao'))>=0) L.push('Situação documental do imóvel');
 if(s.unknown('dist_cidade')) L.push('Distância até a cidade');
 if(s.t('fonte_destino')==='nenhuma') L.push('Informações sobre o turismo no destino');
 if(!s.has('n_conc')||s.n('n_conc')<1) L.push('Pesquisa de concorrentes');
 if(!s.has('diaria_ref')) L.push('Diária de referência');
 if(!s.has('ocup_ref')) L.push('Ocupação de referência com fonte');
 if(c.nExp===0) L.push('Experiências da proposta');
 if(!s.has('invest')) L.push('Investimento estimado');
 if(s.t('base_invest')==='nao') L.push('Base do investimento (cotações)');
 if(!s.has('receita_est')) L.push('Receita anual estimada');
 if(!s.has('payback_est')) L.push('Payback estimado');
 if(s.t('modelo_parc')==='indefinido') L.push('Formato de parceria');
 if(!s.has('aporte')) L.push('Valor de aporte buscado');
 if(s.t('consultou')==='nao') L.push('Orientação de advogado e contador');
 if(c.nMat<3) L.push('Materiais de apoio');
 c.lacunas=L; c.nLacunasItens=L.length;
 return c;
},

metrics:function(s,c){return [
 {label:'Índice de prontidão',value:F.num(c.indice,0)+'/100',tag:'calculado'},
 {label:'Classificação',value:c.classe,tag:'calculado'},
 {label:'Bloco mais fraco',value:c.piorSec[1],tag:'calculado'},
 {label:'Lacunas de informação',value:F.num(c.nLacunasItens),tag:'calculado'},
 {label:'Investimento estimado',value:s.has('invest')?F.brl(s.n('invest')):'—',tag:s.has('invest')?'informado':'hipotese'},
 {label:'Investimento por unidade',value:c.investUnid==null?'—':F.brl(c.investUnid),tag:'calculado'},
 {label:'Receita bruta potencial (referência)',value:c.recPot==null?'—':F.brl(c.recPot),tag:'estimativa'},
 {label:'Aporte buscado',value:s.has('aporte')?F.brl(s.n('aporte')):'—',tag:s.has('aporte')?'informado':'hipotese'}
];},

priorities:function(s,c){var L=[],d=s.t('documentacao'),p=s.t('publico_pitch');
 if(d==='naosei'||d==='posse') L.push({title:'Verificar a documentação do imóvel com advogado',why:'É uma das primeiras perguntas de qualquer parceiro.',score:10});
 if(!s.has('invest')||s.t('base_invest')==='nao') L.push({title:'Montar o orçamento de implantação com cotações',why:'Sem investimento com base, o pitch não responde quanto custa.',score:9});
 if(!s.has('receita_est')||!s.has('payback_est')) L.push({title:'Fazer um estudo econômico preliminar com três cenários',why:'Receita e payback estão ausentes.',score:8});
 if(s.t('fonte_destino')==='nenhuma') L.push({title:'Levantar informações sobre o turismo no destino',why:'Sem elas, não há como mostrar a demanda.',score:8});
 if(!s.has('n_conc')||s.n('n_conc')<5) L.push({title:'Pesquisar pelo menos 5 concorrentes comparáveis',why:'A referência de mercado está fraca.',score:7});
 if(s.t('modelo_parc')==='indefinido') L.push({title:'Definir o formato de parceria a propor',why:'O interlocutor precisa saber o que está sendo proposto.',score:7});
 if(s.t('consultou')==='nao') L.push({title:'Consultar advogado e contador sobre a estrutura da parceria',why:'Acordos sem orientação profissional criam riscos para as duas partes.',score:7});
 if(c.recIncoerente) L.push({title:'Conciliar a receita estimada com as referências de mercado',why:'A receita informada está acima do potencial calculado com sua diária e ocupação de referência.',score:7});
 if((p==='anjo'||p==='fundo')&&c.sec.invest<70) L.push({title:'Completar o bloco de investimento antes de falar com investidor',why:'É o bloco que o investidor mais pergunta.',score:9});
 if(len(s,'conceito')<20) L.push({title:'Reescrever o conceito em uma frase clara',why:'Modelo, público e experiência precisam caber numa frase.',score:6});
 if(c.nMat<3) L.push({title:'Preparar materiais de apoio: fotos, mapa e documentos',why:'Apenas '+c.nMat+' material(is) disponível(is).',score:6});
 if(s.t('acesso')==='terra_ruim') L.push({title:'Apresentar o plano para o acesso ao terreno',why:'Acesso precário é uma objeção previsível.',score:5});
 if(!s.has('aporte')) L.push({title:'Definir o valor de aporte buscado',why:'O pedido precisa ser claro no último slide.',score:5});
 L.push({title:'Ensaiar o pitch no tempo disponível',why:'Clareza e objetividade fazem diferença na primeira conversa.',score:3});
 return L;},

report:function(s,c){
 var inf=tag('informado'), cal=tag('calculado'), hip=tag('hipotese','hipótese'), est=tag('estimativa');
 var U=s.n('unidades',0);
 var prem=ZA.table(['Informação','Valor','Origem'],[
  ['Área',F.num(s.n('area_ha'),2)+' ha',inf],
  ['Documentação',esc(DOC[s.t('documentacao')]||'—'),d0(s.t('documentacao'))],
  ['Distância até a cidade',s.has('dist_cidade')?F.num(s.n('dist_cidade'),1)+' km':'—',s.has('dist_cidade')?inf:hip],
  ['Concorrentes pesquisados',s.has('n_conc')?F.num(s.n('n_conc')):'—',s.has('n_conc')?inf:hip],
  ['Diária / ocupação de referência',(s.has('diaria_ref')?F.brl(s.n('diaria_ref')):'—')+' / '+(s.has('ocup_ref')?F.pct(s.n('ocup_ref'),0):'—'),(s.has('diaria_ref')&&s.has('ocup_ref'))?inf:hip],
  ['Unidades previstas',F.num(U),inf],
  ['Investimento estimado',s.has('invest')?F.brl(s.n('invest')):'—',s.has('invest')?(s.t('base_invest')==='cotacoes'?inf:est):hip],
  ['Receita anual estimada',s.has('receita_est')?F.brl(s.n('receita_est')):'—',s.has('receita_est')?est:hip],
  ['Payback estimado',s.has('payback_est')?F.num(s.n('payback_est'),1)+' anos':'—',s.has('payback_est')?est:hip],
  ['Receita bruta potencial',c.recPot==null?'—':F.brl(c.recPot)+' (unidades × 365 × ocupação × diária de referência)',c.recPot==null?hip:cal],
  ['Aporte buscado',s.has('aporte')?F.brl(s.n('aporte')):'—',s.has('aporte')?inf:hip]],[]);
 function d0(v){return (v==='naosei'||!v)?hip:inf;}
 var pront=ZA.table(['Bloco','Prontidão','Situação'],SEC.map(function(x){return [x[1],F.num(c.sec[x[0]])+'/100',stTag(c.sec[x[0]])];}).concat([['<b>Índice geral</b>','<b>'+F.num(c.indice,0)+'/100</b>',esc(c.classe)]]),[1]);
 var exps=(s.v.experiencias||[]).map(function(v){return lbl(EXP,v);});
 var mats=(s.v.materiais||[]).map(function(v){return lbl(MAT,v);});
 var nome=txt(s,'propriedade'), mun=txt(s,'municipio');
 var slides=[
  ['Capa e conceito','ativo',nome+' · '+mun+'<br>'+txt(s,'conceito','conceito a definir')],
  ['A oportunidade','destino','Terra de '+F.num(s.n('area_ha'),2)+' ha num destino com: '+txt(s,'atrativos','atrativos a descrever')+'.'],
  ['O ativo','ativo','Localização: '+txt(s,'localizacao')+'. Documentação: '+esc(DOC[s.t('documentacao')]||'a verificar')+'. Diferenciais: '+txt(s,'ativo_dif')+'.'],
  ['O destino e o acesso','destino','Distância até a cidade: '+(s.has('dist_cidade')?F.num(s.n('dist_cidade'),1)+' km':'<i>a medir</i>')+'. Acesso: '+esc(({asfalto:'asfalto até a porteira',terra_boa:'estrada de terra em bom estado',terra_ruim:'estrada de terra precária'})[s.t('acesso')]||'—')+'. Fonte das informações: '+esc(({oficial:'órgãos oficiais de turismo',propria:'observação e pesquisa própria',nenhuma:'a levantar'})[s.t('fonte_destino')]||'—')+'.'],
  ['Mercado e público','mercado','Público: '+txt(s,'publico')+'. Concorrentes comparáveis pesquisados: '+(s.has('n_conc')?F.num(s.n('n_conc')):'<i>a pesquisar</i>')+'. Diária de referência: '+(s.has('diaria_ref')?F.brl(s.n('diaria_ref')):'<i>a pesquisar</i>')+'.'],
  ['Conceito e experiências','conceito',esc(MOD[s.t('modelo')]||'—')+', '+F.num(U)+' unidade(s). Experiências: '+(exps.length?esc(exps.join(', ')):'<i>a definir</i>')+'.'],
  ['Investimento e números preliminares','invest','Investimento estimado: '+(s.has('invest')?F.brl(s.n('invest')):'<i>a orçar</i>')+(c.investUnid!=null?' ('+F.brl(c.investUnid)+' por unidade)':'')+'. Receita anual estimada: '+(s.has('receita_est')?F.brl(s.n('receita_est')):'<i>a estudar</i>')+'. Payback estimado: '+(s.has('payback_est')?F.num(s.n('payback_est'),1)+' anos':'<i>a estudar</i>')+'. Todos os valores são estimativas preliminares.'],
  ['Modelo de parceria','parceria',esc(PARC[s.t('modelo_parc')]||'—')+'. Aporte buscado: '+(s.has('aporte')?F.brl(s.n('aporte')):'<i>a definir</i>')+'. Contrapartidas: '+txt(s,'contrapartida')+'. Estrutura a validar com advogado e contador.'],
  ['Pontos de atenção e próximos passos','apres',c.lacunas.length?'Itens em levantamento: '+esc(c.lacunas.slice(0,5).join('; '))+'.':'Informações principais levantadas; próximos passos: visita ao terreno e aprofundamento do estudo.'],
  ['Contato','apres',txt(s,'nome')+(s.t('contato')?' · '+esc(s.t('contato')):'')+' · Pedido: '+(s.has('aporte')?'conversa sobre aporte de '+F.brl(s.n('aporte')):'conversa inicial sobre parceria')+'.']
 ];
 var roteiro=ZA.table(['Slide','Conteúdo montado com suas respostas','Status'],slides.map(function(x,i){return ['<b>'+(i+1)+'. '+x[0]+'</b>',x[2],stTag(c.sec[x[1]])];}),[]);
 var dossie='<div class="za-card"><p><b>'+nome+'</b> · '+mun+'</p><p><b>Conceito:</b> '+txt(s,'conceito')+'</p><p><b>Ativo:</b> '+F.num(s.n('area_ha'),2)+' ha; '+txt(s,'localizacao')+'.</p><p><b>Destino:</b> '+txt(s,'atrativos')+'</p><p><b>Público:</b> '+txt(s,'publico')+'</p><p><b>Parceria proposta:</b> '+esc(PARC[s.t('modelo_parc')]||'—')+'. '+txt(s,'contrapartida')+'</p><p><b>Materiais disponíveis:</b> '+(mats.length?esc(mats.join(', ')):'<i>nenhum ainda</i>')+'.</p></div>';
 var lac=c.lacunas.length?'<ul>'+c.lacunas.map(function(x){return '<li>'+esc(x)+'</li>';}).join('')+'</ul>':'<p class="za-small">Nenhuma lacuna crítica identificada.</p>';
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido até a primeira apresentação</b><ol>'+
  '<li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Revisar o dossiê')+'.</li>'+
  '<li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Completar o bloco mais fraco')+'.</li>'+
  '<li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Preparar materiais de apoio')+'.</li>'+
  '<li><b>Semana 4:</b> montar os 10 slides com o roteiro acima, refazer o índice de prontidão e ensaiar em '+F.num(s.n('tempo',15))+' minutos.</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Índice de prontidão por bloco',html:pront+'<p class="za-small">O índice mede a completude das informações (0 a 100), não a qualidade do negócio. Pronto ≥ 70; ajustar 40 a 69; lacuna &lt; 40.</p>'},
  {title:'Roteiro do pitch slide a slide',html:roteiro},
  {title:'Dossiê preliminar',html:dossie},
  {title:'Lacunas de informação',html:lac}
 ],plan:plan};
}
});
})();
