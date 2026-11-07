/* ZAR-A10 · Sua Hospedagem Só Funciona com Você? · Organizador Operacional Zion */
(function(){
var F=ZA.fmt, esc=ZA.esc;
var SEM_MES=52/12;
var TASKS=[
 {id:'t_atend',v:'atend',l:'Atendimento e mensagens',passos:['Responder consultas e hóspedes com as mensagens-modelo','Registrar pedidos especiais na ficha da reserva','Enviar guia pré-chegada 2 dias antes','Escalar problemas para o responsável de manutenção']},
 {id:'t_checkin',v:'checkin',l:'Check-in e check-out',passos:['Conferir a unidade liberada pela limpeza (fotos)','Confirmar horário de chegada e enviar instruções de acesso','Receber ou orientar a entrada; apresentar a casa em 5 minutos','No check-out: vistoria rápida, registro de danos e liberação para limpeza']},
 {id:'t_limpeza',v:'limpeza',l:'Limpeza e arrumação',passos:['Seguir o checklist por cômodo, sempre na mesma ordem','Trocar enxoval e repor amenities do kit padrão','Inspecionar banheiro, ralos e cozinha','Enviar as fotos padronizadas de conclusão']},
 {id:'t_lavanderia',v:'lavanderia',l:'Lavanderia e enxoval',passos:['Separar enxoval por tipo e manchas','Lavar, secar e dobrar no padrão definido','Guardar em kits por unidade','Registrar peças danificadas para reposição']},
 {id:'t_manut',v:'manut',l:'Manutenção e reparos',passos:['Registrar cada ocorrência (data, problema, solução)','Acionar o técnico da lista de contatos','Confirmar a solução com o hóspede','Executar a manutenção preventiva do calendário']},
 {id:'t_compras',v:'compras',l:'Compras e reposição',passos:['Conferir o estoque mínimo toda semana','Comprar pela lista padrão de itens e quantidades','Guardar notas e lançar na planilha','Avisar quando um item faltar ou mudar de preço']},
 {id:'t_financeiro',v:'financeiro',l:'Financeiro e pagamentos',passos:['Conferir repasses das plataformas e pagamentos diretos','Pagar contas e prestadores nas datas fixas','Lançar receitas e despesas na planilha','Fechar o resultado do mês']},
 {id:'t_anuncio',v:'anuncio',l:'Anúncios, preços e calendário',passos:['Revisar calendário e bloqueios da semana','Ajustar preços de datas próximas e feriados','Responder avaliações','Atualizar fotos e descrição quando algo mudar']}
];
var DEP=[{v:'checkin',l:'Check-in dos hóspedes'},{v:'limpeza',l:'Limpeza entre estadias'},{v:'atendimento',l:'Respostas aos hóspedes'},{v:'pagamentos',l:'Pagamentos e contas'},{v:'manutencao',l:'Solução de problemas de manutenção'}];
var PAD=[{v:'checklist',l:'Checklist de limpeza com fotos de conclusão'},{v:'cama',l:'Padrão de montagem de cama e toalhas'},{v:'kit',l:'Kit fixo de amenities por estadia'},{v:'resposta',l:'Tempo máximo de resposta definido'},{v:'mensagens',l:'Mensagens-modelo para cada etapa'},{v:'estoque',l:'Estoque mínimo definido para cada item'}];
var ROT=[{v:'diaria',l:'Diária: conferir reservas, chegadas e saídas do dia'},{v:'semanal_estoque',l:'Semanal: conferir estoque e enxoval'},{v:'mensal_fin',l:'Mensal: fechamento financeiro'},{v:'trimestral_manut',l:'Trimestral: manutenção preventiva (gás, elétrica, aquecedor, pragas)'},{v:'semestral_rev',l:'Semestral: revisão de enxoval, colchões e itens de conforto'}];
var CTRL=[{v:'planilha',l:'Planilha financeira (receitas e despesas)'},{v:'calendario',l:'Calendário compartilhado com quem ajuda'},{v:'estoque',l:'Controle de estoque'},{v:'manutencao',l:'Registro de manutenção'},{v:'contatos',l:'Lista de contatos de prestadores e emergências'}];
var SECOES=[{v:'boasvindas',l:'Apresentação da hospedagem e padrões de atendimento'},{v:'contatos',l:'Contatos (prestadores, emergência, substituto)'},{v:'checkin',l:'Check-in e check-out'},{v:'limpeza',l:'Limpeza e enxoval'},{v:'manutencao',l:'Manutenção e problemas comuns'},{v:'emergencias',l:'Emergências (energia, água, gás, saúde)'},{v:'atendimento',l:'Mensagens-modelo'},{v:'financeiro',l:'Rotina financeira'}];
var AJUDA={ninguem:'a pessoa a contratar',familia:'familiar',freelancer:'diarista ou freelancer',equipe:'equipe'};
function arr(s,id){return Array.isArray(s.v[id])?s.v[id]:[];}
function lst(opts,vals){return vals.map(function(v){var o=opts.filter(function(x){return x.v===v;})[0];return o?o.l:v;});}

ZA.register({
id:'A10', code:'ZAR-A10', collection:'Hospedagem',
title:'Sua Hospedagem Só Funciona com Você?',
subtitle:'Organize a Operação e Recupere Seu Tempo',
tool:'Organizador Operacional Zion',
deliverable:'Manual Operacional Personalizado',
nameField:'nome', propertyField:'propriedade',
disclaimer:'As horas, os custos de delegação e o índice de organização são estimativas construídas com os dados que você informou. Antes de contratar ajuda, confirme com um contador a forma correta de contratação (diarista, prestador ou funcionário) e as obrigações envolvidas. O material é orientativo e não garante redução de horas, economia ou resultados.',

intro:[
 {kind:'mirror', title:'Você é dono da hospedagem ou funcionário dela?',
  lead:'O celular não para, a lista de tarefas não acaba e, quando você pensa em viajar, a primeira pergunta é: “quem vai fazer o check-in?”. A hospedagem funciona, mas só enquanto você estiver por perto.',
  body:'<div class="za-card"><p>Veja se alguma destas frases é sua:</p><ul><li>“Se eu ficar doente, ninguém sabe a senha de nada.”</li><li>“Explico a mesma coisa para a diarista toda semana.”</li><li>“Não sei quantas horas trabalho, só sei que são muitas.”</li><li>“Já pensei em contratar ajuda, mas não sei se compensa.”</li></ul></div>'},
 {kind:'collapse', title:'Trabalhar mais horas nem sempre resolve uma operação desorganizada.',
  lead:'Quando tudo está na sua cabeça, cada tarefa depende de você. Mais horas só aumentam o cansaço, não a capacidade.',
  body:'<div class="za-card"><p>Uma operação que funciona sem você precisa de quatro coisas:</p><ol><li><b>Tarefas mapeadas</b>, com quanto tempo cada uma consome.</li><li><b>Processos e padrões escritos</b>, para qualquer pessoa executar do mesmo jeito.</li><li><b>Responsáveis definidos</b>, com o custo de delegar calculado.</li><li><b>Calendário e controles</b>, para nada depender da memória.</li></ol><p>No final, você sai com um <b>Manual Operacional</b> montado a partir das suas respostas.</p></div>'},
 {kind:'start', title:'Vamos organizar a sua operação',
  lead:'Em 7 pilares, você vai diagnosticar a operação, mapear as tarefas e as horas, definir processos, padrões e responsáveis, montar o calendário e gerar o seu manual.',
  body:'<p>Pense numa semana típica de operação. Se não souber um dado com precisão, uma estimativa honesta já ajuda; quando não souber mesmo, marque “não sei”.</p>',
  fields:[
   {id:'nome',label:'Seu nome',type:'text',required:true,placeholder:'Ex.: Ana'},
   {id:'propriedade',label:'Nome da hospedagem',type:'text',required:true,placeholder:'Ex.: Pousada Recanto Azul'},
   {id:'tipo',label:'Tipo de hospedagem',type:'select',required:true,options:[{v:'airbnb',l:'Apartamento ou casa (Airbnb/temporada)'},{v:'cabana',l:'Cabana ou chalé'},{v:'glamping',l:'Glamping'},{v:'pousada',l:'Pequena pousada'},{v:'outro',l:'Outro'}]},
   {id:'destino',label:'Cidade / destino',type:'text',required:true,placeholder:'Ex.: Paraty (RJ)'},
   {id:'unidades',label:'Quantas unidades você opera?',type:'number',required:true,min:1,max:200,step:1,unit:'unidade(s)'}
  ]}
],

pillars:[
/* 1 */
{title:'Diagnóstico operacional', screens:[
 {kind:'learn', title:'O primeiro passo é enxergar a dependência',
  body:'<p>Uma operação é <b>dependente do dono</b> quando tarefas essenciais só acontecem se ele estiver presente: o check-in, a limpeza, a resposta ao hóspede, o pagamento das contas, a solução de um problema.</p><p>O diagnóstico começa com três perguntas simples: <b>quantas horas por semana você dedica</b>, <b>quantos dias por mês você fica totalmente livre</b> e <b>o que pararia se você se afastasse por uma semana</b>. Não há resposta certa: o objetivo é ter um ponto de partida para medir a melhora.</p>',
  example:'Exemplo ilustrativo: um anfitrião estima 45 horas por semana e 2 dias livres por mês. Se ele se afastar, param check-in, limpeza, atendimento e pagamentos: 4 de 5 funções dependem só dele.'},
 {kind:'compare', title:'Operação dependente × operação organizada',
  cols:[{h:'Dependente',type:'bad',items:['Tudo está na cabeça do dono','Senhas e contatos só no celular dele','Cada pessoa faz de um jeito','Folga só quando não há reserva']},
        {h:'Organizada',type:'good',items:['Tarefas e horas mapeadas','Processos escritos e acessíveis','Padrões que qualquer pessoa segue','Substituto definido e informado']}]},
 {kind:'form', title:'Como está a sua operação hoje',
  fields:[
   {id:'do_horas',label:'Quantas horas por semana você dedica à hospedagem, em média?',type:'number',required:true,min:0,max:140,step:1,unit:'h/semana'},
   {id:'do_folga',label:'Quantos dias por mês você fica totalmente sem trabalhar na hospedagem?',type:'number',required:true,min:0,max:31,step:1,unit:'dias'},
   {id:'do_reservas',label:'Quantas reservas (check-ins) por mês, em média?',type:'number',required:true,min:0,max:10000,step:1,unit:'reservas'},
   {id:'do_dependencia',label:'Se você se afastasse por uma semana, o que pararia?',type:'checks',options:DEP},
   {id:'do_controle',label:'Onde estão hoje as informações da operação?',type:'radio',required:true,options:[{v:'cabeca',l:'Na minha cabeça e no meu celular'},{v:'parcial',l:'Uma parte anotada, uma parte de memória'},{v:'organizado',l:'Organizadas e acessíveis a quem ajuda'}]}
  ]},
 {kind:'feedback', title:'O seu grau de dependência',
  metrics:function(s,c){return [{label:'Horas por semana (estimativa)',value:F.num(c.hEstimado),tag:'informado'},{label:'Dias livres por mês',value:F.num(s.n('do_folga')),tag:'informado'},{label:'Funções que dependem só de você',value:c.depN+' de 5',tag:'informado'}];},
  feedback:function(s,c){var o=[];
   if(c.depN>=4) o.push({lv:'bad',t:c.depN+' das 5 funções essenciais param sem você. A hospedagem está concentrada em uma pessoa só, o que é um risco para a operação e para a sua saúde.'});
   else if(c.depN>=2) o.push({lv:'warn',t:c.depN+' funções ainda dependem só de você: '+lst(DEP,arr(s,'do_dependencia')).join('; ').toLowerCase()+'.'});
   else o.push({lv:'ok',t:'Poucas funções dependem só de você. O foco agora é padronizar e registrar.'});
   if(s.n('do_folga',0)<=2) o.push({lv:'warn',t:'Com '+F.num(s.n('do_folga',0))+' dia(s) livre(s) por mês, não há descanso de verdade. Recuperar tempo é um objetivo legítimo do seu plano.'});
   if(c.hEstimado>=44) o.push({lv:'info',t:'Cerca de '+F.num(c.hEstimado)+' horas por semana é uma jornada de tempo integral. No próximo pilar, vamos ver para onde vão essas horas.'});
   if(s.t('do_controle')==='cabeca') o.push({lv:'warn',t:'Com as informações só na sua cabeça e no celular, ninguém consegue substituir você numa emergência.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 1',
  actions:[{id:'a1_1',text:'Anotar durante uma semana o tempo gasto em cada tarefa'},{id:'a1_2',text:'Reunir senhas, contatos e acessos em um único lugar seguro'},{id:'a1_3',text:'Escolher uma pessoa que possa substituir você numa emergência'}]}
]},
/* 2 */
{title:'Mapeamento de tarefas', screens:[
 {kind:'learn', title:'O que não é medido parece infinito',
  body:'<p>“Trabalho o tempo todo” não ajuda a decidir nada. Quando você distribui as horas da semana entre as tarefas, aparecem duas coisas: <b>as tarefas que mais consomem tempo</b> e <b>as que poderiam ser feitas por outra pessoa</b>.</p><p>As tarefas de uma hospedagem se dividem em <b>operacionais</b> (limpeza, lavanderia, check-in, manutenção, compras) e <b>de gestão</b> (atendimento, financeiro, anúncios e preços). Em geral, as operacionais são as mais fáceis de delegar com um bom processo; as de gestão exigem mais confiança e controle.</p>',
  example:'Exemplo ilustrativo: 40 horas mapeadas, das quais 12 em limpeza e 5 em lavanderia. Só essas duas tarefas somam 17 horas por semana, mais de 40% do tempo.'},
 {kind:'compare', title:'Lista de afazeres × mapa de tarefas',
  cols:[{h:'Lista de afazeres',type:'bad',items:['Tarefas sem tempo estimado','Tudo parece urgente','Não separa operar de gerir','Não mostra o que delegar']},
        {h:'Mapa de tarefas',type:'good',items:['Horas por semana em cada tarefa','Mostra onde está o maior peso','Separa tarefas operacionais e de gestão','Base para decidir o que delegar']}]},
 {kind:'form', title:'Para onde vão as suas horas', intro:'Informe quantas horas por semana <b>você mesmo</b> gasta em cada tarefa. Coloque 0 no que outra pessoa já faz.',
  fields:TASKS.map(function(t){return {id:t.id,label:t.l,type:'number',required:true,min:0,max:100,step:0.5,unit:'h/semana'};})},
 {kind:'feedback', title:'O seu mapa de tarefas',
  metrics:function(s,c){return [{label:'Horas mapeadas/semana',value:F.num(c.hTotal,1),tag:'calculado'},{label:'Maior tarefa',value:c.topTask?c.topTask.l:'—',tag:'calculado'},{label:'Horas por reserva',value:c.hPorReserva==null?'—':F.num(c.hPorReserva,1),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.hTotal===0) o.push({lv:'warn',t:'Nenhuma hora foi mapeada. Se outras pessoas fazem tudo, ótimo; se não, preencha uma estimativa para cada tarefa.'});
   if(c.topTask&&c.hTotal>0) o.push({lv:'info',t:'<b>'+c.topTask.l+'</b> é a tarefa que mais consome seu tempo: '+F.num(c.topTask.h,1)+' h por semana ('+F.pct(c.topTask.h/c.hTotal*100,0)+' do total mapeado).'});
   if(c.hTotal>0&&c.hEstimado>0&&Math.abs(c.hTotal-c.hEstimado)/c.hEstimado>0.25) o.push({lv:'warn',t:'Você estimou '+F.num(c.hEstimado)+' h por semana, mas o mapa soma '+F.num(c.hTotal,1)+' h. A diferença pode estar em tarefas “invisíveis” (deslocamentos, imprevistos, mensagens fora de hora). Anote uma semana real para confirmar.'});
   if(c.hTotal>0) o.push({lv:'info',t:'Tarefas operacionais somam '+F.num(c.hOp,1)+' h e tarefas de gestão, '+F.num(c.hAdm,1)+' h por semana.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 2',
  actions:[{id:'a2_1',text:'Cronometrar a maior tarefa durante uma semana real'},{id:'a2_2',text:'Anotar as tarefas “invisíveis” que não estavam no mapa'},{id:'a2_3',text:'Revisar o mapa de tarefas a cada temporada'}]}
]},
/* 3 */
{title:'Processos', screens:[
 {kind:'learn', title:'Processo é o passo a passo que tira a tarefa da sua cabeça',
  body:'<p>Um processo é a descrição curta de <b>como uma tarefa é feita, do início ao fim</b>: o gatilho (quando começa), os passos, o resultado esperado e o que fazer se algo der errado. Ele não precisa ser um documento longo: uma página com 4 a 8 passos resolve a maioria das tarefas.</p><p>Comece pelas tarefas que mais consomem horas e pelas que você quer delegar. Sem processo escrito, delegar vira “explicar de novo toda semana”.</p>',
  example:'Exemplo ilustrativo de processo de check-out: (1) às 11h, mensagem de despedida; (2) vistoria rápida com fotos; (3) registrar danos ou itens faltando; (4) liberar a unidade para a limpeza no calendário.'},
 {kind:'compare', title:'Saber fazer × ter um processo',
  cols:[{h:'Saber fazer',type:'bad',items:['“Eu sei como é, é só fazer”','Cada vez sai um pouco diferente','Ninguém consegue assumir','Erros se repetem']},
        {h:'Ter um processo',type:'good',items:['Passos escritos, curtos e na ordem','Resultado igual, quem quer que faça','Base para treinar outra pessoa','Erros viram ajustes no processo']}]},
 {kind:'form', title:'Quais processos já existem',
  fields:[
   {id:'pr_escritos',label:'Quais tarefas já têm passo a passo escrito?',type:'checks',options:TASKS.map(function(t){return {v:t.v,l:t.l};})},
   {id:'pr_ferramenta',label:'Onde ficam (ou ficarão) os processos?',type:'radio',required:true,options:[{v:'cabeca',l:'Ainda não ficam em lugar nenhum'},{v:'papel',l:'Papel ou caderno na unidade'},{v:'digital',l:'Documento ou aplicativo compartilhado'}]}
  ]},
 {kind:'feedback', title:'Cobertura dos seus processos',
  metrics:function(s,c){return [{label:'Tarefas ativas com processo',value:c.procN+' de '+c.ativas,tag:'calculado'},{label:'Cobertura de processos',value:F.pct(c.procCov*100,0),tag:'calculado'}];},
  feedback:function(s,c){var o=[];
   if(c.ativas===0) o.push({lv:'info',t:'Nenhuma tarefa com horas mapeadas. Os processos do manual serão sugeridos para todas as tarefas.'});
   else if(c.procCov<0.3) o.push({lv:'bad',t:'Só '+c.procN+' das '+c.ativas+' tarefas que você executa têm processo escrito. O manual deste produto traz um passo a passo inicial para cada uma.'});
   else if(c.procCov<1) o.push({lv:'warn',t:'Faltam processos para: '+c.semProc.map(function(t){return t.l.toLowerCase();}).join('; ')+'.'});
   else o.push({lv:'ok',t:'Todas as tarefas que você executa têm processo escrito. Revise-os a cada temporada.'});
   if(c.topTask&&c.semProc.some(function(t){return t.v===c.topTask.v;})) o.push({lv:'warn',t:'Sua maior tarefa (<b>'+c.topTask.l+'</b>) não tem processo escrito. Comece por ela.'});
   if(s.t('pr_ferramenta')==='cabeca') o.push({lv:'warn',t:'Defina um lugar para os processos. Um documento compartilhado permite que quem ajuda consulte de qualquer lugar.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 3',
  actions:[{id:'a3_1',text:'Escrever o processo da maior tarefa esta semana'},{id:'a3_2',text:'Guardar todos os processos em um único lugar compartilhado'},{id:'a3_3',text:'Pedir a quem executa que revise o processo e sugira ajustes'}]}
]},
/* 4 */
{title:'Padrões', screens:[
 {kind:'learn', title:'Padrão é o “como deve ficar”',
  body:'<p>O processo diz <b>como fazer</b>; o padrão diz <b>como deve ficar</b>. Cama montada sempre do mesmo jeito, o mesmo kit de amenities, a mesma resposta em até 1 hora, o mesmo estoque mínimo. O padrão permite conferir o trabalho sem refazer.</p><p>O sinal de que faltam padrões é o <b>retrabalho</b>: refazer a cama, voltar para buscar um item que faltou, corrigir uma informação errada enviada ao hóspede. Cada retrabalho é tempo perdido e, muitas vezes, uma avaliação em risco.</p>',
  example:'Exemplo ilustrativo: uma foto de referência da cama arrumada colada na porta do armário de enxoval. Qualquer pessoa compara e confere em segundos.'},
 {kind:'compare', title:'Sem padrão × com padrão',
  cols:[{h:'Sem padrão',type:'bad',items:['“Arruma do seu jeito”','Kit diferente a cada estadia','Estoque acaba sem aviso','Conferência depende do dono']},
        {h:'Com padrão',type:'good',items:['Foto de referência do resultado','Kit fixo com quantidades','Estoque mínimo para cada item','Qualquer pessoa consegue conferir']}]},
 {kind:'form', title:'Seus padrões',
  fields:[
   {id:'pa_itens',label:'Quais padrões já estão definidos?',type:'checks',options:PAD},
   {id:'pa_retrabalho',label:'Quantas vezes por mês algo precisa ser refeito ou corrigido?',type:'number',required:true,min:0,max:500,step:1,unit:'vezes/mês',allowUnknown:true,help:'Cama refeita, item esquecido, informação errada, limpeza repetida etc.'}
  ]},
 {kind:'feedback', title:'O nível de padronização',
  metrics:function(s,c){return [{label:'Padrões definidos',value:c.padN+' de 6',tag:'informado'},{label:'Retrabalhos por mês',value:s.unknown('pa_retrabalho')?'—':F.num(s.n('pa_retrabalho')),tag:'informado'}];},
  feedback:function(s,c){var o=[];var f=PAD.filter(function(p){return arr(s,'pa_itens').indexOf(p.v)<0;});
   if(c.padN<=2) o.push({lv:'bad',t:'Só '+c.padN+' de 6 padrões definidos. Sem padrão, conferir significa refazer.'});
   else if(f.length) o.push({lv:'warn',t:'Padrões a definir: '+f.map(function(x){return x.l.toLowerCase();}).join('; ')+'.'});
   else o.push({lv:'ok',t:'Todos os padrões básicos estão definidos.'});
   var r=s.n('pa_retrabalho');
   if(r!=null&&s.n('do_reservas',0)>0&&r/s.n('do_reservas')>0.2) o.push({lv:'warn',t:'São '+F.num(r)+' retrabalhos por mês para '+F.num(s.n('do_reservas'))+' reservas: cerca de 1 a cada '+F.num(s.n('do_reservas')/r,0)+' estadias. Padrões e conferência com foto reduzem esse número.'});
   if(s.unknown('pa_retrabalho')) o.push({lv:'info',t:'Comece a anotar cada retrabalho: é o melhor indicador de que um padrão está faltando.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 4',
  actions:[{id:'a4_1',text:'Fotografar o resultado padrão de cama, banheiro e cozinha'},{id:'a4_2',text:'Definir o kit fixo de amenities e o estoque mínimo'},{id:'a4_3',text:'Anotar cada retrabalho durante um mês'}]}
]},
/* 5 */
{title:'Responsabilidades', screens:[
 {kind:'learn', title:'Delegar tem custo. Não delegar também.',
  body:'<p>Para decidir o que delegar, compare dois valores:</p><ul><li><b>Custo de delegar</b>: horas delegadas × custo da hora de quem vai assumir.</li><li><b>Valor do seu tempo</b>: as mesmas horas × quanto vale a sua hora (o que você ganharia ou deixaria de perder usando esse tempo em outra coisa, inclusive descanso).</li></ul><p>A conta mensal usa 52 semanas ÷ 12 meses ≈ 4,33 semanas por mês. Delegar uma tarefa sem processo e padrão, porém, só troca o seu trabalho de executar pelo trabalho de corrigir. Por isso este pilar vem depois dos processos.</p>',
  example:'Exemplo ilustrativo: delegar 17 h por semana de limpeza e lavanderia a R$ 25 por hora custa 17 × 25 × 4,33 ≈ R$ 1.842 por mês e libera cerca de 74 horas mensais.'},
 {kind:'compare', title:'Mais fáceis × mais delicadas de delegar',
  cols:[{h:'Mais fáceis (com processo)',items:['Limpeza e arrumação','Lavanderia e enxoval','Compras pela lista padrão','Check-in com instruções claras']},
        {h:'Mais delicadas (com controle)',items:['Financeiro e pagamentos','Preços e calendário','Respostas a avaliações','Negociação com hóspedes']}]},
 {kind:'form', title:'Quem faz o quê',
  fields:[
   {id:'re_delegar',label:'Quais tarefas você quer delegar?',type:'checks',options:TASKS.map(function(t){return {v:t.v,l:t.l};})},
   {id:'re_custo_hora',label:'Quanto custaria, por hora, a pessoa que assumiria essas tarefas?',type:'money',required:true,help:'Use o valor que você pagaria na sua região (diária ÷ horas, ou valor-hora combinado).'},
   {id:'re_valor_hora',label:'Quanto vale uma hora do seu tempo?',type:'money',required:true,allowUnknown:true,help:'Pode ser sua renda por hora em outra atividade, ou o valor que você dá ao seu descanso.'},
   {id:'re_ajuda',label:'Quem poderia assumir?',type:'radio',required:true,options:[{v:'ninguem',l:'Ainda não tenho ninguém'},{v:'familia',l:'Alguém da família'},{v:'freelancer',l:'Diarista ou prestador de serviço'},{v:'equipe',l:'Funcionário ou equipe'}]}
  ]},
 {kind:'feedback', title:'O custo e o ganho de delegar',
  metrics:function(s,c){return [{label:'Horas delegadas/semana',value:F.num(c.hDeleg,1),tag:'calculado'},{label:'Horas liberadas/mês',value:F.num(c.horasLibMes,1),tag:'calculado'},{label:'Custo da delegação/mês',value:F.brl(c.custoDelegMes),tag:'estimativa'},{label:'Custo por reserva',value:c.custoPorReserva==null?'—':F.brl(c.custoPorReserva),tag:'estimativa'}];},
  feedback:function(s,c){var o=[];
   if(c.hDeleg===0) o.push({lv:'info',t:'Nenhuma tarefa marcada para delegar (ou as marcadas têm 0 h). Se você quer recuperar tempo, comece pela tarefa operacional de maior peso.'});
   else o.push({lv:'info',t:'Delegar '+F.num(c.hDeleg,1)+' h por semana custa cerca de <b>'+F.brl(c.custoDelegMes)+' por mês</b> e libera <b>'+F.num(c.horasLibMes,0)+' horas</b> do seu mês.'});
   if(c.valorTempoMes!=null&&c.hDeleg>0){
    if(c.saldoDeleg>=0) o.push({lv:'ok',t:'Pelo valor que você atribui à sua hora, o tempo liberado vale '+F.brl(c.valorTempoMes)+' por mês, '+F.brl(c.saldoDeleg)+' acima do custo de delegar.'});
    else o.push({lv:'warn',t:'Pelo valor que você atribui à sua hora, o tempo liberado ('+F.brl(c.valorTempoMes)+') vale menos que o custo de delegar. Ainda pode fazer sentido por descanso ou risco, mas é uma decisão consciente.'});}
   if(s.unknown('re_valor_hora')) o.push({lv:'info',t:'Sem o valor da sua hora, não comparamos custo e ganho. Uma referência simples: sua renda mensal em outra atividade ÷ horas trabalhadas.'});
   if(c.delegSemProc.length) o.push({lv:'warn',t:'Você quer delegar tarefas sem processo escrito: '+c.delegSemProc.map(function(t){return t.l.toLowerCase();}).join('; ')+'. Escreva o processo antes de passar adiante.'});
   if(s.t('re_ajuda')==='ninguem'&&c.hDeleg>0) o.push({lv:'warn',t:'Ainda não há quem assuma. Converse com 2 ou 3 pessoas da região e faça um período de teste acompanhado.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 5',
  actions:[{id:'a5_1',text:'Escolher a primeira tarefa a delegar e a pessoa responsável'},{id:'a5_2',text:'Fazer duas execuções acompanhadas usando o processo escrito'},{id:'a5_3',text:'Confirmar com um contador a forma correta de contratação'}]}
]},
/* 6 */
{title:'Calendário e controles', screens:[
 {kind:'learn', title:'Rotina no calendário, não na memória',
  body:'<p>Muitas tarefas não são diárias, e por isso são esquecidas: conferir o estoque, fechar o financeiro, fazer a manutenção preventiva do aquecedor ou do gás, revisar o enxoval. A solução é um <b>calendário de rotinas</b> com frequência fixa (diária, semanal, mensal, trimestral, semestral) e um responsável.</p><p>Os <b>controles</b> são os registros que mostram se a rotina aconteceu: planilha financeira, calendário compartilhado, controle de estoque, registro de manutenção e lista de contatos. Com eles, você acompanha a operação sem precisar estar lá.</p>',
  example:'Exemplo ilustrativo: toda segunda-feira às 9h, 20 minutos para conferir estoque e enxoval; todo dia 5, fechamento financeiro do mês anterior; em março, junho, setembro e dezembro, revisão preventiva.'},
 {kind:'compare', title:'Apagar incêndio × rotina com controle',
  cols:[{h:'Apagar incêndio',type:'bad',items:['Descobre que o gás acabou com o hóspede lá','Financeiro só quando a conta aperta','Manutenção só quando quebra','Ninguém sabe o que já foi feito']},
        {h:'Rotina com controle',type:'good',items:['Estoque conferido toda semana','Fechamento financeiro mensal','Preventiva com data marcada','Registros que qualquer um consulta']}]},
 {kind:'form', title:'Suas rotinas e seus controles',
  fields:[
   {id:'ca_rotinas',label:'Quais rotinas já acontecem com frequência fixa?',type:'checks',options:ROT},
   {id:'ca_controles',label:'Quais controles você já usa?',type:'checks',options:CTRL},
   {id:'ca_meta',label:'Quantas horas por semana você gostaria de dedicar à hospedagem?',type:'number',required:true,min:0,max:140,step:1,unit:'h/semana'}
  ]},
 {kind:'feedback', title:'Seu tempo depois da reorganização',
  metrics:function(s,c){return [{label:'Horas mapeadas hoje',value:F.num(c.hTotal,1),tag:'calculado'},{label:'Horas após delegar',value:F.num(c.hRestante,1),tag:'calculado'},{label:'Meta',value:F.num(s.n('ca_meta')),tag:'informado'},{label:'Rotinas e controles',value:(c.rotN+c.ctrlN)+' de 10',tag:'informado'}];},
  feedback:function(s,c){var o=[];var m=s.n('ca_meta',0);
   if(c.hRestante>m) o.push({lv:'warn',t:'Depois de delegar, você ainda ficaria com '+F.num(c.hRestante,1)+' h por semana, '+F.num(c.hRestante-m,1)+' h acima da sua meta. Avalie delegar mais uma tarefa ou reduzir o tempo da maior com processo e padrão.'});
   else o.push({lv:'ok',t:'Com as delegações escolhidas, suas horas mapeadas ficariam em '+F.num(c.hRestante,1)+' h por semana, dentro da meta de '+F.num(m)+' h.'});
   if(c.rotN<=2) o.push({lv:'warn',t:'Só '+c.rotN+' rotinas com frequência fixa. As que faltam estão no calendário do seu manual.'});
   if(arr(s,'ca_controles').indexOf('planilha')<0) o.push({lv:'warn',t:'Sem planilha financeira, não há como saber se a operação, inclusive a delegação, cabe no orçamento.'});
   if(arr(s,'ca_controles').indexOf('contatos')<0) o.push({lv:'info',t:'A lista de contatos é o controle mais simples e o mais útil numa emergência.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 6',
  actions:[{id:'a6_1',text:'Lançar as rotinas no calendário do celular com lembrete'},{id:'a6_2',text:'Criar a planilha financeira e a lista de contatos'},{id:'a6_3',text:'Compartilhar o calendário com quem ajuda na operação'}]}
]},
/* 7 */
{title:'Manual operacional', screens:[
 {kind:'learn', title:'O manual é a operação escrita em um só lugar',
  body:'<p>O manual operacional reúne o que você construiu: <b>quem faz cada tarefa, o passo a passo, os padrões, o calendário de rotinas, os controles e os contatos</b>. Ele serve para treinar quem chega, para conferir quem já faz e para que alguém assuma no seu lugar numa emergência.</p><p>Um bom manual é curto, prático e vivo: revisado com frequência definida e atualizado sempre que um processo muda. Ele deve indicar também <b>quem substitui você</b> quando você não estiver disponível.</p>',
  example:'Exemplo ilustrativo: um documento compartilhado de 8 páginas, uma por seção, com fotos de referência. A diarista nova lê a seção de limpeza no primeiro dia e faz a primeira limpeza acompanhada.'},
 {kind:'compare', title:'Manual de gaveta × manual vivo',
  cols:[{h:'De gaveta',type:'bad',items:['Documento enorme que ninguém lê','Escrito uma vez e esquecido','Sem fotos nem exemplos','Ninguém sabe onde está']},
        {h:'Vivo',type:'good',items:['Uma página por seção, direto ao ponto','Revisão com data marcada','Fotos de referência dos padrões','Acessível a todos que ajudam']}]},
 {kind:'form', title:'O seu manual',
  fields:[
   {id:'ma_secoes',label:'Quais seções o seu manual deve ter?',type:'checks',options:SECOES},
   {id:'ma_substituto',label:'Quem assume a operação quando você não estiver disponível?',type:'text',required:true,placeholder:'Ex.: Maria (irmã) · (00) 00000-0000'},
   {id:'ma_revisao',label:'Com que frequência o manual será revisado?',type:'radio',required:true,options:[{v:'mensal',l:'Mensal'},{v:'trimestral',l:'Trimestral'},{v:'semestral',l:'Semestral'}]}
  ]},
 {kind:'feedback', title:'Seu Índice de Organização Operacional',
  metrics:function(s,c){return [{label:'Índice de organização',value:F.num(c.io,0)+' / 100',tag:'calculado'},{label:'Horas liberadas/mês',value:F.num(c.horasLibMes,0),tag:'calculado'},{label:'Custo da delegação/mês',value:F.brl(c.custoDelegMes),tag:'estimativa'}];},
  feedback:function(s,c){var o=[];
   o.push({lv:c.io>=70?'ok':c.io>=40?'warn':'bad',t:'Seu índice de organização é <b>'+F.num(c.io,0)+'</b> de 100. Ele combina cobertura de processos (30%), padrões (25%), rotinas (20%), controles (15%) e independência do dono (10%).'});
   var f=SECOES.filter(function(x){return arr(s,'ma_secoes').indexOf(x.v)<0;});
   if(f.length) o.push({lv:'info',t:'O relatório traz a estrutura completa do manual. Seções que você não marcou e valem considerar: '+f.map(function(x){return x.l.toLowerCase();}).join('; ')+'.'});
   if(arr(s,'ma_secoes').indexOf('emergencias')<0) o.push({lv:'warn',t:'A seção de emergências é a que mais faz falta quando você não está. Inclua-a.'});
   o.push({lv:'info',t:'Substituto definido: <b>'+esc(s.t('ma_substituto'))+'</b>. Combine com essa pessoa e entregue a ela o manual e os acessos.'});
   return o;}},
 {kind:'apply', title:'Compromissos do Pilar 7',
  actions:[{id:'a7_1',text:'Montar o manual a partir do relatório e compartilhar com quem ajuda'},{id:'a7_2',text:'Fazer um “dia sem o dono” para testar o manual'},{id:'a7_3',text:'Marcar no calendário a data da próxima revisão do manual'}]}
]}
],

compute:function(s){
 var c={};
 c.hEstimado=s.n('do_horas',0); c.res=s.n('do_reservas',0);
 c.depN=arr(s,'do_dependencia').length;
 c.tasks=TASKS.map(function(t){return {id:t.id,v:t.v,l:t.l,passos:t.passos,h:s.n(t.id,0)||0,op:['checkin','limpeza','lavanderia','manut','compras'].indexOf(t.v)>=0};});
 c.hTotal=0; c.hOp=0; c.hAdm=0;
 c.tasks.forEach(function(t){c.hTotal+=t.h; if(t.op)c.hOp+=t.h; else c.hAdm+=t.h;});
 var srt=c.tasks.filter(function(t){return t.h>0;}).sort(function(a,b){return b.h-a.h;}); c.topTask=srt[0]||null;
 c.hPorReserva=c.res>0?c.hTotal*SEM_MES/c.res:null;
 var esc_=arr(s,'pr_escritos'), del=arr(s,'re_delegar');
 var ativas=c.tasks.filter(function(t){return t.h>0;});
 c.ativas=ativas.length; c.procN=ativas.filter(function(t){return esc_.indexOf(t.v)>=0;}).length;
 c.procCov=c.ativas>0?c.procN/c.ativas:0;
 c.semProc=ativas.filter(function(t){return esc_.indexOf(t.v)<0;});
 c.padN=arr(s,'pa_itens').length;
 c.hDeleg=0; c.tasks.forEach(function(t){t.delegar=del.indexOf(t.v)>=0; t.processo=esc_.indexOf(t.v)>=0; if(t.delegar)c.hDeleg+=t.h;});
 c.delegSemProc=c.tasks.filter(function(t){return t.delegar&&t.h>0&&!t.processo;});
 c.custoHora=s.n('re_custo_hora',0)||0;
 c.horasLibMes=c.hDeleg*SEM_MES;
 c.custoDelegSem=c.hDeleg*c.custoHora; c.custoDelegMes=c.custoDelegSem*SEM_MES;
 c.custoPorReserva=c.res>0?c.custoDelegMes/c.res:null;
 var vh=s.n('re_valor_hora'); c.valorTempoMes=vh==null?null:c.horasLibMes*vh;
 c.saldoDeleg=c.valorTempoMes==null?null:c.valorTempoMes-c.custoDelegMes;
 c.hRestante=c.hTotal-c.hDeleg; c.gapMeta=c.hRestante-s.n('ca_meta',0);
 c.rotN=arr(s,'ca_rotinas').length; c.ctrlN=arr(s,'ca_controles').length;
 c.io=100*(0.30*c.procCov+0.25*c.padN/6+0.20*c.rotN/5+0.15*c.ctrlN/5+0.10*(1-c.depN/5));
 return c;
},

metrics:function(s,c){return [
 {label:'Índice de organização operacional',value:F.num(c.io,0)+' / 100',tag:'calculado'},
 {label:'Horas mapeadas/semana',value:F.num(c.hTotal,1),tag:'calculado'},
 {label:'Horas após delegar/semana',value:F.num(c.hRestante,1),tag:'calculado'},
 {label:'Meta de horas/semana',value:F.num(s.n('ca_meta')),tag:'informado'},
 {label:'Horas liberadas/mês',value:F.num(c.horasLibMes,0),tag:'calculado'},
 {label:'Custo da delegação/mês',value:F.brl(c.custoDelegMes),tag:'estimativa'},
 {label:'Cobertura de processos',value:F.pct(c.procCov*100,0),tag:'calculado'},
 {label:'Funções que dependem só de você',value:c.depN+' de 5',tag:'informado'}
];},

priorities:function(s,c){var L=[];
 if(c.depN>=4) L.push({title:'Preparar um substituto e reunir acessos e contatos',why:c.depN+' de 5 funções essenciais param sem você.',score:9});
 if(c.topTask&&c.semProc.some(function(t){return t.v===c.topTask.v;})) L.push({title:'Escrever o processo de '+c.topTask.l.toLowerCase(),why:'É a tarefa que mais consome seu tempo ('+F.num(c.topTask.h,1)+' h/semana) e não tem processo.',score:9});
 if(c.procCov<0.5&&c.ativas>0) L.push({title:'Escrever os processos das tarefas que você executa',why:'Cobertura de processos de '+F.pct(c.procCov*100,0)+'.',score:7});
 if(c.delegSemProc.length) L.push({title:'Escrever o processo antes de delegar '+c.delegSemProc[0].l.toLowerCase(),why:'Delegar sem processo vira retrabalho.',score:8});
 if(c.gapMeta>0) L.push({title:'Reduzir mais '+F.num(c.gapMeta,1)+' h por semana para chegar à meta',why:'Após delegar, você ainda fica acima das horas desejadas.',score:7});
 if(c.hDeleg>0&&s.t('re_ajuda')==='ninguem') L.push({title:'Encontrar e testar quem vai assumir as tarefas delegadas',why:'Há '+F.num(c.hDeleg,1)+' h/semana para delegar e ninguém definido.',score:7});
 if(c.hDeleg===0&&c.topTask&&c.topTask.op) L.push({title:'Avaliar delegar '+c.topTask.l.toLowerCase(),why:'É sua maior tarefa e é operacional.',score:6});
 if(c.padN<=2) L.push({title:'Definir padrões com foto de referência e kit fixo',why:'Só '+c.padN+' de 6 padrões definidos.',score:6});
 if(s.n('pa_retrabalho')!=null&&c.res>0&&s.n('pa_retrabalho')/c.res>0.2) L.push({title:'Reduzir o retrabalho com padrões e conferência',why:F.num(s.n('pa_retrabalho'))+' retrabalhos por mês.',score:6});
 if(arr(s,'ca_controles').indexOf('planilha')<0) L.push({title:'Criar a planilha financeira da operação',why:'Sem ela, não se sabe se a delegação cabe no orçamento.',score:6});
 if(c.rotN<=2) L.push({title:'Lançar as rotinas fixas no calendário',why:'Só '+c.rotN+' de 5 rotinas acontecem com frequência fixa.',score:5});
 if(arr(s,'ca_controles').indexOf('contatos')<0) L.push({title:'Montar a lista de contatos de prestadores e emergências',why:'É o controle mais útil quando você não está.',score:5});
 if(s.t('do_controle')==='cabeca') L.push({title:'Tirar as informações da cabeça e colocar em um documento compartilhado',why:'Hoje ninguém consegue substituir você.',score:6});
 if(arr(s,'ma_secoes').indexOf('emergencias')<0) L.push({title:'Incluir a seção de emergências no manual',why:'É a primeira consulta de quem substitui você.',score:4});
 if(s.n('do_folga',0)<=2) L.push({title:'Marcar no calendário pelo menos 2 dias livres por mês',why:'Hoje são '+F.num(s.n('do_folga',0))+' dia(s) livre(s).',score:4});
 return L;},

report:function(s,c){
 var tg=function(t,l){return '<span class="za-tag '+t+'">'+(l||t)+'</span>';};
 var aj=AJUDA[s.t('re_ajuda')]||'responsável a definir';
 var prem=ZA.table(['Premissa','Valor','Origem'],[
  ['Horas por semana (sua estimativa)',F.num(c.hEstimado),tg('informado')],
  ['Horas mapeadas por tarefa (soma)',F.num(c.hTotal,1),tg('informado')],
  ['Reservas por mês',F.num(c.res),tg('informado')],
  ['Custo da hora de quem assume',F.brl(c.custoHora),tg('estimativa','estimativa sua')],
  ['Valor da sua hora',s.unknown('re_valor_hora')?'—':F.brl(s.n('re_valor_hora')),s.unknown('re_valor_hora')?tg('hipotese','não informado'):tg('estimativa','estimativa sua')],
  ['Semanas por mês','52 ÷ 12 ≈ 4,33',tg('calculado')],
  ['Pesos do índice','Processos 30% · Padrões 25% · Rotinas 20% · Controles 15% · Independência do dono 10%',tg('recomendacao','metodologia Zion')]],[]);
 var mapa=ZA.table(['Tarefa','Horas/semana','Responsável proposto','Processo escrito','Custo/mês se delegada'],c.tasks.map(function(t){
  return [t.l,F.num(t.h,1),t.h===0?'outra pessoa (já não é você)':(t.delegar?'Delegar: '+esc(aj):esc(s.t('nome')||'Você')),t.processo?'sim':'<b>a escrever</b>',t.delegar&&t.h>0?F.brl(t.h*c.custoHora*SEM_MES):'—'];})
  .concat([['<b>Total</b>','<b>'+F.num(c.hTotal,1)+'</b>','<b>'+F.num(c.hDeleg,1)+' h delegadas · '+F.num(c.hRestante,1)+' h com você</b>','',  '<b>'+F.brl(c.custoDelegMes)+'</b>']]),[1,4]);
 var proc=c.tasks.filter(function(t){return t.h>0||t.delegar;}); if(!proc.length) proc=c.tasks;
 var procHtml=proc.map(function(t){return '<div class="za-card"><b>'+t.l+'</b> · responsável: '+(t.delegar?esc(aj):esc(s.t('nome')||'você'))+(t.processo?' <span class="za-tag informado">processo existente: revisar</span>':' <span class="za-tag recomendacao">passo a passo inicial sugerido</span>')+'<ol>'+t.passos.map(function(p){return '<li>'+p+'</li>';}).join('')+'</ol></div>';}).join('');
 var padT=ZA.table(['Padrão','Situação'],PAD.map(function(p){return [p.l,arr(s,'pa_itens').indexOf(p.v)>=0?'definido':'<b>a definir</b>'];}),[]);
 var rotT=ZA.table(['Rotina','Situação'],ROT.map(function(r){return [r.l,arr(s,'ca_rotinas').indexOf(r.v)>=0?'em prática':'<b>a implantar</b>'];}),[]);
 var ctrlT=ZA.table(['Controle','Situação'],CTRL.map(function(r){return [r.l,arr(s,'ca_controles').indexOf(r.v)>=0?'em uso':'<b>a criar</b>'];}),[]);
 var sec=arr(s,'ma_secoes');
 var estrutura='<div class="za-card"><ol>'+SECOES.map(function(x){return '<li>'+x.l+(sec.indexOf(x.v)>=0?'':' <span class="za-small">(sugerida)</span>')+'</li>';}).join('')+'</ol><p><b>Substituto:</b> '+esc(s.t('ma_substituto'))+' · <b>Revisão:</b> '+({mensal:'mensal',trimestral:'trimestral',semestral:'semestral'}[s.t('ma_revisao')]||'a definir')+'</p></div>';
 var deleg='<div class="za-card"><p>Horas delegadas: <b>'+F.num(c.hDeleg,1)+' h/semana</b> · horas liberadas: <b>'+F.num(c.horasLibMes,0)+' h/mês</b> · custo estimado: <b>'+F.brl(c.custoDelegMes)+'/mês</b>'+(c.custoPorReserva!=null?' ('+F.brl(c.custoPorReserva)+' por reserva)':'')+'.</p>'+(c.valorTempoMes!=null?'<p>Pelo valor que você atribui à sua hora, o tempo liberado vale '+F.brl(c.valorTempoMes)+' por mês (diferença de '+F.brl(c.saldoDeleg)+' em relação ao custo).</p>':'')+'<p class="za-small">Estimativas. Confirme a forma de contratação com um contador.</p></div>';
 var top=ZA.op3d(this.priorities(s,c)).l1;
 var plan='<div class="za-card"><b>Roteiro sugerido de 30 dias</b><ol><li><b>Semana 1:</b> '+(top[0]?esc(top[0].title):'Reunir acessos e contatos em um único lugar')+'.</li><li><b>Semana 2:</b> '+(top[1]?esc(top[1].title):'Escrever o processo da maior tarefa')+'.</li><li><b>Semana 3:</b> '+(top[2]?esc(top[2].title):'Fazer duas execuções acompanhadas da tarefa delegada')+'.</li><li><b>Semana 4:</b> “dia sem o dono” com '+esc(s.t('ma_substituto')||'o substituto')+' usando o manual; anotar o que faltou e refazer o Organizador (índice hoje: '+F.num(c.io,0)+').</li></ol></div>';
 return {sections:[
  {title:'Premissas utilizadas',html:prem},
  {title:'Mapa de tarefas e responsabilidades',html:mapa},
  {title:'Delegação: custo e tempo liberado',html:deleg},
  {title:'Processos (passo a passo)',html:procHtml+'<p class="za-small">Passos iniciais sugeridos pela metodologia: adapte à sua operação antes de entregar a quem executa.</p>'},
  {title:'Padrões',html:padT},
  {title:'Calendário de rotinas',html:rotT},
  {title:'Controles',html:ctrlT},
  {title:'Estrutura do seu Manual Operacional',html:estrutura}
 ],plan:plan};
}
});
})();
