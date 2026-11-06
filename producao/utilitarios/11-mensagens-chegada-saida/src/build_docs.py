"""Gera os HTML do guia, dos modelos imprimíveis e da demonstração da Ferramenta 11 com os valores
REAIS recalculados da planilha (LibreOffice). Depois: node src/render.js build dist
Uso: python3 -I src/build_docs.py dist build"""
import sys, pathlib, subprocess, tempfile, html, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mensagens import CAMPOS, MENSAGENS, rotulo
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
REPO = pathlib.Path(__file__).resolve().parents[4]
FONTS, BRAND, OPS = REPO / "docs/assets/fonts", REPO / "docs/brand", REPO / "docs/assets/operacoes"
E = html.escape; N = len(MENSAGENS)

def recalc():
    tmp = pathlib.Path(tempfile.mkdtemp()); out = tmp / "o"; out.mkdir()
    ex = DIST / "Kit-Mensagens-Zion-EXEMPLO.xlsx"; wb = load_workbook(ex); f = wb["Ficha"]
    for r in range(1, 60):
        if str(f.cell(r, 1).value or "").startswith("Wi-Fi: senha"): f.cell(r, 2).value = None
    var = tmp / "SemSenha.xlsx"; wb.save(var)
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(out), str(ex), str(var)],
                   check=True, capture_output=True, timeout=300)
    return load_workbook(out / ex.name, data_only=True), load_workbook(out / var.name, data_only=True)
EXW, SSW = recalc()
def msgs(wb):
    m = wb["Mensagens"]
    return [dict(id=m[f"A{r}"].value, tit=m[f"B{r}"].value, quando=m[f"C{r}"].value, data=m[f"D{r}"].value, txt=m[f"E{r}"].value or "", st=m[f"F{r}"].value)
            for r in range(6, 6 + N)], m["C3"].value, m["E3"].value
EXM, EXP, EXD = msgs(EXW); SSM, SSP, _ = msgs(SSW)
def ficha(wb):
    f = wb["Ficha"]; return {str(f.cell(r, 1).value).rstrip(" *"): f.cell(r, 2).value for r in range(1, 60) if f.cell(r, 1).value}
FX = ficha(EXW)

CSS = f"""
@font-face {{ font-family: Cormorant; src: url('{(FONTS/'cormorant.woff2').as_uri()}'); }}
@font-face {{ font-family: Aventa; src: url('{(FONTS/'aventa.woff2').as_uri()}'); }}
:root {{ --musgo:#1B2117; --creme:#FEF5F0; --areia:#DED6BF; --terra:#8B714E; --dourado:#C9B37E; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: Aventa, Arial, sans-serif; color: var(--musgo); background: var(--creme); font-size: 11pt; line-height: 1.45; }}
h1, h2, h3 {{ font-family: Cormorant, Georgia, serif; font-weight: 600; margin: 0 0 .4em; line-height: 1.1; }}
h1 {{ font-size: 40pt; }} h2 {{ font-size: 26pt; }} h3 {{ font-size: 15pt; margin-top: .8em; }}
.kicker {{ font-size: 8.5pt; letter-spacing: .18em; text-transform: uppercase; color: var(--terra); font-weight: 700; margin-bottom: 6px; }}
.page {{ width: 210mm; height: 297mm; padding: 18mm 18mm 16mm; position: relative; overflow: hidden; page-break-after: always; background: var(--creme); }}
.page:last-child {{ page-break-after: auto; }}
.foot {{ position: absolute; bottom: 9mm; left: 18mm; right: 18mm; font-size: 7.5pt; color: #6b6656; display: flex; justify-content: space-between; border-top: 1px solid var(--areia); padding-top: 4px; }}
.box {{ background: #fff; border: 1px solid var(--areia); border-radius: 10px; padding: 12px 14px; margin: 10px 0; }}
.box.ex {{ border-left: 5px solid var(--dourado); }} .box.alerta {{ border-left: 5px solid #A0522D; }}
.tag {{ display:inline-block; font-size: 8pt; font-weight:700; padding: 2px 8px; border-radius: 99px; background: var(--musgo); color: var(--creme); }}
table {{ border-collapse: collapse; width: 100%; font-size: 9.5pt; }}
th {{ background: var(--musgo); color: var(--creme); text-align: left; padding: 5px 7px; font-weight: 600; }}
td {{ border-bottom: 1px solid var(--areia); padding: 5px 7px; vertical-align: top; }}
.ok {{ background:#C8E6C0; }} .pend {{ background:#F4C7C3; font-weight:700; }}
ol.passos li {{ margin: 0 0 6px; }} .linha {{ border-bottom: 1px solid #b9b19b; height: 22px; }}
.fict {{ color:#A0522D; font-weight:700; font-size: 8.5pt; }}
.bolha {{ background:#E7F3E2; border-radius: 10px 10px 10px 2px; padding: 9px 12px; font-size: 10pt; margin: 6px 0; }}
mark {{ background:#F4C7C3; font-weight:700; }}
"""
def foot(n, tot): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 11 · Kit de Mensagens de Chegada e Saída</span><span>{n}/{tot}</span></div>'
def marca(t): return re.sub(r"(\[PREENCHA: [^\]]+\])", r"<mark>\1</mark>", E(t))
def get(lst, mid): return next(x for x in lst if x["id"] == mid)

