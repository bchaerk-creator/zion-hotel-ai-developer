/* ZAR-A09 · Vale a Pena Investir em uma Cabana ou Airbnb? · Simulador de Viabilidade Zion */
(function(){
var F=ZA.fmt, esc=ZA.esc;
var RISCOS=[{v:'sazonal',l:'Demanda muito concentrada em poucos meses'},{v:'acesso',l:'Acesso difícil (estrada de terra, distância, sinalização)'},{v:'concorrencia',l:'Muitas hospedagens parecidas na região'},{v:'licencas',l:'Licenças, documentação ou regras do condomínio ainda pendentes'},{v:'reserva',l:'Sem reserva financeira além do investimento'},{v:'obra',l:'Obra com prazo ou orçamento ainda incertos'}];
var MODELOS={cabana:'Cabana',chale:'Chalé',glamping:'Glamping',casa:'Casa de temporada',pousada:'Pequena pousada'};
function arr(s,id){return Array.isArray(s.v[id])?s.v[id]:[];}
function rowsOk(s,id){return (s.v[id]||[]).filter(function(r){return r&&ZA.isNum(r.value)&&r.value>0;});}
function anos(v){return v==null?'não se paga no período':F.num(v,1)+' anos';}
function pctOr(v,d){return v==null?'—':F.pct(v*100,d==null?1:d);}

ZA.register({
id:'A09', code:'ZAR-A09', collection:'Hospedagem',
title:'Vale a Pena Investir em uma Cabana ou Airbnb?',
subtitle:'Faça as Contas Antes de Investir',
tool:'Simulador de Viabilidade Zion',
deliverable:'Estudo Econômico Preliminar',
nameField:'nome', propertyField:'propriedade',
disclaimer:'Este é um estudo econômico preliminar e educacional, construído inteiramente com as premissas que você informou. Ele não é recomendação de investimento, não substitui orçamento de obra, projeto, análise jurídica ou contábil e não garante ocupação, receita, lucro, retorno ou prazo de payback. Antes de investir, valide os números com cotações reais e consulte contador, engenheiro ou arquiteto e advogado.',

intro:[
 {kind:'mirror', title:'Antes de investir suas economias, descubra se a conta fecha.',
  lead:'Você viu cabanas lindas lotadas nas redes sociais, ouviu que “hospedagem dá dinheiro” e já tem até o lugar em mente. Mas quando tenta fazer as contas, os números não param quietos.',
  body:'<div class="za-card"><p>Talvez você esteja pensando:</p><ul><li>“Quanto preciso investir, de verdade, para deixar tudo pronto?”</li><li>“Com quantas noites vendidas por mês a conta fecha?”</li><li>“Em quantos anos recupero o dinheiro?”</li><li>“E se a ocupação for menor do que eu imagino?”</li></ul></div>'},
 {kind:'collapse', title:'Uma cabana bonita e uma diária alta não garantem um investimento rentável.',
  lead:'Diária alta com ocupação baixa, custo fixo esquecido e infraestrutura subestimada podem transformar um sonho em um investimento que demora décadas para voltar.',
  body:'<div class="za-card"><p>A pergunta certa não é “quanto vou faturar?”, e sim:</p><ol><li><b>Quanto custa tudo</b> (unidades, infraestrutura, projetos, imprevistos)?</li><li><b>Quanto sobra por ano</b> depois de comissões, impostos e custos?</li><li><b>Em quanto tempo o investimento volta</b>, num cenário prudente?</li></ol><p>Neste percurso você monta um estudo preliminar com três cenários e premissas explícitas. É um ponto de partida para decidir com mais clareza, não uma promessa de resultado.</p></div>'},
 {kind:'start', title:'Vamos montar o seu Estudo Econômico Preliminar',
  lead:'Em 7 pilares, você vai definir o modelo de negócio, levantar o investimento e a infraestrutura, estimar receitas e custos e comparar três cenários.',
  body:'<p>Tenha à mão, se possível: cotações de construção ou aquisição, orçamentos de infraestrutura e preços de hospedagens parecidas na região. Quando um valor for apenas sua estimativa, o estudo deve ser lido com ainda mais cautela.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Ana'},
   {id:'propriedade',label:'Nome do projeto',type:'text',required:true,placeholder:'Ex.: Cabanas Mirante do Vale'},
   {id:'destino',label:'Cidade / região do projeto',type:'text',required:true,placeholder:'Ex.: Urubici (SC)'},
   {id:'unidades',label:'Quantas unidades você planeja?',type:'number',required:true,min:1,max:100,step:1,unit:'unidade(s)'}
  ]}
],

pillars:[
/* 1 */
{title:'Modelo de negócio', screens:[
 {kind:'learn', title:'Antes dos números: que negócio é esse?',
  body:'<p>O mesmo terreno pode receber negócios muito diferentes. O <b>modelo</b> (cabana, chalé, glamping, casa de temporada, pousada) define o investimento por unidade, o tipo de hóspede e a operação. A <b>gestão</b> (você mesmo ou uma empresa terceirizada) muda os custos: a gestão terceirizada costuma cobrar um percentual da receita.</p><p>O <b>objetivo</b> também muda a leitura dos números: quem busca renda complementar aceita prazos diferentes de quem quer fazer da hospedagem o negócio principal.</p>',
  example:'Exemplo ilustrativo: duas cabanas com a mesma diária. Na primeira, o dono faz a gestão; na segunda, paga 20% da receita a uma administradora. Com receita de R$ 120 mil por ano, a diferença é de R$ 24 mil anuais no resultado.'},
 {kind:'compare', title:'Decidir pelo encanto × decidir pelo modelo',
  cols:[{h:'Pelo encanto',type:'bad',items:['“Vi no Instagram e quero igual”','Escolhe o modelo antes de olhar o terreno e o público','Não pensa em quem vai operar','Objetivo vago (“ganhar dinheiro”)']},
        {h:'Pelo modelo',type:'good',items:['Modelo coerente com terreno, público e orçamento','Gestão definida desde o início','Custos da operação considerados','Objetivo e prazo claros']}]},
 {kind:'form', title:'O seu modelo de negócio',
  fields:[
   {id:'mn_modelo',label:'Modelo de hospedagem',type:'radio',required:true,options:[{v:'cabana',l:'Cabana'},{v:'chale',l:'Chalé'},{v:'glamping',l:'Glamping'},{v:'casa',l:'Casa de temporada'},{v:'pousada',l:'Pequena pousada'}]},
   {id:'mn_gestao',label:'Quem fará a gestão?',type:'radio',required:true,options:[{v:'propria',l:'Eu mesmo (ou minha família)'},{v:'terceirizada',l:'Empresa ou profissional terceirizado, com comissão'}]},
   {id:'mn_objetivo',label:'Qual é o objetivo principal?',type:'radio',required:true,options:[{v:'renda',l:'Renda complementar'},{v:'principal',l:'Negócio principal'},{v:'patrimonio',l:'Patrimônio e uso próprio, com alguma renda'}]},
   {id:'mn_terreno',label:'Situação do terreno ou imóvel',type:'radio',required:true,options:[{v:'proprio',l:'Já é meu'},{v:'comprar',l:'Vou comprar'},{v:'arrendar',l:'Vou arrendar ou alugar'}]}
  ]},
 {kind:'feedback', title:'O que o seu modelo pede',
  feedback:function(s){var o=[];
   o.push({lv:'info',t:'Modelo escolhido: <b>'+(MODELOS[s.t('mn_modelo')]||'—')+'</b> com '+F.num(s.n('unidades'))+' unidade(s). Os próximos pilares calculam o investimento e a operação desse modelo.'});
   if(s.t('mn_gestao')==='terceirizada') o.push({lv:'warn',t:'Com gestão terceirizada, inclua a comissão da gestora no Pilar 5. Ela incide sobre toda a receita.'});
   else o.push({lv:'info',t:'Gestão própria reduz custos, mas consome seu tempo. Se você tiver outro trabalho, considere o custo de alguém para limpeza e atendimento.'});
   if(s.t('mn_terreno')==='comprar') o.push({lv:'warn',t:'Comprar o terreno aumenta bastante o investimento. Inclua o valor no Pilar 2 e, antes de qualquer compra, verifique documentação e restrições com um advogado.'});
   if(s.t('mn_terreno')==='proprio') o.push({lv:'info',t:'Terreno próprio: ele não entra como desembolso, mas tem valor. Se quiser, inclua-o no investimento para ver o retorno sobre o patrimônio todo.'});
   if(s.t('mn_terreno')==='arrendar') o.push({lv:'info',t:'Com arrendamento, o valor mensal entra como custo fixo no Pilar 5. Contratos de arrendamento devem ser analisados por um advogado.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Escrever em uma frase o objetivo do investimento e o prazo aceitável'},{id:'a1_2',text:'Definir quem vai operar no dia a dia'},{id:'a1_3',text:'Verificar documentação e restrições do terreno com profissional habilitado'}]}
]},
/* 2 */
{title:'Investimento inicial', screens:[
 {kind:'learn', title:'Investimento é tudo o que sai antes da primeira reserva',
  body:'<p>O erro mais comum é olhar só o preço da cabana. O investimento inicial inclui: terreno (se for comprar), construção ou aquisição das unidades, projetos, licenças e taxas, mobiliário, enxoval e equipamentos, decoração, fotos e anúncio, e o <b>capital de giro</b> para pagar as contas nos primeiros meses, quando as reservas ainda estão começando.</p><p>Sobre o total, aplique uma <b>contingência</b>: um percentual para imprevistos. Em obras, imprevisto não é exceção. Se os valores forem estimativas suas, e não cotações, prefira uma contingência maior.</p>',
  example:'Exemplo ilustrativo: R$ 385 mil em unidades, projetos, mobiliário e capital de giro, mais R$ 55 mil de infraestrutura, com 10% de contingência: investimento total de R$ 484 mil.'},
 {kind:'compare', title:'Orçamento de folheto × orçamento completo',
  cols:[{h:'Orçamento de folheto',type:'bad',items:['Só o kit da cabana','Sem frete, fundação e instalação','Sem móveis e enxoval','Sem capital de giro e sem contingência']},
        {h:'Orçamento completo',type:'good',items:['Unidade instalada e pronta para uso','Projetos, licenças e taxas','Mobiliário, enxoval, fotos e anúncio','Capital de giro e contingência']}]},
 {kind:'form', title:'O seu investimento nas unidades', intro:'Informe valores <b>totais</b> do projeto (todas as unidades). A infraestrutura vem no próximo pilar.',
  fields:[
   {id:'inv',label:'Investimento inicial',type:'list',required:true,preset:['Terreno (se for comprar)','Construção ou aquisição das unidades','Projetos, licenças e taxas','Mobiliário, enxoval e equipamentos','Decoração, fotos e anúncio','Capital de giro inicial'],namePlaceholder:'Item',valuePlaceholder:'R$'},
   {id:'inv_origem',label:'De onde vêm esses valores?',type:'radio',required:true,options:[{v:'cotacao',l:'Cotações formais de fornecedores'},{v:'misto',l:'Parte cotação, parte estimativa'},{v:'estimativa',l:'Estimativa minha'}]},
   {id:'inv_cont',label:'Contingência para imprevistos',type:'percent',required:true,max:50,help:'Percentual aplicado sobre investimento e infraestrutura.'}
  ]},
 {kind:'feedback', title:'Composição do investimento',
  metrics:function(s,c){return [{label:'Unidades e itens',value:F.brl0(c.invItens),tag:'informado'},{label:'Investimento por unidade (itens)',value:F.brl0(c.invItens/c.U),tag:'calculado'},{label:'Contingência',value:F.pct(c.cont*100,0),tag:'informado'}];},
  feedback:function(s,c){var o=[];var n=rowsOk(s,'inv').map(function(r){return (r.name||'').toLowerCase();}).join('|');
   if(!/giro/.test(n)) o.push({lv:'warn',t:'Não há capital de giro no investimento. Os primeiros meses costumam ter ocupação baixa e as contas chegam do mesmo jeito.'});
   if(!/projeto|licen|taxa/.test(n)) o.push({lv:'warn',t:'Projetos, licenças e taxas não foram informados. Consulte a prefeitura e um engenheiro ou arquiteto sobre o que o seu projeto exige.'});
   if(!/mobili|enxoval|equip/.test(n)) o.push({lv:'warn',t:'Mobiliário, enxoval e equipamentos não aparecem. Eles costumam pesar no orçamento.'});
   if(s.t('inv_origem')==='estimativa'&&c.cont<0.15) o.push({lv:'warn',t:'Valores são estimativas suas e a contingência é de '+F.pct(c.cont*100,0)+'. Com estimativas, uma margem de imprevistos maior é mais prudente.'});
   if(c.cont===0) o.push({lv:'bad',t:'Contingência zero: qualquer imprevisto de obra sai do seu bolso fora do planejado.'});
   if(c.invMaior) o.push({lv:'info',t:'O maior item é <b>'+esc(c.invMaior.name)+'</b> ('+F.brl0(c.invMaior.value)+'). É onde uma segunda cotação mais pode mudar o resultado.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Pedir pelo menos 2 cotações formais para o maior item do investimento'},{id:'a2_2',text:'Incluir capital de giro para os primeiros meses de operação'},{id:'a2_3',text:'Consultar a prefeitura e um engenheiro ou arquiteto sobre projetos e licenças'}]}
]},
/* 3 */
{title:'Infraestrutura', screens:[
 {kind:'learn', title:'A infraestrutura que ninguém fotografa',
  body:'<p>Antes de a primeira cabana ficar de pé, o terreno precisa de <b>acesso</b> (estrada interna, estacionamento), <b>energia</b> (rede, transformador, solar), <b>água</b> (poço, reservatório, tratamento), <b>esgoto</b> (fossa, biodigestor, conforme exigências locais), <b>internet</b> e iluminação.</p><p>Em áreas rurais, a infraestrutura pode custar tanto quanto as próprias unidades, e é a parte mais sujeita a surpresas. Por isso ela tem um pilar só para ela.</p>',
  example:'Exemplo ilustrativo: um terreno a 800 m da rede elétrica pode exigir extensão de rede ou sistema solar; um terreno sem rede de esgoto exige solução individual aprovada. São valores que só uma visita técnica e cotações confirmam.'},
 {kind:'compare', title:'Supor × verificar',
  cols:[{h:'Supor',type:'bad',items:['“Tem luz na estrada, então é fácil”','“Faço um poço depois”','Esgoto resolvido “do jeito que der”','Internet pelo celular']},
        {h:'Verificar',type:'good',items:['Consulta à concessionária de energia','Teste ou laudo da fonte de água','Solução de esgoto conforme exigência local, com profissional','Teste de sinal e cotação de internet']}]},
 {kind:'form', title:'O custo da sua infraestrutura', intro:'Deixe em branco o que já existe ou não se aplica.',
  fields:[
   {id:'infra',label:'Infraestrutura',type:'list',required:false,preset:['Acesso e estrada interna','Energia (rede, transformador, solar)','Água (poço, reservatório, tratamento)','Esgoto (fossa, biodigestor)','Internet','Paisagismo, estacionamento e iluminação'],namePlaceholder:'Item',valuePlaceholder:'R$'},
   {id:'infra_status',label:'Como está a infraestrutura do terreno hoje?',type:'radio',required:true,options:[{v:'existente',l:'Já existe quase tudo (energia, água, acesso)'},{v:'parcial',l:'Existe uma parte'},{v:'inexistente',l:'Praticamente nada, terreno bruto'}]}
  ]},
 {kind:'feedback', title:'Investimento total do projeto',
  metrics:function(s,c){return [{label:'Infraestrutura',value:F.brl0(c.infra),tag:'informado'},{label:'Contingência',value:F.brl0(c.invCont),tag:'calculado'},{label:'Investimento total',value:F.brl0(c.invTotal),tag:'calculado'},{label:'Investimento total por unidade',value:F.brl0(c.invTotal/c.U),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(s.t('infra_status')==='inexistente'&&c.infra<c.invItens*0.1) o.push({lv:'warn',t:'Terreno bruto com infraestrutura orçada em '+F.brl0(c.infra)+' ('+F.pct(c.invBase>0?c.infra/c.invBase*100:0,0)+' do total). Confirme com cotações: em terreno sem estrutura, esse valor costuma ser subestimado.'});
   if(c.infra===0&&s.t('infra_status')!=='existente') o.push({lv:'bad',t:'Nenhum valor de infraestrutura informado, mas o terreno não tem estrutura completa. O investimento total está incompleto.'});
   if(c.invBase>0) o.push({lv:'info',t:'A infraestrutura representa '+F.pct(c.infra/c.invBase*100,0)+' do investimento antes da contingência. Investimento total: <b>'+F.brl0(c.invTotal)+'</b>.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Consultar a concessionária de energia sobre a ligação no terreno'},{id:'a3_2',text:'Verificar a solução de água e esgoto exigida no município com profissional habilitado'},{id:'a3_3',text:'Testar o sinal de internet e celular no local'}]}
]},
/* 4 */
{title:'Receitas', screens:[
 {kind:'learn', title:'Receita = noites vendidas × diária',
  body:'<p>A receita anual de hospedagem é: <b>unidades × noites disponíveis por mês × meses de operação × ocupação × diária média</b>. Receitas extras (café da manhã, experiências) entram à parte.</p><p>A ocupação é a premissa mais sensível do estudo. Ela não deve vir do melhor mês de um vizinho, e sim de uma média anual prudente. Pense também nos primeiros meses: hospedagens novas costumam levar um tempo para formar avaliações e ganhar ritmo. Se não houver dados da região, trate o número como hipótese e olhe com atenção o cenário conservador.</p>',
  example:'Exemplo ilustrativo: 2 cabanas × 30 noites × 12 meses × 40% de ocupação = 288 noites por ano. A R$ 450, são R$ 129.600 de receita de hospedagem por ano.'},
 {kind:'compare', title:'Receita de sonho × receita prudente',
  cols:[{h:'De sonho',type:'bad',items:['Ocupação de feriado como média do ano','Diária da alta temporada o ano todo','Ignora meses fechados para manutenção','Conta extras como certos']},
        {h:'Prudente',type:'good',items:['Ocupação média anual, com fonte','Diária média ponderada pelas temporadas','Meses de operação realistas','Extras como complemento, não como base']}]},
 {kind:'form', title:'Suas premissas de receita',
  fields:[
   {id:'rc_diaria',label:'Diária média prevista (média do ano)',type:'money',required:true,min:1},
   {id:'rc_ocup',label:'Ocupação média anual prevista',type:'percent',required:true,min:1,max:100,help:'Noites vendidas ÷ noites disponíveis. Use uma média anual prudente.'},
   {id:'rc_noites',label:'Noites disponíveis por mês, por unidade (opcional)',type:'number',required:false,min:1,max:31,step:1,unit:'noites',help:'Em branco, o simulador usa o calendário real: os dias de cada mês, 365 por ano (366 em ano bissexto). Se preencher, o total do ano nunca passa dos dias reais.'},
   {id:'rc_ano',label:'Ano de referência (opcional)',type:'number',required:false,min:2000,max:2100,step:1,help:'Usado para saber se o ano tem 366 dias. Em branco, 365.'},
   {id:'rc_meses',label:'Meses de operação por ano',type:'number',required:true,min:1,max:12,step:1,unit:'meses'},
   {id:'rc_extras',label:'Receitas extras por mês de operação (café, experiências etc.)',type:'money',required:false,help:'Valor total do projeto; deixe em branco se não houver. O simulador ajusta esse valor proporcionalmente à ocupação de cada cenário.'}
  ]},
 {kind:'feedback', title:'Sua receita anual prevista',
  metrics:function(s,c){var b=c.cen[1];return [{label:'Noites vendidas/ano',value:F.num(b.noites,0),tag:'estimativa'},{label:'Receita de hospedagem/ano',value:F.brl0(b.recHosp),tag:'estimativa'},{label:'Receita bruta total/ano',value:F.brl0(b.recBruta),tag:'estimativa'}];},
  feedback:function(s,c){var o=[];var oc=s.n('rc_ocup',0);
   if(oc>70) o.push({lv:'warn',t:'Ocupação média anual de '+F.pct(oc,0)+' é uma premissa exigente para o ano inteiro. Confirme com dados da região e confira o cenário conservador.'});
   o.push({lv:'info',t:'No cenário intermediário, o projeto venderia cerca de '+F.num(c.cen[1].noites,0)+' noites por ano, ou '+F.num(c.cen[1].noites/12,0)+' por mês em média.'});
   if(c.ext>0&&c.cen[1].recBruta>0&&c.cen[1].recExtra/c.cen[1].recBruta>0.2) o.push({lv:'warn',t:'As receitas extras representam '+F.pct(c.cen[1].recExtra/c.cen[1].recBruta*100,0)+' da receita. Trate-as como complemento: o negócio deve se sustentar com a hospedagem.'});
   if(s.n('rc_meses',12)<12) o.push({lv:'info',t:'Operação de '+F.num(s.n('rc_meses'))+' meses por ano: os custos fixos continuam correndo nos meses fechados e estão considerados nos 12 meses.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Pesquisar diárias de 5 hospedagens parecidas na região em datas diferentes'},{id:'a4_2',text:'Buscar uma fonte para a ocupação média anual (associações, gestores locais, dados próprios)'},{id:'a4_3',text:'Considerar uma rampa de ocupação mais baixa no primeiro ano'}]}
]},
/* 5 */
{title:'Custos operacionais', screens:[
 {kind:'learn', title:'Operar custa, mesmo com a cabana vazia',
  body:'<p>Os custos da operação têm três partes:</p><ul><li><b>Fixos mensais</b>: energia e água (parte básica), internet, manutenção, funcionários, seguro, contador, arrendamento, software e anúncios. Correm os 12 meses do ano.</li><li><b>Por estadia</b>: limpeza, lavanderia e amenities, a cada troca de hóspede.</li><li><b>Percentuais sobre a receita</b>: comissão das plataformas, impostos e, se houver, a comissão da gestão terceirizada.</li></ul><p>O resultado anual é a receita menos tudo isso. Ele ainda não considera a depreciação nem a reposição futura de móveis e equipamentos: uma razão a mais para tratar o estudo com cautela.</p>',
  example:'Exemplo ilustrativo: R$ 3.200 de custos fixos por mês são R$ 38.400 por ano. Com 144 estadias a R$ 150 de limpeza e lavanderia, mais R$ 21.600. Comissão e imposto de 21% sobre R$ 135.600 de receita: R$ 28.476.'},
 {kind:'compare', title:'Custos lembrados × custos reais',
  cols:[{h:'Costumam lembrar',type:'bad',items:['Energia e internet','Limpeza','Comissão da plataforma']},
        {h:'Costumam esquecer',type:'good',items:['Manutenção e reposição de enxoval','Seguro, contador e taxas','Imposto sobre a receita','Custos nos meses de baixa ou fechados']}]},
 {kind:'form', title:'Os custos da sua operação', intro:'Valores do projeto inteiro (todas as unidades).',
  fields:[
   {id:'co_fixos',label:'Custos fixos mensais',type:'list',required:true,preset:['Energia e água (parte básica)','Internet','Manutenção e reposição','Funcionários ou diaristas fixos','Seguro','Contador e taxas','Arrendamento do terreno','Software, anúncios e site'],namePlaceholder:'Item',valuePlaceholder:'R$ / mês'},
   {id:'co_estadia',label:'Custo por estadia (limpeza, lavanderia, amenities)',type:'money',required:true},
   {id:'co_estmedia',label:'Estadia média prevista',type:'number',required:true,min:1,max:60,step:0.1,unit:'noites',allowUnknown:true,help:'Se não souber, o cálculo usa 2 noites como hipótese.'},
   {id:'co_comissao',label:'Comissão média das plataformas',type:'percent',required:true,max:40},
   {id:'co_imposto',label:'Imposto sobre a receita',type:'percent',required:true,max:30,allowUnknown:true,help:'Confirme com um contador o enquadramento do seu caso.'},
   {id:'co_gestao',label:'Comissão da gestão terceirizada (se houver)',type:'percent',required:false,max:40}
  ]},
 {kind:'feedback', title:'O peso dos custos',
  metrics:function(s,c){var b=c.cen[1];return [{label:'Custos fixos/ano',value:F.brl0(c.cfAno),tag:'calculado'},{label:'Custos por estadia/ano',value:F.brl0(b.cVar),tag:'estimativa'},{label:'Deduções sobre a receita',value:F.pct(c.ded*100),tag:'calculado'},{label:'Resultado anual (intermediário)',value:F.brl0(b.resultado),tag:'estimativa'}];},
  feedback:function(s,c){var o=[];var b=c.cen[1];
   if(s.unknown('co_imposto')) o.push({lv:'warn',t:'Imposto desconhecido: o cálculo considera 0%, o que deixa o resultado otimista. Consulte um contador.'});
   if(s.unknown('co_estmedia')) o.push({lv:'warn',t:'Estadia média desconhecida: usamos 2 noites como hipótese.'});
   if(s.t('mn_gestao')==='terceirizada'&&!s.n('co_gestao')) o.push({lv:'warn',t:'Você escolheu gestão terceirizada, mas não informou a comissão da gestora.'});
   if(rowsOk(s,'co_fixos').length<4) o.push({lv:'warn',t:'Poucos custos fixos informados. Confira manutenção, seguro, contador e funcionários.'});
   if(b.resultado<=0) o.push({lv:'bad',t:'No cenário intermediário, a operação fecha o ano com resultado de '+F.brl0(b.resultado)+'. Com essas premissas, o projeto não se paga.'});
   else o.push({lv:'info',t:'No cenário intermediário, sobram cerca de <b>'+F.brl0(b.resultado)+' por ano</b> ('+pctOr(b.margem,0)+' da receita bruta) antes de depreciação e imposto de renda.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Confirmar com um contador o imposto e o enquadramento do negócio'},{id:'a5_2',text:'Cotar limpeza e lavanderia por estadia com prestadores da região'},{id:'a5_3',text:'Incluir uma reserva mensal para manutenção e reposição'}]}
]},
/* 6 */
{title:'Indicadores financeiros', screens:[
 {kind:'learn', title:'Lucro, ROI e payback: o que cada um diz',
  body:'<ul><li><b>Resultado anual</b>: o que sobra no ano depois de deduções e custos operacionais (antes de depreciação e imposto de renda).</li><li><b>ROI anual</b>: resultado anual ÷ investimento total. Mostra quanto o investimento rende por ano, em percentual.</li><li><b>Payback simples</b>: investimento total ÷ resultado anual. Quantos anos o resultado leva para somar o valor investido, sem considerar inflação, juros ou reformas.</li><li><b>Ocupação de equilíbrio</b>: a ocupação em que o resultado anual é zero.</li></ul><p>Compare o ROI com o rendimento de uma aplicação de referência que você conheça: o investimento em hospedagem envolve trabalho e risco que uma aplicação não tem. Essa comparação é sua, e não uma recomendação.</p>',
  example:'Exemplo ilustrativo: investimento de R$ 484 mil e resultado de R$ 47.124 por ano. ROI = 47.124 ÷ 484.000 = <b>9,7% ao ano</b>. Payback simples = 484.000 ÷ 47.124 = <b>10,3 anos</b>.'},
 {kind:'compare', title:'Leitura apressada × leitura cuidadosa',
  cols:[{h:'Apressada',type:'bad',items:['Olha só a receita bruta','Usa o cenário otimista como base','Ignora o prazo de construção','Compara com o lucro de outra pessoa']},
        {h:'Cuidadosa',type:'good',items:['Olha o resultado depois de todos os custos','Testa o cenário conservador','Considera o tempo até a primeira reserva','Compara com seus próprios objetivos e alternativas']}]},
 {kind:'form', title:'Seus critérios de decisão',
  fields:[
   {id:'ind_ref',label:'Rendimento anual de uma aplicação que você usa como referência',type:'percent',required:true,max:50,allowUnknown:true,help:'Valor que você mesmo conhece (por exemplo, o rendimento da sua aplicação atual). Usado apenas para comparação.'},
   {id:'ind_prazo',label:'Prazo máximo de retorno que você considera aceitável',type:'number',required:true,min:1,max:50,step:1,unit:'anos'}
  ]},
 {kind:'feedback', title:'Seus indicadores',
  metrics:function(s,c){var b=c.cen[1];return [{label:'Resultado anual',value:F.brl0(b.resultado),tag:'estimativa'},{label:'ROI anual',value:pctOr(b.roi),tag:'calculado'},{label:'Payback simples',value:anos(b.payback),tag:'calculado'},{label:'Ocupação de equilíbrio',value:c.occBE==null||c.occBE>1?'inalcançável':F.pct(c.occBE*100),tag:'calculado'}];},
  feedback:function(s,c){var o=[];var b=c.cen[1],pz=s.n('ind_prazo'),rf=s.n('ind_ref');
   if(b.payback==null) o.push({lv:'bad',t:'Com as premissas do cenário intermediário, o resultado anual não é positivo e o investimento não retorna.'});
   else if(pz!=null&&b.payback>pz) o.push({lv:'warn',t:'O payback simples ('+anos(b.payback)+') é maior que o prazo que você considera aceitável ('+F.num(pz)+' anos).'});
   else if(pz!=null) o.push({lv:'info',t:'O payback simples ('+anos(b.payback)+') fica dentro do prazo que você considera aceitável ('+F.num(pz)+' anos), no cenário intermediário. Confira o conservador no próximo pilar.'});
   if(rf!=null&&b.roi!=null) o.push({lv:b.roi<rf/100?'warn':'info',t:'ROI anual estimado de '+pctOr(b.roi)+' contra '+F.pct(rf)+' da sua aplicação de referência. Lembre que a hospedagem envolve trabalho, risco e menor liquidez.'});
   if(s.unknown('ind_ref')) o.push({lv:'info',t:'Sem uma aplicação de referência, compare o ROI com o rendimento que você teria deixando o dinheiro aplicado.'});
   if(c.occBE!=null&&c.occBE<=1) o.push({lv:c.occBE>s.n('rc_ocup',0)/100*0.8?'warn':'info',t:'A ocupação de equilíbrio é de '+F.pct(c.occBE*100)+' (sua premissa: '+F.pct(s.n('rc_ocup',0),0)+'). Quanto mais perto uma da outra, menor a margem de segurança.'});
   else o.push({lv:'bad',t:'Mesmo com 100% de ocupação, a diária e os custos informados não fecham a conta.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Anotar o resultado, o ROI e o payback dos três cenários'},{id:'a6_2',text:'Comparar com o rendimento da sua alternativa atual'},{id:'a6_3',text:'Levar o estudo para um contador revisar as premissas'}]}
]},
/* 7 */
{title:'Cenários e decisão', screens:[
 {kind:'learn', title:'Decidir olhando para o cenário prudente',
  body:'<p>Nenhuma premissa é certa. Por isso o estudo mostra <b>três cenários</b>:</p><ul><li><b>Conservador</b>: ocupação e diária abaixo da sua premissa.</li><li><b>Intermediário</b>: suas premissas exatamente como informadas.</li><li><b>Otimista</b>: ocupação e diária acima da sua premissa.</li></ul><p>Você escolhe a variação. Uma boa pergunta para a decisão é: <b>“se o cenário conservador acontecer, eu consigo sustentar o projeto?”</b>. Liste também os riscos que não aparecem nos números: acesso, licenças, concorrência, prazo de obra.</p>',
  example:'Exemplo ilustrativo: com variação de 10 pontos de ocupação e 10% na diária, uma premissa de 40% a R$ 450 vira 30% a R$ 405 no conservador e 50% a R$ 495 no otimista.'},
 {kind:'compare', title:'Decisão por entusiasmo × decisão por cenários',
  cols:[{h:'Entusiasmo',type:'bad',items:['Só existe o cenário otimista','Riscos “resolvo depois”','Investe todas as economias','Sem plano se a ocupação vier menor']},
        {h:'Cenários',type:'good',items:['Conservador sustentável ou plano B definido','Riscos listados com responsável','Reserva financeira separada','Implantação por etapas, se necessário']}]},
 {kind:'form', title:'Seus cenários e riscos',
  fields:[
   {id:'ce_var_ocup',label:'Variação de ocupação entre os cenários',type:'number',required:true,min:0,max:50,step:1,unit:'pontos percentuais',help:'Ex.: 10 = conservador com 10 pontos a menos e otimista com 10 a mais.'},
   {id:'ce_var_diaria',label:'Variação da diária entre os cenários',type:'percent',required:true,max:50},
   {id:'ce_riscos',label:'Quais riscos se aplicam ao seu projeto?',type:'checks',options:RISCOS}
  ]},
 {kind:'feedback', title:'Seus três cenários',
  metrics:function(s,c){return c.cen.map(function(x){return {label:x.nome+' · resultado/ano',value:F.brl0(x.resultado),tag:'estimativa'};});},
  feedback:function(s,c){var o=[];var cs=c.cen[0],ot=c.cen[2];
   if(cs.resultado<=0) o.push({lv:'bad',t:'No cenário conservador ('+F.pct(cs.occ*100,0)+' de ocupação, '+F.brl0(cs.diaria)+' de diária), o resultado anual é '+F.brl0(cs.resultado)+'. Pergunte-se se você conseguiria sustentar esse cenário.'});
   else o.push({lv:'info',t:'Mesmo no conservador, o resultado anual seria positivo ('+F.brl0(cs.resultado)+'), com payback simples de '+anos(cs.payback)+'.'});
   o.push({lv:'info',t:'Entre o conservador e o otimista, o payback simples vai de <b>'+anos(cs.payback)+'</b> a <b>'+anos(ot.payback)+'</b>. É essa faixa, e não um número único, que descreve o projeto.'});
   var r=arr(s,'ce_riscos');
   if(r.length>=3) o.push({lv:'warn',t:'Você marcou '+r.length+' riscos. Antes de investir, defina como reduzir cada um; a implantação por etapas pode diminuir a exposição.'});
   if(r.indexOf('licencas')>=0) o.push({lv:'warn',t:'Pendências de licença ou documentação devem ser resolvidas com profissional habilitado antes de qualquer obra.'});
   if(r.indexOf('reserva')>=0) o.push({lv:'warn',t:'Sem reserva financeira além do investimento, um atraso de obra ou meses fracos podem comprometer o projeto.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Definir o que fazer se o cenário conservador acontecer'},{id:'a7_2',text:'Atribuir um responsável e um prazo para reduzir cada risco marcado'},{id:'a7_3',text:'Refazer o estudo com cotações reais antes de decidir'}]}
]}
],

compute:function(s){
 var c={}; c.U=s.n('unidades',1)||1;
 var inv=rowsOk(s,'inv'), inf=rowsOk(s,'infra');
 c.invItens=ZA.listSum(inv); c.infra=ZA.listSum(inf); c.invBase=c.invItens+c.infra;
 c.invMaior=inv.slice().sort(function(a,b){return b.value-a.value;})[0]||null;
 c.cont=s.n('inv_cont',0)/100; c.invCont=c.invBase*c.cont; c.invTotal=c.invBase+c.invCont;
 c.d=s.n('rc_diaria',0); c.occ=s.n('rc_ocup',1)/100; c.N=s.n('rc_noites',0); c.M=s.n('rc_meses',12);
 // A09 · calendário real (premissa aprovada pelo Bruno em 10/11/2026): 365 dias, ou 366 em ano bissexto,
 // distribuídos pelos meses de operação. Noites informadas por mês ficam limitadas aos dias reais (31 × 12 não vira 372).
 var anoRef=s.n('rc_ano',0); c.diasAno=(anoRef&&((anoRef%4===0&&anoRef%100!==0)||anoRef%400===0))?366:365;
 c.noitesUnAno=c.N>0?Math.min(c.N*c.M,c.diasAno*c.M/12):c.diasAno*c.M/12; c.ext=s.n('rc_extras',0)||0;
 c.cfMes=ZA.listSum(rowsOk(s,'co_fixos')); c.cfAno=c.cfMes*12;
 c.ce=s.n('co_estadia',0); c.est=s.n('co_estmedia',2)||2;
 c.ded=(s.n('co_comissao',0)+s.n('co_imposto',0)+(s.n('co_gestao',0)||0))/100;
 function cen(nome,occ,d){
  var noites=c.U*c.noitesUnAno*occ, recHosp=noites*d, recExtra=c.occ>0?c.ext*c.M*(occ/c.occ):0, recBruta=recHosp+recExtra;
  var dedV=recBruta*c.ded, estadias=noites/c.est, cVar=estadias*c.ce, res=recBruta-dedV-cVar-c.cfAno;
  return {nome:nome,occ:occ,diaria:d,noites:noites,recHosp:recHosp,recExtra:recExtra,recBruta:recBruta,ded:dedV,cVar:cVar,cFix:c.cfAno,resultado:res,
   margem:recBruta>0?res/recBruta:null,roi:c.invTotal>0?res/c.invTotal:null,payback:(res>0&&c.invTotal>0)?c.invTotal/res:null};
 }
 var vo=s.n('ce_var_ocup',0)/100, vd=s.n('ce_var_diaria',0)/100;
 c.cen=[cen('Conservador',Math.max(0.01,c.occ-vo),c.d*(1-vd)),cen('Intermediário',c.occ,c.d),cen('Otimista',Math.min(1,c.occ+vo),c.d*(1+vd))];
 var K=c.U*c.noitesUnAno*(c.d*(1-c.ded)-c.ce/c.est)+(c.occ>0?c.ext*c.M/c.occ*(1-c.ded):0);
 c.occBE=K>0?c.cfAno/K:null;
 var b=c.cen[1]; var den=b.noites*(1-c.ded);
 c.dBE=den>0?(c.cfAno+b.cVar-c.ext*c.M*(1-c.ded))/den:null;
 if(c.dBE!=null&&c.dBE<0) c.dBE=0;
 return c;
},

metrics:function(s,c){var b=c.cen[1];return [
 {label:'Investimento total',value:F.brl0(c.invTotal),tag:'calculado'},
 {label:'Receita bruta/ano (intermediário)',value:F.brl0(b.recBruta),tag:'estimativa'},
 {label:'Resultado anual (intermediário)',value:F.brl0(b.resultado),tag:'estimativa'},
 {label:'ROI anual (intermediário)',value:pctOr(b.roi),tag:'calculado'},
 {label:'Payback simples (intermediário)',value:anos(b.payback),tag:'calculado'},
 {label:'Ocupação de equilíbrio',value:c.occBE==null||c.occBE>1?'inalcançável':F.pct(c.occBE*100),tag:'calculado'},
 {label:'Diária de equilíbrio (na ocupação prevista)',value:c.dBE==null?'—':F.brl0(c.dBE),tag:'calculado'},
 {label:'Faixa de payback (conservador a otimista)',value:anos(c.cen[0].payback)+' a '+anos(c.cen[2].payback),tag:'estimativa'}
];},

priorities:function(s,c){var L=[];var b=c.cen[1],cs=c.cen[0],pz=s.n('ind_prazo');var r=arr(s,'ce_riscos');
 if(b.resultado<=0) L.push({title:'Rever o projeto antes de investir: o cenário intermediário não fecha',why:'Resultado anual estimado de '+F.brl0(b.resultado)+'.',score:10});
 if(c.occBE!=null&&c.occBE>1) L.push({title:'Rever diária e custos por estadia',why:'Nem com 100% de ocupação a conta fecha.',score:9});
 else if(c.occBE!=null&&c.occBE>c.occ*0.8) L.push({title:'Aumentar a margem de segurança da ocupação',why:'Equilíbrio em '+F.pct(c.occBE*100,0)+', perto da premissa de '+F.pct(c.occ*100,0)+'.',score:8});
 if(cs.resultado<=0&&b.resultado>0) L.push({title:'Montar um plano para o cenário conservador',why:'No conservador o resultado anual é '+F.brl0(cs.resultado)+'.',score:8});
 if(b.payback!=null&&pz!=null&&b.payback>pz) L.push({title:'Reduzir o investimento ou implantar por etapas',why:'Payback de '+anos(b.payback)+' acima do prazo aceitável de '+F.num(pz)+' anos.',score:8});
 if(s.t('inv_origem')!=='cotacao') L.push({title:'Substituir estimativas por cotações formais',why:'O investimento total ainda depende de estimativas.',score:7});
 if(c.cont<0.1) L.push({title:'Aumentar a contingência do orçamento',why:'Contingência de '+F.pct(c.cont*100,0)+' para imprevistos.',score:6});
 if(c.infra===0&&s.t('infra_status')!=='existente') L.push({title:'Orçar a infraestrutura do terreno',why:'Nenhum valor informado para um terreno sem estrutura completa.',score:8});
 if(s.unknown('co_imposto')) L.push({title:'Confirmar o imposto com um contador',why:'O estudo usa 0% de imposto, o que deixa o resultado otimista.',score:7});
 if(s.unknown('co_estmedia')) L.push({title:'Estimar a estadia média com dados da região',why:'O custo por estadia usa 2 noites como hipótese.',score:4});
 if(r.indexOf('licencas')>=0) L.push({title:'Resolver licenças e documentação com profissional habilitado',why:'Pendência marcada como risco do projeto.',score:7});
 if(r.indexOf('reserva')>=0) L.push({title:'Separar uma reserva financeira além do investimento',why:'Protege contra atrasos e meses fracos.',score:6});
 if(r.indexOf('obra')>=0) L.push({title:'Fechar prazo e escopo da obra em contrato',why:'Prazo ou orçamento de obra ainda incertos.',score:5});
 if(s.n('rc_ocup',0)>70) L.push({title:'Validar a ocupação prevista com fontes da região',why:'Premissa de '+F.pct(s.n('rc_ocup'),0)+' é exigente para a média do ano.',score:6});
 if(s.t('mn_gestao')==='terceirizada'&&!s.n('co_gestao')) L.push({title:'Incluir a comissão da gestora nos custos',why:'Gestão terceirizada sem custo informado.',score:6});
 if(!/giro/.test(rowsOk(s,'inv').map(function(x){return (x.name||'').toLowerCase();}).join('|'))) L.push({title:'Incluir capital de giro no investimento',why:'Os primeiros meses costumam ter ocupação menor.',score:5});
 return L;},

report:function(s,c){
 var tg=function(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';};
 var orig=s.t('inv_origem')==='cotacao'?tg('informado','cotação'):s.t('inv_origem')==='misto'?tg('estimativa','cotação + estimativa'):tg('estimativa','estimativa sua');
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Modelo',(MODELOS[s.t('mn_modelo')]||'—')+' · '+F.num(c.U)+' unidade(s)',tg('informado')],
  ['Investimento nas unidades e itens',F.brl0(c.invItens),orig],
  ['Infraestrutura',F.brl0(c.infra),orig],
  ['Contingência',F.pct(c.cont*100,0)+' = '+F.brl0(c.invCont),tg('informado')],
  ['Diária média',F.brl(c.d),tg('estimativa','premissa sua')],
  ['Ocupação média anual',F.pct(c.occ*100,0),tg('estimativa','premissa sua')],
  ['Noites disponíveis por unidade no ano · meses de operação',F.num(c.noitesUnAno,1)+' · '+F.num(c.M),tg(c.N>0?'informado':'calculado')],
  ['Receitas extras por mês de operação',F.brl(c.ext),tg('estimativa','premissa sua')],
  ['Custos fixos mensais',F.brl(c.cfMes)+' (12 meses no ano)',tg('informado')],
  ['Custo por estadia · estadia média',F.brl(c.ce)+' · '+F.num(c.est,1)+' noites',s.unknown('co_estmedia')?tg('hipotese','estadia: hipótese'):tg('informado')],
  ['Deduções (comissão + imposto + gestão)',F.pct(c.ded*100),s.unknown('co_imposto')?tg('hipotese','imposto não informado = 0%'):tg('informado')],
  ['Variação dos cenários','± '+F.num(s.n('ce_var_ocup',0))+' p.p. de ocupação · ± '+F.pct(s.n('ce_var_diaria',0),0)+' na diária',tg('hipotese','premissa de cenário')]],[]);
 var invRows=rowsOk(s,'inv').map(function(r){return [esc(r.name),F.brl0(r.value),F.pct(c.invTotal>0?r.value/c.invTotal*100:0,1)];})
  .concat(rowsOk(s,'infra').map(function(r){return [esc(r.name)+' <span class="za-small">(infraestrutura)</span>',F.brl0(r.value),F.pct(c.invTotal>0?r.value/c.invTotal*100:0,1)];}))
  .concat([['Contingência ('+F.pct(c.cont*100,0)+')',F.brl0(c.invCont),F.pct(c.invTotal>0?c.invCont/c.invTotal*100:0,1)],['<b>Investimento total</b>','<b>'+F.brl0(c.invTotal)+'</b>','100%']]);
 var invT=ZA.table(['Item','Valor','% do total'],invRows,[1,2]);
 var L=function(lbl,f){return [lbl].concat(c.cen.map(f));};
 var cenT=ZA.table(['Indicador anual','Conservador','Intermediário','Otimista'],[
  L('Ocupação',function(x){return F.pct(x.occ*100,0);}),
  L('Diária média',function(x){return F.brl0(x.diaria);}),
  L('Noites vendidas',function(x){return F.num(x.noites,0);}),
  L('Receita de hospedagem',function(x){return F.brl0(x.recHosp);}),
  L('Receitas extras',function(x){return F.brl0(x.recExtra);}),
  L('Receita bruta',function(x){return F.brl0(x.recBruta);}),
  L('(−) Comissões, impostos e gestão',function(x){return F.brl0(x.ded);}),
  L('(−) Custos por estadia',function(x){return F.brl0(x.cVar);}),
  L('(−) Custos fixos',function(x){return F.brl0(x.cFix);}),
  L('<b>Resultado anual</b>',function(x){return '<b>'+F.brl0(x.resultado)+'</b>';}),
  L('Margem sobre a receita',function(x){return pctOr(x.margem,0);}),
  L('ROI anual',function(x){return pctOr(x.roi);}),
  L('Payback simples',function(x){return anos(x.payback);})],[1,2,3]);
 var riscos=arr(s,'ce_riscos');
 var dec='<div class="za-card"><p><b>Investimento total:</b> '+F.brl0(c.invTotal)+' · <b>Prazo aceitável informado:</b> '+F.num(s.n('ind_prazo'))+' anos'+(s.n('ind_ref')!=null?' · <b>Aplicação de referência:</b> '+F.pct(s.n('ind_ref'))+' ao ano':'')+'</p>'+
  '<p><b>Ocupação de equilíbrio:</b> '+(c.occBE==null||c.occBE>1?'inalcançável com a diária e os custos informados':F.pct(c.occBE*100))+' · <b>Diária de equilíbrio</b> na ocupação prevista: '+(c.dBE==null?'—':F.brl0(c.dBE))+'</p>'+
  '<p><b>Riscos marcados:</b> '+(riscos.length?riscos.map(function(v){return RISCOS.filter(function(x){return x.v===v;})[0].l;}).join('; '):'nenhum')+'.</p>'+
  '<p class="za-small">Perguntas para a sua decisão: o cenário conservador é sustentável para você? O payback cabe no seu prazo? Os valores vieram de cotações? O estudo não decide por você nem recomenda investir ou não investir.</p></div>';
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido de 30 dias (antes de qualquer desembolso)</b><ol><li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Pedir cotações formais do maior item do investimento')+'.</li><li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Validar diária e ocupação com fontes da região')+'.</li><li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Revisar impostos e custos com um contador')+'.</li><li><b>Semana 4:</b> refazer o Simulador com os números confirmados e comparar os três cenários com o seu prazo aceitável.</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Investimento total',html:invT},
  {title:'Cenários: Conservador, Intermediário e Otimista',html:cenT+'<p class="za-small">Resultado anual antes de depreciação, reposição de ativos e imposto de renda. Payback simples sem juros, inflação nem rampa de ocupação. Cenários ilustrativos, não previsões.</p>'},
  {title:'Indicadores para a decisão',html:dec}
 ],plan:plan};
}
});
})();
