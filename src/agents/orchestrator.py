"""
Orquestrador principal do Zion Hotel AI Developer.
Coordena a execução sequencial dos agentes especializados.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from .zion_score_agent import ZionScoreAgent
from .market_agent import MarketAgent
from .financial_agent import FinancialAgent
from .product_agent import ProductAgent
from .business_agent import BusinessAgent
from .investor_agent import InvestorAgent
from .governance_agent import GovernanceAgent
from src.config import OUTPUT_DIR, ZION_STAGES

logger = logging.getLogger(__name__)


class ZionOrchestrator:
    """
    Orquestrador que coordena todos os agentes do método Zion.
    Gerencia o fluxo sequencial das etapas e o estado do projeto.
    """

    def __init__(self):
        self.agents = {
            0: ZionScoreAgent(),
            1: MarketAgent(),
            2: FinancialAgent(),
            3: ProductAgent(),
            4: BusinessAgent(),
            5: InvestorAgent(),
            6: GovernanceAgent(),
        }
        self.project_state: Dict[str, Any] = {}
        self.execution_history: List[Dict[str, Any]] = []

    def initialize_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inicializa um novo projeto no sistema.

        Args:
            project_data: Dados de entrada do projeto

        Returns:
            Estado inicial do projeto
        """
        project_id = f"ZION-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        self.project_state = {
            "projeto_id": project_id,
            "nome_projeto": project_data.get("nome_projeto", "Projeto Sem Nome"),
            "data_criacao": datetime.now().isoformat(),
            "etapa_atual": 0,
            "status": "inicializado",
            "dados_entrada": project_data,
            "resultados": {},
            "relatorios": [],
        }

        logger.info(f"Projeto inicializado: {project_id} - {self.project_state['nome_projeto']}")

        # Salvar estado
        self._save_state()

        return self.project_state

    def execute_stage(self, stage: int, project_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executa uma etapa específica do método Zion.

        Args:
            stage: Número da etapa (0-6)
            project_data: Dados adicionais (opcional, usa estado atual se não fornecido)

        Returns:
            Resultado da etapa
        """
        if stage not in self.agents:
            raise ValueError(f"Etapa {stage} não existe. Etapas válidas: 0-6")

        # Usar dados do estado atual se não fornecidos
        if project_data is None:
            project_data = self._get_current_project_data()

        stage_name = ZION_STAGES.get(stage, f"Etapa {stage}")
        logger.info(f"Executando: {stage_name}")

        # Executar o agente
        agent = self.agents[stage]
        result = agent.execute(project_data)

        # Atualizar estado
        self.project_state["etapa_atual"] = stage
        self.project_state["status"] = "em_progresso"
        self.project_state["resultados"][f"etapa_{stage}"] = result

        if "relatorio_path" in result:
            self.project_state["relatorios"].append({
                "etapa": stage,
                "path": result["relatorio_path"],
                "data": datetime.now().isoformat(),
            })

        # Registrar no histórico
        self.execution_history.append({
            "etapa": stage,
            "nome": stage_name,
            "data": datetime.now().isoformat(),
            "status": result.get("status", "concluido"),
        })

        # Salvar estado
        self._save_state()

        return result

    def execute_full_pipeline(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa o pipeline completo (Etapas 0-5).

        Args:
            project_data: Dados de entrada do projeto

        Returns:
            Estado final do projeto com todos os resultados
        """
        logger.info("Iniciando pipeline completo do método Zion")

        # Inicializar projeto
        self.initialize_project(project_data)

        # Executar cada etapa sequencialmente
        for stage in range(6):  # Etapas 0-5 (6 é contínua)
            try:
                result = self.execute_stage(stage, self._get_current_project_data())
                logger.info(f"Etapa {stage} concluída com sucesso")
            except Exception as e:
                logger.error(f"Erro na Etapa {stage}: {e}")
                self.project_state["status"] = f"erro_etapa_{stage}"
                self._save_state()
                raise

        self.project_state["status"] = "pipeline_completo"
        self._save_state()

        logger.info("Pipeline completo executado com sucesso!")
        return self.project_state

    def get_project_summary(self) -> str:
        """Retorna um resumo do estado atual do projeto."""
        if not self.project_state:
            return "Nenhum projeto inicializado."

        lines = [
            f"# Resumo do Projeto: {self.project_state.get('nome_projeto', 'N/A')}",
            f"",
            f"**ID:** {self.project_state.get('projeto_id', 'N/A')}",
            f"**Status:** {self.project_state.get('status', 'N/A')}",
            f"**Etapa atual:** {self.project_state.get('etapa_atual', 0)}",
            f"**Data de criação:** {self.project_state.get('data_criacao', 'N/A')}",
            f"",
            f"## Etapas Concluídas",
        ]

        for entry in self.execution_history:
            lines.append(f"- Etapa {entry['etapa']}: {entry['nome']} ({entry['status']})")

        if self.project_state.get("relatorios"):
            lines.append(f"\n## Relatórios Gerados")
            for report in self.project_state["relatorios"]:
                lines.append(f"- Etapa {report['etapa']}: {report['path']}")

        return "\n".join(lines)

    def _get_current_project_data(self) -> Dict[str, Any]:
        """Constrói os dados do projeto com resultados acumulados."""
        data = dict(self.project_state.get("dados_entrada", {}))

        # Adicionar resultados das etapas anteriores como contexto
        resultados = self.project_state.get("resultados", {})

        if "etapa_0" in resultados:
            data["zion_score_resultado"] = resultados["etapa_0"].get("analise", "")
        if "etapa_1" in resultados:
            data["market_study_resultado"] = resultados["etapa_1"].get("analise", "")
        if "etapa_2" in resultados:
            data["financial_resultado"] = resultados["etapa_2"].get("analise", "")
        if "etapa_3" in resultados:
            data["product_resultado"] = resultados["etapa_3"].get("analise", "")
        if "etapa_4" in resultados:
            data["business_resultado"] = resultados["etapa_4"].get("analise", "")

        return data

    def _save_state(self) -> None:
        """Salva o estado atual do projeto em disco."""
        state_dir = OUTPUT_DIR / "state"
        state_dir.mkdir(parents=True, exist_ok=True)

        project_id = self.project_state.get("projeto_id", "unknown")
        state_file = state_dir / f"{project_id}.json"

        with open(state_file, "w", encoding="utf-8") as f:
            # Serializar apenas dados serializáveis
            serializable_state = {
                k: v for k, v in self.project_state.items()
                if isinstance(v, (str, int, float, bool, list, dict, type(None)))
            }
            json.dump(serializable_state, f, ensure_ascii=False, indent=2)

    def load_project(self, project_id: str) -> Dict[str, Any]:
        """Carrega um projeto salvo anteriormente."""
        state_file = OUTPUT_DIR / "state" / f"{project_id}.json"

        if not state_file.exists():
            raise FileNotFoundError(f"Projeto {project_id} não encontrado")

        with open(state_file, "r", encoding="utf-8") as f:
            self.project_state = json.load(f)

        logger.info(f"Projeto carregado: {project_id}")
        return self.project_state
