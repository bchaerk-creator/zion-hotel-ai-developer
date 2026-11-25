"""Testes com DADOS FICTÍCIOS. Rodar: python3 -I tests/test_score.py (de dentro de diagnostico/)."""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import score as S

# Exemplos fictícios, um por faixa (dados fictícios; não representam ninguém).
EX = {
    "F1": {"situacao": "terreno", "produto": "nao_definido", "local": "nada", "documentos": "nao_sei",
           "numeros": "nenhum", "apresentacao": "nada"},
    "F1b": {"situacao": "ideia", "produto": "varias_ideias", "numeros": "nenhum", "apresentacao": "nada"},
    "F2": {"situacao": "terreno", "produto": "tipo_escolhido", "local": "tamanho_localizacao", "documentos": "alguns",
           "numeros": "estimativa_de_cabeca", "apresentacao": "anotacoes_soltas"},
    "F3": {"situacao": "hospedagem", "produto": "tipo_escolhido", "local": "acesso_entorno", "documentos": "reunidos",
           "numeros": "planilha_parcial", "apresentacao": "resumo_simples"},
    "F4": {"situacao": "terreno", "produto": "conceito_descrito", "local": "levantamento_feito", "documentos": "reunidos",
           "numeros": "planilha_completa", "apresentacao": "material_organizado"},
}


