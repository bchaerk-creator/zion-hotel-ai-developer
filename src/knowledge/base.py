"""
Grafo de conhecimento do Zion Knowledge Engine™.

Nenhum conhecimento vive isolado. Este módulo guarda os bancos (conceitos,
ferramentas, entregáveis, perguntas, erros, decisões, cases, números) e as
relações entre eles: o que vem antes, o que vem depois, que decisão isso permite.
"""

from typing import Dict, List, Optional

from src.knowledge.models import (
    Case,
    Conceito,
    Decisao,
    Divergencia,
    Entregavel,
    Erro,
    Ferramenta,
    Lacuna,
    Nivel,
    Pergunta,
    Pilar,
    Proveniencia,
    RegistroNumerico,
    Status,
)

# Sequência canônica do Método Zion 360°.
SEQUENCIA_PILARES: List[Pilar] = [
    Pilar.TERRITORIO,
    Pilar.MERCADO,
    Pilar.PRODUTO,
    Pilar.ESTRATEGIA,
    Pilar.INVESTIMENTO,
    Pilar.IMPLANTACAO,
    Pilar.LANCAMENTO,
]

PERGUNTA_DO_PILAR: Dict[Pilar, str] = {
    Pilar.TERRITORIO: "O que este território sustenta?",
    Pilar.MERCADO: "Existe demanda?",
    Pilar.PRODUTO: "O que devemos criar?",
    Pilar.ESTRATEGIA: "Como transformar isso em negócio?",
    Pilar.INVESTIMENTO: "Os números fecham?",
    Pilar.IMPLANTACAO: "Como tirar do papel?",
    Pilar.LANCAMENTO: "Como colocar no mercado?",
    Pilar.TRANSVERSAL: "Atravessa todos os pilares.",
}


