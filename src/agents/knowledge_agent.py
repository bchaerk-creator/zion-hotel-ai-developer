"""
Agente do ZION KNOWLEDGE ENGINE™.

A base de conhecimento, o grafo e a auditoria são determinísticos e rodam sem
LLM. O modelo entra apenas para ensinar, montar aula, criar exercício e avaliar
entregável — sempre com o estado real da base injetado no contexto, para que
não haja espaço para preencher lacuna com invenção.
"""

import logging
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent
from src.knowledge import auditar, construir_base, relatorio_auditoria
from src.knowledge.base import PERGUNTA_DO_PILAR, KnowledgeBase
from src.knowledge.models import Pilar, Status
from src.prompts import PROMPT_KNOWLEDGE_ENGINE

logger = logging.getLogger(__name__)


class KnowledgeAgent(BaseAgent):
    """Fonte de verdade do Método Zion 360°."""

    def __init__(self, kb: Optional[KnowledgeBase] = None):
        super().__init__(etapa=8, nome="Zion Knowledge Engine")
        self.kb = kb or construir_base()

    @property
    def system_prompt(self) -> str:
        return PROMPT_KNOWLEDGE_ENGINE

    # ------------------------------------------------------------------
    # Determinístico
    # ------------------------------------------------------------------

    def auditar_metodo(self) -> Dict[str, Any]:
        """AUDITAR MÉTODO — inconsistências, lacunas e divergências."""
        resultado = auditar(self.kb)
        return {
            "resultado": resultado,
            "relatorio": relatorio_auditoria(resultado),
        }

    def mapear(self, termo: str) -> Dict[str, List]:
        """MAPEAR CONHECIMENTO — o que existe sobre um termo."""
        return self.kb.buscar(termo)

    def conectar(self, conceito_id: str) -> Dict[str, Any]:
        """CONECTAR CONCEITOS — a cadeia completa de um conceito."""
        return self.kb.cadeia(conceito_id)

    def verificar_fonte(self, item_id: str) -> Dict[str, Any]:
        """VERIFICAR FONTE — de onde vem uma informação."""
        for nome_banco, banco in self.kb._bancos().items():
            if item_id in banco:
                item = banco[item_id]
                fonte = getattr(item, "fonte", None)
                status = getattr(item, "status", None)
                return {
                    "banco": nome_banco,
                    "item": item,
                    "fonte": fonte,
                    "proveniencia": getattr(item, "proveniencia", None),
                    "status": status,
                    # A fonte pode estar disponível e ainda assim só provar que o NOME
                    # foi declarado. Conteúdo verificável exige as duas condições.
                    "fonte_disponivel": bool(fonte and fonte.disponivel_no_sistema),
                    "conteudo_verificavel": bool(
                        fonte
                        and fonte.disponivel_no_sistema
                        and status != Status.PENDENTE_DE_FONTE
                    ),
                }
        raise KeyError(f"Item '{item_id}' não está registrado na base.")

    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa a auditoria do método e gera o relatório."""
        saida = self.auditar_metodo()
        report_path = self.generate_report(
            content=saida["relatorio"],
            title="Auditoria do Método Zion",
            projeto_nome="Zion Knowledge Engine",
        )
        return {
            "etapa": 8,
            "status": "concluido",
            "analise": saida["relatorio"],
            "relatorio_path": report_path,
            "achados": len(saida["resultado"].achados),
            "bloqueantes": len(saida["resultado"].bloqueantes),
        }

    # ------------------------------------------------------------------
    # Modos com LLM
    # ------------------------------------------------------------------

    def ensinar(self, tema: str) -> str:
        return self.analyze(
            user_input=f"ENSINAR: {tema}\n\n{self._contexto(tema)}", use_thinking=True
        )

    def criar_aula(self, tema: str) -> str:
        return self.analyze(
            user_input=f"CRIAR AULA: {tema}\n\n{self._contexto(tema)}", use_thinking=True
        )

    def criar_exercicio(self, tema: str) -> str:
        return self.analyze(user_input=f"CRIAR EXERCÍCIO: {tema}\n\n{self._contexto(tema)}")

    def avaliar(self, entregavel: str, conteudo: str) -> str:
        return self.analyze(
            user_input=(
                f"AVALIAR o entregável '{entregavel}'.\n\n"
                f"{self._contexto(entregavel)}\n\n"
                f"---\n\nConteúdo submetido:\n{conteudo}"
            ),
            use_thinking=True,
        )

    # ------------------------------------------------------------------

    def _contexto(self, termo: str) -> str:
        """
        Injeta o estado real da base: o que existe, com fonte, e o que falta.

        É esta injeção que impede o modelo de preencher lacuna com invenção —
        ele recebe as lacunas nomeadas junto com o conhecimento disponível.
        """
        linhas = ["## Estado da base de conhecimento", ""]

        achados = self.kb.buscar(termo)
        if achados:
            linhas.append(f"### Registrado sobre '{termo}'")
            linhas.append("")
            for banco, itens in achados.items():
                for item in itens:
                    nome = getattr(item, "nome", None) or getattr(item, "pergunta", item.id)
                    status = getattr(item, "status", None)
                    fonte = getattr(item, "fonte", None)
                    marca = f" [{status.value}]" if status else ""
                    origem = f" — fonte: {fonte.documento}" if fonte else ""
                    linhas.append(f"- ({banco}) {item.id}: {nome}{marca}{origem}")
                    obs = getattr(item, "observacoes", None)
                    if obs:
                        linhas.append(f"  - obs: {obs}")
            linhas.append("")
        else:
            linhas.append(
                f"### Nada registrado sobre '{termo}'\n\n"
                "Não há item na base sobre este termo. Diga isso explicitamente em vez de "
                "produzir conteúdo como se fosse metodologia Zion documentada.\n"
            )

        pendentes = [
            f for f in self.kb.ferramentas.values() if f.status == Status.PENDENTE_DE_FONTE
        ]
        if pendentes:
            linhas += ["### Ferramentas com definição ausente — citar nome, não inventar conteúdo", ""]
            linhas += [f"- {f.nome} ({f.id})" for f in pendentes]
            linhas.append("")

        divergencias = [d for d in self.kb.divergencias.values() if d.resolucao is None]
        if divergencias:
            linhas += ["### Divergências não resolvidas — não escolher lado", ""]
            for d in divergencias:
                linhas.append(f"- {d.tema}: {d.versao_a} VERSUS {d.versao_b}")
            linhas.append("")

        if not self.kb.cases:
            linhas += [
                "### Prova",
                "",
                "Nenhum case com resultado documentado está carregado. Não afirmar prova, "
                "resultado ou evidência de operação.",
                "",
            ]

        linhas += ["### Sequência dos pilares", ""]
        for pilar, pergunta in PERGUNTA_DO_PILAR.items():
            if pilar != Pilar.TRANSVERSAL:
                linhas.append(f"- {pilar.value}: {pergunta}")

        return "\n".join(linhas)
