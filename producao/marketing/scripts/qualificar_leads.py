import json,sys,collections,datetime,html,os
# Uso: python3 qualificar_leads.py <pasta com leads_all.json>  (export do Windsor facebook_leads)
# E-mails de teste a ignorar: variável ZION_TEST_EMAILS (separados por vírgula)
TEST=set(e.strip() for e in os.environ.get('ZION_TEST_EMAILS','').split(',') if e.strip())
S=sys.argv[1]
d=json.load(open(S+'/leads_all.json'))['data']
seen=set();L=[]
for r in d:
    if (r.get('email') or '') in TEST or r['id'] in seen: continue
    seen.add(r['id']);L.append(r)
def brt(t):
    x=datetime.datetime.strptime(t[:19],'%Y-%m-%dT%H:%M:%S')-datetime.timedelta(hours=3)
    return x.strftime('%d/%m %Hh%M')
def lab(v):
    if v is None: return ''
    v=str(v).replace('_',' ').strip().replace('r$','R$').replace('  ',' ')
    return v[:1].upper()+v[1:]
Q=[('qual_a_localização_do_terreno_ou_projeto_','Localização do terreno ou projeto'),
('você_possui:_','Você possui'),
('qual_o_tamanho_aproximado_da_área','Tamanho aproximado da área'),
('qual_objetivo_com_o_terreno','Estágio (objetivo com o terreno)'),
('qual_o_objetivo_do_projeto_','Objetivo do projeto'),
('qual_investimento_previsto_para_o_projeto','Investimento previsto'),
('qual_é_o_valor_estimado_da_sua_área_hoje','Valor estimado da área hoje'),
('como_está_a_documentação_da_área','Documentação da área'),
('o_que_você_busca_com_a_zion','O que busca com a Zion'),
('o_que_você_busca_para_tirar_o_projeto_do_papel','O que busca para tirar o projeto do papel'),
('qual_é_a_sua_maior_dificuldade_para_começar_o_projeto','Maior dificuldade para começar'),
('depois_de_construído_quem_vai_operar_o_empreendimento','Quem vai operar'),
('quando_o_projeto_estiver_pronto_como_você_pretende_operar','Como pretende operar'),
('você_gostaria_de_realizar_essa_análise_para_o_seu_terreno','O que quer da análise'),
('que_tipo_de_imóveis_ou_áreas_você_mais_trabalha_hoje','(Imobiliária) Tipo de imóvel com que trabalha'),
('você_já_atua_ou_tem_interesse_em_projetos_turísticos_ou_hoteleiros_por_quê','(Imobiliária) Atua ou tem interesse em turismo? Por quê?'),
('como_você_enxerga_o_potencial_turístico_das_áreas_que_comercializa','(Imobiliária) Potencial turístico das áreas')]
OPEN={'qual_a_localização_do_terreno_ou_projeto_','você_já_atua_ou_tem_interesse_em_projetos_turísticos_ou_hoteleiros_por_quê','como_você_enxerga_o_potencial_turístico_das_áreas_que_comercializa'}
g=lambda r,k:(r.get(k) or '')
def seg(r):
    pos=g(r,'você_possui:_');area=g(r,'qual_o_tamanho_aproximado_da_área');est=g(r,'qual_objetivo_com_o_terreno')
    inv=g(r,'qual_investimento_previsto_para_o_projeto');doc=g(r,'como_está_a_documentação_da_área');val=g(r,'qual_é_o_valor_estimado_da_sua_área_hoje')
    busca=g(r,'o_que_você_busca_para_tirar_o_projeto_do_papel')+' '+g(r,'o_que_você_busca_com_a_zion')
    op=g(r,'depois_de_construído_quem_vai_operar_o_empreendimento')+g(r,'quando_o_projeto_estiver_pronto_como_você_pretende_operar')
    s={'acima_de_r$3_milhões':4,'r$1_milhão_a_r$3_milhões':3,'r$400_mil_a_r$1_milhão':2}.get(inv,0)
    s+={'mais_de_50.000_m²_':2,'20.000_m²_a_50.000_m²_':2,'5.000_m²_a_20.000_m²_':1}.get(area,0)
    s+={'projeto_em_desenvolvimento_':2,'já_tenho_o_terreno_':1}.get(est,0)
    s+=2 if 'escritura' in doc else (-1 if 'posse' in doc else 0)
    s+={'acima_de_r$_5_milhões':2,'de_r$_2_milhões_a_r$_5_milhões':2,'de_r$_500_mil_a_r$_2_milhões':1}.get(val,0)
    if 'experiência' in op: s+=1
    esc='escritura' in doc
    if not pos and g(r,'que_tipo_de_imóveis_ou_áreas_você_mais_trabalha_hoje'): P=('IMOB','Imobiliária parceira','Programa de imobiliárias parceiras · reunião')
    elif 'hotel_ou_pousada' in pos: P=('D','Operador / expansão','Land Bank → reunião com o Bruno (expansão)')
    elif 'empresa_especializada' in op and s>=5: P=('F','Quer um operador','Land Bank → reunião com o Bruno (feito por você / parceria)')
    elif esc and (inv not in ('r$150_mil_a_r$400_mil','') or val in ('acima_de_r$_5_milhões','de_r$_2_milhões_a_r$_5_milhões')): P=('A','Pronto para o Land Bank','Land Bank → reunião com o Bruno')
    elif esc: P=('B','Terra estruturável','Land Bank → reunião com o CS')
    elif 'posse' in doc or ('sócio' in busca or 'capital' in busca): P=('C','Quer sócio / posse','Masterclass (ou Land Bank se a nota for 6 ou mais) → mentoria + regularização')
    elif s>=4: P=('B?','Terra estruturável (confirmar a escritura)','Trava 1 (escritura) → Land Bank')
    else: P=('E','Ideia inicial','Masterclass → reunião')
    t='QUENTE' if s>=6 else 'MORNO' if s>=3 else 'FRIO'
    return s,t,P