def guia():
    T = 7; p = []
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">
<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)"><img src="{(DIST/'demonstracao/demo-falta.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"><img src="{(DIST/'demonstracao/demo-pronta.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 11 · Guia do comprador</div>
<h1 style="color:var(--creme)">Kit de Mensagens de Chegada e Saída</h1>
<p style="font-size:13pt;max-width:155mm">Aprenda o passo a passo para enviar, no momento certo, as mensagens de confirmação, acesso, chegada, apoio durante a estadia e saída, com as informações da sua hospedagem.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas e glampings. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> anfitriões de aluguel por temporada, pousadas, glampings e pequenos hotéis que conversam com o hóspede por WhatsApp ou pela plataforma.<br>
<b>Quando usar:</b> a cada reserva, da confirmação até depois da saída.</div>
<h3>Você termina com</h3><ol class="passos"><li>Uma ficha com as informações da sua hospedagem, preenchida uma vez.</li>
<li>As {N} mensagens da jornada prontas para cada reserva, com o nome do hóspede, as datas e a data de envio de cada uma.</li>
<li>Duas respostas prontas para imprevistos: chegada fora do horário e problema durante a estadia.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 10 minutos).</li><li>Abra a versão de exemplo e veja as mensagens montadas.</li>
<li>Na versão em branco, preencha a ficha da hospedagem (cerca de 15 minutos).</li><li>Na próxima reserva, preencha nome e datas e siga a coluna "Data de envio".</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Kit-Mensagens-Zion-EM-BRANCO.xlsx</td><td>Sua planilha: ficha, mensagens montadas e modelos</td></tr>
<tr><td>Kit-Mensagens-Zion-EXEMPLO.xlsx</td><td>Uma hospedagem e uma reserva fictícias, com as {N} mensagens prontas</td></tr>
<tr><td>Mensagens-Modelo.pdf</td><td>Os {N} modelos com campos entre colchetes, para quem prefere copiar à mão</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    dicas = [("Nome da hospedagem", "Como o hóspede conhece o lugar", "Recanto Exemplo"),
             ("Como é o acesso", "Complete a frase \"O acesso é por...\"", FX.get("Como é o acesso")),
             ("Regras principais", "Frases curtas, com ponto final", FX.get("Regras principais")),
             ("O que fazer na saída", "Complete a frase \"Antes de sair, ...\"", FX.get("O que fazer na saída")),
             ("Dica para a chegada", "Opcional. Frase completa", FX.get("Dica para a chegada"))]
    tr = "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(str(c))}</td></tr>" for a, b, c in dicas)
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · aba Ficha</div><h2>Preencha a ficha uma vez</h2>
<p>As mensagens são montadas a partir da ficha. Escreva cada campo como ele vai aparecer na frase: a planilha não corrige nem completa.</p>
<table><tr><th>Campo</th><th>Como escrever</th><th>Exemplo (fictício)</th></tr>{tr}</table>
<div class="box"><b>Obrigatórios</b> (marcados com *): se ficarem vazios, a mensagem mostra <mark>[PREENCHA: nome do campo]</mark> e a Situação fica vermelha.<br>
<b>Opcionais</b> (mapa, estacionamento, código, link de avaliação, dica, orientação de emergência): se ficarem vazios, a frase some da mensagem.</div>
<div class="box"><b>Exercício 1.</b> Escreva como você explica o acesso à sua hospedagem em uma linha, começando por "O acesso é por...".<div class="linha"></div><div class="linha"></div></div>
<div class="box alerta"><b>Segurança:</b> se a senha da porta muda a cada reserva, use o campo "Código de acesso desta reserva" (parte de baixo da ficha), e não a ficha da hospedagem. Envie código e senha só ao hóspede da reserva, perto da chegada.</div>{foot(3,T)}</section>""")
    tr = "".join(f"<tr><td>{x['id']}</td><td>{E(x['tit'])}</td><td>{E(x['quando'])}</td><td>{E(str(x['data']))}</td></tr>" for x in EXM)
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · aba Mensagens</div><h2>Siga o calendário da reserva</h2>
<p>Na parte de baixo da ficha, preencha nome do hóspede, entrada e saída. A planilha calcula a data de envio de cada mensagem.</p>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span> Entrada em 12/12/2026, saída em 14/12/2026 ({E(str(EXD))}).
<table style="margin-top:8px"><tr><th>Nº</th><th>Mensagem</th><th>Quando enviar</th><th>Data de envio</th></tr>{tr}</table></div>
<ul style="font-size:10pt"><li><b>Estadia de 1 noite:</b> a mensagem de apoio (M05) aparece como "Pule".</li>
<li><b>Datas trocadas:</b> se a saída não for depois da entrada, as datas de envio mostram "Confira as datas".</li></ul>{foot(4,T)}</section>""")
    m4, s4 = get(EXM, "M04"), get(SSM, "M04")
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · copiar e enviar</div><h2>Copie, releia e envie</h2>
<ol class="passos"><li>Confira a coluna <b>Situação</b>: só envie as que estão em "Pronta para copiar".</li>
<li>Clique na célula do <b>Texto pronto</b> e copie o conteúdo pela barra de fórmulas (ou dê dois cliques e selecione o texto). Assim o texto sai sem aspas.</li>
<li>Cole no WhatsApp ou na conversa da plataforma. Se a sua plataforma oferece mensagens rápidas ou programadas, você pode colar o texto lá também.</li>
<li>Releia: nome, datas e horários batem com a reserva?</li></ol>
<p><b>Demonstração</b> com a planilha de exemplo (valores calculados pela própria planilha):</p>
<div class="box ex"><span class="tag">M04 · Boas-vindas · {E(m4['st'])}</span><div class="bolha">{marca(m4['txt'])}</div></div>
<div class="box alerta"><span class="tag" style="background:#A0522D">A mesma mensagem sem a senha do Wi-Fi · {E(s4['st'])}</span><div class="bolha">{marca(s4['txt'])}</div>
<p style="font-size:9pt;margin:4px 0 0">A planilha não inventa a senha: marca o que falta e a mensagem não aparece como pronta ({E(str(SSP))} prontas).</p></div>{foot(5,T)}</section>""")
    m9, m10 = get(EXM, "M09"), get(EXM, "M10")
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · imprevistos e o seu jeito de falar</div><h2>Responda rápido e ajuste o tom</h2>
<p>Duas mensagens são respostas, para usar quando acontecer:</p>
<div class="box ex"><span class="tag">M09 · Chegada fora do horário</span><div class="bolha">{E(m9['txt'])}</div></div>
<div class="box ex"><span class="tag">M10 · Problema durante a estadia</span><div class="bolha">{E(m10['txt'])}</div>
<p style="font-size:9pt;margin:4px 0 0">Responder que já está verificando não resolve o problema: combine com a equipe quem age e em quanto tempo, e cumpra o que disser ao hóspede.</p></div>
<h3>Adaptar ao seu tom</h3><p>Os textos são neutros e cordiais. Para ajustar ao seu jeito, edite a mensagem depois de colar, sem mudar as informações (datas, horários, senha, endereço). Evite exageros como "incrível" ou "mágico" e use no máximo um emoji por mensagem, como fazemos na Zion.</p>
<div class="box"><b>Exercício 2.</b> Reescreva a M07 (dia da saída) do seu jeito, mantendo o horário do check-out.<div class="linha"></div><div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Ficha completa</td><td>Todos os campos com * preenchidos; "Prontas para copiar" mostra {N} de {N} numa reserva de teste</td></tr>
<tr><td>Calendário certo</td><td>As datas de envio batem com a entrada e a saída da reserva</td></tr>
<tr><td>Nada inventado</td><td>Nenhuma mensagem enviada com [PREENCHA]; senha e endereço conferidos</td></tr>
<tr><td>Uso real</td><td>Na primeira reserva, as mensagens de M01 a M08 saíram na data indicada</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Preenchi a ficha da hospedagem &nbsp; ☐ Fiz uma reserva de teste com {N} de {N} prontas &nbsp; ☐ Copiei uma mensagem sem aspas<br>
☐ Ajustei uma mensagem ao meu tom &nbsp; ☐ Combinei com a equipe a resposta a imprevistos &nbsp; ☐ Usei o kit numa reserva real</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>O kit monta textos; não envia mensagens sozinho e não se conecta ao WhatsApp nem às plataformas.</li>
<li>Confira as regras da sua plataforma sobre mensagens, contato fora dela e pedidos de avaliação. Peça avaliação honesta, sem oferecer nada em troca nem pedir uma nota.</li>
<li>Os textos são em português e para uma reserva por vez (preencha os dados da reserva a cada hóspede).</li>
<li>Não garante avaliações, reservas nem ocupação.</li>
<li>A jornada parte dos scripts de atendimento usados nas unidades da Zion, generalizados para qualquer hospedagem.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com hospedagem, pessoas, telefone e links fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def modelos():
    blocos = ""
    for mid, tit, quando, regra, segs in MENSAGENS:
        txt = ""
        for s in segs:
            if s[0] == "t": txt += re.sub(r"\{(\w+)\}", lambda m: f"<b>[{E(rotulo(m.group(1)))}]</b>", E(s[1]))
            elif s[0] == "o": txt += ' <i style="color:#6b6656">(se houver:' + re.sub(r"\{(\w+)\}", lambda m: f"<b>[{E(rotulo(m.group(1)))}]</b>", E(s[1])) + ")</i>"
            elif s[0] == "v": txt += ' <i style="color:#6b6656">(se ainda não souber o horário:' + E(s[2]) + ")</i>"
        blocos += f'<div style="page-break-inside:avoid;margin-bottom:10px"><div class="kicker">{mid} · {E(quando)}</div><h3 style="margin:0 0 4px">{E(tit)}</h3><div class="bolha">{txt}</div></div>'
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}@page{{size:A4;margin:14mm 14mm 14mm}} body{{background:#fff}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 11</div>
<h2 style="font-size:22pt">Modelos de mensagens</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<p style="font-size:9.5pt">Troque o que está entre colchetes pelos dados da sua hospedagem e da reserva. Os trechos "(se houver: ...)" só entram se você tiver a informação. Nunca envie com colchetes.</p>{blocos}</body></html>"""

def demo(lst, prontas, falta):
    m = get(lst, "M04")
    cor = "#F4C7C3" if falta else "#C8E6C0"
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Kit de Mensagens · Ferramenta 11</div>
<div style="font-family:Cormorant,serif;font-size:24px">M04 · Boas-vindas</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(m['st'])} · {E(str(prontas))} prontas</div>
<div style="padding:12px 14px"><div class="bolha" style="font-size:13px">{marca(m['txt'])}</div></div>
<div style="padding:0 14px 12px;font-size:11px;color:#6b6656">Texto montado pela planilha a partir da ficha da hospedagem.</div></body></html>"""

(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(modelos(), encoding="utf-8")
(BUILD / "demo-pronta.html").write_text(demo(EXM, EXP, False), encoding="utf-8")
(BUILD / "demo-falta.html").write_text(demo(SSM, SSP, True), encoding="utf-8")
print("exemplo:", EXP, "prontas | sem senha:", SSP)
