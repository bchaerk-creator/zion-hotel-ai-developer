"""
Relatório comercial do ZION CRM & LEAD INTELLIGENCE™.
"""

from typing import List

from src.crm.models import RelatorioComercial, Temperatura

ICONE = {
    Temperatura.OPORTUNIDADE: "🔥",
    Temperatura.QUENTE: "🟢",
    Temperatura.MORNO: "🟡",
    Temperatura.FRIO: "🔴",
}


def _num(valor: float, casas: int = 0) -> str:
    return f"{valor:,.{casas}f}".replace(",", "§").replace(".", ",").replace("§", ".")


def _brl(valor: float) -> str:
    if abs(valor) >= 1_000_000:
        return f"R$ {_num(valor / 1_000_000, 2)} mi"
    return f"R$ {_num(valor)}"


def gerar_relatorio_comercial(r: RelatorioComercial) -> str:
    """Monta o relatório comercial completo em Markdown."""
    linhas: List[str] = [
        "# Relatório Comercial Zion",
        "",
        f"**Data:** {r.data}  ",
        f"**Base analisada:** {r.total_leads} leads",
        "",
        "---",
        "",
        "## 1. Painel",
        "",
        "| Indicador | Valor |",
        "|---|---:|",
        f"| Total de leads | {r.total_leads} |",
        f"| Novos leads | {r.novos} |",
        f"| Oportunidades | {r.oportunidades} |",
        f"| Leads quentes | {r.quentes} |",
        f"| Leads parados | {r.parados} |",
        f"| Follow-ups atrasados | {r.followups_atrasados} |",
        f"| Pipeline aberto | {_brl(r.pipeline_aberto_brl)} |",
        "",
    ]

    linhas += ["## 2. Prioridade Comercial", ""]
    linhas += [
        "| # | Lead | Perfil | Temp. | Score | Confiança | Porta | Próximo passo |",
        "|---:|---|---|:--:|---:|---:|---|---|",
    ]
    for q in r.qualificados[:15]:
        linhas.append(
            f"| {q.prioridade} | {q.lead.nome} | {q.lead.perfil.value.split('_', 1)[1]} | "
            f"{ICONE[q.score.temperatura]} | {_num(q.score.score, 1)} | "
            f"{_num(q.score.confianca * 100)}% | {q.roteamento.porta.value} | "
            f"{q.roteamento.proximo_passo_logico} |"
        )
    linhas.append("")

    baixa = [q for q in r.qualificados if q.score.confianca < 0.5]
    if baixa:
        linhas += [
            "> **Atenção à confiança.** "
            f"{len(baixa)} lead(s) têm score apoiado em menos de metade das dimensões. "
            "Score baixo por falta de informação não é lead ruim — é lead não qualificado. "
            "Levantar dado antes de descartar.",
            "",
        ]

    if r.funil:
        f = r.funil
        linhas += ["## 3. Funil", "", "| Estágio | Volume | Conversão da anterior | Valor |",
                   "|---|---:|---:|---:|"]
        for etapa in f.etapas:
            conv = f"{_num(etapa.conversao_da_anterior * 100, 1)}%" if etapa.conversao_da_anterior is not None else "—"
            linhas.append(
                f"| {etapa.estagio.value} | {etapa.quantidade} | {conv} | "
                f"{_brl(etapa.valor_potencial_brl)} |"
            )
        linhas += ["", f"**Diagnóstico:** {f.diagnostico}", ""]
        linhas.append(
            f"**Fechamento:** {f.ganhos} ganho(s), {f.perdidos} perdido(s), "
            f"conversão total de "
            + (f"{_num((f.taxa_conversao_total or 0) * 100, 1)}%" if f.taxa_conversao_total is not None else "n/a")
            + "."
        )
        linhas.append("")
        if f.motivos_perda:
            linhas += ["**Motivos de perda:**", ""]
            for motivo, n in sorted(f.motivos_perda.items(), key=lambda x: -x[1]):
                linhas.append(f"- {motivo.replace('_', ' ')}: {n}")
            linhas.append("")

    if r.higiene:
        linhas += ["## 4. Higiene da Base", ""]
        for a in r.higiene:
            linhas.append(f"### [{a.gravidade.upper()}] {a.tema}")
            linhas += ["", a.descricao, ""]
            if a.leads:
                amostra = ", ".join(a.leads[:8])
                extra = f" (+{len(a.leads) - 8})" if len(a.leads) > 8 else ""
                linhas += [f"Afeta {len(a.leads)} registro(s): {amostra}{extra}", ""]
            linhas += [f"**Ação:** {a.acao}", ""]

    if r.reativacao:
        linhas += [
            "## 5. Lista de Reativação",
            "",
            "Silêncio não é desinteresse. Pode ser mensagem errada, canal errado, oferta "
            "errada ou timing. Antes de perder, requalificar.",
            "",
            "| Lead | Score | Parado há | Porta | Provável problema | Abordagem |",
            "|---|---:|---:|---|---|---|",
        ]
        for i in r.reativacao[:10]:
            dias = f"{i.dias_parado} dias" if i.dias_parado is not None else "—"
            linhas.append(
                f"| {i.nome} | {_num(i.score, 1)} | {dias} | {i.porta_potencial.value} | "
                f"{i.provavel_problema} | {i.abordagem_recomendada} |"
            )
        linhas.append("")

    if r.acoes_recomendadas:
        linhas += ["## 6. Ações Recomendadas", ""]
        for i, acao in enumerate(r.acoes_recomendadas, start=1):
            linhas.append(f"{i}. {acao}")
        linhas.append("")

    return "\n".join(linhas)


