"""
Testes dos pilares comerciais da Zion.
"""

import pytest

from src.config.pilares import (
    CADEIA_DE_VALOR,
    ORDEM_PILARES,
    PILARES,
    bloco_pilares_para_prompt,
    listar_pilares,
    obter_pilar,
    pilares_da_etapa,
)


def test_seis_pilares_definidos():
    assert len(PILARES) == 6
    assert set(PILARES) == {
        "PRODUTO",
        "DESENVOLVIMENTO",
        "CAPITAL",
        "CONHECIMENTO",
        "PARCERIA",
        "SUSTENTABILIDADE",
    }


def test_ordem_canonica_cobre_todos_os_pilares():
    assert set(ORDEM_PILARES) == set(PILARES)
    assert len(ORDEM_PILARES) == len(PILARES)
    assert [p.codigo for p in listar_pilares()] == ORDEM_PILARES


def test_todo_pilar_tem_oferta_cliente_e_receita():
    for pilar in listar_pilares():
        assert pilar.oferta
        assert pilar.cliente
        assert pilar.modelo_receita
        assert pilar.ativo_zion
        assert pilar.escopo


def test_etapas_declaradas_sao_validas():
    """Nenhum pilar pode apontar para etapa que não existe."""
    from src.config import ZION_ETAPAS_EXECUTAVEIS

    for pilar in listar_pilares():
        for etapa in pilar.etapas_zion:
            assert etapa in ZION_ETAPAS_EXECUTAVEIS


def test_obter_pilar_ignora_caixa():
    assert obter_pilar("parceria").codigo == "PARCERIA"
    assert obter_pilar("  Capital  ").codigo == "CAPITAL"


def test_obter_pilar_inexistente_lista_os_validos():
    with pytest.raises(KeyError, match="PRODUTO"):
        obter_pilar("MARKETING")


def test_pilares_da_etapa():
    """A etapa 5 é de captação: alimenta o pilar Capital."""
    codigos = [p.codigo for p in pilares_da_etapa(5)]
    assert "CAPITAL" in codigos
    assert "PRODUTO" not in codigos


def test_land_bank_alimenta_sustentabilidade_e_parceria():
    codigos = [p.codigo for p in pilares_da_etapa(7)]
    assert "SUSTENTABILIDADE" in codigos
    assert "PARCERIA" in codigos


def test_bloco_para_prompt_lista_todos_os_pilares():
    bloco = bloco_pilares_para_prompt()
    for pilar in listar_pilares():
        assert pilar.nome in bloco
    for elo in CADEIA_DE_VALOR:
        assert elo in bloco


def test_pilares_entram_no_system_prompt_base():
    """Todo agente precisa saber por qual frente a oportunidade entra."""
    from src.prompts.base import SYSTEM_PROMPT_BASE

    assert "Pilares Comerciais da Zion" in SYSTEM_PROMPT_BASE
    assert "Zion Joint Venture" in SYSTEM_PROMPT_BASE
    assert "Pirâmide Invertida" in SYSTEM_PROMPT_BASE
    assert "## Tom e Estilo" in SYSTEM_PROMPT_BASE


def test_pilares_sao_imutaveis():
    """A estrutura comercial não muda em runtime."""
    with pytest.raises(Exception):
        obter_pilar("PRODUTO").nome = "outro"
