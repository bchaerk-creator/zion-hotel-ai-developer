"""Comando 05G-B · Teste B · esperados independentes da composição com pró-labore, reserva, quebra, contingência,
taxas e múltiplos alternativos. Não importa nem executa código da ZAIOS. Regras: Dicionário v0.4 e FORMULAS.md
(regra documentada da ZAIOS, família R2 do 05F), estendidas aos parâmetros abaixo. Valores em reais, float.
Saída: esperados_05g.json (ao lado)."""
import json, math, pathlib
AQUI = pathlib.Path(__file__).resolve().parent
F05 = json.loads((AQUI.parent / "composicao_05f" / "cenarios_05f.json").read_text())
ENT = json.loads((AQUI / "cenarios_05g.json").read_text())
COM = F05["comum_adotado"]; BASE = {c["id"]: c for c in F05["cenarios"]}
MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
DIAS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
JAN = {"projeto": (2, 5), "infra": (5, 8), "obra": (5, 8), "apoio": (5, 8), "ffe": (7, 8), "ose": (7, 8), "pre": (8, 9)}
SEMANAS = 4.33

def rampa(k): return 0.4 if k <= 3 else 0.5 if k <= 6 else 0.75
def tabela(c, dd=0.0, oo=0.0):
    s = c["sazonalidade"]
    if s:
        t = ["alta" if m in s["meses_alta"] else "baixa" if m in s["meses_baixa"] else "media" for m in MESES]
        return [(s["diaria"][x] * (1 + dd), min(1, s["ocupacao"][x] * (1 + oo))) for x in t]
    return [(c["diaria"] * (1 + dd), min(1, c["ocupacao"] * (1 + oo)))] * 12

def modelo(c, p, dd=0.0, oo=0.0, fixo_mult=1.0):
    tab0 = tabela(c)
    hosp_reg0 = sum(c["unidades"] * DIAS[m] * o * d for m, (d, o) in enumerate(tab0))
    outras_pct = c["outras_anuais"] / hosp_reg0 if hosp_reg0 else 0.0  # percentual fixado no cenário base (como a ZAIOS)
    retirada = p["horas_semana"] * p["custo_hora"] * SEMANAS
    fixo = c["fixo_mensal"] * fixo_mult
    tab = tabela(c, dd, oo)
    def mes(m, f):
        d, o = tab[m]
        n = c["unidades"] * DIAS[m] * o * f; h = n * d; ou = h * outras_pct; b = h + ou
        ded = b * c["tributos_pct"]
        cv = (n / c["permanencia"]) * c["custo_estadia"] + h * p["quebra_pct"]
        mc = b - ded - cv; fx = fixo + retirada; op = mc - fx
        mod = c["aluguel_mensal"] + b * (c["gestao_pct"] + c["royalty_pct"]); eb = op - mod; res = b * p["reserva_pct"]
        return dict(noites=n, hosp=h, outras=ou, bruta=b, ded=ded, cv=cv, mc=mc, fixos=fx, op=op, modelo=mod, ebitda=eb, reserva=res, ger=eb - res)
    reg = [mes(m, 1.0) for m in range(12)]
    ab = MESES.index(c["mes_abertura"])
    def pri(abertura): return [mes((abertura + k) % 12, rampa(k + 1)) for k in range(12)]
    return reg, pri, retirada, fixo

def soma(ms): return {k: sum(m[k] for m in ms) for k in ms[0]}
def vpl(f, i): return sum(v / (1 + i) ** t for t, v in enumerate(f))
def trocas(f):
    s = [1 if v > 0 else -1 for v in f if abs(v) > 1e-9]
    return sum(1 for a, b in zip(s, s[1:]) if a != b)
def tir(f):
    if trocas(f) == 0: return None
    g = [-0.99 + 0.001 * i for i in range(1990)] + [1 + 0.01 * i for i in range(901)]
    for a, b in zip(g, g[1:]):
        fa, fb = vpl(f, a), vpl(f, b)
        if fa == 0: return a
        if (fa > 0) != (fb > 0):
            for _ in range(200):
                m = (a + b) / 2; fm = vpl(f, m)
                if (fm > 0) == (fa > 0): a, fa = m, fm
                else: b = m
            return (a + b) / 2
    return None
def pb(f, reg=None, descontado_i=None):
    if descontado_i is None and reg is not None and reg <= 0: return None
    ff = [v / (1 + descontado_i) ** t for t, v in enumerate(f)] if descontado_i is not None else f
    acc = 0.0
    for t, v in enumerate(ff):
        ant = acc; acc += v
        if t == 0 and acc >= 0: return 0.0
        if t > 0 and acc >= 0: return t - 1 + (-ant) / v
    return None if descontado_i is not None else len(f) - 1 + (-acc) / reg

