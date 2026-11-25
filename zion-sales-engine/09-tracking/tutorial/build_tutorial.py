#!/usr/bin/env python3
"""Gera index.html do tutorial de rastreamento (Python 3, biblioteca padrao). Rode: python3 build_tutorial.py"""
from pathlib import Path
from html import escape

OUT = Path(__file__).parent / "index.html"
NC = '<span class="nc">NC</span>'
E = '<span class="e">confirmado</span>'


def step(code, title, body, onde=None, ver=None, print_=None, cuidado=None, mock=None):
    h = f'<div class="step" id="{code.lower()}"><div class="num">{code}</div><div><h3>{title}</h3>{body}'
    if mock:
        h += mock
    if onde:
        h += f'<div class="box onde"><b class="t">Onde clicar</b>{onde}</div>'
    if ver:
        h += f'<div class="box ver"><b class="t">O que você deve ver</b>{ver}</div>'
    if cuidado:
        h += f'<div class="box cuidado"><b class="t">Cuidado</b>{cuidado}</div>'
    if print_:
        h += f'<div class="box print"><b class="t">O que me enviar (print)</b>{print_}</div>'
    return h + '</div></div>'


def mock(rows, title=None):
    h = '<div class="mock">'
    if title:
        h += f'<div class="row"><b>{title}</b></div>'
    for r in rows:
        h += f'<div class="row">{r}</div>'
    return h + '</div>'


def sec(id_, title, lead, content, pb=False):
    return f'<section id="{id_}"{" class=\"pb\"" if pb else ""}><h2>{title}</h2><p class="lead">{lead}</p>{content}</section>'


PIXEL = "903918118859018"
TEST_URL = ("https://infoprodutos-zion.clickmax.space/mini-mentoria?utm_source=meta&amp;utm_medium=paid&amp;utm_campaign=teste-rastreamento"
            "&amp;utm_content=teste01&amp;utm_term=900000000000001&amp;sck=900000000000002&amp;ad_id=900000000000001"
            "&amp;campaign_id=900000000000002&amp;adset_id=900000000000003")
CHANNEL_URL = ("https://infoprodutos-zion.clickmax.space/mini-mentoria?utm_source=whatsapp&amp;utm_medium=bela&amp;utm_campaign=teste-canal&amp;src=whatsapp_bela")

# ---------------------------------------------------------------- A) ClickMax
A = ""
A += step("A1", "Abra a lista de pixels",
          "<p>É aqui que o pixel é cadastrado e que você liga a API de Conversões. A tela é só lista e cadastro; <b>onde</b> o pixel rastreia se escolhe dentro de cada produto, oferta ou página.</p>",
          onde="Menu lateral &rsaquo; <b>Marketing</b> &rsaquo; <b>Tráfego</b> &rsaquo; <b>Pixel e trackeamento</b>. " + E,
          ver=f"Uma lista com o pixel de apelido que você deu, ID <span class=\"mono\">{PIXEL}</span>, plataforma Meta e situação <b>Ativo</b>.",
          print_="Print da lista inteira (pode cobrir o que não for o pixel).",
          mock=mock(['<span>Tráfego &rsaquo; Pixel e trackeamento</span><span class="btn">Adicionar pixel</span>',
                     f'<span>Apelido do pixel &middot; Meta &middot; {PIXEL}</span><span class="pill p-ok">Ativo</span><span class="btn hl">&#8943; ações</span>']))
A += step("A2", "Veja onde o pixel está sendo usado e se tem credencial",
          "<p>O quadro no topo diz se a <b>API de Conversões</b> tem <b>Credencial configurada</b> ou está <b>Sem credencial</b>. Abaixo, o bloco <b>Onde este pixel está</b> lista cada tela que escolheu o pixel (Produto, Oferta, Página, Funil…).</p>",
          onde="Na linha do pixel, abra o menu de ações (&#8943;) &rsaquo; <b>Ver detalhes</b>. " + E,
          ver="Em <b>Onde este pixel está</b>: uma linha de <b>Produto</b> e uma de <b>Oferta</b> para cada oferta vendida (Mini Mentoria R$ 47, R$ 97, R$ 47). Se faltar, o checkout dessa oferta não manda evento.",
          print_="Print do topo (Credencial) e do bloco \"Onde este pixel está\".",
          mock=mock(['<span>Plataforma Meta &middot; ID</span><span>API de Conversões: <span class="pill p-wip hl">Credencial configurada / Sem credencial</span></span>',
                     '<span>Produto &middot; nome do produto</span><span class="btn">Remover</span>',
                     '<span>Oferta &middot; nome da oferta</span><span class="btn">Remover</span>',
                     '<span>Página &middot; /mini-mentoria</span><span class="btn">Remover</span>'], "Onde este pixel está"))
A += step("A3", "Ligue a API de Conversões e cole o token (você mesmo, nunca no chat)",
          "<p>Sem token, o evento de venda sai só pelo navegador, e é o motivo mais comum de \"o Meta não recebeu minha venda no Pix\". O token fica escondido depois de salvo (\"Token guardado\").</p>"
          "<p>Para gerar o token: Meta &rsaquo; Gerenciador de Eventos &rsaquo; seu conjunto de dados &rsaquo; Configurações &rsaquo; API de Conversões &rsaquo; gerar token de acesso " + NC + " (o nome exato do botão muda; procure por <i>API de Conversões</i> e <i>token de acesso</i>).</p>",
          onde="Menu de ações do pixel &rsaquo; <b>Editar</b> &rsaquo; bloco <b>API de Conversões da Meta</b>: ligue <b>Usar API de Conversão</b>, cole o <b>Token de acesso</b> e clique <b>Testar token</b>. O campo <b>Código de teste</b> só se preenche durante os testes. " + E + " (a posição exata da chave \"Usar API de Conversão\" " + NC + ")",
          ver="Depois do teste, mensagem de sucesso (o teste envia um evento de teste, que não conta como compra). Se aparecer <b>Token recusado</b>: gere outro token e cole de novo. Ao reabrir, aparece <b>Token guardado</b> com <b>Trocar token</b> e <b>Remover</b>.",
          cuidado="Enquanto o <b>Código de teste</b> estiver preenchido, os eventos aparecem só na aba Testar eventos da Meta e <b>não contam</b> como conversão. Limpe o campo antes de rodar anúncio de verdade.",
          print_="Print do bloco SEM mostrar o token (ele não aparece mesmo). Mostre a mensagem do <b>Testar token</b> e o estado \"Token guardado\".",
          mock=mock(['<span>Usar API de Conversão</span><span class="sw"></span>',
                     '<span>Token de acesso</span><span class="mono">&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull; (Token guardado)</span>',
                     '<span class="btn hl">Testar token</span><span class="btn">Trocar token</span><span class="btn">Remover</span>',
                     '<span>Código de teste</span><span class="mono hl">(vazio em produção)</span>'], "API de Conversões da Meta"))
