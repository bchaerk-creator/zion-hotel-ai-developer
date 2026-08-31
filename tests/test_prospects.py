"""
Testes da carteira de prospects.

Rodam sem ScrapeGraphAI instalado — é justamente a garantia de que o núcleo
não depende dele.
"""

import sys
import unittest
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.prospect import (  # noqa: E402
    BaseLegal, Estagio, Modalidade, Origem, Prospect, Territorio,
)
from src.prospects.icp import inferir_modalidade  # noqa: E402
from src.prospects.scoring import classificar_lead, pontuar_lead  # noqa: E402
from src.prospects.repositorio import RepositorioProspects, gerar_id  # noqa: E402


def fazer_prospect(**kwargs) -> Prospect:
    base = dict(
        id="teste",
        nome="Fazenda Exemplo",
        origem=Origem(fonte="https://exemplo.com.br", tipo="manual"),
    )
    base.update(kwargs)
    return Prospect(**base)


class TestGerarId(unittest.TestCase):
    def test_estavel_e_sem_acento(self):
        self.assertEqual(gerar_id("Pousada Araucária"), "pousada-araucaria")

    def test_mesmo_nome_gera_mesmo_id(self):
        self.assertEqual(gerar_id("Sítio São João"), gerar_id("Sítio São João"))

    def test_empresa_entra_na_chave(self):
        self.assertNotEqual(gerar_id("Ana", "Alfa"), gerar_id("Ana", "Beta"))

    def test_nome_vazio_nao_quebra(self):
        self.assertEqual(gerar_id(""), "sem-nome")


class TestICP(unittest.TestCase):
    """O que sobrou no módulo de ICP: a inferência de modalidade."""

    def test_inferir_modalidade(self):
        self.assertEqual(
            inferir_modalidade(fazer_prospect(territorio=Territorio(area_ha=10))),
            Modalidade.DEVELOPMENT)
        self.assertEqual(
            inferir_modalidade(fazer_prospect(territorio=Territorio(unidades=12))),
            Modalidade.MANAGEMENT)
        self.assertEqual(
            inferir_modalidade(fazer_prospect()),
            Modalidade.INDEFINIDA)


class TestEscalaDoScore(unittest.TestCase):
    """
    O campo `score` guarda o ZION LEAD SCORE (0–100).

    Regressão: ele já teve teto 10, do ICP antigo. O import gravava 81,8 e a
    leitura do banco quebrava na validação.
    """

    def test_score_de_cem_persiste_e_volta(self):
        with TemporaryDirectory() as tmp:
            with RepositorioProspects(Path(tmp) / "c.db") as repo:
                p = pontuar_lead(fazer_prospect(
                    id="alto", modalidade=Modalidade.DEVELOPMENT,
                    territorio=Territorio(uf="SC", municipio="Urubici", area_ha=40),
                    email="a@b.com", site="https://x.com",
                    notas="terreno parado"), destination_score=79)
                self.assertGreater(p.score, 10)
                repo.salvar(p)
                self.assertAlmostEqual(repo.buscar("alto").score, p.score)

    def test_score_acima_de_cem_e_recusado(self):
        from pydantic import ValidationError
        with self.assertRaises(ValidationError):
            fazer_prospect(score=101)


