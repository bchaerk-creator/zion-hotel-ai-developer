/* ZAR-B06 · Como Saber Quanto Custa Construir uma Hospedagem? · Calculadora de Implantação Turística */
(function(){
var F=ZA.fmt, esc=ZA.esc;
function rowsOf(s,id){return (s.v[id]||[]).filter(function(r){return r&&ZA.isNum(r.value)&&r.value>0;});}
function tag(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';}
ZA.register({
id:'B06', code:'ZAR-B06', collection:'Terrenos',
title:'Como Saber Quanto Custa Construir uma Hospedagem?',
subtitle:'Monte Seu Orçamento de Implantação',
tool:'Calculadora de Implantação Turística',
deliverable:'Orçamento Preliminar de Implantação',
nameField:'nome', propertyField:'propriedade',
disclaimer:'Este orçamento é preliminar e soma apenas os valores que você informou (cotações e estimativas próprias). A Zion não fornece preços de mercado. Custos de obra mudam com o projeto, o terreno, o fornecedor e o tempo: confirme cada item com orçamentos formais e com engenheiro ou arquiteto habilitado. Licenças, regularização e exigências ambientais devem ser verificadas com a prefeitura, o órgão ambiental e profissionais habilitados; este material não garante aprovação, prazo nem custo final.',

intro:[
 {kind:'mirror', title:'Você sabe o preço da cabana. Mas sabe quanto custa deixar tudo pronto?',
  lead:'Você viu o valor de uma cabana pronta, fez a conta de quantas cabem no terreno e imaginou o investimento. Mas, quando começa a perguntar, aparecem estrada, energia, fossa, projeto, taxa, móveis, enxoval… e o número não para de crescer.',
  body:'<div class="za-card"><p>Se você se reconhece em alguma destas situações, esta mini mentoria foi feita para você:</p><ul><li>“Tenho o orçamento da cabana, mas não sei quanto custa o resto.”</li><li>“Não sei se preciso de projeto, licença ou responsável técnico.”</li><li>“Tenho medo de começar a obra e o dinheiro acabar no meio.”</li><li>“Não sei quanto guardar para os primeiros meses de operação.”</li></ul></div>'},
 {kind:'collapse', title:'O preço de uma unidade de hospedagem pode representar apenas parte do investimento necessário.',
  lead:'Uma cabana precisa de chão firme, acesso, água, energia, esgoto, documentação, mobília e caixa para funcionar até as reservas engrenarem. Quem orça só a unidade orça só uma parte do projeto.',
  body:'<div class="za-card"><p>Um orçamento de implantação completo tem <b>seis blocos</b>:</p><ol><li>Projetos, licenças e documentação</li><li>Infraestrutura do terreno</li><li>Construção e instalação das unidades e áreas comuns</li><li>Mobiliário, equipamentos e pré-operação</li><li>Capital de giro para os primeiros meses</li><li>Contingência para imprevistos</li></ol><p>Neste percurso, você preenche cada bloco com <b>as suas cotações</b>. A ferramenta soma, mostra a composição e monta três cenários. Nenhum preço é inventado pela ferramenta.</p></div>'},
 {kind:'start', title:'Vamos montar o seu orçamento de implantação',
  lead:'Em 7 pilares, você vai listar tudo o que custa para colocar a hospedagem em funcionamento e sair com um orçamento preliminar em três cenários.',
  body:'<p>Tenha à mão, se possível: orçamentos de fornecedores de cabanas ou construtoras, cotações de terraplanagem, poço, fossa e energia, e uma lista de móveis e enxoval. Se ainda não tiver um valor, marque “não sei” onde houver essa opção ou deixe a linha em branco. O relatório mostrará o que ficou de fora.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Marta'},
   {id:'propriedade',label:'Nome do projeto ou da propriedade',type:'text',required:true,placeholder:'Ex.: Refúgio Serra Azul'},
   {id:'municipio',label:'Município / região do terreno',type:'text',required:true,placeholder:'Ex.: Alto Paraíso (GO)'},
   {id:'modelo',label:'Modelo de hospedagem que você pretende implantar',type:'select',required:true,options:[{v:'cabana',l:'Cabanas'},{v:'chale',l:'Chalés'},{v:'glamping',l:'Glamping (tendas, domos, bolhas)'},{v:'container',l:'Módulos / contêineres'},{v:'pousada',l:'Pequena pousada'},{v:'outro',l:'Outro'}]}
  ]}
],

pillars:[
/* 1 */
{title:'Modelo de hospedagem', screens:[
 {kind:'learn', title:'O modelo define o tamanho da conta',
  body:'<p>Antes de orçar, é preciso saber <b>o que</b> será construído. O modelo (cabana, chalé, glamping, módulo, pousada) e o <b>padrão de acabamento</b> mudam praticamente todos os itens: fundação, área construída, instalações, mobiliário e até o tipo de licença exigida.</p><p>Por isso, o primeiro passo é descrever a unidade-padrão: área aproximada, padrão (econômico, intermediário ou alto) e o que vem incluído na cotação do fornecedor. Uma cotação “cabana pronta” pode incluir ou não fundação, instalação elétrica, hidráulica, frete e montagem.</p><p>Também importa a <b>qualidade da informação</b>: uma cotação formal por escrito vale mais do que um valor visto num anúncio.</p>',
  example:'Exemplo ilustrativo: duas cotações de “cabana de 30 m²” podem parecer próximas, mas uma inclui fundação e montagem e a outra entrega apenas o kit. Comparar sem ler o escopo pode criar uma diferença grande no orçamento final.'},
 {kind:'compare', title:'Cotação incompleta × cotação comparável',
  cols:[{h:'Cotação que engana',type:'bad',items:['Valor de anúncio ou de conversa informal','Não diz o que está incluído','Sem prazo de validade','Sem frete, montagem ou fundação']},
        {h:'Cotação comparável',type:'good',items:['Por escrito, com data e validade','Escopo detalhado: o que está e o que não está incluído','Mesma área e mesmo padrão para comparar fornecedores','Frete, montagem e fundação discriminados']}]},
 {kind:'form', title:'Descreva a unidade-padrão', intro:'Pense na unidade de hospedagem que se repetirá no projeto.',
  fields:[
   {id:'padrao',label:'Padrão de acabamento pretendido',type:'radio',required:true,options:[{v:'economico',l:'Econômico'},{v:'intermediario',l:'Intermediário'},{v:'alto',l:'Alto padrão'}]},
   {id:'area_unid',label:'Área aproximada de cada unidade',type:'number',required:true,min:1,max:2000,step:1,unit:'m²',allowUnknown:true},
   {id:'qualidade_cot',label:'Que tipo de valores você tem hoje?',type:'radio',required:true,options:[{v:'formal',l:'Cotações formais por escrito'},{v:'informal',l:'Valores de conversa, anúncio ou site'},{v:'nenhum',l:'Ainda não tenho valores, vou buscar'}]},
   {id:'n_cotacoes',label:'Quantos fornecedores você consultou para a unidade?',type:'number',required:true,min:0,max:50,step:1,unit:'fornecedor(es)'}
  ]},
 {kind:'feedback', title:'A qualidade do seu ponto de partida',
  metrics:function(s,c){return [{label:'Padrão',value:({economico:'Econômico',intermediario:'Intermediário',alto:'Alto padrão'})[s.t('padrao')]||'—',tag:'informado'},{label:'Área por unidade',value:s.has('area_unid')?F.num(s.n('area_unid'))+' m²':'—',tag:'informado'},{label:'Fornecedores consultados',value:F.num(s.n('n_cotacoes',0)),tag:'informado'}];},
  feedback:function(s,c){var o=[],q=s.t('qualidade_cot'),n=s.n('n_cotacoes',0);
   if(q==='formal') o.push({lv:'ok',t:'Você trabalha com cotações formais. Isso dá muito mais confiança ao orçamento. Confira a validade de cada uma.'});
   if(q==='informal') o.push({lv:'warn',t:'Valores de conversa ou anúncio servem para uma primeira noção, mas o relatório deve ser lido como <b>estimativa</b>. Peça propostas por escrito com escopo detalhado.'});
   if(q==='nenhum') o.push({lv:'bad',t:'Sem valores, o orçamento ainda não pode ser fechado. Use este percurso como <b>roteiro de cotação</b>: cada linha que você deixar em branco é um pedido de orçamento a fazer.'});
   if(n<3) o.push({lv:'warn',t:'Você consultou '+F.num(n)+' fornecedor(es). Comparar pelo menos 3 propostas com o mesmo escopo ajuda a identificar valores fora da curva.'});
   else o.push({lv:'ok',t:F.num(n)+' fornecedores consultados: boa base para comparação.'});
   if(s.unknown('area_unid')) o.push({lv:'warn',t:'Sem a área da unidade, não será possível calcular o custo por m². Defina pelo menos uma área aproximada com o fornecedor ou arquiteto.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Pedir propostas por escrito a pelo menos 3 fornecedores, com o mesmo escopo'},{id:'a1_2',text:'Montar uma planilha comparando o que cada cotação inclui e não inclui'},{id:'a1_3',text:'Definir a área e o padrão da unidade antes de pedir novos orçamentos'}]}
]},
/* 2 */
{title:'Quantidade de unidades', screens:[
 {kind:'learn', title:'Quantas unidades: a decisão que multiplica tudo',
  body:'<p>O número de unidades multiplica o custo de construção e de mobiliário, mas <b>não multiplica</b> boa parte da infraestrutura: a estrada de acesso, o padrão de energia e o projeto servem para 2 ou para 6 unidades (com ajustes). Por isso, o <b>custo por unidade</b> costuma cair quando a quantidade aumenta, mas o desembolso total sobe.</p><p>A quantidade deve nascer de três limites: o que o terreno comporta (e a legislação permite), o que a demanda sustenta e o que o seu orçamento alcança. Escolher pelo terreno sem olhar o orçamento é o caminho mais curto para uma obra parada.</p>',
  example:'Exemplo ilustrativo: R$ 60.000 de infraestrutura divididos por 2 unidades pesam R$ 30.000 em cada uma; divididos por 5, pesam R$ 12.000. Mas 5 unidades exigem muito mais capital total.'},
 {kind:'compare', title:'Como decidir a quantidade',
  cols:[{h:'Decisões arriscadas',type:'bad',items:['“Cabem 10 no terreno, então vou fazer 10”','Copiar a quantidade de outro empreendimento','Ignorar o limite de ocupação permitido pela prefeitura','Decidir sem saber o custo total']},
        {h:'Decisão estruturada',type:'good',items:['Partir do orçamento disponível e do custo total por unidade','Confirmar com a prefeitura e um profissional o que é permitido','Considerar começar menor e expandir por etapas','Olhar a demanda do destino antes de multiplicar']}]},
 {kind:'form', title:'Quantas unidades você pretende implantar', intro:'Considere o projeto que você quer orçar agora.',
  fields:[
   {id:'unidades',label:'Quantidade de unidades de hospedagem',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)'},
   {id:'hospedes_unid',label:'Hóspedes por unidade (capacidade)',type:'number',required:true,min:1,max:30,step:1,unit:'pessoas'},
   {id:'motivo_qtd',label:'O que mais definiu essa quantidade?',type:'radio',required:true,options:[{v:'orcamento',l:'O orçamento que tenho'},{v:'terreno',l:'O espaço do terreno'},{v:'demanda',l:'A demanda que pesquisei'},{v:'intuicao',l:'Intuição / referência de outro lugar'}]}
  ]},
 {kind:'feedback', title:'O tamanho do seu projeto',
  metrics:function(s,c){return [{label:'Unidades',value:F.num(c.U),tag:'informado'},{label:'Capacidade total',value:F.num(c.leitos)+' hóspedes',tag:'calculado'}];},
  feedback:function(s,c){var o=[],m=s.t('motivo_qtd');
   if(m==='terreno') o.push({lv:'warn',t:'A quantidade foi definida pelo espaço do terreno. Confira se o orçamento acompanha: no Pilar 7 você verá quanto custa cada unidade com toda a infraestrutura.'});
   if(m==='intuicao') o.push({lv:'warn',t:'Quantidade definida por intuição. Use o custo total por unidade (Pilar 7) e a demanda do destino para validar esse número.'});
   if(m==='orcamento') o.push({lv:'ok',t:'Você partiu do orçamento. Ótimo: o Pilar 7 vai mostrar se as '+F.num(c.U)+' unidades cabem nele com contingência.'});
   if(m==='demanda') o.push({lv:'ok',t:'Quantidade baseada em demanda pesquisada. Guarde as fontes dessa pesquisa para o relatório.'});
   if(c.U>=8) o.push({lv:'info',t:'Com '+F.num(c.U)+' unidades, avalie implantar por etapas: começar com parte das unidades reduz o capital inicial e permite testar a demanda.'});
   o.push({lv:'info',t:'Capacidade total de '+F.num(c.leitos)+' hóspedes simultâneos. Esse número influencia exigências de água, esgoto, estacionamento e, em alguns municípios, o tipo de licença.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Consultar a prefeitura sobre o limite de ocupação e o uso permitido no terreno'},{id:'a2_2',text:'Simular o orçamento com menos unidades para comparar'},{id:'a2_3',text:'Registrar de onde veio a quantidade escolhida (orçamento, terreno ou demanda)'}]}
]},
/* 3 */
{title:'Projetos e licenças', screens:[
 {kind:'learn', title:'Projetos e licenças: o custo que vem antes do primeiro tijolo',
  body:'<p>Antes de construir, um empreendimento de hospedagem geralmente passa por etapas técnicas e documentais: levantamento topográfico, projeto arquitetônico, projetos complementares (estrutural, elétrico, hidráulico, sanitário), estudos e licenças ambientais quando exigidos, alvarás e taxas municipais, regularização do imóvel e responsável técnico (ART ou RRT).</p><p>Quais etapas se aplicam ao seu caso depende do município, do tamanho do projeto, da localização (por exemplo, áreas de preservação) e da situação documental do terreno. <b>Quem define isso são a prefeitura, o órgão ambiental e os profissionais habilitados</b> (arquiteto, engenheiro, advogado). Aqui você só registra os custos que levantou com eles.</p>',
  example:'Exemplo ilustrativo: um proprietário que orçou R$ 0 para projetos e licenças descobre, ao pedir o alvará, que precisa de topografia, projeto e responsável técnico. O custo e o prazo dessas etapas entram depois, quando o dinheiro já foi para a obra.'},
 {kind:'compare', title:'Pular etapas × planejar etapas',
  cols:[{h:'Pular etapas',type:'bad',items:['Construir antes de saber o que a prefeitura permite','Não ter responsável técnico pela obra','Deixar a regularização do terreno para depois','Descobrir exigências ambientais no meio da obra']},
        {h:'Planejar etapas',type:'good',items:['Consulta prévia à prefeitura sobre uso e ocupação','Orçar projetos e responsável técnico desde o início','Verificar a documentação do imóvel com advogado','Consultar o órgão ambiental antes de definir a implantação']}]},
 {kind:'form', title:'Seus custos de projetos, licenças e documentação', intro:'Informe o valor total de cada item para o projeto inteiro. Deixe em branco o que não se aplica ou o que ainda não foi cotado.',
  fields:[
   {id:'projetos',label:'Projetos, licenças e documentação',type:'list',required:true,preset:['Levantamento topográfico','Projeto arquitetônico','Projetos complementares (estrutural, elétrico, hidráulico)','Estudos e licenças ambientais','Alvarás e taxas municipais','Regularização documental / cartório','Responsável técnico (ART/RRT) e acompanhamento'],namePlaceholder:'Item',valuePlaceholder:'R$ total'},
   {id:'status_lic',label:'Em que ponto está a parte de licenças?',type:'radio',required:true,options:[{v:'nada',l:'Ainda não comecei'},{v:'consulta',l:'Já fiz consulta prévia à prefeitura ou ao órgão ambiental'},{v:'andamento',l:'Processo em andamento'},{v:'aprovado',l:'Já tenho as aprovações necessárias'}]}
  ]},
 {kind:'feedback', title:'O peso dos projetos e licenças',
  metrics:function(s,c){return [{label:'Projetos e licenças',value:F.brl(c.projetos),tag:'calculado'},{label:'Itens orçados',value:F.num(c.projItens)+' de '+F.num((s.v.projetos||[]).length),tag:'calculado'}];},
  feedback:function(s,c){var o=[],st=s.t('status_lic');
   if(c.projItens<3) o.push({lv:'warn',t:'Apenas '+F.num(c.projItens)+' item(ns) de projeto e licença têm valor. Confirme com arquiteto ou engenheiro quais etapas se aplicam ao seu caso antes de considerar esse bloco fechado.'});
   else o.push({lv:'ok',t:F.num(c.projItens)+' itens de projetos e licenças orçados, somando '+F.brl(c.projetos)+'.'});
   if(!c.temResp) o.push({lv:'warn',t:'Não há valor para responsável técnico (ART/RRT). Em obras, normalmente é exigido um profissional habilitado responsável. Confirme com a prefeitura.'});
   if(st==='nada') o.push({lv:'bad',t:'As licenças ainda não foram iniciadas. Antes de contratar a obra, faça uma consulta prévia à prefeitura e, se houver área sensível, ao órgão ambiental. Prazos de aprovação podem afetar todo o cronograma.'});
   if(st==='consulta') o.push({lv:'info',t:'Você já fez consulta prévia. Registre por escrito o que foi orientado e confirme com um profissional habilitado.'});
   if(st==='aprovado') o.push({lv:'ok',t:'Aprovações já obtidas. Guarde os documentos: eles serão pedidos por sócios, financiadores e seguradoras.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Fazer a consulta prévia de uso e ocupação do solo na prefeitura'},{id:'a3_2',text:'Pedir a um arquiteto ou engenheiro a lista de projetos e licenças necessários'},{id:'a3_3',text:'Verificar a documentação do terreno com um advogado ou no cartório'}]}
]},
/* 4 */
{title:'Infraestrutura', screens:[
 {kind:'learn', title:'Infraestrutura: o investimento que o hóspede não vê, mas sente',
  body:'<p>Terrenos rurais e áreas de natureza raramente estão prontos para receber hóspedes. A infraestrutura inclui: acesso e estrada interna, terraplanagem, rede elétrica e padrão de entrada, água (poço, caixa d’água, rede), tratamento de esgoto, internet, estacionamento, iluminação externa, paisagismo e trilhas.</p><p>Esse bloco costuma ser o mais subestimado porque depende do terreno: distância da rede de energia, tipo de solo, declividade, disponibilidade de água. Só um levantamento no local, com fornecedores e profissionais, dá o valor real.</p>',
  example:'Exemplo ilustrativo: uma cabana pode custar o mesmo em dois terrenos, mas num deles a rede elétrica está na porteira e no outro a centenas de metros. A diferença está toda na infraestrutura.'},
 {kind:'compare', title:'O que o terreno já tem × o que precisa ser feito',
  cols:[{h:'Erros comuns',type:'bad',items:['Supor que “depois a gente puxa a luz”','Não testar vazão e qualidade da água','Esquecer o tratamento de esgoto','Não prever estacionamento e iluminação']},
        {h:'Boa prática',type:'good',items:['Listar o que existe e o que falta, item por item','Pedir orçamento à concessionária de energia','Consultar profissional sobre poço e tratamento de esgoto','Orçar acesso transitável em época de chuva']}]},
 {kind:'form', title:'Infraestrutura do terreno', intro:'Primeiro marque o que o terreno <b>já tem</b> funcionando. Depois informe o custo total do que precisa ser feito.',
  fields:[
   {id:'infra_existe',label:'O terreno já tem, funcionando:',type:'checks',options:[{v:'acesso',l:'Acesso transitável o ano todo'},{v:'energia',l:'Energia elétrica no local'},{v:'agua',l:'Água em quantidade suficiente'},{v:'esgoto',l:'Solução de esgoto adequada'},{v:'internet',l:'Internet / sinal de celular'}]},
   {id:'infra',label:'Custos de infraestrutura',type:'list',required:true,preset:['Acesso e estrada interna','Terraplanagem e drenagem','Rede elétrica e padrão de entrada','Água (poço, caixa, rede)','Tratamento de esgoto','Internet','Estacionamento','Iluminação externa','Paisagismo e trilhas'],namePlaceholder:'Item',valuePlaceholder:'R$ total'}
  ]},
 {kind:'feedback', title:'Infraestrutura: o que pode estar faltando',
  metrics:function(s,c){return [{label:'Infraestrutura',value:F.brl(c.infra),tag:'calculado'},{label:'Infraestrutura por unidade',value:F.brl(c.infraUnid),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   c.infraLacunas.forEach(function(x){o.push({lv:'bad',t:'Você indicou que o terreno <b>não tem '+x+'</b>, mas não há valor orçado para isso. Esse item precisa de cotação antes de o orçamento ser considerado completo.'});});
   if(!c.infraLacunas.length) o.push({lv:'ok',t:'Os itens que o terreno não tem aparecem com valor orçado. Boa coerência.'});
   if(c.infra===0) o.push({lv:'warn',t:'Nenhum custo de infraestrutura informado. Mesmo terrenos bem servidos costumam precisar de estacionamento, iluminação ou ajustes de acesso.'});
   if(c.infraMaior) o.push({lv:'info',t:'Seu maior item de infraestrutura é <b>'+esc(c.infraMaior.name)+'</b> ('+F.brl(c.infraMaior.value)+'). Vale buscar uma segunda cotação para ele.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Solicitar à concessionária o orçamento de ligação de energia'},{id:'a4_2',text:'Consultar um profissional sobre água e tratamento de esgoto no terreno'},{id:'a4_3',text:'Visitar o terreno em dia de chuva para avaliar o acesso'}]}
]},
/* 5 */
{title:'Construção e instalação', screens:[
 {kind:'learn', title:'Construção: a unidade e tudo o que a cerca',
  body:'<p>O custo de construção tem duas partes:</p><ul><li><b>Por unidade:</b> a cabana, chalé ou tenda em si, com fundação, estrutura, cobertura, instalações e acabamento, mais frete e montagem quando o fornecedor não inclui.</li><li><b>Áreas comuns:</b> recepção ou apoio, área de convivência, lavanderia e rouparia, depósito ou casa de máquinas, deck, piscina ou ofurô coletivo.</li></ul><p>Um indicador útil é o <b>custo por m²</b> da unidade (custo ÷ área). Ele permite comparar fornecedores com tamanhos diferentes e perceber cotações fora do padrão das demais que você recebeu.</p>',
  example:'Exemplo ilustrativo: uma unidade de 30 m² cotada em R$ 120.000 custa R$ 4.000 por m². Se outra proposta de 25 m² vem por R$ 115.000, o m² sobe para R$ 4.600, mesmo parecendo mais barata.'},
 {kind:'compare', title:'Construção completa × construção pela metade',
  cols:[{h:'Orçamento pela metade',type:'bad',items:['Só o valor do kit da cabana','Sem frete até o terreno','Sem fundação e montagem','Sem lavanderia, depósito ou área de apoio']},
        {h:'Orçamento completo',type:'good',items:['Unidade com fundação, instalações e acabamento','Frete e montagem discriminados','Áreas de apoio que a operação exige','Mesmo padrão em todas as cotações']}]},
 {kind:'form', title:'Custos de construção', intro:'Use os valores das suas cotações.',
  fields:[
   {id:'custo_unid',label:'Custo de construção por unidade (fundação, estrutura, instalações e acabamento)',type:'money',required:true,min:1},
   {id:'frete_unid',label:'Frete e montagem por unidade (se não incluídos acima)',type:'money',required:true,allowUnknown:true,help:'Se já estão incluídos na cotação, informe 0.'},
   {id:'comuns',label:'Áreas comuns e de apoio (valor total)',type:'list',required:false,preset:['Recepção / apoio','Área de convivência','Lavanderia e rouparia','Depósito / casa de máquinas','Deck, piscina ou ofurô coletivo'],namePlaceholder:'Item',valuePlaceholder:'R$ total'},
   {id:'prazo_obra',label:'Prazo estimado da obra',type:'number',required:true,min:1,max:60,step:1,unit:'meses'}
  ]},
 {kind:'feedback', title:'Sua construção em números',
  metrics:function(s,c){return [{label:'Construção total',value:F.brl(c.construcao),tag:'calculado'},{label:'Custo por m² da unidade',value:c.m2==null?'—':F.brl(c.m2),tag:'calculado'},{label:'Áreas comuns',value:F.brl(c.comuns),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(s.unknown('frete_unid')) o.push({lv:'warn',t:'Frete e montagem não informados: o cálculo usou <b>R$ 0</b>. Pergunte ao fornecedor se estão incluídos; em terrenos afastados esse valor pode ser relevante.'});
   if(c.comuns===0) o.push({lv:'warn',t:'Nenhuma área comum orçada. Mesmo projetos pequenos costumam precisar de um espaço para rouparia, lavanderia ou depósito de materiais de limpeza.'});
   else o.push({lv:'ok',t:'Áreas comuns orçadas em '+F.brl(c.comuns)+'.'});
   if(c.m2!=null) o.push({lv:'info',t:'Sua unidade custa '+F.brl(c.m2)+' por m² (custo de construção + frete ÷ área). Use esse número para comparar as propostas recebidas entre si.'});
   if(s.n('prazo_obra',0)<=2&&c.U>2) o.push({lv:'warn',t:'Prazo de '+F.num(s.n('prazo_obra'))+' mês(es) para '+F.num(c.U)+' unidades parece curto. Confirme com o fornecedor e inclua o tempo de aprovação das licenças.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Comparar as propostas pelo custo por m², com o mesmo escopo'},{id:'a5_2',text:'Confirmar por escrito se frete, fundação e montagem estão incluídos'},{id:'a5_3',text:'Listar as áreas de apoio que a operação vai exigir'}]}
]},
/* 6 */
{title:'Equipamentos e capital de giro', screens:[
 {kind:'learn', title:'Pronto para receber hóspede não é o mesmo que obra pronta',
  body:'<p>Com a obra concluída, ainda faltam: <b>mobiliário e enxoval</b> de cada unidade (cama, colchão, roupa de cama e banho, cozinha, eletrodomésticos, decoração), <b>equipamentos gerais</b> (lavanderia, ferramentas, gerador, carrinho de limpeza) e a <b>pré-operação</b> (fotos profissionais, site, identidade visual, enxoval de reserva, treinamento).</p><p>Depois vem o <b>capital de giro</b>: dinheiro guardado para pagar os custos fixos nos primeiros meses, enquanto as reservas ainda estão começando. Ele é calculado como <b>custo fixo mensal × meses de cobertura</b>. Sem ele, o empreendimento pode ficar pronto e não ter caixa para funcionar.</p>',
  example:'Exemplo ilustrativo: custo fixo de R$ 5.000 por mês e 6 meses de cobertura = R$ 30.000 de capital de giro reservados antes da inauguração.'},
 {kind:'compare', title:'Inaugurar no limite × inaugurar com fôlego',
  cols:[{h:'No limite',type:'bad',items:['Mobiliar com o que sobrou do orçamento','Sem fotos profissionais no lançamento','Nenhuma reserva para os primeiros meses','Contar com as primeiras reservas para pagar contas']},
        {h:'Com fôlego',type:'good',items:['Mobiliário e enxoval orçados por unidade','Pré-operação planejada (fotos, anúncio, site)','Capital de giro separado antes de inaugurar','Meses de cobertura definidos conscientemente']}]},
 {kind:'form', title:'Equipamentos, pré-operação e capital de giro',
  fields:[
   {id:'mob_unid',label:'Mobiliário, enxoval e eletrodomésticos por unidade',type:'money',required:true},
   {id:'equip_gerais',label:'Equipamentos gerais da operação (total)',type:'money',required:true,allowUnknown:true},
   {id:'pre_op',label:'Pré-operação: fotos, site, identidade visual, lançamento (total)',type:'money',required:true,allowUnknown:true},
   {id:'cf_mensal',label:'Custo fixo mensal previsto da operação',type:'money',required:true,help:'Energia, internet, funcionários, manutenção, contador, software. Use sua estimativa ou a de um estudo de operação.'},
   {id:'meses_giro',label:'Meses de custo fixo que você quer cobrir com capital de giro',type:'number',required:true,min:0,max:24,step:1,unit:'meses'}
  ]},
 {kind:'feedback', title:'Equipamentos e fôlego financeiro',
  metrics:function(s,c){return [{label:'Equipamentos e pré-operação',value:F.brl(c.equipamentos),tag:'calculado'},{label:'Capital de giro',value:F.brl(c.giro),tag:'calculado'}];},
  feedback:function(s,c){var o=[],m=s.n('meses_giro',0);
   if(m===0) o.push({lv:'bad',t:'Nenhum mês de capital de giro. O empreendimento ficaria pronto sem caixa para pagar os custos fixos até as reservas engrenarem.'});
   else if(m<3) o.push({lv:'warn',t:'Cobertura de '+F.num(m)+' mês(es). Os primeiros meses de um empreendimento novo costumam ter ocupação baixa; considere ampliar essa reserva.'});
   else o.push({lv:'ok',t:'Capital de giro para '+F.num(m)+' meses ('+F.brl(c.giro)+'). Você terá fôlego para ajustar a operação.'});
   if(s.unknown('pre_op')) o.push({lv:'warn',t:'Pré-operação não orçada (considerada R$ 0). Fotos e anúncio bem feitos são a vitrine do lançamento.'});
   if(s.unknown('equip_gerais')) o.push({lv:'warn',t:'Equipamentos gerais não orçados (considerados R$ 0). Liste lavanderia, ferramentas e materiais de manutenção.'});
   if(s.n('mob_unid',0)===0) o.push({lv:'bad',t:'Mobiliário por unidade igual a zero. Confirme se a cotação da unidade já inclui móveis e enxoval.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Montar a lista completa de mobiliário e enxoval de uma unidade, com preços'},{id:'a6_2',text:'Separar o capital de giro em conta própria antes da inauguração'},{id:'a6_3',text:'Orçar fotos profissionais e anúncio para o lançamento'}]}
]},
/* 7 */
{title:'Orçamento consolidado', screens:[
 {kind:'learn', title:'Contingência e cenários: o orçamento que aguenta imprevistos',
  body:'<p>Todo orçamento de obra tem incertezas: chuva atrasa, o solo exige mais fundação, um material sobe de preço. Por isso, o orçamento consolidado inclui:</p><ul><li><b>Contingência:</b> um percentual sobre os custos de implantação reservado para imprevistos. O percentual é uma escolha sua, idealmente discutida com o engenheiro ou arquiteto do projeto.</li><li><b>Variação de custo:</b> quanto os preços podem subir entre a cotação e a compra (validade vencida, reajustes, escopo maior).</li></ul><p>A Calculadora monta três cenários: <b>Otimista</b> (as cotações se confirmam, sem imprevistos), <b>Intermediário</b> (com contingência) e <b>Conservador</b> (com variação de custo e contingência). O capital de giro entra igual nos três.</p>',
  example:'Exemplo ilustrativo: R$ 400.000 de implantação, contingência de 10% e variação de 15%. Otimista: R$ 400.000. Intermediário: R$ 440.000. Conservador: 400.000 × 1,15 × 1,10 = R$ 506.000. Mais o capital de giro em todos.'},
 {kind:'compare', title:'Orçamento frágil × orçamento robusto',
  cols:[{h:'Frágil',type:'bad',items:['Um único número, sem margem','Sem contingência','Cotações vencidas','Recursos disponíveis exatamente iguais ao orçamento']},
        {h:'Robusto',type:'good',items:['Três cenários com premissas explícitas','Contingência definida com o profissional da obra','Cotações dentro da validade','Folga entre recursos e cenário conservador']}]},
 {kind:'form', title:'Contingência, variação e recursos',
  fields:[
   {id:'contingencia',label:'Contingência para imprevistos',type:'percent',required:true,max:50,help:'Percentual sobre os custos de implantação (não incide sobre o capital de giro). Defina com o profissional responsável.'},
   {id:'variacao',label:'Variação de custo para o cenário conservador',type:'percent',required:true,max:60,help:'Quanto os preços podem subir até a compra.'},
   {id:'recursos',label:'Recursos disponíveis para o projeto',type:'money',required:true,allowUnknown:true,help:'Capital próprio e aportes já confirmados.'}
  ]},
 {kind:'feedback', title:'Seu orçamento consolidado',
  metrics:function(s,c){return [{label:'Otimista',value:F.brl(c.otim),tag:'calculado'},{label:'Intermediário',value:F.brl(c.inter),tag:'calculado'},{label:'Conservador',value:F.brl(c.cons),tag:'calculado'},{label:'Custo total por unidade (intermediário)',value:F.brl(c.porUnid),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:'info',t:'A unidade em si (construção sem frete) representa <b>'+F.pct(c.pesoCabana*100,0)+'</b> dos custos de implantação. O restante está em projetos, infraestrutura, áreas comuns, frete, mobiliário e pré-operação.'});
   if(s.n('contingencia',0)===0) o.push({lv:'bad',t:'Contingência zero: qualquer imprevisto vira falta de dinheiro. Defina um percentual com o profissional da obra.'});
   if(c.gap!=null){
    if(c.gap<0) o.push({lv:'bad',t:'Seus recursos ('+F.brl(s.n('recursos'))+') cobrem '+F.pct(c.cobertura*100,0)+' do cenário intermediário. Faltam <b>'+F.brl(-c.gap)+'</b>. Caminhos: reduzir unidades, implantar por etapas, rever padrão ou buscar parceria.'});
    else if(c.gapCons<0) o.push({lv:'warn',t:'Os recursos cobrem o cenário intermediário, mas não o conservador (faltariam '+F.brl(-c.gapCons)+'). A folga é pequena.'});
    else o.push({lv:'ok',t:'Seus recursos cobrem até o cenário conservador, com folga de '+F.brl(c.gapCons)+'.'});
   } else o.push({lv:'warn',t:'Recursos disponíveis não informados. Sem esse número, não é possível saber se o projeto cabe no seu bolso.'});
   o.push({lv:'info',t:'Desembolso médio durante a obra: '+F.brl(c.desembMes)+' por mês, em '+F.num(s.n('prazo_obra'))+' meses (intermediário, sem capital de giro).'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Validar a contingência com o engenheiro ou arquiteto do projeto'},{id:'a7_2',text:'Atualizar as cotações vencidas antes de qualquer contratação'},{id:'a7_3',text:'Montar o cronograma de desembolso mês a mês com o fornecedor'}]}
]}
],

compute:function(s){
 var c={};
 c.U=Math.max(1,s.n('unidades',1)); c.leitos=c.U*s.n('hospedes_unid',1);
 var pr=rowsOf(s,'projetos'); c.projetos=ZA.listSum(pr); c.projItens=pr.length;
 c.temResp=pr.some(function(r){return /respons|ART|RRT/i.test(r.name||'');});
 var ir=rowsOf(s,'infra'); c.infra=ZA.listSum(ir); c.infraItens=ir.length; c.infraUnid=c.infra/c.U;
 c.infraMaior=ir.slice().sort(function(a,b){return b.value-a.value;})[0]||null;
 var ex=s.v.infra_existe||[], lac=[];
 var mapa=[['acesso',/acesso|estrada/i,'acesso transitável'],['energia',/el[eé]tric|energia/i,'energia elétrica'],['agua',/[aá]gua|po[cç]o/i,'água suficiente'],['esgoto',/esgoto|fossa/i,'solução de esgoto'],['internet',/internet/i,'internet']];
 mapa.forEach(function(m){ if(ex.indexOf(m[0])<0 && !ir.some(function(r){return m[1].test(r.name||'');})) lac.push(m[2]); });
 c.infraLacunas=lac;
 c.cu=s.n('custo_unid',0); c.frete=s.n('frete_unid',0)||0;
 c.comuns=ZA.listSum(rowsOf(s,'comuns'));
 c.construcao=c.U*(c.cu+c.frete)+c.comuns;
 c.m2=s.has('area_unid')&&s.n('area_unid')>0?(c.cu+c.frete)/s.n('area_unid'):null;
 c.equipamentos=c.U*s.n('mob_unid',0)+s.n('equip_gerais',0)+s.n('pre_op',0);
 c.giro=s.n('cf_mensal',0)*s.n('meses_giro',0);
 c.capex=c.projetos+c.infra+c.construcao+c.equipamentos;
 var ct=s.n('contingencia',0)/100, vr=s.n('variacao',0)/100; c.ct=ct; c.vr=vr;
 c.otim=c.capex+c.giro;
 c.inter=c.capex*(1+ct)+c.giro;
 c.cons=c.capex*(1+vr)*(1+ct)+c.giro;
 c.contValor=c.capex*ct;
 c.porUnid=c.inter/c.U; c.porLeito=c.leitos>0?c.inter/c.leitos:null;
 c.pesoCabana=c.capex>0?c.U*c.cu/c.capex:0;
 c.desembMes=c.capex*(1+ct)/Math.max(1,s.n('prazo_obra',1));
 if(s.has('recursos')){var r=s.n('recursos'); c.gap=r-c.inter; c.gapCons=r-c.cons; c.gapOtim=r-c.otim; c.cobertura=c.inter>0?r/c.inter:null;}
 else {c.gap=null; c.gapCons=null; c.gapOtim=null; c.cobertura=null;}
 c.blocos=[['Projetos, licenças e documentação',c.projetos],['Infraestrutura',c.infra],['Construção das unidades',c.U*c.cu],['Frete e montagem',c.U*c.frete],['Áreas comuns e de apoio',c.comuns],['Mobiliário e enxoval',c.U*s.n('mob_unid',0)],['Equipamentos gerais',s.n('equip_gerais',0)],['Pré-operação',s.n('pre_op',0)]];
 c.maiorBloco=c.blocos.slice().sort(function(a,b){return b[1]-a[1];})[0];
 return c;
},

metrics:function(s,c){return [
 {label:'Custos de implantação (sem contingência)',value:F.brl(c.capex),tag:'calculado'},
 {label:'Contingência',value:F.brl(c.contValor)+' ('+F.pct(c.ct*100,0)+')',tag:'informado'},
 {label:'Capital de giro',value:F.brl(c.giro),tag:'calculado'},
 {label:'Orçamento intermediário',value:F.brl(c.inter),tag:'calculado'},
 {label:'Orçamento conservador',value:F.brl(c.cons),tag:'calculado'},
 {label:'Custo total por unidade',value:F.brl(c.porUnid),tag:'calculado'},
 {label:'Peso da unidade no investimento',value:F.pct(c.pesoCabana*100,0),tag:'calculado'},
 {label:'Recursos − orçamento intermediário',value:c.gap==null?'—':F.brl(c.gap),tag:c.gap==null?'hipotese':'calculado'}
];},

priorities:function(s,c){var L=[];
 if(c.gap!=null&&c.gap<0) L.push({title:'Fechar a diferença de '+F.brl(-c.gap)+' entre recursos e orçamento',why:'Começar a obra sem cobrir o cenário intermediário aumenta o risco de obra parada.',score:10});
 if(s.t('qualidade_cot')==='nenhum') L.push({title:'Conseguir cotações formais para os itens principais',why:'Sem valores reais, o orçamento é apenas um roteiro.',score:9});
 if(c.infraLacunas.length) L.push({title:'Orçar a infraestrutura que falta: '+c.infraLacunas.join(', '),why:'O terreno não tem esses itens e eles não aparecem no orçamento.',score:9});
 if(s.t('status_lic')==='nada') L.push({title:'Fazer a consulta prévia de licenças antes de contratar a obra',why:'Exigências e prazos de aprovação podem mudar o projeto e o custo.',score:8});
 if(s.n('contingencia',0)===0) L.push({title:'Definir uma contingência com o profissional da obra',why:'Sem reserva para imprevistos, qualquer desvio vira falta de caixa.',score:8});
 if(s.n('meses_giro',0)<3) L.push({title:'Ampliar o capital de giro para pelo menos 3 meses de custo fixo',why:'Os primeiros meses de operação costumam ter menos reservas.',score:7});
 if(s.t('qualidade_cot')==='informal') L.push({title:'Transformar valores informais em propostas por escrito',why:'Valores de anúncio não mostram escopo nem validade.',score:7});
 if(s.n('n_cotacoes',0)<3) L.push({title:'Comparar ao menos 3 fornecedores com o mesmo escopo',why:'Uma única proposta não permite saber se o valor está coerente.',score:6});
 if(c.projItens<3) L.push({title:'Levantar com arquiteto/engenheiro os projetos e licenças aplicáveis',why:'Apenas '+c.projItens+' item(ns) de projeto orçado(s).',score:6});
 if(c.gap!=null&&c.gap>=0&&c.gapCons<0) L.push({title:'Criar folga para o cenário conservador',why:'Os recursos cobrem o intermediário, mas não o conservador.',score:6});
 if(c.gap==null) L.push({title:'Definir quanto de recurso está realmente disponível',why:'Sem isso, não há como saber se o projeto cabe no orçamento.',score:7});
 if(c.U>=6||(c.gap!=null&&c.gap<0)) L.push({title:'Simular a implantação por etapas',why:'Começar com parte das unidades reduz o capital inicial.',score:5});
 if(s.unknown('frete_unid')) L.push({title:'Confirmar frete e montagem com o fornecedor',why:'Item considerado R$ 0 no cálculo.',score:4});
 if(c.comuns===0) L.push({title:'Orçar as áreas de apoio da operação',why:'Lavanderia, rouparia e depósito são necessários mesmo em projetos pequenos.',score:4});
 if(s.unknown('pre_op')) L.push({title:'Orçar fotos e anúncio para o lançamento',why:'A pré-operação ficou fora do orçamento.',score:3});
 return L;},

report:function(s,c){
 var inf=tag('informado'), calc=tag('calculado'), hip=tag('hipotese','hipótese');
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Modelo / padrão',esc(({cabana:'Cabanas',chale:'Chalés',glamping:'Glamping',container:'Módulos / contêineres',pousada:'Pequena pousada',outro:'Outro'})[s.t('modelo')]||'—')+' · '+esc(({economico:'econômico',intermediario:'intermediário',alto:'alto padrão'})[s.t('padrao')]||'—'),inf],
  ['Unidades / capacidade',F.num(c.U)+' unidades · '+F.num(c.leitos)+' hóspedes',inf],
  ['Área por unidade',s.has('area_unid')?F.num(s.n('area_unid'))+' m²':'—',s.has('area_unid')?inf:hip],
  ['Tipo de valores usados',esc(({formal:'Cotações formais',informal:'Valores informais',nenhum:'Sem cotações'})[s.t('qualidade_cot')]||'—'),inf],
  ['Construção por unidade',F.brl(c.cu),inf],
  ['Frete e montagem por unidade',F.brl(c.frete),s.unknown('frete_unid')?hip+' R$ 0':inf],
  ['Equipamentos gerais / pré-operação',F.brl(s.n('equip_gerais',0))+' / '+F.brl(s.n('pre_op',0)),(s.unknown('equip_gerais')||s.unknown('pre_op'))?hip+' R$ 0 no que faltou':inf],
  ['Custo fixo mensal × meses de giro',F.brl(s.n('cf_mensal',0))+' × '+F.num(s.n('meses_giro',0)),inf],
  ['Contingência',F.pct(c.ct*100,0),inf],
  ['Variação de custo (conservador)',F.pct(c.vr*100,0),inf],
  ['Recursos disponíveis',s.has('recursos')?F.brl(s.n('recursos')):'—',s.has('recursos')?inf:hip]],[1]);
 var comp=ZA.table(['Bloco','Valor','% da implantação'],c.blocos.map(function(b){return [b[0],F.brl(b[1]),F.pct(c.capex>0?b[1]/c.capex*100:0,1)];}).concat([['<b>Subtotal de implantação</b>','<b>'+F.brl(c.capex)+'</b>','100,0%'],['Contingência ('+F.pct(c.ct*100,0)+')',F.brl(c.contValor),'—'],['Capital de giro',F.brl(c.giro),'—']]),[1,2]);
 var det=function(id,t){var r=rowsOf(s,id);return r.length?ZA.table([t,'Valor'],r.map(function(x){return [esc(x.name||'(sem descrição)'),F.brl(x.value)];}),[1]):'<p class="za-small">Nenhum item com valor em '+t.toLowerCase()+'.</p>';};
 var cen=ZA.table(['Item','Otimista','Intermediário','Conservador'],[
  ['Implantação',F.brl(c.capex),F.brl(c.capex*(1+c.ct)),F.brl(c.capex*(1+c.vr)*(1+c.ct))],
  ['Capital de giro',F.brl(c.giro),F.brl(c.giro),F.brl(c.giro)],
  ['<b>Total</b>','<b>'+F.brl(c.otim)+'</b>','<b>'+F.brl(c.inter)+'</b>','<b>'+F.brl(c.cons)+'</b>'],
  ['Por unidade',F.brl(c.otim/c.U),F.brl(c.inter/c.U),F.brl(c.cons/c.U)],
  ['Recursos − total',c.gapOtim==null?'—':F.brl(c.gapOtim),c.gap==null?'—':F.brl(c.gap),c.gapCons==null?'—':F.brl(c.gapCons)]],[1,2,3]);
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido para fechar o orçamento</b><ol>'+
  '<li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Revisar todos os itens com valor zero')+'.</li>'+
  '<li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Pedir propostas formais aos fornecedores principais')+'.</li>'+
  '<li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Validar contingência e cronograma com o profissional da obra')+'.</li>'+
  '<li><b>Semana 4:</b> refazer a Calculadora com as cotações atualizadas e decidir: implantar tudo, implantar por etapas ou ajustar o projeto.</li></ol>'+
  '<p class="za-small">Antes de contratar a obra: consulta prévia à prefeitura, verificação documental do terreno com advogado e responsável técnico definido.</p></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Composição do investimento',html:comp+'<p class="za-small">Maior bloco: <b>'+esc(c.maiorBloco[0])+'</b>. A unidade em si representa '+F.pct(c.pesoCabana*100,0)+' dos custos de implantação.</p>'},
  {title:'Detalhamento dos itens informados',html:det('projetos','Projetos e licenças')+det('infra','Infraestrutura')+det('comuns','Áreas comuns')},
  {title:'Três cenários de orçamento',html:'<ul class="za-small"><li><b>Otimista:</b> cotações se confirmam, sem imprevistos.</li><li><b>Intermediário:</b> implantação + contingência de '+F.pct(c.ct*100,0)+'.</li><li><b>Conservador:</b> implantação + variação de custo de '+F.pct(c.vr*100,0)+' e contingência.</li></ul>'+cen+'<p class="za-small">Contingência aplicada sobre a implantação; capital de giro igual nos três. Cenários são simulações a partir das suas premissas, não previsões de custo.</p>'+(c.infraLacunas.length?'<p class="za-missing">Atenção: o terreno não tem '+esc(c.infraLacunas.join(', '))+' e esses itens não foram orçados. O total real tende a ser maior.</p>':'')},
  {title:'Desembolso durante a obra',html:'<p>Prazo informado: <b>'+F.num(s.n('prazo_obra'))+' meses</b>. Desembolso médio: <b>'+F.brl(c.desembMes)+' por mês</b> (implantação com contingência ÷ prazo). O capital de giro deve estar separado antes da inauguração.</p><p class="za-small">A distribuição real depende do contrato com cada fornecedor (sinal, etapas, entrega).</p>'}
 ],plan:plan};
}
});
})();