A += step("A4", "Confira os eventos: Comprou e Abriu o checkout",
          "<p>O pixel tem 13 eventos, cada um com dois interruptores: <b>No navegador</b> e <b>Pelo servidor</b>. Quando o mesmo evento vai pelos dois caminhos, a Meta conta <b>uma</b> conversão (mesmo identificador). Duas linhas importam agora:</p>"
          "<ul><li><b>Comprou</b> (vira <code>Purchase</code>): navegador <b>e</b> servidor ligados; em <b>Formas de pagamento</b>, <b>Pix e cartão</b> marcados. Se desmarcar Pix, a venda paga no Pix não gera evento nenhum.</li>"
          "<li><b>Abriu o checkout</b> (hoje <code>InitiateCheckout</code>): ligue <b>Só contar depois dos dados pessoais</b>. Assim o evento só conta quando a pessoa informa nome e e-mail, e deixa de ser igual a \"viu a página\".</li></ul>",
          onde="Menu de ações &rsaquo; <b>Editar</b> &rsaquo; passo <b>Eventos</b> (lista dos 13 eventos). " + E,
          ver="Linha <b>Comprou</b> com dois interruptores verdes e as formas de pagamento marcadas; linha <b>Abriu o checkout</b> com a opção de dados pessoais ligada.",
          cuidado="NÃO clique em <b>Ativar eventos novos</b> sem falar com quem cuida dos anúncios: esse botão troca o nome <code>InitiateCheckout</code> por <code>AddToCart</code> (e outros), e campanha que otimiza pelo nome antigo perde a base. Só com \"aprovado\".",
          print_="Print da linha <b>Comprou</b> (com Formas de pagamento) e da linha <b>Abriu o checkout</b>. Se aparecer o aviso <b>Eventos novos disponíveis</b>, mande print dele (sem clicar).",
          mock=mock(['<span>Comprou &middot; Purchase</span><span>Navegador <span class="sw"></span> Servidor <span class="sw"></span></span>',
                     '<span class="hl">Formas de pagamento: [x] Pix [x] Cartão</span>',
                     '<span>Abriu o checkout &middot; InitiateCheckout</span><span>Navegador <span class="sw"></span> Servidor <span class="sw"></span></span>',
                     '<span class="hl">Só contar depois dos dados pessoais</span><span class="sw"></span>'], "Eventos"))
A += step("A5", "Leia o Histórico de envio: a resposta de \"por que não chegou\"",
          "<p>Cada linha é um evento que o <b>servidor</b> do ClickMax tentou mandar à Meta. Eventos só do navegador não aparecem aqui (zero aqui não prova que o pixel não dispara).</p>"
          "<table><tr><th>Resultado</th><th>Significa</th></tr><tr><td>Enviado</td><td>A Meta recebeu</td></tr><tr><td>Falhou</td><td>Tentativa não completou; o ClickMax tenta de novo</td></tr>"
          "<tr><td>Não enviado</td><td>Alguma configuração impediu; o motivo está na linha (evento desligado, falta token, espera dados pessoais, Meta recusou, passou de 7 dias)</td></tr><tr><td>Em andamento</td><td>Ainda enviando</td></tr></table>",
          onde="Menu de ações do pixel &rsaquo; <b>Histórico de envio</b> (ou, em <b>Ver detalhes</b>, role até o bloco de histórico). Use os botões <b>Todos / Enviados / Falharam / Não enviados</b>. " + E,
          ver="Depois da correção: linhas <b>Purchase &middot; Enviado</b> e, na linha aceita, o <b>ID de rastreio (fbtrace_id)</b>. Hoje o esperado é o oposto: vazio ou \"Não enviado\" com motivo.",
          print_="Print do histórico das <b>linhas da data das compras reais em diante</b> (com data, evento, resultado e motivo). Se houver linha de Purchase, mande print dela aberta.",
          mock=mock(['<span>Todos 0 &middot; Enviados 0 &middot; Falharam 0 &middot; Não enviados 0</span>',
                     '<span>Purchase &middot; dd/mm hh:mm (exemplo)</span><span class="pill p-no">Não enviado</span><span>motivo na linha</span>',
                     '<span>Purchase &middot; data</span><span class="pill p-ok">Enviado</span><span class="mono">fbtrace_id</span>'], "Histórico de envio"))
A += step("A6", "Marque o pixel no produto e na oferta (aba Pixels)",
          "<p>O checkout segue o pixel marcado no <b>produto/oferta</b>, não o da página. Se o evento aparece na página e não no checkout, é este o motivo.</p>",
          onde="<b>Produtos</b> &rsaquo; abra o produto &rsaquo; aba <b>Pixels</b> (\"Pixels deste produto\") e, dentro dele, abra a <b>oferta</b> (\"Pixels desta oferta\"). Cada caixa marcada é salva na hora. " + E,
          ver="O pixel com a caixa marcada, em cada oferta que você vende.",
          print_="Print da aba Pixels do produto da Mini Mentoria e da oferta R$ 47. Repita para R$ 97 e para o produto/oferta do R$ 47 do Clube se houver anúncio ativo para eles.")
A += step("A7", "Confira o que um contato recebeu (aba Eventos de pixel)",
          "<p>Na ficha de quem comprou, a aba mostra cada evento e, por pixel, os selos <b>Navegador</b> e <b>Servidor</b> (enviado, enviando, falhou, não enviado, com motivo).</p>",
          onde="<b>Contatos</b> &rsaquo; abra o contato de teste &rsaquo; aba <b>Eventos de pixel</b>. Precisa de permissão para ver <b>Tráfego</b>. " + E,
          ver="Depois da compra de teste: <b>Purchase</b> com selo <b>Conversão</b>, <b>Navegador</b> verde e <b>Servidor &middot; enviado</b> verde.",
          print_="Print da linha Purchase da compra de teste.")
A += step("A8", "Webhook (só se a correção nativa falhar: opção C)",
          "<p>Não faça agora. Se o teste D mostrar que o Purchase pago não chega, o Claude entrega o receptor pronto (<span class=\"mono\">capi-webhook/</span>) e o JSON para colar. O caminho é: produto &rsaquo; oferta &rsaquo; <b>entrega do tipo webhook</b> (URL, método, autenticação personalizada, eventos, <b>Personalizar payload</b>, <b>Enviar teste</b>, <b>Ver payload</b>). " + E + " Quais eventos a lista oferece: " + NC + ".</p>",
          print_="Se quiser adiantar: print da tela de entrega tipo webhook com a lista <b>Selecione os eventos para disparo</b> aberta.")

# ---------------------------------------------------------------- B) Meta
B = ""
B += step("B1", "Abra o Gerenciador de Eventos",
          "<p>É o único lugar que mostra tudo o que o Meta realmente recebeu (navegador e servidor), inclusive compras sem atribuição a anúncio. O relatório de anúncios mostra só o que o Meta atribuiu.</p>",
          onde="Meta Business (business.facebook.com) &rsaquo; menu &rsaquo; <b>Gerenciador de Eventos</b> (também aparece como \"Fontes de dados\") " + NC + ". Escolha a conta de negócios certa.",
          ver="Lista de fontes de dados (pixels/conjuntos de dados).",
          print_="Print da lista de fontes de dados (pode borrar nomes que não sejam da Zion).")
B += step("B2", "Escolha o dataset do pixel " + PIXEL + " e veja a ligação",
          "<p>Hoje o Meta chama o pixel de <b>conjunto de dados</b>; os dois costumam ser o mesmo objeto. Confira que o ID é <span class=\"mono\">" + PIXEL + "</span> e que está ligado à conta de anúncios usada nas campanhas.</p>",
          onde="Gerenciador de Eventos &rsaquo; clique na fonte de dados <b>" + PIXEL + "</b> &rsaquo; aba <b>Configurações</b>. Procure o ID do pixel/conjunto de dados, <b>API de Conversões</b> e <b>contas de anúncios/ativos</b> vinculados " + NC + ".",
          ver="O mesmo ID do pixel que está no ClickMax; a conta de anúncios das campanhas aparece como vinculada; a API de Conversões mostra o método de conexão (parceiro/manual).",
          print_="Print do topo da Visão geral (com o ID) e da área de Configurações que mostra contas vinculadas e a API de Conversões.")