class TestRepositorio(unittest.TestCase):
    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.repo = RepositorioProspects(Path(self._tmp.name) / "carteira.db")

    def tearDown(self):
        self.repo.fechar()
        self._tmp.cleanup()

    def test_salvar_e_buscar(self):
        self.repo.salvar(fazer_prospect(id="p1", nome="Pousada Um"))
        achado = self.repo.buscar("p1")
        self.assertIsNotNone(achado)
        self.assertEqual(achado.nome, "Pousada Um")

    def test_salvar_duas_vezes_atualiza_em_vez_de_duplicar(self):
        self.repo.salvar(fazer_prospect(id="p1", nome="Antes"))
        self.repo.salvar(fazer_prospect(id="p1", nome="Depois"))
        self.assertEqual(self.repo.total(), 1)
        self.assertEqual(self.repo.buscar("p1").nome, "Depois")

    def test_filtrar_por_modalidade_e_uf(self):
        self.repo.salvar(fazer_prospect(
            id="a", modalidade=Modalidade.DEVELOPMENT, territorio=Territorio(uf="SC")))
        self.repo.salvar(fazer_prospect(
            id="b", modalidade=Modalidade.MANAGEMENT, territorio=Territorio(uf="RS")))
        self.assertEqual(len(self.repo.listar(modalidade=Modalidade.DEVELOPMENT)), 1)
        self.assertEqual(len(self.repo.listar(uf="sc")), 1)

    def test_ordena_por_score_decrescente(self):
        self.repo.salvar(fazer_prospect(id="baixo", score=3.0, email="a@b.com"))
        self.repo.salvar(fazer_prospect(id="alto", score=9.0, email="c@d.com"))
        self.assertEqual([p.id for p in self.repo.listar()], ["alto", "baixo"])

    def test_nao_contatar_sai_dos_contataveis(self):
        self.repo.salvar(fazer_prospect(id="ok", email="a@b.com"))
        self.repo.salvar(fazer_prospect(id="opt-out", email="c@d.com", nao_contatar=True))
        ids = [p.id for p in self.repo.listar(apenas_contataveis=True)]
        self.assertIn("ok", ids)
        self.assertNotIn("opt-out", ids)

    def test_sem_canal_de_contato_nao_e_contatavel(self):
        self.repo.salvar(fazer_prospect(id="mudo"))
        self.assertEqual(self.repo.listar(apenas_contataveis=True), [])

    def test_marcar_nao_contatar(self):
        self.repo.salvar(fazer_prospect(id="p1", email="a@b.com"))
        self.assertTrue(self.repo.marcar_nao_contatar("p1"))
        p = self.repo.buscar("p1")
        self.assertTrue(p.nao_contatar)
        self.assertEqual(p.estagio, Estagio.DESCARTADO)
        self.assertFalse(p.contatavel)

    def test_marcar_inexistente_devolve_falso(self):
        self.assertFalse(self.repo.marcar_nao_contatar("fantasma"))

    def test_resumo(self):
        self.repo.salvar(fazer_prospect(id="a", modalidade=Modalidade.DEVELOPMENT, score=8.0))
        self.repo.salvar(fazer_prospect(id="b", modalidade=Modalidade.DEVELOPMENT, score=6.0))
        r = self.repo.resumo()
        self.assertEqual(r["total"], 2)
        self.assertEqual(r["por_modalidade"]["development"], 2)
        self.assertEqual(r["score_medio"], 7.0)

    def test_exportar_csv_omite_nao_contatar(self):
        self.repo.salvar(fazer_prospect(id="ok", nome="Vai", email="a@b.com"))
        self.repo.salvar(fazer_prospect(id="no", nome="Fica", email="c@d.com", nao_contatar=True))
        destino = Path(self._tmp.name) / "saida.csv"
        self.repo.exportar_csv(destino)
        conteudo = destino.read_text(encoding="utf-8")
        self.assertIn("Vai", conteudo)
        self.assertNotIn("Fica", conteudo)

    def test_persiste_entre_conexoes(self):
        caminho = Path(self._tmp.name) / "outra.db"
        with RepositorioProspects(caminho) as repo:
            repo.salvar(fazer_prospect(id="p1", nome="Persistente"))
        with RepositorioProspects(caminho) as repo:
            self.assertEqual(repo.buscar("p1").nome, "Persistente")


