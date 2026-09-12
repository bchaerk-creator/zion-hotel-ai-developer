"""
Testes da ponte Land Bank × CRM.

O que precisa estar certo aqui não é o número em si: é a regra de contagem.
Hectare vinculado não conta duas vezes, ausência de informação não vira zero,
e cada total carrega a definição que o gerou.
"""

import json
from datetime import date, timedelta
from pathlib import Path

import pytest

from src.crm.models import (
    Ativos, BaseComercial, DadosFinanceiros, DadosTerreno, Estagio, Lead,
    Perfil, ProximaAcao, Tri,
)
from src.crm.relatorio import gerar_painel_territorial
from src.crm.territorio import (
    TOLERANCIA_AREA,
    area_declarada,
    consolidar_territorio,
    contar_oportunidades,
    investimento_declarado,
    listar_originacao,
    somar_areas,
    somar_investimentos,
    sugerir_vinculos,
)
from src.models.land_bank import (
    Bioma, Gleba, LandBank, StatusDominial, Talhao, UsoSolo,
)

BASE_EXEMPLO = Path(__file__).resolve().parent.parent / "data" / "exemplo_base_comercial.json"
LB_EXEMPLO = Path(__file__).resolve().parent.parent / "data" / "exemplo_land_bank.json"
HOJE = date(2026, 8, 28)


def lead(**kwargs) -> Lead:
    dados = dict(
        id="LD-T", nome="Lead de Teste", email="teste@exemplo.com",
        cidade="Urubici", estado="SC",
        perfil=Perfil.PROPRIETARIO_TERRENO, estagio=Estagio.QUALIFICACAO,
        responsavel="Bruno", data_ultima_atividade=HOJE - timedelta(days=3),
        proxima_acao=ProximaAcao(acao="Ligar", data_prevista=HOJE + timedelta(days=2), responsavel="Bruno"),
    )
    dados.update(kwargs)
    return Lead(**dados)


def gleba(**kwargs) -> Gleba:
    dados = dict(
        id="GL-T", nome="Gleba de Teste", municipio="Urubici", uf="SC",
        bioma=Bioma.MATA_ATLANTICA, area_total_ha=300.0,
        status_dominial=StatusDominial.EM_NEGOCIACAO,
        talhoes=[Talhao(id="T1", area_ha=300.0, uso_solo=UsoSolo.PASTAGEM_DEGRADADA)],
    )
    dados.update(kwargs)
    return Gleba(**dados)


@pytest.fixture
def base_exemplo() -> BaseComercial:
    with open(BASE_EXEMPLO, encoding="utf-8") as f:
        return BaseComercial(**json.load(f))


@pytest.fixture
def land_bank_exemplo() -> LandBank:
    with open(LB_EXEMPLO, encoding="utf-8") as f:
        return LandBank(**json.load(f))


# ---------------------------------------------------------------------------
# Leitura de declaração
# ---------------------------------------------------------------------------

def test_investimento_ausente_nao_vira_zero():
    assert investimento_declarado(lead()) is None


def test_faixa_de_investimento_tem_precedencia_sobre_capital():
    l = lead(financeiro=DadosFinanceiros(capital_disponivel_brl=1_000_000, faixa_investimento_brl=4_000_000))
    assert investimento_declarado(l) == 4_000_000


def test_capital_serve_quando_nao_ha_faixa():
    l = lead(financeiro=DadosFinanceiros(capital_disponivel_brl=1_000_000))
    assert investimento_declarado(l) == 1_000_000


def test_area_zero_nao_conta_como_area_declarada():
    assert area_declarada(lead(terreno=DadosTerreno(area_ha=0))) is None


# ---------------------------------------------------------------------------
# Oportunidades
# ---------------------------------------------------------------------------

def test_oportunidades_separam_aberto_de_fechado():
    base = BaseComercial(leads=[
        lead(id="A", estagio=Estagio.NEGOCIACAO),
        lead(id="B", estagio=Estagio.GANHO),
        lead(id="C", estagio=Estagio.PERDIDO),
    ])
    o = contar_oportunidades(base, HOJE)
    assert (o.abertas, o.ganhas, o.perdidas, o.total_base) == (1, 1, 1, 3)
    assert o.com_oferta_na_mesa == 1


def test_oportunidade_territorial_conta_terreno_sem_area():
    """Quem diz ter terra é oportunidade territorial mesmo sem informar hectare."""
    base = BaseComercial(leads=[lead(ativos=Ativos(terreno=Tri.SIM))])
    assert contar_oportunidades(base, HOJE).territoriais == 1


# ---------------------------------------------------------------------------
# Investimento declarado
# ---------------------------------------------------------------------------

