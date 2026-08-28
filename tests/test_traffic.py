"""
Testes do Zion Traffic & Acquisition Architect™.
"""

import json
from datetime import date
from pathlib import Path

import pytest

from src.crm.models import BaseComercial
from src.traffic import (
    analisar_conta, atribuir, avaliar_gate, calcular_metricas, comparar_proporcoes,
    decidir, diagnosticar, gerar_relatorio_trafego, leitura_da_atribuicao,
    prob_zero_conversoes, volume_suficiente,
)
from src.traffic.metricas import PERGUNTAS_OBRIGATORIAS, agregar
from src.traffic.models import (
    BriefingCampanha, Campanha, Canal, ContaTrafego, EstagioPublico, EtapaCadeia,
    Intencao, MetasCampanha, MetricasCampanha, ProdutoZion,
)

CONTA = Path(__file__).resolve().parent.parent / "data" / "exemplo_conta_trafego.json"
CRM = Path(__file__).resolve().parent.parent / "data" / "exemplo_base_comercial.json"


def briefing_completo() -> BriefingCampanha:
    return BriefingCampanha(
        o_que_vendemos="Mentoria", para_quem="Terrenistas", qual_problema="Não sabe desenvolver",
        qual_desejo="Clareza", qual_transformacao="Projeto estruturado", qual_oferta="Mentoria 7 semanas",
        qual_preco_brl=4900.0, qual_funil="Anúncio → página → aplicação",
        qual_evento_conversao="Aplicação", meta_receita_brl=98000.0,
    )


def campanha_base(**kwargs) -> Campanha:
    dados = dict(
        id="C-T", nome="Teste", canal=Canal.META, produto=ProdutoZion.MENTORIA,
        intencao=Intencao.DECISAO, estagio_publico=EstagioPublico.MORNO,
        objetivo="Converter", briefing=briefing_completo(),
        evento_conversao="Lead", utm_campaign="teste-utm",
        landing_page="https://zion.com/x",
        metas=MetasCampanha(cac_alvo_brl=1500.0, cpqo_alvo_brl=800.0),
        criativos=[],
    )
    dados.update(kwargs)
    return Campanha(**dados)


# ---------------------------------------------------------------------------
# Métricas
# ---------------------------------------------------------------------------

def test_metricas_derivadas():
    m = MetricasCampanha(
        investimento_brl=1000.0, impressoes=100_000, cliques=2000, visitas_pagina=1900,
        leads=190, leads_qualificados=50, oportunidades=10, vendas=2, receita_brl=9800.0,
    )
    r = calcular_metricas(m)
    assert r.cpm_brl == pytest.approx(10.0)
    assert r.ctr == pytest.approx(0.02)
    assert r.cpc_brl == pytest.approx(0.5)
    assert r.cpl_brl == pytest.approx(1000 / 190)
    assert r.cpqo_brl == pytest.approx(100.0)
    assert r.cac_brl == pytest.approx(500.0)
    assert r.roas == pytest.approx(9.8)


def test_metrica_sem_denominador_e_none_nao_zero():
    """'Nenhuma venda' e 'nenhum dado' não podem virar o mesmo número."""
    r = calcular_metricas(MetricasCampanha(investimento_brl=500.0))
    assert r.cac_brl is None, "sem vendas não há CAC — não é CAC zero"
    assert r.cpl_brl is None
    assert r.ctr is None
    # ROAS é 0.0, não None: o denominador existe. Gastou e não retornou é um
    # fato mensurável, diferente de não haver dado.
    assert r.roas == 0.0


def test_lucro_considera_margem():
    m = MetricasCampanha(investimento_brl=1000.0, receita_brl=10_000.0)
    assert calcular_metricas(m, margem=0.5).lucro_bruto_brl == pytest.approx(4000.0)


def test_agregar_soma_campanhas():
    c1 = campanha_base(id="A", metricas=MetricasCampanha(investimento_brl=100.0, leads=10))
    c2 = campanha_base(id="B", metricas=MetricasCampanha(investimento_brl=200.0, leads=5))
    total = agregar([c1, c2])
    assert total.investimento_brl == 300.0
    assert total.leads == 15


# ---------------------------------------------------------------------------
# Gate
# ---------------------------------------------------------------------------

