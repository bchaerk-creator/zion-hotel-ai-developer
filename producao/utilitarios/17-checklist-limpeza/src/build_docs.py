"""Gera os HTML do guia, do checklist imprimível e da demonstração a partir dos valores REAIS
recalculados da planilha de exemplo (LibreOffice). Depois, tests/../src/render.js imprime PDF e PNG.
Uso: python3 -I src/build_docs.py dist build"""
import sys, pathlib, subprocess, tempfile, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from modelo_itens import ITENS
from openpyxl import load_workbook

DIST, BUILD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); BUILD.mkdir(parents=True, exist_ok=True)
REPO = pathlib.Path(__file__).resolve().parents[4]
FONTS, BRAND, OPS = REPO / "docs/assets/fonts", REPO / "docs/brand", REPO / "docs/assets/operacoes"
E = html.escape

# ---------- valores reais da planilha ----------
def recalc_variantes():
    tmp = pathlib.Path(tempfile.mkdtemp()); out = tmp / "o"; out.mkdir()
    ex = DIST / "Checklist-Limpeza-Zion-EXEMPLO.xlsx"
    wb = load_workbook(ex); t = wb["Troca"]
    for r in range(14, 14 + len(ITENS)):
        if t[f"F{r}"].value == "Reprovado" and t[f"E{r}"].value == "Feito": t[f"F{r}"] = "Aprovado"; t[f"G{r}"] = "Manutenção resolveu. Água quente em 40 s."
    lib = tmp / "Exemplo-Liberada.xlsx"; wb.save(lib)
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(out), str(ex), str(lib)],
                   check=True, capture_output=True, timeout=300)
    return load_workbook(out / ex.name, data_only=True), load_workbook(out / lib.name, data_only=True)

EXW, LIBW = recalc_variantes()
def troca(wb):
    t = wb["Troca"]
    linhas = [[t[f"{c}{r}"].value or "" for c in "ABCDEFGH"] for r in range(14, 14 + len(ITENS))]
    return dict(titulo=t["A1"].value, un=t["B3"].value, exe=t["B5"].value, conf=t["B6"].value, status=t["B10"].value,
                itens=t["E3"].value, obrig=t["E4"].value, pend=t["E5"].value, aten=t["E6"].value, tempo=t["E7"].value, linhas=linhas)
EXT, LIBT = troca(EXW), troca(LIBW)
PEND = [[EXW["Pendências"][f"{c}{r}"].value for c in "ABCDEFGHI"] for r in (6, 7, 8)]

# ---------- estilo ----------
CSS = f"""
@font-face {{ font-family: Cormorant; src: url('{(FONTS/'cormorant.woff2').as_uri()}'); }}
@font-face {{ font-family: Aventa; src: url('{(FONTS/'aventa.woff2').as_uri()}'); }}
:root {{ --preto:#040605; --musgo:#1B2117; --creme:#FEF5F0; --areia:#DED6BF; --terra:#8B714E; --dourado:#C9B37E; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: Aventa, Arial, sans-serif; color: var(--musgo); background: var(--creme); font-size: 11pt; line-height: 1.45; }}
h1, h2, h3 {{ font-family: Cormorant, Georgia, serif; font-weight: 600; margin: 0 0 .4em; line-height: 1.1; }}
h1 {{ font-size: 40pt; }} h2 {{ font-size: 26pt; }} h3 {{ font-size: 15pt; margin-top: .8em; }}
.kicker {{ font-size: 8.5pt; letter-spacing: .18em; text-transform: uppercase; color: var(--terra); font-weight: 700; margin-bottom: 6px; }}
.page {{ width: 210mm; height: 297mm; padding: 18mm 18mm 16mm; position: relative; overflow: hidden; page-break-after: always; background: var(--creme); }}
.page:last-child {{ page-break-after: auto; }}
.foot {{ position: absolute; bottom: 9mm; left: 18mm; right: 18mm; font-size: 7.5pt; color: #6b6656; display: flex; justify-content: space-between; border-top: 1px solid var(--areia); padding-top: 4px; }}
.box {{ background: #fff; border: 1px solid var(--areia); border-radius: 10px; padding: 12px 14px; margin: 10px 0; }}
.box.ex {{ border-left: 5px solid var(--dourado); }}
.box.alerta {{ border-left: 5px solid #A0522D; }}
.tag {{ display:inline-block; font-size: 8pt; font-weight:700; padding: 2px 8px; border-radius: 99px; background: var(--musgo); color: var(--creme); }}
table {{ border-collapse: collapse; width: 100%; font-size: 9.5pt; }}
th {{ background: var(--musgo); color: var(--creme); text-align: left; padding: 5px 7px; font-weight: 600; }}
td {{ border-bottom: 1px solid var(--areia); padding: 5px 7px; vertical-align: top; }}
.ok {{ background:#C8E6C0; }} .pend {{ background:#F4C7C3; font-weight:700; }} .aten {{ background:#FCE8B2; }}
ol.passos li {{ margin: 0 0 6px; }}
.linha {{ border-bottom: 1px solid #b9b19b; height: 22px; }}
.fict {{ color:#A0522D; font-weight:700; font-size: 8.5pt; }}
"""

