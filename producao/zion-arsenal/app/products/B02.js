/* ZAR-B02 · Como Atrair um Sócio para Desenvolver Minha Terra? · Simulador de Sociedade e Parcerias */
(function(){
var F=ZA.fmt, esc=ZA.esc;
function tag(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';}
function arr(s,id){var x=s.v[id];return (!s.unknown(id)&&Array.isArray(x))?x:[];}
function has(a,v){return a.indexOf(v)>=0;}
function pct(x){return x==null?'—':F.pct(x*100,1);}
function rows(s,id){return arr(s,id).filter(function(r){return r&&ZA.isNum(r.value)&&r.value>0;});}

var RESP_OPTS=[{v:'prop',l:'Proprietário'},{v:'parc',l:'Parceiro'},{v:'ambos',l:'Ambos'},{v:'terceiro',l:'Terceiro contratado'},{v:'indef',l:'Ainda não definido'}];
var RESP=[{id:'resp_obra',n:'Obra e implantação'},{id:'resp_gestao',n:'Gestão da operação'},{id:'resp_financeiro',n:'Financeiro e contábil'},{id:'resp_comercial',n:'Vendas e marketing'},{id:'resp_docs',n:'Licenças e documentação'}];
var RISCOS=[{v:'doc',l:'Pendência documental ou ambiental atrasar o projeto',cl:'condicao',cn:'Condição prévia: regularização documental antes dos aportes'},
 {v:'orcamento',l:'Obra custar mais que o previsto',cl:'aportes',cn:'Regras para aportes adicionais e diluição'},
 {v:'decisao',l:'Divergência sobre decisões importantes',cl:'governanca',cn:'Governança: quem decide o quê e com qual quórum'},
 {v:'saida',l:'Uma das partes querer sair',cl:'saida',cn:'Regras de saída, preferência de compra e avaliação'},
 {v:'sucessao',l:'Falecimento ou incapacidade de uma das partes',cl:'sucessao',cn:'Sucessão e entrada de herdeiros'},
 {v:'desempenho',l:'Operação render menos que o esperado',cl:'resultados',cn:'Distribuição de resultados, metas e revisão'}];
var MOD={A:'Modelo A · todas as contribuições pelo valor cheio',B:'Modelo B · só terra e dinheiro',C:'Modelo C · terra com desconto de liquidez',arrendamento:'Arrendamento ou cessão de uso',permuta:'Permuta por unidades'};
var COMPAT={renda:{retorno:1,uso_pessoal:0.5,operar:1,diversificar:1,nao_sei:0.5},valorizacao:{retorno:0.5,uso_pessoal:0.5,operar:0.5,diversificar:1,nao_sei:0.5},gestao:{retorno:1,uso_pessoal:0.5,operar:0,diversificar:1,nao_sei:0.5},liquidez:{retorno:0.5,uso_pessoal:0.5,operar:0.5,diversificar:0.5,nao_sei:0.5}};

ZA.register({
id:'B02', code:'ZAR-B02', collection:'Terrenos',
title:'Como Atrair um Sócio para Desenvolver Minha Terra?',
subtitle:'Estruturar uma Proposta de Parceria',
tool:'Simulador de Sociedade e Parcerias',
deliverable:'Proposta Preliminar de Parceria',
nameField:'nome', propertyField:'propriedade',
disclaimer:'As participações calculadas são simulações orientativas feitas com valores informados por você; não são avaliação de imóvel, parecer jurídico, contábil ou tributário, nem garantem que um parceiro aceite a proposta ou que o projeto gere retorno. Qualquer sociedade, arrendamento ou permuta deve ser desenhada e revisada por advogado e contador antes de assinatura.',

intro:[
 {kind:'mirror', title:'Você tem a terra. Seu parceiro pode ter o capital. Como montar uma proposta que faça sentido para os dois?',
  lead:'Você já conversou com alguém interessado, ou imagina essa conversa. Mas quando chega a hora de falar em “quanto é de quem”, ninguém sabe por onde começar.',
  body:'<div class="za-card"><p>Situações comuns de quem chega até aqui:</p><ul><li>“Ele entra com o dinheiro e eu com a terra. Fica meio a meio?”</li><li>“Não sei quanto vale minha terra dentro de um projeto.”</li><li>“Eu vou trabalhar no dia a dia. Isso conta como contribuição?”</li><li>“Tenho medo de perder a terra se der errado.”</li></ul></div>'},
 {kind:'collapse', title:'Encontrar um parceiro não basta. É preciso uma proposta com contribuições, responsabilidades e expectativas claras.',
  lead:'Muitas parcerias não terminam por falta de dinheiro, mas por falta de clareza: quem colocou o quê, quem decide, quem faz o trabalho e o que acontece se alguém quiser sair.',
  body:'<div class="za-card"><p>Uma proposta de parceria madura responde a cinco perguntas:</p><ol><li><b>Quanto vale cada contribuição?</b> Terra, dinheiro, trabalho, projetos.</li><li><b>Quais são os objetivos de cada lado?</b> Renda, valorização, operação.</li><li><b>Qual formato faz sentido?</b> Sociedade, arrendamento, permuta.</li><li><b>Quem faz o quê?</b> Obra, gestão, financeiro, vendas, documentação.</li><li><b>O que acontece quando algo sai do plano?</b> Riscos e cláusulas.</li></ol><p>O Simulador calcula participações em modelos diferentes, para você negociar com números, não com palpites. O desenho final é sempre de advogado e contador.</p></div>'},
 {kind:'start', title:'Vamos estruturar a sua proposta de parceria',
  lead:'Em 7 pilares você valora as contribuições, compara modelos de participação, distribui responsabilidades e sai com uma proposta preliminar.',
  body:'<p>Tenha em mente: uma referência de valor da terra, quanto o parceiro poderia aportar e quanto tempo cada um dedicaria ao projeto. Se não souber algum dado, marque “não sei”.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Pedro'},
   {id:'propriedade',label:'Nome da terra ou do projeto',type:'text',required:true,placeholder:'Ex.: Chácara Bela Vista'},
   {id:'cidade',label:'Município e estado',type:'text',required:true,placeholder:'Ex.: Bueno Brandão (MG)'},
   {id:'parceiro_nome',label:'Nome ou perfil do parceiro (opcional)',type:'text',required:false,placeholder:'Ex.: investidor da região'},
   {id:'situacao',label:'Você já tem um parceiro em vista?',type:'radio',required:true,options:[{v:'em_vista',l:'Sim, já existe uma pessoa ou empresa interessada'},{v:'procurando',l:'Não, ainda estou procurando'}]}
  ]}
],

pillars:[
/* 1 */
{title:'O ativo', screens:[
 {kind:'learn', title:'Antes de dividir, saiba o que a terra representa no projeto',
  body:'<p>A terra costuma ser a maior contribuição do proprietário. Mas há uma diferença importante entre <b>colocar a terra no projeto</b> (ela passa a pertencer ao negócio) e <b>ceder apenas o direito de uso</b> por um prazo (ela continua sua). Cada caminho muda o risco e o valor da sua contribuição.</p><p>Três perguntas sobre o ativo:</p><ul><li><b>Quanto vale?</b> Laudo de avaliador é a referência mais sólida; opinião de corretor é intermediária; estimativa própria é a mais frágil.</li><li><b>Está regular?</b> Pendências documentais reduzem o valor percebido.</li><li><b>Entra a propriedade ou só o uso?</b></li></ul>',
  example:'Exemplo: uma terra estimada em R$ 800 mil pelo proprietário pode ser vista pelo parceiro como R$ 600 mil se não houver laudo e a matrícula tiver pendências. A diferença vira discussão de participação.'},
 {kind:'compare', title:'Propriedade no projeto × direito de uso',
  cols:[{h:'Terra entra no projeto',items:['A terra passa a ser do negócio (empresa ou condomínio)','Sua participação tende a ser maior','Se o projeto der errado, a terra está exposta','Exige cuidado societário e tributário']},
        {h:'Só o direito de uso',items:['A terra continua sua; o projeto usa por prazo','Contribuição menor, risco menor','Ao fim do prazo, benfeitorias precisam de regra','Contrato precisa prever renovação e saída']}],
  after:'<p class="za-small">Qual é melhor depende do seu objetivo. Os efeitos jurídicos e tributários devem ser avaliados com advogado e contador.</p>'},
 {kind:'form', title:'Seu ativo',
  fields:[
   {id:'valor_terra',label:'Valor de referência da terra',type:'money',required:true,allowUnknown:true,help:'Use o valor de um laudo ou de corretores da região, se tiver.'},
   {id:'valor_origem',label:'De onde vem esse valor?',type:'radio',required:true,options:[{v:'laudo',l:'Laudo de avaliador'},{v:'corretor',l:'Opinião de corretores da região'},{v:'estimativa',l:'Estimativa própria'}]},
   {id:'doc_status',label:'Situação da propriedade, pelo que você sabe',type:'radio',required:true,allowUnknown:true,options:[{v:'regular',l:'Matrícula em meu nome, sem pendência conhecida'},{v:'parcial',l:'Há algo a resolver (inventário, escritura, divisão)'},{v:'irregular',l:'Só posse ou contrato particular'}]},
   {id:'area_ha',label:'Área do terreno',type:'number',required:true,min:0.1,max:100000,step:'any',unit:'hectares'},
   {id:'uso_terra',label:'Como a terra entraria na parceria?',type:'radio',required:true,options:[{v:'propriedade',l:'A propriedade da terra (ou parte dela) entra no projeto'},{v:'uso',l:'Só o direito de uso, por prazo determinado'}]}
  ]},
 {kind:'feedback', title:'Força da sua principal contribuição',
  metrics:function(s,c){return [{label:'Valor de referência da terra',value:F.brl0(c.T),tag:s.t('valor_origem')==='laudo'?'informado':'estimativa'},{label:'Valor por hectare',value:F.brl0(c.T!=null?ZA.safeDiv(c.T,s.n('area_ha')):null),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.T==null) o.push({lv:'bad',t:'Sem valor de referência da terra, não é possível calcular participações. Peça a opinião de 2 ou 3 corretores da região ou contrate um avaliador.'});
   else if(s.t('valor_origem')==='estimativa') o.push({lv:'warn',t:'O valor é estimativa sua. O parceiro provavelmente vai questionar. Uma referência externa (corretores ou avaliador) evita que a negociação comece em desconfiança.'});
   else if(s.t('valor_origem')==='corretor') o.push({lv:'info',t:'Valor baseado em corretores: boa referência inicial. Para fechar participação, um laudo de avaliador tende a encerrar discussões.'});
   else o.push({lv:'ok',t:'Valor com laudo de avaliador: base sólida para negociar.'});
   if(s.unknown('doc_status')||s.t('doc_status')==='irregular') o.push({lv:'bad',t:'Situação da propriedade incerta ou sem registro. Antes de propor sociedade, procure um advogado: o parceiro não deve aportar sobre um ativo que não pode ser formalizado.'});
   else if(s.t('doc_status')==='parcial') o.push({lv:'warn',t:'Há pendência na propriedade. Uma saída comum é condicionar os aportes à regularização; o formato deve ser definido com advogado.'});
   if(s.t('uso_terra')==='uso') o.push({lv:'info',t:'Você prefere ceder só o uso. Isso protege a terra, mas o valor da sua contribuição deixa de ser o valor do imóvel inteiro; nos modelos, considere aplicar o desconto do Pilar 4.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Obter referência de valor da terra com corretores ou avaliador'},{id:'a1_2',text:'Atualizar a certidão de matrícula e levar a um advogado'},{id:'a1_3',text:'Decidir se ofereço a propriedade ou só o direito de uso'}]}
]},
/* 2 */
{title:'Objetivos dos parceiros', screens:[
 {kind:'learn', title:'Parcerias quebram quando os objetivos não combinam',
  body:'<p>Duas pessoas podem concordar com o projeto e discordar de tudo o que importa: <b>quando</b> esperam resultado, <b>o que</b> querem dele e <b>quem</b> vai trabalhar. Por isso, antes de falar em percentuais, compare objetivos.</p><p>O Simulador calcula um <b>índice de alinhamento</b> com três componentes:</p><ul><li><b>Horizonte (40 pontos):</b> quanto mais próximos os prazos de permanência, melhor.</li><li><b>Objetivos (30 pontos):</b> renda, valorização, gestão e liquidez combinam de formas diferentes com os objetivos do parceiro.</li><li><b>Envolvimento (30 pontos):</b> o ideal é que exatamente uma das partes opere; dois operadores tendem a disputar decisões, e nenhum exige contratar gestão.</li></ul>',
  example:'Exemplo: proprietário quer renda por 10 anos; investidor quer retorno e pensa em sair em 7. Diferença de 3 anos: o horizonte vale 40 × (1 − 3/10) = 28 pontos. Objetivos compatíveis (30) e só o proprietário opera (30): alinhamento 88/100.'},
 {kind:'compare', title:'Objetivos desalinhados × alinhados',
  cols:[{h:'Desalinhados',type:'bad',items:['Um quer reinvestir tudo; o outro quer distribuir lucro todo ano','Um pensa em 3 anos; o outro, em 20','Os dois querem mandar na operação','Ninguém quer operar']},
        {h:'Alinhados',type:'good',items:['Política de distribuição combinada desde o início','Horizontes parecidos ou regra de saída clara','Papéis complementares','Operação definida: um dos sócios ou gestor contratado']}]},
 {kind:'form', title:'Os objetivos de cada lado', intro:'Responda pelo parceiro com o que você sabe ou imagina. Se não souber, marque “não sei”: vale perguntar a ele.',
  fields:[
   {id:'obj_prop',label:'Seu principal objetivo',type:'radio',required:true,options:[{v:'renda',l:'Renda recorrente'},{v:'valorizacao',l:'Valorizar a terra no longo prazo'},{v:'gestao',l:'Gerir um negócio próprio'},{v:'liquidez',l:'Transformar parte da terra em dinheiro'}]},
   {id:'obj_parc',label:'Principal objetivo do parceiro',type:'radio',required:true,options:[{v:'retorno',l:'Retorno financeiro do capital'},{v:'uso_pessoal',l:'Uso pessoal / estilo de vida'},{v:'operar',l:'Operar o negócio'},{v:'diversificar',l:'Diversificar patrimônio'},{v:'nao_sei',l:'Não sei'}]},
   {id:'horiz_prop',label:'Por quantos anos você pretende ficar no projeto?',type:'number',required:true,min:1,max:50,step:1,unit:'anos'},
   {id:'horiz_parc',label:'Por quantos anos o parceiro pretende ficar?',type:'number',required:true,allowUnknown:true,min:1,max:50,step:1,unit:'anos'},
   {id:'envolv_prop',label:'Seu envolvimento na operação',type:'radio',required:true,options:[{v:'operar',l:'Quero operar no dia a dia'},{v:'acompanhar',l:'Quero acompanhar e decidir, sem operar'},{v:'nada',l:'Não quero me envolver'}]},
   {id:'envolv_parc',label:'Envolvimento do parceiro',type:'radio',required:true,options:[{v:'operar',l:'Quer operar no dia a dia'},{v:'acompanhar',l:'Quer acompanhar e decidir'},{v:'nada',l:'Só quer aportar'},{v:'nao_sei',l:'Não sei'}]}
  ]},
 {kind:'feedback', title:'Seu índice de alinhamento',
  metrics:function(s,c){return [{label:'Alinhamento',value:F.num(c.alinh,0)+'/100',tag:'calculado'},{label:'Horizonte',value:F.num(c.alH,0)+'/40',tag:'calculado'},{label:'Objetivos',value:F.num(c.alO,0)+'/30',tag:'calculado'},{label:'Envolvimento',value:F.num(c.alE,0)+'/30',tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.alinh>=75) o.push({lv:'ok',t:'Alinhamento de '+F.num(c.alinh,0)+'/100: boa base para conversar sobre números.'});
   else if(c.alinh>=50) o.push({lv:'warn',t:'Alinhamento de '+F.num(c.alinh,0)+'/100: há pontos a conversar antes de discutir percentuais.'});
   else o.push({lv:'bad',t:'Alinhamento de '+F.num(c.alinh,0)+'/100: há risco alto de conflito. Esclareça objetivos e papéis antes de avançar.'});
   if(s.unknown('horiz_parc')) o.push({lv:'warn',t:'Você não sabe por quanto tempo o parceiro quer ficar. Pergunte: é uma das informações mais importantes para desenhar a saída.'});
   else if(c.difH>=5) o.push({lv:'warn',t:'Diferença de '+F.num(c.difH)+' anos entre os horizontes. Será preciso uma regra de saída clara (quem compra a parte de quem, e por qual valor).'});
   if(s.t('envolv_prop')==='operar'&&s.t('envolv_parc')==='operar') o.push({lv:'bad',t:'Os dois querem operar. Defina já quem decide o quê no dia a dia; essa é uma das causas mais comuns de conflito.'});
   if(s.t('envolv_prop')!=='operar'&&s.t('envolv_parc')!=='operar'&&s.t('envolv_parc')!=='nao_sei') o.push({lv:'warn',t:'Ninguém pretende operar. O projeto vai precisar de gestor contratado, e esse custo deve entrar nas contas.'});
   if(s.t('obj_prop')==='gestao'&&s.t('obj_parc')==='operar') o.push({lv:'bad',t:'Você quer gerir e o parceiro quer operar: objetivos que competem pelo mesmo papel.'});
   if(s.t('obj_parc')==='nao_sei') o.push({lv:'warn',t:'Objetivo do parceiro desconhecido. Pergunte diretamente o que ele espera do projeto e em quanto tempo.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Perguntar ao parceiro, de forma direta, seu objetivo e prazo no projeto'},{id:'a2_2',text:'Combinar quem vai operar o dia a dia (ou se haverá gestor contratado)'},{id:'a2_3',text:'Conversar sobre política de distribuição de resultados antes dos percentuais'}]}
]},
/* 3 */
{title:'Contribuições', screens:[
 {kind:'learn', title:'Toda contribuição tem valor, e precisa ser medida da mesma forma',
  body:'<p>Num projeto de hospedagem, as partes costumam contribuir com coisas diferentes:</p><ul><li><b>Terra</b> (ou direito de uso): valor de referência do Pilar 1.</li><li><b>Dinheiro</b>: aporte de capital de cada parte.</li><li><b>Trabalho não remunerado</b> na implantação: horas por mês × valor da hora × meses. Use como valor da hora quanto custaria contratar alguém para fazer aquilo.</li><li><b>Outras contribuições</b>: projetos já pagos, equipamentos, estrada interna, licenças obtidas.</li></ul><p>Se o trabalho for remunerado por salário ou pró-labore, ele <b>não</b> entra como contribuição: já está sendo pago.</p>',
  example:'Exemplo: proprietário dedica 80 horas por mês durante 12 meses de implantação, a R$ 50/hora: 80 × 50 × 12 = R$ 48.000 de contribuição em trabalho.'},
 {kind:'compare', title:'Contribuições que costumam gerar discussão',
  cols:[{h:'Sem regra',type:'bad',items:['“Eu trabalhei muito” sem registro de horas','Equipamento usado avaliado pelo preço de novo','Dinheiro aportado sem recibo nem registro','Contribuição de “rede de contatos” sem valor combinado']},
        {h:'Com regra',type:'good',items:['Horas registradas e valor da hora combinado','Bens avaliados pelo valor atual','Aportes registrados e documentados','Contribuições intangíveis tratadas à parte ou com valor fixo combinado']}]},
 {kind:'form', title:'O que cada parte coloca',
  fields:[
   {id:'cap_parc',label:'Dinheiro que o parceiro aportaria',type:'money',required:true},
   {id:'cap_prop',label:'Dinheiro que você aportaria',type:'money',required:true,help:'Pode ser zero.'},
   {id:'horas_prop',label:'Suas horas por mês na implantação (sem remuneração)',type:'number',required:true,min:0,max:400,step:1,unit:'h/mês'},
   {id:'horas_parc',label:'Horas por mês do parceiro na implantação (sem remuneração)',type:'number',required:true,min:0,max:400,step:1,unit:'h/mês'},
   {id:'valor_hora',label:'Valor da hora de trabalho combinado',type:'money',required:true,help:'Quanto custaria contratar alguém para esse trabalho. Use o mesmo valor para os dois.'},
   {id:'meses_impl',label:'Meses de implantação',type:'number',required:true,min:1,max:60,step:1,unit:'meses'},
   {id:'outros_prop',label:'Outras contribuições suas (valor atual)',type:'list',required:false,preset:['Projetos ou estudos já pagos','Benfeitorias existentes (estrada, poço, energia)'],namePlaceholder:'Descrição',valuePlaceholder:'R$'},
   {id:'outros_parc',label:'Outras contribuições do parceiro (valor atual)',type:'list',required:false,preset:['Equipamentos ou materiais'],namePlaceholder:'Descrição',valuePlaceholder:'R$'}
  ]},
 {kind:'feedback', title:'Contribuições valoradas',
  metrics:function(s,c){return [{label:'Suas contribuições',value:F.brl0(c.contribP),tag:'calculado'},{label:'Contribuições do parceiro',value:F.brl0(c.contribI),tag:'calculado'},{label:'Seu trabalho valorado',value:F.brl0(c.trabP),tag:'calculado'},{label:'Trabalho do parceiro',value:F.brl0(c.trabI),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.T==null) o.push({lv:'warn',t:'Sem o valor da terra, só é possível somar dinheiro, trabalho e outras contribuições. A terra fica fora da conta até você ter uma referência.'});
   if(c.contribI<=0) o.push({lv:'warn',t:'O parceiro ainda não tem nenhuma contribuição informada. Sem saber o que ele coloca, não há divisão a calcular.'});
   if(c.T!=null&&c.contribI>0) o.push({lv:'info',t:'Somando tudo pelo valor cheio, você responde por '+pct(c.pA)+' do valor colocado no projeto e o parceiro por '+pct(c.pA==null?null:1-c.pA)+'. No próximo pilar você vê outros modelos.'});
   if(c.trabP>0&&c.contribP>0&&c.trabP/c.contribP>0.3) o.push({lv:'warn',t:'Seu trabalho representa '+F.pct(c.trabP/c.contribP*100,0)+' das suas contribuições. Combine como as horas serão registradas, ou isso vira discussão.'});
   if(s.n('valor_hora',0)===0&&(s.n('horas_prop',0)>0||s.n('horas_parc',0)>0)) o.push({lv:'warn',t:'Há horas informadas, mas o valor da hora é zero: o trabalho não está sendo considerado.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Combinar com o parceiro o valor da hora e como registrar as horas'},{id:'a3_2',text:'Listar e documentar as benfeitorias e projetos que já existem'},{id:'a3_3',text:'Registrar todo aporte de dinheiro com comprovante'}]}
]},
/* 4 */
{title:'Modalidades de parceria', screens:[
 {kind:'learn', title:'O mesmo projeto, cinco formas de dividir',
  body:'<p>O Simulador compara cinco formas de remunerar as contribuições. Nenhuma é “a certa”: cada uma reflete uma visão diferente sobre risco e valor.</p><ul><li><b>Modelo A · valor cheio:</b> participação proporcional a tudo o que cada um colocou (terra, dinheiro, trabalho, outros).</li><li><b>Modelo B · terra e dinheiro:</b> só ativos e capital contam; trabalho é remunerado à parte.</li><li><b>Modelo C · terra com desconto:</b> como o A, mas a terra entra com um desconto de liquidez, porque ela não é dinheiro disponível para a obra. O percentual é negociado.</li><li><b>Arrendamento:</b> o operador paga um valor mensal pelo uso; você não participa do resultado.</li><li><b>Permuta:</b> você recebe unidades prontas em troca da área.</li></ul>',
  example:'Exemplo: terra de R$ 800 mil com desconto de 20% entra como R$ 640 mil no Modelo C. Num arrendamento de R$ 4.000 por mês, a renda anual equivale a 6% do valor da terra (48.000 ÷ 800.000).'},
 {kind:'compare', title:'Sociedade × arrendamento × permuta',
  cols:[{h:'Sociedade (A, B, C)',items:['Você participa do resultado e do risco','Precisa de regras de governança e saída','Participação depende de como a terra é valorada']},
        {h:'Arrendamento e permuta',items:['Arrendamento: renda definida em contrato, sem risco da operação, sem ganho extra','Permuta: você recebe unidades e pode explorá-las ou vendê-las','Ambos exigem contrato bem desenhado sobre prazos e benfeitorias']}]},
 {kind:'form', title:'Parâmetros das modalidades',
  fields:[
   {id:'desconto_terra',label:'Desconto de liquidez aplicado à terra no Modelo C',type:'percent',required:true,max:60,help:'Valor negociado. 0% = terra pelo valor cheio. Quanto mais incerto o ativo (documentação, acesso), maior o desconto que o parceiro tende a pedir.'},
   {id:'arrend_mensal',label:'Valor mensal de arrendamento que você pediria (ou que lhe ofereceram)',type:'money',required:true,allowUnknown:true},
   {id:'unid_total',label:'Quantas unidades o projeto teria no total',type:'number',required:true,allowUnknown:true,min:1,max:500,step:1,unit:'unidades'},
   {id:'unid_permuta',label:'Quantas unidades você receberia numa permuta',type:'number',required:true,allowUnknown:true,min:0,max:500,step:1,unit:'unidades',validate:function(v,s){var t=s.n('unid_total');return (t!=null&&v>t)?'Não pode passar do total de unidades.':'';}}
  ]},
 {kind:'feedback', title:'As cinco modalidades lado a lado',
  metrics:function(s,c){return [{label:'Modelo A (valor cheio)',value:pct(c.pA),tag:'calculado'},{label:'Modelo B (terra e dinheiro)',value:pct(c.pB),tag:'calculado'},{label:'Modelo C (terra com desconto)',value:pct(c.pC),tag:'calculado'},{label:'Arrendamento: renda anual / valor da terra',value:pct(c.yArr),tag:'calculado'},{label:'Permuta: unidades recebidas',value:pct(c.pPerm),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.pA==null) o.push({lv:'warn',t:'Faltam o valor da terra ou as contribuições do parceiro para calcular as participações.'});
   else{ var mx=Math.max(c.pA,c.pB==null?0:c.pB,c.pC), mn=Math.min(c.pA,c.pB==null?1:c.pB,c.pC);
     o.push({lv:'info',t:'Sua participação varia de '+pct(mn)+' a '+pct(mx)+' conforme o modelo. Essa faixa é o seu espaço de negociação.'});
     if(c.pA-c.pC>0.05) o.push({lv:'info',t:'O desconto de liquidez reduz sua participação em '+F.num((c.pA-c.pC)*100,1)+' pontos percentuais. Documentação organizada e laudo de avaliação são argumentos para negociar um desconto menor.'});}
   if(c.yArr!=null) o.push({lv:'info',t:'O arrendamento proposto gera '+F.brl0(c.arrAnual)+' por ano, equivalente a '+pct(c.yArr)+' do valor de referência da terra. Compare com o que você esperaria receber como sócio, lembrando que no arrendamento você não corre o risco da operação.'});
   if(c.pPerm!=null&&c.pA!=null) o.push({lv:c.pPerm<c.pA-0.1?'warn':'info',t:'Na permuta você ficaria com '+pct(c.pPerm)+' das unidades, contra '+pct(c.pA)+' de participação no Modelo A.'+(c.pPerm<c.pA-0.1?' A permuta parece desfavorável a você com esses números.':'')});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Escolher o modelo mais coerente com meus objetivos para levar à conversa'},{id:'a4_2',text:'Preparar argumentos (documentos, laudo) para reduzir o desconto da terra'},{id:'a4_3',text:'Pedir a um contador que compare os efeitos tributários de sociedade, arrendamento e permuta'}]}
]},
/* 5 */
{title:'Participações e responsabilidades', screens:[
 {kind:'learn', title:'Participação é sobre o que se colocou. Responsabilidade é sobre o que se faz.',
  body:'<p>Uma divisão 50/50 de capital pode esconder uma divisão 90/10 de trabalho. Por isso, além do percentual, a proposta precisa de uma <b>matriz de responsabilidades</b>: quem cuida da obra, da gestão, do financeiro, das vendas e da documentação.</p><p>Duas regras práticas:</p><ul><li>Toda área precisa de <b>um</b> responsável, mesmo que as decisões grandes sejam conjuntas.</li><li>Defina antes a sua <b>participação desejada</b> e a <b>mínima aceitável</b>. Abaixo da mínima, você tem uma alternativa melhor (Pilar 6).</li></ul>',
  example:'Exemplo: participação desejada 60%, mínima 45%. Se o modelo escolhido resulta em 54%, você está dentro da faixa e pode negociar o restante com responsabilidades e regras de distribuição.'},
 {kind:'compare', title:'Responsabilidades difusas × claras',
  cols:[{h:'Difusas',type:'bad',items:['“A gente vê junto”','Os dois aprovam cada compra','Ninguém responde pelas licenças','Marketing “quando der”']},
        {h:'Claras',type:'good',items:['Um responsável por área','Alçada de valor para decisões do dia a dia','Decisões grandes com quórum definido','Prestação de contas periódica']}]},
 {kind:'form', title:'Sua faixa de participação e a matriz de responsabilidades',
  fields:[
   {id:'part_desejada',label:'Participação que você deseja',type:'percent',required:true,min:1,max:100},
   {id:'part_minima',label:'Participação mínima aceitável',type:'percent',required:true,min:0,max:100,validate:function(v,s){var d=s.n('part_desejada');return (d!=null&&v>d)?'A mínima não pode ser maior que a desejada.':'';}},
   {id:'resp_obra',label:'Obra e implantação',type:'radio',required:true,options:RESP_OPTS},
   {id:'resp_gestao',label:'Gestão da operação',type:'radio',required:true,options:RESP_OPTS},
   {id:'resp_financeiro',label:'Financeiro e contábil',type:'radio',required:true,options:RESP_OPTS},
   {id:'resp_comercial',label:'Vendas e marketing',type:'radio',required:true,options:RESP_OPTS},
   {id:'resp_docs',label:'Licenças e documentação',type:'radio',required:true,options:RESP_OPTS}
  ]},
 {kind:'feedback', title:'Sua faixa e o equilíbrio de tarefas',
  metrics:function(s,c){return [{label:'Áreas sem responsável',value:c.nIndef+' de 5',tag:'calculado'},{label:'Áreas suas',value:String(c.nProp),tag:'calculado'},{label:'Áreas do parceiro',value:String(c.nParc),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.nIndef>0) o.push({lv:c.nIndef>=3?'bad':'warn',t:c.nIndef+' área(s) sem responsável definido: '+c.indefNomes.join(', ')+'.'});
   else o.push({lv:'ok',t:'Todas as áreas têm responsável.'});
   if(c.nAmbos>=3) o.push({lv:'warn',t:'Muitas áreas marcadas como “ambos”. Na prática, isso costuma significar “ninguém”. Escolha um responsável e deixe o outro como apoio.'});
   if(c.nProp>=4&&c.pA!=null&&c.pA<0.5) o.push({lv:'warn',t:'Você assume '+c.nProp+' das 5 áreas, mas teria menos da metade do projeto. Considere remuneração pela gestão ou ajuste na participação.'});
   if(c.pA!=null){var mx=Math.max(c.pA,c.pB||0,c.pC);
     if(mx*100<s.n('part_minima',0)) o.push({lv:'bad',t:'Nenhum modelo de sociedade chega à sua participação mínima ('+F.pct(s.n('part_minima'),0)+'). Reveja a expectativa, aumente sua contribuição ou considere arrendamento/permuta.'});
     else if(mx*100<s.n('part_desejada',0)) o.push({lv:'info',t:'Sua participação desejada ('+F.pct(s.n('part_desejada'),0)+') fica acima de todos os modelos; o melhor chega a '+pct(mx)+'. A diferença precisa ser negociada com argumentos, não com insistência.'});
     else o.push({lv:'ok',t:'Pelo menos um modelo alcança a sua participação desejada.'});}
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Definir um único responsável para cada área'},{id:'a5_2',text:'Combinar a alçada de decisões do dia a dia e o que exige decisão conjunta'},{id:'a5_3',text:'Guardar para mim a participação mínima aceitável antes de negociar'}]}
]},
/* 6 */
{title:'Riscos e negociação', screens:[
 {kind:'learn', title:'Toda parceria precisa de um plano para quando as coisas saem do plano',
  body:'<p>Os riscos mais comuns em parcerias de terra e hospedagem são previsíveis. A proteção é combinar <b>antes</b> o que acontece em cada caso. A ferramenta liga cada risco a um tipo de cláusula:</p><ul>'+RISCOS.map(function(r){return '<li><b>'+r.l+'</b> → '+r.cn+'</li>';}).join('')+'</ul><p>E, para negociar bem, defina sua <b>melhor alternativa</b> caso o acordo não saia. Quem não tem alternativa aceita qualquer proposta.</p><p class="za-small">A redação de cláusulas é trabalho de advogado. Aqui você só mapeia o que precisa ser tratado.</p>',
  example:'Exemplo: você identificou “obra custar mais que o previsto”, mas não pensou em regra para aportes adicionais. Se faltar dinheiro, quem coloca? E a participação muda? Essa é uma lacuna a levar ao advogado.'},
 {kind:'compare', title:'Negociar sem e com alternativa',
  cols:[{h:'Sem alternativa',type:'bad',items:['Aceitar a primeira proposta por medo de perder o parceiro','Ceder participação sem contrapartida','Assinar sem ler com assessoria']},
        {h:'Com alternativa',type:'good',items:['Saber o que fará se não houver acordo (esperar, arrendar, começar pequeno)','Negociar entre a participação desejada e a mínima','Levar a minuta ao advogado antes de assinar']}]},
 {kind:'form', title:'Seus riscos e as proteções pensadas',
  fields:[
   {id:'riscos',label:'Riscos que você enxerga neste projeto',type:'checks',options:RISCOS.map(function(r){return {v:r.v,l:r.l};})},
   {id:'clausulas',label:'Temas que você já pretende tratar no acordo',type:'checks',options:RISCOS.map(function(r){return {v:r.cl,l:r.cn};})},
   {id:'alternativa',label:'Se o acordo não sair, qual é sua melhor alternativa?',type:'radio',required:true,options:[{v:'outro_parceiro',l:'Procurar outro parceiro'},{v:'arrendar',l:'Arrendar a área a um operador'},{v:'progressivo',l:'Começar pequeno, com recursos próprios'},{v:'esperar',l:'Esperar e manter a terra como está'},{v:'nenhuma',l:'Não tenho alternativa'}]}
  ]},
 {kind:'feedback', title:'Cobertura dos riscos',
  metrics:function(s,c){return [{label:'Riscos identificados',value:String(c.nRiscos),tag:'informado'},{label:'Cobertura por cláusulas',value:c.cobertura==null?'—':F.pct(c.cobertura*100,0),tag:'calculado'},{label:'Riscos sem proteção',value:String(c.descobertos.length),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.nRiscos===0) o.push({lv:'warn',t:'Nenhum risco identificado. Todo projeto tem riscos; volte à lista e marque os que se aplicam ao seu caso.'});
   else if(c.descobertos.length) o.push({lv:'warn',t:'Riscos sem tema de proteção: '+c.descobertos.map(function(r){return '<b>'+r.l+'</b> (falta: '+r.cn.toLowerCase()+')';}).join('; ')+'.'});
   else o.push({lv:'ok',t:'Todos os riscos identificados têm um tema de proteção previsto. Leve a lista ao advogado.'});
   if(!has(c.riscos,'sucessao')) o.push({lv:'info',t:'Sucessão costuma ser esquecida. Em projetos longos, vale prever o que acontece se uma das partes faltar.'});
   if(s.t('alternativa')==='nenhuma') o.push({lv:'bad',t:'Sem alternativa, sua posição de negociação é fraca. Mesmo “começar pequeno” ou “arrendar” já é uma alternativa a considerar.'});
   if((s.unknown('doc_status')||s.t('doc_status')!=='regular')&&!has(c.claus,'condicao')) o.push({lv:'warn',t:'Há incerteza documental e nenhuma condição prévia prevista. Peça ao advogado para avaliar condicionar aportes à regularização.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Levar a lista de riscos e temas de proteção a um advogado'},{id:'a6_2',text:'Definir minha melhor alternativa caso o acordo não saia'},{id:'a6_3',text:'Não assinar nenhum documento, nem carta de intenções, sem revisão jurídica'}]}
]},
/* 7 */
{title:'Proposta preliminar', screens:[
 {kind:'learn', title:'Da simulação à proposta: um documento para abrir a conversa',
  body:'<p>A proposta preliminar não é contrato. É um documento de <b>uma ou duas páginas</b> que organiza a conversa: o ativo, as contribuições, o modelo de participação sugerido, as responsabilidades, a distribuição de resultados, o prazo e os temas que o acordo final precisa tratar.</p><p>Formas comuns de distribuir resultados:</p><ul><li><b>Proporcional:</b> cada um recebe conforme a participação.</li><li><b>Preferencial:</b> o investidor recebe primeiro até recuperar o aporte; depois, proporcional.</li><li><b>Fixo + variável:</b> uma parte fixa para quem opera, o restante proporcional.</li></ul>',
  example:'Exemplo: “Proposta preliminar: Modelo C, participação de 54% do proprietário e 46% do parceiro; obra sob responsabilidade do parceiro, gestão com o proprietário; distribuição proporcional; prazo de 10 anos; temas a tratar com advogado: aportes adicionais e regras de saída.”'},
 {kind:'compare', title:'Proposta que trava × proposta que avança',
  cols:[{h:'Trava',type:'bad',items:['Só o percentual, sem justificativa','Tom de “pegar ou largar”','Nada sobre saída e riscos']},
        {h:'Avança',type:'good',items:['Percentual explicado pelas contribuições','Faixa e alternativas abertas à conversa','Temas sensíveis listados para o advogado']}]},
 {kind:'form', title:'Monte sua proposta',
  fields:[
   {id:'modelo_escolhido',label:'Modelo que você vai propor',type:'radio',required:true,options:[{v:'A',l:MOD.A},{v:'B',l:MOD.B},{v:'C',l:MOD.C},{v:'arrendamento',l:MOD.arrendamento},{v:'permuta',l:MOD.permuta}]},
   {id:'prazo_anos',label:'Prazo inicial do acordo',type:'number',required:true,min:1,max:99,step:1,unit:'anos'},
   {id:'distribuicao',label:'Distribuição de resultados (se for sociedade)',type:'radio',required:true,options:[{v:'proporcional',l:'Proporcional à participação'},{v:'preferencial',l:'Preferencial ao investidor até recuperar o aporte'},{v:'fixo_variavel',l:'Fixo para quem opera + variável proporcional'}]}
  ]},
 {kind:'feedback', title:'Sua proposta, conferida',
  metrics:function(s,c){return [{label:'Modelo proposto',value:MOD[s.t('modelo_escolhido')]?MOD[s.t('modelo_escolhido')].split(' · ')[0]:'—',tag:'informado'},{label:c.propTipo==='renda'?'Renda anual proposta':'Sua participação proposta',value:c.propTipo==='renda'?F.brl0(c.arrAnual):pct(c.pProp),tag:'calculado'},{label:'Alinhamento',value:F.num(c.alinh,0)+'/100',tag:'calculado'}];},
  feedback:function(s,c){var o=[];var m=s.t('modelo_escolhido');
   if(c.propTipo==='renda'){ if(c.arrAnual==null) o.push({lv:'warn',t:'Você escolheu arrendamento, mas não informou o valor mensal. Pesquise quanto operadores pagam por áreas parecidas.'});
     else o.push({lv:'info',t:'Proposta de arrendamento: '+F.brl0(c.arrAnual)+' por ano por '+F.num(s.n('prazo_anos'))+' anos ('+F.brl0(c.arrAnual*s.n('prazo_anos',0))+' no prazo, sem correção). Defina com advogado como ficam as benfeitorias ao fim do contrato.'});}
   else if(c.pProp==null) o.push({lv:'warn',t:'Faltam dados para calcular a participação do modelo escolhido.'});
   else{var d=c.pProp*100-s.n('part_desejada',0), mi=s.n('part_minima',0);
     if(c.pProp*100<mi) o.push({lv:'bad',t:'O modelo escolhido dá '+pct(c.pProp)+', abaixo da sua mínima ('+F.pct(mi,0)+'). Reveja o modelo ou a sua expectativa antes de apresentar.'});
     else if(d<0) o.push({lv:'info',t:'O modelo escolhido dá '+pct(c.pProp)+', '+F.num(-d,1)+' p.p. abaixo do desejado e acima da mínima: dentro da sua faixa de negociação.'});
     else o.push({lv:'ok',t:'O modelo escolhido dá '+pct(c.pProp)+', igual ou acima da participação desejada. Prepare-se para justificar esse número com as contribuições.'});}
   if(m==='B'&&c.trabP>0) o.push({lv:'info',t:'No Modelo B o trabalho não entra na participação. Combine remuneração (pró-labore) para quem vai trabalhar na implantação.'});
   if(s.t('distribuicao')==='preferencial') o.push({lv:'info',t:'Distribuição preferencial costuma tornar a proposta mais atraente para o investidor, mas você recebe mais tarde. Simule o efeito com um contador.'});
   if(c.alinh<50) o.push({lv:'warn',t:'O alinhamento de objetivos está baixo. Resolva essa conversa antes de apresentar a proposta.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Enviar a proposta preliminar ao parceiro como base de conversa, não como contrato'},{id:'a7_2',text:'Marcar uma reunião com advogado e contador para desenhar o acordo final'},{id:'a7_3',text:'Revisar a proposta depois da primeira conversa e refazer a simulação'}]}
]}
],

compute:function(s){
 var c={};
 c.T=s.n('valor_terra');
 // alinhamento
 var hp=s.n('horiz_prop',0), hq=s.n('horiz_parc');
 c.difH=hq==null?null:Math.abs(hp-hq);
 c.alH=40*(hq==null?0.5:Math.max(0,1-c.difH/10));
 c.alO=30*(((COMPAT[s.t('obj_prop')]||{})[s.t('obj_parc')])!=null?COMPAT[s.t('obj_prop')][s.t('obj_parc')]:0.5);
 var ep=s.t('envolv_prop'), eq=s.t('envolv_parc');
 var env=eq==='nao_sei'?0.5:(ep==='operar'&&eq==='operar')?0:(ep==='operar'||eq==='operar')?1:0.5;
 c.alE=30*env; c.alinh=c.alH+c.alO+c.alE;
 // contribuições
 var vh=s.n('valor_hora',0), mm=s.n('meses_impl',0);
 c.trabP=s.n('horas_prop',0)*vh*mm; c.trabI=s.n('horas_parc',0)*vh*mm;
 c.outP=ZA.listSum(rows(s,'outros_prop')); c.outI=ZA.listSum(rows(s,'outros_parc'));
 c.capP=s.n('cap_prop',0); c.capI=s.n('cap_parc',0);
 c.contribP=(c.T||0)+c.capP+c.trabP+c.outP; c.contribI=c.capI+c.trabI+c.outI;
 c.totalA=c.contribP+c.contribI;
 var ok=c.T!=null&&c.contribI>0;
 c.pA=ok?c.contribP/c.totalA:null;
 c.pB=(ok&&(c.T+c.capP+c.capI)>0&&c.capI>0)?(c.T+c.capP)/(c.T+c.capP+c.capI):null;
 c.d=s.n('desconto_terra',0)/100; c.Td=c.T!=null?c.T*(1-c.d):null;
 var pC=ok?(c.Td+c.capP+c.trabP+c.outP):null; c.pC=ok?pC/(pC+c.contribI):null;
 var am=s.n('arrend_mensal'); c.arrAnual=am!=null?am*12:null;
 c.yArr=(c.arrAnual!=null&&c.T)?c.arrAnual/c.T:null;
 var ut=s.n('unid_total'), up=s.n('unid_permuta'); c.pPerm=(ut&&up!=null)?up/ut:null;
 // responsabilidades
 var R=RESP.map(function(r){return {n:r.n,v:s.t(r.id)};});
 c.nIndef=R.filter(function(r){return r.v==='indef'||!r.v;}).length; c.indefNomes=R.filter(function(r){return r.v==='indef'||!r.v;}).map(function(r){return r.n;});
 c.nProp=R.filter(function(r){return r.v==='prop';}).length; c.nParc=R.filter(function(r){return r.v==='parc';}).length; c.nAmbos=R.filter(function(r){return r.v==='ambos';}).length;
 c.resp=R;
 // riscos
 c.riscos=arr(s,'riscos'); c.claus=arr(s,'clausulas');
 var ident=RISCOS.filter(function(r){return has(c.riscos,r.v);});
 c.nRiscos=ident.length; c.descobertos=ident.filter(function(r){return !has(c.claus,r.cl);});
 c.cobertura=c.nRiscos?(c.nRiscos-c.descobertos.length)/c.nRiscos:null;
 // proposta
 var m=s.t('modelo_escolhido');
 c.propTipo=m==='arrendamento'?'renda':m==='permuta'?'permuta':'sociedade';
 c.pProp={A:c.pA,B:c.pB,C:c.pC,permuta:c.pPerm}[m]; if(c.pProp===undefined) c.pProp=null;
 return c;
},

metrics:function(s,c){return [
 {label:'Valor de referência da terra',value:F.brl0(c.T),tag:s.t('valor_origem')==='laudo'?'informado':'estimativa'},
 {label:'Suas contribuições (valor cheio)',value:F.brl0(c.contribP),tag:'calculado'},
 {label:'Contribuições do parceiro',value:F.brl0(c.contribI),tag:'calculado'},
 {label:'Participação · Modelo A',value:pct(c.pA),tag:'calculado'},
 {label:'Participação · Modelo C',value:pct(c.pC),tag:'calculado'},
 {label:'Alinhamento de objetivos',value:F.num(c.alinh,0)+'/100',tag:'calculado'},
 {label:'Áreas sem responsável',value:c.nIndef+' de 5',tag:'calculado'},
 {label:'Cobertura de riscos',value:c.cobertura==null?'—':F.pct(c.cobertura*100,0),tag:'calculado'}
];},

priorities:function(s,c){var L=[];
 if(c.T==null) L.push({title:'Obter um valor de referência da terra',why:'Sem ele não há como calcular participação.',score:10});
 else if(s.t('valor_origem')==='estimativa') L.push({title:'Substituir a estimativa própria por referência de corretores ou laudo',why:'Valor sem referência externa abre a negociação em desconfiança.',score:6});
 if(s.unknown('doc_status')||s.t('doc_status')==='irregular') L.push({title:'Esclarecer a situação da propriedade com advogado antes de propor sociedade',why:'Parceiro não deve aportar sobre ativo que não pode ser formalizado.',score:9});
 else if(s.t('doc_status')==='parcial') L.push({title:'Definir com advogado se os aportes ficam condicionados à regularização',why:'Há pendência documental na terra.',score:7});
 if(c.contribI<=0) L.push({title:'Definir o que o parceiro vai aportar',why:'Sem contribuição do parceiro não há divisão a negociar.',score:8});
 if(c.alinh<50) L.push({title:'Alinhar objetivos, prazos e papéis com o parceiro antes dos percentuais',why:'Alinhamento de '+F.num(c.alinh,0)+'/100.',score:8});
 else if(c.alinh<75) L.push({title:'Conversar sobre os pontos de desalinhamento',why:'Alinhamento de '+F.num(c.alinh,0)+'/100.',score:5});
 if(s.unknown('horiz_parc')||s.t('obj_parc')==='nao_sei') L.push({title:'Perguntar ao parceiro objetivo e prazo de permanência',why:'Informação essencial para regras de saída.',score:6});
 if(s.t('envolv_prop')==='operar'&&s.t('envolv_parc')==='operar') L.push({title:'Definir quem opera o dia a dia',why:'As duas partes querem operar.',score:7});
 if(c.nIndef>0) L.push({title:'Definir responsável para '+c.indefNomes.join(', '),why:c.nIndef+' área(s) sem dono.',score:c.nIndef>=3?7:5});
 if(c.descobertos.length) L.push({title:'Levar ao advogado: '+c.descobertos.map(function(r){return r.cn.split(':')[0].toLowerCase();}).join('; '),why:c.descobertos.length+' risco(s) sem tema de proteção.',score:6});
 if(c.nRiscos===0) L.push({title:'Mapear os riscos do projeto',why:'Nenhum risco identificado.',score:5});
 if(s.t('alternativa')==='nenhuma') L.push({title:'Construir uma alternativa ao acordo (arrendar, começar pequeno, outro parceiro)',why:'Sem alternativa, a negociação fica fraca.',score:6});
 if(c.pProp!=null&&c.pProp*100<s.n('part_minima',0)) L.push({title:'Rever o modelo proposto ou a expectativa de participação',why:'O modelo escolhido fica abaixo da sua mínima.',score:8});
 if(c.pA!=null&&c.pA-c.pC>0.05) L.push({title:'Reunir argumentos para reduzir o desconto da terra',why:'O desconto tira '+F.num((c.pA-c.pC)*100,1)+' p.p. da sua participação.',score:4});
 L.push({title:'Validar o formato com advogado e contador antes de qualquer assinatura',why:'Sociedade, arrendamento e permuta têm efeitos jurídicos e tributários diferentes.',score:5});
 return L;},

report:function(s,c){
 var contrib=ZA.table(['Contribuição','Você','Parceiro'],[
  ['Terra (valor de referência)',F.brl0(c.T),'—'],['Dinheiro',F.brl0(c.capP),F.brl0(c.capI)],
  ['Trabalho na implantação',F.brl0(c.trabP),F.brl0(c.trabI)],['Outras contribuições',F.brl0(c.outP),F.brl0(c.outI)],
  ['<b>Total (valor cheio)</b>','<b>'+F.brl0(c.contribP)+'</b>','<b>'+F.brl0(c.contribI)+'</b>']],[1,2]);
 var mods=ZA.table(['Modalidade','Você','Parceiro','Leitura'],[
  [MOD.A,pct(c.pA),pct(c.pA==null?null:1-c.pA),'Tudo conta pelo valor informado'],
  [MOD.B,pct(c.pB),pct(c.pB==null?null:1-c.pB),'Trabalho remunerado à parte'],
  [MOD.C+' ('+F.pct(c.d*100,0)+')',pct(c.pC),pct(c.pC==null?null:1-c.pC),'Reconhece que a terra não é dinheiro disponível'],
  [MOD.arrendamento,c.arrAnual==null?'—':F.brl0(c.arrAnual)+'/ano','Operação e resultado',c.yArr==null?'—':'Renda anual = '+pct(c.yArr)+' do valor da terra'],
  [MOD.permuta,pct(c.pPerm),pct(c.pPerm==null?null:1-c.pPerm),'Percentual das unidades']],[1,2]);
 var resp=ZA.table(['Área','Responsável'],c.resp.map(function(r){return [esc(r.n),esc(({prop:'Proprietário',parc:'Parceiro',ambos:'Ambos',terceiro:'Terceiro contratado',indef:'A definir'})[r.v]||'A definir')];}));
 var riscos=c.nRiscos?ZA.table(['Risco identificado','Tema de proteção','Situação'],RISCOS.filter(function(r){return has(c.riscos,r.v);}).map(function(r){return [esc(r.l),esc(r.cn),has(c.claus,r.cl)?'previsto':'<b>lacuna</b>'];})):'<p class="za-missing">Nenhum risco identificado. Revise o Pilar 6.</p>';
 var m=s.t('modelo_escolhido'), pn=s.t('parceiro_nome')?esc(s.t('parceiro_nome')):'o parceiro';
 var dist={proporcional:'proporcional à participação',preferencial:'preferencial ao investidor até a recuperação do aporte e, depois, proporcional',fixo_variavel:'parcela fixa para quem opera e o restante proporcional à participação'}[s.t('distribuicao')]||'a definir';
 var corpo=c.propTipo==='renda'?'<p>Proposta de <b>arrendamento ou cessão de uso</b> de <b>'+esc(s.t('propriedade'))+'</b> ('+F.num(s.n('area_ha'),1)+' ha, '+esc(s.t('cidade'))+') a '+pn+', por '+F.num(s.n('prazo_anos'))+' anos, com valor mensal de '+F.brl0(s.n('arrend_mensal'))+'. O operador assume a implantação e a operação.</p>'
  :c.propTipo==='permuta'?'<p>Proposta de <b>permuta</b>: cessão de área de <b>'+esc(s.t('propriedade'))+'</b> a '+pn+' em troca de '+F.num(s.n('unid_permuta'))+' de '+F.num(s.n('unid_total'))+' unidades do projeto ('+pct(c.pPerm)+').</p>'
  :'<p>Proposta de <b>parceria societária</b> para desenvolver <b>'+esc(s.t('propriedade'))+'</b> ('+F.num(s.n('area_ha'),1)+' ha, '+esc(s.t('cidade'))+') com '+pn+'. Base de participação: <b>'+esc(MOD[m]||'')+'</b>, resultando em <b>'+pct(c.pProp)+'</b> para o proprietário e <b>'+pct(c.pProp==null?null:1-c.pProp)+'</b> para o parceiro, conforme as contribuições valoradas acima. Distribuição de resultados: '+dist+'. Prazo inicial: '+F.num(s.n('prazo_anos'))+' anos. A terra entra '+(s.t('uso_terra')==='uso'?'como <b>direito de uso por prazo determinado</b>':'como <b>propriedade</b> no projeto')+'.</p>';
 var prop='<div class="za-card"><b>Proposta preliminar (rascunho para conversa)</b>'+corpo+'<p>Temas a tratar no acordo final, com advogado e contador: '+(c.descobertos.length?c.descobertos.map(function(r){return esc(r.cn.split(':')[0].toLowerCase());}).join('; ')+'; ':'')+'governança e quórum; regras de saída; sucessão; aportes adicionais.</p><p class="za-small">Este texto não é contrato nem oferta vinculante. Ele organiza a conversa.</p></div>';
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Valor de referência da terra',F.brl0(c.T),c.T==null?tag('hipotese','ausente'):tag(s.t('valor_origem')==='laudo'?'informado':'estimativa',{laudo:'laudo',corretor:'corretores',estimativa:'estimativa própria'}[s.t('valor_origem')])],
  ['Valor da hora de trabalho',F.brl(s.n('valor_hora')),tag('informado','combinado')],
  ['Meses de implantação',F.num(s.n('meses_impl')),tag('informado')],
  ['Desconto de liquidez da terra (Modelo C)',F.pct(c.d*100,0),tag('informado','negociado')],
  ['Arrendamento mensal',F.brl0(s.n('arrend_mensal')),s.unknown('arrend_mensal')?tag('hipotese','ausente'):tag('informado')],
  ['Unidades totais / em permuta',F.num(s.n('unid_total'))+' / '+F.num(s.n('unid_permuta')),(s.unknown('unid_total')||s.unknown('unid_permuta'))?tag('hipotese','ausente'):tag('informado')],
  ['Horizonte do parceiro',s.unknown('horiz_parc')?'—':F.num(s.n('horiz_parc'))+' anos',s.unknown('horiz_parc')?tag('hipotese','neutro (20/40)'):tag('informado')],
  ['Pesos do alinhamento','horizonte 40 · objetivos 30 · envolvimento 30',tag('recomendacao','metodologia Zion')]],[1]);
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido de 30 dias</b><ol><li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Revisar os dados da simulação')+'.</li><li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Conversar com o parceiro sobre objetivos')+'.</li><li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Reunião com advogado e contador')+'.</li><li><b>Semana 4:</b> apresentar a proposta preliminar como base de conversa, registrar as objeções e refazer a simulação com os novos números.</li></ol></div>';
 return {sections:[
  {title:'Contribuições valoradas',html:contrib},
  {title:'Simulação de participações',html:mods+'<p>Sua faixa de negociação: desejada '+F.pct(s.n('part_desejada'),0)+' · mínima '+F.pct(s.n('part_minima'),0)+'.</p><p class="za-small">Simulações orientativas. A participação final depende de negociação, avaliação do ativo e do formato jurídico escolhido.</p>'},
  {title:'Alinhamento de objetivos',html:ZA.table(['Componente','Pontos'],[['Horizonte',F.num(c.alH,0)+'/40'],['Objetivos',F.num(c.alO,0)+'/30'],['Envolvimento',F.num(c.alE,0)+'/30'],['<b>Total</b>','<b>'+F.num(c.alinh,0)+'/100</b>']],[1])},
  {title:'Matriz de responsabilidades',html:resp},
  {title:'Riscos e temas de proteção',html:riscos+'<p>Sua alternativa se o acordo não sair: <b>'+esc({outro_parceiro:'procurar outro parceiro',arrendar:'arrendar a área',progressivo:'começar pequeno com recursos próprios',esperar:'esperar e manter a terra',nenhuma:'nenhuma definida'}[s.t('alternativa')]||'—')+'</b>.</p>'},
  {title:'Proposta preliminar',html:prop},
  {title:'Premissas utilizadas',html:prem}
 ],plan:plan};
}
});
})();
