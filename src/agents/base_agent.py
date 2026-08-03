"""
Classe base para todos os agentes especializados do Zion Hotel AI Developer.
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from src.utils.llm_client import ZionLLMClient
from src.utils.report_generator import ReportGenerator
from src.prompts.base import SYSTEM_PROMPT_BASE

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Classe base abstrata para agentes especializados."""

    def __init__(self, etapa: int, nome: str):
        """
        Inicializa o agente base.

        Args:
            etapa: Número da etapa (0-6)
            nome: Nome do agente
        """
        self.etapa = etapa
        self.nome = nome
        self.llm = ZionLLMClient()
        self.report_gen = ReportGenerator()
        self.context: Dict[str, Any] = {}

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Retorna o system prompt específico do agente."""
        pass

    @property
    def full_system_prompt(self) -> str:
        """Combina o prompt base com o prompt específico."""
        return f"{SYSTEM_PROMPT_BASE}\n\n---\n\n{self.system_prompt}"

    @abstractmethod
    def execute(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a análise principal do agente.

        Args:
            project_data: Dados do projeto

        Returns:
            Resultado da análise
        """
        pass

    def analyze(
        self,
        user_input: str,
        context: Optional[str] = None,
        use_thinking: bool = False,
    ) -> str:
        """
        Executa uma análise usando o LLM.

        Args:
            user_input: Input do usuário/sistema
            context: Contexto adicional do projeto
            use_thinking: Se deve usar raciocínio estendido

        Returns:
            Resultado da análise como texto
        """
        messages = [
            {"role": "system", "content": self.full_system_prompt},
        ]

        if context:
            content = f"Contexto do projeto:\n{context}\n\n---\n\nSolicitação:\n{user_input}"
        else:
            content = user_input

        messages.append({"role": "user", "content": content})

        if use_thinking:
            return self.llm.think(messages)
        else:
            return self.llm.chat(messages)

    def generate_report(
        self,
        content: str,
        title: str,
        projeto_nome: str = "Projeto",
    ) -> str:
        """
        Gera um relatório formatado.

        Args:
            content: Conteúdo do relatório
            title: Título do relatório
            projeto_nome: Nome do projeto

        Returns:
            Caminho do arquivo gerado
        """
        return self.report_gen.generate_markdown(
            title=title,
            content=content,
            projeto_nome=projeto_nome,
            etapa=self.etapa,
        )

    def set_context(self, key: str, value: Any) -> None:
        """Define um valor no contexto do agente."""
        self.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Obtém um valor do contexto do agente."""
        return self.context.get(key, default)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} etapa={self.etapa} nome='{self.nome}'>"
