"""Gera o HTML do resumo da aula do Módulo 4 (Marketing e vendas) e o TXT do prompt de IA.
Depois, src/render_pdf.js imprime o HTML em PDF (8 páginas A4 + capa).
Uso: python3 -I src/build_resumo.py <pasta-build>
Saídas: <pasta-build>/resumo.html e docs/trilha2/materiais/Modulo-4-Prompt-de-IA.txt
Molde: producao/jornada2/02-financas/src/build_resumo.py (mesmo CSS)."""
import sys, pathlib, re
B = pathlib.Path(sys.argv[1]); B.mkdir(parents=True, exist_ok=True)
HERE = pathlib.Path(__file__).resolve().parent; LICAO = HERE.parent
REPO = LICAO.parents[2]; F = REPO / "docs/assets/fonts"; BR = REPO / "docs/brand"
MAT = REPO / "docs/trilha2/materiais"; MAT.mkdir(parents=True, exist_ok=True)

# ---------- Prompt de IA em texto puro (extraído de PROMPT_IA.md, bloco de código) ----------
md = (LICAO / "PROMPT_IA.md").read_text(encoding="utf-8")
bloco = re.search(r"```\n(.*?)```", md, re.S).group(1).strip()
txt = ("PROMPT DE IA · REVISAR A MARCA E CAPTAÇÃO\n"
       "Zion Hotel Academy · Jornada de Gestão · Módulo 4 · Marketing e vendas\n\n"
       "Como usar: exporte a sua Marca e Captação em PDF (ou copie as abas Marca em uma folha e Captação do mês da planilha), abra qualquer assistente de IA, "
       "cole o prompt abaixo inteiro e, logo depois, cole o conteúdo. O assistente não decide por você: ele confere as contas "
       "e faz perguntas. Não cole dados pessoais de hóspedes nem senhas.\n\n"
       "----- COPIE DAQUI PARA BAIXO -----\n\n" + bloco + "\n\n----- FIM DO PROMPT -----\n\n"
       "Depois da revisão, se trocar a promessa, teste a nova frase com cinco pessoas de fora antes de levar para o anúncio.\n"
       "Conteúdo educacional. Não é promessa de renda, retorno, ocupação, reservas ou resultado.\n")
(MAT / "Modulo-4-Prompt-de-IA.txt").write_text(txt, encoding="utf-8")

