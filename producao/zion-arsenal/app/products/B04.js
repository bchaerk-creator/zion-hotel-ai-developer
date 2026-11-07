/* ZAR-B04 · Tenho Terra, mas Não Tenho Dinheiro. E Agora? · Mapa de Alternativas de Capital */
(function(){
var F=ZA.fmt, esc=ZA.esc;
function tag(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';}
function esc5(lo,hi){return [1,2,3,4,5].map(function(k){return {v:String(k),l:k+(k===1?' · '+lo:k===5?' · '+hi:'')};});}
function sc(s,id,def){var x=Number(s.t(id));return (s.t(id)!==''&&isFinite(x))?x:def;}
var SNT={sim:1,talvez:0.5,nao:0};

var ALT=[
 {k:'proprios',n:'Recursos próprios',d:'Você financia com o que tem, no ritmo do seu caixa.',rel:'',quem:'Você e seu contador (planejamento do caixa)'},
 {k:'parceria',n:'Parceria / sociedade',d:'Um sócio entra com capital (e talvez gestão) em troca de participação.',rel:'B02 · Simulador de Sociedade e Parcerias',quem:'Advogado e contador'},
 {k:'arrendamento',n:'Arrendamento ou cessão de uso',d:'Um operador implanta e opera; você recebe pelo uso da área.',rel:'',quem:'Advogado'},
 {k:'permuta',n:'Permuta',d:'Você cede parte da área ou de direitos em troca de construção ou unidades prontas.',rel:'',quem:'Advogado, contador e engenheiro'},
 {k:'financiamento',n:'Financiamento',d:'Crédito pago em parcelas; exige renda, garantias e cadastro.',rel:'',quem:'Seu banco ou cooperativa e seu contador'},
 {k:'progressiva',n:'Implantação progressiva',d:'Começar com a menor etapa que funciona e crescer com a receita.',rel:'B09 · Planejador de Implantação Progressiva',quem:'Arquiteto ou engenheiro (projeto por etapas)'}];
var BONUS={controle:['proprios','progressiva','financiamento'],rapidez:['parceria','financiamento'],risco:['arrendamento','progressiva'],terra:['proprios','financiamento','progressiva','arrendamento']};

ZA.register({
id:'B04', code:'ZAR-B04', collection:'Terrenos',
title:'Tenho Terra, mas Não Tenho Dinheiro. E Agora?',
subtitle:'Alternativas para Desenvolver Sua Propriedade',
tool:'Mapa de Alternativas de Capital',
deliverable:'Mapa de Alternativas de Capitalização',
nameField:'nome', propertyField:'propriedade',
disclaimer:'O Mapa de Alternativas pontua a aderência de cada caminho ao seu perfil, com base nas suas respostas e numa ponderação orientativa da metodologia Zion. Ele não é recomendação de investimento, não indica linhas de crédito nem condições de bancos, e não garante captação, aprovação de crédito, aprovação de licenças ou retorno. Taxas e prazos usados nos cálculos são os que você informou a partir de simulações próprias. Antes de contratar crédito, sociedade, arrendamento ou permuta, consulte contador e advogado habilitados.',

intro:[
 {kind:'mirror', title:'Sua terra está parada porque você acredita que precisa pagar tudo sozinho?',
  lead:'Você tem a área, tem a ideia, talvez até um desenho das cabanas. Mas a conta da obra é muito maior que as suas economias, e o projeto fica sempre para “quando sobrar dinheiro”.',
  body:'<div class="za-card"><p>Pensamentos comuns de quem está nesse ponto:</p><ul><li>“Financiamento é perigoso, sociedade dá briga, então não faço nada.”</li><li>“Só conheço duas opções: juntar dinheiro ou vender a terra.”</li><li>“Não sei se alguém aceitaria a minha terra como parte do negócio.”</li><li>“Não sei quanto eu conseguiria pagar por mês.”</li></ul></div>'},
 {kind:'collapse', title:'Desenvolver um empreendimento não significa necessariamente financiar cada etapa com recursos próprios.',
  lead:'Existem pelo menos seis caminhos para capitalizar um projeto em terra própria. Cada um combina melhor com um perfil, um nível de risco e um grau de controle.',
  body:'<div class="za-card"><p>Os seis caminhos que você vai avaliar:</p><ol>'+ALT.map(function(a){return '<li><b>'+a.n+':</b> '+a.d+'</li>';}).join('')+'</ol><p>O Mapa pontua de 0 a 100 a <b>aderência</b> de cada alternativa ao seu caso e monta uma estrutura de capital preliminar combinando as mais aderentes. Nada aqui é promessa de que um caminho vai dar certo: é um mapa para decidir por onde começar.</p></div>'},
 {kind:'start', title:'Vamos mapear as suas alternativas de capital',
  lead:'Em 7 pilares, você faz o diagnóstico financeiro, avalia a terra como ativo e testa cada alternativa.',
  body:'<p>Se tiver uma simulação de financiamento feita em banco ou cooperativa, deixe à mão: a taxa e o prazo que você recebeu entram no cálculo. Se não tiver, marque “não sei”.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Cláudio'},
   {id:'propriedade',label:'Nome da terra ou do projeto',type:'text',required:true,placeholder:'Ex.: Sítio Três Pedras'},
   {id:'cidade',label:'Município e estado',type:'text',required:true,placeholder:'Ex.: Rancho Queimado (SC)'},
   {id:'estagio',label:'Em que estágio está o projeto?',type:'radio',required:true,options:[{v:'ideia',l:'Só a ideia'},{v:'conceito',l:'Conceito definido (modelo, unidades)'},{v:'orcado',l:'Já tenho orçamentos'}]}
  ]}
],

pillars:[
/* 1 */
{title:'Diagnóstico financeiro', screens:[
 {kind:'learn', title:'Antes de buscar dinheiro, saiba quanto falta e quanto você aguenta',
  body:'<p>Três números orientam todo o mapa:</p><ul><li><b>Necessidade:</b> quanto o projeto (ou a primeira etapa) custa.</li><li><b>Recursos próprios:</b> quanto você pode colocar sem comprometer sua reserva de emergência.</li><li><b>Capacidade de pagamento:</b> quanto você conseguiria pagar por mês, com folga, se usasse crédito.</li></ul><div class="za-card"><b>Lacuna de capital = Necessidade − Recursos próprios</b></div><p>É essa lacuna que as outras alternativas precisam cobrir. Também conta o seu <b>apetite por dívida</b>: há quem durma tranquilo com parcelas e há quem não durma.</p>',
  example:'Exemplo: projeto de R$ 500 mil, R$ 60 mil disponíveis. A lacuna é de R$ 440 mil. Com capacidade de R$ 3.000 por mês, só uma parte dela caberia em crédito; o restante precisa vir de outro caminho ou de etapas menores.'},
 {kind:'compare', title:'Diagnóstico que engana × diagnóstico honesto',
  cols:[{h:'Engana',type:'bad',items:['Colocar todas as economias, inclusive a reserva','Calcular a parcela com a renda dos melhores meses','Ignorar que a obra pode atrasar e a receita demorar']},
        {h:'Honesto',type:'good',items:['Separar a reserva de emergência antes','Capacidade de pagamento com a renda dos meses fracos','Considerar meses sem receita no início da operação']}]},
 {kind:'form', title:'Seu ponto de partida financeiro',
  fields:[
   {id:'necessidade',label:'Investimento necessário (projeto completo ou primeira etapa)',type:'money',required:true,allowUnknown:true,help:'Se não souber, o B06 ajuda a montar o orçamento.'},
   {id:'recursos',label:'Recursos próprios disponíveis para o projeto',type:'money',required:true,help:'Sem contar sua reserva de emergência. Pode ser zero.'},
   {id:'parcela_max',label:'Parcela mensal que você conseguiria pagar com folga',type:'money',required:true,help:'Use a renda dos meses mais fracos. Pode ser zero.'},
   {id:'reserva',label:'Você tem reserva de emergência separada?',type:'radio',required:true,options:[{v:'sim',l:'Sim'},{v:'nao',l:'Não'}]},
   {id:'tol_divida',label:'Seu conforto com dívidas (1 a 5)',type:'radio',required:true,options:esc5('evito qualquer dívida','confortável com parcelas planejadas')}
  ]},
 {kind:'feedback', title:'Sua lacuna de capital',
  metrics:function(s,c){return [{label:'Necessidade',value:F.brl0(c.need),tag:c.needOrig==='f1'?'estimativa':'informado'},{label:'Recursos próprios',value:F.brl0(s.n('recursos')),tag:'informado'},{label:'Lacuna de capital',value:F.brl0(c.gap),tag:'calculado'},{label:'Cobertura própria',value:c.need?F.pct(c.cobProp*100,0):'—',tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.need==null) o.push({lv:'warn',t:'Sem a necessidade de investimento, o mapa compara alternativas pelo seu perfil, mas não consegue dimensionar quanto cada uma cobriria. Monte um orçamento preliminar.'});
   else if(c.gap===0) o.push({lv:'ok',t:'Seus recursos cobrem a necessidade informada. Avalie se vale manter parte em caixa como reserva do projeto.'});
   else o.push({lv:'info',t:'Seus recursos cobrem '+F.pct(c.cobProp*100,0)+' da necessidade. A lacuna de '+F.brl0(c.gap)+' é o que o mapa vai tentar distribuir entre as alternativas.'});
   if(s.t('reserva')==='nao') o.push({lv:'warn',t:'Sem reserva de emergência, qualquer imprevisto vira dívida cara. Considere separar uma reserva antes de colocar dinheiro no projeto.'});
   if(sc(s,'tol_divida',3)<=2&&s.n('parcela_max',0)>0) o.push({lv:'info',t:'Você tem capacidade de pagamento, mas pouco conforto com dívida. O mapa vai pesar menos o financiamento.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Separar a reserva de emergência antes de definir quanto vai ao projeto'},{id:'a1_2',text:'Calcular a capacidade de pagamento com a renda dos meses mais fracos'},{id:'a1_3',text:'Montar ou revisar o orçamento do projeto e da primeira etapa'}]}
]},
/* 2 */
{title:'O terreno como ativo', screens:[
 {kind:'learn', title:'Sua terra pode ser mais que o lugar da obra: pode ser parte da solução',
  body:'<p>Para quem tem terra e pouco dinheiro, a própria terra costuma ser o principal ativo de negociação. Ela pode entrar como:</p><ul><li><b>Participação</b> numa sociedade (você cede parte da propriedade ou dos direitos ao projeto);</li><li><b>Direito de uso</b> num arrendamento (a terra continua sua);</li><li><b>Moeda de troca</b> numa permuta (área por construção);</li><li><b>Garantia</b> em algumas operações de crédito, conforme exigências de cada instituição.</li></ul><p>Para tudo isso, a <b>documentação</b> pesa muito: terra com pendência vale menos como ativo de negociação e pode não ser aceita como garantia. Quem confirma a situação é o cartório e um advogado.</p>',
  example:'Exemplo: dois proprietários com terras de mesmo valor. Um aceita ceder participação; o outro não aceita dividir a propriedade, mas aceita ceder o uso por 15 anos. Para o primeiro, sociedade e permuta ganham aderência; para o segundo, arrendamento.'},
 {kind:'compare', title:'O que você aceita ceder muda o mapa',
  cols:[{h:'Não aceito ceder nada',items:['Restam recursos próprios, financiamento e etapas','Controle total, mas capital limitado','O ritmo depende do seu caixa e do crédito']},
        {h:'Aceito ceder participação ou uso',items:['Abrem-se sociedade, permuta e arrendamento','Menos capital próprio necessário','Exige contratos bem desenhados com advogado']}]},
 {kind:'form', title:'Sua terra na negociação',
  fields:[
   {id:'valor_terra',label:'Valor de referência da terra',type:'money',required:true,allowUnknown:true},
   {id:'doc_status',label:'Situação da propriedade, pelo que você sabe',type:'radio',required:true,allowUnknown:true,options:[{v:'regular',l:'Matrícula em meu nome, sem pendência conhecida'},{v:'parcial',l:'Há algo a resolver (inventário, escritura, divisão)'},{v:'irregular',l:'Só posse ou contrato particular'}]},
   {id:'cede_parte',label:'Você aceitaria dividir a propriedade ou ceder participação no projeto?',type:'radio',required:true,options:[{v:'sim',l:'Sim'},{v:'talvez',l:'Talvez, dependendo das condições'},{v:'nao',l:'Não'}]},
   {id:'cede_uso',label:'Você aceitaria ceder o uso da área a um operador por um prazo?',type:'radio',required:true,options:[{v:'sim',l:'Sim'},{v:'talvez',l:'Talvez'},{v:'nao',l:'Não'}]}
  ]},
 {kind:'feedback', title:'A força da terra como ativo',
  metrics:function(s,c){return [{label:'Valor da terra',value:F.brl0(s.n('valor_terra')),tag:'informado'},{label:'Terra ÷ lacuna',value:c.terraGap==null?'—':F.num(c.terraGap,2)+'×',tag:'calculado'},{label:'Fator documental',value:F.pct(c.docF*100,0),tag:'recomendacao'}];},
  feedback:function(s,c){var o=[];
   if(s.unknown('doc_status')) o.push({lv:'bad',t:'Situação documental desconhecida. Ela reduz a aderência de quase todas as alternativas que usam a terra. Peça a certidão da matrícula e leve a um advogado.'});
   else if(s.t('doc_status')==='irregular') o.push({lv:'bad',t:'Posse sem registro limita muito sociedade, permuta, arrendamento formal e crédito com garantia. Regularizar (com advogado) pode ser o primeiro “investimento”.'});
   else if(s.t('doc_status')==='parcial') o.push({lv:'warn',t:'Há pendência documental. Ela não fecha portas, mas parceiros e instituições vão querer saber prazo e custo para resolver.'});
   else o.push({lv:'ok',t:'Documentação sem pendência conhecida: a terra pode ser usada com mais liberdade como ativo de negociação.'});
   if(c.terraGap!=null) o.push({lv:'info',t:'O valor de referência da terra equivale a '+F.num(c.terraGap,2)+' vez(es) a sua lacuna de capital. '+(c.terraGap>=1?'Como ativo de negociação, ela tem peso relevante frente ao que falta.':'Mesmo cedendo parte da terra, provavelmente será preciso combinar com outras alternativas.')});
   if(s.t('cede_parte')==='nao'&&s.t('cede_uso')==='nao') o.push({lv:'info',t:'Você não aceita ceder participação nem uso. Restam principalmente recursos próprios, financiamento e implantação progressiva.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Atualizar a certidão de matrícula e verificar pendências com advogado'},{id:'a2_2',text:'Obter referência de valor da terra com corretores ou avaliador'},{id:'a2_3',text:'Decidir até onde aceito ceder: participação, uso ou nada'}]}
]},
/* 3 */
{title:'Parcerias', screens:[
 {kind:'learn', title:'Parceria troca capital por participação, e um pouco de controle',
  body:'<p>Numa sociedade, o parceiro entra com dinheiro (e às vezes gestão) e recebe uma parte do projeto. Em troca, você passa a dividir decisões. A aderência dessa alternativa depende de três fatores:</p><ul><li><b>Aceitar ceder participação</b> (Pilar 2): 40 pontos.</li><li><b>Pouca necessidade de controle total</b>: 30 pontos.</li><li><b>Rede de contatos</b> com possíveis parceiros: 30 pontos.</li></ul><p>A soma é multiplicada pelo <b>fator documental</b>: terra com pendência reduz a aderência.</p><p>Permuta usa os mesmos ingredientes de outra forma: você cede área em troca de obra, então pesa mais a disposição de ceder e a documentação.</p>',
  example:'Exemplo: proprietário que aceita “talvez” ceder participação (20 de 40), dá muita importância ao controle (7,5 de 30) e conhece algumas pessoas (15 de 30) tem aderência 42,5/100 à parceria, antes do fator documental.'},
 {kind:'compare', title:'Parceria × permuta',
  cols:[{h:'Parceria / sociedade',items:['Parceiro coloca capital e divide resultado','Você continua sócio do negócio inteiro','Exige governança e regras de saída']},
        {h:'Permuta',items:['Construtor ou investidor faz a obra e fica com parte da área ou das unidades','Você recebe unidades prontas, sem colocar dinheiro','Exige definição precisa do que cada parte recebe']}]},
 {kind:'form', title:'Seu perfil para parcerias',
  fields:[
   {id:'controle',label:'Importância de manter o controle total das decisões (1 a 5)',type:'radio',required:true,options:esc5('pouca','total')},
   {id:'rede',label:'Você conhece pessoas que poderiam ser sócias do projeto?',type:'radio',required:true,options:[{v:'sim',l:'Sim, conheço mais de uma'},{v:'algum',l:'Conheço uma ou outra'},{v:'nao',l:'Não conheço'}]},
   {id:'quer_operar',label:'Você quer operar a hospedagem no dia a dia?',type:'radio',required:true,options:[{v:'sim',l:'Sim'},{v:'nao',l:'Não'}]}
  ]},
 {kind:'feedback', title:'Aderência a parceria e permuta',
  metrics:function(s,c){return [{label:'Parceria / sociedade',value:F.num(c.alt.parceria,0)+'/100',tag:'calculado'},{label:'Permuta',value:F.num(c.alt.permuta,0)+'/100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.alt.parceria>=60) o.push({lv:'ok',t:'Boa aderência à parceria ('+F.num(c.alt.parceria,0)+'/100). O B02 · Simulador de Sociedade e Parcerias ajuda a valorar contribuições e montar a proposta.'});
   else if(c.alt.parceria>=35) o.push({lv:'info',t:'Aderência média à parceria ('+F.num(c.alt.parceria,0)+'/100).'+(c.ctrl>=0.75?' O desejo de controle total é o fator que mais pesa contra.':'')});
   else o.push({lv:'warn',t:'Baixa aderência à parceria ('+F.num(c.alt.parceria,0)+'/100) com o seu perfil atual.'});
   if(s.t('rede')==='nao') o.push({lv:'info',t:'Sem rede de contatos, a parceria fica mais lenta. Associações comerciais e de turismo da região são um ponto de partida.'});
   if(s.t('quer_operar')==='sim'&&s.t('cede_uso')==='sim') o.push({lv:'info',t:'Você quer operar, mas aceita ceder o uso. No arrendamento quem opera é o arrendatário: avalie o que pesa mais para você.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Listar 5 pessoas ou empresas que poderiam ser parceiras'},{id:'a3_2',text:'Definir quais decisões abro mão de tomar sozinho'},{id:'a3_3',text:'Pesquisar se construtores da região fazem permuta em projetos rurais'}]}
]},
/* 4 */
{title:'Arrendamento', screens:[
 {kind:'learn', title:'Arrendamento: a terra trabalha, outro opera',
  body:'<p>No arrendamento (ou cessão de uso), um operador implanta e opera a hospedagem na sua área por um prazo e paga por esse uso. Você não precisa de capital, não opera e não corre o risco do negócio, mas também não participa do resultado além do valor combinado.</p><p>Pontos de atenção:</p><ul><li><b>Prazo:</b> quem investe em construções precisa de tempo para recuperar o investimento. Prazos curtos costumam afastar operadores.</li><li><b>Benfeitorias:</b> o contrato deve dizer de quem são as construções ao fim do prazo.</li><li><b>Demanda de operadores:</b> há empresas de turismo procurando áreas na sua região?</li></ul><p>A aderência pondera: aceitar ceder o uso (40), preferência por renda sem operar (30) e sinais de operadores interessados (30), multiplicados pelo fator documental.</p>',
  example:'Exemplo: proprietário que aceita ceder o uso (40), tem pouca preferência por renda passiva (7,5 de 30) e não sabe se há operadores na região (15 de 30) tem aderência de 62,5/100.'},
 {kind:'compare', title:'Arrendamento bem e mal desenhado',
  cols:[{h:'Mal desenhado',type:'bad',items:['Prazo curto demais para o operador investir','Nada dito sobre benfeitorias','Valor sem reajuste','Sem regras sobre uso da área e preservação']},
        {h:'Bem desenhado',type:'good',items:['Prazo coerente com o investimento do operador','Destino das construções definido','Reajuste e garantias previstos','Contrato revisado por advogado']}]},
 {kind:'form', title:'Seu perfil para arrendamento',
  fields:[
   {id:'interesse_renda',label:'Preferência por renda sem operar (1 a 5)',type:'radio',required:true,options:esc5('quero participar do negócio','prefiro só receber pelo uso')},
   {id:'prazo_cessao',label:'Por quantos anos você aceitaria ceder o uso?',type:'number',required:true,min:0,max:99,step:1,unit:'anos',help:'Zero = não aceito.'},
   {id:'demanda_operador',label:'Há operadores de turismo procurando áreas na região?',type:'radio',required:true,options:[{v:'sim',l:'Sim, já soube de interessados'},{v:'nao_sei',l:'Não sei'},{v:'nao',l:'Não'}]}
  ]},
 {kind:'feedback', title:'Aderência ao arrendamento',
  metrics:function(s,c){return [{label:'Arrendamento',value:F.num(c.alt.arrendamento,0)+'/100',tag:'calculado'},{label:'Prazo aceito',value:F.num(s.n('prazo_cessao'))+' anos',tag:'informado'}];},
  feedback:function(s,c){var o=[];var p=s.n('prazo_cessao',0);
   if(s.t('cede_uso')==='nao'||p===0) o.push({lv:'info',t:'Você não aceita ceder o uso, então o arrendamento tem aderência limitada no seu caso.'});
   else if(p<10) o.push({lv:'warn',t:'Prazo de '+F.num(p)+' anos pode ser curto para um operador que vai construir. Confirme com operadores reais qual prazo eles consideram, e defina com advogado o destino das benfeitorias.'});
   else o.push({lv:'ok',t:'Prazo de '+F.num(p)+' anos: tende a ser compatível com quem investe em construções. Defina com advogado o destino das benfeitorias.'});
   if(s.t('demanda_operador')==='nao_sei') o.push({lv:'info',t:'Descubra se há operadores interessados: converse com hospedagens maiores da região e com a associação de turismo local.'});
   if(c.alt.arrendamento>=60) o.push({lv:'ok',t:'Aderência de '+F.num(c.alt.arrendamento,0)+'/100: o arrendamento é um caminho real para você.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Conversar com 2 operadores da região sobre interesse e prazo'},{id:'a4_2',text:'Definir o que acontece com as construções ao fim do contrato'},{id:'a4_3',text:'Levar qualquer proposta de arrendamento para revisão de advogado'}]}
]},
/* 5 */
{title:'Financiamento', screens:[
 {kind:'learn', title:'Financiamento: quanto da lacuna cabe na sua parcela',
  body:'<p>Crédito é uma ferramenta, não um vilão nem uma solução mágica. A pergunta certa é: <b>quanto da minha lacuna cabe numa parcela que eu consigo pagar mesmo se a hospedagem demorar a gerar receita?</b></p><p>O Mapa calcula o <b>valor financiável</b> com a sua parcela máxima e a <b>taxa e o prazo de uma simulação que você mesmo fez</b> em banco ou cooperativa:</p><div class="za-card"><b>Valor financiável = Parcela × [1 − (1 + taxa)<sup>−prazo</sup>] ÷ taxa</b></div><p>Esta mini mentoria não indica linhas de crédito nem taxas: cada instituição tem condições próprias, que mudam com o tempo e com o seu perfil. Faça simulações e leve-as ao seu contador.</p>',
  example:'Exemplo ilustrativo: parcela de R$ 3.000, taxa de 1,5% ao mês e 120 meses resultam em cerca de R$ 166 mil financiáveis. Sem a taxa, o teto “parcela × prazo” (R$ 360 mil) superestima muito o valor.'},
 {kind:'compare', title:'Crédito perigoso × crédito planejado',
  cols:[{h:'Perigoso',type:'bad',items:['Parcela que depende da hospedagem já estar cheia','Começar a pagar antes de a obra terminar, sem reserva','Comparar só a taxa, sem o custo total','Dar a terra em garantia sem entender as consequências']},
        {h:'Planejado',type:'good',items:['Parcela paga com a renda atual, com folga','Carência ou reserva para o período de obra','Custo efetivo total comparado entre instituições','Garantias analisadas com contador e advogado']}]},
 {kind:'form', title:'Seu perfil para crédito',
  fields:[
   {id:'renda_comprovavel',label:'Você tem renda que consegue comprovar?',type:'radio',required:true,options:[{v:'sim',l:'Sim, formal'},{v:'parcial',l:'Parcialmente'},{v:'nao',l:'Não'}]},
   {id:'credito',label:'Situação do seu cadastro de crédito',type:'radio',required:true,options:[{v:'limpo',l:'Sem restrições'},{v:'nao_sei',l:'Não sei'},{v:'restricao',l:'Com restrições'}]},
   {id:'taxa_mensal',label:'Taxa de juros mensal de uma simulação que você fez',type:'percent',required:true,allowUnknown:true,max:10,step:'any',help:'Use o número da sua simulação (custo efetivo, se tiver). Não usamos taxas de referência.'},
   {id:'prazo_fin',label:'Prazo dessa simulação (ou o prazo que você consideraria)',type:'number',required:true,min:1,max:420,step:1,unit:'meses'}
  ]},
 {kind:'feedback', title:'Quanto o crédito poderia cobrir',
  metrics:function(s,c){return [{label:'Valor financiável',value:c.capFin==null?'—':F.brl0(c.capFin),tag:c.capFin==null?'hipotese':'calculado'},{label:'Teto sem juros (parcela × prazo)',value:F.brl0(c.teto),tag:'calculado'},{label:'Cobertura da lacuna',value:c.covFinTxt,tag:'calculado'},{label:'Financiamento',value:F.num(c.alt.financiamento,0)+'/100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.capFin==null) o.push({lv:'warn',t:'Sem taxa de uma simulação real, só é possível mostrar o teto sem juros ('+F.brl0(c.teto)+'), que superestima o valor. Faça ao menos duas simulações em instituições diferentes.'});
   else if(c.gap!=null&&c.gap>0) o.push({lv:'info',t:'Com a sua parcela, a taxa e o prazo informados, o crédito cobriria cerca de '+F.brl0(c.capFin)+' ('+c.covFinTxt+' da lacuna).'});
   if(s.n('parcela_max',0)===0) o.push({lv:'warn',t:'Parcela máxima zero: no momento, o crédito não é uma alternativa para você.'});
   if(s.t('credito')==='restricao') o.push({lv:'bad',t:'Com restrição no cadastro, o crédito tende a ser mais difícil e mais caro. Resolver as pendências vem antes.'});
   if(s.t('renda_comprovavel')==='nao') o.push({lv:'warn',t:'Sem renda comprovável, instituições costumam exigir outras garantias. Converse com seu contador sobre como organizar a comprovação.'});
   if(sc(s,'tol_divida',3)<=2) o.push({lv:'info',t:'Seu conforto com dívida é baixo. Mesmo que o crédito seja possível, ele pode não ser o melhor caminho para você.'});
   o.push({lv:'info',t:'Lembre: a parcela começa a correr, em geral, antes de a hospedagem gerar receita. Pergunte sobre carência e mantenha reserva para o período de obra.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Fazer simulações em pelo menos duas instituições e comparar o custo efetivo total'},{id:'a5_2',text:'Consultar meu cadastro de crédito e resolver pendências'},{id:'a5_3',text:'Levar as simulações ao contador antes de decidir'}]}
]},
/* 6 */
{title:'Implantação progressiva', screens:[
 {kind:'learn', title:'Começar menor também é uma forma de capitalizar',
  body:'<p>Se a lacuna é grande, outra saída é <b>diminuir a necessidade</b>: começar com a menor etapa que já funciona como hospedagem (uma ou duas unidades, infraestrutura essencial) e usar o resultado dela para ajudar nas etapas seguintes.</p><p>A aderência considera:</p><ul><li><b>Cobertura da etapa 1 pelos seus recursos</b> (50 pontos);</li><li><b>Prazo que você aceita para chegar ao projeto completo</b> (25 pontos, máximo com 5 anos ou mais);</li><li><b>Disposição de reinvestir o resultado</b> das primeiras unidades (25 pontos).</li></ul><p>A implantação progressiva pode ser combinada com qualquer outra alternativa: uma etapa 1 menor também exige menos crédito ou menos participação de sócio.</p>',
  example:'Exemplo: etapa 1 de R$ 150 mil, recursos de R$ 60 mil (cobertura de 40% = 20 pontos), aceita 5 anos para crescer (25) e reinveste tudo (25): aderência de 70/100.'},
 {kind:'compare', title:'Etapa 1 mal escolhida × bem escolhida',
  cols:[{h:'Mal escolhida',type:'bad',items:['Uma unidade sem infraestrutura que permita expandir','Etapa que não funciona sozinha (só fundações, só estrada)','Projeto que precisa ser refeito para crescer']},
        {h:'Bem escolhida',type:'good',items:['Unidades que já recebem hóspedes','Infraestrutura dimensionada pensando nas próximas etapas','Projeto geral aprovado, executado por partes']}]},
 {kind:'form', title:'Sua primeira etapa possível',
  fields:[
   {id:'custo_f1',label:'Custo da menor etapa que já funcionaria como hospedagem',type:'money',required:true,allowUnknown:true},
   {id:'prazo_crescer',label:'Em quantos anos você aceitaria chegar ao projeto completo?',type:'number',required:true,min:0,max:30,step:1,unit:'anos'},
   {id:'reinvestir',label:'Você reinvestiria o resultado das primeiras unidades?',type:'radio',required:true,options:[{v:'sim',l:'Sim, todo'},{v:'parcial',l:'Em parte'},{v:'nao',l:'Não, preciso dessa renda'}]}
  ]},
 {kind:'feedback', title:'Aderência à implantação progressiva',
  metrics:function(s,c){return [{label:'Implantação progressiva',value:F.num(c.alt.progressiva,0)+'/100',tag:'calculado'},{label:'Cobertura da etapa 1',value:c.f1==null?'—':F.pct(c.f1cov*100,0),tag:'calculado'},{label:'Falta para a etapa 1',value:c.f1==null?'—':F.brl0(Math.max(0,c.f1-s.n('recursos',0))),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.f1==null) o.push({lv:'warn',t:'Sem o custo da menor etapa possível, não dá para medir a implantação progressiva. Peça orçamento para 1 ou 2 unidades com a infraestrutura essencial.'});
   else if(c.f1cov>=1) o.push({lv:'ok',t:'Seus recursos já cobrem a primeira etapa. Começar pequeno pode ser o caminho mais direto para tirar o projeto do papel.'});
   else o.push({lv:'info',t:'Seus recursos cobrem '+F.pct(c.f1cov*100,0)+' da primeira etapa. Uma combinação com crédito ou parceiro menor pode completar.'});
   if(c.need!=null&&c.f1!=null&&c.f1>=c.need&&c.needOrig!=='f1') o.push({lv:'warn',t:'A etapa 1 custa o mesmo que o projeto todo. Reveja: qual é o mínimo que já recebe hóspedes?'});
   if(s.t('reinvestir')==='nao') o.push({lv:'info',t:'Sem reinvestimento, as próximas etapas vão depender de novos recursos. Isso alonga o prazo de expansão.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Definir a menor etapa que já recebe hóspedes'},{id:'a6_2',text:'Pedir orçamento só para essa etapa, com infraestrutura pensada para crescer'},{id:'a6_3',text:'Conhecer o B09 · Planejador de Implantação Progressiva para detalhar as fases'}]}
]},
/* 7 */
{title:'Plano de capitalização', screens:[
 {kind:'learn', title:'O plano raramente é uma alternativa só: é uma combinação',
  body:'<p>Com as aderências calculadas, o Mapa ordena as alternativas e monta uma <b>estrutura de capital preliminar</b>:</p><ol><li>Primeiro, seus <b>recursos próprios</b> (até a necessidade).</li><li>Depois, o <b>financiamento</b> que cabe na sua parcela, se a aderência ao crédito for de pelo menos 50/100.</li><li>O restante é a <b>lacuna a cobrir</b> com parceria, permuta, arrendamento ou redução por etapas.</li></ol><p>Sua <b>prioridade</b> também conta: quem quer manter controle, quem quer rapidez, quem quer menor risco e quem quer manter a terra 100% sua recebem um ajuste (+10) nas alternativas mais coerentes com isso.</p>',
  example:'Exemplo: necessidade de R$ 500 mil, R$ 60 mil próprios, R$ 166 mil financiáveis. Restam R$ 274 mil, que podem vir de um parceiro ou ser reduzidos começando com uma etapa menor.'},
 {kind:'compare', title:'Plano de capitalização frágil × robusto',
  cols:[{h:'Frágil',type:'bad',items:['Depende de uma única fonte','Sem plano B se o crédito não sair','Começa a obra sem todo o recurso da etapa garantido']},
        {h:'Robusto',type:'good',items:['Combina duas ou três fontes','Tem alternativa ordenada para cada etapa','Só inicia a etapa com o recurso dela assegurado']}]},
 {kind:'form', title:'Sua prioridade e seu prazo',
  fields:[
   {id:'prioridade',label:'O que é mais importante para você?',type:'radio',required:true,options:[{v:'controle',l:'Manter o controle das decisões'},{v:'rapidez',l:'Tirar o projeto do papel mais rápido'},{v:'risco',l:'Correr o menor risco financeiro'},{v:'terra',l:'Manter a terra 100% minha'}]},
   {id:'prazo_decisao',label:'Em quantos meses você quer decidir o caminho?',type:'number',required:true,min:1,max:36,step:1,unit:'meses'}
  ]},
 {kind:'feedback', title:'Seu mapa de alternativas',
  metrics:function(s,c){return c.rank.slice(0,3).map(function(a,i){return {label:(i+1)+'º · '+a.n,value:F.num(a.v,0)+'/100',tag:'calculado'};});},
  feedback:function(s,c){var o=[];var t=c.rank[0], t2=c.rank[1];
   if(t.v<35) o.push({lv:'warn',t:'Nenhuma alternativa tem aderência alta com o seu perfil atual. Os pontos que mais limitam: '+c.limitantes.join('; ')+'.'});
   else o.push({lv:'info',t:'Alternativa mais aderente: <b>'+t.n+'</b> ('+F.num(t.v,0)+'/100), seguida de <b>'+t2.n+'</b> ('+F.num(t2.v,0)+'/100).'});
   if(c.mix) o.push({lv:'info',t:'Estrutura preliminar: '+F.brl0(c.mix.own)+' próprios + '+F.brl0(c.mix.fin)+' em crédito + '+F.brl0(c.mix.rest)+' a cobrir com outras alternativas ou com etapas.'});
   if(c.bloqueio) o.push({lv:'bad',t:'A situação documental limita quase todos os caminhos. Comece por ela, com advogado.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Escolher a alternativa principal e a alternativa de reserva'},{id:'a7_2',text:'Dar o primeiro passo da alternativa principal nos próximos 15 dias'},{id:'a7_3',text:'Refazer o Mapa quando tiver orçamentos ou simulações novas'}]}
]}
],

compute:function(s){
 var c={};
 var nec=s.n('necessidade'), f1=s.n('custo_f1'), rec=s.n('recursos',0), parc=s.n('parcela_max',0);
 c.f1=f1; c.need=nec!=null?nec:f1; c.needOrig=nec!=null?'nec':(f1!=null?'f1':null);
 c.gap=c.need!=null?Math.max(0,c.need-rec):null;
 c.cobProp=c.need?Math.min(1,rec/c.need):0;
 var ds=s.t('doc_status'); c.bloqueio=s.unknown('doc_status')||ds==='irregular';
 c.docF=s.unknown('doc_status')?0.5:({regular:1,parcial:0.75,irregular:0.5}[ds]||0.5);
 var docOk=s.unknown('doc_status')?0:({regular:1,parcial:0.5,irregular:0}[ds]||0);
 var vt=s.n('valor_terra'); c.terraGap=(vt!=null&&c.gap)?vt/c.gap:null;
 var cp=SNT[s.t('cede_parte')]||0, cu=SNT[s.t('cede_uso')]||0;
 c.ctrl=(sc(s,'controle',3)-1)/4;
 var rede={sim:1,algum:0.5,nao:0}[s.t('rede')]||0;
 var renda=(sc(s,'interesse_renda',3)-1)/4, dem={sim:1,nao_sei:0.5,nao:0}[s.t('demanda_operador')]||0;
 var rc={sim:1,parcial:0.5,nao:0}[s.t('renda_comprovavel')]||0, cr={limpo:1,nao_sei:0.5,restricao:0}[s.t('credito')]||0, tol=(sc(s,'tol_divida',3)-1)/4;
 var i=s.n('taxa_mensal'), n=s.n('prazo_fin',1);
 c.teto=parc*n;
 c.capFin=i==null?null:(i===0?parc*n:parc*(1-Math.pow(1+i/100,-n))/(i/100));
 c.covFin=c.gap==null?0.5:(c.gap===0?1:(c.capFin==null?0.5:Math.min(1,c.capFin/c.gap)));
 c.covFinTxt=(c.gap==null||c.capFin==null)?'—':(c.gap===0?'100%':F.pct(Math.min(1,c.capFin/c.gap)*100,0));
 c.f1cov=f1?Math.min(1,rec/f1):0;
 var prazoF=Math.min(1,s.n('prazo_crescer',0)/5), reinv={sim:1,parcial:0.5,nao:0}[s.t('reinvestir')]||0;
 var base={
  proprios:100*c.cobProp,
  parceria:(40*cp+30*(1-c.ctrl)+30*rede)*c.docF,
  arrendamento:(40*cu+30*renda+30*dem)*c.docF,
  permuta:50*cp+30*docOk+20*(1-c.ctrl),
  financiamento:(30*rc+20*cr+20*tol+30*c.covFin)*c.docF,
  progressiva:50*c.f1cov+25*prazoF+25*reinv};
 c.base=base; c.alt={};
 var bon=BONUS[s.t('prioridade')]||[];
 ALT.forEach(function(a){var v=base[a.k]; if(v>0&&bon.indexOf(a.k)>=0) v+=10; c.alt[a.k]=ZA.clamp(v,0,100);});
 c.rank=ALT.map(function(a,ix){return {k:a.k,n:a.n,d:a.d,quem:a.quem,rel:a.rel,v:c.alt[a.k],ix:ix};}).sort(function(a,b){return (b.v-a.v)||(a.ix-b.ix);});
 // limitantes
 var lim=[]; if(c.need==null) lim.push('necessidade de investimento desconhecida'); if(c.bloqueio) lim.push('situação documental'); if(cp===0&&cu===0) lim.push('não aceitar ceder participação nem uso'); if(rec===0) lim.push('nenhum recurso próprio'); if(parc===0) lim.push('sem capacidade de pagar parcelas'); if(!lim.length) lim.push('combinação de fatores do perfil');
 c.limitantes=lim;
 // estrutura de capital
 if(c.need!=null){var own=Math.min(rec,c.need), fin=(c.alt.financiamento>=50&&c.capFin!=null)?Math.min(c.capFin,c.need-own):0;
  c.mix={own:own,fin:fin,rest:Math.max(0,c.need-own-fin)};} else c.mix=null;
 c.mixRest=c.mix?c.mix.rest:null; c.mixFin=c.mix?c.mix.fin:null;
 return c;
},

metrics:function(s,c){return [
 {label:'Necessidade de investimento',value:F.brl0(c.need),tag:c.needOrig==='nec'?'informado':c.needOrig==='f1'?'estimativa':'hipotese'},
 {label:'Lacuna de capital',value:F.brl0(c.gap),tag:'calculado'},
 {label:'Alternativa mais aderente',value:c.rank[0].n,tag:'calculado'},
 {label:'Aderência da 1ª alternativa',value:F.num(c.rank[0].v,0)+'/100',tag:'calculado'},
 {label:'Valor financiável (sua simulação)',value:c.capFin==null?'—':F.brl0(c.capFin),tag:c.capFin==null?'hipotese':'calculado'},
 {label:'Etapa 1 · cobertura própria',value:c.f1==null?'—':F.pct(c.f1cov*100,0),tag:'calculado'},
 {label:'A cobrir após próprios e crédito',value:c.mix?F.brl0(c.mix.rest):'—',tag:'calculado'},
 {label:'Prazo para decidir',value:F.num(s.n('prazo_decisao'))+' meses',tag:'informado'}
];},

priorities:function(s,c){var L=[];var t=c.rank[0];
 if(c.bloqueio) L.push({title:'Esclarecer a situação documental da terra com advogado',why:'Reduz a aderência de parceria, arrendamento, permuta e crédito.',score:10});
 if(c.need==null) L.push({title:'Montar o orçamento do projeto e da primeira etapa',why:'Sem necessidade definida, não há como dimensionar o capital.',score:9});
 if(t.v>=35) L.push({title:'Dar o primeiro passo em '+t.n.toLowerCase(),why:'Alternativa mais aderente ao seu perfil ('+F.num(t.v,0)+'/100). Quem pode ajudar: '+t.quem+'.',score:8});
 if(c.rank[1].v>=35) L.push({title:'Preparar a alternativa de reserva: '+c.rank[1].n.toLowerCase(),why:'Segunda mais aderente ('+F.num(c.rank[1].v,0)+'/100).',score:6});
 if(s.t('reserva')==='nao') L.push({title:'Formar reserva de emergência antes de comprometer recursos',why:'Imprevistos sem reserva viram dívida cara.',score:7});
 if(s.n('taxa_mensal')==null&&s.n('parcela_max',0)>0) L.push({title:'Fazer simulações de crédito em duas instituições',why:'Sem taxa real, o valor financiável é desconhecido.',score:5});
 if(s.t('credito')==='restricao') L.push({title:'Resolver restrições de cadastro',why:'Restrição limita o acesso ao crédito.',score:6});
 if(c.f1==null) L.push({title:'Orçar a menor etapa que já recebe hóspedes',why:'Abre o caminho da implantação progressiva.',score:6});
 else if(c.f1cov>=1) L.push({title:'Avaliar começar já pela etapa 1 com recursos próprios',why:'Seus recursos cobrem a primeira etapa.',score:7});
 if(s.unknown('valor_terra')) L.push({title:'Obter referência de valor da terra',why:'Base para negociar parceria, permuta ou garantia.',score:5});
 if(s.t('demanda_operador')==='nao_sei'&&c.alt.arrendamento>=40) L.push({title:'Sondar operadores de turismo da região',why:'O arrendamento tem aderência, mas falta confirmar interesse.',score:4});
 if(s.t('rede')==='nao'&&c.alt.parceria>=40) L.push({title:'Construir rede: associações comerciais e de turismo',why:'Parceria aderente, mas sem contatos.',score:4});
 if(c.mix&&c.mix.rest>0) L.push({title:'Definir como cobrir '+F.brl0(c.mix.rest)+' restantes (parceria, permuta ou etapa menor)',why:'Valor não coberto por recursos próprios e crédito.',score:5});
 L.push({title:'Levar o mapa ao contador e ao advogado antes de decidir',why:'Cada alternativa tem efeitos tributários e jurídicos próprios.',score:3});
 return L;},

report:function(s,c){
 var mapa=ZA.table(['#','Alternativa','Aderência','Como funciona','Quem procurar'],c.rank.map(function(a,i){return [String(i+1),'<b>'+esc(a.n)+'</b>',F.num(a.v,0)+'/100',esc(a.d)+(a.rel?' <span class="za-small">(ver '+esc(a.rel)+')</span>':''),esc(a.quem)];}),[2]);
 var mix=c.mix?ZA.table(['Fonte','Valor','Participação'],[['Recursos próprios',F.brl0(c.mix.own),F.pct(c.mix.own/c.need*100,0)],['Financiamento (sua simulação)',F.brl0(c.mix.fin),F.pct(c.mix.fin/c.need*100,0)],['A cobrir com parceria, permuta, arrendamento ou etapa menor',F.brl0(c.mix.rest),F.pct(c.mix.rest/c.need*100,0)],['<b>Necessidade</b>','<b>'+F.brl0(c.need)+'</b>','100%']],[1,2])+'<p class="za-small">O crédito só entra na estrutura quando a aderência ao financiamento é de pelo menos 50/100 e há taxa de uma simulação sua.'+(c.alt.financiamento<50?' No seu caso, ficou fora.':'')+'</p>':'<p class="za-missing">Sem a necessidade de investimento, a estrutura de capital não pode ser dimensionada.</p>';
 var fin=ZA.table(['Item','Valor'],[['Parcela máxima',F.brl0(s.n('parcela_max'))],['Taxa mensal (sua simulação)',s.unknown('taxa_mensal')?'—':F.pct(s.n('taxa_mensal'),2)],['Prazo',F.num(s.n('prazo_fin'))+' meses'],['Valor financiável',c.capFin==null?'—':F.brl0(c.capFin)],['Teto sem juros (só referência)',F.brl0(c.teto)]],[1]);
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Necessidade de investimento',F.brl0(c.need),c.needOrig==='nec'?tag('informado'):c.needOrig==='f1'?tag('estimativa','= custo da etapa 1'):tag('hipotese','ausente')],
  ['Recursos próprios',F.brl0(s.n('recursos')),tag('informado')],
  ['Taxa e prazo do crédito',s.unknown('taxa_mensal')?'—':F.pct(s.n('taxa_mensal'),2)+' a.m. · '+F.num(s.n('prazo_fin'))+' meses',s.unknown('taxa_mensal')?tag('hipotese','ausente'):tag('informado','sua simulação')],
  ['Fator documental','regular 100% · pendência 75% · posse 50% · desconhecida 50%',tag('recomendacao','metodologia Zion')],
  ['Pesos de aderência','ver fórmulas em cada pilar',tag('recomendacao','metodologia Zion')],
  ['Ajuste por prioridade','+10 nas alternativas coerentes com “'+esc({controle:'manter o controle',rapidez:'rapidez',risco:'menor risco',terra:'manter a terra 100% minha'}[s.t('prioridade')]||'—')+'”',tag('recomendacao','metodologia Zion')]],[1]);
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro para decidir em '+F.num(s.n('prazo_decisao'))+' meses</b><ol><li><b>Mês 1 · base:</b> '+(top[0]?esc(top[0].title):'Revisar o orçamento')+'.</li><li><b>Mês 1 e 2 · alternativa principal:</b> '+(top[1]?esc(top[1].title):'Primeiro passo na alternativa principal')+'.</li><li><b>Mês 2 e 3 · reserva:</b> '+(top[2]?esc(top[2].title):'Preparar a alternativa de reserva')+'.</li><li><b>Até o prazo:</b> comparar as propostas reais (de sócios, operadores ou instituições) com este mapa e decidir com contador e advogado.</li></ol></div>';
 return {sections:[
  {title:'Mapa de alternativas · aderência ao seu perfil',html:mapa},
  {title:'Estrutura de capital preliminar',html:mix},
  {title:'Crédito: o que cabe na sua parcela',html:fin+'<p class="za-small">Não indicamos linhas de crédito nem instituições. Compare o custo efetivo total das propostas que receber.</p>'},
  {title:'Premissas utilizadas',html:prem}
 ],plan:plan};
}
});
})();
