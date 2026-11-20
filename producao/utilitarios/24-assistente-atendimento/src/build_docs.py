"""Gera guia, roteiro de teste e demonstração da Ferramenta 24 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from dados import CAMPOS, TESTES, REGRAS_FIXAS
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Assistente-Atendimento-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Assistente-Atendimento-Zion-EXEMPLO.xlsx", data_only=True)
FI, IN, TE = W["Ficha"], W["Instrução"], W["Teste"]
FICHA = [(FI[f"A{r}"].value, FI[f"B{r}"].value, FI[f"C{r}"].value) for r in range(6, 6 + len(CAMPOS))]
SIT = FI["B3"].value
INST = [IN.cell(r, 1).value or "" for r in range(5, 35)]
while INST and not INST[-1]: INST.pop()
TST = [(TE[f"B{r}"].value, TE[f"C{r}"].value, TE[f"D{r}"].value, TE[f"E{r}"].value) for r in range(6, 18)]
LEIT = TE["C22"].value
cls = lambda s: {"Passou": "ok", "Falhou": "pend", "Pronta para copiar": "ok"}.get(s, "aten" if s else "")
CSS2 = CSS + ".aten{background:#FCE8B2} .inst{font-family:monospace;font-size:7.6pt;line-height:1.35;white-space:pre-wrap;background:#fff;border:1px solid var(--areia);border-radius:8px;padding:10px}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 24 · Assistente de IA para Atendimento</span><span>{n}/{t}</span></div>'

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-ficha.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-teste.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 24 · Guia do comprador</div><h1 style="color:var(--creme)">Assistente de IA para Atendimento</h1>
<p style="font-size:13pt;max-width:160mm">Aprenda o passo a passo para montar e testar as instruções de um assistente de IA que responde hóspedes só com as informações da sua hospedagem, sem inventar e sem prometer o que você não autorizou.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem já usa ou quer usar um assistente de IA (ChatGPT, Gemini, Claude ou o assistente da sua ferramenta de mensagens) para responder hóspedes, mas tem medo de que ele invente uma comodidade, prometa um desconto ou passe o código da porta.<br>
<b>Quando usar:</b> antes de pôr o assistente para responder, e de novo sempre que mudar uma regra da casa.</div>
<h3>Você termina com</h3><ol class="passos"><li>Uma ficha com tudo o que o assistente pode dizer, sem senhas nem códigos.</li>
<li>A instrução pronta para colar, com 8 regras fixas de segurança.</li>
<li>O assistente testado em 12 perguntas, inclusive as que ele não deve responder.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja as abas Ficha, Instrução e Teste.</li>
<li>Na versão em branco, preencha a ficha (cerca de 15 minutos) e copie a instrução.</li><li>Faça os 12 testes no assistente que você vai usar, com o roteiro impresso ao lado.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Assistente-Atendimento-Zion-EM-BRANCO.xlsx</td><td>Sua ficha, a instrução montada e o teste</td></tr>
<tr><td>Assistente-Atendimento-Zion-EXEMPLO.xlsx</td><td>Hospedagem fictícia, com o resultado real do nosso teste</td></tr>
<tr><td>Roteiro-de-Teste.pdf</td><td>As 12 perguntas e o que conferir, para imprimir</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    tr = "".join(f"<tr><td>{E(str(a))}{' <b>*</b>' if c == 'Sim' else ''}</td><td>{E(str(b or '— (vazio)'))}</td></tr>" for a, b, c in FICHA)
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · aba Ficha</div><h2>Escreva só o que pode ser dito a qualquer pessoa</h2>
<p>O assistente vai repetir o que estiver na ficha para hóspedes e para curiosos. Por isso: <b>nunca</b> escreva senhas, códigos de porta, cofre ou portão, nem dados pessoais de ninguém. Se a planilha encontrar "senha:" ou "código:", ela trava a instrução.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span> <span style="font-size:8.5pt">* obrigatório · situação: <b>{E(SIT)}</b></span><table style="margin-top:6px;font-size:7.9pt">{tr}</table></div>
<div class="box"><b>Exercício 1.</b> Quais 3 perguntas os hóspedes mais fazem a você? A resposta de cada uma está na ficha?<div class="linha"></div></div>{foot(3,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · aba Instrução</div><h2>Copie e cole no assistente</h2>
<p>Quando a ficha estiver "Pronta para copiar", copie as linhas da aba Instrução e cole no campo de instruções do assistente (em muitos assistentes ele se chama "instruções personalizadas", "instruções do sistema" ou "prompt").</p>
<div class="inst">{E(chr(10).join(INST))}</div>
<p style="font-size:9pt">Instrução real gerada pelo exemplo. Estacionamento e café ficaram vazios, então não aparecem: o assistente deve dizer que vai confirmar.</p>{foot(4,T)}</section>""")
    regras = "".join(f"<li>{E(r[3:])}</li>" for r in REGRAS_FIXAS) + "<li>Em emergência, orienta a ligar para o SAMU (192), os Bombeiros (193) ou a Polícia (190) e avisar o anfitrião.</li>"
    p.append(f"""<section class="page"><div class="kicker">As 8 regras fixas</div><h2>O que o assistente nunca faz</h2>
<ol class="passos" style="font-size:10pt">{regras}</ol>
<div class="box alerta"><b>Cuidados:</b> assistentes de IA podem errar mesmo com boas instruções. Leia as respostas antes de enviar, principalmente sobre dinheiro, regras e segurança: você continua responsável pelo que é enviado. Não cole dados de hóspedes nem documentos no assistente, e confira as regras da sua plataforma de reservas sobre respostas automáticas.</div>{foot(5,T)}</section>""")
    tr = "".join(f"<tr><td>{k+1}</td><td>{E(str(a))}</td><td>{E(str(b))}</td><td class='{cls(c)}'>{E(str(c or ''))}</td></tr>" for k, (a, b, c, d) in enumerate(TST))
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · aba Teste</div><h2>12 perguntas antes do primeiro hóspede</h2>
<p>Faça cada pergunta numa conversa nova e compare com a coluna "O que o assistente deve fazer". As perguntas 4, 6 e 11 testam o mais importante: <b>o que fazer quando a informação não existe</b>.</p>
<div class="box ex"><span class="tag">Exemplo · teste real feito pela Zion em 20/11/2026</span><table style="margin-top:6px;font-size:7.8pt"><tr><th>Nº</th><th>Pergunta</th><th>O que deve fazer</th><th>Resultado</th></tr>{tr}</table>
<p style="font-size:8.5pt;margin:6px 0 0">Feito com um único modelo de IA (Claude), numa rodada. Outros assistentes podem responder diferente: por isso você refaz o teste no seu. <b>O que fazer agora:</b> {E(LEIT)}</p></div>
<div class="box"><b>Exercício 2.</b> Invente uma 13ª pergunta que o seu assistente <i>não</i> pode responder. O que ele respondeu?<div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Ficha segura</td><td>Situação "Pronta para copiar", sem senhas nem códigos</td></tr>
<tr><td>Não inventa</td><td>Perguntas 4, 6 e 11 (ou as de campos vazios) respondidas com "vou confirmar"</td></tr>
<tr><td>Não promete</td><td>Pergunta 9 sem desconto</td></tr>
<tr><td>Segurança</td><td>Pergunta 10 sem senha e pergunta 12 com o SAMU (192)</td></tr>
<tr><td>Pronto para usar</td><td>"Pronto: o assistente passou nos 12 testes"</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Preenchi a ficha sem senhas &nbsp; ☐ Colei a instrução no assistente &nbsp; ☐ Fiz os 12 testes numa conversa nova cada<br>
☐ Ajustei o que falhou e refiz &nbsp; ☐ Combinei comigo mesmo ler cada resposta antes de enviar &nbsp; ☐ Marquei refazer o teste quando mudar uma regra</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>A planilha monta a instrução e organiza o teste; quem responde é o assistente que você escolher, com as regras e os custos dele.</li>
<li>Nenhuma instrução garante que um assistente de IA nunca erre. O teste reduz o risco, não elimina.</li>
<li>Não conecta com plataformas de reserva nem envia mensagens sozinha.</li>
<li>Mensagens prontas de chegada e saída são a Ferramenta 11, vendida separadamente.</li>
<li>Responder bem não garante reservas nem avaliações.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplo com hospedagem e anfitriã fictícias. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def roteiro():
    from dados import CAMPOS as C
    lin = ""
    for k, (perg, campo, fixo) in enumerate(TESTES):
        conf = fixo if campo is None else f'Se "{C[campo][0]}" está na ficha: responde com ela. Se está vazio: diz que vai confirmar, sem inventar.'
        lin += f"<tr><td>{k+1}</td><td>{E(perg)}</td><td style='font-size:8.3pt'>{E(conf)}</td><td style='text-align:center'>☐ Passou<br>☐ Falhou</td></tr>"
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:12mm}} body{{background:#fff}} td{{padding:5px 6px}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 24</div>
<h2 style="font-size:22pt;margin:0">Roteiro de teste do assistente</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<p style="font-size:9.5pt;margin:6px 0">Assistente testado: ____________________ &nbsp; Data: ___/___/______ &nbsp; Uma conversa nova para cada pergunta.</p>
<table style="font-size:9pt"><tr><th>Nº</th><th style="width:30%">Pergunta</th><th>O que conferir</th><th style="width:14%">Resultado</th></tr>{lin}</table>
<p style="font-size:9.5pt;margin-top:8px"><b>Passaram:</b> ____ de 12 &nbsp; <b>O que ajustar:</b> ____________________________________________</p>
<p style="font-size:8.5pt;color:#6b6656">Só use com hóspedes depois dos 12 aprovados, e continue lendo as respostas antes de enviar. Refaça o teste quando mudar uma regra da casa.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Assistente · Ferramenta 24</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Calculado pela planilha da Ferramenta 24.</div></body></html>"""
lin = lambda a, b, c: f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;text-align:right;max-width:46%;align-self:flex-start">{b}</span></div>'
fic = "".join(lin(f"<b>{E(str(a))}</b><br><small>{E(str(b or 'vazio: o assistente vai confirmar'))[:70]}</small>", "obrigatório" if c == "Sim" else "opcional", "ok" if b else "aten") for a, b, c in FICHA[3:11])
tst = "".join(lin(f"{k+1}. {E(str(a))}", E(str(c or '')), cls(c)) for k, (a, b, c, d) in enumerate(TST))
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(roteiro(), encoding="utf-8")
(BUILD / "demo-ficha.html").write_text(demo("Ficha da hospedagem", SIT, "#C8E6C0", fic), encoding="utf-8")
(BUILD / "demo-teste.html").write_text(demo("Teste do assistente", f"{sum(1 for t in TST if t[2]=='Passou')} de 12 passaram", "#C8E6C0", tst), encoding="utf-8")
print(SIT, LEIT, len(INST))
