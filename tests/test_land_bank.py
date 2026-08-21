"""
Testes do módulo Land Bank — engine de carbono e agregação territorial.
"""

import json
from pathlib import Path

import pytest

from src.models.land_bank import (
    Bioma,
    ClasseElegibilidade,
    Gleba,
    Instrumento,
    LandBank,
    Metodologia,
    PremissasCarbono,
    StatusDominial,
    Talhao,
    UsoSolo,
)
from src.modules.carbon_engine import (
    ESTOQUE_CARBONO_HA,
    analisar_land_bank,
    avaliar_gleba,
    clusterizar,
    curva_sequestro,
    fator_remocao,
    haversine_km,
)
from src.modules.land_bank_report import gerar_relatorio_land_bank

EXEMPLO = Path(__file__).resolve().parent.parent / "data" / "exemplo_land_bank.json"


def gleba_base(**kwargs) -> Gleba:
    """Gleba de pastagem degradada, regular e sem bloqueios."""
    dados = dict(
        id="GL-TEST",
        nome="Gleba de Teste",
        municipio="Urubici",
        uf="SC",
        bioma=Bioma.MATA_ATLANTICA,
        latitude=-28.0,
        longitude=-49.6,
        area_total_ha=200.0,
        status_dominial=StatusDominial.PROPRIO,
        car_ativo=True,
        matricula_regular=True,
        uso_solo_predominante=UsoSolo.PASTAGEM_DEGRADADA,
    )
    dados.update(kwargs)
    return Gleba(**dados)


# ---------------------------------------------------------------------------
# Utilitários técnicos
# ---------------------------------------------------------------------------

def test_curva_sequestro_normalizada():
    """A soma dos fatores anuais deve igualar o horizonte, preservando a média."""
    curva = curva_sequestro(Metodologia.ARR_PLANTIO, 30)
    assert len(curva) == 30
    assert sum(curva) == pytest.approx(30.0, rel=1e-6)


def test_curva_sequestro_e_crescente_no_inicio():
    """Floresta jovem sequestra menos que floresta em pleno crescimento."""
    curva = curva_sequestro(Metodologia.ARR_PLANTIO, 30)
    assert curva[0] < curva[9]
    assert curva[9] > curva[29]


def test_curva_constante_para_emissao_evitada():
    curva = curva_sequestro(Metodologia.REDD_CONSERVACAO, 20)
    assert curva == [1.0] * 20


def test_haversine_distancia_conhecida():
    """Urubici a Rio Rufino: pouco mais de 20 km em linha reta."""
    dist = haversine_km(-28.0153, -49.5920, -27.9163, -49.7789)
    assert 15 < dist < 30


def test_fator_redd_deriva_do_estoque():
    premissas = PremissasCarbono(taxa_desmatamento_baseline=0.01)
    esperado = ESTOQUE_CARBONO_HA[Bioma.AMAZONIA] * 0.01
    assert fator_remocao(Bioma.AMAZONIA, Metodologia.REDD_CONSERVACAO, premissas) == esperado


# ---------------------------------------------------------------------------
# Elegibilidade
# ---------------------------------------------------------------------------

def test_pastagem_degradada_e_elegivel():
    avaliada = avaliar_gleba(gleba_base(), PremissasCarbono())
    assert avaliada.area_elegivel_ha == 200.0
    assert avaliada.vcus_liquidos > 0
    assert avaliada.talhoes[0].metodologia == Metodologia.ARR_PLANTIO


def test_desmatamento_recente_bloqueia_elegibilidade():
    avaliada = avaliar_gleba(gleba_base(desmatamento_recente=True), PremissasCarbono())
    assert avaliada.area_elegivel_ha == 0
    assert avaliada.vcus_liquidos == 0
    assert avaliada.bloqueios


def test_litigio_dominial_bloqueia_elegibilidade():
    avaliada = avaliar_gleba(gleba_base(litigio_dominial=True), PremissasCarbono())
    assert avaliada.area_elegivel_ha == 0
    assert any("dominial" in b.lower() for b in avaliada.bloqueios)


def test_sobreposicao_sensivel_zera_readiness_de_risco():
    avaliada = avaliar_gleba(gleba_base(sobreposicao_sensivel=True), PremissasCarbono())
    assert avaliada.area_elegivel_ha == 0
    assert avaliada.readiness_score <= 4.0


