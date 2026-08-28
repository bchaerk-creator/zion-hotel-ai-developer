"""
Pilares Comerciais da Zion Hotel Group International.

Definição canônica das seis frentes pelas quais a Zion gera receita. Este
módulo é a fonte única da verdade: agentes, prompts, relatórios e materiais
comerciais leem daqui em vez de repetir a estrutura em prosa.

A leitura estratégica dos pilares está em docs/PILARES_COMERCIAIS.md.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class PilarComercial:
    """Uma frente comercial da Zion."""

    codigo: str
    nome: str
    oferta: str
    escopo: List[str]
    cliente: str
    modelo_receita: str
    ativo_zion: str
    etapas_zion: List[int]
    modulo_sistema: Optional[str] = None
    observacoes: Optional[str] = None


PILARES: Dict[str, PilarComercial] = {
    "PRODUTO": PilarComercial(
        codigo="PRODUTO",
        nome="Produto",
        oferta="Venda de bubbles e cabanas.",
        escopo=[
            "Bubbles Zion — unidade habitacional transparente de hospitalidade",
            "Cabanas — unidade habitacional modular de hospitalidade",
            "Especificação técnica, fornecimento e instalação da unidade",
        ],
        cliente="Proprietário de terra, operador e investidor que já tem projeto definido",
        modelo_receita="Venda de unidade — receita por ativo entregue",
        ativo_zion="Produto físico validado em operação própria",
        etapas_zion=[3],
        modulo_sistema="Etapa 3 — Product Designer",
        observacoes=(
            "É o pilar de entrada mais rápido e o único com receita imediata. "
            "Também é a moeda de entrada do pilar Parceria."
        ),
    ),
    "DESENVOLVIMENTO": PilarComercial(
        codigo="DESENVOLVIMENTO",
        nome="Desenvolvimento",
        oferta="Prestação de serviço com o escopo inteiro do desenvolvimento hoteleiro.",
        escopo=[
            "Diagnóstico territorial e Zion Score™",
            "Viabilidade mercadológica e econômico-financeira",
            "Definição de produto, posicionamento e master plan conceitual",
            "Estruturação societária e jurídica do negócio",
            "Coordenação de implantação e governança da tese",
        ],
        cliente="Dono de terreno ou de projeto que quer desenvolver e não sabe como",
        modelo_receita="Fee de serviço por etapa ou por escopo fechado",
        ativo_zion="Método da Pirâmide Invertida© e capacidade de execução ponta a ponta",
        etapas_zion=[0, 1, 2, 3, 4, 6],
        modulo_sistema="Etapas 0 a 4 e 6",
        observacoes="É o pilar que sustenta todos os outros: quem desenvolve, conhece o ativo.",
    ),
    "CAPITAL": PilarComercial(
        codigo="CAPITAL",
        nome="Capital",
        oferta="Estruturação do projeto para apresentar a bancos, linhas de crédito e investidores.",
        escopo=[
            "Modelagem econômico-financeira em formato de análise de crédito",
            "Tese de investimento, teaser e information memorandum",
            "Pitch deck institucional e adequação por perfil de investidor",
            "Estruturação de instrumento: dívida, mútuo conversível, equity",
            "Preparação de dossiê para banco e para linha de crédito",
        ],
        cliente="Projeto estruturado que precisa de capital para sair do papel",
        modelo_receita="Fee de estruturação e comissão de êxito sobre o capital captado",
        ativo_zion="Modelagem que fala a língua de comitê de crédito e de investidor",
        etapas_zion=[2, 4, 5],
        modulo_sistema="Etapas 2, 4 e 5",
        observacoes=(
            "Depende de Desenvolvimento entregue: não se estrutura captação sobre projeto "
            "sem viabilidade lastreada."
        ),
    ),
    "CONHECIMENTO": PilarComercial(
        codigo="CONHECIMENTO",
        nome="Conhecimento",
        oferta="Mentoria para quem quer desenvolver o próprio projeto.",
        escopo=[
            "Formação em land development turístico",
            "Mentoria aplicada ao projeto do próprio aluno",
            "Templates, planilhas e método replicável",
            "Comunidade e esteira educacional",
        ],
        cliente="Desenvolvedor iniciante e proprietário que quer conduzir o próprio projeto",
        modelo_receita="Formação, mentoria e recorrência de comunidade",
        ativo_zion="Método documentado e autoridade construída em operação real",
        etapas_zion=[0, 1, 2, 3, 4, 5],
        modulo_sistema="Transversal a todas as etapas",
        observacoes=(
            "É o pilar de menor ticket e maior alcance. Funciona como topo de funil dos "
            "demais: quem tenta sozinho e trava vira cliente de Desenvolvimento ou Parceria."
        ),
    ),
    "PARCERIA": PilarComercial(
        codigo="PARCERIA",
        nome="Parceria — Zion Joint Venture",
        oferta=(
            "A Zion entra com as bubbles e entra no equity, desenvolvendo o destino "
            "junto com o dono da terra."
        ),
        escopo=[
            "Aporte de unidades (bubbles e cabanas) como capital em espécie",
            "Aporte de método, marca e capacidade de desenvolvimento",
            "Participação societária no destino desenvolvido",
            "Desenvolvimento e operação sob bandeira Zion",
        ],
        cliente="Terrenista com terra de alto potencial e sem capital para desenvolver",
        modelo_receita="Participação no equity do destino e no resultado da operação",
        ativo_zion="Produto, método e marca convertidos em participação societária",
        etapas_zion=[0, 1, 2, 3, 4, 7],
        modulo_sistema="Etapas 0 a 4 e módulo 7 (Land Bank)",
        observacoes=(
            "É o pilar de maior retorno e maior prazo. Converte venda de produto em "
            "posição patrimonial, e é o instrumento natural de expansão territorial."
        ),
    ),
    "SUSTENTABILIDADE": PilarComercial(
        codigo="SUSTENTABILIDADE",
        nome="Sustentabilidade",
        oferta="Selos ambientais, crédito de carbono e projetos fotovoltaicos.",
        escopo=[
            "Certificação e selos ambientais do empreendimento",
            "Originação de crédito de carbono por agregação territorial",
            "Projetos fotovoltaicos e autonomia energética do destino",
        ],
        cliente="Destino em desenvolvimento e portfólio territorial da própria Zion",
        modelo_receita=(
            "Venda de crédito de carbono, redução de custo energético e valorização "
            "do ativo por certificação"
        ),
        ativo_zion="Land Bank agregado e engine de carbono proprietária",
        etapas_zion=[3, 5, 6, 7],
        modulo_sistema="Módulo 7 — Land Bank",
        observacoes=(
            "É o pilar mais novo e o de maturação mais longa: crédito de carbono só entra "
            "em caixa após a primeira verificação. Vale mais, no curto prazo, como "
            "diferencial de captação e de narrativa do que como linha de receita."
        ),
    ),
}

# Ordem canônica de apresentação, do ciclo mais curto para o mais longo.
ORDEM_PILARES: List[str] = [
    "PRODUTO",
    "DESENVOLVIMENTO",
    "CAPITAL",
    "CONHECIMENTO",
    "PARCERIA",
    "SUSTENTABILIDADE",
]

# Como um pilar alimenta o outro. Não são silos: é uma escada.
CADEIA_DE_VALOR: List[str] = [
    "CONHECIMENTO atrai e educa o mercado, gerando demanda qualificada",
    "DESENVOLVIMENTO estrutura o projeto de quem não quer ou não consegue fazer sozinho",
    "CAPITAL viabiliza o projeto estruturado diante de banco e investidor",
    "PRODUTO equipa o destino viabilizado com bubbles e cabanas",
    "PARCERIA converte produto e método em equity quando a terra é boa e falta capital",
    "SUSTENTABILIDADE valoriza o destino e monetiza a terra que não vira edificação",
]


def listar_pilares() -> List[PilarComercial]:
    """Retorna os pilares na ordem canônica."""
    return [PILARES[codigo] for codigo in ORDEM_PILARES]


def obter_pilar(codigo: str) -> PilarComercial:
    """Busca um pilar pelo código, sem depender de caixa."""
    chave = codigo.strip().upper()
    if chave not in PILARES:
        validos = ", ".join(ORDEM_PILARES)
        raise KeyError(f"Pilar '{codigo}' não existe. Válidos: {validos}")
    return PILARES[chave]


def pilares_da_etapa(etapa: int) -> List[PilarComercial]:
    """Quais pilares comerciais são alimentados por uma etapa do método."""
    return [p for p in listar_pilares() if etapa in p.etapas_zion]


def bloco_pilares_para_prompt() -> str:
    """Renderiza os pilares para injeção no system prompt dos agentes."""
    linhas = [
        "## Pilares Comerciais da Zion",
        "",
        "A Zion gera receita por seis frentes. Toda recomendação deve indicar, quando "
        "couber, por qual pilar a oportunidade entra:",
        "",
        "| Pilar | Oferta | Como a Zion ganha |",
        "|---|---|---|",
    ]
    for p in listar_pilares():
        linhas.append(f"| **{p.nome}** | {p.oferta} | {p.modelo_receita} |")

    linhas += ["", "Os pilares formam uma escada, não silos:", ""]
    linhas += [f"- {elo}" for elo in CADEIA_DE_VALOR]
    return "\n".join(linhas)
