"""Comando Mestre · Esperados independentes das regras aprovadas (O7 a O14, P-O8 a P-O14), escritos a partir
do texto das decisões, sem importar nem executar código da ZAIOS.

Regras (resumo): O8 indicação preliminar (positiva / atenção / negativa) e margem EBITDA; O9 saída = MAX(0, múltiplo × EBITDA);
O10 curva de 120 meses, saldos anuais, primeiro mês negativo, capital adicional, atraso de 6 meses no horizonte fixo com
CAPEX no cronograma original e aluguel + taxas fixas mantidos, VPL anual; O11 gestão e royalty sobre hospedagem, bruta
ou valor fixo; O12 giro = (déficit da rampa + meses negativos) + meses de reserva × (fixo + retirada + aluguel + taxas fixas
+ outras obrigações); O13 disponível x necessário; O14 categorias A (por noite), B (ticket × adesão × estadias),
C (anual nos meses escolhidos, sem rampa por padrão), custos e alíquota próprios.
Entradas: composicao_05f/cenarios_05f.json + mestre/cenarios_mestre.json. Saída: esperados_mestre.json. Reais, float.
"""
import json, pathlib, copy
AQUI = pathlib.Path(__file__).resolve().parent
F05 = json.loads((AQUI.parent / "composicao_05f" / "cenarios_05f.json").read_text())
E05 = json.loads((AQUI.parent / "independente" / "esperados_05f.json").read_text())
CASOS = json.loads((AQUI / "cenarios_mestre.json").read_text())["casos"]
BASE = {c["id"]: c for c in F05["cenarios"]}; COM = F05["comum_adotado"]
MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
DIAS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
JANELAS = {"projeto": (2, 5), "infra": (5, 8), "obra": (5, 8), "apoio": (5, 8), "ffe": (7, 8), "ose": (7, 8), "pre": (8, 9)}
TAXA, MULT, ATRASO, H = COM["taxa_desconto"], COM["multiplo_saida"], 6, 120

def rampa(k): return 0.4 if k <= 3 else 0.5 if k <= 6 else 0.75
def tab(c):
    s = c["sazonalidade"]
    if not s: return [(c["diaria"], c["ocupacao"])] * 12
    t = ["alta" if m in s["meses_alta"] else "baixa" if m in s["meses_baixa"] else "media" for m in MESES]
    return [(s["diaria"][x], s["ocupacao"][x]) for x in t]

def taxa_modelo(base, pct, fixo, hosp, bruta):
    return fixo if base == "fixo" else (hosp if base == "hospedagem" else bruta) * pct

def mes(c, m, fat):
    d, o = tab(c)[m]; n = c["unidades"] * DIAS[m] * o * fat; hosp = n * d
    est = n / c["permanencia"]; k = c["compl"]
    legado = hosp * c["outras_pct"]
    a_nova = n * k.get("a_noite", 0); b = est * k.get("b_adesao", 0) * k.get("b_ticket", 0)
    mc = k.get("c_meses") or MESES; cc = k.get("c_anual", 0) / len(mc) if MESES[m] in mc else 0.0
    if k.get("c_rampa"): cc *= fat
    bruta = hosp + legado + a_nova + b + cc
    aliq = k.get("aliquota", c["tributos_pct"])
    ded = (hosp + legado) * c["tributos_pct"] + (a_nova + b + cc) * aliq
    custo_compl = a_nova * k.get("a_custo", 0) + b * k.get("b_custo", 0) + cc * k.get("c_custo", 0)
    cv = est * c["custo_estadia"] + custo_compl
    mcontr = bruta - ded - cv; fixos = c["fixo_mensal"]; op = mcontr - fixos
    g = taxa_modelo(c["gestao_base"], c["gestao_pct"], c["gestao_fixo"], hosp, bruta)
    r = taxa_modelo(c["royalty_base"], c["royalty_pct"], c["royalty_fixo"], hosp, bruta)
    modelo = c["aluguel_mensal"] + g + r; ebitda = op - modelo
    return dict(noites=n, hosp=hosp, A=legado + a_nova, B=b, C=cc, bruta=bruta, ded=ded, custo_compl=custo_compl, cv=cv, mc=mcontr, fixos=fixos,
                op=op, gestao=g, royalty=r, modelo=modelo, ebitda=ebitda, ger=ebitda)

def soma(ms): return {k: sum(x[k] for x in ms) for k in ms[0]}
def regime(c): return [mes(c, m, 1.0) for m in range(12)]
def primeiro(c, ab): return [mes(c, (ab + k) % 12, rampa(k + 1)) for k in range(12)]
def ops(c, ab, n, campo="ger"):
    reg, pri = regime(c), primeiro(c, ab)
    return [(pri[k] if k < 12 else reg[(ab + k) % 12])[campo] for k in range(n)]
