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



# ────────────────────────────────── Carteira de prospects ──────────────────

@cli.group()
def prospects():
    """Carteira de clientes potenciais da Zion."""
    pass


@prospects.command("listar")
@click.option("--modalidade", "-m", type=click.Choice(["development", "management", "collection", "indefinida"]))
@click.option("--uf", "-u", help="Filtrar por UF (sigla)")
@click.option("--score-minimo", "-s", type=float, help="Score mínimo de aderência ao ICP")
@click.option("--todos", is_flag=True, help="Incluir quem pediu para não ser contatado")
@click.option("--limite", "-n", type=int, default=30, show_default=True)
def prospects_listar(modalidade, uf, score_minimo, todos, limite):
    """Lista a carteira, do maior score para o menor."""
    from src.models.prospect import Modalidade
    from src.prospects import RepositorioProspects
    from src.prospects.scoring import classificar_lead

    with RepositorioProspects() as repo:
        registros = repo.listar(
            modalidade=Modalidade(modalidade) if modalidade else None,
            uf=uf,
            score_minimo=score_minimo,
            apenas_contataveis=not todos,
            limite=limite,
        )

    if not registros:
        console.print("[yellow]Nenhum prospect encontrado com esse filtro.[/yellow]")
        return

    tabela = Table(title="Carteira de Prospects · ZION LEAD SCORE", show_lines=False)
    for coluna in ("Score", "Classe", "Nome", "Modalidade", "Território", "Estágio"):
        tabela.add_column(coluna)

    for p in registros:
        local = " / ".join(x for x in (p.territorio.municipio, p.territorio.uf) if x) or "—"
        tabela.add_row(
            f"{p.score:.0f}" if p.score is not None else "—",
            classificar_lead(p.score),
            p.nome,
            p.modalidade.value,
            local,
            p.estagio.value,
        )

    console.print(tabela)
    console.print(f"[dim]{len(registros)} registro(s).[/dim]")


@prospects.command("resumo")
def prospects_resumo():
    """Painel da carteira: totais por modalidade e por estágio."""
    from src.prospects import RepositorioProspects

    with RepositorioProspects() as repo:
        r = repo.resumo()

    if not r["total"]:
        console.print("[yellow]Carteira vazia.[/yellow]")
        return

    console.print(Panel(
        f"[bold]{r['total']}[/bold] prospects · score médio [bold]{r['score_medio']}[/bold]\n"
        f"[dim]{r['nao_contatar']} marcado(s) como não-contatar[/dim]",
        title="Carteira Zion",
    ))

    for titulo, dados in (("Por modalidade", r["por_modalidade"]), ("Por estágio", r["por_estagio"])):
        tabela = Table(title=titulo)
        tabela.add_column("Chave"); tabela.add_column("Total", justify="right")
        for chave, total in sorted(dados.items(), key=lambda x: -x[1]):
            tabela.add_row(chave, str(total))
        console.print(tabela)


@prospects.command("importar")
@click.option("--arquivo", "-f", "arquivo", type=click.Path(exists=True), required=True,
              help="CSV com colunas nome, empresa, email, telefone, municipio, uf, area_ha, unidades")
@click.option("--fonte", default="importacao-manual", show_default=True,
              help="Origem do dado, registrada em cada linha")
def prospects_importar(arquivo, fonte):
    """Importa prospects de um CSV, pontuando cada linha pelo ICP."""
    import csv
    from datetime import date, timedelta
    from src.models.prospect import Origem, Prospect, Territorio
    from src.prospects import RepositorioProspects, gerar_id, inferir_modalidade
    from src.prospects.destinos import buscar as buscar_destino
    from src.prospects.scoring import pontuar_lead

    def numero(valor, conversor):
        try:
            return conversor(valor) if valor not in (None, "", "null") else None
        except (TypeError, ValueError):
            return None

    novos = []
    with open(arquivo, newline="", encoding="utf-8") as fh:
        for linha in csv.DictReader(fh):
            nome = (linha.get("nome") or "").strip()
            if not nome:
                continue
            p = Prospect(
                id=gerar_id(nome, linha.get("empresa")),
                nome=nome,
                empresa=linha.get("empresa") or None,
                email=linha.get("email") or None,
                telefone=linha.get("telefone") or None,
                site=linha.get("site") or None,
                instagram=linha.get("instagram") or None,
                territorio=Territorio(
                    municipio=linha.get("municipio") or None,
                    uf=linha.get("uf") or None,
                    bioma=linha.get("bioma") or None,
                    area_ha=numero(linha.get("area_ha"), float),
                    unidades=numero(linha.get("unidades"), int),
                ),
                origem=Origem(fonte=fonte, tipo="manual", coletado_por="cli"),
                revisar_ate=date.today() + timedelta(days=365),
            )
            p.modalidade = inferir_modalidade(p)
            destino = (buscar_destino(p.territorio.municipio, p.territorio.uf)
                       if p.territorio.municipio and p.territorio.uf else None)
            novos.append(pontuar_lead(p, destino.destination_score if destino else None))

    with RepositorioProspects() as repo:
        total = repo.salvar_muitos(novos)

    console.print(f"[green]{total} prospect(s) importado(s) e pontuado(s).[/green]")


