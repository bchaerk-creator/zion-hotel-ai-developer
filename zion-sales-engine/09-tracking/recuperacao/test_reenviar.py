import hashlib
import io
import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, Path(__file__).resolve().parent.as_posix())  # necessario com python3 -I (modo isolado)

import reenviar_compras as R

HERE = Path(__file__).parent
EXAMPLE = HERE / "compras.csv.example"
NOW = R.parse_time("2026-11-25T12:00:00Z")


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


class FakeGraph:
    def __init__(self, fail=False):
        self.calls = []
        outer = self

        class H(BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["content-length"])))
                outer.calls.append((self.path, body))
                code = 500 if fail else 200
                self.send_response(code)
                self.send_header("content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"events_received": 0 if fail else len(body["data"]), "fbtrace_id": "FAKE"}).encode())

            def log_message(self, *a):
                pass

        self.srv = HTTPServer(("127.0.0.1", 0), H)
        self.base = f"http://127.0.0.1:{self.srv.server_port}"
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def close(self):
        self.srv.shutdown()


def args(csv_path, send=False, ledger=None):
    return SimpleNamespace(csv=str(csv_path), send=send, ledger=ledger, allow_inside_repo=True)


class Tests(unittest.TestCase):
    def collect(self, a, env, now=NOW):
        buf = []
        code = R.run(a, env=env, now=now, out=buf.append)
        return code, "\n".join(buf)

    def test_dry_run_nao_toca_a_rede_e_nao_imprime_dado_pessoal(self):
        def no_net(*a, **k):
            raise AssertionError("dry-run nao pode usar a rede")
        buf = []
        code = R.run(args(EXAMPLE), env={}, now=NOW, out=buf.append, opener=no_net)
        text = "\n".join(buf)
        self.assertEqual(code, 0)
        self.assertIn("DRY-RUN: 2 pronta(s), 0 bloqueada(s)", text)
        for bad in ("example.com", "example.org", "maria", "5548999990000", "98888"):
            self.assertNotIn(bad, text.lower())

    def test_hash_e_valor_corretos(self):
        row = {"event_id": "T1", "paid_at": "2026-11-23T10:05:00Z", "value_brl": "97.00", "currency": "BRL",
               "email": "  Maria.Exemplo@Example.COM ", "phone": "(48) 99999-0000", "fullname": "Maria Exemplo da Silva"}
        ev, why = R.build_event(row, NOW)
        self.assertIsNone(why)
        self.assertEqual(ev["user_data"]["em"], [sha("maria.exemplo@example.com")])
        self.assertEqual(ev["user_data"]["ph"], [sha("5548999990000")])
        self.assertEqual(ev["custom_data"]["value"], 97.0)
        self.assertEqual(ev["custom_data"]["currency"], "BRL")
        self.assertEqual(ev["event_id"], "T1")
        self.assertEqual(ev["event_time"], R.parse_time("2026-11-23T10:05:00Z"))
        self.assertEqual(ev["action_source"], "website")

    def test_valor_com_virgula_e_faixa(self):
        base = {"event_id": "T", "paid_at": "2026-11-23T10:05:00Z", "email": "a@example.com"}
        ev, _ = R.build_event({**base, "value_brl": "97,00"}, NOW)
        self.assertEqual(ev["custom_data"]["value"], 97.0)
        self.assertEqual(R.build_event({**base, "value_brl": "0.97"}, NOW)[1][:19], "valor_fora_da_faixa")
        self.assertEqual(R.build_event({**base, "value_brl": "9700"}, NOW)[1][:19], "valor_fora_da_faixa")

    def test_bloqueia_mais_de_7_dias_e_sem_correspondencia(self):
        base = {"event_id": "T", "value_brl": "97", "email": "a@example.com"}
        self.assertEqual(R.build_event({**base, "paid_at": "2026-11-10T00:00:00Z"}, NOW)[1], "mais_de_7_dias_o_meta_recusa")
        self.assertEqual(R.build_event({"event_id": "T", "value_brl": "97", "paid_at": "2026-11-23T10:05:00Z"}, NOW)[1], "sem_dado_para_correspondencia")

    def test_nao_atribui_sem_dado(self):
        ev, _ = R.build_event({"event_id": "T", "value_brl": "97", "paid_at": "2026-11-23T10:05:00Z", "email": "a@example.com"}, NOW)
        for k in R.UTM_COLS:
            self.assertNotIn(k, ev["custom_data"])
        self.assertNotIn("fbc", ev["user_data"])
        ev2, _ = R.build_event({"event_id": "T", "value_brl": "97", "paid_at": "2026-11-23T10:05:00Z", "email": "a@example.com", "utm_campaign": "c1", "fbc": "fb.1.1.AB"}, NOW)
        self.assertEqual(ev2["custom_data"]["utm_campaign"], "c1")
        self.assertEqual(ev2["user_data"]["fbc"], "fb.1.1.AB")

    def test_send_envia_ao_graph_simulado_e_e_idempotente(self):
        g = FakeGraph()
        try:
            with tempfile.TemporaryDirectory() as d:
                led = Path(d) / "ids.txt"
                env = {"META_PIXEL_ID": "999", "META_ACCESS_TOKEN": "TOKEN_FALSO", "META_GRAPH_BASE": g.base}
                code, text = self.collect(args(EXAMPLE, send=True, ledger=str(led)), env)
                self.assertEqual(code, 0, text)
                self.assertEqual(len(g.calls), 1)
                self.assertEqual(len(g.calls[0][1]["data"]), 2)
                self.assertNotIn("test_event_code", g.calls[0][1])
                self.assertNotIn("TOKEN_FALSO", text)
                self.assertEqual(led.read_text().split(), ["TX-FICTICIA-0001", "TX-FICTICIA-0002"])
                code, text = self.collect(args(EXAMPLE, send=True, ledger=str(led)), env)
                self.assertIn("JA ENVIADA", text)
                self.assertEqual(len(g.calls), 1, "segundo envio nao chama o Meta")
        finally:
            g.close()

    def test_modo_teste_envia_codigo_e_nao_grava_controle(self):
        g = FakeGraph()
        try:
            with tempfile.TemporaryDirectory() as d:
                led = Path(d) / "ids.txt"
                env = {"META_PIXEL_ID": "999", "META_ACCESS_TOKEN": "T", "META_GRAPH_BASE": g.base, "META_TEST_EVENT_CODE": "TEST123"}
                code, text = self.collect(args(EXAMPLE, send=True, ledger=str(led)), env)
                self.assertEqual(code, 0)
                self.assertEqual(g.calls[0][1]["test_event_code"], "TEST123")
                self.assertFalse(led.exists())
        finally:
            g.close()

    def test_falha_do_meta_nao_atualiza_controle(self):
        g = FakeGraph(fail=True)
        try:
            with tempfile.TemporaryDirectory() as d:
                led = Path(d) / "ids.txt"
                env = {"META_PIXEL_ID": "999", "META_ACCESS_TOKEN": "T", "META_GRAPH_BASE": g.base}
                code, text = self.collect(args(EXAMPLE, send=True, ledger=str(led)), env)
                self.assertEqual(code, 1)
                self.assertFalse(led.exists())
        finally:
            g.close()

    def test_send_sem_variaveis_de_ambiente_para(self):
        code, text = self.collect(args(EXAMPLE, send=True), {})
        self.assertEqual(code, 2)
        self.assertIn("META_ACCESS_TOKEN", text)

    def test_recusa_csv_dentro_do_repositorio(self):
        a = SimpleNamespace(csv=str(EXAMPLE), send=False, ledger=None, allow_inside_repo=False)
        code, text = self.collect(a, {})
        self.assertEqual(code, 2)
        self.assertIn("RECUSADO", text)

    def test_csv_fora_do_repo_e_aceito(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.csv"
            p.write_text(EXAMPLE.read_text())
            a = SimpleNamespace(csv=str(p), send=False, ledger=None, allow_inside_repo=False)
            code, text = self.collect(a, {})
            self.assertEqual(code, 0)
            self.assertIn("DRY-RUN", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
