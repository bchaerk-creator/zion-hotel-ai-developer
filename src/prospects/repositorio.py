"""
Repositório de prospects em SQLite.

Sem dependência nova: usa apenas sqlite3 da biblioteca padrão. O ScrapeGraphAI
é opcional e só entra no coletor — a carteira funciona sem ele.
"""

import json
import logging
import re
import sqlite3
import unicodedata
from datetime import date, datetime
from pathlib import Path
from typing import Iterable, Iterator, List, Optional

from src.config import DATA_DIR
from src.models.prospect import Estagio, Modalidade, Prospect

logger = logging.getLogger(__name__)

CAMINHO_PADRAO = DATA_DIR / "prospects" / "carteira.db"

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS prospects (
    id            TEXT PRIMARY KEY,
    nome          TEXT NOT NULL,
    empresa       TEXT,
    modalidade    TEXT NOT NULL,
    estagio       TEXT NOT NULL,
    uf            TEXT,
    municipio     TEXT,
    score         REAL,
    nao_contatar  INTEGER NOT NULL DEFAULT 0,
    atualizado_em TEXT NOT NULL,
    payload       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_prospects_modalidade ON prospects (modalidade);
CREATE INDEX IF NOT EXISTS ix_prospects_estagio    ON prospects (estagio);
CREATE INDEX IF NOT EXISTS ix_prospects_uf         ON prospects (uf);
CREATE INDEX IF NOT EXISTS ix_prospects_score      ON prospects (score DESC);
"""


def gerar_id(nome: str, empresa: Optional[str] = None) -> str:
    """
    Deriva um id estável a partir do nome (e da empresa, quando houver).

    Estável importa: é o que faz a mesma pessoa coletada duas vezes de fontes
    diferentes cair no mesmo registro em vez de duplicar a carteira.
    """
    bruto = f"{empresa or ''} {nome}".strip()
    sem_acento = unicodedata.normalize("NFKD", bruto).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", sem_acento.lower()).strip("-")
    return slug or "sem-nome"


def _serializar(valor):
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    raise TypeError(f"não sei serializar {type(valor)}")


class RepositorioProspects:
    """Carteira de prospects persistida em SQLite."""

    def __init__(self, caminho: Optional[Path] = None):
        self.caminho = Path(caminho) if caminho else CAMINHO_PADRAO
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self._con = sqlite3.connect(self.caminho)
        self._con.row_factory = sqlite3.Row
        self._con.executescript(_ESQUEMA)
        self._con.commit()

    # ------------------------------------------------------------ escrita

    def salvar(self, prospect: Prospect) -> Prospect:
        """Insere ou atualiza um prospect. O id decide qual dos dois."""
        prospect.atualizado_em = datetime.now()
        payload = json.dumps(prospect.model_dump(mode="json"), ensure_ascii=False, default=_serializar)

        self._con.execute(
            """
            INSERT INTO prospects
                (id, nome, empresa, modalidade, estagio, uf, municipio,
                 score, nao_contatar, atualizado_em, payload)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET
                nome=excluded.nome, empresa=excluded.empresa,
                modalidade=excluded.modalidade, estagio=excluded.estagio,
                uf=excluded.uf, municipio=excluded.municipio,
                score=excluded.score, nao_contatar=excluded.nao_contatar,
                atualizado_em=excluded.atualizado_em, payload=excluded.payload
            """,
            (
                prospect.id, prospect.nome, prospect.empresa,
                prospect.modalidade.value, prospect.estagio.value,
                prospect.territorio.uf, prospect.territorio.municipio,
                prospect.score, int(prospect.nao_contatar),
                prospect.atualizado_em.isoformat(), payload,
            ),
        )
        self._con.commit()
        return prospect

    def salvar_muitos(self, prospects: Iterable[Prospect]) -> int:
        total = 0
        for p in prospects:
            self.salvar(p)
            total += 1
        return total

    def marcar_nao_contatar(self, prospect_id: str) -> bool:
        """
        Atende um pedido de oposição do titular (LGPD Art. 18, § 2º).

        Não apagamos o registro: manter o id na lista com a marca é o que
        garante que uma coleta futura não o traga de volta silenciosamente.
        """
        p = self.buscar(prospect_id)
        if not p:
            return False
        p.nao_contatar = True
        p.estagio = Estagio.DESCARTADO
        self.salvar(p)
        logger.info("prospect %s marcado como não-contatar", prospect_id)
        return True

    def remover(self, prospect_id: str) -> bool:
        cur = self._con.execute("DELETE FROM prospects WHERE id = ?", (prospect_id,))
        self._con.commit()
        return cur.rowcount > 0

    # ------------------------------------------------------------- leitura

    def buscar(self, prospect_id: str) -> Optional[Prospect]:
        row = self._con.execute(
            "SELECT payload FROM prospects WHERE id = ?", (prospect_id,)
        ).fetchone()
        return Prospect.model_validate_json(row["payload"]) if row else None

    def listar(
        self,
        modalidade: Optional[Modalidade] = None,
        estagio: Optional[Estagio] = None,
        uf: Optional[str] = None,
        score_minimo: Optional[float] = None,
        apenas_contataveis: bool = False,
        limite: Optional[int] = None,
    ) -> List[Prospect]:
        """Lista a carteira, do maior score para o menor."""
        sql = "SELECT payload FROM prospects WHERE 1=1"
        args: list = []

        if modalidade:
            sql += " AND modalidade = ?"; args.append(modalidade.value)
        if estagio:
            sql += " AND estagio = ?"; args.append(estagio.value)
        if uf:
            sql += " AND uf = ?"; args.append(uf.upper())
        if score_minimo is not None:
            sql += " AND score >= ?"; args.append(score_minimo)
        if apenas_contataveis:
            sql += " AND nao_contatar = 0 AND estagio != ?"; args.append(Estagio.DESCARTADO.value)

        sql += " ORDER BY score DESC NULLS LAST, nome ASC"
        if limite:
            sql += " LIMIT ?"; args.append(limite)

        registros = [Prospect.model_validate_json(r["payload"])
                     for r in self._con.execute(sql, args)]

        # `contatavel` também exige ter algum canal de contato, o que o SQL não sabe
        if apenas_contataveis:
            registros = [p for p in registros if p.contatavel]
        return registros

    def __iter__(self) -> Iterator[Prospect]:
        return iter(self.listar())

    def total(self) -> int:
        return self._con.execute("SELECT COUNT(*) AS n FROM prospects").fetchone()["n"]

    def resumo(self) -> dict:
        """Contagem por modalidade e por estágio, para o painel."""
        def contar(coluna: str) -> dict:
            return {
                r[coluna]: r["n"]
                for r in self._con.execute(
                    f"SELECT {coluna}, COUNT(*) AS n FROM prospects GROUP BY {coluna}"
                )
            }

        media = self._con.execute(
            "SELECT AVG(score) AS m FROM prospects WHERE score IS NOT NULL"
        ).fetchone()["m"]

        return {
            "total": self.total(),
            "por_modalidade": contar("modalidade"),
            "por_estagio": contar("estagio"),
            "score_medio": round(media, 2) if media is not None else None,
            "nao_contatar": self._con.execute(
                "SELECT COUNT(*) AS n FROM prospects WHERE nao_contatar = 1"
            ).fetchone()["n"],
        }

    # ------------------------------------------------------------ exportar

    def exportar_csv(self, destino: Path, apenas_contataveis: bool = True) -> Path:
        """
        Exporta a carteira em CSV.

        Por padrão só sai quem pode ser abordado — exportar quem pediu para não
        ser contatado é o caminho mais curto para o dado vazar de volta para uma
        ferramenta de disparo.
        """
        import csv

        destino = Path(destino)
        destino.parent.mkdir(parents=True, exist_ok=True)
        registros = self.listar(apenas_contataveis=apenas_contataveis)

        colunas = [
            "id", "nome", "empresa", "cargo", "email", "telefone", "site", "instagram",
            "modalidade", "estagio", "score", "municipio", "uf", "bioma",
            "area_ha", "unidades", "base_legal", "fonte", "coletado_em", "notas",
        ]

        with destino.open("w", newline="", encoding="utf-8") as fh:
            escritor = csv.DictWriter(fh, fieldnames=colunas)
            escritor.writeheader()
            for p in registros:
                escritor.writerow({
                    "id": p.id, "nome": p.nome, "empresa": p.empresa, "cargo": p.cargo,
                    "email": p.email, "telefone": p.telefone, "site": p.site,
                    "instagram": p.instagram, "modalidade": p.modalidade.value,
                    "estagio": p.estagio.value, "score": p.score,
                    "municipio": p.territorio.municipio, "uf": p.territorio.uf,
                    "bioma": p.territorio.bioma, "area_ha": p.territorio.area_ha,
                    "unidades": p.territorio.unidades, "base_legal": p.base_legal.value,
                    "fonte": p.origem.fonte, "coletado_em": p.origem.coletado_em.isoformat(),
                    "notas": p.notas,
                })

        logger.info("exportados %d prospects para %s", len(registros), destino)
        return destino

    def fechar(self) -> None:
        self._con.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.fechar()