def foot(n, total, txt="Ferramenta 17 · Checklist de Limpeza, Inspeção e Liberação"):
    return f'<div class="foot"><span>Zion Hospitality Business · {txt}</span><span>{n}/{total}</span></div>'

def status_cls(s): return "ok" if str(s).startswith("LIBERADA") else "pend"
def sit_cls(s): return {"OK": "ok", "PENDENTE": "pend", "Atenção": "aten"}.get(s, "")

def tabela_troca(t, filtro=None, max_l=None):
    rows = [l for l in t["linhas"] if l[1] and (filtro is None or filtro(l))][:max_l]
    tr = "".join(f'<tr><td>{E(l[0])}</td><td>{E(l[1])}</td><td>{E(l[2])}</td><td>{E(l[4])}</td><td>{E(l[5])}</td><td>{E(l[6])}</td>'
                 f'<td class="{sit_cls(l[7])}">{E(l[7])}</td></tr>' for l in rows)
    return f'<table><tr><th>Ambiente</th><th>O que fazer</th><th>Obrig.</th><th>Execução</th><th>Conferência</th><th>Observação</th><th>Situação</th></tr>{tr}</table>'

def painel(t):
    return (f'<div class="box"><div class="kicker">{E(t["titulo"])} · <span class="fict">dados fictícios</span></div>'
            f'<div>Unidade: <b>{E(t["un"])}</b> · Quem limpou: <b>{E(t["exe"])}</b> · Quem conferiu: <b>{E(t["conf"])}</b> · Tempo: <b>{t["tempo"]} min</b></div>'
            f'<div style="margin-top:6px">Itens: {t["itens"]} · Obrigatórios: {t["obrig"]} · Obrigatórios pendentes: <b>{t["pend"]}</b> · Opcionais em atenção: {t["aten"]}</div>'
            f'<div class="{status_cls(t["status"])}" style="margin-top:8px;padding:8px 10px;border-radius:8px;font-weight:700">Situação da troca: {E(t["status"])}</div></div>')