B += step("B3", "Visão geral: o Purchase das compras reais existe?",
          "<p>Esta é a <b>pergunta 1</b> antes de qualquer reenvio das compras reais sem UTM. Se o Purchase já está lá, não reenvie.</p>",
          onde="Gerenciador de Eventos &rsaquo; fonte de dados &rsaquo; <b>Visão geral</b> &rsaquo; ajuste o período para <b>da data da primeira compra real até hoje</b> &rsaquo; clique no evento <b>Purchase</b> (ou <b>Compra</b>). Procure a coluna de <b>Origem</b> (Navegador, Servidor, Navegador e Servidor), o <b>valor</b> e a <b>moeda</b> " + NC + ".",
          ver="Esperado depois da correção: Purchase com <b>Navegador e Servidor</b> (ou só <b>Servidor</b> para Pix), valor 47,00 ou 97,00, BRL. Hoje, pela auditoria, o esperado é nenhum Purchase.",
          print_="Print da Visão geral com o intervalo e a linha do Purchase (ou da falta dele); se existir, print dos detalhes com valor e moeda.")
B += step("B4", "Testar eventos: ver o evento chegando em tempo real",
          "<p>Mostra eventos de teste na hora. Para o <b>servidor</b> do ClickMax aparecer aqui, cole o <b>código de teste</b> (<span class=\"mono\">TEST...</span>) no campo <b>Código de teste</b> do pixel no ClickMax (passo A3) durante o teste, e limpe depois.</p>",
          onde="Gerenciador de Eventos &rsaquo; fonte de dados &rsaquo; aba <b>Testar eventos</b>. Copie o código de teste mostrado ali " + NC + ".",
          ver="Linhas de evento em tempo real, cada uma com origem <b>Navegador</b> ou <b>Servidor</b>. Clique na linha para ver <code>value</code>, <code>currency</code> e <code>event_id</code>.",
          cuidado="O código de teste vai só no ClickMax, e é você que cola. Não mande o código por e-mail nem o deixe lá depois do teste.",
          print_="Print da lista de eventos do teste e de um evento Purchase aberto (parâmetros).")
B += step("B5", "Diagnóstico",
          "<p>Mostra alertas do Meta sobre o que está errado nos eventos.</p>",
          onde="Gerenciador de Eventos &rsaquo; fonte de dados &rsaquo; aba <b>Diagnóstico</b> " + NC + " (se o nome mudou, procure por \"problemas\" ou \"alertas\").",
          ver="Sem alerta como \"parâmetros ausentes (valor/moeda)\", \"eventos duplicados\", \"event_id ausente\" ou \"correspondência baixa\".",
          print_="Print da aba inteira, com cada alerta aberto se houver.")
B += step("B6", "Qualidade de correspondência e Deduplicação",
          "<p><b>Qualidade de correspondência</b> (EMQ) é a nota de quão bem o Meta consegue ligar o evento a uma pessoa. <b>Deduplicação</b> mostra se evento do navegador e do servidor estão sendo contados como um só.</p>",
          onde="Visão geral &rsaquo; clique no evento <b>Purchase</b> &rsaquo; procure os cartões <b>Qualidade da correspondência de eventos</b> e <b>Deduplicação</b> (ou \"Eventos desduplicados\") " + NC + ".",
          ver="EMQ do Purchase com nota 6 ou mais (e-mail e telefone chegando). Deduplicação: Purchase de navegador + servidor com o mesmo <code>event_id</code> contado uma vez.",
          print_="Print dos dois cartões para o Purchase.")
B += step("B7", "Parâmetros de URL no anúncio (para a UTM padrão)",
          "<p>O Meta preenche as macros por anúncio. O texto padrão fica em <span class=\"mono\">PLANO_EXECUTAVEL.md</span> (seção 1.7). Mexer em anúncio ativo exige \"aprovado\" e pode reiniciar a revisão do anúncio.</p>",
          onde="Gerenciador de Anúncios &rsaquo; edite o <b>anúncio</b> &rsaquo; seção de rastreamento &rsaquo; <b>Parâmetros de URL</b> " + NC + ".",
          ver="O campo de parâmetros com o texto padrão (utm_source=meta&amp;utm_medium=paid&amp;&hellip;&amp;adset_id={{adset.id}}). Veja o padrão completo em <code>09-tracking/PADRAO_UTM.md</code> (<code>utm_campaign=mm47</code>; os ids de teste do passo D abaixo são fictícios).",
          print_="Por ora, print do campo <b>Parâmetros de URL</b> de 1 anúncio de cada campanha ativa (para eu comparar com o padrão).")

# ---------------------------------------------------------------- C) Ticto
C = ""
C += step("C1", "Extrato de vendas com todos os status",
          "<p>A Ticto processa o pagamento por trás do checkout do ClickMax. O extrato dela mostra o que o ClickMax pode não mostrar: Pix gerado e vencido, cartão recusado, antifraude. Sem acesso ao painel e à documentação da Ticto, <b>não consegui confirmar os nomes dos menus</b>. " + NC + "</p>",
          onde="Entre na Ticto (ticto.com.br). Procure no menu por <b>Vendas</b>, <b>Pedidos</b> ou <b>Relatórios</b> e use o filtro de <b>período</b> (22 a 25/11) e de <b>status</b> (todos). Se existir <b>Exportar</b>, exporte.",
          ver="Lista de pedidos com status (aprovado/pago, aguardando pagamento, Pix expirado, recusado, reembolsado).",
          print_="Print do extrato filtrado 22 a 25/11 <b>com todos os status</b> (borre nome, e-mail e telefone). Se exportar planilha, <b>não</b> a envie: guarde fora do repositório; me diga só as colunas.")
C += step("C2", "Pix expirado e recusas",
          "<p>O ClickMax só registra o que a Ticto repassa. Pix gerado que venceu dentro da Ticto e cartão recusado podem existir só lá.</p>",
          onde="No mesmo extrato, filtre por status <b>Pix expirado</b> e <b>recusado/negado</b> (os nomes exatos " + NC + ").",
          ver="A contagem de Pix gerados × pagos, e o motivo de cada recusa (se a Ticto mostra).",
          print_="Print dos filtros e das contagens (sem dados pessoais).")
C += step("C3", "Parâmetros e UTMs (src, sck, utm_*) na venda",
          "<p>O ClickMax recebe <code>utm_*</code>, <code>src</code> e <code>sck</code> pela URL e guarda na venda; não está provado que a Ticto também os guarde ou devolva. É o que este passo descobre. " + NC + "</p>",
          onde="Abra <b>uma venda</b> (use a compra de teste) e procure campos como <b>origem</b>, <b>UTM</b>, <b>parâmetros</b>, <b>src</b>, <b>sck</b> ou <b>URL do checkout</b>. Anote os nomes que aparecem.",
          ver="Se a Ticto guarda: os valores do link de teste (utm_campaign=teste-rastreamento, sck=900000000000002). Se não guarda: campo vazio ou inexistente; isso não é problema, o ClickMax guarda do lado dele.",
          print_="Print da tela de detalhe da venda de teste (borre dados pessoais), mostrando os campos de origem/UTM ou a ausência deles.")
C += step("C4", "Webhooks cadastrados e histórico de envios",
          "<p>O ClickMax recebe os eventos da Ticto por webhook. Se um evento não chega, a Ticto mostra a falha e a resposta do servidor.</p>",
          onde="Ticto &rsaquo; <b>Tictools</b> &rsaquo; <b>Webhooks</b> (abra a pasta com o ícone de olho). Cada webhook mostra a versão (deve ser <b>2.0</b>), formato <b>JSON</b>, itens enviados e os eventos marcados. O histórico de envios tem <b>Detalhes do evento</b> com a resposta do servidor. " + E + " (via documentação do ClickMax)",
          ver="Webhook do ClickMax na versão 2.0, JSON, com <b>Enviar Order Bump / Combo junto com a oferta principal</b>, e eventos: Venda Realizada, Pix Gerado, Pix Expirado, Reembolso, Chargeback etc.",
          print_="Print da lista de webhooks e dos eventos marcados do webhook do ClickMax (<b>cubra o token</b>, ele é segredo).")