def test_passivo_legal_vira_potencial_condicionado():
    """APP e Reserva Legal não entram no núcleo bancável."""
    gleba = gleba_base(
        uso_solo_predominante=None,
        talhoes=[
            Talhao(id="T1", area_ha=120.0, uso_solo=UsoSolo.PASTAGEM_DEGRADADA),
            Talhao(id="T2", area_ha=80.0, uso_solo=UsoSolo.SOLO_EXPOSTO, obrigacao_legal=True),
        ],
    )
    avaliada = avaliar_gleba(gleba, PremissasCarbono())
    assert avaliada.area_elegivel_ha == 120.0
    assert avaliada.area_condicionada_ha == 80.0
    assert avaliada.vcus_condicionados > 0
    condicionado = next(t for t in avaliada.talhoes if t.talhao_id == "T2")
    assert condicionado.classe == ClasseElegibilidade.CONDICIONADA


def test_area_edificada_e_inelegivel():
    gleba = gleba_base(
        uso_solo_predominante=None,
        talhoes=[
            Talhao(id="T1", area_ha=150.0, uso_solo=UsoSolo.PASTAGEM_DEGRADADA),
            Talhao(id="T2", area_ha=50.0, uso_solo=UsoSolo.AREA_EDIFICADA),
        ],
    )
    avaliada = avaliar_gleba(gleba, PremissasCarbono())
    assert avaliada.area_elegivel_ha == 150.0
    assert avaliada.area_inelegivel_ha == 50.0


def test_floresta_conservada_vai_para_redd():
    gleba = gleba_base(uso_solo_predominante=UsoSolo.FLORESTA_CONSERVADA)
    avaliada = avaliar_gleba(gleba, PremissasCarbono())
    assert avaliada.talhoes[0].metodologia == Metodologia.REDD_CONSERVACAO


def test_metodologia_forcada_prevalece():
    gleba = gleba_base(
        uso_solo_predominante=None,
        talhoes=[
            Talhao(
                id="T1",
                area_ha=200.0,
                uso_solo=UsoSolo.PASTAGEM_DEGRADADA,
                metodologia_forcada=Metodologia.ARR_REGENERACAO,
            )
        ],
    )
    avaliada = avaliar_gleba(gleba, PremissasCarbono())
    assert avaliada.talhoes[0].metodologia == Metodologia.ARR_REGENERACAO


def test_buffer_e_incerteza_reduzem_o_credito():
    premissas = PremissasCarbono(buffer_remocao=0.20, incerteza_desconto=0.05)
    avaliada = avaliar_gleba(gleba_base(), premissas)
    bruto = avaliada.tco2e_bruto_horizonte
    assert avaliada.vcus_liquidos == pytest.approx(bruto * 0.80 * 0.95, rel=1e-6)


def test_readiness_maior_para_area_propria_e_regular():
    propria = avaliar_gleba(gleba_base(), PremissasCarbono())
    prospeccao = avaliar_gleba(
        gleba_base(status_dominial=StatusDominial.PROSPECCAO, car_ativo=False, matricula_regular=False),
        PremissasCarbono(),
    )
    assert propria.readiness_score > prospeccao.readiness_score
    assert 0 <= prospeccao.readiness_score <= 10


# ---------------------------------------------------------------------------
# Clusterização
# ---------------------------------------------------------------------------

def test_clusteriza_glebas_proximas_no_mesmo_projeto():
    perto = gleba_base(id="A", latitude=-28.0, longitude=-49.6)
    vizinha = gleba_base(id="B", latitude=-28.05, longitude=-49.65)
    premissas = PremissasCarbono(raio_cluster_km=50.0)
    avaliadas = {g.id: avaliar_gleba(g, premissas) for g in (perto, vizinha)}
    clusters = clusterizar([perto, vizinha], avaliadas, premissas)
    assert len(clusters) == 1
    assert set(clusters[0].glebas_ids) == {"A", "B"}


def test_separa_glebas_alem_do_raio():
    sc = gleba_base(id="A", latitude=-28.0, longitude=-49.6)
    al = gleba_base(id="B", municipio="Passo de Camaragibe", uf="AL", latitude=-9.24, longitude=-35.47)
    premissas = PremissasCarbono(raio_cluster_km=50.0)
    avaliadas = {g.id: avaliar_gleba(g, premissas) for g in (sc, al)}
    clusters = clusterizar([sc, al], avaliadas, premissas)
    assert len(clusters) == 2