# ---------- guia ----------
def guia():
    N = 8; p = []
    p.append(f"""<section class="page" style="padding:0;background:var(--musgo);color:var(--creme)">
<img src="{(OPS/'op05.webp').as_uri()}" style="width:100%;height:150mm;object-fit:cover;display:block">
<div style="padding:14mm 18mm">
<img src="{(BRAND/'zion-logo-claro.png').as_uri()}" style="height:16mm;margin-bottom:8mm">
<div class="kicker" style="color:var(--dourado)">Ferramenta 17 · Guia do comprador</div>
<h1 style="color:var(--creme)">Checklist de Limpeza, Inspeção e Liberação</h1>
<p style="font-size:13pt;max-width:150mm">Aprenda o passo a passo para limpar, conferir e liberar cada unidade com o mesmo padrão, sabendo quem fez, quem conferiu e o que ficou pendente.</p>
<p style="font-size:8pt;color:var(--areia);margin-top:10mm">Foto real: interior de uma unidade da Zion Bubble Glamping.</p>
</div></section>""")
    p.append(f"""<section class="page"><div class="kicker">Antes de começar</div><h2>Para quem é e com o que você termina</h2>
<div class="box"><b>Para quem é:</b> anfitriões, pousadas, glampings e pequenos hotéis que fazem troca de hóspede, com equipe ou sozinhos.<br>
<b>Quando usar:</b> a cada saída de hóspede, antes de liberar a unidade para o próximo; e ao treinar alguém novo na limpeza.</div>
<h3>Você termina com</h3><ol class="passos">
<li>Uma lista de limpeza e inspeção ajustada à sua unidade, com o que é obrigatório e o critério de conferência de cada item.</li>
<li>Uma regra clara de liberação: a unidade só aparece como liberada com todos os obrigatórios feitos e aprovados.</li>
<li>O registro de cada troca (quem fez, quem conferiu, tempo) e das pendências, com prazo e responsável.</li></ol>
<h3>Como estudar e aplicar</h3><ol class="passos">
<li>Leia este guia uma vez (cerca de 15 minutos).</li><li>Abra a versão de exemplo e veja uma troca preenchida.</li>
<li>Na versão em branco, faça os passos 1 e 2 (cerca de 20 minutos).</li><li>Use na próxima troca de hóspede. Ajuste o modelo depois da primeira semana.</li></ol>
<h3>O que vem no pacote</h3><table><tr><th>Arquivo</th><th>Para quê</th></tr>
<tr><td>Checklist-Limpeza-Zion-EM-BRANCO.xlsx</td><td>Sua planilha, com o modelo-padrão de {len(ITENS)} itens pronto para ajustar</td></tr>
<tr><td>Checklist-Limpeza-Zion-EXEMPLO.xlsx</td><td>Uma troca preenchida com dados fictícios</td></tr>
<tr><td>Checklist-Imprimivel.pdf</td><td>Versão em papel, para quem prefere prancheta</td></tr>
<tr><td>Este guia</td><td>O passo a passo, os exercícios e os critérios de conferência</td></tr></table>
<p style="font-size:9.5pt">Funciona no Excel, no Google Sheets (Arquivo → Importar) e no LibreOffice. No celular, use o app do Google Sheets ou do Excel.</p>{foot(2,N)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 1 · aba Modelo</div><h2>Ajuste a lista à sua unidade</h2>
<p>A planilha já vem com um modelo-padrão de {len(ITENS)} itens em 8 ambientes, na ordem de uma troca de hóspede: primeiro se tira o que é do hóspede anterior (lixo e enxoval), depois se limpa, se repõe, se testa e, por último, se confere.</p>
<ol class="passos"><li><b>Apague</b> o que não existe na sua unidade (por exemplo, banheira).</li>
<li><b>Acrescente</b> o que falta, em qualquer linha vazia. A aba Troca copia a lista sozinha.</li>
<li><b>Marque o que é obrigatório para liberar.</b> Pergunta-guia: se este item falhar, o próximo hóspede vai perceber ou ter um problema?</li>
<li><b>Escreva o critério de conferência</b> de cada item: algo que outra pessoa consegue verificar olhando, tocando ou testando.</li></ol>
<div class="box ex"><span class="tag">Exemplo</span><table style="margin-top:8px"><tr><th>Critério fraco</th><th>Critério que dá para conferir</th></tr>
<tr><td>Banheiro limpo</td><td>Box e espelho sem marcas de água, olhando contra a luz</td></tr>
<tr><td>Cama arrumada</td><td>Lençol esticado, sem manchas nem cabelos</td></tr>
<tr><td>Chuveiro ok</td><td>Água quente em até 1 minuto</td></tr>
<tr><td>Wi-Fi funcionando</td><td>Celular conecta com a senha informada ao hóspede</td></tr></table></div>
<div class="box"><b>Exercício 1.</b> Escolha três itens da sua unidade que já geraram reclamação ou retrabalho. Para cada um, escreva um critério que caiba numa linha e que outra pessoa consiga verificar.<div class="linha"></div><div class="linha"></div><div class="linha"></div></div>
<div class="box alerta"><b>Atenção:</b> não colocamos produtos de limpeza na lista. Quem define os produtos e os equipamentos de proteção é o responsável pela unidade, seguindo o rótulo e as orientações dos fabricantes.</div>{foot(3,N)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 2 · aba Ajustes</div><h2>Defina quem faz e quem confere</h2>
<p>A conferência funciona melhor quando quem confere não é quem limpou: o olhar de fora encontra o que quem executou já não vê. Por isso a planilha separa as duas colunas e, por padrão, bloqueia a liberação se o mesmo nome aparecer nos dois campos.</p>
<table><tr><th>Sua situação</th><th>Ajuste "Exigir conferente diferente?"</th><th>Como fica</th></tr>
<tr><td>Tem equipe (duas pessoas ou mais)</td><td><b>Sim</b></td><td>O nome de quem conferiu é obrigatório e precisa ser diferente</td></tr>
<tr><td>Trabalha sozinho</td><td><b>Não</b></td><td>Você marca as duas colunas. Faça a conferência depois de terminar tudo, entrando como hóspede</td></tr></table>
<div class="box"><b>Exercício 2.</b> Escreva quem limpa e quem confere em cada dia da semana. Se for você nas duas funções, escreva em que momento fará a conferência.<div class="linha"></div><div class="linha"></div></div>
<h3>Combine antes da primeira troca</h3><ol class="passos">
<li>Onde fica a planilha (celular de quem? papel na prancheta?).</li><li>Quem pode marcar "Aprovado".</li>
<li>O que fazer quando um item obrigatório falha: registrar a pendência e avisar quem decide.</li></ol>{foot(4,N)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Passo 3 · aba Troca</div><h2>Execute a troca, item por item</h2>
<ol class="passos"><li>Preencha unidade, data, quem limpou, quem conferiu, início e fim.</li>
<li>Quem limpa marca a coluna <b>Execução</b>: Feito, Não feito ou Não se aplica.</li>
<li>Quem confere passa pelos itens e marca a coluna <b>Conferência</b>: Aprovado, Reprovado ou Não se aplica, usando o critério da linha.</li>
<li>Qualquer coisa fora do normal vai na <b>Observação</b>.</li></ol>
<p><b>Demonstração</b> com a planilha de exemplo (valores recalculados pela própria planilha):</p>{painel(EXT)}
{tabela_troca(EXT, filtro=lambda l: l[1].startswith(("Limpar o vaso", "Limpar box", "Repor toalhas", "Testar o chuveiro", "Repor café")))}
<p style="font-size:9pt">Trecho da aba Troca: banheiro, chuveiro e cortesias. O chuveiro foi feito, mas a conferência reprovou: o item é obrigatório, então fica PENDENTE e bloqueia a liberação. O café faltou, mas é opcional: fica em Atenção e não bloqueia.</p>{foot(5,N)}</section>""")
    est = [("PREENCHA O CABEÇALHO", "Falta unidade, data ou um dos nomes", "Complete o topo da aba Troca"),
           ("NÃO LIBERAR: a conferência precisa ser feita por outra pessoa", "O mesmo nome em quem limpou e quem conferiu (com o ajuste Sim)", "Peça a outra pessoa para conferir"),
           ("NÃO LIBERAR: N itens obrigatórios pendentes", "Algum obrigatório não está em Feito + Aprovado", "Resolva, confira de novo ou registre a pendência e não libere"),
           ("CADASTRE OS ITENS OBRIGATÓRIOS NA ABA MODELO", "Nenhum item marcado como obrigatório", "Volte ao passo 1"),
           ("LIBERADA PARA O PRÓXIMO HÓSPEDE", "Todos os obrigatórios feitos e aprovados", "Registre no Histórico e libere")]
    tr = "".join(f'<tr><td class="{"ok" if a.startswith("LIB") else "pend" if a.startswith("NÃO") else "aten"}">{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>' for a, b, c in est)
    p.append(f"""<section class="page"><div class="kicker">Passo 4 · Situação da troca</div><h2>Confira e libere (ou não)</h2>
<p>No alto da aba Troca, a planilha mostra uma das cinco situações abaixo. Ela não decide por você: ela mostra se a sua regra foi cumprida.</p>
<table><tr><th>Mensagem</th><th>Por quê</th><th>O que fazer</th></tr>{tr}</table>
<p style="margin-top:12px"><b>Demonstração:</b> a mesma troca do exemplo depois que a manutenção resolveu o chuveiro e a conferência aprovou o item.</p>{painel(LIBT)}
<div class="box"><b>Regra de ouro:</b> "Não se aplica" em item obrigatório conta como pendente. Se o item não existe na unidade, tire-o do Modelo ou marque-o como não obrigatório. Assim ninguém libera uma unidade "pulando" um item importante.</div>{foot(6,N)}</section>""")
    trp = "".join(f'<tr><td>{r[1]}</td><td>{E(str(r[3]))}</td><td>{E(str(r[4]))}</td><td class="{ {"Atrasada":"pend","Resolvida":"ok"}.get(r[8],"aten")}">{E(str(r[8]))}</td></tr>' for r in PEND)
    p.append(f"""<section class="page"><div class="kicker">Passo 5 · abas Pendências e Histórico</div><h2>Registre o que ficou para depois</h2>
<ol class="passos"><li>Toda falha que não foi resolvida na hora vira uma linha em <b>Pendências</b>: unidade, ambiente, o que aconteceu, responsável, prazo e evidência (foto ou link).</li>
<li>Quando resolver, preencha <b>Resolvida em</b>. A planilha marca como Atrasada o que passou do prazo.</li>
<li>No fim de cada troca, copie o resultado para o <b>Histórico</b> (data, unidade, nomes, horários, resultado). Depois apague as marcações amarelas da aba Troca, ou duplique a aba, para a próxima troca.</li></ol>
<div class="box ex"><span class="tag">Exemplo · dados fictícios</span><table style="margin-top:8px"><tr><th>Unidade</th><th>O que aconteceu</th><th>Responsável</th><th>Situação</th></tr>{trp}</table>
<p style="font-size:9pt;margin:6px 0 0">Com a data de referência 06/11/2026: a pendência do chuveiro venceu em 05/11 e aparece como Atrasada.</p></div>
<h3>Revisão de 10 minutos por semana</h3><ol class="passos"><li>Quais pendências estão atrasadas e quem resolve?</li>
<li>Algum item aparece reprovado toda semana? Ele precisa de um critério mais claro ou de treino.</li><li>O tempo médio da troca no Histórico mudou? Por quê?</li></ol>
<div class="box"><b>Exercício 3.</b> Lance no Histórico as três últimas trocas que você lembra e uma pendência real da sua unidade.</div>{foot(7,N)}</section>""")
    p.append(f"""<section class="page"><div class="kicker">Conclusão</div><h2>Como conferir que deu certo</h2>
<table><tr><th>Critério</th><th>Como verificar</th></tr>
<tr><td>Modelo ajustado</td><td>Nenhum item que não existe na unidade; cada obrigatório tem um critério que outra pessoa consegue verificar</td></tr>
<tr><td>Troca registrada</td><td>Cabeçalho completo e todas as linhas com Execução e Conferência marcadas</td></tr>
<tr><td>Liberação coerente</td><td>A unidade só foi liberada quando a Situação mostrou LIBERADA</td></tr>
<tr><td>Pendências fechadas</td><td>Toda pendência tem responsável e prazo; nenhuma atrasada sem explicação</td></tr>
<tr><td>Histórico em dia</td><td>Uma linha por troca na última semana</td></tr></table>
<h3>Checklist de conclusão</h3><div class="box">
☐ Ajustei o Modelo à minha unidade &nbsp; ☐ Defini quem limpa e quem confere &nbsp; ☐ Fiz a primeira troca na planilha<br>
☐ Registrei pelo menos uma pendência ou confirmei que não havia &nbsp; ☐ Lancei a troca no Histórico &nbsp; ☐ Marquei a revisão semanal</div>
<h3>Limitações e dependências</h3><ul style="font-size:10pt">
<li>A planilha organiza e registra. A qualidade da limpeza depende de quem executa e de quem confere.</li>
<li>Não substitui normas sanitárias, de segurança, de piscinas ou de equipamentos, nem orientações dos fabricantes. Rotinas técnicas (jacuzzi, gás, elétrica) seguem o responsável técnico.</li>
<li>Não prescreve produtos de limpeza nem garante avaliações, reservas ou ocupação.</li>
<li>Cada aba Troca guarda uma troca por vez; o histórico depende de você copiar o resultado.</li>
<li>A sequência do modelo-padrão parte da rotina de troca usada nas unidades da Zion, generalizada para qualquer hospedagem. Ajuste à sua.</li></ul>
<p style="font-size:9pt;color:#6b6656">Exemplos com pessoas e unidades fictícias. Material educativo da Zion Hospitality Business · Bruno Chaerk.</p>{foot(8,N)}</section>""")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}@page{{size:A4;margin:0}}</style></head><body>{"".join(p)}</body></html>'

