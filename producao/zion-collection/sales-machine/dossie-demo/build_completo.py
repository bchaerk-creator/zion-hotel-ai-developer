# Gera a AMOSTRA do Dossiê completo (capa + painel dos 7 pilares + 2 páginas por pilar + decisão). Dados fictícios.
import re, html
src = open('exemplo.html', encoding='utf-8').read()
css = src[src.index('<style>'):src.index('</style>') + 8]
css = css.replace('</style>', '''
.pill{display:flex;align-items:center;gap:4mm;padding:1.7mm 0;border-bottom:1px solid rgba(201,179,126,.28)}
.pill .n{font-family:"CormorantZ";font-size:20pt;color:var(--ouro);width:9mm}
.pill .t{flex:1}.pill .t b{display:block;font-size:11pt;color:var(--creme)}.pill .t span{font-size:8pt;color:var(--areia)}
.chip{font-size:7pt;letter-spacing:.12em;text-transform:uppercase;border:1px solid var(--ouro);color:var(--ouro);padding:1mm 2.6mm;border-radius:99px}
.chip.f{background:var(--ouro);color:var(--musgo)}
.etapa{font-size:7.5pt;letter-spacing:.24em;text-transform:uppercase;color:var(--ouro);margin:5mm 0 0}
.camp{display:grid;grid-template-columns:40mm 1fr 30mm;gap:3mm;padding:3.4mm 0;border-bottom:1px solid var(--areia);font-size:10pt;align-items:start}
.camp b{color:var(--musgo)}.camp .tg{text-align:right;white-space:nowrap}.tag{white-space:nowrap}
.sec{margin-top:6mm}.sec h3{font-size:16pt;color:var(--musgo);margin-bottom:2mm}
.vd{display:inline-block;background:var(--musgo);color:var(--ouro);padding:2mm 5mm;font-family:"CormorantZ";font-size:18pt;border-radius:2mm}
.sm{font-size:9.5pt;line-height:1.5}
</style>''')

def tag(k):
    return {'D': '<span class="tag t-dec">Declarado</span>', 'O': '<span class="tag t-ori">Orientação</span>',
            'V': '<span class="tag t-ver">A verificar</span>', 'N': '<span class="tag t-ver">Não sei</span>'}[k]

