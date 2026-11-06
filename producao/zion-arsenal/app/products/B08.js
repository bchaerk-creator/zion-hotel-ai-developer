/* ZAR-B08 · Como Calcular o Retorno de um Projeto Turístico? · Simulador de Viabilidade Econômica */
(function(){
var F=ZA.fmt, esc=ZA.esc, H=10;
function tag(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';}
function anos(v){if(!ZA.isNum(v))return 'não ocorre em 10 anos';return F.num(v,1)+' anos';}
/* VPL de uma série de fluxos (índice 0 = ano 0) */
function npv(r,fl){var t,v=0;for(t=0;t<fl.length;t++)v+=fl[t]/Math.pow(1+r,t);return v;}
/* TIR por bissecção: procura a primeira troca de sinal do VPL em r ∈ (−99%, 1000%]; null se não existir */
function irr(fl){
 var pos=fl.some(function(x){return x>0;}), neg=fl.some(function(x){return x<0;});
 if(!pos||!neg) return null;
 var grid=[],r; for(r=-0.99;r<1;r+=0.01) grid.push(r); for(r=1;r<=10;r+=0.25) grid.push(r);
 var a=null,b=null,fa,fb,i;
 for(i=0;i<grid.length-1;i++){fa=npv(grid[i],fl);fb=npv(grid[i+1],fl);
  if(!ZA.isNum(fa)||!ZA.isNum(fb)) continue;
  if(fa===0) return grid[i];
  if(fa*fb<0){a=grid[i];b=grid[i+1];break;}}
 if(a==null) return null;
 for(i=0;i<200;i++){var m=(a+b)/2,fm=npv(m,fl); if(!ZA.isNum(fm)) return null; if(fm===0) return m; if(fa*fm<0){b=m;}else{a=m;fa=fm;} if(b-a<1e-12) break;}
 return (a+b)/2;
}
function payback(I,arr){var cum=-I,t;for(t=0;t<arr.length;t++){var prev=cum;cum+=arr[t];if(cum>=0&&arr[t]>0)return t+(-prev)/arr[t];}return null;}
function signChanges(fl){var n=0,last=0;fl.forEach(function(x){var sg=x>0?1:x<0?-1:0;if(sg!==0){if(last!==0&&sg!==last)n++;last=sg;}});return n;}

ZA.register({
id:'B08', code:'ZAR-B08', collection:'Terrenos',
title:'Como Calcular o Retorno de um Projeto Turístico?',
subtitle:'Simule Receita, ROI e Payback',
tool:'Simulador de Viabilidade Econômica',
deliverable:'Estudo Econômico Preliminar',
nameField:'nome', propertyField:'propriedade',
disclaimer:'Este estudo é uma simulação preliminar construída apenas com as premissas que você informou. Ocupação, diária, custos e taxa de desconto são hipóteses, não previsões: o resultado real pode ser diferente. ROI, payback, VPL e TIR aqui calculados não constituem promessa de retorno nem recomendação de investimento. Para decisões de investimento, sociedade, tributação e financiamento, consulte contador, advogado e demais profissionais habilitados.',

intro:[
 {kind:'mirror', title:'Se um investidor perguntar quanto custa, quanto rende e quando retorna, você sabe responder?',
  lead:'Você tem o terreno, uma ideia de quantas unidades construir e uma diária em mente. Mas, quando alguém pergunta “em quanto tempo o dinheiro volta?”, a resposta sai no improviso.',
  body:'<div class="za-card"><p>Talvez você esteja aqui por um destes motivos:</p><ul><li>“Fiz a conta diária × 30 dias e o número ficou bonito demais.”</li><li>“Não sei como considerar que o primeiro ano terá menos ocupação.”</li><li>“Já ouvi falar de VPL e TIR, mas não sei calcular nem explicar.”</li><li>“Quero conversar com um sócio, mas não tenho números organizados.”</li></ul></div>'},
 {kind:'collapse', title:'Uma projeção baseada apenas na diária média pode esconder custos e riscos importantes.',
  lead:'Diária × noites × 12 meses não é retorno. Entre a receita e o dinheiro que sobra existem comissões, impostos, custos fixos, custos por hóspede, reposição de itens e, principalmente, o tempo que um empreendimento novo leva para encher.',
  body:'<div class="za-card"><p>Um estudo econômico preliminar responde a quatro perguntas, com premissas declaradas:</p><ol><li><b>Quanto entra e quanto sai</b> em cada um dos próximos 10 anos (fluxo de caixa)?</li><li><b>Quando o investimento é recuperado</b> (payback simples e descontado)?</li><li><b>Quanto o projeto vale hoje</b>, comparado com a rentabilidade mínima que você exige (VPL)?</li><li><b>Qual é a taxa de retorno implícita</b> do projeto (TIR)?</li></ol><p>E faz isso em três cenários, porque ninguém conhece o futuro.</p></div>'},
 {kind:'start', title:'Vamos simular o retorno do seu projeto',
  lead:'Em 7 pilares, você informa investimento, capacidade, preço, ocupação e custos, e o Simulador monta o fluxo de caixa de 10 anos com os indicadores que um sócio ou investidor costuma perguntar.',
  body:'<p>Use os melhores números que você tiver: orçamento de implantação (o B06 ajuda), pesquisa de diárias de concorrentes e estimativa de custos de operação. Onde houver a opção “não sei”, o relatório indicará a hipótese usada.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Fernanda'},
   {id:'propriedade',label:'Nome do projeto',type:'text',required:true,placeholder:'Ex.: Cabanas Rio Claro'},
   {id:'municipio',label:'Município / destino',type:'text',required:true,placeholder:'Ex.: Monte Verde (MG)'},
   {id:'modelo',label:'Modelo de hospedagem',type:'select',required:true,options:[{v:'cabana',l:'Cabanas'},{v:'chale',l:'Chalés'},{v:'glamping',l:'Glamping'},{v:'pousada',l:'Pequena pousada'},{v:'misto',l:'Misto'},{v:'outro',l:'Outro'}]}
  ]}
],

pillars:[
/* 1 */
{title:'Investimento', screens:[
 {kind:'learn', title:'O ponto de partida: quanto sai do bolso antes de entrar o primeiro real',
  body:'<p>O <b>investimento inicial</b> é tudo o que precisa ser pago antes de a hospedagem começar a operar: projetos e licenças, infraestrutura, construção, mobiliário, pré-operação e capital de giro. No fluxo de caixa, ele aparece no <b>ano 0</b> como valor negativo.</p><p>Quanto mais confiável o investimento, mais confiável todo o estudo. Um orçamento feito item por item, com cotações, vale mais do que um número redondo estimado. Se o investimento estiver subestimado, todos os indicadores ficam otimistas demais.</p>',
  example:'Exemplo ilustrativo: um projeto orçado em R$ 600.000 que, na obra, custa R$ 690.000 (15% a mais) precisa de mais anos de resultado para devolver o capital. Por isso o cenário conservador deste Simulador aumenta o investimento.'},
 {kind:'compare', title:'Investimento frágil × investimento defensável',
  cols:[{h:'Frágil',type:'bad',items:['Número redondo “de cabeça”','Só o preço das unidades','Sem capital de giro','Sem margem para imprevistos']},
        {h:'Defensável',type:'good',items:['Orçamento por blocos, com cotações','Infraestrutura, projetos e mobiliário incluídos','Capital de giro para os primeiros meses','Contingência declarada']}]},
 {kind:'form', title:'Seu investimento inicial',
  fields:[
   {id:'invest',label:'Investimento inicial total (ano 0)',type:'money',required:true,min:1,help:'Inclua implantação, contingência e capital de giro.'},
   {id:'invest_base',label:'De onde vem esse número?',type:'radio',required:true,options:[{v:'orcamento',l:'Orçamento detalhado por itens, com cotações'},{v:'parcial',l:'Algumas cotações e algumas estimativas'},{v:'estimativa',l:'Estimativa geral'}]},
   {id:'invest_origem',label:'Como o investimento seria financiado?',type:'radio',required:true,options:[{v:'proprio',l:'Recursos próprios'},{v:'socio',l:'Sócio ou investidor'},{v:'financiamento',l:'Financiamento'},{v:'misto',l:'Combinação'}]}
  ]},
 {kind:'feedback', title:'A base do seu estudo',
  metrics:function(s,c){return [{label:'Investimento inicial',value:F.brl(c.I),tag:'informado'},{label:'Investimento por unidade',value:F.brl(c.I/c.U),tag:'calculado'}];},
  feedback:function(s,c){var o=[],b=s.t('invest_base');
   if(b==='orcamento') o.push({lv:'ok',t:'Investimento baseado em orçamento detalhado: boa base para o estudo.'});
   if(b==='parcial') o.push({lv:'warn',t:'Parte do investimento é estimativa. Dê atenção especial ao cenário conservador, que aumenta o investimento.'});
   if(b==='estimativa') o.push({lv:'bad',t:'O investimento é uma estimativa geral. Todos os indicadores dependem dele: faça um orçamento item por item (o B06 ajuda) antes de apresentar o estudo a alguém.'});
   if(s.t('invest_origem')==='financiamento'||s.t('invest_origem')==='misto') o.push({lv:'info',t:'Este Simulador analisa o projeto sem juros de financiamento (fluxo do projeto). Parcelas e juros mudam o fluxo do proprietário: simule com o seu contador ou com a instituição financeira.'});
   if(s.t('invest_origem')==='socio') o.push({lv:'info',t:'Com sócio ou investidor, o retorno do projeto ainda precisará ser dividido conforme o acordo. Estruture isso com advogado e contador.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Revisar o investimento com um orçamento por blocos e cotações'},{id:'a1_2',text:'Confirmar se o capital de giro está incluído no investimento'},{id:'a1_3',text:'Guardar as cotações que sustentam o número para mostrar a sócios'}]}
]},
/* 2 */
{title:'Capacidade de hospedagem', screens:[
 {kind:'learn', title:'Capacidade: o teto da sua receita',
  body:'<p>A <b>capacidade anual</b> é o número máximo de diárias que o empreendimento pode vender num ano:</p><div class="za-card"><b>Capacidade = unidades × noites de operação no ano</b></div><p>Noites de operação são as noites em que a hospedagem fica aberta, já descontando fechamentos para manutenção, uso próprio ou temporadas sem funcionamento. Nenhuma projeção pode vender mais do que esse teto. Toda receita do estudo nasce de <b>capacidade × ocupação × diária</b>.</p>',
  example:'Exemplo ilustrativo: 3 cabanas abertas 365 noites por ano = 1.095 diárias disponíveis. Com 50% de ocupação, são 547,5 diárias vendidas no ano.'},
 {kind:'compare', title:'Capacidade imaginada × capacidade real',
  cols:[{h:'Imaginada',type:'bad',items:['Contar 365 noites sem nenhum fechamento','Contar unidades que ainda não têm orçamento','Somar leitos em vez de unidades vendáveis']},
        {h:'Real',type:'good',items:['Descontar manutenção e uso próprio','Contar só unidades do orçamento','Usar a unidade que é efetivamente vendida (cabana, quarto, tenda)']}]},
 {kind:'form', title:'Sua capacidade',
  fields:[
   {id:'unidades',label:'Unidades de hospedagem',type:'number',required:true,min:1,max:300,step:1,unit:'unidade(s)'},
   {id:'noites_ano',label:'Noites de operação por ano',type:'number',required:true,min:1,max:366,step:1,unit:'noites',help:'365 menos fechamentos previstos.'},
   {id:'hospedes_unid',label:'Hóspedes por unidade',type:'number',required:true,min:1,max:30,step:1,unit:'pessoas'}
  ]},
 {kind:'feedback', title:'O teto do seu projeto',
  metrics:function(s,c){return [{label:'Diárias disponíveis por ano',value:F.num(c.cap),tag:'calculado'},{label:'Capacidade de hóspedes simultâneos',value:F.num(c.U*s.n('hospedes_unid',1)),tag:'calculado'}];},
  feedback:function(s,c){var o=[],n=s.n('noites_ano',365);
   if(n>=365) o.push({lv:'warn',t:'Você considerou operação em todas as noites do ano. Na prática, manutenção e imprevistos costumam fechar unidades em alguns dias: avalie descontar.'});
   else o.push({lv:'ok',t:'Você descontou '+F.num(365-n)+' noite(s) de fechamento por ano. Premissa mais realista.'});
   o.push({lv:'info',t:'Teto anual: '+F.num(c.cap)+' diárias. Nenhum cenário poderá vender mais do que isso.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Definir o calendário de fechamento para manutenção'},{id:'a2_2',text:'Confirmar que todas as unidades do estudo estão no orçamento'},{id:'a2_3',text:'Registrar a capacidade anual no resumo do projeto'}]}
]},
/* 3 */
{title:'Preço', screens:[
 {kind:'learn', title:'Diária média, reajuste e receitas extras',
  body:'<p>A <b>diária média</b> do estudo é a média do ano inteiro, considerando alta e baixa temporada, fins de semana e descontos. Ela deve vir de pesquisa: anúncios parecidos no destino, nas mesmas datas, com estrutura comparável.</p><p>O <b>reajuste anual</b> aplica-se à diária e aos custos ao longo dos 10 anos. Usar o mesmo percentual nos dois evita que o estudo fique otimista por reajustar só a receita. Se você preferir analisar em valores de hoje, use 0%.</p><p><b>Receitas extras</b> (café da manhã, experiências, passeios) entram como percentual da receita de hospedagem. Sem dado, use 0%.</p>',
  example:'Exemplo ilustrativo: diária média de R$ 550 com 4% de reajuste ao ano vira R$ 572 no ano 2 e cerca de R$ 783 no ano 10. Os custos crescem no mesmo ritmo.'},
 {kind:'compare', title:'Diária de vitrine × diária média do ano',
  cols:[{h:'Vitrine',type:'bad',items:['Usar o preço do feriado como média','Copiar o concorrente mais caro','Reajustar a receita e não os custos']},
        {h:'Média do ano',type:'good',items:['Média ponderada entre alta e baixa temporada','Referência em concorrentes comparáveis','Mesmo reajuste para receita e custos']}]},
 {kind:'form', title:'Seu preço',
  fields:[
   {id:'diaria',label:'Diária média do ano (por unidade)',type:'money',required:true,min:1},
   {id:'diaria_fonte',label:'Como você chegou a essa diária?',type:'radio',required:true,options:[{v:'pesquisa',l:'Pesquisa de concorrentes comparáveis'},{v:'calculo',l:'Cálculo de custos e margem (ex.: A02)'},{v:'estimativa',l:'Estimativa própria'}]},
   {id:'reajuste',label:'Reajuste anual de diária e custos',type:'percent',required:true,max:30},
   {id:'extras',label:'Receitas extras, em % da receita de hospedagem',type:'percent',required:true,max:100,allowUnknown:true}
  ]},
 {kind:'feedback', title:'Seu preço no estudo',
  metrics:function(s,c){return [{label:'Diária ano 1',value:F.brl(c.d),tag:'informado'},{label:'Diária ano 10',value:F.brl(c.base.diaria10),tag:'calculado'},{label:'Receitas extras',value:F.pct(c.x*100,0),tag:s.unknown('extras')?'hipotese':'informado'}];},
  feedback:function(s,c){var o=[];
   if(s.t('diaria_fonte')==='estimativa') o.push({lv:'warn',t:'A diária é uma estimativa própria. Pesquise 5 concorrentes comparáveis: a diária é uma das premissas que mais mexem no resultado.'});
   else o.push({lv:'ok',t:'Diária com base em '+(s.t('diaria_fonte')==='pesquisa'?'pesquisa de concorrentes':'cálculo de custos')+'. Registre a fonte no estudo.'});
   if(s.unknown('extras')) o.push({lv:'info',t:'Receitas extras não informadas: o estudo usa 0%. Isso deixa a projeção mais conservadora.'});
   if(c.x>0.3) o.push({lv:'warn',t:'Receitas extras de '+F.pct(c.x*100,0)+' da hospedagem é uma premissa alta. Confirme se há estrutura e demanda para isso.'});
   if(c.g>0.08) o.push({lv:'warn',t:'Reajuste de '+F.pct(c.g*100,0)+' ao ano aplicado por 10 anos. Lembre que a taxa de desconto (Pilar 6) deve ser coerente: se o fluxo tem reajuste, a taxa também deve incluir inflação.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Pesquisar diárias de 5 concorrentes comparáveis em alta e baixa temporada'},{id:'a3_2',text:'Calcular a diária média ponderada do ano'},{id:'a3_3',text:'Listar as receitas extras possíveis e testar a demanda'}]}
]},
/* 4 */
{title:'Ocupação', screens:[
 {kind:'learn', title:'Rampa de ocupação: ninguém começa cheio',
  body:'<p>Um empreendimento novo precisa de tempo para ganhar avaliações, aparecer nas buscas e ser indicado. Por isso o Simulador usa uma <b>rampa de ocupação</b>:</p><ul><li><b>Ocupação do ano 1:</b> o ponto de partida.</li><li><b>Ocupação estabilizada:</b> o patamar que você considera sustentável depois que o negócio amadurece.</li><li><b>Anos de rampa:</b> quantos anos a ocupação leva para sair do ano 1 e chegar ao patamar estabilizado, subindo em partes iguais.</li></ul><p>A ocupação deve ser uma hipótese prudente. Se você não tiver dados do destino, prefira valores conservadores e teste no cenário pessimista.</p>',
  example:'Exemplo ilustrativo: 30% no ano 1, 50% estabilizada e 2 anos de rampa. Ano 1: 30%. Ano 2: 40%. Do ano 3 em diante: 50%.'},
 {kind:'compare', title:'Ocupação de sonho × ocupação de estudo',
  cols:[{h:'De sonho',type:'bad',items:['Casa cheia desde o primeiro mês','Usar a ocupação de feriado como média','Mesma ocupação em todos os anos']},
        {h:'De estudo',type:'good',items:['Rampa de crescimento nos primeiros anos','Média anual, com baixa temporada','Teste com ocupação menor no cenário conservador']}]},
 {kind:'form', title:'Sua rampa de ocupação',
  fields:[
   {id:'ocup1',label:'Ocupação no ano 1',type:'percent',required:true},
   {id:'ocup_est',label:'Ocupação estabilizada',type:'percent',required:true,min:1},
   {id:'rampa',label:'Anos de rampa até estabilizar',type:'number',required:true,min:1,max:9,step:1,unit:'anos'},
   {id:'ocup_fonte',label:'De onde vem a ocupação estabilizada?',type:'radio',required:true,options:[{v:'dados',l:'Dados de hospedagens do destino que eu conheço'},{v:'estimativa',l:'Estimativa própria'}]}
  ]},
 {kind:'feedback', title:'Sua ocupação ano a ano',
  metrics:function(s,c){return [{label:'Ano 1',value:F.pct(c.base.occ[0]*100,0),tag:'informado'},{label:'Ano 2',value:F.pct(c.base.occ[1]*100,0),tag:'calculado'},{label:'Estabilizada (a partir do ano '+c.anoEstab+')',value:F.pct(c.oe*100,0),tag:'informado'},{label:'Ocupação de equilíbrio (ano 1)',value:c.occBE==null?'inalcançável':F.pct(c.occBE*100,0),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.o1>c.oe) o.push({lv:'warn',t:'A ocupação do ano 1 está acima da estabilizada. Isso significa que a ocupação cai ao longo do tempo. Confira se é intencional.'});
   if(c.oe>0.75) o.push({lv:'warn',t:'Ocupação estabilizada de '+F.pct(c.oe*100,0)+' é uma premissa exigente para média anual. Teste o resultado com o cenário conservador.'});
   if(s.t('ocup_fonte')==='estimativa') o.push({lv:'warn',t:'A ocupação estabilizada é estimativa própria. Converse com operadores do destino ou consulte fontes oficiais de turismo do seu município antes de apresentar o estudo.'});
   if(c.occBE==null) o.push({lv:'bad',t:'Com a diária e os custos por noite informados, cada diária vendida não cobre o próprio custo variável. Nenhuma ocupação fecha a conta.'});
   else if(c.occBE>1) o.push({lv:'bad',t:'Seria preciso mais de 100% de ocupação para cobrir os custos do ano 1. Revise diária ou custos fixos.'});
   else if(c.occBE>c.o1) o.push({lv:'warn',t:'No ano 1 o projeto precisa de '+F.pct(c.occBE*100,0)+' de ocupação para empatar, acima dos '+F.pct(c.o1*100,0)+' previstos: o primeiro ano deve fechar no negativo. Planeje caixa para isso.'});
   else o.push({lv:'ok',t:'A ocupação de equilíbrio ('+F.pct(c.occBE*100,0)+') está abaixo da ocupação do ano 1.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Conversar com 3 operadores do destino sobre ocupação média anual'},{id:'a4_2',text:'Planejar caixa para os anos de rampa'},{id:'a4_3',text:'Definir ações de lançamento para acelerar a rampa (fotos, avaliações, parcerias)'}]}
]},
/* 5 */
{title:'Custos', screens:[
 {kind:'learn', title:'Custos: o que separa receita de resultado',
  body:'<p>O Simulador usa quatro grupos de custo:</p><ul><li><b>Custo fixo anual:</b> existe com ou sem hóspede (equipe fixa, manutenção, energia mínima, internet, seguro, contador, software).</li><li><b>Custo variável por diária vendida:</b> limpeza, lavanderia, amenities, energia e água extras.</li><li><b>Deduções sobre a receita:</b> comissões de plataformas, taxa de pagamento e impostos.</li><li><b>Reserva de reposição:</b> percentual da receita guardado para trocar enxoval, móveis e equipamentos ao longo dos anos.</li></ul><p>O resultado de cada ano é: <b>receita − deduções − reserva − custo variável − custo fixo</b>. Este estudo não inclui juros de financiamento nem imposto de renda sobre o lucro, que dependem da estrutura escolhida: confirme com seu contador.</p>',
  example:'Exemplo ilustrativo: receita de R$ 300.000, deduções e reserva de 23% (R$ 69.000), custo variável de R$ 33.000 e fixo de R$ 80.000. Resultado do ano: R$ 118.000.'},
 {kind:'compare', title:'Custos esquecidos × custos completos',
  cols:[{h:'Esquecidos',type:'bad',items:['Comissão das plataformas','Imposto sobre a receita','Troca de enxoval e colchões','Manutenção de estruturas expostas ao tempo']},
        {h:'Completos',type:'good',items:['Deduções percentuais separadas','Custo por diária vendida','Reserva anual de reposição','Fixo anual com equipe e manutenção']}]},
 {kind:'form', title:'Seus custos de operação (valores do ano 1)',
  fields:[
   {id:'cf_ano',label:'Custo fixo anual',type:'money',required:true},
   {id:'cv_noite',label:'Custo variável por diária vendida',type:'money',required:true},
   {id:'comissao',label:'Comissões e taxas de pagamento',type:'percent',required:true,max:40},
   {id:'imposto',label:'Impostos sobre a receita',type:'percent',required:true,max:30,allowUnknown:true,help:'Confirme a alíquota com seu contador.'},
   {id:'reserva',label:'Reserva de reposição',type:'percent',required:true,max:20,allowUnknown:true}
  ]},
 {kind:'feedback', title:'Seus custos no ano estabilizado',
  metrics:function(s,c){var y=c.base.anos[c.anoEstab-1];return [{label:'Deduções + reserva',value:F.pct(c.ded*100,1),tag:'calculado'},{label:'Receita (ano '+c.anoEstab+')',value:F.brl(y.receita),tag:'calculado'},{label:'Resultado (ano '+c.anoEstab+')',value:F.brl(y.fc),tag:'calculado'},{label:'Margem (ano '+c.anoEstab+')',value:y.receita>0?F.pct(y.fc/y.receita*100,0):'—',tag:'calculado'}];},
  feedback:function(s,c){var o=[],y=c.base.anos[c.anoEstab-1];
   if(s.unknown('imposto')) o.push({lv:'warn',t:'Imposto sobre a receita não informado: o estudo usou 0%. O resultado fica otimista. Confirme a alíquota com um contador.'});
   if(s.unknown('reserva')) o.push({lv:'warn',t:'Reserva de reposição não informada: usamos 0%. Sem ela, a troca de enxoval e móveis sai do resultado de algum ano.'});
   if(y.fc<0) o.push({lv:'bad',t:'Mesmo no ano estabilizado o resultado é negativo ('+F.brl(y.fc)+'). Com estas premissas, a operação não se paga.'});
   else if(y.receita>0&&y.fc/y.receita<0.15) o.push({lv:'warn',t:'Margem de '+F.pct(y.fc/y.receita*100,0)+' no ano estabilizado: pouco espaço para imprevistos.'});
   else o.push({lv:'ok',t:'No ano estabilizado sobram '+F.brl(y.fc)+' ('+F.pct(y.receita>0?y.fc/y.receita*100:0,0)+' da receita) antes de juros e imposto de renda.'});
   if(c.cfPeso>0.5) o.push({lv:'warn',t:'O custo fixo consome '+F.pct(c.cfPeso*100,0)+' da receita estabilizada. Projetos com fixo alto sofrem mais com meses fracos.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Confirmar a alíquota de imposto com um contador'},{id:'a5_2',text:'Detalhar o custo fixo anual item por item'},{id:'a5_3',text:'Definir a reserva anual de reposição'}]}
]},
/* 6 */
{title:'Fluxo de caixa e retorno', screens:[
 {kind:'learn', title:'Os indicadores que o investidor pergunta',
  body:'<ul><li><b>Fluxo de caixa:</b> investimento no ano 0 (negativo) e resultado de cada ano de 1 a 10.</li><li><b>ROI em 10 anos:</b> (soma dos resultados − investimento) ÷ investimento.</li><li><b>Payback simples:</b> em quantos anos a soma dos resultados devolve o investimento.</li><li><b>Taxa de desconto:</b> a rentabilidade mínima que <b>você</b> exige para colocar dinheiro neste projeto em vez de outra alternativa. É uma escolha sua.</li><li><b>Payback descontado:</b> o mesmo que o simples, mas com cada resultado trazido a valor de hoje pela taxa de desconto.</li><li><b>VPL (valor presente líquido):</b> soma dos resultados trazidos a valor de hoje, menos o investimento. VPL positivo indica que, <b>com estas premissas</b>, o projeto supera a taxa exigida.</li><li><b>TIR (taxa interna de retorno):</b> a taxa que zera o VPL. Quando os fluxos nunca devolvem o investimento, a TIR não existe e aparece “—”.</li></ul>',
  example:'Exemplo ilustrativo: R$ 100.000 investidos e R$ 30.000 por ano durante 5 anos. Payback simples: 3,3 anos. A 10% ao ano, o VPL é cerca de R$ 13.700 e a TIR fica perto de 15% ao ano.'},
 {kind:'compare', title:'Payback simples × payback descontado',
  cols:[{h:'Payback simples',items:['Soma os resultados como se R$ 1 de daqui a 8 anos valesse R$ 1 hoje','Fácil de explicar','Tende a parecer mais curto']},
        {h:'Payback descontado',items:['Considera que dinheiro no futuro vale menos','Usa a sua taxa de desconto','Mais exigente e mais realista para comparar investimentos']}]},
 {kind:'form', title:'Taxa de desconto e valor residual',
  fields:[
   {id:'taxa',label:'Taxa de desconto (rentabilidade mínima que você exige ao ano)',type:'percent',required:true,max:50,help:'Por exemplo: o rendimento que você teria em outra aplicação, mais um adicional pelo risco do projeto. A escolha é sua.'},
   {id:'residual',label:'Valor residual do empreendimento no ano 10, em % do investimento',type:'percent',required:false,max:100,help:'Opcional. Deixe em branco para não considerar (mais conservador). Entra no VPL, na TIR e no ROI, não no payback.'}
  ]},
 {kind:'feedback', title:'Retorno no cenário intermediário',
  metrics:function(s,c){var b=c.base;return [{label:'VPL',value:F.brl(b.vpl),tag:'calculado'},{label:'TIR',value:b.tir==null?'—':F.pct(b.tir*100,1)+' a.a.',tag:'calculado'},{label:'Payback simples',value:anos(b.paybackS),tag:'calculado'},{label:'Payback descontado',value:anos(b.paybackD),tag:'calculado'},{label:'ROI em 10 anos',value:F.pct(b.roi10*100,0),tag:'calculado'}];},
  feedback:function(s,c){var o=[],b=c.base;
   if(b.vpl>=0) o.push({lv:'ok',t:'VPL positivo de '+F.brl(b.vpl)+': com estas premissas, o projeto supera a taxa de '+F.pct(c.i*100,1)+' que você exige. Não é garantia: é o resultado das hipóteses informadas.'});
   else o.push({lv:'bad',t:'VPL negativo de '+F.brl(b.vpl)+': com estas premissas, o projeto não alcança a taxa de '+F.pct(c.i*100,1)+' que você exige.'});
   if(b.tir==null) o.push({lv:'warn',t:'A TIR não existe para estes fluxos (o investimento não é recuperado ou não há troca de sinal). Ela aparece como “—”.'});
   if(b.tirMultipla) o.push({lv:'warn',t:'O fluxo muda de sinal mais de uma vez; pode haver mais de uma TIR. Use o VPL como indicador principal.'});
   if(b.paybackS==null) o.push({lv:'bad',t:'O investimento não é recuperado dentro de 10 anos.'});
   else if(b.paybackD==null) o.push({lv:'warn',t:'O payback simples ocorre em '+anos(b.paybackS)+', mas, descontando a '+F.pct(c.i*100,1)+', o investimento não é recuperado em 10 anos.'});
   if(c.residual>0) o.push({lv:'info',t:'O estudo inclui valor residual de '+F.pct(c.residual*100,0)+' do investimento no ano 10 ('+F.brl(c.I*c.residual)+'). Sem ele, o VPL seria '+F.brl(b.vplSemResidual)+'.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Definir e justificar por escrito a taxa de desconto escolhida'},{id:'a6_2',text:'Revisar com um contador o efeito de impostos sobre o lucro'},{id:'a6_3',text:'Preparar a explicação de VPL, TIR e payback em linguagem simples para sócios'}]}
]},
/* 7 */
{title:'Cenários e análise', screens:[
 {kind:'learn', title:'Três cenários: porque o futuro não é um número só',
  body:'<p>O cenário <b>Intermediário</b> usa exatamente as premissas que você informou. Os outros dois variam as premissas mais sensíveis:</p><ul><li><b>Conservador:</b> ocupação menor em todos os anos, diária menor e investimento maior (estouro de orçamento).</li><li><b>Otimista:</b> ocupação maior e diária maior, com o mesmo investimento.</li></ul><p>As variações são definidas por você. Se o projeto só fica de pé no cenário otimista, o risco é alto. Se resiste ao conservador, o estudo é mais robusto. Nenhum dos três é previsão.</p>',
  example:'Exemplo ilustrativo: variação de 10 pontos de ocupação, 10% de diária e 15% de investimento. Uma ocupação estabilizada de 50% vira 40% no conservador e 60% no otimista.'},
 {kind:'compare', title:'Estudo de vendedor × estudo de investidor',
  cols:[{h:'Estudo de vendedor',type:'bad',items:['Um único cenário, o melhor','Premissas escondidas','Indicadores sem explicação','Promessa de retorno']},
        {h:'Estudo de investidor',type:'good',items:['Três cenários com variações declaradas','Premissas em tabela, com origem','VPL, TIR e paybacks explicados','Riscos e próximos passos']}]},
 {kind:'form', title:'Defina as variações dos cenários',
  fields:[
   {id:'var_ocup',label:'Variação de ocupação (pontos percentuais)',type:'number',required:true,min:0,max:50,step:1,unit:'p.p.'},
   {id:'var_diaria',label:'Variação de diária',type:'percent',required:true,max:50},
   {id:'var_invest',label:'Aumento do investimento no cenário conservador',type:'percent',required:true,max:60}
  ]},
 {kind:'feedback', title:'Seu projeto nos três cenários',
  metrics:function(s,c){return c.cen.map(function(x){return {label:x.nome+' · VPL',value:F.brl(x.vpl),tag:'calculado'};});},
  feedback:function(s,c){var o=[],k=c.cen[0],t=c.cen[2];
   if(k.vpl>=0) o.push({lv:'ok',t:'Mesmo no cenário conservador o VPL é positivo ('+F.brl(k.vpl)+'). O estudo resiste às variações que você definiu.'});
   else if(c.base.vpl>=0) o.push({lv:'warn',t:'O VPL é positivo no intermediário, mas negativo no conservador ('+F.brl(k.vpl)+'). O resultado depende de as premissas se confirmarem.'});
   else if(t.vpl>=0) o.push({lv:'bad',t:'O projeto só tem VPL positivo no cenário otimista. Com estas premissas, o risco é alto: reveja investimento, custos ou modelo.'});
   else o.push({lv:'bad',t:'O VPL é negativo nos três cenários. Com estas premissas, o projeto não alcança a taxa exigida.'});
   if(s.n('var_ocup',0)===0&&s.n('var_diaria',0)===0&&s.n('var_invest',0)===0) o.push({lv:'warn',t:'As variações estão zeradas: os três cenários ficam iguais. Defina variações para testar o risco.'});
   o.push({lv:'info',t:'Payback simples: '+anos(k.paybackS)+' (conservador), '+anos(c.base.paybackS)+' (intermediário), '+anos(t.paybackS)+' (otimista).'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Revisar as premissas que mais mexem no resultado (ocupação, diária, investimento)'},{id:'a7_2',text:'Apresentar sempre os três cenários, nunca apenas o otimista'},{id:'a7_3',text:'Validar o estudo com um contador antes de mostrar a sócios ou investidores'}]}
]}
],

compute:function(s){
 var c={};
 c.I=s.n('invest',0); c.U=Math.max(1,s.n('unidades',1)); c.N=s.n('noites_ano',365); c.cap=c.U*c.N;
 c.d=s.n('diaria',0); c.g=s.n('reajuste',0)/100; c.x=s.n('extras',0)/100;
 c.o1=s.n('ocup1',0)/100; c.oe=s.n('ocup_est',50)/100; c.R=Math.max(1,s.n('rampa',1)); c.anoEstab=Math.min(H,c.R+1);
 c.cf=s.n('cf_ano',0); c.cv=s.n('cv_noite',0);
 c.com=s.n('comissao',0)/100; c.imp=s.n('imposto',0)/100; c.rr=s.n('reserva',0)/100; c.ded=c.com+c.imp+c.rr;
 c.i=s.n('taxa',0)/100; c.residual=s.n('residual',0)/100;
 var vo=s.n('var_ocup',0)/100, vd=s.n('var_diaria',0)/100, vi=s.n('var_invest',0)/100;
 function model(dOcc,fD,fI){
  var m={anos:[],occ:[],fl:[]}, I=c.I*fI; m.I=I; m.fl.push(-I);
  for(var t=1;t<=H;t++){
   var occ=c.o1+(c.oe-c.o1)*Math.min(1,(t-1)/c.R); occ=ZA.clamp(occ+dOcc,0,1); m.occ.push(occ);
   var k=Math.pow(1+c.g,t-1), diaria=c.d*fD*k, noites=c.cap*occ;
   var rh=noites*diaria, rec=rh*(1+c.x), ded=rec*c.ded, cv=noites*c.cv*k, cf=c.cf*k;
   var fc=rec-ded-cv-cf;
   m.anos.push({t:t,occ:occ,noites:noites,diaria:diaria,receita:rec,deducoes:ded,cv:cv,cf:cf,fc:fc});
   m.fl.push(fc);
  }
  m.diaria10=m.anos[H-1].diaria;
  var res=I*c.residual; m.res=res;
  var flR=m.fl.slice(); flR[H]+=res; m.flR=flR;
  var op=m.anos.map(function(a){return a.fc;});
  m.somaFc=op.reduce(function(a,b){return a+b;},0);
  m.roi10=I>0?(m.somaFc+res-I)/I:null;
  m.paybackS=payback(I,op);
  m.paybackD=payback(I,op.map(function(v,j){return v/Math.pow(1+c.i,j+1);}));
  m.vpl=npv(c.i,flR); m.vplSemResidual=npv(c.i,m.fl);
  m.tir=irr(flR); m.tirMultipla=signChanges(flR)>1;
  m.fcEstab=m.anos[c.anoEstab-1].fc; m.roiEstab=I>0?m.fcEstab/I:null;
  var acc=-I; m.acum=op.map(function(v){acc+=v;return acc;});
  return m;
 }
 c.base=model(0,1,1);
 c.cen=[{nome:'Conservador',m:model(-vo,1-vd,1+vi),p:'Ocupação −'+F.num(vo*100)+' p.p., diária −'+F.pct(vd*100,0)+', investimento +'+F.pct(vi*100,0)},
        {nome:'Intermediário',m:c.base,p:'Premissas informadas'},
        {nome:'Otimista',m:model(vo,1+vd,1),p:'Ocupação +'+F.num(vo*100)+' p.p., diária +'+F.pct(vd*100,0)}].map(function(x){var m=x.m;return {nome:x.nome,premissa:x.p,I:m.I,vpl:m.vpl,tir:m.tir,paybackS:m.paybackS,paybackD:m.paybackD,roi10:m.roi10,fcEstab:m.fcEstab,somaFc:m.somaFc};});
 // indicadores de atalho para o cenário intermediário
 c.vpl=c.base.vpl; c.tir=c.base.tir; c.paybackS=c.base.paybackS; c.paybackD=c.base.paybackD; c.roi10=c.base.roi10;
 c.fc1=c.base.anos[0].fc; c.fcEstab=c.base.fcEstab;
 var contrib=c.d*(1+c.x)*(1-c.ded)-c.cv;
 c.occBE=(contrib>0&&c.cap>0)?c.cf/(c.cap*contrib):null;
 var ye=c.base.anos[c.anoEstab-1]; c.cfPeso=ye.receita>0?ye.cf/ye.receita:0;
 return c;
},

metrics:function(s,c){var b=c.base;return [
 {label:'Investimento inicial',value:F.brl(c.I),tag:'informado'},
 {label:'Resultado no ano 1',value:F.brl(c.fc1),tag:'calculado'},
 {label:'Resultado no ano estabilizado',value:F.brl(c.fcEstab),tag:'calculado'},
 {label:'ROI em 10 anos',value:b.roi10==null?'—':F.pct(b.roi10*100,0),tag:'calculado'},
 {label:'Payback simples',value:anos(b.paybackS),tag:'calculado'},
 {label:'Payback descontado',value:anos(b.paybackD),tag:'calculado'},
 {label:'VPL a '+F.pct(c.i*100,1),value:F.brl(b.vpl),tag:'calculado'},
 {label:'TIR',value:b.tir==null?'—':F.pct(b.tir*100,1)+' a.a.',tag:'calculado'}
];},

priorities:function(s,c){var L=[],b=c.base,k=c.cen[0];
 if(b.vpl<0) L.push({title:'Rever o projeto: o VPL é negativo no cenário intermediário',why:'Com as premissas informadas, o projeto não alcança a taxa de desconto exigida.',score:10});
 if(c.occBE==null||c.occBE>1) L.push({title:'Reestruturar diária e custos: nenhuma ocupação cobre a operação',why:'A conta de cada diária ou do custo fixo não fecha.',score:10});
 if(b.vpl>=0&&k.vpl<0) L.push({title:'Reduzir a sensibilidade do projeto ao cenário conservador',why:'O VPL fica negativo com as variações que você definiu.',score:8});
 if(s.t('invest_base')==='estimativa') L.push({title:'Transformar o investimento em orçamento detalhado',why:'Todos os indicadores dependem desse número.',score:9});
 if(s.t('ocup_fonte')==='estimativa') L.push({title:'Validar a ocupação estabilizada com operadores ou fontes oficiais do destino',why:'É a premissa que mais mexe na receita.',score:8});
 if(s.t('diaria_fonte')==='estimativa') L.push({title:'Pesquisar diárias de concorrentes comparáveis',why:'A diária do estudo é estimativa própria.',score:7});
 if(s.unknown('imposto')) L.push({title:'Confirmar com contador o imposto sobre a receita',why:'O estudo usou 0%, o que deixa o resultado otimista.',score:7});
 if(c.occBE!=null&&c.occBE<=1&&c.occBE>c.o1) L.push({title:'Planejar caixa para cobrir o prejuízo do ano 1',why:'A ocupação prevista no ano 1 está abaixo do equilíbrio ('+F.pct(c.occBE*100,0)+').',score:7});
 if(b.paybackS==null) L.push({title:'Buscar formas de reduzir o investimento ou implantar por etapas',why:'O investimento não volta em 10 anos.',score:8});
 if(s.unknown('reserva')) L.push({title:'Incluir reserva de reposição no estudo',why:'Sem ela, trocas de enxoval e móveis ficam fora da conta.',score:5});
 if(c.cfPeso>0.5) L.push({title:'Reduzir o custo fixo anual',why:'Ele consome '+F.pct(c.cfPeso*100,0)+' da receita estabilizada.',score:6});
 if(c.oe>0.75) L.push({title:'Testar o estudo com ocupação estabilizada menor',why:'Premissa de '+F.pct(c.oe*100,0)+' é exigente para média anual.',score:6});
 if(s.t('invest_origem')==='financiamento'||s.t('invest_origem')==='misto') L.push({title:'Simular parcelas e juros do financiamento com contador ou banco',why:'O estudo mostra o fluxo do projeto, sem juros.',score:5});
 L.push({title:'Validar o estudo com um contador antes de apresentá-lo',why:'Impostos sobre o lucro e estrutura societária não estão no cálculo.',score:4});
 return L;},

report:function(s,c){
 var inf=tag('informado'), cal=tag('calculado'), hip=tag('hipotese','hipótese');
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Investimento inicial',F.brl(c.I),s.t('invest_base')==='estimativa'?tag('estimativa'):inf],
  ['Unidades × noites de operação',F.num(c.U)+' × '+F.num(c.N)+' = '+F.num(c.cap)+' diárias/ano',cal],
  ['Diária média (ano 1)',F.brl(c.d),s.t('diaria_fonte')==='estimativa'?tag('estimativa'):inf],
  ['Reajuste anual (diária e custos)',F.pct(c.g*100,1),inf],
  ['Receitas extras',F.pct(c.x*100,0),s.unknown('extras')?hip+' 0%':inf],
  ['Ocupação ano 1 → estabilizada',F.pct(c.o1*100,0)+' → '+F.pct(c.oe*100,0)+' em '+F.num(c.R)+' ano(s)',s.t('ocup_fonte')==='estimativa'?tag('estimativa'):inf],
  ['Custo fixo anual (ano 1)',F.brl(c.cf),inf],
  ['Custo variável por diária (ano 1)',F.brl(c.cv),inf],
  ['Comissões / impostos / reserva',F.pct(c.com*100,1)+' / '+F.pct(c.imp*100,1)+' / '+F.pct(c.rr*100,1),(s.unknown('imposto')||s.unknown('reserva'))?hip+' 0% no que faltou':inf],
  ['Taxa de desconto',F.pct(c.i*100,1)+' a.a.',inf],
  ['Valor residual no ano 10',F.pct(c.residual*100,0)+' do investimento',inf],
  ['Horizonte','10 anos; sem juros de financiamento e sem imposto de renda',tag('recomendacao','premissa do método')]],[1]);
 var b=c.base;
 var fluxo=ZA.table(['Ano','Ocupação','Receita','Deduções e reserva','Custos (variáveis + fixos)','Resultado','Acumulado'],
  [['0','—','—','—','—',F.brl0(-b.I),F.brl0(-b.I)]].concat(b.anos.map(function(a,j){return [String(a.t),F.pct(a.occ*100,0),F.brl0(a.receita),F.brl0(a.deducoes),F.brl0(a.cv+a.cf),F.brl0(a.fc),F.brl0(b.acum[j])];})).concat(b.res>0?[['10 (residual)','','','','',F.brl0(b.res),'']]:[]),[1,2,3,4,5,6]);
 var ind=ZA.table(['Indicador','Valor','Como ler'],[
  ['ROI em 10 anos',b.roi10==null?'—':F.pct(b.roi10*100,1),'(soma dos resultados + residual − investimento) ÷ investimento'],
  ['Retorno anual no ano estabilizado',b.roiEstab==null?'—':F.pct(b.roiEstab*100,1),'resultado do ano '+c.anoEstab+' ÷ investimento'],
  ['Payback simples',anos(b.paybackS),'anos até a soma dos resultados igualar o investimento'],
  ['Payback descontado',anos(b.paybackD),'o mesmo, com resultados descontados a '+F.pct(c.i*100,1)],
  ['VPL',F.brl(b.vpl),'positivo = supera a taxa exigida, com estas premissas'],
  ['TIR',b.tir==null?'—':F.pct(b.tir*100,2)+' a.a.','taxa que zera o VPL; “—” quando não existe']],[1]);
 var C=c.cen, row=function(l,f){return [l].concat(C.map(f));};
 var cen=ZA.table(['Indicador'].concat(C.map(function(x){return x.nome;})),[
  row('Investimento',function(x){return F.brl0(x.I);}),
  row('Resultado no ano estabilizado',function(x){return F.brl0(x.fcEstab);}),
  row('ROI em 10 anos',function(x){return x.roi10==null?'—':F.pct(x.roi10*100,0);}),
  row('Payback simples',function(x){return anos(x.paybackS);}),
  row('Payback descontado',function(x){return anos(x.paybackD);}),
  row('VPL',function(x){return F.brl0(x.vpl);}),
  row('TIR',function(x){return x.tir==null?'—':F.pct(x.tir*100,1)+' a.a.';})],[1,2,3]);
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido de 30 dias</b><ol>'+
  '<li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Revisar as premissas de maior impacto')+'.</li>'+
  '<li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Validar ocupação e diária no destino')+'.</li>'+
  '<li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Revisar custos e impostos com contador')+'.</li>'+
  '<li><b>Semana 4:</b> refazer o Simulador com as premissas confirmadas e preparar a apresentação dos três cenários.</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Fluxo de caixa de 10 anos (cenário intermediário)',html:fluxo+'<p class="za-small">Valores nominais com reajuste de '+F.pct(c.g*100,1)+' ao ano (diária do ano 1: '+F.brl(c.d)+'; do ano 10: '+F.brl(b.diaria10)+'). Resultado = receita − deduções − reserva − custos variáveis − custos fixos.</p>'},
  {title:'Indicadores de retorno',html:ind},
  {title:'Três cenários',html:'<ul class="za-small">'+C.map(function(x){return '<li><b>'+x.nome+':</b> '+x.premissa+'</li>';}).join('')+'</ul>'+cen+'<p class="za-small">Cenários são simulações a partir das variações definidas por você. Não são previsões nem promessa de retorno.</p>'}
 ],plan:plan};
}
});
})();
