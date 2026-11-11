"""Landing low ticket (v3, 11/11): topo dividido (foto real da bolha de um lado, texto do outro; nada escrito sobre a foto),
o que ele ganha / recebe / leva deixado explícito, preço e botão cedo, barra fixa no celular, checkout ClickMax com bump.
Uso: python3 -I landing/build_landing_lt.py  → landing/dist/clickmax_lt.html"""
import pathlib
A = pathlib.Path(__file__).resolve().parent
FOTO = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/assets/"
BUMP = "ef27848a-37cc-4804-9941-52ac87f8d9ef"
CTA = "Sim, quero meu diagnóstico por R$ 47"
DIMS = [("Fotos e apresentação", 2, 1), ("Título e descrição", 3, 1), ("Preço e posicionamento", 3, 0), ("Diferenciais e experiência", 4, 0),
        ("Avaliações e confiança", 4, 0), ("Atendimento e comunicação", 2, 1), ("Conforto e infraestrutura", 4, 0)]

css = """<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<style>
.zl{background:#040605;color:#DED6BF;font-family:Jost,Arial,sans-serif;font-size:17px;line-height:1.55;padding-bottom:84px}
.zl *{box-sizing:border-box}.zl p,.zl li,.zl span,.zl label,.zl b,.zl small,.zl strong{font-family:Jost,Arial,sans-serif}
.zl .w{max-width:640px;margin:0 auto;padding:0 16px}.zl .sec{padding:44px 0}
.zl h1,.zl h2,.zl h3{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;line-height:1.04;color:#FEF5F0;margin:0 0 14px}
.zl h1{font-size:clamp(34px,8.5vw,52px)}.zl h2{font-size:clamp(30px,8vw,42px)}.zl em{color:#C9B37E;font-style:italic}
.zl p{color:#DED6BF;margin:0 0 14px}.zl .k{display:block;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:#C9B37E;font-weight:600;margin:0 0 12px}
.zl .btn{display:block;width:100%;background:#C9B37E;color:#040605;font-weight:600;font-size:18px;padding:18px 20px;border-radius:12px;text-decoration:none;text-align:center}
.zl .confia{display:flex;flex-wrap:wrap;gap:6px 14px;margin:12px 0 0;font-size:13px}.zl .confia span{color:#A39E8E}
.zl .preco{display:flex;align-items:baseline;gap:10px;margin:14px 0 12px}.zl .preco b{font-family:"Cormorant Garamond",serif;font-size:48px;font-weight:500;color:#FEF5F0;line-height:1}.zl .preco span{color:#A39E8E;font-size:15px}
.zl .split{display:grid;grid-template-columns:1fr 1fr;min-height:100vh}
.zl .split .foto{position:relative;background:#040605 url(""" + FOTO + """store/hero.webp) center/cover no-repeat;min-height:100%}
.zl .split .txt{display:flex;flex-direction:column;justify-content:center;padding:28px 40px;max-width:640px}
.zl .split .leg{display:block;font-size:11px;color:#A39E8E;margin:12px 0 0}
.zl .ganhos{list-style:none;padding:0;margin:2px 0 4px}.zl .ganhos li{color:#FEF5F0;padding:5px 0 5px 28px;position:relative;font-size:16px}
.zl .ganhos li:before{content:"✓";position:absolute;left:2px;top:5px;color:#C9B37E;font-weight:600}
@media(max-width:820px){.zl .split{grid-template-columns:1fr;min-height:0}.zl .split .foto{height:24vh;min-height:170px}.zl .split .txt{padding:20px 16px 30px}}
.zl .formula{display:grid;gap:10px;margin:6px 0 4px}
.zl .formula>div{border:1px solid rgba(201,179,126,.35);border-radius:12px;padding:12px 14px;background:#0d110b}
.zl .formula .fk{display:block;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:#C9B37E;font-weight:600;margin:0 0 4px}
.zl .formula strong{color:#FEF5F0;font-weight:600;font-size:16px}
.zl .formula ul{list-style:none;padding:0;margin:0}.zl .formula li{color:#FEF5F0;font-size:15px;padding:3px 0 3px 24px;position:relative}
.zl .formula li:before{content:"✓";position:absolute;left:2px;top:3px;color:#C9B37E;font-weight:600}
.zl .formula .f3{border-color:#C9B37E;background:rgba(201,179,126,.08)}
.zl .musgo{background:#1B2117}
.zl .dor{list-style:none;padding:0;margin:0}.zl .dor li{color:#FEF5F0;padding:12px 0 12px 34px;position:relative;border-top:1px solid rgba(201,179,126,.18)}
.zl .dor li:before{content:"✕";position:absolute;left:4px;top:12px;color:#C2643F;font-weight:600}
.zl .resul{display:grid;gap:12px;margin:18px 0}.zl .resul div{background:#0d110b;border:1px solid rgba(201,179,126,.3);border-radius:14px;padding:16px 16px 16px 60px;position:relative}
.zl .resul b{position:absolute;left:18px;top:12px;font-family:"Cormorant Garamond",serif;font-size:34px;color:#C9B37E;font-weight:500;line-height:1}
.zl .resul strong{display:block;color:#FEF5F0;font-weight:600}.zl .resul span{color:#A39E8E;font-size:14px}
.zl .aviso{font-size:14px;color:#A39E8E;border-left:3px solid #C9B37E;padding:6px 12px}
.zl .demo{background:#0d110b;border:1px solid rgba(201,179,126,.3);border-radius:14px;padding:16px;margin:18px 0}
.zl .topo{display:flex;gap:14px;align-items:center;margin-bottom:10px}
.zl .anel{width:78px;height:78px;border-radius:50%;flex:none;display:grid;place-items:center;background:conic-gradient(#C9B37E 0 63%,rgba(222,214,191,.15) 63% 100%)}
.zl .anel span{width:62px;height:62px;border-radius:50%;background:#0d110b;display:grid;place-items:center;font-family:"Cormorant Garamond",serif;font-size:28px;color:#FEF5F0}
.zl .bar{display:flex;justify-content:space-between;font-size:13px;margin-top:7px}.zl .bar span{color:#DED6BF}
.zl .tr{height:5px;border-radius:5px;background:rgba(222,214,191,.15);overflow:hidden}.zl .tr i{display:block;height:100%;background:#C9B37E}.zl .tr i.p{background:#C2643F}
.zl .cards{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:18px 0}.zl .cards div{border:1px solid rgba(201,179,126,.35);border-radius:14px;padding:16px;background:#0d110b}
.zl .cards b{display:block;font-family:"Cormorant Garamond",serif;font-size:30px;font-weight:500;color:#C9B37E;line-height:1}.zl .cards strong{display:block;color:#FEF5F0;margin:6px 0 2px}.zl .cards span{color:#A39E8E;font-size:14px}
@media(max-width:520px){.zl .cards{grid-template-columns:1fr}}
.zl .foto2{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:center;margin:18px 0}.zl .foto2 .img{height:220px;border-radius:14px;background:url(""" + FOTO + """operacoes/op12.webp) center/cover}
.zl .foto2 small{display:block;font-size:11px;color:#A39E8E;margin-top:6px}
@media(max-width:520px){.zl .foto2{grid-template-columns:1fr}}
.zl .oferta{border:2px solid #C9B37E;border-radius:16px;padding:18px;background:#0d110b}
.zl .resumo{list-style:none;padding:0;margin:0 0 6px}.zl .resumo li{display:flex;justify-content:space-between;gap:10px;padding:8px 0;border-top:1px solid rgba(201,179,126,.18);font-size:15px}.zl .resumo li span{color:#FEF5F0}.zl .resumo li small{color:#A39E8E}
.zl .bump{display:flex;gap:12px;align-items:flex-start;border:1px dashed #C9B37E;border-radius:12px;padding:14px;margin:14px 0;background:rgba(201,179,126,.07)}
.zl .bump input{width:22px;height:22px;flex:none;margin-top:2px;accent-color:#C9B37E}.zl .bump span{color:#DED6BF;font-size:15px}.zl .bump b{color:#FEF5F0}
.zl .selo{display:flex;gap:12px;align-items:center;margin:16px 0 0;padding:14px;border-radius:12px;background:#1B2117}.zl .selo b{white-space:nowrap;font-family:"Cormorant Garamond",serif;font-size:30px;color:#C9B37E;font-weight:500;line-height:1}.zl .selo span{color:#DED6BF;font-size:14px}
.zl .faq .q{border-top:1px solid rgba(201,179,126,.2);padding:14px 0}.zl .faq .cm-accordion-header{color:#FEF5F0;font-weight:600;cursor:pointer}.zl .faq .cm-accordion-content p{margin:8px 0 0;font-size:15px}
.zl .fixa{position:fixed;left:0;right:0;bottom:0;z-index:50;background:rgba(4,6,5,.96);border-top:1px solid rgba(201,179,126,.35);padding:10px 16px}
.zl .fixa{display:none}@media(max-width:820px){.zl .fixa{display:block}}
.zl .fixa .btn{max-width:640px;margin:0 auto;padding:14px 16px;font-size:17px}
.zl .rod{text-align:center;font-size:12px;padding:24px 16px}.zl .rod span{color:#7d796d}
</style>"""

