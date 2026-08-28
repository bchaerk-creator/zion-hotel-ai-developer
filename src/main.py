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
from src.config import (
    AGENT_NAME,
    AGENT_VERSION,
    ZION_ETAPAS_EXECUTAVEIS,
    ZION_MODULOS,
    ZION_STAGES,
)
from src.config.pilares import CADEIA_DE_VALOR, listar_pilares, obter_pilar, pilares_da_etapa
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

    modulos = Table(title="Módulos Transversais", show_header=True)
    modulos.add_column("Código", style="bold gold1", width=6)
    modulos.add_column("Nome", style="white")
    modulos.add_column("Pergunta-chave", style="dim")

    perguntas_modulos = {
        7: "Quanta terra falta para o carbono fechar conta?",
    }

    for num, nome in ZION_MODULOS.items():
        modulos.add_row(str(num), nome, perguntas_modulos.get(num, ""))

    console.print(modulos)


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
@click.option("--stage", "-s", type=int, required=True, help="Número da etapa (0-6) ou módulo (7)")
@click.option("--input", "-i", "input_file", type=click.Path(exists=True), required=True, help="Arquivo JSON com dados do projeto")
@click.option("--output", "-o", "output_dir", type=click.Path(), help="Diretório de saída")
def run(stage: int, input_file: str, output_dir: str = None):
    """Executa uma etapa específica do método Zion."""
    show_banner()

    if stage not in ZION_ETAPAS_EXECUTAVEIS:
        validas = ", ".join(str(k) for k in sorted(ZION_ETAPAS_EXECUTAVEIS))
        console.print(f"[red]Erro: Etapa {stage} não existe. Use: {validas}.[/red]")
        return

    console.print(f"\n[bold]Executando: {ZION_ETAPAS_EXECUTAVEIS[stage]}[/bold]\n")

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
@click.option("--pilar", "-p", "codigo", help="Detalha um pilar específico (ex.: PARCERIA)")
@click.option("--etapa", "-e", type=int, help="Mostra os pilares alimentados por uma etapa do método")
def pilares(codigo: str = None, etapa: int = None):
    """Exibe os pilares comerciais da Zion."""
    show_banner()

    if codigo:
        try:
            p = obter_pilar(codigo)
        except KeyError as erro:
            console.print(f"[red]{erro}[/red]")
            return

        console.print(f"\n[bold gold1]{p.nome}[/bold gold1]")
        console.print(f"[italic]{p.oferta}[/italic]\n")

        detalhe = Table(show_header=False)
        detalhe.add_column("Campo", style="bold")
        detalhe.add_column("Valor")
        detalhe.add_row("Cliente", p.cliente)
        detalhe.add_row("Modelo de receita", p.modelo_receita)
        detalhe.add_row("O que a Zion coloca", p.ativo_zion)
        detalhe.add_row("Etapas do método", ", ".join(str(e) for e in p.etapas_zion))
        detalhe.add_row("Módulo do sistema", p.modulo_sistema or "—")
        console.print(detalhe)

        console.print("\n[bold]Escopo:[/bold]")
        for item in p.escopo:
            console.print(f"  • {item}")

        if p.observacoes:
            console.print(f"\n[dim]{p.observacoes}[/dim]")
        return

    if etapa is not None:
        encontrados = pilares_da_etapa(etapa)
        nome_etapa = ZION_ETAPAS_EXECUTAVEIS.get(etapa, f"Etapa {etapa}")
        console.print(f"\n[bold]Pilares alimentados por: {nome_etapa}[/bold]\n")
        if not encontrados:
            console.print("[dim]Nenhum pilar mapeado para esta etapa.[/dim]")
            return
        for p in encontrados:
            console.print(f"  • [bold gold1]{p.nome}[/bold gold1] — {p.oferta}")
        return

    tabela = Table(title="Pilares Comerciais da Zion", show_header=True)
    tabela.add_column("Pilar", style="bold gold1")
    tabela.add_column("Oferta", style="white")
    tabela.add_column("Como a Zion ganha", style="dim")

    for p in listar_pilares():
        tabela.add_row(p.nome, p.oferta, p.modelo_receita)

    console.print(tabela)

    console.print("\n[bold]A escada — como um pilar alimenta o outro:[/bold]\n")
    for i, elo in enumerate(CADEIA_DE_VALOR, start=1):
        console.print(f"  {i}. {elo}")
    console.print()