C += step("C5", "Pixel da Ticto",
          "<p>Se a Ticto tiver pixel próprio ligado a este produto, ele poderia duplicar o Purchase. Não há sinal de que exista, mas só o painel dela confirma. " + NC + "</p>",
          onde="Ticto &rsaquo; seu produto &rsaquo; procure uma seção chamada <b>Pixel</b>, <b>Integrações</b>, <b>Rastreamento</b> ou <b>Facebook/Meta</b>.",
          ver="Ou nada configurado (esperado) ou um pixel com o ID <span class=\"mono\">" + PIXEL + "</span> ou outro.",
          print_="Print da seção, ou a mensagem \"não encontrei\" e onde você procurou.")

# ---------------------------------------------------------------- D) Compra de teste
D = ""
D += step("D0", "Antes de comprar",
          "<ul><li>Use <b>e-mail e telefone seus</b> (do contato de teste). A compra é real e <b>reembolsável</b> (7 dias, CDC).</li>"
          "<li>Janela anônima, <b>sem bloqueador de anúncio</b>; se possível, repita uma vez no celular.</li>"
          "<li>Publicada é o que vale: o rastreamento <b>não roda no preview do editor</b>.</li>"
          "<li>Anote o horário de cada passo (ajuda a achar o evento).</li>"
          "<li><b>Rodada 1</b>: cole o <b>código de teste</b> da Meta no pixel do ClickMax (A3) e abra B4 (Testar eventos). <b>Rodada 2</b>: sem código de teste.</li></ul>",
          print_="Nada ainda. Só confirme que fez A1–A5 e mandou os prints.")
D += step("D1", "Link de teste com UTM completa",
          "<p>Use este link (ids fictícios que começam com <b>9000</b>, para nunca se confundir com anúncio real):</p>"
          f"<pre>{TEST_URL}</pre>"
          "<p>Variante com ancora (para ver se a UTM sobrevive ao <code>#pagar</code>):</p>"
          f"<pre>{TEST_URL}#pagar</pre>",
          ver="Depois que a página carrega, a barra de endereço <b>ainda mostra</b> <code>?utm_source=meta&hellip;</code>. Se o <code>#pagar</code> faz sumir a UTM, anote.",
          print_="Print da barra de endereço com a página carregada (link sem e com <code>#pagar</code>).")
D += step("D2", "Abra a página, sem rolar e sem clicar",
          "<p>Deixe 30 segundos. No Testar eventos você deve ver <code>PageView</code>. Não deve aparecer <code>InitiateCheckout</code> ainda (se o passo A4 foi feito).</p>",
          ver="<code>PageView</code> sim; <code>InitiateCheckout</code> <b>não</b> (R1 do início da compra).",
          print_="Print do Testar eventos neste momento.")
D += step("D3", "Preencha nome e e-mail no checkout",
          "<p>Pare antes de escolher Pix ou cartão.</p>",
          ver="<code>InitiateCheckout</code> aparece <b>uma</b> vez (o início efetivo da compra).",
          print_="Print do Testar eventos com a linha do evento.")
D += step("D4", "Escolha Pix e gere o código (NÃO pague)",
          "<p>Espere 2 minutos olhando o Testar eventos. Esta é a prova principal contra o defeito \"Purchase no Pix gerado\" (critérios R1 e R8).</p>",
          ver="Pode aparecer <code>AddPaymentInfo</code>. <b>Nenhum</b> <code>Purchase</code>.",
          cuidado="Se aparecer Purchase aqui, <b>pare</b> e me mande o print: o defeito está confirmado e vamos para a opção C.",
          print_="Print do Testar eventos depois de 2 minutos, e da venda <b>pendente</b> em ClickMax &rsaquo; <b>Vendas</b> (se aparecer): veja se as UTMs do link já estão gravadas nela " + NC + ".")
D += step("D5", "Pague o Pix",
          "<p>Pague o Pix do valor da oferta pelo app do seu banco. Aguarde até 5 minutos.</p>",
          ver="<b>Um</b> <code>Purchase</code>, origem <b>Servidor</b> (e <b>Navegador</b> se a aba ainda estiver aberta), <code>value</code> = valor da oferta (47,00), <code>currency</code> = BRL, mesmo <code>event_id</code> nas duas origens.",
          cuidado="<code>value</code> 0,47, 4700 ou 0 = erro de unidade (R2 falha). Mais de um Purchase = duplicidade (R4 falha).",
          print_="Print do Purchase aberto (parâmetros: value, currency, event_id) nas duas origens.")
D += step("D6", "Confira no ClickMax",
          "<ul><li><b>Vendas</b>: a venda aparece como <b>Paga</b>; abra e veja se <b>utm_source/medium/campaign/content/term</b>, <b>src</b> e <b>sck</b> vieram do link de teste.</li>"
          "<li>Pixel &rsaquo; <b>Histórico de envio</b>: linha <b>Purchase &middot; Enviado</b>, e <b>nenhum</b> Purchase para o Pix gerado.</li>"
          "<li>Contato &rsaquo; <b>Eventos de pixel</b>: Purchase com Servidor enviado.</li></ul>",
          print_="Print da venda (UTMs), do histórico de envio e da aba Eventos de pixel.")
D += step("D7", "Acesso entregue",
          "<p>Abra o e-mail do contato de teste e entre na área de membros. A regra do projeto: só vale se for provado o caminho todo, do pagamento ao acesso.</p>",
          ver="Em poucos minutos: e-mail com link de acesso, login funcionando, as aulas da turma da Mini Mentoria visíveis.",
          print_="Print da tela de acesso/aulas (sem dados pessoais) e a hora em que o e-mail chegou.")
D += step("D8", "Link de WhatsApp (sem pagar)",
          "<p>Prova a origem de canal sem gastar. Abra este link, gere um Pix e <b>não pague</b>:</p>"
          f"<pre>{CHANNEL_URL}</pre>",
          ver="Na venda pendente, a origem de canal (<code>utm_source=whatsapp</code>, <code>src=whatsapp_bela</code>) gravada. Anúncio original <b>não</b> aparece (é o esperado, ver plano 1.7).",
          print_="Print da venda pendente com as UTMs.")
D += step("D9", "Rodada 2: cartão, sem código de teste",
          "<p>Limpe o <b>Código de teste</b> do pixel (A3) e faça uma segunda compra pequena, desta vez por <b>cartão</b> (à vista). Dê até 20 minutos.</p>",
          ver="Na <b>Visão geral</b> do Meta, o Purchase aparece (com atraso), com Servidor; o cartão <b>Deduplicação</b> e o <b>Diagnóstico</b> sem alerta.",
          print_="Print da Visão geral (Purchase com origem), de Deduplicação e de Diagnóstico.")
D += step("D10", "Reembolse as compras de teste",
          "<p>Reembolso no ClickMax (ou na Ticto), nas duas compras de teste.</p>",
          ver="Venda <b>Reembolsada</b> e <b>nenhum Purchase novo</b> no Testar eventos, na Visão geral e no Histórico de envio.",
          cuidado="Nunca remova acesso de comprador real. O acesso do contato de teste é decisão sua.",
          print_="Print da venda reembolsada e do Histórico de envio depois do reembolso.")


