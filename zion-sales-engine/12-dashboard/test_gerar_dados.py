#!/usr/bin/env python3
"""Testes de gerar_dados.py (python3 -I test_gerar_dados.py). Dados FICTICIOS de exemplos/. Contas independentes: leem os CSV direto."""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # necessario com python3 -I
import gerar_dados as G

EX = os.path.join(HERE, "exemplos")


def rd(n):
    with open(os.path.join(EX, n), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


META, VEN, EVE, TIC = rd("MODELO_meta_anuncios.csv"), rd("MODELO_clickmax_vendas.csv"), rd("MODELO_clickmax_eventos.csv"), rd("MODELO_ticto.csv")
FIX = dict(ficticio=True, checkout_def="efetivo", gerado_em="2030-01-08T00:00:00Z")


def cri(d, nome):
    return next(c for c in d["analise"]["criativos"] if c["criativo"] == nome)


class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = G.gerar(META, VEN, EVE, TIC, **FIX)

    # --- somas contra conta independente
    def test_gasto_total(self):
        self.assertAlmostEqual(self.d["analise"]["totais"]["gasto"], sum(float(r["spend"]) for r in META), places=2)
        self.assertAlmostEqual(self.d["analise"]["totais"]["gasto"], 1300.0, places=2)

    def test_compras_base_exclui_teste_e_pendente(self):
        pagas = [r for r in VEN if r["status"] in ("paid", "refunded") and r["is_test"] != "1"]
        self.assertEqual(self.d["analise"]["totais"]["compras"], len(pagas))
        self.assertEqual(len(pagas), 33)  # 31 atribuidas + 2 sem origem; teste e pendente ficam fora

    def test_por_anuncio_bate_com_csv(self):
        por = defaultdict(lambda: dict(g=0.0, v=0, c=0, k=0, s=0))
        for r in META: por[r["ad_name"]]["g"] += float(r["spend"])
        for r in EVE:
            por[r["utm_content"]]["v"] += int(r["landing_view"]); por[r["utm_content"]]["c"] += int(r["checkout_start"]); por[r["utm_content"]]["k"] += int(r["cta_price_click"])
        for r in VEN:
            if r["status"] in ("paid", "refunded") and r["is_test"] != "1" and r["utm_content"]:
                por[r["utm_content"]]["s"] += 1
        for nome, e in por.items():
            c = cri(self.d, nome)
            self.assertAlmostEqual(c["gasto"], e["g"], places=2, msg=nome)
            self.assertEqual((c["visitas"], c["checkouts"], c["cliques_cta"], c["compras"]), (e["v"], e["c"], e["k"], e["s"]), nome)
            if e["s"]:
                self.assertAlmostEqual(c["cpa"], e["g"] / e["s"], places=6)
            self.assertAlmostEqual(c["cpv"], e["g"] / e["v"], places=6)
            self.assertAlmostEqual(c["cp_chk"], e["g"] / e["c"], places=6)
            self.assertAlmostEqual(c["conv_landing"], e["k"] / e["v"], places=6)
            self.assertAlmostEqual(c["conv_checkout"], e["s"] / e["c"], places=6)

    def test_sem_atribuicao_nao_e_distribuida(self):
        s = cri(self.d, G.SEM_ATRIB)
        self.assertEqual(s["compras"], 2)
        self.assertIsNone(s["gasto"])
        self.assertEqual(s["decisao"], "SEM DECISÃO")
        soma_atrib = sum(c["compras"] for c in self.d["analise"]["criativos"] if c["criativo"] != G.SEM_ATRIB)
        self.assertEqual(soma_atrib + 2, self.d["analise"]["totais"]["compras"])
        # CPA geral (todas as compras) menor que o atribuido: sem origem nao entra no anuncio
        t = self.d["analise"]["totais"]
        self.assertAlmostEqual(t["cpa"], 1300 / 33, places=6)
        self.assertAlmostEqual(t["cpa_atribuido"], 1300 / 31, places=6)

    # --- financeiro
    def test_liquido_e_referencias(self):
        F = self.d["meta"]["financeiro"]
        self.assertEqual(F["liquido"], 44.51)  # Pix R$47 [E]
        self.assertEqual(G.liquido_venda(97.0, 2.49, 0.0699, 47.0), 87.73)  # regra por faixa [NC], so para valor > 47
        self.assertEqual(F["cpa_max"], 44.51)
        self.assertEqual(F["cpa_desejado"], round(44.51 * 0.7, 2))
        self.assertTrue(F["parcial"])  # imposto e custo variavel 'a definir'

    def test_receita_liquida_e_margem(self):
        t = self.d["analise"]["totais"]
        pagas = [r for r in VEN if r["status"] in ("paid", "refunded") and r["is_test"] != "1"]
        esperado = sum((float(r["value_brl"]) - 2.49 - (0.0699 * float(r["value_brl"]) if float(r["value_brl"]) > 47 else 0)) for r in pagas if r["status"] == "paid")
        self.assertAlmostEqual(t["receita_liquida"], esperado, places=1)
        self.assertAlmostEqual(t["receita_bruta"], sum(float(r["value_brl"]) for r in pagas), places=2)
        self.assertAlmostEqual(t["roas"], t["receita_bruta"] / 1300, places=6)
        self.assertEqual(t["reembolsos"], 1)
        self.assertAlmostEqual(t["resultado_midia"], t["margem_contribuicao"] - 1300, places=2)

    # --- decisao e curioso x comprador
    def test_semaforo(self):
        esperado = {"criativo-b-comprador": "ESCALAR", "criativo-c-medio": "MANTER", "criativo-a-curioso": "PAUSAR",
                    "criativo-d-caro": "PAUSAR", "criativo-e-novo": "SEM DECISÃO"}
        for n, dec in esperado.items():
            self.assertEqual(cri(self.d, n)["decisao"], dec, n)
        self.assertEqual(self.d["analise"]["vencedor"], "criativo-b-comprador")

    def test_vencedor_nao_e_cpc_baixo_nem_muitos_checkouts(self):
        a, b = cri(self.d, "criativo-a-curioso"), cri(self.d, "criativo-b-comprador")
        self.assertLess(a["cp_chk"], b["cp_chk"])  # A tem checkout mais barato
        self.assertGreater(a["checkouts"], b["checkouts"])  # e mais checkouts
        self.assertLess(b["cpa"], a["cpa"])  # mas B vende mais barato por comprador
        self.assertTrue(b["vencedor"]); self.assertFalse(a["vencedor"])
        self.assertIn("menor custo por checkout", a["armadilha"])

    def test_perfil_curioso_comprador(self):
        self.assertEqual(cri(self.d, "criativo-a-curioso")["perfil"], "CURIOSO")
        self.assertEqual(cri(self.d, "criativo-b-comprador")["perfil"], "COMPRADOR")
        self.assertEqual(cri(self.d, "criativo-c-medio")["perfil"], "MISTO")
        self.assertEqual(cri(self.d, "criativo-e-novo")["perfil"], "AMOSTRA PEQUENA")
        tot_c, tot_s = 210 + 95 + 90 + 45 + 5, 4 + 16 + 8 + 2 + 1
        self.assertAlmostEqual(cri(self.d, "criativo-a-curioso")["indice_curiosidade"], (210 / tot_c) / (4 / tot_s), places=6)

    def test_stop_loss_pausa_sem_compra(self):
        meta = [dict(r) for r in META]; ven = [r for r in VEN if r["utm_content"] != "criativo-d-caro"]
        d = G.gerar(meta, ven, EVE, TIC, **FIX)
        c = cri(d, "criativo-d-caro")
        self.assertEqual(c["compras"], 0)
        self.assertEqual(c["decisao"], "PAUSAR")  # gasto 210 >= 3 x 44,51
        self.assertIn("Corte de perda", c["motivo"])
        self.assertTrue(c["sem_venda"]); self.assertIsNone(c["cpa"])

    def test_reembolso_acima_do_limite_vira_manter(self):
        d = G.gerar(META, VEN, EVE, TIC, limiares={"reembolso_max": 0.05}, **FIX)  # B tem 1/16 = 6,25%
        self.assertEqual(cri(d, "criativo-b-comprador")["decisao"], "MANTER")
        self.assertIsNone(d["analise"]["vencedor"])

    def test_amostra_minima_bloqueia(self):
        d = G.gerar(META, VEN, EVE, TIC, limiares={"min_compras": 20}, **FIX)
        self.assertEqual(cri(d, "criativo-b-comprador")["decisao"], "SEM DECISÃO")

    # --- indisponivel nunca vira zero
    def test_sem_eventos_fica_indisponivel(self):
        d = G.gerar(META, VEN, None, TIC, **FIX)
        b = cri(d, "criativo-b-comprador")
        for k in ("visitas", "ofertas", "cliques_cta", "checkouts", "pix_gerados", "cpv", "cp_chk", "conv_landing", "conv_checkout", "pix_pago"):
            self.assertIsNone(b[k], k)
        self.assertAlmostEqual(b["cpa"], 350 / 16, places=6)  # o que existe continua calculado
        self.assertEqual(b["decisao"], "SEM DECISÃO")
        self.assertIsNone(b["perfil"])
        self.assertEqual(d["qualidade"]["pixel"]["status"], "ALERTA")
        self.assertIn("checkout_start", d["qualidade"]["pixel"]["eventos_ausentes"])

    def test_qualidade(self):
        q = self.d["qualidade"]
        self.assertEqual(q["utm"]["sem_origem"], 2)
        self.assertAlmostEqual(q["utm"]["pct_com_origem"], 31 / 33, places=6)
        self.assertEqual(q["conciliacao"]["status"], "ALERTA")
        self.assertEqual(q["conciliacao"]["gateway"]["divergencias"][0]["order_id"], "TX-X-099")
        self.assertEqual(q["pixel"]["status"], "OK")
        d2 = G.gerar(META, VEN, EVE, TIC, ficticio=True, checkout_def="carregamento")
        self.assertEqual(d2["qualidade"]["pixel"]["status"], "ALERTA")

    def test_funil_taxas(self):
        f = {e["campo"]: e for e in self.d["analise"]["funil"]}
        self.assertEqual(f["visitas"]["quantidade"], 3140)
        self.assertAlmostEqual(f["ofertas"]["taxa_anterior"], 1930 / 3140, places=6)
        self.assertAlmostEqual(f["compras"]["taxa_visitas"], 33 / 3140, places=6)
        self.assertEqual(len(self.d["analise"]["funil"]), 7)

    # --- rotulo, privacidade e artefatos
    def test_rotulo_ficticio(self):
        self.assertEqual(self.d["meta"]["rotulo"], "dados fictícios")
        self.assertTrue(self.d["meta"]["ficticio"])

    def test_sem_dado_pessoal_nas_colunas(self):
        txt = json.dumps(self.d, ensure_ascii=False).lower()
        for proibido in ("@", "email", "e-mail", "telefone", "phone", "cpf", "nome_cliente"):
            self.assertNotIn(proibido, txt, proibido)

    def test_exemplo_commitado_esta_atualizado(self):
        p = os.path.join(HERE, "dados_exemplo.json")
        self.assertTrue(os.path.exists(p), "gere dados_exemplo.json (ver README)")
        with open(p, encoding="utf-8") as f:
            atual = json.load(f)
        self.assertEqual(atual, json.loads(json.dumps(self.d, ensure_ascii=False)))

    def test_cli_e_html_embutido(self):
        with tempfile.TemporaryDirectory() as t:
            saida, html = os.path.join(t, "dados.json"), os.path.join(t, "dash.html")
            base = os.path.join(HERE, "dashboard.html")
            self.assertTrue(os.path.exists(base))
            r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "gerar_dados.py"),
                                "--meta", os.path.join(EX, "MODELO_meta_anuncios.csv"), "--vendas", os.path.join(EX, "MODELO_clickmax_vendas.csv"),
                                "--eventos", os.path.join(EX, "MODELO_clickmax_eventos.csv"), "--ticto", os.path.join(EX, "MODELO_ticto.csv"),
                                "--saida", saida, "--ficticio", "--checkout-start", "efetivo", "--html-base", base, "--html-saida", html],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            with open(saida, encoding="utf-8") as f:
                j = json.load(f)
            self.assertEqual(j["meta"]["rotulo"], "dados fictícios")
            with open(html, encoding="utf-8") as f:
                h = f.read()
            self.assertIn('"rotulo": "dados fictícios"', h)
            self.assertEqual(h.count('id="dados-embutidos"'), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
