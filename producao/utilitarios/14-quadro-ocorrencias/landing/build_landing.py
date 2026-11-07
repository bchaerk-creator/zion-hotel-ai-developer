"""Gera landing/dist/clickmax.html da Ferramenta 14 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
V, A_, M = "#F4C7C3", "#FCE8B2", "#C8E6C0"
t1 = tela("PAINEL", "1 unidade bloqueada · 2 atrasadas", V,
          [linha("Cabana 1 · 0 aberta(s)", "Liberada", M), linha("Cabana 2 · 2 aberta(s)", "Liberada", M),
           linha("Cabana 3 · 1 aberta(s)", "Liberada", M), linha("Suíte Jardim · 1 aberta(s)", "BLOQUEADA", V)],
          "A fechadura com defeito marcada como bloqueio trava a Suíte Jardim.")
t2 = tela("OCORRÊNCIAS", "4 abertas · 1 a completar", A_,
          [linha("Cabana 2 · Ar-condicionado", "Atrasada", V), linha("Suíte Jardim · Fechadura", "Atrasada", V),
           linha("Cabana 3 · Deck", "Aberta", A_), linha("Cabana 1 · Abajur", "Fechada sem descrição", M), linha("Cabana 2 · Banheiro", "Complete os dados", V)],
          "Sem responsável, a ocorrência pede para ser completada.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow">Ferramenta 14 · Zion Hospitality Business</span>
<h1>O problema foi avisado. <em>Alguém resolveu?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para registrar cada problema com responsável, prioridade e prazo, acompanhar até resolver e saber quais unidades não podem receber hóspede.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero o meu quadro</a><span class="micro">Planilha + ficha + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow">O problema</span>
<h2>Problema no grupo de mensagens <em>some</em>.</h2>
<p>O chuveiro esquentando pouco, a fechadura falhando, a tábua solta no deck. Cada aviso chega por um canal, ninguém sabe quem ficou de resolver e o próximo hóspede descobre antes de você.</p>
<ul class="lista"><li>Não fica claro quem é o responsável.</li><li>Não existe prazo, então tudo vira "depois".</li><li>A unidade é liberada com um problema que impede a estadia.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow">Como funciona</span>
<h2>Uma linha por problema. <em>Um painel para decidir.</em></h2>
<p>Você registra o problema com unidade, responsável e prioridade. O prazo sai da prioridade, o atraso fica destacado e a unidade aparece como BLOQUEADA quando há um problema aberto que impede receber hóspede.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (dados fictícios, data de referência 07/11/2026).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Combine prioridades e prazos com quem resolve.</li><li><b style="color:#C9B37E">2.</b> Registre cada problema com responsável.</li><li><b style="color:#C9B37E">3.</b> Feche com data, descrição e custo.</li><li><b style="color:#C9B37E">4.</b> Confira o painel antes de cada entrada.</li></ul>
<p>A lógica parte da rotina de manutenção usada nas unidades da Zion, com ronda diária e nenhum problema sem responsável, generalizada para qualquer hospedagem.</p>
<figure style="margin:18px 0 0"><img src="{BASE}assets/operacoes/op08.webp" alt="Unidade da Zion Bubble Glamping" style="width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:6px;display:block"><figcaption style="font-size:13px;color:#A39E8E;margin-top:6px">Foto real · unidade da Zion Bubble Glamping, onde essa rotina de manutenção é usada.</figcaption></figure></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/ocorrencias-14/capa.jpg" alt="Capa do produto: Quadro de Ocorrências e Manutenção" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco com ajustes, cadastros, ocorrências e painel</li><li>Exemplo preenchido (dados fictícios)</li><li>Ficha de ronda para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow">Perguntas frequentes</span>
<details><summary>Serve para apartamento ou casa de temporada?</summary><p>Serve. Funciona com uma unidade ou com várias, com você sozinho ou com equipe e prestadores.</p></details>
<details><summary>Avisa o responsável sozinha?</summary><p>Não. A planilha mostra o que está aberto e atrasado; alguém precisa olhar o painel e cobrar.</p></details>
<details><summary>Os prazos são fixos?</summary><p>Não. Vêm com um ponto de partida por prioridade, e você ajusta ao tempo real da sua equipe.</p></details>
<details><summary>Diz como consertar?</summary><p>Não. Gás, elétrica, piscina e estrutura seguem o profissional habilitado. A planilha registra e acompanha.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Nenhum problema <em>sem dono</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o meu quadro</a><span class="micro">Material educativo. Não garante avaliações, reservas nem ocupação.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))