P = [
 (1, 'ETAPA 1 · LER O LUGAR', 'Território e destino', 'Ficha do Território', 'Avançar',
  [('Onde fica', 'Terreno Exemplo, a 18 km do centro do destino (fictício)', 'D'), ('Tamanho', '2,4 ha, área útil estimada em 1,1 ha', 'D'), ('Acesso', 'Estrada de terra batida, 3 km após o asfalto', 'D'), ('Água', 'Nascente no terreno; vazão ainda não medida', 'N'), ('Energia', 'Rede elétrica a 600 m do portão', 'D'), ('Documentação', 'Matrícula em nome do declarante; certidões ainda não conferidas', 'V')],
  ['Terreno bom no papel não é terreno bom no chão: acesso, água e energia decidem quanto custa começar.', 'Os quatro limites (legal, ambiental, físico e de infraestrutura) são lidos antes de qualquer desenho.', 'O destino em volta importa tanto quanto o terreno: de onde vem o hóspede e como ele chega.'],
  ['Medir a vazão da nascente (não declarada).', 'Conferir matrícula e certidões atualizadas.', 'Confirmar com o órgão local o que a área permite.'], 'Cumprir as três verificações e seguir para o Mercado.'),
 (2, 'ETAPA 1 · LER O LUGAR', 'Mercado e demanda', 'Ficha do Mercado', 'Testar',
  [('Comparáveis', '3 hospedagens parecidas levantadas no destino (fictício)', 'D'), ('Diária de referência', 'R$ 000 (valor ilustrativo, não é dado de mercado)', 'D'), ('Quem paga', 'Casais e pequenos grupos, fins de semana (hipótese)', 'D'), ('Curva do ano', 'Ainda não levantada', 'N'), ('Unidades que o destino compra', 'Não sei', 'N')],
  ['Diária e ocupação são hipóteses até serem medidas; a ficha separa o que foi medido do que foi suposto.', 'Comparáveis servem para ler o mercado, não para copiar preço.', 'Sem a curva do ano, qualquer conta de receita fica frágil.'],
  ['Levantar a curva do ano com fonte e data.', 'Anotar a fonte de cada diária de referência.', 'Estimar quantas unidades o destino absorve.'], 'Voltar ao Mercado e fechar a curva do ano antes de seguir.'),
 (3, 'ETAPA 2 · DESENHAR O PRODUTO', 'Produto e tipologias', 'Ficha do Produto', 'Avançar',
  [('Tipo de hospedagem', '6 chalés compactos (hipótese)', 'D'), ('Público principal', 'Casais; segundo público: pequenos grupos', 'D'), ('Momento assinatura', 'Café da manhã na varanda, vista do vale', 'D'), ('Estadia mínima', '2 noites', 'D'), ('Promessa da unidade', 'Descanso com vista, sem atrito na chegada', 'D')],
  ['Produto bem definido responde: o que vendo, para quem, e qual momento a pessoa lembra depois.', 'A promessa é sobre a experiência, nunca sobre resultado financeiro.', 'Uma tipologia por público evita um produto que não serve a ninguém.'],
  ['Testar a promessa com 5 pessoas do público (anotar respostas).', 'Conferir se a estadia mínima combina com o acesso.'], 'Seguir para o Modelo de negócio.'),
 (4, 'ETAPA 2 · DESENHAR O PRODUTO', 'Modelo de negócio', 'Modelo de Negócio', 'Avançar',
  [('Modelo principal', 'Renda: operar as unidades (degrau 1)', 'D'), ('Modelo secundário', 'Venda futura de parte do conjunto', 'D'), ('Quem opera', 'Equipe própria, com apoio de um parceiro (ainda não definido)', 'N'), ('Canal de venda', 'Plataformas de reserva e canal direto', 'D')],
  ['Existem dois caminhos: renda ou venda. Misturar sem decidir é a causa mais comum de projeto parado.', 'Do balcão para dentro e do balcão para fora: quem faz o quê.', 'O modelo escolhido define a conta do Pilar 6.'],
  ['Definir quem opera e por qual contrato.', 'Listar as taxas de cada canal de venda.'], 'Desenhar o terreno inteiro no Masterplan.'),
 (5, 'ETAPA 3 · DESENHAR O TERRENO', 'Masterplan faseado', 'Masterplan faseado', 'Ajustar',
  [('Onde nunca construir', 'Entorno da nascente e encosta leste', 'D'), ('O que precisa existir', 'Acesso, água, energia, recepção', 'D'), ('O que cabe', '6 unidades na fase 1; mais 6 na fase 2 (hipótese)', 'D'), ('Fase 1', '3 unidades + recepção', 'D'), ('Licenças', 'Não sei', 'N')],
  ['O terreno inteiro no papel evita que a fase 1 atrapalhe a fase 2.', 'Fase 1 é o menor pedaço que já se sustenta sozinho.', 'Área protegida desenhada primeiro não é perda: é o que mantém o valor do lugar.'],
  ['Conferir licenças por fase.', 'Validar a fase 1 com um profissional habilitado (a plataforma não substitui).'], 'Ajustar a fase 1 e seguir para a Pré-viabilidade.'),
 (6, 'ETAPA 4 · FECHAR A CONTA', 'Pré-viabilidade', 'Pré-viabilidade', 'Testar',
  [('Custo da fase 1', 'R$ 000.000 (valor fictício)', 'D'), ('Receita de referência', 'R$ 000.000 por ano (ilustrativa; receita bruta não é lucro)', 'D'), ('Três cenários', 'Conservador, base e otimista preenchidos', 'D'), ('Tempo de volta', 'Calculado só como referência', 'D'), ('Cotações escritas', 'Nenhuma ainda', 'V')],
  ['Toda conta aqui é de referência e ilustrativa; receita bruta não é lucro.', 'Os três cenários mostram o quanto a conclusão depende da hipótese.', 'Número redondo sem fonte não vale; linha em branco declarada vale.'],
  ['Trocar cada referência por cotação escrita.', 'Conferir impostos e taxas com contador.'], 'Fechar com cotações e seguir ao Capital e decisão.'),
 (7, 'ETAPA 4 · FECHAR A CONTA', 'Capital e decisão', 'Dossiê e decisão', 'Ajustar',
  [('Pedido de capital', 'Valor ainda não definido', 'N'), ('Limite de perda', 'Preenchido; confere com a renda do declarante', 'D'), ('Fontes consideradas', 'Recurso próprio e banco (hipóteses)', 'D'), ('O que falta', 'Cotações, licenças e curva do ano', 'V')],
  ['Precisar de dinheiro é diferente de precisar de um sócio.', 'Três caminhos: fazer sozinho, levar a banco ou investidor, ou conversar com a Zion, que avalia cada caso.', 'O projeto anda na velocidade da página mais fraca: não é votação.'],
  ['Fechar as páginas fracas antes de pedir capital.', 'Definir o valor do pedido a partir da Pré-viabilidade.'], 'Ajustar e voltar a gerar o Dossiê.'),
]