@prospects.command("exportar")
@click.option("--saida", "-o", type=click.Path(), default="output/prospects.csv", show_default=True)
@click.option("--todos", is_flag=True, help="Incluir quem pediu para não ser contatado")
def prospects_exportar(saida, todos):
    """Exporta a carteira em CSV."""
    from src.prospects import RepositorioProspects

    with RepositorioProspects() as repo:
        destino = repo.exportar_csv(Path(saida), apenas_contataveis=not todos)

    console.print(f"[green]Carteira exportada para {destino}[/green]")
    if todos:
        console.print("[yellow]Atenção: a exportação inclui registros marcados como "
                      "não-contatar. Não use este arquivo para disparo.[/yellow]")


@prospects.command("nao-contatar")
@click.argument("prospect_id")
def prospects_nao_contatar(prospect_id):
    """Registra pedido de oposição do titular (LGPD Art. 18)."""
    from src.prospects import RepositorioProspects

    with RepositorioProspects() as repo:
        ok = repo.marcar_nao_contatar(prospect_id)

    if ok:
        console.print(f"[green]{prospect_id} marcado como não-contatar.[/green]")
    else:
        console.print(f"[red]Prospect {prospect_id} não encontrado.[/red]")


@prospects.command("coletar")
@click.option("--url", "-u", "urls", multiple=True, required=True, help="URL a coletar (repetível)")
@click.option("--salvar/--simular", default=True, show_default=True,
              help="Gravar na carteira ou apenas exibir o que seria coletado")
def prospects_coletar(urls, salvar):
    """
    Coleta prospects de páginas públicas via ScrapeGraphAI.

    Requer o extra opcional: pip install -e ".[prospects]" (Python 3.12+).
    Respeita robots.txt e a lista de domínios bloqueados.
    """
    from src.prospects.coletor import Coletor, ColetorIndisponivel
    from src.prospects import RepositorioProspects

    try:
        coletor = Coletor()
    except ColetorIndisponivel as erro:
        from rich.markup import escape
        console.print(f"[red]{escape(str(erro))}[/red]")
        sys.exit(1)

    achados = coletor.coletar_muitos(list(urls))
    if not achados:
        console.print("[yellow]Nenhum prospect coletado.[/yellow]")
        return

    for p in achados:
        console.print(f"  [bold]{p.score:.1f}[/bold]  {p.nome}  [dim]{p.origem.fonte}[/dim]")

    if salvar:
        with RepositorioProspects() as repo:
            repo.salvar_muitos(achados)
        console.print(f"[green]{len(achados)} prospect(s) gravado(s) na carteira.[/green]")
    else:
        console.print(f"[dim]Simulação: {len(achados)} prospect(s) não foram gravados.[/dim]")




# ────────────────────────────────── Destinos turísticos ────────────────────

@cli.group()
def destinos():
    """Mapa de destinos turísticos — as praças de prospecção."""
    pass


@destinos.command("listar")
@click.option("--uf", "-u", help="Filtrar por UF (sigla)")
@click.option("--relevancia", "-r", type=click.Choice(["alta", "media", "baixa"]),
              help="Filtrar por relevância para o modelo Zion")
@click.option("--bioma", "-b", help="Filtrar por bioma")
@click.option("--prioridade", is_flag=True, help="Ordenar por relevância em vez de por ranking da UF")
def destinos_listar(uf, relevancia, bioma, prioridade):
    """Lista os destinos mapeados."""
    from src.prospects.destinos import listar

    itens = listar(uf=uf, relevancia=relevancia, bioma=bioma, por_relevancia=prioridade)
    if not itens:
        console.print("[yellow]Nenhum destino com esse filtro.[/yellow]")
        return

    cor = {"prioridade estratégica": "bright_green", "alta prioridade": "green",
           "boa oportunidade": "yellow", "monitoramento": "bright_black",
           "baixa prioridade": "red"}
    tabela = Table(title="ZION DESTINATION SCORE — Praças de Prospecção")
    for coluna in ("UF", "Score", "Município", "Classificação", "Vocação", "Sazonalidade"):
        tabela.add_column(coluna, justify="right" if coluna == "Score" else "left")

    for d in itens:
        tabela.add_row(
            d.uf, str(d.destination_score), d.municipio,
            f"[{cor.get(d.classificacao, 'white')}]{d.classificacao}[/]",
            d.vocacao, d.sazonalidade,
        )

    console.print(tabela)
    altas = sum(1 for d in itens if d.destination_score >= 75)
    console.print(f"[dim]{len(itens)} destino(s) · {altas} de alta prioridade ou acima.[/dim]")


