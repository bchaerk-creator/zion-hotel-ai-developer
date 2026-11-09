"""Comando 05F · Esperados independentes da camada de composição da ZAIOS (3 cenários + estresse).

Não importa nem executa código da ZAIOS. Duas famílias de regra:
- R1 (regra do Comando 05F): gestão e royalties sobre a receita de hospedagem; outras receitas em R$/ano;
  capital de giro informado.
- R2 (regra documentada da ZAIOS: Dicionário v0.4 e FORMULAS.md): gestão e royalties sobre a receita bruta;
  outras = % das diárias; rampa 40/50/75; giro A/B; fluxo de 10 anos; curva de 36 meses; régua de 5 passos.
Entradas: testes/financeiro/composicao_05f/cenarios_05f.json. Saída: esperados_05f.json (ao lado).
Valores em reais, precisão completa (float), sem arredondamento.
"""
import json, pathlib
AQUI = pathlib.Path(__file__).resolve().parent
ENT = json.loads((AQUI.parent / "composicao_05f" / "cenarios_05f.json").read_text())
MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
DIAS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
assert sum(DIAS) == 365
COM = ENT["comum_adotado"]
JANELAS = {"projeto": (2, 5), "infra": (5, 8), "obra": (5, 8), "apoio": (5, 8), "ffe": (7, 8), "ose": (7, 8), "pre": (8, 9)}

def rampa(k):  # k = mês da operação, começando em 1
    return 0.4 if k <= 3 else 0.5 if k <= 6 else 0.75

def temporadas(c):
    s = c["sazonalidade"]
    if not s: return ["media"] * 12
    return ["alta" if m in s["meses_alta"] else "baixa" if m in s["meses_baixa"] else "media" for m in MESES]

def tabela(c):
    s = c["sazonalidade"]; t = temporadas(c)
    if s: return [(s["diaria"][x], s["ocupacao"][x]) for x in t]
    return [(c["diaria"], c["ocupacao"])] * 12

def noites_hosp(c, fat=None):
    """Noites vendidas e receita de hospedagem por mês (fat = fatores de rampa por mês do calendário)."""
    out = []
    for m, (d, o) in enumerate(tabela(c)):
        f = 1.0 if fat is None else fat[m]
        n = c["unidades"] * DIAS[m] * o * f
        out.append((n, n * d))
    return out

def mes_dre(c, n, hosp, outras, base_modelo):
    """Demonstrativo de um mês. base_modelo: 'bruta' (R2) ou 'hospedagem' (R1)."""
    bruta = hosp + outras
    trib = bruta * c["tributos_pct"]
    estadias = n / c["permanencia"]
    cv = estadias * c["custo_estadia"]
    fixo = c["fixo_mensal"]
    op = bruta - trib - cv - fixo
    base = bruta if base_modelo == "bruta" else hosp
    gr = base * (c["gestao_pct"] + c["royalty_pct"])
    modelo = c["aluguel_mensal"] + gr
    ebitda = op - modelo
    return dict(noites=n, estadias=estadias, hosp=hosp, outras=outras, bruta=bruta, trib=trib, cv=cv, fixo=fixo, op=op,
                aluguel=c["aluguel_mensal"], gestao_royalty=gr, modelo=modelo, ebitda=ebitda, ger=ebitda)

def soma(meses):
    return {k: sum(m[k] for m in meses) for k in meses[0]}

def outras_pct(c):
    hosp_ano = sum(h for _, h in noites_hosp(c))
    return c["outras_anuais"] / hosp_ano if hosp_ano > 0 else 0.0

def regime(c, base, regra_outras):
    pct = outras_pct(c)
    meses = []
    for m, (n, h) in enumerate(noites_hosp(c)):
        # R2: outras proporcionais às diárias; R1: só o total anual importa no regime (distribuídas igual, para o mês a mês)
        o = h * pct if regra_outras == "pct" else c["outras_anuais"] * DIAS[m] / 365
        meses.append(mes_dre(c, n, h, o, base))
    return meses

def primeiro_ano(c, base, abertura):
    pct = outras_pct(c); meses = []
    for k in range(12):
        m = (abertura + k) % 12; f = rampa(k + 1)
        d, o = tabela(c)[m]
        n = c["unidades"] * DIAS[m] * o * f; h = n * d
        meses.append(mes_dre(c, n, h, h * pct, base))
    return meses