def test_gate_libera_campanha_completa():
    from src.traffic.models import Criativo, FuncaoCriativo, Angulo

    campanha = campanha_base(criativos=[
        Criativo(id="CR", nome="A", funcao=FuncaoCriativo.VENDER,
                 angulo=Angulo.TRANSFORMACAO, hook="Hook real")
    ])
    resultado = avaliar_gate(campanha)
    assert resultado.liberada
    assert not resultado.perguntas_sem_resposta


def test_gate_bloqueia_briefing_incompleto():
    campanha = campanha_base(briefing=BriefingCampanha(o_que_vendemos="Algo"))
    resultado = avaliar_gate(campanha)
    assert not resultado.liberada
    assert len(resultado.perguntas_sem_resposta) == len(PERGUNTAS_OBRIGATORIAS) - 1
    assert "NÃO CRIAR CAMPANHA AINDA" in resultado.veredito


def test_gate_exige_utm_para_atribuicao():
    resultado = avaliar_gate(campanha_base(utm_campaign=None))
    assert not resultado.liberada
    assert any("UTM" in p for p in resultado.pendencias_estruturais)


def test_gate_exige_meta_de_cac_ou_cpqo():
    resultado = avaliar_gate(campanha_base(metas=MetasCampanha()))
    assert any("meta de CAC" in p for p in resultado.pendencias_estruturais)


# ---------------------------------------------------------------------------
# Estatística
# ---------------------------------------------------------------------------

def test_zero_conversoes_com_pouco_volume_e_ruido():
    """20 cliques sem lead não provam nada."""
    assert prob_zero_conversoes(20, 0.10) > 0.05


def test_zero_conversoes_com_muito_volume_e_evidencia():
    """500 cliques sem lead, com conversão esperada de 10%, não é acaso."""
    assert prob_zero_conversoes(500, 0.10) < 0.001


def test_comparar_proporcoes_detecta_diferenca_real():
    p_valor, leitura = comparar_proporcoes(200, 1000, 100, 1000)
    assert p_valor < 0.05
    assert "significativa" in leitura


def test_comparar_proporcoes_nao_declara_vencedor_sem_evidencia():
    """Dois criativos parecidos com pouco volume não têm vencedor."""
    p_valor, leitura = comparar_proporcoes(11, 100, 9, 100)
    assert p_valor > 0.05
    assert "não declarar vencedor" in leitura.lower()


def test_comparar_proporcoes_sem_volume():
    p_valor, leitura = comparar_proporcoes(0, 0, 5, 100)
    assert p_valor is None


def test_volume_insuficiente_e_reportado():
    ok, leitura = volume_suficiente(MetricasCampanha(impressoes=100, cliques=5))
    assert not ok
    assert "insuficiente" in leitura.lower()


def test_volume_suficiente_exige_leads_para_qualidade():
    ok, leitura = volume_suficiente(
        MetricasCampanha(impressoes=50_000, cliques=800, leads=3)
    )
    assert not ok
    assert "leads" in leitura


# ---------------------------------------------------------------------------
# Diagnóstico
# ---------------------------------------------------------------------------

def test_ctr_baixo_aponta_criativo():
    campanha = campanha_base(metricas=MetricasCampanha(
        investimento_brl=2000.0, impressoes=300_000, cliques=900,
        visitas_pagina=880, leads=120, leads_qualificados=60,
        oportunidades=20, vendas=5, receita_brl=24_500.0,
    ))
    d = diagnosticar(campanha)
    assert any(a.etapa == EtapaCadeia.CRIATIVO for a in d.achados)


def test_muitos_cliques_poucas_conversoes_aponta_pagina():
    campanha = campanha_base(metricas=MetricasCampanha(
        investimento_brl=3000.0, impressoes=200_000, cliques=4000,
        visitas_pagina=3800, leads=95, leads_qualificados=60,
        oportunidades=25, vendas=6, receita_brl=29_400.0,
    ))
    d = diagnosticar(campanha)
    assert any(a.etapa == EtapaCadeia.PAGINA for a in d.achados)


