#!/usr/bin/env python3
"""gerar_dados.py: transforma os CSVs de exportacao (Meta, ClickMax, Ticto) no dados.json do painel.

Entradas (CSV; modelos FICTICIOS em exemplos/MODELO_*.csv; dados reais ficam FORA do repositorio):
  --meta       date,campaign_id,campaign_name,adset_id,ad_id,ad_name,spend,impressions,link_clicks,purchases,purchase_value_brl
  --vendas     ClickMax: order_id,paid_at,value_brl,status,is_test,utm_campaign,utm_content,ad_id,campaign_id,adset_id[,payment_method,delivered,net_brl]
  --eventos    ClickMax/GTM (opcional): date,ad_id,utm_content,landing_view,offer_view,cta_price_click,checkout_start,pix_generated
  --ticto      Gateway (opcional, so para conciliar): order_id,paid_at,value_brl,status,payment_method
  --hibrido    Funil hibrido (opcional): campo,valor (gasto_captacao, gasto_quente, gasto_fria, leads, compradores_quente, compradores_frio,
               compradores_nao_atribuidos, compradores_unicos, reembolsos_quente, reembolsos_frio, reembolsos_nao_atribuidos, data_leitura)
  --coortes    Coortes diarias de leads (opcional): data,leads,comp_7d,comp_14d,comp_hoje,soma_dias_ate_compra
Saida: --saida dados.json (e, com --html-base e --html-saida, uma copia do dashboard com o JSON embutido para abrir por duplo clique).

Regras (ver INDICADORES_P0.md):
- Compra = status paid ou refunded, sem is_test=1 (mesma base do conciliar.py). Reembolsada conta como compra e como reembolso.
- Atribuicao: venda com ad_id conhecido (ou utm_content igual ao nome do anuncio) vai para o anuncio; sem origem vai para
  '(sem atribuicao)' e NUNCA e distribuida.
- Campo sem dado = null (Indisponivel). Nunca vira zero. Sem arquivo de eventos, visitas/ofertas/cliques CTA/checkouts/Pix ficam null.
- Decisao (semaforo) so como RECOMENDACAO; executar depende de 'aprovado' de Bruno.
Codigo de saida 0; avisos de qualidade vao dentro do JSON.
"""
import argparse
import csv
import importlib.util
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SEM_ATRIB = "(sem atribuição)"
LIMIARES_PADRAO = {  # todos [H]: Bruno ajusta (ver INDICADORES_P0.md)
    "min_visitas": 300, "min_checkouts": 30, "min_compras": 5, "conv_checkout_min": 0.10, "reembolso_max": 0.10,
    "stop_loss_mult": 3, "idx_curioso": 1.5, "idx_comprador": 0.67, "utm_min_pct": 0.90,
}
CAMPOS_EVENTO = ["visitas", "ofertas", "cliques_cta", "checkouts", "pix_gerados"]
CAMPOS_SOMA = ["gasto", "impressoes", "cliques_link", "visitas", "ofertas", "cliques_cta", "checkouts", "pix_gerados", "pix_pagos",
               "compras", "entregues", "reembolsos", "receita_bruta", "receita_liquida"]