def vpl(f, i): return sum(v / (1 + i) ** t for t, v in enumerate(f))

def trocas(f):
    s = [1 if v > 0 else -1 for v in f if abs(v) > 1e-9]
    return sum(1 for a, b in zip(s, s[1:]) if a != b)

def tir(f):
    """Raiz de VPL(r)=0 por bissecção, no menor r da grade em que o VPL troca de sinal (−0,99 a 10)."""
    if trocas(f) == 0: return None
    grade = [-0.99 + 0.001 * i for i in range(1990)] + [1 + 0.01 * i for i in range(901)]
    for a, b in zip(grade, grade[1:]):
        fa, fb = vpl(f, a), vpl(f, b)
        if fa == 0: return a
        if (fa > 0) != (fb > 0):
            for _ in range(200):
                mid = (a + b) / 2; fm = vpl(f, mid)
                if (fm > 0) == (fa > 0): a, fa = mid, fm
                else: b = mid
            return (a + b) / 2
    return None

def payback_simples(f, reg):
    if reg <= 0: return None
    acc = 0.0
    for t, v in enumerate(f):
        ant = acc; acc += v
        if t == 0 and acc >= 0: return 0.0
        if t > 0 and acc >= 0: return t - 1 + (-ant) / v
    return len(f) - 1 + (-acc) / reg

def payback_desc(f, i):
    pv = [v / (1 + i) ** t for t, v in enumerate(f)]; acc = 0.0
    for t, v in enumerate(pv):
        ant = acc; acc += v
        if t == 0 and acc >= 0: return 0.0
        if t > 0 and acc >= 0: return t - 1 + (-ant) / v
    return None

def cronograma(capex_linhas):
    meses = [0.0] * 9
    for k, (a, b) in JANELAS.items():
        n = b - a + 1; v = capex_linhas[k]
        for m in range(a, b + 1): meses[m - 1] += v / n
    return meses

def curva(captacao, crono, mes_proj, geracoes, total=36):
    saldo, pontos = 0.0, []
    for mes in range(1, total + 1):
        if mes == 1: saldo += captacao
        if mes <= len(crono): saldo -= crono[mes - 1]
        k = mes - mes_proj
        if 0 <= k < len(geracoes): saldo += geracoes[k]
        pontos.append(saldo)
    menor = min(pontos)
    return {"menor": menor, "mesMenor": pontos.index(menor) + 1, "final": pontos[-1]}

