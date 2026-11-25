#!/usr/bin/env python3
"""Gera os MODELO_*.csv de exemplo (DADOS FICTICIOS, periodo 2030-01-01 a 2030-01-07; nada aqui e dado real).
Cenario: A curioso (barato no checkout, quase nao compra), B comprador (vencedor), C medio, D caro, E novo (amostra pequena).
Uso: python3 -I gerar_exemplos.py"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DAYS = [f"2030-01-0{d}" for d in range(1, 8)]
CAMP = {"1": ("120250000000000001", "campanha-ficticia-1"), "2": ("120250000000000002", "campanha-ficticia-2")}
# nome, campanha, ad_id, adset, gasto, impressoes, cliques_link, visitas, ofertas, cta, checkouts, pix_gerado, compras, reembolsos, dias
CRE = [
    ("criativo-a-curioso", "1", "120250000000000011", "120250000000000021", 420.0, 52000, 1500, 1300, 760, 330, 210, 150, 4, 0, DAYS),
    ("criativo-b-comprador", "1", "120250000000000012", "120250000000000021", 350.0, 30000, 700, 620, 450, 200, 95, 80, 16, 1, DAYS),
    ("criativo-c-medio", "2", "120250000000000013", "120250000000000022", 280.0, 26000, 900, 800, 480, 190, 90, 60, 8, 0, DAYS),
    ("criativo-d-caro", "2", "120250000000000014", "120250000000000022", 210.0, 21000, 400, 350, 200, 70, 45, 30, 2, 0, DAYS),
    ("criativo-e-novo", "2", "120250000000000015", "120250000000000022", 40.0, 4000, 90, 70, 40, 12, 5, 3, 1, 0, DAYS[5:]),
]


def split(total, n):
    base, rem = divmod(int(total), n)
    return [base + (1 if i < rem else 0) for i in range(n)]


def splitf(total, n):
    return [round(total / n, 2)] * (n - 1) + [round(total - round(total / n, 2) * (n - 1), 2)]


def w(name, header, rows):
    with open(os.path.join(HERE, name), "w", newline="", encoding="utf-8") as f:
        cw = csv.writer(f); cw.writerow(header); cw.writerows(rows)


meta, ev, sales, gw = [], [], [], []
n = 0
for (nm, ck, ad, adset, gasto, imp, lk, vis, ofe, cta, chk, pix, comp, reemb, dias) in CRE:
    k = len(dias)
    cid, cname = CAMP[ck]
    cols = [splitf(gasto, k)] + [split(x, k) for x in (imp, lk, vis, ofe, cta, chk, pix)]
    mp = split(comp, k)
    for i, d in enumerate(dias):
        meta.append([d, cid, cname, adset, ad, nm, f"{cols[0][i]:.2f}", cols[1][i], cols[2][i], mp[i] - (1 if (nm == "criativo-b-comprador" and i == 6) else 0), ""])
        ev.append([d, ad, nm, cols[3][i], cols[4][i], cols[5][i], cols[6][i], cols[7][i]])
    # vendas
    for j in range(comp):
        n += 1
        d = dias[j % k]
        status = "refunded" if (j < reemb) else "paid"
        entreg = 0 if (nm == "criativo-b-comprador" and j == 3) else 1
        oid = f"TX-X-{n:03d}"
        sales.append([oid, f"{d}T{10 + j % 10:02d}:15:00Z", "47.00", status, 0, "mm47", nm, ad, cid, adset, "pix", entreg])
        gw.append([oid, f"{d}T{10 + j % 10:02d}:15:20Z", "47.00", status, "pix"])
# vendas sem origem (sem UTM), uma de R$97; um teste interno; um pendente
n += 1; sales.append([f"TX-X-{n:03d}", "2030-01-03T12:00:00Z", "47.00", "paid", 0, "", "", "", "", "", "pix", 1]); gw.append([f"TX-X-{n:03d}", "2030-01-03T12:00:20Z", "47.00", "paid", "pix"])
n += 1; sales.append([f"TX-X-{n:03d}", "2030-01-05T09:30:00Z", "97.00", "paid", 0, "", "", "", "", "", "pix", 1]); gw.append([f"TX-X-{n:03d}", "2030-01-05T09:30:20Z", "97.00", "paid", "pix"])
n += 1; sales.append([f"TX-X-{n:03d}", "2030-01-04T08:00:00Z", "47.00", "paid", 1, "", "", "", "", "", "pix", 1]); gw.append([f"TX-X-{n:03d}", "2030-01-04T08:00:10Z", "47.00", "paid", "pix"])
n += 1; sales.append([f"TX-X-{n:03d}", "2030-01-06T15:00:00Z", "47.00", "pending", 0, "mm47", "criativo-c-medio", "120250000000000013", "120250000000000002", "120250000000000022", "pix", 0])
gw.append(["TX-X-099", "2030-01-06T16:00:00Z", "47.00", "paid", "pix"])  # divergencia de proposito: so no gateway
w("MODELO_meta_anuncios.csv", ["date", "campaign_id", "campaign_name", "adset_id", "ad_id", "ad_name", "spend", "impressions", "link_clicks", "purchases", "purchase_value_brl"],
  [r[:10] + [round(float(r[9]) * 47, 2)] for r in meta])
w("MODELO_clickmax_eventos.csv", ["date", "ad_id", "utm_content", "landing_view", "offer_view", "cta_price_click", "checkout_start", "pix_generated"], ev)
w("MODELO_clickmax_vendas.csv", ["order_id", "paid_at", "value_brl", "status", "is_test", "utm_campaign", "utm_content", "ad_id", "campaign_id", "adset_id", "payment_method", "delivered"], sales)
w("MODELO_ticto.csv", ["order_id", "paid_at", "value_brl", "status", "payment_method"], gw)
print("ok", len(meta), len(ev), len(sales), len(gw))
