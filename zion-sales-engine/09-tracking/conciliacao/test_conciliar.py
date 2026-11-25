import sys
import unittest
from pathlib import Path

sys.path.insert(0, Path(__file__).resolve().parent.as_posix())  # necessario com python3 -I (modo isolado)

import conciliar as C

H = Path(__file__).parent
CM = C.read(H / "MODELO_clickmax.csv")
GW = C.read(H / "MODELO_gateway.csv")
ME = C.read(H / "MODELO_meta.csv")


class T(unittest.TestCase):
    def test_base_exclui_teste_pendente(self):
        ids = sorted(r["order_id"] for r in C.clickmax_base(CM))
        self.assertEqual(ids, ["TX-F-001", "TX-F-002", "TX-F-004", "TX-F-005"])  # F-003 teste, F-006 pendente

    def test_verdict_tolerancia_10pct(self):
        self.assertEqual(C.verdict(100, 110), (10.0, "OK"))
        self.assertEqual(C.verdict(100, 90), (-10.0, "OK"))
        self.assertEqual(C.verdict(100, 89)[1], "ALERTA")
        self.assertEqual(C.verdict(100, 111)[1], "ALERTA")
        self.assertEqual(C.verdict(0, 0), (0.0, "OK"))
        self.assertEqual(C.verdict(0, 1), (None, "ALERTA"))

    def test_gateway_acha_divergencias(self):
        g = C.reconcile_gateway(CM, GW)
        probs = {i["order_id"]: i["problema"] for i in g["divergencias"]}
        self.assertIn("TX-F-007", probs)           # so no gateway
        self.assertNotIn("TX-F-003", probs)        # teste do ClickMax e ignorado dos dois lados
        self.assertEqual(g["clickmax_compras"], 4)
        self.assertEqual(g["gateway_compras"], 4)
        self.assertEqual(g["clickmax_valor"], 47 + 47 + 97 + 47)

    def test_valor_e_status_divergentes(self):
        gw = [dict(r) for r in GW]
        gw[0]["value_brl"] = "40.00"
        gw[1]["status"] = "pending"
        probs = " | ".join(i["problema"] for i in C.reconcile_gateway(CM, gw)["divergencias"])
        self.assertIn("valor diferente", probs)
        self.assertIn("status diferente", probs)

    def test_meta_por_dia(self):
        days, total = C.reconcile_meta_by_day(CM, ME)
        d20 = next(d for d in days if d["data"] == "2026-11-20")
        d21 = next(d for d in days if d["data"] == "2026-11-21")
        self.assertEqual((d20["clickmax_compras"], d20["meta_compras"], d20["veredito"]), (2, 2, "OK"))
        self.assertEqual((d21["clickmax_compras"], d21["meta_compras"]), (2, 1))
        self.assertEqual(d21["dif_compras_pct"], -50.0)
        self.assertEqual(d21["veredito"], "ALERTA")
        self.assertEqual(total["clickmax_compras"], 4)
        self.assertEqual(total["meta_compras"], 3)
        self.assertTrue(total["amostra_pequena"])

    def test_sem_atribuicao_nao_entra_por_campanha(self):
        camps, sem = C.reconcile_by_campaign(CM, ME)
        self.assertEqual(sem["ids"], ["TX-F-004"])
        a = next(c for c in camps if c["campaign_id"] == "120250000000000001")
        self.assertEqual((a["clickmax_compras"], a["meta_compras"]), (3, 3))
        self.assertEqual(a["veredito"], "OK")
        b = next(c for c in camps if c["campaign_id"] == "120250000000000002")
        self.assertEqual((b["clickmax_compras"], b["meta_compras"], b["veredito"]), (0, 0, "OK"))

    def test_relatorio_e_codigo_de_saida(self):
        lines = []
        res = C.report(CM, GW, ME, out=lines.append)
        self.assertTrue(C.has_alert(res))
        self.assertTrue(any("ALERTA" in l for l in lines))
        ok_me = [r for r in ME if r["date"] == "2026-11-20"]
        ok_cm = [r for r in CM if r["paid_at"].startswith("2026-11-20")]
        res2 = C.report(ok_cm, None, ok_me, out=lambda *_: None)
        self.assertFalse(C.has_alert(res2))


FU = C.read(H / "MODELO_funil.csv")


class TFunil(unittest.TestCase):
    def setUp(self):
        self.res = {f["data"]: f for f in C.reconcile_funil(FU, CM)}

    def test_dia_coerente_sem_alerta(self):
        f = self.res["2026-11-20"]  # ClickMax tem 2 compras pagas/reembolsadas em 20/11 (F-001, F-002)
        self.assertEqual(f["veredito"], "OK")
        self.assertEqual(f["taxas_pct"]["oferta/visita"], 45.0)
        self.assertEqual(f["taxas_pct"]["clique CTA/visita"], 15.0)
        self.assertEqual(f["taxas_pct"]["checkout efetivo/clique CTA"], 33.3)
        self.assertEqual(f["taxas_pct"]["aprovado/checkout efetivo"], 10.0)
        self.assertEqual(f["taxas_pct"]["entregue/aprovado"], 100.0)

    def test_entrega_menor_que_aprovado_gera_motivo(self):
        f = self.res["2026-11-21"]  # funil diz 2 aprovados; ClickMax base de 21/11 = 2 (F-004, F-005); entregues 1
        self.assertEqual(f["veredito"], "ALERTA")
        self.assertTrue(any("entrega pendente" in m for m in f["motivos_divergencia"]))
        self.assertFalse(any("diferentes da base ClickMax" in m for m in f["motivos_divergencia"]))

    def test_checkout_maior_que_clique_e_indisponivel_nao_vira_zero(self):
        f = self.res["2026-11-22"]
        self.assertTrue(any("carregamento do iframe" in m for m in f["motivos_divergencia"]))
        self.assertIn("Pix gerado", f["indisponiveis"])
        self.assertIn("entregue", f["indisponiveis"])
        self.assertEqual(f["approved"], 0)  # vazio no CSV: usa a base ClickMax (0 em 22/11), fonte registrada
        self.assertEqual(f["approved_fonte"], "clickmax")
        self.assertIsNone(f["taxas_pct"]["entregue/aprovado"])

    def test_aprovado_do_funil_diferente_do_clickmax(self):
        rows = [dict(r) for r in FU]
        rows[0]["approved"] = "5"
        f = {x["data"]: x for x in C.reconcile_funil(rows, CM)}["2026-11-20"]
        self.assertTrue(any("diferentes da base ClickMax" in m for m in f["motivos_divergencia"]))

    def test_pix_nao_e_compra_e_aprovado_acima_do_checkout(self):
        rows = [dict(r) for r in FU]
        rows[0]["approved"] = "30"
        rows[0]["delivered"] = "30"
        f = {x["data"]: x for x in C.reconcile_funil(rows, CM)}["2026-11-20"]
        self.assertTrue(any("aprovados maiores que checkout efetivo" in m for m in f["motivos_divergencia"]))

    def test_relatorio_com_funil(self):
        lines = []
        res = C.report(CM, None, None, out=lines.append, funil=FU)
        self.assertTrue(C.has_alert(res))
        self.assertTrue(any(l.strip().startswith("motivo:") for l in lines))


if __name__ == "__main__":
    unittest.main(verbosity=2)