@cli.command("land-bank")
@click.option("--input", "-i", "input_file", type=click.Path(exists=True), required=True, help="Arquivo JSON do Land Bank")
@click.option("--output", "-o", "output_file", type=click.Path(), help="Caminho do relatório Markdown de saída")
@click.option("--json", "json_file", type=click.Path(), help="Exporta o resultado completo em JSON")
@click.option("--ia", is_flag=True, help="Adiciona a camada estratégica com LLM (requer chave de API)")
def land_bank(input_file: str, output_file: str = None, json_file: str = None, ia: bool = False):
    """Analisa o Land Bank: elegibilidade, clusters de carbono e fila de agregação."""
    show_banner()

    from src.agents.land_bank_agent import LandBankAgent

    with open(input_file, "r", encoding="utf-8") as f:
        dados = json.load(f)

    agent = LandBankAgent()

    with console.status("[bold gold1]Rodando engine de carbono...[/bold gold1]"):
        resultado, relatorio = agent.analisar(dados)

    console.print(f"\n[bold]{resultado.nome}[/bold]\n")

    resumo = Table(title="Land Bank — Consolidado", show_header=False)
    resumo.add_column("Indicador", style="bold")
    resumo.add_column("Valor", justify="right")
    resumo.add_row("Glebas mapeadas", f"{resultado.total_glebas}")
    resumo.add_row("Área total", f"{resultado.area_total_ha:,.0f} ha")
    resumo.add_row("Área elegível", f"{resultado.area_elegivel_ha:,.0f} ha")
    resumo.add_row("Área contratada", f"{resultado.area_contratada_ha:,.0f} ha")
    resumo.add_row("Área em pipeline", f"{resultado.area_prospeccao_ha:,.0f} ha")
    resumo.add_row("Créditos líquidos", f"[bold gold1]{resultado.vcus_liquidos:,.0f} tCO2e[/bold gold1]")
    resumo.add_row("Créditos contratados", f"{resultado.vcus_contratados:,.0f} tCO2e")
    resumo.add_row("Receita bruta projetada", f"R$ {resultado.receita_bruta_brl:,.0f}")
    resumo.add_row("VPL consolidado", f"R$ {resultado.vpl_total_brl:,.0f}")
    resumo.add_row("Carbon Readiness médio", f"{resultado.readiness_medio:.2f}/10")
    if resultado.meta_tco2e:
        resumo.add_row(
            "Meta do portfólio",
            f"{resultado.meta_tco2e:,.0f} tCO2e ({(resultado.atingimento_meta or 0) * 100:.1f}%)",
        )
    console.print(resumo)

    clusters = Table(title="Clusters de Carbono", show_header=True)
    clusters.add_column("Cluster", style="bold gold1")
    clusters.add_column("Elegível", justify="right")
    clusters.add_column("Contratado", justify="right")
    clusters.add_column("tCO2e líq.", justify="right")
    clusters.add_column("VPL", justify="right")
    clusters.add_column("Equilíbrio", justify="right")
    clusters.add_column("Pré-venda mín.", justify="right")
    clusters.add_column("Escala")

    for c in sorted(resultado.clusters, key=lambda x: x.vcus_liquidos, reverse=True):
        if c.prevenda_minima == 0:
            prevenda = "dispensável"
        elif c.prevenda_minima:
            prevenda = f"{c.prevenda_minima * 100:.0f}%"
        else:
            prevenda = "não resolve"
        clusters.add_row(
            c.id,
            f"{c.area_elegivel_ha:,.0f} ha",
            f"{c.area_contratada_ha:,.0f} ha",
            f"{c.vcus_liquidos:,.0f}",
            f"R$ {c.vpl_brl:,.0f}",
            f"R$ {c.preco_equilibrio_brl:,.0f}" if c.preco_equilibrio_brl else "—",
            prevenda,
            c.escala,
        )
    console.print(clusters)

    if resultado.prioridades:
        fila = Table(title="Fila de Agregação", show_header=True)
        fila.add_column("#", width=3)
        fila.add_column("Gleba", style="bold")
        fila.add_column("Instrumento")
        fila.add_column("Elegível", justify="right")
        fila.add_column("tCO2e líq.", justify="right")
        fila.add_column("Entrada", justify="right")
        fila.add_column("Destrava")

        for p in resultado.prioridades:
            fila.add_row(
                str(p.prioridade),
                f"{p.gleba_id} {p.nome}",
                p.instrumento_recomendado.value.replace("_", " "),
                f"{p.area_elegivel_ha:,.0f} ha",
                f"{p.vcus_liquidos:,.0f}",
                f"R$ {p.custo_entrada_brl:,.0f}",
                "sim" if p.destrava_escala else "",
            )
        console.print(fila)

    for alerta in resultado.alertas:
        console.print(f"[yellow]• {alerta}[/yellow]")

    if ia:
        console.print("\n[dim]Gerando camada estratégica com IA...[/dim]")
        with console.status("[bold gold1]Analisando estratégia de agregação...[/bold gold1]"):
            saida = agent.execute(dados)
        console.print(Panel(
            Markdown(saida["analise"]),
            title="[bold]Estratégia de Agregação[/bold]",
            border_style="gold1",
        ))
        console.print(f"\n[green]Relatório completo salvo em: {saida['relatorio_path']}[/green]")
        relatorio = saida["relatorio_numerico"]

    if output_file:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(relatorio)
        console.print(f"\n[green]Relatório salvo em: {output_file}[/green]")

    if json_file:
        Path(json_file).parent.mkdir(parents=True, exist_ok=True)
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(resultado.model_dump(), f, ensure_ascii=False, indent=2, default=str)
        console.print(f"[green]Resultado exportado em: {json_file}[/green]")


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