def foot(n, extra=''):
    return f'<div class="foot"><span>Meu terreno. Minha visão. Meu projeto. · Exemplo com dados fictícios{extra}</span><span>{n}</span></div>'

pages = []
# capa
rows = '<div class="etapa">Marco Zero · ponto de partida</div><div class="pill"><span class="n">0</span><span class="t"><b>Diagnóstico prévio</b><span>A página zero do seu Dossiê</span></span><span class="chip f">Feita</span></div>'
last = None
for n, et, nome, ent, vd, *_ in P:
    if et != last:
        rows += f'<div class="etapa">{et}</div>'; last = et
    rows += f'<div class="pill"><span class="n">{n}</span><span class="t"><b>{nome}</b><span>{ent}</span></span><span style="font-size:8.5pt;color:var(--areia);margin-right:2mm">{vd}</span><span class="chip f">Feita</span></div>'
pages.append(f'''<section class="pg dark cover">
<img src="file:///home/user/zion-hotel-ai-developer/docs/brand/zion-logo-claro.png" style="height:11mm;position:absolute;top:18mm;left:20mm" alt="">
<div class="badge">Exemplo ilustrativo · dados fictícios</div>
<div style="position:absolute;left:20mm;right:20mm;top:38mm"><p class="eyebrow">Zion Collection · Dossiê de estruturação · os 7 pilares</p>
<h1 style="font-size:27pt;white-space:nowrap">Meu terreno. Minha visão. <em>Meu projeto.</em></h1><hr class="rule" style="margin:4mm 0">
<p style="font-size:9.5pt;color:var(--areia)"><b style="color:var(--creme)">Empreendedor:</b> Proprietário Exemplo · <b style="color:var(--creme)">Propriedade:</b> Terreno Exemplo (fictício)</p>
<div style="margin-top:3mm">{rows}</div></div>
<div style="position:absolute;left:20mm;right:20mm;bottom:16mm;font-size:7.5pt;color:var(--areia)">Documento de organização das informações declaradas pelo empreendedor. Não é promessa de investimento, parceria ou resultado, nem projeto executivo ou laudo.</div></section>''')
# como ler
pages.append(f'''<section class="pg"><p class="eyebrow">Como ler este documento</p><h2 style="font-size:30pt">Três partes. <em style="color:var(--terra)">Um projeto seu.</em></h2><hr class="rule">
<div class="grid" style="grid-template-columns:1fr;gap:4mm">
<div class="box"><span class="part">Parte 1 · Pilares 1 e 2 e Marco Zero</span><h3>Meu terreno</h3><p class="sm">As características do terreno e da região, o que existe de infraestrutura e o que falta, e o mercado em volta. Fotos do terreno entram aqui.</p></div>
<div class="box"><span class="part">Parte 2 · Pilares 3, 4 e 5</span><h3>Minha visão</h3><p class="sm">A ideia com as próprias palavras: o produto, o público, o modelo de negócio e o desenho do terreno inteiro, em fases.</p></div>
<div class="box"><span class="part">Parte 3 · Pilares 6 e 7</span><h3>Meu projeto</h3><p class="sm">A conta de referência, os três cenários, o capital e a decisão: avançar, ajustar ou parar.</p></div></div>
<h3 style="font-size:16pt;margin-top:8mm">Em cada página, três marcas</h3>
<p class="sm">{tag('D')} o que você preencheu. {tag('O')} a leitura do método. {tag('V')} o que precisa ser conferido fora da plataforma. {tag('N')} o que você marcou como "não sei": vira o que falta descobrir.</p>
<p class="aviso">Cada pilar ocupa duas páginas: a primeira com o que foi declarado; a segunda com a leitura do método, o veredito, o que falta verificar e o próximo passo.</p>{foot(2)}</section>''')
# marco zero
pages.append(f'''<section class="pg"><span class="part">Marco Zero · página 0</span><h2 style="font-size:28pt;margin:2mm 0">Diagnóstico prévio</h2><hr class="rule">
<div class="camp"><b>Objetivo</b><span>Estruturar um projeto de 6 chalés em terreno próprio (fictício)</span><span class="tg">{tag('D')}</span></div>
<div class="camp"><b>Fase da ideia</b><span>Terreno parado, sem projeto escrito</span><span class="tg">{tag('D')}</span></div>
<div class="camp"><b>Experiência em hospedagem</b><span>Não sei</span><span class="tg">{tag('N')}</span></div>
<div class="camp"><b>Maior dúvida hoje</b><span>Por onde começar e quanto custa a primeira fase</span><span class="tg">{tag('D')}</span></div>
<div class="sec"><h3>Fotos do terreno</h3><div class="ph">Espaço para até 6 fotos anexadas pelo empreendedor<br>(sem foto neste exemplo)</div></div>
<div class="sec"><h3>Leitura do método</h3><p class="sm">{tag('O')} O diagnóstico não dá veredito: ele marca o ponto de partida e mostra quais pilares pedem mais atenção. Terreno parado quase nunca é falta de dinheiro; é falta de ordem.</p></div>{foot(3)}</section>''')
n = 4
for num, et, nome, ent, vd, campos, leitura, verif, prox in P:
    c = ''.join(f'<div class="camp"><b>{html.escape(r)}</b><span>{html.escape(v)}</span><span class="tg">{tag(k)}</span></div>' for r, v, k in campos)
    pages.append(f'''<section class="pg"><span class="part">{et} · Pilar {num}</span><h2 style="font-size:28pt;margin:2mm 0">{nome}</h2><p class="sm" style="color:var(--terra)">{ent} · página {num} do Dossiê · 1 de 2: o que você declarou</p><hr class="rule">{c}
<div class="sec"><h3>Fotos e anexos</h3><div class="ph" style="height:30mm">Espaço reservado para fotos e anotações deste pilar (sem anexo neste exemplo)</div></div>{foot(n, f' · Pilar {num}')}</section>''')
    n += 1
    lt = ''.join(f'<li>{html.escape(x)}</li>' for x in leitura); vt = ''.join(f'<li>{html.escape(x)}</li>' for x in verif)
    pages.append(f'''<section class="pg"><span class="part">{et} · Pilar {num}</span><h2 style="font-size:28pt;margin:2mm 0">{nome}</h2><p class="sm" style="color:var(--terra)">2 de 2: leitura, veredito e próximo passo</p><hr class="rule">
<div class="sec" style="margin-top:0"><h3>Veredito desta página</h3><span class="vd">{vd}</span><p class="aviso" style="margin-top:2mm">Veredito de referência, calculado com o que foi declarado. Não é garantia nem parecer técnico.</p></div>
<div class="sec"><h3>Leitura do método {tag('O')}</h3><ul class="s sm">{lt}</ul></div>
<div class="sec"><h3>O que falta verificar {tag('V')}</h3><ul class="s sm">{vt}</ul></div>
<div class="sec"><h3>Próximo passo</h3><p class="quote">{html.escape(prox)}</p></div>{foot(n, f' · Pilar {num}')}</section>''')
    n += 1
