"""Gera landing/dist/clickmax.html da Ferramenta 30 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
import pathlib
A = pathlib.Path(__file__).resolve().parent
src = (A.parents[1] / "17-checklist-limpeza/landing/build_landing.py").read_text()
estilo = src[src.index('<link href='):src.index('</style>') + len('</style>')].replace("{{", "{").replace("}}", "}")
BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
def linha(a, b, cor):
    return (f'<div style="display:flex;justify-content:space-between;gap:6px;padding:7px 10px;border-top:1px solid #DED6BF;font-size:12px">'
            f'<span style="color:#1B2117">{a}</span><span style="color:#1B2117;background:{cor};padding:0 6px;border-radius:4px;font-weight:600">{b}</span></div>')
def tela(tit, status, cor, linhas, leg):
    return (f'<figure style="margin:0"><div style="background:#fff;border-radius:10px;overflow:hidden"><div style="background:#1B2117;padding:10px">'
            f'<span style="color:#C9B37E;font-size:11px;letter-spacing:.12em">{tit} · EXEMPLO FICTÍCIO</span></div>'
            f'<div style="background:{cor};padding:10px;font-weight:700;font-size:13px"><span style="color:#040605">{status}</span></div>{"".join(linhas)}</div>'
            f'<figcaption>{leg}</figcaption></figure>')
V, A_, M, G, AZ = "#F4C7C3", "#FCE8B2", "#C8E6C0", "#E6E6E6", "#D6E4F0"
t1 = tela("MENSAGENS DA SAÍDA", "Café da manhã na trilha · 12/12", M,
          [linha("B02 Confirmação da reserva", "Logo", M), linha("B03 Saída confirmada", "10/12", M), linha("B05 Lembrete da véspera", "11/12", M),
           linha("B06 Briefing de quem conduz", "11/12", M), linha("B08 Agradecimento", "12/12", M), linha("B07 Mudança por clima", "Sob demanda", G)],
          "Cada texto já sai com o dia de enviar.")
t2 = tela("FICHA DA SAÍDA", "Mínimo atingido: use a B03", M,
          [linha("Participantes", "5", "#FFFFFF"), linha("Mínimo para confirmar", "4", "#FFFFFF"), linha("Textos prontos", "8 de 8", M), linha("Restrições do grupo", "Anotadas", AZ)],
          "Se faltar um dado, a planilha avisa antes de você enviar.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 30 · Zion Hospitality Business</span>
<h1>Toda saída, <em>a mesma explicação de novo?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para escrever o briefing da sua experiência uma vez e gerar, a cada saída, a descrição, as mensagens ao cliente e o briefing de quem conduz.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings que oferecem passeios, cafés, trilhas e vivências.</span><a class="btn" href="#oferta" data-cx-cta>Quero o gerador de briefing</a><span class="micro" style="color:#A39E8E">Planilha + modelos em PDF + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>A informação fica <em>espalhada</em>.</h2>
<p>O que levar está num áudio, o ponto de encontro numa conversa antiga, a regra de chuva na cabeça de alguém. O hóspede chega sem casaco, o guia não sabe da restrição alimentar e ninguém lembrou de avisar que faltou gente para confirmar.</p>
<ul class="lista"><li>Cada mensagem escrita do zero.</li><li>Quem conduz recebe o grupo sem saber nada dele.</li><li>Mínimo, clima e cancelamento sem regra escrita.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Escreva uma vez, <em>use em toda saída</em>.</h2>
<p>Você preenche a ficha da experiência uma vez: o que acontece, duração, ponto de encontro, o que está incluído, o que levar, para quem é, regra de chuva, mínimo de participantes e cancelamento. A cada saída, anota cliente, data, horário e pessoas. A planilha monta 8 textos prontos para copiar, com o dia de enviar cada um, e avisa o que falta preencher.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (experiência, pessoas e datas fictícias).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Preencha a ficha da experiência.</li><li><b style="color:#C9B37E">2.</b> A cada reserva, anote os dados da saída.</li><li><b style="color:#C9B37E">3.</b> Confira o mínimo: confirmar ou remarcar.</li><li><b style="color:#C9B37E">4.</b> Copie cada texto no dia indicado.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/briefing-30/capa.jpg" alt="Capa do produto: Gerador de Briefing de Experiência" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco que gera 8 textos com a data de envio</li><li>Exemplo preenchido (dados fictícios)</li><li>Modelos das mensagens em PDF</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>Serve para que tipo de experiência?</summary><p>Passeios, trilhas, cafés especiais, aulas, vivências: qualquer atividade com data, horário e grupo.</p></details>
<details><summary>Verifica a segurança ou as autorizações da atividade?</summary><p>Não. A planilha organiza o que você informa. Segurança, seguro e autorizações seguem com você e com profissionais habilitados.</p></details>
<details><summary>Envia as mensagens sozinha?</summary><p>Não. Ela monta os textos e diz o dia; você copia e envia pelo seu WhatsApp ou e-mail.</p></details>
<details><summary>Serve para mais de uma experiência?</summary><p>Sim, um arquivo por experiência: é só duplicar.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Escreva uma vez, <em>explique sempre igual</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o gerador de briefing</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante vendas, reservas nem lotação das saídas.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))