# ---------------------------------------------------------------- E) Funil P0
EVT = """
<table><tr><th>#</th><th>Evento</th><th>Nome</th><th>Hoje</th><th>Onde conferir</th></tr>
<tr><td>1</td><td>Visualização da landing</td><td>PageView</td><td>ok</td><td>Testar eventos</td></tr>
<tr><td>2</td><td>Visualização da oferta</td><td>ViewContent (pixel) / element_visible (ClickMax)</td><td>desligado</td><td>Testar eventos / análise ClickMax</td></tr>
<tr><td>3</td><td>Clique no CTA com preço</td><td>button_click do botão (só no ClickMax)</td><td>mede no ClickMax</td><td>Análise de visitantes ClickMax</td></tr>
<tr><td>4</td><td>Início efetivo de checkout</td><td>InitiateCheckout</td><td>errado (iframe)</td><td>Testar eventos, Histórico de envio</td></tr>
<tr><td>5</td><td>Pix gerado</td><td>pix_generated (interno); PixGenerated só se o receptor for ligado</td><td>só interno</td><td>Vendas (pendente Pix), ficha do contato</td></tr>
<tr><td>6</td><td>Pagamento aprovado</td><td>Purchase</td><td>só após pago</td><td>Testar eventos, Histórico de envio, Vendas</td></tr>
<tr><td>7</td><td>Entrega do produto</td><td>membro na turma + e-mail de acesso</td><td>sem evento no Meta</td><td>Turma do portal, e-mail</td></tr></table>
<div class="box ver"><b class="t">Regras</b>O carregamento do checkout <b>não</b> é intenção. Pix gerado <b>não</b> é compra. Clique no CTA <b>com preço</b> é o clique qualificado.</div>"""

E_ = ""
E_ += step("E1", "Entenda os 7 eventos (leia antes de mexer)",
           "<p>O funil P0 separa quem viu, quem clicou sabendo o preço, quem começou a comprar, quem gerou Pix, quem pagou e quem recebeu. Esquema abaixo; detalhes no arquivo <span class=\"mono\">FUNIL_DE_EVENTOS_P0.md</span>.</p>" + EVT,
           print_="Nada a enviar neste passo.")
E_ += step("E2", "Confirme que o clique qualificado é medido no ClickMax (sem mexer em nada)",
           "<p>O ClickMax mede sozinho o clique em cada botão da página publicada (<code>button_click</code>, com o código do botão). Os 6 botões com preço da página nova de teste aparecem como <b>cta-0 a cta-5</b>. Esse número fica no ClickMax; <b>não vai ao Meta</b>. " + E + "</p>"
           "<p>Para ver: abra a página publicada em janela anônima, clique em um botão com preço e confira a lista de ações recentes.</p>",
           onde="<b>Visitantes</b> (análise e ações recentes) &rsaquo; ações das últimas 24 h, ou o funil da página em <b>Funis</b> &rsaquo; análise. A tela exata que lista cliques por botão: " + NC + ".",
           ver="Uma linha de clique com a página e (se identificado) o contato, logo depois do seu clique. Se você clicar em botões diferentes, o código do botão muda.",
           print_="Print da lista de ações recentes com o seu clique (borre nomes). Se a tela mostrar cliques por botão, print dela também.",
           mock=mock(['<span>Visitantes &rsaquo; Ações recentes</span><span class="btn">24 h</span>',
                      '<span>página /mini-mentoria-a</span><span class="pill p-ok">clique no botão</span><span class="mono">cta-2</span>'], "Esquema"))
E_ += step("E3", "Ligue \"Só contar depois dos dados pessoais\" (início efetivo de checkout)",
           "<p>Hoje o evento de início de checkout dispara ao <b>carregar</b> o checkout. Com a opção ligada, só conta quando a pessoa informa nome e e-mail. É a mesma chave do passo A4. " + E + "</p>",
           onde="<b>Marketing</b> &rsaquo; <b>Tráfego</b> &rsaquo; <b>Pixel e trackeamento</b> &rsaquo; &#8943; &rsaquo; <b>Editar</b> &rsaquo; passo <b>Eventos</b> &rsaquo; linha <b>Abriu o checkout</b> &rsaquo; <b>Só contar depois dos dados pessoais</b>. " + E,
           ver="Interruptor ligado. No teste: abrir o checkout sem preencher nada <b>não</b> gera o evento; depois de nome e e-mail, gera <b>um</b>.",
           cuidado="Não clique em <b>Ativar eventos novos</b> (troca <code>InitiateCheckout</code> por <code>AddToCart</code>). Só com \"aprovado\" e aviso a quem cuida dos anúncios.",
           print_="Print da linha <b>Abriu o checkout</b> com a opção ligada.")
E_ += step("E4", "Visualização da oferta: marque \"Página de conteúdo\" SÓ numa página de oferta nova",
           "<p>O ClickMax só envia <b>ViewContent</b> para a Meta se a página estiver marcada como <b>Página de conteúdo</b>; o evento sai quando a página <b>abre</b>. Numa landing única isso seria igual ao PageView, então a marcação faz sentido só numa <b>página de oferta separada</b> (landing &rarr; clique no botão com preço &rarr; página da oferta com o checkout). " + E + "</p>"
           "<p><b>Não marque</b> a página de checkout, de obrigado nem as páginas existentes (<span class=\"mono\">/mini-mentoria</span>, <span class=\"mono\">/inscricao-47</span>).</p>",
           onde="Página nova &rsaquo; editor &rsaquo; <b>Configurações da Página</b> &rsaquo; <b>Scripts</b> &rsaquo; ligue <b>Página de conteúdo</b> (salva na hora). Ou, no canvas do funil, abra a etapa &rsaquo; <b>Rastreamento</b>. " + E,
           ver="Na página publicada: <b>ViewContent</b> no Testar eventos ao abrir a página de oferta, e <b>nenhum</b> ViewContent na landing.",
           cuidado="Só em página <b>nova</b> e com \"aprovado\". Testar sempre na página publicada, nunca no preview do editor. Se a UTM some ao passar da landing para a oferta: " + NC + " (anote e me envie a URL antes e depois).",
           print_="Print da chave <b>Página de conteúdo</b> ligada na página de oferta e do Testar eventos mostrando ViewContent.",
           mock=mock(['<span>Landing (PageView)</span><span class="arrow-s">&rarr; botão R$47 &rarr;</span>',
                      '<span>Oferta <span class="pill p-ok hl">Página de conteúdo</span> (ViewContent)</span>',
                      '<span>Checkout (InitiateCheckout só após nome e e-mail)</span>'], "Esquema do desenho (d)"))
E_ += step("E5", "Pergunta ao painel: o funil tem ação \"enviar evento ao pixel\" no clique ou na rolagem?",
           "<p>Pela documentação, os gatilhos de página (clique no botão, rolagem, tempo na página) <b>só levam o contato para a próxima etapa do funil</b>; não há ação que dispare evento do pixel. Pode haver algo na tela que a documentação não cita. " + NC + "</p>",
           onde="<b>Funis</b> &rsaquo; abra o funil &rsaquo; clique na conexão entre duas etapas (ou nas configurações da etapa) &rsaquo; lista de <b>gatilhos</b> e de <b>ações</b>.",
           ver="A lista mostra gatilhos como <b>Clique no Botão</b>, <b>Scroll</b>, <b>Tempo na Página</b>. Se existir um campo \"enviar evento ao pixel\" ou \"evento personalizado\", é novidade: me mande o print.",
           print_="Print da tela de gatilhos/ações de uma conexão do funil (aberta, sem salvar nada).")
E_ += step("E6", "Visualização da oferta dentro da própria landing (opcional, só página nova)",
           "<p>Marcar a <b>seção da oferta</b> com <code>data-cx-track=\"visible\"</code> faz o ClickMax registrar <b>element_visible</b> quando a seção aparece na tela. " + E + " (mecanismo). Se o importador de páginas mantém o atributo: " + NC + ". Quem faz: o agente de páginas, <b>em página nova</b>, e depois você confere no E2 se a ação aparece.</p>",
           ver="Na lista de ações recentes, uma ação do tipo \"elemento visível\" ao rolar até a oferta. Se não aparecer, use o desenho do E4.",
           print_="Print da ação de elemento visível (ou da ausência dela).")