def vpl(f, i=TAXA): return sum(v / (1 + i) ** t for t, v in enumerate(f))
def tir(f):
    s = [1 if v > 0 else -1 for v in f if abs(v) > 1e-9]
    if sum(1 for a, b in zip(s, s[1:]) if a != b) == 0: return None
    grade = [-0.99 + 0.001 * i for i in range(1990)] + [1 + 0.01 * i for i in range(901)]
    for a, b in zip(grade, grade[1:]):
        fa, fb = vpl(f, a), vpl(f, b)
        if (fa > 0) != (fb > 0):
            for _ in range(200):
                mid = (a + b) / 2; fm = vpl(f, mid)
                if (fm > 0) == (fa > 0): a, fa = mid, fm
                else: b = mid
            return (a + b) / 2
    return None
def payback(f, reg):
    if reg <= 0: return None
    acc = 0.0
    for t, v in enumerate(f):
        ant = acc; acc += v
        if t > 0 and acc >= 0: return t - 1 + (-ant) / v
    return len(f) - 1 + (-acc) / reg
def curva(capt, crono, mes_proj, ger):
    saldo, p = 0.0, []
    for m in range(1, H + 1):
        if m == 1: saldo += capt
        if m <= len(crono): saldo -= crono[m - 1]
        k = m - mes_proj
        if 0 <= k < len(ger): saldo += ger[k]
        p.append(saldo)
    menor = min(p); neg = next((i + 1 for i, s in enumerate(p) if s < 0), None)
    return {"menor": menor, "mes_menor": p.index(menor) + 1, "final": p[-1], "menor36": min(p[:36]), "saldo36": p[35], "primeiro_negativo": neg,
            "capital_adicional": max(0.0, -menor), "anuais": [p[12 * k + 11] for k in range(10)]}

def preparar(caso):
    c = copy.deepcopy(BASE[caso["base"]])
    c["outras_pct"] = 0.0 if caso.get("outras_pct_zero") else E05["cenarios"][c["id"]]["R2_zaios"]["outras_pct"]
    c["gestao_base"] = caso.get("gestao_base", "bruta"); c["royalty_base"] = caso.get("royalty_base", "bruta")
    c["gestao_fixo"] = caso.get("gestao_fixo", 0.0); c["royalty_fixo"] = caso.get("royalty_fixo", 0.0)
    c["compl"] = caso.get("compl", {}); return c