class TestConformidade(unittest.TestCase):
    """As guardas de LGPD e de coleta, sem depender do ScrapeGraphAI."""

    def test_dominio_bloqueado_e_recusado(self):
        from src.prospects.coletor import ColetaBloqueada, verificar_url
        with self.assertRaises(ColetaBloqueada):
            verificar_url("https://www.instagram.com/algum-perfil")

    def test_otas_sao_bloqueadas(self):
        """Airbnb, Booking e afins não são coletáveis — decisão, não descuido."""
        from src.prospects.coletor import ColetaBloqueada, verificar_url
        for url in ("https://www.airbnb.com.br/rooms/123",
                    "https://www.booking.com/hotel/br/x.html",
                    "https://www.tripadvisor.com.br/Hotel_Review-x"):
            with self.assertRaises(ColetaBloqueada, msg=url):
                verificar_url(url)

    def test_url_invalida_e_recusada(self):
        from src.prospects.coletor import ColetaBloqueada, verificar_url
        with self.assertRaises(ColetaBloqueada):
            verificar_url("nao-e-url")

    def test_prospects_vencidos(self):
        from src.prospects.coletor import prospects_vencidos
        antigo = fazer_prospect(id="velho", revisar_ate=date.today() - timedelta(days=1))
        novo = fazer_prospect(id="novo", revisar_ate=date.today() + timedelta(days=30))
        vencidos = prospects_vencidos([antigo, novo])
        self.assertEqual([p.id for p in vencidos], ["velho"])

    def test_coletor_sem_biblioteca_avisa_direito(self):
        """Sem scrapegraphai, o erro tem que explicar como instalar."""
        from src.prospects.coletor import Coletor, ColetorIndisponivel
        try:
            import scrapegraphai  # noqa: F401
            self.skipTest("scrapegraphai instalado neste ambiente")
        except ImportError:
            pass
        with self.assertRaises(ColetorIndisponivel) as ctx:
            Coletor()
        self.assertIn("prospects", str(ctx.exception))

    def test_base_legal_padrao_e_legitimo_interesse(self):
        self.assertEqual(fazer_prospect().base_legal, BaseLegal.LEGITIMO_INTERESSE)



