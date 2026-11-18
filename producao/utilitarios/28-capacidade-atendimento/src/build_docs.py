"""Gera guia, ficha de saída e demonstração da Ferramenta 28 com valores REAIS recalculados (LibreOffice).
Uso: python3 -I src/build_docs.py dist build && node src/render.js build dist"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _css import CSS, R
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
BRAND = R / "docs/brand"; E = html.escape
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(tmp),
                str(DIST / "Capacidade-Atendimento-Zion-EXEMPLO.xlsx")], check=True, capture_output=True, timeout=300)
W = load_workbook(tmp / "Capacidade-Atendimento-Zion-EXEMPLO.xlsx", data_only=True)
EX, SA, P = W["Experiências"], W["Saídas"], W["Painel"]
EXP = [[EX[f"{c}{r}"].value for c in "ABCDEFGHIJ"] for r in range(7, 27) if EX[f"A{r}"].value]
SAI = [[SA[f"{c}{r}"].value for c in "ABCDEFGHIJKL"] for r in range(7, 207) if SA[f"L{r}"].value]
PAI = [(P[f"A{r}"].value, P[f"B{r}"].value) for r in range(4, 18)]
LEIT = P["A20"].value
dmy = lambda v: v.strftime("%d/%m") if hasattr(v, "strftime") else ""
num = lambda v: "" if v in (None, "") else (f"{v:.0%}" if isinstance(v, float) and v < 5 and v != int(v) else str(int(v)) if isinstance(v, (int, float)) else str(v))
pct = lambda v: f"{v:.0%}" if isinstance(v, (int, float)) else ""
curto = lambda s: str(s or "").replace(" (fictícia)", "").replace(" (fictício)", "")
cls = lambda s: {"Confirmada": "ok", "Lotada": "ok", "Pronta": "ok", "Já passou": "", "Lotada, com lista de espera": "aten", "Abaixo do mínimo": "aten",
                 "Decida: confirmar ou cancelar": "aten", "Falta condutor": "aten"}.get(s, "pend" if s else "")
CSS2 = CSS + ".aten{background:#FCE8B2}"
def foot(n, t): return f'<div class="foot"><span>Zion Hospitality Business · Ferramenta 28 · Planner de Capacidade e Atendimento</span><span>{n}/{t}</span></div>'

def guia():
    T = 7; p = []
    capa = f"""<div style="height:150mm;position:relative;background:radial-gradient(circle at 70% 40%,#2c3524,#1B2117 60%,#121610)">