def estudo(caso):
    c = preparar(caso); ab = MESES.index(c["mes_abertura"])
    reg, pri = regime(c), primeiro(c, ab); R, P = soma(reg), soma(pri)
    linhas = {k: c["investimento"] * v for k, v in COM["linhas_capex_proporcao"].items()}; capex = sum(linhas.values())
    crono = [0.0] * 9
    for k, (a, b) in JANELAS.items():
        for m in range(a, b + 1): crono[m - 1] += linhas[k] / (b - a + 1)
    mes_proj = max(i + 1 for i, v in enumerate(crono) if v > 0) + 1
    # O8
    m_op = R["op"] / R["bruta"]; m_eb = R["ebitda"] / R["bruta"]
    gfix, rfix = c["gestao_base"] == "fixo", c["royalty_base"] == "fixo"
    tx_var = (0 if gfix else R["gestao"]) + (0 if rfix else R["royalty"])
    tx_fix = 12 * ((c["gestao_fixo"] if gfix else 0) + (c["royalty_fixo"] if rfix else 0))
    k = c["compl"]; aliqC = k.get("aliquota", c["tributos_pct"])
    cliq = R["C"] * (1 - aliqC - k.get("c_custo", 0) - (c["gestao_pct"] if c["gestao_base"] == "bruta" else 0) - (c["royalty_pct"] if c["royalty_base"] == "bruta" else 0))
    contrib = (R["mc"] - tx_var - cliq) / R["noites"]
    disp = sum(c["unidades"] * d for d in DIAS); ocup_media = R["noites"] / disp
    eq = max(0.0, 12 * c["fixo_mensal"] + 12 * c["aluguel_mensal"] + tx_fix - cliq) / contrib if contrib > 0 else None
    folga = ocup_media - eq / disp if eq is not None else None
    neg = m_op < 0.1 - 1e-9 or (folga is not None and folga < 0) or (eq is None) or m_eb < 0
    indic = "negativa" if neg else "atencao" if m_eb < 0.1 - 1e-9 else "positiva"
    # O12
    acc, mn = 0.0, 0.0
    for x in pri: acc += x["ger"]; mn = min(mn, acc)
    deficit = -mn; saz = sum(-x["ger"] for x in reg if x["ger"] < 0); tecnica = deficit + saz
    base_m = c["fixo_mensal"] + (0 if caso.get("fixo_inclui_aluguel") else c["aluguel_mensal"]) + tx_fix / 12 + caso.get("outras_obrigacoes", 0)
    meses_res = caso.get("reserva_meses", 3); reserva = meses_res * base_m; giro = tecnica + reserva
    capt = capex + giro
    # O9 e fluxo
    f = [-capex, P["ger"]] + [R["ger"]] * 9; saida = max(0.0, MULT * R["ebitda"]); fc = f[:-1] + [f[-1] + saida]
    # O10
    cv = curva(capt, crono, mes_proj, ops(c, ab, H))
    ab2 = (ab + ATRASO) % 12; custo_atr = c["aluguel_mensal"] + tx_fix / 12
    cv2 = curva(capt, crono, mes_proj, [-custo_atr] * ATRASO + ops(c, ab2, H))
    n_op = H - (mes_proj - 1)
    rec_nr = sum(ops(c, ab, n_op, "bruta")) - sum(ops(c, ab2, n_op - ATRASO, "bruta"))
    serie = [-custo_atr] * ATRASO + ops(c, ab2, 120 - ATRASO)
    vpl_atr = vpl([-capex] + [sum(serie[12 * j:12 * j + 12]) for j in range(10)])
    # cenários
    def cen(dd, oo):
        c2 = copy.deepcopy(c)
        if c2["sazonalidade"]:
            for t in ("alta", "media", "baixa"): c2["sazonalidade"]["diaria"][t] *= 1 + dd; c2["sazonalidade"]["ocupacao"][t] = min(1, c2["sazonalidade"]["ocupacao"][t] * (1 + oo))
        c2["diaria"] *= 1 + dd; c2["ocupacao"] = min(1, c2["ocupacao"] * (1 + oo))
        Rv, Pv = soma(regime(c2)), soma(primeiro(c2, ab)); fv = [-capex, Pv["ger"]] + [Rv["ger"]] * 9
        return {"geracao_regime": Rv["ger"], "vpl_sem": vpl(fv), "vpl_com": vpl(fv[:-1] + [fv[-1] + max(0.0, MULT * Rv["ebitda"])]), "complC": Rv["C"]}
    cons, otim = cen(-0.1, -0.2), cen(0.1, 0.15)
    pb = payback(f, R["ger"]); col = cv["menor"] / capex
    passos = ["passa" if R["ger"] >= 0 else "redesenhar",
              "passa" if cons["geracao_regime"] >= 0 else ("ajustar" if -cons["geracao_regime"] <= 3 * c["fixo_mensal"] + 1e-9 else "redesenhar"),
              "redesenhar" if pb is None else "passa" if pb <= 8 + 1e-9 else "ajustar" if pb <= 12 + 1e-9 else "redesenhar",
              "passa" if vpl(f) >= 0 else ("ajustar" if vpl(fc) > 0 else "redesenhar"),
              "redesenhar" if col < 0 else "passa" if col >= 0.1 - 1e-9 else "ajustar"]
    decisao = "Redesenhar" if "redesenhar" in passos else "Ajustar" if "ajustar" in passos else "Avançar"
    out = {"hospedagem": R["hosp"], "compl_a": R["A"], "compl_b": R["B"], "compl_c": R["C"], "receita_bruta": R["bruta"], "deducoes": R["ded"], "custos_complementares": R["custo_compl"],
           "custos_variaveis": R["cv"], "gestao": R["gestao"], "royalty": R["royalty"], "custos_modelo": R["modelo"], "ebitda": R["ebitda"], "geracao_regime": R["ger"], "geracao_ano1": P["ger"],
           "margem_operacional": m_op, "margem_ebitda": m_eb, "indicacao": indic, "equilibrio_noites": eq, "deficit_rampa": deficit, "sazonalidade": saz, "giro_tecnica": tecnica,
           "giro_base_mensal": base_m, "giro_reserva": reserva, "giro": giro, "captacao": capt, "valor_saida": saida, "vpl_sem": vpl(f), "vpl_com": vpl(fc), "tir_sem": tir(f),
           "payback_simples": pb, "conservador_vpl_sem": cons["vpl_sem"], "otimista_vpl_sem": otim["vpl_sem"], "conservador_compl_c": cons["complC"],
           "curva_meses": H, "curva_menor": cv["menor"], "curva_mes_menor": cv["mes_menor"], "curva_final": cv["final"], "curva_menor36": cv["menor36"], "curva_primeiro_negativo": cv["primeiro_negativo"],
           "capital_adicional": cv["capital_adicional"], "saldos_anuais": cv["anuais"], "atraso_custos_mantidos": custo_atr * ATRASO, "atraso_receita_nao_realizada": rec_nr,
           "atraso_perda_saldo_final": cv["final"] - cv2["final"], "atraso_vpl_sem": vpl_atr, "atraso_perda_vpl": vpl(f) - vpl_atr, "atraso_menor": cv2["menor"],
           "colchao": col, "passos": passos, "decisao": decisao}
    if "giro_disponivel" in caso:
        d = caso["giro_disponivel"]; dif = d - giro
        out.update({"giro_disponivel": d, "giro_diferenca": dif, "giro_deficit": max(0.0, -dif), "giro_excedente": max(0.0, dif), "usos_totais": capt})
    return out

if __name__ == "__main__":
    res = {"_gerado_por": "referencia_mestre.py", "casos": {cs["id"]: {"entrada": cs, "esperado": estudo(cs)} for cs in CASOS}}
    (AQUI / "esperados_mestre.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    for k, v in res["casos"].items():
        e = v["esperado"]; print(k, round(e["ebitda"], 2), round(e["giro"], 2), e["indicacao"], e["decisao"], e["curva_primeiro_negativo"])
