#!/usr/bin/env python3
"""Conciliacao ClickMax x gateway x Meta (compras pagas).

Entradas (CSV, modelos em MODELO_*.csv, dados FICTICIOS):
  --clickmax  order_id,paid_at,value_brl,status,is_test,utm_campaign,utm_content,ad_id,campaign_id,adset_id
  --gateway   order_id,paid_at,value_brl,status,payment_method
  --meta      date,campaign_id,campaign_name,purchases,purchase_value_brl
  --funil     date,campaign_id,landing_view,offer_view,qualified_click,checkout_effective,pix_generated,approved,delivered
              (funil de 7 eventos P0, ver ../FUNIL_DE_EVENTOS_P0.md; celula vazia = indisponivel, nunca zero)

Regras (criterio R7):
- Base de compras = vendas do ClickMax com status paid ou refunded (foram pagas), sem is_test=1.
  Pendente, Pix gerado, falha e teste ficam FORA.
- Diferenca % = (Meta - ClickMax) / ClickMax. Tolerancia: |diferenca| <= 10%.
- ClickMax = 0 e Meta = 0 -> OK. ClickMax = 0 e Meta > 0 -> ALERTA.
- Menos de 10 compras na base: marca 'amostra pequena' e exige explicacao venda a venda.
- Compras do ClickMax SEM campaign_id nao entram na comparacao por campanha: ficam em 'sem atribuicao'
  (nunca se atribui a anuncio sem dado).
- Datas precisam estar no mesmo fuso nas tres fontes (informe qual fuso foi usado no relatorio).
Funil P0 (--funil): taxas entre etapas e MOTIVO DE DIVERGENCIA quando a conta nao fecha (etapa posterior
maior que a anterior, aprovado diferente do ClickMax, entregue menor que aprovado). 'approved' do CSV e
conferido contra a base do ClickMax (mesmo dia); se vazio, usa a base do ClickMax.
Saida: tabelas no terminal; --json grava o resultado. Codigo de saida 1 se houver ALERTA.
"""
import argparse
import csv
import json
import sys
from collections import defaultdict

TOL = 0.10
SMALL = 10
PAID = {"paid", "refunded"}


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def money(v):
    return round(float(str(v or 0).replace(",", ".")), 2)


def day(ts):
    return str(ts)[:10]


def verdict(cm, other):
    if cm == 0 and other == 0:
        return 0.0, "OK"
    if cm == 0:
        return None, "ALERTA"
    diff = (other - cm) / cm
    return round(diff * 100, 1), "OK" if abs(diff) <= TOL else "ALERTA"


def clickmax_base(rows):
    return [r for r in rows if (r.get("status") or "").lower() in PAID and str(r.get("is_test") or "0") != "1"]


def reconcile_gateway(cm_rows, gw_rows):
    cm = {r["order_id"]: r for r in cm_rows if str(r.get("is_test") or "0") != "1"}
    test_ids = {r["order_id"] for r in cm_rows if str(r.get("is_test") or "0") == "1"}
    gw = {r["order_id"]: r for r in gw_rows if r["order_id"] not in test_ids}  # teste marcado no ClickMax sai dos dois lados
    issues = []
    for oid, r in cm.items():
        g = gw.get(oid)
        if g is None:
            if (r["status"] or "").lower() in PAID:
                issues.append({"order_id": oid, "problema": "paga no ClickMax e ausente no gateway"})
            continue
        if (r["status"] or "").lower() != (g["status"] or "").lower():
            issues.append({"order_id": oid, "problema": f"status diferente (ClickMax {r['status']}, gateway {g['status']})"})
        elif money(r["value_brl"]) != money(g["value_brl"]):
            issues.append({"order_id": oid, "problema": f"valor diferente (ClickMax {money(r['value_brl'])}, gateway {money(g['value_brl'])})"})
    for oid, g in gw.items():
        if oid not in cm and (g["status"] or "").lower() in PAID:
            issues.append({"order_id": oid, "problema": "paga no gateway e ausente no ClickMax"})
    base_cm = clickmax_base(list(cm.values()))
    # compara o gateway so com o que o ClickMax conhece (sem testes), para nao poluir a conta
    base_gw = [g for g in gw.values() if (g["status"] or "").lower() in PAID and g["order_id"] in cm]
    n_cm, n_gw = len(base_cm), len(base_gw)
    v_cm, v_gw = round(sum(money(r["value_brl"]) for r in base_cm), 2), round(sum(money(g["value_brl"]) for g in base_gw), 2)
    diff, ver = verdict(n_cm, n_gw)
    return {"clickmax_compras": n_cm, "gateway_compras": n_gw, "clickmax_valor": v_cm, "gateway_valor": v_gw,
            "dif_compras_pct": diff, "veredito": ver, "divergencias": issues}


