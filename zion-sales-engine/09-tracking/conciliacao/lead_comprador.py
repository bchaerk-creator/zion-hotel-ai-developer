#!/usr/bin/env python3
"""Conciliacao LEAD x COMPRADOR (funil hibrido: quente = captacao -> formulario -> compra; frio = venda direta).

Cruza dois CSVs (leads e compras) por E-MAIL NORMALIZADO e classifica cada compra em:
  quente           lead ANTERIOR a compra (mesmo e-mail normalizado); leva origem, criativo, campanha e coorte do lead
  frio             sem lead anterior e com utm_campaign de venda fria (padrao: venda-fria)
  nao_atribuida    sem lead anterior e sem UTM de venda fria (inclui sem UTM nenhuma)

REGRA DE PRECEDENCIA (um comprador unico conta uma vez, na primeira compra valida dele):
  1. Lead anterior a compra  -> quente (evidencia identificada e datada no CRM; vence a UTM da compra).
  2. Senao, UTM de venda fria -> frio.
  3. Senao                    -> nao_atribuida. (UTM 'venda-quente' sem lead encontrado tambem fica aqui, com motivo.)
  Se o comprador e quente E a compra tem UTM de venda fria, conta como QUENTE e entra em 'sobreposicao_quente_e_frio'
  (aparece nos dois caminhos; nunca soma duas vezes no CPA global).

CORRESPONDENCIA (nunca presumida):
  - Padrao: e-mail em minusculas e sem espacos nas pontas. So igualdade exata conta.
  - Regra OPCIONAL e ROTULADA (--gmail-rules): para gmail.com/googlemail.com, remove pontos e '+tag' do usuario.
    Compradores casados SO por essa regra ficam em 'match_regra_gmail_opcional' (conferir) e entram em quente.
  - Telefone NUNCA casa sozinho: pares com e-mail diferente e telefone normalizado igual vao para
    'possiveis_correspondencias_para_revisao_humana' (so contagem na saida agregada; --revisao-out grava ids sem PII).

PRIVACIDADE: entrada com PII fica FORA do repositorio (o script recusa CSV dentro do repo). A saida e AGREGADA: nenhum
e-mail, telefone ou nome. Coortes com poucos casos vem marcadas 'amostra_pequena' (<10): nao tire conclusao delas.

Uso:
  python3 -I lead_comprador.py --leads /fora/leads.csv --compras /fora/compras.csv --as-of 2026-12-10 [--gmail-rules] [--json saida.json]
Colunas leads : email, telefone (opc.), created_at (ISO 8601), utm_source, utm_medium, utm_campaign, utm_content (opc.), lead_ref (opc., id interno)
Colunas compras: order_id, paid_at (ISO 8601), value_brl, status (paid|refunded|...), is_test (0/1), email, telefone (opc.), utm_source, utm_medium, utm_campaign, utm_content
"""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone, date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
COLD_DEFAULT = ("venda-fria",)
HOT_UTM = "venda-quente"
VALID_STATUS = ("paid", "refunded")  # foram pagas (reembolsada conta como compra e e marcada)
SMALL = 10


# ------------------------------------------------------------------ normalizacao
def norm_email(v, gmail_rules=False):
    s = (v or "").strip().lower()
    if "@" not in s:
        return None
    if gmail_rules:
        user, _, dom = s.partition("@")
        if dom in ("gmail.com", "googlemail.com"):
            user = user.split("+", 1)[0].replace(".", "")
            s = f"{user}@gmail.com"
    return s


def norm_phone(v):
    d = re.sub(r"\D+", "", v or "").lstrip("0")
    if not d:
        return None
    if len(d) in (10, 11):
        d = "55" + d
    return d if len(d) >= 11 else None


def parse_dt(v):
    s = (v or "").strip()
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def clean(v):
    return (v or "").strip()


