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


# ---------------------------------------------------------------------------
# Land Bank no CRM
# ---------------------------------------------------------------------------

def _ha(valor: float) -> str:
    return f"{_num(valor, 1)} ha"


def gerar_painel_territorial(p) -> str:
    """
    Painel Land Bank × CRM em Markdown.

    Três números de diretoria — oportunidades, investimento declarado e
    hectares — cada um com a definição e a cobertura do lado, para que o
    número possa ser defendido numa reunião.
    """
    o, inv, a = p.oportunidades, p.investimentos, p.areas

    linhas: List[str] = [
        "# Land Bank no CRM",
        "",
        f"**Data:** {p.data}  ",
        f"**Base:** {p.base_nome}  ",
        f"**Banco de áreas:** {p.land_bank_nome or 'não carregado'}",
        "",
        "| Total | Número | O que é |",
        "|---|---:|---|",
        f"| Oportunidades abertas | **{o.abertas}** | Leads em estágio aberto — o pipeline real |",
        f"| Investimento declarado | **{_brl(inv.declarado_brl)}** | "
        f"Declarado por {inv.leads_declarantes} de {o.total_base} leads — não verificado |",
        f"| Áreas no banco | **{_ha(a.total_consolidado_ha)}** | "
        f"{_ha(a.land_bank_ha)} no Land Bank + {_ha(a.originacao_aberta_ha)} em originação |",
        "",
        "---",
        "",
        "## 1. Oportunidades",
        "",
        "| Recorte | Qtd. |",
        "|---|---:|",
        f"| Abertas (pipeline) | {o.abertas} |",
        f"| Com oferta na mesa | {o.com_oferta_na_mesa} |",
        f"| Sinalizadas como oportunidade pelo score | {o.sinalizadas_quentes} |",
        f"| Territoriais (trazem terra) | {o.territoriais} |",
        f"| Ganhas | {o.ganhas} |",
        f"| Perdidas | {o.perdidas} |",
        f"| **Base total** | **{o.total_base}** |",
        "",
    ]

    if o.por_estagio:
        linhas += ["**Por estágio:** " + " · ".join(
            f"{k.split('_', 1)[1]}: {v}" for k, v in o.por_estagio.items()
        ), ""]

    linhas += [
        "## 2. Investimento declarado",
        "",
        "Soma do que a base declarou pretender ou poder investir. Ninguém conferiu "
        "extrato: serve para dimensionar apetite, não para lastrear captação.",
        "",
        "| Recorte | Valor |",
        "|---|---:|",
        f"| Declarado total | {_brl(inv.declarado_brl)} |",
        f"| Em pipeline aberto | {_brl(inv.declarado_aberto_brl)} |",
        f"| Em leads ganhos | {_brl(inv.declarado_ganho_brl)} |",
        f"| Em leads perdidos | {_brl(inv.declarado_perdido_brl)} |",
        f"| Ticket médio declarado | {_brl(inv.ticket_medio_brl)} |",
        f"| Maior declaração | {_brl(inv.maior_declaracao_brl)}"
        + (f" — {inv.maior_declarante}" if inv.maior_declarante else "") + " |",
        f"| Cobertura | {_num(inv.cobertura * 100)}% da base "
        f"({inv.leads_sem_declaracao} sem declaração) |",
        "",
        f"> Pipeline Zion (receita da própria Zion, número diferente e não somável a este): "
        f"{_brl(inv.pipeline_zion_brl)}.",
        "",
        "## 3. Áreas no banco de áreas",
        "",
        "| Origem | Hectares |",
        "|---|---:|",
        f"| Land Bank — {a.land_bank_glebas} gleba(s) | {_ha(a.land_bank_ha)} |",
        f"| — sob controle (própria + contratada) | {_ha(a.sob_controle_ha)} |",
        f"| Originação no CRM (leads abertos, fora do banco) | {_ha(a.originacao_aberta_ha)} |",
        f"| **Total consolidado** | **{_ha(a.total_consolidado_ha)}** |",
        f"| Sobreposição descontada (já no banco e no CRM) | {_ha(a.sobreposicao_ha)} |",
        f"| Fora do pipeline (leads ganhos/perdidos) | {_ha(a.originacao_fechada_ha)} |",
        "",
    ]

    if a.por_status_ha:
        linhas += ["**Land Bank por status dominial:** " + " · ".join(
            f"{k.replace('_', ' ')}: {_num(v)} ha" for k, v in a.por_status_ha.items()
        ), ""]

    if a.por_uf_ha:
        linhas += [
            "| UF | No banco | Em originação | Somado |",
            "|---|---:|---:|---:|",
        ]
        for uf, d in a.por_uf_ha.items():
            linhas.append(
                f"| {uf} | {_num(d['land_bank_ha'])} ha | {_num(d['originacao_ha'])} ha | "
                f"{_num(d['land_bank_ha'] + d['originacao_ha'])} ha |"
            )
        linhas.append("")

    if p.vinculos:
        linhas += ["## 4. Vínculos lead ↔ gleba", "",
                   "| Lead | Gleba | Município | Área declarada | Área registrada | Status |",
                   "|---|---|---|---:|---:|---|"]
        for v in p.vinculos:
            linhas.append(
                f"| {v.lead_nome} | {v.gleba_id} — {v.gleba_nome} | {v.municipio}/{v.uf} | "
                f"{_ha(v.area_lead_ha) if v.area_lead_ha else '—'} | {_ha(v.area_gleba_ha or 0)} | "
                f"{v.status_dominial.value if v.status_dominial else '—'} |"
            )
        linhas.append("")

    if p.originacao:
        linhas += [
            "## 5. Terra no CRM fora do banco de áreas",
            "",
            "Ordenado por hectare — é o que falta para um projeto agrupado fechar escala. "
            "O score diz quais desses hectares são trabalháveis hoje.",
            "",
            "| Lead | Local | Área | Estágio | Temp. | Score | Investimento declarado |",
            "|---|---|---:|---|:--:|---:|---:|",
        ]
        for i in p.originacao:
            local = f"{i.municipio or '—'}/{i.uf or '—'}"
            linhas.append(
                f"| {i.nome} | {local} | {_ha(i.area_ha)} | {i.estagio.value.split('_', 1)[1]} | "
                f"{ICONE[i.temperatura]} | {_num(i.score, 1)} | "
                f"{_brl(i.investimento_declarado_brl) if i.investimento_declarado_brl else '—'} |"
            )
        linhas.append("")

    if p.alertas:
        linhas += ["## 6. Alertas", ""]
        linhas += [f"- {x}" for x in p.alertas]
        linhas.append("")

    return "\n".join(linhas)
