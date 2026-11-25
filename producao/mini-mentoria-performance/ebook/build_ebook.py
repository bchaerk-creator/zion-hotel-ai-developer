"""Gera ebook/dist/guia-N.html (A5) e capa/dist/capa-N.html (1080x1350). Uso: python3 -I producao/mini-mentoria-performance/ebook/build_ebook.py"""
import json, html, pathlib
A = pathlib.Path(__file__).resolve().parent.parent; R = A.parents[1]; D = R/"docs"
U = lambda p: "file://" + str(D/p)
FORM = json.load(open(A/"fontes/formularios.json", encoding="utf8"))["questions"]
META = json.load(open(A/"src/meta.json"))
CALC = {"C1": "Calculadora de Posicionamento", "C2": "Calculadora de Ocupação e Canais", "C3": "Calculadora de Diária e RevPAR", "C4": "Calculadora de Contribuição e Equilíbrio", "C5": "Calculadora de Capacidade e Estoque", "C6": "Calculadora de Custo e Retorno da Expansão", "C7": "Calculadora de Necessidade de Capital"}
FOTO = {1: ("store/hero.webp", "center 60%", "Foto real: Zion Bubble Glamping"), 2: ("store/noite.webp", "center 55%", "Foto real: Zion Bubble Glamping"), 3: ("store/dentro.webp", "center 55%", "Foto real: Zion Bubble Glamping"), 4: ("operacoes/op09.webp", "center 45%", "Foto real: Zion Bubble Glamping"), 5: ("operacoes/op12.webp", "center 50%", "Foto real: Zion Bubble Glamping"), 6: ("operacoes/op08.webp", "center 50%", "Foto real: Zion Bubble Glamping"), 7: ("store/deck.webp", "center 45%", "Foto real: Zion Bubble Glamping")}
NOMES = {1: "Identidade", 2: "Vendas", 3: "Experiência", 4: "Finanças", 5: "Operação", 6: "Expansão", 7: "Parcerias"}
e = lambda s: html.escape(str(s), quote=False)
FONTS = f"""@font-face{{font-family:C;src:url({U('assets/fonts/cormorant.woff2')});font-weight:300 700}}
@font-face{{font-family:C;font-style:italic;src:url({U('assets/fonts/cormorant-italic.woff2')});font-weight:300 700}}
@font-face{{font-family:A;src:url({U('assets/fonts/aventa.woff2')});font-weight:300 900}}"""
LINHA = "Para Airbnb, casas, apartamentos, pousadas e glampings"
def capa_corpo(m, tit, sub, w, h):
    f, pos, cred = FOTO[m]
    return f"""<div class="capa" style="width:{w}px;height:{h}px"><div class="foto" style="background-image:url({U('assets/'+f)});background-position:{pos}"></div><div class="veu"></div>
<img class="logo" src="{U('brand/zion-logo-claro.png')}"><div class="topo">ZION HOTEL ACADEMY · GUIA {m:02d} DE 07</div>
<div class="bloco"><div class="mod">MÓDULO {m} · {NOMES[m].upper()}</div><h1>{e(tit)}</h1><div class="sub">{e(sub)}</div><div class="filete"></div><div class="mm">MINI MENTORIA DE PERFORMANCE HOTELEIRA</div><div class="rx">Raio-X da Hospedagem</div></div>
<div class="faixa">{LINHA}</div><div class="cred">{cred}</div></div>"""
CAPA_CSS = FONTS + """*{margin:0;box-sizing:border-box}body{background:#040605}.capa{position:relative;overflow:hidden;font-family:A;color:#FEF5F0;background:#1B2117}.foto{position:absolute;inset:0;background-size:cover}
.veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,6,5,.62) 0%,rgba(4,6,5,.08) 24%,rgba(4,6,5,.80) 47%,rgba(4,6,5,.97) 100%)}
.logo{position:absolute;left:7%;top:5.2%;height:4.2%;width:auto}.topo{position:absolute;right:7%;top:6%;font-size:1.25%;letter-spacing:.2em;color:#C9B37E}
.bloco{position:absolute;left:7%;right:7%;bottom:12%}.mod{font-size:1.9%;letter-spacing:.24em;color:#C9B37E}.capa h1{font-family:C;font-weight:500;font-size:7.4%;line-height:1.04;margin:2.4% 0 2%}
.sub{font-family:C;font-style:italic;font-size:3.6%;color:#DED6BF}.filete{width:12%;height:2px;background:#C9B37E;margin:5% 0 3%}.mm{font-size:1.8%;letter-spacing:.2em;color:#FEF5F0}.rx{font-family:C;font-size:3.4%;color:#C9B37E;margin-top:1%}
.faixa{position:absolute;left:0;right:0;bottom:0;height:7%;background:#C9B37E;color:#040605;display:flex;align-items:center;justify-content:center;font-size:1.9%;letter-spacing:.06em;text-align:center}.cred{position:absolute;right:7%;bottom:8%;font-size:1.25%;color:#DED6BF;opacity:.8}"""
def tam(css, w):  # converte % de altura em px, para o tamanho da capa
    return css
