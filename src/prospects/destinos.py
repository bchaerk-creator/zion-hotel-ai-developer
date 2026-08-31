"""
Mapa de destinos turísticos por estado.

Cada destino é uma praça de prospecção: define onde procurar pousada, hotel,
terreno e imobiliária. A relevância para a Zion não é o tamanho do fluxo — é o
quanto o destino comporta o modelo de poucas unidades e ticket alto.

Origem do dado: ver `docs/PROSPECCAO.md`. O arquivo em data/destinos/ foi
montado a partir de conhecimento da geografia turística brasileira e **precisa
ser validado contra o Mapa do Turismo Brasileiro vigente** (MTur) antes de
virar meta comercial.
"""

import csv
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from src.config import DATA_DIR

logger = logging.getLogger(__name__)

DIRETORIO = DATA_DIR / "destinos"

RELEVANCIA_ORDEM = {"alta": 0, "media": 1, "baixa": 2}


@dataclass(frozen=True)
class Destino:
    """Uma praça de prospecção."""

    uf: str
    rank_uf: int
    municipio: str
    regiao_turistica: str
    vocacao: str
    bioma: str
    sazonalidade: str
    relevancia_zion: str
    nota: str
    demanda: int = 0
    premium: int = 0
    natureza: int = 0
    glamping: int = 0
    imobiliario: int = 0
    acesso: int = 0
    ticket: int = 0
    destination_score: int = 0

    @property
    def prioritario(self) -> bool:
        return self.relevancia_zion == "alta"

    @property
    def classificacao(self) -> str:
        """Faixa de prioridade do ZION DESTINATION SCORE."""
        from src.prospects.scoring import classificar_destino
        return classificar_destino(self.destination_score)

    @property
    def notas(self) -> Dict[str, int]:
        """As sete parcelas que compõem o score."""
        return {
            "demanda": self.demanda, "premium": self.premium,
            "natureza": self.natureza, "glamping": self.glamping,
            "imobiliario": self.imobiliario, "acesso": self.acesso,
            "ticket": self.ticket,
        }


def carregar(arquivo: Optional[Path] = None) -> List[Destino]:
    """
    Carrega os destinos. Sem argumento, lê todos os CSVs de data/destinos/.
    """
    arquivos = [Path(arquivo)] if arquivo else sorted(DIRETORIO.glob("destinos_*.csv"))
    if not arquivos:
        logger.warning("nenhum arquivo de destinos em %s", DIRETORIO)
        return []

    destinos: List[Destino] = []
    for caminho in arquivos:
        with caminho.open(encoding="utf-8") as fh:
            for linha in csv.DictReader(fh):
                destinos.append(Destino(
                    uf=linha["uf"].strip().upper(),
                    rank_uf=int(linha["rank_uf"]),
                    municipio=linha["municipio"].strip(),
                    regiao_turistica=linha["regiao_turistica"].strip(),
                    vocacao=linha["vocacao"].strip(),
                    bioma=linha["bioma"].strip(),
                    sazonalidade=linha["sazonalidade"].strip(),
                    relevancia_zion=linha["relevancia_zion"].strip().lower(),
                    nota=linha["nota"].strip(),
                    demanda=int(linha.get("demanda") or 0),
                    premium=int(linha.get("premium") or 0),
                    natureza=int(linha.get("natureza") or 0),
                    glamping=int(linha.get("glamping") or 0),
                    imobiliario=int(linha.get("imobiliario") or 0),
                    acesso=int(linha.get("acesso") or 0),
                    ticket=int(linha.get("ticket") or 0),
                    destination_score=int(linha.get("destination_score") or 0),
                ))
    return destinos


def listar(
    uf: Optional[str] = None,
    relevancia: Optional[str] = None,
    bioma: Optional[str] = None,
    por_relevancia: bool = False,
) -> List[Destino]:
    """Filtra e ordena os destinos."""
    itens = carregar()

    if uf:
        itens = [d for d in itens if d.uf == uf.strip().upper()]
    if relevancia:
        itens = [d for d in itens if d.relevancia_zion == relevancia.strip().lower()]
    if bioma:
        alvo = bioma.strip().lower()
        itens = [d for d in itens if alvo in d.bioma.lower()]

    if por_relevancia:
        itens.sort(key=lambda d: (-d.destination_score, d.uf))
    else:
        itens.sort(key=lambda d: (d.uf, -d.destination_score))
    return itens


def top(uf: str, n: int = 5) -> List[Destino]:
    """Os N destinos de maior Destination Score na UF."""
    return sorted(listar(uf=uf), key=lambda d: -d.destination_score)[:n]


def buscar(municipio: str, uf: str) -> Optional[Destino]:
    """Encontra um destino pelo início do nome."""
    alvo = municipio.strip().lower()
    for d in listar(uf=uf):
        if d.municipio.lower().startswith(alvo):
            return d
    return None


def resumo() -> Dict[str, dict]:
    """Contagem por UF e por relevância."""
    itens = carregar()
    saida: Dict[str, dict] = {}
    for d in itens:
        bloco = saida.setdefault(d.uf, {"total": 0, "alta": 0, "media": 0, "baixa": 0})
        bloco["total"] += 1
        if d.relevancia_zion in bloco:
            bloco[d.relevancia_zion] += 1
    return saida


def consultas_prospeccao(destino: Destino) -> Dict[str, List[str]]:
    """
    Monta as buscas que abrem a prospecção num destino.

    Devolve termos de busca, não URLs: quem escolhe a fonte é a pessoa, depois
    de conferir se o site permite coleta. O coletor recusa qualquer domínio
    bloqueado e consulta robots.txt de todo modo.
    """
    cidade = f"{destino.municipio} {destino.uf}"
    return {
        "hospedagem": [
            f"pousada {cidade} site oficial contato",
            f"hotel boutique {cidade} contato comercial",
            f"glamping {cidade}",
        ],
        "terreno": [
            f"terreno rural à venda {cidade} hectares",
            f"fazenda à venda {cidade}",
            f"área turística à venda {destino.regiao_turistica}",
        ],
        "imobiliaria": [
            f"imobiliária {cidade} CRECI rural",
            f"corretor de imóveis rurais {destino.regiao_turistica}",
        ],
        "institucional": [
            f"ABIH {destino.uf} associados",
            f"sindicato de hotéis {destino.regiao_turistica}",
            f"convention bureau {destino.regiao_turistica}",
            f"secretaria de turismo {destino.municipio}",
        ],
    }