def briefing_lead(qualificado) -> str:
    """PREPARAR REUNIÃO — briefing de um lead específico."""
    lead, score, rot = qualificado.lead, qualificado.score, qualificado.roteamento

    linhas = [
        f"# Briefing — {lead.nome}",
        "",
        f"**Perfil:** {lead.perfil.value} · **Estágio:** {lead.estagio.value} · "
        f"**Temperatura:** {ICONE[score.temperatura]} {score.temperatura.value}  ",
        f"**Zion Lead Score™:** {_num(score.score, 1)}/10 "
        f"(confiança {_num(score.confianca * 100)}%)",
        "",
        "## Composição do score",
        "",
        "| Dimensão | Nota | Peso | Base | Justificativa |",
        "|---|---:|---:|---|---|",
    ]
    for d in score.dimensoes:
        linhas.append(
            f"| {d.nome} | {_num(d.valor, 1)} | {_num(d.peso * 100)}% | {d.base} | "
            f"{d.justificativa} |"
        )

    linhas += ["", "## O que ele tem", ""]
    possui = lead.ativos.possui()
    linhas.append("- Ativos: " + (", ".join(possui) if possui else "nenhum confirmado"))
    if lead.terreno.area_ha:
        linhas.append(f"- Terreno: {_num(lead.terreno.area_ha, 1)} ha em {lead.terreno.localizacao or 'local não informado'}")
    if lead.financeiro.capital_disponivel_brl:
        linhas.append(f"- Capital declarado: {_brl(lead.financeiro.capital_disponivel_brl)}")
    if lead.projeto.estagio:
        linhas.append(f"- Projeto em estágio de {lead.projeto.estagio}")

    linhas += [
        "",
        "## Roteamento",
        "",
        f"**Porta:** {rot.porta.value}  ",
        f"**Por quê:** {rot.justificativa}  ",
        f"**Próximo passo lógico:** {rot.proximo_passo_logico}",
        "",
    ]

    if rot.nao_ofertar:
        linhas += ["**Não ofertar agora:**", ""]
        linhas += [f"- {n}" for n in rot.nao_ofertar]
        linhas.append("")

    if score.alertas:
        linhas += ["## Alertas", ""]
        linhas += [f"- {a}" for a in score.alertas]
        linhas.append("")

    if rot.perguntas_de_qualificacao:
        linhas += ["## Perguntas de qualificação para esta conversa", ""]
        for i, p in enumerate(rot.perguntas_de_qualificacao, start=1):
            linhas.append(f"{i}. {p}")
        linhas.append("")

    if lead.interacoes:
        linhas += ["## Histórico", ""]
        for it in lead.interacoes[-5:]:
            resposta = it.resposta or "sem resposta"
            linhas.append(f"- {it.data.strftime('%d/%m/%Y')} ({it.canal}): {it.o_que_foi_enviado} → {resposta}")
        linhas.append("")

    return "\n".join(linhas)
