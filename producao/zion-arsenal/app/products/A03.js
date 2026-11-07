/* ZAR-A03 · Sua Hospedagem Fatura, mas Dá Lucro? · Calculadora de Custos e Rentabilidade */
(function(){
var F=ZA.fmt, esc=ZA.esc;
var TGL={hipotese:'hipótese',recomendacao:'recomendação'};
function tg(t,l){return '<span class="za-tag '+t+'">'+(l||TGL[t]||t)+'</span>';}
var DESP={energia:'Energia e aquecimento ligados sem hóspede',lavanderia:'Lavanderia cara ou sem controle de peças',reposicao:'Reposição de amenities sem controle de estoque',assinaturas:'Assinaturas e serviços pouco usados',comissao:'Quase tudo vendido por plataforma, sem reserva direta',limpeza:'Limpeza sem padrão de tempo e checklist',manutencao:'Consertos de emergência por falta de manutenção preventiva',quebras:'Quebras e extravios sem caução ou regra'};
/* DRE simplificada mensal */
function dre(p){
 var d={};
 d.recHosp=p.D*p.N; d.recLimp=p.R*p.TL; d.recExtras=p.EX; d.rb=d.recHosp+d.recLimp+d.recExtras;
 var baseHosp=d.recHosp+d.recLimp;
 d.comissoes=baseHosp*p.share*p.com; d.impostos=d.rb*p.imp; d.taxasPag=(baseHosp*(1-p.share)+p.EX)*p.tp;
 d.deducoes=d.comissoes+d.impostos+d.taxasPag; d.rl=d.rb-d.deducoes;
 d.cvReserva=p.R*(p.limp+p.amen); d.cvNoite=p.N*p.cons; d.cvExtras=p.EX*p.cex; d.cv=d.cvReserva+d.cvNoite+d.cvExtras;
 d.repos=d.rb*p.fundo; d.mc=d.rl-d.cv-d.repos; d.cf=p.CF; d.pl=p.PL;
 d.resOp=d.mc-d.cf; d.resFinal=d.resOp-d.pl;
 d.margemOp=d.rb>0?d.resOp/d.rb:null; d.margemFinal=d.rb>0?d.resFinal/d.rb:null;
 return d;
}

ZA.register({
id:'A03', code:'ZAR-A03', collection:'Hospedagem',
title:'Sua Hospedagem Fatura, mas Dá Lucro?',
subtitle:'Descubra Quanto Realmente Sobra',
tool:'Calculadora de Custos e Rentabilidade',
deliverable:'Demonstrativo Financeiro Simplificado',
nameField:'nome', propertyField:'propriedade',
disclaimer:'O demonstrativo é gerencial e simplificado, montado com os valores que você informou; não substitui a contabilidade nem a orientação de um contador sobre impostos. Cenários são simulações, não previsões: não há garantia de faturamento, lucro ou retorno.',

intro:[
 {kind:'mirror', title:'Seu calendário está cheio. Mas seu bolso também?',
  lead:'O mês foi movimentado, chegaram vários pagamentos da plataforma, e mesmo assim, quando você olha a conta, parece que quase nada ficou.',
  body:'<div class="za-card"><p>Algumas frases comuns de quem está nessa situação:</p><ul><li>“Faturei bem, mas não sei para onde foi o dinheiro.”</li><li>“Misturo a conta da hospedagem com a da casa.”</li><li>“Nunca coloquei no papel quanto gasto com lavanderia e reposição.”</li><li>“Trabalho todo dia na hospedagem e não tiro salário.”</li></ul></div>'},
 {kind:'collapse', title:'Faturamento não é lucro.',
  lead:'Uma hospedagem movimentada pode ter margens muito pequenas. Entre o que o hóspede paga e o que sobra existem comissões, impostos, limpeza, reposição, contas fixas e o seu próprio trabalho.',
  body:'<div class="za-card"><p>O Demonstrativo Financeiro Simplificado organiza o mês em degraus:</p><ol><li><b>Receita bruta</b>: tudo que o hóspede pagou;</li><li><b>Receita líquida</b>: depois de comissões, impostos e taxas;</li><li><b>Margem de contribuição</b>: depois dos custos de cada estadia;</li><li><b>Resultado operacional</b>: depois dos custos fixos;</li><li><b>Resultado final</b>: depois do seu pró-labore.</li></ol><p>Em cada degrau você vai ver quanto sai e por quê. Este produto olha o <b>resultado do mês e do ano</b>; a formação da diária é tema da mini mentoria A02.</p></div>'},
 {kind:'start', title:'Vamos montar o seu demonstrativo',
  lead:'Em 7 pilares você vai levantar receita, custos e taxas, calcular sua margem real, encontrar desperdícios e simular um plano de melhoria em três cenários.',
  body:'<p>Use um mês típico (nem o melhor nem o pior). Tenha à mão: extrato da plataforma, contas do mês, recibos de limpeza e lavanderia. O que não souber, marque “não sei”: o demonstrativo mostrará a premissa usada.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Juliana'},
   {id:'propriedade',label:'Nome da hospedagem',type:'text',required:true,placeholder:'Ex.: Cabanas do Vale'},
   {id:'tipo',label:'Tipo de hospedagem',type:'select',required:true,options:[{v:'airbnb',l:'Apartamento ou casa (Airbnb/temporada)'},{v:'cabana',l:'Cabana ou chalé'},{v:'glamping',l:'Glamping'},{v:'pousada',l:'Pequena pousada'},{v:'outro',l:'Outro'}]},
   {id:'destino',label:'Cidade / destino',type:'text',required:true,placeholder:'Ex.: Monte Verde (MG)'},
   {id:'unidades',label:'Quantas unidades você aluga?',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)'}
  ]}
],

pillars:[
/* 1 */
{title:'Receita real', screens:[
 {kind:'learn', title:'Receita bruta é tudo o que o hóspede pagou',
  body:'<p>O valor que cai na sua conta já vem descontado da comissão. Para enxergar o negócio, comece pelo valor <b>cheio</b>: diárias, taxa de limpeza cobrada e qualquer extra vendido (café, passeio, lenha, decoração especial). Essa é a <b>receita bruta</b>.</p><p>Use a receita do mês em que a estadia aconteceu, não do mês em que o dinheiro caiu (as plataformas costumam repassar depois do check-in). Assim, receita e custos do mesmo mês ficam lado a lado.</p>',
  example:'Exemplo ilustrativo: 14 noites a R$ 300 (R$ 4.200) + 5 reservas com taxa de limpeza de R$ 80 (R$ 400) + R$ 200 de extras = receita bruta de <b>R$ 4.800</b>. O depósito da plataforma será menor, porque a comissão já foi retirada.'},
 {kind:'compare', title:'O que conta como receita',
  cols:[{h:'Erro comum',type:'bad',items:['Considerar só o valor depositado','Esquecer a taxa de limpeza cobrada','Misturar extras com dinheiro pessoal','Somar o pagamento de uma reserva do mês que vem']},
        {h:'Forma correta',type:'good',items:['Partir do valor cheio pago pelo hóspede','Separar diária, limpeza e extras','Registrar extras numa linha própria','Usar o mês da estadia (competência)']}]},
 {kind:'form', title:'Sua receita no mês típico',
  fields:[
   {id:'diaria_media',label:'Diária média cobrada',type:'money',required:true,min:1},
   {id:'noites_vend',label:'Noites vendidas no mês (todas as unidades)',type:'number',required:true,min:0,max:6200,step:1,unit:'noites'},
   {id:'reservas_mes',label:'Número de reservas no mês',type:'number',required:true,min:0,step:1,allowUnknown:true,help:'Se não souber, o cálculo usa a hipótese de estadia média de 2 noites.'},
   {id:'taxa_limp_cobrada',label:'Taxa de limpeza cobrada do hóspede, por reserva',type:'money',required:true,help:'Coloque 0 se você não cobra separadamente.'},
   {id:'extras_mes',label:'Receitas extras no mês (café, passeios, kits, lenha…)',type:'money',required:true,help:'Coloque 0 se não vende extras.'}
  ]},
 {kind:'feedback', title:'Sua receita bruta',
  metrics:function(s,c){var d=c.d;return [{label:'Receita bruta mensal',value:F.brl(d.rb),tag:'calculado'},{label:'Hospedagem',value:F.brl(d.recHosp),tag:'calculado'},{label:'Taxa de limpeza',value:F.brl(d.recLimp),tag:c.R_hip?'estimativa':'calculado'},{label:'Extras',value:F.brl(d.recExtras),tag:'informado'}];},
  feedback:function(s,c){var o=[],d=c.d;
   if(c.R_hip) o.push({lv:'warn',t:'Sem o número de reservas, usamos <b>'+F.num(c.R,1)+' reservas</b> (hipótese de 2 noites por estadia). Confira no extrato: isso muda receita de limpeza e custos por reserva.'});
   if(d.rb>0&&d.recExtras===0) o.push({lv:'info',t:'Sua receita vem só de hospedagem e limpeza. Receitas extras podem melhorar a margem sem precisar de mais noites (tema da mini mentoria A08).'});
   if(d.rb>0) o.push({lv:'info',t:'A hospedagem responde por '+F.pct(d.recHosp/d.rb*100,0)+' da receita bruta. Anualizando o mês típico, a receita bruta seria de '+F.brl(d.rb*12)+'.'});
   if(d.rb===0) o.push({lv:'bad',t:'Receita zero no mês informado. O demonstrativo vai mostrar o tamanho do custo que precisa ser coberto.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Abrir uma conta bancária só para a hospedagem'},{id:'a1_2',text:'Registrar a receita de cada estadia no mês em que ela aconteceu'},{id:'a1_3',text:'Separar diária, limpeza e extras na planilha de controle'}]}
]},
/* 2 */
{title:'Custos fixos', screens:[
 {kind:'learn', title:'Custos fixos: o mês começa devendo',
  body:'<p>No demonstrativo, custos fixos são o que você paga mesmo que nenhum hóspede venha: financiamento ou aluguel, condomínio, IPTU, internet, funcionários fixos, contador, softwares, seguro e manutenção preventiva.</p><p>Contas anuais precisam ser <b>mensalizadas</b> (IPTU de R$ 1.200 = R$ 100 por mês). E o seu trabalho entra à parte, como <b>pró-labore</b>: sem ele, o “lucro” pode ser apenas o seu salário que não foi pago.</p>',
  example:'Exemplo ilustrativo: R$ 1.200 de financiamento + R$ 250 de condomínio + R$ 120 de internet + R$ 150 de energia fixa = R$ 1.720 por mês. Com pró-labore de R$ 500, o mês precisa gerar R$ 2.220 de margem antes de sobrar qualquer centavo.'},
 {kind:'compare', title:'Mensalizar × esquecer',
  cols:[{h:'Esquecido',type:'bad',items:['IPTU e seguro pagos uma vez por ano','Software anual pago no cartão','Seu tempo de trabalho','Parcela de móveis e eletrodomésticos']},
        {h:'Mensalizado',type:'good',items:['Valor anual ÷ 12 em cada mês','Assinaturas somadas numa linha','Pró-labore definido e registrado','Parcelas listadas até terminar']}]},
 {kind:'form', title:'Seus custos fixos mensais', intro:'Valores mensais da operação inteira. Deixe em branco o que não se aplica; adicione itens se precisar.',
  fields:[
   {id:'cf',label:'Custos fixos por mês',type:'list',required:true,preset:['Financiamento ou aluguel do imóvel','Condomínio / IPTU (mensalizado)','Internet e TV','Energia e água (parte fixa)','Funcionários fixos','Contador','Software / channel manager','Seguro','Manutenção preventiva'],namePlaceholder:'Descrição',valuePlaceholder:'R$ / mês'},
   {id:'prolabore',label:'Pró-labore mensal (o valor do seu trabalho)',type:'money',required:false,help:'Deixe em branco se não trabalha na operação.'}
  ]},
 {kind:'feedback', title:'Seu custo fixo',
  metrics:function(s,c){var d=c.d;return [{label:'Custos fixos mensais',value:F.brl(d.cf),tag:'calculado'},{label:'Peso na receita bruta',value:d.rb>0?F.pct(d.cf/d.rb*100):'—',tag:'calculado'},{label:'Pró-labore',value:F.brl(d.pl),tag:'informado'}];},
  feedback:function(s,c){var o=[],d=c.d;
   if(c.cfMaior) o.push({lv:'info',t:'Maior custo fixo: <b>'+esc(c.cfMaior.name)+'</b> ('+F.brl(c.cfMaior.value)+', '+F.pct(c.cfMaior.value/d.cf*100,0)+' do total).'});
   if(d.rb>0&&d.cf/d.rb>0.5) o.push({lv:'bad',t:'Os custos fixos consomem '+F.pct(d.cf/d.rb*100,0)+' da receita bruta. Sobra pouco espaço para comissões, custos variáveis e margem.'});
   else if(d.rb>0&&d.cf/d.rb>0.35) o.push({lv:'warn',t:'Custos fixos de '+F.pct(d.cf/d.rb*100,0)+' da receita bruta. Meses fracos podem fechar no negativo.'});
   if(c.cfItens<3) o.push({lv:'warn',t:'Só '+c.cfItens+' item(ns) de custo fixo. Confira se não faltam internet, contador, IPTU mensalizado ou manutenção.'});
   if(d.pl===0) o.push({lv:'warn',t:'Sem pró-labore. Se você trabalha na operação, o resultado final vai parecer maior do que realmente é.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Mensalizar todas as contas anuais (IPTU, seguro, softwares)'},{id:'a2_2',text:'Definir e registrar um pró-labore, mesmo que pequeno'},{id:'a2_3',text:'Pedir proposta de renegociação do maior custo fixo'}]}
]},
/* 3 */
{title:'Custos variáveis', screens:[
 {kind:'learn', title:'Custos variáveis: cada estadia tem um custo',
  body:'<p>Custos variáveis só existem quando há hóspede, e crescem junto com o movimento. No demonstrativo eles são separados em três grupos:</p><ul><li><b>Por reserva</b>: limpeza, lavanderia, kit de boas-vindas e amenities;</li><li><b>Por noite</b>: energia, água, gás e lenha consumidos durante a estadia;</li><li><b>Dos extras</b>: o custo do café, do passeio ou do kit que você vende à parte (em % do preço de venda).</li></ul><p>Somados, eles mostram quanto o mês “cresce em gasto” quando o calendário enche.</p>',
  example:'Exemplo ilustrativo: 5 reservas × (R$ 90 de limpeza + R$ 20 de amenities) = R$ 550; 14 noites × R$ 25 de consumo = R$ 350; extras de R$ 200 com custo de 40% = R$ 80. Custo variável do mês: <b>R$ 980</b>.'},
 {kind:'compare', title:'Por reserva × por noite',
  cols:[{h:'Por reserva',items:['Limpeza e lavanderia','Kit de boas-vindas','Amenities (sabonete, café, papel)','Reposição de pequenos itens']},
        {h:'Por noite',items:['Energia e água extras','Gás, lenha, aquecimento','Café da manhã incluso','Aquecimento de ofurô ou piscina']}]},
 {kind:'form', title:'Quanto custa cada estadia',
  fields:[
   {id:'custo_limpeza',label:'Limpeza + lavanderia, por reserva',type:'money',required:true},
   {id:'custo_amen',label:'Amenities e kit, por reserva',type:'money',required:true,allowUnknown:true},
   {id:'consumo_noite',label:'Energia, água, gás e café por noite ocupada',type:'money',required:true,allowUnknown:true},
   {id:'custo_extras_pct',label:'Custo dos extras vendidos (% do preço de venda)',type:'percent',required:true,allowUnknown:true,help:'Se não souber, usamos a hipótese de 50%.'}
  ]},
 {kind:'feedback', title:'Seu custo variável',
  metrics:function(s,c){var d=c.d;return [{label:'Custo variável mensal',value:F.brl(d.cv),tag:c.cvHip?'estimativa':'calculado'},{label:'Custo por reserva',value:F.brl(c.P.limp+c.P.amen),tag:'calculado'},{label:'Peso na receita bruta',value:d.rb>0?F.pct(d.cv/d.rb*100):'—',tag:'calculado'}];},
  feedback:function(s,c){var o=[],d=c.d;
   if(s.unknown('custo_amen')||s.unknown('consumo_noite')) o.push({lv:'warn',t:'Amenities ou consumo por noite ficaram sem valor e entraram como <b>R$ 0</b>. O custo real é maior: anote as compras e contas de um mês.'});
   if(s.unknown('custo_extras_pct')&&d.recExtras>0) o.push({lv:'warn',t:'Custo dos extras desconhecido: usamos a hipótese de 50% do preço de venda.'});
   if(d.rb>0&&d.cv/d.rb>0.3) o.push({lv:'warn',t:'Custos variáveis de '+F.pct(d.cv/d.rb*100,0)+' da receita bruta. Padronizar limpeza e reposição costuma ser o primeiro passo.'});
   if(c.P.TL===0&&c.R>0&&c.P.limp>0) o.push({lv:'info',t:'Você não cobra taxa de limpeza e cada reserva custa '+F.brl(c.P.limp)+' só de limpeza. Avalie cobrar à parte ou exigir estadia mínima.'});
   else if(c.P.TL>0) o.push({lv:'ok',t:'A taxa de limpeza cobrada ('+F.brl(c.P.TL)+') cobre '+F.pct(c.P.TL/Math.max(1,c.P.limp)*100,0)+' do custo de limpeza por reserva.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Anotar as compras de amenities e reposição de um mês inteiro'},{id:'a3_2',text:'Criar um checklist de limpeza com tempo padrão'},{id:'a3_3',text:'Calcular o custo real de cada extra vendido'}]}
]},
/* 4 */
{title:'Taxas e comissões', screens:[
 {kind:'learn', title:'O que sai antes de você receber',
  body:'<p>Três deduções incidem sobre a receita antes de qualquer custo:</p><ul><li><b>Comissão das plataformas</b>: incide sobre a parte vendida por elas (diária e taxa de limpeza);</li><li><b>Impostos sobre a receita</b>: dependem do seu enquadramento (pessoa física, MEI, Simples etc.). Confirme o percentual com um contador;</li><li><b>Taxa do meio de pagamento</b>: cartão, maquininha ou link de pagamento das reservas diretas e dos extras.</li></ul><p>A soma delas é a diferença entre receita bruta e <b>receita líquida</b>.</p>',
  example:'Exemplo ilustrativo: R$ 4.600 de hospedagem e limpeza, 100% via plataforma com 15% de comissão = R$ 690. Imposto de 6% sobre R$ 4.800 = R$ 288. Taxa de 3% sobre R$ 200 de extras = R$ 6. Deduções: <b>R$ 984</b>, ou 20,5% da receita bruta.'},
 {kind:'compare', title:'Canal de venda e deduções',
  cols:[{h:'Só plataforma',items:['Comissão sobre todas as reservas','Mais exposição e proteção da plataforma','Menos controle sobre o relacionamento']},
        {h:'Mix com reservas diretas',items:['Comissão só sobre parte das reservas','Taxa de pagamento menor que a comissão (confira a sua)','Exige atendimento, política clara e contrato']}]},
 {kind:'form', title:'Suas deduções',
  fields:[
   {id:'share_plat',label:'Parte da receita de hospedagem vendida por plataformas',type:'percent',required:true,help:'100% se todas as reservas vêm de plataformas.'},
   {id:'comissao',label:'Comissão média das plataformas',type:'percent',required:true,max:40},
   {id:'imposto',label:'Imposto sobre a receita',type:'percent',required:true,max:30,allowUnknown:true,help:'Na dúvida, confirme com um contador. Se marcar “não sei”, o cálculo usa 0% e avisa.'},
   {id:'taxa_pag',label:'Taxa do meio de pagamento (reservas diretas e extras)',type:'percent',required:true,max:10,allowUnknown:true}
  ]},
 {kind:'feedback', title:'Da receita bruta à líquida',
  metrics:function(s,c){var d=c.d;return [{label:'Deduções no mês',value:F.brl(d.deducoes),tag:'calculado'},{label:'Peso das deduções',value:d.rb>0?F.pct(d.deducoes/d.rb*100):'—',tag:'calculado'},{label:'Receita líquida',value:F.brl(d.rl),tag:'calculado'}];},
  feedback:function(s,c){var o=[],d=c.d;
   if(s.unknown('imposto')) o.push({lv:'bad',t:'Imposto desconhecido: o demonstrativo usa <b>0%</b>, o que deixa o resultado melhor do que provavelmente é. Confirme o enquadramento com um contador.'});
   if(d.rb>0&&d.deducoes/d.rb>0.22) o.push({lv:'warn',t:'Deduções de '+F.pct(d.deducoes/d.rb*100,0)+' da receita bruta. As comissões sozinhas somam '+F.brl(d.comissoes)+' por mês ('+F.brl(d.comissoes*12)+' por ano).'});
   else if(d.rb>0) o.push({lv:'ok',t:'Deduções de '+F.pct(d.deducoes/d.rb*100,0)+' da receita bruta.'});
   if(c.P.share>=0.9&&d.comissoes>0) o.push({lv:'info',t:'Quase toda a receita passa por plataformas. Cada 10 pontos percentuais migrados para reserva direta economizariam cerca de '+F.brl((d.recHosp+d.recLimp)*0.1*(c.P.com-c.P.tp))+' por mês (comissão menos taxa de pagamento), mantido o volume.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Confirmar com um contador o enquadramento e o imposto correto'},{id:'a4_2',text:'Criar um canal de reserva direta para hóspedes que voltam'},{id:'a4_3',text:'Comparar as taxas de pagamento disponíveis para reservas diretas'}]}
]},
/* 5 */
{title:'Margem operacional', screens:[
 {kind:'learn', title:'Margem de contribuição, resultado e ponto de equilíbrio',
  body:'<p>Com receita, deduções e custos, o demonstrativo fecha assim:</p><div class="za-card">Receita bruta − deduções = <b>receita líquida</b><br>Receita líquida − custos variáveis − fundo de reposição = <b>margem de contribuição</b><br>Margem de contribuição − custos fixos = <b>resultado operacional</b><br>Resultado operacional − pró-labore = <b>resultado final</b></div><p>A <b>margem operacional</b> é o resultado operacional dividido pela receita bruta. O <b>ponto de equilíbrio</b> é a receita (ou o número de noites) em que o resultado final chega a zero.</p><p>O <b>fundo de reposição</b> é uma porcentagem da receita guardada todo mês para trocar enxoval, colchões e eletrodomésticos quando chegar a hora.</p>',
  example:'Exemplo ilustrativo: margem de contribuição de R$ 2.692 sobre R$ 4.800 de receita (56%). Custos fixos de R$ 1.720 e pró-labore de R$ 500: resultado final de R$ 472 (9,8%). Equilíbrio: R$ 2.220 ÷ 56% ≈ R$ 3.958 de receita.'},
 {kind:'compare', title:'Lucro aparente × lucro real',
  cols:[{h:'Aparente',type:'bad',items:['Depósito da plataforma menos contas do mês','Sem fundo para trocar enxoval e móveis','Sem pró-labore','Mês bom tomado como média']},
        {h:'Real',type:'good',items:['Demonstrativo em degraus','Fundo de reposição mensal','Pró-labore registrado','Cenários para meses fracos e fortes']}]},
 {kind:'form', title:'Sua meta de margem',
  fields:[
   {id:'margem_desejada',label:'Margem final desejada sobre a receita bruta',type:'percent',required:true,max:80,help:'É a meta do que deve sobrar depois de tudo, inclusive do pró-labore.'},
   {id:'fundo_repos',label:'Fundo de reposição (% da receita bruta)',type:'percent',required:true,max:20,help:'Valor guardado para trocas futuras. Coloque 0 se não reserva nada hoje.'}
  ]},
 {kind:'feedback', title:'Seu resultado do mês',
  metrics:function(s,c){var d=c.d;return [{label:'Margem de contribuição',value:F.brl(d.mc),tag:'calculado'},{label:'Resultado operacional',value:F.brl(d.resOp),tag:'calculado'},{label:'Resultado final',value:F.brl(d.resFinal),tag:'calculado'},{label:'Margem final',value:F.pct(d.margemFinal==null?null:d.margemFinal*100),tag:'calculado'},{label:'Equilíbrio em noites/mês',value:c.beNoites==null?'inalcançável':F.num(c.beNoites,1),tag:'calculado'}];},
  feedback:function(s,c){var o=[],d=c.d,m=c.m;
   if(d.resFinal<0&&d.resOp>=0) o.push({lv:'warn',t:'A operação paga os custos, mas não paga o seu pró-labore: faltam '+F.brl(-d.resFinal)+' por mês.'});
   else if(d.resOp<0) o.push({lv:'bad',t:'O resultado operacional é negativo ('+F.brl(d.resOp)+'). A hospedagem não cobre os próprios custos no mês típico.'});
   else if(d.margemFinal!=null&&d.margemFinal<m) o.push({lv:'warn',t:'Margem final de '+F.pct(d.margemFinal*100)+', abaixo da meta de '+F.pct(m*100,0)+'.'});
   else o.push({lv:'ok',t:'Margem final de '+F.pct(d.margemFinal==null?0:d.margemFinal*100)+', dentro da meta de '+F.pct(m*100,0)+'.'});
   if(c.beNoites==null) o.push({lv:'bad',t:'A margem de contribuição não é positiva: nenhum volume de noites fecha a conta com os preços e custos atuais.'});
   else o.push({lv:'info',t:'O resultado final chega a zero com cerca de '+F.num(c.beNoites,1)+' noites por mês ('+F.brl(c.beReceita)+' de receita bruta), mantidos preço e custos.'});
   if(c.receitaMeta==null) o.push({lv:'warn',t:'Com a estrutura atual, a margem desejada não é alcançável só com mais volume: a margem de contribuição ('+F.pct(c.mcPct*100,0)+') é menor ou igual à meta. É preciso mexer em preço ou custos.'});
   else if(d.margemFinal!=null&&d.margemFinal<m) o.push({lv:'info',t:'Mantida a estrutura, a meta de '+F.pct(m*100,0)+' exigiria cerca de '+F.brl(c.receitaMeta)+' de receita bruta por mês.'});
   if(s.n('fundo_repos',0)===0) o.push({lv:'warn',t:'Sem fundo de reposição, a primeira troca de colchões ou geladeira sai do caixa de um único mês.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Fechar o demonstrativo todo mês, no mesmo dia'},{id:'a5_2',text:'Separar o fundo de reposição numa conta ou aplicação própria'},{id:'a5_3',text:'Acompanhar o número de noites de equilíbrio a cada mês'}]}
]},
/* 6 */
{title:'Pontos de desperdício', screens:[
 {kind:'learn', title:'Dinheiro que sai sem gerar valor para o hóspede',
  body:'<p>Desperdício é o gasto que o hóspede não percebe e que não melhora a experiência: aquecedor ligado com a casa vazia, lavanderia cobrando por peça sem conferência, amenities repostos sem controle, assinaturas esquecidas, retrabalho de limpeza, consertos de emergência que custam mais do que a manutenção preventiva.</p><p>O caminho é <b>medir antes de cortar</b>: cortar às cegas costuma atingir justamente o que o hóspede valoriza (enxoval, café, limpeza).</p>',
  example:'Exemplo ilustrativo: se os custos variáveis são R$ 980 por mês, uma redução de 10% com controle de estoque e checklist de limpeza vale R$ 98 por mês, ou R$ 1.176 por ano, sem mexer na diária.'},
 {kind:'compare', title:'Cortar × eliminar desperdício',
  cols:[{h:'Corte que prejudica',type:'bad',items:['Trocar enxoval por um de qualidade inferior','Tirar o café de boas-vindas','Reduzir o tempo de limpeza sem checklist','Desligar o Wi-Fi para economizar']},
        {h:'Desperdício eliminado',type:'good',items:['Termostato e timer no aquecimento','Contagem de peças na lavanderia','Kit de amenities padronizado por estadia','Revisão de assinaturas a cada 6 meses']}]},
 {kind:'form', title:'Onde o seu dinheiro escapa',
  fields:[
   {id:'desperd',label:'Quais destes pontos acontecem na sua operação?',type:'checks',options:Object.keys(DESP).map(function(k){return {v:k,l:DESP[k]};})},
   {id:'corte_fixo',label:'Quanto você acredita que dá para reduzir nos custos fixos por mês?',type:'money',required:true,help:'Coloque 0 se não vê espaço.',validate:function(v,s){var t=ZA.listSum((s.v.cf||[]));return v>t?'A redução não pode ser maior que o total de custos fixos ('+F.brl(t)+').':'';}},
   {id:'corte_var_pct',label:'Redução possível nos custos variáveis',type:'percent',required:true,max:50}
  ]},
 {kind:'feedback', title:'O tamanho do desperdício',
  metrics:function(s,c){return [{label:'Economia mensal estimada',value:F.brl(c.economia),tag:'estimativa'},{label:'Economia anual estimada',value:F.brl(c.economia*12),tag:'estimativa'},{label:'Pontos marcados',value:String(c.nDesp),tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(c.nDesp===0) o.push({lv:'info',t:'Nenhum ponto marcado. Mesmo assim, vale conferir a conta de energia de um mês com pouca ocupação: ela mostra quanto se gasta com a casa vazia.'});
   else o.push({lv:'warn',t:'Pontos a atacar: '+c.despNomes.map(function(x){return '<b>'+x+'</b>';}).join('; ')+'.'});
   if(c.economia>0) o.push({lv:'info',t:'As reduções que você estimou somam '+F.brl(c.economia)+' por mês. É uma estimativa sua: confirme depois de 30 dias de controle.'});
   if(c.d.resFinal<0&&c.economia<-c.d.resFinal) o.push({lv:'warn',t:'Mesmo com essas reduções, o resultado final continuaria negativo. Será preciso mexer também em preço, canal de venda ou volume.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Instalar timer ou termostato no aquecimento e conferir a conta seguinte'},{id:'a6_2',text:'Contar as peças enviadas e recebidas da lavanderia'},{id:'a6_3',text:'Cancelar as assinaturas não usadas nos últimos 3 meses'}]}
]},
/* 7 */
{title:'Plano de melhoria financeira', screens:[
 {kind:'learn', title:'Três alavancas: preço, canal e custos',
  body:'<p>O resultado do mês muda por três alavancas principais:</p><ul><li><b>Preço</b>: um pequeno reajuste da diária vai quase inteiro para o resultado, se o volume se mantiver;</li><li><b>Canal</b>: trocar parte das reservas de plataforma por reservas diretas reduz deduções;</li><li><b>Custos</b>: as reduções do Pilar 6.</li></ul><p>O simulador aplica as três sobre o seu mês típico, <b>mantendo o mesmo número de noites</b>. Esse é o ponto mais incerto: reajustes podem reduzir a procura. Por isso o demonstrativo mostra também cenários de volume.</p>',
  example:'Exemplo ilustrativo: reajuste de 10% na diária, 20% das reservas migradas para venda direta, R$ 100 a menos de custo fixo e 10% a menos de custo variável podem levar um resultado de R$ 472 para cerca de R$ 1.110, se o número de noites se mantiver.'},
 {kind:'compare', title:'Plano no papel × plano testado',
  cols:[{h:'No papel',type:'bad',items:['Reajustar tudo de uma vez','Contar com o mesmo volume sem acompanhar','Cortar custos sem medir','Olhar o resultado só no fim do ano']},
        {h:'Testado',type:'good',items:['Uma alavanca por vez, com data','Comparar noites vendidas antes e depois','Medir 30 dias antes de decidir','Demonstrativo mensal e cenários']}]},
 {kind:'form', title:'Simule o seu plano',
  fields:[
   {id:'aumento_diaria',label:'Reajuste de diária que você quer testar',type:'percent',required:true,max:50},
   {id:'share_meta',label:'Parte da receita de hospedagem por plataformas, depois do plano',type:'percent',required:true},
   {id:'meta_resultado',label:'Resultado final mensal que você gostaria de alcançar',type:'money',required:true}
  ]},
 {kind:'feedback', title:'O efeito do plano',
  metrics:function(s,c){return [{label:'Resultado final hoje',value:F.brl(c.d.resFinal),tag:'calculado'},{label:'Resultado com o plano',value:F.brl(c.dp.resFinal),tag:'estimativa'},{label:'Diferença mensal',value:F.brl(c.ganhoPlano),tag:'estimativa'},{label:'Margem final com o plano',value:F.pct(c.dp.margemFinal==null?null:c.dp.margemFinal*100),tag:'estimativa'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:'info',t:'Premissa principal: <b>mesmo número de noites</b> ('+F.num(c.P.N)+') e reservas. Se o reajuste reduzir a procura, o ganho será menor.'});
   if(c.ganhoPlano>0) o.push({lv:'ok',t:'O plano melhora o resultado em '+F.brl(c.ganhoPlano)+' por mês ('+F.brl(c.ganhoPlano*12)+' por ano) nas premissas informadas.'});
   if(c.dp.resFinal<0) o.push({lv:'bad',t:'Mesmo com o plano, o mês típico fecharia em '+F.brl(c.dp.resFinal)+'. A estrutura de custos precisa ser revista com mais profundidade.'});
   var mr=s.n('meta_resultado',0);
   if(mr>0) o.push({lv:c.dp.resFinal>=mr?'ok':'warn',t:c.dp.resFinal>=mr?'Com o plano, a meta de '+F.brl(mr)+' por mês seria alcançada.':'Faltariam '+F.brl(mr-c.dp.resFinal)+' por mês para a meta de '+F.brl(mr)+'.'});
   if(c.aumento>0) o.push({lv:'info',t:'Para o reajuste de '+F.pct(c.aumento*100,0)+' não piorar o resultado de hoje, o número de noites pode cair no máximo até cerca de '+F.num(c.noitesLimite,1)+' por mês (estimativa simplificada).'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Aplicar uma alavanca por vez e anotar a data de início'},{id:'a7_2',text:'Comparar noites vendidas e resultado com o mês anterior'},{id:'a7_3',text:'Refazer o demonstrativo depois de 30 dias com os números reais'}]}
]}
],

compute:function(s){
 var c={};
 var rows=(s.v.cf||[]).filter(function(r){return ZA.isNum(r.value)&&r.value>0;});
 c.cfItens=rows.length; c.cfMaior=rows.slice().sort(function(a,b){return b.value-a.value;})[0]||null;
 var N=s.n('noites_vend',0);
 c.R_hip=!s.has('reservas_mes'); c.R=c.R_hip?N/2:s.n('reservas_mes',0);
 c.cvHip=s.unknown('custo_amen')||s.unknown('consumo_noite')||s.unknown('custo_extras_pct');
 var P={D:s.n('diaria_media',0),N:N,R:c.R,TL:s.n('taxa_limp_cobrada',0),EX:s.n('extras_mes',0),
  share:s.n('share_plat',100)/100,com:s.n('comissao',0)/100,imp:s.n('imposto',0)/100,tp:s.n('taxa_pag',0)/100,
  limp:s.n('custo_limpeza',0),amen:s.n('custo_amen',0),cons:s.n('consumo_noite',0),cex:s.n('custo_extras_pct',50)/100,
  fundo:s.n('fundo_repos',0)/100,CF:ZA.listSum(rows),PL:s.n('prolabore',0)||0};
 c.P=P; var d=dre(P); c.d=d;
 // atalhos para testes
 c.rb=d.rb; c.deducoes=d.deducoes; c.rl=d.rl; c.cv=d.cv; c.mc=d.mc; c.cf=d.cf; c.resOp=d.resOp; c.resFinal=d.resFinal; c.margemOp=d.margemOp; c.margemFinal=d.margemFinal; c.resAnual=d.resFinal*12;
 c.m=s.n('margem_desejada',0)/100;
 c.mcPct=d.rb>0?d.mc/d.rb:0;
 var fixos=d.cf+d.pl;
 c.beNoites=d.mc>0?N*fixos/d.mc:null;
 c.beReceita=c.mcPct>0?fixos/c.mcPct:null;
 c.receitaMeta=(c.mcPct-c.m)>0?fixos/(c.mcPct-c.m):null;
 // cenários de volume (noites, reservas e extras variam juntos; fixos constantes)
 c.cen=[['Conservador',0.8],['Intermediário',1],['Otimista',1.15]].map(function(x){var f=x[1];var rb=d.rb*f,res=d.mc*f-fixos;
   return {nome:x[0],f:f,noites:N*f,rb:rb,mc:d.mc*f,res:res,margem:rb>0?res/rb:null};});
 c.resConservador=c.cen[0].res; c.resOtimista=c.cen[2].res;
 // desperdício e plano
 var desp=s.v.desperd||[]; c.nDesp=desp.length; c.despNomes=desp.map(function(k){return DESP[k]||k;});
 c.corteFixo=Math.min(s.n('corte_fixo',0),d.cf); c.corteVar=s.n('corte_var_pct',0)/100;
 c.economia=c.corteFixo+d.cv*c.corteVar;
 c.aumento=s.n('aumento_diaria',0)/100;
 var Pp=Object.assign({},P,{D:P.D*(1+c.aumento),share:s.n('share_meta',P.share*100)/100,limp:P.limp*(1-c.corteVar),amen:P.amen*(1-c.corteVar),cons:P.cons*(1-c.corteVar),cex:P.cex*(1-c.corteVar),CF:P.CF-c.corteFixo});
 c.dp=dre(Pp); c.resPlano=c.dp.resFinal; c.ganhoPlano=c.dp.resFinal-d.resFinal;
 // noites-limite: volume com o novo preço (sem outras alavancas) que mantém o resultado de hoje
 var Pa=Object.assign({},P,{D:P.D*(1+c.aumento)}), da=dre(Pa);
 c.noitesLimite=da.mc>0?N*(fixos+d.resFinal)/da.mc:null;
 if(c.noitesLimite!=null&&c.noitesLimite<0) c.noitesLimite=0;
 // maior linha de saída
 var linhas=[['Comissões',d.comissoes],['Impostos',d.impostos],['Taxas de pagamento',d.taxasPag],['Custos variáveis',d.cv],['Fundo de reposição',d.repos],['Custos fixos',d.cf],['Pró-labore',d.pl]];
 c.maiorSaida=linhas.slice().sort(function(a,b){return b[1]-a[1];})[0];
 return c;
},

metrics:function(s,c){var d=c.d;return [
 {label:'Receita bruta mensal',value:F.brl(d.rb),tag:'calculado'},
 {label:'Receita líquida',value:F.brl(d.rl),tag:'calculado'},
 {label:'Margem de contribuição',value:F.brl(d.mc),tag:'calculado'},
 {label:'Resultado operacional',value:F.brl(d.resOp),tag:'calculado'},
 {label:'Resultado final (após pró-labore)',value:F.brl(d.resFinal),tag:c.R_hip||c.cvHip||s.unknown('imposto')?'estimativa':'calculado'},
 {label:'Margem final',value:F.pct(d.margemFinal==null?null:d.margemFinal*100),tag:'calculado'},
 {label:'Resultado anual (mês típico × 12)',value:F.brl(c.resAnual),tag:'estimativa'},
 {label:'Noites de equilíbrio por mês',value:c.beNoites==null?'inalcançável':F.num(c.beNoites,1),tag:'calculado'}
];},

priorities:function(s,c){var d=c.d,L=[];
 if(d.resOp<0) L.push({title:'Sair do prejuízo operacional: rever preço, canal e o maior custo ('+c.maiorSaida[0].toLowerCase()+')',why:'A operação perde '+F.brl(-d.resOp)+' por mês antes do pró-labore.',score:10});
 else if(d.resFinal<0) L.push({title:'Gerar margem suficiente para pagar o seu pró-labore',why:'Faltam '+F.brl(-d.resFinal)+' por mês.',score:9});
 if(d.resFinal>=0&&d.margemFinal!=null&&d.margemFinal<c.m) L.push({title:'Fechar a diferença para a margem desejada de '+F.pct(c.m*100,0),why:'Margem atual de '+F.pct(d.margemFinal*100,1)+'.',score:7});
 if(s.unknown('imposto')) L.push({title:'Confirmar com um contador o imposto sobre a receita',why:'O demonstrativo usa 0% e pode estar otimista.',score:8});
 if(d.rb>0&&d.cf/d.rb>0.4&&c.cfMaior) L.push({title:'Renegociar ou reduzir o maior custo fixo: '+c.cfMaior.name,why:'Custos fixos consomem '+F.pct(d.cf/d.rb*100,0)+' da receita.',score:8});
 if(d.rb>0&&d.deducoes/d.rb>0.2) L.push({title:'Aumentar a participação de reservas diretas',why:'Deduções de '+F.pct(d.deducoes/d.rb*100,0)+' da receita bruta ('+F.brl(d.comissoes*12)+' de comissões por ano).',score:7});
 if(d.rb>0&&d.cv/d.rb>0.25) L.push({title:'Padronizar limpeza, lavanderia e reposição',why:'Custos variáveis de '+F.pct(d.cv/d.rb*100,0)+' da receita.',score:6});
 if(c.resConservador<0&&d.resFinal>=0) L.push({title:'Formar uma reserva de caixa para meses fracos',why:'No cenário conservador (−20% de volume) o mês fecha em '+F.brl(c.resConservador)+'.',score:7});
 if(c.nDesp>0) L.push({title:'Eliminar o desperdício: '+c.despNomes[0].toLowerCase(),why:c.nDesp+' ponto(s) de desperdício identificados.',score:6});
 if(s.n('fundo_repos',0)===0) L.push({title:'Criar um fundo de reposição mensal',why:'Trocas de enxoval e equipamentos sairão do caixa de um único mês.',score:5});
 if(d.pl===0) L.push({title:'Definir um pró-labore e incluí-lo no demonstrativo',why:'Sem ele, o resultado parece maior do que é.',score:5});
 if(c.P.TL===0&&c.R>0&&c.P.limp>0) L.push({title:'Avaliar cobrar taxa de limpeza ou exigir estadia mínima',why:'Cada reserva custa '+F.brl(c.P.limp)+' de limpeza sem receita específica.',score:5});
 if(d.recExtras===0) L.push({title:'Testar uma receita extra simples (café, kit, lenha)',why:'Toda a receita depende de diárias.',score:4});
 if(c.R_hip||c.cvHip) L.push({title:'Registrar reservas e custos reais por 30 dias',why:'Parte do demonstrativo usa hipóteses.',score:6});
 if(c.ganhoPlano>0) L.push({title:'Executar o plano simulado, uma alavanca por vez',why:'Ganho estimado de '+F.brl(c.ganhoPlano)+' por mês nas premissas informadas.',score:6});
 return L;},

report:function(s,c){
 var d=c.d, dp=c.dp;
 function pc(v,b){return b>0?F.pct(v/b*100,1):'—';}
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Diária média',F.brl(c.P.D),tg('informado')],
  ['Noites vendidas no mês',F.num(c.P.N),tg('informado')],
  ['Reservas no mês',F.num(c.R,1),c.R_hip?tg('hipotese','hipótese: 2 noites por reserva'):tg('informado')],
  ['Vendas por plataforma / comissão',F.pct(c.P.share*100,0)+' / '+F.pct(c.P.com*100,1),tg('informado')],
  ['Imposto sobre a receita',F.pct(c.P.imp*100,1),s.unknown('imposto')?tg('hipotese','hipótese: 0%'):tg('informado')],
  ['Taxa de pagamento',F.pct(c.P.tp*100,1),s.unknown('taxa_pag')?tg('hipotese','hipótese: 0%'):tg('informado')],
  ['Custo por reserva (limpeza + amenities)',F.brl(c.P.limp+c.P.amen),s.unknown('custo_amen')?tg('hipotese','amenities = R$ 0'):tg('informado')],
  ['Consumo por noite',F.brl(c.P.cons),s.unknown('consumo_noite')?tg('hipotese','hipótese: R$ 0'):tg('informado')],
  ['Custo dos extras',F.pct(c.P.cex*100,0)+' do preço',s.unknown('custo_extras_pct')?tg('hipotese','hipótese: 50%'):tg('informado')],
  ['Fundo de reposição',F.pct(c.P.fundo*100,1)+' da receita',tg('informado')],
  ['Anualização','mês típico × 12',tg('estimativa')]],[1]);
 var L=[['<b>Receita bruta</b>',d.rb],['&nbsp;&nbsp;Hospedagem',d.recHosp],['&nbsp;&nbsp;Taxa de limpeza cobrada',d.recLimp],['&nbsp;&nbsp;Extras',d.recExtras],
  ['(−) Comissões',-d.comissoes],['(−) Impostos',-d.impostos],['(−) Taxas de pagamento',-d.taxasPag],['<b>= Receita líquida</b>',d.rl],
  ['(−) Custos por reserva',-d.cvReserva],['(−) Consumo por noite',-d.cvNoite],['(−) Custo dos extras',-d.cvExtras],['(−) Fundo de reposição',-d.repos],['<b>= Margem de contribuição</b>',d.mc],
  ['(−) Custos fixos',-d.cf],['<b>= Resultado operacional</b>',d.resOp],['(−) Pró-labore',-d.pl],['<b>= Resultado final</b>',d.resFinal]];
 var dreT=ZA.table(['Linha','Mensal','Anual','% da receita'],L.map(function(r){return [r[0],F.brl(r[1]),F.brl(r[1]*12),pc(Math.abs(r[1]),d.rb)];}),[1,2,3]);
 var cen=ZA.table(['Cenário','Volume','Noites/mês','Receita bruta','Resultado final/mês','Resultado/ano','Margem final'],c.cen.map(function(x){return [x.nome,(x.f===1?'atual':(x.f>1?'+':'')+F.pct((x.f-1)*100,0)),F.num(x.noites,1),F.brl(x.rb),F.brl(x.res),F.brl(x.res*12),x.margem==null?'—':F.pct(x.margem*100,1)];}),[2,3,4,5,6]);
 var plano=ZA.table(['Linha','Hoje','Com o plano','Diferença'],[
  ['Receita bruta',F.brl(d.rb),F.brl(dp.rb),F.brl(dp.rb-d.rb)],['Deduções',F.brl(d.deducoes),F.brl(dp.deducoes),F.brl(dp.deducoes-d.deducoes)],
  ['Custos variáveis',F.brl(d.cv),F.brl(dp.cv),F.brl(dp.cv-d.cv)],['Custos fixos',F.brl(d.cf),F.brl(dp.cf),F.brl(dp.cf-d.cf)],
  ['<b>Resultado final</b>',F.brl(d.resFinal),F.brl(dp.resFinal),F.brl(c.ganhoPlano)]],[1,2,3]);
 var desp=c.nDesp?'<ul>'+c.despNomes.map(function(x){return '<li>'+esc(x)+'</li>';}).join('')+'</ul>':'<p class="za-small">Nenhum ponto de desperdício marcado.</p>';
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro de 30 dias</b><ol>'+
  '<li><b>Semana 1:</b> abrir (ou conferir) a conta separada da hospedagem e '+(top[0]?esc(top[0].title).replace(/^./,function(x){return x.toLowerCase();}):'confirmar os números do mês típico')+'.</li>'+
  '<li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Revisar os custos fixos')+'.</li>'+
  '<li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Eliminar o primeiro ponto de desperdício')+'.</li>'+
  '<li><b>Semana 4:</b> fechar o demonstrativo do mês com os números reais, comparar com este relatório (resultado de '+F.brl(d.resFinal)+') e escolher a próxima alavanca.</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Demonstrativo do resultado (DRE simplificada)',html:dreT+'<p class="za-small">Valores anuais = mês típico × 12. Se a sua receita varia muito entre temporadas, use os cenários abaixo como faixa.</p>'},
  {title:'Ponto de equilíbrio',html:'<p>O resultado final chega a zero com <b>'+(c.beNoites==null?'nenhum volume (margem de contribuição não positiva)':F.num(c.beNoites,1)+' noites por mês')+'</b>'+(c.beReceita!=null?', ou '+F.brl(c.beReceita)+' de receita bruta':'')+'. Margem de contribuição: '+F.pct(c.mcPct*100,1)+' da receita.</p>'+(c.receitaMeta!=null?'<p>Para a margem desejada de '+F.pct(c.m*100,0)+', a receita bruta mensal precisaria ser de cerca de <b>'+F.brl(c.receitaMeta)+'</b>, mantida a estrutura atual.</p>':'<p>A margem desejada de '+F.pct(c.m*100,0)+' não é alcançável só com volume: exige mudança de preço ou custos.</p>')},
  {title:'Cenários: Conservador, Intermediário e Otimista',html:cen+'<p class="za-small">Premissas: Conservador = 20% menos noites, reservas e extras; Intermediário = mês típico informado; Otimista = 15% mais. Preços e custos fixos constantes; custos variáveis e deduções acompanham o volume. Simulações, não previsões.</p>'},
  {title:'Plano de melhoria simulado',html:plano+'<p class="za-small">Premissas do plano: reajuste de '+F.pct(c.aumento*100,0)+' na diária, '+F.pct(s.n('share_meta',0),0)+' da hospedagem por plataformas, redução de '+F.brl(c.corteFixo)+' nos custos fixos e de '+F.pct(c.corteVar*100,0)+' nos variáveis, <b>mantido o número de noites</b>.</p>'},
  {title:'Pontos de desperdício identificados',html:desp+'<p>Economia estimada por você: '+F.brl(c.economia)+' por mês ('+F.brl(c.economia*12)+' por ano).</p>'}
 ],plan:plan};
}
});
})();
