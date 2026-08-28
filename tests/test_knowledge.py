"""
Testes do Zion Knowledge Engine™.
"""

import pytest

from src.knowledge import auditar, construir_base, relatorio_auditoria
from src.knowledge.base import SEQUENCIA_PILARES
from src.knowledge.models import Pilar, Proveniencia, Status


@pytest.fixture(scope="module")
def kb():
    return construir_base()


def test_base_registra_todos_os_bancos(kb):
    resumo = kb.resumo()
    for banco in ("conceitos", "ferramentas", "entregaveis", "decisoes", "erros", "perguntas"):
        assert resumo[banco] > 0


def test_todo_item_tem_fonte(kb):
    """Nada entra na base sem origem declarada."""
    for banco in ("conceitos", "ferramentas", "entregaveis", "perguntas", "erros",
                  "decisoes", "cases", "numeros"):
        for item in getattr(kb, banco).values():
            assert item.fonte is not None
            assert item.fonte.documento


def test_ferramenta_sem_definicao_fica_pendente(kb):
    """Nome preservado, conteúdo não inventado."""
    for fid in ("FE_IPM_Z", "FE_DNA_TERRITORIO", "FE_LAUNCH_SYSTEM"):
        ferramenta = kb.ferramentas[fid]
        assert ferramenta.status == Status.PENDENTE_DE_FONTE
        assert ferramenta.nome
        assert not ferramenta.processo, "Ferramenta sem fonte não pode ter processo descrito"
        assert not ferramenta.saida, "Ferramenta sem fonte não pode ter saída descrita"


def test_inferencia_nao_se_passa_por_metodologia(kb):
    """Conclusão estratégica é marcada como inferência, não como método Zion."""
    conceito = kb.conceitos["C_DESCASAMENTO_CAIXA"]
    assert conceito.proveniencia == Proveniencia.INFERENCIA
    assert "INFERÊNCIA" in (conceito.observacoes or "")


def test_numeros_sem_periodo_ficam_marcados(kb):
    """Número sem período não pode ser citado como fato."""
    for numero in kb.numeros.values():
        if numero.periodo.startswith("Período não informado"):
            assert numero.status == Status.PENDENTE_VALIDACAO


def test_citacao_de_numero_traz_fonte_e_periodo(kb):
    citacao = kb.numeros["N_ADR_URUBICI"].citacao()
    assert "Segundo" in citacao
    assert "Período não informado na fonte" in citacao


def test_divergencias_registradas_e_nao_resolvidas(kb):
    """Conflito entre fontes é registrado, nunca decidido em silêncio."""
    assert len(kb.divergencias) >= 3
    for d in kb.divergencias.values():
        assert d.resolucao is None
        assert d.versao_a and d.versao_b
        assert d.impacto


def test_divergencia_de_ordem_esta_documentada(kb):
    d = kb.divergencias["D_ORDEM_PRODUTO_INVESTIMENTO"]
    assert "Pirâmide Invertida" in d.versao_a
    assert "Zion 360" in d.versao_b


def test_lacunas_apontam_fontes_ausentes(kb):
    assert "L_LIVROS" in kb.lacunas
    assert kb.lacunas["L_LIVROS"].bloqueia


def test_fontes_de_livro_nao_estao_disponiveis(kb):
    """A base não pode fingir que tem os livros carregados."""
    from src.knowledge.seed import F_LIVROS, F_LIVRO_MAE
    assert not F_LIVROS.disponivel_no_sistema
    assert not F_LIVRO_MAE.disponivel_no_sistema


def test_sequencia_de_pilares_e_navegavel(kb):
    assert kb.pilar_anterior(Pilar.TERRITORIO) is None
    assert kb.pilar_seguinte(Pilar.TERRITORIO) == Pilar.MERCADO
    assert kb.pilar_seguinte(Pilar.LANCAMENTO) is None
    assert kb.pilar_anterior(Pilar.LANCAMENTO) == Pilar.IMPLANTACAO


def test_cadeia_conecta_conceito_a_decisao(kb):
    cadeia = kb.cadeia("C_TERRITORIO_PRIMEIRO")
    assert cadeia["pilar"] == Pilar.TERRITORIO
    assert cadeia["pilar_seguinte"] == Pilar.MERCADO
    assert any(f.id == "FE_ZION_SCORE" for f in cadeia["ferramentas"])
    assert cadeia["pergunta_do_pilar"]


def test_cadeia_de_conceito_inexistente_falha_claramente(kb):
    with pytest.raises(KeyError):
        kb.cadeia("C_NAO_EXISTE")


def test_busca_encontra_por_nome(kb):
    achados = kb.buscar("Zion Score")
    assert "ferramentas" in achados


def test_decisoes_formam_cadeia_ordenada(kb):
    assert kb.decisoes["D01"].decisao_anterior is None
    assert kb.decisoes["D01"].decisao_seguinte == "D02"
    assert kb.decisoes["D10"].decisao_seguinte is None


def test_matriz_expoe_lacunas(kb):
    matriz = kb.matriz_conhecimento_decisao()
    assert len(matriz) == len(SEQUENCIA_PILARES)
    incompletas = [l for l in matriz if l["completa"] == "não"]
    assert incompletas, "A matriz precisa expor os pilares sem instrumentação"


def test_auditoria_encontra_bloqueantes(kb):
    resultado = auditar(kb)
    codigos = {a.codigo for a in resultado.achados}
    assert "AUD_DIVERGENCIA" in codigos
    assert "AUD_FERRAMENTA_SEM_FONTE" in codigos
    assert "AUD_LACUNAS" in codigos
    assert resultado.bloqueantes


def test_auditoria_sinaliza_ausencia_de_prova(kb):
    """Sem case documentado, nenhuma prova pode ser afirmada."""
    resultado = auditar(kb)
    assert any(a.codigo == "AUD_SEM_CASE" for a in resultado.achados)


def test_auditoria_ordena_por_gravidade(kb):
    achados = auditar(kb).achados
    gravidades = [a.gravidade for a in achados]
    ordem = {"bloqueante": 0, "alta": 1, "media": 2}
    assert gravidades == sorted(gravidades, key=lambda g: ordem[g])


def test_relatorio_de_auditoria_e_completo(kb):
    texto = relatorio_auditoria(auditar(kb))
    assert "Auditoria do Método Zion" in texto
    assert "Matriz Conhecimento → Decisão" in texto


def test_agente_distingue_fonte_de_conteudo():
    """Fonte disponível não significa conteúdo verificável."""
    from src.agents.knowledge_agent import KnowledgeAgent

    agent = KnowledgeAgent()
    pendente = agent.verificar_fonte("FE_IPM_Z")
    assert pendente["fonte_disponivel"] is True
    assert pendente["conteudo_verificavel"] is False

    documentada = agent.verificar_fonte("FE_ZION_SCORE")
    assert documentada["conteudo_verificavel"] is True


def test_contexto_do_llm_carrega_as_restricoes():
    """O modelo precisa receber as lacunas junto com o conhecimento."""
    from src.agents.knowledge_agent import KnowledgeAgent

    contexto = KnowledgeAgent()._contexto("Zion Score")
    assert "Ferramentas com definição ausente" in contexto
    assert "Divergências não resolvidas" in contexto
    assert "Nenhum case com resultado documentado" in contexto


def test_agente_roda_sem_chave_de_api():
    from src.agents.knowledge_agent import KnowledgeAgent

    saida = KnowledgeAgent().auditar_metodo()
    assert saida["resultado"].total_itens > 0
    assert "Auditoria" in saida["relatorio"]
