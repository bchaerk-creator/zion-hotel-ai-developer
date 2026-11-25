#!/usr/bin/env python3
"""Teste do modelo: recalcula no LibreOffice e compara com conta independente (Python).
Usa DADOS FICTÍCIOS só para exercitar as fórmulas. Uso: python3 -I test_modelo.py
Testes 1 a 5: modelo v1. Testes 6 e 7: aba Funil P0 do v2 (em branco e com dados fictícios)."""
import os, subprocess, tempfile, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openpyxl import load_workbook
import build_modelo as bm

def recalc(path, outdir):
    subprocess.run(["soffice", "--headless", "--convert-to", "xlsx", "--outdir", outdir, path], check=True, capture_output=True, timeout=180)
    return load_workbook(os.path.join(outdir, os.path.basename(path)), data_only=True)

def val(wb, ref):
    sh, cell = ref.split("!"); return wb[sh.strip("'")][cell.replace("$", "")].value

fails = 0
def chk(name, got, exp, tol=1e-6):
    global fails
    ok = (got == exp) if isinstance(exp, str) else (isinstance(got, (int, float)) and abs(got - exp) <= tol)
    print(("OK   " if ok else "FALHA"), name, "| planilha:", got, "| independente:", exp)
    if not ok: fails += 1

tmp = tempfile.mkdtemp(); out = tempfile.mkdtemp()
# ---------- Teste 1: estado em branco (como será entregue)
p1 = os.path.join(tmp, "blank.xlsx"); C = bm.build(p1); wb = recalc(p1, out)
print("== Teste 1: modelo em branco (valores padrão) ==")
chk("líquido Pix R$47", val(wb, C["liq_pix"]), 47 - 2.49)
chk("conferência com referência", val(wb, C["chk_ref"]), "OK: bate com R$ 44,51")
chk("CPA máximo = líquido", val(wb, C["mm_cpamax"]), 44.51)
chk("ROAS equilíbrio", val(wb, C["mm_roasbe"]), 47 / 44.51)
chk("CPA projetado sem dado", val(wb, C["mm_cpaproj"]), "indisponível")
chk("decisão sem dado", val(wb, C["mm_decisao"]), "SEM DECISÃO: falta custo por checkout efetivo e conversão real")
chk("vendas/dia equilíbrio teto 60", val(wb, C["mm_pe_dia"]), 60 / 44.51)
chk("capital de giro sem prazo", val(wb, C["mm_cg"]), "indisponível")
chk("LTV conservador", val(wb, C["mm_ltv"]), 44.51)
# ---------- Teste 2: dados FICTÍCIOS
inp = dict(imposto=0.04, custos_var=1.5, reemb=0.03, mix_pix=0.8, cx_fixa=2.49, cx_pct=0.0499, margem_alvo=0.30,
           cpchk=3.0, conv_chk=0.08, cpc=0.9, cplpv=1.2, prazo_pix=1, prazo_cartao=30, obs_chk=200, obs_vendas=16, p2=0.1, mc2=20)
p2 = os.path.join(tmp, "fict.xlsx"); C = bm.build(p2, inp)
# conciliação fictícia
wbx = load_workbook(p2); wk = wbx["Conciliação"]
rows = [(1, "Camp teste A", 120.0, 4, 3, 188.0, 170.0), (2, "Camp teste B", 60.0, 0, 0, 0, 0)]
for i, (d, nm, g, v, vt, rb, lq) in enumerate(rows, start=C["con_first"]):
    for col, x in zip(range(1, 8), (d, nm, g, v, vt, rb, lq)): wk.cell(row=i, column=col, value=x)