E_ += step("E7", "Pix gerado e Purchase: o que NÃO pode acontecer",
           "<ul><li>Gerar o Pix <b>não</b> pode criar <code>Purchase</code>. No Testar eventos pode aparecer <b>AddPaymentInfo</b> (escolheu a forma de pagamento), que <b>não é</b> Pix gerado nem compra.</li>"
           "<li>O ClickMax <b>não</b> manda \"Pix gerado\" ao Meta como evento próprio. Medimos o Pix gerado no ClickMax (venda pendente por Pix). A versão para a Meta (<code>PixGenerated</code>) existe no receptor e fica <b>desligada</b>.</li>"
           "<li>Purchase só depois que o Pix é <b>pago</b> ou o cartão é aprovado, com valor 47,00 e moeda BRL.</li></ul>",
           ver="Pix gerado e não pago: nenhum Purchase, venda pendente. Pix pago: um Purchase, 47,00 BRL.",
           print_="Prints no roteiro E8 abaixo.")
E_ += step("E8", "Roteiro da compra de teste cobrindo os 7 eventos",
           "<p>Use a página <b>publicada</b> em janela anônima, sem bloqueador, com o link de teste (UTMs do passo D1). Com o pixel em <b>Código de teste</b> (A3) preenchido, os eventos vão só para a aba Testar eventos. Faça na ordem; <b>anote a hora de cada passo</b>.</p>"
           "<ol class=\"prints\">"
           "<li><b>Visita</b>: abra a landing. Esperado: <b>PageView</b> no Testar eventos. (evento 1)</li>"
           "<li><b>Oferta</b>: role até a oferta (ou chegue à página de oferta). Esperado: <b>ViewContent</b> só se a página de oferta estiver marcada; ou ação de <b>elemento visível</b> no ClickMax. (evento 2)</li>"
           "<li><b>Clique no CTA</b>: clique em <b>um</b> botão com preço. Esperado: clique registrado no ClickMax (E2). Clique antes em um botão <b>sem</b> preço (se houver) e confira que ele <b>não</b> conta como qualificado. (evento 3)</li>"
           "<li><b>Checkout carregado, sem preencher</b>: espere 30 segundos. Esperado: <b>nenhum</b> InitiateCheckout. (evento 4, parte 1)</li>"
           "<li><b>Nome e e-mail preenchidos</b> (dados seus de teste): Esperado: <b>um</b> InitiateCheckout. (evento 4, parte 2)</li>"
           "<li><b>Gerar Pix, sem pagar</b>: espere 5 minutos. Esperado: <b>nenhum Purchase</b>; venda pendente (Pix) no ClickMax; AddPaymentInfo é normal. (evento 5)</li>"
           "<li><b>Pagar o Pix</b> (valor de R$ 47): espere até 5 minutos. Esperado: <b>um</b> Purchase, 47,00 BRL, origem navegador e servidor com o <b>mesmo event_id</b>; venda <b>Paga</b> com UTMs. (evento 6)</li>"
           "<li><b>Entrega</b>: confira o e-mail de acesso, a presença do contato de teste na turma do portal e o login. Esperado: acesso liberado em minutos; a página de obrigado mostra o produto e R$ 47 (sem R$ 97, R$ 270 nem reunião). (evento 7)</li>"
           "<li><b>Reembolse</b> a compra de teste (A8/D10). Esperado: <b>nenhum Purchase novo</b>.</li></ol>",
           cuidado="Nunca remova acesso de comprador real. Limpe o <b>Código de teste</b> depois (A3). Dados do teste: só seus.",
           print_="<b>P11</b>: prints de 1 a 3 (Testar eventos com PageView; ViewContent ou elemento visível; clique registrado). <b>P12</b>: passos 4 e 5 (sem IC antes, um IC depois). <b>P13</b>: passos 6 e 7 (venda pendente; Purchase aberto com value, currency, event_id; Histórico de envio). <b>P14</b>: passo 8 (e-mail de acesso, turma, obrigado) e 9 (reembolso, Histórico).")
E_ += ('<div class="box cuidado"><b class="t">[NC] resumo</b>O que a documentação não confirma e este roteiro resolve: (1) se o relatório separa cliques por botão; (2) se o importador mantém <code>data-cx-track</code>; (3) se há ação de funil que envie evento ao pixel; '
       '(4) se o ClickMax manda <code>content_name</code>/<code>content_ids</code> nos eventos nativos; (5) se a UTM atravessa landing &rarr; oferta; (6) quando o webhook de entrega dispara para o evento de acesso entregue.</div>')


# ---------------------------------------------------------------- F) Lead, Reembolso e públicos (funil híbrido, 25/11/2026)
F_ = ""
F_ += step("F1", "Lead: confirme que o contato chega com origem, campanha e criativo",
           "<p>O Lead nasce no formulário do anúncio. No ClickMax, o contato guarda o <b>nome da campanha</b> e o <b>nome do anúncio</b>. É isso que permite saber o custo por lead de cada criativo.</p>",
           onde="ClickMax &rsaquo; <b>Contatos</b> &rsaquo; abra um contato recente da captação &rsaquo; seção de <b>origem/UTM</b> (ou peça ao Claude: <span class=\"mono\">leads_get</span>, campo <span class=\"mono\">submissions</span>). " + E,
           ver="<code>utm_source=facebook</code>, <code>utm_medium=lead_ads</code>, <code>utm_campaign</code> com o nome da campanha e <code>utm_content</code> com o nome do anúncio. Hoje <b>não</b> vêm <code>sck</code>, <code>src</code> nem ids de campanha/anúncio (lacunas 1 a 5 de <code>PADRAO_UTM.md</code> &sect;9.3).",
           cuidado="Não renomeie campanha ou anúncio que já gerou lead: o lead guarda o nome antigo e a ligação com o gasto se perde. Crie campanha nova com o nome do padrão (<code>captacao | AAAA-MM-DD</code>).",
           print_="Print do contato (borre nome, e-mail e telefone) mostrando só a parte de UTM.",
           mock=mock(['<span>utm_source &middot; utm_medium</span><span class="mono">facebook &middot; lead_ads</span>', '<span>utm_campaign</span><span class="mono">nome da campanha</span>', '<span>utm_content</span><span class="mono">nome do anúncio (criativo)</span>'], "Contato da captação (esquema)"))
F_ += step("F2", "Reembolso: confirme que não gera Purchase novo",
           "<p>Reembolso é o 8&ordm; evento. Ele <b>reduz a receita líquida</b>; não apaga a venda no Meta e <b>nunca</b> vira Purchase. O receptor de teste já provou isso (<span class=\"mono\">VALIDACAO_EM_TESTE.md</span>); a prova real é o passo 8 da compra de teste.",
           onde="ClickMax &rsaquo; <b>Vendas</b> &rsaquo; a compra de teste &rsaquo; status <b>Reembolsada</b>; Meta &rsaquo; Gerenciador de Eventos &rsaquo; <b>Testar eventos</b> (nenhum Purchase novo).",
           ver="Venda <b>Reembolsada</b>; <b>nenhum</b> evento Purchase extra. Na conciliação o comprador aparece em <code>reembolsados_entre_compradores</code>.",
           print_="Print da venda reembolsada e do Testar eventos depois do reembolso.")
F_ += step("F3", "Etiquetas de coorte (com aprovação)",
           "<p>Coorte = leads que entraram no mesmo dia. Serve para <b>não comparar lead novo com lead que já teve tempo de comprar</b>. A coorte também sai sem etiqueta (pelo filtro de data); a etiqueta ajuda a excluir e segmentar.</p>",
           onde="ClickMax &rsaquo; <b>Contatos</b> &rsaquo; <b>Etiquetas</b> &rsaquo; criar <code>COORTE | AAAA-MM-DD | captacao</code> e aplicar aos contatos do dia (ou pedir ao Claude, com seu \"aprovado\"). " + NC + " (nome exato dos menus).",
           ver="Etiqueta com a contagem de contatos do dia. A etiqueta antiga <b>INSCRIÇÃO 270 | LEAD DO FORMULÁRIO</b> continua sendo por formulário, não por coorte.",
           cuidado="Escrever etiqueta em contatos é mudança no CRM: só com \"aprovado\". Não ative fluxo nenhum para isso.")
