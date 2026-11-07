/* ZAR-A08 · Quanto Você Deixa de Ganhar com Cada Hóspede? · Calculadora de Receitas Extras */
(function(){
var F=ZA.fmt, esc=ZA.esc;
var MOMENTOS=[{v:'chegada',l:'Chegada (kit de boas-vindas, translado, compras prontas)'},{v:'primeira_noite',l:'Primeira noite (jantar, vinho, fondue, lenha)'},{v:'cafe',l:'Café da manhã'},{v:'dia',l:'Durante o dia (passeios, piquenique, bicicleta, massagem)'},{v:'especial',l:'Ocasiões especiais (decoração, bolo, flores)'},{v:'saida',l:'Saída (late check-out, produtos locais para levar)'}];
var PEDIDOS=[{v:'lenha',l:'Lenha ou carvão extra'},{v:'cafe',l:'Café da manhã ou cesta'},{v:'decoracao',l:'Decoração para data especial'},{v:'late',l:'Sair mais tarde (late check-out)'},{v:'translado',l:'Translado ou indicação de transporte'},{v:'passeio',l:'Passeios e guias'},{v:'churrasco',l:'Kit churrasco ou refeição pronta'},{v:'vinho',l:'Vinho, espumante ou bebidas'}];
var CANAIS=[{v:'prechegada',l:'Mensagem pré-chegada com o cardápio'},{v:'qrcode',l:'QR code ou cardápio na unidade'},{v:'anuncio',l:'Menção no anúncio e nas fotos'},{v:'checkin',l:'Oferta verbal no check-in'},{v:'confirmacao',l:'Na confirmação da reserva'}];
var GRUPO={1:'Alimentos e bebidas',2:'Alimentos e bebidas',3:'Experiências',4:'Experiências'};
var MULT=[['Conservador',0.5],['Intermediário',1],['Otimista',1.5]];
function arr(s,id){return Array.isArray(s.v[id])?s.v[id]:[];}
function itemFields(k,req,ex){return [
 {id:'i'+k+'_nome',label:'Item '+k+': nome',type:'text',required:req,placeholder:ex[0]},
 {id:'i'+k+'_custo',label:'Item '+k+': custo por venda (insumos, fornecedor, mão de obra)',type:'money',required:req,help:'Quanto você gasta cada vez que vende uma unidade do item.'},
 {id:'i'+k+'_preco',label:'Item '+k+': preço de venda',type:'money',required:req},
 {id:'i'+k+'_adesao',label:'Item '+k+': de cada 100 reservas, quantas comprariam?',type:'percent',required:req,allowUnknown:req,help:'Sua estimativa. Se não souber, o cálculo usa 10% como hipótese a validar.'}
];}
function itemFb(s,c,ks){var o=[];
 ks.forEach(function(k){var it=c.items[k-1]; if(!it.ativo) return;
  if(it.margemUnit<=0) o.push({lv:'bad',t:'<b>'+esc(it.nome)+'</b> dá prejuízo: depois de taxa e perdas, cada venda deixa '+F.brl(it.margemUnit)+'. Reveja preço ou custo.'});
  else if(it.margemPct<0.3) o.push({lv:'warn',t:'<b>'+esc(it.nome)+'</b> deixa '+F.brl(it.margemUnit)+' por venda ('+F.pct(it.margemPct*100,0)+' do preço). Margem apertada para o trabalho envolvido.'});
  else o.push({lv:'ok',t:'<b>'+esc(it.nome)+'</b> deixa '+F.brl(it.margemUnit)+' por venda ('+F.pct(it.margemPct*100,0)+' do preço), com cerca de '+F.num(it.vendas,1)+' vendas por mês.'});
  if(it.adesHip) o.push({lv:'warn',t:'Adesão de '+esc(it.nome)+' desconhecida: usamos 10% como hipótese. Teste a oferta com os próximos hóspedes e anote quantos compram.'});
 });
 return o;}

ZA.register({
id:'A08', code:'ZAR-A08', collection:'Hospedagem',
title:'Quanto Você Deixa de Ganhar com Cada Hóspede?',
subtitle:'Aprenda a Criar Receitas Além da Diária',
tool:'Calculadora de Receitas Extras',
deliverable:'Cardápio de Adicionais com Precificação',
nameField:'nome', propertyField:'propriedade',
disclaimer:'A receita extra é uma estimativa construída com os custos, preços e taxas de adesão que você informou (ou com hipóteses indicadas). Os três cenários são ilustrativos e não são previsões: não há garantia de vendas, faturamento ou lucro. Venda de alimentos e bebidas e oferta de passeios podem exigir regras sanitárias, licenças ou parceiros habilitados; confirme com a prefeitura e um contador.',

intro:[
 {kind:'mirror', title:'Seu hóspede poderia comprar mais, mas você não oferece nada?',
  lead:'Ele chega, pergunta se tem lenha, se dá para tomar café na cabana, se você conhece alguém que faz passeio. Você improvisa, indica um conhecido ou diz que não tem.',
  body:'<div class="za-card"><p>Veja se você se reconhece:</p><ul><li>“O hóspede pediu e eu dei de graça, sem saber quanto custava.”</li><li>“Já pensei em vender café da manhã, mas não sei que preço cobrar.”</li><li>“Indico o passeio de um vizinho e não ganho nada com isso.”</li><li>“Para faturar mais, só penso em conseguir mais reservas.”</li></ul></div>'},
 {kind:'collapse', title:'Talvez aumentar o faturamento não dependa só de conseguir mais reservas.',
  lead:'O hóspede que já reservou confia em você e está no clima da viagem. Oferecer algo que melhore a estadia dele é serviço, não incômodo.',
  body:'<div class="za-card"><p>Receita extra bem feita tem três condições:</p><ol><li><b>Faz sentido para o hóspede</b> (resolve um desejo real da viagem).</li><li><b>Deixa margem</b> depois de custo, perdas e taxas.</li><li><b>É oferecida no momento certo</b>, de forma simples.</li></ol><p>Neste percurso você vai escolher até 4 adicionais, calcular custo, preço e margem de cada um e estimar a receita extra mensal em três cenários.</p></div>'},
 {kind:'start', title:'Vamos montar o seu cardápio de adicionais',
  lead:'Em 7 pilares, você vai mapear a jornada de consumo do hóspede, escolher alimentos, bebidas e experiências, precificar e montar a apresentação do cardápio.',
  body:'<p>Tenha à mão, se possível: o número de reservas por mês e o custo dos itens que você pensa em oferecer (cotação do fornecedor, preço no mercado). Se não tiver um dado, marque “não sei”.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Ana'},
   {id:'propriedade',label:'Nome da hospedagem',type:'text',required:true,placeholder:'Ex.: Refúgio das Hortênsias'},
   {id:'tipo',label:'Tipo de hospedagem',type:'select',required:true,options:[{v:'airbnb',l:'Apartamento ou casa (Airbnb/temporada)'},{v:'cabana',l:'Cabana ou chalé'},{v:'glamping',l:'Glamping'},{v:'pousada',l:'Pequena pousada'},{v:'outro',l:'Outro'}]},
   {id:'destino',label:'Cidade / destino',type:'text',required:true,placeholder:'Ex.: Gonçalves (MG)'},
   {id:'unidades',label:'Quantas unidades você aluga?',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)'}
  ]}
],

pillars:[
/* 1 */
{title:'Jornada de consumo', screens:[
 {kind:'learn', title:'O hóspede consome em momentos, não em listas',
  body:'<p>Um cardápio de adicionais funciona quando cada item aparece <b>no momento em que o hóspede sente a necessidade</b>: a cesta de café para a primeira manhã, o vinho para a primeira noite, a decoração para a data especial, o late check-out no último dia.</p><p>Para estimar a receita, a conta parte de três números: <b>reservas por mês</b>, <b>quantas dessas reservas compram cada item</b> (adesão) e <b>quanto cada venda deixa</b> depois dos custos. Neste pilar você informa a base: reservas, tamanho do grupo e os momentos da estadia que fazem sentido no seu caso.</p>',
  example:'Exemplo ilustrativo: 20 reservas por mês; se 30% compram uma cesta de café, são 6 vendas no mês. Se cada venda deixa R$ 45, são R$ 270 por mês com um único item.'},
 {kind:'compare', title:'Vender por acaso × vender pela jornada',
  cols:[{h:'Por acaso',type:'bad',items:['Só vende se o hóspede perguntar','Lista de itens sem relação com a viagem','Oferece tudo no check-in, de uma vez','Sem registro de quem comprou']},
        {h:'Pela jornada',type:'good',items:['Cada item ligado a um momento da estadia','Oferta antes da chegada, quando o hóspede planeja','Lembrete no momento de uso','Mede a adesão de cada item']}]},
 {kind:'form', title:'A base da sua receita extra', intro:'Use a média dos últimos meses.',
  fields:[
   {id:'jc_reservas',label:'Reservas por mês (todas as unidades)',type:'number',required:true,min:1,max:10000,step:1,unit:'reservas'},
   {id:'jc_pessoas',label:'Hóspedes por reserva, em média',type:'number',required:true,min:1,max:30,step:0.1,unit:'pessoas'},
   {id:'jc_estadia',label:'Estadia média',type:'number',required:true,min:1,max:60,step:0.1,unit:'noites',allowUnknown:true},
   {id:'jc_diaria',label:'Diária média',type:'money',required:true,min:1,allowUnknown:true,help:'Serve para comparar a receita extra com o valor da hospedagem.'},
   {id:'jc_momentos',label:'Em quais momentos faz sentido oferecer algo?',type:'checks',options:MOMENTOS},
   {id:'jc_hoje',label:'O que você oferece hoje?',type:'radio',required:true,options:[{v:'nada',l:'Nada além da hospedagem'},{v:'informal',l:'Algumas coisas, de forma informal'},{v:'cardapio',l:'Tenho um cardápio de adicionais'}]}
  ]},
 {kind:'feedback', title:'O tamanho da sua oportunidade',
  metrics:function(s,c){return [{label:'Reservas/mês',value:F.num(c.res),tag:'informado'},{label:'Hóspedes/mês',value:F.num(c.hospMes,0),tag:'calculado'},{label:'Valor médio da hospedagem por reserva',value:c.ticket==null?'—':F.brl(c.ticket),tag:'calculado'}];},
  feedback:function(s,c){var o=[];var m=arr(s,'jc_momentos');
   o.push({lv:'info',t:'São cerca de <b>'+F.num(c.hospMes,0)+' hóspedes por mês</b> ('+F.num(c.res)+' reservas). Cada 10% de adesão a um item representa '+F.num(c.res*0.1,1)+' vendas por mês.'});
   if(!m.length) o.push({lv:'warn',t:'Nenhum momento marcado. Revise a jornada: chegada, primeira noite e café da manhã costumam ser os mais naturais.'});
   else o.push({lv:'ok',t:m.length+' momento(s) de consumo identificados. Nos próximos pilares você escolhe o item de cada momento.'});
   if(s.t('jc_hoje')==='nada') o.push({lv:'info',t:'Você parte do zero: comece com 2 ou 3 itens simples e meça a adesão antes de ampliar.'});
   if(s.t('jc_hoje')==='informal') o.push({lv:'warn',t:'Ofertas informais costumam ter preço sem cálculo e custo esquecido. Vamos colocar cada item na ponta do lápis.'});
   if(s.unknown('jc_diaria')||s.unknown('jc_estadia')) o.push({lv:'info',t:'Sem diária ou estadia média, não comparamos a receita extra com o valor da hospedagem. O restante do cálculo segue normalmente.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Listar o que os hóspedes já pediram nas últimas estadias'},{id:'a1_2',text:'Escolher os 2 ou 3 momentos da estadia com mais potencial'},{id:'a1_3',text:'Começar a anotar o que cada reserva compra'}]}
]},
/* 2 */
{title:'Identificação de oportunidades', screens:[
 {kind:'learn', title:'O melhor adicional é aquele que o hóspede já pede',
  body:'<p>Antes de inventar produtos, olhe para três fontes: <b>o que os hóspedes já pedem</b>, <b>o perfil de quem vem</b> (casais, famílias, grupos) e <b>o que a região oferece</b> (produtores, guias, restaurantes que entregam).</p><p>Itens que dependem de parceiros locais têm duas vantagens: você não precisa estocar e ajuda a economia do destino. Nesse caso, sua receita pode vir de uma comissão combinada ou de um preço de revenda. Combine por escrito e com transparência.</p>',
  example:'Exemplo ilustrativo: num destino de serra, com público de casais, os pedidos mais comuns são lenha, vinho e decoração para aniversário. São três itens de baixo estoque e preparo simples.'},
 {kind:'compare', title:'Ideia de catálogo × oportunidade real',
  cols:[{h:'Ideia de catálogo',type:'bad',items:['Copiar o cardápio de um hotel grande','Itens que exigem cozinha profissional','Estoque grande de produtos perecíveis','Produto sem ligação com o destino']},
        {h:'Oportunidade real',type:'good',items:['Responde a um pedido frequente','Preparo simples ou feito por parceiro','Pedido antecipado, compra sob demanda','Valoriza produtores e serviços locais']}]},
 {kind:'form', title:'Onde estão as suas oportunidades',
  fields:[
   {id:'op_perfil',label:'Perfil principal dos hóspedes',type:'select',required:true,options:[{v:'casais',l:'Casais'},{v:'familias',l:'Famílias com crianças'},{v:'amigos',l:'Grupos de amigos'},{v:'trabalho',l:'Viagem a trabalho'},{v:'pets',l:'Pessoas com pet'}]},
   {id:'op_pedidos',label:'O que os hóspedes já pediram ou perguntaram?',type:'checks',options:PEDIDOS},
   {id:'op_fornecedores',label:'Você tem fornecedores ou parceiros locais?',type:'radio',required:true,options:[{v:'tenho',l:'Sim, já tenho com quem contar'},{v:'alguns',l:'Conheço alguns, mas sem nada combinado'},{v:'nao',l:'Ainda não'}]}
  ]},
 {kind:'feedback', title:'Suas pistas de oportunidade',
  metrics:function(s,c){return [{label:'Pedidos já recebidos',value:String(arr(s,'op_pedidos').length),tag:'informado'}];},
  feedback:function(s,c){var o=[];var p=arr(s,'op_pedidos'),pf=s.t('op_perfil');
   if(p.length) o.push({lv:'ok',t:'Os hóspedes já pediram: '+p.map(function(v){return PEDIDOS.filter(function(x){return x.v===v;})[0].l.toLowerCase();}).join('; ')+'. Esses são os primeiros candidatos ao seu cardápio.'});
   else o.push({lv:'info',t:'Nenhum pedido registrado. Pergunte aos próximos hóspedes, na mensagem pós-estadia, o que teria deixado a viagem melhor.'});
   var sug={casais:'decoração para datas especiais, vinho ou espumante, café da manhã na cabana',familias:'kit lanche, refeição pronta, passeio adequado a crianças',amigos:'kit churrasco, bebidas, passeios em grupo',trabalho:'café da manhã, refeição pronta, late check-out',pets:'kit pet (cama, potes, petiscos), passeio pet friendly'}[pf];
   if(sug) o.push({lv:'info',t:'Para o perfil escolhido, itens que costumam fazer sentido: '+sug+'. São sugestões para avaliar, não regras.'});
   if(s.t('op_fornecedores')==='nao') o.push({lv:'warn',t:'Sem parceiros locais, prefira itens que você mesmo prepara com pouco estoque.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Conversar com 2 fornecedores ou parceiros locais esta semana'},{id:'a2_2',text:'Incluir a pergunta “o que teria deixado sua viagem melhor?” na mensagem pós-estadia'},{id:'a2_3',text:'Combinar por escrito condições e comissões com os parceiros'}]}
]},
/* 3 */
{title:'Alimentos e bebidas', screens:[
 {kind:'learn', title:'Alimentos e bebidas: alta adesão, atenção ao desperdício',
  body:'<p>Café da manhã, cestas, kits de queijos e vinhos, refeições prontas: são os adicionais com mais adesão porque resolvem uma necessidade real da viagem. Também são os que mais escondem custos: <b>insumos que estragam</b>, embalagem, tempo de preparo e entrega.</p><p>Para cada item, informe o <b>custo por venda</b> (tudo o que sai do seu bolso para entregar uma unidade), o <b>preço</b> e a sua estimativa de <b>adesão</b>: de cada 100 reservas, quantas comprariam. As perdas e taxas entram no Pilar 5.</p>',
  example:'Exemplo ilustrativo: cesta de café para 2 pessoas com pães, frutas, frios e suco. Insumos R$ 30 + embalagem R$ 5 = R$ 35 de custo. Vendida a R$ 90, com 30 de cada 100 reservas comprando.'},
 {kind:'compare', title:'Item que dá trabalho × item que dá resultado',
  cols:[{h:'Dá trabalho',type:'bad',items:['Preparado na hora, sem pedido prévio','Muitos ingredientes perecíveis','Preço definido “de cabeça”','Entrega que exige sua presença']},
        {h:'Dá resultado',type:'good',items:['Pedido até a véspera','Poucos insumos, de boa durabilidade','Preço calculado sobre o custo real','Deixado na unidade ou entregue por parceiro']}]},
 {kind:'form', title:'Seus itens de alimentos e bebidas', intro:'O item 1 é obrigatório; o item 2 é opcional (deixe em branco se não houver).',
  fields:itemFields(1,true,['Ex.: Cesta de café da manhã para 2']).concat(itemFields(2,false,['Ex.: Vinho e tábua de queijos']))},
 {kind:'feedback', title:'Margem dos seus alimentos e bebidas',
  metrics:function(s,c){var a=c.items[0],b=c.items[1];var m=[{label:a.ativo?a.nome:'Item 1',value:a.ativo?F.brl(a.margemUnit)+' por venda':'—',tag:'calculado'}];if(b.ativo)m.push({label:b.nome,value:F.brl(b.margemUnit)+' por venda',tag:'calculado'});return m;},
  intro:'Cálculo já com as taxas e perdas, se você já preencheu o Pilar 5; caso contrário, por enquanto sem elas.',
  feedback:function(s,c){return itemFb(s,c,[1,2]);}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Cotar os insumos dos itens escolhidos com 2 fornecedores'},{id:'a3_2',text:'Definir prazo de pedido (ex.: até a véspera) para não desperdiçar'},{id:'a3_3',text:'Verificar com a prefeitura as exigências para venda de alimentos'}]}
]},
/* 4 */
{title:'Experiências', screens:[
 {kind:'learn', title:'Experiências vendem lembrança, não objeto',
  body:'<p>Passeios, decoração para datas especiais, aula de culinária, massagem, piquenique montado: experiências têm adesão menor que alimentos, mas costumam ter <b>preço e margem maiores</b> e marcam a estadia.</p><p>Muitas experiências são feitas por parceiros. Nesse caso, o custo por venda é o que você repassa ao parceiro; se você só indica e recebe comissão, o custo é zero e o preço é a comissão. O importante é que o hóspede saiba quem presta o serviço e que o parceiro tenha as autorizações necessárias.</p>',
  example:'Exemplo ilustrativo: decoração romântica com pétalas, balões e bilhete. Materiais R$ 45 + 30 minutos de montagem (R$ 15) = R$ 60 de custo. Vendida a R$ 180 para cerca de 10 de cada 100 reservas.'},
 {kind:'compare', title:'Indicar de graça × oferecer com estrutura',
  cols:[{h:'Indicar de graça',type:'bad',items:['Passa o telefone do guia','Não sabe se o hóspede foi bem atendido','Não recebe nada pela indicação','Sem regra para cancelamento']},
        {h:'Oferecer com estrutura',type:'good',items:['Experiência no cardápio, com preço','Parceiro escolhido e avaliado','Comissão ou margem combinada','Regras claras de agendamento e cancelamento']}]},
 {kind:'form', title:'Suas experiências', intro:'O item 3 é obrigatório; o item 4 é opcional.',
  fields:itemFields(3,true,['Ex.: Decoração para data especial']).concat(itemFields(4,false,['Ex.: Passeio guiado à cachoeira']))},
 {kind:'feedback', title:'Margem das suas experiências',
  metrics:function(s,c){var a=c.items[2],b=c.items[3];var m=[{label:a.ativo?a.nome:'Item 3',value:a.ativo?F.brl(a.margemUnit)+' por venda':'—',tag:'calculado'}];if(b.ativo)m.push({label:b.nome,value:F.brl(b.margemUnit)+' por venda',tag:'calculado'});return m;},
  feedback:function(s,c){var o=itemFb(s,c,[3,4]);
   var ab=c.items.filter(function(x){return x.ativo&&x.k<=2;}),ex=c.items.filter(function(x){return x.ativo&&x.k>=3;});
   if(ab.length&&ex.length){var ma=ab.reduce(function(t,x){return t+x.margemUnit;},0)/ab.length,me=ex.reduce(function(t,x){return t+x.margemUnit;},0)/ex.length;
    o.push({lv:'info',t:'Em média, cada venda de experiência deixa '+F.brl(me)+' e cada venda de alimentos e bebidas deixa '+F.brl(ma)+'. Combine itens de alta adesão com itens de margem alta.'});}
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Montar um protótipo da experiência e fotografar para o cardápio'},{id:'a4_2',text:'Definir regras de agendamento e cancelamento com os parceiros'},{id:'a4_3',text:'Confirmar se os parceiros têm as autorizações necessárias'}]}
]},
/* 5 */
{title:'Custos', screens:[
 {kind:'learn', title:'O custo que não aparece na nota do mercado',
  body:'<p>Além do custo por venda, três custos costumam ser esquecidos:</p><ul><li><b>Perdas</b>: insumo que estragou, item que voltou, quebra. Entram como um percentual sobre o custo.</li><li><b>Taxas</b>: cartão, maquininha ou comissão da plataforma quando o adicional é cobrado por ela. Entram como percentual sobre o preço.</li><li><b>Custo fixo do programa</b>: estoque mínimo, embalagens, cardápio impresso, geladeira extra. Entra como valor mensal, vendendo ou não.</li></ul><p>A conta por item fica: <b>Margem por venda = Preço × (1 − taxa) − Custo × (1 + perdas)</b>.</p>',
  example:'Exemplo ilustrativo: preço R$ 90, taxa de 5%, custo R$ 35 e perdas de 10%. Margem = 90 × 0,95 − 35 × 1,10 = 85,50 − 38,50 = <b>R$ 47 por venda</b>.'},
 {kind:'compare', title:'Conta otimista × conta completa',
  cols:[{h:'Conta otimista',type:'bad',items:['Preço menos insumo, e só','Ignora o que estraga','Esquece a taxa do cartão','Não conta embalagem nem cardápio']},
        {h:'Conta completa',type:'good',items:['Custo com percentual de perdas','Taxa descontada do preço','Custo fixo mensal do programa','Resultado só depois de tudo isso']}]},
 {kind:'form', title:'Seus custos adicionais',
  fields:[
   {id:'cu_taxa',label:'Taxa média sobre o preço dos adicionais (cartão, maquininha, plataforma)',type:'percent',required:true,max:30},
   {id:'cu_perda',label:'Perdas e desperdício (percentual sobre o custo dos itens)',type:'percent',required:true,max:50,help:'Se não souber, uma estimativa prudente é melhor que zero. Revise depois de 2 meses.'},
   {id:'cu_fixo',label:'Custo fixo mensal do programa de adicionais',type:'money',required:true,help:'Estoque mínimo, embalagens, impressão do cardápio etc. Coloque 0 se não houver.'}
  ]},
 {kind:'feedback', title:'Resultado depois de todos os custos',
  metrics:function(s,c){return [{label:'Contribuição mensal dos itens',value:F.brl(c.contribMes),tag:'calculado'},{label:'Custo fixo do programa',value:F.brl(c.fixo),tag:'informado'},{label:'Resultado extra/mês',value:F.brl(c.resultadoMes),tag:'estimativa'}];},
  feedback:function(s,c){var o=[];
   if(c.resultadoMes<=0) o.push({lv:'bad',t:'Com as premissas atuais, o programa de adicionais não cobre o próprio custo fixo ('+F.brl(c.resultadoMes)+' por mês). Reduza o custo fixo, ajuste preços ou foque nos itens de maior margem.'});
   else o.push({lv:'ok',t:'Depois de taxas, perdas e custo fixo, a estimativa é de <b>'+F.brl(c.resultadoMes)+'</b> por mês no cenário intermediário.'});
   if(c.fixo>0&&c.contribMes>0&&c.fixo/c.contribMes>0.4) o.push({lv:'warn',t:'O custo fixo consome '+F.pct(c.fixo/c.contribMes*100,0)+' da contribuição dos itens. Comece com menos estoque e amplie conforme as vendas.'});
   if(s.n('cu_perda',0)===0) o.push({lv:'info',t:'Perdas de 0%: confirme se nenhum insumo estraga ou sobra. Com itens perecíveis, raramente é zero.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Registrar perdas e sobras dos primeiros 2 meses'},{id:'a5_2',text:'Começar com estoque mínimo e compra sob encomenda'},{id:'a5_3',text:'Separar a receita e os custos dos adicionais nas contas'}]}
]},
/* 6 */
{title:'Precificação', screens:[
 {kind:'learn', title:'Preço do adicional: custo, margem e percepção',
  body:'<p>O preço mínimo de um adicional cobre o custo com perdas e as taxas. O <b>preço sugerido</b> acrescenta a margem que você deseja, calculada sobre o preço (e não somando um percentual ao custo):</p><div class="za-card"><b>Preço sugerido = Custo × (1 + perdas) ÷ (1 − taxa − margem desejada)</b></div><p>Depois, confira a <b>percepção</b>: o preço faz sentido para o hóspede, comparado ao que ele pagaria na cidade? Se o preço sugerido ficar alto demais, reduza o custo ou troque o item.</p>',
  example:'Exemplo ilustrativo: custo R$ 70, perdas 10%, taxa 5% e margem desejada 50%. Preço sugerido = 77 ÷ 0,45 = <b>R$ 171,11</b>. Vender a R$ 150 deixa uma margem menor que a desejada.'},
 {kind:'compare', title:'Formas de cobrar',
  cols:[{h:'Antecipado (na reserva ou pré-chegada)',items:['Garante a compra e evita desperdício','Permite comprar sob encomenda','Exige oferta clara e antecedência']},
        {h:'Na estadia ou no check-out',items:['Permite venda por impulso','Risco de calote ou discussão no final','Exige controle do que foi consumido']}]},
 {kind:'form', title:'Sua regra de preço',
  fields:[
   {id:'pr_margem',label:'Margem desejada sobre o preço de cada adicional',type:'percent',required:true,max:80,help:'Referência orientativa: escolha uma margem que remunere seu trabalho e o risco do item.'},
   {id:'pr_cobranca',label:'Como você vai cobrar os adicionais?',type:'radio',required:true,options:[{v:'antecipado',l:'Antecipado, na reserva ou antes da chegada'},{v:'checkin',l:'No check-in'},{v:'checkout',l:'No check-out, pelo consumo'}]}
  ]},
 {kind:'feedback', title:'Preço atual × preço sugerido',
  metrics:function(s,c){var ab=c.items.filter(function(x){return x.ativo;});return [{label:'Itens no cardápio',value:String(ab.length),tag:'informado'},{label:'Itens abaixo do preço sugerido',value:String(c.abaixoSug),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.denom<=0){o.push({lv:'bad',t:'Taxa + margem desejada somam 100% ou mais: não existe preço que atenda. Reduza a margem desejada.'});return o;}
   c.items.forEach(function(it){if(!it.ativo)return;
    if(it.preco<it.precoSug) o.push({lv:'warn',t:'<b>'+esc(it.nome)+'</b>: preço atual '+F.brl(it.preco)+', sugerido '+F.brl(it.precoSug)+' para atingir '+F.pct(c.m*100,0)+' de margem.'});
    else o.push({lv:'ok',t:'<b>'+esc(it.nome)+'</b>: preço atual '+F.brl(it.preco)+' já atinge a margem desejada (sugerido: '+F.brl(it.precoSug)+').'});});
   if(s.t('pr_cobranca')==='checkout') o.push({lv:'info',t:'Cobrar no check-out exige registro do consumo e combinado claro antes. Para itens perecíveis, o pedido antecipado reduz perdas.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Ajustar os itens que estão abaixo do preço sugerido'},{id:'a6_2',text:'Comparar os preços com o que o hóspede pagaria na cidade'},{id:'a6_3',text:'Definir a forma de cobrança e informá-la no cardápio'}]}
]},
/* 7 */
{title:'Cardápio e apresentação', screens:[
 {kind:'learn', title:'Ninguém compra o que não sabe que existe',
  body:'<p>O cardápio de adicionais precisa ser <b>curto</b> (de 3 a 6 itens), <b>com foto</b>, <b>preço claro</b> e <b>prazo de pedido</b>. A melhor hora de oferecer é quando o hóspede está planejando a viagem: na confirmação da reserva e na mensagem pré-chegada. Na unidade, um QR code ou um cartão lembra a oferta no momento de uso.</p><p>Escolha um <b>item de destaque</b>, aquele que combina melhor com o perfil do hóspede, e apresente-o primeiro.</p>',
  example:'Exemplo ilustrativo de texto: “Para deixar sua estadia ainda mais especial: Cesta de café da manhã na cabana · R$ 90 (pedido até as 18h da véspera).” Uma linha por item, com foto.'},
 {kind:'compare', title:'Cardápio que confunde × cardápio que vende',
  cols:[{h:'Confunde',type:'bad',items:['Lista longa, sem foto','“Consulte valores”','Oferecido só no check-in','Sem prazo nem forma de pedido']},
        {h:'Vende',type:'good',items:['3 a 6 itens com foto','Preço e o que está incluído','Enviado antes da chegada e lembrado na unidade','Prazo e forma de pedido claros']}]},
 {kind:'form', title:'Como você vai apresentar o cardápio',
  fields:[
   {id:'ap_canais',label:'Onde o cardápio vai aparecer?',type:'checks',options:CANAIS},
   {id:'ap_antecedencia',label:'Prazo para pedidos antes do uso',type:'number',required:true,min:0,max:168,step:1,unit:'horas'},
   {id:'ap_destaque',label:'Qual item será o destaque?',type:'select',required:true,options:[{v:'1',l:'Item 1 (alimentos e bebidas)'},{v:'2',l:'Item 2 (alimentos e bebidas)'},{v:'3',l:'Item 3 (experiência)'},{v:'4',l:'Item 4 (experiência)'}]}
  ]},
 {kind:'feedback', title:'Seu cardápio em três cenários',
  metrics:function(s,c){return c.cen.map(function(x){return {label:x.nome+' · resultado/mês',value:F.brl(x.resultado),tag:'estimativa'};});},
  feedback:function(s,c){var o=[];var ch=arr(s,'ap_canais');
   if(ch.indexOf('prechegada')<0&&ch.indexOf('confirmacao')<0) o.push({lv:'warn',t:'O cardápio não aparece antes da chegada. É quando o hóspede planeja e decide: inclua-o na confirmação ou na mensagem pré-chegada.'});
   if(ch.length>=3) o.push({lv:'ok',t:'O cardápio aparece em '+ch.length+' pontos da jornada.'});
   var d=c.items[Number(s.t('ap_destaque'))-1];
   if(d&&!d.ativo) o.push({lv:'warn',t:'O item escolhido como destaque não foi preenchido. Escolha um item do seu cardápio.'});
   else if(d) o.push({lv:'info',t:'Destaque: <b>'+esc(d.nome)+'</b>, que deixa '+F.brl(d.margemUnit)+' por venda.'});
   o.push({lv:'info',t:'No cenário intermediário, a receita extra estimada é de '+F.brl(c.receitaMes)+' por mês, ou '+F.brl(c.extraPorReserva)+' por reserva'+(c.pctTicket!=null?' ('+F.pct(c.pctTicket*100)+' do valor médio da hospedagem)':'')+'.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Montar o cardápio com fotos, preços e prazo de pedido'},{id:'a7_2',text:'Incluir o cardápio na confirmação da reserva e na mensagem pré-chegada'},{id:'a7_3',text:'Medir a adesão real de cada item depois de 30 dias'}]}
]}
],

compute:function(s){
 var c={};
 c.res=s.n('jc_reservas',0); c.pessoas=s.n('jc_pessoas',1); c.hospMes=c.res*c.pessoas;
 c.est=s.n('jc_estadia'); c.diaria=s.n('jc_diaria');
 c.ticket=(c.est!=null&&c.diaria!=null)?c.est*c.diaria:null;
 c.taxa=s.n('cu_taxa',0)/100; c.perda=s.n('cu_perda',0)/100; c.fixo=s.n('cu_fixo',0)||0;
 c.m=s.n('pr_margem',0)/100; c.denom=1-c.taxa-c.m;
 c.items=[1,2,3,4].map(function(k){
  var nome=String(s.t('i'+k+'_nome')).trim(), preco=s.n('i'+k+'_preco',0), custo=s.n('i'+k+'_custo',0);
  var adesHip=s.n('i'+k+'_adesao')==null; var ades=adesHip?10:s.n('i'+k+'_adesao');
  var ativo=!!nome&&preco>0;
  var custoEf=custo*(1+c.perda), mu=preco*(1-c.taxa)-custoEf, vendas=c.res*ades/100;
  return {k:k,grupo:GRUPO[k],nome:nome||('Item '+k),ativo:ativo,custo:custo,preco:preco,ades:ades,adesHip:ativo&&adesHip,custoEf:custoEf,margemUnit:mu,margemPct:preco>0?mu/preco:0,vendas:ativo?vendas:0,receita:ativo?vendas*preco:0,contrib:ativo?vendas*mu:0,precoSug:c.denom>0?custoEf/c.denom:null};
 });
 var at=c.items.filter(function(x){return x.ativo;});
 c.receitaMes=0; c.contribMes=0; at.forEach(function(x){c.receitaMes+=x.receita;c.contribMes+=x.contrib;});
 c.resultadoMes=c.contribMes-c.fixo; c.resultadoAno=c.resultadoMes*12;
 c.extraPorReserva=c.res>0?c.receitaMes/c.res:0;
 c.pctTicket=c.ticket?c.extraPorReserva/c.ticket:null;
 c.abaixoSug=at.filter(function(x){return x.precoSug!=null&&x.preco<x.precoSug;}).length;
 c.negativos=at.filter(function(x){return x.margemUnit<=0;}).length;
 c.adesHip=at.filter(function(x){return x.adesHip;}).length;
 var best=at.slice().sort(function(a,b){return b.contrib-a.contrib;}); c.melhor=best[0]||null;
 c.cen=MULT.map(function(x){var rec=0,con=0;at.forEach(function(it){var a=Math.min(100,it.ades*x[1]);var v=c.res*a/100;rec+=v*it.preco;con+=v*it.margemUnit;});
  return {nome:x[0],mult:x[1],receita:rec,contrib:con,resultado:con-c.fixo,anual:(con-c.fixo)*12};});
 return c;
},

metrics:function(s,c){return [
 {label:'Receita extra/mês (intermediário)',value:F.brl(c.receitaMes),tag:'estimativa'},
 {label:'Resultado extra/mês (intermediário)',value:F.brl(c.resultadoMes),tag:'estimativa'},
 {label:'Resultado extra/ano (intermediário)',value:F.brl(c.resultadoAno),tag:'estimativa'},
 {label:'Receita extra por reserva',value:F.brl(c.extraPorReserva),tag:'estimativa'},
 {label:'Extra sobre o valor da hospedagem',value:c.pctTicket==null?'—':F.pct(c.pctTicket*100),tag:'calculado'},
 {label:'Item que mais contribui',value:c.melhor?c.melhor.nome:'—',tag:'calculado'},
 {label:'Faixa de resultado/mês (conservador a otimista)',value:F.brl0(c.cen[0].resultado)+' a '+F.brl0(c.cen[2].resultado),tag:'estimativa'},
 {label:'Custo fixo do programa',value:F.brl(c.fixo),tag:'informado'}
];},

priorities:function(s,c){var L=[];
 c.items.forEach(function(it){if(!it.ativo)return;
  if(it.margemUnit<=0) L.push({title:'Corrigir o preço ou o custo de '+it.nome,why:'Cada venda hoje deixa '+F.brl(it.margemUnit)+'.',score:10});
  else if(it.precoSug!=null&&it.preco<it.precoSug) L.push({title:'Ajustar '+it.nome+' para perto de '+F.brl(it.precoSug),why:'Preço atual abaixo da margem desejada.',score:6});
 });
 if(c.resultadoMes<=0) L.push({title:'Reduzir o custo fixo do programa de adicionais',why:'O resultado mensal estimado não cobre o custo fixo.',score:9});
 if(c.denom<=0) L.push({title:'Rever a margem desejada',why:'Taxa + margem ≥ 100% tornam impossível o preço sugerido.',score:8});
 var ch=arr(s,'ap_canais');
 if(ch.indexOf('prechegada')<0&&ch.indexOf('confirmacao')<0) L.push({title:'Enviar o cardápio na confirmação e na mensagem pré-chegada',why:'Hoje o hóspede só descobre os adicionais na unidade (ou não descobre).',score:8});
 if(s.t('jc_hoje')==='nada') L.push({title:'Lançar um cardápio piloto com '+Math.max(2,c.items.filter(function(x){return x.ativo;}).length)+' itens',why:'Hoje não há receita além da diária.',score:8});
 if(c.melhor) L.push({title:'Dar destaque a '+c.melhor.nome,why:'É o item que mais contribui no cenário intermediário ('+F.brl(c.melhor.contrib)+'/mês).',score:7});
 if(c.adesHip) L.push({title:'Medir a adesão real dos itens estimados por hipótese',why:c.adesHip+' item(ns) usam 10% como hipótese.',score:6});
 if(c.fixo>0&&c.contribMes>0&&c.fixo/c.contribMes>0.4) L.push({title:'Começar com estoque mínimo e compra sob encomenda',why:'O custo fixo consome '+F.pct(c.fixo/c.contribMes*100,0)+' da contribuição.',score:6});
 if(s.t('op_fornecedores')!=='tenho') L.push({title:'Fechar parceria com fornecedores locais',why:'Reduz estoque e amplia as experiências possíveis.',score:4});
 if(s.t('pr_cobranca')==='checkout') L.push({title:'Passar a cobrar itens perecíveis antecipadamente',why:'Reduz perdas e discussões no check-out.',score:4});
 if(s.n('cu_perda',0)===0) L.push({title:'Registrar perdas e sobras por 2 meses',why:'Perdas informadas como zero.',score:3});
 if(c.items.filter(function(x){return x.ativo;}).length<3) L.push({title:'Completar o cardápio com mais um item de outro momento da estadia',why:'Poucos itens limitam a receita por reserva.',score:3});
 return L;},

report:function(s,c){
 var tg=function(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';};
 var at=c.items.filter(function(x){return x.ativo;});
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Reservas por mês',F.num(c.res),tg('informado')],
  ['Hóspedes por reserva',F.num(c.pessoas,1),tg('informado')],
  ['Taxa sobre o preço dos adicionais',F.pct(c.taxa*100),tg('informado')],
  ['Perdas sobre o custo',F.pct(c.perda*100),tg('informado')],
  ['Custo fixo mensal do programa',F.brl(c.fixo),tg('informado')],
  ['Margem desejada',F.pct(c.m*100,0),tg('informado')],
  ['Adesão por item','estimativa sua'+(c.adesHip?'; '+c.adesHip+' item(ns) com 10% como hipótese':''),c.adesHip?tg('hipotese'):tg('estimativa')],
  ['Cenários','Conservador = 50% da adesão estimada · Intermediário = 100% · Otimista = 150% (limite de 100%)',tg('hipotese','premissa de cenário')]],[]);
 var card=at.length?ZA.table(['Item','Custo c/ perdas','Preço','Preço sugerido','Margem/venda','Margem %'],at.map(function(x){return [esc(x.nome)+'<br><span class="za-small">'+x.grupo+'</span>',F.brl(x.custoEf),F.brl(x.preco),x.precoSug==null?'—':F.brl(x.precoSug),F.brl(x.margemUnit),F.pct(x.margemPct*100,0)];}),[1,2,3,4,5])+
  '<h3>Volume estimado (cenário intermediário)</h3>'+ZA.table(['Item','Adesão','Vendas/mês','Receita/mês','Contribuição/mês'],at.map(function(x){return [esc(x.nome),F.pct(x.ades,0)+(x.adesHip?' (hipótese)':''),F.num(x.vendas,1),F.brl(x.receita),F.brl(x.contrib)];}).concat([['<b>Total</b>','',F.num(at.reduce(function(t,x){return t+x.vendas;},0),1),'<b>'+F.brl(c.receitaMes)+'</b>','<b>'+F.brl(c.contribMes)+'</b>']]),[1,2,3,4]):'<p class="za-missing">Nenhum item completo (nome e preço).</p>';
 var cen=ZA.table(['Cenário','Adesão aplicada','Receita extra/mês','Contribuição/mês','Resultado/mês (− custo fixo)','Resultado/ano'],c.cen.map(function(x){return [x.nome,F.pct(x.mult*100,0)+' da estimada',F.brl(x.receita),F.brl(x.contrib),F.brl(x.resultado),F.brl(x.anual)];}),[2,3,4,5]);
 var dest=c.items[Number(s.t('ap_destaque'))-1];
 var ordem=at.slice().sort(function(a,b){return (dest&&a.k===dest.k)?-1:(dest&&b.k===dest.k)?1:a.k-b.k;});
 var menu='<div class="za-card"><b>Para deixar sua estadia na '+esc(s.t('propriedade'))+' ainda mais especial</b><ul>'+ordem.map(function(x){return '<li><b>'+esc(x.nome)+'</b> · '+F.brl(x.preco)+(dest&&x.k===dest.k?' <span class="za-tag recomendacao">destaque</span>':'')+'</li>';}).join('')+'</ul><p class="za-small">Pedidos com '+F.num(s.n('ap_antecedencia',24))+' h de antecedência · Cobrança: '+({antecipado:'antecipada, na reserva ou antes da chegada',checkin:'no check-in',checkout:'no check-out'}[s.t('pr_cobranca')]||'a definir')+'.</p></div>'+
  '<p class="za-small">Onde apresentar: '+(arr(s,'ap_canais').length?arr(s,'ap_canais').map(function(v){return CANAIS.filter(function(x){return x.v===v;})[0].l.toLowerCase();}).join('; '):'a definir (sugestão: confirmação da reserva e mensagem pré-chegada)')+'.</p>';
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido de 30 dias</b><ol><li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Fechar preços e fornecedores dos itens')+'.</li><li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Fotografar os itens e montar o cardápio')+'.</li><li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Enviar o cardápio a todas as reservas confirmadas')+'.</li><li><b>Semana 4:</b> contar vendas, adesão real e perdas de cada item; comparar com o cenário intermediário ('+F.brl(c.resultadoMes)+'/mês) e refazer a Calculadora com os números reais.</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Cardápio de adicionais com precificação',html:card+'<p class="za-small">Margem por venda = preço × (1 − taxa) − custo × (1 + perdas). Preço sugerido = custo × (1 + perdas) ÷ (1 − taxa − margem desejada).</p>'},
  {title:'Receita extra em três cenários',html:cen+'<p class="za-small">Cenários ilustrativos, construídos sobre as suas estimativas de adesão. Não são previsões de venda.</p>'},
  {title:'Apresentação do cardápio',html:menu}
 ],plan:plan};
}
});
})();
