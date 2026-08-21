"""
Relatório executivo do Land Bank Zion.

Converte o resultado da engine de carbono em um documento Markdown pronto
para mesa de negociação, comitê de investimento e due diligence.
"""

from typing import List, Optional

from src.models.land_bank import (
    ClasseElegibilidade,
    ClusterCarbono,
    ResultadoLandBank,
    StatusDominial,
)


def _num(valor: float, casas: int = 0) -> str:
    """Formata número no padrão brasileiro."""
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "§").replace(".", ",").replace("§", ".")


def _brl(valor: float) -> str:
    """Formata valor monetário em BRL."""
    if abs(valor) >= 1_000_000:
        return f"R$ {_num(valor / 1_000_000, 2)} mi"
    return f"R$ {_num(valor, 0)}"


def _pct(valor: Optional[float]) -> str:
    return f"{_num(valor * 100, 1)}%" if valor is not None else "n/a"


def _rotulo_status(status: StatusDominial) -> str:
    return {
        StatusDominial.PROPRIO: "próprio",
        StatusDominial.CONTRATADO: "contratado",
        StatusDominial.EM_NEGOCIACAO: "em negociação",
        StatusDominial.PROSPECCAO: "prospecção",
    }[status]


def _sumario(r: ResultadoLandBank) -> List[str]:
    linhas = [
        "## 1. Sumário Executivo",
        "",
        f"O Land Bank **{r.nome}** reúne **{r.total_glebas} glebas** e "
        f"**{_num(r.area_total_ha)} hectares** mapeados, dos quais "
        f"**{_num(r.area_elegivel_ha)} ha** são tecnicamente elegíveis para originação de "
        f"crédito de carbono em um horizonte de {r.horizonte_anos} anos.",
        "",
        "| Indicador | Valor |",
        "|---|---|",
        f"| Área total mapeada | {_num(r.area_total_ha)} ha |",
        f"| Área elegível (núcleo bancável) | {_num(r.area_elegivel_ha)} ha |",
        f"| Área com potencial condicionado | {_num(r.area_condicionada_ha)} ha |",
        f"| Área já contratada | {_num(r.area_contratada_ha)} ha |",
        f"| Área em pipeline (negociação/prospecção) | {_num(r.area_prospeccao_ha)} ha |",
        f"| **Créditos líquidos no horizonte** | **{_num(r.vcus_liquidos)} tCO2e** |",
        f"| Créditos já travados por contrato | {_num(r.vcus_contratados)} tCO2e |",
        f"| Créditos condicionados (não projetar) | {_num(r.vcus_condicionados)} tCO2e |",
        f"| Receita bruta projetada | {_brl(r.receita_bruta_brl)} |",
        f"| Resultado líquido Zion (nominal) | {_brl(r.resultado_liquido_zion_brl)} |",
        f"| VPL consolidado | {_brl(r.vpl_total_brl)} |",
        f"| Carbon Readiness médio | {_num(r.readiness_medio, 2)}/10 |",
        f"| Clusters identificados | {len(r.clusters)} |",
    ]

    if r.meta_tco2e:
        linhas.append(
            f"| Meta do portfólio | {_num(r.meta_tco2e)} tCO2e "
            f"({_pct(r.atingimento_meta)} atingido) |"
        )

    linhas.append("")
    return linhas


def _painel_glebas(r: ResultadoLandBank) -> List[str]:
    linhas = [
        "## 2. Painel de Glebas",
        "",
        "| ID | Gleba | Município | Área (ha) | Elegível (ha) | tCO2e líq. | Status | Readiness |",
        "|---|---|---|---:|---:|---:|---|---:|",
    ]
    for g in sorted(r.glebas, key=lambda x: x.vcus_liquidos, reverse=True):
        linhas.append(
            f"| {g.gleba_id} | {g.nome} | {g.municipio}/{g.uf} | {_num(g.area_total_ha)} | "
            f"{_num(g.area_elegivel_ha)} | {_num(g.vcus_liquidos)} | "
            f"{_rotulo_status(g.status_dominial)} | {_num(g.readiness_score, 1)} |"
        )
    linhas.append("")

    bloqueadas = [g for g in r.glebas if g.bloqueios]
    if bloqueadas:
        linhas += ["### Glebas com bloqueio de elegibilidade", ""]
        for g in bloqueadas:
            linhas.append(f"**{g.gleba_id} — {g.nome}**")
            for b in g.bloqueios:
                linhas.append(f"- {b}")
            linhas.append("")
    return linhas