def estudo(c, base="bruta", giro_rule="zaios", regra_outras="pct"):
    abertura = MESES.index(c["mes_abertura"])
    reg = regime(c, base, regra_outras); R = soma(reg)
    pri = primeiro_ano(c, base, abertura); P = soma(pri)
    inv = c["investimento"]
    linhas = {k: inv * v for k, v in COM["linhas_capex_proporcao"].items()}
    capex = sum(linhas.values())
    # capital de giro
    acc, mn = 0.0, 0.0
    for m in pri: acc += m["ger"]; mn = min(mn, acc)
    deficit = -mn
    saz = sum(-m["ger"] for m in reg if m["ger"] < 0)
    giroA = 6 * c["fixo_mensal"]; giroB = deficit + saz + 3 * c["fixo_mensal"]
    giro = max(giroA, giroB) if giro_rule == "zaios" else c["giro_informado"]
    captacao = capex + giro
    taxa, mult = COM["taxa_desconto"], COM["multiplo_saida"]
    f = [-capex, P["ger"]] + [R["ger"]] * 9
    saida = mult * R["ebitda"]
    fc = f[:-1] + [f[-1] + saida]
    crono = cronograma(linhas)
    mes_proj = max(i + 1 for i, v in enumerate(crono) if v > 0) + 1
    ger_op = [m["ger"] for m in pri] + [reg[(abertura + k) % 12]["ger"] for k in range(12, 36)]
    cv = curva(captacao, crono, mes_proj, ger_op)
    # atraso de 6 meses
    ab2 = (abertura + 6) % 12
    pri2 = primeiro_ano(c, base, ab2)
    ger2 = [m["ger"] for m in pri2] + [reg[(ab2 + k) % 12]["ger"] for k in range(12, 36)]
    cv2 = curva(captacao, crono, mes_proj + 6, ger2)
    col = cv["menor"] / capex
    # cenários (diária e ocupação variam; ocupação limitada a 100%)
    def variante(dd, oo, fixo_mult=1.0):
        c2 = json.loads(json.dumps(c))
        if c2["sazonalidade"]:
            for t in ("alta", "media", "baixa"):
                c2["sazonalidade"]["diaria"][t] *= (1 + dd); c2["sazonalidade"]["ocupacao"][t] = min(1, c2["sazonalidade"]["ocupacao"][t] * (1 + oo))
        c2["diaria"] *= (1 + dd); c2["ocupacao"] = min(1, c2["ocupacao"] * (1 + oo)); c2["fixo_mensal"] *= fixo_mult
        # outras_pct fica igual ao do cenário base (a ZAIOS mantém o percentual)
        c2["_pct"] = outras_pct(c)
        return c2
    def ger_variante(c2):
        pct = c2["_pct"]
        regv = [mes_dre(c2, n, h, h * pct, base) for n, h in noites_hosp(c2)]
        priv = []
        for k in range(12):
            m = (abertura + k) % 12; d, o = tabela(c2)[m]; n = c2["unidades"] * DIAS[m] * o * rampa(k + 1); h = n * d
            priv.append(mes_dre(c2, n, h, h * pct, base))
        Rv, Pv = soma(regv), soma(priv)
        fv = [-capex, Pv["ger"]] + [Rv["ger"]] * 9
        return Rv, Pv, fv
    cen = {}
    for nome, (dd, oo) in {"conservador": (-0.1, -0.2), "otimista": (0.1, 0.15)}.items():
        Rv, Pv, fv = ger_variante(variante(dd, oo))
        cen[nome] = {"geracaoRegime": Rv["ger"], "geracaoAno1": Pv["ger"], "ebitdaRegime": Rv["ebitda"], "payback": payback_simples(fv, Rv["ger"]),
                     "vplSem": vpl(fv, taxa), "vplCom": vpl(fv[:-1] + [fv[-1] + mult * Rv["ebitda"]], taxa)}
    sens = {}
    for nome, args in {"diaria": (-0.1, 0, 1), "ocupacao": (0, -0.1, 1), "fixo": (0, 0, 1.1)}.items():
        _, _, fv = ger_variante(variante(*args)); sens[nome] = vpl(fv, taxa)
    sens["capex"] = vpl([-capex * 1.1] + f[1:], taxa)
    fm = [-capex * 1.25] + f[1:]
    # régua
    p1 = "passa" if R["ger"] >= 0 else "redesenhar"
    gc = cen["conservador"]["geracaoRegime"]
    p2 = "passa" if gc >= 0 else ("ajustar" if -gc <= 3 * c["fixo_mensal"] + 1e-9 else "redesenhar")
    pb = payback_simples(f, R["ger"])
    p3 = "redesenhar" if pb is None else "passa" if pb <= 8 + 1e-9 else "ajustar" if pb <= 12 + 1e-9 else "redesenhar"
    vs, vc = vpl(f, taxa), vpl(fc, taxa)
    p4 = "passa" if vs >= 0 else ("ajustar" if vc > 0 else "redesenhar")
    p5 = "redesenhar" if col < 0 else "passa" if col >= 0.1 - 1e-9 else "ajustar"
    passos = [p1, p2, p3, p4, p5]
    decisao = "Redesenhar" if "redesenhar" in passos else "Ajustar" if "ajustar" in passos else "Avançar"
    # equilíbrio anual (custos do modelo incluídos) e margem operacional (antes dos custos do modelo)
    base_ano = R["bruta"] if base == "bruta" else R["hosp"]
    contrib = (R["bruta"] - R["trib"] - R["cv"] - base_ano * (c["gestao_pct"] + c["royalty_pct"])) / R["noites"]
    disp = c["unidades"] * 365
    eq_noites = (R["fixo"] + 12 * c["aluguel_mensal"]) / contrib if contrib > 0 else None
    eq_ocup = eq_noites / disp if eq_noites is not None else None
    ocup_media = R["noites"] / disp
    margem_op = R["op"] / R["bruta"]
    folga = None if eq_ocup is None else ocup_media - eq_ocup
    folga_neg = (contrib <= 0) if eq_ocup is None else folga < 0
    regua = "boa" if margem_op >= 0.3 - 1e-9 else "viavel" if margem_op >= 0.2 - 1e-9 else "apertada" if margem_op >= 0.1 - 1e-9 else "nao_fecha"
    selo_p6 = "Ajustar" if (margem_op < 0.1 - 1e-9 or folga_neg) else "Avançar"
    return {
        "receita_hospedagem": R["hosp"], "noites_vendidas": R["noites"], "estadias": R["estadias"], "outras": R["outras"], "receita_bruta": R["bruta"],
        "tributos": R["trib"], "custos_variaveis": R["cv"], "custos_fixos": R["fixo"], "resultado_operacional": R["op"], "aluguel": R["aluguel"],
        "gestao_royalty": R["gestao_royalty"], "custos_modelo": R["modelo"], "ebitda": R["ebitda"], "geracao_regime": R["ger"],
        "receita_bruta_ano1": P["bruta"], "ebitda_ano1": P["ebitda"], "geracao_ano1": P["ger"],
        "meses_negativos_regime": sum(1 for m in reg if m["ger"] < 0), "pior_mes_regime": min(m["ger"] for m in reg),
        "ocupacao_media": ocup_media, "margem_operacional": margem_op, "regua_margem": regua, "selo_p6": selo_p6,
        "equilibrio_contribuicao_noite": contrib, "equilibrio_noites": eq_noites, "equilibrio_ocupacao": eq_ocup, "equilibrio_folga": folga,
        "capex": capex, "deficit_rampa": deficit, "sazonalidade_giro": saz, "giro_a": giroA, "giro_b": giroB, "giro": giro, "captacao": captacao,
        "retorno_anual": R["ger"] / capex, "retorno_ebitda": R["ebitda"] / capex,
        "payback_simples": pb, "payback_descontado": payback_desc(f, taxa), "valor_saida": saida, "vpl_sem": vs, "vpl_com": vc,
        "tir_sem": tir(f), "tir_com": tir(fc), "tir_com_varias": trocas(fc) > 1,
        "mes_abertura_projeto": mes_proj, "curva_menor": cv["menor"], "curva_mes_menor": cv["mesMenor"], "curva_final": cv["final"], "colchao": col,
        "atraso_menor": cv2["menor"], "estresse_receita_menor": R["ger"] - 0.3 * R["bruta"], "estresse_capex_maior": capex * 1.25,
        "estresse_vpl_capex_maior": vpl(fm, taxa), "estresse_payback_capex_maior": payback_simples(fm, R["ger"]),
        "conservador": cen["conservador"], "otimista": cen["otimista"], "sensibilidade": sens, "passos": passos, "decisao": decisao,
        "outras_pct": outras_pct(c),
    }