def capa_html(m, tit, sub, w=1080, h=1350):
    # tamanhos em % da altura: usa unidades vh simuladas por escala fixa
    css = CAPA_CSS
    import re
    def pct(mo):
        return f"{float(mo.group(1))*h/100:.1f}px"
    css = re.sub(r"font-size:([\d.]+)%", lambda mo: f"font-size:{float(mo.group(1))*h/100:.1f}px", css)
    css = re.sub(r"(letter-spacing:[\d.]+)em", r"\1em", css)
    return f"<!doctype html><meta charset=utf-8><style>{css}</style>{capa_corpo(m, tit, sub, w, h)}"
PAG_CSS = FONTS + """@page{size:148mm 210mm;margin:0}*{margin:0;box-sizing:border-box}body{font-family:A;color:#1d211b;font-size:9.4pt;line-height:1.45;background:#fff}
.pg{width:148mm;height:210mm;position:relative;overflow:hidden;page-break-after:always;background:#FEF5F0;padding:15mm 14mm 16mm 14mm}.pg.capa-pg{padding:0;background:#1B2117}
.cab{position:absolute;left:0;right:0;top:0;height:9mm;background:#1B2117;color:#DED6BF;font-size:6.4pt;letter-spacing:.16em;display:flex;align-items:center;justify-content:space-between;padding:0 14mm}
.rod{position:absolute;left:14mm;right:14mm;bottom:6mm;font-size:6.6pt;color:#8B714E;display:flex;justify-content:space-between;border-top:.3mm solid #DED6BF;padding-top:1.6mm}
.in{position:absolute;left:14mm;right:14mm;top:17mm;bottom:15mm}
h1,h2,h3{font-family:C;font-weight:500;color:#1B2117;line-height:1.05}h2{font-size:22pt;margin:0 0 3mm}h3{font-size:12.5pt;margin:4mm 0 1.5mm}
.kick{font-size:6.8pt;letter-spacing:.22em;color:#8B714E;text-transform:uppercase;margin-bottom:2mm}
.perg{font-family:C;font-style:italic;font-size:21pt;line-height:1.05;color:#1B2117;margin:0 0 3mm}.crit{display:inline-block;font-size:6.6pt;letter-spacing:.12em;background:#f2d6d6;color:#8e2b2b;padding:.6mm 2mm;border-radius:2mm;margin-left:2mm}
.fio{border-left:1.2mm solid #C9B37E;background:#fbf6ea;padding:2.4mm 3.2mm;margin:2.5mm 0;font-size:8.8pt}
ol.p{list-style:none;counter-reset:s;margin:0;padding:0}ol.p li{counter-increment:s;display:grid;grid-template-columns:7mm 1fr;gap:1mm;margin:0 0 2.2mm}ol.p li:before{content:counter(s);font-family:C;font-size:16pt;line-height:1;color:#C9B37E}
.ex{background:#1B2117;color:#FEF5F0;border-radius:2mm;padding:4mm;margin:2mm 0}.ex h3{color:#C9B37E;margin-top:0}.ex p{color:#DED6BF}
.err{border:.3mm solid #8B714E;border-radius:2mm;padding:3mm;margin:3mm 0}.err b,.fio b{color:#1B2117}
.nota{display:grid;grid-template-columns:27mm 1fr;gap:2mm;align-items:start;border-top:.3mm dotted #b9ad8c;padding:2mm 0}.nota span{font-family:C;font-size:11pt;white-space:nowrap;color:#1B2117}.nota.n0 span{color:#8e2b2b}.nota.n1 span{color:#9a5b13}.nota.n2 span{color:#2f6b3a}
.reg{margin-top:4mm}.reg .ln{border-bottom:.3mm solid #b9ad8c;height:6.4mm;font-size:7pt;color:#8B714E;display:flex;align-items:flex-end}
table.pl{width:100%;border-collapse:collapse;font-size:7.4pt;margin-top:2mm}table.pl th{background:#1B2117;color:#FEF5F0;font-weight:400;padding:1.4mm;text-align:left}table.pl td{border-bottom:.3mm solid #b9ad8c;height:9mm}
ul.t{margin:1mm 0 0 4mm;padding:0}ul.t li{margin:0 0 1mm}.gl{font-size:8.4pt;line-height:1.35}.gl dt{font-weight:700;color:#1B2117}.gl dd{margin:0 0 1.4mm}.aviso{font-size:8pt;color:#555;background:#f3eee0;padding:2.4mm;border-radius:2mm;margin-top:3mm}
.cap-pg .capa{width:148mm!important;height:210mm!important}"""
def pagina(corpo, m, n, tot=None):
    return f'<section class="pg"><div class="cab"><span>ZION HOTEL ACADEMY · GUIA {m:02d} · {NOMES[m].upper()}</span><span>RAIO-X DA HOSPEDAGEM</span></div><div class="in">{corpo}</div><div class="rod"><span>Mini Mentoria de Performance Hoteleira</span><span>{n}</span></div></section>'
