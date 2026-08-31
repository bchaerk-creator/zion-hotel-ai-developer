"""
Coleta de prospects a partir de páginas públicas, via ScrapeGraphAI.

O ScrapeGraphAI é dependência **opcional**: a carteira, a pontuação e a
exportação funcionam sem ele. Só a coleta automática exige.

    pip install -e ".[prospects]"    # requer Python 3.12+

Guardas embutidas — não são enfeite, são o que separa prospecção B2B legítima
de raspagem indiscriminada:

* respeita robots.txt do domínio antes de qualquer requisição;
* intervalo mínimo entre requisições ao mesmo host;
* registra a URL de origem em todo registro produzido;
* recusa domínios na lista de bloqueio (redes sociais, agregadores de CPF).
"""

import logging
import time
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

from src.config import OPENAI_API_KEY, ZION_MODEL
from src.models.prospect import BaseLegal, Origem, Prospect, Territorio
from src.prospects.icp import inferir_modalidade
from src.prospects.scoring import pontuar_lead
from src.prospects.repositorio import gerar_id

logger = logging.getLogger(__name__)

INTERVALO_MINIMO_S = 2.0
RETENCAO_DIAS = 365

# Domínios que não raspamos, por decisão nossa e não por limitação técnica:
# ou proíbem em termos de uso, ou concentram dado pessoal que a prospecção
# B2B da Zion não precisa.
DOMINIOS_BLOQUEADOS = {
    # Redes sociais: termos de uso proíbem extração e o dado é majoritariamente
    # de pessoa física.
    "facebook.com", "instagram.com", "linkedin.com", "x.com", "twitter.com",
    "tiktok.com", "whatsapp.com",
    # OTAs: os termos proíbem extração de dados de anfitrião e de anúncio, as
    # duas litigam contra scrapers, e o anfitrião típico é pessoa física — sem
    # base legal para prospecção fria.
    "airbnb.com", "airbnb.com.br", "booking.com", "expedia.com",
    "vrbo.com", "hoteis.com", "despegar.com.br", "tripadvisor.com",
    "tripadvisor.com.br",
}

ESQUEMA_EXTRACAO = """
Extraia os estabelecimentos de hospedagem ou anúncios de terreno rural desta
página. Para cada um retorne um objeto com as chaves:
  nome, empresa, site, email, telefone, municipio, uf, area_ha, unidades, notas
Use null onde a informação não estiver na página. Não invente nenhum valor.
Retorne uma lista sob a chave "resultados".
"""


class ColetorIndisponivel(RuntimeError):
    """ScrapeGraphAI não está instalado neste ambiente."""


class ColetaBloqueada(RuntimeError):
    """A URL não pode ser coletada (robots.txt ou domínio bloqueado)."""