# ---------- HTML do resumo ----------
CSS = f"""
@font-face{{font-family:Cormorant;src:url('{(F/'cormorant.woff2').as_uri()}')}} @font-face{{font-family:Cormorant;font-style:italic;src:url('{(F/'cormorant-italic.woff2').as_uri()}')}} @font-face{{font-family:Aventa;src:url('{(F/'aventa.woff2').as_uri()}')}}
:root{{--musgo:#1B2117;--verde:#16261C;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--ouro:#C9B37E;--texto:#1B2117;--cinza:#5A5F55}}
@page{{size:A4;margin:0}} *{{box-sizing:border-box}}
body{{margin:0;font-family:Aventa,Arial,sans-serif;color:var(--texto);background:#fff;font-size:10.4pt;line-height:1.38}}
.pg{{width:210mm;min-height:297mm;padding:20mm 20mm 20mm;page-break-after:always;position:relative}}
.pg:last-child{{page-break-after:auto}}
.capa{{background:var(--musgo);color:var(--creme);display:flex;flex-direction:column;justify-content:space-between;padding-top:22mm}}
.capa img{{height:16mm}} .capa .k{{color:var(--ouro);letter-spacing:.2em;text-transform:uppercase;font-weight:700;font-size:10pt}}
.capa h1{{font-family:Cormorant,serif;font-weight:500;font-size:50pt;line-height:1.02;margin:6mm 0 5mm}} .capa h1 i{{color:var(--ouro)}}
.capa p{{color:var(--areia);font-size:13pt;max-width:140mm}}
h2{{font-family:Cormorant,serif;font-weight:500;font-size:25pt;line-height:1.1;margin:0 0 3.5mm;color:var(--verde)}}
h3{{font-size:10pt;letter-spacing:.14em;text-transform:uppercase;color:var(--terra);margin:4.5mm 0 1.8mm}}
p{{margin:0 0 2.6mm}} ul,ol{{margin:0 0 2.6mm;padding-left:5mm}} li{{margin-bottom:1mm}}
.cita{{font-family:Cormorant,serif;font-style:italic;font-size:15pt;line-height:1.22;border-left:3px solid var(--ouro);padding-left:6mm;margin:3.2mm 0;color:var(--verde)}} .cita small{{display:block;font-family:Aventa,sans-serif;font-style:normal;font-size:8.5pt;color:var(--cinza);margin-top:1.5mm;letter-spacing:.1em;text-transform:uppercase}}
table{{width:100%;border-collapse:collapse;font-size:9.1pt;margin:2.2mm 0 3mm;line-height:1.3}} th,td{{text-align:left;padding:1.3mm 2mm;border-bottom:1px solid var(--areia);vertical-align:top}} th{{background:var(--musgo);color:var(--creme);font-weight:600}}
td.n,th.n{{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}} tr.tot td{{background:#F6F1E6;font-weight:700}} tr.sub td{{color:var(--cinza)}}
.ex{{background:#F6F1E6;border:1px solid var(--areia);border-radius:4mm;padding:3.8mm 5mm;margin:3mm 0}} .ex.compacto table{{font-size:8.7pt}} .ex.compacto td,.ex.compacto th{{padding:1.1mm 1.8mm}} .ex b.rot{{display:block;font-size:9pt;letter-spacing:.14em;text-transform:uppercase;color:#A0522D;margin-bottom:2mm}} .ex table{{background:#fff}}
.caixa{{border:1px dashed var(--terra);border-radius:4mm;padding:3.5mm 5.5mm;margin:3.5mm 0}} .caixa h3{{margin-top:0}}
.rod{{position:absolute;left:20mm;right:20mm;bottom:10mm;font-size:8.5pt;color:var(--cinza);display:flex;justify-content:space-between;gap:8mm;border-top:1px solid var(--areia);padding-top:2mm}}
.num{{font-family:Cormorant,serif;font-size:34pt;color:var(--ouro);line-height:1}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm;margin:2mm 0 3mm}} .grid3{{grid-template-columns:1fr 1fr 1fr}} .card{{border:1px solid var(--areia);border-radius:3mm;padding:2.6mm 3.2mm;font-size:9.5pt}} .card b{{display:block;color:var(--verde);margin-bottom:.8mm}} .card small{{color:var(--cinza);font-size:9pt;line-height:1.32;display:block}}
.fonte{{font-size:9pt;color:var(--cinza)}} .ref{{display:inline-block;background:var(--areia);color:var(--musgo);font-size:8.5pt;padding:.3mm 2mm;border-radius:2mm;letter-spacing:.06em;text-transform:uppercase}}
.casc li{{margin-bottom:.6mm}} .casc b{{color:var(--verde)}}
.check{{font-size:9.7pt;line-height:1.34}} .check li{{margin-bottom:.9mm}} .check b{{color:var(--verde)}}
"""