class KnowledgeBase:
    """Base de conhecimento com proveniência e rastreabilidade."""

    def __init__(self) -> None:
        self.conceitos: Dict[str, Conceito] = {}
        self.ferramentas: Dict[str, Ferramenta] = {}
        self.entregaveis: Dict[str, Entregavel] = {}
        self.perguntas: Dict[str, Pergunta] = {}
        self.erros: Dict[str, Erro] = {}
        self.decisoes: Dict[str, Decisao] = {}
        self.cases: Dict[str, Case] = {}
        self.numeros: Dict[str, RegistroNumerico] = {}
        self.divergencias: Dict[str, Divergencia] = {}
        self.lacunas: Dict[str, Lacuna] = {}

    # ------------------------------------------------------------------
    # Registro
    # ------------------------------------------------------------------

    def registrar(self, item) -> None:
        """Registra qualquer item no banco correspondente ao seu tipo."""
        destino = {
            Conceito: self.conceitos,
            Ferramenta: self.ferramentas,
            Entregavel: self.entregaveis,
            Pergunta: self.perguntas,
            Erro: self.erros,
            Decisao: self.decisoes,
            Case: self.cases,
            RegistroNumerico: self.numeros,
            Divergencia: self.divergencias,
            Lacuna: self.lacunas,
        }.get(type(item))

        if destino is None:
            raise TypeError(f"Tipo não registrável no Knowledge Engine: {type(item).__name__}")
        destino[item.id] = item

    def registrar_todos(self, itens: List) -> None:
        for item in itens:
            self.registrar(item)

    # ------------------------------------------------------------------
    # Consulta
    # ------------------------------------------------------------------

    def buscar(self, termo: str) -> Dict[str, List]:
        """Busca por nome, id ou definição em todos os bancos."""
        alvo = termo.strip().lower()
        resultado: Dict[str, List] = {}

        for nome_banco, banco in self._bancos().items():
            achados = []
            for item in banco.values():
                textos = [item.id, getattr(item, "nome", ""), getattr(item, "pergunta", "")]
                textos.append(getattr(item, "definicao", "") or "")
                textos.append(getattr(item, "objetivo", "") or "")
                textos.append(getattr(item, "o_que_e", "") or "")
                if any(alvo in (t or "").lower() for t in textos):
                    achados.append(item)
            if achados:
                resultado[nome_banco] = achados
        return resultado

    def por_pilar(self, pilar: Pilar) -> Dict[str, List]:
        """Tudo que existe sob um pilar do Método Zion 360°."""
        resultado: Dict[str, List] = {}
        for nome_banco, banco in self._bancos().items():
            achados = [i for i in banco.values() if getattr(i, "pilar", None) == pilar]
            if achados:
                resultado[nome_banco] = achados
        return resultado

    def por_status(self, status: Status) -> List:
        """Todos os itens em um determinado estado de validação."""
        itens = []
        for banco in self._bancos().values():
            itens.extend(i for i in banco.values() if getattr(i, "status", None) == status)
        return itens

    def por_proveniencia(self, proveniencia: Proveniencia) -> List:
        itens = []
        for banco in self._bancos().values():
            itens.extend(
                i for i in banco.values() if getattr(i, "proveniencia", None) == proveniencia
            )
        return itens

    # ------------------------------------------------------------------
    # Grafo — a regra de conexão
    # ------------------------------------------------------------------

    def pilar_anterior(self, pilar: Pilar) -> Optional[Pilar]:
        if pilar not in SEQUENCIA_PILARES:
            return None
        i = SEQUENCIA_PILARES.index(pilar)
        return SEQUENCIA_PILARES[i - 1] if i > 0 else None

    def pilar_seguinte(self, pilar: Pilar) -> Optional[Pilar]:
        if pilar not in SEQUENCIA_PILARES:
            return None
        i = SEQUENCIA_PILARES.index(pilar)
        return SEQUENCIA_PILARES[i + 1] if i < len(SEQUENCIA_PILARES) - 1 else None

    def cadeia(self, conceito_id: str) -> Dict[str, object]:
        """
        Conceito → pilar → ferramenta → entregável → decisão → próximo pilar.

        É a travessia que impede o conhecimento de virar informação solta.
        """
        conceito = self.conceitos.get(conceito_id)
        if conceito is None:
            raise KeyError(f"Conceito '{conceito_id}' não registrado.")

        ferramentas = [self.ferramentas[f] for f in conceito.ferramentas_relacionadas if f in self.ferramentas]
        entregaveis = [self.entregaveis[e] for e in conceito.entregaveis_relacionados if e in self.entregaveis]
        decisoes = [d for d in self.decisoes.values() if conceito_id in d.conhecimento_necessario]

        return {
            "conceito": conceito,
            "pilar": conceito.pilar,
            "pergunta_do_pilar": PERGUNTA_DO_PILAR.get(conceito.pilar, ""),
            "pilar_anterior": self.pilar_anterior(conceito.pilar),
            "pilar_seguinte": self.pilar_seguinte(conceito.pilar),
            "ferramentas": ferramentas,
            "entregaveis": entregaveis,
            "decisoes": decisoes,
            "perguntas": conceito.perguntas,
            "fonte": conceito.fonte,
        }

    def matriz_conhecimento_decisao(self) -> List[Dict[str, str]]:
        """
        Matriz Conhecimento → Ferramenta → Entregável → Decisão, por pilar.

        Uma linha incompleta é um buraco na metodologia, não um detalhe de
        formatação — por isso as lacunas aparecem explicitamente.
        """
        linhas: List[Dict[str, str]] = []

        for pilar in SEQUENCIA_PILARES:
            ferramentas = [f for f in self.ferramentas.values() if f.pilar == pilar]
            entregaveis = [e for e in self.entregaveis.values() if e.pilar == pilar]
            decisoes = [d for d in self.decisoes.values() if d.pilar == pilar]

            linhas.append({
                "pilar": pilar.value,
                "pergunta": PERGUNTA_DO_PILAR[pilar],
                "ferramenta": ", ".join(f.nome for f in ferramentas) or "— lacuna —",
                "entregavel": ", ".join(e.nome for e in entregaveis) or "— lacuna —",
                "decisao": ", ".join(d.pergunta for d in decisoes) or "— lacuna —",
                "completa": "sim" if (ferramentas and entregaveis and decisoes) else "não",
            })
        return linhas

    # ------------------------------------------------------------------
    # Estatísticas
    # ------------------------------------------------------------------

    def resumo(self) -> Dict[str, int]:
        return {nome: len(banco) for nome, banco in self._bancos().items()}

    def cobertura_por_pilar(self) -> Dict[str, int]:
        contagem = {p.value: 0 for p in SEQUENCIA_PILARES}
        for banco in self._bancos().values():
            for item in banco.values():
                pilar = getattr(item, "pilar", None)
                if pilar in SEQUENCIA_PILARES:
                    contagem[pilar.value] += 1
        return contagem

    def _bancos(self) -> Dict[str, Dict]:
        return {
            "conceitos": self.conceitos,
            "ferramentas": self.ferramentas,
            "entregaveis": self.entregaveis,
            "perguntas": self.perguntas,
            "erros": self.erros,
            "decisoes": self.decisoes,
            "cases": self.cases,
            "numeros": self.numeros,
            "divergencias": self.divergencias,
            "lacunas": self.lacunas,
        }
