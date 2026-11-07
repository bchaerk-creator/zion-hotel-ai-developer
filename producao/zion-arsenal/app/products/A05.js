/* ZAR-A05 · Como Fazer Sua Hospedagem Valer Mais? · Construtor de Experiências e Valor */
(function(){
var F=ZA.fmt, esc=ZA.esc;
var TGL={hipotese:'hipótese',recomendacao:'recomendação'};
function tg(t,l){return '<span class="za-tag '+t+'">'+(l||TGL[t]||t)+'</span>';}
var DIFS=[{v:'vista',l:'Vista (montanha, mar, vale, lago)',c:'vista'},{v:'ofuro',l:'Ofurô, banheira ou hidromassagem',c:'ofurô'},{v:'lareira',l:'Lareira ou fogão a lenha',c:'lareira'},{v:'piscina',l:'Piscina',c:'piscina'},{v:'natureza',l:'Trilhas, mata ou cachoeira',c:'natureza no entorno'},{v:'cafe',l:'Café da manhã caseiro',c:'café da manhã caseiro'},{v:'pet',l:'Aceita pets',c:'espaço para pets'},{v:'homeoffice',l:'Internet rápida para trabalhar',c:'internet para trabalhar'},{v:'centro',l:'Localização central',c:'localização central'},{v:'cozinha',l:'Cozinha completa',c:'cozinha completa'},{v:'estacionamento',l:'Estacionamento',c:'estacionamento'},{v:'anfitriao',l:'Anfitrião que conhece a região',c:'dicas de quem conhece a região'}];
var PERFIL={casais:'casais',familias:'famílias',amigos:'grupos de amigos',remoto:'profissionais em trabalho remoto',pet:'tutores de pets',aventura:'viajantes de aventura'};
var MOTIVO={comemorar:'para comemorar uma data especial',descansar:'para descansar',explorar:'para explorar a região',trabalhar:'para trabalhar com tranquilidade',reunir:'para reunir quem gostam'};
var CANAIS={anuncio:'No anúncio (fotos e descrição)',reserva:'Na mensagem de confirmação da reserva',pre_chegada:'Na mensagem de pré-chegada',guia:'No guia digital da hospedagem',qr:'Em um cartão com QR code no quarto',checkin:'Pessoalmente, no check-in'};

ZA.register({
id:'A05', code:'ZAR-A05', collection:'Hospedagem',
title:'Como Fazer Sua Hospedagem Valer Mais?',
subtitle:'Pare de Competir Apenas pelo Menor Preço',
tool:'Construtor de Experiências e Valor',
deliverable:'Cardápio de Experiências e Proposta de Valor',
nameField:'nome', propertyField:'propriedade',
disclaimer:'Preços sugeridos, margens e receitas extras são calculados com os custos, as horas e as taxas de adesão que você informou ou simulou. A adesão real dos hóspedes só se conhece testando: não há garantia de vendas, faturamento ou lucro.',

intro:[
 {kind:'mirror', title:'Sua hospedagem é bonita. Mas por que alguém escolheria ela?',
  lead:'Você cuida de cada detalhe, recebe elogios, e mesmo assim sente que o hóspede só compara o preço. Quando outro anúncio cobra R$ 30 a menos, ele vai para lá.',
  body:'<div class="za-card"><p>Talvez você já tenha pensado:</p><ul><li>“Se eu não baixar o preço, não alugo.”</li><li>“Minha cabana é melhor que a do vizinho, mas no anúncio parecem iguais.”</li><li>“Os hóspedes pedem sugestões de passeio e eu dou de graça.”</li><li>“Já pensei em oferecer um café especial, mas não sei quanto cobrar.”</li></ul></div>'},
 {kind:'collapse', title:'O problema pode não ser seu preço.',
  lead:'Pode ser a falta de motivos claros para o hóspede perceber mais valor. Quando tudo parece igual, o preço vira o único critério de escolha.',
  body:'<div class="za-card"><p><b>Valor percebido</b> é o quanto o hóspede acha que a estadia vale, comparado com o que vai pagar. Ele sobe quando:</p><ul><li>os diferenciais reais ficam visíveis e comprovados;</li><li>a estadia vira uma <b>experiência</b> pensada para o perfil daquele hóspede;</li><li>há <b>pacotes</b> que resolvem a viagem inteira, não só a cama.</li></ul><p>Neste percurso você vai montar experiências com custo, preço e margem calculados, criar um pacote e escrever a sua proposta de valor.</p></div>'},
 {kind:'start', title:'Vamos construir o seu cardápio de valor',
  lead:'Em 7 pilares você vai entender o valor percebido, conhecer o perfil do hóspede, listar diferenciais reais, criar e precificar experiências e montar a apresentação comercial.',
  body:'<p>Pense em até três experiências que você conseguiria oferecer com o que já tem (um café especial, uma decoração, uma trilha guiada, um jantar). Você vai precisar estimar quanto cada uma custa e quanto tempo leva.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Luciana'},
   {id:'propriedade',label:'Nome da hospedagem',type:'text',required:true,placeholder:'Ex.: Cabana Bosque Encantado'},
   {id:'tipo',label:'Tipo de hospedagem',type:'select',required:true,options:[{v:'airbnb',l:'Apartamento ou casa (Airbnb/temporada)'},{v:'cabana',l:'Cabana ou chalé'},{v:'glamping',l:'Glamping'},{v:'pousada',l:'Pequena pousada'},{v:'outro',l:'Outro'}]},
   {id:'destino',label:'Cidade / destino',type:'text',required:true,placeholder:'Ex.: Gonçalves (MG)'},
   {id:'unidades',label:'Quantas unidades você aluga?',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)'}
  ]}
],

pillars:[
/* 1 */
{title:'Valor percebido', screens:[
 {kind:'learn', title:'Preço é o que o hóspede paga. Valor é o que ele acha que leva.',
  body:'<p>Duas cabanas com a mesma diária podem parecer “cara” e “barata” ao mesmo tempo, dependendo do que cada uma mostra. O hóspede faz uma conta rápida: <b>o que vou viver aqui</b> compensa <b>o que vou pagar</b>?</p><p>Quando o anúncio não dá motivos, a única variável que sobra é o preço, e quem tem a menor diária ganha. Quando há motivos claros, você consegue cobrar o que o seu trabalho vale e ainda assim ser escolhido.</p><p>Um sinal de alerta: dar descontos com frequência. Desconto constante ensina o hóspede a esperar desconto e reduz o valor percebido.</p>',
  example:'Exemplo ilustrativo: diária de R$ 350 contra R$ 380 dos concorrentes. Se o hóspede não enxerga diferença, os R$ 30 decidem. Se enxerga um ofurô com vista e um café colonial entregue na porta, o preço deixa de ser o único critério.'},
 {kind:'compare', title:'Competir por preço × competir por valor',
  cols:[{h:'Por preço',type:'bad',items:['Baixar a diária quando o calendário esvazia','Anúncio que lista móveis','Dar de graça o que poderia ser vendido','Igual aos outros, só que mais barato']},
        {h:'Por valor',type:'good',items:['Manter a diária e oferecer mais motivos','Anúncio que mostra momentos','Experiências com preço e margem','Diferente dos outros, para um público claro']}]},
 {kind:'form', title:'Seu ponto de partida',
  fields:[
   {id:'diaria_atual',label:'Diária média atual',type:'money',required:true,min:1},
   {id:'preco_conc',label:'Diária média de 3 a 5 concorrentes parecidos',type:'money',required:true,allowUnknown:true},
   {id:'motivo_escolha',label:'Por que os hóspedes escolhem você hoje?',type:'radio',required:true,options:[{v:'preco',l:'Pelo preço'},{v:'local',l:'Pela localização'},{v:'estrutura',l:'Pela estrutura (ofurô, vista, piscina…)'},{v:'atendimento',l:'Pelo atendimento e pelos detalhes'},{v:'naosei',l:'Não sei'}]},
   {id:'desconto_freq',label:'Com que frequência você dá desconto?',type:'radio',required:true,options:[{v:'nunca',l:'Quase nunca'},{v:'asvezes',l:'Às vezes, em datas fracas'},{v:'sempre',l:'Quase sempre, para conseguir reservar'}]}
  ]},
 {kind:'feedback', title:'Onde você está hoje',
  metrics:function(s,c){return [{label:'Diária atual',value:F.brl(c.D),tag:'informado'},{label:'Diferença para concorrentes',value:c.gap==null?'sem dado':(c.gap>=0?'+':'')+F.pct(c.gap*100,1),tag:c.gap==null?'hipotese':'calculado'}];},
  feedback:function(s,c){var o=[],m=s.t('motivo_escolha');
   if(c.gap==null) o.push({lv:'warn',t:'Sem a diária dos concorrentes, não sabemos se você está competindo por preço. Pesquise 3 a 5 anúncios parecidos.'});
   else if(c.gap<-0.1) o.push({lv:'warn',t:'Sua diária está '+F.pct(-c.gap*100,0)+' abaixo dos concorrentes. Se a estrutura é parecida ou melhor, falta mostrar valor, não baixar mais.'});
   else if(c.gap>0.1) o.push({lv:'info',t:'Sua diária está '+F.pct(c.gap*100,0)+' acima dos concorrentes. Para sustentar isso, o valor precisa estar evidente e comprovado.'});
   else o.push({lv:'info',t:'Diária próxima da concorrência. Experiências e pacotes podem ser o que diferencia a sua oferta.'});
   if(m==='preco') o.push({lv:'bad',t:'Se o preço é o principal motivo de escolha, qualquer concorrente mais barato leva o seu hóspede. Vamos construir outros motivos.'});
   if(m==='naosei') o.push({lv:'warn',t:'Você não sabe por que te escolhem. Pergunte aos próximos hóspedes: a resposta orienta tudo o que vem a seguir.'});
   if(s.t('desconto_freq')==='sempre') o.push({lv:'bad',t:'Desconto quase sempre é sinal de valor pouco percebido. No Pilar 5, você vai trocar desconto por pacote.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Perguntar aos próximos 5 hóspedes por que escolheram a hospedagem'},{id:'a1_2',text:'Suspender descontos sem motivo e sem prazo'},{id:'a1_3',text:'Listar o que você oferece de graça e que poderia virar experiência'}]}
]},
/* 2 */
{title:'Perfil do hóspede', screens:[
 {kind:'learn', title:'Experiência boa é a que combina com quem chega',
  body:'<p>Um jantar à luz de velas encanta um casal em aniversário de namoro e não faz sentido para uma família com três crianças. Antes de criar experiências, defina:</p><ul><li><b>Perfil principal</b>: quem mais reserva;</li><li><b>Motivo da viagem</b>: comemorar, descansar, explorar, trabalhar, reunir;</li><li><b>Sensibilidade a preço</b>: há quem conte cada real e há quem pague mais por algo memorável;</li><li><b>Volume</b>: quantas reservas e quantas pessoas por reserva, para calcular o potencial.</li></ul>',
  example:'Exemplo: casais que vêm comemorar e buscam experiência aceitam bem um kit romântico. Famílias sensíveis a preço preferem um item simples e útil, como um kit de café da manhã para as crianças.'},
 {kind:'compare', title:'Experiência genérica × experiência sob medida',
  cols:[{h:'Genérica',type:'bad',items:['O mesmo “pacote especial” para todos','Oferta feita sem saber o motivo da viagem','Preço alto para quem é sensível a preço']},
        {h:'Sob medida',type:'good',items:['Ofertas por perfil (casal, família, trabalho)','Pergunta sobre o motivo da viagem na reserva','Opções de entrada e uma opção premium']}]},
 {kind:'form', title:'Quem é o seu hóspede',
  fields:[
   {id:'perfil',label:'Perfil principal',type:'radio',required:true,options:Object.keys(PERFIL).map(function(k){return {v:k,l:PERFIL[k].charAt(0).toUpperCase()+PERFIL[k].slice(1)};})},
   {id:'motivo_viagem',label:'Motivo mais comum da viagem',type:'radio',required:true,options:[{v:'comemorar',l:'Comemorar uma data'},{v:'descansar',l:'Descansar'},{v:'explorar',l:'Explorar a região'},{v:'trabalhar',l:'Trabalhar remoto'},{v:'reunir',l:'Reunir família ou amigos'}]},
   {id:'sensibilidade',label:'Como esse hóspede se relaciona com preço?',type:'radio',required:true,options:[{v:'preco',l:'Muito sensível a preço'},{v:'equilibrio',l:'Busca equilíbrio entre preço e qualidade'},{v:'experiencia',l:'Paga mais por algo memorável'}]},
   {id:'reservas_mes',label:'Reservas por mês (média)',type:'number',required:true,min:0,step:1,allowUnknown:true,help:'Se não souber, os cálculos usam uma base ilustrativa de 10 reservas.'},
   {id:'hospedes_reserva',label:'Pessoas por reserva (média)',type:'number',required:true,min:1,max:30,step:0.5,unit:'pessoas'}
  ]},
 {kind:'feedback', title:'O que esse perfil pede',
  metrics:function(s,c){return [{label:'Perfil',value:PERFIL[s.t('perfil')]||'—',tag:'informado'},{label:'Reservas/mês usadas nos cálculos',value:F.num(c.reservasBase),tag:c.reservasHip?'hipotese':'informado'}];},
  feedback:function(s,c){var o=[],se=s.t('sensibilidade');
   if(se==='preco') o.push({lv:'info',t:'Hóspede sensível a preço: comece por experiências de custo baixo e preço acessível, que pareçam um presente bem pensado.'});
   if(se==='experiencia') o.push({lv:'ok',t:'Hóspede que paga por algo memorável: há espaço para uma experiência premium, desde que entregue com capricho.'});
   if(se==='equilibrio') o.push({lv:'info',t:'Hóspede que busca equilíbrio: ofereça uma opção simples e uma completa, e deixe-o escolher.'});
   if(s.t('motivo_viagem')==='comemorar') o.push({lv:'info',t:'Quem vem comemorar costuma valorizar decoração, bebida e um momento especial preparado com antecedência.'});
   if(c.reservasHip) o.push({lv:'warn',t:'Reservas por mês desconhecidas: os potenciais serão mostrados com base ilustrativa de 10 reservas. Não é uma previsão.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Incluir na mensagem de confirmação a pergunta “qual o motivo da viagem?”'},{id:'a2_2',text:'Anotar perfil e motivo de cada reserva por 30 dias'},{id:'a2_3',text:'Separar ideias de experiência por perfil de hóspede'}]}
]},
/* 3 */
{title:'Diferenciais reais', screens:[
 {kind:'learn', title:'Diferencial real é o que você entrega e consegue provar',
  body:'<p>“Lugar tranquilo” e “ótimo atendimento” todo anúncio promete. <b>Diferencial real</b> é concreto e verificável: o ofurô existe, a vista aparece na foto, o café é feito com produtos da região. Ele serve de base para as experiências: um ofurô vira “ofurô aquecido com sais e espumante”; o conhecimento da região vira “roteiro de trilhas personalizado”.</p><p>Todo diferencial precisa de <b>prova</b>: uma foto, um trecho de avaliação, um detalhe na descrição.</p>',
  example:'Exemplo: “Conhecemos a região” é promessa. “Mapa impresso com as 5 cachoeiras mais próximas, tempo de caminhada e nível de dificuldade” é diferencial real e pode até ser vendido como parte de um pacote.'},
 {kind:'compare', title:'Promessa × diferencial comprovado',
  cols:[{h:'Promessa',type:'bad',items:['“Ambiente aconchegante”','“Ótima localização”','“Atendimento diferenciado”']},
        {h:'Comprovado',type:'good',items:['Foto da lareira acesa com mantas no sofá','“A 400 m da praia, 5 minutos a pé”','Trecho de avaliação citando a ajuda do anfitrião']}]},
 {kind:'form', title:'Seus diferenciais reais',
  fields:[
   {id:'difs',label:'Quais diferenciais você realmente tem?',type:'checks',options:DIFS.map(function(d){return {v:d.v,l:d.l};})},
   {id:'difs_prova',label:'Esses diferenciais têm prova no anúncio (foto, detalhe, avaliação)?',type:'radio',required:true,options:[{v:'todos',l:'Todos'},{v:'alguns',l:'Alguns'},{v:'nenhum',l:'Nenhum'}]},
   {id:'dif_unico',label:'Algo que só você oferece na região (opcional)',type:'text',required:false,max:100,placeholder:'Ex.: queijos da fazenda vizinha no café'}
  ]},
 {kind:'feedback', title:'Sua base de valor',
  metrics:function(s,c){return [{label:'Diferenciais reais',value:String(c.nDifs),tag:'informado'},{label:'Prova no anúncio',value:{todos:'todos',alguns:'alguns',nenhum:'nenhum'}[s.t('difs_prova')]||'—',tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(c.nDifs===0) o.push({lv:'bad',t:'Nenhum diferencial marcado. As experiências do próximo pilar podem se tornar o seu primeiro diferencial.'});
   else o.push({lv:'info',t:'Diferenciais que podem virar experiência: '+c.difsNomes.map(function(x){return '<b>'+x+'</b>';}).join(', ')+'.'});
   if(s.t('difs_prova')==='nenhum'&&c.nDifs>0) o.push({lv:'bad',t:'Diferenciais sem prova não aumentam o valor percebido. Fotografe cada um e cite-os na descrição.'});
   else if(s.t('difs_prova')==='alguns') o.push({lv:'warn',t:'Parte dos diferenciais ainda não tem prova no anúncio.'});
   if(s.t('dif_unico')) o.push({lv:'ok',t:'“'+esc(s.t('dif_unico'))+'” é um diferencial difícil de copiar. Ele merece destaque na proposta de valor.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Fotografar cada diferencial em uso'},{id:'a3_2',text:'Trocar promessas genéricas da descrição por fatos verificáveis'},{id:'a3_3',text:'Escolher um diferencial para transformar em experiência paga'}]}
]},
/* 4 */
{title:'Experiências', screens:[
 {kind:'learn', title:'Experiência é um momento com começo, meio e fim',
  body:'<p>Uma boa experiência para hospedagem é <b>simples de entregar</b>, <b>ligada a um diferencial</b> e <b>pensada para o perfil</b> do hóspede. Exemplos: cesta de café colonial na porta, kit romântico com decoração e espumante, trilha guiada, fondue na lareira, kit de piquenique.</p><p>Para precificar, você precisa de dois custos:</p><ul><li><b>Custo direto</b>: ingredientes, produtos, terceiros, por venda;</li><li><b>Tempo</b>: horas de preparo e entrega, multiplicadas pelo <b>valor da sua hora</b> (ou da equipe).</li></ul><p>E de duas decisões: a <b>taxa</b> que incide sobre a venda (cartão, comissão) e a <b>margem</b> que deve sobrar.</p><div class="za-card"><b>Preço sugerido = (custo direto + horas × valor da hora) ÷ (1 − taxa − margem)</b></div>',
  example:'Exemplo ilustrativo: cesta de café com R$ 60 de ingredientes e 30 minutos de preparo, hora valendo R$ 40: custo total de R$ 80. Com taxa de 5% e margem de 30%, o preço sugerido é 80 ÷ 0,65 = <b>R$ 123,08</b>.'},
 {kind:'compare', title:'Ideias que costumam dar trabalho × ideias simples de entregar',
  cols:[{h:'Exigem mais estrutura',type:'bad',items:['Jantar completo com chef todo dia','Passeios que dependem de veículo próprio','Itens perecíveis sem demanda confirmada']},
        {h:'Simples de começar',type:'good',items:['Kits montados sob encomenda com antecedência','Parceria com guia ou produtor local','Itens com boa durabilidade (vinho, lenha, mapas)']}]},
 {kind:'form', title:'Suas experiências (até 3)', intro:'A primeira é obrigatória; as outras, se tiver. Custos por venda.',
  fields:[
   {id:'exp1_nome',label:'Experiência 1 · nome',type:'text',required:true,max:60,placeholder:'Ex.: Cesta de café colonial'},
   {id:'exp1_custo',label:'Experiência 1 · custo direto por venda',type:'money',required:true},
   {id:'exp1_horas',label:'Experiência 1 · horas de preparo e entrega',type:'number',required:true,min:0,max:24,step:0.25,unit:'h'},
   {id:'exp2_nome',label:'Experiência 2 · nome (opcional)',type:'text',required:false,max:60},
   {id:'exp2_custo',label:'Experiência 2 · custo direto por venda',type:'money',required:false},
   {id:'exp2_horas',label:'Experiência 2 · horas',type:'number',required:false,min:0,max:24,step:0.25,unit:'h'},
   {id:'exp3_nome',label:'Experiência 3 · nome (opcional)',type:'text',required:false,max:60},
   {id:'exp3_custo',label:'Experiência 3 · custo direto por venda',type:'money',required:false},
   {id:'exp3_horas',label:'Experiência 3 · horas',type:'number',required:false,min:0,max:24,step:0.25,unit:'h'},
   {id:'valor_hora',label:'Quanto vale uma hora do seu trabalho (ou da equipe)?',type:'money',required:true,help:'Use 0 se preferir não considerar o tempo, mas saiba que ele tem valor.'},
   {id:'taxa_exp',label:'Taxa sobre a venda (cartão, comissão)',type:'percent',required:true,max:40},
   {id:'margem_exp',label:'Margem desejada sobre o preço das experiências',type:'percent',required:true,max:90}
  ]},
 {kind:'feedback', title:'Preço sugerido de cada experiência',
  metrics:function(s,c){return c.exps.map(function(e){return {label:e.nome,value:e.sug==null?'inviável':F.brl(e.sug),tag:'calculado'};});},
  feedback:function(s,c){var o=[];
   if(c.denom<=0) o.push({lv:'bad',t:'Taxa + margem somam '+F.pct((1-c.denom)*100,0)+'. Com 100% ou mais, não existe preço possível. Reduza a margem desejada.'});
   c.exps.forEach(function(e){ if(e.sug!=null) o.push({lv:'info',t:'<b>'+esc(e.nome)+'</b>: custo total de '+F.brl(e.custoTotal)+' ('+F.brl(e.custo)+' diretos + '+F.num(e.horas,2)+' h × '+F.brl(c.vh)+'). Preço sugerido: <b>'+F.brl(e.sug)+'</b>.'}); });
   if(c.vh===0) o.push({lv:'warn',t:'Valor da hora igual a zero: o preço sugerido não paga o seu tempo de preparo.'});
   if(c.exps.length<2) o.push({lv:'info',t:'Com uma só experiência, o hóspede tem menos opções. Pense numa segunda, de preço mais acessível.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Montar uma unidade de teste de cada experiência e cronometrar o tempo'},{id:'a4_2',text:'Pedir cotação a um parceiro local (produtor, guia, restaurante)'},{id:'a4_3',text:'Fotografar a experiência pronta para usar no anúncio'}]}
]},
/* 5 */
{title:'Pacotes', screens:[
 {kind:'learn', title:'Pacote: trocar desconto por valor',
  body:'<p>Em vez de baixar a diária, o pacote junta <b>noites + experiências</b> num preço único. O hóspede sente que ganhou algo (desconto sobre a soma dos itens), e você aumenta o valor de cada reserva sem mexer na diária.</p><p>O Construtor calcula:</p><ul><li><b>Preço do pacote</b> = (diária × noites + preço das experiências incluídas) × (1 − desconto);</li><li><b>Contribuição do pacote</b> = preço × (1 − taxa) − custo por noite × noites − custo total das experiências;</li><li><b>Valor adicional</b> = preço do pacote − diárias sem pacote.</li></ul>',
  example:'Exemplo ilustrativo: 2 noites a R$ 350 + cesta (R$ 120) + kit romântico (R$ 184,62), com 10% de desconto: (700 + 120 + 184,62) × 0,90 = <b>R$ 904,15</b>. São R$ 204,15 a mais que as diárias sozinhas.'},
 {kind:'compare', title:'Desconto × pacote',
  cols:[{h:'Desconto de 10% na diária',type:'bad',items:['Você recebe menos pela mesma estadia','O hóspede aprende a esperar desconto','Nada muda na experiência']},
        {h:'Pacote com 10% sobre a soma',type:'good',items:['O valor da reserva aumenta','O desconto incide sobre itens com margem','O hóspede leva uma lembrança da viagem']}]},
 {kind:'form', title:'Monte o seu pacote',
  fields:[
   {id:'pac_nome',label:'Nome do pacote',type:'text',required:true,max:60,placeholder:'Ex.: Refúgio Romântico'},
   {id:'pac_noites',label:'Noites incluídas',type:'number',required:true,min:1,max:30,step:1,unit:'noites'},
   {id:'pac_exps',label:'Experiências incluídas',type:'checks',options:[{v:'e1',l:'Experiência 1'},{v:'e2',l:'Experiência 2'},{v:'e3',l:'Experiência 3'}]},
   {id:'pac_desc',label:'Desconto sobre a soma dos itens',type:'percent',required:true,max:40},
   {id:'custo_noite',label:'Custo variável por noite (limpeza rateada, energia, amenities)',type:'money',required:true,allowUnknown:true}
  ]},
 {kind:'feedback', title:'O seu pacote em números',
  intro:'Calculado com os preços sugeridos no Pilar 4; no Pilar 6 você define o preço final de cada experiência.',
  metrics:function(s,c){var p=c.pac;return [{label:'Preço do pacote',value:F.brl(p.preco),tag:'calculado'},{label:'Valor adicional por reserva',value:F.brl(p.adicional),tag:'calculado'},{label:'Contribuição do pacote',value:F.brl(p.contrib),tag:s.unknown('custo_noite')?'estimativa':'calculado'},{label:'Diária efetiva no pacote',value:F.brl(p.diariaEfetiva),tag:'calculado'}];},
  feedback:function(s,c){var o=[],p=c.pac;
   if(!p.itens.length) o.push({lv:'warn',t:'Nenhuma experiência com preço foi incluída. Sem elas, o pacote é só um desconto na diária.'});
   else o.push({lv:'ok',t:'O pacote “'+esc(s.t('pac_nome'))+'” inclui '+p.itens.map(function(e){return esc(e.nome);}).join(' + ')+' e soma '+F.brl(p.adicional)+' ao valor da reserva.'});
   if(p.ignorados) o.push({lv:'warn',t:p.ignorados+' experiência(s) marcada(s) no pacote não têm nome ou preço possível e ficaram de fora.'});
   if(s.unknown('custo_noite')) o.push({lv:'warn',t:'Custo por noite desconhecido: entrou como R$ 0. A contribuição real do pacote é menor.'});
   if(p.diariaEfetiva<c.D) o.push({lv:'warn',t:'A diária efetiva do pacote ('+F.brl(p.diariaEfetiva)+') ficou abaixo da diária normal. Reduza o desconto ou inclua mais valor.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Publicar o pacote como opção nas datas de maior procura'},{id:'a5_2',text:'Oferecer o pacote no lugar de desconto quando o hóspede pedir abatimento'},{id:'a5_3',text:'Definir com quantos dias de antecedência o pacote precisa ser reservado'}]}
]},
/* 6 */
{title:'Precificação das experiências', screens:[
 {kind:'learn', title:'Do preço sugerido ao preço final',
  body:'<p>O preço sugerido garante a margem desejada. O <b>preço final</b> é uma decisão comercial: você pode arredondar (R$ 123,08 vira R$ 125), testar um valor abaixo para lançar ou um valor acima para uma versão premium. O Construtor mostra a margem real de cada escolha.</p><p>A receita extra depende da <b>adesão</b>: de cada 100 reservas, quantas compram a experiência. Ninguém sabe esse número antes de testar; por isso ele aparece em três cenários.</p>',
  example:'Exemplo ilustrativo: cesta com custo total de R$ 80 e taxa de 5%. A R$ 120, sobra 120 × 0,95 − 80 = R$ 34 (margem de 28,3%). A R$ 125, sobram R$ 38,75 (31%). Com 6 reservas no mês e 25% de adesão, são 1,5 vendas por mês, em média.'},
 {kind:'compare', title:'Formas de definir o preço final',
  cols:[{h:'Arriscado',type:'bad',items:['Cobrar só o custo dos ingredientes','Copiar o preço de restaurante da cidade sem contar seu tempo','Preço que não paga a taxa do cartão']},
        {h:'Seguro',type:'good',items:['Partir do preço sugerido','Arredondar para um valor fácil de lembrar','Conferir a margem real antes de publicar']}]},
 {kind:'form', title:'Seus preços finais', intro:'Deixe em branco para usar o preço sugerido.',
  fields:[
   {id:'exp1_preco',label:'Preço final · Experiência 1',type:'money',required:false},
   {id:'exp2_preco',label:'Preço final · Experiência 2',type:'money',required:false},
   {id:'exp3_preco',label:'Preço final · Experiência 3',type:'money',required:false},
   {id:'adesao',label:'Quantos hóspedes, a cada 100 reservas, você acredita que comprariam cada experiência?',type:'percent',required:true,allowUnknown:true,help:'É uma suposição para teste. Se marcar “não sei”, os cenários usam 10%, 20% e 30%.'}
  ]},
 {kind:'feedback', title:'Margem real e potencial',
  metrics:function(s,c){return [{label:'Receita extra mensal (cenário intermediário)',value:F.brl(c.receitaExtra),tag:'estimativa'},{label:'Contribuição extra mensal',value:F.brl(c.lucroExtra),tag:'estimativa'},{label:'Adesão usada',value:F.pct(c.adesaoUsada,1),tag:c.adesaoHip?'hipotese':'informado'}];},
  feedback:function(s,c){var o=[];
   c.exps.forEach(function(e){
    if(e.preco==null) o.push({lv:'bad',t:'<b>'+esc(e.nome)+'</b>: sem preço possível com a taxa e a margem informadas.'});
    else if(e.margem<c.margemExp-0.0001) o.push({lv:'warn',t:'<b>'+esc(e.nome)+'</b> a '+F.brl(e.preco)+': margem real de '+F.pct(e.margem*100,1)+', abaixo da desejada ('+F.pct(c.margemExp*100,0)+'). Preço sugerido: '+F.brl(e.sug)+'.'});
    else o.push({lv:'ok',t:'<b>'+esc(e.nome)+'</b> a '+F.brl(e.preco)+': sobram '+F.brl(e.contrib)+' por venda (margem de '+F.pct(e.margem*100,1)+').'});
    if(e.preco!=null&&e.contrib<0) o.push({lv:'bad',t:'<b>'+esc(e.nome)+'</b> dá prejuízo a cada venda. Revise o preço.'});
   });
   o.push({lv:'info',t:'Com '+F.num(c.reservasBase)+' reservas/mês'+(c.reservasHip?' (base ilustrativa)':'')+' e adesão de '+F.pct(c.adesaoUsada,0)+', a estimativa é de '+F.num(c.vendasExp,1)+' venda(s) de cada experiência por mês. É uma simulação para orientar o teste.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Oferecer as experiências para as próximas 10 reservas e anotar quantas compraram'},{id:'a6_2',text:'Revisar preço e margem depois do teste'},{id:'a6_3',text:'Definir prazo de antecedência para pedidos de cada experiência'}]}
]},
/* 7 */
{title:'Apresentação comercial', screens:[
 {kind:'learn', title:'Proposta de valor e cardápio: como o hóspede fica sabendo',
  body:'<p>Experiência que o hóspede não conhece não vende. A apresentação tem duas peças:</p><ul><li><b>Proposta de valor</b>: uma frase que junta perfil, motivo da viagem, diferencial e experiência. Ela vai para o início da descrição e para a mensagem de confirmação.</li><li><b>Cardápio de experiências</b>: nome, o que inclui, preço e antecedência, apresentado em mais de um momento da jornada.</li></ul><p>O melhor momento costuma ser <b>antes da chegada</b>: o hóspede ainda está planejando e tem tempo de encomendar.</p>',
  example:'Exemplo de proposta: “Para casais que vêm comemorar uma data especial, a Cabana Bosque oferece ofurô com vista e experiências como a cesta de café colonial e o kit romântico, para voltar para casa com a sensação de ter vivido algo só de vocês.”'},
 {kind:'compare', title:'Oferta escondida × oferta apresentada',
  cols:[{h:'Escondida',type:'bad',items:['“Se quiser algo, é só pedir”','Cardápio só no quarto, depois da chegada','Preço informado só quando perguntam']},
        {h:'Apresentada',type:'good',items:['Proposta de valor no anúncio','Cardápio na mensagem de pré-chegada','Preço, inclusões e prazo de pedido claros']}]},
 {kind:'form', title:'Sua apresentação',
  fields:[
   {id:'transformacao',label:'Com que sensação você quer que o hóspede volte para casa?',type:'text',required:true,max:120,placeholder:'Ex.: com a sensação de ter vivido algo só de vocês'},
   {id:'canais',label:'Onde você vai apresentar as experiências?',type:'checks',options:Object.keys(CANAIS).map(function(k){return {v:k,l:CANAIS[k]};})},
   {id:'antecedencia',label:'Com quanta antecedência o hóspede precisa pedir?',type:'number',required:true,min:0,max:30,step:1,unit:'dias'}
  ]},
 {kind:'feedback', title:'Sua proposta de valor',
  metrics:function(s,c){return [{label:'Índice de valor',value:F.num(c.indiceValor,0)+'/100',tag:'calculado'},{label:'Canais de apresentação',value:String(c.nCanais),tag:'informado'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:'ok',t:'“'+c.proposta+'”'});
   if(c.nCanais<2) o.push({lv:'warn',t:'Apresentar as experiências em só '+c.nCanais+' momento(s) limita a adesão. Combine anúncio e mensagem de pré-chegada.'});
   if(s.v.canais&&s.v.canais.indexOf('pre_chegada')<0) o.push({lv:'info',t:'A mensagem de pré-chegada é o momento em que o hóspede ainda planeja a viagem. Inclua o cardápio nela.'});
   if(s.n('antecedencia',0)>0) o.push({lv:'info',t:'Pedido com '+F.num(s.n('antecedencia'))+' dia(s) de antecedência: envie o cardápio pelo menos alguns dias antes desse prazo.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Colocar a proposta de valor no início da descrição do anúncio'},{id:'a7_2',text:'Incluir o cardápio na mensagem de pré-chegada'},{id:'a7_3',text:'Criar um cartão com QR code do cardápio para o quarto'}]}
]}
],

compute:function(s){
 var c={};
 c.D=s.n('diaria_atual',0);
 c.conc=s.has('preco_conc')&&s.n('preco_conc')>0?s.n('preco_conc'):null; c.gap=c.conc!=null?c.D/c.conc-1:null;
 c.reservasHip=!s.has('reservas_mes'); c.reservasBase=c.reservasHip?10:s.n('reservas_mes',0);
 var dsel=s.v.difs||[]; c.nDifs=dsel.length; c.difsNomes=DIFS.filter(function(d){return dsel.indexOf(d.v)>=0;}).map(function(d){return d.c;});
 c.vh=s.n('valor_hora',0); c.taxa=s.n('taxa_exp',0)/100; c.margemExp=s.n('margem_exp',0)/100; c.denom=1-c.taxa-c.margemExp;
 c.exps=[]; c.expsAll={};
 [1,2,3].forEach(function(i){var nome=s.t('exp'+i+'_nome').trim(); if(!nome) return;
   var e={id:'e'+i,i:i,nome:nome,custo:s.n('exp'+i+'_custo',0)||0,horas:s.n('exp'+i+'_horas',0)||0};
   e.custoTotal=e.custo+e.horas*c.vh; e.sug=c.denom>0?e.custoTotal/c.denom:null;
   e.precoInf=s.has('exp'+i+'_preco')?s.n('exp'+i+'_preco'):null;
   e.preco=e.precoInf!=null&&e.precoInf>0?e.precoInf:e.sug;
   e.contrib=e.preco!=null?e.preco*(1-c.taxa)-e.custoTotal:null;
   e.margem=(e.preco!=null&&e.preco>0)?e.contrib/e.preco:null;
   c.exps.push(e); c.expsAll[e.id]=e;});
 c.nExps=c.exps.length;
 c.indiceValor=Math.min(c.nDifs,5)*8+({todos:30,alguns:15,nenhum:0}[s.t('difs_prova')]||0)+c.nExps*10;
 // pacote
 var N=s.n('pac_noites',1)||1, cn=s.n('custo_noite',0)||0, desc=s.n('pac_desc',0)/100;
 var marc=s.v.pac_exps||[], itens=[], ign=0;
 marc.forEach(function(k){var e=c.expsAll[k]; if(e&&e.preco!=null) itens.push(e); else ign++;});
 var p={itens:itens,ignorados:ign,noites:N};
 p.base=c.D*N+ZA.sum(itens.map(function(e){return e.preco;}));
 p.preco=p.base*(1-desc); p.custo=N*cn+ZA.sum(itens.map(function(e){return e.custoTotal;}));
 p.contrib=p.preco*(1-c.taxa)-p.custo; p.margem=p.preco>0?p.contrib/p.preco:null;
 p.adicional=p.preco-c.D*N; p.diariaEfetiva=p.preco/N;
 c.pac=p; c.pacPreco=p.preco; c.pacContrib=p.contrib; c.pacMargem=p.margem; c.pacAdicional=p.adicional;
 // adesão e potencial
 c.adesaoHip=!s.has('adesao'); var a=c.adesaoHip?20:s.n('adesao',0);
 c.adesaoUsada=a; c.vendasExp=c.reservasBase*a/100;
 var precos=c.exps.filter(function(e){return e.preco!=null;});
 var somaP=ZA.sum(precos.map(function(e){return e.preco;})), somaC=ZA.sum(precos.map(function(e){return e.contrib;}));
 c.receitaExtra=c.vendasExp*somaP; c.lucroExtra=c.vendasExp*somaC;
 var cenA=c.adesaoHip?[10,20,30]:[a/2,a,Math.min(100,a*1.5)];
 c.cen=[['Conservador',cenA[0]],['Intermediário',cenA[1]],['Otimista',cenA[2]]].map(function(x){var v=c.reservasBase*x[1]/100;return {nome:x[0],adesao:x[1],vendas:v,receita:v*somaP,lucro:v*somaC,anual:v*somaC*12};});
 c.lucroConservador=c.cen[0].lucro; c.lucroOtimista=c.cen[2].lucro;
 c.abaixoMargem=c.exps.filter(function(e){return e.preco!=null&&e.margem<c.margemExp-0.0001;});
 // proposta de valor
 c.nCanais=(s.v.canais||[]).length;
 var difTxt=s.t('dif_unico')?esc(s.t('dif_unico')):(c.difsNomes.length?c.difsNomes.slice(0,2).join(', '):'um cuidado em cada detalhe');
 var expTxt=c.exps.length?' e experiências como '+(c.exps.length>1?c.exps.slice(0,-1).map(function(e){return esc(e.nome);}).join(', ')+' e '+esc(c.exps[c.exps.length-1].nome):esc(c.exps[0].nome)):'';
 c.proposta='Para '+(PERFIL[s.t('perfil')]||'hóspedes')+' que vêm '+(MOTIVO[s.t('motivo_viagem')]||'para a região')+', a '+esc(s.t('propriedade'))+' oferece '+difTxt+expTxt+(s.t('transformacao')?', para voltar para casa '+esc(String(s.t('transformacao')).trim().replace(/^para voltar para casa\s*/i,'').replace(/[.!\s]+$/,'')):'')+'.';
 return c;
},

metrics:function(s,c){var L=[
 {label:'Diária atual',value:F.brl(c.D),tag:'informado'},
 {label:'Diferença para concorrentes',value:c.gap==null?'sem dado':(c.gap>=0?'+':'')+F.pct(c.gap*100,1),tag:c.gap==null?'hipotese':'calculado'},
 {label:'Índice de valor',value:F.num(c.indiceValor,0)+'/100',tag:'calculado'},
 {label:'Experiências no cardápio',value:String(c.nExps),tag:'informado'},
 {label:'Preço do pacote',value:F.brl(c.pac.preco),tag:'calculado'},
 {label:'Valor adicional por reserva com pacote',value:F.brl(c.pac.adicional),tag:'calculado'},
 {label:'Contribuição extra mensal (intermediário)',value:F.brl(c.lucroExtra),tag:'estimativa'}];
 return L;},

priorities:function(s,c){var L=[];
 if(c.denom<=0) L.push({title:'Rever taxa e margem desejada das experiências',why:'Com a combinação atual, não existe preço possível.',score:10});
 c.abaixoMargem.forEach(function(e){L.push({title:'Ajustar o preço de “'+e.nome+'” para cerca de '+F.brl(e.sug),why:'Margem real de '+F.pct(e.margem*100,1)+', abaixo da desejada.',score:e.contrib<0?9:7});});
 if(s.t('desconto_freq')==='sempre') L.push({title:'Trocar descontos pelo pacote “'+s.t('pac_nome')+'”',why:'Desconto frequente reduz o valor percebido.',score:9});
 if(c.pac.itens.length) L.push({title:'Lançar o pacote “'+s.t('pac_nome')+'” por '+F.brl(c.pac.preco),why:'Soma '+F.brl(c.pac.adicional)+' ao valor de cada reserva que o escolher.',score:7});
 if(s.t('difs_prova')!=='todos'&&c.nDifs>0) L.push({title:'Mostrar a prova de cada diferencial no anúncio',why:'Diferencial sem prova não aumenta o valor percebido.',score:7});
 if(c.nDifs<3) L.push({title:'Mapear e comunicar diferenciais reais',why:'Só '+c.nDifs+' diferencial(is) marcado(s).',score:7});
 if(c.gap!=null&&c.gap<-0.1) L.push({title:'Parar de reduzir a diária e reforçar a oferta de valor',why:'Diária '+F.pct(-c.gap*100,0)+' abaixo dos concorrentes.',score:7});
 if(['preco','naosei'].indexOf(s.t('motivo_escolha'))>=0) L.push({title:'Descobrir com os hóspedes por que escolhem você',why:s.t('motivo_escolha')==='preco'?'Hoje o preço é o principal motivo de escolha.':'O motivo de escolha é desconhecido.',score:6});
 if(c.adesaoHip||c.reservasHip) L.push({title:'Testar o cardápio com as próximas 10 reservas e medir a adesão',why:'Os potenciais usam '+(c.adesaoHip?'adesão':'volume de reservas')+' hipotético(a).',score:6});
 else L.push({title:'Acompanhar a adesão real de cada experiência',why:'A estimativa usa '+F.pct(c.adesaoUsada,0)+' de adesão informada por você.',score:4});
 if(c.nCanais<2) L.push({title:'Apresentar o cardápio no anúncio e na pré-chegada',why:'Experiência que o hóspede não conhece não vende.',score:6});
 if(c.nExps<2) L.push({title:'Criar uma segunda experiência, de preço mais acessível',why:'Uma única opção limita a escolha do hóspede.',score:5});
 if(c.vh===0) L.push({title:'Incluir o valor do seu tempo no preço das experiências',why:'Hoje o preço não paga as horas de preparo.',score:5});
 if(s.unknown('custo_noite')) L.push({title:'Calcular o custo variável por noite',why:'A contribuição do pacote está superestimada.',score:4});
 return L;},

report:function(s,c){
 var p=c.pac;
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Diária atual',F.brl(c.D),tg('informado')],
  ['Diária dos concorrentes',c.conc==null?'—':F.brl(c.conc),c.conc==null?tg('hipotese','sem dado'):tg('informado')],
  ['Valor da hora',F.brl(c.vh),tg('informado')],
  ['Taxa sobre a venda / margem desejada',F.pct(c.taxa*100,1)+' / '+F.pct(c.margemExp*100,0),tg('informado')],
  ['Reservas por mês',F.num(c.reservasBase),c.reservasHip?tg('hipotese','base ilustrativa'):tg('informado')],
  ['Adesão por experiência',F.pct(c.adesaoUsada,1),c.adesaoHip?tg('hipotese','hipótese de teste'):tg('informado','suposição sua')],
  ['Custo variável por noite',F.brl(s.n('custo_noite',0)||0),s.unknown('custo_noite')?tg('hipotese','hipótese: R$ 0'):tg('informado')]],[1]);
 var card=c.exps.length?ZA.table(['Experiência','Custo total','Preço sugerido','Preço final','Sobra por venda','Margem'],c.exps.map(function(e){return [esc(e.nome),F.brl(e.custoTotal),e.sug==null?'inviável':F.brl(e.sug),e.preco==null?'—':F.brl(e.preco)+(e.precoInf==null?' '+tg('recomendacao','sugerido'):''),e.contrib==null?'—':F.brl(e.contrib),e.margem==null?'—':F.pct(e.margem*100,1)];}),[1,2,3,4,5]):'<p class="za-missing">Nenhuma experiência cadastrada.</p>';
 var pac=ZA.table(['Item','Valor'],[
  ['Noites',F.num(p.noites)+' × '+F.brl(c.D)],['Experiências incluídas',p.itens.length?p.itens.map(function(e){return esc(e.nome);}).join(' + '):'nenhuma'],
  ['Soma dos itens',F.brl(p.base)],['Desconto',F.pct(s.n('pac_desc',0),0)],['<b>Preço do pacote</b>','<b>'+F.brl(p.preco)+'</b>'],
  ['Diária efetiva',F.brl(p.diariaEfetiva)],['Valor adicional sobre as diárias',F.brl(p.adicional)],['Contribuição do pacote',F.brl(p.contrib)+(p.margem==null?'':' ('+F.pct(p.margem*100,1)+')')]],[1]);
 var cen=ZA.table(['Cenário','Adesão','Vendas/mês por experiência','Receita extra/mês','Contribuição/mês','Contribuição/ano'],c.cen.map(function(x){return [x.nome,F.pct(x.adesao,1),F.num(x.vendas,1),F.brl(x.receita),F.brl(x.lucro),F.brl(x.anual)];}),[1,2,3,4,5]);
 var canais=(s.v.canais||[]).map(function(k){return CANAIS[k];}).filter(Boolean);
 var ant=s.n('antecedencia',0);
 var msg='<div class="za-card"><b>Modelo de mensagem de pré-chegada</b><p>Olá! Falta pouco para a sua estadia na '+esc(s.t('propriedade'))+'. Para deixar a viagem ainda mais especial, preparamos algumas experiências:</p><ul>'+c.exps.filter(function(e){return e.preco!=null;}).map(function(e){return '<li>'+esc(e.nome)+' · '+F.brl(e.preco)+'</li>';}).join('')+'</ul><p>'+(ant>0?'Os pedidos precisam ser feitos com '+F.num(ant)+' dia(s) de antecedência. ':'')+'É só responder esta mensagem.</p></div>';
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro de 30 dias</b><ol>'+
  '<li><b>Semana 1:</b> montar uma unidade de teste de cada experiência, cronometrar e conferir o custo. '+(top[0]?'Prioridade: '+esc(top[0].title)+'.':'')+'</li>'+
  '<li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Publicar a proposta de valor no anúncio')+'; fotografar as experiências.</li>'+
  '<li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Enviar o cardápio na pré-chegada')+'.</li>'+
  '<li><b>Semana 4:</b> contar quantas reservas compraram cada experiência ou o pacote, comparar com o cenário intermediário ('+F.num(c.vendasExp,1)+' venda(s) de cada) e ajustar preços.</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Proposta de valor',html:'<div class="za-card"><p style="font-size:18px">“'+c.proposta+'”</p></div><p class="za-small">Frase montada a partir das suas respostas. Ajuste ao seu jeito de falar e use no início da descrição e na confirmação da reserva.</p>'},
  {title:'Cardápio de experiências',html:card+'<p class="za-small">Preço sugerido = (custo direto + horas × valor da hora) ÷ (1 − taxa − margem). Sobra por venda = preço × (1 − taxa) − custo total.</p>'},
  {title:'Pacote: '+s.t('pac_nome'),html:pac},
  {title:'Cenários de receita extra: Conservador, Intermediário e Otimista',html:cen+'<p class="za-small">Simulação com '+F.num(c.reservasBase)+' reservas/mês'+(c.reservasHip?' (base ilustrativa, não informada)':'')+'. Adesão '+(c.adesaoHip?'hipotética de 10%, 20% e 30%':'informada por você, com metade e 1,5 vez esse valor')+'. Não é previsão de vendas.</p>'},
  {title:'Apresentação comercial',html:(canais.length?'<p>Onde apresentar: '+canais.map(esc).join('; ')+'.</p>':'<p class="za-missing">Nenhum canal de apresentação escolhido.</p>')+msg}
 ],plan:plan};
}
});
})();