<img src="{(DIST/'demonstracao/demo-saidas.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:52mm;top:16mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(-4deg);box-shadow:0 18px 36px rgba(0,0,0,.5)">
<img src="{(DIST/'demonstracao/demo-painel.png').resolve().as_uri()}" style="position:absolute;width:62mm;left:104mm;top:30mm;border:5px solid #0b0e09;border-radius:16px;transform:rotate(5deg);box-shadow:0 18px 36px rgba(0,0,0,.5)"></div>"""
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">{capa}
<div style="padding:14mm 18mm"><img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 28 · Guia do comprador</div><h1 style="color:var(--creme)">Planner de Capacidade e Atendimento</h1>
<p style="font-size:13pt;max-width:160mm">Aprenda o passo a passo para planejar as saídas das suas experiências: quantas pessoas cabem, quantos condutores escalar, quando confirmar ou cancelar e o que fazer com a lista de espera.</p>
<p style="font-size:9pt;color:var(--dourado);margin-top:8mm">Para Airbnb, casas, apartamentos, pousadas, glampings e quem oferece passeios e experiências. Telas reais da planilha, com dados fictícios.</p></div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> quem oferece trilha, passeio, aula, café especial ou outra experiência com horário marcado e já passou por saída lotada demais, guia faltando ou passeio com duas pessoas que não pagou o dia.<br>
<b>Quando usar:</b> ao abrir a agenda da semana, a cada nova reserva e um dia antes de cada saída.</div>
<h3>Você termina com</h3><ol class="passos"><li>As regras de cada experiência anotadas: capacidade, pessoas por condutor, mínimo e prazo para decidir.</li>
<li>A agenda de saídas com vagas, condutores necessários e situação de cada uma.</li>
<li>Um painel que diz o que fazer agora e o que a próxima semana pede de equipe.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos"><li>Leia este guia (cerca de 15 minutos).</li><li>Abra o exemplo e veja as abas Saídas e Painel.</li>
<li>Na versão em branco, cadastre as suas experiências e as saídas das próximas duas semanas (cerca de 20 minutos).</li><li>Imprima uma Ficha de Saída para cada saída confirmada.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Capacidade-Atendimento-Zion-EM-BRANCO.xlsx</td><td>Sua planilha: até 20 experiências e 200 saídas</td></tr>
<tr><td>Capacidade-Atendimento-Zion-EXEMPLO.xlsx</td><td>4 experiências e 11 saídas fictícias</td></tr>
<tr><td>Ficha-de-Saida.pdf</td><td>Uma página para conferir cada saída antes, durante e depois</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>{foot(2,T)}</section>""")
    tr = "".join(f"<tr><td>{E(curto(l[0]))}</td><td>{num(l[1])}</td><td>{num(l[2])}</td><td>{num(l[3]) or '—'}</td><td>{num(l[4]) or '—'}</td><td class='{cls(l[6])}'>{E(str(l[6]))}</td></tr>" for l in EXP)
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · aba Experiências</div><h2>Escreva as regras antes da agenda</h2>
<p>Capacidade e quantas pessoas cada condutor atende são decisões suas, de acordo com a atividade, o local, o equipamento e as regras que valem para a sua região. Anote uma vez e a planilha aplica em todas as saídas.</p>
<table><tr><th>Campo</th><th>Pergunta que responde</th></tr>
<tr><td>Capacidade por saída</td><td>Quantas pessoas cabem com conforto e segurança (veículo, mesa, trilha, sala)?</td></tr>
<tr><td>Pessoas por condutor</td><td>Quantos participantes um guia, instrutor ou monitor consegue acompanhar bem?</td></tr>
<tr><td>Mínimo para confirmar</td><td>Abaixo de quantas pessoas a saída não se paga? (A Ferramenta 29 ajuda nessa conta; é vendida separadamente.)</td></tr>
<tr><td>Decidir com quantos dias</td><td>Até quando você pode cancelar avisando os participantes com tempo?</td></tr></table>
<div class="box ex" style="margin-top:8px"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px;font-size:9pt"><tr><th>Experiência</th><th>Capacidade</th><th>Por condutor</th><th>Mínimo</th><th>Decidir (dias)</th><th>Situação</th></tr>{tr}</table></div>
<div class="box"><b>Exercício 1.</b> Para a sua experiência principal: quantas pessoas cabem, quantas cada condutor acompanha e qual o mínimo para valer a saída?<div class="linha"></div></div>{foot(3,T)}</section>""")
    tr = "".join(f"<tr><td>{dmy(s[0])}</td><td>{E(curto(s[2]))}</td><td>{num(s[3])}</td><td>{num(s[4])}</td><td>{num(s[7])}</td><td>{num(s[8])}</td><td class='{cls(s[11])}'>{E(str(s[11]))}</td></tr>" for s in SAI)
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · aba Saídas</div><h2>Uma linha por saída, só com quantidades</h2>
<ol class="passos"><li>Data, horário e experiência (escolha na lista).</li>
<li>Pessoas reservadas, condutores escalados e, se houver, quantas pessoas estão na lista de espera.</li>
<li><b>Nunca</b> o nome, o telefone ou o documento dos participantes: só números.</li></ol>
<div class="box ex"><span class="tag">Exemplo · dados fictícios · hoje = 20/11</span><table style="margin-top:8px;font-size:8.3pt"><tr><th>Data</th><th>Experiência</th><th>Reserv.</th><th>Cond.</th><th>Vagas</th><th>Cond. necess.</th><th>Situação</th></tr>{tr}</table>
<p style="font-size:9pt;margin:6px 0 0">A cavalgada não está cadastrada e uma saída está sem data: as duas ficam fora das contas até serem corrigidas.</p></div>{foot(4,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · a coluna Situação</div><h2>O que cada situação pede de você</h2>
<table><tr><th>Situação</th><th>O que fazer</th></tr>
<tr><td class="pend">Acima da capacidade</td><td>Ofereça outro horário a parte do grupo ou abra uma saída extra, se houver condutor.</td></tr>
<tr><td class="aten">Falta condutor</td><td>Escale mais um condutor ou limite as reservas ao que a equipe atende.</td></tr>
<tr><td class="aten">Abaixo do mínimo</td><td>Ainda dá tempo: divulgue a saída para quem está hospedado ou junte com outro horário.</td></tr>
<tr><td class="aten">Decida: confirmar ou cancelar</td><td>O prazo chegou. Confirme assumindo o custo ou cancele avisando os participantes e oferecendo outra data.</td></tr>
<tr><td class="aten">Lotada, com lista de espera</td><td>Há procura sobrando: veja se cabe outro horário.</td></tr>
<tr><td class="ok">Lotada / Confirmada</td><td>Imprima a Ficha de Saída e confira equipe e equipamento na véspera.</td></tr>
<tr><td>Já passou</td><td>Sai das contas. Anote na ficha o que aconteceu, para ajustar as regras.</td></tr></table>
<p style="font-size:10pt">A planilha olha nessa ordem: primeiro a capacidade, depois a equipe, depois o mínimo. Uma saída acima da capacidade só aparece assim, mesmo que também falte condutor.</p>
<div class="box alerta"><b>Cuidados:</b> combine com os participantes, antes da reserva, o mínimo de pessoas e o que acontece se a saída for cancelada. A planilha faz contas com o que você informar; não substitui as regras de segurança da atividade.</div>{foot(5,T)}</section>""")
    tr = "".join(f"<tr><td>{E(str(a))}</td><td><b>{dmy(b) if a == 'Data de hoje' else num(b)}</b></td></tr>" for a, b in PAI)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · aba Painel</div><h2>Uma olhada por dia, uma revisão por semana</h2>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px;font-size:9.5pt">{tr}</table>
