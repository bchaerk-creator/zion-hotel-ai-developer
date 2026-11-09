"""Gera landing/dist/clickmax.html da Ferramenta 18 (estilo da página da Ferramenta 17). Uso: python3 -I landing/build_landing.py"""
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
V, A_, M, G = "#F4C7C3", "#FCE8B2", "#C8E6C0", "#E6E6E6"
t1 = tela("PRÓXIMAS TAREFAS", "Hoje: 15/11/2026", A_,
          [linha("Gás: mangueira e regulador", "08/11 · Atrasada", V), linha("Filtro do ar · Chalé 1", "09/11 · Atrasada", V),
           linha("Calhas e telhas", "16/11 · Em breve", A_), linha("Detector de fumaça · Chalé 1", "19/11 · Em breve", A_),
           linha("Refil do filtro de água", "22/11 · Em breve", A_), linha("Detector de fumaça · Chalé 2", "Sem registro", G)],
          "A próxima data de cada tarefa sai da última vez que foi feita.")
t2 = tela("PAINEL DA SEMANA", "Há tarefas atrasadas: comece por elas", V,
          [linha("Tarefas no plano", "16", "#FFFFFF"), linha("Atrasadas", "2", V), linha("Vencem em breve (7 dias)", "4", A_),
           linha("Em dia", "9", M), linha("Custo anual estimado", "R$ 4.731,38", "#FFFFFF")],
          "Abra uma vez por semana e comece pelo que passou da data.")
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow" style="color:#C9B37E">Ferramenta 18 · Zion Hospitality Business</span>
<h1>O problema aparece <em>quando o hóspede chega?</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para montar um plano de manutenção preventiva da sua hospedagem: o que conferir, de quanto em quanto tempo, quem faz e o que está atrasado.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero o planner</a><span class="micro" style="color:#A39E8E">Planilha + ficha de ronda + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow" style="color:#C9B37E">O problema</span>
<h2>Ninguém lembra <em>da última vez</em>.</h2>
<p>O filtro do ar, a pilha do detector, a calha, a mangueira do gás, o rejunte do box: cada um tem o seu tempo, e quase sempre a gente só lembra quando quebra. Aí o conserto vira urgência, com hóspede na unidade.</p>
<ul class="lista"><li>Tarefas que dependem da memória de alguém.</li><li>Sem data da última vez, sem saber o que está atrasado.</li><li>Manutenção fora do orçamento do ano.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow" style="color:#C9B37E">Como funciona</span>
<h2>Plano, registro, <em>painel</em>.</h2>
<p>A planilha já traz 21 tarefas sugeridas. As de todo dia partem da ronda usada nas unidades da Zion; as demais são comuns a qualquer hospedagem. Você ajusta, define quem faz e anota cada tarefa feita. A planilha calcula a próxima data e mostra, toda semana, o que está atrasado e o que vem a seguir.</p>
<div class="demo">{t1}{t2}</div>
<p style="font-size:14px;color:#A39E8E">Resultados calculados pela planilha no arquivo de exemplo (hospedagem, pessoas, datas e custos fictícios).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Ajuste a lista e as frequências à sua hospedagem.</li><li><b style="color:#C9B37E">2.</b> Defina o responsável e anote a última vez.</li><li><b style="color:#C9B37E">3.</b> Faça a ronda com a ficha e registre o que foi feito.</li><li><b style="color:#C9B37E">4.</b> Abra o Painel toda semana e comece pelas atrasadas.</li></ul></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow" style="color:#C9B37E">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/manutencao-18/capa.jpg" alt="Capa do produto: Planner de Manutenção Preventiva" data-cx-image-slot="offer" data-cx-image-hint="Capa do produto" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco com 21 tarefas sugeridas, registro e painel</li><li>Exemplo preenchido (dados fictícios)</li><li>Ficha de ronda preventiva para imprimir</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow" style="color:#C9B37E">Perguntas frequentes</span>
<details><summary>As frequências valem para qualquer equipamento?</summary><p>São um ponto de partida. Ajuste ao manual do fabricante, às regras locais e ao profissional responsável.</p></details>
<details><summary>Substitui eletricista, técnico de gás ou laudos?</summary><p>Não. A planilha organiza o que fazer e quando; serviços técnicos, vistorias e laudos continuam com profissionais habilitados.</p></details>
<details><summary>Serve para uma casa só?</summary><p>Sim. Funciona para uma unidade ou várias, com até 120 tarefas por arquivo.</p></details>
<details><summary>E quando algo quebra?</summary><p>O planner é para a preventiva. O conserto vai para um quadro de ocorrências, com prazo e responsável.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Cuide antes <em>de quebrar</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o planner</a><span class="micro" style="color:#A39E8E">Material educativo. Não garante ausência de defeitos, reservas nem resultado financeiro.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))