def test_biomas_diferentes_nao_se_misturam():
    mata = gleba_base(id="A", latitude=-15.0, longitude=-47.9)
    cerrado = gleba_base(id="B", bioma=Bioma.CERRADO, latitude=-15.02, longitude=-47.92)
    premissas = PremissasCarbono(raio_cluster_km=50.0)
    avaliadas = {g.id: avaliar_gleba(g, premissas) for g in (mata, cerrado)}
    clusters = clusterizar([mata, cerrado], avaliadas, premissas)
    assert len(clusters) == 2


def test_escala_minima_marca_subescala():
    pequena = gleba_base(area_total_ha=100.0)
    premissas = PremissasCarbono(area_minima_cluster_ha=500.0)
    avaliadas = {pequena.id: avaliar_gleba(pequena, premissas)}
    cluster = clusterizar([pequena], avaliadas, premissas)[0]
    assert cluster.escala == "subescala"
    assert cluster.gap_escala_ha == 400.0


# ---------------------------------------------------------------------------
# Análise consolidada
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def resultado_exemplo():
    with open(EXEMPLO, "r", encoding="utf-8") as f:
        return analisar_land_bank(LandBank(**json.load(f)))


def test_exemplo_carrega_e_analisa(resultado_exemplo):
    r = resultado_exemplo
    assert r.total_glebas == 9
    assert r.area_elegivel_ha > 0
    assert r.vcus_liquidos > 0
    assert r.clusters


def test_areas_sempre_fecham_com_o_total(resultado_exemplo):
    """Nenhum hectare pode sumir nem ser contado duas vezes."""
    for g in resultado_exemplo.glebas:
        soma = g.area_elegivel_ha + g.area_condicionada_ha + g.area_inelegivel_ha
        assert soma == pytest.approx(g.area_total_ha, rel=1e-6)


def test_area_contratada_nunca_excede_a_elegivel(resultado_exemplo):
    assert resultado_exemplo.area_contratada_ha <= resultado_exemplo.area_elegivel_ha
    for c in resultado_exemplo.clusters:
        assert c.area_contratada_ha <= c.area_elegivel_ha


def test_fluxo_de_caixa_comeca_negativo(resultado_exemplo):
    """O CAPEX sai antes de qualquer crédito ser emitido."""
    for c in resultado_exemplo.clusters:
        assert c.fluxo[0].ano == 0
        assert c.fluxo[0].fluxo_liquido_brl < 0
        assert c.fluxo[0].vcus_emitidos == 0


def test_primeira_emissao_respeita_a_verificacao(resultado_exemplo):
    ano_previsto = resultado_exemplo.premissas["ano_primeira_emissao"]
    for c in resultado_exemplo.clusters:
        emissoes = [f.ano for f in c.fluxo if f.vcus_emitidos > 0]
        assert emissoes
        assert min(emissoes) >= ano_previsto


def test_creditos_do_cluster_batem_com_os_do_fluxo(resultado_exemplo):
    for c in resultado_exemplo.clusters:
        assert sum(f.vcus_emitidos for f in c.fluxo) == pytest.approx(c.vcus_liquidos, rel=1e-3)


def test_prioridades_ignoram_area_ja_contratada(resultado_exemplo):
    ids = {p.gleba_id for p in resultado_exemplo.prioridades}
    contratadas = {
        g.gleba_id
        for g in resultado_exemplo.glebas
        if g.status_dominial in (StatusDominial.PROPRIO, StatusDominial.CONTRATADO)
    }
    assert not ids & contratadas


def test_prioridades_ignoram_glebas_bloqueadas(resultado_exemplo):
    bloqueadas = {g.gleba_id for g in resultado_exemplo.glebas if g.bloqueios}
    assert not {p.gleba_id for p in resultado_exemplo.prioridades} & bloqueadas


def test_cenarios_ordenam_por_agressividade(resultado_exemplo):
    por_nome = {c.nome: c for c in resultado_exemplo.cenarios}
    assert por_nome["conservador"].vpl_brl < por_nome["base"].vpl_brl
    assert por_nome["base"].vpl_brl < por_nome["otimista"].vpl_brl


