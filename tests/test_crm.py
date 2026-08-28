"""
Testes do Zion CRM & Lead Intelligence™.
"""

import json
from datetime import date, timedelta
from pathlib import Path

import pytest

from src.crm import analisar_base, auditar_base, analisar_funil, listar_reativacao, qualificar
from src.crm.engine import PESOS, calcular_score, rotear
from src.crm.models import (
    Ativos, BaseComercial, DadosFinanceiros, DadosProjeto, DadosTerreno,
    Estagio, Interacao, Lead, MotivoPerda, Objetivo, Perfil, Porta,
    ProximaAcao, Temperatura, Tri,
)
from src.crm.relatorio import briefing_lead, gerar_relatorio_comercial

EXEMPLO = Path(__file__).resolve().parent.parent / "data" / "exemplo_base_comercial.json"
HOJE = date(2026, 8, 28)


def lead_base(**kwargs) -> Lead:
    dados = dict(
        id="LD-T", nome="Lead de Teste", email="teste@exemplo.com", telefone="48999990000",
        perfil=Perfil.PROPRIETARIO_TERRENO, objetivo=Objetivo.DESENVOLVER,
        estagio=Estagio.QUALIFICACAO, e_decisor=Tri.SIM, responsavel="Bruno",
        data_ultima_atividade=HOJE - timedelta(days=3),
        proxima_acao=ProximaAcao(acao="Ligar", data_prevista=HOJE + timedelta(days=2), responsavel="Bruno"),
    )
    dados.update(kwargs)
    return Lead(**dados)


# ---------------------------------------------------------------------------
# Score
# ---------------------------------------------------------------------------

def test_pesos_somam_um():
    assert sum(PESOS.values()) == pytest.approx(1.0)


def test_engajamento_tem_o_menor_peso():
    """Regra metodológica: engajamento vale menos que fit, ativo e capacidade."""
    assert PESOS["ENGAGEMENT"] == min(PESOS.values())
    assert PESOS["ENGAGEMENT"] < PESOS["FIT"]
    assert PESOS["ENGAGEMENT"] < PESOS["ATIVO"]


def test_score_fica_na_escala():
    score = calcular_score(lead_base(), HOJE)
    assert 0 <= score.score <= 10
    assert 0 <= score.confianca <= 1
    assert len(score.dimensoes) == 8


def test_lead_sem_informacao_tem_confianca_baixa_nao_score_zero():
    """Ausência de dado é falta de qualificação, não demérito do lead."""
    vazio = Lead(id="LD-V", nome="Sem dados")
    score = calcular_score(vazio, HOJE)
    assert score.confianca < 0.4
    assert any("Confiança baixa" in a for a in score.alertas)


def test_lead_com_ativo_forte_e_sem_engajamento_supera_lead_engajado():
    """
    O caso central da regra de score: terreno grande e capital vencem curtidas.
    """
    ativo_forte = lead_base(
        id="LD-A",
        ativos=Ativos(terreno=Tri.SIM, capital=Tri.SIM, projeto=Tri.NAO),
        terreno=DadosTerreno(area_ha=150.0),
        financeiro=DadosFinanceiros(capital_disponivel_brl=5_000_000),
        projeto=DadosProjeto(prazo_meses=9),
        interacoes=[],
    )
    engajado = lead_base(
        id="LD-B", perfil=Perfil.ALUNO, objetivo=Objetivo.APRENDER,
        ativos=Ativos(terreno=Tri.NAO, capital=Tri.NAO, projeto=Tri.NAO),
        financeiro=DadosFinanceiros(capital_disponivel_brl=20_000),
        interacoes=[
            Interacao(data=HOJE, canal="instagram", o_que_foi_enviado=f"interação {i}")
            for i in range(8)
        ],
    )
    assert calcular_score(ativo_forte, HOJE).score > calcular_score(engajado, HOJE).score


def test_dimensao_desconhecida_nao_entra_no_calculo():
    conhecido = calcular_score(
        lead_base(e_decisor=Tri.SIM, ativos=Ativos(terreno=Tri.SIM)), HOJE
    )
    desconhecido = calcular_score(
        lead_base(e_decisor=Tri.DESCONHECIDO, ativos=Ativos(terreno=Tri.SIM)), HOJE
    )
    assert desconhecido.confianca < conhecido.confianca


def test_capital_informado_marca_base_informada():
    score = calcular_score(
        lead_base(financeiro=DadosFinanceiros(capital_disponivel_brl=3_000_000)), HOJE
    )
    capital = next(d for d in score.dimensoes if d.nome == "CAPITAL")
    assert capital.base == "informada"
    assert capital.valor >= 9


# ---------------------------------------------------------------------------
# Temperatura
# ---------------------------------------------------------------------------

def test_oportunidade_exige_projeto_e_estagio_avancado():
    lead = lead_base(
        ativos=Ativos(terreno=Tri.SIM, capital=Tri.SIM, projeto=Tri.SIM),
        projeto=DadosProjeto(estagio="projeto", prazo_meses=6),
        estagio=Estagio.OFERTA,
    )
    assert calcular_score(lead, HOJE).temperatura == Temperatura.OPORTUNIDADE