def estudo(c, p):
    taxa, mult = p["taxa_desconto"], p["multiplo_saida"]
    reg, pri, retirada, fixo = modelo(c, p); R = soma(reg)
    ab = MESES.index(c["mes_abertura"]); P = pri(ab); PS = soma(P)
    inv = c["investimento"]; linhas = {k: inv * v for k, v in COM["linhas_capex_proporcao"].items()}
    base_cont = linhas["infra"] + linhas["obra"] + linhas["apoio"]
    cont = round(base_cont * 100 * p["contingencia_pct"]) / 100  # centavos inteiros
    capex = sum(linhas.values()) + cont
    acc, mn = 0.0, 0.0
    for m in P: acc += m["ger"]; mn = min(mn, acc)
    deficit = -mn; saz = sum(-m["ger"] for m in reg if m["ger"] < 0)
    giroA = 6 * c["fixo_mensal"]; giroB = deficit + saz + 3 * (fixo + retirada); giro = max(giroA, giroB)
    captacao = capex + giro
    f = [-capex, PS["ger"]] + [R["ger"]] * 9
    saida = mult * R["ebitda"]; fc = f[:-1] + [f[-1] + saida]
    crono = [0.0] * 9
    for k, (a, b) in JAN.items():
        for m in range(a, b + 1): crono[m - 1] += linhas[k] / (b - a + 1)
    mes_proj = max(i + 1 for i, v in enumerate(crono) if v > 0) + 1
    def curva(mp, abertura, usar):
        Pm = pri(abertura); ger = [m["ger"] for m in Pm] + [reg[(abertura + k) % 12]["ger"] for k in range(12, 36)]
        saldo, pts = 0.0, []
        for mes in range(1, 37):
            if mes == 1: saldo += captacao
            if mes <= 9: saldo -= crono[mes - 1]
            if usar and 5 <= mes <= 8: saldo -= cont / 4
            k = mes - mp
            if 0 <= k < 36: saldo += ger[k] if k < len(ger) else 0
            pts.append(saldo)
        mn_ = min(pts); return {"menor": mn_, "mes": pts.index(mn_) + 1, "final": pts[-1]}
    sem, com = curva(mes_proj, ab, False), curva(mes_proj, ab, True)
    atr = curva(mes_proj + 6, (ab + 6) % 12, True)
    col = com["menor"] / capex
    def var(dd, oo, fm=1.0):
        r2, pri2, _, _ = modelo(c, p, dd, oo, fm); Rv = soma(r2); Pv = soma(pri2(ab))
        fv = [-capex, Pv["ger"]] + [Rv["ger"]] * 9
        return Rv, fv
    Rc, fcv = var(-0.1, -0.2)
    cons = {"geracaoRegime": Rc["ger"], "payback": pb(fcv, Rc["ger"]), "vplSem": vpl(fcv, taxa), "vplCom": vpl(fcv[:-1] + [fcv[-1] + mult * Rc["ebitda"]], taxa)}
    sens = {"diaria": vpl(var(-0.1, 0)[1], taxa), "ocupacao": vpl(var(0, -0.1)[1], taxa), "fixo": vpl(var(0, 0, 1.1)[1], taxa), "capex": vpl([-capex * 1.1] + f[1:], taxa)}
    fixocr = fixo + retirada; gc = cons["geracaoRegime"]; pbs = pb(f, R["ger"]); vs, vc = vpl(f, taxa), vpl(fc, taxa)
    passos = ["passa" if R["ger"] >= 0 else "redesenhar",
              "passa" if gc >= 0 else ("ajustar" if -gc <= 3 * fixocr + 1e-9 else "redesenhar"),
              "redesenhar" if pbs is None else "passa" if pbs <= 8 + 1e-9 else "ajustar" if pbs <= 12 + 1e-9 else "redesenhar",
              "passa" if vs >= 0 else ("ajustar" if vc > 0 else "redesenhar"),
              "redesenhar" if col < 0 else "passa" if col >= 0.1 - 1e-9 else "ajustar"]
    contrib = (R["mc"] - R["bruta"] * (c["gestao_pct"] + c["royalty_pct"])) / R["noites"]
    eq = (R["fixos"] + 12 * c["aluguel_mensal"]) / contrib if contrib > 0 else None
    return {"retirada_mensal": retirada, "receita_bruta": R["bruta"], "custos_variaveis": R["cv"], "custos_fixos": R["fixos"], "resultado_operacional": R["op"],
            "custos_modelo": R["modelo"], "ebitda": R["ebitda"], "reserva": R["reserva"], "geracao_regime": R["ger"], "geracao_ano1": PS["ger"],
            "margem_operacional": R["op"] / R["bruta"], "equilibrio_noites": eq, "contingencia": cont, "capex": capex, "deficit_rampa": deficit,
            "sazonalidade_giro": saz, "giro_a": giroA, "giro_b": giroB, "giro": giro, "captacao": captacao, "retorno_anual": R["ger"] / capex,
            "retorno_ebitda": R["ebitda"] / capex, "payback_simples": pbs, "payback_descontado": pb(f, descontado_i=taxa), "valor_saida": saida,
            "vpl_sem": vs, "vpl_com": vc, "tir_sem": tir(f), "tir_com": tir(fc), "curva_sem_menor": sem["menor"], "curva_com_menor": com["menor"],
            "curva_com_mes_menor": com["mes"], "curva_com_final": com["final"], "colchao": col, "atraso_com_menor": atr["menor"],
            "estresse_receita_menor": R["ger"] - 0.3 * R["bruta"], "estresse_vpl_capex_maior": vpl([-capex * 1.25] + f[1:], taxa),
            "conservador": cons, "sensibilidade": sens, "passos": passos,
            "decisao": "Redesenhar" if "redesenhar" in passos else "Ajustar" if "ajustar" in passos else "Avançar"}

out = {"_gerado_por": "composicao_05g_referencia.py", "cenarios": {}}
for p in ENT["cenarios"]:
    out["cenarios"][p["id"]] = estudo(BASE[p["base"]], p)
(AQUI / "esperados_05g.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
for k, v in out["cenarios"].items():
    print(k, "ebitda %.2f ger %.2f capex %.2f giro %.2f vpl %.2f vplc %.2f pb %s tir %s col %.4f %s" % (v["ebitda"], v["geracao_regime"], v["capex"], v["giro"], v["vpl_sem"], v["vpl_com"], v["payback_simples"], v["tir_sem"], v["colchao"], v["decisao"]))