def _conciliar():
    p = os.path.join(HERE, "..", "09-tracking", "conciliacao", "conciliar.py")
    spec = importlib.util.spec_from_file_location("conciliar", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def ler(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(v, default=None):
    if v is None or str(v).strip() == "":
        return default
    return float(str(v).replace(",", "."))


def dia(ts):
    return str(ts)[:10]


# ---------- aritmetica sensivel a null (Indisponivel nunca vira zero)
def soma(vals):
    v = [x for x in vals if x is not None]
    return round(sum(v), 6) if v else None


def div(a, b):
    if a is None or b is None or b == 0:
        return None
    return a / b


def liquido_venda(valor, taxa_fixa, taxa_pct_alta, limite_faixa):
    """Liquido por venda (Pix): taxa fixa para valor <= limite_faixa; fixa + % acima. Regra por faixa e [NC]; confirmar no extrato da Ticto."""
    pct = 0.0 if valor <= limite_faixa else taxa_pct_alta
    return round(valor - taxa_fixa - pct * valor, 2)


def construir_linhas(meta_rows, venda_rows, evento_rows, p):
    """Uma linha por (dia, campanha, anuncio). Retorna (linhas, info_atribuicao)."""
    nome_por_ad = {}
    ad_por_nome = {}
    camp_nome = {}
    L = {}

    def linha(d, cid, cnome, ad, nome):
        k = (d, cid or "", ad or "", nome)
        if k not in L:
            L[k] = {"data": d, "campaign_id": cid or "", "campaign_name": cnome or "", "ad_id": ad or "", "criativo": nome,
                    **{c: None for c in CAMPOS_SOMA}}
        return L[k]

    for r in meta_rows:
        ad, nm = r["ad_id"].strip(), r["ad_name"].strip()
        nome_por_ad[ad] = nm
        ad_por_nome[nm] = ad
        camp_nome[r["campaign_id"].strip()] = r["campaign_name"].strip()
        x = linha(r["date"], r["campaign_id"].strip(), r["campaign_name"].strip(), ad, nm)
        x["gasto"] = (x["gasto"] or 0) + num(r["spend"], 0)
        x["impressoes"] = (x["impressoes"] or 0) + int(num(r["impressions"], 0))
        x["cliques_link"] = (x["cliques_link"] or 0) + int(num(r["link_clicks"], 0))
    tem_eventos = evento_rows is not None
    if tem_eventos:
        col = {"landing_view": "visitas", "offer_view": "ofertas", "cta_price_click": "cliques_cta", "checkout_start": "checkouts", "pix_generated": "pix_gerados"}
        for r in evento_rows:
            ad = (r.get("ad_id") or "").strip() or ad_por_nome.get((r.get("utm_content") or "").strip(), "")
            nm = nome_por_ad.get(ad, (r.get("utm_content") or "").strip())
            cid = next((k[1] for k in L if k[2] == ad and k[1]), "")
            x = linha(r["date"], cid, camp_nome.get(cid, ""), ad, nm)
            for fonte, dest in col.items():
                if (r.get(fonte) or "").strip() != "":
                    x[dest] = (x[dest] or 0) + int(num(r[fonte], 0))
    sem_origem, total_pagas = 0, 0
    for r in venda_rows:
        st = (r.get("status") or "").lower()
        if st not in ("paid", "refunded") or str(r.get("is_test") or "0") == "1":
            continue
        total_pagas += 1
        d = dia(r["paid_at"])
        ad = (r.get("ad_id") or "").strip()
        nm = (r.get("utm_content") or "").strip()
        if not ad and nm in ad_por_nome:
            ad = ad_por_nome[nm]
        if ad and ad in nome_por_ad:
            nome = nome_por_ad[ad]
            cid = next((k[1] for k in L if k[2] == ad and k[1]), (r.get("campaign_id") or "").strip())
            x = linha(d, cid, camp_nome.get(cid, ""), ad, nome)
        else:
            sem_origem += 1
            x = linha(d, "", "", "", SEM_ATRIB)
        valor = num(r["value_brl"], 0)
        net = num(r.get("net_brl")) if "net_brl" in r else None
        if net is None:
            net = liquido_venda(valor, p["taxa_fixa"], p["taxa_pct_alta"], p["limite_faixa"])
        x["compras"] = (x["compras"] or 0) + 1
        x["receita_bruta"] = round((x["receita_bruta"] or 0) + valor, 2)
        refund = st == "refunded"
        x["reembolsos"] = (x["reembolsos"] or 0) + (1 if refund else 0)
        x["receita_liquida"] = round((x["receita_liquida"] or 0) + (0 if refund else net), 2)
        if (r.get("payment_method") or "").lower() == "pix":
            x["pix_pagos"] = (x["pix_pagos"] or 0) + 1
        if "delivered" in r and str(r.get("delivered") or "").strip() != "":
            x["entregues"] = (x["entregues"] or 0) + (1 if str(r["delivered"]) == "1" else 0)
    # fontes obrigatorias (Meta e vendas): ausencia de linha = zero. Fontes opcionais (eventos, payment_method, delivered): ausencia = null.
    tem_pm = any("payment_method" in r for r in venda_rows)
    tem_dl = any("delivered" in r and str(r.get("delivered") or "").strip() != "" for r in venda_rows)
    for x in L.values():
        for k in ("compras", "reembolsos", "receita_bruta", "receita_liquida"):
            if x[k] is None:
                x[k] = 0
        for k in ("impressoes", "cliques_link"):
            if x[k] is None and x["criativo"] != SEM_ATRIB:
                x[k] = 0
        if x["gasto"] is None and x["criativo"] != SEM_ATRIB:
            x["gasto"] = 0.0
        x["gasto"] = None if x["gasto"] is None else round(x["gasto"], 2)
        if tem_pm and x["pix_pagos"] is None:
            x["pix_pagos"] = 0
        if tem_dl and x["entregues"] is None:
            x["entregues"] = 0
    linhas = sorted(L.values(), key=lambda z: (z["data"], z["campaign_id"], z["ad_id"], z["criativo"]))
    return linhas, {"vendas_pagas": total_pagas, "sem_origem": sem_origem, "tem_eventos": tem_eventos}


def derivar(t, F, lim):
    """Indicadores de um agregado t (gasto, visitas, ...). F = parametros financeiros. Tudo null-safe."""
    d = {}
    d["cpc"] = div(t["gasto"], t["cliques_link"])
    d["cpv"] = div(t["gasto"], t["visitas"])
    d["conv_landing"] = div(t["cliques_cta"], t["visitas"])
    d["cp_cliqueq"] = div(t["gasto"], t["cliques_cta"])
    d["cp_chk"] = div(t["gasto"], t["checkouts"])
    d["conv_checkout"] = div(t["compras"], t["checkouts"])
    d["cpa"] = div(t["gasto"], t["compras"]) if t["compras"] else None
    d["sem_venda"] = bool(t["gasto"]) and (t["compras"] or 0) == 0
    d["taxa_reembolso"] = div(t["reembolsos"], t["compras"])
    d["pix_pago"] = div(t["pix_pagos"], t["pix_gerados"])
    d["visita_compra"] = div(t["compras"], t["visitas"])
    d["roas"] = div(t["receita_bruta"], t["gasto"])
    d["roas_liquido"] = div(t["receita_liquida"], t["gasto"])
    # margem de contribuicao realizada (parcial enquanto imposto e custo variavel estiverem 'a definir')
    if t["compras"] is None:
        d["margem_contribuicao"] = None
    else:
        liq_ok = (t["compras"] - (t["reembolsos"] or 0))
        d["margem_contribuicao"] = round((t["receita_liquida"] or 0) - liq_ok * (F["imposto"] * F["preco"] + F["custos_var"]), 2)
    d["resultado_midia"] = None if (d["margem_contribuicao"] is None or t["gasto"] is None) else round(d["margem_contribuicao"] - t["gasto"], 2)
    return d


def decidir(c, F, lim, totais):
    """Semaforo de um criativo. Retorna (decisao, motivo). Ordem de INDICADORES_P0.md secao 3."""
    if c["criativo"] == SEM_ATRIB:
        return "SEM DECISÃO", "Linha de vendas sem origem: não é anúncio."
    cpamax = F["cpa_max"]
    gasto = c["gasto"] or 0
    compras = c["compras"] or 0
    cpa = c["cpa"]
    if cpamax <= 0:
        return "PAUSAR", "A margem de contribuição não cobre a mídia."
    if gasto >= lim["stop_loss_mult"] * cpamax and (compras == 0 or (cpa is not None and cpa > cpamax)):
        return "PAUSAR", f"Corte de perda: gasto já passou de {lim['stop_loss_mult']}x o CPA máximo sem compras suficientes para pagar a mídia."
    faltas = []
    if c["visitas"] is None or c["checkouts"] is None:
        faltas.append("falta medir visitas e/ou início efetivo de checkout")
    else:
        if c["visitas"] < lim["min_visitas"]:
            faltas.append(f"visitas {int(c['visitas'])} < {lim['min_visitas']}")
        if c["checkouts"] < lim["min_checkouts"]:
            faltas.append(f"checkouts efetivos {int(c['checkouts'])} < {lim['min_checkouts']}")
    if compras < lim["min_compras"]:
        faltas.append(f"compras {compras} < {lim['min_compras']}")
    if faltas:
        return "SEM DECISÃO", "Amostra insuficiente: " + "; ".join(faltas) + "."
    if cpa is None or cpa > cpamax:
        return "PAUSAR", "CPA acima do CPA máximo: cada venda perde dinheiro."
    conv_ok = c["conv_checkout"] is not None and c["conv_checkout"] >= lim["conv_checkout_min"]
    reemb_ok = (c["taxa_reembolso"] or 0) <= lim["reembolso_max"]
    if cpa <= F["cpa_desejado"] and conv_ok and reemb_ok:
        return "ESCALAR", "CPA no desejado, conversão do checkout e reembolso dentro do limite (executar só com aprovado de Bruno)."
    motivos = []
    if cpa > F["cpa_desejado"]:
        motivos.append("CPA entre o desejado e o máximo")
    if not conv_ok:
        motivos.append("conversão checkout → aprovado abaixo do piso")
    if not reemb_ok:
        motivos.append("reembolso acima do limite")
    m = "; ".join(motivos)
    return "MANTER", m[:1].upper() + m[1:] + "."


def perfil_curioso(c, tot_chk, tot_compras, lim):
    """CURIOSO / COMPRADOR / MISTO / AMOSTRA PEQUENA / None (indisponivel). Retorna (perfil, indice)."""
    if c["criativo"] == SEM_ATRIB or c["checkouts"] is None or tot_chk in (None, 0) or c["compras"] is None or not tot_compras:
        return None, None
    if c["checkouts"] < lim["min_checkouts"]:
        return "AMOSTRA PEQUENA", None
    if c["compras"] == 0:
        return "CURIOSO", None
    idx = (c["checkouts"] / tot_chk) / (c["compras"] / tot_compras)
    if idx >= lim["idx_curioso"]:
        return "CURIOSO", idx
    if idx <= lim["idx_comprador"]:
        return "COMPRADOR", idx
    return "MISTO", idx


def analisar(linhas, F, lim):
    """Agrega por anuncio, deriva indicadores, classifica e decide. Retorna dict com criativos, totais e funil."""
    grupos = defaultdict(list)
    for x in linhas:
        grupos[(x["campaign_id"], x["ad_id"], x["criativo"])].append(x)
    criativos = []
    for (cid, ad, nm), rows in grupos.items():
        c = {"campaign_id": cid, "campaign_name": rows[0]["campaign_name"], "ad_id": ad, "criativo": nm}
        for k in CAMPOS_SOMA:
            c[k] = soma([r[k] for r in rows])
        # gasto de linha sem fonte de gasto (so vendas) e null; para anuncio com gasto zero deixa null
        c.update(derivar(c, F, lim))
        criativos.append(c)
    atrib = [c for c in criativos if c["criativo"] != SEM_ATRIB]
    tot_chk = soma([c["checkouts"] for c in atrib])
    tot_comp = soma([c["compras"] for c in atrib])
    for c in criativos:
        c["perfil"], c["indice_curiosidade"] = perfil_curioso(c, tot_chk, tot_comp, lim)
        c["part_checkouts"] = div(c["checkouts"], tot_chk) if c["criativo"] != SEM_ATRIB else None
        c["part_compras"] = div(c["compras"], tot_comp) if c["criativo"] != SEM_ATRIB else None
        c["decisao"], c["motivo"] = decidir(c, F, lim, None)
    escalam = [c for c in criativos if c["decisao"] == "ESCALAR"]
    venc = min(escalam, key=lambda c: c["cpa"]) if escalam else None
    com_cpa = [c for c in atrib if c["decisao"] != "SEM DECISÃO" and c["cpa"] is not None]
    barato = [c for c in atrib if c["cp_chk"] is not None]
    menor_chk = min(barato, key=lambda c: c["cp_chk"]) if barato else None
    menor_cpc = min([c for c in atrib if c["cpc"] is not None] or [None], key=lambda c: c["cpc"] if c else 0)
    for c in criativos:
        c["vencedor"] = bool(venc and c is venc)
        c["armadilha"] = None
        if venc and c is not venc and c in atrib:
            if menor_chk is c:
                c["armadilha"] = "menor custo por checkout, mas não é o menor CPA"
            elif menor_cpc is c:
                c["armadilha"] = "menor CPC, mas não é o menor CPA"
    criativos.sort(key=lambda c: (c["criativo"] == SEM_ATRIB, c["cpa"] is None, c["cpa"] if c["cpa"] is not None else 0, c["criativo"]))
    # totais (inclui sem atribuicao: venda e venda)
    tot = {k: soma([x[k] for x in linhas]) for k in CAMPOS_SOMA}
    tot.update(derivar(tot, F, lim))
    tot["cpa_atribuido"] = div(soma([c["gasto"] for c in atrib]), soma([c["compras"] for c in atrib])) if soma([c["compras"] for c in atrib]) else None
    etapas = [("Visualização da landing", "visitas"), ("Visualização da oferta", "ofertas"), ("Clique no CTA com preço", "cliques_cta"),
              ("Início efetivo de checkout", "checkouts"), ("Pix gerado", "pix_gerados"), ("Pagamento aprovado", "compras"), ("Entrega do produto", "entregues")]
    funil, ant = [], None
    base = tot["visitas"]
    for nome, k in etapas:
        q = tot[k]
        funil.append({"etapa": nome, "campo": k, "quantidade": q, "taxa_anterior": div(q, ant) if ant is not None else None,
                      "taxa_visitas": div(q, base) if k != "visitas" else None})
        ant = q if q is not None else ant
    return {"criativos": criativos, "totais": tot, "funil": funil,
            "vencedor": venc["criativo"] if venc else None}


def qualidade(info, linhas, conc, checkout_def, lim, venda_rows, meta_rows):
    q = {}
    ev = {k: soma([x[k] for x in linhas]) for k in CAMPOS_EVENTO}
    nomes = {"visitas": "landing_view", "ofertas": "offer_view", "cliques_cta": "cta_price_click", "checkouts": "checkout_start", "pix_gerados": "pix_generated"}
    ausentes = [nomes[k] for k, v in ev.items() if v is None]
    pagos_evento = soma([x["compras"] for x in linhas])
    q["pixel"] = {
        "eventos_ausentes": ausentes,
        "checkout_start_definicao": checkout_def,
        "status": "ALERTA" if (ausentes or checkout_def != "efetivo") else "OK",
        "nota": ("Início de checkout medido no carregamento do iframe não vale como intenção." if checkout_def == "carregamento"
                 else "Definição do início de checkout não informada." if checkout_def == "desconhecido" else "Início efetivo informado."),
        "compras_aprovadas": pagos_evento,
    }
    pagas, sem = info["vendas_pagas"], info["sem_origem"]
    pct = (pagas - sem) / pagas if pagas else None
    q["utm"] = {"compras_aprovadas": pagas, "sem_origem": sem, "pct_com_origem": pct,
                "status": "SEM DADO" if pct is None else ("OK" if pct >= lim["utm_min_pct"] else "ALERTA"),
                "nota": "Compra sem origem fica em '(sem atribuição)': o CPA por anúncio é limite superior."}
    q["conciliacao"] = conc
    q["amostra"] = {"compras": pagas, "status": "AMOSTRA PEQUENA" if pagas < 10 else "OK"}
    return q


def conciliacao(vendas, ticto, meta_rows):
    C = _conciliar()
    res = {"status": "SEM DADO", "gateway": None, "meta": None, "por_dia_alertas": None, "sem_atribuicao": None}
    alerta = False
    if ticto is not None:
        g = C.reconcile_gateway(vendas, ticto)
        res["gateway"] = {"clickmax_compras": g["clickmax_compras"], "gateway_compras": g["gateway_compras"], "dif_pct": g["dif_compras_pct"],
                          "veredito": g["veredito"], "divergencias": g["divergencias"]}
        alerta = alerta or g["veredito"] == "ALERTA" or bool(g["divergencias"])
    if meta_rows:
        agg = defaultdict(lambda: [0, 0.0])
        info = {}
        for r in meta_rows:
            k = (r["date"], r["campaign_id"])
            agg[k][0] += int(num(r.get("purchases"), 0)); agg[k][1] += num(r.get("purchase_value_brl"), 0)
            info[r["campaign_id"]] = r["campaign_name"]
        meta_c = [{"date": k[0], "campaign_id": k[1], "campaign_name": info[k[1]], "purchases": v[0], "purchase_value_brl": v[1]} for k, v in sorted(agg.items())]
        dias, total = C.reconcile_meta_by_day(vendas, meta_c)
        camps, sem = C.reconcile_by_campaign(vendas, meta_c)
        res["meta"] = {"total": total, "por_campanha": camps}
        res["por_dia_alertas"] = sum(1 for d in dias if d["veredito"] == "ALERTA")
        res["sem_atribuicao"] = sem["compras_sem_atribuicao"]
        alerta = alerta or total["veredito"] == "ALERTA"
    if ticto is not None or meta_rows:
        res["status"] = "ALERTA" if alerta else "OK"
    return res


def gerar(meta_rows, venda_rows, evento_rows=None, ticto_rows=None, *, ficticio, periodo=None, preco=47.0, taxa_fixa=2.49, taxa_pct_alta=0.0699,
          limite_faixa=47.0, imposto=0.0, custos_var=0.0, reembolso_reserva=0.0, margem_alvo=0.30, limiares=None, checkout_def="desconhecido",
          rotulo=None, fuso="America/Sao_Paulo", gerado_em=None, hibrido_rows=None, coorte_rows=None, hib_params=None):
    lim = dict(LIMIARES_PADRAO, **(limiares or {}))
    p = {"taxa_fixa": taxa_fixa, "taxa_pct_alta": taxa_pct_alta, "limite_faixa": limite_faixa}
    liquido = liquido_venda(preco, taxa_fixa, taxa_pct_alta, limite_faixa)
    cpa_max = round(liquido - imposto * preco - custos_var - reembolso_reserva * liquido, 2)
    F = {"preco": preco, "liquido": liquido, "imposto": imposto, "custos_var": custos_var, "cpa_max": cpa_max,
         "cpa_desejado": round(cpa_max * (1 - margem_alvo), 2), "margem_alvo": margem_alvo,
         "roas_equilibrio": round(preco / cpa_max, 4) if cpa_max > 0 else None,
         "parcial": (imposto == 0 and custos_var == 0)}
    linhas, info = construir_linhas(meta_rows, venda_rows, evento_rows, p)
    an = analisar(linhas, F, lim)
    conc = conciliacao(venda_rows, ticto_rows, meta_rows)
    datas = sorted({x["data"] for x in linhas})
    out = {
        "meta": {
            "rotulo": rotulo or ("dados fictícios" if ficticio else "dados reais"),
            "ficticio": bool(ficticio),
            "gerado_em": gerado_em or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "periodo": periodo or {"de": datas[0] if datas else None, "ate": datas[-1] if datas else None},
            "fuso": fuso, "produto": "Mini Mentoria de Estruturação Zion", "slug": "mm47",
            "financeiro": F, "limiares": lim,
            "fontes": {"meta": "Meta (export/Windsor)", "vendas": "ClickMax", "eventos": "ClickMax/GTM" if info["tem_eventos"] else "indisponível",
                       "gateway": "Ticto" if ticto_rows is not None else "indisponível"},
        },
        "linhas": linhas,
        "analise": an,
        "qualidade": qualidade(info, linhas, conc, checkout_def, lim, venda_rows, meta_rows),
    }
    hb = hibrido(hibrido_rows, coorte_rows, F, hib_params)
    if hb is not None:
        hb["rotulo"] = out["meta"]["rotulo"]
        out["hibrido"] = hb
    return out


HIB_PADRAO = {"teto_dia": 60.0, "dias": 14, "cap_dia": 30.0, "q_dia": 15.0, "f_dia": 15.0, "k": 3.0}  # [H] proposta de Bruno de 25/11; parametros
HIB_CAMPOS = ["gasto_captacao", "gasto_quente", "gasto_fria", "leads", "compradores_quente", "compradores_frio", "compradores_nao_atribuidos",
              "compradores_unicos", "reembolsos_quente", "reembolsos_frio", "reembolsos_nao_atribuidos"]


def _idade(data, leitura):
    if not data or not leitura:
        return None
    return (datetime.strptime(leitura, "%Y-%m-%d") - datetime.strptime(data, "%Y-%m-%d")).days


def hibrido(hib_rows, coorte_rows, F, params=None):
    """Funil hibrido: quente (captacao + venda quente), frio (venda fria) e global (compradores unicos). Mesmas formulas da aba
    'Funil Hibrido' do modelo v3. Campo sem dado = None (indisponivel, nunca zero). Retorna None se nao houver arquivo."""
    if hib_rows is None and coorte_rows is None:
        return None
    P = dict(HIB_PADRAO, **(params or {}))
    e = {k: None for k in HIB_CAMPOS}
    e["data_leitura"] = None
    for r in hib_rows or []:
        c = (r.get("campo") or "").strip()
        v = (r.get("valor") or "").strip()
        if c in e:
            e[c] = v if c == "data_leitura" and v else (num(v) if c != "data_leitura" else None)
    unit = F["liquido"] - F["imposto"] * F["preco"] - F["custos_var"]  # margem realizada por venda (sem reserva de reembolso)
    perda = P["k"] * F["cpa_max"]

    def dif(a, b):
        return None if a is None or b is None else a - b

    gastos = [e["gasto_captacao"], e["gasto_quente"], e["gasto_fria"]]
    inv = soma(gastos)
    inv_q = soma([e["gasto_captacao"], e["gasto_quente"]])
    reemb_tot = soma([e["reembolsos_quente"], e["reembolsos_frio"], e["reembolsos_nao_atribuidos"]])
    soma_c = soma([e["compradores_quente"], e["compradores_frio"], e["compradores_nao_atribuidos"]])

    def faixa(cpa):
        if cpa is None:
            return None
        return "abaixo do CPA desejado" if cpa <= F["cpa_desejado"] else ("entre o desejado e o máximo" if cpa <= F["cpa_max"] else "acima do CPA máximo")

    def caminho(nome, invest, comp, reemb):
        liq = None if comp is None else (comp - (reemb or 0))
        d = {"caminho": nome, "investimento": invest, "compradores": comp, "reembolsos": reemb,
             "cpa": div(invest, comp) if comp else None, "sem_compra": comp == 0 and invest is not None}
        d["receita_liquida"] = None if liq is None else round(liq * F["liquido"], 2)
        d["margem_contribuicao"] = None if liq is None else round(liq * unit, 2)
        d["resultado_midia"] = None if d["margem_contribuicao"] is None or invest is None else round(d["margem_contribuicao"] - invest, 2)
        d["roas"] = div(None if comp is None else comp * F["preco"], invest)
        d["equilibrio_compradores"] = div(invest, F["cpa_max"]) if F["cpa_max"] > 0 else None
        d["faixa"] = faixa(d["cpa"])
        d["limite_perda"] = None if invest is None or comp is None else ("LIMITE ATINGIDO" if (invest >= perda and comp == 0) else "dentro do limite")
        return d
    out = {
        "rotulo": None,
        "parametros": {**P, "orcamento_teste": P["teto_dia"] * P["dias"], "soma_papeis_dia": P["cap_dia"] + P["q_dia"] + P["f_dia"], "limite_perda": round(perda, 2)},
        "entradas": e,
        "cpl": div(e["gasto_captacao"], e["leads"]),
        "caminhos": {"quente": caminho("quente", inv_q, e["compradores_quente"], e["reembolsos_quente"]),
                     "frio": caminho("frio", e["gasto_fria"], e["compradores_frio"], e["reembolsos_frio"]),
                     "global": caminho("global", inv, e["compradores_unicos"], reemb_tot)},
        "duplicidade": (None if soma_c is None or e["compradores_unicos"] is None else
                        ("OK: sem duplicidade" if soma_c == e["compradores_unicos"] else
                         ("DUPLICIDADE: soma maior que únicos" if soma_c > e["compradores_unicos"] else "FALTA: soma menor que únicos"))),
        "soma_grupos": soma_c,
        "orcamento": {"consumido": div(inv, P["teto_dia"] * P["dias"]), "restante": dif(P["teto_dia"] * P["dias"], inv)},
    }
    cs = []
    for r in coorte_rows or []:
        d = (r.get("data") or "").strip()
        leads, c7, c14, hoje, sd = (num(r.get(k)) for k in ("leads", "comp_7d", "comp_14d", "comp_hoje", "soma_dias_ate_compra"))
        idade = _idade(d, e["data_leitura"])
        m7 = idade is not None and idade >= 7
        m14 = idade is not None and idade >= 14
        cs.append({"data": d, "leads": leads, "comp_7d": c7, "comp_14d": c14, "comp_hoje": hoje, "soma_dias": sd, "idade": idade,
                   "madura_7d": m7, "madura_14d": m14,
                   "conv_7d": div(c7, leads) if m7 else None, "conv_14d": div(c14, leads) if m14 else None,
                   "dias_medios": div(sd, hoje) if hoje else None})
    out["coortes"] = cs

    def agg(flag, campo):
        sel = [c for c in cs if c[flag] and c["leads"] and c[campo] is not None]
        return div(sum(c[campo] for c in sel), sum(c["leads"] for c in sel)) if sel else None
    out["coortes_total"] = {"conv_7d": agg("madura_7d", "comp_7d"), "conv_14d": agg("madura_14d", "comp_14d"),
                            "dias_medios": div(soma([c["soma_dias"] for c in cs]), soma([c["comp_hoje"] for c in cs])),
                            "coortes_maduras_7d": sum(1 for c in cs if c["madura_7d"]), "coortes_maduras_14d": sum(1 for c in cs if c["madura_14d"])}
    return out


def embutir(html_base, dados, destino):
    with open(html_base, encoding="utf-8") as f:
        h = f.read()
    marca = '<script id="dados-embutidos" type="application/json"></script>'
    if marca not in h:
        raise SystemExit("marcador dados-embutidos não encontrado no HTML base")
    payload = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(h.replace(marca, f'<script id="dados-embutidos" type="application/json">{payload}</script>'))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--vendas", required=True)
    ap.add_argument("--eventos")
    ap.add_argument("--ticto")
    ap.add_argument("--hibrido", help="CSV campo,valor do funil híbrido (opcional)")
    ap.add_argument("--coortes", help="CSV de coortes diárias de leads (opcional)")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--ficticio", action="store_true", help="marca como 'dados fictícios' (use só nos modelos)")
    ap.add_argument("--rotulo")
    ap.add_argument("--preco", type=float, default=47.0)
    ap.add_argument("--taxa-fixa", type=float, default=2.49)
    ap.add_argument("--taxa-pct-alta", type=float, default=0.0699)
    ap.add_argument("--imposto", type=float, default=0.0, help="% do preço (a definir: 0 = parcial)")
    ap.add_argument("--custos-var", type=float, default=0.0)
    ap.add_argument("--margem-alvo", type=float, default=0.30)
    ap.add_argument("--checkout-start", choices=["efetivo", "carregamento", "desconhecido"], default="desconhecido")
    ap.add_argument("--limiares", help="JSON com limiares [H] a trocar")
    ap.add_argument("--html-base")
    ap.add_argument("--html-saida")
    a = ap.parse_args(argv)
    lim = json.load(open(a.limiares, encoding="utf-8")) if a.limiares else None
    d = gerar(ler(a.meta), ler(a.vendas), ler(a.eventos) if a.eventos else None, ler(a.ticto) if a.ticto else None,
              ficticio=a.ficticio, rotulo=a.rotulo, preco=a.preco, taxa_fixa=a.taxa_fixa, taxa_pct_alta=a.taxa_pct_alta, imposto=a.imposto,
              custos_var=a.custos_var, margem_alvo=a.margem_alvo, limiares=lim, checkout_def=a.checkout_start,
              hibrido_rows=ler(a.hibrido) if a.hibrido else None, coorte_rows=ler(a.coortes) if a.coortes else None)
    with open(a.saida, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("ok", a.saida, "| rótulo:", d["meta"]["rotulo"], "| anúncios:", len(d["analise"]["criativos"]))
    if a.html_base and a.html_saida:
        embutir(a.html_base, d, a.html_saida)
        print("ok", a.html_saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