# decisão
rows = ''.join(f'<tr><td>{p[0]}. {p[2]}</td><td>{p[4]}</td><td>{p[6][0] if False else html.escape(p[7][0])}</td></tr>' for p in P)
pages.append(f'''<section class="pg dark"><p class="eyebrow">Decisão do Dossiê</p><h2 style="font-size:34pt">Ajustar</h2><hr class="rule">
<p style="font-size:11pt;color:var(--areia);max-width:140mm">O projeto anda na velocidade da página mais fraca. Neste exemplo, as páginas de Mercado, Pré-viabilidade e Masterplan pedem ajuste antes de avançar.</p>
<table style="color:var(--creme)"><tr><th style="color:var(--ouro)">Pilar</th><th style="color:var(--ouro)">Veredito</th><th style="color:var(--ouro)">Primeira verificação</th></tr>{rows}</table>
<p style="font-size:9pt;color:var(--areia);margin-top:8mm">Caminhos: fazer sozinho, levar a um banco ou a um investidor, ou conversar com a Zion, que avalia cada caso, sujeito à análise e à agenda. Parceria e investimento não são garantidos.</p>
<div class="foot"><span>Exemplo ilustrativo · todos os dados são fictícios · não é promessa de resultado</span><span>{n}</span></div></section>''')

out = '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Dossiê completo · Exemplo</title>' + css + '</head><body>' + ''.join(pages) + '</body></html>'
open('exemplo-completo.html', 'w', encoding='utf-8').write(out)
print('paginas', len(pages))
