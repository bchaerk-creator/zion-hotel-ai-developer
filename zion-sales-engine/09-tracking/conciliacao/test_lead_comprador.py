#!/usr/bin/env python3
"""Testes de lead_comprador.py com dados FICTICIOS. Rode: python3 -I test_lead_comprador.py"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lead_comprador as lc  # noqa: E402

AS_OF = datetime(2026, 12, 20, tzinfo=timezone.utc)


def L(email, created, campaign="captacao", content="cri-A", phone="", source="facebook", medium="lead_ads"):
    return {"email": email, "telefone": phone, "created_at": created, "utm_source": source, "utm_medium": medium, "utm_campaign": campaign, "utm_content": content}


def C(order, paid, email, campaign="", content="", status="paid", is_test="0", phone=""):
    return {"order_id": order, "paid_at": paid, "value_brl": "47.00", "status": status, "is_test": is_test, "email": email, "telefone": phone,
            "utm_source": "meta" if campaign else "", "utm_medium": "paid" if campaign else "", "utm_campaign": campaign, "utm_content": content}


class T(unittest.TestCase):
    def run_(self, leads, compras, **kw):
        return lc.conciliar(leads, compras, AS_OF, **kw)

    def test_quente_frio_nao_atribuida(self):
        leads = [L("Ana@Exemplo.invalid ", "2026-11-26T10:00:00Z", content="cri-A")]
        compras = [C("P1", "2026-11-28T10:00:00Z", "ana@exemplo.invalid"),                      # quente (e-mail normalizado)
                   C("P2", "2026-11-28T11:00:00Z", "bia@exemplo.invalid", "venda-fria", "cri-F"),  # frio
                   C("P3", "2026-11-28T12:00:00Z", "caio@exemplo.invalid")]                       # sem UTM, sem lead
        r = self.run_(leads, compras)
        self.assertEqual((r["quente"], r["frio"], r["nao_atribuida"]), (1, 1, 1))
        self.assertTrue(r["soma_confere"])
        self.assertEqual(r["nao_atribuida_motivos"], {"sem_utm_e_sem_lead": 1})
        self.assertEqual(r["quentes_por_criativo"], {"cri-A": 1})

    def test_tempo_ate_a_compra_em_dias(self):
        r = self.run_([L("a@x.invalid", "2026-11-26T00:00:00Z")], [C("P1", "2026-11-29T12:00:00Z", "a@x.invalid")])
        self.assertEqual(r["tempo_ate_a_compra_dias_quentes"]["mediana"], 3.5)

    def test_lead_posterior_a_compra_nao_e_quente(self):
        r = self.run_([L("a@x.invalid", "2026-11-30T00:00:00Z")], [C("P1", "2026-11-28T00:00:00Z", "a@x.invalid")])
        self.assertEqual(r["quente"], 0)
        self.assertEqual(r["nao_atribuida_motivos"], {"lead_posterior_a_compra": 1})

    def test_precedencia_quente_vence_frio_e_nao_duplica(self):
        r = self.run_([L("a@x.invalid", "2026-11-26T00:00:00Z")], [C("P1", "2026-11-28T00:00:00Z", "a@x.invalid", "venda-fria", "cri-F")])
        self.assertEqual((r["quente"], r["frio"], r["compradores_unicos"]), (1, 0, 1))
        self.assertEqual(r["sobreposicao_quente_e_frio"], 1)

    def test_comprador_com_duas_compras_conta_uma_vez(self):
        compras = [C("P1", "2026-11-28T00:00:00Z", "a@x.invalid", "venda-fria"), C("P2", "2026-11-29T00:00:00Z", "A@x.invalid")]
        r = self.run_([], compras)
        self.assertEqual(r["compradores_unicos"], 1)
        self.assertEqual(r["compras_repetidas_do_mesmo_comprador"], 1)
        self.assertEqual(r["frio"], 1)  # classifica pela PRIMEIRA compra

    def test_email_divergente_nao_presume_correspondencia_e_telefone_vai_para_revisao(self):
        leads = [L("maria.silva@x.invalid", "2026-11-26T00:00:00Z", phone="(48) 99999-0001")]
        compras = [C("P1", "2026-11-28T00:00:00Z", "maria.s@outro.invalid", phone="5548999990001")]
        r = self.run_(leads, compras)
        self.assertEqual(r["quente"], 0)
        self.assertEqual(r["nao_atribuida"], 1)
        self.assertEqual(r["possiveis_correspondencias_para_revisao_humana"], 1)

    def test_gmail_so_com_regra_opcional_e_rotulada(self):
        leads = [L("joao.pereira@gmail.com", "2026-11-26T00:00:00Z")]
        compras = [C("P1", "2026-11-28T00:00:00Z", "joaopereira+zion@gmail.com")]
        sem = self.run_(leads, compras)
        self.assertEqual(sem["quente"], 0)                       # sem a regra: nao casa
        self.assertFalse(sem["regra_gmail_ativa"])
        com = self.run_(leads, compras, gmail_rules=True)
        self.assertEqual(com["quente"], 1)
        self.assertEqual(com["match_regra_gmail_opcional"], 1)   # rotulado para conferencia
        self.assertTrue(com["regra_gmail_ativa"])

    def test_gmail_regra_nao_se_aplica_a_outros_dominios(self):
        leads = [L("a.b@empresa.invalid", "2026-11-26T00:00:00Z")]
        r = self.run_(leads, [C("P1", "2026-11-28T00:00:00Z", "ab@empresa.invalid")], gmail_rules=True)
        self.assertEqual(r["quente"], 0)

    def test_teste_e_status_nao_pago_ficam_fora_reembolso_conta_e_marca(self):
        compras = [C("P1", "2026-11-28T00:00:00Z", "a@x.invalid", is_test="1"), C("P2", "2026-11-28T00:00:00Z", "b@x.invalid", status="pending"),
                   C("P3", "2026-11-28T00:00:00Z", "c@x.invalid", status="refunded")]
        r = self.run_([], compras)
        self.assertEqual(r["compradores_unicos"], 1)
        self.assertEqual(r["reembolsados_entre_compradores"], 1)
        self.assertEqual(r["entrada"]["compras_descartadas"], {"teste": 1, "status_nao_pago": 1})

    def test_utm_venda_quente_sem_lead_fica_nao_atribuida_com_motivo(self):
        r = self.run_([], [C("P1", "2026-11-28T00:00:00Z", "a@x.invalid", "venda-quente")])
        self.assertEqual(r["nao_atribuida_motivos"], {"utm_venda_quente_sem_lead_encontrado": 1})

    def test_lead_duplicado_usa_o_mais_antigo(self):
        leads = [L("a@x.invalid", "2026-11-27T00:00:00Z"), L("A@x.invalid", "2026-11-25T00:00:00Z")]
        r = self.run_(leads, [C("P1", "2026-11-28T00:00:00Z", "a@x.invalid")])
        self.assertEqual(r["entrada"]["leads_duplicados_por_email"], 1)
        self.assertEqual(r["tempo_ate_a_compra_dias_quentes"]["mediana"], 3.0)

    def test_coorte_por_data_e_maturidade_7_14_dias(self):
        leads = [L("a@x.invalid", "2026-12-01T10:00:00Z"), L("b@x.invalid", "2026-12-01T11:00:00Z"),
                 L("c@x.invalid", "2026-12-18T10:00:00Z")]
        compras = [C("P1", "2026-12-03T10:00:00Z", "a@x.invalid"), C("P2", "2026-12-15T10:00:00Z", "b@x.invalid")]
        r = self.run_(leads, compras)
        t = {x["coorte"]: x for x in r["coortes"]}
        self.assertEqual(t["2026-12-01"]["leads"], 2)
        self.assertEqual(t["2026-12-01"]["compradores"], 2)
        self.assertEqual(t["2026-12-01"]["conv_7d"], 50.0)    # 1 de 2 comprou em ate 7 dias
        self.assertEqual(t["2026-12-01"]["conv_14d"], 100.0)
        self.assertEqual(t["2026-12-18"]["conv_7d"], "imatura (<7 dias)")  # lead de 2 dias: nao compare com os antigos
        self.assertTrue(t["2026-12-18"]["amostra_pequena"])

    def test_saida_nao_tem_pii(self):
        leads = [L("pessoa.secreta@x.invalid", "2026-11-26T00:00:00Z", phone="48999990001")]
        r = self.run_(leads, [C("PEDIDO-SECRETO-1", "2026-11-28T00:00:00Z", "pessoa.secreta@x.invalid", phone="48999990001")])
        r.pop("_revisao")
        s = json.dumps(r, ensure_ascii=False)
        for proibido in ("pessoa.secreta", "x.invalid", "48999990001", "PEDIDO-SECRETO"):
            self.assertNotIn(proibido, s)

    def test_cli_recusa_csv_dentro_do_repo_e_roda_fora(self):
        dentro = Path(__file__).resolve().parent / "MODELO_clickmax.csv"
        p = subprocess.run([sys.executable, "-I", str(Path(__file__).resolve().parent / "lead_comprador.py"), "--leads", str(dentro), "--compras", str(dentro)], capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("RECUSADO", p.stderr)
        with tempfile.TemporaryDirectory() as d:
            lf, cf = Path(d) / "leads.csv", Path(d) / "compras.csv"
            lf.write_text("email,telefone,created_at,utm_source,utm_medium,utm_campaign,utm_content\na@x.invalid,,2026-11-26T00:00:00Z,facebook,lead_ads,captacao,cri-A\n")
            cf.write_text("order_id,paid_at,value_brl,status,is_test,email,telefone,utm_source,utm_medium,utm_campaign,utm_content\nP1,2026-11-28T00:00:00Z,47.00,paid,0,a@x.invalid,,,,,\n")
            p = subprocess.run([sys.executable, "-I", str(Path(__file__).resolve().parent / "lead_comprador.py"), "--leads", str(lf), "--compras", str(cf), "--as-of", "2026-12-20"], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(json.loads(p.stdout)["quente"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