class TestRobots(unittest.TestCase):
    """
    Verifica que a guarda de robots.txt realmente distingue permitido de
    proibido — e não apenas nega tudo por falha de rede.
    """

    @classmethod
    def setUpClass(cls):
        import http.server
        import socketserver
        import threading

        robots = (
            b"User-agent: ZionProspects\n"
            b"Disallow: /privado\n"
            b"Allow: /\n"
        )

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                corpo = robots if self.path == "/robots.txt" else b"ok"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(corpo)))
                self.end_headers()
                self.wfile.write(corpo)

            def log_message(self, *_):
                pass

        socketserver.TCPServer.allow_reuse_address = True
        cls.servidor = socketserver.TCPServer(("127.0.0.1", 0), Handler)
        cls.porta = cls.servidor.server_address[1]
        cls.thread = threading.Thread(target=cls.servidor.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()
        cls.servidor.server_close()

    def _url(self, caminho):
        return f"http://127.0.0.1:{self.porta}{caminho}"

    def test_permite_caminho_liberado(self):
        from src.prospects.coletor import robots_permite
        self.assertTrue(robots_permite(self._url("/publico")))

    def test_recusa_caminho_proibido(self):
        from src.prospects.coletor import robots_permite
        self.assertFalse(robots_permite(self._url("/privado/lista")))

    def test_host_inexistente_falha_fechado(self):
        """Erro de rede tem que negar, nunca liberar."""
        from src.prospects.coletor import robots_permite
        self.assertFalse(robots_permite("http://127.0.0.1:1/qualquer"))



if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestScoring(unittest.TestCase):
    """ZION DESTINATION SCORE e ZION LEAD SCORE."""

    def test_faixas_do_destino(self):
        from src.prospects.scoring import classificar_destino
        for score, esperado in ((95, "prioridade estratégica"), (80, "alta prioridade"),
                                (65, "boa oportunidade"), (45, "monitoramento"),
                                (20, "baixa prioridade")):
            self.assertEqual(classificar_destino(score), esperado, msg=score)

    def test_faixas_do_lead(self):
        from src.prospects.scoring import classificar_lead
        for score, esperado in ((95, "A+"), (80, "A"), (65, "B"), (45, "C"), (10, "D")):
            self.assertEqual(classificar_lead(score), esperado, msg=score)
        self.assertEqual(classificar_lead(None), "não pontuado")

    def test_pesos_do_lead_somam_cem(self):
        from src.prospects.scoring import PESOS_LEAD
        self.assertEqual(sum(PESOS_LEAD.values()), 100)

    def test_pesos_do_destino_somam_noventa_e_cinco(self):
        """
        A especificação declara total 100, mas as sete dimensões somam 95.
        Mantemos os pesos verbatim e normalizamos — este teste fixa o fato
        para a divergência não voltar despercebida.
        """
        from src.prospects.scoring import PESOS_DESTINO, TOTAL_DESTINO_BRUTO
        self.assertEqual(sum(PESOS_DESTINO.values()), 95)
        self.assertEqual(TOTAL_DESTINO_BRUTO, 95)

    def test_normalizacao_alcanca_as_faixas_altas(self):
        from src.prospects.scoring import classificar_destino, normalizar_destino
        self.assertEqual(normalizar_destino(95), 100.0)
        self.assertEqual(classificar_destino(95), "prioridade estratégica")
        self.assertEqual(classificar_destino(86), "prioridade estratégica")

    def test_validar_notas_recusa_nota_estourada(self):
        from src.prospects.scoring import validar_notas_destino
        boas = {"demanda": 20, "premium": 15, "natureza": 15, "glamping": 15,
                "imobiliario": 10, "acesso": 10, "ticket": 10}
        validar_notas_destino(boas)  # não levanta
        with self.assertRaises(ValueError):
            validar_notas_destino({**boas, "acesso": 11})
        with self.assertRaises(ValueError):
            validar_notas_destino({k: v for k, v in boas.items() if k != "ticket"})

    def test_lead_score_nunca_passa_de_cem(self):
        from src.prospects.scoring import pontuar_lead
        p = pontuar_lead(fazer_prospect(
            modalidade=Modalidade.DEVELOPMENT,
            territorio=Territorio(uf="SC", municipio="Urubici", area_ha=40),
            email="a@b.com", telefone="48999", instagram="@x", site="https://x.com",
            notas="Terreno parado há 3 anos, quer renda",
        ), destination_score=100)
        self.assertLessEqual(p.score, 100.0)
        self.assertEqual(len(p.score_motivos), 7)

    def test_destino_melhor_puxa_o_lead_para_cima(self):
        from src.prospects.scoring import pontuar_lead
        def montar():
            return fazer_prospect(modalidade=Modalidade.DEVELOPMENT,
                                  territorio=Territorio(uf="SC", area_ha=40),
                                  email="a@b.com")
        forte = pontuar_lead(montar(), destination_score=90)
        fraco = pontuar_lead(montar(), destination_score=40)
        self.assertGreater(forte.score, fraco.score)

    def test_nao_contatar_zera_o_lead_score(self):
        from src.prospects.scoring import pontuar_lead
        p = pontuar_lead(fazer_prospect(
            nao_contatar=True, territorio=Territorio(uf="SC", area_ha=40),
            email="a@b.com"), destination_score=90)
        self.assertEqual(p.score, 0.0)

    def test_produto_recomendado_por_modalidade(self):
        from src.prospects.scoring import produto_recomendado
        grande = fazer_prospect(modalidade=Modalidade.DEVELOPMENT,
                                territorio=Territorio(area_ha=40))
        pequeno = fazer_prospect(modalidade=Modalidade.DEVELOPMENT,
                                 territorio=Territorio(area_ha=4))
        self.assertIn("diagnóstico", produto_recomendado(grande))
        self.assertIn("bubble", produto_recomendado(pequeno).lower())


class TestDestinos(unittest.TestCase):
    def test_sessenta_destinos_carregam(self):
        from src.prospects.destinos import carregar
        self.assertEqual(len(carregar()), 60)

    def test_todo_destino_tem_score_coerente(self):
        """A soma das sete parcelas tem que bater com o score gravado."""
        from src.prospects.destinos import carregar
        from src.prospects.scoring import validar_notas_destino
        for d in carregar():
            validar_notas_destino(d.notas)
            self.assertEqual(sum(d.notas.values()), d.destination_score,
                             msg=f"{d.municipio}/{d.uf}")

    def test_top_devolve_ordenado(self):
        from src.prospects.destinos import top
        cinco = top("SC", 5)
        self.assertEqual(len(cinco), 5)
        scores = [d.destination_score for d in cinco]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_vinte_por_uf(self):
        from src.prospects.destinos import listar
        for uf in ("SC", "PR", "RS"):
            self.assertEqual(len(listar(uf=uf)), 20, msg=uf)

    def test_buscar_municipio(self):
        from src.prospects.destinos import buscar
        self.assertIsNotNone(buscar("Urubici", "SC"))
        self.assertIsNone(buscar("Narnia", "SC"))