def reconcile_meta_by_day(cm_rows, meta_rows):
    base = clickmax_base(cm_rows)
    cm_n, cm_v = defaultdict(int), defaultdict(float)
    for r in base:
        d = day(r["paid_at"])
        cm_n[d] += 1
        cm_v[d] += money(r["value_brl"])
    me_n, me_v = defaultdict(int), defaultdict(float)
    for r in meta_rows:
        me_n[r["date"]] += int(float(r["purchases"] or 0))
        me_v[r["date"]] += money(r["purchase_value_brl"])
    out = []
    for d in sorted(set(cm_n) | set(me_n)):
        diff, ver = verdict(cm_n[d], me_n[d])
        vdiff, _ = verdict(round(cm_v[d], 2), round(me_v[d], 2))
        out.append({"data": d, "clickmax_compras": cm_n[d], "meta_compras": me_n[d], "dif_compras_pct": diff,
                    "clickmax_valor": round(cm_v[d], 2), "meta_valor": round(me_v[d], 2), "dif_valor_pct": vdiff,
                    "veredito": ver})
    tn_cm, tn_me = sum(cm_n.values()), sum(me_n.values())
    diff, ver = verdict(tn_cm, tn_me)
    total = {"clickmax_compras": tn_cm, "meta_compras": tn_me, "dif_compras_pct": diff, "veredito": ver,
             "amostra_pequena": tn_cm < SMALL}
    return out, total


def reconcile_by_campaign(cm_rows, meta_rows):
    base = clickmax_base(cm_rows)
    with_id = [r for r in base if (r.get("campaign_id") or "").strip()]
    without = [r for r in base if not (r.get("campaign_id") or "").strip()]
    cm_n = defaultdict(int)
    for r in with_id:
        cm_n[r["campaign_id"].strip()] += 1
    me_n, names = defaultdict(int), {}
    for r in meta_rows:
        me_n[r["campaign_id"]] += int(float(r["purchases"] or 0))
        names[r["campaign_id"]] = r.get("campaign_name", "")
    out = []
    for cid in sorted(set(cm_n) | set(me_n)):
        diff, ver = verdict(cm_n[cid], me_n[cid])
        out.append({"campaign_id": cid, "campanha": names.get(cid, ""), "clickmax_compras": cm_n[cid], "meta_compras": me_n[cid],
                    "dif_pct": diff, "veredito": ver})
    return out, {"compras_sem_atribuicao": len(without), "ids": [r["order_id"] for r in without]}


FUNIL_ETAPAS = ["landing_view", "offer_view", "qualified_click", "checkout_effective", "pix_generated", "approved", "delivered"]
FUNIL_ROTULO = {"landing_view": "visita", "offer_view": "oferta", "qualified_click": "clique CTA", "checkout_effective": "checkout efetivo",
                "pix_generated": "Pix gerado", "approved": "aprovado", "delivered": "entregue"}