def paginas(BR, ROD):
    logo = (BR / 'zion-logo-claro.png').as_uri()
    return f"""
<section class="pg capa"><img src="{logo}" alt="Zion"><div><div class="k">Jornada de Gestão · Módulo 4 · Resumo da aula</div><h1>Audiência alugada <i>não é audiência.</i></h1><p>Marketing e vendas. O que ficou da aula em oito páginas: por que alguém escolheria a sua casa; a promessa e a prova; o tom e os pontos de contato; a lista própria; o custo por reserva e a venda direta; um exemplo didático; o checklist; o critério de conclusão e a próxima etapa.</p></div><div class="k" style="font-size:9pt">Aprenda o passo a passo · Zion Hotel Academy · Método Zion 360°</div></section>

<section class="pg"><h2>1. Por que alguém escolheria a sua casa?</h2>
<div class="cita">“O hóspede não compara quartos. Compara motivos.”<small>Panorama do Desenvolvimento Hoteleiro · Trilha B · Pilar G1 “Marca e Narrativa”</small></div>
<p>Vinte cabanas com banheira e vista, no mesmo destino, parecem a mesma coisa para quem está escolhendo. Quando tudo parece igual, decide-se por preço, e essa é uma disputa que a hospedagem pequena nunca ganha.</p>
<div class="cita">“Marca, aqui, não é logotipo nem paleta. É a razão declarada que faz alguém pagar mais caro na sua casa do que na do vizinho, e a forma como essa razão aparece antes da reserva.”<small>Panorama · Trilha B · Pilar G1 · O que é</small></div>
<h3>Três decisões formam a marca</h3>
<table><tr><th>Decisão</th><th>O que é</th><th>Na folha de marca</th></tr>
<tr><td><b>O que você promete</b></td><td>Não o que você tem: o que o hóspede vai viver.</td><td>Promessa e prova</td></tr>
<tr><td><b>Para quem</b></td><td>Dito com clareza suficiente para que quem não é daquele público entenda que não é.</td><td>Para quem</td></tr>
<tr><td><b>O que você nunca faz</b></td><td>A decisão mais difícil e a que mais constrói marca.</td><td>O que nunca fazemos</td></tr></table>
<p class="fonte">Jornada do COMO · Etapa 05 “Criar uma marca”, Passo 01: “Uma hospedagem que aceita tudo não promete nada.”</p>
<div class="caixa"><h3>O erro comum do pilar</h3><p>“Confundir identidade visual com marca. Trocar o logotipo não muda o motivo pelo qual alguém escolhe você, e custa dinheiro que resolveria outra coisa.” <span class="fonte">(Pilar G1 · Erro comum)</span></p></div>
<p>Este módulo junta dois pilares da Trilha B: o G1 dá o motivo (a marca em uma folha) e o G4 dá o caminho (a lista própria e o custo por reserva). Os dois formam a página 4 do seu Plano de Gestão.</p>{ROD}</section>

<section class="pg"><h2>2. A promessa e a prova</h2>
<div class="cita">“A lista diz o que existe. A promessa diz o que acontece.”<small>Jornada do COMO · Etapa 05 · Passo 02 · Frase de Promessa Zion™</small></div>
<p>A promessa cabe em uma frase com três partes: a <b>ocasião</b>, a <b>experiência central</b> e o <b>elemento que a torna possível</b>. Concreto é melhor que bonito.</p>
<h3>Corte os adjetivos genéricos</h3>
<p>Aconchegante, único, especial, exclusivo, inesquecível, incrível e perfeito aparecem em quase todo anúncio, e por isso não distinguem nada. Uma frase escrita com substantivo e verbo, descrevendo o que acontece, já diferencia.</p>
<h3>Os quatro testes</h3>
<table><tr><th>Teste</th><th>A pergunta</th></tr>
<tr><td><b>Recusa</b></td><td>Ela faz alguém entender que não é para ele?</td></tr>
<tr><td><b>Cumprimento</b></td><td>O produto entrega isso, toda vez?</td></tr>
<tr><td><b>Diferença</b></td><td>O concorrente ao lado poderia dizer a mesma frase?</td></tr>
<tr><td><b>Memória</b></td><td>Alguém repetiria essa frase ao recomendar?</td></tr></table>
<div class="cita">“Mostre a frase a quem não conhece o projeto. Se precisarem perguntar o que é, a frase ainda não existe.”<small>Panorama · Pilar G1 · Passo 02</small></div>
<h3>A prova</h3>
<p>“A foto de capa do anúncio tem que mostrar exatamente o que a frase diz. Quando as duas discordam, a reserva não acontece.” <span class="fonte">(Pilar G1 · Passo 03)</span>. Na folha de marca, a prova é a foto (ou o fato visível) que mostra a promessa antes da reserva.</p>{ROD}</section>

<section class="pg"><h2>3. O tom e os pontos de contato</h2>
<p>O jeito de escrever o anúncio, as mensagens e as respostas às avaliações é marca tanto quanto o logotipo. E é de graça. O tom se define em três decisões <span class="fonte">(Etapa 05 · Passo 09 · Guia de Tom de Voz™)</span>:</p>
<ol class="check"><li><b>Formal ou próximo.</b> Próximo não significa íntimo nem informal demais.</li><li><b>Descritivo ou evocativo.</b> A promessa já aponta a direção.</li><li><b>O que você nunca escreve.</b> A lista de palavras banidas, começando pelos adjetivos genéricos e pelos clichês do setor.</li></ol>
<h3>Onde a promessa precisa aparecer</h3>
<div class="cita">“Anúncio, site, resposta de WhatsApp, placa na entrada e mensagem de boas-vindas. Promessa que aparece só no site não é promessa, é texto.”<small>Panorama · Pilar G1 · Passo 04</small></div>
<p>As mensagens de boas-vindas (M04) e de agradecimento com pedido de avaliação honesta (M08) já estão prontas no <b>Kit de Mensagens de Chegada e Saída (Ferramenta 11)</b>. Use o kit como está e ajuste o texto ao seu tom.</p>
<h3>A marca em uma folha</h3>
<p>Nesta jornada, a folha tem quatro linhas obrigatórias e uma opcional: <b>para quem</b> (e para quem não é), <b>promessa</b>, <b>prova</b>, <b>tom</b> e <b>o que nunca fazemos</b>. A Etapa 05 completa a folha em nove linhas, incluindo a assinatura da marca e “o que não cai quando a ocupação está baixa”.</p>
<div class="caixa"><h3>Por que escrever</h3><p>“Marca se perde devagar, por concessões pequenas feitas em momentos de aperto”, e a folha transforma cada concessão em decisão consciente. <span class="fonte">(Etapa 05 · Passo 12)</span></p></div>{ROD}</section>

<section class="pg"><h2>4. A lista própria</h2>
<div class="cita">“Audiência alugada não é audiência.”<small>Panorama · Trilha B · Pilar G4 “Captação de Hóspede”</small></div>
<p>“A diferença entre seguidor e contato é que o contato você alcança quando quiser, sem pedir licença ao algoritmo nem pagar comissão.” Sem base própria, “toda reserva nova custa comissão, inclusive a do hóspede que já esteve na sua casa”. <span class="fonte">(Pilar G4 · Por que importa e O que custa ignorar)</span></p>
<h3>Os quatro passos do pilar</h3>
<table><tr><th>Passo</th><th>O que fazer</th></tr>
<tr><td><b>1 · Comece a lista hoje</b></td><td>“Peça e-mail e WhatsApp no check-in, com autorização explícita, e guarde num lugar que não seja o seu celular.”</td></tr>
<tr><td><b>2 · Separe quem já veio</b></td><td>“Para quem já veio, você lembra; para quem nunca veio, você precisa provar.”</td></tr>
<tr><td><b>3 · Um canal, bem feito</b></td><td>“Uma régua de WhatsApp bem feita vale mais que presença fraca em cinco redes.”</td></tr>
<tr><td><b>4 · Meça o custo por reserva</b></td><td>Próxima página.</td></tr></table>
<h3>Como montar <span class="fonte">(Etapa 07 · Passo 07 · Base de Hóspedes Zion™)</span></h3>
<ul><li><b>Oito campos, dois minutos por estadia:</b> nome, telefone, e-mail, datas, pessoas, como chegou, uma observação e a autorização.</li><li><b>A autorização:</b> uma frase no check-in. Quem diz sim entra na lista; quem diz não fica só no histórico e não recebe nada.</li><li><b>Onde mora:</b> numa planilha fora da plataforma, com cópia, atualizada no dia da saída.</li><li><b>Quatro contatos por ano, no máximo</b> (Passo 08): agradecimento, aniversário da estadia, abertura de temporada e oferta de baixa, sempre com o caminho de reserva direta.</li></ul>
<p class="fonte">Cautela: antes de pedir contato a quem reservou por uma plataforma, confira as regras dela. As fontes Zion não tratam de lei de proteção de dados; para dúvidas, procure um profissional habilitado.</p>{ROD}</section>

<section class="pg"><h2>5. O custo por reserva e a venda direta</h2>
<div class="cita">“Quanto você gastou dividido por quantas reservas vieram daquele esforço. Sem esse número, investir em captação é aposta.”<small>Panorama · Pilar G4 · Passo 04</small></div>
<h3>A conta, canal por canal</h3>
<ul class="casc"><li><b>Plataforma:</b> custo = comissão sobre a receita do canal (mais algum gasto extra, se houver).</li><li><b>Canal direto:</b> custo = o que você gastou no mês para trazer o hóspede (impulsionamento, anúncio, brinde). Hóspede que volta e indicação podem custar zero.</li><li><b>Custo por reserva</b> = custo do canal ÷ reservas do canal.</li><li><b>Venda direta</b> = receita das reservas sem plataforma ÷ receita de hospedagem (a mesma definição do Painel, Módulo 1).</li></ul>
<p class="fonte">Incluir a comissão como custo da plataforma é elaboração desta aula a partir do Pilar G2 (“cada canal tem um custo de aquisição diferente”). Taxa de cartão e imposto ficam na Folha Única do Mês (Módulo 2).</p>
<h3>A meta de venda direta</h3>
<div class="cita">“Um número, não uma intenção. E o prazo para chegar nele.”<small>Panorama · Pilar G2 · Passo 03</small></div>
<p>A meta é a mesma do seu Painel de Gestão (Módulo 1) e da Tabela de Preço e Canais (Módulo 3). A ficha calcula o que ela pede num mês com a mesma receita e a comissão que deixaria de sair nesse mês. É conta com os seus números, não previsão.</p>
<h3>Medir a fonte real</h3>
<p>“Pergunte a todo hóspede como ele chegou até você” <span class="fonte">(Etapa 07 · Passo 02)</span>. Um hóspede pode reservar pela plataforma e ter chegado por indicação: sem a pergunta, você paga comissão sobre quem já tinha decidido. A Etapa 07 lembra que as fontes próprias (base, indicação e busca pelo nome) levam de seis a vinte e quatro meses para produzir efeito relevante.</p>{ROD}</section>

<section class="pg"><h2>6. Exemplo aplicado</h2>
<div class="ex compacto"><b class="rot">Exemplo didático · dados fictícios</b><p><b>Cabanas do Vale</b>, quatro unidades na serra, a Ana opera sozinha. Mesmo mês dos módulos anteriores: outubro de 2026, 25 reservas, R$ 16.240,00 de hospedagem.</p>
<p><b>Marca em uma folha.</b> Para quem: casais que vêm de carro, de até três horas de distância, para duas ou três noites (não é para grupos e festas). Promessa: “Duas noites a dois, com a lareira acesa e o vale na janela da cama, sem vizinho à vista.” Prova: a foto de capa com a cama de frente para a janela e a lareira acesa. Tom: próximo, concreto, calmo. Quatro testes com Sim; 4 de 5 pessoas de fora entenderam: ela reescreve e testa de novo. A promessa aparece no anúncio e nas redes; falta no site, na resposta de WhatsApp, na mensagem de boas-vindas e na placa.</p>
<table><tr><th>Canal</th><th class="n">Reservas</th><th class="n">Receita</th><th class="n">Custo</th><th class="n">Por reserva</th></tr>
<tr><td>Plataforma A (16%)</td><td class="n">12</td><td class="n">R$ 8.120,00</td><td class="n">R$ 1.299,20</td><td class="n">R$ 108,27</td></tr>
<tr><td>Plataforma B (15%)</td><td class="n">5</td><td class="n">R$ 3.248,00</td><td class="n">R$ 487,20</td><td class="n">R$ 97,44</td></tr>
<tr><td>Instagram com impulsionamento</td><td class="n">2</td><td class="n">R$ 1.120,00</td><td class="n">R$ 150,00</td><td class="n">R$ 75,00</td></tr>
<tr><td>Hóspede que volta (WhatsApp)</td><td class="n">3</td><td class="n">R$ 1.848,00</td><td class="n">R$ 0,00</td><td class="n">R$ 0,00</td></tr>
<tr><td>Indicação</td><td class="n">3</td><td class="n">R$ 1.904,00</td><td class="n">R$ 0,00</td><td class="n">R$ 0,00</td></tr>
<tr class="tot"><td>Total</td><td class="n">25</td><td class="n">R$ 16.240,00</td><td class="n">R$ 1.936,40</td><td class="n">R$ 77,46</td></tr></table>
<p><b>Venda direta:</b> R$ 4.872,00 de R$ 16.240,00 = <b>30%</b> da receita (8 de 25 reservas). A captação custou 11,9% da receita. <b>Meta:</b> 40% até 30/06/2027, a mesma do Painel e da Tabela de Preço; num mês com a mesma receita, pede R$ 6.496,00 de venda direta e deixariam de sair cerca de <b>R$ 255,20</b> de comissão (R$ 1.624,00 × 15,7%, a comissão média das plataformas).</p>
<p><b>Lista própria:</b> 64 contatos no celular, nenhum com autorização. Meta: 120 contatos com autorização em 12 meses, cerca de 10 por mês, 40% das 25 estadias. Canal para fazer bem: WhatsApp.</p>
<p><b>Atenção da ficha:</b> a lista ainda não existe (64 contatos sem autorização); ela mora só no celular; nem todos entenderam a promessa.</p></div>
<p>O exemplo não promete que a meta será atingida: ele mostra como escrever a marca, começar a lista e medir cada canal. O resultado depende da execução.</p>{ROD}</section>

<section class="pg"><h2>7. Checklist da Marca e Captação</h2>
<h3>Montar (uma vez)</h3>
<ol class="check"><li><b>Para quem</b>, e para quem não é.</li><li><b>A promessa em uma frase</b>, sem adjetivo genérico, aprovada nos quatro testes.</li><li><b>O teste das cinco pessoas</b>: ninguém precisou perguntar o que é.</li><li><b>A prova e o tom</b>: a foto de capa mostra a frase; o tom em três palavras, com a lista do que você nunca escreve.</li><li><b>A lista começada</b>: frase de autorização, planilha fora do celular e com cópia, quem tem acesso, um canal para fazer bem.</li><li><b>O custo por reserva de cada canal</b> e a <b>meta de venda direta</b> com prazo, a mesma do Painel.</li></ol>
<h3>A rotina</h3>
<ol class="check" start="7"><li><b>A cada check-in:</b> pedir o contato com a autorização e perguntar como a pessoa chegou.</li><li><b>A cada saída (2 minutos):</b> preencher a linha da estadia na aba Lista própria.</li><li><b>Todo mês (10 minutos):</b> lançar os canais, conferir o custo por reserva e a venda direta contra a meta.</li><li><b>A promessa em todo ponto de contato</b>; só quem autorizou recebe os quatro contatos do ano.</li></ol>
<div class="caixa"><h3>O erro mais comum</h3><p>“Trocar a lista própria por seguidores. Seguidor é audiência emprestada: a plataforma decide quantos deles veem você, e essa decisão muda sem aviso.” <span class="fonte">(Pilar G4 · Erro comum)</span></p></div>
<div class="cita">“Uma lista de pessoas que já se hospedaram, com permissão para receber contato, é o ativo de marketing mais barato que uma hospedagem pode ter. Ela não cobra comissão e não muda de regra.”<small>Panorama · Pilar G4 · Na prática</small></div>{ROD}</section>

<section class="pg"><h2>8. Faça agora, critério de conclusão e próxima etapa</h2>
<h3>Faça agora</h3><p>Abra a ficha <b>A minha Marca e Captação</b> (link na aula). Cinco telas, de 20 a 25 minutos: para quem e a promessa, a prova e o tom, a lista própria, os canais com o custo por reserva e a meta de venda direta. O resultado vem em cinco partes: o resultado (a marca em uma folha e a tabela de canais), o que isso significa, atenção, o que fazer e como verificar. As respostas ficam só no seu aparelho; o PDF é a página 4 do seu Plano de Gestão. Depois, abra a planilha <b>Plano de Captação</b> (em branco e exemplo) e comece a aba Lista própria no próximo check-in.</p>
<div class="caixa"><h3>Critério de conclusão do Módulo 4</h3><ul><li>A marca em uma folha tem para quem, promessa, prova e tom.</li><li>A lista tem os números de hoje, o lugar onde fica, a frase de autorização, o canal e a meta.</li><li>Os canais do último mês têm o custo por reserva; a meta de venda direta tem prazo.</li><li>O plano está escrito, com a data do primeiro check-in com o pedido de autorização, e o PDF foi baixado.</li><li>Em 30 dias: a aba Lista própria tem uma linha por estadia, com a autorização registrada.</li></ul></div>
<h3>Prompt de IA</h3><p>Para uma segunda leitura, use o prompt do módulo (arquivo <b>Modulo-4-Prompt-de-IA.txt</b>, na aba Materiais): ele revisa a promessa e a prova, reescreve um texto no seu tom, confere o custo por reserva e a venda direta e sugere três perguntas antes do próximo contato com a lista. Não cole dados de hóspedes nem senhas.</p>
<h3>A próxima etapa</h3><p>Siga para o <b>Módulo 5 · Pessoas e organização das áreas</b>: quem pede a autorização no check-in, quem responde o WhatsApp e quem registra o canal de cada reserva vira tarefa com dono e alçada.</p>
<p style="font-size:9.5pt;color:var(--cinza)">Fontes Zion: Panorama do Desenvolvimento Hoteleiro (Trilha B · Pilares G1, G2 e G4); Jornada do COMO, Etapas 05 e 07. Ferramenta reaproveitada: Kit de Mensagens de Chegada e Saída (Ferramenta 11). Material educacional da Zion Hospitality Business. Não é promessa de renda, retorno, ocupação, reservas ou resultado: o resultado depende da execução de cada hospedagem.</p>{ROD}</section>
"""

ROD = '<div class="rod"><span>Zion Hotel Academy · Jornada de Gestão · Módulo 4</span><span>Conteúdo educacional. Não é promessa de renda, retorno, reservas ou resultado.</span></div>'
html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Módulo 4 · Marketing e vendas · Resumo</title><style>{CSS}</style></head><body>{paginas(BR, ROD)}</body></html>"""
(B / "resumo.html").write_text(html, encoding="utf-8"); print("ok", B / "resumo.html")