barras = "".join(f'<div class="bar"><span>{n}</span><span>{v}/5</span></div><div class="tr"><i class="{"p" if p else ""}" style="width:{v * 20}%"></i></div>' for n, v, p in DIMS)
faq = [("Em quanto tempo eu começo a usar?", "No mesmo dia. O acesso chega por e-mail assim que o pagamento é confirmado, e o diagnóstico leva cerca de 15 minutos."),
       ("Serve para casa, apartamento, pousada ou glamping?", "Sim. O método olha a oferta com os olhos do hóspede e vale para qualquer hospedagem."),
       ("Preciso saber planilha ou tecnologia?", "Não. A ferramenta abre no celular e faz as contas. Você só responde e escolhe as ações."),
       ("Isso garante mais reservas?", "Não. Reservas dependem da região, da época, da concorrência e da execução. O que você leva com certeza é o diagnóstico, as prioridades e o plano prontos para executar."),
       ("E se eu não gostar?", "Você tem 7 dias para pedir o reembolso, como prevê o Código de Defesa do Consumidor.")]
faq_html = "".join(f'<div class="q"><div class="cm-accordion-header">{q}</div><div class="cm-accordion-content"><p>{a}</p></div></div>' for q, a in faq)

corpo = f"""
<div class="zl">
<section class="split" data-cx-section="hero">
<div class="foto" role="img" aria-label="Foto real da Zion Bubble Glamping" data-cx-image-slot="hero" data-cx-image-hint="Foto do produto, 16:9" data-cx-image-kind="ambient"></div>
<div class="txt">
<span class="k">Zion Collection · Guia + ferramenta</span>
<h1>Seu Airbnb está vazio? <em>O problema pode estar na sua oferta.</em></h1>
<div class="formula">
<div class="f1"><span class="fk">1 · Aprenda</span><strong>o passo a passo para descobrir o que está afastando o hóspede da sua oferta</strong></div>
<div class="f2"><span class="fk">2 · Receba</span><ul><li>Diagnóstico Zion de Oferta (celular e planilha)</li><li>E-book de 60 páginas</li><li>Aula + videoaula prática</li><li>3 fichas para imprimir</li></ul></div>
<div class="f3"><span class="fk">3 · Para ter</span><ul><li>Clareza do que mudar primeiro: as 3 prioridades</li><li>Uma oferta mais clara para o hóspede que compara</li><li>Um plano de 30 dias com prazo e forma de medir</li></ul></div>
</div>
<div class="preco"><b>R$ 47</b><span>pagamento único · Pix ou cartão</span></div>
<a class="btn" href="#oferta" data-cx-cta>{CTA}</a>
<div class="confia"><span>✓ Acesso no mesmo dia</span><span>✓ 7 dias para reembolso</span><span>✓ Airbnb, casas, apartamentos, pousadas e glampings</span></div>
<span class="leg">Foto: Zion Bubble Glamping (SC), real, onde nasceu o método.</span>
</div>
</section>

<section class="sec musgo" data-cx-section="problem"><div class="w">
<span class="k">Você se reconhece?</span>
<h2>Baixar a diária <em>não conserta</em> uma oferta confusa.</h2>
<ul class="dor"><li>Semanas livres no calendário e nenhuma pista do porquê.</li><li>Mudanças feitas no escuro: preço, foto e texto, tudo ao mesmo tempo.</li><li>Nenhum número para saber se alguma coisa melhorou.</li></ul>
<p style="margin-top:16px">O hóspede compara fotos, título, avaliações e a sua resposta antes de olhar o preço. Se a oferta não convence, desconto só faz você ganhar menos pelo mesmo problema.</p>
</div></section>

<section class="sec" data-cx-section="solution"><div class="w">
<span class="k">Como funciona</span>
<h2>15 minutos para <em>saber por onde começar.</em></h2>
<div class="resul">
<div><b>1</b><strong>Você dá 7 notas à sua oferta</strong><span>De 0 a 5, sempre com uma evidência: foto, avaliação, mensagem ou número.</span></div>
<div><b>2</b><strong>A ferramenta calcula e prioriza</strong><span>Pontuação de 0 a 100 e as 3 mudanças que mais pesam na decisão do hóspede.</span></div>
<div><b>3</b><strong>Você sai com o plano de 30 dias</strong><span>Cada ação com responsável, prazo, custo e como medir. Em PDF.</span></div>
</div>
<div class="demo"><div class="topo"><div class="anel"><span>63</span></div><div><span class="k" style="margin:0 0 2px">Exemplo · dados fictícios</span><b style="font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:500;color:#FEF5F0">Ajustes prioritários</b></div></div>{barras}</div>
<p class="aviso">Tela do Diagnóstico Zion de Oferta. Em vermelho, as 3 prioridades. O que acontece com as reservas depende da sua execução: nós entregamos a clareza e o plano.</p>
<a class="btn" href="#oferta" data-cx-cta style="margin-top:18px">{CTA}</a>
</div></section>

<section class="sec musgo"><div class="w">
<span class="k">O que você recebe</span>
<h2>Tudo isso <em>por R$ 47.</em></h2>
<div class="cards">
<div><b>7 notas</b><strong>Diagnóstico Zion de Oferta</strong><span>No celular e em planilha. Calcula a pontuação, as prioridades e monta o plano.</span></div>
<div><b>60 páginas</b><strong>E-book com 10 capítulos</strong><span>Do calendário vazio ao plano, com um exercício por capítulo.</span></div>
<div><b>2 aulas</b><strong>Aula e videoaula prática</strong><span>A ferramenta preenchida tela por tela, com legenda.</span></div>
<div><b>3 fichas</b><strong>Para imprimir</strong><span>Diagnóstico, plano de ação e registro diário de 30 dias.</span></div>
</div>
<div class="foto2"><div><div class="img" role="img" aria-label="Foto real da Zion Bubble Glamping"></div><small>Foto real · Zion Bubble Glamping (SC)</small></div>
<p style="margin:0;font-size:15px">O método parte da rotina usada nas unidades da Zion Hotel Group International: evidência, poucas prioridades, execução com prazo e medição.</p></div>
</div></section>

<section class="sec" id="oferta" data-cx-section="offer"><div class="w">
<span class="k">Garanta o seu acesso</span>
<h2>Comece hoje <em>por R$ 47.</em></h2>
<div class="oferta">
<div class="formula">
<div class="f1"><span class="fk">1 · Aprenda</span><strong>o passo a passo para descobrir o que está afastando o hóspede da sua oferta</strong></div>
<div class="f2"><span class="fk">2 · Receba</span><ul><li>Diagnóstico Zion de Oferta (celular e planilha)</li><li>E-book de 60 páginas</li><li>Aula + videoaula prática</li><li>3 fichas para imprimir</li></ul></div>
<div class="f3"><span class="fk">3 · Para ter</span><ul><li>Clareza do que mudar primeiro: as 3 prioridades</li><li>Uma oferta mais clara para o hóspede que compara</li><li>Um plano de 30 dias com prazo e forma de medir</li></ul></div>
</div>
<div class="preco"><b>R$ 47</b><span>pagamento único · acesso no mesmo dia</span></div>
<label class="bump"><input class="cm-checkmark-checkbox" type="checkbox" data-orderbump-id="{BUMP}"><span><b>Sim, quero o Calendário comercial de 30 dias por + R$ 19.</b> Uma ação curta por dia, já escrita, para colocar o plano em prática. Opcional: o guia funciona sem ele.</span></label>
<div data-cx-checkout></div>
<div class="selo"><b>7 dias</b><span>Se não fizer sentido para você, peça o reembolso em até 7 dias após a compra.</span></div>
</div>
</div></section>

<section class="sec musgo faq" data-cx-section="faq"><div class="w"><span class="k">Dúvidas</span>{faq_html}</div></section>

<section class="sec" data-cx-section="cta"><div class="w" style="text-align:center">
<h2>Aprenda, receba <em>e saia com o plano.</em></h2>
<p>Diagnóstico, 3 prioridades e plano de 30 dias. Hoje.</p>
<a class="btn" href="#oferta" data-cx-cta>{CTA}</a>
</div></section>
<div class="rod"><span>Zion Hotel Group International · material educativo: resultados dependem do contexto e da execução · suporte WhatsApp +55 48 6137-1061</span></div>
<div class="fixa"><a class="btn" href="#oferta" data-cx-cta>{CTA}</a></div>
</div>"""
(A / "dist").mkdir(exist_ok=True)
(A / "dist/clickmax_lt.html").write_text(css + corpo)
print("landing/dist/clickmax_lt.html", len(css + corpo), "caracteres")