def test_cobertura_de_investimento_reflete_quem_declarou():
    base = BaseComercial(leads=[
        lead(id="A", financeiro=DadosFinanceiros(capital_disponivel_brl=2_000_000)),
        lead(id="B"),
    ])
    inv = somar_investimentos(base)
    assert inv.declarado_brl == 2_000_000
    assert inv.leads_declarantes == 1
    assert inv.leads_sem_declaracao == 1
    assert inv.cobertura == 0.5
    assert inv.ticket_medio_brl == 2_000_000  # média sobre quem declarou, não sobre a base


def test_investimento_de_lead_perdido_fica_separado_do_pipeline():
    base = BaseComercial(leads=[
        lead(id="A", estagio=Estagio.PERDIDO, financeiro=DadosFinanceiros(capital_disponivel_brl=5_000_000)),
    ])
    inv = somar_investimentos(base)
    assert inv.declarado_brl == 5_000_000
    assert inv.declarado_aberto_brl == 0
    assert inv.declarado_perdido_brl == 5_000_000


# ---------------------------------------------------------------------------
# Áreas — a regra que mais importa
# ---------------------------------------------------------------------------

def test_area_vinculada_nao_conta_duas_vezes():
    lb = LandBank(nome="LB", glebas=[gleba(id="GL-1", area_total_ha=300.0)])
    base = BaseComercial(leads=[
        lead(id="A", terreno=DadosTerreno(area_ha=300.0), glebas_land_bank=["GL-1"]),
    ])
    p = consolidar_territorio(base, lb, HOJE)
    assert p.areas.land_bank_ha == 300.0
    assert p.areas.originacao_aberta_ha == 0.0
    assert p.areas.sobreposicao_ha == 300.0
    assert p.areas.total_consolidado_ha == 300.0


def test_area_nao_vinculada_soma_ao_banco():
    lb = LandBank(nome="LB", glebas=[gleba(id="GL-1", area_total_ha=300.0)])
    base = BaseComercial(leads=[lead(id="A", terreno=DadosTerreno(area_ha=140.0))])
    areas = somar_areas(base, lb, [])
    assert areas.total_consolidado_ha == 440.0
    assert areas.originacao_aberta_ha == 140.0
    assert areas.sobreposicao_ha == 0.0


def test_area_de_lead_fechado_fica_fora_do_total():
    base = BaseComercial(leads=[
        lead(id="A", estagio=Estagio.PERDIDO, terreno=DadosTerreno(area_ha=45.0)),
        lead(id="B", estagio=Estagio.GANHO, terreno=DadosTerreno(area_ha=80.0)),
    ])
    areas = somar_areas(base, None, [])
    assert areas.originacao_fechada_ha == 125.0
    assert areas.total_consolidado_ha == 0.0


def test_terreno_sem_area_declarada_vira_hectare_invisivel():
    base = BaseComercial(leads=[lead(ativos=Ativos(terreno=Tri.SIM))])
    areas = somar_areas(base, None, [])
    assert areas.leads_terreno_sem_area == 1
    assert areas.total_consolidado_ha == 0.0


def test_sem_land_bank_tudo_e_originacao():
    base = BaseComercial(leads=[lead(terreno=DadosTerreno(area_ha=140.0))])
    p = consolidar_territorio(base, None, HOJE)
    assert p.areas.land_bank_ha == 0.0
    assert p.areas.total_consolidado_ha == 140.0
    assert p.land_bank_nome is None


# ---------------------------------------------------------------------------
# Vínculos
# ---------------------------------------------------------------------------

def test_gleba_inexistente_vira_alerta_e_nao_desconta_area():
    base = BaseComercial(leads=[
        lead(id="A", terreno=DadosTerreno(area_ha=140.0), glebas_land_bank=["GL-FANTASMA"]),
    ])
    p = consolidar_territorio(base, LandBank(nome="LB", glebas=[gleba(id="GL-1")]), HOJE)
    assert p.vinculos == []
    assert p.areas.originacao_aberta_ha == 140.0
    assert any("GL-FANTASMA" in a for a in p.alertas)


def test_divergencia_de_area_no_vinculo_vira_alerta():
    lb = LandBank(nome="LB", glebas=[gleba(id="GL-1", area_total_ha=300.0)])
    base = BaseComercial(leads=[
        lead(id="A", terreno=DadosTerreno(area_ha=500.0), glebas_land_bank=["GL-1"]),
    ])
    p = consolidar_territorio(base, lb, HOJE)
    assert p.vinculos[0].divergencia_area > TOLERANCIA_AREA
    assert any("diferença" in a for a in p.alertas)