def test_muitos_leads_poucas_oportunidades_aponta_qualificacao():
    campanha = campanha_base(metricas=MetricasCampanha(
        investimento_brl=5000.0, impressoes=400_000, cliques=8000,
        visitas_pagina=7800, leads=1200, leads_qualificados=60,
        oportunidades=15, vendas=4, receita_brl=19_600.0,
    ))
    d = diagnosticar(campanha)
    assert any(a.etapa == EtapaCadeia.QUALIFICACAO for a in d.achados)


def test_gargalo_e_o_primeiro_ponto_da_cadeia():
    """Nunca otimizar a última etapa sem verificar as anteriores."""
    campanha = campanha_base(metricas=MetricasCampanha(
        investimento_brl=5000.0, impressoes=900_000, cliques=2000,
        visitas_pagina=1900, leads=90, leads_qualificados=10,
        oportunidades=12, vendas=1, receita_brl=4900.0,
    ))
    d = diagnosticar(campanha)
    etapas = [a.etapa for a in d.achados]
    assert len(etapas) > 1
    assert d.gargalo == etapas[0]
    ordem = list(EtapaCadeia)
    assert all(ordem.index(d.gargalo) <= ordem.index(e) for e in etapas)


def test_zero_leads_com_pouco_volume_nao_manda_pausar():
    campanha = campanha_base(metricas=MetricasCampanha(
        investimento_brl=90.0, impressoes=9_000, cliques=15, visitas_pagina=14,
    ))
    d = diagnosticar(campanha)
    achado = next(a for a in d.achados if a.etapa == EtapaCadeia.LEAD)
    assert achado.gravidade == "media"
    assert "impaciência" in achado.acao


def test_zero_leads_com_muito_volume_e_bloqueante():
    campanha = campanha_base(metricas=MetricasCampanha(
        investimento_brl=4000.0, impressoes=300_000, cliques=900, visitas_pagina=880,
    ))
    d = diagnosticar(campanha)
    achado = next(a for a in d.achados if a.etapa == EtapaCadeia.LEAD)
    assert achado.gravidade == "bloqueante"


# ---------------------------------------------------------------------------
# Decisão
# ---------------------------------------------------------------------------

def test_sem_volume_aguarda_em_vez_de_decidir():
    campanha = campanha_base(metricas=MetricasCampanha(
        investimento_brl=150.0, impressoes=500, cliques=12,
    ))
    d = diagnosticar(campanha)
    assert decidir(campanha, d).acao == "aguardar_volume"


def test_escala_exige_cac_na_meta_e_volume_de_vendas():
    campanha = campanha_base(metricas=MetricasCampanha(
        investimento_brl=12_000.0, impressoes=400_000, cliques=8000,
        visitas_pagina=7600, leads=1600, leads_qualificados=700,
        oportunidades=260, vendas=60, receita_brl=294_000.0,
    ))
    d = diagnosticar(campanha)
    decisao = decidir(campanha, d)
    assert decisao.acao == "escalar"
    assert any("capacidade" in b for b in decisao.bloqueios_de_escala)


def test_poucas_vendas_bloqueia_escala_mesmo_com_cac_bom():
    """CAC calculado sobre 2 vendas não é CAC, é sorte."""
    campanha = campanha_base(metricas=MetricasCampanha(
        investimento_brl=2000.0, impressoes=200_000, cliques=4000,
        visitas_pagina=3800, leads=600, leads_qualificados=300,
        oportunidades=100, vendas=2, receita_brl=9800.0,
    ))
    d = diagnosticar(campanha)
    decisao = decidir(campanha, d)
    assert decisao.acao != "escalar"
    assert any("ainda não é estável" in b for b in decisao.bloqueios_de_escala)


def test_cpl_bom_e_cpqo_ruim_bloqueia_escala():
    """A armadilha: lead barato que não vira negócio."""
    campanha = campanha_base(
        metas=MetasCampanha(cac_alvo_brl=1500.0, cpqo_alvo_brl=800.0),
        metricas=MetricasCampanha(
            investimento_brl=9000.0, impressoes=500_000, cliques=9000,
            visitas_pagina=8600, leads=1800, leads_qualificados=900,
            oportunidades=5, vendas=1, receita_brl=4900.0,
        ),
    )
    d = diagnosticar(campanha)
    decisao = decidir(campanha, d)
    assert decisao.acao != "escalar"
    assert any("lead barato" in b for b in decisao.bloqueios_de_escala)


