"""
Análise consolidada e relatório do ZION TRAFFIC & ACQUISITION ARCHITECT™.
"""

from datetime import date
from typing import List, Optional

from src.crm.models import BaseComercial
from src.traffic.atribuicao import atribuir, leitura_da_atribuicao
from src.traffic.diagnostico import diagnosticar, decidir
from src.traffic.metricas import agregar, avaliar_gate, calcular_metricas
from src.traffic.models import (
    AtribuicaoCampanha,
    ContaTrafego,
    EtapaCadeia,
    RelatorioTrafego,
)


def _num(valor: float, casas: int = 0) -> str:
    return f"{valor:,.{casas}f}".replace(",", "§").replace(".", ",").replace("§", ".")


def _brl(valor: Optional[float]) -> str:
    if valor is None:
        return "—"
    if abs(valor) >= 1_000_000:
        return f"R$ {_num(valor / 1_000_000, 2)} mi"
    return f"R$ {_num(valor)}"


def _pct(valor: Optional[float], casas: int = 2) -> str:
    return f"{_num((valor or 0) * 100, casas)}%" if valor is not None else "—"


def analisar_conta(
    conta: ContaTrafego, base: Optional[BaseComercial] = None
) -> RelatorioTrafego:
    """Roda gate, diagnóstico, decisão e — se houver CRM — atribuição real."""
    gates = [avaliar_gate(c) for c in conta.campanhas]

    diagnosticos = []
    decisoes = []
    for campanha in conta.campanhas:
        margem = conta.margem_por_produto.get(campanha.produto.value)
        d = diagnosticar(campanha, margem)
        diagnosticos.append(d)
        decisoes.append(decidir(campanha, d, margem))

    total = agregar(conta.campanhas)
    geral = calcular_metricas(total)

    atribuicao: List[AtribuicaoCampanha] = []
    if base is not None:
        atribuicao = atribuir(conta, base)

    # O gargalo geral é o ponto mais recorrente entre as campanhas com volume.
    contagem = {}
    for d in diagnosticos:
        if d.gargalo and d.volume_suficiente:
            contagem[d.gargalo] = contagem.get(d.gargalo, 0) + 1
    gargalo_geral = max(contagem, key=contagem.get) if contagem else None

    return RelatorioTrafego(
        data=(conta.data_referencia or date.today()).strftime("%d/%m/%Y"),
        periodo=conta.periodo,
        investimento_total_brl=total.investimento_brl,
        receita_total_brl=total.receita_brl,
        roas_geral=geral.roas,
        leads=total.leads,
        oportunidades=total.oportunidades,
        vendas=total.vendas,
        cpqo_geral_brl=geral.cpqo_brl,
        cac_geral_brl=geral.cac_brl,
        gates=gates,
        diagnosticos=diagnosticos,
        decisoes=decisoes,
        atribuicao=atribuicao,
        gargalo_geral=gargalo_geral,
        acoes_recomendadas=_acoes(
            gates, diagnosticos, decisoes, atribuicao, gargalo_geral, conta
        ),
    )


def _acoes(gates, diagnosticos, decisoes, atribuicao, gargalo_geral, conta=None) -> List[str]:
    acoes: List[str] = []

    bloqueadas = [g for g in gates if not g.liberada and g.perguntas_sem_resposta]
    if bloqueadas:
        acoes.append(
            f"Não subir {len(bloqueadas)} campanha(s) sem responder o briefing: "
            + ", ".join(g.campanha_id for g in bloqueadas) + "."
        )

    pausar = [d for d in decisoes if d.acao == "pausar"]
    if pausar:
        acoes.append(
            f"Pausar após verificar rastreamento: "
            + ", ".join(d.campanha_id for d in pausar) + "."
        )

    if gargalo_geral:
        acoes.append(
            f"O gargalo predominante da conta está em {gargalo_geral.value}. "
            f"Corrigir ali antes de mexer em orçamento — o resto é sintoma."
        )

    escalar = [d for d in decisoes if d.acao == "escalar"]
    if escalar:
        acoes.append(
            f"Avaliar escala de {', '.join(d.campanha_id for d in escalar)}, "
            f"confirmando antes a capacidade comercial e de entrega."
        )

    if atribuicao:
        divergentes = [a for a in atribuicao if a.divergencia_de_ranking]
        if divergentes:
            acoes.append(
                f"Rever alocação de orçamento: {len(divergentes)} campanha(s) têm posição "
                f"muito diferente em volume de leads e em receita gerada."
            )

    investigar = [d for d in decisoes if d.acao == "investigar"]
    if investigar:
        acoes.append(
            f"Investigar antes de qualquer mudança de verba: "
            + ", ".join(d.campanha_id for d in investigar) + "."
        )

    return acoes[:5]