def _detalhe_cluster(c: ClusterCarbono, r: ResultadoLandBank) -> List[str]:
    glebas = [g for g in r.glebas if g.gleba_id in c.glebas_ids]
    linhas = [
        f"### {c.id} — {c.nome}",
        "",
        f"**Municípios:** {', '.join(c.municipios)}  ",
        f"**Glebas:** {', '.join(c.glebas_ids)}  ",
        f"**Raio máximo do centroide:** {_num(c.raio_max_km, 1)} km  ",
        f"**Escala:** {c.escala}"
        + (f" (faltam {_num(c.gap_escala_ha)} ha)" if c.gap_escala_ha > 0 else ""),
        "",
        "| Indicador | Valor |",
        "|---|---|",
        f"| Área elegível | {_num(c.area_elegivel_ha)} ha |",
        f"| Área contratada | {_num(c.area_contratada_ha)} ha |",
        f"| Créditos líquidos | {_num(c.vcus_liquidos)} tCO2e |",
        f"| Receita bruta | {_brl(c.receita_bruta_brl)} |",
        f"| Repasse a terrenistas | {_brl(c.receita_terrenistas_brl)} |",
        f"| Custo de estruturação | {_brl(c.custo_estruturacao_brl)} |",
        f"| Custo de implantação | {_brl(c.custo_implantacao_brl)} |",
        f"| Custo de MRV e verificação | {_brl(c.custo_mrv_brl)} |",
        f"| Custo de originação da terra | {_brl(c.custo_entrada_brl)} |",
        f"| Custo por crédito | R$ {_num(c.custo_por_vcu_brl, 2)}/tCO2e |",
        f"| Preço de equilíbrio | "
        + (f"R$ {_num(c.preco_equilibrio_brl, 2)}/tCO2e" if c.preco_equilibrio_brl else "fora de faixa")
        + " |",
        f"| Pré-venda mínima para virar o VPL | "
        + (
            "não é necessária"
            if c.prevenda_minima == 0
            else (f"{_num(c.prevenda_minima * 100, 0)}% dos créditos" if c.prevenda_minima else "não resolve")
        )
        + " |",
        f"| Resultado líquido Zion | {_brl(c.resultado_liquido_zion_brl)} |",
        f"| VPL | {_brl(c.vpl_brl)} |",
        f"| TIR | {_pct(c.tir)} |",
        f"| Payback | {'ano ' + str(c.payback_ano) if c.payback_ano else 'fora do horizonte'} |",
        f"| Veredito | {'projeto viável' if c.viavel else 'não fecha nas premissas atuais'} |",
        "",
    ]

    if c.alertas:
        linhas.append("**Pontos de atenção:**")
        linhas.append("")
        for a in c.alertas:
            linhas.append(f"- {a}")
        linhas.append("")

    linhas += ["**Composição por gleba:**", "", "| Gleba | Elegível (ha) | tCO2e líq. | Rotas |", "|---|---:|---:|---|"]
    for g in glebas:
        rotas = sorted(
            {
                t.metodologia.value
                for t in g.talhoes
                if t.classe == ClasseElegibilidade.ELEGIVEL
            }
        )
        linhas.append(
            f"| {g.gleba_id} — {g.nome} | {_num(g.area_elegivel_ha)} | "
            f"{_num(g.vcus_liquidos)} | {', '.join(rotas) or '—'} |"
        )
    linhas.append("")
    return linhas