# ---------------------------------------------------------------------------
# Atribuição
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def relatorio():
    with open(CONTA, encoding="utf-8") as f:
        conta = ContaTrafego(**json.load(f))
    with open(CRM, encoding="utf-8") as f:
        base = BaseComercial(**json.load(f))
    return analisar_conta(conta, base), conta


def test_atribuicao_liga_campanha_a_receita(relatorio):
    r, _ = relatorio
    dev = next(a for a in r.atribuicao if a.campanha_id == "CAMP-DEV")
    assert dev.clientes >= 1
    assert dev.receita_brl > 0
    assert dev.ranking_por_receita == 1


def test_campanha_de_mais_leads_nao_e_a_de_mais_receita(relatorio):
    """O achado central do loop de atribuição."""
    r, conta = relatorio
    campeao_leads = min(r.atribuicao, key=lambda a: a.ranking_por_leads)
    campeao_receita = min(r.atribuicao, key=lambda a: a.ranking_por_receita)
    assert campeao_leads.campanha_id != campeao_receita.campanha_id
    leitura = leitura_da_atribuicao(r.atribuicao, conta)
    assert any("teria escalado a campanha errada" in o for o in leitura)


def test_atribuicao_alerta_perda_de_rastreamento(relatorio):
    """Plataforma reportando muito mais lead que o CRM é rastreamento, não qualidade."""
    r, conta = relatorio
    leitura = leitura_da_atribuicao(r.atribuicao, conta)
    assert any("não está sendo medida" in o for o in leitura)


def test_campanha_sem_utm_nao_recebe_atribuicao(relatorio):
    r, _ = relatorio
    pmax = next(a for a in r.atribuicao if a.campanha_id == "CAMP-PMAX")
    assert pmax.leads == 0
    assert pmax.cac_brl is None


# ---------------------------------------------------------------------------
# Conta completa
# ---------------------------------------------------------------------------

def test_conta_analisa(relatorio):
    r, _ = relatorio
    assert r.investimento_total_brl > 0
    assert len(r.diagnosticos) == 5
    assert len(r.decisoes) == 5


def test_gate_bloqueia_campanha_de_teste(relatorio):
    r, _ = relatorio
    pmax = next(g for g in r.gates if g.campanha_id == "CAMP-PMAX")
    assert not pmax.liberada
    assert len(pmax.perguntas_sem_resposta) == 8


def test_gargalo_geral_identificado(relatorio):
    r, _ = relatorio
    assert r.gargalo_geral is not None


def test_cpqo_e_calculado(relatorio):
    r, _ = relatorio
    assert r.cpqo_geral_brl is not None
    assert r.cpqo_geral_brl > 0


def test_relatorio_markdown_completo(relatorio):
    r, conta = relatorio
    md = gerar_relatorio_trafego(r, conta)
    for secao in ("Painel", "Gate de Campanha", "Diagnóstico por Campanha",
                  "Atribuição Real", "Ações Recomendadas"):
        assert secao in md
    assert "custo por oportunidade qualificada" in md.lower()


def test_conta_sem_crm_nao_quebra():
    with open(CONTA, encoding="utf-8") as f:
        conta = ContaTrafego(**json.load(f))
    r = analisar_conta(conta, None)
    assert r.atribuicao == []
    assert r.diagnosticos


def test_conta_vazia_nao_quebra():
    r = analisar_conta(ContaTrafego(nome="vazia", campanhas=[]), None)
    assert r.investimento_total_brl == 0
    assert r.diagnosticos == []


def test_agente_roda_sem_chave_de_api():
    from src.agents.traffic_agent import TrafficAgent

    with open(CONTA, encoding="utf-8") as f:
        dados = json.load(f)
    with open(CRM, encoding="utf-8") as f:
        crm = json.load(f)
    relatorio, markdown = TrafficAgent().analisar(dados, crm)
    assert relatorio.investimento_total_brl > 0
    assert "Relatório de Aquisição Zion" in markdown


def test_agente_rejeita_dados_invalidos():
    from src.agents.traffic_agent import TrafficAgent

    with pytest.raises(ValueError, match="campanhas"):
        TrafficAgent().carregar({"nome": "sem campanhas"})
