#!/usr/bin/env python3
"""Conciliacao ClickMax x gateway x Meta (compras pagas).

Entradas (CSV, modelos em MODELO_*.csv, dados FICTICIOS):
  --clickmax  order_id,paid_at,value_brl,status,is_test,utm_campaign,utm_content,ad_id,campaign_id,adset_id
  --gateway   order_id,paid_at,value_brl,status,payment_method
  --meta      date,campaign_id,campaign_name,purchases,purchase_value_brl

Regras (criterio R7):
- Base de compras = vendas do ClickMax com status paid ou refunded (foram pagas), sem is_test=1.
  Pendente, Pix gerado, falha e teste ficam FORA.
- Diferenca % = (Meta - ClickMax) / ClickMax. Tolerancia: |diferenca| <= 10%.
- ClickMax = 0 e Meta = 0 -> OK. ClickMax = 0 e Meta > 0 -> ALERTA.
- Menos de 10 compras na base: marca 'amostra pequena' e exige explicacao venda a venda.
- Compras do ClickMax SEM campaign_id nao entram na comparacao por campanha: ficam em 'sem atribuicao'
  (nunca se atribui a anuncio sem dado).
- Datas precisam estar no mesmo fuso nas tres fontes (informe qual fuso foi usado no relatorio).
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


def fmt_pct(v):
    return "n/d" if v is None else f"{v:+.1f}%"


def report(cm, gw, me, out=print):
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
    return res


def has_alert(res):
    if "gateway" in res and res["gateway"]["veredito"] == "ALERTA":
        return True
    if "gateway" in res and res["gateway"]["divergencias"]:
        return True
    if "meta_total" in res and res["meta_total"]["veredito"] == "ALERTA":
        return True
    return any(d["veredito"] == "ALERTA" for d in res.get("meta_por_dia", []))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clickmax", required=True)
    ap.add_argument("--gateway")
    ap.add_argument("--meta")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    res = report(read(a.clickmax), read(a.gateway) if a.gateway else None, read(a.meta) if a.meta else None)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
    return 1 if has_alert(res) else 0


if __name__ == "__main__":
    sys.exit(main())