# ------------------------------------------------------------------ nucleo
def conciliar(leads_rows, compras_rows, as_of, cold_campaigns=COLD_DEFAULT, gmail_rules=False, cohort_by="day"):
    # 1) leads: um por e-mail normalizado (o mais antigo vence). Sem e-mail valido nao entra no cruzamento.
    leads, leads_sem_email, leads_dup = {}, 0, 0
    for r in leads_rows:
        em = norm_email(r.get("email"))
        created = parse_dt(r.get("created_at"))
        if not em or not created:
            leads_sem_email += 1
            continue
        rec = {"em": em, "em_gmail": norm_email(r.get("email"), True), "ph": norm_phone(r.get("telefone")), "created": created,
               "origin": clean(r.get("utm_source")) + "/" + clean(r.get("utm_medium")),
               "campaign": clean(r.get("utm_campaign")) or "(sem campanha)",
               "content": clean(r.get("utm_content")) or "(sem criativo)"}
        if em in leads:
            leads_dup += 1
            if created < leads[em]["created"]:
                leads[em] = rec
        else:
            leads[em] = rec
    by_gmail = defaultdict(list)
    by_phone = defaultdict(list)
    for em, rec in leads.items():
        by_gmail[rec["em_gmail"]].append(em)
        if rec["ph"]:
            by_phone[rec["ph"]].append(em)

    # 2) compras validas, agrupadas por comprador unico (e-mail normalizado; sem e-mail = o proprio pedido)
    compras, descartadas = [], defaultdict(int)
    for r in compras_rows:
        st = clean(r.get("status")).lower()
        if clean(r.get("is_test")) in ("1", "true", "sim", "yes"):
            descartadas["teste"] += 1
            continue
        if st not in VALID_STATUS:
            descartadas["status_nao_pago"] += 1
            continue
        paid = parse_dt(r.get("paid_at"))
        if not paid:
            descartadas["sem_data_de_pagamento"] += 1
            continue
        compras.append({"order": clean(r.get("order_id")), "paid": paid, "status": st, "em": norm_email(r.get("email")),
                        "em_gmail": norm_email(r.get("email"), True), "ph": norm_phone(r.get("telefone")),
                        "campaign": clean(r.get("utm_campaign")), "content": clean(r.get("utm_content")),
                        "source": clean(r.get("utm_source")), "medium": clean(r.get("utm_medium"))})
    compras.sort(key=lambda c: c["paid"])
    buyers = {}
    n_compras_repetidas = 0
    for c in compras:
        key = c["em"] or ("pedido:" + c["order"])
        if key in buyers:
            buyers[key]["extra_orders"] += 1
            n_compras_repetidas += 1
            continue
        buyers[key] = {"first": c, "extra_orders": 0}

    # 3) classificacao do comprador unico
    out_rows = []
    revisao = []
    for key, b in buyers.items():
        c = b["first"]
        lead, how = None, None
        if c["em"] in leads:
            lead, how = leads[c["em"]], "email_exato"
        elif gmail_rules and c["em_gmail"] in by_gmail:
            cand = leads[by_gmail[c["em_gmail"]][0]]
            lead, how = cand, "regra_gmail_opcional"
        lead_anterior = lead is not None and lead["created"] <= c["paid"]
        lead_posterior = lead is not None and not lead_anterior
        is_cold_utm = c["campaign"].lower() in [x.lower() for x in cold_campaigns]
        reason = None
        if lead_anterior:
            cls = "quente"
        elif is_cold_utm:
            cls = "frio"
        else:
            cls = "nao_atribuida"
            if lead_posterior:
                reason = "lead_posterior_a_compra"
            elif c["campaign"].lower() == HOT_UTM:
                reason = "utm_venda_quente_sem_lead_encontrado"
            elif not c["campaign"]:
                reason = "sem_utm_e_sem_lead"
            else:
                reason = "utm_de_outra_campanha_sem_lead"
        # possiveis correspondencias por telefone (so quando NAO ha lead por e-mail)
        if lead is None and c["ph"] and c["ph"] in by_phone:
            revisao.append({"order_id": c["order"], "lead_emails_candidatos": len(by_phone[c["ph"]]), "motivo": "telefone_igual_email_diferente"})
        row = {"class": cls, "reason": reason, "how": how, "refunded": c["status"] == "refunded", "extra_orders": b["extra_orders"],
               "overlap": bool(lead_anterior and is_cold_utm)}
        if lead_anterior:
            row["days"] = round((c["paid"] - lead["created"]).total_seconds() / 86400, 2)
            row["cohort"] = cohort_key(lead["created"], cohort_by)
            row["lead_created"] = lead["created"]
            row["campaign"], row["content"], row["origin"] = lead["campaign"], lead["content"], lead["origin"]
        out_rows.append(row)

    # 4) agregados
    agg = {"entrada": {"leads_linhas": len(leads_rows), "leads_unicos_com_email": len(leads), "leads_sem_email_ou_data": leads_sem_email,
                       "leads_duplicados_por_email": leads_dup, "compras_linhas": len(compras_rows),
                       "compras_validas": len(compras), "compras_descartadas": dict(descartadas)},
           "compradores_unicos": len(buyers), "compras_repetidas_do_mesmo_comprador": n_compras_repetidas}
    for cls in ("quente", "frio", "nao_atribuida"):
        agg[cls] = sum(1 for r in out_rows if r["class"] == cls)
    agg["soma_confere"] = agg["quente"] + agg["frio"] + agg["nao_atribuida"] == agg["compradores_unicos"]
    agg["nao_atribuida_motivos"] = dict(_count(r["reason"] for r in out_rows if r["class"] == "nao_atribuida"))
    agg["sobreposicao_quente_e_frio"] = sum(1 for r in out_rows if r["overlap"])
    agg["match_regra_gmail_opcional"] = sum(1 for r in out_rows if r["how"] == "regra_gmail_opcional" and r["class"] == "quente")
    agg["regra_gmail_ativa"] = bool(gmail_rules)
    agg["reembolsados_entre_compradores"] = sum(1 for r in out_rows if r["refunded"])
    agg["possiveis_correspondencias_para_revisao_humana"] = len(revisao)
    agg["tempo_ate_a_compra_dias_quentes"] = _stats([r["days"] for r in out_rows if r["class"] == "quente"])
    agg["quentes_por_criativo"] = dict(_count(r["content"] for r in out_rows if r["class"] == "quente"))
    agg["quentes_por_campanha"] = dict(_count(r["campaign"] for r in out_rows if r["class"] == "quente"))

    # 5) coortes: leads por data de entrada x compradores quentes dessa coorte (7 e 14 dias so se a coorte ja amadureceu)
    coh = defaultdict(lambda: {"leads": 0, "compradores": 0, "ate_7d": 0, "ate_14d": 0})
    for em, l in leads.items():
        coh[cohort_key(l["created"], cohort_by)]["leads"] += 1
    # idade da coorte = idade do lead MAIS RECENTE dela (so conta como madura quando todos tiveram o prazo)
    youngest = {}
    for em, l in leads.items():
        k = cohort_key(l["created"], cohort_by)
        age = (as_of - l["created"]).total_seconds() / 86400
        youngest[k] = min(youngest.get(k, age), age)
    for r in out_rows:
        if r["class"] == "quente":
            c = coh[r["cohort"]]
            c["compradores"] += 1
            if r["days"] <= 7:
                c["ate_7d"] += 1
            if r["days"] <= 14:
                c["ate_14d"] += 1
    table = []
    for k in sorted(coh):
        c = coh[k]
        row = {"coorte": k, "leads": c["leads"], "compradores": c["compradores"],
               "conversao": _pct(c["compradores"], c["leads"]),
               "conv_7d": _pct(c["ate_7d"], c["leads"]) if youngest[k] >= 7 else "imatura (<7 dias)",
               "conv_14d": _pct(c["ate_14d"], c["leads"]) if youngest[k] >= 14 else "imatura (<14 dias)",
               "amostra_pequena": c["leads"] < SMALL}
        table.append(row)
    agg["coortes"] = table
    agg["_revisao"] = revisao  # so ids de pedido; removido da saida padrao
    return agg