def _fluxo_caixa(c: ClusterCarbono) -> List[str]:
    """Mostra ano 0 e os anos com movimento relevante."""
    linhas = [
        f"### Fluxo de caixa — {c.id}",
        "",
        "| Ano | VCUs emitidos | Receita | Custos | Fluxo líquido | Acumulado |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for f in c.fluxo:
        relevante = f.ano == 0 or f.vcus_emitidos > 0 or abs(f.fluxo_liquido_brl) > 50_000
        if not relevante:
            continue
        linhas.append(
            f"| {f.ano} | {_num(f.vcus_emitidos)} | {_brl(f.receita_bruta_brl)} | "
            f"{_brl(f.custos_brl)} | {_brl(f.fluxo_liquido_brl)} | {_brl(f.fluxo_acumulado_brl)} |"
        )
    linhas.append("")
    linhas.append(
        "> A primeira emissão só acontece após a primeira verificação. "
        "Todo o CAPEX de restauração sai antes disso — é essa defasagem que exige "
        "capital de giro estruturado, não receita de carbono."
    )
    linhas.append("")
    return linhas


def _cenarios(r: ResultadoLandBank) -> List[str]:
    linhas = [
        "## 4. Cenários",
        "",
        "| Cenário | Preço | Produtividade | tCO2e líq. | Receita bruta | Resultado Zion | VPL |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for c in r.cenarios:
        linhas.append(
            f"| {c.nome} | {_num(c.fator_preco * 100)}% | {_num(c.fator_produtividade * 100)}% | "
            f"{_num(c.vcus_liquidos)} | {_brl(c.receita_bruta_brl)} | "
            f"{_brl(c.resultado_liquido_zion_brl)} | {_brl(c.vpl_brl)} |"
        )
    linhas.append("")
    return linhas


def _alavancas(r: ResultadoLandBank) -> List[str]:
    """Diagnóstico de o que precisa mudar para cada cluster fechar conta."""
    linhas = [
        "## 5. Alavancas de Viabilidade",
        "",
        "Projeto de carbono não quebra por falta de tonelada, quebra por descasamento de caixa: "
        "o CAPEX de restauração sai no ano 0 e o primeiro crédito só é emitido depois da primeira "
        "verificação. A tabela abaixo mostra, por cluster, o que precisa acontecer para o VPL virar.",
        "",
        "| Cluster | Custo/crédito | Preço modelado | Preço de equilíbrio | Pré-venda mínima | Veredito |",
        "|---|---:|---:|---:|---:|---|",
    ]
    preco_modelado = r.premissas.get("preco_tco2e_remocao_brl", 0.0)

    for c in sorted(r.clusters, key=lambda x: x.vpl_brl, reverse=True):
        if c.prevenda_minima == 0:
            prevenda = "dispensável"
        elif c.prevenda_minima:
            prevenda = f"{_num(c.prevenda_minima * 100, 0)}%"
        else:
            prevenda = "não resolve"

        if c.viavel:
            veredito = "fecha nas premissas atuais"
        elif c.prevenda_minima:
            veredito = "fecha com pré-venda estruturada"
        else:
            veredito = "reestruturar antes de originar"

        linhas.append(
            f"| {c.id} | R$ {_num(c.custo_por_vcu_brl, 2)} | R$ {_num(preco_modelado, 2)} | "
            + (f"R$ {_num(c.preco_equilibrio_brl, 2)}" if c.preco_equilibrio_brl else "—")
            + f" | {prevenda} | {veredito} |"
        )

    linhas += [
        "",
        "**Ordem de ataque das alavancas, da mais barata para a mais cara:**",
        "",
        "1. **Escala** — agregar área ao cluster dilui o custo fixo de estruturação e MRV "
        "sem aumentar o custo por hectare.",
        "2. **Rota metodológica** — regeneração natural assistida custa uma fração do plantio "
        "por hectare. Onde o solo e a fonte de propágulo permitem, é a rota que mais move o custo por crédito.",
        "3. **Split com o terrenista** — repartição sobre receita líquida, após recuperação do CAPEX, "
        "em vez de sobre receita bruta. Muda o resultado sem mudar uma tonelada.",
        "4. **Pré-venda com adiantamento** — offtaker paga adiantado com deságio e resolve o "
        "descasamento de caixa. É financiamento, não receita extra: use depois de esgotar as três acima.",
        "",
    ]
    return linhas


def _prioridades(r: ResultadoLandBank) -> List[str]:
    linhas = [
        "## 6. Fila de Agregação — o que travar primeiro",
        "",
    ]
    if not r.prioridades:
        linhas += ["Nenhuma gleba em pipeline. Todo o portfólio já está contratado ou é próprio.", ""]
        return linhas

    linhas += [
        "| # | Gleba | Cluster | Instrumento | Elegível (ha) | tCO2e líq. | Entrada | tCO2e/R$ mil | Destrava escala |",
        "|---:|---|---|---|---:|---:|---:|---:|---|",
    ]
    for p in r.prioridades:
        linhas.append(
            f"| {p.prioridade} | {p.gleba_id} — {p.nome} | {p.cluster_id or '—'} | "
            f"{p.instrumento_recomendado.value.replace('_', ' ')} | {_num(p.area_elegivel_ha)} | "
            f"{_num(p.vcus_liquidos)} | {_brl(p.custo_entrada_brl)} | "
            f"{_num(p.vcus_por_mil_brl, 1)} | {'sim' if p.destrava_escala else 'não'} |"
        )
    linhas.append("")
    linhas.append("**Justificativa por gleba:**")
    linhas.append("")
    for p in r.prioridades:
        linhas.append(f"{p.prioridade}. **{p.nome}** — {p.justificativa}")
    linhas.append("")
    return linhas


def _alertas(r: ResultadoLandBank) -> List[str]:
    if not r.alertas:
        return []
    linhas = ["## 7. Alertas do Portfólio", ""]
    for a in r.alertas:
        linhas.append(f"- {a}")
    linhas.append("")
    return linhas


def _premissas(r: ResultadoLandBank) -> List[str]:
    p = r.premissas
    return [
        "## 8. Premissas do Modelo",
        "",
        "| Premissa | Valor |",
        "|---|---|",
        f"| Horizonte de creditação | {p['horizonte_anos']} anos |",
        f"| Taxa de desconto | {_pct(p['taxa_desconto'])} |",
        f"| Preço remoção (ARR/SAF) | R$ {_num(p['preco_tco2e_remocao_brl'], 2)}/tCO2e |",
        f"| Preço emissão evitada (REDD) | R$ {_num(p['preco_tco2e_evitada_brl'], 2)}/tCO2e |",
        f"| Buffer de não permanência (remoção) | {_pct(p['buffer_remocao'])} |",
        f"| Buffer de não permanência (evitada) | {_pct(p['buffer_evitada'])} |",
        f"| Desconto por incerteza | {_pct(p['incerteza_desconto'])} |",
        f"| Custo de estruturação por projeto | {_brl(p['custo_estruturacao_brl'])} |",
        f"| Custo por verificação | {_brl(p['custo_verificacao_brl'])} |",
        f"| Intervalo de verificação | {p['intervalo_verificacao_anos']} anos |",
        f"| Primeira emissão | ano {p['ano_primeira_emissao']} |",
        f"| MRV fixo anual | {_brl(p['custo_mrv_fixo_ano_brl'])} |",
        f"| MRV variável | R$ {_num(p['custo_mrv_ha_ano_brl'], 2)}/ha/ano |",
        f"| Split padrão do terrenista | {_pct(p['percentual_receita_terrenista'])} |",
        f"| Escala mínima por cluster | {_num(p['area_minima_cluster_ha'])} ha |",
        f"| Escala alvo por cluster | {_num(p['area_alvo_cluster_ha'])} ha |",
        f"| Raio de clusterização | {_num(p['raio_cluster_km'])} km |",
        "",
        "> Os fatores de remoção por bioma e os preços de crédito são ordens de grandeza "
        "calibradas sobre referências públicas do mercado voluntário brasileiro. Servem para "
        "priorizar terra e dimensionar a tese. Antes de contrato, captação ou emissão, "
        "substituir por inventário florestal de campo, análise dominial completa e cotação real "
        "de mercado.",
        "",
    ]


def gerar_relatorio_land_bank(resultado: ResultadoLandBank) -> str:
    """Monta o relatório completo do Land Bank em Markdown."""
    linhas: List[str] = [
        f"# Land Bank — {resultado.nome}",
        "",
        f"**Análise gerada em:** {resultado.data_analise}  ",
        f"**Horizonte de creditação:** {resultado.horizonte_anos} anos  ",
        "**Metodologia:** agregação territorial em projetos agrupados (grouped projects)",
        "",
        "---",
        "",
    ]

    linhas += _sumario(resultado)
    linhas += _painel_glebas(resultado)

    linhas += ["## 3. Clusters de Carbono", ""]
    linhas += [
        "Cada cluster é um projeto agrupado candidato: um único PDD, uma única validação, "
        "uma única linha de verificação, várias glebas dentro. É assim que o custo fixo "
        "deixa de ser proibitivo.",
        "",
        "| Cluster | Bioma | Glebas | Elegível (ha) | tCO2e líq. | VPL | Escala |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for c in sorted(resultado.clusters, key=lambda x: x.vcus_liquidos, reverse=True):
        linhas.append(
            f"| {c.id} | {c.bioma.value.replace('_', ' ')} | {len(c.glebas_ids)} | "
            f"{_num(c.area_elegivel_ha)} | {_num(c.vcus_liquidos)} | {_brl(c.vpl_brl)} | {c.escala} |"
        )
    linhas.append("")

    for c in sorted(resultado.clusters, key=lambda x: x.vcus_liquidos, reverse=True):
        linhas += _detalhe_cluster(c, resultado)

    if resultado.clusters:
        ancora = max(resultado.clusters, key=lambda x: x.vcus_liquidos)
        linhas += _fluxo_caixa(ancora)

    linhas += _cenarios(resultado)
    linhas += _alavancas(resultado)
    linhas += _prioridades(resultado)
    linhas += _alertas(resultado)
    linhas += _premissas(resultado)

    return "\n".join(linhas)