# ---------- objection map
OBJ={
'você_possui:_':{
 'terreno_em_área_turística__':("Será que a minha área vale a pena? / Quanto vale?","A sua área já está numa região que atrai gente. O que define se vale a pena é o projeto: é isso que a avaliação técnica mostra."),
 'área_rural_ou_natural__':("Minha área não é turística / é longe.","O turismo de natureza procura justamente área rural: silêncio, mata e vista. A pergunta não é se é turística, é qual experiência ela comporta."),
 'hotel_ou_pousada_que_deseja_expandir__':("Já sei operar, não preciso de ajuda.","Quem já opera ganha mais com a expansão certa: uma unidade de experiência pode subir a diária da casa toda. É conversa de operador para operador, com o Bruno."),
 'já_tenho_um_empreendimento_e_quero_um_parceiro':("Quero um parceiro que entre comigo no negócio.","Parceria séria começa por um projeto que mostre a conta. No Land Bank, o seu empreendimento fica visível para possíveis parceiros, e a Zion avalia cada caso."),
 'projeto_turístico_em_desenvolvimento__':("Já tenho projeto / arquiteto.","Ótimo! A pergunta é se ele é competitivo para atrair sócio ou crédito. Na avaliação técnica a gente olha a conta e o produto do seu projeto.")},
'qual_o_tamanho_aproximado_da_área':{
 'até_5.000_m²_':("Meu terreno é pequeno demais.","Não precisa de área grande, precisa do modelo certo. Com 2 ou 3 unidades bem desenhadas já se faz um produto de experiência."),
 '5.000_m²_a_20.000_m²_':("Não sei quantas unidades cabem.","É exatamente o desenho do terreno, um dos pilares da avaliação técnica."),
 '20.000_m²_a_50.000_m²_':("É muita área, não sei por onde começar.","Área grande se desenvolve em fases. A avaliação mostra qual parte começar primeiro."),
 'mais_de_50.000_m²_':("Talvez seja melhor vender ou lotear.","Não venda a sua terra: venda a experiência nela. Uma área grande estruturada vale mais e pode receber parceiro sem você abrir mão dela.")},
'qual_objetivo_com_o_terreno':{
 'apenas_ideia_':("Ainda é cedo para mim.","É a melhor fase: é quando mais se economiza erro. Quem estrutura antes de construir não paga duas vezes."),
 'já_tenho_o_terreno_':("Tenho a terra, mas não sei o próximo passo.","O próximo passo é a leitura do lugar e do produto. É isso que o Land Bank organiza."),
 'projeto_em_desenvolvimento_':("Já estou fazendo, não preciso.","Então é hora de validar a conta antes de investir mais. Errar no meio custa mais do que no começo.")},
'qual_o_objetivo_do_projeto_':{
 'criar_chalés_ou_cabanas_':("Qual modelo dá mais dinheiro?","Depende do lugar, do público e da conta. Não existe modelo campeão sem a leitura da sua área: é isso que a avaliação técnica responde."),
 'desenvolver_glamping_':("Glamping é moda, será que dura?","A Zion opera glamping desde 2020, com notas 9,6 no Booking e Superhost no Airbnb. O que dura é produto bem desenhado para o público certo."),
 'criar_pousada_ou_hotel_boutique_':("Pousada exige muito investimento.","Dá para começar com um núcleo menor e crescer em fases. A conta certa define o tamanho da primeira etapa.")},
'qual_investimento_previsto_para_o_projeto':{
 'r$150_mil_a_r$400_mil':("Não tenho muito dinheiro / é pouco.","Dá para começar com 1 ou 2 unidades e crescer com o resultado. O importante é a ordem certa, para não gastar no que não volta."),
 'r$400_mil_a_r$1_milhão':("É muito dinheiro, tenho medo de errar.","Por isso a Zion valida a conta antes de construir. Um projeto estruturado reduz o risco de pagar duas vezes."),
 'r$1_milhão_a_r$3_milhões':("Quero segurança antes de investir.","Para esse volume, o certo é o projeto competitivo e o Dossiê. A reunião é com o Bruno, que opera desde 2020."),
 'acima_de_r$3_milhões':("Quem vai cuidar disso para mim?","Existe o caminho feito por você, com a nossa equipe conduzindo, e o modelo de parceria, avaliado caso a caso.")},
'qual_é_o_valor_estimado_da_sua_área_hoje':{
 'até_r$_500_mil':("Minha área vale pouco.","O valor da área muda quando ela tem um projeto. Terra parada vale menos que terra com plano."),
 'de_r$_500_mil_a_r$_2_milhões':("Vale mais vender?","Vender é uma vez só. Uma área estruturada pode gerar receita e continuar sua."),
 'de_r$_2_milhões_a_r$_5_milhões':("Não quero arriscar um patrimônio desse.","Justamente por isso: o projeto vem antes do investimento, e a área pode até virar garantia de crédito."),
 'acima_de_r$_5_milhões':("Não preciso de ajuda, tenho patrimônio.","Patrimônio parado é custo. Com o projeto certo, ele atrai parceiro sem você vender nem um metro.")},
'como_está_a_documentação_da_área':{
 'escritura_ou_matrícula_em_dia':("(sem objeção: é o ponto forte)","Use como alavanca: a área já pode virar garantia e entrar no Land Bank."),
 'só_contrato_ou_posse':("Não tenho escritura, então não dá.","Esse é o primeiro passo, não o fim: com a área regularizada, ela ganha valor e vira garantia. A gente te ajuda a montar esse caminho junto com o projeto.")},
'o_que_você_busca_com_a_zion':{
 'buscar_um_sócio_ou_investidor':("A Zion investe? Vocês me arrumam sócio?","A Zion avalia parcerias caso a caso. Sócio entra em projeto, não em terreno: primeiro o Land Bank e a avaliação técnica. Não prometemos sócio nem crédito."),
 'entender_se_o_meu_terreno_tem_potencial':("Só quero saber se serve.","É exatamente o que a avaliação técnica responde, com o plano de ação."),
 'ser_acompanhado_por_especialistas':("Quero alguém do lado.","Esse é o caminho feito com você: a mentoria. A avaliação técnica define o formato.")},
'o_que_você_busca_para_tirar_o_projeto_do_papel':{
 'um_parceiro_para_desenvolver_comigo':("Quero dividir o risco com alguém.","Parceiro sério entra quando vê o projeto. No Land Bank, a sua área fica visível para possíveis parcerias, desde que esteja estruturada."),
 'conhecimento_para_fazer_sozinho':("Prefiro aprender e fazer sozinho (não quero pagar mentoria).","Perfeito: existe o caminho você faz sozinho, com as trilhas. Ele começa pelo Land Bank e pela avaliação, para você não errar a ordem."),
 'investimento_ou_capital_para_o_projeto':("Não tenho dinheiro.","Quase todo mundo que chega aqui tem a terra e não tem o capital. O dinheiro existe; o que falta é o projeto onde ele possa entrar."),
 'mentoria_de_quem_já_opera':("Quero aprender com quem faz.","O Bruno opera desde 2020 e tem 20 anos de hotelaria. A reunião é o primeiro passo.")},
'qual_é_a_sua_maior_dificuldade_para_começar_o_projeto':{
 'falta_capital_ou_financiamento':("Sem dinheiro não começo.","Sócio e banco entram em projeto, não em terreno. O primeiro passo custa pouco: estruturar."),
 'não_sei_por_onde_começar_(o_passo_a_passo)':("É complicado demais.","São 4 etapas: ler o lugar, desenhar o produto, desenhar o terreno e fechar a conta. A gente te ajuda na ordem."),
 'não_sei_se_o_meu_terreno_serve':("E se meu terreno não servir?","Melhor descobrir agora, por R$ 47 ou R$ 270, do que depois de investir R$ 400 mil."),
 'medo_de_errar_depois_de_pronto':("Tenho medo de investir e dar errado.","O medo é saudável: por isso a Zion valida a conta antes de construir. Errar no papel custa pouco.")},
'depois_de_construído_quem_vai_operar_o_empreendimento':{
 'eu_mesmo_—_mas_quero_aprender_a_operar_profissionalmente':("Não sei operar hospedagem.","A operação se aprende. A Zion ensina o que opera: é o pilar de operação do método."),
 'eu_mesmo_—_já_tenho_experiência_com_hospedagem':("Já sei, não preciso.","Ótimo, é meio caminho. O que falta é o produto e a conta para a área nova."),
 'prefiro_que_uma_empresa_especializada_opere_por_mim':("Quero renda sem trabalhar nisso.","Existe o modelo de parceria em que a operação é conduzida por especialistas, avaliado caso a caso. Não prometemos renda: o primeiro passo é a avaliação técnica.")},
'você_gostaria_de_realizar_essa_análise_para_o_seu_terreno':{
 'quero_entender_investimento_e_retorno_do_projeto':("Quanto eu vou ganhar?","Não dá para prometer retorno sem a conta da sua área. O que mostramos é o case da Zion, que não é promessa, e na avaliação técnica você vê a conta da sua."),
 'quero_avaliar_o_potencial_turístico_da_área':("Só quero saber o potencial.","A avaliação técnica faz essa leitura: acesso, demanda, atrativos e restrições.")},
}
OBJ['quando_o_projeto_estiver_pronto_como_você_pretende_operar']=OBJ['depois_de_construído_quem_vai_operar_o_empreendimento']
# ---------- build
E=html.escape
rec=sorted([r for r in L if r['created_time']>='2026-11-03T00:00'],key=lambda r:r['created_time'])
css='''@page{size:A4;margin:14mm 12mm}body{font-family:Inter,Arial,sans-serif;color:#1d2a22;font-size:9.5pt;line-height:1.38}
h1{font-family:Georgia,serif;font-size:22pt;margin:0 0 4px;color:#123a2a}h2{font-family:Georgia,serif;color:#123a2a;font-size:15pt;border-bottom:2px solid #c9a96a;padding-bottom:3px;margin-top:22px;page-break-after:avoid}
h3{font-size:11pt;margin:14px 0 4px;color:#123a2a;page-break-after:avoid}.sub{color:#5a6b60;margin-bottom:12px}
.card{border:1px solid #d9e0da;border-radius:8px;padding:8px 10px;margin:8px 0;page-break-inside:avoid}.hd{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.nm{font-weight:700;font-size:11pt}.tag{display:inline-block;border-radius:10px;padding:1px 7px;font-size:8pt;font-weight:700;margin-left:4px}
.QUENTE{background:#f7d9c9;color:#8a2e05}.MORNO{background:#f4ecc8;color:#6b5300}.FRIO{background:#dde7ef;color:#264a66}.pf{background:#123a2a;color:#fff}
.meta{color:#5a6b60;font-size:8.3pt}table{border-collapse:collapse;width:100%;margin:4px 0}td,th{border-bottom:1px solid #e6ebe7;padding:2.5px 5px;vertical-align:top;text-align:left}
th{background:#f2f5f2;font-size:8.5pt}.q{width:38%;color:#3d4d43}.nx{background:#f6f1e4;border-radius:5px;padding:4px 7px;margin-top:5px}
.bar{display:inline-block;height:8px;background:#2f6b4f;border-radius:3px;vertical-align:middle}.num{white-space:nowrap;text-align:right;width:70px}
.kpi{display:flex;gap:8px;margin:8px 0}.k{flex:1;border:1px solid #d9e0da;border-radius:8px;padding:6px 8px}.k b{display:block;font-size:15pt;color:#123a2a}
.warn{background:#fff4e5;border-left:4px solid #c9a96a;padding:6px 9px;margin:8px 0}.small{font-size:8pt;color:#5a6b60}'''
H=[f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>']
H.append('<h1>Zion Collection · Leads e objeções</h1><div class="sub">Relatório dos formulários do Meta (página Zion Glamping Collection) · gerado em 03/11/2026 · documento interno com dados pessoais: não compartilhar</div>')
P1=[seg(r) for r in rec]
H.append('<div class="kpi">'+''.join(f'<div class="k"><b>{v}</b>{k}</div>' for k,v in [('Leads de 02/11 (noite) a 03/11',len(rec)),('Quentes (nota 6 ou mais)',sum(1 for p in P1 if p[1]=='QUENTE')),('Do Land Bank (formulários novos)',sum(1 for r in rec if 'Land Bank' in r['form_name'])),('Base dos últimos 90 dias',len(L))])+'</div>')
H.append('<h2>Parte 1 · Leads de ontem para hoje (todas as respostas)</h2><div class="small">Horários de Brasília. Nota de 0 a 15 e perfil conforme o manual do SDR. Ordem: do mais recente para o mais antigo.</div>')
for r,(s,t,P) in sorted(zip(rec,P1),key=lambda x:x[0]['created_time'],reverse=True):
    rows=''.join(f'<tr><td class="q">{E(lbl)}</td><td>{E(lab(r.get(k)) if k not in OPEN else str(r.get(k)))}</td></tr>' for k,lbl in Q if r.get(k))
    H.append(f'''<div class="card"><div class="hd"><div><span class="nm">{E(r.get("full_name") or "")}</span><span class="tag pf">Perfil {P[0]}</span><span class="tag {t}">{t} · {s}</span></div><div class="meta">{brt(r["created_time"])}</div></div>
<div class="meta">📱 {E(r.get("phone") or r.get("phone_number") or "")} · ✉️ {E(r.get("email") or "")}<br>Formulário: {E(r["form_name"])} · Anúncio: {E(r.get("ad_name") or "-")} · Conjunto: {E(r.get("adset_name") or "-")}</div>
<table>{rows}</table><div class="nx"><b>{E(P[1])}</b> → {E(P[2])}</div></div>''')
# Part 2 catalog
H.append('<h2>Parte 2 · Todas as perguntas e as opções de resposta</h2><div class="small">Opções observadas nas respostas dos últimos 90 dias. Uma opção que existe no formulário mas nunca foi escolhida não aparece aqui.</div>')
forms=collections.defaultdict(list)
for r in L: forms[r['form_name']].append(r)
for fn,rs in sorted(forms.items(),key=lambda x:-len(x[1])):
    H.append(f'<h3>{E(fn)} · {len(rs)} leads</h3><table><tr><th>Pergunta</th><th>Opções de resposta (quantidade)</th></tr>')
    for k,lbl in Q:
        vals=[r.get(k) for r in rs if r.get(k)]
        if not vals: continue
        if k in OPEN: H.append(f'<tr><td class="q">{E(lbl)}</td><td><i>Resposta aberta (texto livre)</i></td></tr>');continue
        c=collections.Counter(vals)
        H.append(f'<tr><td class="q">{E(lbl)}</td><td>'+' · '.join(f'{E(lab(v))} ({n})' for v,n in c.most_common())+'</td></tr>')
    H.append('</table>')
# Part 3 analysis
H.append('<h2>Parte 3 · Últimos 90 dias: o que responderam</h2>')
for k,lbl in Q:
    if k in OPEN: continue
    c=collections.Counter(r.get(k) for r in L if r.get(k));n=sum(c.values())
    if n<5: continue
    H.append(f'<h3>{E(lbl)} <span class="small">({n} respostas)</span></h3><table>'+''.join(f'<tr><td class="q">{E(lab(v))}</td><td><span class="bar" style="width:{int(260*q/n)}px"></span></td><td class="num">{q} · {q*100//n}%</td></tr>' for v,q in c.most_common())+'</table>')
# combos
H.append('<h3>Combinações mais frequentes (o "retrato" do lead)</h3><table><tr><th>Estágio · Investimento · Dificuldade · O que busca</th><th class="num">Leads</th></tr>')
cc=collections.Counter(' · '.join(lab(g(r,k)) or '–' for k in ['qual_objetivo_com_o_terreno','qual_investimento_previsto_para_o_projeto','qual_é_a_sua_maior_dificuldade_para_começar_o_projeto','o_que_você_busca_para_tirar_o_projeto_do_papel']) for r in L if g(r,'qual_objetivo_com_o_terreno'))
for v,q in cc.most_common(12): H.append(f'<tr><td>{E(v)}</td><td class="num">{q}</td></tr>')
H.append('</table>')
segc=collections.Counter(seg(r)[2][0]+' · '+seg(r)[2][1] for r in L)
H.append('<h3>Perfis na base (regras do SDR)</h3><table>'+''.join(f'<tr><td class="q">{E(v)}</td><td class="num">{q} · {q*100//len(L)}%</td></tr>' for v,q in segc.most_common())+'</table>')
# Part 4 objections
H.append('<h2>Parte 4 · As objeções escondidas em cada resposta (base para a Zaia)</h2><div class="small">Cada resposta do formulário revela uma objeção que o lead ainda não disse. A Zaia antecipa a objeção antes que ela apareça. A coluna "% base" mostra o quanto ela pesa nos últimos 90 dias.</div>')
for k,lbl in Q:
    if k not in OBJ: continue
    if k=='quando_o_projeto_estiver_pronto_como_você_pretende_operar': continue
    c=collections.Counter(r.get(k) for r in L if r.get(k));n=max(sum(c.values()),1)
    H.append(f'<h3>{E(lbl)}</h3><table><tr><th>Resposta</th><th>Objeção escondida</th><th>O que a Zaia responde</th><th class="num">% base</th></tr>')
    for v,(o,a) in OBJ[k].items():
        H.append(f'<tr><td>{E(lab(v))}</td><td><b>{E(o)}</b></td><td>{E(a)}</td><td class="num">{c.get(v,0)*100//n}%</td></tr>')
    H.append('</table>')
tot=len(L);f=lambda k,v:sum(1 for r in L if g(r,k)==v)*100//tot
H.append(f'''<h2>Parte 5 · As 6 objeções principais (por peso na base)</h2><table><tr><th>#</th><th>Objeção</th><th>De onde vem</th><th>Linha-mestra da Zaia</th></tr>
<tr><td>1</td><td><b>"Quanto vou ganhar?"</b></td><td>{f("você_gostaria_de_realizar_essa_análise_para_o_seu_terreno","quero_entender_investimento_e_retorno_do_projeto")}% querem entender investimento e retorno</td><td>Sem a conta da área não existe número honesto. Mostrar o case da Zion (não é promessa) → a avaliação técnica traz a conta da área dele.</td></tr>
<tr><td>2</td><td><b>"Ainda é cedo / é só uma ideia"</b></td><td>{f("qual_objetivo_com_o_terreno","apenas_ideia_")}% estão só na ideia</td><td>É a fase em que mais se economiza erro → Masterclass R$ 47.</td></tr>
<tr><td>3</td><td><b>"Não tenho dinheiro"</b></td><td>{f("qual_é_a_sua_maior_dificuldade_para_começar_o_projeto","falta_capital_ou_financiamento")}% citam falta de capital · {f("qual_investimento_previsto_para_o_projeto","r$150_mil_a_r$400_mil")}% marcaram a menor faixa de investimento</td><td>Sócio entra em projeto, não em terreno. Começar em fases. O dinheiro existe; falta o projeto.</td></tr>
<tr><td>4</td><td><b>"Quero um parceiro que faça comigo"</b></td><td>{f("o_que_você_busca_para_tirar_o_projeto_do_papel","um_parceiro_para_desenvolver_comigo")}% buscam parceiro</td><td>Parceiro sério entra quando vê o projeto: o Land Bank coloca a área visível, desde que estruturada.</td></tr>
<tr><td>5</td><td><b>"Não sei operar" / "Quero que operem por mim"</b></td><td>{f("depois_de_construído_quem_vai_operar_o_empreendimento","eu_mesmo_—_mas_quero_aprender_a_operar_profissionalmente")}% querem aprender a operar · {f("depois_de_construído_quem_vai_operar_o_empreendimento","prefiro_que_uma_empresa_especializada_opere_por_mim")}% preferem empresa</td><td>A Zion ensina o que opera (com você) ou conduz (por você / parceria, caso a caso).</td></tr>
<tr><td>6</td><td><b>"Não sei por onde começar / se o terreno serve"</b></td><td>{f("qual_é_a_sua_maior_dificuldade_para_começar_o_projeto","não_sei_por_onde_começar_(o_passo_a_passo)")+f("qual_é_a_sua_maior_dificuldade_para_começar_o_projeto","não_sei_se_o_meu_terreno_serve")}% das respostas</td><td>4 etapas na ordem certa; melhor descobrir agora por R$ 47 do que depois de investir R$ 400 mil.</td></tr></table>''')
H.append('''<h2>Parte 6 · Proposta: formulário novo (as perguntas que faltam para a Zaia)</h2>
<div class="warn">Hoje os formulários não perguntam o que mais decide a venda: documentação (só os 2 do Land Bank perguntam), recurso próprio, quem decide e prazo. A Zaia precisa perguntar isso no WhatsApp, e uma parte dos leads esfria antes. Proposta: <b>duplicar o formulário campeão</b> ("[360] Avaliação Oficial… WhatsApp") e trocar 2 perguntas pouco úteis por 4 decisivas, ficando com até 11 perguntas.</div>
<table><tr><th>Pergunta nova</th><th>Opções</th><th>Para que serve na Zaia</th></tr>
<tr><td>A área tem escritura ou matrícula em seu nome?</td><td>Escritura/matrícula em dia · Só contrato ou posse · Não sei</td><td>Trava 1: define Land Bank (A/B) ou regularização (C)</td></tr>
<tr><td>Hoje você tem recurso próprio para começar?</td><td>Sim, tenho o valor · Tenho uma parte · Dependo de sócio ou investidor</td><td>Trava 2: separa quem compra de quem só busca capital</td></tr>
<tr><td>Quem decide sobre o projeto?</td><td>Eu sozinho · Eu e sócio/família</td><td>Trava 3: convidar os decisores para a reunião</td></tr>
<tr><td>Quando você quer dar o primeiro passo?</td><td>Nos próximos 30 dias · Em até 6 meses · Ainda estou pesquisando</td><td>Urgência: separa o interessado do curioso</td></tr>
<tr><td>O que mais te impediu de começar até hoje?</td><td>Dinheiro · Falta de conhecimento · Falta de tempo · Medo de errar · Documentação · Não encontrei parceiro</td><td>Revela a objeção principal antes da conversa</td></tr></table>
<p><b>Cortar:</b> "O que você busca para tirar o projeto do papel?" (repete "O que busca com a Zion") e "O que quer da análise" (82% escolhem a mesma opção).</p>
<p><b>Tela final:</b> "Falar no WhatsApp" → https://wa.me/554861371061</p>
<p class="small">Regras: as respostas da Zaia seguem "te ajudamos" e "possíveis parcerias"; nunca prometem renda, retorno, sócio ou crédito; números só do case da Zion, com o aviso.</p></body></html>''')
open(S+'/relatorio-leads.html','w').write('\n'.join(H))
print('ok',len(rec),len(L))