def guia(m):
    g = json.load(open(A/f"ebook/conteudo/mod{m}.json", encoding="utf8")); qs = [q for q in FORM if q["module"] == m]; pgs = []; n = [1]
    def add(c): n[0] += 1; pgs.append(pagina(c, m, n[0]))
    # capa (usa o mesmo desenho da capa, em escala A5 em px: 559x794)
    import re
    h = 794; css = re.sub(r"font-size:([\d.]+)%", lambda mo: f"font-size:{float(mo.group(1))*h/100:.1f}px", CAPA_CSS.replace(FONTS, ""))
    capa = f'<section class="pg capa-pg"><style>{css}</style>{capa_corpo(m, g["titulo"], g["subtitulo"], 559, 794)}</section>'
    a = g["abertura"]
    add(f'<div class="kick">Como usar este guia</div><h2>{e(g["titulo"])}</h2><p>{e(a["para_que_serve"])}</p><h3>Tenha em mãos</h3><ul class="t">' + "".join(f"<li>{e(x)}</li>" for x in a["tenha_em_maos"]) + f'</ul><div class="fio"><b>Como trabalhar.</b> {e(a["como_trabalhar"])}</div><div class="aviso">Percurso do módulo: ' + " • ".join(e(q["topic"]) for q in qs) + '. Para cada pergunta, escolha: implementado e comprovado, parcial, ausente, não sei ou não se aplica. “Não sei” não vale zero.</div>')
    for i, (q, p) in enumerate(zip(qs, g["perguntas"]), 1):
        mt = META[q["id"]]; cal = CALC.get(mt["calc"]) if mt["calc"] else None
        add(f'<div class="kick">{m}.{i:02d} · {e(q["topic"])}' + ('<span class="crit">SEGURANÇA · LEGALIDADE</span>' if mt["critico"] else "") + f'</div><div class="perg">{e(q["question"])}</div><div class="fio"><b>Como fazer:</b> {e(q["procedure"])}<br><b>Evidência esperada:</b> {e(q["evidence"])}</div><h3>Por que importa</h3><p>{e(p["por_que_importa"])}</p><h3>Como coletar</h3><ol class="p">' + "".join(f"<li><span>{e(s)}</span></li>" for s in p["como_coletar"]) + "</ol>" + (f'<div class="aviso">Ferramenta ligada a esta pergunta: {e(cal)}.</div>' if cal else ""))
        add(f'<div class="kick">{m}.{i:02d} · exemplo e armadilha</div><div class="ex"><h3>{e(p["exemplo"]["titulo"])}</h3><p>{e(p["exemplo"]["texto"])}</p></div><div class="err"><b>Erro comum.</b> {e(p["erro_comum"])}</div><div class="aviso">Exemplos são sempre ilustrativos (dados fictícios), para mostrar o raciocínio. Os seus números podem ser muito diferentes.</div>')
        cl = p["como_ler"]
        add(f'<div class="kick">{m}.{i:02d} · como pontuar e verificar</div><h2 style="font-size:17pt">{e(q["question"])}</h2><div class="nota n0"><span>Ausente · 0</span><div>{e(cl["ausente"])}</div></div><div class="nota n1"><span>Parcial · 1</span><div>{e(cl["parcial"])}</div></div><div class="nota n2"><span>Comprovado · 2</span><div>{e(cl["comprovado"])}</div></div><h3>Ação sugerida</h3><p>{e(q["action"])}</p><h3>Como verificar</h3><p>{e(p["verificacao"])}</p><div class="reg"><div class="ln">Situação inicial</div><div class="ln">Ação · responsável · prazo</div><div class="ln">Resultado e decisão</div></div>')
    f = g["fechamento"]
    add(f'<div class="kick">Fechamento do módulo</div><h2>O que levar daqui</h2><p>{e(f["resumo"])}</p><h3>Glossário</h3><dl class="gl">' + "".join(f'<dt>{e(x["termo"])}</dt><dd>{e(x["definicao"])}</dd>' for x in f["glossario"]) + f'</dl><div class="aviso"><b>Limites.</b> {e(f["limites"])}</div>')
    add('<div class="kick">Seu plano do módulo</div><h2>Três ações para os próximos 30 dias</h2><table class="pl"><tr><th>Ação</th><th>Responsável</th><th>Prazo</th><th>Indicador</th><th>Evidência</th></tr>' + "<tr>" + "<td></td>" * 5 + "</tr>" * 1 + ("<tr>" + "<td></td>" * 5 + "</tr>") * 5 + '</table><div class="aviso">No portal, o Raio-X junta todos os módulos e monta o plano de 7, 30, 60 e 90 dias com o seu diagnóstico.</div>')
    html_ = f"<!doctype html><html lang=pt-BR><meta charset=utf-8><title>Guia {m:02d} · {e(g['titulo'])}</title><style>{PAG_CSS}</style>{capa}{''.join(pgs)}"
    (A/f"ebook/dist/guia-{m}.html").write_text(html_)
    (A/f"capa/dist/capa-{m}.html").write_text(capa_html(m, g["titulo"], g["subtitulo"]))
    return len(pgs) + 1
if __name__ == "__main__":
    print({m: guia(m) for m in range(1, 8)})
