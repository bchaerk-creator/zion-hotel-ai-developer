"""
ZION DESTINATION SCORE™ e ZION LEAD SCORE™.

Dois modelos de 100 pontos, com os pesos definidos pelo Market Intelligence &
Lead Engine. Determinísticos e auditáveis: cada nota devolve as parcelas que a
compuseram, para a decisão comercial poder ser contestada.
"""

import logging
from typing import Dict, List, Optional, Tuple

from src.models.prospect import Modalidade, Prospect

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════ ZION DESTINATION SCORE™

PESOS_DESTINO: Dict[str, int] = {
    "demanda": 20,       # demanda turística medida ou observada
    "premium": 15,       # potencial de hospitalidade premium
    "natureza": 15,      # natureza e paisagem
    "glamping": 15,      # aptidão específica para glamping
    "imobiliario": 10,   # potencial imobiliário (terra disponível e preço)
    "acesso": 10,        # acessibilidade
    "ticket": 10,        # ticket médio potencial
}

# As sete dimensões, como especificadas, somam 95 — não 100. O documento de
# origem declara total 100, mas a lista de pesos fecha em 95. Mantemos os pesos
# verbatim (são a decisão comercial) e normalizamos para 100 na classificação,
# senão a faixa 90+ exigiria 94,7% do máximo real e ficaria inalcançável.
TOTAL_DESTINO_BRUTO = sum(PESOS_DESTINO.values())   # 95

FAIXAS_DESTINO: List[Tuple[int, str]] = [
    (90, "prioridade estratégica"),
    (75, "alta prioridade"),
    (60, "boa oportunidade"),
    (40, "monitoramento"),
    (0, "baixa prioridade"),
]


def normalizar_destino(score_bruto: int) -> float:
    """Converte a soma bruta (máx. 95) para a escala de 100 das faixas."""
    return round(score_bruto / TOTAL_DESTINO_BRUTO * 100, 1)


def classificar_destino(score_bruto: int) -> str:
    """Traduz o Destination Score na faixa de prioridade."""
    normalizado = normalizar_destino(score_bruto)
    for minimo, rotulo in FAIXAS_DESTINO:
        if normalizado >= minimo:
            return rotulo
    return "baixa prioridade"


def validar_notas_destino(notas: Dict[str, int]) -> None:
    """
    Confere que nenhuma dimensão passou do seu teto.

    Erro aqui é silencioso e caro: uma nota estourada inflaria o ranking sem
    ninguém perceber.
    """
    for dimensao, teto in PESOS_DESTINO.items():
        valor = notas.get(dimensao)
        if valor is None:
            raise ValueError(f"dimensão ausente no Destination Score: {dimensao}")
        if not 0 <= valor <= teto:
            raise ValueError(
                f"'{dimensao}' = {valor} fora da faixa 0..{teto}")


# ═════════════════════════════════════════════════════ ZION LEAD SCORE™

PESOS_LEAD: Dict[str, int] = {
    "localizacao": 15,
    "qualidade_ativo": 15,
    "potencial_financeiro": 15,
    "potencial_expansao": 15,
    "adequacao_zion": 20,
    "urgencia_dor": 10,
    "facilidade_contato": 10,
}

FAIXAS_LEAD: List[Tuple[int, str]] = [
    (90, "A+"),
    (75, "A"),
    (60, "B"),
    (40, "C"),
    (0, "D"),
]


def classificar_lead(score: Optional[float]) -> str:
    """Traduz o Lead Score na classificação A+ / A / B / C / D."""
    if score is None:
        return "não pontuado"
    for minimo, rotulo in FAIXAS_LEAD:
        if score >= minimo:
            return rotulo
    return "D"


def _localizacao(p: Prospect, destination_score: Optional[int]) -> Tuple[float, str]:
    """15 pontos. Herda a nota do destino quando ele está mapeado."""
    if destination_score is not None:
        pontos = 15.0 * (destination_score / 100)
        return pontos, f"destino pontua {destination_score}/100"
    if p.territorio.uf:
        return 6.0, f"{p.territorio.uf} fora do mapa de destinos"
    return 0.0, "sem localização"


def _qualidade_ativo(p: Prospect) -> Tuple[float, str]:
    """15 pontos. O que a pessoa tem em mãos."""
    area, unidades = p.territorio.area_ha, p.territorio.unidades

    if area is not None:
        if 3 <= area <= 500:
            return 15.0, f"{area:g} ha na faixa do modelo"
        if area < 3:
            return 5.0, f"{area:g} ha é pequeno para o modelo"
        return 9.0, f"{area:g} ha exige fasear a implantação"

    if unidades is not None:
        if 5 <= unidades <= 40:
            return 15.0, f"{unidades} UHs é porte de hotelaria de experiência"
        if unidades < 5:
            return 6.0, f"{unidades} UHs não sustenta estrutura"
        return 4.0, f"{unidades} UHs foge do boutique"

    return 0.0, "ativo não qualificado"


