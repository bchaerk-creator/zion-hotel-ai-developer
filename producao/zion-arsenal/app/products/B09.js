/* ZAR-B09 · Como Começar um Projeto Turístico com Pouco Capital? · Planejador de Implantação Progressiva */
(function(){
var F=ZA.fmt, esc=ZA.esc, HM=120;
function tag(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';}
function mes(m){return ZA.isNum(m)?'mês '+m:'não ocorre em 10 anos';}
function rowsOf(s,id){return (s.v[id]||[]).filter(function(r){return r&&ZA.isNum(r.value)&&r.value>0;});}
ZA.register({
id:'B09', code:'ZAR-B09', collection:'Terrenos',
title:'Como Começar um Projeto Turístico com Pouco Capital?',
subtitle:'Desenvolva Seu Projeto por Etapas',
tool:'Planejador de Implantação Progressiva',
deliverable:'Plano de Implantação por Etapas',
nameField:'nome', propertyField:'propriedade',
disclaimer:'O plano por etapas é uma simulação preliminar feita com as premissas que você informou. A geração de caixa de cada fase depende de ocupação, diária e custos reais, que podem ser diferentes: não há garantia de que a primeira etapa financie as seguintes, nem de prazos, reservas ou retorno. Projetos, licenças e a viabilidade de construir em fases devem ser confirmados com arquiteto, engenheiro, prefeitura e órgão ambiental; questões societárias e tributárias, com advogado e contador.',

intro:[
 {kind:'mirror', title:'Você não precisa começar com dez cabanas. Mas precisa saber como começar.',
  lead:'Você tem a terra e o sonho do projeto completo. Quando soma tudo, o valor assusta e o projeto fica parado esperando um dinheiro que talvez nunca chegue de uma vez.',
  body:'<div class="za-card"><p>Talvez você pense assim:</p><ul><li>“Só vale a pena começar quando eu tiver o dinheiro para fazer tudo.”</li><li>“Uma cabana só não paga a infraestrutura.”</li><li>“Não sei o que construir primeiro.”</li><li>“Tenho medo de começar pequeno e não conseguir crescer.”</li></ul></div>'},
 {kind:'collapse', title:'Um projeto menor, planejado corretamente, pode ser uma alternativa a começar uma obra maior sem estrutura financeira.',
  lead:'A implantação progressiva divide o projeto em fases: uma primeira etapa enxuta, que já pode receber hóspedes, e expansões planejadas, em parte financiadas pelo resultado da operação.',
  body:'<div class="za-card"><p>Para funcionar, o plano por etapas precisa responder:</p><ol><li>Qual é a <b>visão final</b> do projeto?</li><li>Que <b>infraestrutura essencial</b> precisa existir desde o início?</li><li>Qual é a <b>menor primeira etapa</b> capaz de operar bem?</li><li>Quanto cada fase <b>custa</b> e quanto <b>gera</b> por mês?</li><li>Em que <b>mês</b> cada nova fase pode começar, com o caixa acumulado?</li></ol><p>O Planejador simula isso mês a mês por até 10 anos.</p></div>'},
 {kind:'start', title:'Vamos planejar a sua implantação por etapas',
  lead:'Em 7 pilares, você define a visão final, a primeira etapa e as expansões, e sai com um cronograma de fases e a geração de caixa de cada uma.',
  body:'<p>Tenha à mão, se possível: orçamento de infraestrutura e de uma unidade (o B06 ajuda), uma diária de referência e uma estimativa de custos mensais. Onde não tiver um dado, marque “não sei” quando houver a opção.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Roberto'},
   {id:'propriedade',label:'Nome do projeto',type:'text',required:true,placeholder:'Ex.: Recanto das Pedras'},
   {id:'municipio',label:'Município / destino',type:'text',required:true,placeholder:'Ex.: São Bento do Sapucaí (SP)'},
   {id:'modelo',label:'Modelo de hospedagem',type:'select',required:true,options:[{v:'cabana',l:'Cabanas'},{v:'chale',l:'Chalés'},{v:'glamping',l:'Glamping'},{v:'container',l:'Módulos / contêineres'},{v:'pousada',l:'Pousada em módulos'},{v:'outro',l:'Outro'}]}
  ]}
],

pillars:[
/* 1 */
{title:'Visão final', screens:[
 {kind:'learn', title:'Comece pelo fim: a visão final orienta cada etapa',
  body:'<p>Implantar por etapas não é improvisar. A <b>visão final</b> é o desenho do projeto completo: quantas unidades, onde ficam, quais áreas comuns. Mesmo que só uma parte seja construída agora, a primeira etapa deve ser posicionada pensando no todo: caminhos, redes de água e energia, esgoto e acessos dimensionados para crescer.</p><p>Sem a visão final, cada fase vira um remendo: rede elétrica refeita, unidade no lugar errado, obra que atrapalha hóspedes.</p>',
  example:'Exemplo ilustrativo: um projeto de 6 cabanas com implantação em 3 fases de 2 cabanas. O projeto arquitetônico mostra as 6 posições desde o início, e a primeira fase ocupa as posições mais próximas do acesso.'},
 {kind:'compare', title:'Crescer no improviso × crescer com plano',
  cols:[{h:'Improviso',type:'bad',items:['Construir a primeira unidade “onde der”','Redes dimensionadas só para a primeira fase','Ampliar sem saber se a prefeitura permite']},
        {h:'Plano',type:'good',items:['Projeto da visão final aprovado ou orientado por profissional','Redes e acessos pensados para o total','Cada fase com posição e cronograma definidos']}]},
 {kind:'form', title:'Sua visão final',
  fields:[
   {id:'unid_final',label:'Quantidade total de unidades na visão final',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)'},
   {id:'prazo_visao',label:'Em quantos anos você gostaria de chegar à visão final?',type:'number',required:true,min:1,max:15,step:1,unit:'anos'},
   {id:'tem_projeto',label:'Existe um projeto da visão final?',type:'radio',required:true,options:[{v:'aprovado',l:'Sim, com profissional e consulta à prefeitura'},{v:'croqui',l:'Tenho um croqui ou desenho meu'},{v:'nao',l:'Ainda não'}]}
  ]},
 {kind:'feedback', title:'Sua visão de longo prazo',
  metrics:function(s,c){return [{label:'Unidades na visão final',value:F.num(c.uFinal),tag:'informado'},{label:'Prazo desejado',value:F.num(s.n('prazo_visao'))+' anos',tag:'informado'}];},
  feedback:function(s,c){var o=[],p=s.t('tem_projeto');
   if(p==='nao') o.push({lv:'bad',t:'Sem projeto da visão final, a primeira etapa corre o risco de ser construída no lugar errado ou com redes subdimensionadas. Procure um arquiteto ou engenheiro para um estudo de implantação.'});
   if(p==='croqui') o.push({lv:'warn',t:'Um croqui ajuda, mas confirme com profissional habilitado e com a prefeitura se a implantação total é possível no terreno.'});
   if(p==='aprovado') o.push({lv:'ok',t:'Projeto da visão final com orientação profissional: base sólida para planejar as fases.'});
   o.push({lv:'info',t:'Visão de '+F.num(c.uFinal)+' unidades em '+F.num(s.n('prazo_visao'))+' anos. No Pilar 7 você verá se o caixa gerado pelas fases permite chegar lá nesse prazo.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Contratar ou consultar um profissional para o estudo de implantação total'},{id:'a1_2',text:'Marcar no mapa do terreno a posição de todas as unidades da visão final'},{id:'a1_3',text:'Consultar a prefeitura sobre a possibilidade de aprovar o projeto por etapas'}]}
]},
/* 2 */
{title:'Infraestrutura essencial', screens:[
 {kind:'learn', title:'O que precisa existir antes da primeira unidade',
  body:'<p>A primeira fase carrega um peso especial: ela precisa pagar a <b>infraestrutura essencial</b>, que serve ao projeto inteiro. Normalmente: acesso transitável, energia, água, tratamento de esgoto, projetos e licenças. Parte dela pode ser feita em módulos (por exemplo, um sistema de esgoto ampliável), mas alguns itens não podem ser divididos.</p><p>Por isso a primeira fase costuma ter o maior custo por unidade. Nas fases seguintes, entra apenas uma <b>infraestrutura de expansão</b> (extensão de redes e caminhos até as novas unidades).</p>',
  example:'Exemplo ilustrativo: R$ 65.000 de infraestrutura essencial + 2 cabanas de R$ 90.000 = R$ 245.000 na fase 1, ou R$ 122.500 por unidade. Uma fase 2 com 2 cabanas e R$ 10.000 de extensão de redes custa R$ 190.000, ou R$ 95.000 por unidade.'},
 {kind:'compare', title:'Infraestrutura mínima × infraestrutura essencial',
  cols:[{h:'Mínima demais',type:'bad',items:['Fossa improvisada para “depois ver”','Energia emprestada do vizinho','Acesso que fecha na chuva']},
        {h:'Essencial bem feita',type:'good',items:['Solução de esgoto adequada, orientada por profissional','Padrão de energia dimensionado para crescer','Acesso transitável o ano todo']}]},
 {kind:'form', title:'Infraestrutura da fase 1 e das expansões', intro:'Informe valores totais das suas cotações.',
  fields:[
   {id:'infra_ess',label:'Infraestrutura essencial (antes da primeira unidade)',type:'list',required:true,preset:['Acesso e estrada','Energia elétrica','Água','Tratamento de esgoto','Projetos, licenças e taxas','Terraplanagem'],namePlaceholder:'Item',valuePlaceholder:'R$ total'},
   {id:'infra_exp',label:'Infraestrutura adicional em cada fase de expansão',type:'money',required:true,allowUnknown:true,help:'Extensão de redes, caminhos e ligações até as novas unidades, por fase.'}
  ]},
 {kind:'feedback', title:'O peso da infraestrutura',
  metrics:function(s,c){return [{label:'Infraestrutura essencial',value:F.brl(c.infraEss),tag:'calculado'},{label:'Por unidade da visão final',value:F.brl(c.infraEss/c.uFinal),tag:'calculado'},{label:'Infra por expansão',value:F.brl(c.infraExp),tag:s.unknown('infra_exp')?'hipotese':'informado'}];},
  feedback:function(s,c){var o=[];
   if(c.infraItens<3) o.push({lv:'warn',t:'Apenas '+F.num(c.infraItens)+' item(ns) de infraestrutura essencial com valor. Confira acesso, energia, água, esgoto e licenças.'});
   else o.push({lv:'ok',t:F.num(c.infraItens)+' itens de infraestrutura essencial orçados ('+F.brl(c.infraEss)+').'});
   if(!c.temEsgoto) o.push({lv:'warn',t:'Não há valor para tratamento de esgoto. É um item que costuma ser exigido desde a primeira unidade: consulte um profissional habilitado.'});
   if(s.unknown('infra_exp')) o.push({lv:'warn',t:'Infraestrutura de expansão não informada: o plano usa R$ 0 por fase. As fases seguintes podem ficar mais caras do que o simulado.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Pedir que as redes de energia e água sejam dimensionadas para a visão final'},{id:'a2_2',text:'Consultar profissional sobre solução de esgoto ampliável'},{id:'a2_3',text:'Orçar a extensão de redes para cada fase de expansão'}]}
]},
/* 3 */
{title:'Primeira etapa', screens:[
 {kind:'learn', title:'A menor etapa que opera bem',
  body:'<p>A primeira etapa deve ser a <b>menor configuração capaz de entregar uma boa experiência</b> e gerar caixa. Pequena demais, não paga os custos fixos; grande demais, consome todo o capital e não deixa reserva.</p><p>O teste é simples: com o seu capital disponível, você consegue pagar a infraestrutura essencial e as unidades da fase 1 <b>e ainda manter uma reserva</b>? Se faltar dinheiro, o plano mostra quanto precisaria vir de outra fonte (sócio, parceria, financiamento), o que deve ser estruturado com advogado e contador.</p>',
  example:'Exemplo ilustrativo: capital de R$ 260.000 e fase 1 de R$ 245.000. Sobram R$ 15.000, que ajudam a formar o caixa da próxima fase.'},
 {kind:'compare', title:'Primeira etapa frágil × primeira etapa sólida',
  cols:[{h:'Frágil',type:'bad',items:['Uma unidade sem padrão de qualidade','Todo o capital gasto na obra','Sem enxoval de reserva nem fotos','Unidade que não poderá ser repetida']},
        {h:'Sólida',type:'good',items:['Unidades com o padrão final do projeto','Reserva mantida após a obra','Pronta para gerar avaliações boas desde o início','Modelo replicável nas próximas fases']}]},
 {kind:'form', title:'Sua primeira etapa',
  fields:[
   {id:'unid_f1',label:'Unidades na fase 1',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)',validate:function(v,s){var f=s.n('unid_final');return (ZA.isNum(f)&&v>f)?'A fase 1 não pode ter mais unidades que a visão final.':'';}},
   {id:'custo_unid',label:'Custo por unidade (construção + mobiliário)',type:'money',required:true,min:1},
   {id:'capital',label:'Capital disponível para começar',type:'money',required:true}
  ]},
 {kind:'feedback', title:'A primeira etapa cabe no seu capital?',
  metrics:function(s,c){return [{label:'Custo da fase 1',value:F.brl(c.custoF1),tag:'calculado'},{label:'Custo por unidade na fase 1',value:F.brl(c.custoF1/c.u1),tag:'calculado'},{label:c.falta>0?'Falta para a fase 1':'Sobra após a fase 1',value:F.brl(c.falta>0?c.falta:c.sobra),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.falta>0) o.push({lv:'bad',t:'O capital disponível não cobre a fase 1: faltam <b>'+F.brl(c.falta)+'</b>. Opções: reduzir unidades da fase 1, rever padrão ou buscar uma fonte complementar (estruturada com advogado e contador). A simulação seguinte considera, como hipótese, que essa diferença foi coberta.'});
   else if(c.sobra<c.custoF1*0.05) o.push({lv:'warn',t:'O capital cobre a fase 1, mas a sobra ('+F.brl(c.sobra)+') é pequena. Um imprevisto na obra pode faltar.'});
   else o.push({lv:'ok',t:'O capital cobre a fase 1 e sobram '+F.brl(c.sobra)+'.'});
   o.push({lv:'info',t:'Fazer tudo de uma vez custaria cerca de '+F.brl(c.custoTotal)+'. A fase 1 representa '+F.pct(c.custoF1/c.custoTotal*100,0)+' desse valor.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Definir a configuração mínima da fase 1 com o padrão final'},{id:'a3_2',text:'Manter uma reserva após a obra da fase 1'},{id:'a3_3',text:'Se faltar capital, listar fontes complementares e conversar com advogado e contador'}]}
]},
/* 4 */
{title:'Custos', screens:[
 {kind:'learn', title:'Quanto cada fase gera por mês',
  body:'<p>O motor do plano por etapas é o <b>resultado mensal</b> da operação. Ele é calculado para cada número de unidades em operação:</p><div class="za-card"><b>Resultado = diárias vendidas × diária × (1 − deduções) − diárias vendidas × custo variável − custo fixo</b><br>Diárias vendidas = unidades × 30 × ocupação.</div><p>O custo fixo cresce quando novas unidades entram (mais limpeza, manutenção, energia mínima). Por isso você informa também o <b>custo fixo adicional por unidade</b> nas expansões.</p>',
  example:'Exemplo ilustrativo: 2 unidades, 40% de ocupação = 24 diárias no mês. A R$ 350 com 18% de deduções: R$ 6.888. Menos R$ 1.200 de custo variável e R$ 3.000 de fixo: resultado de R$ 2.688 por mês.'},
 {kind:'compare', title:'Resultado inflado × resultado realista',
  cols:[{h:'Inflado',type:'bad',items:['Ocupação de alta temporada o ano todo','Sem comissão e imposto','Custo fixo igual com 2 ou 6 unidades']},
        {h:'Realista',type:'good',items:['Ocupação média anual','Deduções sobre a receita','Custo fixo que cresce com a operação']}]},
 {kind:'form', title:'Receita e custos da operação',
  fields:[
   {id:'diaria',label:'Diária média do ano',type:'money',required:true,min:1},
   {id:'ocupacao',label:'Ocupação média anual esperada',type:'percent',required:true,min:1},
   {id:'cf_mes',label:'Custo fixo mensal com a fase 1',type:'money',required:true},
   {id:'cv_noite',label:'Custo variável por diária vendida',type:'money',required:true},
   {id:'deducoes',label:'Deduções (comissões, impostos, taxas)',type:'percent',required:true,max:60},
   {id:'cf_add',label:'Custo fixo mensal adicional por unidade nova',type:'money',required:true,allowUnknown:true}
  ]},
 {kind:'feedback', title:'Geração de caixa da fase 1',
  metrics:function(s,c){return [{label:'Resultado mensal (fase 1)',value:F.brl(c.resF1),tag:'calculado'},{label:'Diárias vendidas/mês',value:F.num(c.u1*30*c.occ,1),tag:'calculado'},{label:'Ocupação de equilíbrio (fase 1)',value:c.occBE==null?'inalcançável':F.pct(c.occBE*100,0),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.resF1<=0) o.push({lv:'bad',t:'Com estas premissas, a fase 1 não gera caixa ('+F.brl(c.resF1)+' por mês). Ela não conseguirá ajudar a financiar as próximas fases. Reveja tamanho da fase 1, diária ou custo fixo.'});
   else o.push({lv:'ok',t:'A fase 1 gera cerca de '+F.brl(c.resF1)+' por mês com estas premissas.'});
   if(c.occBE!=null&&c.occBE<=1&&c.occBE>c.occ*0.8) o.push({lv:'warn',t:'A ocupação de equilíbrio ('+F.pct(c.occBE*100,0)+') está perto da ocupação esperada. Pouca folga para meses fracos.'});
   if(s.unknown('cf_add')) o.push({lv:'warn',t:'Custo fixo adicional por unidade não informado: usamos R$ 0. O resultado das fases seguintes pode estar superestimado.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Validar a diária com pesquisa de concorrentes comparáveis'},{id:'a4_2',text:'Detalhar o custo fixo mensal da fase 1'},{id:'a4_3',text:'Estimar quanto o custo fixo cresce a cada unidade nova'}]}
]},
/* 5 */
{title:'Cronograma', screens:[
 {kind:'learn', title:'Tempo de obra, reinvestimento e aportes',
  body:'<p>O cronograma depende de três escolhas:</p><ul><li><b>Prazo de obra:</b> quantos meses a fase 1 e cada expansão levam até receber hóspedes (inclua o tempo de licenças).</li><li><b>Reinvestimento:</b> que parte do resultado mensal vai para o caixa de expansão. O restante fica com você ou cobre outras necessidades.</li><li><b>Aporte mensal:</b> dinheiro novo que você consegue colocar todo mês (por exemplo, de outra renda).</li></ul><p>O Planejador simula mês a mês: soma o reinvestimento e o aporte ao caixa e, quando o caixa cobre o custo da próxima fase mais a reserva mínima, a fase começa.</p>',
  example:'Exemplo ilustrativo: resultado de R$ 2.688, reinvestimento de 80% (R$ 2.150) e aporte de R$ 1.000. O caixa de expansão cresce R$ 3.150 por mês.'},
 {kind:'compare', title:'Cronograma de desejo × cronograma de caixa',
  cols:[{h:'Desejo',type:'bad',items:['“Ano que vem faço mais duas”','Retirar todo o resultado','Ignorar o tempo de obra e licença']},
        {h:'Caixa',type:'good',items:['Fase seguinte quando o caixa permite','Percentual de reinvestimento definido','Prazo de obra e licença no cronograma']}]},
 {kind:'form', title:'Seu cronograma',
  fields:[
   {id:'meses_f1',label:'Meses até a fase 1 operar (licenças + obra)',type:'number',required:true,min:1,max:36,step:1,unit:'meses'},
   {id:'meses_fase',label:'Meses de obra de cada expansão',type:'number',required:true,min:1,max:36,step:1,unit:'meses'},
   {id:'reinvest',label:'Parte do resultado reinvestida na expansão',type:'percent',required:true},
   {id:'aporte',label:'Aporte mensal adicional',type:'money',required:true,allowUnknown:true}
  ]},
 {kind:'feedback', title:'Velocidade do seu caixa de expansão',
  metrics:function(s,c){return [{label:'Caixa de expansão/mês (fase 1)',value:F.brl(c.ritmoF1),tag:'calculado'},{label:'Início da operação',value:'mês '+(c.m1+1),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.ritmoF1<=0) o.push({lv:'bad',t:'O caixa de expansão não cresce: com o resultado e os aportes informados, as próximas fases não começam.'});
   else o.push({lv:'info',t:'Com a fase 1 operando, o caixa de expansão cresce cerca de '+F.brl(c.ritmoF1)+' por mês.'});
   if(s.n('reinvest',0)<50&&c.resF1>0) o.push({lv:'warn',t:'Você reinveste '+F.pct(s.n('reinvest'),0)+' do resultado. Isso é uma escolha legítima, mas alonga o prazo das próximas fases.'});
   if(s.unknown('aporte')) o.push({lv:'info',t:'Aporte mensal não informado: o plano considera R$ 0.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Incluir o prazo de licenças no cronograma da fase 1'},{id:'a5_2',text:'Abrir uma conta separada para o caixa de expansão'},{id:'a5_3',text:'Definir por escrito o percentual de reinvestimento'}]}
]},
/* 6 */
{title:'Expansão', screens:[
 {kind:'learn', title:'As fases seguintes e os gatilhos',
  body:'<p>Cada expansão tem um tamanho (unidades) e um custo (unidades × custo por unidade + infraestrutura de expansão). Além do caixa, é prudente usar <b>gatilhos</b> para liberar a próxima fase:</p><ul><li><b>Reserva mínima:</b> um valor que fica sempre no caixa, mesmo depois de pagar a expansão.</li><li><b>Ocupação mínima:</b> só expandir se a ocupação real sustentar o patamar definido. Se a ocupação premissa for menor que o gatilho, o plano não libera a expansão.</li></ul><p>O Planejador aceita até duas expansões (fases 2 e 3).</p>',
  example:'Exemplo ilustrativo: fase 2 de R$ 190.000 com reserva mínima de R$ 5.000. A obra só começa quando o caixa chega a R$ 195.000.'},
 {kind:'compare', title:'Expandir por empolgação × expandir por gatilho',
  cols:[{h:'Empolgação',type:'bad',items:['Expandir depois de um bom feriado','Zerar o caixa para começar a obra','Expandir com ocupação abaixo do esperado']},
        {h:'Gatilho',type:'good',items:['Caixa da fase + reserva mínima disponíveis','Ocupação dos últimos meses acima do gatilho','Avaliações boas e operação estável']}]},
 {kind:'form', title:'Suas fases de expansão',
  fields:[
   {id:'unid_f2',label:'Unidades na fase 2',type:'number',required:true,min:0,max:200,step:1,unit:'unidade(s)',validate:function(v,s){var f=s.n('unid_final'),a=s.n('unid_f1',0);return (ZA.isNum(f)&&a+v>f)?'Fases 1 e 2 somam mais que a visão final.':'';}},
   {id:'unid_f3',label:'Unidades na fase 3',type:'number',required:true,min:0,max:200,step:1,unit:'unidade(s)',validate:function(v,s){var f=s.n('unid_final'),a=s.n('unid_f1',0)+s.n('unid_f2',0);return (ZA.isNum(f)&&a+v>f)?'As três fases somam mais que a visão final.':'';}},
   {id:'reserva_min',label:'Reserva mínima que deve ficar no caixa',type:'money',required:true},
   {id:'gatilho',label:'Ocupação mínima para liberar uma expansão',type:'percent',required:true,allowUnknown:true}
  ]},
 {kind:'feedback', title:'O desenho das suas fases',
  metrics:function(s,c){return c.base.fases.map(function(f,i){return {label:'Fase '+(i+2)+' · '+F.num(f.u)+' un.',value:F.brl(f.custo),tag:'calculado'};});},
  feedback:function(s,c){var o=[],tot=c.u1+c.u2+c.u3;
   if(tot<c.uFinal) o.push({lv:'warn',t:'As três fases somam '+F.num(tot)+' unidades, menos que as '+F.num(c.uFinal)+' da visão final. As unidades restantes ficam fora desta simulação.'});
   if(!c.base.fases.length) o.push({lv:'info',t:'Nenhuma expansão definida: o plano simula apenas a fase 1.'});
   if(c.gatilhoBloqueia) o.push({lv:'bad',t:'A ocupação esperada ('+F.pct(c.occ*100,0)+') está abaixo do gatilho de '+F.pct(s.n('gatilho'),0)+'. Pelas suas regras, nenhuma expansão seria liberada.'});
   if(s.n('reserva_min',0)===0) o.push({lv:'warn',t:'Reserva mínima zero: cada expansão poderia zerar o caixa. Defina um valor de segurança.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Escrever os gatilhos de expansão (caixa, reserva e ocupação)'},{id:'a6_2',text:'Acompanhar a ocupação real mês a mês para comparar com o gatilho'},{id:'a6_3',text:'Atualizar as cotações das fases seguintes antes de iniciar cada obra'}]}
]},
/* 7 */
{title:'Plano de implantação', screens:[
 {kind:'learn', title:'O cronograma completo e os cenários',
  body:'<p>Com todas as premissas, o Planejador simula 120 meses e responde: <b>em que mês cada fase começa, em que mês passa a operar e quanto gera</b>. Também mostra se a visão final cabe no prazo que você deseja.</p><p>Como nenhuma premissa é certa, o plano é testado em três cenários:</p><ul><li><b>Conservador:</b> custos de obra maiores e ocupação menor.</li><li><b>Intermediário:</b> as premissas que você informou.</li><li><b>Otimista:</b> ocupação maior, custos iguais.</li></ul><p>Se o plano só funciona no otimista, é sinal de que as fases estão grandes demais ou de que a primeira etapa precisa gerar mais caixa.</p>',
  example:'Exemplo ilustrativo: no intermediário, a fase 2 começa no mês 62; no conservador, só depois do mês 100. A diferença mostra o quanto o plano depende da ocupação.'},
 {kind:'compare', title:'Plano rígido × plano por etapas vivo',
  cols:[{h:'Rígido',type:'bad',items:['Datas fixas, independentemente do caixa','Ignorar o que acontece na operação','Um único cenário']},
        {h:'Vivo',type:'good',items:['Datas dependem dos gatilhos','Revisão a cada 6 meses com números reais','Três cenários para decidir com prudência']}]},
 {kind:'form', title:'Variações para os cenários',
  fields:[
   {id:'var_custo',label:'Aumento de custo de obra no cenário conservador',type:'percent',required:true,max:60},
   {id:'var_ocup',label:'Variação de ocupação nos cenários',type:'number',required:true,min:0,max:50,step:1,unit:'p.p.'}
  ]},
 {kind:'feedback', title:'Seu plano nos três cenários',
  metrics:function(s,c){return c.cen.map(function(x){return {label:x.nome+' · visão alcançada',value:x.mesFinal==null?'não em 10 anos':'mês '+x.mesFinal,tag:'calculado'};});},
  feedback:function(s,c){var o=[],b=c.base,meta=s.n('prazo_visao',10)*12;
   if(b.mesFinal==null) o.push({lv:'bad',t:'No cenário intermediário, a visão simulada ('+F.num(c.uSim)+' unidades) não é alcançada em 10 anos. Considere fases menores, maior reinvestimento, aportes ou parceria.'});
   else if(b.mesFinal>meta) o.push({lv:'warn',t:'A visão simulada fica pronta no mês '+b.mesFinal+', depois do prazo desejado de '+F.num(meta)+' meses.'});
   else o.push({lv:'ok',t:'No cenário intermediário, a visão simulada fica pronta no mês '+b.mesFinal+', dentro do prazo desejado.'});
   if(c.cen[0].mesFinal==null&&b.mesFinal!=null) o.push({lv:'warn',t:'No cenário conservador a visão não é alcançada em 10 anos. O plano é sensível a custo e ocupação.'});
   if(b.caixaMin<0) o.push({lv:'bad',t:'Em algum mês o caixa fica negativo ('+F.brl(b.caixaMin)+'): a operação precisaria de dinheiro extra.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Revisar o plano a cada 6 meses com os números reais da operação'},{id:'a7_2',text:'Apresentar o plano por etapas a um possível sócio ou parceiro, com os três cenários'},{id:'a7_3',text:'Validar com arquiteto e prefeitura a aprovação do projeto em fases'}]}
]}
],

compute:function(s){
 var c={};
 c.uFinal=Math.max(1,s.n('unid_final',1));
 var ir=rowsOf(s,'infra_ess'); c.infraEss=ZA.listSum(ir); c.infraItens=ir.length;
 c.temEsgoto=ir.some(function(r){return /esgoto|fossa/i.test(r.name||'');});
 c.infraExp=s.n('infra_exp',0)||0;
 c.u1=Math.max(1,s.n('unid_f1',1)); c.u2=s.n('unid_f2',0)||0; c.u3=s.n('unid_f3',0)||0; c.uSim=c.u1+c.u2+c.u3;
 c.cu=s.n('custo_unid',0); c.capital=s.n('capital',0);
 c.d=s.n('diaria',0); c.occ=s.n('ocupacao',0)/100; c.cf=s.n('cf_mes',0); c.cv=s.n('cv_noite',0); c.ded=s.n('deducoes',0)/100; c.cfAdd=s.n('cf_add',0)||0;
 c.m1=Math.max(1,s.n('meses_f1',1)); c.mf=Math.max(1,s.n('meses_fase',1)); c.reinv=s.n('reinvest',0)/100; c.aporte=s.n('aporte',0)||0;
 c.reserva=s.n('reserva_min',0); c.gatilho=s.has('gatilho')?s.n('gatilho')/100:null;
 c.custoF1=c.infraEss+c.u1*c.cu;
 c.falta=Math.max(0,c.custoF1-c.capital); c.sobra=Math.max(0,c.capital-c.custoF1);
 var nf=(c.u2>0?1:0)+(c.u3>0?1:0);
 c.custoTotal=c.custoF1+(c.u2+c.u3)*c.cu+nf*c.infraExp;
 function resMes(n,occ){var nv=n*30*occ;return nv*c.d*(1-c.ded)-nv*c.cv-(c.cf+c.cfAdd*(n-c.u1));}
 c.resF1=resMes(c.u1,c.occ);
 var contrib=c.d*(1-c.ded)-c.cv; c.occBE=(contrib>0)?c.cf/(c.u1*30*contrib):null;
 c.ritmoF1=(c.resF1>0?c.resF1*c.reinv:c.resF1)+c.aporte;
 function sim(occ,fc){
  occ=ZA.clamp(occ,0,1);
  var cu=c.cu*fc, f1=c.infraEss*fc+c.u1*cu, caixa=Math.max(0,c.capital-f1), r={falta:Math.max(0,f1-c.capital),custoF1:f1};
  var fases=[]; if(c.u2>0) fases.push({u:c.u2,custo:c.u2*cu+c.infraExp*fc,inicio:null,fim:null,opera:null}); if(c.u3>0) fases.push({u:c.u3,custo:c.u3*cu+c.infraExp*fc,inicio:null,fim:null,opera:null});
  var bloq=(c.gatilho!=null&&occ<c.gatilho), idx=0, building=false, cmin=caixa, gerado=0;
  for(var m=1;m<=HM;m++){
   var n=m>c.m1?c.u1:0; fases.forEach(function(f){if(f.opera!=null&&m>=f.opera)n+=f.u;});
   var res=n>0?resMes(n,occ):0; if(n>0) gerado+=res;
   caixa+=(res>0?res*c.reinv:res)+c.aporte;
   if(caixa<cmin) cmin=caixa;
   if(!building&&idx<fases.length&&!bloq&&m>c.m1&&caixa-c.reserva>=fases[idx].custo){caixa-=fases[idx].custo;fases[idx].inicio=m;fases[idx].fim=m+c.mf;building=true;}
   if(building&&m===fases[idx].fim){building=false;fases[idx].opera=m+1;idx++;}
  }
  r.fases=fases; r.caixaFinal=caixa; r.caixaMin=cmin; r.gerado=gerado; r.bloq=bloq;
  r.mesFinal=fases.length?fases[fases.length-1].opera:c.m1+1;
  if(r.mesFinal!=null&&r.mesFinal>HM) r.mesFinal=null;
  r.res=[resMes(c.u1,occ)]; var acc=c.u1; fases.forEach(function(f){acc+=f.u;r.res.push(resMes(acc,occ));});
  return r;
 }
 c.base=sim(c.occ,1);
 c.gatilhoBloqueia=c.base.bloq;
 var vc=s.n('var_custo',0)/100, vo=s.n('var_ocup',0)/100;
 c.cen=[['Conservador',sim(c.occ-vo,1+vc),'Custo de obra +'+F.pct(vc*100,0)+', ocupação −'+F.num(vo*100)+' p.p.'],['Intermediário',c.base,'Premissas informadas'],['Otimista',sim(c.occ+vo,1),'Ocupação +'+F.num(vo*100)+' p.p.']].map(function(x){return {nome:x[0],premissa:x[2],mesFinal:x[1].mesFinal,f2:x[1].fases[0]?x[1].fases[0].inicio:null,f3:x[1].fases[1]?x[1].fases[1].inicio:null,resFinal:x[1].res[x[1].res.length-1],falta:x[1].falta,caixaMin:x[1].caixaMin};});
 var f=c.base.fases;
 c.fase2Inicio=f[0]?f[0].inicio:null; c.fase2Opera=f[0]?f[0].opera:null;
 c.fase3Inicio=f[1]?f[1].inicio:null; c.fase3Opera=f[1]?f[1].opera:null;
 c.mesFinal=c.base.mesFinal;
 c.resFinal=c.base.res[c.base.res.length-1];
 return c;
},

metrics:function(s,c){return [
 {label:'Custo da fase 1',value:F.brl(c.custoF1),tag:'calculado'},
 {label:'Capital disponível',value:F.brl(c.capital),tag:'informado'},
 {label:c.falta>0?'Falta para a fase 1':'Sobra após a fase 1',value:F.brl(c.falta>0?c.falta:c.sobra),tag:'calculado'},
 {label:'Resultado mensal da fase 1',value:F.brl(c.resF1),tag:'estimativa'},
 {label:'Início da fase 2',value:c.base.fases[0]?mes(c.fase2Inicio):'sem fase 2',tag:'calculado'},
 {label:'Início da fase 3',value:c.base.fases[1]?mes(c.fase3Inicio):'sem fase 3',tag:'calculado'},
 {label:'Visão simulada ('+F.num(c.uSim)+' un.) operando',value:mes(c.mesFinal),tag:'calculado'},
 {label:'Investimento total das fases',value:F.brl(c.custoTotal),tag:'calculado'}
];},

priorities:function(s,c){var L=[],b=c.base;
 if(c.falta>0) L.push({title:'Cobrir a diferença de '+F.brl(c.falta)+' da fase 1 ou reduzir a primeira etapa',why:'O capital disponível não paga a fase 1.',score:10});
 if(c.resF1<=0) L.push({title:'Redesenhar a fase 1 para gerar caixa',why:'Com as premissas atuais, a primeira etapa não gera resultado positivo.',score:10});
 if(c.gatilhoBloqueia) L.push({title:'Rever o gatilho de ocupação ou a ocupação esperada',why:'Pelas regras definidas, nenhuma expansão seria liberada.',score:8});
 if(s.t('tem_projeto')==='nao') L.push({title:'Fazer o estudo de implantação da visão final com profissional',why:'Sem ele, a fase 1 pode ficar no lugar errado ou com redes insuficientes.',score:9});
 if(b.fases.length&&b.mesFinal==null) L.push({title:'Encurtar o caminho até a visão final',why:'No cenário intermediário ela não é alcançada em 10 anos. Avalie fases menores, mais reinvestimento ou parceria.',score:8});
 else if(b.mesFinal!=null&&b.mesFinal>s.n('prazo_visao',10)*12) L.push({title:'Ajustar o prazo da visão final ou acelerar o caixa',why:'O plano simulado termina depois do prazo desejado.',score:6});
 if(c.cen[0].mesFinal==null&&b.mesFinal!=null) L.push({title:'Proteger o plano contra o cenário conservador',why:'Com custo maior e ocupação menor, a visão não é alcançada em 10 anos.',score:6});
 if(!c.temEsgoto) L.push({title:'Orçar a solução de esgoto da fase 1',why:'Item essencial sem valor no plano.',score:7});
 if(c.falta===0&&c.sobra<c.custoF1*0.05) L.push({title:'Criar reserva para imprevistos da obra da fase 1',why:'A sobra de capital após a fase 1 é pequena.',score:6});
 if(s.n('reserva_min',0)===0) L.push({title:'Definir uma reserva mínima no caixa',why:'Sem ela, cada expansão pode zerar o caixa.',score:5});
 if(s.unknown('cf_add')) L.push({title:'Estimar o custo fixo adicional de cada nova unidade',why:'Considerado R$ 0 no plano.',score:5});
 if(s.unknown('infra_exp')) L.push({title:'Orçar a infraestrutura de cada expansão',why:'Considerada R$ 0 no plano.',score:5});
 if(c.uSim<c.uFinal) L.push({title:'Planejar as unidades restantes da visão final',why:F.num(c.uFinal-c.uSim)+' unidade(s) ficaram fora das fases simuladas.',score:3});
 L.push({title:'Revisar o plano a cada 6 meses com números reais',why:'As datas das fases dependem do caixa efetivamente gerado.',score:4});
 return L;},

report:function(s,c){
 var inf=tag('informado'), cal=tag('calculado'), hip=tag('hipotese','hipótese');
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Visão final',F.num(c.uFinal)+' unidades em '+F.num(s.n('prazo_visao'))+' anos',inf],
  ['Fases simuladas',F.num(c.u1)+' + '+F.num(c.u2)+' + '+F.num(c.u3)+' unidades',inf],
  ['Infraestrutura essencial',F.brl(c.infraEss),cal],
  ['Infraestrutura por expansão',F.brl(c.infraExp),s.unknown('infra_exp')?hip+' R$ 0':inf],
  ['Custo por unidade',F.brl(c.cu),inf],
  ['Capital disponível',F.brl(c.capital),inf],
  ['Diária / ocupação',F.brl(c.d)+' / '+F.pct(c.occ*100,0),inf],
  ['Custo fixo mensal (fase 1) / adicional por unidade',F.brl(c.cf)+' / '+F.brl(c.cfAdd),s.unknown('cf_add')?hip+' adicional R$ 0':inf],
  ['Custo variável por diária / deduções',F.brl(c.cv)+' / '+F.pct(c.ded*100,0),inf],
  ['Prazo fase 1 / prazo de cada expansão',F.num(c.m1)+' / '+F.num(c.mf)+' meses',inf],
  ['Reinvestimento / aporte mensal',F.pct(c.reinv*100,0)+' / '+F.brl(c.aporte),s.unknown('aporte')?hip+' aporte R$ 0':inf],
  ['Reserva mínima / gatilho de ocupação',F.brl(c.reserva)+' / '+(c.gatilho==null?'—':F.pct(c.gatilho*100,0)),s.unknown('gatilho')?hip+' sem gatilho':inf],
  ['Mês com 30 noites; horizonte de 120 meses','—',tag('recomendacao','premissa do método')]],[1]);
 var b=c.base, acc=c.u1;
 var linhas=[['Fase 1',F.num(c.u1),F.brl(b.custoF1),'mês 1','mês '+(c.m1+1),F.brl(b.res[0])]];
 b.fases.forEach(function(f,i){acc+=f.u;linhas.push(['Fase '+(i+2),F.num(f.u)+' (total '+F.num(acc)+')',F.brl(f.custo),mes(f.inicio),mes(f.opera),F.brl(b.res[i+1])]);});
 var crono=ZA.table(['Fase','Unidades','Custo','Início da obra','Começa a operar','Resultado mensal com a fase'],linhas,[2,5]);
 var C=c.cen, row=function(l,f){return [l].concat(C.map(f));};
 var cen=ZA.table(['Indicador'].concat(C.map(function(x){return x.nome;})),[
  row('Falta na fase 1',function(x){return F.brl(x.falta);}),
  row('Início da fase 2',function(x){return b.fases[0]?mes(x.f2):'—';}),
  row('Início da fase 3',function(x){return b.fases[1]?mes(x.f3):'—';}),
  row('Visão simulada operando',function(x){return mes(x.mesFinal);}),
  row('Resultado mensal com todas as fases',function(x){return F.brl(x.resFinal);})],[1,2,3]);
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro por etapas</b><ol>'+
  '<li><b>Agora (30 dias):</b> '+(top[0]?esc(top[0].title):'Confirmar o projeto da visão final')+'; '+(top[1]?esc(top[1].title).toLowerCase():'confirmar cotações da fase 1')+'.</li>'+
  '<li><b>Antes da obra:</b> '+(top[2]?esc(top[2].title):'Aprovar projeto e licenças da fase 1')+'; licenças e projeto da fase 1 confirmados com profissional e prefeitura.</li>'+
  '<li><b>Meses 1 a '+c.m1+':</b> obra da fase 1 ('+F.num(c.u1)+' unidades, '+F.brl(c.custoF1)+').</li>'+
  '<li><b>A partir do mês '+(c.m1+1)+':</b> operar, medir ocupação e resultado reais e alimentar o caixa de expansão.</li>'+
  b.fases.map(function(f,i){return '<li><b>Fase '+(i+2)+':</b> '+(f.inicio?'gatilho previsto no mês '+f.inicio+', operação no mês '+f.opera:'não alcançada em 10 anos com estas premissas')+'.</li>';}).join('')+
  '</ol><p class="za-small">Revise o plano a cada 6 meses com os números reais: as datas acima mudam conforme o caixa efetivamente gerado.</p></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Cronograma de fases (cenário intermediário)',html:crono+(c.falta>0?'<p class="za-missing">Hipótese: a falta de '+F.brl(c.falta)+' na fase 1 foi considerada coberta por outra fonte. Isso precisa ser resolvido antes da obra.</p>':'')+'<p class="za-small">Comparação: fazer todas as fases de uma vez exigiria cerca de '+F.brl(c.custoTotal)+'.</p>'},
  {title:'Três cenários',html:'<ul class="za-small">'+C.map(function(x){return '<li><b>'+x.nome+':</b> '+x.premissa+'</li>';}).join('')+'</ul>'+cen+'<p class="za-small">Simulações a partir das variações que você definiu. Não são previsões de prazo nem de resultado.</p>'}
 ],plan:plan};
}
});
})();