def test_projeto_sem_estagio_avancado_nao_e_oportunidade():
    lead = lead_base(
        ativos=Ativos(projeto=Tri.SIM), projeto=DadosProjeto(estagio="projeto"),
        estagio=Estagio.QUALIFICACAO,
    )
    assert calcular_score(lead, HOJE).temperatura != Temperatura.OPORTUNIDADE


def test_quente_exige_autoridade_capital_e_urgencia():
    """Sem decisor, não é quente por mais alto que seja o score."""
    sem_autoridade = lead_base(
        e_decisor=Tri.NAO,
        ativos=Ativos(terreno=Tri.SIM, capital=Tri.SIM),
        terreno=DadosTerreno(area_ha=200.0),
        financeiro=DadosFinanceiros(capital_disponivel_brl=8_000_000),
        projeto=DadosProjeto(prazo_meses=6),
    )
    assert calcular_score(sem_autoridade, HOJE).temperatura != Temperatura.QUENTE


def test_lead_sem_objetivo_e_frio():
    lead = Lead(id="LD-F", nome="Frio", perfil=Perfil.PROFISSIONAL)
    assert calcular_score(lead, HOJE).temperatura == Temperatura.FRIO


# ---------------------------------------------------------------------------
# Roteamento — a regra de não empurrar venda
# ---------------------------------------------------------------------------

def test_quer_comprar_sem_projeto_vai_para_diagnostico():
    """Se não sabe o que construir, não se vende bubble."""
    lead = lead_base(
        perfil=Perfil.EMPREENDEDOR, objetivo=Objetivo.COMPRAR,
        ativos=Ativos(terreno=Tri.NAO, capital=Tri.SIM, projeto=Tri.NAO),
    )
    score, rot = qualificar(lead, HOJE)
    assert rot.porta == Porta.DIAGNOSTICO
    assert any("bubble" in n.lower() or "Produto" in n for n in rot.nao_ofertar)


def test_quer_comprar_com_projeto_vai_para_produto():
    lead = lead_base(
        perfil=Perfil.EMPREENDEDOR, objetivo=Objetivo.COMPRAR,
        ativos=Ativos(projeto=Tri.SIM, capital=Tri.SIM),
        projeto=DadosProjeto(estagio="projeto"),
    )
    assert qualificar(lead, HOJE)[1].porta == Porta.PRODUTO


def test_sem_projeto_nunca_oferta_capital():
    """Não se vende captação para quem não tem projeto."""
    lead = lead_base(ativos=Ativos(terreno=Tri.SIM, projeto=Tri.NAO))
    rot = qualificar(lead, HOJE)[1]
    assert any("Capital" in n for n in rot.nao_ofertar)


def test_nao_sabe_o_que_fazer_vai_para_diagnostico():
    lead = lead_base(objetivo=Objetivo.NAO_SABE, ativos=Ativos(terreno=Tri.SIM))
    assert qualificar(lead, HOJE)[1].porta == Porta.DIAGNOSTICO


def test_terreno_mais_aprender_vai_para_mentoria():
    lead = lead_base(objetivo=Objetivo.APRENDER, ativos=Ativos(terreno=Tri.SIM))
    assert qualificar(lead, HOJE)[1].porta == Porta.MENTORIA


def test_terreno_mais_delegar_vai_para_desenvolvimento():
    lead = lead_base(objetivo=Objetivo.DESENVOLVER, ativos=Ativos(terreno=Tri.SIM))
    assert qualificar(lead, HOJE)[1].porta == Porta.DESENVOLVIMENTO


def test_projeto_mais_necessidade_de_capital_vai_para_capital():
    lead = lead_base(
        perfil=Perfil.DESENVOLVEDOR, objetivo=Objetivo.CAPITAL,
        ativos=Ativos(terreno=Tri.SIM, projeto=Tri.SIM),
    )
    assert qualificar(lead, HOJE)[1].porta == Porta.CAPITAL


def test_parceria_sem_ativo_complementar_vira_diagnostico():
    """Parceria só com fit estratégico real."""
    lead = lead_base(
        perfil=Perfil.PROFISSIONAL, objetivo=Objetivo.PARCERIA,
        ativos=Ativos(terreno=Tri.NAO, capital=Tri.NAO, operacao=Tri.NAO),
    )
    assert qualificar(lead, HOJE)[1].porta == Porta.DIAGNOSTICO


def test_lead_novo_nao_recebe_proposta_fechada():
    lead = lead_base(estagio=Estagio.NOVO_LEAD)
    rot = qualificar(lead, HOJE)[1]
    assert any("qualificação" in n for n in rot.nao_ofertar)


def test_perguntas_de_qualificacao_por_perfil():
    proprietario = qualificar(lead_base(), HOJE)[1]
    assert len(proprietario.perguntas_de_qualificacao) == 12
    investidor = qualificar(lead_base(perfil=Perfil.INVESTIDOR, objetivo=Objetivo.INVESTIR), HOJE)[1]
    assert len(investidor.perguntas_de_qualificacao) == 10