def _potencial_financeiro(p: Prospect, destination_score: Optional[int]) -> Tuple[float, str]:
    """15 pontos. Proxy: ticket e demanda do destino."""
    if destination_score is None:
        return 5.0, "sem destino mapeado para estimar ticket"
    pontos = 15.0 * (destination_score / 100)
    return pontos, "ticket potencial herdado do destino"


def _potencial_expansao(p: Prospect) -> Tuple[float, str]:
    """15 pontos. Terra sobrando é o que permite crescer sem comprar."""
    area = p.territorio.area_ha
    if area is None:
        return 4.0, "área desconhecida — expansão não avaliável"
    if area >= 20:
        return 15.0, f"{area:g} ha comporta fases futuras"
    if area >= 5:
        return 10.0, f"{area:g} ha comporta expansão limitada"
    return 4.0, f"{area:g} ha praticamente sem folga"


def _adequacao_zion(p: Prospect) -> Tuple[float, str]:
    """20 pontos, o maior peso. O quanto o caso é do feitio da Zion."""
    if p.modalidade == Modalidade.DEVELOPMENT:
        return 20.0, "terreno a desenvolver — núcleo do método"
    if p.modalidade == Modalidade.COLLECTION:
        return 17.0, "operação para bandeira"
    if p.modalidade == Modalidade.MANAGEMENT:
        return 14.0, "operação para gestão"
    return 6.0, "modalidade indefinida"


def _urgencia_dor(p: Prospect) -> Tuple[float, str]:
    """
    10 pontos. Dor declarada é o que separa interesse de compra.

    Só pontua quando alguém registrou a dor na ficha: inferir urgência de
    dado coletado seria inventar.
    """
    if p.notas and p.notas.strip():
        return 10.0, "dor ou contexto registrado na ficha"
    return 0.0, "nenhuma dor identificada ainda"


def _facilidade_contato(p: Prospect) -> Tuple[float, str]:
    """10 pontos."""
    canais = sum(bool(c) for c in (p.email, p.telefone, p.instagram, p.site))
    if not canais:
        return 0.0, "sem canal de contato"
    return min(canais * 3.0, 10.0), f"{canais} canal(is) comercial(is)"


def pontuar_lead(
    p: Prospect,
    destination_score: Optional[int] = None,
) -> Prospect:
    """
    Aplica o ZION LEAD SCORE™ (0–100) e registra as parcelas em
    `score_motivos`. Grava em `score`.

    `destination_score` é a nota do destino onde o lead está; quando informada,
    puxa localização e potencial financeiro.
    """
    if p.nao_contatar:
        p.score = 0.0
        p.score_motivos = ["titular pediu para não ser contatado"]
        return p

    parcelas = [
        ("localizacao", *_localizacao(p, destination_score)),
        ("qualidade_ativo", *_qualidade_ativo(p)),
        ("potencial_financeiro", *_potencial_financeiro(p, destination_score)),
        ("potencial_expansao", *_potencial_expansao(p)),
        ("adequacao_zion", *_adequacao_zion(p)),
        ("urgencia_dor", *_urgencia_dor(p)),
        ("facilidade_contato", *_facilidade_contato(p)),
    ]

    total = 0.0
    motivos: List[str] = []
    for dimensao, pontos, razao in parcelas:
        teto = PESOS_LEAD[dimensao]
        pontos = min(pontos, teto)
        total += pontos
        motivos.append(f"{dimensao} {pontos:.0f}/{teto} — {razao}")

    p.score = round(min(total, 100.0), 1)
    p.score_motivos = motivos
    return p


def produto_recomendado(p: Prospect) -> str:
    """
    Sugere qual produto Zion abre a conversa com este lead.

    É o primeiro passo, não o contrato: quem tem terra e nada mais entra por
    diagnóstico, não por desenvolvimento.
    """
    if p.modalidade == Modalidade.DEVELOPMENT:
        area = p.territorio.area_ha or 0
        if area >= 20:
            return "diagnóstico territorial → viabilidade"
        return "bubble glamping (entrada turnkey)"
    if p.modalidade == Modalidade.COLLECTION:
        return "bandeira e reposicionamento"
    if p.modalidade == Modalidade.MANAGEMENT:
        return "reposicionamento e gestão"
    return "diagnóstico territorial"