def _dominio(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def robots_permite(url: str, user_agent: str = "ZionProspects") -> bool:
    """
    Consulta o robots.txt do domínio.

    Erro de rede devolve False: na dúvida não coletamos, porque o custo de
    raspar indevidamente é maior que o de perder uma fonte.
    """
    partes = urlparse(url)
    if not partes.scheme or not partes.netloc:
        return False
    try:
        rp = RobotFileParser()
        rp.set_url(f"{partes.scheme}://{partes.netloc}/robots.txt")
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as erro:
        logger.warning("robots.txt de %s ilegível (%s) — tratando como proibido", partes.netloc, erro)
        return False


def verificar_url(url: str) -> None:
    """Levanta ColetaBloqueada se a URL não puder ser coletada."""
    dom = _dominio(url)
    if not dom:
        raise ColetaBloqueada(f"URL inválida: {url}")
    if any(dom == b or dom.endswith("." + b) for b in DOMINIOS_BLOQUEADOS):
        raise ColetaBloqueada(f"{dom} está na lista de bloqueio da Zion")
    if not robots_permite(url):
        raise ColetaBloqueada(f"robots.txt de {dom} não permite esta coleta")


class Coletor:
    """Extrai prospects de páginas públicas usando ScrapeGraphAI."""

    def __init__(self, modelo: Optional[str] = None, api_key: Optional[str] = None):
        self.modelo = modelo or ZION_MODEL
        self.api_key = api_key or OPENAI_API_KEY
        self._ultimo_acesso: Dict[str, float] = {}

        try:
            from scrapegraphai.graphs import SmartScraperGraph  # noqa: F401
        except ImportError as erro:
            raise ColetorIndisponivel(
                "ScrapeGraphAI não instalado. Rode: pip install -e \".[prospects]\" "
                "(requer Python 3.12+)."
            ) from erro

        if not self.api_key:
            raise ColetorIndisponivel("OPENAI_API_KEY não configurada — a coleta usa LLM.")

    def _respeitar_intervalo(self, url: str) -> None:
        dom = _dominio(url)
        agora = time.monotonic()
        anterior = self._ultimo_acesso.get(dom)
        if anterior is not None:
            espera = INTERVALO_MINIMO_S - (agora - anterior)
            if espera > 0:
                time.sleep(espera)
        self._ultimo_acesso[dom] = time.monotonic()

    def coletar(self, url: str, prompt: Optional[str] = None) -> List[Prospect]:
        """
        Coleta prospects de uma URL.

        Levanta ColetaBloqueada se robots.txt ou a lista de bloqueio proibirem.
        """
        from scrapegraphai.graphs import SmartScraperGraph

        verificar_url(url)
        self._respeitar_intervalo(url)

        grafo = SmartScraperGraph(
            prompt=prompt or ESQUEMA_EXTRACAO,
            source=url,
            config={
                "llm": {"api_key": self.api_key, "model": f"openai/{self.modelo}"},
                "verbose": False,
                "headless": True,
            },
        )

        bruto = grafo.run()
        itens = bruto.get("resultados", bruto) if isinstance(bruto, dict) else bruto
        if not isinstance(itens, list):
            logger.warning("resposta inesperada de %s: %r", url, type(itens))
            return []

        return [p for p in (self._para_prospect(i, url) for i in itens) if p]

    def coletar_muitos(self, urls: List[str], prompt: Optional[str] = None) -> List[Prospect]:
        """Coleta várias URLs. Uma falha não derruba as demais."""
        encontrados: List[Prospect] = []
        for url in urls:
            try:
                achados = self.coletar(url, prompt)
                encontrados.extend(achados)
                logger.info("%s -> %d prospects", url, len(achados))
            except ColetaBloqueada as erro:
                logger.warning("pulando %s: %s", url, erro)
            except Exception as erro:
                logger.error("falha em %s: %s", url, erro)
        return encontrados

    @staticmethod
    def _para_prospect(item: dict, url: str) -> Optional[Prospect]:
        """Converte um item extraído em Prospect já pontuado."""
        if not isinstance(item, dict):
            return None

        nome = (item.get("nome") or item.get("empresa") or "").strip()
        if not nome:
            return None

        def numero(chave, conversor):
            valor = item.get(chave)
            try:
                return conversor(valor) if valor not in (None, "", "null") else None
            except (TypeError, ValueError):
                return None

        prospect = Prospect(
            id=gerar_id(nome, item.get("empresa")),
            nome=nome,
            empresa=(item.get("empresa") or None),
            email=(item.get("email") or None),
            telefone=(item.get("telefone") or None),
            site=(item.get("site") or None),
            territorio=Territorio(
                municipio=(item.get("municipio") or None),
                uf=(item.get("uf") or None),
                area_ha=numero("area_ha", float),
                unidades=numero("unidades", int),
            ),
            origem=Origem(fonte=url, tipo="web", coletado_por="scrapegraphai"),
            base_legal=BaseLegal.LEGITIMO_INTERESSE,
            revisar_ate=date.today() + timedelta(days=RETENCAO_DIAS),
            notas=(item.get("notas") or None),
        )
        prospect.modalidade = inferir_modalidade(prospect)
        return pontuar_lead(prospect)


def prospects_vencidos(prospects: List[Prospect], hoje: Optional[date] = None) -> List[Prospect]:
    """
    Devolve os registros que passaram da data de revisão.

    A LGPD manda não guardar dado além do necessário (Art. 15, I). Sem uma
    varredura periódica, uma carteira de prospecção vira arquivo morto de
    dado pessoal.
    """
    hoje = hoje or date.today()
    return [p for p in prospects if p.revisar_ate and p.revisar_ate < hoje]