# ---------------------------------------------------------------------------
# Base de exemplo e operações
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def relatorio():
    with open(EXEMPLO, "r", encoding="utf-8") as f:
        return analisar_base(BaseComercial(**json.load(f)), HOJE)


def test_exemplo_analisa(relatorio):
    assert relatorio.total_leads == 15
    assert relatorio.qualificados
    assert relatorio.funil


def test_prioridades_sao_sequenciais(relatorio):
    assert [q.prioridade for q in relatorio.qualificados] == list(
        range(1, len(relatorio.qualificados) + 1)
    )


def test_leads_fechados_ficam_no_fim_da_fila(relatorio):
    """Lead perdido não disputa atenção com lead aberto."""
    fechados = [
        q.prioridade for q in relatorio.qualificados
        if q.lead.estagio in (Estagio.GANHO, Estagio.PERDIDO)
    ]
    abertos = [
        q.prioridade for q in relatorio.qualificados
        if q.lead.estagio not in (Estagio.GANHO, Estagio.PERDIDO)
    ]
    assert min(fechados) > max(abertos)


def test_higiene_detecta_duplicidade(relatorio):
    codigos = {a.codigo for a in relatorio.higiene}
    assert "CRM_DUPLICADO" in codigos


def test_higiene_detecta_perda_sem_motivo(relatorio):
    achado = next(a for a in relatorio.higiene if a.codigo == "CRM_PERDA_SEM_MOTIVO")
    assert achado.gravidade == "bloqueante"
    assert "LD-011" in achado.leads


def test_higiene_detecta_lead_sem_proxima_acao(relatorio):
    achado = next(a for a in relatorio.higiene if a.codigo == "CRM_SEM_PROXIMA_ACAO")
    assert achado.gravidade == "bloqueante"


def test_higiene_detecta_followup_vencido(relatorio):
    achado = next(a for a in relatorio.higiene if a.codigo == "CRM_FOLLOWUP_ATRASADO")
    assert "LD-004" in achado.leads


def test_higiene_detecta_lead_sem_canal(relatorio):
    achado = next(a for a in relatorio.higiene if a.codigo == "CRM_SEM_CONTATO")
    assert "LD-013" in achado.leads


def test_funil_identifica_gargalo(relatorio):
    assert relatorio.funil.gargalo
    assert relatorio.funil.diagnostico


def test_funil_e_monotonicamente_decrescente(relatorio):
    """Volume acumulado nunca cresce ao avançar no funil."""
    volumes = [e.quantidade for e in relatorio.funil.etapas]
    assert volumes == sorted(volumes, reverse=True)


def test_reativacao_inclui_perdido_sem_motivo():
    """Quem saiu sem motivo registrado é o primeiro a requalificar."""
    with open(EXEMPLO, "r", encoding="utf-8") as f:
        base = BaseComercial(**json.load(f))
    itens = listar_reativacao(base, HOJE, score_minimo=0.0)
    ids = {i.lead_id for i in itens}
    assert "LD-011" in ids
    sem_motivo = next(i for i in itens if i.lead_id == "LD-011")
    assert "sem motivo registrado" in sem_motivo.provavel_problema


def test_reativacao_ignora_ganhos():
    with open(EXEMPLO, "r", encoding="utf-8") as f:
        base = BaseComercial(**json.load(f))
    base.leads[0].estagio = Estagio.GANHO
    base.leads[0].data_ultima_atividade = date(2025, 1, 1)
    ids = {i.lead_id for i in listar_reativacao(base, HOJE, score_minimo=0.0)}
    assert base.leads[0].id not in ids


def test_acoes_recomendadas_sao_no_maximo_cinco(relatorio):
    assert 0 < len(relatorio.acoes_recomendadas) <= 5


def test_relatorio_markdown_completo(relatorio):
    md = gerar_relatorio_comercial(relatorio)
    for secao in ("Painel", "Prioridade Comercial", "Funil", "Higiene da Base",
                  "Reativação", "Ações Recomendadas"):
        assert secao in md


def test_briefing_traz_composicao_do_score(relatorio):
    briefing = briefing_lead(relatorio.qualificados[0])
    assert "Composição do score" in briefing
    assert "Roteamento" in briefing
    for dimensao in PESOS:
        assert dimensao in briefing


def test_base_vazia_nao_quebra():
    r = analisar_base(BaseComercial(nome="vazia", leads=[]), HOJE)
    assert r.total_leads == 0
    assert r.qualificados == []


def test_agente_roda_sem_chave_de_api():
    from src.agents.crm_agent import CRMAgent

    with open(EXEMPLO, "r", encoding="utf-8") as f:
        dados = json.load(f)
    relatorio, markdown = CRMAgent().analisar(dados, HOJE)
    assert relatorio.total_leads == 15
    assert "Relatório Comercial Zion" in markdown


def test_agente_rejeita_dados_invalidos():
    from src.agents.crm_agent import CRMAgent

    with pytest.raises(ValueError, match="leads"):
        CRMAgent().carregar({"nome": "sem leads"})