class T(unittest.TestCase):
    def test_pesos_somam_100(self):
        self.assertEqual(sum(c["max"] for c in S.CRITERIOS.values()), 100)
        for c in S.CRITERIOS.values():
            self.assertEqual(max(c["opcoes"].values()), c["max"])
            self.assertEqual(min(c["opcoes"].values()), 0)

    def test_faixas_cobrem_0_a_100_sem_buraco(self):
        for n in range(101):
            S.faixa_de(n)
        self.assertEqual(S.FAIXAS[0][0], 0)
        self.assertEqual(S.FAIXAS[-1][1], 100)
        for a, b in zip(S.FAIXAS, S.FAIXAS[1:]):
            self.assertEqual(a[1] + 1, b[0])

    def test_faixa_esperada_por_exemplo(self):
        esperado = {"F1": ("F1", 0), "F1b": ("F1", 11), "F2": ("F2", 43), "F3": ("F3", 74), "F4": ("F4", 100)}
        for k, (f, n) in esperado.items():
            r = S.diagnosticar(EX[k])
            self.assertEqual((r["faixa"], r["score"]), (f, n), k)

    def test_conta_independente(self):
        # F3: produto 14 + local 14 + docs 15 + números 17 + apresentação 14 = 74 de 100
        r = S.diagnosticar(EX["F3"])
        self.assertEqual((r["pontos"], r["pontos_maximos"]), (74, 100))
        # F1b sem terreno: 7 + 0 + 0 = 7 de 65 -> 11
        r = S.diagnosticar(EX["F1b"])
        self.assertEqual((r["pontos"], r["pontos_maximos"], r["score"]), (7, 65, 11))

    def test_sem_terreno_nao_penaliza(self):
        # Mesmo estágio relativo: sem terreno com o máximo em tudo = 100, não 65.
        r = S.diagnosticar({"situacao": "ideia", "produto": "conceito_descrito", "numeros": "planilha_completa",
                            "apresentacao": "material_organizado"})
        self.assertEqual(r["score"], 100)
        self.assertEqual(r["faixa"], "F4")

    def test_monotonico(self):
        # Melhorar qualquer resposta nunca reduz a nota.
        base = dict(EX["F2"])
        n0 = S.diagnosticar(base)["score"]
        for c in S.ORDEM:
            ops = sorted(S.CRITERIOS[c]["opcoes"].items(), key=lambda kv: kv[1])
            ant = -1
            for cod, _ in ops:
                b = dict(base); b[c] = cod
                n = S.diagnosticar(b)["score"]
                self.assertGreaterEqual(n, ant)
                ant = n
        self.assertEqual(n0, S.diagnosticar(base)["score"])

    def test_nao_mede_valor_nem_capital(self):
        for chave in ("valor_terreno", "capital", "localizacao", "nome", "telefone", "email", "documento_enviado"):
            r = dict(EX["F2"]); r[chave] = "x"
            with self.assertRaises(ValueError):
                S.diagnosticar(r)

    def test_respostas_invalidas(self):
        with self.assertRaises(ValueError):
            S.diagnosticar({"situacao": "terreno", "produto": "otimo"})
        r = dict(EX["F1b"]); r["local"] = "nada"
        with self.assertRaises(ValueError):  # critério não se aplica
            S.diagnosticar(r)
        r = dict(EX["F2"]); del r["numeros"]
        with self.assertRaises(ValueError):
            S.diagnosticar(r)
        with self.assertRaises(ValueError):
            S.diagnosticar({"situacao": "investidor"})

    def test_parecer_seguro_em_todas_as_combinacoes(self):
        # Varre TODAS as combinações possíveis de respostas.
        import itertools
        total = 0
        for sit in S.SITUACOES:
            crit = [c for c in S.ORDEM if sit in S.CRITERIOS[c]["aplica"]]
            for combo in itertools.product(*[list(S.CRITERIOS[c]["opcoes"]) for c in crit]):
                r = {"situacao": sit}; r.update(dict(zip(crit, combo)))
                out = S.diagnosticar(r)
                txt = out["parecer"].lower()
                for p in S.PALAVRAS_PROIBIDAS:
                    self.assertNotIn(p, txt, (p, r))
                self.assertIn(S.LIMITE, out["parecer"])
                self.assertIn("possibilidade, sujeita à análise", out["parecer"])
                self.assertTrue(0 <= out["score"] <= 100)
                self.assertIn("{nome}", out["parecer"])
                total += 1
        # terreno/hospedagem: 4*4*3*4*4=768 cada; ideia/aprender: 4*4*4=64 cada
        self.assertEqual(total, 768 * 2 + 64 * 2)
        print("combinações varridas:", total)

    def test_parecer_por_faixa_tem_linguagem_de_estagio(self):
        r1 = S.diagnosticar(EX["F1"])["parecer"]
        self.assertIn("muito preliminares", r1)
        self.assertIn("potenciais parceiros e investidores", r1)
        self.assertIn("Mini Mentoria de Estruturação Zion", r1)
        r4 = S.diagnosticar(EX["F4"])["parecer"]
        self.assertIn("A decisão é sua", r4)
        r1b = S.diagnosticar(EX["F1b"])["parecer"]
        self.assertIn("a ideia e o projeto", r1b)
        self.assertNotIn("e a área", r1b)

    def test_prioridades_e_onde(self):
        r = S.diagnosticar(EX["F2"])
        self.assertEqual(len(r["prioridades"]), 2)
        self.assertIn("Na Mini Mentoria você trabalha isso em", r["parecer"])
        r = S.diagnosticar(EX["F4"])
        self.assertEqual(r["prioridades"], [])
        self.assertNotIn("Na Mini Mentoria você trabalha", r["parecer"])

    def test_explicacao_transparente(self):
        r = S.diagnosticar(EX["F1b"])
        t = S.explicar(r)
        self.assertIn("não se aplica ao seu caso", t)
        self.assertIn("Nota: 11 de 100", t)
        self.assertIn("revisão por uma pessoa", t)
        self.assertIn("valor da área", t)

    def test_crm(self):
        r = S.diagnosticar(EX["F3"])
        self.assertEqual(r["crm"]["campos"]["diag_faixa"], "F3")
        self.assertEqual(r["crm"]["etiqueta"], "DIAG | F3 PROJETO EM MONTAGEM")
        self.assertIn("revisão", r["revisao_humana"])
        for v in r["crm"]["campos"].values():
            self.assertNotIn("@", str(v))

    def test_determinismo(self):
        self.assertEqual(S.diagnosticar(EX["F3"]), S.diagnosticar(dict(EX["F3"])))


if __name__ == "__main__":
    unittest.main(verbosity=2)
