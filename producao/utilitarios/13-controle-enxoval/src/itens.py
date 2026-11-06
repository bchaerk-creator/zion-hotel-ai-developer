"""Cadastro-padrão e exemplo fictício da Ferramenta 13 (Controle de Enxoval e Reposição).
Lógica inspirada no Controle de Estoque da Zion (Notion, Manual Gerencial): categorias, mínimo por item,
conferência semanal e compra ao atingir o mínimo. Números do exemplo são fictícios."""

CATEGORIAS = ["Enxoval", "Amenities", "Limpeza", "Outros"]
UNIDADES = ["peça", "jogo", "par", "unid.", "rolo", "pacote", "litro"]
TIPOS = ["Entrada", "Saída"]
MOTIVOS = ["Compra", "Doação ou transferência", "Consumo", "Descarte", "Perda", "Dano", "Outro"]

# (categoria, item, unidade de medida) — entra nas duas versões; o comprador ajusta
PADRAO = [
    ("Enxoval", "Jogo de lençol casal", "jogo"), ("Enxoval", "Jogo de lençol solteiro", "jogo"), ("Enxoval", "Fronha", "peça"),
    ("Enxoval", "Toalha de banho", "peça"), ("Enxoval", "Toalha de rosto", "peça"), ("Enxoval", "Piso de banheiro", "peça"),
    ("Enxoval", "Protetor de colchão", "peça"), ("Enxoval", "Edredom ou cobertor", "peça"), ("Enxoval", "Manta", "peça"),
    ("Amenities", "Sabonete", "unid."), ("Amenities", "Shampoo", "unid."), ("Amenities", "Papel higiênico", "rolo"),
    ("Limpeza", "Saco de lixo", "pacote"),
]

# exemplo fictício: item -> (peças por unidade, unidades que usam, jogos em rotação, mínimo manual, custo unitário)
EX_ITENS = {
    "Jogo de lençol casal": (1, 4, 3, None, 120), "Jogo de lençol solteiro": (None, None, None, None, None),
    "Fronha": (2, 4, 3, None, 18), "Toalha de banho": (2, 4, 3, None, 45), "Toalha de rosto": (2, 4, 3, None, 20),
    "Piso de banheiro": (1, 4, 3, None, 25), "Protetor de colchão": (1, 4, 2, None, 60),
    "Edredom ou cobertor": (1, 4, 2, None, 150), "Manta": (None, None, None, 6, 90),
    "Sabonete": (None, None, None, 20, 2.5), "Shampoo": (None, None, None, 15, 4),
    "Papel higiênico": (None, None, None, 24, 1.8), "Saco de lixo": (None, None, None, 3, 12),
}
# (data ISO, item, tipo, quantidade, motivo, observação)
EX_MOV = [
    ("2026-11-02", "Jogo de lençol casal", "Entrada", 12, "Compra", ""), ("2026-11-02", "Fronha", "Entrada", 28, "Compra", ""),
    ("2026-11-02", "Toalha de banho", "Entrada", 24, "Compra", ""), ("2026-11-02", "Toalha de rosto", "Entrada", 26, "Compra", ""),
    ("2026-11-02", "Piso de banheiro", "Entrada", 12, "Compra", ""), ("2026-11-02", "Protetor de colchão", "Entrada", 10, "Compra", ""),
    ("2026-11-02", "Edredom ou cobertor", "Entrada", 9, "Compra", ""), ("2026-11-02", "Manta", "Entrada", 8, "Compra", ""),
    ("2026-11-02", "Sabonete", "Entrada", 40, "Compra", ""), ("2026-11-02", "Shampoo", "Entrada", 30, "Compra", ""),
    ("2026-11-02", "Papel higiênico", "Entrada", 48, "Compra", ""), ("2026-11-02", "Saco de lixo", "Entrada", 4, "Compra", ""),
    ("2026-11-04", "Jogo de lençol casal", "Saída", 2, "Dano", "Mancha que não saiu na lavagem"),
    ("2026-11-05", "Toalha de banho", "Saída", 3, "Descarte", "Desgaste"),
    ("2026-11-05", "Piso de banheiro", "Saída", 1, "Perda", "Não voltou da lavanderia"),
    ("2026-11-06", "Sabonete", "Saída", 26, "Consumo", ""), ("2026-11-06", "Shampoo", "Saída", 15, "Consumo", ""),
    ("2026-11-06", "Papel higiênico", "Saída", 30, "Consumo", ""),
    ("2026-11-06", "Toalha de praia", "Entrada", 4, "Compra", "Item ainda não cadastrado"),
]
EX_CONTAGEM = {"Toalha de rosto": 22}
