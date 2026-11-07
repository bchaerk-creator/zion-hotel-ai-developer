"""Configuração e exemplo fictício da Ferramenta 14 (Quadro de Ocorrências e Manutenção).
Lógica inspirada no Manual Técnico e Manutenção da Zion (Notion): ronda diária e nenhum problema sem responsável.
Prazos por prioridade são sugestão inicial editável, não norma."""
PRIORIDADES = [("Urgente", 0), ("Alta", 2), ("Média", 7), ("Baixa", 30)]   # dias até o prazo (editável)
SIMNAO = ["Sim", "Não"]
EX_UNIDADES = ["Cabana 1", "Cabana 2", "Cabana 3", "Suíte Jardim"]
EX_RESP = ["Carlos (fictício)", "Ana (fictícia)", "Fornecedor do ar (fictício)"]
EX_REF = "2026-11-07"
# (aberta, unidade, local, o que aconteceu, prioridade, responsável, prazo manual, bloqueia, evidência, resolvida, como, custo)
EX_OC = [
    ("2026-11-01", "Cabana 1", "Chuveiro", "Água morna depois de 3 minutos", "Alta", "Carlos (fictício)", None, "Sim", "Foto do aquecedor", "2026-11-02", "Troca da resistência", 85),
    ("2026-11-04", "Cabana 2", "Ar-condicionado", "Liga, mas não gela", "Alta", "Fornecedor do ar (fictício)", None, "Não", "Vídeo no grupo", None, None, None),
    ("2026-11-05", "Suíte Jardim", "Fechadura eletrônica", "Senha não abre na primeira tentativa", "Urgente", "Carlos (fictício)", None, "Sim", None, None, None, None),
    ("2026-11-06", "Cabana 3", "Deck", "Tábua solta perto da escada", "Média", "Carlos (fictício)", None, "Não", "Foto", None, None, None),
    ("2026-11-06", "Cabana 1", "Abajur", "Lâmpada queimada", "Baixa", "Ana (fictícia)", "2026-11-10", "Não", None, "2026-11-06", None, 12),
    ("2026-11-07", "Cabana 2", "Banheiro", "Torneira da pia pingando", "Média", None, None, "Não", None, None, None, None),
]