wbx.save(p2)
wb = recalc(p2, out)
print("== Teste 2: dados fictícios ==")
P, tx, pct = 47.0, 2.49, 0.0
liq_pix = P - tx - pct * P; liq_c = P - 2.49 - 0.0499 * P
liq = 0.8 * liq_pix + 0.2 * liq_c
res = 0.03 * liq; mc = liq - 0.04 * P - 1.5 - res
des = mc * 0.7
chk("líquido médio", val(wb, C["liq_medio"]), liq)
chk("margem de contribuição", val(wb, C["mm_mc"]), mc)
chk("CPA máximo", val(wb, C["mm_cpamax"]), mc)
chk("CPA desejado", val(wb, C["mm_cpades"]), des)
chk("ROAS equilíbrio", val(wb, C["mm_roasbe"]), P / mc)
chk("ROAS alvo", val(wb, C["mm_roasalvo"]), P / des)
cpa = 3.0 / 0.08
chk("CPA projetado", val(wb, C["mm_cpaproj"]), cpa)
chk("custo máx por checkout (desejado)", val(wb, C["mm_maxchk"]), des * 0.08)
chk("custo máx por checkout (equilíbrio)", val(wb, C["mm_maxchk_be"]), mc * 0.08)
chk("vendas/dia equilíbrio", val(wb, C["mm_pe_dia"]), 60 / mc)
chk("vendas/dia margem alvo", val(wb, C["mm_pe_alvo"]), 60 / des)
chk("checkouts/dia", val(wb, C["mm_chk_dia"]), 60 / 3.0)
chk("vendas/dia projetadas", val(wb, C["mm_vend_dia"]), 60 / 3.0 * 0.08)
chk("resultado diário projetado", val(wb, C["mm_res_dia"]), 60 / 3.0 * 0.08 * mc - 60)
chk("capital de giro", val(wb, C["mm_cg"]), 60 * (0.8 * 1 + 0.2 * 30))
chk("LTV cenário (rotulado)", val(wb, C["mm_ltv2"]), mc + 0.1 * 20)
exp_dec = "PAUSAR (com aprovado de Bruno)" if cpa > mc else ("MANTER" if cpa > des else "ESCALAR (com aprovado de Bruno)")
chk("decisão (CPA proj. %.2f; máx %.2f)" % (cpa, mc), val(wb, C["mm_decisao"]), exp_dec)
# faixa: troca de conversão para cair em MANTER e ESCALAR
for cv, label in ((0.15, "ESCALAR"), (0.0, None)):
    pass
# Outros produtos (conta independente)
wo = wb["Outros produtos"]
fx = 2.49; pa = 0.0699
for r in range(C["out_first"], C["out_last"] + 1):
    pr = wo.cell(row=r, column=4).value; rg = wo.cell(row=r, column=5).value
    l = pr - fx if rg == 1 else pr - fx - pa * pr
    cp = l - 0.04 * pr - 1.5 - 0.03 * l
    cons = (pr - fx - pa * pr); cons = cons - 0.04 * pr - 1.5 - 0.03 * cons
    chk("CPA máx produto R$%g regra %d" % (pr, rg), wo.cell(row=r, column=10).value, cp)
    chk("  ROAS BE conservador R$%g" % pr, wo.cell(row=r, column=14).value, pr / cons if cons > 0 else "indisponível")
# ranking: maior CPA máximo = 1
vals = [wo.cell(row=r, column=10).value for r in range(C["out_first"], C["out_last"] + 1)]
for r in range(C["out_first"], C["out_last"] + 1):
    v = wo.cell(row=r, column=10).value
    chk("ranking linha %d" % r, wo.cell(row=r, column=17).value, 1 + sum(1 for x in vals if x > v + 1e-12))
# Cenários: matriz
wc = wb["Cenários"]
for i, ck in enumerate([2, 4, 6, 8, 10, 15]):
    for j, cv in enumerate([0.03, 0.05, 0.08, 0.12, 0.20]):
        v = ck / cv; exp = "E" if v <= des else ("M" if v <= mc else "P")
        chk("matriz %g/%g" % (ck, cv), wc.cell(row=15 + i, column=2 + j).value, exp)
        chk("  CPA %g/%g" % (ck, cv), wc.cell(row=6 + i, column=2 + j).value, v)
