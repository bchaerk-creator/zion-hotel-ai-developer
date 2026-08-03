"""
Zion Hotel AI Developer — Ponto de Entrada Principal

Agente de IA para desenvolvimento hoteleiro baseado no método
da Pirâmide Invertida© da Zion Hotel Group International.
"""

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agents.orchestrator import ZionOrchestrator
from src.config import AGENT_NAME, AGENT_VERSION, ZION_STAGES
from src.utils.logger import setup_logger

console = Console()
logger = setup_logger("zion")


def show_banner():
    """Exibe o banner do agente."""
    banner = f"""
[bold gold1]╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ZION HOTEL AI DEVELOPER                                ║
║   Agente de IA para Desenvolvimento Hoteleiro            ║
║                                                          ║
║   Zion Hotel Group International                         ║
║   Método da Pirâmide Invertida©                          ║
║                                                          ║
║   Versão: {AGENT_VERSION}                                        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝[/bold gold1]
"""
    console.print(banner)


def show_stages():
    """Exibe as etapas disponíveis."""
    table = Table(title="Etapas do Método Zion", show_header=True)
    table.add_column("Etapa", style="bold gold1", width=6)
    table.add_column("Nome", style="white")
    table.add_column("Pergunta-chave", style="dim")

    perguntas = {
        0: "Vale a pena seguir?",
        1: "Existe demanda e a que preço?",
        2: "O projeto se paga?",
        3: "O que vamos construir?",
        4: "Em que veículo isso vai morar?",
        5: "Como levantamos o capital?",
        6: "Como garantimos que a tese se mantém?",
    }

    for num, nome in ZION_STAGES.items():
        table.add_row(str(num), nome, perguntas.get(num, ""))

    console.print(table)


@click.group()
def cli():
    """Zion Hotel AI Developer — Agente de IA para Desenvolvimento Hoteleiro."""
    pass


@cli.command()
def info():
    """Exibe informações sobre o agente."""
    show_banner()
    show_stages()


@cli.command()
@click.option("--stage", "-s", type=int, required=True, help="Número da etapa (0-6)")
@click.option("--input", "-i", "input_file", type=click.Path(exists=True), required=True, help="Arquivo JSON com dados do projeto")
@click.option("--output", "-o", "output_dir", type=click.Path(), help="Diretório de saída")
def run(stage: int, input_file: str, output_dir: str = None):
    """Executa uma etapa específica do método Zion."""
    show_banner()

    if stage not in ZION_STAGES:
        console.print(f"[red]Erro: Etapa {stage} não existe. Use 0-6.[/red]")
        return

    console.print(f"\n[bold]Executando: {ZION_STAGES[stage]}[/bold]\n")

    # Carregar dados do projeto
    with open(input_file, "r", encoding="utf-8") as f:
        project_data = json.load(f)

    console.print(f"[dim]Projeto: {project_data.get('nome_projeto', 'N/A')}[/dim]")
    console.print(f"[dim]Localização: {project_data.get('localizacao', 'N/A')}[/dim]\n")

    # Executar
    orchestrator = ZionOrchestrator()
    orchestrator.initialize_project(project_data)

    with console.status(f"[bold gold1]Processando Etapa {stage}...[/bold gold1]"):
        result = orchestrator.execute_stage(stage, project_data)

    # Exibir resultado
    console.print(Panel(
        Markdown(result.get("analise", "Sem resultado")),
        title=f"[bold]Resultado — Etapa {stage}[/bold]",
        border_style="gold1",
    ))

    if "relatorio_path" in result:
        console.print(f"\n[green]Relatório salvo em: {result['relatorio_path']}[/green]")


@cli.command()
@click.option("--input", "-i", "input_file", type=click.Path(exists=True), required=True, help="Arquivo JSON com dados do projeto")
def pipeline(input_file: str):
    """Executa o pipeline completo (Etapas 0-5)."""
    show_banner()

    with open(input_file, "r", encoding="utf-8") as f:
        project_data = json.load(f)

    console.print(f"\n[bold]Pipeline Completo — {project_data.get('nome_projeto', 'Projeto')}[/bold]\n")

    orchestrator = ZionOrchestrator()

    with console.status("[bold gold1]Executando pipeline completo...[/bold gold1]"):
        state = orchestrator.execute_full_pipeline(project_data)

    console.print("\n[bold green]Pipeline concluído com sucesso![/bold green]\n")
    console.print(Markdown(orchestrator.get_project_summary()))


@cli.command()
@click.option("--input", "-i", "input_file", type=click.Path(exists=True), required=True, help="Arquivo JSON com dados do projeto")
def quick_score(input_file: str):
    """Executa apenas o Zion Score rápido (diagnóstico preliminar)."""
    show_banner()

    with open(input_file, "r", encoding="utf-8") as f:
        project_data = json.load(f)

    console.print(f"\n[bold]Zion Score™ Rápido — {project_data.get('nome_projeto', 'Projeto')}[/bold]\n")

    from src.agents.zion_score_agent import ZionScoreAgent
    agent = ZionScoreAgent()

    with console.status("[bold gold1]Calculando Zion Score...[/bold gold1]"):
        result = agent.quick_score(project_data)

    # Exibir resultado
    table = Table(title="Zion Score™", show_header=False)
    table.add_column("Campo", style="bold")
    table.add_column("Valor")

    table.add_row("Zion Score", f"[bold gold1]{result.get('zion_score', 'N/A')}/10[/bold gold1]")
    table.add_row("Classificação", result.get("classificacao", "N/A"))
    table.add_row("Vocação", result.get("vocacao_principal", "N/A"))
    table.add_row("ADR Estimado", f"R$ {result.get('adr_estimado_brl', 0):,.2f}")
    table.add_row("Recomendação", result.get("recomendacao", "N/A"))

    console.print(table)
    console.print(f"\n[dim]{result.get('resumo', '')}[/dim]")


@cli.command()
def interactive():
    """Modo interativo — conversa com o agente Zion."""
    show_banner()
    console.print("\n[bold]Modo Interativo[/bold]")
    console.print("[dim]Digite suas perguntas sobre desenvolvimento hoteleiro.")
    console.print("Use 'sair' para encerrar.[/dim]\n")

    from src.utils.llm_client import ZionLLMClient
    from src.prompts.base import SYSTEM_PROMPT_BASE

    llm = ZionLLMClient()
    messages = [{"role": "system", "content": SYSTEM_PROMPT_BASE}]

    while True:
        try:
            user_input = console.input("[bold gold1]Você > [/bold gold1]")
        except (KeyboardInterrupt, EOFError):
            break

        if user_input.lower() in ("sair", "exit", "quit"):
            console.print("\n[dim]Encerrando. Até a próxima![/dim]")
            break

        if not user_input.strip():
            continue

        messages.append({"role": "user", "content": user_input})

        with console.status("[bold gold1]Pensando...[/bold gold1]"):
            response = llm.chat(messages)

        messages.append({"role": "assistant", "content": response})

        console.print(f"\n[bold]Zion AI >[/bold]")
        console.print(Markdown(response))
        console.print()


if __name__ == "__main__":
    cli()