def gerar_relatorio_trafego(
    r: RelatorioTrafego, conta: Optional[ContaTrafego] = None
) -> str:
    """Monta o relatório de aquisição em Markdown."""
    linhas: List[str] = [
        "# Relatório de Aquisição Zion",
        "",
        f"**Data:** {r.data}" + (f" · **Período:** {r.periodo}" if r.periodo else ""),
        "",
        "---",
        "",
        "## 1. Painel",
        "",
        "| Indicador | Valor |",
        "|---|---:|",
        f"| Investimento | {_brl(r.investimento_total_brl)} |",
        f"| Receita atribuída | {_brl(r.receita_total_brl)} |",
        f"| ROAS | {_num(r.roas_geral, 2) + 'x' if r.roas_geral else '—'} |",
        f"| Leads | {r.leads} |",
        f"| Oportunidades | {r.oportunidades} |",
        f"| Vendas | {r.vendas} |",
        f"| **Custo por oportunidade qualificada** | **{_brl(r.cpqo_geral_brl)}** |",
        f"| CAC | {_brl(r.cac_geral_brl)} |",
        "",
        "> Lead barato não é sucesso. A métrica que manda é o custo por oportunidade "
        "qualificada, e depois dela o CAC e a receita por real investido.",
        "",
    ]

    bloqueadas = [g for g in r.gates if not g.liberada]
    if bloqueadas:
        linhas += ["## 2. Gate de Campanha", ""]
        for g in bloqueadas:
            linhas.append(f"### {g.campanha_id}")
            linhas += ["", f"**{g.veredito}**", ""]
            if g.perguntas_sem_resposta:
                linhas.append("Perguntas sem resposta:")
                linhas += [f"- {p}" for p in g.perguntas_sem_resposta]
                linhas.append("")
            if g.pendencias_estruturais:
                linhas.append("Pendências de estrutura:")
                linhas += [f"- {p}" for p in g.pendencias_estruturais]
                linhas.append("")

    linhas += [
        "## 3. Diagnóstico por Campanha",
        "",
        "| Campanha | Invest. | CTR | CPL | CPQO | CAC | ROAS | Gargalo | Decisão |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    decisao_por_id = {d.campanha_id: d for d in r.decisoes}
    for d in r.diagnosticos:
        m = d.metricas
        acao = decisao_por_id[d.campanha_id].acao
        linhas.append(
            f"| {d.nome} | {_brl(m.investimento_brl)} | {_pct(m.ctr)} | {_brl(m.cpl_brl)} | "
            f"{_brl(m.cpqo_brl)} | {_brl(m.cac_brl)} | "
            f"{(_num(m.roas, 2) + 'x') if m.roas else '—'} | "
            f"{d.gargalo.value if d.gargalo else '—'} | {acao} |"
        )
    linhas.append("")

    for d in r.diagnosticos:
        if not d.achados:
            continue
        linhas += [f"### {d.nome}", "", d.leitura, ""]
        for a in d.achados:
            linhas += [
                f"**[{a.gravidade.upper()}] {a.etapa.value}** — {a.sintoma}",
                "",
                f"- Causa provável: {a.causa_provavel}",
                f"- Ação: {a.acao}",
                f"- Base estatística: {a.confianca_estatistica}",
                "",
            ]
        decisao = decisao_por_id[d.campanha_id]
        linhas += [f"**Decisão: {decisao.acao}.** {decisao.justificativa}", ""]
        if decisao.bloqueios_de_escala:
            linhas.append("Bloqueios de escala:")
            linhas += [f"- {b}" for b in decisao.bloqueios_de_escala]
            linhas.append("")

    if r.atribuicao:
        linhas += [
            "## 4. Atribuição Real — o que o CRM diz",
            "",
            "A plataforma sabe quanto custou o lead. Só o CRM sabe se ele virou negócio.",
            "",
            "| Campanha | Invest. | Leads | Qualif. | Oport. | Clientes | Receita | CPL | CPQO | CAC | ROAS |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for a in sorted(r.atribuicao, key=lambda x: x.receita_brl, reverse=True):
            linhas.append(
                f"| {a.nome} | {_brl(a.investimento_brl)} | {a.leads} | {a.qualificados} | "
                f"{a.oportunidades} | {a.clientes} | {_brl(a.receita_brl)} | {_brl(a.cpl_brl)} | "
                f"{_brl(a.cpqo_brl)} | {_brl(a.cac_brl)} | "
                f"{(_num(a.roas, 2) + 'x') if a.roas else '—'} |"
            )
        linhas.append("")

        observacoes = leitura_da_atribuicao(r.atribuicao, conta)
        if observacoes:
            linhas += ["**Leitura:**", ""]
            linhas += [f"- {o}" for o in observacoes]
            linhas.append("")

    if r.acoes_recomendadas:
        linhas += ["## 5. Ações Recomendadas", ""]
        for i, acao in enumerate(r.acoes_recomendadas, start=1):
            linhas.append(f"{i}. {acao}")
        linhas.append("")

    return "\n".join(linhas)