saida = {"_gerado_por": "composicao_05f_referencia.py", "conferencias": {}, "cenarios": {}}
for c in ENT["cenarios"]:
    s = c["sazonalidade"]
    if s:
        pond = sum(DIAS[m] * s["ocupacao"][t] for m, t in enumerate(temporadas(c))) / 365
        dias_t = {t: sum(DIAS[m] for m, x in enumerate(temporadas(c)) if x == t) for t in ("alta", "media", "baixa")}
        saida["conferencias"][c["id"]] = {"ocupacao_ponderada": pond, "dias_por_temporada": dias_t,
                                          "media_aritmetica_simples_12_meses": sum(s["ocupacao"][t] for t in temporadas(c)) / 12,
                                          "ocupacao_por_mes": dict(zip(MESES, [s["ocupacao"][t] for t in temporadas(c)]))}
    saida["cenarios"][c["id"]] = {"R2_zaios": estudo(c, "bruta", "zaios", "pct"), "R1_comando": estudo(c, "hospedagem", "informado", "anual")}
(AQUI / "esperados_05f.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1))
for k, v in saida["cenarios"].items():
    a, b = v["R2_zaios"], v["R1_comando"]
    print(k, "bruta %.2f ebitda R2 %.2f R1 %.2f giro %.2f captR2 %.2f vpl %.2f pb %s tir %s decisao %s selo %s regua %s" % (a["receita_bruta"], a["ebitda"], b["ebitda"], a["giro"], a["captacao"], a["vpl_sem"], a["payback_simples"], a["tir_sem"], a["decisao"], a["selo_p6"], a["regua_margem"]))
print(saida["conferencias"])