# ---------- checklist imprimível ----------
def imprimivel():
    grupos = {}
    for it in ITENS: grupos.setdefault(it[0], []).append(it)
    linhas = ""
    for g, its in grupos.items():
        linhas += f'<tr><td colspan="5" style="background:var(--areia);font-weight:700">{E(g)}</td></tr>'
        linhas += "".join(f'<tr><td>{E(i[1])}{" <b>*</b>" if i[2]=="Sim" else ""}</td><td style="font-size:8pt;color:#555">{E(i[3])}</td>'
                          f'<td style="text-align:center">☐</td><td style="text-align:center">☐</td><td></td></tr>' for i in its)
    cab = "".join(f'<div style="flex:1 1 45%"><span style="font-size:8.5pt">{r}</span><div class="linha"></div></div>' for r in
                  ("Unidade", "Data", "Quem limpou", "Quem conferiu", "Início", "Fim"))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}
@page{{size:A4;margin:12mm 12mm 14mm}} body{{background:#fff}} td{{padding:3px 6px;font-size:9pt}} th{{font-size:8.5pt}}
tr{{page-break-inside:avoid}}</style></head><body>
<div style="display:flex;justify-content:space-between;align-items:center"><div><div class="kicker">Zion Hospitality Business · Ferramenta 17</div>
<h2 style="font-size:22pt">Checklist de troca de hóspede</h2></div><img src="{(BRAND/'zion-logo-escuro.png').as_uri()}" style="height:13mm"></div>
<div style="display:flex;flex-wrap:wrap;gap:4px 18px;margin:4px 0 10px">{cab}</div>
<table><tr><th style="width:36%">O que fazer (* = obrigatório para liberar)</th><th>Como conferir</th><th style="width:8%">Feito</th><th style="width:9%">Aprovado</th><th style="width:16%">Observação</th></tr>{linhas}</table>
<div class="box" style="margin-top:10px;font-size:9.5pt"><b>Liberar só se</b> todos os itens com * estiverem marcados em Feito e Aprovado. Pendência? Anote abaixo com responsável e prazo.
<div class="linha"></div><div class="linha"></div></div>
<div style="display:flex;gap:20px;margin-top:14px;font-size:9pt"><div style="flex:1"><div class="linha"></div>Assinatura de quem limpou</div><div style="flex:1"><div class="linha"></div>Assinatura de quem conferiu</div></div>
<p style="font-size:7.5pt;color:#6b6656;margin-top:8px">Modelo-padrão. Ajuste à sua unidade na planilha. Produtos de limpeza e equipamentos de proteção: conforme o responsável e o rótulo.</p></body></html>"""

# ---------- demonstração (formato celular e quadro do anúncio) ----------
def demo(t, nome):
    rows = "".join(f'<div style="display:flex;justify-content:space-between;gap:8px;padding:9px 12px;border-bottom:1px solid var(--areia);font-size:13px">'
                   f'<span>{E(l[1])}</span><span class="{sit_cls(l[7])}" style="padding:1px 8px;border-radius:6px;white-space:nowrap">{E(l[7])}</span></div>'
                   for l in t["linhas"] if l[0].startswith(("3", "7")))
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS} body{{width:390px;background:#fff}}</style></head><body>
<div style="background:var(--musgo);color:var(--creme);padding:16px"><div class="kicker" style="color:var(--dourado)">{E(t["titulo"])}</div>
<div style="font-family:Cormorant,serif;font-size:24px">{E(t["un"])} · {t["tempo"]} min</div><div class="fict" style="color:var(--dourado)">Exemplo com dados fictícios</div></div>
<div class="{status_cls(t["status"])}" style="padding:14px 16px;font-weight:700;font-size:15px">{E(t["status"])}</div>
{rows}<div style="padding:10px 12px;font-size:11px;color:#6b6656">Valores calculados pela planilha da Ferramenta 17.</div></body></html>"""

(BUILD / "guia.html").write_text(guia(), encoding="utf-8")
(BUILD / "imprimivel.html").write_text(imprimivel(), encoding="utf-8")
(BUILD / "demo-bloqueada.html").write_text(demo(EXT, "b"), encoding="utf-8")
(BUILD / "demo-liberada.html").write_text(demo(LIBT, "l"), encoding="utf-8")
print("status exemplo:", EXT["status"], "| depois do conserto:", LIBT["status"])