# (etapa, etapa anterior que ela nao pode superar, motivo se superar)
FUNIL_LIMITES = [
    ("offer_view", "landing_view", "visualizacao da oferta maior que visitas: evento da oferta dispara fora da landing ou conta mais de uma vez por visita"),
    ("qualified_click", "landing_view", "cliques no CTA maiores que visitas: clique contado em dobro ou visita sem PageView (bloqueador/consentimento)"),
    ("checkout_effective", "qualified_click", "checkout efetivo maior que cliques no CTA: checkout abre sem passar pelo CTA (link direto) ou o evento ainda conta o carregamento do iframe"),
    ("pix_generated", "checkout_effective", "Pix gerado maior que checkout efetivo: checkout efetivo subcontado (dados pessoais nao capturados) ou Pix contado em dobro"),
    ("approved", "checkout_effective", "aprovados maiores que checkout efetivo: compra sem checkout registrado (pagamento fora do site, UTM/ID perdido ou evento mal configurado)"),
]
FUNIL_TAXAS = [("offer_view", "landing_view"), ("qualified_click", "landing_view"), ("checkout_effective", "qualified_click"),
               ("approved", "checkout_effective"), ("delivered", "approved")]


def cell(v):
    """None = indisponivel (celula vazia). Zero e zero de verdade."""
    s = str(v if v is not None else "").strip()
    return None if s == "" else int(float(s.replace(",", ".")))


def rate(num, den):
    if num is None or den is None or den == 0:
        return None
    return round(num / den * 100, 1)


def funil_aggregate(funil_rows):
    """Soma por data+campanha; uma etapa so e numero se TODAS as linhas a informaram (senao n/d)."""
    groups = {}
    for r in funil_rows:
        groups.setdefault((r["date"], (r.get("campaign_id") or "").strip()), []).append(r)
    out = []
    for (d, cid), rows in sorted(groups.items()):
        rec = {"data": d, "campaign_id": cid}
        for e in FUNIL_ETAPAS:
            vals = [cell(x.get(e)) for x in rows]
            rec[e] = None if any(v is None for v in vals) else sum(vals)
        out.append(rec)
    return out


def reconcile_funil(funil_rows, cm_rows):
    base = clickmax_base(cm_rows)
    cm_by_day = defaultdict(int)
    for r in base:
        cm_by_day[day(r["paid_at"])] += 1
    lines = []
    for rec in funil_aggregate(funil_rows):
        motivos = []
        for etapa, anterior, motivo in FUNIL_LIMITES:
            if rec[etapa] is not None and rec[anterior] is not None and rec[etapa] > rec[anterior]:
                motivos.append(motivo)
        cm_n = cm_by_day.get(rec["data"], 0)
        # aprovado do funil x base ClickMax: so quando a linha e do dia inteiro (sem campaign_id) ou ha uma unica campanha no dia
        if rec["approved"] is None:
            rec["approved_fonte"] = "clickmax"
            rec["approved"] = cm_n if not rec["campaign_id"] else None
        else:
            rec["approved_fonte"] = "funil"
            if not rec["campaign_id"] and rec["approved"] != cm_n:
                motivos.append(f"aprovados do funil ({rec['approved']}) diferentes da base ClickMax ({cm_n}): fonte de evento diferente da venda (Purchase no Meta atrasado, teste nao marcado ou reembolso contado)")
        if rec["delivered"] is not None and rec["approved"] is not None:
            if rec["delivered"] < rec["approved"]:
                motivos.append(f"entregues ({rec['delivered']}) menos que aprovados ({rec['approved']}): entrega pendente ou falha de acesso, verificar compra a compra")
            elif rec["delivered"] > rec["approved"]:
                motivos.append("entregues maiores que aprovados: acesso liberado sem pagamento aprovado (teste, cortesia ou erro de regra)")
        if rec["pix_generated"] is not None and rec["approved"] is not None and rec["approved"] > 0 and rec["pix_generated"] == 0:
            motivos.append("aprovados sem nenhum Pix gerado: todas as compras foram no cartao ou o evento de Pix gerado esta desligado (padrao)")
        rec["taxas_pct"] = {f"{FUNIL_ROTULO[n]}/{FUNIL_ROTULO[d]}": rate(rec[n], rec[d]) for n, d in FUNIL_TAXAS}
        rec["indisponiveis"] = [FUNIL_ROTULO[e] for e in FUNIL_ETAPAS if rec[e] is None]
        rec["motivos_divergencia"] = motivos
        rec["veredito"] = "ALERTA" if motivos else "OK"
        lines.append(rec)
    return lines