def test_preco_de_equilibrio_zera_o_vpl(resultado_exemplo):
    """No preço de equilíbrio o cluster deixa de destruir valor."""
    for c in resultado_exemplo.clusters:
        if c.preco_equilibrio_brl is None:
            continue
        modelado = resultado_exemplo.premissas["preco_tco2e_remocao_brl"]
        if c.vpl_brl < 0:
            assert c.preco_equilibrio_brl > modelado
        else:
            assert c.preco_equilibrio_brl <= modelado


def test_prevenda_reduz_a_pressao_de_caixa():
    """Adiantamento do offtaker melhora o VPL, mesmo com deságio."""
    with open(EXEMPLO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    sem_prevenda = analisar_land_bank(LandBank(**dados))
    dados["premissas"]["percentual_prevenda"] = 0.60
    com_prevenda = analisar_land_bank(LandBank(**dados))

    assert com_prevenda.vpl_total_brl > sem_prevenda.vpl_total_brl
    assert com_prevenda.vcus_liquidos == pytest.approx(sem_prevenda.vcus_liquidos, rel=1e-6)


def test_split_liquido_favorece_quem_banca_o_capex():
    """Repartir sobre receita líquida protege quem paga a restauração."""
    with open(EXEMPLO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    dados["premissas"]["base_reparticao"] = "liquida"
    liquida = analisar_land_bank(LandBank(**dados))
    dados["premissas"]["base_reparticao"] = "bruta"
    bruta = analisar_land_bank(LandBank(**dados))

    assert liquida.vpl_total_brl > bruta.vpl_total_brl


def test_agregar_area_dilui_custo_fixo():
    """A tese do Land Bank: mais área no mesmo cluster derruba o custo por crédito."""
    premissas = PremissasCarbono()
    sozinha = LandBank(nome="uma", glebas=[gleba_base(id="A")], premissas=premissas)
    agregada = LandBank(
        nome="tres",
        glebas=[
            gleba_base(id="A"),
            gleba_base(id="B", latitude=-28.05, longitude=-49.65),
            gleba_base(id="C", latitude=-28.10, longitude=-49.70),
        ],
        premissas=premissas,
    )

    r1 = analisar_land_bank(sozinha)
    r3 = analisar_land_bank(agregada)

    assert len(r3.clusters) == 1
    assert r3.clusters[0].custo_por_vcu_brl < r1.clusters[0].custo_por_vcu_brl


def test_meta_do_portfolio_e_calculada():
    lb = LandBank(nome="meta", glebas=[gleba_base()], meta_tco2e=10_000.0)
    r = analisar_land_bank(lb)
    assert r.atingimento_meta == pytest.approx(r.vcus_liquidos / 10_000.0, rel=1e-6)


def test_portfolio_vazio_nao_quebra():
    r = analisar_land_bank(LandBank(nome="vazio", glebas=[]))
    assert r.total_glebas == 0
    assert r.clusters == []
    assert r.vcus_liquidos == 0


def test_relatorio_markdown_completo(resultado_exemplo):
    md = gerar_relatorio_land_bank(resultado_exemplo)
    assert "# Land Bank" in md
    assert "Sumário Executivo" in md
    assert "Clusters de Carbono" in md
    assert "Alavancas de Viabilidade" in md
    assert "Fila de Agregação" in md
    assert "Premissas do Modelo" in md
    for c in resultado_exemplo.clusters:
        assert c.id in md


def test_agente_roda_sem_chave_de_api():
    """A camada determinística não pode depender de credencial de LLM."""
    from src.agents.land_bank_agent import LandBankAgent

    with open(EXEMPLO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    agent = LandBankAgent()
    resultado, relatorio = agent.analisar(dados)
    assert resultado.vcus_liquidos > 0
    assert "Land Bank" in relatorio


def test_agente_rejeita_dados_invalidos():
    from src.agents.land_bank_agent import LandBankAgent

    with pytest.raises(ValueError, match="glebas"):
        LandBankAgent().carregar({"nome_projeto": "sem glebas"})


def test_instrumento_recomendado_para_floresta_em_pe():
    """Floresta conservada não se compra, se trava o direito ao crédito."""
    from src.modules.carbon_engine import _instrumento_recomendado

    gleba = gleba_base(
        status_dominial=StatusDominial.PROSPECCAO,
        uso_solo_predominante=UsoSolo.FLORESTA_CONSERVADA,
        distancia_hub_km=80.0,
    )
    avaliada = avaliar_gleba(gleba, PremissasCarbono())
    assert _instrumento_recomendado(gleba, avaliada) == Instrumento.CESSAO_DIREITOS_CARBONO