# cenário C conservador
liqC = 0.7 * (47 - 2.49 - 0.0699 * 47) + 0.3 * (47 - 2.49 - 0.0699 * 47)
cpaC = liqC - 0.06 * 47 - 1.0 - 0.05 * liqC
chk("cenário C CPA máximo", wc.cell(row=C["cen_cpa_row"], column=4).value, cpaC)
liqA = 47 - 2.49; cpaA = liqA - 0.04 * 47 - 1.5 - 0.03 * liqA
chk("cenário A CPA máximo (herda imposto/custo/reembolso dos Parâmetros)", wc.cell(row=C["cen_cpa_row"], column=2).value, cpaA)
chk("capital de giro cenário 30 dias", wc.cell(row=C["cen_cg_row"] + 4, column=2).value, 1800)
# Conciliação
wk = wb["Conciliação"]; f0 = C["con_first"]
chk("conc. CPA real A", wk.cell(row=f0, column=9).value, 120 / 4)
chk("conc. ROAS A", wk.cell(row=f0, column=10).value, 188 / 120)
chk("conc. resultado de mídia A", wk.cell(row=f0, column=11).value, 170 - 120)
chk("conc. divergência A", wk.cell(row=f0, column=8).value, 1)
chk("conc. CPA A vs máx", wk.cell(row=f0, column=12).value, "dentro do máximo" if 30 <= mc else "acima do máximo")
chk("conc. linha B sem venda", wk.cell(row=f0 + 1, column=9).value, "sem venda")
t = C["con_total"]
chk("conc. total gasto", wk.cell(row=t, column=3).value, 180)
chk("conc. total CPA", wk.cell(row=t, column=9).value, 180 / 4)
chk("conc. total resultado", wk.cell(row=t, column=11).value, 170 - 180)
# ---------- Teste 3: amostra pequena
inp3 = dict(inp, obs_chk=20, obs_vendas=1)
p3 = os.path.join(tmp, "small.xlsx"); C3 = bm.build(p3, inp3); wb3 = recalc(p3, out)
chk("amostra pequena", val(wb3, C3["mm_decisao"]), "AMOSTRA PEQUENA: manter o teto e coletar dados")
# ---------- Teste 4: faixas ESCALAR e MANTER
for cvv, exp in ((0.40, "ESCALAR (com aprovado de Bruno)"), ):
    p4 = os.path.join(tmp, "esc.xlsx"); C4 = bm.build(p4, dict(inp, conv_chk=cvv)); wb4 = recalc(p4, out)
    chk("faixa escalar (CPA %.2f)" % (3 / cvv), val(wb4, C4["mm_decisao"]), exp)
cv_m = 3.0 / ((des + mc) / 2)
p5 = os.path.join(tmp, "man.xlsx"); C5 = bm.build(p5, dict(inp, conv_chk=cv_m)); wb5 = recalc(p5, out)
chk("faixa manter", val(wb5, C5["mm_decisao"]), "MANTER")

# ---------- Teste 6 (P0): aba Funil P0, v2 (em branco, depois dados FICTÍCIOS)
print("== Teste 6: aba Funil P0 (v2) em branco ==")
IND = "indisponível"
pv = os.path.join(tmp, "v2blank.xlsx"); CV = bm.build(pv, p0=True); wbv = recalc(pv, out)
wf = wbv["Funil P0"]
chk_v1 = "Funil P0" not in load_workbook(p1).sheetnames
print(("OK   " if chk_v1 else "FALHA"), "v1 (build sem p0) não ganhou a aba Funil P0"); fails += 0 if chk_v1 else 1
for nm in ("f_cpv", "f_conv_land", "f_cp_chk", "f_cp_cliqueq", "f_conv_chk", "f_cpa", "f_pix_pago", "f_reemb_taxa", "f_rec_bruta", "f_rec_liq", "f_mc_real",
           "f_res_midia", "f_roas_bruto", "f_roas_liq", "f_pe_vendas", "f_cpv_max", "f_p_cpa", "f_p_roas", "f_p_res", "f_p_faixa", "f_cpa_vs"):
    chk("em branco: %s" % nm, val(wbv, CV[nm]), IND)
chk("em branco: referência CPA máximo = 44,51", val(wbv, CV["f_cpamax"]), 44.51)
chk("em branco: sinalização do criativo 1", wf["B%d" % CV["f_cr_sinal"]].value, IND)
chk("em branco: vencedor", wf["B%d" % CV["f_cr_venc"]].value, "—")
for k in range(1, 8):
    cell = wf["C%d" % CV["f_stage_row_%d" % k]]
    assert cell.value is None, "entrada do funil deveria estar vazia"
print("OK   entradas de dados reais do funil estão VAZIAS (7 etapas)")

print("== Teste 7: aba Funil P0 com dados FICTÍCIOS ==")
fi = dict(inp, v_land=2000, v_oferta=1100, v_cta=260, v_chk=100, v_pix=70, v_aprov=30, v_entr=29, gasto=600.0, cliques=3100, pix_pagos=28, reemb_n=3,
          gasto_plan=500.0, cpv_plan=0.5, t1=0.55, t2=0.25, t3=0.4, t4=0.7, t5=0.4, t6=0.95,
          cr1_nome="criativo-1", cr1_gasto=200.0, cr1_visitas=800, cr1_cliq=120, cr1_chk=70, cr1_vend=3, cr1_reemb=0,
          cr2_nome="criativo-2", cr2_gasto=220.0, cr2_visitas=700, cr2_cliq=60, cr2_chk=30, cr2_vend=9, cr2_reemb=1,
          cr3_nome="criativo-3", cr3_gasto=180.0, cr3_visitas=500, cr3_cliq=40, cr3_chk=20, cr3_vend=2, cr3_reemb=0)
