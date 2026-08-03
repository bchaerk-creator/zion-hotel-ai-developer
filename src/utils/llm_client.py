"""
Cliente LLM para o Zion Hotel AI Developer.
Gerencia chamadas à API OpenAI com suporte a diferentes modelos e modos de raciocínio.
"""

import json
import logging
from typing import Optional, Dict, Any, List

from openai import OpenAI

from src.config import (
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    ZION_MODEL,
    ZION_THINKING_MODEL,
    ZION_FAST_MODEL,
)

logger = logging.getLogger(__name__)


class ZionLLMClient:
    """Cliente LLM especializado para o agente Zion."""

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE,
        )
        self.default_model = ZION_MODEL
        self.thinking_model = ZION_THINKING_MODEL
        self.fast_model = ZION_FAST_MODEL

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Executa uma chamada de chat simples.

        Args:
            messages: Lista de mensagens no formato OpenAI
            model: Modelo a usar (padrão: ZION_MODEL)
            temperature: Temperatura de geração
            max_tokens: Máximo de tokens na resposta
            response_format: Formato de resposta (JSON schema, etc.)

        Returns:
            Conteúdo da resposta como string
        """
        model = model or self.default_model
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_format:
            kwargs["response_format"] = response_format

        logger.info(f"Chamando modelo {model} com {len(messages)} mensagens")

        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content

        logger.info(
            f"Resposta recebida: {response.usage.prompt_tokens} prompt tokens, "
            f"{response.usage.completion_tokens} completion tokens"
        )

        return content

    def think(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        reasoning_effort: str = "high",
        max_tokens: int = 8192,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Executa uma chamada com raciocínio estendido para análises complexas.

        Args:
            messages: Lista de mensagens
            model: Modelo de raciocínio (padrão: ZION_THINKING_MODEL)
            reasoning_effort: Esforço de raciocínio (minimal/low/medium/high)
            max_tokens: Máximo de tokens
            response_format: Formato de resposta

        Returns:
            Conteúdo da resposta
        """
        model = model or self.thinking_model
        kwargs = {
            "model": model,
            "messages": messages,
            "max_completion_tokens": max_tokens,
            "extra_body": {"reasoning": {"effort": reasoning_effort}},
        }
        if response_format:
            kwargs["response_format"] = response_format

        logger.info(f"Chamando modelo de raciocínio {model} (effort={reasoning_effort})")

        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content

        logger.info(
            f"Resposta de raciocínio recebida: {response.usage.prompt_tokens} prompt, "
            f"{response.usage.completion_tokens} completion tokens"
        )

        return content

    def fast(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2048,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Executa uma chamada rápida e econômica para tarefas simples.

        Args:
            messages: Lista de mensagens
            max_tokens: Máximo de tokens
            response_format: Formato de resposta

        Returns:
            Conteúdo da resposta
        """
        return self.chat(
            messages=messages,
            model=self.fast_model,
            temperature=0.3,
            max_tokens=max_tokens,
            response_format=response_format,
        )

    def structured_output(
        self,
        messages: List[Dict[str, str]],
        schema: Dict[str, Any],
        schema_name: str = "output",
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Executa uma chamada com output estruturado (JSON Schema).

        Args:
            messages: Lista de mensagens
            schema: JSON Schema para a resposta
            schema_name: Nome do schema
            model: Modelo a usar

        Returns:
            Dicionário com a resposta estruturada
        """
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "strict": True,
                "schema": schema,
            },
        }

        content = self.chat(
            messages=messages,
            model=model,
            response_format=response_format,
        )

        return json.loads(content)

    def analyze_with_context(
        self,
        system_prompt: str,
        user_input: str,
        context: Optional[str] = None,
        use_thinking: bool = False,
    ) -> str:
        """
        Executa uma análise com contexto opcional.

        Args:
            system_prompt: Prompt de sistema
            user_input: Input do usuário
            context: Contexto adicional
            use_thinking: Se deve usar modelo de raciocínio

        Returns:
            Conteúdo da resposta
        """
        messages = [{"role": "system", "content": system_prompt}]

        if context:
            messages.append({
                "role": "user",
                "content": f"Contexto do projeto:\n{context}\n\n---\n\nSolicitação:\n{user_input}",
            })
        else:
            messages.append({"role": "user", "content": user_input})

        if use_thinking:
            return self.think(messages)
        else:
            return self.chat(messages)