def cohort_key(dt, by):
    d = dt.date()
    if by == "week":
        y, w, _ = d.isocalendar()
        return f"{y}-S{w:02d}"
    return d.isoformat()


def _count(it):
    d = defaultdict(int)
    for x in it:
        d[x] += 1
    return sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))


def _pct(a, b):
    return round(100.0 * a / b, 1) if b else None


def _stats(vals):
    if not vals:
        return {"n": 0}
    v = sorted(vals)
    mid = v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2
    return {"n": len(v), "mediana": round(mid, 2), "min": v[0], "max": v[-1], "amostra_pequena": len(v) < SMALL}


# ------------------------------------------------------------------ CLI
def read_csv(path, allow_inside):
    p = Path(path).resolve()
    if not allow_inside and (REPO_ROOT in p.parents):
        sys.exit(f"RECUSADO: {p} esta dentro do repositorio. Dados de leads e compradores ficam FORA do Git.")
    with open(p, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--leads", required=True)
    ap.add_argument("--compras", required=True)
    ap.add_argument("--as-of", help="data de corte AAAA-MM-DD (padrao: hoje, UTC)")
    ap.add_argument("--gmail-rules", action="store_true", help="REGRA OPCIONAL: ignora pontos e +tag em gmail.com (rotulada na saida)")
    ap.add_argument("--cold-campaign", action="append", help="utm_campaign de venda fria (padrao: venda-fria); repita para mais de uma")
    ap.add_argument("--cohort-by", choices=("day", "week"), default="day")
    ap.add_argument("--json", help="grava a saida agregada neste arquivo (fora do repositorio)")
    ap.add_argument("--revisao-out", help="grava ids de pedido para revisao humana (sem PII), fora do repositorio")
    ap.add_argument("--allow-inside-repo", action="store_true", help="so para os arquivos .example ficticios")
    a = ap.parse_args(argv)
    as_of = datetime.fromisoformat(a.as_of).replace(tzinfo=timezone.utc) if a.as_of else datetime.now(timezone.utc)
    res = conciliar(read_csv(a.leads, a.allow_inside_repo), read_csv(a.compras, a.allow_inside_repo), as_of,
                    tuple(a.cold_campaign) if a.cold_campaign else COLD_DEFAULT, a.gmail_rules, a.cohort_by)
    rev = res.pop("_revisao")
    if a.revisao_out:
        Path(a.revisao_out).write_text(json.dumps(rev, ensure_ascii=False, indent=1), encoding="utf-8")
    txt = json.dumps(res, ensure_ascii=False, indent=1)
    if a.json:
        Path(a.json).write_text(txt, encoding="utf-8")
    print(txt)
    return 0 if res["soma_confere"] else 1


if __name__ == "__main__":
    sys.exit(main())