def fmt_pct(v):
    return "n/d" if v is None else f"{v:+.1f}%"


def report(cm, gw, me, out=print, funil=None):
    res = {}
    if gw is not None:
        res["gateway"] = reconcile_gateway(cm, gw)
        g = res["gateway"]
        out("== ClickMax x gateway ==")
        out(f"compras ClickMax {g['clickmax_compras']} | gateway {g['gateway_compras']} | dif {fmt_pct(g['dif_compras_pct'])} | {g['veredito']}")
        out(f"valor ClickMax {g['clickmax_valor']:.2f} | gateway {g['gateway_valor']:.2f}")
        for i in g["divergencias"]:
            out(f"  - {i['order_id']}: {i['problema']}")
    if me is not None:
        days, total = reconcile_meta_by_day(cm, me)
        camps, sem = reconcile_by_campaign(cm, me)
        res["meta_por_dia"], res["meta_total"], res["meta_por_campanha"], res["sem_atribuicao"] = days, total, camps, sem
        out("== ClickMax x Meta, por dia ==")
        for d in days:
            out(f"{d['data']} | ClickMax {d['clickmax_compras']} | Meta {d['meta_compras']} | {fmt_pct(d['dif_compras_pct'])} | {d['veredito']}")
        note = " (amostra pequena: explique venda a venda)" if total["amostra_pequena"] else ""
        out(f"TOTAL | ClickMax {total['clickmax_compras']} | Meta {total['meta_compras']} | {fmt_pct(total['dif_compras_pct'])} | {total['veredito']}{note}")
        out("== Por campanha (so compras do ClickMax com campaign_id) ==")
        for c in camps:
            out(f"{c['campaign_id']} {c['campanha']} | ClickMax {c['clickmax_compras']} | Meta {c['meta_compras']} | {fmt_pct(c['dif_pct'])} | {c['veredito']}")
        out(f"Compras sem atribuicao (sem campaign_id no ClickMax): {sem['compras_sem_atribuicao']} {sem['ids']}")
    if funil is not None:
        res["funil"] = reconcile_funil(funil, cm)
        out("== Funil P0 (7 eventos), por dia e campanha ==")
        for f in res["funil"]:
            cols = " | ".join(f"{FUNIL_ROTULO[e]} {'n/d' if f[e] is None else f[e]}" for e in FUNIL_ETAPAS)
            out(f"{f['data']} {f['campaign_id'] or 'todas'} | {cols} | {f['veredito']}")
            out("   taxas: " + "; ".join(f"{k} {'n/d' if v is None else str(v) + '%'}" for k, v in f["taxas_pct"].items()))
            for m in f["motivos_divergencia"]:
                out(f"   motivo: {m}")
    return res


def has_alert(res):
    if "gateway" in res and res["gateway"]["veredito"] == "ALERTA":
        return True
    if "gateway" in res and res["gateway"]["divergencias"]:
        return True
    if "meta_total" in res and res["meta_total"]["veredito"] == "ALERTA":
        return True
    if any(f["veredito"] == "ALERTA" for f in res.get("funil", [])):
        return True
    return any(d["veredito"] == "ALERTA" for d in res.get("meta_por_dia", []))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clickmax", required=True)
    ap.add_argument("--gateway")
    ap.add_argument("--meta")
    ap.add_argument("--funil")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    res = report(read(a.clickmax), read(a.gateway) if a.gateway else None, read(a.meta) if a.meta else None,
                 funil=read(a.funil) if a.funil else None)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
    return 1 if has_alert(res) else 0


if __name__ == "__main__":
    sys.exit(main())