F_ += step("F4", "Exportar listas (fora do Git, sem PII no repositório)",
           "<p>Duas listas: <b>compradores</b> (para excluir dos anúncios) e <b>leads</b> (público quente, só depois da base legal). O arquivo fica em <span class=\"mono\">~/zion-privado/</span>, nunca no repositório, no chat ou em print.</p>",
           onde="ClickMax &rsaquo; <b>Contatos</b> &rsaquo; filtro (compradores: com compras; leads: etiqueta/UTM da captação) &rsaquo; <b>Exportar CSV</b>. Pelo Claude: <span class=\"mono\">leads_export_csv</span>. O export <b>não traz colunas de UTM</b>. " + E,
           ver="Um CSV com e-mail e telefone. Apague depois do upload.",
           cuidado="Não suba lista de leads como público de anúncio enquanto não houver consentimento de publicidade registrado (hoje os contatos novos chegam sem ele). Exclusão de compradores é o primeiro público seguro.")
F_ += step("F5", "Criar o público de exclusão de compradores no Gerenciador de Anúncios",
           "<p>O Windsor <b>não cria públicos</b> (não há essa ação). A criação e a exclusão são feitas por você no Gerenciador de Anúncios. Depois o Claude/ChatGPT só confere o conjunto.</p>",
           onde="Gerenciador de Anúncios &rsaquo; <b>Públicos</b> &rsaquo; <b>Criar público</b> &rsaquo; <b>Público personalizado</b> &rsaquo; <b>Lista de clientes</b> &rsaquo; envie o CSV de compradores (e-mail e telefone) &rsaquo; nome <code>EXCL | compradores MM47 | AAAA-MM-DD</code>. Depois, no conjunto de anúncios &rsaquo; <b>Público</b> &rsaquo; <b>Excluir</b> &rsaquo; escolha esse público. " + NC + " (menus de memória; a documentação da Meta não abriu nesta sessão).",
           ver="O público com status de processamento, tamanho e taxa de correspondência; o conjunto mostrando a exclusão.",
           cuidado="A lista é estática: reenvie quando houver compra nova. Mexer em conjunto de campanha ativa só com \"aprovado\".",
           print_="Print da tela do público (sem mostrar o arquivo) e do bloco Excluir no conjunto.")
F_ += step("F6", "Rodar a conciliação lead × comprador",
           "<p>Um comando, dados fora do repositório. Responde: quantos compradores únicos vieram do funil quente, do frio e quantos ficaram sem origem; tempo até a compra; coortes com 7 e 14 dias.</p>",
           onde="Terminal, na pasta <span class=\"mono\">09-tracking/conciliacao</span>: <span class=\"mono\">python3 -I lead_comprador.py --leads ~/zion-privado/leads.csv --compras ~/zion-privado/compras.csv --as-of AAAA-MM-DD</span>.",
           ver="JSON agregado, sem e-mail nem telefone. <code>soma_confere: true</code>. Coortes com menos de 7/14 dias aparecem como <b>imatura</b>; coorte com menos de 10 leads, <b>amostra_pequena</b>.",
           cuidado="Correspondência só por e-mail igual. E-mail diferente com telefone igual vira lista de <b>revisão humana</b>, nunca atribuição automática.")
F_ += step("F7", "Recuperar as compras de 24/11: a condição exata (B3)",
           "<p>A recuperação é <b>elegível com condição</b>. Prazo duro: pagamento + 7 dias (01/12/2026, no horário do pagamento); execute até 29/11.</p>"
           "<ol><li><b>B3:</b> Visão geral do pixel de 23/11 até hoje: <b>nenhum</b> Purchase dessas compras. Se houver, pare.</li><li><b>A5:</b> Histórico de envio: <b>Falhou</b> ou <b>Não enviado</b>. Se \"Enviado\", pare.</li><li>Teste com código de teste, depois real, só com seu \"aprovado\".</li></ol>",
           onde="Detalhes e comando em <span class=\"mono\">recuperacao/RECUPERACAO_COMPRAS_SEM_UTM.md</span> &sect;8.",
           ver="Um Purchase por compra, valor real em BRL, na data real; nenhuma UTM inventada.",
           cuidado="Nunca preencha UTM, campanha ou anúncio por dedução. Um Purchase enviado não se apaga.")
F_ += '<div class="box cuidado"><b class="t">[NC] resumo do capítulo F</b>Menus do Gerenciador de Anúncios e de etiquetas do ClickMax, hash aceito no upload da lista, aplicação de exclusão via <code>update_adset</code>, base legal para público de leads e hora exata dos pagamentos de 24/11.</div>'

# tabela de conferencia por ponto
points = """
<table><tr><th>Ponto da jornada</th><th>O que conferir</th><th>Onde</th></tr>
<tr><td>Página</td><td>UTM na barra de endereço depois de carregar; PageView; sem IC antes da hora</td><td>Barra do navegador, Testar eventos</td></tr>
<tr><td>Checkout aberto</td><td>IC só depois de nome e e-mail</td><td>Testar eventos</td></tr>
<tr><td>Pix gerado</td><td>AddPaymentInfo sim, Purchase não; venda pendente com UTMs</td><td>Testar eventos, Vendas</td></tr>
<tr><td>Pix pago</td><td>1 Purchase, value 47,00, BRL, Servidor, event_id igual ao do navegador</td><td>Testar eventos, Histórico de envio, Eventos de pixel</td></tr>
<tr><td>ClickMax</td><td>Venda Paga; utm_*, src, sck gravados</td><td>Vendas</td></tr>
<tr><td>Ticto</td><td>Pedido com status pago e mesmo valor; campos de UTM (ou ausência)</td><td>Extrato Ticto</td></tr>
<tr><td>Meta</td><td>Purchase na Visão geral; Deduplicação; Diagnóstico; EMQ</td><td>Gerenciador de Eventos</td></tr>
<tr><td>Acesso</td><td>E-mail, login, aulas</td><td>E-mail e área de membros</td></tr>
<tr><td>Reembolso</td><td>Venda reembolsada, sem novo Purchase</td><td>Vendas, Testar eventos</td></tr></table>"""

crit = """
<table><tr><th>#</th><th>Critério</th><th>Como provar (passo)</th><th>Passou?</th></tr>
<tr><td>R1</td><td>Purchase só depois do pagamento aprovado (e IC só depois do início efetivo)</td><td>D2, D3, D4: sem Purchase no Pix gerado; D5: 1 Purchase após pago</td><td class="chk">[ ] sim [ ] não</td></tr>
<tr><td>R2</td><td>value e currency corretos</td><td>D5: 47,00 BRL (nunca 0,47 / 4700 / 0)</td><td class="chk">[ ] sim [ ] não</td></tr>
<tr><td>R3</td><td>CAPI funcionando</td><td>A3 teste de token; D5 origem Servidor; D6 histórico "Enviado" e aba Eventos de pixel</td><td class="chk">[ ] sim [ ] não</td></tr>
<tr><td>R4</td><td>Deduplicação (navegador + servidor = 1)</td><td>D5 mesmo event_id; D9 cartão Deduplicação sem alerta</td><td class="chk">[ ] sim [ ] não</td></tr>
<tr><td>R5</td><td>Campanha, conjunto e anúncio na venda</td><td>D6: sck, utm_term, utm_content gravados (ids 9000...); ids próprios [NC]</td><td class="chk">[ ] sim [ ] não</td></tr>
<tr><td>R6</td><td>UTM persistente</td><td>D1 (ancora), D8 (origem de canal gravada); persistência entre sessões só com o snippet do plano</td><td class="chk">[ ] sim [ ] não</td></tr>
<tr><td>R7</td><td>Conciliação ClickMax × Meta × Ticto ≤ 10%</td><td>Script de conciliação, depois de vendas reais após as correções; no teste, as compras de teste batem nas 3 fontes</td><td class="chk">[ ] sim [ ] não</td></tr>
<tr><td>R8</td><td>Pix gerado ≠ Pix pago; reembolso sem novo Purchase</td><td>D4 e D10</td><td class="chk">[ ] sim [ ] não</td></tr></table>"""