pw = os.path.join(tmp, "v2fict.xlsx"); CW = bm.build(pw, fi, p0=True); wbw = recalc(pw, out); wf = wbw["Funil P0"]
# conta independente
P = 47.0; liq_pix = P - 2.49; liq_c = P - 2.49 - 0.0499 * P; liq = 0.8 * liq_pix + 0.2 * liq_c
mc_sale = liq - 0.04 * P - 1.5 - 0.03 * liq            # margem de contribuição por venda (modelo, inclui reserva)
cpamax = mc_sale; cpades = cpamax * 0.7
land, oferta, cta, chk_, pix, aprov, entr = 2000, 1100, 260, 100, 70, 30, 29
g, cl, pixp, rb = 600.0, 3100, 28, 3
chk("taxa oferta/landing", wf["D%d" % CW["f_stage_row_2"]].value, oferta / land)
chk("taxa CTA/oferta", wf["D%d" % CW["f_stage_row_3"]].value, cta / oferta)
chk("taxa checkout/CTA", wf["D%d" % CW["f_stage_row_4"]].value, chk_ / cta)
chk("taxa Pix/checkout", wf["D%d" % CW["f_stage_row_5"]].value, pix / chk_)
chk("taxa aprovado/Pix", wf["D%d" % CW["f_stage_row_6"]].value, aprov / pix)
chk("taxa entrega/aprovado", wf["D%d" % CW["f_stage_row_7"]].value, entr / aprov)
chk("aprovado vs visitas", wf["E%d" % CW["f_stage_row_6"]].value, aprov / land)
chk("custo por visita", val(wbw, CW["f_cpv"]), g / land)
chk("custo por clique no link", val(wbw, CW["f_cpc_link"]), g / cl)
chk("conversão da landing", val(wbw, CW["f_conv_land"]), cta / land)
chk("custo por clique qualificado", val(wbw, CW["f_cp_cliqueq"]), g / cta)
chk("custo por checkout efetivo", val(wbw, CW["f_cp_chk"]), g / chk_)
chk("conversão checkout → aprovado", val(wbw, CW["f_conv_chk"]), aprov / chk_)
chk("CPA", val(wbw, CW["f_cpa"]), g / aprov)
chk("visita → compra", val(wbw, CW["f_vis_compra"]), aprov / land)
chk("Pix gerado → pago", val(wbw, CW["f_pix_pago"]), pixp / pix)
chk("taxa de reembolso", val(wbw, CW["f_reemb_taxa"]), rb / aprov)
chk("receita bruta", val(wbw, CW["f_rec_bruta"]), aprov * P)
chk("receita líquida", val(wbw, CW["f_rec_liq"]), (aprov - rb) * liq)
mcr = (aprov - rb) * (liq - 0.04 * P - 1.5)
chk("margem de contribuição realizada", val(wbw, CW["f_mc_real"]), mcr)
chk("margem de contribuição %", val(wbw, CW["f_mc_pct"]), mcr / ((aprov - rb) * P))
chk("resultado de mídia", val(wbw, CW["f_res_midia"]), mcr - g)
chk("ROAS bruto", val(wbw, CW["f_roas_bruto"]), aprov * P / g)
chk("ROAS líquido", val(wbw, CW["f_roas_liq"]), (aprov - rb) * liq / g)
chk("ROAS de equilíbrio (modelo)", val(wbw, CW["f_roas_be"]), P / cpamax)
cpa_o = g / aprov
chk("CPA × referências", val(wbw, CW["f_cpa_vs"]), "abaixo do CPA desejado" if cpa_o <= cpades else ("entre o desejado e o máximo" if cpa_o <= cpamax else "acima do CPA máximo"))
pev = g / cpamax
chk("vendas de equilíbrio", val(wbw, CW["f_pe_vendas"]), pev)
chk("visitas de equilíbrio", val(wbw, CW["f_pe_visitas"]), pev / (aprov / land))
chk("custo máx. por visita", val(wbw, CW["f_cpv_max"]), cpamax * aprov / land)
chk("custo máx. por clique qualificado", val(wbw, CW["f_cpq_max"]), cpamax * aprov / cta)
chk("custo máx. por checkout efetivo", val(wbw, CW["f_cpchk_max"]), cpamax * aprov / chk_)
# projeção
gp, cpvp = 500.0, 0.5; vis = gp / cpvp
st = [vis]
for t in (0.55, 0.25, 0.4, 0.7, 0.4, 0.95): st.append(st[-1] * t)
for k in range(7): chk("projetado etapa %d" % (k + 1), wf["G%d" % CW["f_stage_row_%d" % (k + 1)]].value, st[k])
chk("CPA projetado", val(wbw, CW["f_p_cpa"]), gp / st[5])
chk("custo por checkout projetado", val(wbw, CW["f_p_cpchk"]), gp / st[3])
chk("custo por clique qualificado projetado", val(wbw, CW["f_p_cpq"]), gp / st[2])
chk("ROAS projetado", val(wbw, CW["f_p_roas"]), st[5] * P / gp)
chk("margem projetada", val(wbw, CW["f_p_mc"]), st[5] * mc_sale)
chk("resultado projetado", val(wbw, CW["f_p_res"]), st[5] * mc_sale - gp)
cpap = gp / st[5]
chk("faixa projetada", val(wbw, CW["f_p_faixa"]), "abaixo do CPA desejado" if cpap <= cpades else ("entre o desejado e o máximo" if cpap <= cpamax else "acima do CPA máximo"))
# curioso x comprador
cr = [dict(g=200.0, v=800, q=120, c=70, s=3, r=0), dict(g=220.0, v=700, q=60, c=30, s=9, r=1), dict(g=180.0, v=500, q=40, c=20, s=2, r=0)]
tc, ts = sum(x["c"] for x in cr), sum(x["s"] for x in cr)
elig = [x["g"] / x["s"] if x["s"] >= 5 else None for x in cr]
mn = min(e for e in elig if e is not None)
cheap = min(x["g"] / x["c"] for x in cr)
for j, (col, x) in enumerate(zip("BCD", cr)):
    R = lambda k: wf["%s%d" % (col, CW["f_cr_" + k])].value
    chk("criativo %d custo por visita" % (j + 1), R("cpv"), x["g"] / x["v"])
    chk("criativo %d custo por clique qualificado" % (j + 1), R("cpq"), x["g"] / x["q"])
    chk("criativo %d custo por checkout" % (j + 1), R("cpchk"), x["g"] / x["c"])
    chk("criativo %d CPA" % (j + 1), R("cpa"), x["g"] / x["s"])
    chk("criativo %d conversão checkout→aprovado" % (j + 1), R("conv"), x["s"] / x["c"])
    chk("criativo %d reembolso" % (j + 1), R("rr"), x["r"] / x["s"])
    idx = (x["c"] / tc) / (x["s"] / ts)
    chk("criativo %d índice de curiosidade" % (j + 1), R("idx"), idx)
    exp_sig = "AMOSTRA PEQUENA" if x["c"] < 30 else ("CURIOSO" if idx >= 1.5 else ("COMPRADOR" if idx <= 0.67 else "MISTO"))
    chk("criativo %d sinalização" % (j + 1), R("sinal"), exp_sig)
    e = elig[j]
    chk("criativo %d vencedor por CPA" % (j + 1), R("venc"), "—" if e is None else ("MENOR CPA" if abs(e - mn) < 1e-9 else "não"))
    chk("criativo %d menor custo por checkout" % (j + 1), R("barato"), "sim" if abs(x["g"] / x["c"] - cheap) < 1e-9 else "não")
    arm = "checkout barato, mas NÃO é o menor CPA" if (abs(x["g"] / x["c"] - cheap) < 1e-9 and not (e is not None and abs(e - mn) < 1e-9)) else None
    got = R("arm")
    ok_arm = (got or None) == arm
    print(("OK   " if ok_arm else "FALHA"), "criativo %d alerta de armadilha | planilha: %r | independente: %r" % (j + 1, got, arm)); fails += 0 if ok_arm else 1

print("\nRESULTADO:", "TODOS OS TESTES PASSARAM" if fails == 0 else "%d FALHA(S)" % fails)
shutil.rmtree(tmp); shutil.rmtree(out)
sys.exit(1 if fails else 0)