@destinos.command("resumo")
def destinos_resumo():
    """Contagem de destinos por UF e relevância."""
    from src.prospects.destinos import resumo

    dados = resumo()
    if not dados:
        console.print("[yellow]Nenhum destino carregado.[/yellow]")
        return

    tabela = Table(title="Destinos por UF")
    for coluna in ("UF", "Total", "Alta", "Média", "Baixa"):
        tabela.add_column(coluna, justify="right" if coluna != "UF" else "left")
    for uf, b in sorted(dados.items()):
        tabela.add_row(uf, str(b["total"]), str(b["alta"]), str(b["media"]), str(b["baixa"]))
    console.print(tabela)


@destinos.command("mapear")
@click.argument("uf")
@click.option("--top", "-n", "quantos", type=int, default=5, show_default=True,
              help="Quantos destinos recomendar como prioridade máxima")
def destinos_mapear(uf, quantos):
    """
    Executa MAPEAR [ESTADO]: pontua, classifica e recomenda os TOP N.

    Segue o ZION MARKET INTELLIGENCE & LEAD ENGINE, seção 20.
    """
    from src.prospects.destinos import consultas_prospeccao, listar
    from src.prospects.scoring import PESOS_DESTINO

    itens = sorted(listar(uf=uf), key=lambda d: -d.destination_score)
    if not itens:
        console.print(f"[red]{uf.upper()} não está mapeado.[/red]")
        return

    console.print(Panel(
        f"[bold]{uf.upper()}[/bold] · {len(itens)} destinos mapeados\n"
        f"[dim]ZION DESTINATION SCORE — 100 pontos em 7 dimensões[/dim]",
        title="Mapeamento de Estado",
    ))

    faixas = [("TOP 5 · PRIORIDADE MÁXIMA", itens[:5]),
              ("TOP 6–10 · ALTA PRIORIDADE", itens[5:10]),
              ("TOP 11–20 · MAPEAMENTO ESTRATÉGICO", itens[10:20])]

    for titulo, grupo in faixas:
        if not grupo:
            continue
        tabela = Table(title=titulo)
        tabela.add_column("Score", justify="right")
        for coluna in ("Município", "Classificação", "Vocação"):
            tabela.add_column(coluna)
        for d in grupo:
            tabela.add_row(str(d.destination_score), d.municipio, d.classificacao, d.vocacao)
        console.print(tabela)

    console.print(f"\n[bold]Recomendação — comece por estes {quantos}:[/bold]\n")
    for i, d in enumerate(itens[:quantos], 1):
        parcelas = " · ".join(
            f"{k} {v}/{PESOS_DESTINO[k]}" for k, v in d.notas.items())
        console.print(f"[bold]{i}. {d.municipio}[/bold] — {d.destination_score}/100 "
                      f"({d.classificacao})")
        console.print(f"   [dim]{parcelas}[/dim]")
        console.print(f"   {d.nota}\n")

    console.print("[dim]Próximo passo: zion-ai destinos prospectar "
                  f"\"{itens[0].municipio}\" --uf {uf.upper()}[/dim]")

@destinos.command("prospectar")
@click.argument("municipio")
@click.option("--uf", "-u", required=True, help="UF do município")
def destinos_prospectar(municipio, uf):
    """Mostra por onde começar a prospecção num destino."""
    from src.prospects.destinos import consultas_prospeccao, listar

    achados = [d for d in listar(uf=uf)
               if d.municipio.lower().startswith(municipio.strip().lower())]
    if not achados:
        console.print(f"[red]{municipio}/{uf} não está no mapa de destinos.[/red]")
        return

    d = achados[0]
    console.print(Panel(
        f"[bold]{d.municipio} / {d.uf}[/bold] · {d.regiao_turistica}\n"
        f"{d.vocacao} · {d.bioma} · pico no {d.sazonalidade}\n\n{d.nota}",
        title=f"Relevância Zion: {d.relevancia_zion}",
    ))

    for grupo, termos in consultas_prospeccao(d).items():
        console.print(f"\n[bold]{grupo}[/bold]")
        for t in termos:
            console.print(f"  · {t}")

    console.print("\n[dim]Confira os termos de uso e o robots.txt de cada fonte antes de "
                  "coletar. O coletor recusa domínios bloqueados de todo modo.[/dim]")



if __name__ == "__main__":
    cli()
