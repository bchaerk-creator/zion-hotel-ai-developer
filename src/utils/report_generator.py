"""
Gerador de relatórios para o Zion Hotel AI Developer.
Produz relatórios em Markdown formatados conforme padrão Zion.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from jinja2 import Environment, FileSystemLoader

from src.config import OUTPUT_DIR, DATA_DIR, LANGUAGE


class ReportGenerator:
    """Gerador de relatórios no padrão Zion Hotel Group International."""

    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.templates_dir = DATA_DIR / "templates"
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate_report(
        self,
        template_name: str,
        data: Dict[str, Any],
        output_filename: Optional[str] = None,
        projeto_nome: str = "Projeto",
    ) -> str:
        """
        Gera um relatório a partir de um template Jinja2.

        Args:
            template_name: Nome do template (sem extensão)
            data: Dados para preencher o template
            output_filename: Nome do arquivo de saída
            projeto_nome: Nome do projeto

        Returns:
            Caminho do arquivo gerado
        """
        template = self.env.get_template(f"{template_name}.md.j2")

        context = {
            "data": data,
            "projeto_nome": projeto_nome,
            "data_geracao": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "versao": "1.0",
            "empresa": "Zion Hotel Group International",
        }

        content = template.render(**context)

        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{template_name}_{timestamp}.md"

        output_path = self.output_dir / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return str(output_path)

    def generate_markdown(
        self,
        title: str,
        content: str,
        projeto_nome: str = "Projeto",
        etapa: Optional[int] = None,
    ) -> str:
        """
        Gera um relatório Markdown direto (sem template).

        Args:
            title: Título do relatório
            content: Conteúdo principal em Markdown
            projeto_nome: Nome do projeto
            etapa: Número da etapa (0-6)

        Returns:
            Caminho do arquivo gerado
        """
        header = self._build_header(title, projeto_nome, etapa)
        footer = self._build_footer()

        full_content = f"{header}\n\n{content}\n\n{footer}"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = title.lower().replace(" ", "_").replace("/", "_")[:50]
        output_filename = f"{safe_title}_{timestamp}.md"

        output_path = self.output_dir / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_content)

        return str(output_path)

    def _build_header(
        self, title: str, projeto_nome: str, etapa: Optional[int] = None
    ) -> str:
        """Constrói o cabeçalho padrão Zion."""
        etapa_label = f" | Etapa {etapa}" if etapa is not None else ""
        return f"""---
title: "{title}"
projeto: "{projeto_nome}"
empresa: "Zion Hotel Group International"
data: "{datetime.now().strftime('%d/%m/%Y')}"
etapa: {etapa if etapa is not None else 'N/A'}
---

# {title}

**Projeto:** {projeto_nome}{etapa_label}
**Data:** {datetime.now().strftime('%d/%m/%Y')}
**Elaborado por:** Zion Hotel AI Developer

---"""

    def _build_footer(self) -> str:
        """Constrói o rodapé padrão Zion."""
        return """---

> *Documento gerado pelo Zion Hotel AI Developer*
> *Zion Hotel Group International — Florianópolis (SC) · Barcelona (ESP)*
> *Este documento é confidencial e de uso exclusivo do destinatário.*
"""
