"""Fonte única das listas e do exemplo fictício da Ferramenta 10 (Fechamento Mensal por Imóvel)."""
TODOS = "Todos (dividir igual)"
TIPOS = ["Receita", "Despesa"]
CANAIS = ["Airbnb", "Booking", "Reserva direta", "Outro canal"]
CATEGORIAS = ["Limpeza", "Lavanderia", "Energia", "Água", "Internet", "Condomínio e IPTU", "Manutenção", "Insumos e amenities",
              "Gestão e comissões", "Outras despesas"]
SIM_NAO = ["Sim", "Não"]
EX_MES = "2026-10-01"
EX_IMOVEIS = ["Apto Centro (fictício)", "Casa da Serra (fictícia)", "Chalé do Lago (fictício)"]
A, C, L = EX_IMOVEIS
# (data, imóvel, tipo, categoria ou canal, descrição, valor, conferido no extrato)
EX_LANC = [
    ("2026-09-28", A, "Receita", "Airbnb", "Reserva de setembro", 1850, "Sim"),
    ("2026-09-30", A, "Despesa", "Limpeza", "Faxina de saída", 240, "Sim"),
    ("2026-10-02", A, "Receita", "Airbnb", "Repasse da plataforma", 2100, "Sim"),
    ("2026-10-05", A, "Receita", "Reserva direta", "Pix do hóspede", 900, "Sim"),
    ("2026-10-06", C, "Receita", "Booking", "Repasse da plataforma", 3200, "Sim"),
    ("2026-10-08", L, "Receita", "Airbnb", "Repasse da plataforma", 1400, "Não"),
    ("2026-10-10", A, "Despesa", "Limpeza", "Faxinas do mês", 360, "Sim"),
    ("2026-10-10", C, "Despesa", "Limpeza", "Faxinas do mês", 480, "Sim"),
    ("2026-10-12", TODOS, "Despesa", "Internet", "Plano compartilhado", 300, "Sim"),
    ("2026-10-15", C, "Despesa", "Energia", "Conta de luz", 410, "Sim"),
    ("2026-10-15", A, "Despesa", "Condomínio e IPTU", "Condomínio de outubro", 780, "Sim"),
    ("2026-10-18", L, "Despesa", "Manutenção", "Conserto do aquecedor", 2200, "Sim"),
    ("2026-10-20", C, "Despesa", "Insumos e amenities", "Café, sabonetes e papel", 260, "Não"),
    ("2026-10-22", A, "Despesa", "Jardinagem", "Poda", 150, "Sim"),
    ("2026-10-25", C, "Receita", "Airbnb", "Repasse da plataforma", "mil e duzentos", "Sim"),
    ("2026-10-28", TODOS, "Despesa", "Gestão e comissões", "Ferramenta de gestão", 450, "Sim"),
    ("2026-10-30", L, "Receita", "Booking", "Repasse da plataforma", 980, "Sim"),
]
VALIDAS = ("OK", "A conferir no extrato")