def test_sugestao_exige_municipio_e_corroboracao():
    lb = LandBank(nome="LB", glebas=[
        gleba(id="GL-1", municipio="Urubici", uf="SC", area_total_ha=300.0),
        gleba(id="GL-2", municipio="Gramado", uf="RS", area_total_ha=300.0),
    ])
    # Mesmo município e área compatível → sugere.
    base = BaseComercial(leads=[lead(id="A", cidade="Urubici", estado="SC", terreno=DadosTerreno(area_ha=295.0))])
    assert [s.gleba_id for s in sugerir_vinculos(base, lb)] == ["GL-1"]

    # Mesmo município, área destoante e nome que não bate → não sugere nada.
    base = BaseComercial(leads=[lead(id="B", cidade="Urubici", estado="SC", terreno=DadosTerreno(area_ha=12.0))])
    assert sugerir_vinculos(base, lb) == []


def test_sugestao_por_nome_do_proprietario():
    lb = LandBank(nome="LB", glebas=[gleba(id="GL-1", proprietario="Espólio Antunes")])
    base = BaseComercial(leads=[lead(id="A", nome="Joaquim Antunes", cidade="Urubici", estado="SC")])
    sug = sugerir_vinculos(base, lb)
    assert len(sug) == 1 and sug[0].origem == "sugerido"


def test_lead_ja_vinculado_nao_recebe_sugestao():
    lb = LandBank(nome="LB", glebas=[gleba(id="GL-1", area_total_ha=300.0)])
    base = BaseComercial(leads=[
        lead(id="A", terreno=DadosTerreno(area_ha=300.0), glebas_land_bank=["GL-1"]),
    ])
    assert sugerir_vinculos(base, lb) == []


# ---------------------------------------------------------------------------
# Originação
# ---------------------------------------------------------------------------

def test_originacao_ordena_por_hectare_e_ignora_vinculados():
    base = BaseComercial(leads=[
        lead(id="A", terreno=DadosTerreno(area_ha=18.0)),
        lead(id="B", terreno=DadosTerreno(area_ha=140.0)),
        lead(id="C", terreno=DadosTerreno(area_ha=520.0)),
    ])
    itens = listar_originacao(base, vinculados={"C"}, hoje=HOJE)
    assert [i.lead_id for i in itens] == ["B", "A"]


def test_documentacao_desconhecida_e_registrada_como_pergunta():
    base = BaseComercial(leads=[lead(id="A", terreno=DadosTerreno(area_ha=10.0))])
    item = listar_originacao(base, vinculados=set(), hoje=HOJE)[0]
    assert item.documentacao_regular == Tri.DESCONHECIDO
    assert "desconhecida" in item.observacao


# ---------------------------------------------------------------------------
# Base real de exemplo
# ---------------------------------------------------------------------------

def test_exemplo_consolida_sem_dupla_contagem(base_exemplo, land_bank_exemplo):
    p = consolidar_territorio(base_exemplo, land_bank_exemplo, HOJE)

    soma_glebas = sum(g.area_total_ha for g in land_bank_exemplo.glebas)
    assert p.areas.land_bank_ha == soma_glebas

    # LD-008 e GL-ALM-01 são a mesma terra: 520 ha entram uma vez só.
    assert p.areas.sobreposicao_ha == 520.0
    assert p.areas.total_consolidado_ha == p.areas.land_bank_ha + p.areas.originacao_aberta_ha
    assert all(i.lead_id != "LD-008" for i in p.originacao)

    # Nenhum total pode ser maior que a soma bruta das duas bases.
    bruto = soma_glebas + sum(
        (l.terreno.area_ha or 0) for l in base_exemplo.leads
    )
    assert p.areas.total_consolidado_ha < bruto


def test_exemplo_totais_batem_com_a_base(base_exemplo, land_bank_exemplo):
    p = consolidar_territorio(base_exemplo, land_bank_exemplo, HOJE)
    o, inv = p.oportunidades, p.investimentos

    assert o.total_base == len(base_exemplo.leads)
    assert o.abertas + o.ganhas + o.perdidas == o.total_base
    assert inv.leads_declarantes + inv.leads_sem_declaracao == o.total_base
    assert inv.declarado_aberto_brl + inv.declarado_ganho_brl + inv.declarado_perdido_brl == pytest.approx(
        inv.declarado_brl
    )


def test_painel_markdown_traz_os_tres_totais(base_exemplo, land_bank_exemplo):
    md = gerar_painel_territorial(consolidar_territorio(base_exemplo, land_bank_exemplo, HOJE))
    assert "# Land Bank no CRM" in md
    assert "Oportunidades abertas" in md
    assert "Investimento declarado" in md
    assert "Áreas no banco" in md
    assert "não verificado" in md  # o número nunca sai sem a ressalva
