#!/usr/bin/env python3
"""Teste do modelo: recalcula no LibreOffice e compara com conta independente (Python).
Usa DADOS FICTÍCIOS só para exercitar as fórmulas. Uso: python3 -I test_modelo.py"""
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
print("\nRESULTADO:", "TODOS OS TESTES PASSARAM" if fails == 0 else "%d FALHA(S)" % fails)
shutil.rmtree(tmp); shutil.rmtree(out)
sys.exit(1 if fails else 0)
