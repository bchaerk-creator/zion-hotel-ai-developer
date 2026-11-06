/* ZAR-A02 · Quanto Devo Cobrar pela Minha Diária? · Precificador Inteligente Zion */
(function(){
var F=ZA.fmt, esc=ZA.esc;
ZA.register({
id:'A02', code:'ZAR-A02', collection:'Hospedagem',
title:'Quanto Devo Cobrar pela Minha Diária?',
subtitle:'Aprenda a Precificar Sua Hospedagem',
tool:'Precificador Inteligente Zion',
deliverable:'Plano Personalizado de Precificação',
nameField:'nome', propertyField:'propriedade',
disclaimer:'Os valores dependem das premissas que você informou. Preço é decisão comercial: teste, meça e ajuste. Não há garantia de ocupação, faturamento ou lucro.',

intro:[
 {kind:'mirror', title:'Você sabe quanto precisa cobrar para sua diária valer a pena?',
  lead:'Você olhou o anúncio do vizinho, colocou um valor parecido e torceu para dar certo. No fim do mês, a conta não fecha e você não sabe exatamente por quê.',
  body:'<div class="za-card"><p>Se alguma destas frases parece com você, esta mini mentoria foi feita para o seu caso:</p><ul><li>“Defini minha diária olhando o Airbnb dos outros.”</li><li>“Baixo o preço quando o calendário esvazia, mas não sei até onde posso baixar.”</li><li>“Tenho reservas, mas sobra pouco depois de limpeza, taxas e contas.”</li><li>“Cobro igual no feriado e numa terça-feira de junho.”</li></ul></div>'},
 {kind:'collapse', title:'Copiar o preço do concorrente não significa que sua hospedagem terá lucro.',
  lead:'O concorrente tem outros custos, outra ocupação, outra estrutura. O preço dele resolve a conta dele, não a sua.',
  body:'<div class="za-card"><p>A diária certa nasce de três perguntas, nesta ordem:</p><ol><li><b>Quanto custa manter a hospedagem aberta?</b> (custos fixos e variáveis)</li><li><b>Quantas noites você realmente vende?</b> (ocupação)</li><li><b>Quanto você quer que sobre?</b> (margem)</li></ol><p>Só depois disso o mercado entra como referência de posicionamento. Neste percurso você vai responder às três com os seus números.</p></div>'},
 {kind:'start', title:'Vamos montar o seu preço com os seus números',
  lead:'Em 7 pilares, você vai calcular sua diária mínima, sua diária-alvo, os preços por temporada e sair com um plano de precificação.',
  body:'<p>Tenha à mão, se possível: contas do mês (energia, água, internet), valor pago pela limpeza, extrato de uma plataforma de reservas. Se não tiver um dado, você poderá marcar “não sei” e seguir — o relatório indicará o que ficou como hipótese.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Ana'},
   {id:'propriedade',label:'Nome da hospedagem',type:'text',required:true,placeholder:'Ex.: Cabana Vale das Araucárias'},
   {id:'tipo',label:'Tipo de hospedagem',type:'select',required:true,options:[{v:'airbnb',l:'Apartamento ou casa (Airbnb/temporada)'},{v:'cabana',l:'Cabana ou chalé'},{v:'glamping',l:'Glamping'},{v:'pousada',l:'Pequena pousada'},{v:'outro',l:'Outro'}]},
   {id:'destino',label:'Cidade / destino',type:'text',required:true,placeholder:'Ex.: Urubici (SC)'},
   {id:'unidades',label:'Quantas unidades você aluga?',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)'}
  ]}
],

pillars:[
/* 1 */
{title:'Entendendo a precificação', screens:[
 {kind:'learn', title:'Preço não é um número: é uma conta e uma decisão',
  body:'<p>Toda diária precisa pagar três coisas: <b>o que você gasta para receber o hóspede</b> (custo variável), <b>uma parte do que você gasta para existir</b> (custo fixo dividido pelas noites vendidas) e <b>o que deve sobrar</b> (margem). Além disso, parte do valor fica com plataformas, impostos e taxas de pagamento.</p><p>Por isso, a fórmula do Precificador é:</p><div class="za-card"><b>Diária = (Custo fixo ÷ Noites vendidas + Custo variável por noite) ÷ (1 − Deduções % − Margem %)</b></div><p>Quando a margem é zero, o resultado é a <b>diária mínima</b>: abaixo dela, cada noite vendida aumenta o prejuízo do mês.</p>',
  example:'Uma cabana com R$ 3.000 de custo fixo, 15 noites vendidas, R$ 60 de custo variável por noite e 20% de deduções tem diária mínima de (3.000 ÷ 15 + 60) ÷ 0,80 = <b>R$ 325</b>.'},
 {kind:'compare', title:'Três formas de definir a diária',
  intro:'Compare os métodos mais comuns:',
  cols:[{h:'Formas arriscadas',type:'bad',items:['Copiar o concorrente sem conhecer seus próprios custos','Definir por intuição (“acho que vale isso”)','Baixar o preço sempre que o calendário esvazia','Usar o mesmo preço o ano inteiro']},
        {h:'Forma Zion',type:'good',items:['Calcular a diária mínima a partir dos custos','Somar a margem desejada para chegar à diária-alvo','Ajustar por temporada e dia da semana','Usar o mercado para posicionar, não para decidir sozinho']}]},
 {kind:'form', title:'Seu ponto de partida', intro:'Conte como você precifica hoje.',
  fields:[
   {id:'diaria_atual',label:'Diária média que você cobra hoje',type:'money',required:true,min:1,help:'Se varia muito, use a média dos últimos 3 meses.'},
   {id:'metodo',label:'Como você chegou a esse valor?',type:'radio',required:true,options:[{v:'concorrente',l:'Olhei os concorrentes'},{v:'intuicao',l:'Intuição / sensação de mercado'},{v:'custos',l:'Calculei pelos meus custos'},{v:'ferramenta',l:'Ferramenta de preço dinâmico da plataforma'}]},
   {id:'objetivo',label:'Qual é a sua prioridade agora?',type:'radio',required:true,options:[{v:'ocupar',l:'Ocupar mais noites'},{v:'lucro',l:'Aumentar o que sobra no fim do mês'},{v:'equilibrio',l:'Parar de ter prejuízo'}]}
  ]},
 {kind:'feedback', title:'O que o seu ponto de partida revela',
  feedback:function(s){var o=[];
   if(s.t('metodo')==='concorrente') o.push({lv:'warn',t:'Você usa o preço do concorrente como base. É uma boa referência de mercado, mas não diz se <b>você</b> tem lucro. Nos próximos pilares, vamos checar isso com seus custos.'});
   if(s.t('metodo')==='intuicao') o.push({lv:'warn',t:'Preço por intuição costuma ficar abaixo do necessário quando há custos “invisíveis” (limpeza, lavanderia, comissões). Vamos torná-los visíveis.'});
   if(s.t('metodo')==='ferramenta') o.push({lv:'info',t:'Ferramentas de preço dinâmico ajustam pela demanda, mas não conhecem seus custos. Você vai descobrir o <b>piso</b> abaixo do qual a ferramenta não deveria ir.'});
   if(s.t('metodo')==='custos') o.push({lv:'ok',t:'Ótimo: você já parte dos custos. Vamos revisar se nenhum ficou de fora e incluir margem e sazonalidade.'});
   if(s.t('objetivo')==='ocupar') o.push({lv:'info',t:'Para ocupar mais sem destruir a margem, você precisa saber exatamente até onde pode baixar. Isso é a diária mínima.'});
   if(s.t('objetivo')==='equilibrio') o.push({lv:'info',t:'Sair do prejuízo começa por descobrir a diária mínima e a ocupação de equilíbrio — os dois números que você terá no Pilar 4.'});
   if(s.t('objetivo')==='lucro') o.push({lv:'info',t:'Para aumentar o que sobra, você vai definir uma margem-alvo no Pilar 5 e transformá-la em preço.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1', intro:'Escolha o que vai fazer a partir de agora.',
  actions:[{id:'a1_1',text:'Parar de definir preço apenas pelo concorrente ou pela intuição'},{id:'a1_2',text:'Separar as contas da hospedagem das contas pessoais'},{id:'a1_3',text:'Registrar mensalmente a diária média e a ocupação'}]}
]},
/* 2 */
{title:'Custos fixos', screens:[
 {kind:'learn', title:'Custos fixos: o que você paga mesmo sem hóspede',
  body:'<p>Custo fixo é tudo que existe mesmo que o calendário fique vazio: financiamento ou aluguel do imóvel, condomínio, IPTU, internet, assinaturas, seguro, contador, manutenção preventiva, funcionários fixos e a parte mínima das contas de energia e água.</p><p>Quanto menos noites você vende, mais cada noite precisa carregar desse custo. Por isso, ocupação baixa encarece a diária mínima.</p>',
  example:'R$ 3.600 de custo fixo divididos por 12 noites vendidas = R$ 300 por noite. Com 24 noites, cai para R$ 150.'},
 {kind:'compare', title:'O que costuma ficar de fora',
  cols:[{h:'Esquecidos com frequência',type:'bad',items:['Manutenção (pintura, enxoval, conserto)','Depreciação de móveis e eletrodomésticos','Software de gestão / channel manager','Seu tempo (pró-labore)','Taxas bancárias e contador']},
        {h:'Como tratar',type:'good',items:['Reserve um valor mensal para manutenção (ex.: 1% a 3% do valor do mobiliário por mês, como estimativa)','Some assinaturas anuais divididas por 12','Inclua o pró-labore no Pilar 5','Use a média de 3 a 6 meses das contas']}]},
 {kind:'form', title:'Liste seus custos fixos mensais', intro:'Informe valores <b>mensais</b> da hospedagem inteira (todas as unidades). Deixe em branco o que não se aplica; adicione itens se precisar.',
  fields:[{id:'cf',label:'Custos fixos por mês',type:'list',required:true,preset:['Financiamento ou aluguel do imóvel','Condomínio / IPTU (mensalizado)','Internet e TV','Energia e água (parte fixa)','Manutenção e reposição','Software / channel manager','Contador e taxas','Funcionários fixos','Seguro'],namePlaceholder:'Descrição',valuePlaceholder:'R$ / mês'}]},
 {kind:'feedback', title:'Seu custo fixo e o peso dele em cada noite',
  metrics:function(s,c){return [{label:'Custo fixo mensal',value:F.brl(c.cf),tag:'calculado'},{label:'Itens informados',value:String(c.cfItens),tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(c.cfItens<3) o.push({lv:'warn',t:'Você informou menos de 3 itens de custo fixo. Confira se não faltam manutenção, internet, contador ou o imóvel em si.'});
   else o.push({lv:'ok',t:'Boa base: '+c.cfItens+' itens de custo fixo somando '+F.brl(c.cf)+' por mês.'});
   if(c.cfMaior) o.push({lv:'info',t:'Seu maior custo fixo é <b>'+esc(c.cfMaior.name)+'</b> ('+F.brl(c.cfMaior.value)+', '+F.pct(c.cfMaior.value/c.cf*100,0)+' do total). É aqui que uma renegociação teria mais efeito.'});
   if(!c.temManut) o.push({lv:'warn',t:'Não há reserva para manutenção. Sem ela, o primeiro conserto grande “come” o lucro do mês.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Criar uma reserva mensal de manutenção'},{id:'a2_2',text:'Renegociar o maior custo fixo identificado'},{id:'a2_3',text:'Revisar assinaturas e serviços que não usa'}]}
]},
/* 3 */
{title:'Custos variáveis', screens:[
 {kind:'learn', title:'Custos variáveis: o que cada hóspede custa',
  body:'<p>Custo variável só existe quando há hóspede: limpeza, lavanderia, amenities (sabonete, café, papel), energia e água extras, café da manhã. Alguns são <b>por estadia</b> (a limpeza acontece uma vez, seja 1 ou 5 noites) e outros <b>por noite</b>.</p><p>Há também as <b>deduções percentuais</b>: comissão da plataforma, imposto sobre a receita e taxa do meio de pagamento. Elas saem de cada real recebido.</p>',
  example:'Limpeza de R$ 120 numa estadia de 2 noites pesa R$ 60 por noite. Na estadia de 4 noites, R$ 30. Por isso a estadia mínima e a taxa de limpeza fazem tanta diferença.'},
 {kind:'compare', title:'Por estadia × por noite',
  cols:[{h:'Por estadia (dividido pelas noites)',items:['Limpeza','Lavanderia de enxoval','Kit de boas-vindas e amenities','Check-in presencial (se pago)']},
        {h:'Por noite',items:['Energia e água extras','Gás / lenha','Café da manhã','Aquecimento de ofurô ou piscina']}]},
 {kind:'form', title:'Quanto custa receber um hóspede', intro:'Valores para <b>uma unidade</b>.',
  fields:[
   {id:'limpeza',label:'Limpeza por estadia',type:'money',required:true},
   {id:'lavanderia',label:'Lavanderia por estadia',type:'money',required:true,allowUnknown:true},
   {id:'amenities',label:'Amenities e kit por estadia',type:'money',required:true,allowUnknown:true},
   {id:'extra_noite',label:'Energia, água, gás e café da manhã por noite',type:'money',required:true,allowUnknown:true},
   {id:'estadia_media',label:'Estadia média',type:'number',required:true,min:1,max:60,step:0.1,unit:'noites',allowUnknown:true,help:'Total de noites vendidas ÷ número de reservas. Se não souber, o cálculo usará 2 noites.'},
   {id:'comissao',label:'Comissão média da plataforma',type:'percent',required:true,max:40,help:'Considere a média ponderada entre canais (reservas diretas = 0%).'},
   {id:'imposto',label:'Imposto sobre a receita',type:'percent',required:true,max:30,allowUnknown:true},
   {id:'taxa_pag',label:'Taxa do meio de pagamento',type:'percent',required:true,max:10,allowUnknown:true}
  ]},
 {kind:'feedback', title:'Custo por noite e deduções',
  metrics:function(s,c){return [{label:'Custo variável por noite',value:F.brl(c.cvN),tag:'calculado'},{label:'Deduções sobre a diária',value:F.pct(c.ded*100),tag:'calculado'},{label:'Peso da limpeza por noite',value:F.brl(c.limpN),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(s.unknown('estadia_media')) o.push({lv:'warn',t:'Estadia média desconhecida: usamos <b>2 noites</b> como hipótese. Confira no extrato da plataforma — esse número muda bastante o custo por noite.'});
   if(c.ded>0.25) o.push({lv:'bad',t:'Suas deduções somam '+F.pct(c.ded*100)+'. Um quarto de cada diária sai antes de pagar qualquer custo. Reservas diretas e revisão de canal podem ter grande impacto.'});
   else if(c.ded>0.15) o.push({lv:'warn',t:'Deduções de '+F.pct(c.ded*100)+'. Estão dentro do comum, mas vale medir quanto vem de cada canal.'});
   else o.push({lv:'ok',t:'Deduções de '+F.pct(c.ded*100)+': nível controlado.'});
   if(ZA.isNum(s.n('diaria_atual'))&&c.cvN>s.n('diaria_atual')*0.35) o.push({lv:'warn',t:'O custo variável consome mais de 35% da sua diária atual. Avalie estadia mínima maior ou taxa de limpeza separada.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Calcular a estadia média real com o extrato da plataforma'},{id:'a3_2',text:'Avaliar cobrar taxa de limpeza separada ou exigir estadia mínima'},{id:'a3_3',text:'Criar um canal de reserva direta para reduzir comissões'}]}
]},
/* 4 */
{title:'Ocupação e ponto de equilíbrio', screens:[
 {kind:'learn', title:'Ocupação: o número que decide a sua diária mínima',
  body:'<p><b>Taxa de ocupação</b> = noites vendidas ÷ noites disponíveis. Ela determina por quantas noites o custo fixo será dividido.</p><p>O <b>ponto de equilíbrio</b> pode ser lido de duas formas: a diária mínima para uma ocupação, ou a ocupação mínima para uma diária. Você terá as duas.</p>',
  example:'Com 30 noites disponíveis e 12 vendidas, a ocupação é 40%. Se você planejar a diária contando com 70%, ela ficará baixa demais para a realidade.'},
 {kind:'compare', title:'Ocupação planejada × ocupação real',
  cols:[{h:'Erro comum',type:'bad',items:['Calcular o preço contando com casa cheia','Usar a ocupação da alta temporada como média do ano','Não contar noites bloqueadas para uso próprio']},
        {h:'Como fazer',type:'good',items:['Use a média real dos últimos meses','Planeje com uma ocupação conservadora','Desconte noites de manutenção e uso próprio']}]},
 {kind:'form', title:'Suas noites disponíveis e vendidas',
  fields:[
   {id:'noites_disp',label:'Noites disponíveis por mês, por unidade',type:'number',required:true,min:1,max:31,step:1,unit:'noites',help:'Normalmente 30, menos bloqueios para uso próprio ou manutenção.'},
   {id:'ocup_atual',label:'Ocupação média atual',type:'percent',required:true,allowUnknown:true,help:'Noites vendidas ÷ noites disponíveis nos últimos 3 a 6 meses.'},
   {id:'ocup_plan',label:'Ocupação que você considera realista planejar',type:'percent',required:true,min:1,max:100}
  ]},
 {kind:'feedback', title:'Seu ponto de equilíbrio',
  metrics:function(s,c){return [{label:'Diária mínima (equilíbrio)',value:F.brl(c.pMin),tag:'calculado'},{label:'Ocupação de equilíbrio no preço atual',value:c.occBE==null?'inalcançável':F.pct(c.occBE*100),tag:'calculado'},{label:'Noites vendidas/mês planejadas',value:F.num(c.nv,0),tag:'calculado'}];},
  feedback:function(s,c){var o=[]; var p=s.n('diaria_atual');
   if(c.pMin==null) o.push({lv:'bad',t:'Com as deduções informadas, não é possível calcular a diária mínima. Revise os percentuais do Pilar 3.'});
   else if(p<c.pMin) o.push({lv:'bad',t:'Sua diária atual ('+F.brl(p)+') está <b>abaixo da diária mínima</b> ('+F.brl(c.pMin)+') para a ocupação planejada. Nessa condição, a operação fecha o mês no negativo.'});
   else o.push({lv:'ok',t:'Sua diária atual cobre os custos na ocupação planejada, com folga de '+F.brl(p-c.pMin)+' por noite.'});
   if(c.occBE==null) o.push({lv:'bad',t:'No preço atual, o que sobra de cada noite não cobre o custo variável — nenhuma ocupação fecha a conta.'});
   else if(c.occBE>1) o.push({lv:'bad',t:'No preço atual, seria preciso mais de 100% de ocupação para empatar.'});
   else if(c.occBE>0.6) o.push({lv:'warn',t:'No preço atual, você só empata com '+F.pct(c.occBE*100)+' de ocupação. Pouca margem para meses fracos.'});
   if(!s.unknown('ocup_atual')&&ZA.isNum(s.n('ocup_atual'))&&s.n('ocup_plan')>s.n('ocup_atual')+15) o.push({lv:'warn',t:'Você planejou '+F.pct(s.n('ocup_plan'),0)+' de ocupação, mas hoje tem '+F.pct(s.n('ocup_atual'),0)+'. Planejar acima da realidade gera preço baixo demais.'});
   if(s.unknown('ocup_atual')) o.push({lv:'warn',t:'Ocupação atual desconhecida. Medir esse número é uma das ações mais importantes do seu plano.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Calcular a ocupação real de cada mês dos últimos 6 meses'},{id:'a4_2',text:'Configurar a diária mínima como piso na plataforma / ferramenta de preço'},{id:'a4_3',text:'Planejar com ocupação conservadora, não com a alta temporada'}]}
]},
/* 5 */
{title:'Margem e rentabilidade', screens:[
 {kind:'learn', title:'Margem: o que precisa sobrar',
  body:'<p>Empatar não é objetivo de negócio. A <b>margem</b> é a parte da receita que sobra depois de todos os custos e deduções. Ela paga reinvestimentos, imprevistos e o retorno do seu capital.</p><p>Se você trabalha na operação, inclua também um <b>pró-labore</b>: o valor do seu trabalho. Sem ele, o “lucro” pode ser apenas o seu salário disfarçado.</p>',
  example:'Diária mínima de R$ 300 e margem desejada de 20%: a diária-alvo não é R$ 360 (300 + 20%), porque a margem é calculada sobre a receita. A fórmula do Precificador faz essa conta corretamente.'},
 {kind:'compare', title:'Margem sobre custo × margem sobre receita',
  cols:[{h:'Somar % ao custo',type:'bad',items:['R$ 300 + 20% = R$ 360','Na prática, sobra menos de 20% da receita','Comissões incidem também sobre a margem']},
        {h:'Margem sobre receita (Zion)',type:'good',items:['Diária = custo ÷ (1 − deduções − margem)','A margem real fica igual à desejada','Mostra quando a margem desejada é inviável']}]},
 {kind:'form', title:'Quanto deve sobrar',
  fields:[
   {id:'margem',label:'Margem desejada sobre a receita',type:'percent',required:true,max:60,help:'Referência orientativa: muitos pequenos negócios de hospedagem trabalham entre 10% e 30%. Escolha o que faz sentido para o seu caso.'},
   {id:'prolabore',label:'Pró-labore mensal desejado (se você trabalha na operação)',type:'money',required:false,help:'Deixe em branco se não se aplica.'}
  ]},
 {kind:'feedback', title:'Sua diária-alvo',
  metrics:function(s,c){return [{label:'Diária-alvo',value:c.pAlvo==null?'inviável':F.brl(c.pAlvo),tag:'calculado'},{label:'Diária mínima',value:F.brl(c.pMin),tag:'calculado'},{label:'Resultado mensal na diária atual',value:F.brl(c.lucroAtual),tag:'estimativa'}];},
  feedback:function(s,c){var o=[];var p=s.n('diaria_atual');
   if(c.pAlvo==null) o.push({lv:'bad',t:'Deduções + margem somam 100% ou mais. Reduza a margem desejada ou as deduções para obter um preço possível.'});
   else if(p<c.pAlvo) o.push({lv:'warn',t:'Para atingir sua meta, a diária média precisaria ser <b>'+F.brl(c.pAlvo)+'</b>, '+F.pct((c.pAlvo/p-1)*100,0)+' acima da atual. Se o mercado não aceita esse valor, o caminho é reduzir custos, aumentar ocupação ou estadia média.'});
   else o.push({lv:'ok',t:'Sua diária atual já atinge a margem desejada.'});
   o.push({lv:'info',t:'Na diária atual e ocupação planejada, o resultado estimado é de '+F.brl(c.lucroAtual)+' por mês'+(c.pl?' depois do pró-labore de '+F.brl(c.pl):'')+'.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Definir a diária-alvo como referência de preço médio mensal'},{id:'a5_2',text:'Incluir pró-labore nas contas da hospedagem'},{id:'a5_3',text:'Acompanhar a margem real todo mês'}]}
]},
/* 6 */
{title:'Sazonalidade e posicionamento', screens:[
 {kind:'learn', title:'Um preço só para o ano inteiro deixa dinheiro na mesa',
  body:'<p>A demanda muda com feriados, férias, clima e dias da semana. Um preço fixo fica caro demais na baixa e barato demais na alta. A estratégia Zion parte da diária-alvo como <b>média</b> e distribui: mais alto na alta, mais baixo na baixa — mas nunca abaixo da diária mínima.</p><p>O <b>posicionamento</b> define onde você quer estar em relação ao mercado: econômico, intermediário ou premium. Ele precisa ser coerente com a experiência entregue.</p>',
  example:'Diária-alvo de R$ 400, alta +25% (R$ 500) e baixa −15% (R$ 340). Se a diária mínima for R$ 350, o preço da baixa precisa ser revisto.'},
 {kind:'compare', title:'Posicionamento coerente',
  cols:[{h:'Incoerente',type:'bad',items:['Preço premium com fotos amadoras','Preço econômico numa cabana com ofurô e vista','Descontos constantes que ensinam o hóspede a esperar']},
        {h:'Coerente',type:'good',items:['Preço sustentado por diferenciais visíveis','Variação planejada por temporada','Promoções pontuais com motivo e prazo']}]},
 {kind:'form', title:'Suas temporadas e o mercado',
  fields:[
   {id:'meses_alta',label:'Meses de alta temporada no ano',type:'number',required:true,min:0,max:12,step:1,unit:'meses'},
   {id:'meses_baixa',label:'Meses de baixa temporada no ano',type:'number',required:true,min:0,max:12,step:1,unit:'meses',validate:function(v,s){var a=s.n('meses_alta')||0;return a+v>12?'Alta + baixa não pode passar de 12 meses.':'';}},
   {id:'aj_alta',label:'Aumento na alta temporada',type:'percent',required:true,max:100},
   {id:'aj_baixa',label:'Redução na baixa temporada',type:'percent',required:true,max:60},
   {id:'posic',label:'Posicionamento desejado',type:'radio',required:true,options:[{v:'economico',l:'Econômico'},{v:'intermediario',l:'Intermediário'},{v:'premium',l:'Premium'}]},
   {id:'preco_conc',label:'Diária média de 3 a 5 concorrentes parecidos',type:'money',required:true,allowUnknown:true}
  ]},
 {kind:'feedback', title:'Seus preços por temporada',
  metrics:function(s,c){return c.pAlvo==null?[]:[{label:'Alta',value:F.brl(c.pAltaF),tag:'calculado'},{label:'Média',value:F.brl(c.pMedia),tag:'calculado'},{label:'Baixa',value:F.brl(c.pBaixaF),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.pAlvo==null){o.push({lv:'bad',t:'Defina uma margem viável no Pilar 5 para calcular as temporadas.'});return o;}
   o.push({lv:'info',t:'A diária da temporada média foi ajustada para que a média ponderada do ano fique igual à diária-alvo ('+F.brl(c.pAlvo)+').'});
   if(c.baixaAbaixoMin) o.push({lv:'bad',t:'A diária da baixa ficaria abaixo da mínima. Ela foi travada em '+F.brl(c.pMin)+'. Reduza o desconto de baixa ou reveja custos.'});
   if(s.n('aj_alta')===0&&s.n('aj_baixa')===0) o.push({lv:'warn',t:'Você não diferencia temporadas. Quase sempre há receita a capturar nas datas de maior procura.'});
   if(c.conc!=null){var d=(c.pAlvo/c.conc-1)*100;
     o.push({lv:Math.abs(d)>30?'warn':'info',t:'Sua diária-alvo está '+(d>=0?F.pct(d,0)+' acima':F.pct(-d,0)+' abaixo')+' da média dos concorrentes ('+F.brl(c.conc)+').'+(d>30?' Para sustentar isso, seus diferenciais precisam estar muito evidentes no anúncio.':'')+(d<-30?' Talvez haja espaço para subir o preço.':'')});
     if(s.t('posic')==='premium'&&c.pAlvo<c.conc) o.push({lv:'warn',t:'Você quer ser premium, mas sua diária-alvo está abaixo do mercado. Posicionamento e preço estão desalinhados.'});
   } else o.push({lv:'warn',t:'Sem a média dos concorrentes, não há referência de mercado. Pesquise 3 a 5 anúncios parecidos.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Montar o calendário anual com preços de alta, média e baixa'},{id:'a6_2',text:'Pesquisar 5 concorrentes e registrar preços em datas iguais'},{id:'a6_3',text:'Alinhar fotos e descrição ao posicionamento escolhido'}]}
]},
/* 7 */
{title:'Estratégia de preços', screens:[
 {kind:'learn', title:'Do preço calculado à estratégia de venda',
  body:'<p>Com piso (diária mínima), referência (diária-alvo) e temporadas definidos, as táticas finais são:</p><ul><li><b>Fim de semana:</b> sexta e sábado costumam ter mais demanda.</li><li><b>Estadia mínima:</b> reduz o peso da limpeza por noite.</li><li><b>Desconto semanal:</b> troca preço por ocupação garantida.</li><li><b>Antecedência:</b> preço pode subir conforme a data se aproxima e a demanda se confirma.</li></ul><p>Toda tática deve respeitar a regra de ouro: <b>nenhuma noite abaixo da diária mínima</b>.</p>',
  example:'Diária média R$ 400, fim de semana +20% = R$ 480. Desconto semanal de 10% numa estadia de 7 noites a R$ 400 = R$ 2.520, ainda acima do mínimo se a mínima for R$ 330.'},
 {kind:'compare', title:'Táticas e cuidados',
  cols:[{h:'Tática',items:['Acréscimo de fim de semana','Estadia mínima de 2 noites na alta','Desconto semanal/mensal','Preço de última hora']},
        {h:'Cuidado',items:['Testar e medir conversão','Liberar noites “sobradas” entre reservas','Conferir se o desconto não fura o piso','Não baixar abaixo da diária mínima']}]},
 {kind:'form', title:'Defina suas táticas',
  fields:[
   {id:'aj_fds',label:'Acréscimo de sexta e sábado',type:'percent',required:true,max:100},
   {id:'est_min',label:'Estadia mínima',type:'number',required:true,min:1,max:30,step:1,unit:'noites'},
   {id:'desc_sem',label:'Desconto para 7 noites ou mais',type:'percent',required:true,max:50},
   {id:'taticas',label:'Quais táticas você vai testar?',type:'checks',options:[{v:'fds',l:'Preço diferente no fim de semana'},{v:'feriado',l:'Pacotes de feriado'},{v:'antecedencia',l:'Preço maior para reservas de última hora em datas cheias'},{v:'direta',l:'Desconto para reserva direta (sem comissão)'},{v:'limpeza',l:'Taxa de limpeza separada'}]}
  ]},
 {kind:'feedback', title:'Teste de segurança das suas táticas',
  metrics:function(s,c){return c.pAlvo==null?[]:[{label:'Diária de fim de semana (média)',value:F.brl(c.pFds),tag:'calculado'},{label:'Diária com desconto semanal',value:F.brl(c.pSem),tag:'calculado'},{label:'Limpeza por noite na estadia mínima',value:F.brl(c.limpMin),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.pAlvo==null){o.push({lv:'bad',t:'Defina uma margem viável no Pilar 5.'});return o;}
   if(c.pSem<c.pMin) o.push({lv:'bad',t:'O desconto semanal leva a diária para '+F.brl(c.pSem)+', abaixo da mínima ('+F.brl(c.pMin)+'). Reduza o desconto.'});
   else o.push({lv:'ok',t:'O desconto semanal respeita a diária mínima.'});
   if(c.pSemBaixa<c.pMin) o.push({lv:'warn',t:'Na baixa temporada, o desconto semanal fura o piso ('+F.brl(c.pSemBaixa)+'). Não combine os dois descontos.'});
   if(s.n('est_min')===1&&c.limpN>0) o.push({lv:'info',t:'Com estadia mínima de 1 noite, a limpeza inteira pesa sobre uma diária. Considere 2 noites nos fins de semana.'});
   var t=s.v.taticas||[]; if(t.indexOf('direta')>=0) o.push({lv:'ok',t:'Reserva direta reduz comissão. Garanta que o desconto oferecido seja menor que a comissão economizada.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Aplicar a nova tabela de preços na plataforma nesta semana'},{id:'a7_2',text:'Configurar a estadia mínima definida'},{id:'a7_3',text:'Revisar os resultados depois de 30 dias e ajustar'}]}
]}
],

compute:function(s){
 var c={}; var U=s.n('unidades',1), N=s.n('noites_disp',30);
 var rows=(s.v.cf||[]).filter(function(r){return ZA.isNum(r.value)&&r.value>0;});
 c.cf=ZA.listSum(rows); c.cfItens=rows.length;
 c.cfMaior=rows.slice().sort(function(a,b){return b.value-a.value;})[0]||null;
 c.temManut=rows.some(function(r){return /manuten|reposi/i.test(r.name||'');});
 c.estadia=s.n('estadia_media',2)||2;
 c.limpN=(s.n('limpeza',0)+s.n('lavanderia',0)+s.n('amenities',0))/c.estadia;
 c.cvN=c.limpN+s.n('extra_noite',0);
 c.ded=(s.n('comissao',0)+s.n('imposto',0)+s.n('taxa_pag',0))/100;
 c.m=s.n('margem',0)/100; c.pl=s.n('prolabore',0)||0;
 var occ=(s.n('ocup_plan',50))/100; c.nv=U*N*occ;
 c.pMin=(c.nv>0&&c.ded<1)?(c.cf/c.nv+c.cvN)/(1-c.ded):null;
 c.pAlvo=(c.nv>0&&(1-c.ded-c.m)>0)?((c.cf+c.pl)/c.nv+c.cvN)/(1-c.ded-c.m):null;
 var p=s.n('diaria_atual',0);
 var contrib=p*(1-c.ded)-c.cvN; c.contrib=contrib;
 c.occBE=(contrib>0&&U*N>0)?c.cf/(U*N*contrib):null;
 var occAtual=s.has('ocup_atual')?s.n('ocup_atual')/100:occ; c.occAtualUsada=occAtual;
 c.lucroAtual=U*N*occAtual*contrib-c.cf-c.pl;
 c.lucroPlan=c.nv*contrib-c.cf-c.pl;
 // temporadas: média ponderada = diária-alvo
 var ma=s.n('meses_alta',0), mb=s.n('meses_baixa',0), mm=Math.max(0,12-ma-mb);
 var aa=s.n('aj_alta',0)/100, ab=s.n('aj_baixa',0)/100;
 if(c.pAlvo!=null){
  c.pAlta=c.pAlvo*(1+aa); c.pBaixa=c.pAlvo*(1-ab);
  c.pMedia=mm>0?(12*c.pAlvo-ma*c.pAlta-mb*c.pBaixa)/mm:c.pAlvo;
  c.baixaAbaixoMin=c.pBaixa<c.pMin; c.pBaixaF=Math.max(c.pBaixa,c.pMin||0); c.pAltaF=c.pAlta;
  if(c.pMedia<c.pMin) c.pMedia=c.pMin;
  c.pFds=c.pMedia*(1+s.n('aj_fds',0)/100);
  c.pSem=c.pMedia*(1-s.n('desc_sem',0)/100); c.pSemBaixa=c.pBaixaF*(1-s.n('desc_sem',0)/100);
 }
 c.limpMin=(s.n('limpeza',0)+s.n('lavanderia',0)+s.n('amenities',0))/Math.max(1,s.n('est_min',1));
 c.conc=s.has('preco_conc')?s.n('preco_conc'):null;
 // cenários de ocupação
 var base=s.n('ocup_plan',50);
 c.cen=[['Conservador',Math.max(5,base-15)],['Intermediário',base],['Otimista',Math.min(95,base+10)]].map(function(x){
   var nv=U*N*x[1]/100; return {nome:x[0],occ:x[1],nv:nv,
     pMin:(nv>0&&c.ded<1)?(c.cf/nv+c.cvN)/(1-c.ded):null,
     pAlvo:(nv>0&&(1-c.ded-c.m)>0)?((c.cf+c.pl)/nv+c.cvN)/(1-c.ded-c.m):null,
     receita:nv*p, resultado:nv*contrib-c.cf-c.pl};});
 return c;
},

metrics:function(s,c){return [
 {label:'Diária atual',value:F.brl(s.n('diaria_atual')),tag:'informado'},
 {label:'Diária mínima',value:F.brl(c.pMin),tag:'calculado'},
 {label:'Diária-alvo',value:c.pAlvo==null?'inviável':F.brl(c.pAlvo),tag:'calculado'},
 {label:'Custo fixo mensal',value:F.brl(c.cf),tag:'calculado'},
 {label:'Custo variável por noite',value:F.brl(c.cvN),tag:s.unknown('estadia_media')?'estimativa':'calculado'},
 {label:'Deduções',value:F.pct(c.ded*100),tag:'calculado'},
 {label:'Ocupação de equilíbrio (preço atual)',value:c.occBE==null?'inalcançável':F.pct(c.occBE*100),tag:'calculado'},
 {label:'Resultado mensal estimado (preço atual)',value:F.brl(c.lucroAtual),tag:'estimativa'}
];},

priorities:function(s,c){var p=s.n('diaria_atual',0),L=[];
 if(c.pMin!=null&&p<c.pMin) L.push({title:'Elevar a diária média para no mínimo '+F.brl(c.pMin),why:'Hoje cada mês fecha no negativo na ocupação planejada.',score:10});
 if(c.pAlvo==null) L.push({title:'Rever margem desejada e deduções',why:'A combinação atual torna a meta matematicamente impossível.',score:9});
 else if(p<c.pAlvo) L.push({title:'Caminhar a diária média em direção a '+F.brl(c.pAlvo),why:'É a diária que entrega a margem desejada.',score:p<c.pMin?6:8});
 if(s.unknown('ocup_atual')) L.push({title:'Medir a ocupação real dos últimos 6 meses',why:'Sem ela, o preço é calculado sobre uma suposição.',score:7});
 if(c.cfItens<3) L.push({title:'Completar o levantamento de custos fixos',why:'Custos ausentes fazem a diária mínima parecer menor do que é.',score:7});
 if(c.occBE!=null&&c.occBE>0.6&&c.occBE<=1) L.push({title:'Reduzir o custo fixo ou elevar a contribuição por noite',why:'O equilíbrio exige '+F.pct(c.occBE*100,0)+' de ocupação.',score:6});
 if(c.ded>0.2) L.push({title:'Aumentar reservas diretas para reduzir comissões',why:'Deduções de '+F.pct(c.ded*100,0)+' sobre cada diária.',score:5});
 if(['concorrente','intuicao'].indexOf(s.t('metodo'))>=0) L.push({title:'Adotar a diária mínima como piso em qualquer ferramenta ou desconto',why:'O preço atual não nasce dos seus custos.',score:6});
 if(p>0&&c.limpN>p*0.2) L.push({title:'Definir estadia mínima ou taxa de limpeza separada',why:'A limpeza pesa '+F.brl(c.limpN)+' por noite.',score:5});
 if(s.n('aj_alta',0)===0) L.push({title:'Criar preço de alta temporada e feriados',why:'Receita não capturada nas datas de maior procura.',score:4});
 if(c.baixaAbaixoMin) L.push({title:'Reduzir o desconto da baixa temporada',why:'O preço de baixa fura a diária mínima.',score:6});
 if(s.unknown('preco_conc')) L.push({title:'Pesquisar preços de 5 concorrentes nas mesmas datas',why:'Falta referência de mercado para posicionar.',score:3});
 if(s.t('posic')==='premium'&&c.conc!=null&&c.pAlvo!=null&&c.pAlvo<c.conc) L.push({title:'Alinhar preço ao posicionamento premium',why:'Preço abaixo do mercado contradiz o posicionamento.',score:4});
 if(!c.temManut) L.push({title:'Criar reserva mensal de manutenção',why:'Protege a margem de gastos inesperados.',score:3});
 return L;},

report:function(s,c){
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Unidades',F.num(s.n('unidades')),'<span class="za-tag informado">informado</span>'],
  ['Noites disponíveis/mês por unidade',F.num(s.n('noites_disp')),'<span class="za-tag informado">informado</span>'],
  ['Ocupação planejada',F.pct(s.n('ocup_plan'),0),'<span class="za-tag informado">informado</span>'],
  ['Ocupação atual usada no resultado',F.pct(c.occAtualUsada*100,0),s.has('ocup_atual')?'<span class="za-tag informado">informado</span>':'<span class="za-tag hipotese">hipótese = planejada</span>'],
  ['Estadia média',F.num(c.estadia,1)+' noites',s.unknown('estadia_media')?'<span class="za-tag hipotese">hipótese</span>':'<span class="za-tag informado">informado</span>'],
  ['Custo fixo mensal',F.brl(c.cf),'<span class="za-tag calculado">calculado</span>'],
  ['Custo variável por noite',F.brl(c.cvN),'<span class="za-tag calculado">calculado</span>'],
  ['Deduções (comissão + imposto + taxa)',F.pct(c.ded*100),'<span class="za-tag calculado">calculado</span>'],
  ['Margem desejada',F.pct(c.m*100,0),'<span class="za-tag informado">informado</span>'],
  ['Pró-labore',F.brl(c.pl),'<span class="za-tag informado">informado</span>']],[1]);
 var tab=c.pAlvo==null?'<p class="za-missing">A diária-alvo é inviável com as premissas atuais (deduções + margem ≥ 100%).</p>':ZA.table(['Situação','Diária'],[
  ['Diária mínima (piso absoluto)',F.brl(c.pMin)],['Diária-alvo (média do ano)',F.brl(c.pAlvo)],
  ['Alta temporada ('+F.num(s.n('meses_alta'))+' meses)',F.brl(c.pAltaF)],['Temporada média',F.brl(c.pMedia)],['Baixa temporada ('+F.num(s.n('meses_baixa'))+' meses)',F.brl(c.pBaixaF)],
  ['Sexta e sábado (temporada média)',F.brl(c.pFds)],['Estadias de 7+ noites',F.brl(c.pSem)]],[1]);
 var cen=ZA.table(['Cenário','Ocupação','Diária mínima','Diária-alvo','Resultado/mês no preço atual'],c.cen.map(function(x){return [x.nome,F.pct(x.occ,0),F.brl(x.pMin),x.pAlvo==null?'inviável':F.brl(x.pAlvo),F.brl(x.resultado)];}),[1,2,3,4]);
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido de 30 dias</b><ol><li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Confirmar os dados informados')+'.</li><li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Aplicar a tabela de temporadas')+'.</li><li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Configurar estadia mínima e fim de semana')+'.</li><li><b>Semana 4:</b> medir ocupação, diária média e resultado do mês; refazer o Precificador com os números reais.</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Sua tabela de preços',html:tab+'<p class="za-small">Regra de ouro: nenhuma noite abaixo da diária mínima de '+F.brl(c.pMin)+'.</p>'},
  {title:'Cenários de ocupação',html:cen+'<p class="za-small">Conservador = ocupação planejada −15 p.p.; otimista = +10 p.p. Cenários ilustrativos, não previsões.</p>'}
 ],plan:plan};
}
});
})();