prints = """
<ol class="prints">
<li><b>P1</b>: A1 e A2 (lista de pixels; Credencial; onde o pixel está).</li>
<li><b>P2</b>: A3 (estado do token, sem o token).</li>
<li><b>P3</b>: A4 (Comprou com Formas de pagamento; Abriu o checkout).</li>
<li><b>P4</b>: A5 (Histórico de envio da data das compras reais em diante).</li>
<li><b>P5</b>: A6 (aba Pixels do produto e da oferta).</li>
<li><b>P6</b>: B2, B3 (dataset e Visão geral do Purchase desde a primeira compra real).</li>
<li><b>P7</b>: C1 a C5 (extrato Ticto, filtros, webhooks, pixel Ticto).</li>
<li><b>P8</b>: durante o teste: D1 a D5 (barra de endereço, Testar eventos em cada fase, Purchase aberto).</li>
<li><b>P9</b>: D6, D7 (venda com UTMs, histórico, Eventos de pixel, acesso).</li>
<li><b>P10</b>: D9, D10 (Visão geral, Deduplicação, Diagnóstico, reembolso).</li>
<li><b>P11 a P14</b>: capítulo E (E2, E3, E4, E5, E6 e o roteiro E8 com os 7 eventos).</li>\n<li><b>P15</b>: capítulo F (F1 contato com UTM, borrado; F2 reembolso; F5 público de exclusão; F7 B3 e A5).</li>
</ol>
<div class="box cuidado"><b class="t">Não envie</b>Token, código de acesso, senha, QR, código de teste depois de usado, e-mail, telefone ou CPF de terceiros. Borre dados pessoais nos prints. O chat não é lugar de segredo.</div>"""

nodes = [("Anúncio", "Meta &middot; url_tags", ""), ("Página", "clickmax.space", ""), ("Checkout", "iframe do ClickMax", ""), ("Ticto", "processa Pix e cartão", ""), ("ClickMax", "venda, entrega, eventos", ""), ("Meta", "pixel + API de Conversões", "")]
arrows = ["UTMs na URL", "repassa todos os parâmetros", "pagamento", "webhook: pago", "Purchase (navegador e servidor)"]
flow = '<div class="flow">'
for i, (t, s, _) in enumerate(nodes):
    flow += f'<div class="node"><b>{t}</b><small>{s}</small></div>'
    if i < len(arrows):
        flow += f'<div class="arrow">{arrows[i]}</div>'
flow += '</div>'

intro = f"""
<div class="legend">
<div class="box onde"><b class="t">Onde clicar</b>O caminho de menu, como a documentação oficial descreve.</div>
<div class="box ver"><b class="t">O que você deve ver</b>O resultado certo. Se for diferente, é informação, não erro seu.</div>
<div class="box print"><b class="t">O que me enviar (print)</b>Exatamente a tela que preciso. Pode ser celular.</div>
<div class="box cuidado"><b class="t">Cuidado</b>O que não fazer.</div>
</div>
<p>Selos: <span class="e">confirmado</span> = o caminho está na documentação oficial do ClickMax lida em 25/11/2026. <span class="nc">NC</span> = <b>não confirmado</b>: não consegui abrir o painel nem a documentação oficial desse trecho; o texto diz o que procurar. As telas desenhadas são <b>esquemas</b>; a tela real pode variar. Se o nome for outro, mande print e eu ajusto o guia.</p>
<p><b>Ordem:</b> A, B e C são só leitura (não mudam nada). Depois, as mudanças do plano (você aprova). Depois, o roteiro D, a compra de teste.</p>
<div class="box cuidado"><b class="t">Segurança</b>Token e senhas nunca no chat. Você cola o token direto no painel do ClickMax. Esta cartilha não pede nenhuma credencial.</div>"""

html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Guia visual de rastreamento Zion</title><link rel="stylesheet" href="style.css"></head><body>
<header class="top"><div class="wrap"><img src="../../../docs/brand/zion-logo-claro.png" alt="Zion Hotel Group"><span class="tag">Fase 03 &middot; P0 &middot; 25/11/2026</span>
<h1>Guia visual de rastreamento</h1><p>Onde ver, onde ligar e o que me enviar, passo a passo. Anúncio, página, checkout, Ticto, ClickMax e Meta, com a compra de teste no final.</p></div></header>
<div class="wrap"><nav class="toc"><a href="#fluxo">Fluxo</a><a href="#a">A ClickMax</a><a href="#b">B Meta</a><a href="#c">C Ticto</a><a href="#d">D Compra de teste</a><a href="#e">E Funil P0</a><a href="#f">F Lead, Reembolso, públicos</a><a href="#criterios">Critérios R1 a R8</a><a href="#prints">Prints</a></nav>
{sec("como", "Como usar", "Cada passo tem um número curto e quatro caixas.", intro)}
{sec("fluxo", "O caminho de uma venda", "Esquema simples. Cada seta diz o que viaja.", flow + '<p>O pixel <span class="mono">' + PIXEL + '</span> roda dentro do checkout. O ClickMax guarda a URL do momento em que o checkout abre; por isso a UTM precisa estar na URL da página nessa hora.</p>')}
{sec("a", "A &middot; ClickMax", "Onde ver e ligar pixel, API de Conversões, token, histórico de envio e regras de Purchase e checkout.", A, True)}
{sec("b", "B &middot; Meta", "Gerenciador de Eventos: o que o Meta realmente recebeu. Os nomes dos menus do Meta mudam; onde está NC, procure o termo indicado.", B, True)}
{sec("c", "C &middot; Ticto", "O gateway por trás do checkout. Menus da Ticto: não confirmados, mande print do que encontrar.", C, True)}
{sec("d", "D &middot; Roteiro da compra de teste", "Duas compras pequenas e reembolsáveis (Pix e cartão), com tudo o que conferir em cada ponto.", D + "<h3>O que conferir em cada ponto</h3>" + points, True)}
{sec("e", "E &middot; Eventos do funil P0", "Os 7 eventos separados (visita, oferta, clique com preço, checkout efetivo, Pix gerado, pagamento, entrega): o que configurar, o que o ClickMax não permite e como provar na compra de teste.", E_, True)}
{sec("f", "F &middot; Lead, Reembolso e públicos", "Os 8 eventos (Lead e Reembolso entram), origem e coorte do lead, exportação de listas, públicos no Gerenciador, conciliação lead × comprador e a condição para recuperar as compras de 24/11.", F_, True)}
{sec("criterios", "Critérios R1 a R8", "Marque cada um ao final do teste. Se algum falhar, me envie os prints do passo indicado.", crit)}
{sec("prints", "O que me enviar, na ordem", "Um print por item. Pode mandar tudo junto.", prints)}
</div>
<footer><div class="wrap">Zion Hotel Group International &middot; ZION SALES ENGINE &middot; guia de DATA. Documentos relacionados: <span class="mono">PLANO_EXECUTAVEL.md</span>, <span class="mono">capi-webhook/</span>, <span class="mono">recuperacao/</span>, <span class="mono">conciliacao/</span>.</div></footer>
</body></html>"""
OUT.write_text(html, encoding="utf-8")
print("gerado", OUT, len(html), "bytes")