<p style="margin:8px 0 0"><b>O que fazer agora:</b> {E(LEIT)}</p></div>
<div class="box"><b>Rotina sugerida:</b> todo dia, veja "O que fazer agora". Uma vez por semana, cadastre as saídas das próximas duas semanas e confira se os condutores dos próximos 7 dias estão escalados. "Condutores necessários" soma as saídas; quem conduz duas saídas no mesmo dia conta duas vezes.</div>
<div class="box"><b>Exercício 2.</b> Qual saída da próxima semana corre mais risco (lotar, faltar condutor ou não atingir o mínimo)? O que você faz hoje para evitar?<div class="linha"></div><div class="linha"></div></div>{foot(6,T)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Regras escritas</td><td>Todas as experiências como "Pronta"</td></tr>
<tr><td>Agenda limpa</td><td>"Saídas com problema" igual a 0</td></tr>
<tr><td>Equipe completa</td><td>Nenhuma saída "Falta condutor" ou "Acima da capacidade"</td></tr>
<tr><td>Nada decidido em cima da hora</td><td>Nenhuma saída "Decida" esquecida depois do prazo</td></tr>
<tr><td>Privacidade</td><td>Nenhum nome ou telefone de participante na planilha</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">☐ Cadastrei as experiências &nbsp; ☐ Combinei com os participantes o mínimo e o cancelamento &nbsp; ☐ Lancei as saídas de duas semanas<br>
☐ Escalei os condutores dos próximos 7 dias &nbsp; ☐ Imprimi a Ficha de Saída das confirmadas &nbsp; ☐ Marquei o dia da revisão semanal</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>A planilha calcula com a capacidade e a proporção que você informar; ela não sabe quantas pessoas são seguras para a sua atividade.</li>
<li>Não recebe reservas, não avisa participantes e não sincroniza com plataformas: você atualiza os números.</li>
<li>Não calcula custo nem preço; para isso existe a Ferramenta 29, vendida separadamente.</li>
<li>Planejar a capacidade não garante procura, reservas nem avaliações.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com experiências, datas e números fictícios. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(7,T)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

def ficha():
    campo = lambda t, n=1: f'<div style="margin:4px 0"><span style="font-size:9pt;font-weight:600">{E(t)}</span>' + '<div class="linha"></div>' * n + '</div>'
    chk = ["Previsão do tempo e condições do local conferidas", "Equipamentos e materiais separados e revisados", "Kit de primeiros socorros conferido",
           "Contato de emergência e ponto de apoio combinados", "Regras e cuidados explicados aos participantes", "Contagem de pessoas na saída e na volta"]
    linhas = "".join("<tr><td style='height:20px'></td><td></td><td style='text-align:center'>☐</td></tr>" for _ in range(10))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2}@page{{size:A4;margin:12mm}} body{{background:#fff}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 28</div>
<h2 style="font-size:22pt;margin:0">Ficha de saída</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;gap:14px"><div style="flex:2">{campo('Experiência')}</div><div style="flex:1">{campo('Data')}</div><div style="flex:1">{campo('Horário')}</div></div>
<div style="display:flex;gap:14px"><div style="flex:2">{campo('Ponto de encontro')}</div><div style="flex:2">{campo('Condutor(es)')}</div></div>
<div style="display:flex;gap:14px"><div style="flex:1">{campo('Pessoas reservadas')}</div><div style="flex:1">{campo('Capacidade')}</div><div style="flex:1">{campo('Mínimo')}</div><div style="flex:1">{campo('Decidir até')}</div></div>
<h3 style="font-size:12pt;margin:8px 0 2px">Antes de sair</h3><div style="font-size:9.5pt;columns:2">{''.join(f'<div>☐ {E(c)}</div>' for c in chk)}</div>
<h3 style="font-size:12pt;margin:8px 0 2px">Participantes (pelo código da reserva)</h3>
<table style="font-size:9pt"><tr><th style="width:55%">Código da reserva</th><th>Pessoas</th><th>Presente</th></tr>{linhas}</table>
<div style="display:flex;gap:14px;margin-top:4px"><div style="flex:1">{campo('Contagem na saída')}</div><div style="flex:1">{campo('Contagem na volta')}</div></div>
{campo('Ocorrências e o que ajustar na próxima saída', 2)}
<div style="display:flex;gap:24px;margin-top:6px"><div style="flex:1">{campo('Responsável e assinatura')}</div><div style="flex:1">{campo('Lista de espera avisada? Quem cuidou')}</div></div>
<p style="font-size:8.5pt;color:#6b6656;margin-top:6px">Anote dados de saúde ou contato só se forem necessários à segurança da saída, e guarde com cuidado. Depois, atualize a aba Saídas.</p></body></html>"""

def demo(titulo, status, cor, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS2} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">Capacidade · Ferramenta 28</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(titulo)}</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div style="background:{cor};padding:12px 16px;font-weight:700">{E(status)}</div>{corpo}
<div style="padding:10px 14px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 28.</div></body></html>"""
lin = lambda a, b, c: f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 14px;border-bottom:1px solid var(--areia);font-size:13px"><span>{a}</span><span class="{c}" style="padding:1px 8px;border-radius:6px;text-align:right;max-width:52%;align-self:flex-start">{b}</span></div>'
fut = [s for s in SAI if s[11] not in ("Já passou",) and s[6] not in (None, "")]
sai = "".join(lin(f"{dmy(s[0])} {E(str(s[1] or ''))} · {E(curto(s[2]))}<br><small>{num(s[3])} de {num(s[6])} · {num(s[8])} condutor(es) necessário(s)</small>", E(str(s[11])), cls(s[11])) for s in fut[:7])
pd = dict(PAI)
pai = "".join(lin(E(a), f"<b>{num(pd[a])}</b>", "") for a in ["Próximas saídas", "Confirmadas (inclui lotadas)", "Abaixo do mínimo", "Falta condutor", "Acima da capacidade",
                                                            "Pessoas reservadas nos próximos 7 dias", "Condutores necessários nos próximos 7 dias (soma das saídas)", "Pessoas na lista de espera (próximas saídas)"])
pai += f'<div style="padding:12px 14px;font-size:13px"><b>O que fazer agora:</b><br>{E(LEIT)}</div>'
(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(ficha(), encoding="utf-8")
(BUILD / "demo-saidas.html").write_text(demo("Saídas", f"{pd['Próximas saídas']} próximas · {pd['Confirmadas (inclui lotadas)']} confirmadas · {pd['Falta condutor']} sem condutor", "#FCE8B2", sai), encoding="utf-8")
(BUILD / "demo-painel.html").write_text(demo("Painel", f"{pd['Pessoas reservadas nos próximos 7 dias']} pessoas e {pd['Condutores necessários nos próximos 7 dias (soma das saídas)']} condutores nos próximos 7 dias", "#C8E6C0", pai), encoding="utf-8")
print(PAI, LEIT)
