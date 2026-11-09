"""Comando 05G-A · Esperados independentes dos testes de aceite das decisões O8 a O14.

Especificação: decisões aprovadas pelo Bruno (docs/academy/comando-05g-a/DECISOES_APROVADAS_O8_O14.md).
Não importa nem executa código da ZAIOS. Reaproveita o modelo independente do 05F
(independente/composicao_05f_referencia.py), escrito a partir do texto do Dicionário v0.4 e do FORMULAS.md.
Onde a decisão depende de uma escolha ainda não aprovada (prazo do giro, convenção de desconto mensal),
o esperado é marcado como CONDICIONAL e a premissa fica explícita.
Saída: esperados_aceite_05g.json (ao lado).
"""
import json, pathlib, importlib.util, io, contextlib
AQUI = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ref05f", AQUI.parent / "independente" / "composicao_05f_referencia.py")
with contextlib.redirect_stdout(io.StringIO()):
    M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
CEN = {c["id"]: c for c in M.ENT["cenarios"]}
DIAS = M.DIAS

def curva_longa(c, base="bruta", meses=120, atraso=0, giro=None):
    """Saldo mês a mês no horizonte total (decisão O10: 10 anos), mesma convenção da curva atual estendida."""
    e = M.estudo(c, base)
    abertura = (M.MESES.index(c["mes_abertura"]) + atraso) % 12
    reg = M.regime(c, base, "pct"); pri = M.primeiro_ano(c, base, abertura)
    linhas = {k: c["investimento"] * v for k, v in M.COM["linhas_capex_proporcao"].items()}
    crono = M.cronograma(linhas)
    mes_proj = max(i + 1 for i, v in enumerate(crono) if v > 0) + 1 + atraso
    ger = [m["ger"] for m in pri] + [reg[(abertura + k) % 12]["ger"] for k in range(12, meses)]
    cap = e["capex"] + (e["giro"] if giro is None else giro)
    saldo, pts = 0.0, []
    for mes in range(1, meses + 1):
        if mes == 1: saldo += cap
        if mes <= len(crono): saldo -= crono[mes - 1]
        k = mes - mes_proj
        if 0 <= k < len(ger): saldo += ger[k]
        pts.append(saldo)
    neg = [i + 1 for i, s in enumerate(pts) if s < 0]
    return {"saldo_mes36": pts[35], "menor_36": min(pts[:36]), "menor_120": min(pts), "mes_menor_120": pts.index(min(pts)) + 1,
            "primeiro_mes_negativo": neg[0] if neg else None, "ano_primeiro_negativo": (neg[0] - 1) // 12 + 1 if neg else None,
            "capital_adicional_necessario": max(0.0, -min(pts)), "saldo_final_120": pts[-1],
            "saldos_anuais_fim_de_ano": [pts[12 * a - 1] for a in range(1, meses // 12 + 1)]}

X = {"_gerado_por": "aceite_05g_referencia.py", "testes": {}}
T = X["testes"]
c1, c2, c3, c3e = CEN["C1"], CEN["C2"], CEN["C3"], CEN["C3E"]
e1, e2, e3 = M.estudo(c1), M.estudo(c2), M.estudo(c3)

# ---------- O8 · avaliação preliminar do P6 (regras de estado; sem valor numérico novo) ----------
T["O8-1"] = {"descricao": "P6 nunca apresenta selo de aprovação definitiva", "entrada": "C2 (margem operacional 59,06%)",
             "esperado": {"selo_p6_permitido": ["Indicação preliminar"], "selos_proibidos_no_p6": ["Avançar", "Ajustar", "Redesenhar", "Aprovado", "Viável"],
                          "texto_obrigatorio": "indicação inicial, subordinada à análise financeira completa"}}
T["O8-2"] = {"descricao": "Contradição entre P6 e viabilidade é explicitada", "entrada": "C3E",
             "esperado": {"indicacao_p6": "positiva (margem operacional 45,40%)", "decisao_viabilidade": M.estudo(c3e)["decisao"],
                          "conflito_sinalizado": True, "prevalece": "análise financeira completa"}}
T["O8-3"] = {"descricao": "Margem antes e depois dos custos do modelo aparecem com nomes distintos", "entrada": "C1",
             "esperado": {"margem_operacional_antes_custos_modelo": e1["margem_operacional"], "margem_ebitda": e1["ebitda"] / e1["receita_bruta"]}}

# ---------- O9 · valor de saída = MAX(0, EBITDA × múltiplo) ----------
def saida_o9(e): return max(0.0, 6 * e["ebitda"])
def vpl_com_o9(c):
    e = M.estudo(c); f = [-e["capex"], e["geracao_ano1"]] + [e["geracao_regime"]] * 9
    return M.vpl(f[:-1] + [f[-1] + saida_o9(e)], 0.10), M.tir(f[:-1] + [f[-1] + saida_o9(e)])
v1, t1 = vpl_com_o9(c1); v2, t2 = vpl_com_o9(c2)
T["O9-1"] = {"descricao": "EBITDA negativo não gera valor de saída negativo", "entrada": "C1 (EBITDA −15.419,63)",
             "esperado": {"valor_saida": 0.0, "vpl_com_saida": v1, "vpl_sem_saida": e1["vpl_sem"], "vpl_com_igual_sem": True, "tir_com_saida": t1},
             "atual_05f": {"valor_saida": e1["valor_saida"], "vpl_com_saida": e1["vpl_com"]}}
T["O9-2"] = {"descricao": "EBITDA positivo: valor de saída inalterado", "entrada": "C2", "esperado": {"valor_saida": saida_o9(e2), "vpl_com_saida": v2, "tir_com_saida": t2}}
T["O9-3"] = {"descricao": "Borda: EBITDA = 0 gera saída 0", "entrada": "EBITDA 0, múltiplo 6", "esperado": {"valor_saida": 0.0}}

# ---------- O10 · horizonte de 10 anos (36 meses mensais + anos 4 a 10) ----------
L1 = curva_longa(c1)
T["O10-1"] = {"descricao": "Necessidade de caixa depois do mês 36 aparece na análise (36 primeiros meses positivos)", "entrada": "C1 com o giro calculado pela regra atual",
              "esperado": L1, "verificacao": "menor_36 > 0 e primeiro_mes_negativo > 36"}
base2, atr2 = curva_longa(c2), curva_longa(c2, atraso=6)
T["O10-2"] = {"descricao": "Atraso de 6 meses não pode parecer melhorar o projeto", "entrada": "C2 com e sem atraso (horizonte fixo de 120 meses do calendário do projeto)",
              "esperado": {"saldo_final_120_base": base2["saldo_final_120"], "saldo_final_120_atraso": atr2["saldo_final_120"],
                           "perda_de_caixa_no_horizonte": base2["saldo_final_120"] - atr2["saldo_final_120"],
                           "menor_36_base": base2["menor_36"], "menor_36_atraso": atr2["menor_36"],
                           "regra": "o relatório mostra o efeito do atraso sobre receitas, despesas, investimento, financiamento e valor presente; o saldo final em 10 anos com atraso é menor"},
              "condicional": "convenção de desconto mensal do atraso ainda não aprovada (ver PENDENCIAS_METODOLOGICAS.md, P-O10)"}
T["O10-3"] = {"descricao": "Saldos de fim de ano 1 a 10 (visão anual)", "entrada": "C2", "esperado": base2["saldos_anuais_fim_de_ano"]}

# ---------- O11 · bases configuráveis e independentes ----------
R2c = M.soma(M.regime(c2, "bruta", "pct"))
hosp, bruta, op, alug = R2c["hosp"], R2c["bruta"], R2c["op"], 12 * c2["aluguel_mensal"]
combos = {}
for bg in ("hospedagem", "bruta"):
    for br_ in ("hospedagem", "bruta"):
        g = c2["gestao_pct"] * (hosp if bg == "hospedagem" else bruta); r = c2["royalty_pct"] * (hosp if br_ == "hospedagem" else bruta)
        combos[f"gestao_{bg}__royalty_{br_}"] = {"gestao": g, "royalty": r, "custos_modelo": alug + g + r, "ebitda": op - alug - g - r}
T["O11-1"] = {"descricao": "Gestão e royalties com bases diferentes e independentes", "entrada": "C2 (hospedagem 1.168.584; bruta 1.348.584)", "esperado": combos,
              "verificacao": "diferença entre combinações = percentual × outras receitas (180.000); nenhuma dupla incidência"}
T["O11-2"] = {"descricao": "Sem base contratual definida: premissa marcada como hipótese", "esperado": {"rotulo": "hipótese", "base_exibida": True, "percentual_exibido": True}}

# ---------- O12 · base do capital de giro com aluguel uma vez ----------
def base_giro(c): return c["fixo_mensal"] + c["aluguel_mensal"]
T["O12-1"] = {"descricao": "Aluguel entra na base mensal do capital de giro uma única vez", "esperado": {"C1": base_giro(c1), "C2": base_giro(c2), "C3": base_giro(c3)},
              "atual_05f": {"C1": c1["fixo_mensal"], "C2": c2["fixo_mensal"], "C3": c3["fixo_mensal"]}}
T["O12-2"] = {"descricao": "Giro B com a base nova (déficit e sazonalidade já incluem o aluguel pela geração; o componente de meses fixos usa a base com aluguel)", "entrada": "C1",
              "esperado": {"giro_b": e1["deficit_rampa"] + e1["sazonalidade_giro"] + 3 * base_giro(c1)},
              "condicional": "mantém 3 meses só para conferência; o prazo não está aprovado (O12 não aprova 6 meses universais)"}
T["O12-3"] = {"descricao": "Sem duplicidade: aluguel digitado também dentro do custo fixo deve gerar alerta, não soma dupla", "esperado": {"alerta_duplicidade": True}}

# ---------- O13 · necessário x disponível ----------
def o13(e, disp):
    nec = e["giro"]; dif = disp - nec
    return {"necessario": nec, "disponivel": disp, "diferenca": dif, "deficit": max(0.0, -dif), "excedente": max(0.0, dif),
            "usos_totais": e["capex"] + nec, "fontes_do_empreendedor_para_giro": min(disp, nec), "captacao_adicional_para_giro": max(0.0, -dif)}
T["O13-1"] = {"descricao": "Disponível menor que o necessário gera déficit e necessidade de captação, sem duplicidade", "entrada": "C1, disponível 45.000", "esperado": o13(e1, 45000)}
T["O13-2"] = {"descricao": "Déficit em C2 e C3", "esperado": {"C2": o13(e2, 120000), "C3": o13(e3, 420000)}}
T["O13-3"] = {"descricao": "Excedente", "entrada": "C2, disponível 200.000", "esperado": o13(e2, 200000)}
T["O13-4"] = {"descricao": "Disponível não substitui o necessário na curva de caixa", "entrada": "C1",
              "esperado": {"curva_com_necessario_menor_36": L1["menor_36"], "curva_com_disponivel_menor_36": curva_longa(c1, giro=45000)["menor_36"],
                           "regra": "a curva técnica usa o necessário; o disponível aparece como fonte e o déficit como captação adicional"}}

# ---------- O14 · categorias de receitas complementares ----------
HIP = {"A_por_noite": 40.0, "B_ticket_por_estadia": 250.0, "B_taxa_adesao": 0.35, "C_fixa_anual": 480000.0,
       "custo_A": 0.40, "custo_B": 0.50, "custo_C": 0.30}
def compl(c):
    R = M.soma(M.regime(c, "bruta", "pct"))
    n, est = R["noites"], R["estadias"]
    A = HIP["A_por_noite"] * n; B = HIP["B_ticket_por_estadia"] * HIP["B_taxa_adesao"] * est; C = HIP["C_fixa_anual"]
    tot = A + B + C; custos = A * HIP["custo_A"] + B * HIP["custo_B"] + C * HIP["custo_C"]
    trib = (R["hosp"] + tot) * c["tributos_pct"]
    return {"noites": n, "estadias": est, "hospedagem": R["hosp"], "A": A, "B": B, "C": C, "complementares": tot,
            "receita_bruta": R["hosp"] + tot, "tributos": trib, "custos_complementares": custos}
a3, a3e = compl(c3), compl(c3e)
T["O14-1"] = {"descricao": "Receita independente da ocupação não cai quando a ocupação cai", "entrada": "C3 → C3E (hipóteses de teste: A R$ 40/noite; B R$ 250 × 35% das estadias; C R$ 480.000/ano)",
              "hipoteses": HIP, "esperado": {"C3": a3, "C3E": a3e, "C_inalterada": a3["C"] == a3e["C"],
                                             "A_variacao": a3e["A"] / a3["A"] - 1, "B_variacao": a3e["B"] / a3["B"] - 1}}
T["O14-2"] = {"descricao": "Sem duplicidade: a receita de hospedagem não muda ao incluir complementares", "esperado": {"hospedagem_C3": a3["hospedagem"]}}

# ---------- Integração das sete decisões ----------
c1i = json.loads(json.dumps(c1))
e1i = M.estudo(c1i, "hospedagem")
gestao = c1["gestao_pct"] * e1i["receita_hospedagem"]; roy = c1["royalty_pct"] * e1i["receita_bruta"]
T["INT-1"] = {"descricao": "Integração no C1: gestão sobre hospedagem, royalty sobre bruta (iguais em C1, sem complementares), saída MAX(0), giro necessário x disponível, horizonte de 10 anos",
              "esperado": {"ebitda": e1i["ebitda"], "valor_saida": max(0.0, 6 * e1i["ebitda"]), "o13": o13(e1, 45000),
                           "horizonte": {"primeiro_mes_negativo": L1["primeiro_mes_negativo"], "capital_adicional_necessario": L1["capital_adicional_necessario"]},
                           "p6": "indicação preliminar, conflito sinalizado com a decisão Redesenhar"},
              "condicional": "base do giro com aluguel (O12) muda o necessário; prazo não aprovado"}
(AQUI / "esperados_aceite_05g.json").write_text(json.dumps(X, ensure_ascii=False, indent=1))
for k, v in T.items(): print(k, json.dumps(v.get("esperado"), ensure_ascii=False)[:260])
